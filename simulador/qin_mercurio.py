"""¿Puede el mercurio de la tumba de Qin Shi Huang llegar a la superficie por difusión?

Datos: Duan, Zhang y Svanberg (Sci. Rep. 10, 10387, 2020), lidar de mercurio atómico sobre el
túmulo (julio–agosto de 2016): flujo de emisión estimado ≈ 5×10⁻⁸ kg/s (incertidumbre ~×2).
Geometría (misma fuente): cámara central ~80 × 50 × 15 m con el techo a ~30 m bajo el suelo
circundante; palacio subterráneo ~140 × 110 × 30 m; túmulo ~380 × 330 m en planta y ~50 m de alto.
Suelo del túmulo: Hg medio ~190 ppb (Chang y Li 1983/85; Jin et al. 2008).

Si en la cámara hay mercurio líquido, su aire está saturado de vapor (C_sat ≈ 9 mg/m³ a 15 °C).
Tres vías para el flujo medido:
  A. difusión a través de la tierra: F ≤ D_ef · C_sat · A / L (cota superior de estado estacionario;
     la adsorción del Hg en el suelo solo la reduce);
  B. emisión del propio suelo del túmulo (Hg ~190 ppb) a ritmos típicos de suelos así;
  C. advección: la cámara "respira" (bombeo barométrico o térmico por grietas). Caudal necesario
     Q = F / C_sat, que se compara con la capacidad del bombeo barométrico del volumen subterráneo.

Monte Carlo sobre todos los parámetros inciertos. Uso:
    PYTHONPATH=. python qin_mercurio.py → ../resultados/42_qin_mercurio.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M_HG = 0.20059          # kg/mol
R = 8.314
N = 200_000


def presion_vapor_hg(T):
    """Presión de vapor del mercurio líquido (Pa). Ajuste log10 p = 10,122 − 3190/T (±3 % en 0–40 °C;
    0,172 Pa a 20 °C frente a 0,170 de Huber et al. 2006)."""
    return 10 ** (10.122 - 3190.0 / T)


def c_sat(T):
    """Concentración de saturación del vapor de Hg (kg/m³)."""
    return presion_vapor_hg(T) * M_HG / (R * T)


def main():
    rng = np.random.default_rng(42)
    F = 5e-8 * np.exp(rng.normal(0, np.log(2), N))              # kg/s (lidar)
    T = rng.uniform(13, 17, N) + 273.15                          # temperatura de la cámara
    C = c_sat(T)
    A = np.exp(rng.uniform(np.log(4000), np.log(15400), N))      # m²: cámara central … palacio
    L = rng.uniform(30, 80, N)                                   # m de tierra hasta la superficie
    D_aire = 1.3e-5 * rng.uniform(0.9, 1.1, N)                   # m²/s, Hg en aire
    phi = rng.uniform(0.30, 0.45, N)                             # porosidad (loess / tierra apisonada)
    S = rng.uniform(0.3, 0.8, N)                                 # grado de saturación de agua
    theta_a = phi * (1 - S)
    D_ef = D_aire * theta_a ** (10 / 3) / phi ** 2               # Millington–Quirk (1961)
    # A. difusión
    F_dif = D_ef * C * A / L
    F_aire = D_aire * C * A / L                                  # cota absoluta: canal de aire libre
    # B. suelo del túmulo: área 380×330 m², flujos típicos 10–100 ng/m²/h para suelos de 0,1–1 µg/g
    A_tumulo = 380 * 330
    f_suelo = np.exp(rng.uniform(np.log(10), np.log(100), N))    # ng/m²/h
    F_suelo = f_suelo * 1e-12 / 3600 * A_tumulo                  # kg/s
    f_necesario = F / A_tumulo * 1e12 * 3600                     # ng/m²/h que haría falta
    # C. advección
    Q = F / C * 86400                                            # m³/día de aire saturado
    V_cam, V_pal = 80 * 50 * 15, 140 * 110 * 30
    # bombeo barométrico: oscilaciones sinópticas de 1–2 % cada 3–7 días
    dPP = rng.uniform(0.01, 0.02, N)
    tau = rng.uniform(3, 7, N)
    Q_baro_cam = V_cam * dPP / tau
    Q_baro_pal = V_pal * dPP / tau
    # superficie mínima de mercurio líquido expuesto para reponer lo que sale (evaporación con
    # convección natural, coeficiente de transferencia 0,5–3 mm/s)
    k = rng.uniform(0.5e-3, 3e-3, N)
    A_min_hg = F / (k * C)
    pc = lambda x: dict(p05=float(f"{np.percentile(x, 5):.3g}"), mediana=float(f"{np.median(x):.3g}"),
                        p95=float(f"{np.percentile(x, 95):.3g}"))
    res = dict(
        entrada=dict(flujo_lidar_kg_s="5e-8 (×2)", temperatura_C="13–17", area_fuente_m2="4000–15400",
                     espesor_m="30–80", porosidad="0,30–0,45", saturacion_agua="0,3–0,8"),
        c_sat_mg_m3=pc(C * 1e6),
        A_difusion=dict(D_efectiva_m2_s=pc(D_ef), flujo_max_kg_s=pc(F_dif),
                        cociente_lidar_sobre_difusion=pc(F / F_dif),
                        prob_difusion_basta=float(np.mean(F_dif >= F)),
                        cota_aire_libre_kg_s=pc(F_aire), cociente_lidar_sobre_aire_libre=pc(F / F_aire),
                        prob_aire_libre_basta=float(np.mean(F_aire >= F))),
        B_suelo=dict(flujo_suelo_tipico_kg_s=pc(F_suelo), flujo_por_area_necesario_ng_m2_h=pc(f_necesario),
                     cociente_lidar_sobre_suelo=pc(F / F_suelo), prob_suelo_basta=float(np.mean(F_suelo >= F))),
        C_adveccion=dict(caudal_necesario_m3_dia=pc(Q), renovacion_camara_dias=pc(V_cam / Q),
                         renovacion_palacio_dias=pc(V_pal / Q),
                         bombeo_barometrico_camara_m3_dia=pc(Q_baro_cam), bombeo_barometrico_palacio_m3_dia=pc(Q_baro_pal),
                         prob_bombeo_camara_basta=float(np.mean(Q_baro_cam >= Q)),
                         prob_bombeo_palacio_basta=float(np.mean(Q_baro_pal >= Q))),
        mercurio=dict(perdido_en_2200_anos_t=pc(F * 2200 * 3.156e7 / 1000),
                      superficie_minima_expuesta_m2=pc(A_min_hg),
                      anos_para_perder_100_t=pc(1e5 / F / 3.156e7)))
    with open(os.path.join(RAIZ, "resultados", "42_qin_mercurio.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
