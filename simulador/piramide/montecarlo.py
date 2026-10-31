"""Monte Carlo sobre los parámetros inciertos: ¿qué modelos son viables?"""
from __future__ import annotations

import math

import numpy as np

from . import geometria as g
from .fisica import Parametros, RANGOS
from .obra import simular, personas_para
from .rampas import catalogo

CRITERIO_ANIOS = 20.0          # obra principal (reinado de Keops ~23-27 años: margen)
CRITERIO_PERSONAS = 25000.0    # estimación alta de la mano de obra (Lehner, Hawass)
CRITERIO_VOLUMEN_AUX = 0.5     # rampas de más de la mitad del volumen de la pirámide: no


def ejecutar(n: int = 600, semilla: int = 2026) -> dict:
    rng = np.random.default_rng(semilla)
    base = Parametros()
    modelos = catalogo()
    muestras = [base.muestrear(rng) for _ in range(n)]
    out = {}
    for m in modelos:
        anios, pers, vaux = [], [], []
        for p in muestras:
            r = simular(m, p, CRITERIO_PERSONAS)
            anios.append(r.anios)
            vaux.append(r.volumen_aux / g.VOLUMEN_TOTAL)
            pers.append(personas_para(m, p, CRITERIO_ANIOS))
        anios, pers, vaux = map(np.array, (anios, pers, vaux))
        viable = (anios <= CRITERIO_ANIOS) & (vaux <= CRITERIO_VOLUMEN_AUX)
        out[m.clave] = dict(
            nombre=m.nombre,
            anios=anios, personas=pers, vaux=vaux,
            p_viable=float(viable.mean()),
            anios_med=float(np.median(anios)),
            anios_p10=float(np.percentile(anios, 10)),
            anios_p90=float(np.percentile(anios, 90)),
            personas_med=float(np.median(pers)),
            vaux_med=float(np.median(vaux)),
        )
    out["_muestras"] = muestras
    return out


def sensibilidad(res_modelo: dict, muestras: list[Parametros]) -> dict[str, float]:
    """Correlación de rangos de Spearman entre cada parámetro y los años de obra."""
    y = res_modelo["anios"]
    ry = np.argsort(np.argsort(y))
    s = {}
    for k in RANGOS:
        x = np.array([getattr(p, k) for p in muestras])
        rx = np.argsort(np.argsort(x))
        c = np.corrcoef(rx, ry)[0, 1]
        s[k] = float(c) if np.isfinite(c) else 0.0
    return dict(sorted(s.items(), key=lambda kv: -abs(kv[1])))
