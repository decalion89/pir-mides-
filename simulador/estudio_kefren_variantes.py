"""Kefrén: variantes (posición de Belzoni, número de muones) y prueba de la pista de Gutowski et al.

Uso: PYTHONPATH=. python estudio_kefren_variantes.py  → ../resultados/22_kefren_variantes.json

La pista se prueba con cámaras del tamaño de la del Rey en un anillo a 30° del cenit sobre el
detector; solo cuentan las posiciones cuya caja queda ENTERA dentro de la pirámide.
"""
import json
import math
import os

import numpy as np
from scipy.ndimage import gaussian_filter

from piramide import cobertura as cb
from piramide import kefren as kf

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = 0.437


def dentro(caja) -> bool:
    h = np.asarray(caja.tam) / 2
    esq = np.array([[a, b, c] for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]) * h + caja.centro
    lim = kf.SEMI * (1 - esq[:, 2] / kf.ALTURA)
    return bool(np.all((np.abs(esq[:, 0]) <= lim) & (np.abs(esq[:, 1]) <= lim) & (esq[:, 2] > 0)
                       & (esq[:, 2] < kf.ALTURA_ACTUAL)))


def alvarez(eventos):
    c = kf.campana_alvarez(100.0)
    cb.preparar(c, [], opacidad_fn=kf.opacidad)
    d = 100 * eventos / kf.eventos_en_cono(c)
    A = cb.preparar(kf.campana_alvarez(d), [], opacidad_fn=kf.opacidad)
    p = A._pre
    p["N0"][p["cos"] < math.cos(math.radians(35))] = 0
    p["N0s"] = gaussian_filter(p["N0"], cb.SIGMA_RES, mode="nearest", truncate=3.0)
    return A


def main():
    out = {}
    for nombre, o in (("nominal", kf.ORIGEN_ALVAREZ.copy()), ("alternativo", kf.ORIGEN_ALTERNATIVO.copy())):
        kf.ORIGEN_ALVAREZ = o
        P = kf.voxeles(6.0)
        en_cono = np.array([kf.fraccion_en_cono(q[None]) for q in P]) > 0
        K = [cb.preparar(c, [], opacidad_fn=kf.opacidad) for c in kf.campanas_propuestas()]
        zk = np.sqrt(np.array([[cb.z_hueco(c, kf.camara_del_rey(q)) ** 2 for c in K] for q in P]).sum(1))
        r = dict(cono=kf.fraccion_en_cono(P), propuesta_cal=float(np.mean(F * zk >= 5)),
                 propuesta_sin_cal=float(np.mean(zk >= 5)), por_eventos={})
        for ev in (7.0e5, 1.0e6):
            A = alvarez(ev)
            za = np.array([cb.z_hueco(A, kf.camara_del_rey(q)) for q in P])
            pista = {}
            for h in (20, 40, 60, 70, 80):
                za_l, zc_l = [], []
                for az in range(0, 360, 10):
                    rr = h / math.cos(math.radians(30))
                    q = o + rr * np.array([0.5 * math.sin(math.radians(az)), 0.5 * math.cos(math.radians(az)),
                                           math.cos(math.radians(30))])
                    caja = kf.camara_del_rey(q)
                    if not dentro(caja):
                        continue
                    za_l.append(F * cb.z_hueco(A, caja))
                    zc_l.append(F * cb.z_hueco(K[0], caja))
                pista[h] = dict(n_dentro=len(za_l), de=36,
                                alvarez=[round(min(za_l), 1), round(max(za_l), 1)] if za_l else None,
                                cenital_min=round(min(zc_l), 1) if zc_l else None)
            r["por_eventos"][f"{ev:.0e}"] = dict(
                alvarez_cal=float(np.mean(F * za >= 5)), alvarez_sin_cal=float(np.mean(za >= 5)),
                cono_5s_cal=float(np.mean(F * za[en_cono] >= 5)), cono_5s_sin_cal=float(np.mean(za[en_cono] >= 5)),
                cono_3s_sin_cal=float(np.mean(za[en_cono] >= 3)), pista_30_grados=pista)
        out[nombre] = r
        print(nombre, json.dumps(r))
    with open(os.path.join(RAIZ, "resultados", "22_kefren_variantes.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
