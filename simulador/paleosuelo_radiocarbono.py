"""Broz et al. (Sci. Rep. 13:7476, 2023; PMC10167333): carbono moderno en paleosuelos del Oligoceno.

Muestra 38 de la auditoría aleatoria (auditoria_aleatoria/). Dos comprobaciones:
1. Aritmética de la tabla 2. El artículo dice que el carbono moderno es "~0.5–2.4% of the total organic C
   pool", con un modelo de mezcla de dos componentes (viejo con FM ≈ 0, moderno con FM ≈ 1). Con ese
   modelo, la fracción moderna del carbono orgánico es FM, pero la columna "Modern C (%)" coincide con
   100 × FM × TOC(wt%) de la tabla 1.
2. Ritmo: ¿puede el carbono orgánico disuelto de la lluvia aportar ese carbono moderno a 1 m de
   profundidad, en el tiempo que la roca ha pasado cerca de la superficie (erosión de 4,94 mm/año)?

Uso: PYTHONPATH=. python paleosuelo_radiocarbono.py → ../resultados/49_paleosuelo_radiocarbono.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# muestra: (TOC de la tabla 1 en wt%, FM de la tabla 2, "Modern C (%)" publicado)
TABLA = {"Lakim 0": (0.302, 0.057, 1.70), "Lakim 25": (0.116, 0.136, 1.56), "Lakim 50": (0.128, 0.080, 1.00),
         "Lakim 75": (0.251, 0.055, 1.36), "Lakim 100": (0.132, 0.181, 2.36), "Luca 22": (0.014, 0.232, 0.32),
         "TC 0": (0.170, 0.028, 0.47), "TC 25": (0.196, 0.028, 0.55), "TC 50": (0.261, 0.024, 0.61),
         "TC 100": (0.115, 0.062, 0.71)}


def main():
    filas = {}
    for k, (toc, fm, pub) in TABLA.items():
        filas[k] = dict(publicado=pub, cien_FM_por_TOC=round(100 * fm * toc, 2), fraccion_moderna_del_COT_pct=round(100 * fm, 1),
                        factor_infraestimacion=round(fm * 100 / pub, 1),
                        carbono_moderno_mg_por_kg_roca=round(fm * toc * 1e4, 0))
    # 2. ritmo: carbono moderno que hay que aportar en una columna de 1 m frente al aporte de COD
    rng = np.random.default_rng(49)
    N = 200_000
    mod = np.array([v["carbono_moderno_mg_por_kg_roca"] for v in filas.values()])
    necesario = rng.choice(mod, N) * rng.uniform(1.6, 2.2, N) * 1000 * 1.0 / 1000      # g C/m² en 1 m (mg/kg × kg/m³ × m → mg/m² /1000)
    lluvia = rng.uniform(0.25, 0.35, N)                                                # m/año
    infil = np.exp(rng.uniform(np.log(0.05), np.log(0.4), N))
    doc = np.exp(rng.uniform(np.log(2), np.log(30), N))                                 # mg/L = g/m³
    reten = rng.uniform(0.1, 0.9, N)
    ventana = np.exp(rng.uniform(np.log(100), np.log(400), N))                         # años cerca de la superficie
    aporte = lluvia * infil * doc * reten * ventana                                    # g/m²
    r = necesario / aporte
    pc = lambda x: dict(p05=float(f"{np.percentile(x, 5):.3g}"), mediana=float(f"{np.median(x):.3g}"),
                        p95=float(f"{np.percentile(x, 95):.3g}"))
    res = dict(tabla=filas,
               ritmo=dict(carbono_moderno_necesario_g_m2=pc(necesario), aporte_COD_g_m2=pc(aporte),
                          cociente_necesario_sobre_aporte=pc(r), prob_cociente_mayor_3=round(float(np.mean(r >= 3)), 3),
                          prob_basta=round(float(np.mean(r <= 1)), 3)))
    json.dump(res, open(os.path.join(RAIZ, "resultados", "49_paleosuelo_radiocarbono.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
