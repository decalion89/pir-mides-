"""El último hueco: telescopios exteriores para el anillo inferior que no cubren ni la Cámara
Subterránea ni la gravedad (doc. 21). ¿Qué área y qué tiempo harían falta?

Para cada cara se coloca un telescopio a 15 m de la base, a ras de suelo, apuntando al centro
del anillo inexplorado de esa cara (a ~55 m del eje y ~20 m de altura), con |tanθ| ≤ 0,6.
Se prueban áreas de 1, 4 y 16 m² durante un año, y cortes de cenit de 70° y 80°.

Uso: PYTHONPATH=. python estudio_anillo.py → ../resultados/26_anillo.json
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import json
import time
from multiprocessing import Pool

import numpy as np

from piramide import cobertura as cb
from piramide import geometria as g

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AREAS = (1.0, 4.0, 16.0)
DIAS = 365.0
FACTOR = 0.437               # calibración conservadora (Nagoya), como en docs/17
_E = {}


def telescopios(area):
    L = g.SEMILADO
    C = []
    for nom, (dx, dy) in (("norte", (0, 1)), ("sur", (0, -1)), ("este", (1, 0)), ("oeste", (-1, 0))):
        o = np.array([dx * (L + 15), dy * (L + 15), 1.0])
        objetivo = np.array([dx * 55.0, dy * 55.0, 20.0])
        v = objetivo - o
        C.append(cb.Campana(f"exterior {nom}", "nagoya", o, v / np.linalg.norm(v), 0.6, area, DIAS,
                            referencia="propuesta"))
    return C


def _init(cenit):
    cb.CENIT_MAX = cenit
    ref = cb.referencia_actual()
    _E["T"] = {a: [cb.preparar(c, ref) for c in telescopios(a)] for a in AREAS}
    _E["cenit"] = cenit


def _trabajo(args):
    P, cenit = args
    if _E.get("cenit") != cenit:
        _init(cenit)
    out = {}
    for a in AREAS:
        z2 = np.array([[(FACTOR * cb.z_hueco(c, cb.cubo(p, 8.0))) ** 2 for c in _E["T"][a]] for p in P])
        out[a] = np.sqrt(z2.sum(axis=1))
    return out


def main():
    t0 = time.time()
    d = np.load(os.path.join(RAIZ, "resultados", "19_cobertura.npz"))
    gv = np.load(os.path.join(RAIZ, "resultados", "25_gravimetria.npz"))
    P, ocup, Zp, T = d["P"], d["ocupado"], d["Z_publicadas"], list(d["tamanos"])
    K = list(d["candidatas"])
    libre = ~ocup
    zmu = Zp[:, T.index(8.0)]
    zsc = d["Z_candidatas_8"][:, K.index("Cámara Subterránea")]
    zg = gv["Zgrav1_8"] / 3.0
    cubierto = (np.sqrt(zmu ** 2 + zsc ** 2) >= 5) | (zg >= 5)
    hueco = libre & ~cubierto
    idx = np.where(hueco)[0]
    res = dict(volumen_libre=int(libre.sum()), sin_cubrir_antes=float(hueco.sum() / libre.sum()),
               altura_media_hueco=float(P[hueco, 2].mean()),
               radio_medio_hueco=float(np.hypot(P[hueco, 0], P[hueco, 1]).mean()), resultados={})
    for cenit in (70.0, 80.0):
        trozos = np.array_split(idx, 32)
        with Pool(os.cpu_count() or 2) as pool:
            partes = pool.map(_trabajo, [(P[t], cenit) for t in trozos])
        r = {}
        for a in AREAS:
            z = np.concatenate([q[a] for q in partes])
            nuevo = z >= 5
            total = cubierto.copy()
            total[idx[nuevo]] = True
            r[f"{a:g} m2"] = dict(cubre_del_hueco=float(nuevo.mean()),
                                  total_explorado=float(total[libre].mean()),
                                  base_0_20=float(total[libre & (P[:, 2] < 20)].mean()))
        res["resultados"][f"cenit_{cenit:g}"] = r
        print(cenit, json.dumps(r), flush=True)
    res["tiempo_s"] = round(time.time() - t0)
    with open(os.path.join(RAIZ, "resultados", "26_anillo.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
