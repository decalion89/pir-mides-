"""Figura del artículo de síntesis "ceguera al ritmo" (docs. 34–36)."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda n: json.load(open(os.path.join(RAIZ, "resultados", n)))
q = R("42_qin_mercurio.json")["A_difusion"]["cociente_lidar_sobre_difusion"]
h = R("44_herculano_vidrio.json")["ritmo_enfriamiento_craneo_K_s"]
hv = [v for c in h.values() for v in c.values()]
s = R("45_saqqara_balance.json")["demanda_de_los_autores_18Mm3"]["fraccion_cubierta_con_perdidas"]
casos = [
    ("Qin Shi Huang tomb:\nmeasured Hg flux / max. diffusive flux", q["mediana"], q["p05"], q["p95"]),
    ("Herculaneum brain:\ninferred cooling rate / max. rate in skull", 1000 / np.median(hv), 1000 / max(hv), 1000 / min(hv)),
    ("Djoser hydraulic lift:\nrequired water / water deliverable", 1 / s["mediana"], 1 / s["p95"], 1 / s["p05"]),
]
fig, ax = plt.subplots(figsize=(7.2, 3.2))
y = np.arange(len(casos))[::-1]
for yi, (nom, med, lo, hi) in zip(y, casos):
    ax.plot([lo, hi], [yi, yi], color="#4a6fa5", lw=6, alpha=0.45, solid_capstyle="butt")
    ax.plot(med, yi, "o", color="#1f3b63", ms=8)
    ax.text(hi * 1.25, yi, f"×{med:,.0f}" if med >= 10 else f"×{med:.1f}", va="center", fontsize=9)
ax.axvline(1, color="#b22222", ls="--")
ax.text(1.05, y.max() + 0.45, "physically allowed (= 1)", color="#b22222", fontsize=8)
ax.set_yticks(y)
ax.set_yticklabels([c[0] for c in casos], fontsize=8)
ax.set_xscale("log")
ax.set_xlim(0.7, 1e5)
ax.set_ylim(-0.6, y.max() + 0.8)
ax.set_xlabel("claim ÷ physical rate limit (median and 90 % range)")
fig.tight_layout()
fig.savefig(os.path.join(RAIZ, "preprint", "ritmo", "fig1_rate_blindness.png"), dpi=200)
print([(c[0].split(':')[0], round(c[1], 1), round(c[2], 1), round(c[3], 1)) for c in casos])
