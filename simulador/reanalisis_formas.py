"""¿Qué forma del Gran Vacío reconcilia a KEK y a las emulsiones?

Con un único corredor recto los dos conjuntos de datos son incompatibles (Δχ² ≈ 70, docs/11).
Aquí se ajustan formas compuestas a ambos a la vez y se compara el χ² conjunto con la suma de
los mínimos por separado (≈ 729, errores reescalados con el χ²/ndf de cada conjunto).

    cd simulador && PYTHONPATH=. python reanalisis_formas.py     (~30-40 min)
"""
import json, math, time
import numpy as np
from scipy.optimize import minimize
from piramide import reanalisis as ra, reanalisis_emulsiones as re_

S_E, S_K = 3.9, 1.69
SUMA_SEPARADOS = 78.0 + 1100.6 / 1.69      # mínimos por separado (escalados)
t0 = time.time()
E = re_.Emulsiones(x_ne1=13.0, x_ne2=3.0)
K = {d: ra.Reanalisis(pos_h1=(7.1 + d[0], -1.9 + d[1], 21.5 + d[2])) for d in ((-1.0, 0.0, 0.0), (1.0, 0.6, 0.8))}


def pen(vals, lims):
    return sum(100 * (max(lo - v, 0) + max(v - hi, 0)) ** 2 for v, (lo, hi) in zip(vals, lims))


def recto(v):
    x, y, z, L, h, w, a = v
    return [ra.Corredor(x, y, z, L, h, ancho=w, inclinacion=a)], pen([y, z, L, h, w, a], [(-10, 45), (45, 85), (10, 70), (0.5, 15), (0.8, 8), (-20, 45)])


def dos_tramos(v):
    # tramo horizontal al sur (desde y_s, longitud Lh) y tramo inclinado que sigue hacia el norte
    x, ys, z, Lh, Li, a, h, w = v
    ar = math.radians(a)
    yj = ys + Lh
    c1 = ra.Corredor(x, ys + Lh / 2, z, max(Lh, 1), h, ancho=w)
    c2 = ra.Corredor(x, yj + 0.5 * Li * math.cos(ar), z - 0.5 * Li * math.sin(ar), max(Li, 1), h, ancho=w, inclinacion=a)
    return [c1, c2], pen([ys, z, Lh, Li, a, h, w], [(-15, 40), (45, 85), (2, 50), (2, 50), (-10, 45), (0.5, 15), (0.8, 8)])


def dos_niveles(v):
    # dos corredores horizontales superpuestos con separación vertical dz
    x, y, z, L, h, w, dz, L2 = v
    return ([ra.Corredor(x, y, z, L, h, ancho=w), ra.Corredor(x, y, z - dz, L2, h, ancho=w)],
            pen([y, z, L, h, w, dz, L2], [(-10, 45), (45, 85), (10, 70), (0.5, 12), (0.8, 8), (3, 25), (5, 70)]))


FORMAS = {
    "recto (1 corredor, inclinación libre)": (recto, [(7.3, 15, 60, 36, 3, 3, 15), (7.3, 10, 58, 45, 2.5, 4, 5)]),
    "dos tramos (horizontal + inclinado)": (dos_tramos, [(7.3, 0, 63, 20, 25, 25, 3, 3), (7.3, 3, 62, 15, 30, 15, 2.5, 4)]),
    "dos niveles (corredores superpuestos)": (dos_niveles, [(7.3, 15, 63, 35, 2.5, 3, 10, 30), (7.3, 12, 62, 40, 2, 3.5, 6, 20)]),
}

res = {}
for nombre, (f, inicios) in FORMAS.items():
    best = None
    for kk in K:
        for ini in inicios:
            def obj(v):
                cajas, p = f(v)
                sg = 0.03
                return E.chi2_vacio(cajas, sigma=sg) / S_E + K[kk].chi2(cajas) / S_K + p
            r = minimize(obj, np.array(ini, float), method="Nelder-Mead",
                         options=dict(maxiter=2500, xatol=0.01, fatol=0.01))
            if best is None or r.fun < best[0]:
                best = (float(r.fun), [float(x) for x in r.x], kk)
    cajas, _ = f(np.array(best[1]))
    ce = E.chi2_vacio(cajas, sigma=0.03) / S_E
    ck = K[best[2]].chi2(cajas) / S_K
    res[nombre] = dict(chi2_conjunto=best[0], chi2_emulsiones=ce, chi2_kek=ck, params=best[1], det_kek=best[2],
                       tension=best[0] - SUMA_SEPARADOS, n_parametros=len(best[1]))
    print(f"{nombre:42s} χ² conjunto {best[0]:7.1f}  (emulsiones {ce:6.1f}, KEK {ck:6.1f})  "
          f"tensión {best[0] - SUMA_SEPARADOS:+6.1f}  params {np.round(best[1], 1)}  ({time.time() - t0:.0f} s)", flush=True)

json.dump(dict(suma_minimos_separados=SUMA_SEPARADOS, formas=res),
          open("../resultados/11_formas_conjuntas.json", "w"), ensure_ascii=False, indent=1)
