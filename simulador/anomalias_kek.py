"""¿Hay algo más en los datos de KEK de 2017 además del Gran Vacío? Búsqueda en los residuos.

Se toma el mejor ajuste del Gran Vacío (corredor inclinado 26°, con la posición del detector
libre; resultados/08) y se buscan agrupaciones de puntos consecutivos con exceso (posible hueco)
o déficit (más densidad) en los residuos normalizados r = (dato − ajuste)/σ.

Precauciones:
- el artefacto en cruz del hodoscopio (Morishima et al. 2017, Métodos: canales centrales) se
  enmascara: |Δx| ≤ 2 canales;
- los residuos están correlacionados a lo largo de cada corte; la hipótesis nula es un proceso
  AR(1) gaussiano por corte con la misma autocorrelación y dispersión que los datos;
- la significación es GLOBAL: se compara el máximo observado con el máximo de cada simulación,
  buscando en todos los cortes, posiciones y anchuras (3–10 puntos).

Uso: PYTHONPATH=. python anomalias_kek.py → ../resultados/29_anomalias_kek.json
"""
from __future__ import annotations

import json
import os

import numpy as np

from piramide import reanalisis as ra

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANCHURAS = range(3, 11)
MASCARA_DX = 2.0


def residuos():
    b = json.load(open(os.path.join(RAIZ, "resultados", "08_reanalisis_kek_incl.json")))["26"]
    p, det = b["params"], b["detector"]
    r = ra.Reanalisis(pos_h1=(7.1 + det[0], -1.9 + det[1], 21.5 + det[2]))
    c = ra.Corredor(p[0], p[1], p[2], p[3], p[4], ancho=p[5], inclinacion=26.0)
    chi, pred = r.chi2(c, devolver_ajuste=True)
    d = r.d
    s = np.sqrt(d["err"] ** 2 + (ra.F_SIS * d["val"]) ** 2)
    return r, (d["val"] - pred) / s, chi


def cortes(r, z):
    """Lista de (clave, índices ordenados por Δx, residuos) con la máscara aplicada."""
    d = r.d
    out = []
    for k, (det, dy0) in enumerate(r.cortes):
        i = np.where((r.id_corte == k) & (np.abs(d["dx"]) > MASCARA_DX))[0]
        i = i[np.argsort(d["dx"][i])]
        out.append(((det, int(dy0)), i, z[i]))
    return out


def max_ventana(series, signo=1):
    mejor = (-np.inf, None)
    for clave, idx, x in series:
        for w in ANCHURAS:
            if len(x) < w:
                continue
            cs = np.concatenate([[0], np.cumsum(signo * x)])
            s = (cs[w:] - cs[:-w]) / np.sqrt(w)
            j = int(np.argmax(s))
            if s[j] > mejor[0]:
                mejor = (float(s[j]), (clave, int(idx[j]), int(idx[j + w - 1]), w))
    return mejor


def ar1(series):
    rho, sd = [], []
    for _, _, x in series:
        if len(x) > 3:
            rho.append(np.corrcoef(x[:-1], x[1:])[0, 1])
            sd.append(np.std(x))
    return float(np.mean(rho)), float(np.mean(sd))


def simular(series, rho, sd, rng):
    sim = []
    for clave, idx, x in series:
        e = rng.normal(size=len(x))
        y = np.empty(len(x))
        y[0] = e[0]
        for t in range(1, len(x)):
            y[t] = rho * y[t - 1] + np.sqrt(1 - rho ** 2) * e[t]
        sim.append((clave, idx, y * sd))
    return sim


def main(n_sim=5000, semilla=2017):
    rng = np.random.default_rng(semilla)
    r, z, chi = residuos()
    S = cortes(r, z)
    rho, sd = ar1(S)
    exc, dfc = max_ventana(S, 1), max_ventana(S, -1)
    nul_e = np.empty(n_sim)
    nul_d = np.empty(n_sim)
    for k in range(n_sim):
        sim = simular(S, rho, sd, rng)
        nul_e[k] = max_ventana(sim, 1)[0]
        nul_d[k] = max_ventana(sim, -1)[0]
    d = r.d

    def describir(m, nul):
        (det, dy0), i0, i1, w = m[1]
        sep = ra.SEPARACION[det]
        return dict(valor=round(m[0], 2), p_global=float(np.mean(nul >= m[0])),
                    detector=det, corte_dy=[int(dy0), int(d["dy1"][i0])],
                    tan_x=[round(d["dx"][i0] * ra.CANAL / sep, 3), round(d["dx"][i1] * ra.CANAL / sep, 3)],
                    tan_y=[round(dy0 * ra.CANAL / sep, 3), round((d["dy1"][i0] + 1) * ra.CANAL / sep, 3)],
                    puntos=w)

    # robustez: sin el primer corte de cada detector (donde cae la rama Δy = 0 del artefacto)
    S2 = [s for s in S if s[0][1] != min(c[0][1] for c in S if c[0][0] == s[0][0])]
    exc2, dfc2 = max_ventana(S2, 1), max_ventana(S2, -1)
    res = dict(chi2_ajuste=round(chi, 1), n_puntos=int(sum(len(s[1]) for s in S)),
               autocorrelacion_lag1=round(rho, 3), dispersion=round(sd, 3),
               exceso=describir(exc, nul_e), deficit=describir(dfc, nul_d),
               sin_primer_corte=dict(exceso=round(exc2[0], 2), deficit=round(dfc2[0], 2)),
               nulo_percentiles_exceso={q: round(float(np.percentile(nul_e, q)), 2) for q in (50, 95, 99)},
               n_sim=n_sim)
    with open(os.path.join(RAIZ, "resultados", "29_anomalias_kek.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))
    np.save(os.path.join(RAIZ, "resultados", "29_residuos_kek.npy"), z)


if __name__ == "__main__":
    main()
