"""¿Qué errores de orientación puede producir el método del gnomon ("círculo indio")?

Método: un palo vertical; se marca la punta de la sombra cuando toca un círculo por la mañana y
otra vez por la tarde (misma altura del sol); la bisectriz de las dos marcas apunta al norte.
Error físico: entre la mañana y la tarde cambia la declinación del sol, así que las dos alturas
iguales no son simétricas respecto al meridiano. Glen Dash (2017) propuso este método, en otoño,
para Keops.

Se calcula con la posición real del sol (declinación con la fórmula de Spencer, latitud de Giza)
el error de la bisectriz para cada día del año y cada altura de observación, y se compara con
los errores medidos de las pirámides (Spence 2000, tabla 1; doc. 15).

Uso: PYTHONPATH=. python metodo_gnomon.py → ../resultados/32_metodo_gnomon.json
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAT = math.radians(29.98)
# errores medidos (′, + = este) — Spence 2000, tabla 1 (lado este); ver piramide/orientacion.py
ERRORES = {"Meidum": -20.6, "Acodada": -17.3, "Roja": -8.7, "Keops": -3.4, "Kefrén": -6.0,
           "Micerino": 12.4, "Sahure": -23.0, "Neferirkara": 30.0, "Unas": 17.1}


def declinacion(dia: np.ndarray) -> np.ndarray:
    """Declinación solar (rad) con la serie de Spencer; `dia` continuo (0 = 1 de enero)."""
    G = 2 * np.pi * dia / 365.0
    return (0.006918 - 0.399912 * np.cos(G) + 0.070257 * np.sin(G) - 0.006758 * np.cos(2 * G)
            + 0.000907 * np.sin(2 * G) - 0.002697 * np.cos(3 * G) + 0.00148 * np.sin(3 * G))


def altaz(dia, h):
    """Altura y acimut del sol (rad; acimut desde el norte, + hacia el este). h = ángulo horario."""
    d = declinacion(dia + h / (2 * np.pi))
    alt = np.arcsin(np.sin(LAT) * np.sin(d) + np.cos(LAT) * np.cos(d) * np.cos(h))
    az = np.arctan2(-np.cos(d) * np.sin(h), np.sin(d) * np.cos(LAT) - np.cos(d) * np.cos(h) * np.sin(LAT))
    return alt, az


def error_bisectriz(dia: float, altura_obs_deg: float) -> float:
    """Error (′, + = este) de la línea norte obtenida con sombras de igual longitud ese día."""
    a = math.radians(altura_obs_deg)
    hh = np.linspace(-np.pi * 0.95, 0, 20000)
    alt_m, _ = altaz(dia, hh)
    ok = np.where(np.diff(np.sign(alt_m - a)) != 0)[0]
    if len(ok) == 0:
        return float("nan")
    i = ok[-1]
    hm = hh[i] + (a - alt_m[i]) * (hh[i + 1] - hh[i]) / (alt_m[i + 1] - alt_m[i])
    hh2 = np.linspace(0, np.pi * 0.95, 20000)
    alt_t, _ = altaz(dia, hh2)
    ok2 = np.where(np.diff(np.sign(alt_t - a)) != 0)[0]
    if len(ok2) == 0:
        return float("nan")
    j = ok2[0]
    ht = hh2[j] + (a - alt_t[j]) * (hh2[j + 1] - hh2[j]) / (alt_t[j + 1] - alt_t[j])
    _, azm = altaz(dia, hm)
    _, azt = altaz(dia, ht)
    # la sombra apunta en la dirección opuesta al sol; la bisectriz de las dos sombras apunta al
    # norte; su desviación es la media angular de los acimutes del sol (respecto al sur)
    m = math.atan2((math.sin(azm) + math.sin(azt)) / 2, (math.cos(azm) + math.cos(azt)) / 2)
    # la línea norte-sur trazada es la bisectriz (sin sentido): su desviación respecto al
    # meridiano es m módulo π, llevada a (−90°, 90°]; + = el extremo norte de la línea va al este
    desv = ((m + math.pi / 2) % math.pi) - math.pi / 2
    return math.degrees(desv) * 60


def main():
    dias = np.arange(0, 365, 1.0)
    alturas = np.arange(15, 61, 5.0)
    E = np.array([[error_bisectriz(d, a) for a in alturas] for d in dias])
    # alturas alcanzables: el sol debe superar la altura de observación ese día
    maxabs = np.nanmax(np.abs(E))
    por_altura = {f"{a:g}": dict(max_abs=round(float(np.nanmax(np.abs(E[:, k]))), 2),
                                 dia_max=int(dias[np.nanargmax(np.abs(E[:, k]))]))
                  for k, a in enumerate(alturas)}
    # ¿qué errores observados puede producir el método (sin ruido de medida)?
    alcanzable = {p: bool(np.nanmin(np.abs(E - e)) < 0.5) for p, e in ERRORES.items()}
    # días y alturas que reproducen el error de Keops (±0,2′)
    k_keops = np.argwhere(np.abs(E - ERRORES["Keops"]) <= 0.2)
    res = dict(latitud=29.98, alturas_deg=alturas.tolist(),
               error_maximo_absoluto_arcmin=round(float(maxabs), 2), por_altura=por_altura,
               errores_observados=ERRORES, reproducible_sin_ruido=alcanzable,
               keops_ejemplos=[dict(dia=int(dias[i]), altura=float(alturas[j]), error=round(float(E[i, j]), 2))
                               for i, j in k_keops[:8]],
               error_en_equinoccios={"20 mar (día 79)": [None if not np.isfinite(x) else round(float(x), 2) for x in E[79]],
                                     "22 sep (día 265)": [None if not np.isfinite(x) else round(float(x), 2) for x in E[265]]})
    with open(os.path.join(RAIZ, "resultados", "32_metodo_gnomon.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)
    print(json.dumps({k: v for k, v in res.items() if k not in ("por_altura",)}, ensure_ascii=False, indent=1))
    print("por altura:", {a: v["max_abs"] for a, v in por_altura.items()})


if __name__ == "__main__":
    main()
