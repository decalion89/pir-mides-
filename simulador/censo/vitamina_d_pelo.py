"""Verificación propia, censo n.º 50 (PMC11760916): 25(OH)D3 en el pelo, con medianas de 20 000–38 442
pg/mg en tres participantes, atribuidas a "the release of stored 25(OH)D3 from adipose tissue and
subsequent uptake in hair" tras perder peso.

Balance:
- 25(OH)D3 que se iría al pelo cada día = producción de pelo (mg/día) × concentración;
- frente al recambio diario de 25(OH)D del cuerpo (5–25 µg/día);
- y concentración en el pelo frente a la del suero (20–40 ng/mL ≈ 20–40 pg/mg).

Uso: PYTHONPATH=. python censo/vitamina_d_pelo.py → ../resultados/55_vitamina_d_pelo.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    rng = np.random.default_rng(55)
    N = 200_000
    pelo = rng.uniform(8e4, 1.2e5, N) * rng.uniform(0.85, 0.9, N) * rng.uniform(0.030, 0.045, N) * rng.uniform(30, 90, N) / 1000   # mg/día
    recambio = rng.uniform(5, 25, N)                                                  # µg/día
    suero = rng.uniform(20, 40, N)                                                    # pg/mg
    pc = lambda x: dict(p05=float(f"{np.percentile(x, 5):.3g}"), mediana=float(f"{np.median(x):.3g}"),
                        p95=float(f"{np.percentile(x, 95):.3g}"))
    res = {"produccion_de_pelo_mg_dia": pc(pelo)}
    for c in (4500, 20000, 38442):
        frac = pelo * c / 1e6 / recambio                                              # pg/mg × mg/día → pg/día → µg/día
        res[f"{c} pg/mg"] = dict(fraccion_del_recambio_diario=pc(frac), veces_la_concentracion_del_suero=pc(c / suero))
    json.dump(res, open(os.path.join(RAIZ, "resultados", "55_vitamina_d_pelo.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
