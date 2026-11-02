"""¿Desde dónde y a qué distancia se podría ver el Gran Vacío?

1. Posteriores de la geometría del Vacío (corredor recto: x, y, z, largo, alto, ancho,
   inclinación) con Metropolis adaptativo, a partir de los datos publicados de 2017 (docs/11):
   emulsiones solas, KEK sola y conjunto (errores reescalados con el χ²/ndf de cada conjunto).
   Se exige que el Vacío no corte ningún espacio conocido (se habría visto).
   Los datos extraídos solo cubren tanθy ≥ 0 (hacia el norte) y no fijan el extremo sur. Se usa
   la información del artículo, sacada de la imagen 2D de KEK, que sí cubre el sur: "the
   structure starts almost at the centre of the Pyramid". Se impone como información previa que
   el extremo sur esté en y ∈ SUR (por defecto −5…+5 m; argumento `libre` para quitarlo).
2. Para cada muestra, la piedra que lo separa de cada espacio accesible: Gran Galería,
   antecámara, Cámara del Rey y las cinco cámaras de descarga (accesibles por los túneles de
   Davison y Vyse).
3. Para puntos del techo de la Gran Galería y de las cámaras de descarga: probabilidad de que el
   Vacío esté a menos de ℓ metros (lo que tendría que atravesar un endoscopio o una perforación).

    cd simulador && PYTHONPATH=. python acceso_gran_vacio.py [libre]
        → ../resultados/41_acceso_gran_vacio[_sur_libre].json y 41_muestras_gran_vacio[...].npz
"""
import json
import math
import sys
import time

import numpy as np
from scipy.optimize import minimize

from piramide import geometria as g
from piramide import reanalisis as ra, reanalisis_emulsiones as re_

S_E, S_K = 3.9, 1.69
rng = np.random.default_rng(41)
t0 = time.time()
E = re_.Emulsiones(x_ne1=13.0, x_ne2=3.0)
K = ra.Reanalisis(pos_h1=(7.1, -1.9, 21.5))
CONOCIDAS = [c for c in g.estructuras_conocidas() if c.delta_densidad < 0]
ACCESIBLES = [c for c in CONOCIDAS if c.nombre.startswith(("Gran Galería", "Antecámara", "Cámara del Rey", "Cámara de descarga"))]
LIMS = [(3, 12), (-15, 50), (35, 85), (8, 75), (0.5, 15), (0.8, 8), (-20, 45)]
SUR = None if "libre" in sys.argv[1:] else (-5.0, 5.0)


def extremo_sur(v):
    c = corr(v).caja()
    ext = [np.asarray(c.centro) + s * (c.tam[1] / 2) * c._R[1] for s in (-1, 1)]
    return min(e[1] for e in ext)


def corr(v):
    x, y, z, L, h, w, a = v
    return ra.Corredor(x, y, z, L, h, ancho=w, inclinacion=a)


def puntos_superficie(c: g.Caja, paso=0.5):
    """Puntos sobre la superficie de la caja (coordenadas globales)."""
    h = np.asarray(c.tam) / 2
    out = []
    for eje in range(3):
        otros = [k for k in range(3) if k != eje]
        a = np.arange(-h[otros[0]], h[otros[0]] + 1e-9, paso)
        b = np.arange(-h[otros[1]], h[otros[1]] + 1e-9, paso)
        A, B = np.meshgrid(a, b, indexing="ij")
        for s in (-1, 1):
            P = np.zeros((A.size, 3))
            P[:, otros[0]] = A.ravel()
            P[:, otros[1]] = B.ravel()
            P[:, eje] = s * h[eje]
            out.append(P)
    P = np.vstack(out)
    return P @ c._R + np.asarray(c.centro)


def distancia_a_caja(P, c: g.Caja):
    """Distancia de los puntos P a la caja c (0 si están dentro)."""
    o = (P - np.asarray(c.centro)) @ c._R.T
    d = np.maximum(np.abs(o) - np.asarray(c.tam) / 2, 0)
    return np.linalg.norm(d, axis=1)


def corta(c: g.Caja, otra: g.Caja):
    return bool(np.any(distancia_a_caja(puntos_superficie(c, 0.7), otra) == 0)) or \
        bool(np.any(distancia_a_caja(puntos_superficie(otra, 0.7), c) == 0))


def chi2(v, cual):
    c = corr(v)
    out = 0.0
    if cual in ("E", "J"):
        out += E.chi2_vacio([c], sigma=0.03) / S_E
    if cual in ("K", "J"):
        out += K.chi2(c) / S_K
    return out


def logp(v, cual):
    if any(not (lo <= x <= hi) for x, (lo, hi) in zip(v, LIMS)):
        return -np.inf
    if SUR is not None and not (SUR[0] <= extremo_sur(v) <= SUR[1]):
        return -np.inf
    return -0.5 * chi2(v, cual)


INICIOS = [(7.2, 18.9, 56.8, 40.4, 2.7, 4.1, 16.0), (7.3, 17.0, 62.0, 34.0, 2.5, 3.5, 3.0), (8.0, 23.5, 50.6, 53.3, 2.5, 3.7, 24.0),
           (7.4, 20.0, 60.0, 40.0, 3.0, 3.0, 10.0), (7.8, 22.0, 54.0, 44.0, 2.5, 4.0, 20.0)]


