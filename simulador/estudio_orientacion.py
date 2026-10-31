"""¿Qué par de estrellas explica la orientación de las pirámides? Búsqueda exhaustiva.

    cd simulador && PYTHONPATH=. python estudio_orientacion.py     (~5 min)
"""
import json, itertools, time
import numpy as np
from piramide import astronomia as a, orientacion as o

t0 = time.time()
cat = a.cargar(vmax=3.5)
anios = np.arange(-3000, -1999, 5.0)
ra, dec = o.ra_dec_fecha(cat, -2549)
cand = [i for i in range(len(cat.hr)) if np.degrees(dec[i]) > 40]
print(f"{len(cand)} estrellas candidatas (V ≤ 3,5, δ > 40° en 2550 a. C.)", flush=True)

# modelos nulos
e = np.array([p[1] for p in o.PIRAMIDES]); s = np.array([p[2] for p in o.PIRAMIDES])
t = np.array([-p[3] for p in o.PIRAMIDES], float)
w = 1 / s ** 2
A = np.stack([np.ones_like(t), t], 1)
th = np.linalg.solve((A.T * w) @ A, (A.T * w) @ e)
chi_lineal = float(np.sum(w * (e - A @ th) ** 2))
chi_const = float(np.sum(w * (e - np.sum(w * e) / np.sum(w)) ** 2))
print(f"nulo constante: χ² {chi_const:.0f};  tendencia lineal libre: χ² {chi_lineal:.1f} (pendiente {th[1]:.3f}′/año)")

res = []
for iA, iB in itertools.combinations(cand, 2):
    c = o.curva_par(cat, iA, iB, anios)
    if all(np.all(np.isnan(v)) for v in c.values()):
        continue
    for perm in (False, True):
        chi, dT, conf = o.ajustar_par(anios, c, perm)
        if dT is None or not np.isfinite(chi):
            continue
        res.append(dict(A=str(cat.nombre[iA]), B=str(cat.nombre[iB]), VA=float(cat.vmag[iA]), VB=float(cat.vmag[iB]),
                        cambio=perm, chi2=float(chi), dT=float(dT), conf=conf))
print(f"{len(res)} ajustes ({time.time() - t0:.0f} s)")
for perm in (False, True):
    r = sorted([x for x in res if x["cambio"] == perm], key=lambda x: x["chi2"])
    print(("\nCON cambio de configuración permitido" if perm else "\nMISMA configuración para todas") + f" — {len(r)} pares")
    for k, x in enumerate(r[:10]):
        print(f"  {k + 1:2d}. {x['A']:10s} + {x['B']:10s} (V {x['VA']:.1f}/{x['VB']:.1f})  χ² {x['chi2']:6.1f}  ΔT {x['dT']:+5.0f} años")
    for par in (("Bet UMi", "Zet UMa"), ("Gam UMa", "Del UMa")):
        for k, x in enumerate(r):
            if {par[0], par[1]} <= {x['A'][-7:], x['B'][-7:]} or (par[0] in x['A'] + x['B'] and par[1] in x['A'] + x['B']):
                print(f"  -> {par[0]} + {par[1]}: puesto {k + 1} de {len(r)} (χ² {x['chi2']:.1f}, ΔT {x['dT']:+.0f})")
                break
json.dump(dict(nulo_constante=chi_const, nulo_lineal=chi_lineal, pendiente_lineal=float(th[1]), pares=res),
          open("../resultados/17_orientacion_pares.json", "w"), ensure_ascii=False, indent=1)
