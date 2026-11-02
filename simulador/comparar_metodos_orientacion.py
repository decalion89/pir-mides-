"""¿Un método o un cambio de método? Comparación de modelos para los errores de orientación de la
dinastía IV (Spence 2000, tabla 1; fechas de piramide/orientacion.py).

Modelos (σ_e = error de ejecución libre; cada pirámide con su error de medida):
  A  constante + ruido                          (k = 2)
  B  solo gnomon: sistemático en [−5,8′, +5,8′] (uniforme, doc. 26) + ruido   (k = 1)
  C  deriva lineal en el tiempo (como un método estelar) + ruido             (k = 3)
  D  deriva lineal en Meidum, Acodada y Roja; gnomon desde Keops + ruido      (k = 3)
Se maximiza la verosimilitud y se comparan AICc y BIC. Además, validación cruzada dejando una
pirámide fuera (log-verosimilitud predictiva), que penaliza el sobreajuste sin fórmulas.

Uso: PYTHONPATH=. python comparar_metodos_orientacion.py → ../resultados/33_metodos_orientacion.json
"""
import json
import math
import os

import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

from piramide.orientacion import PIRAMIDES

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIM = 5.8
NOM = [p[0] for p in PIRAMIDES]
E = np.array([p[1] for p in PIRAMIDES])
S = np.array([p[2] for p in PIRAMIDES])
T = -np.array([p[3] for p in PIRAMIDES], float)      # años (a. C. negativos)
T = T - T.mean()
SOLAR_DESDE = NOM.index("Keops")


def ll_gnomon(e, s):
    """log p(e) con e = u + n, u ~ U(−LIM, LIM), n ~ N(0, s²)."""
    p = (norm.cdf((LIM - e) / s) - norm.cdf((-LIM - e) / s)) / (2 * LIM)
    return np.log(np.maximum(p, 1e-300))


def ll(model, th, idx):
    e, s, t = E[idx], S[idx], T[idx]
    se = abs(th[-1]) + 1e-6
    tot = np.sqrt(s ** 2 + se ** 2)
    if model == "A":
        return norm.logpdf(e, th[0], tot).sum()
    if model == "B":
        return ll_gnomon(e, tot).sum()
    if model == "C":
        return norm.logpdf(e, th[0] + th[1] * t, tot).sum()
    if model == "D":
        est = np.array([i < SOLAR_DESDE for i in idx])
        a = norm.logpdf(e[est], th[0] + th[1] * t[est], tot[est]).sum()
        b = ll_gnomon(e[~est], tot[~est]).sum()
        return a + b


K = {"A": 2, "B": 1, "C": 3, "D": 3}
INI = {"A": [0, 5], "B": [5], "C": [0, 0.3, 3], "D": [0, 0.3, 3]}


def ajustar(model, idx):
    best = None
    for f in (0.5, 1, 2, 4):
        x0 = np.array(INI[model], float) * np.array([1] * (len(INI[model]) - 1) + [f])
        r = minimize(lambda th: -ll(model, th, idx), x0, method="Nelder-Mead",
                     options=dict(maxiter=4000, xatol=1e-6, fatol=1e-8))
        if best is None or r.fun < best.fun:
            best = r
    return best


def main():
    n = len(E)
    todos = np.arange(n)
    res = dict(piramides=NOM, errores=E.tolist(), modelos={})
    for m in "ABCD":
        r = ajustar(m, todos)
        lmax = -r.fun
        k = K[m]
        aicc = -2 * lmax + 2 * k + (2 * k * (k + 1) / (n - k - 1) if n - k - 1 > 0 else float("inf"))
        bic = -2 * lmax + k * math.log(n)
        # validación cruzada dejando una fuera
        loo = 0.0
        for i in range(n):
            tr = np.array([j for j in range(n) if j != i])
            th = ajustar(m, tr).x
            loo += ll(m, th, np.array([i]))
        res["modelos"][m] = dict(k=k, logL=round(lmax, 2), AICc=round(aicc, 2), BIC=round(bic, 2),
                                 loo_logpred=round(float(loo), 2),
                                 parametros=[round(float(x), 3) for x in r.x],
                                 sigma_ejecucion=round(abs(float(r.x[-1])), 2))
        print(m, res["modelos"][m])
    with open(os.path.join(RAIZ, "resultados", "33_metodos_orientacion.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
