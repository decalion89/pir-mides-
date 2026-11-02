"""Prerregistro a ciegas: ¿en qué noches de la campaña lidar de 2016 debió salir más mercurio
si la tumba de Qin Shi Huang "respira" por bombeo barométrico (doc. 34)?

Presión: estación sinóptica de Jinghe (WMO 57131, 34,43 N 108,97 E, 411 m), a ~27 km del
mausoleo; NOAA ISD-Lite 2016 (presión al nivel del mar, cada 3 h), copia en datos/qin/.
Campaña lidar: 24 jul – 12 ago 2016, sobre todo de noche (Duan et al. 2020).

Modelo: el palacio subterráneo exhala cuando la presión baja. Caudal de salida ∝ max(−dP/dt, 0),
filtrado con un tiempo de respuesta τ del recubrimiento (6–24 h). Se calcula:
1. la amplitud real de las variaciones de presión durante la campaña y la capacidad real del
   bombeo barométrico (revisa el supuesto del 1–2 % cada 3–7 días del doc. 34);
2. un índice de emisión relativo para cada noche (20:00–06:00, hora de China) y su orden.

Uso: PYTHONPATH=. python qin_presion_prerregistro.py → ../resultados/43_qin_prerregistro.json
"""
import gzip
import json
import os
from datetime import datetime, timedelta

import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVO = os.path.join(RAIZ, "datos", "qin", "isd-lite_571310-99999-2016_JINGHE.gz")
V_PALACIO, V_CAMARA = 140 * 110 * 30, 80 * 50 * 15
Q_NECESARIO = 458.0          # m³/día (mediana, doc. 34)


def cargar():
    t, p = [], []
    for linea in gzip.open(ARCHIVO, "rt"):
        c = linea.split()
        if len(c) < 7 or int(c[6]) == -9999:
            continue
        utc = datetime(int(c[0]), int(c[1]), int(c[2]), int(c[3]))
        t.append(utc + timedelta(hours=8))                 # hora de China
        p.append(int(c[6]) / 10.0)                         # hPa
    return np.array(t), np.array(p)


def main():
    t, p = cargar()
    t0 = datetime(2016, 7, 20)
    h = np.array([(x - t0).total_seconds() / 3600 for x in t])
    sel = (h >= 0) & (h <= 27 * 24)
    h, p = h[sel], p[sel]
    hh = np.arange(h.min(), h.max() + 1, 1.0)
    ph = np.interp(hh, h, p)                               # horario (lineal entre lecturas de 3 h)
    dpdt = np.gradient(ph, hh)                             # hPa/h
    camp = (hh >= 4 * 24) & (hh < 24 * 24)                 # 24 jul – 12 ago
    # capacidad de bombeo: el aire sale cuando la presión baja; volumen expulsado por hora = V·(−dP/dt)/P
    salida = np.maximum(-dpdt, 0) / ph                     # fracción por hora
    q_pal = V_PALACIO * salida[camp].mean() * 24           # m³/día
    q_cam = V_CAMARA * salida[camp].mean() * 24
    # parte sinóptica (filtro de 24 h) frente a la marea barométrica diaria
    k = np.ones(24) / 24
    psin = np.convolve(ph, k, mode="same")
    dsin = np.gradient(psin, hh)
    q_pal_sin = V_PALACIO * (np.maximum(-dsin, 0) / ph)[camp].mean() * 24
    res = dict(estacion="Jinghe (WMO 57131), 27 km del mausoleo; NOAA ISD-Lite",
               presion_campana_hPa=dict(min=float(p[(h >= 96) & (h < 576)].min()), max=float(p[(h >= 96) & (h < 576)].max()),
                                        desviacion=round(float(ph[camp].std()), 2)),
               variacion_relativa_max_min=round(float((ph[camp].max() - ph[camp].min()) / ph[camp].mean()), 4),
               bombeo_palacio_m3_dia=round(q_pal, 0), bombeo_palacio_solo_sinoptico_m3_dia=round(q_pal_sin, 0),
               bombeo_camara_m3_dia=round(q_cam, 0), caudal_necesario_doc34_m3_dia=Q_NECESARIO,
               cociente_bombeo_palacio_sobre_necesario=round(q_pal / Q_NECESARIO, 2))
    # índice por noche con distintos tiempos de respuesta
    noches = {}
    for tau in (6, 12, 24):
        w = np.exp(-np.arange(0, 5 * tau) / tau)
        w /= w.sum()
        resp = np.convolve(np.maximum(-dpdt, 0), w)[:len(hh)]   # respuesta causal
        for d in range(24, 43 + 1):                              # noches del 24 jul al 12 ago
            # noche del día d de julio (d > 31: agosto): de 20:00 a 06:00, hora de China
            m = (hh >= (d - 20) * 24 + 20) & (hh < (d - 20) * 24 + 30)
            noche = str((datetime(2016, 7, 1) + timedelta(days=d - 1)).date())
            noches.setdefault(noche, {})[f"tau_{tau}h"] = round(float(resp[m].mean()), 4)
    # orden por el índice medio de los tres τ
    media = {n: np.mean(list(v.values())) for n, v in noches.items()}
    orden = sorted(media, key=media.get, reverse=True)
    res["indice_emision_por_noche"] = noches
    res["orden_noches_mas_emision_primero"] = orden
    res["prediccion"] = dict(
        mas_emision=orden[:5], menos_emision=orden[-5:],
        criterio=("Si la tumba respira por bombeo barométrico, el exceso de Hg medido por el lidar en cada noche debe "
                  "correlacionar positivamente (Spearman > 0, p < 0,05 si hay ≥ 10 noches) con este índice. Si la fuente es "
                  "superficial o el lidar no está limitado por la fuente, no debe haber correlación una vez descontado el viento."))
    with open(os.path.join(RAIZ, "resultados", "43_qin_prerregistro.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in res.items() if k != "indice_emision_por_noche"}, indent=1, ensure_ascii=False))
    # serie para inspección
    print("presión diaria media (hPa):", [round(float(ph[(hh >= d * 24) & (hh < d * 24 + 24)].mean()), 1) for d in range(4, 24)])


if __name__ == "__main__":
    main()
