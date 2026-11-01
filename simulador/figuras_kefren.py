"""Figura 09: Kefrén, corte este-oeste. Alvarez (1969) frente a la propuesta de cinco orientaciones.

Uso: PYTHONPATH=. python figuras_kefren.py   (tras estudio_kefren.py)
"""
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
ETQ = ["≥ 5σ", "3–5σ", "< 3σ (sin explorar)"]
F = 0.437                      # calibración de Nagoya, como en Keops


def panel(ax, P, Z, titulo, paso):
    sel = np.abs(P[:, 1] - P[np.argmin(np.abs(P[:, 1])), 1]) < paso / 2
    Q, z = P[sel], Z[sel]
    cls = np.where(z >= 5, 0, np.where(z >= 3, 1, 2))
    ux, uz = np.unique(Q[:, 0]), np.unique(Q[:, 2])
    img = np.full((uz.size, ux.size), np.nan)
    img[np.searchsorted(uz, Q[:, 2]), np.searchsorted(ux, Q[:, 0])] = cls
    cm = ListedColormap(COL)
    cm.set_bad("white")
    ax.imshow(np.ma.masked_invalid(img), origin="lower", cmap=cm, vmin=-0.5, vmax=2.5,
              extent=(ux[0] - paso / 2, ux[-1] + paso / 2, uz[0] - paso / 2, uz[-1] + paso / 2),
              interpolation="nearest")
    ax.plot([-kf.SEMI, 0, kf.SEMI], [0, kf.ALTURA, 0], color=TINTA, lw=1)
    o = kf.ORIGEN_ALVAREZ
    ax.plot(o[0], o[2] - 2, "D", ms=6, mfc="white", mec="#c2410c", mew=1.3)
    ax.set_title(titulo, fontsize=9, color=TINTA, loc="left")
    ax.set_xlabel("x (m, este +)", fontsize=8, color=TINTA2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(TINTA2)
    ax.tick_params(colors=TINTA2, labelsize=8)
    ax.set_ylim(-8, kf.ALTURA + 4)


def main():
    d = np.load(os.path.join(RAIZ, "resultados", "21_kefren.npz"))
    P = d["P"]
    paso = float(np.min(np.diff(np.unique(P[:, 0]))))
    za = F * d["Za_0"]
    zk = F * np.sqrt((d["Zk_0"] ** 2).sum(axis=1))
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.2), constrained_layout=True, sharey=True)
    panel(axs[0], P, za, f"Alvarez 1968–69: 1 millón de muones, cono de 35°\n({np.mean(za >= 5):.0%} del volumen a ≥ 5σ)", paso)
    panel(axs[1], P, zk, f"Propuesta: 5 × (2 m² × 180 d) desde Belzoni\n({np.mean(zk >= 5):.0%} del volumen a ≥ 5σ)", paso)
    axs[0].set_ylabel("altura (m)", fontsize=8, color=TINTA2)
    h = [Patch(color=c, label=l) for c, l in zip(COL, ETQ)]
    h.append(Line2D([], [], ls="", marker="D", mfc="white", mec="#c2410c", mew=1.3, ms=6,
                    label="Cámara de Belzoni (detector)"))
    fig.legend(handles=h, loc="outside lower center", ncol=4, fontsize=8, frameon=False,
               title="Kefrén, corte este-oeste por el centro: ¿se habría visto una cámara del tamaño de la del Rey? (calibración ×0,44)",
               title_fontsize=8)
    fig.savefig(os.path.join(RAIZ, "figuras", "09_kefren_alvarez.png"), dpi=150, bbox_inches="tight", pad_inches=0.15)
    print("figura 09 escrita")


if __name__ == "__main__":
    main()
