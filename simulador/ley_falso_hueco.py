"""¿Cuánta precisión de posición necesita un detector de muones para no inventar cavidades?

Experimento numérico (sin datos reales): se generan cuentas esperadas (Asimov) de la pirámide de
Kefrén SIN ninguna cámara, vistas desde el detector en su posición verdadera, con N muones en
total. Se analizan con el modelo colocado a una distancia δ (en una dirección dada) y con las
mismas molestias que en docs/27: aceptancia separable (filas y columnas) y dos términos
radiales, perfilados. Se busca la cámara del tamaño de la del Rey que más "mejora" el ajuste
(Δχ² mínimo) en una rejilla de posiciones dentro del cono de 35°.

Hipótesis: Δχ²_falso ≈ −k · N · δ², es decir, la precisión necesaria es δ_max ∝ N^(−1/2).

Uso: PYTHONPATH=. python ley_falso_hueco.py → ../resultados/36_ley_falso_hueco.json
"""
from __future__ import annotations

import json
import os

import numpy as np

import exclusion_alvarez as ea
from piramide import kefren as kf

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O_VERDAD = np.array([15.5, 4.0, -0.5])


def mapa(o):
    A = ea.Alvarez(np.asarray(o, float), 0, 1.0)
    return A, np.maximum(A.N0.reshape(30, 30), 1e-9)


def diseno(V, r2):
    filas = np.where(V.any(1))[0]
    cols = np.where(V.any(0))[0]
    idx = np.argwhere(V)
    X = np.zeros((len(idx), len(filas) + len(cols) - 1 + 2))
    for k, (a, b) in enumerate(idx):
        X[k, list(filas).index(a)] = 1
        jb = list(cols).index(b)
        if jb > 0:
            X[k, len(filas) + jb - 1] = 1
        X[k, -2] = r2[a, b]
        X[k, -1] = r2[a, b] ** 2
    return X


def ajustar(y, m, X):
    lm = np.log(m)
    beta = np.zeros(X.shape[1])
    nf = int((X[:, :-2].sum(0) > 0).sum())          # columnas de filas + columnas
    filas = [c for c in range(X.shape[1] - 2) if np.all(np.isin(X[:, c], (0, 1)))][:1]
    beta[:] = 0.0
    beta[np.argmax(X[:, :X.shape[1] - 2].sum(0))] = 0.0
    lm = lm + np.log(y.sum() / m.sum())             # arranque normalizado
    for _ in range(80):
        eta = lm + X @ beta
        mu = np.exp(eta)
        zz = eta - lm + (y - mu) / mu
        beta = np.linalg.lstsq(X * np.sqrt(mu)[:, None], zz * np.sqrt(mu), rcond=None)[0]
    return np.exp(lm + X @ beta)


def main():
    i, j = np.meshgrid(np.arange(30), np.arange(30), indexing="ij")
    th = np.radians(45 + 3 * i + 1.5 - 90)
    ph = np.radians(45 + 3 * j + 1.5 - 90)
    r2 = np.tan(th) ** 2 + np.tan(ph) ** 2
    V = np.sqrt(r2) < 0.7
    X = diseno(V, r2)
    A0, m0 = mapa(O_VERDAD)
    P = kf.voxeles(8.0)
    en_cono = np.array([kf.fraccion_en_cono(q[None], origen=O_VERDAD) for q in P]) > 0
    puntos = [q for q, c in zip(P, en_cono) if c and ea.cabe(kf.camara_del_rey(q))]
    # huellas relativas (cambio de flujo) desde la posición verdadera
    REL = []
    for q in puntos:
        h = A0.huella(kf.camara_del_rey(q))
        REL.append(np.where(A0.N0 > 0, h / np.sqrt(np.maximum(A0.N0, 1e-12)), 0.0).reshape(30, 30)[V])
    REL = np.array(REL)
    res = dict(origen_verdadero=O_VERDAD.tolist(), posiciones=len(puntos), casos=[])
    for Ntot in (6.5e5, 6.5e6, 6.5e7):
        verdad = m0 / m0[V].sum() * Ntot
        y = verdad[V]
        for direccion, u in (("este", (1, 0, 0)), ("norte", (0, 1, 0)), ("abajo", (0, 0, -1))):
            for d in (0.25, 0.5, 1.0, 2.0, 3.5):
                _, md = mapa(O_VERDAD + d * np.array(u, float))
                mu = ajustar(y, md[V], X)
                z = (y - mu) / np.sqrt(mu)
                Q, _ = np.linalg.qr(X * np.sqrt(mu)[:, None])
                perp = lambda x: x - Q @ (Q.T @ x)
                rp = perp(z)
                S = np.array([perp(rel * np.sqrt(mu)) for rel in REL])
                dchi = np.sum((rp[None, :] - S) ** 2, 1) - np.sum(rp ** 2)
                k = int(np.argmin(dchi))
                caso = dict(N=Ntot, direccion=direccion, delta_m=d, chi2_fondo=round(float(np.sum(z ** 2)), 1),
                            dchi2_falso=round(float(dchi[k]), 2), donde=[round(float(x), 1) for x in puntos[k]])
                res["casos"].append(caso)
                print(caso, flush=True)
    # ajuste de la ley: −Δχ² = k · N · δ^a  (por dirección)
    ley = {}
    for direccion in ("este", "norte", "abajo"):
        c = [x for x in res["casos"] if x["direccion"] == direccion and x["dchi2_falso"] < -0.5]
        if len(c) >= 4:
            A = np.c_[np.ones(len(c)), np.log([x["N"] for x in c]), np.log([x["delta_m"] for x in c])]
            b = np.linalg.lstsq(A, np.log([-x["dchi2_falso"] for x in c]), rcond=None)[0]
            ley[direccion] = dict(exponente_N=round(float(b[1]), 3), exponente_delta=round(float(b[2]), 3),
                                  k=float(np.exp(b[0])),
                                  delta_max_para_falso_5sigma_m={f"{N:.0e}": round(float((25 / (np.exp(b[0]) * N)) ** (1 / b[2])), 3)
                                                                  for N in (6.5e5, 1e8, 1e10)})
    res["ley"] = ley
    print(json.dumps(ley, indent=1))
    with open(os.path.join(RAIZ, "resultados", "36_ley_falso_hueco.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
