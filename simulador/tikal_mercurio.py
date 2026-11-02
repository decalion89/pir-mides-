"""¿Envenenaba el mercurio de los sedimentos el agua de beber de Tikal?

Lentz et al. (Sci. Rep. 10:10316, 2020): 25 muestras de sedimento de los embalses del Templo y del
Palacio superan el "toxic effect threshold" (TET = 1,0 µg/g, un umbral para organismos del
sedimento) y 5 lo superan más de 10 veces. De ahí concluyen que los embalses estaban "seriously
compromised as sources of drinking water" y que la élite "likely were fed foods laced with mercury at
every meal". El mercurio procede sobre todo de cinabrio (HgS) de pinturas y rituales.

Paso de sedimento a agua y a persona:
  agua = disuelto (C_sed / Kd, con log Kd = 4,5–6 L/kg para Hg entre sedimento y agua)
         + partículas en suspensión (SSC 5–100 mg/L × C_sed);
  ingesta = (2–3 L/día para beber + 1–2 L/día para cocinar) × agua.
Se compara con la guía de la OMS para agua potable (6 µg/L de Hg inorgánico) y con su ingesta diaria
tolerable (2 µg/kg/día; 120 µg/día para 60 kg), suponiendo que todo el Hg es tan absorbible como el
Hg inorgánico soluble (el HgS lo es mucho menos).

Uso: PYTHONPATH=. python tikal_mercurio.py → ../resultados/48_tikal_mercurio.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    rng = np.random.default_rng(48)
    N = 200_000
    res = {}
    for nombre, (lo, hi) in (("sedimento típico por encima del TET (1–10 µg/g)", (1.0, 10.0)),
                             ("las muestras más altas (10–30 µg/g)", (10.0, 30.0))):
        c_sed = np.exp(rng.uniform(np.log(lo), np.log(hi), N))          # µg/g = mg/kg
        kd = 10 ** rng.uniform(4.5, 6.0, N)                              # L/kg
        disuelto = c_sed * 1e3 / kd                                      # µg/L
        ssc = rng.uniform(5, 100, N) * 1e-6                              # kg/L
        particulado = c_sed * 1e3 * ssc                                  # µg/L
        agua = disuelto + particulado
        ingesta = agua * rng.uniform(3.0, 5.0, N)                        # µg/día
        pc = lambda x: dict(p05=float(f"{np.percentile(x, 5):.3g}"), mediana=float(f"{np.median(x):.3g}"),
                            p95=float(f"{np.percentile(x, 95):.3g}"))
        res[nombre] = dict(hg_en_agua_ug_L=pc(agua), fraccion_guia_OMS_6ugL=pc(agua / 6.0),
                           prob_supera_guia=round(float(np.mean(agua > 6.0)), 4),
                           ingesta_ug_dia=pc(ingesta), fraccion_ingesta_tolerable_120ug=pc(ingesta / 120.0))
        print(nombre, json.dumps(res[nombre], ensure_ascii=False))
    json.dump(res, open(os.path.join(RAIZ, "resultados", "48_tikal_mercurio.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
