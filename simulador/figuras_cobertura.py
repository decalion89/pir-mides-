"""Figuras del mapa de exclusión (08a: cortes; 08b: volumen sin explorar por tamaño).

Uso: PYTHONPATH=. python figuras_cobertura.py   (tras estudio_cobertura.py)
"""
from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from piramide import cobertura as cb
from piramide import geometria as g

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# rampa secuencial azul (más oscuro = hueco más pequeño ya detectable); gris = sin explorar
COLORES = ["#0d366b", "#1c5cab", "#3987e5", "#6da7ec", "#9ec5f4", "#e4e2dd"]
ETIQ = ["≤ 2 m", "3 m", "5 m", "8 m", "12 m", "no detectable (> 12 m)"]
TINTA, TINTA2 = "#1f1f1d", "#6b6a66"


def clase(Z, tamanos, umbral):
    """0..4 = menor tamaño detectable (2,3,5,8,12 m); 5 = ninguno."""
    orden = np.argsort(tamanos)              # 2,3,5,8,12
    out = np.full(len(Z), 5)
    for k, j in enumerate(orden[::-1]):      # de 12 a 2: sobrescribe con el menor
        out[Z[:, j] >= umbral] = len(orden) - 1 - k
    return out


def _estilo(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(TINTA2)
    ax.tick_params(colors=TINTA2, labelsize=8)


def corte(ax, P, cls, eje_fijo, valor, paso, titulo, extra_detectores=()):
    sel = np.abs(P[:, eje_fijo] - valor) <= paso / 2
    h = 0 if eje_fijo == 1 else 1           # horizontal: x si se fija y; y si se fija x
    Q = P[sel]
    ux = np.unique(Q[:, h])
    uz = np.unique(Q[:, 2])
    img = np.full((uz.size, ux.size), np.nan)
    ix = np.searchsorted(ux, Q[:, h])
    iz = np.searchsorted(uz, Q[:, 2])
    img[iz, ix] = cls[sel]
    cmap = ListedColormap(COLORES)
    cmap.set_bad("white")
    ax.imshow(np.ma.masked_invalid(img), origin="lower", cmap=cmap, vmin=-0.5, vmax=5.5,
              extent=(ux[0] - paso / 2, ux[-1] + paso / 2, uz[0] - paso / 2, uz[-1] + paso / 2),
              interpolation="nearest", aspect="equal")
    L = g.SEMILADO
    ax.plot([-L, 0, L], [0, g.ALTURA, 0], color=TINTA, lw=1.0)
    ax.axhline(0, color=TINTA2, lw=0.6)
    for c in cb.referencia_actual():
        if c.delta_densidad >= 0:
            continue
        cx, cy, cz = c.centro
        if abs((cx, cy)[eje_fijo] - valor) < 6:
            ax.plot((cx, cy)[h], cz, "s", ms=2.5, color=TINTA, mew=0)
    for nombre, o, estilo in extra_detectores:
        ax.plot(o[h], o[2], estilo, ms=6, color="#c2410c" if "propuesto" in nombre else TINTA,
                mew=1.2, mfc="white")
    ax.set_title(titulo, fontsize=9, color=TINTA, loc="left")
    ax.set_ylim(-32, g.ALTURA + 4)
    _estilo(ax)


def main():
    d = np.load(os.path.join(RAIZ, "resultados", "19_cobertura.npz"))
    P, Z, T, ocup = d["P"], d["Z_publicadas"], d["tamanos"], d["ocupado"]
    paso = float(np.min(np.diff(np.unique(P[:, 0]))))
    cls = clase(Z, T, 5.0)
    cls[ocup] = 5
    pub = cb.campanas_publicadas()
    det = [(c.nombre, c.origen, "o") for c in pub]
    sc = [("propuesto: Cámara Subterránea", np.array([2.0, -3.0, -27.0]), "D")]
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.6), constrained_layout=True)
    xs = np.unique(P[:, 0])
    x_sec = xs[np.argmin(np.abs(xs - g.X_PASAJES))]
    corte(axs[0], P, cls, 0, x_sec, paso,
          f"Corte norte-sur por los pasajes (x = {x_sec:.0f} m). Norte a la derecha",
          det + sc)
    axs[0].set_xlabel("y (m, norte +)", fontsize=8, color=TINTA2)
    axs[0].set_ylabel("altura (m)", fontsize=8, color=TINTA2)
    ys = np.unique(P[:, 1])
    y_sec = ys[np.argmin(np.abs(ys - 0.0))]
    corte(axs[1], P, cls, 1, y_sec, paso, f"Corte este-oeste por el centro (y = {y_sec:.0f} m)",
          sc)
    axs[1].set_xlabel("x (m, este +)", fontsize=8, color=TINTA2)
    hand = [Patch(color=c, label=l) for c, l in zip(COLORES, ETIQ)]
    fig.legend(handles=hand, loc="outside lower center", ncol=6, fontsize=8, frameon=False,
               title="Menor hueco cúbico que ya se habría detectado (≥ 5σ) con las campañas publicadas",
               title_fontsize=8)
    fig.savefig(os.path.join(RAIZ, "figuras", "08a_mapa_exclusion_cortes.png"), dpi=150)

    # 08b: fracción sin explorar frente al tamaño: hoy, + Cámara Subterránea
    import json
    r = json.load(open(os.path.join(RAIZ, "resultados", "19_cobertura.json")))
    libre = ~ocup
    fig, ax = plt.subplots(figsize=(6.2, 3.6), constrained_layout=True)
    orden = np.argsort(T)
    tam = T[orden]
    hoy = [np.mean(Z[libre, j] < 5.0) * 100 for j in orden]
    ax.plot(tam, hoy, "-o", color="#256abf", lw=2, ms=8, mec="white", mew=2, label="Hoy (campañas 2016–2020)")
    K = list(d["candidatas"])
    for s_key, mark in (("8", "D"), ("5", "s")):
        Zk = d[f"Z_candidatas_{s_key}"]
        j = int(np.where(T == float(s_key))[0][0])
        for nombre, col in (("Cámara Subterránea", "#c2410c"),
                            ("Cámara Subterránea (4 m², 1 año)", "#7c2d12")):
            k = K.index(nombre)
            v = np.mean(np.sqrt(Z[libre, j] ** 2 + Zk[libre, k] ** 2) < 5.0) * 100
            ax.plot(float(s_key), v, mark, color=col, ms=8, mec="white", mew=2)
            ax.annotate(nombre.replace("Cámara Subterránea", "+ C. Subterránea")
                        .replace(" (4 m², 1 año)", ", 4 m² × 1 año") +
                        ("" if "4 m²" in nombre else ", 1 m² × 100 d"),
                        (float(s_key), v), textcoords="offset points", xytext=(8, -3),
                        fontsize=7, color=TINTA2)
    ax.set_xlabel("lado del hueco cúbico (m)", fontsize=8, color=TINTA2)
    ax.set_ylabel("% del volumen donde NO se habría visto", fontsize=8, color=TINTA2)
    ax.set_ylim(0, 100)
    ax.set_xticks(tam)
    ax.grid(axis="y", color="#e4e2dd", lw=0.6)
    ax.legend(fontsize=8, frameon=False, loc="lower left")
    ax.set_title("Volumen de la Gran Pirámide sin explorar con muones (umbral 5σ)", fontsize=9,
                 color=TINTA, loc="left")
    _estilo(ax)
    fig.savefig(os.path.join(RAIZ, "figuras", "08b_volumen_sin_explorar.png"), dpi=150)
    print("figuras 08a y 08b escritas")


if __name__ == "__main__":
    main()
