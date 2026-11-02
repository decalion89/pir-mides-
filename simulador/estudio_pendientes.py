"""¿Siguen los canales el sistema de proporciones de la propia pirámide?

La cara de la Gran Pirámide sube 14 por cada 11 de avance (seked de 5½ palmos, 51,84°).
Los canales medidos por Gantenbrink encajan con 11/11 (45°), 7/11 (32,47°) y 9/11 (39,29°).
¿Con qué probabilidad caerían cuatro ángulos al azar tan cerca de pendientes n/d con el mismo
denominador? Se calcula con d = 11 fijado de antemano por la cara, y también buscando el mejor
denominador entre 5 y 16, que es la corrección por haberlo mirado después.

    cd simulador && PYTHONPATH=. python estudio_pendientes.py
"""
import json, math
import numpy as np
from piramide import astronomia as a

ang = np.array([c["angulo"] for c in a.CANALES.values()])
sig = np.array([c["sigma"] for c in a.CANALES.values()])


def encaja(angs, d):
    """¿Están los 4 ángulos a ≤ 1σ de alguna pendiente n/d (n entero)?"""
    ok = []
    for x, s in zip(angs, sig):
        n = np.arange(1, 4 * d)
        dif = np.min(np.abs(np.degrees(np.arctan(n / d)) - x))
        ok.append(dif <= s)
    return all(ok)


def mejor_d(angs, ds=range(5, 17)):
    return [d for d in ds if encaja(angs, d)]


rng = np.random.default_rng(3)
N = 50000
r11 = 0
rcualquiera = 0
for _ in range(N):
    x = rng.uniform(25, 50, 4)
    r11 += encaja(x, 11)
    rcualquiera += bool(mejor_d(x))
res = dict(
    angulos=ang.tolist(), sigmas=sig.tolist(),
    pendientes_n_11={k: dict(angulo=float(v), n_mas_cercano=int(round(11 * math.tan(math.radians(v)))),
                             angulo_n_11=float(math.degrees(math.atan(round(11 * math.tan(math.radians(v))) / 11))))
                     for k, v in zip(a.CANALES, ang)},
    reales_encajan_d11=encaja(ang, 11), denominadores_que_encajan=mejor_d(ang),
    p_azar_d11=r11 / N, p_azar_algun_d_5_16=rcualquiera / N)
for k, v in res["pendientes_n_11"].items():
    print(f"   {k:12s} {v['angulo']:6.2f}° -> {v['n_mas_cercano']}/11 = {v['angulo_n_11']:.2f}°")
print(f"   ángulos reales encajan con n/11: {res['reales_encajan_d11']};  denominadores 5-16 que encajan: {res['denominadores_que_encajan']}")
print(f"   P(azar) con d = 11 fijado por la cara: {100 * res['p_azar_d11']:.2f} %")
print(f"   P(azar) buscando el mejor d entre 5 y 16: {100 * res['p_azar_algun_d_5_16']:.1f} %")
json.dump(res, open("../resultados/15_pendientes_canales.json", "w"), ensure_ascii=False, indent=1)
