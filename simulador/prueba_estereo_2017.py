"""¿Bastan los datos completos de 2017 (emulsiones NE1 + NE2, estéreo) para decidir la forma?

Prueba a ciegas como en robustez.py, pero con las dos posiciones reales de las emulsiones en
lugar de un único detector en la Cámara de la Reina.

    cd simulador && PYTHONPATH=. python prueba_estereo_2017.py     (~6 min)
"""
import json, math, time
import numpy as np
from piramide import robustez as rb, muones as mu
from ejecutar_profundo import hipotesis_ajustadas

t = time.time()
H = hipotesis_ajustadas()
rq = mu.Rejilla.cuadrada(-0.8, 0.8, -0.2, 1.2, rb.PASO)
P = {"NE1": rb.PuestoMedida("NE1", np.array([13.0, 0.0, 21.5]), np.array([0, 0, 1.0]), rq, 98.0, 0.45),
     "NE2": rb.PuestoMedida("NE2", np.array([3.0, -1.1, 21.5]), np.array([0, 0, 1.0]), rq, 140.0, 0.45)}
P["KC"] = rb.puestos_estandar()["KC"]
bib = rb.Biblioteca.construir(H, P)
print(f"biblioteca {time.time() - t:.0f} s", flush=True)
out = {}
for nombre, usar, fis in (("2017 estéreo (NE1+NE2)", ("NE1", "NE2"), "nominal"),
                          ("2017 estéreo, flujo -10 % e índice +0,05", ("NE1", "NE2"), "perturbado+"),
                          ("2017 estéreo, cámaras desplazadas 1 m", ("NE1", "NE2"), "estructuras"),
                          ("2017 estéreo + Cámara del Rey 60 d", ("NE1", "NE2", "KC"), "nominal")):
    r = rb.prueba_a_ciegas(bib, n=40, usar=usar, fisica=fis)
    marg = {k: float(math.sqrt(max(m, 0))) for k, m in r["margen_mediano"].items()}
    out[nombre] = dict(acierto=r["acierto"], matriz=r["matriz"].tolist(), margen_sigma=marg)
    print(f"{nombre:42s} acierto {100 * r['acierto']:5.1f} %  margen mediano (σ) " +
          " ".join(f"{k}:{v:.1f}" for k, v in marg.items()), f"({time.time() - t:.0f} s)", flush=True)
json.dump(out, open("../resultados/13_estereo_2017.json", "w"), ensure_ascii=False, indent=1)
