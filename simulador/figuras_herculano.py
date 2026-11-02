"""Figura del comentario sobre el cerebro vitrificado de Herculano (doc. 35)."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import herculano_vidrio as hv

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(RAIZ, "resultados", "44_herculano_vidrio.json")))
fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.2))
# (a) ritmos de enfriamiento
nombres, val, col = [], [], []
for caso, v in d["ritmo_enfriamiento_craneo_K_s"].items():
    for p, r in v.items():
        lugar = {"borde_del_cerebro": "brain edge", "a_1cm_del_hueso": "1 cm inside bone", "centro": "centre"}[p]
        hip = {"generoso": "generous", "muy generoso": "very generous", "realista": "realistic"}[caso.split(" (")[0]]
        nombres.append(f"skull: {lugar}\n({hip})")
        val.append(r)
        col.append("#4a6fa5")
for tam, r in d["ritmo_enfriamiento_fragmento_suelto_K_s"].items():
    nombres.append(f"free fragment {tam}\n(still air)")
    val.append(r)
    col.append("#c98b2b")
orden = np.argsort(val)
y = np.arange(len(val))
ax[0].barh(y, np.array(val)[orden], color=np.array(col)[orden])
ax[0].set_yticks(y)
ax[0].set_yticklabels(np.array(nombres)[orden], fontsize=6.5)
ax[0].set_xscale("log")
ax[0].axvline(1000, color="#b22222", ls="--")
ax[0].text(900, 0.2, "1000 K/s\n(Giordano et al.) ", color="#b22222", fontsize=8, ha="right", va="bottom")
ax[0].set_xlabel("cooling rate when crossing 510 °C (K/s)")
ax[0].set_title("(a) Physically possible cooling rates", fontsize=10)
# (b) Tf vs ritmo
q = np.logspace(-2, 3, 100)
tf = np.array([hv.t_ficticia(x) - 273.15 for x in q])
ax[1].plot(q, tf, color="#333")
ax[1].axhspan(315, 465, color="#c98b2b", alpha=0.25, label="burial deposits 315–465 °C")
ax[1].axvspan(0.08, 1.7, color="#4a6fa5", alpha=0.25, label="inside the skull (this work)")
ax[1].plot([1000], [510], "o", color="#b22222", label="inferred in the paper (1000 K/s, 510 °C)")
ax[1].set_xscale("log")
ax[1].set_xlabel("cooling rate (K/s)")
ax[1].set_ylabel("fictive temperature (°C)")
ax[1].set_title("(b) Tf implied by the paper's own kinetics (E = 390 kJ/mol)", fontsize=10)
ax[1].legend(fontsize=7, loc="upper left")
fig.tight_layout()
os.makedirs(os.path.join(RAIZ, "preprint", "herculano"), exist_ok=True)
fig.savefig(os.path.join(RAIZ, "preprint", "herculano", "fig1_cooling.png"), dpi=200)
print("ok")
