"""Significación global del mejor "candidato" en el mapa de exclusión de Alvarez (doc. 20) y prueba
directa de la pista de Gutowski et al. (2017).

- Solo posiciones en que la cámara cabe entera (como en exclusion_alvarez.py).
- Nula: mapas de residuos con la correlación de corto y largo alcance, la dispersión y la media
  observadas tras redondear (reanalisis_alvarez.calibrar_nula).
- σ global con convención de UNA cola (la búsqueda es de déficits de Δχ², es decir, de cámaras).
- Significación local calibrada: distribución nula de Δχ² en la posición del mínimo observado.

Uso: PYTHONPATH=. python significacion_global_alvarez.py [paso_m] [n_sim]
"""
import json
import math
import os
import sys

import numpy as np
from scipy.stats import norm

import exclusion_alvarez as ea
import reanalisis_alvarez as ra
from piramide import cobertura as cb
from piramide import kefren as kf


def main():
    paso = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
    n_sim = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    origen = kf.ORIGEN_ALVAREZ.copy()
    ky, _ = ea.ajustar_ky(origen)
    A = ea.Alvarez(origen, 0, ky)
    P = kf.voxeles(paso)
    M, _ = ra.cargar()
    v = ~np.isnan(M)
    cal = json.load(open(os.path.join(ra.RAIZ, "resultados", "23_reanalisis_alvarez.json")))["nula_correlada"]["calibracion"]
    desv, media = float(np.nanstd(M)), float(np.nanmean(M))
    rng = np.random.default_rng(2026)
    nulos = [ra.campo_correlado(v, cal["sigma_nucleo_bins"], desv * cal["escala"], rng,
                                cal["fraccion_correlada"], media).reshape(-1)[A.valido] for _ in range(n_sim)]
    R = np.array(nulos)                                              # (n_sim, n_bins)
    out = dict(origen=[float(x) for x in origen], ky=ky, n_sim=n_sim)
    for nombre, hueco in (("camara_tipo_rey", kf.camara_del_rey), ("cubo_8m", lambda q: cb.cubo(q, 8.0))):
        Q = np.array([q for q in P if ea.cabe(hueco(q))])
        S = np.array([A.huella(hueco(q))[A.valido] for q in Q])
        S2 = (S ** 2).sum(1)
        r = A.r[A.valido]
        d_obs = (S2 - 2 * S @ r) / A.kappa
        i = int(np.argmin(d_obs))
        D = (S2[None, :] - 2 * R @ S.T) / A.kappa                 # (n_sim, n_pos)
        mins = D.min(1)
        p_glob = float(np.mean(mins <= d_obs[i]))
        p_loc = float(np.mean(D[:, i] <= d_obs[i]))
        out[nombre] = dict(posiciones=len(Q), min_dchi2=round(float(d_obs[i]), 2),
                           posicion=[round(float(x), 1) for x in Q[i]],
                           sigma_local_nominal=round(math.sqrt(max(-d_obs[i], 0)), 2),
                           p_local_calibrado=p_loc, sigma_local_calibrado=round(float(norm.isf(max(p_loc, 1e-6))), 2),
                           p_global=p_glob, sigma_global_una_cola=round(float(norm.isf(max(p_glob, 1e-6))), 2),
                           nulo_mediana_minimo=round(float(np.median(mins)), 2),
                           inflado_varianza_rs=round(float(np.mean(np.var(R @ S.T, axis=0) / (A.kappa * S2))), 2))
        print(nombre, json.dumps(out[nombre], ensure_ascii=False), flush=True)
    # pista de Gutowski et al.: cámara tipo Rey a 30° del cenit, acimut 62–72° (cuatro convenciones)
    pista = {}
    for conv, f in (("desde el norte hacia el este", lambda a: (math.sin(a), math.cos(a))),
                    ("desde el este hacia el norte", lambda a: (math.cos(a), math.sin(a))),
                    ("desde el norte hacia el oeste", lambda a: (-math.sin(a), math.cos(a))),
                    ("desde el este hacia el sur", lambda a: (math.cos(a), -math.sin(a)))):
        filas = {}
        for h in (20, 40, 60, 70):
            ds = []
            for az in (62, 67, 72):
                de, dn = f(math.radians(az))
                q = origen + h * np.array([math.tan(math.radians(30)) * de, math.tan(math.radians(30)) * dn, 1.0])
                c = kf.camara_del_rey(q)
                if ea.cabe(c):
                    ds.append(A.dchi2(c))
            filas[h] = [round(min(ds), 1), round(max(ds), 1)] if ds else None
        pista[conv] = filas
    out["pista_gutowski_dchi2"] = pista
    print(json.dumps(pista, ensure_ascii=False))
    p = os.path.join(ra.RAIZ, "resultados", "24_exclusion_alvarez.json")
    d = json.load(open(p)) if os.path.exists(p) else {}
    d["significacion_global"] = out
    json.dump(d, open(p, "w"), indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
