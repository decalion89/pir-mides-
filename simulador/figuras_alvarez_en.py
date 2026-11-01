"""English versions of figures 10 and 11 for the Alvarez reanalysis note (preprint/alvarez/)."""
import json
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

import reanalisis_alvarez as ra
from piramide import kefren as kf

RAIZ = ra.RAIZ
OUT = os.path.join(RAIZ, "preprint", "alvarez")
TINTA, TINTA2 = "#1f1f1d", "#6b6a66"


def residuals():
    COL = ["#1c5cab", "#6da7ec", "#cde2fb", "#f0efec", "#f7c9b9", "#e8806a", "#b8402c"]
    M, _ = ra.cargar()
    r = json.load(open(os.path.join(RAIZ, "resultados", "23_reanalisis_alvarez.json")))
    nc = r["nula_correlada"]
    fig, ax = plt.subplots(figsize=(6.4, 6.2), constrained_layout=True)
    cm = ListedColormap(COL)
    cm.set_bad("white")
    im = ax.imshow(np.ma.masked_invalid(np.clip(M, -3, 3)), cmap=cm, vmin=-3.5, vmax=3.5,
                   extent=(45, 135, 135, 45), interpolation="nearest")
    for key, col, lab in (("exceso_4x4", "#b8402c", "excess"), ("deficit_3x3", "#1c5cab", "deficit")):
        e = nc[key]
        k = int(key[-1])
        x0, y0 = e["phi"] - 1.5 * k, e["theta"] - 1.5 * k
        ax.add_patch(Rectangle((x0, y0), 3 * k, 3 * k, fill=False, ec=col, lw=2))
        ax.annotate(f"{lab} {k}×{k}: global p = {e['p_global']:.2f}", (x0, y0 - 1), fontsize=8, color=TINTA)
    ax.axhline(90, color=TINTA2, lw=0.6)
    ax.axvline(90, color=TINTA2, lw=0.6)
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(90 + 35 * np.cos(th), 90 + 35 * np.sin(th), color=TINTA2, lw=0.8, ls="--")
    ax.set_xlabel("φ (deg): west ← 90° → east", fontsize=8, color=TINTA2)
    ax.set_ylabel("θ (deg): north ↑ 90° ↓ south", fontsize=8, color=TINTA2)
    ax.tick_params(colors=TINTA2, labelsize=8)
    ax.set_title("Alvarez et al. (1970), Fig. 10: (measured − predicted), integer σ\n"
                 f"nearest-neighbour Moran's I = {r['combinaciones']['+++']['moran']:+.2f} (p < 0.001); dashed: 35° cone",
                 fontsize=8.5, color=TINTA, loc="left")
    cb = fig.colorbar(im, ax=ax, shrink=0.6, ticks=range(-3, 4))
    cb.ax.tick_params(labelsize=8, colors=TINTA2)
    fig.savefig(os.path.join(OUT, "fig1_residuals.png"), dpi=150)


def exclusion():
    COL = ["#1c5cab", "#9ec5f4", "#e4e2dd"]
    d = np.load(os.path.join(RAIZ, "resultados", "24_exclusion_alvarez.npz"))
    P, dk = d["P"], d["dchi2_rey"]
    paso = float(np.min(np.diff(np.unique(P[:, 0]))))
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 4.3), sharey=True)
    for ax, eje, tit in ((axs[0], 0, "East–west section through the centre"),
                         (axs[1], 1, "North–south section through the centre")):
        otro = 1 - eje
        sel = np.abs(P[:, otro] - P[np.argmin(np.abs(P[:, otro])), otro]) < paso / 2
        Q, z = P[sel], dk[sel]
        cls = np.where(z >= 25, 0, np.where(z >= 3.84, 1, 2))
        cls = cls.astype(float)
        cls[np.isnan(z)] = np.nan          # la cámara no cabe entera: no aplicable
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
        for ang, ls in ((35, "--"), (45, ":")):
            t = math.tan(math.radians(ang))
            ax.plot([o[eje], o[eje] - t * 140], [0, 140], color=TINTA2, lw=0.8, ls=ls)
            ax.plot([o[eje], o[eje] + t * 140], [0, 140], color=TINTA2, lw=0.8, ls=ls)
        ax.plot(o[eje], -2, "D", ms=6, mfc="white", mec="#c2410c", mew=1.3)
        ax.set_title(tit, fontsize=9, color=TINTA, loc="left")
        ax.set_xlabel("x (m, east +)" if eje == 0 else "y (m, north +)", fontsize=8, color=TINTA2)
        ax.set_xlim(-kf.SEMI - 4, kf.SEMI + 4)
        ax.set_ylim(-8, kf.ALTURA + 4)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(colors=TINTA2, labelsize=8)
    axs[0].set_ylabel("height (m)", fontsize=8, color=TINTA2)
    h = [Patch(color=COL[0], label="excluded at ≥ 5σ"), Patch(color=COL[1], label="excluded at 95% CL"),
         Patch(color=COL[2], label="not excluded"),
         Line2D([], [], color=TINTA2, ls="--", label="35° cone analysed by Alvarez"),
         Line2D([], [], color=TINTA2, ls=":", label="45° (data limit)")]
    fig.legend(handles=h, loc="upper center", ncol=5, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.02))
    fig.savefig(os.path.join(OUT, "fig2_exclusion.png"), dpi=150, bbox_inches="tight", pad_inches=0.15)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    residuals()
    exclusion()
    print("ok")
