"""¿Qué par de estrellas explica la orientación de las pirámides? Búsqueda exhaustiva (v2).

Cambios tras la revisión independiente:
- Fechas y errores de la tabla 1 de Spence (2000), no las de una cronología comprimida.
- Las dos estrellas deben estar al menos 5° por encima del horizonte (alineación observable).
- Desfases de −500 a +500 años; se descartan los ajustes que tocan el borde.
- Modelos nulos (tendencia lineal, con y sin Kefrén reflejado) calculados aquí mismo.
- Equivalencia: Δχ² < 1 (un parámetro continuo), con y sin reescalar por χ²_min/ndf.
- Retrodicción de la V dinastía (Sahure, Neferirkare, Unas) con los mejores pares.

    cd simulador && PYTHONPATH=. python estudio_orientacion.py     (~5 min)
"""
import itertools
import json
import time

import numpy as np
from scipy.optimize import minimize

from piramide import astronomia as a, orientacion as o

t0 = time.time()
cat = a.cargar(vmax=3.5)
anios = np.arange(-3200, -1999, 5.0)
ra, dec = o.ra_dec_fecha(cat, -2549)
cand = [i for i in range(len(cat.hr)) if np.degrees(dec[i]) > 25]
print(f"{len(cand)} estrellas candidatas (V ≤ 3,5, δ > 25° en 2550 a. C.; el filtro de altura decide)", flush=True)

# --- modelos nulos -------------------------------------------------------------------------
P = o.PIRAMIDES
e = np.array([p[1] for p in P]); s = np.array([p[2] for p in P])
t = np.array([2552 - p[3] for p in P], float)      # años desde la orientación de Keops
st = np.array([p[4] for p in P], float)


def chi_lineal(ee):
    f = lambda v: np.sum((ee - v[0] - v[1] * t) ** 2 / (s ** 2 + (v[1] * st) ** 2))
    r = minimize(f, [0, 0.3], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-8))
    return float(r.fun), [float(x) for x in r.x]


e_ref = e.copy()
e_ref[4] = -e_ref[4]                                   # Kefrén reflejado (configuración opuesta)
nulo = dict(constante=float(np.sum((e - np.sum(e / s ** 2) / np.sum(1 / s ** 2)) ** 2 / s ** 2)),
            lineal=chi_lineal(e), lineal_kefren_reflejado=chi_lineal(e_ref))
print(f"nulo constante χ² {nulo['constante']:.0f}; lineal χ² {nulo['lineal'][0]:.1f} "
      f"(pendiente {nulo['lineal'][1][1]:.3f}′/año); lineal con Kefrén reflejado χ² {nulo['lineal_kefren_reflejado'][0]:.1f}",
      flush=True)

# --- todos los pares ------------------------------------------------------------------------
res = []
curvas = {}
for iA, iB in itertools.combinations(cand, 2):
    c = o.curva_par(cat, iA, iB, anios)
    if all(np.all(np.isnan(v)) for v in c.values()):
        continue
    curvas[(iA, iB)] = c
    for perm in (False, True):
        chi, dT, conf = o.ajustar_par(anios, c, perm)
        if dT is None or not np.isfinite(chi):
            continue
        res.append(dict(A=str(cat.nombre[iA]), B=str(cat.nombre[iB]), iA=int(iA), iB=int(iB),
                        cambio=perm, chi2=float(chi), dT=float(dT), borde=bool(abs(dT) >= 498), conf=conf))
print(f"{len(curvas)} pares observables con alineación cerca del norte; {len(res)} ajustes ({time.time() - t0:.0f} s)",
      flush=True)

