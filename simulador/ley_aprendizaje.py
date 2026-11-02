"""¿Siguió la construcción de pirámides una "ley de aprendizaje" (ley de Wright)?

Datos: volumen de cada pirámide del Reino Antiguo (lista de pirámides egipcias, Wikipedia,
basada en Lehner 1997 y Verner 2001) y duración del reinado con su intervalo según las
cronologías habituales (Canon de Turín, recuentos de ganado, Manetón; ver docs/23). El ritmo
R = V/T (m³/año) es una COTA INFERIOR del ritmo real, porque la obra pudo durar menos que el reinado.

Modelos para R frente a la experiencia acumulada C (volumen construido antes, más la mitad del
propio):
- Wright:  log R = a + b·log C                    (el ritmo crece con la experiencia)
- techo:   R = Rmax·C/(C + C½)                     (aprendizaje que se satura)
- constante: R = R0

Se ajustan a las pirámides de Djoser a Khafre (la fase de crecimiento) por Monte Carlo sobre
las duraciones de los reinados (uniformes en su intervalo), y se compara con AIC corregido. Las
dinastías V y VI se usan después como prueba: ¿sigue la tendencia o se rompe?

Uso: PYTHONPATH=. python ley_aprendizaje.py → ../resultados/28_ley_aprendizaje.json
"""
from __future__ import annotations

import json
import math
import os

import numpy as np
from scipy.optimize import curve_fit

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# rey, volumen total en su reinado (m³), duración del reinado (mín, máx) en años, terminada
REINADOS = [
    ("Djoser", 330_400, (19, 29), True),
    ("Sekhemkhet", 33_600, (6, 7), False),
    ("Khaba", 47_040, (6, 8), False),
    ("Snefru", 638_733 + 1_237_040 + 1_694_000, (24, 48), True),
    ("Keops", 2_583_283, (23, 27), True),
    ("Djedefra", 131_043, (8, 11), False),
    ("Kefrén", 2_211_096, (24, 26), True),
    ("Micerino", 235_183, (18, 28), True),
    ("Userkaf", 87_906, (7, 8), True),
    ("Sahure", 96_542, (12, 14), True),
    ("Neferirkara", 257_250, (10, 20), True),
    ("Niuserra", 112_632, (24, 35), True),
    ("Djedkara", 107_835, (33, 44), True),
    ("Unas", 47_390, (15, 30), True),
    ("Teti", 107_835, (12, 33), True),
    ("Pepi I", 107_835, (25, 50), True),
    ("Merenra", 107_835, (6, 11), True),
    ("Pepi II", 107_835, (64, 94), True),
]
FASE_CRECIMIENTO = ("Djoser", "Snefru", "Keops", "Kefrén")


def acumulado():
    C, prev = {}, 0.0
    for rey, V, _, _ in REINADOS:
        C[rey] = prev + V / 2
        prev += V
    return C


def aicc(rss, n, k):
    if n - k - 1 <= 0:
        return float("nan")
    return n * math.log(rss / n) + 2 * k + 2 * k * (k + 1) / (n - k - 1)


def main(n_mc=20000, semilla=4600):
    rng = np.random.default_rng(semilla)
    C = acumulado()
    tabla = []
    for rey, V, (t0, t1), fin in REINADOS:
        tabla.append(dict(rey=rey, volumen_m3=V, reinado=[t0, t1], terminada=fin,
                          ritmo_m3_ano=[round(V / t1), round(V / t0)],
                          experiencia_acumulada_m3=round(C[rey])))
    idx = [i for i, r in enumerate(REINADOS) if r[0] in FASE_CRECIMIENTO]
    x = np.array([C[REINADOS[i][0]] for i in idx])
    b_wright, aic_w, aic_t, aic_c, rmax, chalf = [], [], [], [], [], []
    for _ in range(n_mc):
        T = np.array([rng.uniform(*REINADOS[i][2]) for i in idx])
        R = np.array([REINADOS[i][1] for i in idx]) / T
        lx, ly = np.log(x), np.log(R)
        A = np.c_[np.ones_like(lx), lx]
        coef, *_ = np.linalg.lstsq(A, ly, rcond=None)
        rss_w = float(np.sum((ly - A @ coef) ** 2))
        b_wright.append(coef[1])
        try:
            p, _ = curve_fit(lambda c, rm, ch: np.log(rm * c / (c + ch)), x, ly, p0=(1e5, 3e5),
                             bounds=((1e3, 1e3), (1e7, 1e8)), maxfev=5000)
            rss_t = float(np.sum((ly - np.log(p[0] * x / (x + p[1]))) ** 2))
            rmax.append(p[0])
            chalf.append(p[1])
        except Exception:
            rss_t = np.nan
        rss_c = float(np.sum((ly - ly.mean()) ** 2))
        n = len(ly)
        aic_w.append(aicc(rss_w, n, 2))
        aic_t.append(aicc(rss_t, n, 2))
        aic_c.append(aicc(rss_c, n, 1))
    b = np.array(b_wright)
    aw, at, ac = map(np.array, (aic_w, aic_t, aic_c))
    ok = np.isfinite(at)
    # ¿qué predice cada modelo para las dinastías V–VI (experiencia aún mayor)?
    post = [r for r in REINADOS if r[0] not in FASE_CRECIMIENTO and REINADOS.index(r) > 7]
    xr = np.array([C[r[0]] for r in post])
    obs = np.array([[r[1] / r[2][1], r[1] / r[2][0]] for r in post])
    b_med = float(np.median(b))
    res = dict(
        tabla=tabla,
        fase_crecimiento=list(FASE_CRECIMIENTO),
        wright_exponente_b=dict(mediana=round(b_med, 3), p05=round(float(np.percentile(b, 5)), 3),
                                p95=round(float(np.percentile(b, 95)), 3),
                                tasa_aprendizaje_por_duplicacion=round(1 - 2 ** (-b_med), 3)),
        techo=dict(Rmax_m3_ano_mediana=round(float(np.median(rmax))),
                   Rmax_p05=round(float(np.percentile(rmax, 5))), Rmax_p95=round(float(np.percentile(rmax, 95))),
                   C_mitad_mediana=round(float(np.median(chalf)))),
        nota_aic="n = 4 puntos: con tan pocos datos el AICc solo distingue diferencias grandes",
        fraccion_mc_mejor_modelo=dict(
            wright=float(np.mean((aw < at) & (aw < ac))),
            techo=float(np.mean(ok & (at < aw) & (at < ac))),
            constante=float(np.mean((ac < aw) & (ac < at)))),
        prueba_dinastias_V_VI=dict(
            reyes=[r[0] for r in post],
            ritmo_observado_rango=[[round(a), round(b_)] for a, b_ in obs],
            ritmo_predicho_techo=round(float(np.median(rmax))),
            caida_respecto_al_techo=[round(float(np.median(rmax)) / ((a + b_) / 2), 1) for a, b_ in obs]),
    )
    with open(os.path.join(RAIZ, "resultados", "28_ley_aprendizaje.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)
    print(json.dumps({k: v for k, v in res.items() if k != "tabla"}, indent=1, ensure_ascii=False))
    for t in tabla:
        print(f"{t['rey']:12s} V={t['volumen_m3']:>9,} T={t['reinado']} R={t['ritmo_m3_ano']} C={t['experiencia_acumulada_m3']:,}")


if __name__ == "__main__":
    main()
