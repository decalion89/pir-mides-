"""Figura 11: Kefrén, lo que excluyen de verdad los datos de Alvarez (cámara tipo Rey).

Uso: PYTHONPATH=. python figuras_exclusion_alvarez.py
"""
import json
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from piramide import kefren as kf

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TINTA, TINTA2 = "#1f1f1d", "#6b6a66"
COL = ["#1c5cab", "#9ec5f4", "#e4e2dd"]


def panel(ax, P, d, eje, titulo, paso):
    otro = 1 - eje
    sel = np.abs(P[:, otro] - P[np.argmin(np.abs(P[:, otro])), otro]) < paso / 2
    Q, z = P[sel], d[sel]
    cls = np.where(z >= 25, 0, np.where(z >= 3.84, 1, 2))
    ux, uz = np.unique(Q[:, eje]), np.unique(Q[:, 2])
    img = np.full((uz.size, ux.size), np.nan)
    img[np.searchsorted(uz, Q[:, 2]), np.searchsorted(ux, Q[:, eje])] = cls
    cm = ListedColormap(COL)
    cm.set_bad("white")
    ax.imshow(np.ma.masked_invalid(img), origin="lower", cmap=cm, vmin=-0.5, vmax=2.5,
              extent=(ux[0] - paso / 2, ux[-1] + paso / 2, uz[0] - paso / 2, uz[-1] + paso / 2),
              interpolation="nearest")
    ax.plot([-kf.SEMI, 0, kf.SEMI], [0, kf.ALTURA, 0], color=TINTA, lw=1)
    o = kf.ORIGEN_ALVAREZ
    for ang in (35, 45):
        t = math.tan(math.radians(ang))
        ls = "--" if ang == 35 else ":"
        ax.plot([o[eje], o[eje] - t * 140], [0, 140], color=TINTA2, lw=0.8, ls=ls)
        ax.plot([o[eje], o[eje] + t * 140], [0, 140], color=TINTA2, lw=0.8, ls=ls)
    ax.plot(o[eje], -2, "D", ms=6, mfc="white", mec="#c2410c", mew=1.3)
    ax.set_title(titulo, fontsize=9, color=TINTA, loc="left")
    ax.set_xlabel(("x (m, este +)" if eje == 0 else "y (m, norte +)"), fontsize=8, color=TINTA2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(TINTA2)
    ax.tick_params(colors=TINTA2, labelsize=8)
    ax.set_xlim(-kf.SEMI - 4, kf.SEMI + 4)
    ax.set_ylim(-8, kf.ALTURA + 4)


def main():
    d = np.load(os.path.join(RAIZ, "resultados", "24_exclusion_alvarez.npz"))
    P, dk = d["P"], d["dchi2_rey"]
    paso = float(np.min(np.diff(np.unique(P[:, 0]))))
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.3), sharey=True)
    panel(axs[0], P, dk, 0, "Corte este-oeste por el centro", paso)
    panel(axs[1], P, dk, 1, "Corte norte-sur por el centro", paso)
    axs[0].set_ylabel("altura (m)", fontsize=8, color=TINTA2)
    h = [Patch(color=COL[0], label="excluida a ≥ 5σ"), Patch(color=COL[1], label="excluida al 95 %"),
         Patch(color=COL[2], label="no excluida"),
         Line2D([], [], color=TINTA2, ls="--", label="cono de 35° (lo que analizó Alvarez)"),
         Line2D([], [], color=TINTA2, ls=":", label="45° (límite de sus datos)")]
    fig.legend(handles=h, loc="lower center", ncol=5, fontsize=8, frameon=False,
               title="Kefrén: dónde excluyen una cámara del tamaño de la del Rey los residuos REALES de Alvarez (1970)",
               title_fontsize=8, bbox_to_anchor=(0.5, -0.02))
    fig.savefig(os.path.join(RAIZ, "figuras", "11_exclusion_datos_alvarez.png"), dpi=150,
                bbox_inches="tight", pad_inches=0.15)
    print("figura 11 escrita")


if __name__ == "__main__":
    main()
