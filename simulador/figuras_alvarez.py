"""Figura 10: mapa de residuos de Alvarez et al. (1970, fig. 10) con las agrupaciones más extremas.

Uso: PYTHONPATH=. python figuras_alvarez.py
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle

import reanalisis_alvarez as ra

RAIZ = ra.RAIZ
# divergente azul ↔ rojo con gris neutro en el centro (−3 … +3)
COL = ["#1c5cab", "#6da7ec", "#cde2fb", "#f0efec", "#f7c9b9", "#e8806a", "#b8402c"]
TINTA, TINTA2 = "#1f1f1d", "#6b6a66"


def main():
    M, _ = ra.cargar()
    r = json.load(open(os.path.join(RAIZ, "resultados", "23_reanalisis_alvarez.json")))
    nc = r["nula_correlada"]
    fig, ax = plt.subplots(figsize=(6.6, 6.4), constrained_layout=True)
    cm = ListedColormap(COL)
    cm.set_bad("white")
    ax.imshow(np.ma.masked_invalid(np.clip(M, -3, 3)), cmap=cm, vmin=-3.5, vmax=3.5,
              extent=(45, 135, 135, 45), interpolation="nearest")
    for nombre, col, et in (("exceso_4x4", "#b8402c", "exceso"), ("deficit_3x3", "#1c5cab", "déficit")):
        e = nc[nombre]
        k = int(nombre[-1])
        x0, y0 = e["phi"] - 1.5 * k, e["theta"] - 1.5 * k
        ax.add_patch(Rectangle((x0, y0), 3 * k, 3 * k, fill=False, ec=col, lw=2))
        ax.annotate(f"{et} {k}×{k}: p = {e['p_global']:.2f}", (x0, y0 - 1), fontsize=8, color=TINTA)
    ax.axhline(90, color=TINTA2, lw=0.6)
    ax.axvline(90, color=TINTA2, lw=0.6)
    th = np.linspace(0, 2 * np.pi, 200)
    rad = 35.0
    ax.plot(90 + rad * np.cos(th), 90 + rad * np.sin(th), color=TINTA2, lw=0.8, ls="--")
    ax.text(90 + rad * 0.72, 90 - rad * 0.74, "35°", fontsize=8, color=TINTA2)
    ax.set_xlabel("φ (°): oeste ← 90° → este", fontsize=8, color=TINTA2)
    ax.set_ylabel("θ (°): norte ↑ 90° ↓ sur", fontsize=8, color=TINTA2)
    ax.tick_params(colors=TINTA2, labelsize=8)
    ax.set_title("Residuos de Alvarez (1970, fig. 10), en σ enteras: medido − predicho\n"
                 f"autocorrelación entre vecinos: I = {r['combinaciones']['+++']['moran']:+.2f} (p < 0,001); "
                 "p de las agrupaciones con nula correlada", fontsize=8.5, color=TINTA, loc="left")
    cb = fig.colorbar(ax.images[0], ax=ax, shrink=0.6, ticks=range(-3, 4))
    cb.ax.tick_params(labelsize=8, colors=TINTA2)
    fig.savefig(os.path.join(RAIZ, "figuras", "10_residuos_alvarez.png"), dpi=150)
    print("figura 10 escrita")


if __name__ == "__main__":
    main()
