"""¿Explica un desajuste entre los datos de KEK y su simulación de normalización la tensión
KEK–emulsiones del Gran Vacío (Δχ² ≈ 78, docs/11)?

Los datos de KEK son cocientes "datos / simulación con estructuras conocidas". Si la simulación
coloca la Gran Galería (y el resto del modelo) desplazada δ respecto al detector real, el cociente
contiene un residuo de la galería: R = I_verdad(p, con vacío) / I_sim(p + δ). Según la ley de la
mitad (docs/30), KEK H1 es el detector más sensible a esto. Aquí δ (este-oeste y vertical) se
deja libre y se repiten los ajustes de KEK sola y conjunto con las emulsiones.

    cd simulador && PYTHONPATH=. python tension_kek_normalizacion.py → ../resultados/39_tension_kek_normalizacion.json
"""
import json
import time

import numpy as np
from scipy.optimize import minimize

from piramide import reanalisis as ra, reanalisis_emulsiones as re_

S_E, S_K = 3.9, 1.69
CHI_E_SOLO = 78.0                       # emulsiones solas (escalado), docs/11
POS = np.array([7.1, -1.9, 21.5])        # H1 nominal
t0 = time.time()
E = re_.Emulsiones(x_ne1=13.0, x_ne2=3.0)


def kek(p, delta):
    """Datos en H1 = POS + p; normalización calculada en POS + p + δ."""
    p = POS + np.asarray(p, float)
    r = ra.Reanalisis(pos_h1=tuple(p))
    if np.any(np.asarray(delta) != 0):
        r.den = ra.Reanalisis(pos_h1=tuple(p + np.asarray(delta, float))).den
    return r


def pen(v):
    lims = [(-10, 45), (45, 85), (10, 70), (0.5, 15), (0.8, 8), (-20, 45)]
    return sum(100 * (max(lo - x, 0) + max(x - hi, 0)) ** 2 for x, (lo, hi) in zip(v[1:], lims))


def corr(v):
    x, y, z, L, h, w, a = v
    return ra.Corredor(x, y, z, L, h, ancho=w, inclinacion=a)


INICIOS = [(7.2, 18.9, 56.8, 40.4, 2.7, 4.1, 16.0), (7.3, 17.0, 62.0, 34.0, 2.5, 3.5, 3.0)]


def ajuste(f):
    best = None
    for ini in INICIOS:
        r = minimize(f, np.array(ini, float), method="Nelder-Mead", options=dict(maxiter=900, xatol=0.01, fatol=0.01))
        if best is None or r.fun < best.fun:
            best = r
    return float(best.fun), [round(float(x), 2) for x in best.x]


def main():
    filas = []
    for px in (0.0, -1.0):
        for dx in np.round(np.arange(-1.5, 1.51, 0.25), 2):
            dz = 0.0
            K = kek((px, 0.0, 0.0), (dx, 0.0, dz))
            sin_vacio = K.chi2_sin_vacio() / S_K
            ck, pk = ajuste(lambda v: K.chi2(corr(v)) / S_K + pen(v))
            cj, pj = ajuste(lambda v: E.chi2_vacio([corr(v)], sigma=0.03) / S_E + K.chi2(corr(v)) / S_K + pen(v))
            ce = E.chi2_vacio([corr(pj)], sigma=0.03) / S_E
            fila = dict(posicion_x=px, delta_x=float(dx), delta_z=dz, chi2_kek_sin_vacio=round(sin_vacio, 1), chi2_kek_solo=round(ck, 1),
                        params_kek_solo=pk, chi2_conjunto=round(cj, 1), chi2_conjunto_emulsiones=round(ce, 1),
                        chi2_conjunto_kek=round(cj - ce, 1), params_conjunto=pj,
                        tension=round(cj - CHI_E_SOLO - ck, 1))
            filas.append(fila)
            print(json.dumps(fila, ensure_ascii=False), f"{time.time() - t0:.0f}s", flush=True)
    i = int(np.argmin([f["chi2_conjunto"] for f in filas]))
    out = dict(chi2_emulsiones_solas=CHI_E_SOLO, posicion_h1_nominal=POS.tolist(), filas=filas,
               mejor_conjunto=filas[i],
               tension_global=round(filas[i]["chi2_conjunto"] - CHI_E_SOLO - min(f["chi2_kek_solo"] for f in filas), 1),
               referencia_sin_desajuste={str(px): [f for f in filas if f["posicion_x"] == px and f["delta_x"] == 0.0][0]
                                         for px in (0.0, -1.0)})
    json.dump(out, open("../resultados/39_tension_kek_normalizacion.json", "w"), ensure_ascii=False, indent=1)
    print("mejor", out["mejor_conjunto"], "tensión global", out["tension_global"])


if __name__ == "__main__":
    main()
