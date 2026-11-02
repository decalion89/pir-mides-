"""Shivakumar, Selvaraj y Dhassaih (Sci. Rep. 11:13261, 2021; PMC8225893): pasta de cal "orgánica"
(cal hidráulica NHL 2.5 + extracto vegetal fermentado). Muestra n.º 6 de la auditoría aleatoria.

Afirmación: "Supply of CO2 has initiated the internal carbonation of the lime putty"; el extracto
resuelve que "internal core mortars remain un-carbonated for decades"; CO2 medido en el espacio de
cabeza de la fermentación: hasta 96 000 ppm; extracto:cal = 0,68–0,74 L/kg; azúcares totales del
extracto de jaggery 6 867 µg/mL (los demás 16–424 µg/mL).

Estequiometría: moles de CO2 que puede aportar el extracto (disuelto en equilibrio con el espacio de
cabeza, con sobresaturación de hasta ×10, o fermentando todo el azúcar residual) frente a los moles de
Ca(OH)2 de la cal (30–60 % de NHL 2.5).

Uso: PYTHONPATH=. python cal_organica.py → ../resultados/50_cal_organica.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    rng = np.random.default_rng(50)
    N = 200_000
    caoh2 = rng.uniform(0.30, 0.60, N) * 1000 / 74.09                 # mol por kg de cal
    liquido = rng.uniform(0.68, 0.74, N)                               # L por kg de cal
    pco2 = rng.uniform(0.036, 0.096, N)                                # atm (36 000–96 000 ppm)
    disuelto = 0.034 * pco2 * np.exp(rng.uniform(0, np.log(10), N))    # mol/L, con hasta ×10 de sobresaturación
    azucar = np.exp(rng.uniform(np.log(0.016), np.log(6.867), N))      # g/L (de aloe vera a jaggery)
    co2_azucar = azucar / 180.16 * 2                                   # mol/L si fermenta todo (C6H12O6 → 2 CO2)
    f_dis = disuelto * liquido / caoh2
    f_max = (disuelto + co2_azucar) * liquido / caoh2
    pc = lambda x: dict(p05=float(f"{np.percentile(x, 5):.3g}"), mediana=float(f"{np.median(x):.3g}"),
                        p95=float(f"{np.percentile(x, 95):.3g}"), maximo=float(f"{np.max(x):.3g}"))
    res = dict(fraccion_carbonatable_solo_CO2_disuelto=pc(f_dis),
               fraccion_carbonatable_fermentando_todo_el_azucar=pc(f_max),
               cociente_carbonatacion_completa_sobre_maximo=pc(1 / f_max),
               prob_cociente_mayor_3=round(float(np.mean(1 / f_max >= 3)), 4))
    json.dump(res, open(os.path.join(RAIZ, "resultados", "50_cal_organica.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
