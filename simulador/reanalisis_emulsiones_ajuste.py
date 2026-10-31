"""Ajuste libre del Gran Vacío solo con las emulsiones de Nagoya (datos digitalizados corregidos).

Guarda los parámetros del mejor ajuste en resultados/18_ajuste_emulsiones.json.

    cd simulador && PYTHONPATH=. python reanalisis_emulsiones_ajuste.py     (~1 min)
"""
import json
import numpy as np
from scipy.optimize import minimize
from piramide import reanalisis_emulsiones as re_
from piramide.reanalisis import Corredor

e = re_.Emulsiones(x_ne1=13.0, x_ne2=3.0)
LIM = [(-10, 45), (45, 85), (10, 60), (1, 15), (0.8, 8), (0, 0.06), (-20, 45)]
NOMBRES = ["x", "y", "z", "largo", "alto", "ancho", "sigma_angular", "inclinacion"]


def f(v):
    x, y, z, L, h, w, sg, a = v
    p = sum(100 * (max(lo - val, 0) + max(val - hi, 0)) ** 2 for val, (lo, hi) in zip(v[1:], LIM))
    return e.chi2_vacio(Corredor(x, y, z, L, h, ancho=w, inclinacion=a), sigma=max(sg, 0)) + p


ajustes = []
for s in [(7.3, 10, 63, 45, 8, 2, 0.033, 5), (7.3, 15, 62, 36, 8, 1.6, 0.03, 0),
          (7.3, 7, 60, 55, 8, 2, 0.035, 10), (7.3, 15, 58, 40, 3, 4, 0.03, 5)]:
    r = minimize(f, np.array(s, float), method="Nelder-Mead", options=dict(maxiter=2500, xatol=0.01, fatol=0.01))
    d = {k: float(v) for k, v in zip(NOMBRES, r.x)}
    d.update(chi2=float(r.fun), seccion_m2=float(r.x[4] * r.x[5]), inicio=list(s))
    ajustes.append(d)
    print(f"χ² {r.fun:.1f}  x {d['x']:.2f}  z {d['z']:.1f}  sección {d['seccion_m2']:.1f} m²  incl {d['inclinacion']:.1f}°")
ajustes.sort(key=lambda d: d["chi2"])
json.dump(dict(nota="Ajustes libres con las emulsiones solas (4 inicios); el primero es el mejor.",
               ajustes=ajustes), open("../resultados/18_ajuste_emulsiones.json", "w"), ensure_ascii=False, indent=1)
