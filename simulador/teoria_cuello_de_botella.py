"""Teoría del cuello de botella: el techo histórico de ~340 m³/día (doc. 23) ¿es un límite físico
de la logística de rampas? Ritmo medio máximo (V / años) de cada sistema de rampas del simulador
(doc. 07, parámetros nominales sin cambiar) al aumentar la mano de obra.

Uso: PYTHONPATH=. python teoria_cuello_de_botella.py → ../resultados/30_cuello_de_botella.json
"""
import json
import os

from piramide import geometria as g
from piramide import obra, rampas
from piramide.fisica import Parametros

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSONAS = (10_000, 25_000, 50_000, 100_000, 300_000, 1_000_000)


def main():
    p = Parametros()
    V = g.volumen_entre(0, g.ALTURA)
    hist = json.load(open(os.path.join(RAIZ, "resultados", "28_ley_aprendizaje.json")))["techo"]
    res = dict(volumen_keops_m3=round(V), dias_trabajo_anio=p.dias_anio, tecnica_giro=p.tecnica_giro,
               techo_historico_m3_ano=dict(asintota=hist["Rmax_m3_ano_mediana"], p05=hist["Rmax_p05"], p95=hist["Rmax_p95"],
                                           observado_snefru_keops_kefren=[74370, 148741]),
               modelos={})
    for m in rampas.catalogo():
        ritmos = [V / obra.simular(m, p, n).anios for n in PERSONAS]
        r = obra.simular(m, p, PERSONAS[-1])
        res["modelos"][m.nombre] = dict(ritmo_m3_ano_por_personas=dict(zip(map(str, PERSONAS), [round(x) for x in ritmos])),
                                        techo_m3_ano=round(ritmos[-1]), techo_m3_dia=round(ritmos[-1] / 365),
                                        anios_minimos_keops=round(V / ritmos[-1], 1),
                                        hiladas_por_cuello=r.cuello)
        print(f"{m.nombre[:45]:45s} techo {ritmos[-1] / 1000:6.0f} k m³/año  ({V / ritmos[-1]:.1f} años mín.)")
    with open(os.path.join(RAIZ, "resultados", "30_cuello_de_botella.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
