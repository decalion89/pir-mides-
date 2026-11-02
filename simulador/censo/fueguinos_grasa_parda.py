"""Watanabe et al. (Sci. Rep. 11:23290, 2021; PMC8639971), censo n.º 156.

Afirmación: "Greater BAT accumulation might therefore explain the Fuegians extreme cold-resistance" y
"the extraordinary cold-adaptation of the Fuegians … was due to an exceptional BAT accumulation". El único
dato del efecto es de Hammel (1960): metabolismo basal (BMR) ~160 % del de un "average white man" expuesto
al frío.

Balance: calor extra necesario (+60 % de un BMR de 60–80 W) frente a lo que puede producir la grasa parda:
masa × potencia específica.
- Humanos (PET): 2–15 W/kg y como mucho ~1 kg.
- Variante generosa: hasta 100 W/kg, un supuesto que se acerca a los roedores.

Uso: PYTHONPATH=. python censo/fueguinos_grasa_parda.py → ../resultados/52_fueguinos.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    rng = np.random.default_rng(52)
    N = 200_000
    necesario = 0.6 * rng.uniform(60, 80, N)                                     # W
    masa = np.exp(rng.uniform(np.log(0.05), np.log(1.0), N))                       # kg
    pc = lambda x: dict(p05=float(f"{np.percentile(x, 5):.3g}"), mediana=float(f"{np.median(x):.3g}"),
                        p95=float(f"{np.percentile(x, 95):.3g}"))
    res = {}
    for nombre, (lo, hi) in (("humana (2–15 W/kg)", (2, 15)), ("generosa (2–100 W/kg)", (2, 100))):
        pot = masa * np.exp(rng.uniform(np.log(lo), np.log(hi), N))
        r = necesario / pot
        res[nombre] = dict(potencia_grasa_parda_W=pc(pot), cociente_necesario_sobre_capacidad=pc(r),
                           prob_mayor_3=round(float(np.mean(r >= 3)), 3), prob_basta=round(float(np.mean(r <= 1)), 3))
    json.dump(res, open(os.path.join(RAIZ, "resultados", "52_fueguinos.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
