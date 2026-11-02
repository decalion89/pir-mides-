"""Figura 12: quién explora qué en la base de la Gran Pirámide (hueco de 8 m, ≥ 5σ).

Uso: PYTHONPATH=. python figuras_gravimetria.py
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from piramide import geometria as g

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TINTA, TINTA2 = "#1f1f1d", "#6b6a66"
# 0 muones hoy, 1 + Cámara Subterránea (muones), 2 + gravedad, 3 sin explorar, 4 hueco conocido
COL = ["#1c5cab", "#6da7ec", "#c2410c", "#e4e2dd", "#1f1f1d"]
ETQ = ["muones (2016–2020)", "+ muones desde la Cámara Subterránea", "+ microgravimetría (σ = 3 µGal)",
       "sin explorar", "hueco conocido"]


def clases():
    d = np.load(os.path.join(RAIZ, "resultados", "19_cobertura.npz"))
    gv = np.load(os.path.join(RAIZ, "resultados", "25_gravimetria.npz"))
    P, ocup, Zp, T = d["P"], d["ocupado"], d["Z_publicadas"], list(d["tamanos"])
    K = list(d["candidatas"])
    zmu = Zp[:, T.index(8.0)]
    zsc = d["Z_candidatas_8"][:, K.index("Cámara Subterránea")]
    zg = gv["Zgrav1_8"] / 3.0
    c = np.full(len(P), 3)
    c[zg >= 5] = 2
    c[np.sqrt(zmu ** 2 + zsc ** 2) >= 5] = 1
    c[zmu >= 5] = 0
    c[ocup] = 4
    return P, c


def dibujar(ax, P, c, fijo, valor, ejes, titulo):
    paso = float(np.min(np.diff(np.unique(P[:, 0]))))
    sel = np.abs(P[:, fijo] - valor) <= paso / 2
    Q, k = P[sel], c[sel]
    a, b = ejes
    ua, ub = np.unique(Q[:, a]), np.unique(Q[:, b])
    img = np.full((ub.size, ua.size), np.nan)
    img[np.searchsorted(ub, Q[:, b]), np.searchsorted(ua, Q[:, a])] = k
    cm = ListedColormap(COL)
    cm.set_bad("white")
    ax.imshow(np.ma.masked_invalid(img), origin="lower", cmap=cm, vmin=-0.5, vmax=4.5,
              extent=(ua[0] - paso / 2, ua[-1] + paso / 2, ub[0] - paso / 2, ub[-1] + paso / 2),
              interpolation="nearest")
    ax.set_title(titulo, fontsize=9, color=TINTA, loc="left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(TINTA2)
    ax.tick_params(colors=TINTA2, labelsize=8)


def main():
    P, c = clases()
    zs = np.unique(P[:, 2])
    z10 = zs[np.argmin(np.abs(zs - 10))]
    ys = np.unique(P[:, 1])
    y0 = ys[np.argmin(np.abs(ys))]
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.8), gridspec_kw=dict(width_ratios=[1, 1.25]))
    dibujar(axs[0], P, c, 2, z10, (0, 1), f"Planta a {z10:.0f} m de altura")
    axs[0].set_xlabel("x (m, este +)", fontsize=8, color=TINTA2)
    axs[0].set_ylabel("y (m, norte +)", fontsize=8, color=TINTA2)
    dibujar(axs[1], P, c, 1, y0, (0, 2), "Corte este-oeste por el centro")
    L = g.SEMILADO
    axs[1].plot([-L, 0, L], [0, g.ALTURA, 0], color=TINTA, lw=1)
    axs[1].set_xlabel("x (m, este +)", fontsize=8, color=TINTA2)
    axs[1].set_ylabel("altura (m)", fontsize=8, color=TINTA2)
    h = [Patch(color=cc, label=l) for cc, l in zip(COL, ETQ)]
    fig.legend(handles=h, loc="upper center", ncol=5, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.0),
               title="Gran Pirámide: ¿se vería un hueco de 8 m (≥ 5σ)? Muones arriba, gravedad en la base",
               title_fontsize=8)
    fig.savefig(os.path.join(RAIZ, "figuras", "12_muones_y_gravedad.png"), dpi=150,
                bbox_inches="tight", pad_inches=0.15)
    print("figura 12 escrita")


if __name__ == "__main__":
    main()
