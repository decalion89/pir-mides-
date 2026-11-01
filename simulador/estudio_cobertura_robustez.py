"""Robustez del mapa de exclusión: posiciones, calibración y sistemáticos.

Uso: PYTHONPATH=. python estudio_cobertura_robustez.py [paso_m]
Resultado: ../resultados/20_cobertura_robustez.json
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import json
import sys
from dataclasses import replace
from multiprocessing import Pool

import numpy as np

from piramide import cobertura as cb

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAMANOS = (8.0, 5.0)
_E = {}


def _preparar(variante, semilla):
    rng = np.random.default_rng(semilla)
    cb.F_SIS = {"sis_1pc": 0.01, "sis_3pc": 0.03}.get(variante, 0.02)
    cb.CENIT_MAX = {"corte_80": 80.0, "corte_85": 85.0}.get(variante, 70.0)
    C = cb.campanas_publicadas()
    if variante == "posiciones":
        C = [replace(c, origen=c.origen + rng.normal(0, 2.0, 3) * np.array([1, 1, 0.5]), _pre={})
             for c in C]
    f = cb.calibrar(C)
    if variante == "sin_calibrar":
        f = dict(nagoya=0.5, cea=0.5)
    ref = cb.referencia_actual()
    for c in C:
        cb.preparar(c, ref)
    _E.update(C=C, f=f)


def _trabajo(args):
    variante, semilla, P = args
    if _E.get("clave") != (variante, semilla):
        _preparar(variante, semilla)
        _E["clave"] = (variante, semilla)
    Z = np.zeros((len(P), len(TAMANOS)))
    for i, p in enumerate(P):
        for j, s in enumerate(TAMANOS):
            z2 = sum((_E["f"][c.familia] * cb.z_hueco(c, cb.cubo(p, s))) ** 2 for c in _E["C"])
            Z[i, j] = np.sqrt(z2)
    return Z


def main():
    paso = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
    P = cb.voxeles(paso)
    P = P[~cb.ocupado_por_conocidas(P, cb.referencia_actual())]
    variantes = [("nominal", 0), ("corte_80", 0), ("corte_85", 0), ("sin_calibrar", 0),
                 ("sis_1pc", 0), ("sis_3pc", 0)] + \
                [("posiciones", s) for s in range(1, 6)]
    trozos = np.array_split(np.arange(len(P)), 16)
    res = {}
    with Pool(os.cpu_count() or 2) as pool:
        for v, s in variantes:
            Z = np.vstack(pool.map(_trabajo, [(v, s, P[t]) for t in trozos]))
            clave = v if v != "posiciones" else f"posiciones_{s}"
            res[clave] = {f"{t:g}": dict(nominal=float(np.mean(Z[:, j] < 5.0)),
                                         optimista=float(np.mean(Z[:, j] < 3.0)),
                                         nominal_0_20=float(np.mean(Z[P[:, 2] < 20, j] < 5.0)),
                                         nominal_20_40=float(np.mean(
                                             Z[(P[:, 2] >= 20) & (P[:, 2] < 40), j] < 5.0)))
                          for j, t in enumerate(TAMANOS)}
            print(clave, res[clave], flush=True)
    out = dict(paso_m=paso, n_voxeles=int(len(P)), sin_explorar=res,
               nota="fracción del volumen libre donde un cubo de ese lado NO se habría detectado")
    with open(os.path.join(RAIZ, "resultados", "20_cobertura_robustez.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
