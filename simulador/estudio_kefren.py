"""Kefrén: ¿cuánto exploró Alvarez de verdad, y cómo terminar su experimento?

Uso: PYTHONPATH=. python estudio_kefren.py [paso_m]
Resultados: ../resultados/21_kefren.json y .npz
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import json
import math
import sys
import time
from multiprocessing import Pool

import numpy as np
from scipy.ndimage import gaussian_filter

from piramide import cobertura as cb
from piramide import kefren as kf

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTOS_ALVAREZ = 7.0e5          # análisis del cono (fig. 13): ~700 000 de "more than a million"
FACTORES = {"calibrado (×0,44, Nagoya)": 0.437, "sin calibrar (×1)": 1.0}
HUECOS = {"cámara tipo Rey": None, "cubo de 8 m": 8.0, "cubo de 5 m": 5.0}
_E = {}


def _hueco(nombre, p):
    s = HUECOS[nombre]
    return kf.camara_del_rey(p) if s is None else cb.cubo(p, s)


def _init():
    c = kf.campana_alvarez(100.0)
    cb.preparar(c, [], opacidad_fn=kf.opacidad)
    dias = 100.0 * EVENTOS_ALVAREZ / kf.eventos_en_cono(c)
    a = kf.campana_alvarez(dias)
    cb.preparar(a, [], opacidad_fn=kf.opacidad)
    p = a._pre                                # análisis restringido al cono de 35°, como Alvarez
    p["N0"][p["cos"] < math.cos(math.radians(35.0))] = 0.0
    p["N0s"] = gaussian_filter(p["N0"], cb.SIGMA_RES, mode="nearest", truncate=3.0)
    K = kf.campanas_propuestas()
    for c in K:
        cb.preparar(c, [], opacidad_fn=kf.opacidad)
    _E.update(A=a, K=K, dias_alvarez=dias)


def _trabajo(P):
    if not _E:
        _init()
    A, K = _E["A"], _E["K"]
    out = {}
    for nombre in HUECOS:
        za = np.array([cb.z_hueco(A, _hueco(nombre, p)) for p in P])
        zk = np.array([[cb.z_hueco(c, _hueco(nombre, p)) for c in K] for p in P])
        out[nombre] = (za, zk)
    return out


def main():
    paso = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
    t0 = time.time()
    _init()
    P = kf.voxeles(paso)
    en_cono = np.array([kf.fraccion_en_cono(p[None]) for p in P]) > 0
    trozos = np.array_split(np.arange(len(P)), 48)
    with Pool(os.cpu_count() or 2) as pool:
        partes = pool.map(_trabajo, [P[t] for t in trozos])
    Za = {n: np.concatenate([q[n][0] for q in partes]) for n in HUECOS}
    Zk = {n: np.vstack([q[n][1] for q in partes]) for n in HUECOS}
    K = _E["K"]
    res = dict(paso_m=paso, n_voxeles=len(P), volumen_m3=float(len(P) * paso ** 3),
               fraccion_cono_35=float(en_cono.mean()), alvarez_publicado=0.19,
               dias_equivalentes_alvarez_modelo=round(_E["dias_alvarez"], 1),
               eventos_alvarez=EVENTOS_ALVAREZ,
               propuesta=dict(area_m2=K[0].area_m2, dias=K[0].dias,
                              puestos=[c.nombre for c in K]),
               resultados={})
    for nombre in HUECOS:
        r = {}
        for fn, f in FACTORES.items():
            za, zk = f * Za[nombre], f * Zk[nombre]
            cen = zk[:, 0]
            todas = np.sqrt((zk ** 2).sum(axis=1))
            r[fn] = dict(
                alvarez_explorado_5s=float(np.mean(za >= 5)),
                alvarez_explorado_3s=float(np.mean(za >= 3)),
                alvarez_fraccion_del_cono_5s=float(np.mean(za[en_cono] >= 5)),
                alvarez_fraccion_del_cono_3s=float(np.mean(za[en_cono] >= 3)),
                cenital_moderna_5s=float(np.mean(cen >= 5)),
                cinco_orientaciones_5s=float(np.mean(todas >= 5)),
                cinco_orientaciones_3s=float(np.mean(todas >= 3)),
                sin_explorar_tras_propuesta_por_altura={
                    f"{a}-{b}": float(np.mean(todas[(P[:, 2] >= a) & (P[:, 2] < b)] < 5))
                    for a, b in ((0, 20), (20, 40), (40, 60), (60, 90), (90, 140))})
        res["resultados"][nombre] = r
        print(nombre, json.dumps(r, ensure_ascii=False))
    z40 = cb.z_hueco(_E["A"], kf.camara_del_rey(kf.ORIGEN_ALVAREZ + np.array([0, 0, 40.0])))
    res["camara_del_rey_40m_sobre_belzoni_Z_modelo"] = round(float(z40), 1)
    res["tiempo_s"] = round(time.time() - t0)
    with open(os.path.join(RAIZ, "resultados", "21_kefren.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)
    np.savez_compressed(os.path.join(RAIZ, "resultados", "21_kefren.npz"), P=P, en_cono=en_cono,
                        **{f"Za_{i}": Za[n] for i, n in enumerate(HUECOS)},
                        **{f"Zk_{i}": Zk[n] for i, n in enumerate(HUECOS)},
                        huecos=np.array(list(HUECOS)), puestos=np.array([c.nombre for c in K]))
    print("tiempo", res["tiempo_s"], "s")


if __name__ == "__main__":
    main()
