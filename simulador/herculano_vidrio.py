"""¿Permite la física la historia térmica del "cerebro vitrificado" de Herculano?

Giordano et al. (2025, Sci. Rep. 15:5955) miden el inicio de la relajación (DSC) de fragmentos
vítreos sacados del cráneo de una víctima del 79 d. C.: 420 °C calentando a 0,42 K/s y 510 °C a
1000 K/s. Infieren que la temperatura ficticia natural es ~510 °C y que el cerebro se enfrió
"at rates comparable with our experimental 1000 K s⁻¹" al disiparse una nube de ceniza diluida
que duró "minutos". Después, depósitos de 315–465 °C enterraron el cuerpo.

Con SUS parámetros cinéticos (energía de activación de los dos inicios, ~390 kJ/mol):
1. Ritmo de enfriamiento físicamente posible: (a) contenido del cráneo (conducción esférica con
   convección y radiación en la superficie); (b) cota: un fragmento suelto en aire quieto.
2. Temperatura ficticia que corresponde a esos ritmos.
3. Tiempo para secar y calentar el cerebro por encima de 510 °C bajo la nube.
4. A las temperaturas de los depósitos: tiempo para ablandarse (relajación del líquido) y tiempo
   para recocerse, es decir, para borrar la temperatura ficticia original (Tool–Narayanaswamy–Moynihan, x = 0,5).

Uso: PYTHONPATH=. python herculano_vidrio.py → ../resultados/44_herculano_vidrio.json
"""
import json
import math
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = 8.314
SIGMA = 5.670e-8
T1, Q1 = 420 + 273.15, 0.42      # inicio C-DSC (K) y ritmo (K/s)
T2, Q2 = 510 + 273.15, 1000.0    # inicio F-DSC
E_R = math.log(Q2 / Q1) / (1 / T1 - 1 / T2)   # E/R (K)


def t_ficticia(q):
    """Tf (K) para un enfriamiento a q (K/s): ln q = const − (E/R)/Tf (Moynihan et al. 1976)."""
    return 1.0 / (1.0 / T2 + math.log(Q2 / q) / E_R)


def tau_equilibrio(T):
    """Tiempo de relajación del líquido (s): τ ≈ (R T²/E)/q en el inicio medido, con Arrhenius."""
    tau1 = (T1 ** 2 / E_R) / Q1
    return tau1 * math.exp(E_R * (1 / T - 1 / T1))


def tau_vidrio(T, Tf, x=0.5):
    """Tool–Narayanaswamy–Moynihan: un vidrio con Tf > T relaja más despacio que el líquido."""
    tau1 = (T1 ** 2 / E_R) / Q1
    return tau1 * math.exp(E_R * (x / T + (1 - x) / Tf - 1 / T1))


def enfriamiento_craneo(r_cer=0.07, e_hueso=0.0065, k=0.5, rho=1200.0, c=1700.0, h=25.0, eps=0.9,
                        T0=560 + 273.15, Ta=40 + 273.15, n=140, t_max=4000.0):
    """Conducción radial en una esfera (cerebro + hueso, propiedades efectivas generosas), con
    convección + radiación en la superficie. Devuelve el ritmo de enfriamiento (K/s) al cruzar 510 °C
    en el centro, a 1 cm de la superficie interna del hueso y en la superficie interna del hueso."""
    Rt = r_cer + e_hueso
    r = np.linspace(0, Rt, n)
    dr = r[1] - r[0]
    a = k / (rho * c)
    dt = 0.2 * dr * dr / a
    T = np.full(n, T0)
    puntos = {"centro": 0, "a_1cm_del_hueso": int(round((r_cer - 0.01) / dr)), "borde_del_cerebro": int(round(r_cer / dr))}
    ritmo = {}
    t = 0.0
    prev = T.copy()
    while t < t_max and len(ritmo) < len(puntos):
        Tn = T.copy()
        lap = np.zeros(n)
        lap[1:-1] = (T[2:] - 2 * T[1:-1] + T[:-2]) / dr ** 2 + (T[2:] - T[:-2]) / (r[1:-1] * dr)
        lap[0] = 6 * (T[1] - T[0]) / dr ** 2
        Tn[:-1] = T[:-1] + a * dt * lap[:-1]
        qs = h * (T[-1] - Ta) + eps * SIGMA * (T[-1] ** 4 - Ta ** 4)
        Tn[-1] = T[-1] + dt * (2 * k * (T[-2] - T[-1]) / dr - 2 * qs) / (rho * c * dr)
        prev, T = T, Tn
        t += dt
        for nombre, i in puntos.items():
            if nombre not in ritmo and prev[i] > T2 >= T[i]:
                ritmo[nombre] = (prev[i] - T[i]) / dt
    return ritmo


