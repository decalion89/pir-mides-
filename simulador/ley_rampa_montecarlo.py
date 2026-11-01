"""¿Es robusta la "ley de la rampa" (doc. 25)? Monte Carlo sobre todos los parámetros inciertos.

Para cada muestra de Parametros (RANGOS triangulares de fisica.py, los mismos de docs/07, que no
se han tocado) y cada técnica de giro, se calcula el techo de ritmo (obreros ilimitados) de los
sistemas de rampas múltiples o híbridos con la geometría de Keops. Se compara con el techo
histórico (85 000–150 000 m³/año; doc. 23) y se miden las sensibilidades (correlación de rangos).

Uso: PYTHONPATH=. python ley_rampa_montecarlo.py [n] → ../resultados/31_ley_rampa_mc.json
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import json
import sys
from dataclasses import replace
from multiprocessing import Pool

import numpy as np
from scipy.stats import spearmanr

from piramide import geometria as g
from piramide import obra, rampas
from piramide.fisica import RANGOS, Parametros

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELOS = ("Rampas integradas en las aristas", "Zigzag en las 4 caras", "Híbrido: recta hasta 45 m + zigzag")
HIST = (85_000, 150_000)


def _una(args):
    semilla, tecnica = args
    rng = np.random.default_rng(semilla)
    p = replace(Parametros().muestrear(rng), tecnica_giro=tecnica)
    V = g.volumen_entre(0, g.ALTURA)
    cat = {m.nombre: m for m in rampas.catalogo()}
    out = {k: getattr(p, k) for k in RANGOS}
    for nombre in MODELOS:
        out[nombre] = V / obra.simular(cat[nombre], p, 1e6).anios
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    res = dict(n=n, techo_historico=HIST, tecnicas={})
    for tecnica in ("parametrica", "pivote", "poste"):
        with Pool(os.cpu_count() or 2) as pool:
            filas = pool.map(_una, [(1000 + i, tecnica) for i in range(n)])
        r = {}
        for nombre in MODELOS:
            x = np.array([f[nombre] for f in filas])
            sens = {k: round(float(spearmanr([f[k] for f in filas], x)[0]), 2) for k in RANGOS}
            top = dict(sorted(sens.items(), key=lambda kv: -abs(kv[1]))[:4])
            r[nombre] = dict(p05=round(float(np.percentile(x, 5))), mediana=round(float(np.median(x))),
                             p95=round(float(np.percentile(x, 95))),
                             fraccion_en_rango_historico=float(np.mean((x >= HIST[0]) & (x <= HIST[1]))),
                             fraccion_por_debajo=float(np.mean(x < HIST[0])),
                             fraccion_por_encima=float(np.mean(x > HIST[1])),
                             sensibilidades_principales=top)
        res["tecnicas"][tecnica] = r
        print(tecnica, json.dumps(r, ensure_ascii=False), flush=True)
    with open(os.path.join(RAIZ, "resultados", "31_ley_rampa_mc.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
