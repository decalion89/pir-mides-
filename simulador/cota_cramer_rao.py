"""Cota de Cramér–Rao para la inclinación del Gran Vacío desde cada puesto.

    cd simulador && PYTHONPATH=. python cota_cramer_rao.py      (~1 min)
"""
import json
import numpy as np
from piramide import robustez as rb, cota_informacion as ci

from piramide import muones as mu
P = rb.puestos_estandar(dias_kc=60.0, dias_d5=7.0)
# configuración real de 2017: emulsiones NE1 (nicho este) y NE2 (esquina suroeste), calibradas en docs/11
rq = mu.Rejilla.cuadrada(-0.8, 0.8, -0.2, 1.2, rb.PASO)
P["NE1"] = rb.PuestoMedida("NE1", np.array([13.0, 0.0, 21.5]), np.array([0, 0, 1.0]), rq, 98.0, 0.45)
P["NE2"] = rb.PuestoMedida("NE2", np.array([3.0, -1.1, 21.5]), np.array([0, 0, 1.0]), rq, 140.0, 0.45)
casos = {}
for nombre, v0 in (("horizontal", (17.0, 63.0, 32.0, 6.0, 2.0, 0.0)),
                   ("inclinado 26°", (17.0, 63.0, 32.0, 6.0, 2.0, 26.0)),
                   ("inclinado 13°", (17.0, 63.0, 32.0, 6.0, 2.0, 13.0))):
    F = {k: ci.fisher(pu, v0) for k, pu in P.items()}
    res = {}
    for etiqueta, Fs in (("2017: NE1 + NE2 (estéreo)", ["NE1", "NE2"]),
                         ("2017 + Cámara del Rey 60 d", ["NE1", "NE2", "KC"]),
                         ("2017 + Campbell 7 d", ["NE1", "NE2", "D5"])):
        n = len(ci.PASOS)
        Ft = ci.combinar(*[F[k] for k in Fs])
        C = np.linalg.inv(Ft)
        s = {ci.NOMBRES[i]: float(np.sqrt(C[i, i])) for i in range(n)}
        res[etiqueta] = s
        print(f"{nombre:14s} {etiqueta:28s} σ(inclinación) ≥ {s['inclinacion']:5.1f}°   σ(z) ≥ {s['z']:4.1f} m   "
              f"σ(alto) ≥ {s['alto']:4.2f} m   σ(ancho) ≥ {s['ancho']:4.2f} m", flush=True)
    casos[nombre] = res
json.dump(casos, open("../resultados/12_cramer_rao.json", "w"), ensure_ascii=False, indent=1)
