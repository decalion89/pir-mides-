"""El anillo inferior desde DEBAJO: detectores en el corredor descendente (en la roca) y en el
pasaje ciego al sur de la Cámara Subterránea, mirando hacia arriba (|tanθ| ≤ 1, 1 m² × 100 d).

Uso: PYTHONPATH=. python estudio_pasajes_bajos.py → ../resultados/27_pasajes_bajos.json
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import json
import math
from multiprocessing import Pool

import numpy as np

from piramide import cobertura as cb
from piramide import geometria as g

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTOR = 0.437
_E = {}


def puestos():
    e = g._puntos_clave()["entrada"]
    cd, sd = math.cos(math.radians(g.ANG_DESC)), math.sin(math.radians(g.ANG_DESC))
    arriba = np.array([0, 0, 1.0])
    P = {}
    for z in (-5.0, -15.0, -25.0):          # corredor descendente, ya dentro de la roca
        t = (e[2] - z) / sd
        o = e + t * np.array([0, -cd, -sd])
        P[f"corredor descendente a {z:.0f} m"] = o
    P["pasaje ciego al sur de la Cámara Subterránea"] = np.array([2.0, -23.0, -28.0])
    return {k: cb.Campana(k, "nagoya", v, arriba, 1.0, 1.0, 100.0, referencia="propuesta") for k, v in P.items()}


def _trabajo(Pv):
    if not _E:
        ref = cb.referencia_actual()
        _E["C"] = {k: cb.preparar(c, ref) for k, c in puestos().items()}
    return {k: np.array([FACTOR * cb.z_hueco(c, cb.cubo(p, 8.0)) for p in Pv]) for k, c in _E["C"].items()}


def main():
    d = np.load(os.path.join(RAIZ, "resultados", "19_cobertura.npz"))
    gv = np.load(os.path.join(RAIZ, "resultados", "25_gravimetria.npz"))
    P, ocup, Zp, T = d["P"], d["ocupado"], d["Z_publicadas"], list(d["tamanos"])
    K = list(d["candidatas"])
    libre = ~ocup
    zmu = Zp[:, T.index(8.0)]
    zsc = d["Z_candidatas_8"][:, K.index("Cámara Subterránea")]
    zg = gv["Zgrav1_8"] / 3.0
    cubierto = (np.sqrt(zmu ** 2 + zsc ** 2) >= 5) | (zg >= 5)
    idx = np.where(libre & ~cubierto)[0]
    with Pool(os.cpu_count() or 2) as pool:
        partes = pool.map(_trabajo, [P[t] for t in np.array_split(idx, 32)])
    nombres = list(partes[0])
    Z = {k: np.concatenate([q[k] for q in partes]) for k in nombres}
    res = dict(sin_cubrir_antes=float(len(idx) / libre.sum()), puestos={})
    z2 = np.zeros(len(idx))
    for k in nombres:
        res["puestos"][k] = dict(origen=[round(float(x), 1) for x in puestos()[k].origen],
                                 cubre_del_hueco=float(np.mean(Z[k] >= 5)))
        z2 += Z[k] ** 2
    nuevo = np.sqrt(z2) >= 5
    total = cubierto.copy()
    total[idx[nuevo]] = True
    res["todos_juntos"] = dict(cubre_del_hueco=float(nuevo.mean()), total_explorado=float(total[libre].mean()),
                               base_0_20=float(total[libre & (P[:, 2] < 20)].mean()),
                               franja_20_40=float(total[libre & (P[:, 2] >= 20) & (P[:, 2] < 40)].mean()))
    # lo que sigue sin cubrir: por cuadrante
    resto = idx[~nuevo]
    q = np.where(np.abs(P[resto, 1]) >= np.abs(P[resto, 0]), np.where(P[resto, 1] > 0, "norte", "sur"),
                 np.where(P[resto, 0] > 0, "este", "oeste"))
    res["resto_por_lado"] = {s: float(np.mean(q == s)) for s in ("norte", "sur", "este", "oeste")}
    print(json.dumps(res, indent=1, ensure_ascii=False))
    with open(os.path.join(RAIZ, "resultados", "27_pasajes_bajos.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
