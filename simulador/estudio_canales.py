"""¿Apuntaban los canales de la Gran Pirámide a estrellas? Fechas y prueba contra el azar.

    cd simulador && PYTHONPATH=. python estudio_canales.py     (~2 min)
"""
import json, math
import numpy as np
from piramide import astronomia as a

cat = a.cargar(vmax=4.0)
anios = np.arange(-3500, -1499, 5.0)
D = a.emparejar(cat, anios)                       # (n_anios, n_estrellas)
PROPUESTAS = {"Rey sur": "Zet Ori", "Rey norte": "Alp Dra", "Reina sur": "Alp CMa", "Reina norte": "Bet UMi"}
idx = {k: int([j for j, n in enumerate(cat.nombre) if v in n][0]) for k, v in PROPUESTAS.items()}

res = {"canales": {}}
print("1) Fecha en que cada estrella propuesta culminaba a lo largo de su canal")
for k, c in a.CANALES.items():
    dt = a.declinacion_objetivo(c["angulo"], c["lado"])
    j = idx[k]
    d = D[:, j]
    s = np.where(np.diff(np.sign(d - dt)) != 0)[0]
    sol = []
    for i in s:
        t = anios[i] + (dt - d[i]) * (anios[i + 1] - anios[i]) / (d[i + 1] - d[i])
        tasa = abs(d[i + 1] - d[i]) / (anios[i + 1] - anios[i])          # grados/año
        sol.append((t, c["sigma"] / tasa))
    res["canales"][k] = dict(estrella=PROPUESTAS[k], vmag=float(cat.vmag[j]), decl_objetivo=dt,
                             soluciones=[dict(anio_aC=a.anio_bc(t), sigma_anios=e) for t, e in sol],
                             fuente=c["fuente"])
    print(f"   {k:12s} {PROPUESTAS[k]:8s} (V={cat.vmag[j]:5.2f}) δ objetivo {dt:7.2f}° -> " +
          ", ".join(f"{a.anio_bc(t):.0f} a. C. ± {e:.0f} años" for t, e in sol))

print("2) ¿Cuántas estrellas brillantes encajan con cada canal entre 2700 y 2400 a. C.?")
ventana = (anios >= -2699) & (anios <= -2399)
for k, c in a.CANALES.items():
    dt = a.declinacion_objetivo(c["angulo"], c["lado"])
    for vlim in (2.0, 3.0, 4.0):
        m = (cat.vmag <= vlim)
        hit = np.any(np.abs(D[ventana][:, m] - dt) <= c["sigma"], axis=0)
        noms = [f"{n}({v:.1f})" for n, v in zip(cat.nombre[m][hit], cat.vmag[m][hit])]
        res["canales"][k][f"estrellas_V{vlim}"] = noms
        print(f"   {k:12s} V≤{vlim}: {len(noms):2d} -> {', '.join(noms[:8])}")

print("3) Prueba contra el azar (Monte Carlo)")
# Para un conjunto de 4 ángulos: ¿existe un año T (en 3500-1500 a. C.) en el que los 4 canales
# tengan a la vez una estrella con V ≤ vlim a menos de su incertidumbre? Se compara con ángulos
# al azar en los mismos rangos plausibles (25-50° norte y sur).
rng = np.random.default_rng(1)
sig = np.array([c["sigma"] for c in a.CANALES.values()])
lados = [c["lado"] for c in a.CANALES.values()]
def coincide(angs, vlim, ventana_anios=50):
    m = cat.vmag <= vlim
    Dm = D[:, m]
    ok = []
    for ang, s_, ld in zip(angs, sig, lados):
        dt = a.declinacion_objetivo(ang, ld)
        ok.append(np.any(np.abs(Dm - dt) <= s_, axis=1))
    ok = np.array(ok)                                   # (4, n_anios)
    # suavizar: el canal coincide en T si coincide en algún año a ±ventana
    k = int(ventana_anios / 5)
    okv = np.array([np.convolve(o, np.ones(2 * k + 1), mode="same") > 0 for o in ok])
    todos = np.all(okv, axis=0)
    return bool(todos.any()), anios[todos]
res["azar"] = {}
reales = [c["angulo"] for c in a.CANALES.values()]
for vlim in (2.5, 3.0, 3.7):
    real, tt = coincide(reales, vlim)
    n = 2000
    exitos = sum(coincide(rng.uniform(25, 50, 4), vlim)[0] for _ in range(n))
    p = exitos / n
    res["azar"][f"V{vlim}"] = dict(real_coincide=real, anios_aC=[float(a.anio_bc(x)) for x in tt[:: max(1, len(tt) // 10)]],
                                   p_azar=p)
    rango = f"{a.anio_bc(tt.max()):.0f}-{a.anio_bc(tt.min()):.0f} a. C." if real else "-"
    print(f"   V≤{vlim}: ángulos reales coinciden a la vez: {real} ({rango});  con ángulos al azar: {100 * p:.1f} % de los casos")
json.dump(res, open("../resultados/14_canales_estelares.json", "w"), ensure_ascii=False, indent=1, default=str)