resumen = {}
for perm in (False, True):
    r = sorted([x for x in res if x["cambio"] == perm and not x["borde"]], key=lambda x: x["chi2"])
    if not r:
        continue
    m = r[0]["chi2"]
    ndf = len(P) - 1
    esc = max(m / ndf, 1.0)
    eq1 = [x for x in r if x["chi2"] - m < 1.0]
    eqE = [x for x in r if (x["chi2"] - m) / esc < 1.0]
    km = next((k for k, x in enumerate(r) if "Bet UMi" in x["A"] + x["B"] and "Zet UMa" in x["A"] + x["B"]), None)
    titulo = "CON cambio de configuración" if perm else "MISMA configuración"
    print(f"\n{titulo}: {len(r)} ajustes sin tocar el borde; mejor χ² {m:.1f} (ndf {ndf})")
    for k, x in enumerate(r[:8]):
        print(f"  {k + 1:2d}. {x['A']:10s} + {x['B']:10s}  χ² {x['chi2']:6.1f}  ΔT {x['dT']:+5.0f} años")
    print(f"  Equivalentes Δχ²<1: {len(eq1)} pares, ΔT de {min(x['dT'] for x in eq1):+.0f} a {max(x['dT'] for x in eq1):+.0f}")
    print(f"  Equivalentes con errores reescalados (×{esc:.1f}): {len(eqE)} pares, ΔT de "
          f"{min(x['dT'] for x in eqE):+.0f} a {max(x['dT'] for x in eqE):+.0f}")
    if km is not None:
        x = r[km]
        print(f"  Kochab + Mizar: puesto {km + 1} de {len(r)}, χ² {x['chi2']:.1f}, ΔT {x['dT']:+.0f} (Spence: −72 a −74)")
    resumen["cambio" if perm else "misma"] = dict(
        mejor_chi2=m, escala=esc, n=len(r), top=[f"{x['A']}+{x['B']} χ²={x['chi2']:.1f} ΔT={x['dT']:+.0f}" for x in r[:8]],
        equivalentes_dchi2_1=dict(n=len(eq1), dT=[min(x['dT'] for x in eq1), max(x['dT'] for x in eq1)],
                                 pares=[f"{x['A']}+{x['B']}" for x in eq1]),
        equivalentes_reescalados=dict(n=len(eqE), dT=[min(x['dT'] for x in eqE), max(x['dT'] for x in eqE)],
                                      pares=[f"{x['A']}+{x['B']}" for x in eqE]),
        kochab_mizar=dict(puesto=None if km is None else km + 1, chi2=None if km is None else r[km]["chi2"],
                          dT=None if km is None else r[km]["dT"]))

# --- retrodicción de la V dinastía con los mejores pares (con cambio permitido) ----------------
print("\nRetrodicción de la V dinastía (Spence: Sahure −23′±10, Neferirkare +30′±10, Unas +17,1′)")
retro = []
r = sorted([x for x in res if x["cambio"] and not x["borde"]], key=lambda x: x["chi2"])
for x in r[:6]:
    c = curvas[(x["iA"], x["iB"])]
    fila = {}
    for nom, ev, sv, bc, sa in o.PIRAMIDES_V:
        tt = (1 - bc) - x["dT"]
        vals = [float(np.interp(tt, anios, c[k], left=np.nan, right=np.nan)) for k in ("A_arriba", "B_arriba")]
        fila[nom] = [None if not np.isfinite(v) else v for v in vals]
    retro.append(dict(par=f"{x['A']}+{x['B']}", dT=x["dT"], predicciones=fila))
    print(f"  {x['A']}+{x['B']} (ΔT {x['dT']:+.0f}): " + "; ".join(
        f"{n} {p[0]}′ o {p[1]}′" for n, p in fila.items()))

json.dump(dict(datos=dict(piramides=P, piramides_V=o.PIRAMIDES_V, fuente="Spence 2000, tabla 1"),
               nulo=nulo, resumen=resumen, retrodiccion_V=retro,
               pares=[{k: v for k, v in x.items() if k not in ("iA", "iB")} for x in res]),
          open("../resultados/17_orientacion_pares.json", "w"), ensure_ascii=False, indent=1, allow_nan=False,
          default=float)
print(f"\nHecho en {time.time() - t0:.0f} s")
