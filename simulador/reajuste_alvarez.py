"""Reanálisis de Alvarez (1970) desde las cuentas en bruto (figs. 8 y 9), con un modelo moderno.

1. Ajuste: N_pred = m_k · exp(Σ c_j b_j(θ, φ)), con m_k el flujo de nuestro modelo (pirámide de
   Kefrén, detector en la posición de Alvarez, rejilla uniforme en ángulo; exclusion_alvarez.py)
   y b_j polinomios de grado D en (θ, φ): la aceptancia y la eficiencia desconocidas del detector
   de 1969. Máxima verosimilitud de Poisson en las 801 casillas de la fig. 10.
2. Residuos propios z = (N8 − N_pred)/√N_pred, comparados con los de Alvarez (fig. 10).
3. Exclusión: para cada posición de una cámara (que quepa entera), Δχ² perfilado sobre los
   parámetros de la corrección (proyección lineal): Δχ² = (|P⊥(r − s)|² − |P⊥ r|²)/κ.
4. Significación global del mejor candidato con nulas correlacionadas calibradas en nuestros
   propios residuos.

Plantilla: 'modelo' (nuestro flujo; no reproduce las zonas muertas del detector de 1969 y ajusta mal)
o 'alvarez' (su predicción, fig. 9, que ya incluye instrumento y pirámide; nuestro modelo solo da la
huella relativa de cada cámara).

Uso: PYTHONPATH=. python reajuste_alvarez.py [grado] [plantilla] → ../resultados/34_reajuste_alvarez_*.json
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

import exclusion_alvarez as ea
import reanalisis_alvarez as ra
from piramide import cobertura as cb
from piramide import kefren as kf

RAIZ = ra.RAIZ
DAT = os.path.join(RAIZ, "datos", "alvarez_1970")


def cargar():
    N8 = np.loadtxt(os.path.join(DAT, "fig8_medidos.csv"), delimiter=",", comments="#")
    N9 = np.loadtxt(os.path.join(DAT, "fig9_predichos.csv"), delimiter=",", comments="#")
    r10, _ = ra.cargar()
    return N8.reshape(-1), N9.reshape(-1), ~np.isnan(r10.reshape(-1))


def base(grado):
    i, j = np.meshgrid(np.arange(30), np.arange(30), indexing="ij")
    u = ((45 + 3 * i + 1.5) - 90) / 45.0      # θ: norte (−) → sur (+)
    w = ((45 + 3 * j + 1.5) - 90) / 45.0      # φ: oeste (−) → este (+)
    cols = [u ** a * w ** b for a in range(grado + 1) for b in range(grado + 1 - a)]
    return np.stack([c.reshape(-1) for c in cols], 1)


def ajustar(N, m, B, v):
    """Máxima verosimilitud de Poisson para N ~ m·exp(B c) en las casillas v."""
    lm = np.log(np.maximum(m, 1e-12))

    def nll(c):
        eta = lm[v] + B[v] @ c
        return float(np.sum(np.exp(eta) - N[v] * eta))

    def grad(c):
        mu = np.exp(lm[v] + B[v] @ c)
        return B[v].T @ (mu - N[v])

    c0 = np.zeros(B.shape[1])
    c0[0] = math.log(N[v].sum() / m[v].sum())
    r = minimize(nll, c0, jac=grad, method="L-BFGS-B")
    return r.x, m * np.exp(B @ r.x)


def main():
    grado = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    plantilla = sys.argv[2] if len(sys.argv) > 2 else "alvarez"
    N8, N9, v = cargar()
    origen = kf.ORIGEN_ALVAREZ.copy()
    ky, _ = ea.ajustar_ky(origen)
    A = ea.Alvarez(origen, 0, ky)
    m = A.N0.copy() if plantilla == "modelo" else np.maximum(N9.astype(float), 0.5)
    B = base(grado)
    c, pred = ajustar(N8, m, B, v)
    z = np.where(v, (N8 - pred) / np.sqrt(np.maximum(pred, 1e-9)), np.nan)
    chi2 = float(np.nansum(z ** 2))
    ndf = int(v.sum() - B.shape[1])
    z_alv = np.where(v, (N8 - N9) / np.sqrt(np.maximum(N9, 1)), np.nan)
    corr = float(np.corrcoef(z[v], z_alv[v])[0, 1])
    M = z.reshape(30, 30)
    res = dict(plantilla=plantilla, grado=grado, n_parametros=int(B.shape[1]), chi2=round(chi2, 1), ndf=ndf,
               chi2_alvarez_recalculado=round(float(np.nansum(z_alv ** 2)), 1),
               correlacion_con_residuos_alvarez=round(corr, 3), moran=round(ra.moran(M), 3),
               cuentas_medidas=int(N8[v].sum()))
    print(json.dumps(res, ensure_ascii=False), flush=True)
    # --- exclusión con perfil sobre la corrección suave
    sq = np.sqrt(np.maximum(pred, 1e-9))
    J = (sq[:, None] * B)[v]                       # ∂z/∂c (signo irrelevante para la proyección)
    Q, _ = np.linalg.qr(J)

    def perp(x):
        return x - Q @ (Q.T @ x)

    r_p = perp(z[v])
    kappa = float(np.mean(z[v] ** 2))
    P = kf.voxeles(8.0)
    en_cono = np.array([kf.fraccion_en_cono(q[None]) for q in P]) > 0
    salida = {}
    for nombre, f in (("camara_tipo_rey", kf.camara_del_rey), ("cubo_8m", lambda q: cb.cubo(q, 8.0))):
        Q_ok = np.array([ea.cabe(f(q)) for q in P])
        S = []
        for q in P[Q_ok]:
            h = A.huella(f(q))                     # dN/√N0 en unidades del modelo
            rel = np.where(A.N0 > 0, h / np.sqrt(np.maximum(A.N0, 1e-12)), 0.0)   # ΔN/N
            S.append(perp((rel * sq)[v]))          # ΔN_pred/√N_pred, sin la parte absorbible
        S = np.array(S)
        d = (np.sum((r_p[None, :] - S) ** 2, 1) - np.sum(r_p ** 2)) / kappa
        cono = en_cono[Q_ok]
        i = int(np.argmin(d))
        # nula correlada calibrada en nuestros residuos
        rng = np.random.default_rng(34)
        cal = ra.calibrar_nula(np.round(M), rng)
        mins = []
        vv = v.reshape(30, 30)
        for _ in range(2000):
            Rn = ra.campo_correlado(vv, cal["sigma_nucleo_bins"], float(np.nanstd(M)) * cal["escala"], rng,
                                    cal["fraccion_correlada"], 0.0).reshape(-1)[v]
            Rp = perp(Rn)
            mins.append(((np.sum((Rp[None, :] - S) ** 2, 1) - np.sum(Rp ** 2)) / kappa).min())
        mins = np.array(mins)
        p = float(np.mean(mins <= d[i]))
        salida[nombre] = dict(posiciones=int(Q_ok.sum()), excluido_95=float(np.mean(d >= 3.84)),
                              excluido_5s=float(np.mean(d >= 25)),
                              dentro_cono_95=float(np.mean(d[cono] >= 3.84)), dentro_cono_5s=float(np.mean(d[cono] >= 25)),
                              fuera_cono_95_sobre_total=float(np.mean((d >= 3.84) & ~cono)),
                              minimo_dchi2=round(float(d[i]), 2), donde_minimo=[round(float(x), 1) for x in P[Q_ok][i]],
                              p_global=p, sigma_global_una_cola=round(float(norm.isf(max(p, 1e-6))), 2))
        print(nombre, json.dumps(salida[nombre], ensure_ascii=False), flush=True)
    res["exclusion"] = salida
    res["kappa"] = round(kappa, 3)
    with open(os.path.join(RAIZ, "resultados", f"34_reajuste_alvarez_{plantilla}_grado{grado}.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)
    np.save(os.path.join(RAIZ, "resultados", f"34_residuos_{plantilla}_grado{grado}.npy"), M)


if __name__ == "__main__":
    main()