def cadena(cual, n=9000, quemado=2500):
    best = None
    for ini in INICIOS:
        r = minimize(lambda v: -2 * logp(v, cual) if np.isfinite(logp(v, cual)) else 1e9, np.array(ini, float),
                     method="Nelder-Mead", options=dict(maxiter=900, xatol=0.01, fatol=0.01))
        if best is None or r.fun < best.fun:
            best = r
    x = best.x.copy()
    lp = logp(x, cual)
    d = len(x)
    cov = np.diag([0.2, 2.0, 1.0, 3.0, 0.3, 0.3, 2.0]) ** 2
    muestras, acept = [], 0
    for i in range(n):
        if i >= 600 and i % 200 == 0:
            S = np.array(muestras[max(0, len(muestras) - 3000):])
            cov = (2.38 ** 2 / d) * np.cov(S.T) + 1e-6 * np.eye(d)
        y = rng.multivariate_normal(x, cov)
        lq = logp(y, cual)
        if np.log(rng.random()) < lq - lp:
            x, lp = y, lq
            acept += 1
        muestras.append(x.copy())
    M = np.array(muestras[quemado:])
    print(cual, "χ² mínimo", round(best.fun, 1), "aceptación", round(acept / n, 2), f"{time.time() - t0:.0f}s", flush=True)
    return M, float(best.fun), [round(float(v), 2) for v in best.x], acept / n


def main():
    gal = [c for c in ACCESIBLES if c.nombre == "Gran Galería"][0]
    # puntos candidatos de acceso: techo de la galería (cada 1 m a lo largo del eje) y techos/
    # paredes norte de las cámaras de descarga
    a = math.radians(gal.inclinacion)
    eje = gal._R[1]
    arriba = gal._R[2]
    s = np.arange(-gal.tam[1] / 2, gal.tam[1] / 2 + 1e-9, 1.0)
    techo = np.asarray(gal.centro) + s[:, None] * eje + (gal.tam[2] / 2) * arriba
    cand = [dict(lugar="techo de la Gran Galería", punto=p) for p in techo]
    for c in ACCESIBLES:
        if c.nombre.startswith("Cámara de descarga"):
            cx, cy, cz = c.centro
            for xx in (cx - 4, cx, cx + 4):
                cand.append(dict(lugar=f"{c.nombre}, pared norte", punto=np.array([xx, cy + c.tam[1] / 2, cz])))
    P_cand = np.array([c["punto"] for c in cand])
    sufijo = "_sur_libre" if SUR is None else ""
    out = dict(espacios_accesibles=[c.nombre for c in ACCESIBLES], prior_extremo_sur_y=SUR, posteriores={})
    guardar = {}
    for cual in ("E", "K", "J"):
        M, chimin, best, acc = cadena(cual)
        sel = M[rng.choice(len(M), size=min(1500, len(M)), replace=False)]
        dist_esp = {c.nombre: [] for c in ACCESIBLES}
        dist_cand = []
        validas = 0
        geo = []
        for v in sel:
            caja = corr(v).caja()
            if any(corta(caja, c) for c in CONOCIDAS):
                continue
            validas += 1
            S = puntos_superficie(caja, 0.5)
            for c in ACCESIBLES:
                dist_esp[c.nombre].append(float(distancia_a_caja(S, c).min()))
            # distancia de cada punto candidato a la caja del Vacío
            dist_cand.append(distancia_a_caja(P_cand, caja))
            geo.append(v)
        dist_cand = np.array(dist_cand)
        geo = np.array(geo)
        guardar[cual] = geo
        sur = np.array([extremo_sur(v) for v in geo])
        res = dict(extremo_sur_y=dict(p05=round(float(np.percentile(sur, 5)), 2), mediana=round(float(np.median(sur)), 2),
                                      p95=round(float(np.percentile(sur, 95)), 2)),
                   chi2_minimo=round(chimin, 1), mejor_ajuste=best, aceptacion=round(acc, 2),
                   muestras_validas=validas, muestras=len(sel),
                   geometria={k: dict(mediana=round(float(np.median(geo[:, i])), 2),
                                      p05=round(float(np.percentile(geo[:, i], 5)), 2),
                                      p95=round(float(np.percentile(geo[:, i], 95)), 2))
                              for i, k in enumerate(("x", "y", "z", "largo", "alto", "ancho", "inclinacion"))},
                   piedra_hasta_espacio={k: dict(mediana=round(float(np.median(v)), 2),
                                                 p05=round(float(np.percentile(v, 5)), 2),
                                                 p95=round(float(np.percentile(v, 95)), 2),
                                                 prob_menos_de={str(l): round(float(np.mean(np.array(v) < l)), 3)
                                                                for l in (1, 2, 3, 5, 10)})
                                         for k, v in dist_esp.items()})
        mejores = {}
        for l in (2, 3, 5, 10):
            pr = np.mean(dist_cand < l, axis=0)
            i = int(np.argmax(pr))
            mejores[str(l)] = dict(lugar=cand[i]["lugar"], punto=[round(float(x), 2) for x in P_cand[i]],
                                   probabilidad=round(float(pr[i]), 3))
        res["mejor_punto_por_profundidad"] = mejores
        res["perfil_techo_galeria"] = [dict(y=round(float(p[1]), 1), z=round(float(p[2]), 1),
                                            prob_5m=round(float(np.mean(dist_cand[:, k] < 5)), 3),
                                            prob_10m=round(float(np.mean(dist_cand[:, k] < 10)), 3),
                                            distancia_mediana=round(float(np.median(dist_cand[:, k])), 2))
                                       for k, p in enumerate(techo)]
        out["posteriores"][cual] = res
        print(cual, json.dumps({k: res[k] for k in ("geometria", "mejor_punto_por_profundidad")}, ensure_ascii=False), flush=True)
        print(cual, json.dumps(res["piedra_hasta_espacio"], ensure_ascii=False), flush=True)
        json.dump(out, open(f"../resultados/41_acceso_gran_vacio{sufijo}.json", "w"), ensure_ascii=False, indent=1)
        np.savez_compressed(f"../resultados/41_muestras_gran_vacio{sufijo}.npz", **guardar)


if __name__ == "__main__":
    main()
