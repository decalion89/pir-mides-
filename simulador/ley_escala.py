"""El dogma de la escala: lo que ocurre en la probeta no es lo que ocurre en el objeto.

Para un proceso de difusión o conducción, la semejanza exige el mismo número de Fourier,
Fo = D·t/L². El tiempo equivalente en el objeto es t_obj = t_lab·(L_obj/L_lab)², y los ritmos
(K/s, mm/día...) escalan como (L_lab/L_obj)². Se aplica a tres extrapolaciones de laboratorio a objeto:
1. Cal "orgánica" (doc. 41): pasta ensayada a los 7 días frente a muros de 0,5–1 m. Profundidad de
   carbonatación d = K·√t; cal aérea K ≈ 1 mm/√día (~19 mm/√año); la cal hidráulica es 2–5 veces más
   lenta. Los aditivos que "aceleran" se modelan como K ×1–2.
2. Vidrio de Herculano (doc. 35): fragmento de calorímetro (~0,5 mm) frente a cabeza (~7,5 cm de radio).
3. Puntas de lanza con polianilina (muestra aleatoria n.º 39): inhibidor disuelto en el electrolito
   (aporte ilimitado) frente a un recubrimiento finito sobre el objeto. Es un desajuste de
   configuración, no de tamaño; se da solo de forma cualitativa.

Uso: PYTHONPATH=. python ley_escala.py → ../resultados/51_ley_escala.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    rng = np.random.default_rng(51)
    N = 200_000
    # 1. cal
    K_aerea = rng.uniform(0.7, 1.3, N)                        # mm/√día
    K_nhl = K_aerea / rng.uniform(2, 5, N)
    aditivo = rng.uniform(1.0, 2.0, N)                         # aceleración atribuible a los aditivos
    semiespesor_muro = rng.uniform(250, 500, N)                # mm (muros de 0,5–1 m carbonatando por las dos caras)
    t_muro_aerea = (semiespesor_muro / (K_aerea * aditivo)) ** 2 / 365.25
    t_muro_nhl = (semiespesor_muro / (K_nhl * aditivo)) ** 2 / 365.25
    prof_7d_nhl = K_nhl * aditivo * np.sqrt(7)                 # mm carbonatados en la probeta en 7 días
    factor_tiempo = (semiespesor_muro / rng.uniform(2.5, 10, N)) ** 2   # probetas de 5–20 mm
    pc = lambda x: dict(p05=float(f"{np.percentile(x, 5):.3g}"), mediana=float(f"{np.median(x):.3g}"),
                        p95=float(f"{np.percentile(x, 95):.3g}"))
    res = dict(cal=dict(profundidad_carbonatada_en_7_dias_NHL_mm=pc(prof_7d_nhl),
                        anos_para_carbonatar_el_nucleo_cal_aerea=pc(t_muro_aerea),
                        anos_para_carbonatar_el_nucleo_NHL=pc(t_muro_nhl),
                        factor_de_tiempo_probeta_a_muro=pc(factor_tiempo),
                        equivalente_en_muro_de_7_dias_de_probeta_anos=pc(7 * factor_tiempo / 365.25)))
    # 2. Herculano: escala térmica
    Lf = rng.uniform(0.25e-3, 2.5e-3, N)                       # m (radio de los fragmentos de 0,5–5 mm)
    Lc = rng.uniform(0.07, 0.08, N)                            # m (radio de la cabeza)
    res["herculano"] = dict(factor_de_ritmo_fragmento_a_craneo=pc((Lc / Lf) ** 2),
                            nota="El ritmo de enfriamiento escala como 1/L² (número de Fourier). El cociente ~10³–10⁵ coincide con el doc. 35.")
    res["polianilina"] = dict(nota="Inhibidor disuelto a 10–100 ppm en el electrolito sobre electrodos de 1 cm², frente a un recubrimiento finito sobre el objeto: el aporte de inhibidor no es comparable (desajuste de Damköhler). Sin cifras de espesor ni de duración del recubrimiento no se puede cuantificar.")
    json.dump(res, open(os.path.join(RAIZ, "resultados", "51_ley_escala.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
