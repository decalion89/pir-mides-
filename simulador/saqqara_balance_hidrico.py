"""¿Había agua para el "ascensor hidráulico" de la pirámide de Djoser?

Landreau et al. (PLOS ONE 19:e0306690, 2024) proponen que un flotador en el pozo norte (7 × 7 m,
28 m de profundidad) elevó las piedras. Sus propias cifras:
- agua necesaria: hasta 18 Mm³ en 20–30 años (0,6–0,9 Mm³/año); con rampas en los primeros 20 m y
  uso doble (elevar al llenar, izar al vaciar) bajaría a ~1/3 o menos;
- aporte: cuenca de Abusir 7 500–68 000 m³/año; Wadi Taflah (si se desvía) 0,2–1,8 Mm³/año, en
  riadas episódicas;
- almacenamiento: embalse de Gisr el-Mudir de 220 000–440 000 m³ con 1–2 m de profundidad, y
  la Deep Trench (> 14 000 m³);
- su suplemento dice: "These values ... do not account for water losses caused by infiltration and
  other factors"; el artículo no menciona la evaporación.

Aquí se simula día a día, durante la obra, un embalse alimentado por riadas (Poisson) que pierde
agua por evaporación e infiltración y suministra al ascensor. Monte Carlo sobre todos los parámetros.

Uso: PYTHONPATH=. python saqqara_balance_hidrico.py → ../resultados/45_saqqara_balance.json
"""
import json
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def simular(rng, anos, aporte_anual, riadas_ano, capacidad, prof, evap, infil, demanda, trinchera):
    """Devuelve las fracciones de la demanda cubierta y del aporte perdido por cada vía."""
    dias = int(anos * 365)
    area_llena = capacidad / prof
    V = 0.0                    # embalse
    T = trinchera              # Deep Trench (sin pérdidas, llena al empezar)
    entregado = ev = inf = rebose = entrada = 0.0
    d_dia = demanda / 365.0
    dias_con_agua = 0
    for _ in range(dias):
        if rng.random() < riadas_ano / 365.0:
            q = rng.exponential(aporte_anual / riadas_ano)
            entrada += q
            V += q
            if V > capacidad:
                rebose += V - capacidad
                V = capacidad
        if V > 0:
            a = area_llena * (V / capacidad) ** 0.5          # orillas en pendiente: el área decrece
            pe = min(V, a * evap / 365.0)
            V -= pe
            ev += pe
            pi = min(V, a * infil / 365.0)
            V -= pi
            inf += pi
        # la trinchera se rellena desde el embalse y suministra al ascensor
        hueco = trinchera - T
        tr = min(V, hueco)
        V -= tr
        T += tr
        s = min(T, d_dia)
        T -= s
        entregado += s
        if s >= 0.999 * d_dia:
            dias_con_agua += 1
    tot = max(entrada, 1e-9)
    return dict(cubierto=entregado / (demanda * anos), evaporacion=ev / tot, infiltracion=inf / tot,
                rebose=rebose / tot, dias_operativos=dias_con_agua / dias)


def main():
    rng = np.random.default_rng(45)
    n = 1500
    res = {}
    for nombre, total in (("demanda_de_los_autores_18Mm3", 18e6), ("demanda_optimizada_6Mm3", 6e6)):
        filas = []
        for _ in range(n):
            anos = rng.uniform(20, 30)
            p = dict(aporte_anual=np.exp(rng.uniform(np.log(0.2e6), np.log(1.8e6))) + rng.uniform(7.5e3, 68e3),
                     riadas_ano=np.exp(rng.uniform(np.log(0.5), np.log(5))),
                     capacidad=rng.uniform(220e3, 440e3), prof=rng.uniform(1.0, 2.0),
                     evap=rng.uniform(1.5, 2.7), infil=np.exp(rng.uniform(np.log(0.1), np.log(3.0))),
                     trinchera=rng.uniform(14e3, 33e3))
            r = simular(rng, anos, demanda=total / anos, **p)
            r_sin = simular(rng, anos, demanda=total / anos, **{**p, "evap": 0.0, "infil": 0.0})
            filas.append(dict(p=p, con_perdidas=r, sin_perdidas=r_sin))
        pc = lambda xs: dict(p05=round(float(np.percentile(xs, 5)), 3), mediana=round(float(np.median(xs)), 3),
                             p95=round(float(np.percentile(xs, 95)), 3))
        cub = np.array([f["con_perdidas"]["cubierto"] for f in filas])
        cub0 = np.array([f["sin_perdidas"]["cubierto"] for f in filas])
        res[nombre] = dict(
            fraccion_cubierta_con_perdidas=pc(cub), fraccion_cubierta_sin_perdidas=pc(cub0),
            prob_cubre_90pc_con_perdidas=round(float(np.mean(cub >= 0.9)), 3),
            prob_cubre_90pc_sin_perdidas=round(float(np.mean(cub0 >= 0.9)), 3),
            perdida_evaporacion=pc([f["con_perdidas"]["evaporacion"] for f in filas]),
            perdida_infiltracion=pc([f["con_perdidas"]["infiltracion"] for f in filas]),
            rebose=pc([f["con_perdidas"]["rebose"] for f in filas]),
            dias_operativos=pc([f["con_perdidas"]["dias_operativos"] for f in filas]))
        print(nombre, json.dumps(res[nombre], ensure_ascii=False), flush=True)
    # mejores casos deterministas (parámetros favorables), con dos embalses posibles
    mejores = {}
    for emb, cap, prof in (("Gisr el-Mudir (440 000 m³, 2 m)", 440e3, 2.0), ("todo el Foso Seco (3,5 Mm³, 20 m)", 3.5e6, 20.0)):
        for dem_nom, total in (("autores 18 Mm³", 18e6), ("optimizada 6 Mm³", 6e6)):
            for aporte in (0.6e6, 1.8e6):
                vals = []
                for k in range(40):
                    r = simular(np.random.default_rng(1000 + k), 25, aporte_anual=aporte + 68e3, riadas_ano=5.0,
                                capacidad=cap, prof=prof, evap=1.5, infil=0.1, demanda=total / 25, trinchera=33e3)
                    vals.append(r["cubierto"])
                mejores[f"{emb}; demanda {dem_nom}; aporte {aporte / 1e6:g} Mm³/año"] = round(float(np.mean(vals)), 3)
    res["mejores_casos_fraccion_cubierta"] = mejores
    print(json.dumps(mejores, ensure_ascii=False, indent=1))
    # tiempo que tarda en secarse el embalse lleno sin aportes
    secado = {}
    for prof in (1.0, 2.0):
        for e, i in ((1.5, 0.1), (2.1, 0.5), (2.7, 3.0)):
            # dV/dt = -(e+i)·A·sqrt(V/C), A = C/prof → t = 2·prof/(e+i)
            secado[f"prof {prof} m, evap {e}, infil {i} m/año"] = round(2 * prof / (e + i) * 12, 1)
    res["meses_para_secarse_el_embalse_lleno"] = secado
    json.dump(res, open(os.path.join(RAIZ, "resultados", "45_saqqara_balance.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(secado, ensure_ascii=False))


if __name__ == "__main__":
    main()