def enfriamiento_particula(d, h_conv=None, eps=0.9, T=T2, Ta=40 + 273.15, rho=1200.0, c=1700.0):
    """Fragmento suelto en aire quieto (cota superior): Nu = 2 → h = 2 k_aire/d."""
    k_aire = 0.055
    h_c = 2 * k_aire / d if h_conv is None else h_conv
    h_r = eps * SIGMA * (T ** 4 - Ta ** 4) / (T - Ta)
    return (h_c + h_r) * (6 / d) * (T - Ta) / (rho * c)


def calentamiento(Tnube, eps, h, area, m_cer=1.35, f_agua=0.77):
    """Tiempo mínimo (s) para evaporar el agua del cerebro y llevar lo seco a 510 °C, con toda la
    potencia que entra en la cabeza llegando al cerebro (cota inferior: sin límite de conducción)."""
    Ts = 100 + 273.15
    qpp = h * (Tnube - Ts) + eps * SIGMA * (Tnube ** 4 - Ts ** 4)
    energia = m_cer * (f_agua * (4186 * 80 + 2.26e6) + (1 - f_agua) * 1700 * 490)
    return energia / (qpp * area)


def main():
    out = dict(E_activacion_kJ_mol=round(E_R * R / 1000, 1))
    # 1. enfriamiento
    casos = {}
    for nombre, kw in {"generoso (k=0,5, h=25, ε=0,9)": dict(k=0.5, h=25.0),
                       "muy generoso (k=1,0, h=100: viento fuerte)": dict(k=1.0, h=100.0),
                       "realista (k=0,2, h=10)": dict(k=0.2, h=10.0)}.items():
        casos[nombre] = {p: round(v, 3) for p, v in enfriamiento_craneo(**kw).items()}
    out["ritmo_enfriamiento_craneo_K_s"] = casos
    out["ritmo_enfriamiento_fragmento_suelto_K_s"] = {f"{d * 1000:g} mm": round(enfriamiento_particula(d), 1)
                                                      for d in (0.5e-3, 1e-3, 2e-3, 5e-3)}
    out["ritmo_fragmento_1mm_con_viento_h200_K_s"] = round(enfriamiento_particula(1e-3, h_conv=200.0), 1)
    # 2. temperatura ficticia
    out["temperatura_ficticia_C"] = {f"{q:g} K/s": round(t_ficticia(q) - 273.15, 1)
                                     for q in (0.01, 0.1, 1.0, 10.0, 100.0, 1000.0)}
    # 3. calentamiento
    cal = {}
    for Tn in (550, 650, 750):
        for eps, h in ((0.3, 30.0), (1.0, 100.0)):
            for area in (0.06, 0.12):
                cal[f"nube {Tn} °C, ε={eps}, h={h:g}, área {area} m²"] = round(calentamiento(Tn + 273.15, eps, h, area) / 60, 1)
    out["minutos_minimos_para_secar_y_calentar_el_cerebro"] = cal
    # 4. supervivencia
    sup = {}
    for Tdep in (315, 350, 400, 465):
        T = Tdep + 273.15
        sup[f"{Tdep} °C"] = dict(tiempo_para_ablandarse_s=float(f"{tau_equilibrio(T):.3g}"),
                                tiempo_de_recocido_si_Tf510_s=float(f"{tau_vidrio(T, T2):.3g}"),
                                tiempo_de_recocido_si_Tf430_s=float(f"{tau_vidrio(T, t_ficticia(1.0)):.3g}"))
    out["en_el_deposito"] = sup
    with open(os.path.join(RAIZ, "resultados", "44_herculano_vidrio.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
