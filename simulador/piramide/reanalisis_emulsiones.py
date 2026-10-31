"""Reanálisis de las emulsiones de Nagoya (Extended Data Fig. 2, Morishima et al. 2017).

Datos (extraer_datos_emulsiones.py): en cada posición (NE1 en el nicho de la pared este,
NE2 en la esquina suroeste) y en cada corte de tanθy hay dos perfiles en tanθx:
  "galeria" = simulación con − sin estructuras internas (la Gran Galería: posición conocida),
  "vacio"   = datos − simulación con estructuras (el Gran Vacío).
Los valores están en píxeles de la figura, así que cada perfil se compara salvo una escala y
una línea base libres: lo que cuenta es la FORMA y la POSICIÓN de los picos.

Convención de la figura: tanθx positivo hacia el OESTE (NE1, al este, ve la Galería en +0,25).

1. Calibración: se ajusta la posición este-oeste de cada detector para que nuestra Gran
   Galería simulada caiga donde cae la de ScanPyramids.
2. Ajuste: un corredor recto con posición, longitud, sección e inclinación libres se ajusta a
   los perfiles "vacio" en la zona usada por los autores (0 ≤ tanθx ≤ 0,2 en NE1;
   −0,2 ≤ tanθx ≤ 0 en NE2), ampliada ±0,05.
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from . import geometria as g
from . import muones as mu
from .reanalisis import Corredor

RUTA = Path(__file__).resolve().parents[2] / "datos" / "scanpyramids_2017" / "emulsiones_diferencias.csv"
CORTES = [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)]
ZONA = {"NE1": (-0.05, 0.25), "NE2": (-0.25, 0.05)}
ANCHO_BIN = 0.025


def cargar(ruta: Path = RUTA) -> dict:
    """Devuelve {(pos, corte, serie): (tanx, valor, error)} con un punto por bin."""
    filas = list(csv.DictReader(open(ruta)))
    out = {}
    for pos in ("NE1", "NE2"):
        for k, (t0, _) in enumerate(CORTES):
            for serie in ("vacio", "galeria"):
                pts = {}
                for f in filas:
                    if f["posicion"] != pos or float(f["ty_min"]) != t0 or f["serie"] != serie:
                        continue
                    t = float(f["tanx"])
                    j = round((t - 0.0125) / ANCHO_BIN)
                    if abs(t - (0.0125 + ANCHO_BIN * j)) < 0.004:
                        cand = (0.0125 + ANCHO_BIN * j, float(f["valor_px"]), max(float(f["error_px"]), 3.0))
                        # si hay varios candidatos en el bin (la cruz y la curva ajustada que pasa
                        # por encima), la cruz es la que tiene barra de error vertical más larga
                        if j not in pts or float(f["error_px"]) > pts[j][2]:
                            pts[j] = cand
                arr = np.array(sorted(pts.values()))
                out[(pos, k, serie)] = (arr[:, 0], arr[:, 1], arr[:, 2])
    return out


class Emulsiones:
    def __init__(self, x_ne1: float = 13.1, x_ne2: float = 2.8, y_ne1: float = 0.0, y_ne2: float = -1.1,
                 z: float = 21.5, n_pos: int = 2, n_sub: int = 3, n_y: int = 5):
        self.d = cargar()
        self.pos = {"NE1": np.array([x_ne1, y_ne1, z]), "NE2": np.array([x_ne2, y_ne2, z])}
        self.n_pos, self.n_sub, self.n_y = n_pos, n_sub, n_y
        self._prep()

    def _prep(self):
        """Rayos por bin para cada panel; opacidad y flujo de referencia precalculados."""
        ref = g.estructuras_conocidas()
        self.paneles = {}
        offs = np.linspace(-0.3, 0.3, self.n_pos)
        for pos in ("NE1", "NE2"):
            for k, (t0, t1) in enumerate(CORTES):
                tx_all = np.arange(-0.5 + 0.0125, 0.6, ANCHO_BIN)
                grupos = []
                for ox in offs:
                    for oy in offs:
                        o = self.pos[pos] + np.array([ox, oy, 0.0])
                        dirs, idx = [], []
                        for i, t in enumerate(tx_all):
                            for sx in np.linspace(-0.4, 0.4, self.n_sub) * ANCHO_BIN:
                                for ty in np.linspace(t0, t1, self.n_y + 2)[1:-1]:
                                    # convención de la figura: +tanθx = oeste
                                    dirs.append((-(t + sx), ty, 1.0))
                                    idx.append(i)
                        dirs = np.array(dirs)
                        dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
                        X = mu.opacidad(o, dirs, ref)
                        X0 = mu.opacidad(o, dirs, [])
                        I = mu.flujo_integral(mu.energia_minima(X), dirs[:, 2])
                        I0 = mu.flujo_integral(mu.energia_minima(X0), dirs[:, 2])
                        grupos.append((o, dirs, np.array(idx), X, I, I0))
                self.paneles[(pos, k)] = (tx_all, grupos)

    def perfil(self, pos: str, k: int, corredor: Corredor | None):
        """(tanx, diferencia galería simulada, diferencia vacío) por bin, en unidades de flujo."""
        tx_all, grupos = self.paneles[(pos, k)]
        n = tx_all.size
        gal = np.zeros(n)
        vac = np.zeros(n)
        cnt = np.zeros(n)
        if corredor is None:
            cajas = []
        elif isinstance(corredor, (list, tuple)):
            cajas = [c.caja() if hasattr(c, "caja") else c for c in corredor]
        else:
            cajas = [corredor.caja()]
        for o, dirs, idx, X, I, I0 in grupos:
            np.add.at(gal, idx, I - I0)
            np.add.at(cnt, idx, 1)
            if cajas:
                c = cajas[0]
                L = sum(cc.longitud_en_rayos(o, dirs) for cc in cajas)
                m = L > 0
                if np.any(m):
                    Ih = I.copy()
                    Ih[m] = mu.flujo_integral(mu.energia_minima(np.maximum(X[m] + c.delta_densidad * L[m] * 100, 0)),
                                              dirs[m, 2])
                    np.add.at(vac, idx, Ih - I)
        return tx_all, gal / cnt, vac / cnt

    @staticmethod
    def _chi2_forma(t_dat, v_dat, e_dat, t_mod, m_mod, zona=None):
        """χ² de los datos frente a escala·modelo + base (escala ≥ 0), en la zona dada."""
        mi = np.interp(t_dat, t_mod, m_mod)
        sel = np.ones_like(t_dat, bool) if zona is None else (t_dat >= zona[0]) & (t_dat <= zona[1])
        w = 1 / e_dat[sel] ** 2
        A = np.stack([mi[sel], np.ones(sel.sum())], axis=1)
        AtW = A.T * w
        th = np.linalg.solve(AtW @ A + np.eye(2) * 1e-12, AtW @ v_dat[sel])
        if th[0] < 0:
            th = np.array([0.0, np.sum(w * v_dat[sel]) / np.sum(w)])
        r = v_dat[sel] - A @ th
        return float(np.sum(w * r ** 2)), th

    def chi2_galeria(self) -> float:
        tot = 0.0
        for pos in ("NE1", "NE2"):
            for k in range(4):
                t, v, e = self.d[(pos, k, "galeria")]
                tm, gal, _ = self.perfil(pos, k, None)
                tot += self._chi2_forma(t, v, e, tm, gal)[0]
        return tot

    def escalas(self) -> dict:
        """Píxeles por unidad de flujo de cada panel, calibrados con la Gran Galería simulada."""
        if getattr(self, "_esc", None) is None:
            self._esc = {}
            for pos in ("NE1", "NE2"):
                for k in range(4):
                    t, v, e = self.d[(pos, k, "galeria")]
                    tm, gal, _ = self.perfil(pos, k, None)
                    gal = self.emborronar(tm, gal, getattr(self, "sigma_gal", 0.0))
                    self._esc[(pos, k)] = self._chi2_forma(t, v, e, tm, gal)[1][0]
        return self._esc

    @staticmethod
    def emborronar(tm: np.ndarray, perfil: np.ndarray, sigma: float) -> np.ndarray:
        """Convolución gaussiana en tanθx: dispersión múltiple en la roca + resolución."""
        if sigma <= 1e-4:
            return perfil
        d = tm[:, None] - tm[None, :]
        k = np.exp(-0.5 * (d / sigma) ** 2)
        k /= k.sum(axis=1, keepdims=True)
        return k @ perfil

    def chi2_vacio(self, corredor: Corredor, cortes=range(4), escala_libre: bool = False,
                   sigma: float = 0.0, residuo_galeria: bool = False, zona: dict | None = None) -> float:
        """χ² de los perfiles del Vacío. Por defecto la escala de cada panel es la de su Gran
        Galería (se conserva la amplitud) y solo la línea base es libre."""
        tot = 0.0
        esc = self.escalas()
        for pos in ("NE1", "NE2"):
            for k in cortes:
                t, v, e = self.d[(pos, k, "vacio")]
                tm, gal, vac = self.perfil(pos, k, corredor)
                vac = self.emborronar(tm, vac, sigma)
                zn = (zona or ZONA)[pos]
                if escala_libre:
                    tot += self._chi2_forma(t, v, e, tm, vac, zn)[0]
                    continue
                sel = (t >= zn[0]) & (t <= zn[1])
                mod = esc[(pos, k)] * np.interp(t[sel], tm, vac)
                w = 1 / e[sel] ** 2
                if residuo_galeria:
                    # la simulación de ScanPyramids pudo sobre/infraestimar las estructuras
                    # conocidas: se ajusta un residuo ε·(Gran Galería) por panel
                    G = esc[(pos, k)] * np.interp(t[sel], tm, gal)
                    A = np.stack([np.ones(sel.sum()), G], axis=1)
                    AtW = A.T * w
                    th = np.linalg.solve(AtW @ A + np.eye(2) * 1e-9, AtW @ (v[sel] - mod))
                    r = v[sel] - mod - A @ th
                    tot += float(np.sum(w * r ** 2))
                    continue
                base = np.sum(w * (v[sel] - mod)) / np.sum(w)
                tot += float(np.sum(w * (v[sel] - mod - base) ** 2))
        return tot


def calibrar(xs1=np.arange(11.0, 15.01, 0.5), xs2=np.arange(1.0, 4.61, 0.4), **kw) -> tuple[float, float, dict]:
    """Busca las posiciones este-oeste de NE1 y NE2 que mejor reproducen la Gran Galería."""
    tabla = {}
    best1 = best2 = None
    for x1 in xs1:
        e = Emulsiones(x_ne1=x1, x_ne2=2.8, **kw)
        c = sum(e._chi2_forma(*e.d[("NE1", k, "galeria")], *(lambda r: (r[0], r[1]))(e.perfil("NE1", k, None)))[0]
                for k in range(4))
        tabla[("NE1", float(x1))] = c
        if best1 is None or c < best1[0]:
            best1 = (c, float(x1))
    for x2 in xs2:
        e = Emulsiones(x_ne1=13.1, x_ne2=x2, **kw)
        c = sum(e._chi2_forma(*e.d[("NE2", k, "galeria")], *(lambda r: (r[0], r[1]))(e.perfil("NE2", k, None)))[0]
                for k in range(4))
        tabla[("NE2", float(x2))] = c
        if best2 is None or c < best2[0]:
            best2 = (c, float(x2))
    return best1[1], best2[1], tabla
