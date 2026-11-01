"""¿Qué parámetro del instrumento KEK reconcilia sus datos con las emulsiones (tensión Δχ² ≈ 66–70)?

Los cocientes de KEK son "datos / simulación", así que las estructuras conocidas se cancelan y la
posición absoluta del detector solo entra a través del propio Vacío. Por eso un desplazamiento
común de H1 y H2 equivale a desplazar el Vacío visto por KEK. Se prueban, de uno en uno y en el
ajuste conjunto con las emulsiones (corredor con posición, tamaño e inclinación libres):
  - desplazamiento común este-oeste (px) y vertical (pz) de los hodoscopios;
  - separación H1–H2 (nominal 2,9 m): fija la paralaje y la altura del Vacío;
  - escala angular k: separación entre planos ×k (nominal 1,5 m y 1,0 m).
Para cada valor: χ² de KEK sola, χ² conjunto y tensión = conjunto − emulsiones solas (78) − KEK sola.

    cd simulador && PYTHONPATH=. python sistematicos_kek.py → ../resultados/40_sistematicos_kek.json
"""
import json
import time

import numpy as np
from scipy.optimize import minimize

from piramide import reanalisis as ra, reanalisis_emulsiones as re_

S_E, S_K = 3.9, 1.69
CHI_E_SOLO = 78.0
POS = np.array([7.1, -1.9, 21.5])
SEP0 = dict(ra.SEPARACION)
B0 = ra.SEP_H1_H2
t0 = time.time()
E = re_.Emulsiones(x_ne1=13.0, x_ne2=3.0)
INICIOS = [(7.2, 18.9, 56.8, 40.4, 2.7, 4.1, 16.0), (7.3, 17.0, 62.0, 34.0, 2.5, 3.5, 3.0), (8.0, 23.5, 50.6, 53.3, 2.5, 3.7, 24.0)]


def kek(px=0.0, pz=0.0, base=B0, k=1.0):
    ra.SEPARACION.update({d: v * k for d, v in SEP0.items()})
    ra.SEP_H1_H2 = base
    try:
        return ra.Reanalisis(pos_h1=tuple(POS + np.array([px, 0.0, pz])))
    finally:
        ra.SEPARACION.update(SEP0)
        ra.SEP_H1_H2 = B0


def pen(v):
    lims = [(-10, 45), (40, 85), (10, 70), (0.5, 15), (0.8, 8), (-20, 45)]
    return sum(100 * (max(lo - x, 0) + max(x - hi, 0)) ** 2 for x, (lo, hi) in zip(v[1:], lims))


def corr(v):
    x, y, z, L, h, w, a = v
    return ra.Corredor(x, y, z, L, h, ancho=w, inclinacion=a)


def ajuste(f):
    best = None
    for ini in INICIOS:
        r = minimize(f, np.array(ini, float), method="Nelder-Mead", options=dict(maxiter=900, xatol=0.01, fatol=0.01))
        if best is None or r.fun < best.fun:
            best = r
    return float(best.fun), [round(float(x), 2) for x in best.x]


def evaluar(nombre, valor, K):
    ck, pk = ajuste(lambda v: K.chi2(corr(v)) / S_K + pen(v))
    cj, pj = ajuste(lambda v: E.chi2_vacio([corr(v)], sigma=0.03) / S_E + K.chi2(corr(v)) / S_K + pen(v))
    ce = E.chi2_vacio([corr(pj)], sigma=0.03) / S_E
    ck = min(ck, cj - ce)                      # protege frente a mínimos locales del ajuste solo
    f = dict(parametro=nombre, valor=valor, chi2_kek_solo=round(ck, 1), params_kek_solo=pk,
             chi2_conjunto=round(cj, 1), chi2_conjunto_emulsiones=round(ce, 1), params_conjunto=pj,
             tension=round(cj - CHI_E_SOLO - ck, 1))
    print(json.dumps(f, ensure_ascii=False), f"{time.time() - t0:.0f}s", flush=True)
    return f


def main():
    filas = [evaluar("nominal", 0.0, kek())]
    for px in (-2.5, -2.0, -1.5, -1.0, -0.5, 0.5, 1.0):
        filas.append(evaluar("px_m", px, kek(px=px)))
    for pz in (-1.0, -0.5, 0.5, 1.0, 2.0):
        filas.append(evaluar("pz_m", pz, kek(pz=pz)))
    for b in (2.3, 2.6, 3.2, 3.5, 4.0):
        filas.append(evaluar("separacion_H1_H2_m", b, kek(base=b)))
    for k in (0.85, 0.9, 0.95, 1.05, 1.1, 1.15):
        filas.append(evaluar("escala_angular_k", k, kek(k=k)))
    json.dump(dict(chi2_emulsiones_solas=CHI_E_SOLO, posicion_h1_nominal=POS.tolist(), separacion_nominal=B0,
                   separacion_planos_nominal=SEP0, filas=filas),
              open("../resultados/40_sistematicos_kek.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
