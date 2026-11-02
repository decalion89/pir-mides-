"""Mapa de exclusión de Kefrén a partir de los residuos REALES de Alvarez (1970, fig. 10).

Para cada posición de una cámara hipotética se predice su huella en los bins de 3° × 3° de
Alvarez, en σ: s = (N_con − N_sin)/√N_sin. Si la cámara existiera, los residuos publicados (ajuste
sin cámara) contendrían esa huella. Se compara:

    Δχ² = [Σ (r − s)² − Σ r²] / κ

r son los residuos publicados y κ = var(r) ≈ 1,35 infla los errores por los sistemáticos con
estructura espacial (doc. 19). La cámara queda excluida si Δχ² ≥ 25 (≈ 5σ) o, con criterio
habitual de exclusión, si Δχ² ≥ 3,84 (95 %). Solo se usan los 801 bins de la figura 10.

Normalización: un bin central de 3° × 3° contiene ~1600 muones predichos ("in a typical 3- by
3-degree bin there are 1600 events"). Aceptancia: pila de ~1,8 m de profundidad y 1,8 m de lado,
que se anula hacia 45°, como en la figura 9.

Uso: PYTHONPATH=. python exclusion_alvarez.py [paso_m] → ../resultados/24_exclusion_alvarez.json
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

import reanalisis_alvarez as ra
from piramide import cobertura as cb
from piramide import kefren as kf

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUB = 12                    # subdivisiones por bin de 3° (0,25°)
KX = 1.0                    # aceptancia este-oeste: se anula a 45° (coincide con la fig. 9)
KY = 1.08                   # aceptancia norte-sur ajustada a la fig. 9 (ajustar_ky): se anula a ~43°
CUENTAS_BIN_CENTRAL = 1600.0


class Alvarez:
    def __init__(self, origen, desplazamiento_filas=0, ky=KY):
        self.o = np.asarray(origen, float)
        # rejilla fina UNIFORME EN ÁNGULO (SUB por bin de 3°): sin aliasing al agrupar
        a = np.radians(-45 + (np.arange(30 * SUB) + 0.5) * 3.0 / SUB)
        AX, AY = np.meshgrid(a, a, indexing="xy")                  # x = este, y = norte
        TX, TY = np.tan(AX), np.tan(AY)
        d = np.stack([TX, TY, np.ones_like(TX)], -1)
        nrm = np.linalg.norm(d, axis=-1)
        self.dirs = (d / nrm[..., None]).reshape(-1, 3)
        dA = np.radians(3.0 / SUB) ** 2
        ang = (dA / (np.cos(AX) ** 2 * np.cos(AY) ** 2) / nrm ** 3).reshape(-1)   # dΩ exacto
        X0 = kf.opacidad(self.o, self.dirs)
        F0 = cb.mu.flujo_integral(cb.mu.energia_minima(X0), self.dirs[:, 2])
        acept = (np.clip(1 - KX * np.abs(TX), 0, 1) * np.clip(1 - ky * np.abs(TY), 0, 1)).reshape(-1)
        self.X0 = X0
        self.w0 = F0 * ang * acept * self.dirs[:, 2]
        jj, ii = np.meshgrid(np.arange(30 * SUB) // SUB, np.arange(30 * SUB) // SUB, indexing="xy")
        ii = 29 - ii                                   # fila 0 = norte (θ = 45°)
        ii = ii + desplazamiento_filas
        idx = ii * 30 + jj
        idx[(ii < 0) | (ii > 29)] = 900              # fuera de la matriz: se descarta
        self.idx = idx.reshape(-1)
        N0 = np.bincount(self.idx, weights=self.w0, minlength=901)[:900]
        escala = CUENTAS_BIN_CENTRAL / N0.reshape(30, 30)[14:16, 14:16].mean()
        self.w0 *= escala
        self.N0 = N0 * escala
        r, _ = ra.cargar()
        self.r = r.reshape(-1)
        self.valido = ~np.isnan(self.r)
        self.kappa = float(np.nanvar(r) + np.nanmean(r) ** 2)

    def huella(self, caja) -> np.ndarray:
        L = caja.longitud_en_rayos(self.o, self.dirs)
        m = L > 0
        if not m.any():
            return np.zeros(900)
        X1 = np.maximum(self.X0[m] - kf.DENSIDAD * L[m] * 100.0, 0.0)
        cos = self.dirs[m, 2]
        rat = cb.mu.flujo_integral(cb.mu.energia_minima(X1), cos) / np.maximum(
            cb.mu.flujo_integral(cb.mu.energia_minima(self.X0[m]), cos), 1e-300)
        dN = np.bincount(self.idx[m], weights=self.w0[m] * (rat - 1.0), minlength=901)[:900]
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(self.N0 > 0, dN / np.sqrt(self.N0), 0.0)

    def dchi2(self, caja) -> float:
        s = self.huella(caja)[self.valido]
        r = self.r[self.valido]
        return float((np.sum((r - s) ** 2) - np.sum(r ** 2)) / self.kappa)


# Predicciones de Alvarez (fig. 9) en las dos columnas centrales, filas del borde norte y sur
FIG9_COLUMNA_CENTRAL = {2: 129.5, 3: 423.5, 4: 739.5, 5: 1009.5, 27: 490.0, 28: 322.5, 29: 140.0, 30: 8.5}
FIG9_FILA_16 = {1: 88, 2: 351, 3: 577, 4: 798, 27: 846, 28: 501, 29: 84}


def ajustar_ky(origen=None):
    """Ajusta KY para que la caída norte-sur reproduzca la fig. 9 (filas en numeración 1..30)."""
    mejor = None
    for ky in np.arange(1.0, 1.6, 0.02):
        A = Alvarez(kf.ORIGEN_ALVAREZ if origen is None else origen, 0, ky)
        N = A.N0.reshape(30, 30)
        pred = np.array([N[f - 1, 14:16].mean() for f in FIG9_COLUMNA_CENTRAL])
        obs = np.array(list(FIG9_COLUMNA_CENTRAL.values()))
        m = pred > 0
        e = np.sum((np.log(pred[m] + 5) - np.log(obs[m] + 5)) ** 2) + 10 * (~m).sum()
        if mejor is None or e < mejor[1]:
            mejor = (round(float(ky), 2), float(e))
    return mejor


def cabe(caja) -> bool:
    """La caja entera dentro de la Kefrén actual (sin sobresalir de caras ni vértice)."""
    h = np.asarray(caja.tam) / 2
    esq = np.array([[a, b, c] for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]) * h + caja.centro
    lim = kf.SEMI * (1 - esq[:, 2] / kf.ALTURA)
    return bool(np.all((np.abs(esq[:, 0]) <= lim) & (np.abs(esq[:, 1]) <= lim) & (esq[:, 2] > 0)
                       & (esq[:, 2] < kf.ALTURA_ACTUAL)))


def main():
    paso = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
    t0 = time.time()
    origen0 = kf.ORIGEN_ALVAREZ.copy()
    res = {}
    for nombre, origen, df in (("nominal", origen0, 0), ("fila_-1", origen0, -1),
                               ("fila_+1", origen0, 1), ("alternativo", kf.ORIGEN_ALTERNATIVO, 0)):
        kf.ORIGEN_ALVAREZ = np.asarray(origen, float)
        ky, _ = ajustar_ky(origen)
        A = Alvarez(origen, df, ky)
        P = kf.voxeles(paso)
        en_cono = np.array([kf.fraccion_en_cono(q[None]) for q in P]) > 0
        r = dict(origen=[float(x) for x in origen], ky=ky, kappa=round(A.kappa, 3),
                 cuentas_totales_bins_validos=round(float(A.N0[A.valido].sum())))
        guardar = {}
        for h, f in (("camara_tipo_rey", kf.camara_del_rey), ("cubo_8m", lambda q: cb.cubo(q, 8.0))):
            ok = np.array([cabe(f(q)) for q in P])
            d = np.full(len(P), np.nan)
            d[ok] = [A.dchi2(f(q)) for q in P[ok]]
            dd, cono = d[ok], en_cono[ok]
            i_min = int(np.nanargmin(d))
            r[h] = dict(posiciones_que_caben=int(ok.sum()), de=len(P),
                        excluido_95=float(np.mean(dd >= 3.84)), excluido_5s=float(np.mean(dd >= 25)),
                        dentro_cono_95=float(np.mean(dd[cono] >= 3.84)), dentro_cono_5s=float(np.mean(dd[cono] >= 25)),
                        fuera_cono_95_sobre_total=float(np.mean((dd >= 3.84) & ~cono)),
                        fuera_cono_95_sobre_fuera=float(np.mean(dd[~cono] >= 3.84)),
                        minimo_dchi2=round(float(d[i_min]), 2), donde_minimo=[round(float(x), 1) for x in P[i_min]])
            guardar[h] = d
        res[nombre] = r
        print(nombre, json.dumps(r, ensure_ascii=False), flush=True)
        if nombre == "nominal":
            np.savez_compressed(os.path.join(RAIZ, "resultados", "24_exclusion_alvarez.npz"), P=P,
                                dchi2_rey=guardar["camara_tipo_rey"], dchi2_8m=guardar["cubo_8m"], en_cono=en_cono)
    kf.ORIGEN_ALVAREZ = origen0
    res["tiempo_s"] = round(time.time() - t0)
    res["criterios"] = ("Solo posiciones en que la cámara cabe entera (denominador común). Δχ² ≥ 3,84 = 95 % CL; "
                        "Δχ² ≥ 25: ~5σ nominal (≈ 4,2σ si se tiene en cuenta la correlación de los residuos); "
                        "Δχ² < 0: los datos prefieren la cámara")
    with open(os.path.join(RAIZ, "resultados", "24_exclusion_alvarez.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
