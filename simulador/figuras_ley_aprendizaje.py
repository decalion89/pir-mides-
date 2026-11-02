"""Figura 13: ritmo de construcción de pirámides por reinado (m³/año), con su intervalo."""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TINTA, TINTA2 = "#1f1f1d", "#6b6a66"


def main():
    r = json.load(open(os.path.join(RAIZ, "resultados", "28_ley_aprendizaje.json")))
    t = r["tabla"]
    fig, ax = plt.subplots(figsize=(9.5, 4.2), constrained_layout=True)
    x = np.arange(len(t))
    for i, f in enumerate(t):
        lo, hi = f["ritmo_m3_ano"]
        col = "#256abf" if f["terminada"] else "#9ec5f4"
        ax.plot([i, i], [lo, hi], color=col, lw=6, solid_capstyle="round")
    tc = r["techo"]
    ax.axhspan(tc["Rmax_p05"], tc["Rmax_p95"], color="#c2410c", alpha=0.15, lw=0)
    ax.axhline(tc["Rmax_m3_ano_mediana"], color="#c2410c", lw=1.2)
    ax.text(len(t) - 0.5, tc["Rmax_m3_ano_mediana"] * 1.12,
            f"techo ≈ {tc['Rmax_m3_ano_mediana'] / 1000:.0f} 000 m³/año (≈ {tc['Rmax_m3_ano_mediana'] / 365:.0f} m³/día)",
            ha="right", fontsize=8, color="#c2410c")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([f["rey"] for f in t], rotation=55, ha="right", fontsize=8, color=TINTA2)
    ax.set_ylabel("ritmo = volumen / años de reinado (m³/año)", fontsize=8, color=TINTA2)
    ax.tick_params(colors=TINTA2, labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#e4e2dd", lw=0.6)
    ax.set_title("Pirámides del Reino Antiguo: subida en una generación, techo durante tres reinados y caída por decisión\n"
                 "(barras: intervalo por la incertidumbre del reinado; claro: pirámide inacabada)",
                 fontsize=9, color=TINTA, loc="left")
    fig.savefig(os.path.join(RAIZ, "figuras", "13_ritmo_de_construccion.png"), dpi=150)
    print("figura 13 escrita")


if __name__ == "__main__":
    main()
