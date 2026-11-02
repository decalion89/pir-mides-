"""Forti et al. (Sci. Rep. 13:7683, 2023; PMC10195873), censo n.º 5: erosión de tells con RUSLE.

R = 807,6 MJ mm ha⁻¹ h⁻¹ año⁻¹ (unidades SI, Renard y Freimund 1994, P = 419,45 mm) y
K = 0,30 "for anthrosols" (cita a Hu et al. 2019), con A en t/ha/año y clases de riesgo absolutas
(minimal 0–10 … extreme > 150).

Comprobación de unidades: en SI (t·ha·h·ha⁻¹·MJ⁻¹·mm⁻¹) el factor K del nomograma no pasa de ~0,09
(0,69 en unidades de EE. UU. × 0,1317), y en suelos arcillosos o limo-arcillosos ronda 0,02–0,06.
K = 0,30 es un valor de escala estadounidense. Como A ∝ K, el factor de sobrestimación es 0,30/K_SI.
Comprobación física: descenso de la superficie del montículo = A / densidad aparente, comparado con la
edad del tell y su altura.

Uso: PYTHONPATH=. python censo/tells_rusle.py → ../resultados/53_tells_rusle.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    R = 0.04830 * 419.45 ** 1.61                    # Renard y Freimund (1994)
    rng = np.random.default_rng(53)
    N = 200_000
    k_us = rng.uniform(0.15, 0.45, N)              # valor de escala estadounidense plausible para limos arcillosos
    k_si = k_us * 0.1317
    factor = 0.30 / k_si
    rho = rng.uniform(1.3, 1.7, N)                 # t/m³
    descenso_extremo = 150 / (rho * 1e4) * 1e3     # mm/año para A = 150 t/ha/año
    pc = lambda x: dict(p05=float(f"{np.percentile(x, 5):.3g}"), mediana=float(f"{np.median(x):.3g}"),
                        p95=float(f"{np.percentile(x, 95):.3g}"))
    res = dict(R_reproducido=round(R, 1), factor_contra_maximo_fisico_SI=round(0.30 / 0.091, 2),
               factor_sobrestimacion=pc(factor), prob_mayor_3=round(float(np.mean(factor >= 3)), 3),
               descenso_superficie_clase_extrema_mm_ano=pc(descenso_extremo),
               metros_perdidos_en_2000_anos_a_150t=pc(descenso_extremo * 2000 / 1000),
               umbral_extremo_equivalente_con_K_corregido_t_ha_ano=pc(150 / factor))
    json.dump(res, open(os.path.join(RAIZ, "resultados", "53_tells_rusle.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
