"""Kefrén: variante de posición de la Cámara de Belzoni y prueba de la pista de Gutowski et al. (2017).

Uso: PYTHONPATH=. python estudio_kefren_variantes.py  → ../resultados/22_kefren_variantes.json
"""
import math, json, numpy as np
from scipy.ndimage import gaussian_filter
from piramide import kefren as kf, cobertura as cb
out = {}
for nombre, o in (("nominal", kf.ORIGEN_ALVAREZ.copy()), ("alternativo", kf.ORIGEN_ALTERNATIVO.copy())):
    kf.ORIGEN_ALVAREZ = o
    c = kf.campana_alvarez(100.0); cb.preparar(c, [], opacidad_fn=kf.opacidad)
    d = 100 * 1e6 / kf.eventos_en_cono(c)
    A = cb.preparar(kf.campana_alvarez(d), [], opacidad_fn=kf.opacidad)
    p = A._pre; p["N0"][p["cos"] < math.cos(math.radians(35))] = 0
    p["N0s"] = gaussian_filter(p["N0"], cb.SIGMA_RES, mode="nearest", truncate=3.0)
    K = [cb.preparar(c, [], opacidad_fn=kf.opacidad) for c in kf.campanas_propuestas()]
    P = kf.voxeles(6.0)
    za = np.array([cb.z_hueco(A, kf.camara_del_rey(q)) for q in P])
    zk = np.sqrt(np.array([[cb.z_hueco(c, kf.camara_del_rey(q)) ** 2 for c in K] for q in P]).sum(1))
    r = dict(cono=kf.fraccion_en_cono(P), alv_cal=float(np.mean(0.437*za >= 5)), alv_raw=float(np.mean(za >= 5)),
             prop_cal=float(np.mean(0.437*zk >= 5)), prop_raw=float(np.mean(zk >= 5)))
    # pista de Gutowski et al.: cámara tipo Rey a 30° del cenit, cualquier acimut, distintas alturas
    pista = {}
    for h in (20, 40, 60, 80, 100):
        zs_a, zs_c = [], []
        for az in range(0, 360, 10):
            rr = h / math.cos(math.radians(30))
            q = o + rr * np.array([math.sin(math.radians(30))*math.sin(math.radians(az)),
                                   math.sin(math.radians(30))*math.cos(math.radians(az)),
                                   math.cos(math.radians(30))])
            caja = kf.camara_del_rey(q)
            zs_a.append(0.437 * cb.z_hueco(A, caja)); zs_c.append(0.437 * cb.z_hueco(K[0], caja))
        pista[h] = dict(alvarez_min=round(min(zs_a),1), alvarez_max=round(max(zs_a),1),
                        cenital_min=round(min(zs_c),1))
    r["pista_30_grados"] = pista
    out[nombre] = r
    print(nombre, json.dumps(r))
json.dump(out, open("../resultados/22_kefren_variantes.json", "w"), indent=1)
