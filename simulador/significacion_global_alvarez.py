"""Significación global del mejor "candidato" en el mapa de exclusión de Alvarez (doc. 20).

Se precalculan las huellas s_v de una cámara tipo Rey en cada posición v. Para cualquier mapa de
residuos r, Δχ²_v = (Σ s_v² − 2 r·s_v)/κ. Se generan mapas nulos con la misma correlación
espacial, dispersión y redondeo que los datos (como en doc. 19) y se cuenta cuántas veces el mínimo
de Δχ² sobre TODAS las posiciones es igual o menor que el observado.

Uso: PYTHONPATH=. python significacion_global_alvarez.py [paso_m] [n_sim]
→ ../resultados/24_exclusion_alvarez.json (clave "significacion_global")
"""
import json
import os
import sys

import numpy as np

import exclusion_alvarez as ea
import reanalisis_alvarez as ra
from piramide import cobertura as cb
from piramide import kefren as kf


def main():
    paso = float(sys.argv[1]) if len(sys.argv) > 1 else 8.0
    n_sim = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    A = ea.Alvarez(kf.ORIGEN_ALVAREZ)
    P = kf.voxeles(paso)
    out = {}
    for nombre, hueco in (("camara_tipo_rey", kf.camara_del_rey), ("cubo_8m", lambda q: cb.cubo(q, 8.0))):
        S = np.array([A.huella(hueco(q))[A.valido] for q in P])          # (n_vox, n_bins)
        S2 = (S ** 2).sum(1)
        r = A.r[A.valido]
        d_obs = (S2 - 2 * S @ r) / A.kappa
        i_min = int(np.argmin(d_obs))
        rng = np.random.default_rng(2026)
        M, _ = ra.cargar()
        v = ~np.isnan(M)
        sk = json.load(open(os.path.join(ra.RAIZ, "resultados", "23_reanalisis_alvarez.json")))[
            "nula_correlada"]["sigma_nucleo_bins"]
        desv = float(np.nanstd(M))
        mins = np.empty(n_sim)
        for k in range(n_sim):
            R = ra.campo_correlado(v, sk, desv, rng)
            rr = R.reshape(-1)[A.valido]
            mins[k] = ((S2 - 2 * S @ rr) / A.kappa).min()
        p = float(np.mean(mins <= d_obs[i_min]))
        from scipy.stats import norm
        out[nombre] = dict(min_dchi2=round(float(d_obs[i_min]), 2), posicion=[round(float(x), 1) for x in P[i_min]],
                           sigma_local=round(float(np.sqrt(max(-d_obs[i_min], 0))), 2),
                           p_global=p, sigma_global=round(float(norm.isf(max(p, 1e-6) / 2)), 2) if p < 1 else 0.0,
                           nulo_percentiles={q: round(float(np.percentile(mins, q)), 2) for q in (5, 50, 95)},
                           n_sim=n_sim, n_posiciones=len(P))
        print(nombre, json.dumps(out[nombre], ensure_ascii=False), flush=True)
    p = os.path.join(ra.RAIZ, "resultados", "24_exclusion_alvarez.json")
    d = json.load(open(p)) if os.path.exists(p) else {}
    d["significacion_global"] = out
    json.dump(d, open(p, "w"), indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
