"""Gravedad + muones: ¿pueden juntos explorar la base de la Gran Pirámide?

Uso: PYTHONPATH=. python estudio_gravimetria.py   (tras estudio_cobertura.py)
Resultados: ../resultados/25_gravimetria.json y .npz
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import json
import time
from multiprocessing import Pool

import numpy as np

from piramide import gravimetria as gr

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUECOS = {"8": (8.0, 8.0, 8.0), "5": (5.0, 5.0, 5.0)}
SIGMAS = (3.0, 6.0)
_E = {}


def _trabajo(P):
    if not _E:
        _E["E"] = gr.estaciones()
    E = _E["E"]
    out = {}
    for h, lados in HUECOS.items():
        tot = np.array([gr.z_gravedad(p, lados, E, 1.0) for p in P])
        grupos = np.array([[gr.z_gravedad(p, lados, {k: v}, 1.0) for k, v in E.items()] for p in P])
        out[h] = (tot, grupos)
    return out


def main():
    t0 = time.time()
    d = np.load(os.path.join(RAIZ, "resultados", "19_cobertura.npz"))
    P, ocup, Zp, T = d["P"], d["ocupado"], d["Z_publicadas"], list(d["tamanos"])
    K = list(d["candidatas"])
    libre = ~ocup
    trozos = np.array_split(np.arange(len(P)), 64)
    with Pool(os.cpu_count() or 2) as pool:
        partes = pool.map(_trabajo, [P[t] for t in trozos])
    E = gr.estaciones()
    nombres = list(E)
    zc = P[:, 2]
    bandas = ((0, 20), (20, 40), (40, 60), (60, 147))
    res = dict(n_estaciones={k: int(len(v)) for k, v in E.items()}, sigmas_ugal=SIGMAS, resultados={})
    npz = {}
    for h in HUECOS:
        G1 = np.concatenate([q[h][0] for q in partes])           # Z con σ = 1 µGal
        Gg = np.vstack([q[h][1] for q in partes])
        jm = T.index(float(h))
        zmu = Zp[:, jm]
        zsc = d[f"Z_candidatas_{h}"][:, K.index("Cámara Subterránea")]
        npz[f"Zgrav1_{h}"] = G1
        r = {}
        for s in SIGMAS:
            zg = G1 / s
            mu_hoy = zmu >= 5
            mu_sc = np.sqrt(zmu ** 2 + zsc ** 2) >= 5
            grav = zg >= 5
            r[f"sigma_{s:g}"] = dict(
                gravedad_sola=float(np.mean(grav[libre])),
                muones_hoy=float(np.mean(mu_hoy[libre])),
                muones_hoy_mas_gravedad=float(np.mean((mu_hoy | grav)[libre])),
                muones_con_camara_subterranea=float(np.mean(mu_sc[libre])),
                todo=float(np.mean((mu_sc | grav)[libre])),
                por_altura={f"{a}-{b}": dict(
                    muones_hoy=float(np.mean(mu_hoy[libre & (zc >= a) & (zc < b)])),
                    gravedad=float(np.mean(grav[libre & (zc >= a) & (zc < b)])),
                    todo=float(np.mean((mu_sc | grav)[libre & (zc >= a) & (zc < b)])))
                    for a, b in bandas},
                por_grupo_de_estaciones={n: float(np.mean((Gg[:, i] / s >= 5)[libre])) for i, n in enumerate(nombres)})
        res["resultados"][h] = r
        print(h, json.dumps(r, ensure_ascii=False), flush=True)
    res["tiempo_s"] = round(time.time() - t0)
    with open(os.path.join(RAIZ, "resultados", "25_gravimetria.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)
    np.savez_compressed(os.path.join(RAIZ, "resultados", "25_gravimetria.npz"), P=P, **npz)


if __name__ == "__main__":
    main()
