"""Estudio del giro en las esquinas: ¿qué cambia si el tiempo de giro sale de la física?

    cd simulador && PYTHONPATH=. python estudio_giros.py      (~3 min)

Repite el Monte Carlo de construcción para las técnicas de giro "parametrica" (la suposición
original: 2-15 min por esquina), "pivote" y "poste" (giro.py), y guarda
resultados/10_giros.json y figuras/07_giros.png.
"""
from __future__ import annotations

import json

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from piramide import giro, obra, rampas
from piramide import geometria as g
from piramide.fisica import Parametros
from ejecutar_todo import RES, FIG, COLORES, TINTA, estilo

CLAVES = ("zigzag", "espiral", "interna", "aristas", "recta+zigzag", "recta+palancas")
TECNICAS = ("parametrica", "pivote", "poste")


def main(n: int = 400, semilla: int = 2026):
    rng = np.random.default_rng(semilla)
    muestras = [Parametros().muestrear(rng) for _ in range(n)]
    cat = {m.clave: m for m in rampas.catalogo()}
    out = {"fisica_del_giro": giro.comparar(), "n": n, "modelos": {}}
    for k in CLAVES:
        out["modelos"][k] = {}
        for tec in TECNICAS:
            anios, equipos = [], []
            for p in muestras:
                p.tecnica_giro = tec
                r = obra.simular(cat[k], p, 25000)
                anios.append(r.anios)
                equipos.append(r.equipo_max)
            a = np.array(anios)
            vaux = cat[k].volumen_aux(g.ALTURA) / g.VOLUMEN_TOTAL
            out["modelos"][k][tec] = dict(p_viable=float(np.mean((a <= 20) & (vaux <= 0.5))),
                                          p_27=float(np.mean((a <= 27) & (vaux <= 0.5))),
                                          mediana=float(np.median(a)), p10=float(np.percentile(a, 10)),
                                          p90=float(np.percentile(a, 90)), equipo_mediano=float(np.median(equipos)))
            print(f"{k:15s} {tec:12s} P(≤20 a)={out['modelos'][k][tec]['p_viable']:.2f}  "
                  f"P(≤27 a)={out['modelos'][k][tec]['p_27']:.2f}  mediana {np.median(a):5.1f} "
                  f"[{np.percentile(a, 10):.1f}-{np.percentile(a, 90):.1f}]  equipo {np.median(equipos):.0f}", flush=True)
    (RES / "10_giros.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    fig, ax = plt.subplots(figsize=(9, 4.2))
    w = 0.26
    xs = np.arange(len(CLAVES))
    nombres = {"parametrica": "suposición inicial (2–15 min)", "pivote": "parar y pivotar (física)",
               "poste": "poste de reenvío (física)"}
    for i, tec in enumerate(TECNICAS):
        ax.bar(xs + (i - 1) * w, [100 * out["modelos"][k][tec]["p_viable"] for k in CLAVES], w,
               color=COLORES[i], label=nombres[tec])
    ax.set_xticks(xs, CLAVES, fontsize=8)
    ax.set_ylabel("% de escenarios que terminan en ≤ 20 años", fontsize=9)
    ax.set_title("La física del giro cambia el veredicto sobre las rampas de un solo carril", fontsize=10,
                 color=TINTA, loc="left")
    ax.legend(fontsize=8, frameon=False)
    estilo(ax)
    fig.tight_layout()
    fig.savefig(FIG / "07_giros.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
