"""Reanálisis independiente de los datos publicados de KEK sobre el Gran Vacío.

Datos: los 679 puntos de la Extended Data Fig. 4 de Morishima et al. (Nature 552, 2017),
extraídos de los vectores del PDF (extraer_datos_kek.py). Son cocientes "datos / simulación con
las estructuras conocidas" en 9 cortes, medidos por dos hodoscopios en la Cámara de la Reina:
H1 (esquina sureste, planos separados 1,5 m) y H2 (2,9 m al oeste, planos separados 1,0 m).
Cada canal de Δx o Δy corresponde a 1 cm entre planos, es decir, tanθ = Δ·0,01/separación.

Modelo: para cada punto se trazan rayos que cubren el área del detector (1,2 x 1,2 m), la
anchura del canal y el corte en Δy; el cociente predicho es Σ I(con vacío) / Σ I(sin vacío).
El vacío es un corredor recto con posición, longitud, sección e INCLINACIÓN libres. En cada
corte se ajustan una normalización y una pendiente (la simulación original de KEK no es la
nuestra) y se añade un 0,5 % de error sistemático en cuadratura.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import geometria as g
from . import muones as mu

RUTA = Path(__file__).resolve().parents[2] / "datos" / "scanpyramids_2017" / "kek_cortes.csv"
SEPARACION = {"H1": 1.5, "H2": 1.0}      # m entre planos (Morishima et al., Métodos)
CANAL = 0.01                             # m, anchura de una barra de centelleador
LADO_DET = 1.2                           # m
SEP_H1_H2 = 2.9                          # m, H2 al oeste de H1
F_SIS = 0.005


def cargar(ruta: Path = RUTA) -> dict[str, np.ndarray]:
    filas = list(csv.DictReader(open(ruta)))
    return dict(det=np.array([f["detector"] for f in filas]),
                dy0=np.array([int(f["dy_min"]) for f in filas]),
                dy1=np.array([int(f["dy_max"]) for f in filas]),
                dx=np.array([float(f["dx"]) for f in filas]),
                val=np.array([float(f["cociente"]) for f in filas]),
                err=np.array([float(f["error"]) for f in filas]))


@dataclass
class Corredor:
    x: float            # centro (m)
    y: float
    z: float
    largo: float
    alto: float
    ancho: float = 1.6
    inclinacion: float = 0.0     # grados; positivo = sube hacia el sur (como la Gran Galería)

    def caja(self) -> g.Caja:
        return g.Caja("Corredor ajustado", (self.x, self.y, self.z), (self.ancho, self.largo, self.alto),
                      inclinacion=self.inclinacion, tipo="ajuste")


class Reanalisis:
    def __init__(self, datos=None, pos_h1=(7.1, -1.9, 21.5), n_pos: int = 3, n_y: int = 6,
                 sub_x=(-0.5, 0.0, 0.5)):
        self.d = cargar() if datos is None else datos
        d = self.d
        n = d["val"].size
        self.cortes = sorted(set(zip(d["det"], d["dy0"])))
        self.id_corte = np.array([self.cortes.index((a, b)) for a, b in zip(d["det"], d["dy0"])])
        offs = np.linspace(-LADO_DET / 2 + 0.2, LADO_DET / 2 - 0.2, n_pos)
        self.grupos = []        # (origen, dirs, índice del punto de cada rayo)
        ref = g.estructuras_conocidas()
        for det in ("H1", "H2"):
            base = np.array(pos_h1, float) - (np.array([SEP_H1_H2, 0, 0]) if det == "H2" else 0)
            D = SEPARACION[det]
            sel = np.where(d["det"] == det)[0]
            for ox in offs:
                for oy in offs:
                    o = base + np.array([ox, oy, 0.0])
                    dirs, idx = [], []
                    for i in sel:
                        for sx in sub_x:
                            tx = (d["dx"][i] + sx) * CANAL / D
                            for ty in np.linspace(d["dy0"][i], d["dy1"][i] + 1, n_y) * CANAL / D:
                                dirs.append((tx, ty, 1.0))
                                idx.append(i)
                    dirs = np.array(dirs)
                    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
                    X = mu.opacidad(o, dirs, ref)
                    I0 = mu.flujo_integral(mu.energia_minima(X), dirs[:, 2])
                    self.grupos.append((o, dirs, np.array(idx), X, I0))
        self.n = n
        self.den = np.zeros(n)
        for _, _, idx, _, I0 in self.grupos:
            np.add.at(self.den, idx, I0)
        tx_pt = np.array([d["dx"][i] * CANAL / SEPARACION[d["det"][i]] for i in range(n)])
        self.tx = tx_pt

    def razon(self, corredor) -> np.ndarray:
        """`corredor` puede ser un Corredor o una lista de Corredor/Caja (formas compuestas)."""
        if isinstance(corredor, (list, tuple)):
            cajas = [c.caja() if hasattr(c, "caja") else c for c in corredor]
        else:
            cajas = [corredor.caja()]
        c = cajas[0]
        num = np.zeros(self.n)
        for o, dirs, idx, X, I0 in self.grupos:
            L = sum(cc.longitud_en_rayos(o, dirs) for cc in cajas)
            m = L > 0
            I = I0.copy()
            if np.any(m):
                Xh = X[m] + c.delta_densidad * L[m] * 100.0
                I[m] = mu.flujo_integral(mu.energia_minima(np.maximum(Xh, 0)), dirs[m, 2])
            np.add.at(num, idx, I)
        return num / self.den

    def chi2(self, corredor: Corredor, devolver_ajuste: bool = False):
        m = self.razon(corredor)
        d = self.d
        var = d["err"] ** 2 + (F_SIS * d["val"]) ** 2
        w = 1 / var
        chi = 0.0
        ajuste = np.empty(self.n)
        for k in range(len(self.cortes)):
            s = self.id_corte == k
            A = np.stack([m[s], m[s] * self.tx[s]], axis=1)
            AtW = A.T * w[s]
            th = np.linalg.solve(AtW @ A + np.diag([1e-6, 1e-6]), AtW @ d["val"][s])
            pred = A @ th
            ajuste[s] = pred
            chi += float(np.sum(w[s] * (d["val"][s] - pred) ** 2))
        return (chi, ajuste) if devolver_ajuste else chi

    def chi2_sin_vacio(self) -> float:
        return self.chi2(Corredor(0, 500, 500, 1, 1))     # caja fuera de la pirámide


def ajustar(r: Reanalisis, inclinacion: float | None = None, inicios=None, libres_seccion=True):
    """Ajusta (x, y, z, largo, alto[, inclinación]). Devuelve (chi2, Corredor)."""
    from scipy.optimize import minimize

    if inicios is None:
        inicios = [(7.3, 17.0, 63.0, 30.0, 8.0), (7.3, 15.0, 58.0, 35.0, 6.0), (6.5, 20.0, 66.0, 25.0, 10.0)]

    def construir(v):
        x, y, z, L, h = v[:5]
        a = inclinacion if inclinacion is not None else v[5]
        return Corredor(x, y, z, max(L, 5.0), max(h, 0.5) if libres_seccion else 8.0, inclinacion=a)

    def f(v):
        return r.chi2(construir(v))

    mejor = None
    for ini in inicios:
        v0 = list(ini) + ([] if inclinacion is not None else [10.0])
        res = minimize(f, np.array(v0, float), method="Nelder-Mead",
                       options=dict(maxiter=500, xatol=0.05, fatol=0.05))
        if mejor is None or res.fun < mejor.fun:
            mejor = res
    return float(mejor.fun), construir(mejor.x)
