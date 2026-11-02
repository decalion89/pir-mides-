"""Verificación propia de dos casos CONDICIONALES del censo.

1. Gliozzo et al. (Sci. Rep. 2021; PMC8160351), censo n.º 140. Inclusiones metálicas casi esféricas de
   6 y 10 mm en vidrio romano, atribuidas a que "the colloidal metal–glass system reached then a
   supersaturation condition and the latter ultimately induced metal expulsion and agglomeration"
   (~900 °C). Se compara el tiempo de aglomeración browniana (Smoluchowski, t½ = 3η/(4 k_B T n₀)) y el
   de sedimentación (Stokes) con una fusión de 3–48 h.
2. Lajia (PMC11109126), censo n.º 29. Un flujo de lodo provocado por un terremoto exige loess saturado.
   Hoy lo satura el riego de invierno. Se calcula el agua necesaria para saturar 5–14 m de loess y los
   años de recarga natural semiárida que equivale.

Uso: PYTHONPATH=. python censo/vidrio_y_lajia.py → ../resultados/54_vidrio_lajia.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KB = 1.380649e-23


def main():
    rng = np.random.default_rng(54)
    N = 200_000
    pc = lambda x: dict(p05=float(f"{np.percentile(x, 5):.3g}"), mediana=float(f"{np.median(x):.3g}"),
                        p95=float(f"{np.percentile(x, 95):.3g}"))
    # 1. vidrio
    eta = 10 ** rng.uniform(2.5, 5.0, N)                          # Pa·s, fundido de vidrio a 900–1100 °C
    T = rng.uniform(1173, 1373, N)
    phi = np.exp(rng.uniform(np.log(0.005), np.log(0.05), N))     # fracción de volumen de metal
    a = np.exp(rng.uniform(np.log(1e-6), np.log(50e-6), N))       # m, radio del polvo metálico
    n0 = phi / (4 / 3 * np.pi * a ** 3)
    t_half_h = 3 * eta / (4 * KB * T * n0) / 3600
    drho = rng.uniform(6000, 6500, N)                              # kg/m³ (Cu frente a vidrio)
    altura = rng.uniform(0.05, 0.3, N)                             # m de fundido en el crisol
    v_polvo = 2 * drho * 9.81 * a ** 2 / (9 * eta)
    t_sed_polvo_h = altura / v_polvo / 3600
    a_chat = np.exp(rng.uniform(np.log(0.25e-3), np.log(2e-3), N))   # chatarra gruesa de 0,5–4 mm
    t_sed_chat_h = altura / (2 * drho * 9.81 * a_chat ** 2 / (9 * eta)) / 3600
    fusion = np.exp(rng.uniform(np.log(3), np.log(48), N))
    res = {"vidrio_romano": dict(semivida_aglomeracion_browniana_h=pc(t_half_h),
                                 prob_semivida_mayor_3_fusiones=round(float(np.mean(t_half_h >= 3 * fusion)), 3),
                                 sedimentacion_polvo_h=pc(t_sed_polvo_h), sedimentacion_chatarra_gruesa_h=pc(t_sed_chat_h),
                                 prob_chatarra_sedimenta_en_la_fusion=round(float(np.mean(t_sed_chat_h <= fusion)), 3),
                                 nota="El cobre puro (inclusión n.º 1) funde a 1085 °C: a 900 °C es sólido y no se redondea por tensión superficial.")}
    # 2. Lajia
    n = rng.uniform(0.40, 0.50, N)
    Sr = rng.uniform(0.26, 0.48, N)
    H = rng.uniform(5, 14, N)
    agua = (1 - Sr) * n * H                                        # m de agua por m² para saturar
    recarga = np.exp(rng.uniform(np.log(0.003), np.log(0.02), N))  # m/año de recarga natural semiárida
    res["lajia"] = dict(agua_para_saturar_m=pc(agua), anos_de_recarga_natural=pc(agua / recarga),
                        nota="El artículo atribuye la saturación de 2023 al riego de invierno y al nivel freático alto; no muestra esas condiciones hace ~4 000 años.")
    json.dump(res, open(os.path.join(RAIZ, "resultados", "54_vidrio_lajia.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
