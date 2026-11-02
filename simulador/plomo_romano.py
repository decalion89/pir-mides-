"""¿Pudo el plomo del aire romano subir 2,4 µg/dl la sangre de los niños y quitar 2,5–3 puntos de CI?

McConnell et al. (PNAS 122:e2419630121, 2025): el aire de Europa tenía +1,04 ng/m³ de plomo de
media (0,16–157 ng/m³) durante la Pax Romana; con BLL = exp[1,932 + 0,140·ln(PbA)] (PbA en µg/m³;
Richmond-Bryant et al. 2014, NHANES III, EE. UU., 1988–94, modelo sin ajustar) obtienen un
"aumento" de 2,0–5,3 µg/dl, que suman a una base neolítica de 1 µg/dl, y con
CI = −3,315·ln(BLL + 1) un déficit de 2,5–3 puntos.

Dos comprobaciones:
A. Su propia regresión, diferenciada correctamente: BLL(C_fondo + ΔC) − BLL(C_fondo). La
   regresión es la plombemia TOTAL de niños de EE. UU. en 1988–94 (pintura, polvo, dieta...), no
   el aumento debido al aire.
B. Balance de ingesta desde cero, con factores de pendiente estándar:
   - inhalación directa: 1–3 µg/dl por µg/m³;
   - dieta: plomo depositado sobre los cultivos (interceptación, rendimiento, lavado), con el
     depósito total del propio artículo (> 500 kt en ~175 años sobre el Imperio); cereales (rendimiento
     romano de grano bajo, 0,05–0,1 kg/m², interceptación por el grano 1–5 %, 30–70 % retenido tras
     limpiar y moler) y verduras por separado;
   - agua de lluvia de cisternas (concentración = depósito anual / lluvia anual; 0,5–1,5 L/día);
   - suelo y polvo: ingestión de 50–200 mg/día de suelo enriquecido por ese depósito;
   - plombemia por ingesta: 0,10–0,24 µg/dl por µg/día ingerido (ATSDR, niños).

Uso: PYTHONPATH=. python plomo_romano.py → ../resultados/46_plomo_romano.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def bll_regresion(pba_ug_m3, b0=1.932, b1=0.140):
    return np.exp(b0 + b1 * np.log(pba_ug_m3))


def deficit_ci(delta_bll, base=1.0):
    """Déficit de CI respecto a la base con el modelo del artículo: −3,315·ln(BLL + 1)."""
    return 3.315 * (np.log(base + delta_bll + 1) - np.log(base + 1))


def main():
    rng = np.random.default_rng(46)
    N = 200_000
    dC = 1.04e-3                                         # µg/m³, media europea del artículo
    # A. regresión diferenciada
    c_fondo = np.exp(rng.uniform(np.log(1e-5), np.log(1e-4), N))   # 0,01–0,1 ng/m³ de fondo natural
    dA = bll_regresion(c_fondo + dC) - bll_regresion(c_fondo)
    # B. balance de ingesta
    inh = rng.uniform(1.0, 3.0, N) * dC                  # µg/dl
    dep_total = rng.uniform(500e9, 800e9, N)             # g de plomo en 175 años
    area = rng.uniform(3e12, 6e12, N)                    # m² donde se depositó "the bulk"
    Fd = dep_total / 175 / 365 / area * 1e6              # µg/m²/día
    lam = rng.uniform(0.03, 0.07, N)                     # 1/día, pérdida por lluvia y viento
    # verduras
    c_veg = Fd * rng.uniform(0.1, 0.3, N) / (rng.uniform(1.0, 3.0, N) * lam)            # µg/kg
    ing_veg = c_veg * rng.uniform(0.05, 0.2, N)                                          # µg/día
    # cereales (la base de la dieta romana)
    c_cer = Fd * rng.uniform(0.01, 0.05, N) / (rng.uniform(0.05, 0.10, N) * lam) * rng.uniform(0.3, 0.7, N)
    ing_cer = c_cer * rng.uniform(0.15, 0.30, N)
    ing_dieta = ing_veg + ing_cer
    # agua de cisterna
    lluvia = rng.uniform(0.4, 0.9, N) * 1000.0                                           # L/m²/año
    c_cist = Fd * 365 / lluvia                                                           # µg/L
    ing_cist = c_cist * rng.uniform(0.5, 1.5, N)
    prof = rng.uniform(0.02, 0.10, N)                    # m de mezcla en el suelo
    dsuelo = dep_total / area / (prof * 1.3e3) * 1e6     # µg/kg (g/m² ÷ kg/m² × 10⁶); densidad 1300 kg/m³
    ing_suelo = dsuelo * rng.uniform(50e-6, 200e-6, N)   # µg/día (50–200 mg = 5–20×10⁻⁵ kg de suelo al día)
    pend = rng.uniform(0.10, 0.24, N)                    # µg/dl por µg/día ingerido
    dB = inh + pend * (ing_dieta + ing_suelo + ing_cist)
    pc = lambda x: dict(p05=float(f"{np.percentile(x, 5):.3g}"), mediana=float(f"{np.median(x):.3g}"),
                        p95=float(f"{np.percentile(x, 95):.3g}"))
    res = dict(
        pendiente_richmond_bryant_a_bajo_PbA_ug_dl_por_ug_m3="15,3–16,5 (Richmond-Bryant et al. 2014)",
        aumento_con_pendiente_16_ug_dl=round(16.0 * dC, 4),
        reproduccion_del_articulo=dict(aumento_a_1_04_ng=round(float(bll_regresion(dC)), 2),
                                       a_0_16_ng=round(float(bll_regresion(0.16e-3)), 2),
                                       a_157_ng=round(float(bll_regresion(157e-3)), 2),
                                       deficit_ci_con_2_4=round(float(deficit_ci(2.4)), 2),
                                       bll_predicho_con_aire_limpio_0_03_ng=round(float(bll_regresion(3e-5)), 2),
                                       pendiente_implicita_ug_dl_por_ug_m3=round(float(0.140 * bll_regresion(dC) / dC), 0)),
        A_regresion_diferenciada=dict(aumento_ug_dl=pc(dA), deficit_ci=pc(deficit_ci(dA))),
        B_balance=dict(deposito_ug_m2_dia=pc(Fd), plomo_en_verduras_ug_kg=pc(c_veg), plomo_en_cereal_ug_kg=pc(c_cer),
                       ingesta_verduras_ug_dia=pc(ing_veg), ingesta_cereal_ug_dia=pc(ing_cer),
                       ingesta_dieta_ug_dia=pc(ing_dieta), plomo_cisterna_ug_L=pc(c_cist), ingesta_cisterna_ug_dia=pc(ing_cist), aumento_suelo_mg_kg=pc(dsuelo / 1e3),
                       ingesta_suelo_ug_dia=pc(ing_suelo), aumento_por_inhalacion_ug_dl=pc(inh),
                       aumento_total_ug_dl=pc(dB), deficit_ci=pc(deficit_ci(dB)),
                       cociente_articulo_sobre_balance=pc(2.4 / dB)))
    json.dump(res, open(os.path.join(RAIZ, "resultados", "46_plomo_romano.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
