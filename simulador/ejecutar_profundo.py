"""Fase 2: robustez del experimento decisivo, prueba a ciegas y huella de las rampas.

    cd simulador && python ejecutar_profundo.py      (~10 min; requiere resultados/04_gran_vacio.json)
"""
from __future__ import annotations

import copy
import json
import time
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from piramide import vacio as v, robustez as rb, aristas_muones as am
from ejecutar_todo import guardar, estilo, TINTA, TENUE, COLORES, RES, FIG


def hipotesis_ajustadas():
    p = RES / "04_gran_vacio.json"
    H = [h for h in v.hipotesis_base() if h.clave != "H6"]     # H6 ya descartada (29σ)
    if p.exists():
        d = json.loads(p.read_text(encoding="utf-8"))
        aj = {h["clave"]: (h["parametro"], h["dy"], h["dz"]) for h in d["hipotesis"]}
        for h in H:
            h.parametro, h.dy, h.dz = aj[h.clave]
    else:
        obs = H[0].cajas()
        for h in H:
            v.ajustar_a_observacion(h, obs)
    return H


def escalar_dias(bib: rb.Biblioteca, clave: str, dias: float) -> rb.Biblioteca:
    b = copy.copy(bib)
    b.puestos = dict(bib.puestos)
    pu = copy.copy(bib.puestos[clave])
    f = dias / pu.dias
    pu.dias = dias
    b.puestos[clave] = pu
    b.mapas = {h: dict(m) for h, m in bib.mapas.items()}
    for h in b.mapas:
        b.mapas[h][clave] = bib.mapas[h][clave] * f
    return b


def main():
    t = time.time()
    H = hipotesis_ajustadas()
    P = rb.puestos_estandar(dias_kc=60.0, dias_d5=7.0)
    print("Construyendo la biblioteca de mapas...", flush=True)
    bib = rb.Biblioteca.construir(H, P)
    print(f"   {sum(len(x) for x in bib.variantes.values())} variantes ({time.time() - t:.0f} s)", flush=True)

    # 1) Separación sin ruido (Asimov) con ajuste conjunto y sistemáticos perfilados
    escenarios = {"Solo QC (2017)": ("QC",), "QC + Cámara del Rey 60 d": ("QC", "KC"),
                  "QC + Cámara de Campbell 7 d": ("QC", "D5")}
    asimov = {}
    for h in H:
        ver = rb.generar_verdad(h, P, 0.7, -0.6)
        asimov[h.clave] = {n: rb.z_asimov(bib, ver, h.clave, u) for n, u in escenarios.items()}
    print("Separación mínima frente a la mejor alternativa:", flush=True)
    for k, d in asimov.items():
        print("   " + k + ": " + ", ".join(f"{n}: {min(z.values()):.1f}σ" for n, z in d.items()), flush=True)

    # 2) Prueba a ciegas con física nominal y alterada
    casos = [("Solo QC (2017)", ("QC",), "nominal"),
             ("QC + KC 60 d", ("QC", "KC"), "nominal"),
             ("QC + KC 60 d, flujo -10 % y índice +0,05", ("QC", "KC"), "perturbado+"),
             ("QC + KC 60 d, flujo +10 % e índice -0,05", ("QC", "KC"), "perturbado-"),
             ("QC + KC 60 d, espectro de Gaisser (extremo)", ("QC", "KC"), "gaisser"),
             ("QC + KC 60 d, caliza 2,35 g/cm³", ("QC", "KC"), "densidad"),
             ("QC + KC 60 d, cámaras desplazadas 1 m", ("QC", "KC"), "estructuras"),
             ("QC + Campbell 7 d", ("QC", "D5"), "nominal")]
    ciegas = {}
    for nombre, usar, fis in casos:
        r = rb.prueba_a_ciegas(bib, n=40, usar=usar, fisica=fis)
        ciegas[nombre] = r
        print(f"   ciegas [{nombre}]: acierto {100 * r['acierto']:.1f} %  ({time.time() - t:.0f} s)", flush=True)

    # 3) Acierto en función de los días en la Cámara del Rey
    dias_kc = [3, 7, 14, 30, 60, 120]
    curva = {}
    for d in dias_kc:
        b = escalar_dias(bib, "KC", d)
        curva[d] = rb.prueba_a_ciegas(b, n=30, usar=("QC", "KC"), semilla=11)["acierto"]
        print(f"   KC {d} días: acierto {100 * curva[d]:.1f} %", flush=True)

    # 4) Huella de las rampas en las aristas
    aristas = []
    for dd in (-0.02, -0.05, -0.1, -0.2):
        for dias in (30, 100, 300):
            r = am.significacion(dd, dias=dias)
            aristas.append(dict(delta_densidad=dd, dias=dias, Z=r["Z"], exceso_max=r["exceso_max"]))
    print("   aristas:", [(a["delta_densidad"], a["dias"], round(a["Z"], 1)) for a in aristas], flush=True)

    guardar("05_robustez.json", dict(
        notas=("Ajuste conjunto (dy, dz y forma de cada hipótesis libres en una rejilla de 75 variantes) "
               "con normalización y gradientes perfilados (±5 %), 2 % de sistemático por bin y "
               "exposición efectiva x0,25. Prueba a ciegas: 40 pseudo-experimentos por hipótesis con "
               "la verdad desplazada al azar ±1,5 m, sección ±15 % y ruido estadístico y sistemático. Biblioteca: posición, forma y sección (x0,75-1,25) libres."),
        asimov=asimov,
        ciegas={k: dict(claves=r["claves"], matriz=r["matriz"], acierto=r["acierto"],
                        margen_mediano=r["margen_mediano"]) for k, r in ciegas.items()},
        acierto_vs_dias_KC=curva))
    guardar("06_aristas.json", dict(
        notas="Detector de 1 m² a 15 m del pie de la cara este, elevación 45°, exposición efectiva x0,25.",
        resultados=aristas))

    # Figuras
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.8))
    for ax, nombre in zip(axs, ["Solo QC (2017)", "QC + KC 60 d", "QC + Campbell 7 d"]):
        r = ciegas[nombre]
        M = np.array(r["matriz"])
        ax.imshow(M, cmap="Blues", vmin=0, vmax=40)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                ax.text(j, i, M[i, j], ha="center", va="center", fontsize=8,
                        color="white" if M[i, j] > 20 else TINTA)
        ax.set_xticks(range(len(r["claves"])), r["claves"], fontsize=8)
        ax.set_yticks(range(len(r["claves"])), r["claves"], fontsize=8)
        ax.set_xlabel("hipótesis elegida", fontsize=8)
        ax.set_ylabel("hipótesis verdadera", fontsize=8)
        ax.set_title(f"{nombre}\nacierto {100 * r['acierto']:.0f} %", fontsize=9, color=TINTA)
    fig.suptitle("Prueba a ciegas: 40 experimentos simulados con ruido por hipótesis", fontsize=10,
                 color=TINTA, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(FIG / "05a_prueba_a_ciegas.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.plot(dias_kc, [100 * curva[d] for d in dias_kc], "o-", color=COLORES[0], lw=1.8)
    ax.axhline(100 * ciegas["Solo QC (2017)"]["acierto"], color=COLORES[1], ls="--", lw=1)
    ax.text(dias_kc[-1], 100 * ciegas["Solo QC (2017)"]["acierto"] + 1.5, "solo datos de 2017",
            color=COLORES[1], fontsize=8, ha="right")
    ax.set_xscale("log")
    ax.set_xticks(dias_kc, [str(d) for d in dias_kc])
    ax.set_ylim(0, 102)
    ax.set_xlabel("Días de exposición en la Cámara del Rey (1 m²)", fontsize=9)
    ax.set_ylabel("% de veces que se identifica la hipótesis verdadera", fontsize=9)
    ax.set_title("¿Cuánto hay que medir para saber qué es el Gran Vacío?", fontsize=10, color=TINTA, loc="left")
    estilo(ax)
    fig.tight_layout()
    fig.savefig(FIG / "05b_acierto_vs_dias.png", dpi=150)
    plt.close(fig)

    r = am.significacion(-0.1, dias=100)
    rej = r["rejilla"]
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
    im = axs[0].imshow(100 * r["mapa_exceso"], origin="lower", cmap="magma", vmin=0,
                       extent=[rej.tx[0], rej.tx[-1], rej.ty[0], rej.ty[-1]], aspect="auto")
    fig.colorbar(im, ax=axs[0]).set_label("exceso de muones (%)", fontsize=8)
    axs[0].set_title("Rampas en las aristas rellenas con un 4,5 % menos de densidad\n"
                     "vistas desde el pie de la cara este", fontsize=9, color=TINTA)
    axs[0].set_xlabel("tan θx", fontsize=8)
    axs[0].set_ylabel("tan θy", fontsize=8)
    for i, dias in enumerate((30, 100, 300)):
        xs = [a["delta_densidad"] for a in aristas if a["dias"] == dias]
        ys = [a["Z"] for a in aristas if a["dias"] == dias]
        axs[1].plot([-100 * x / 2.2 for x in xs], ys, "o-", color=COLORES[i], label=f"{dias} días")
    axs[1].axhline(5, color="#d1495b", ls="--", lw=1)
    axs[1].set_xlabel("Déficit de densidad del relleno (%)", fontsize=9)
    axs[1].set_ylabel("Significación (σ), 1 m²", fontsize=9)
    axs[1].legend(fontsize=8, frameon=False)
    axs[1].set_title("¿Se ven las rampas integradas desde fuera?", fontsize=9, color=TINTA)
    estilo(axs[1])
    fig.tight_layout()
    fig.savefig(FIG / "06_huella_aristas.png", dpi=150)
    plt.close(fig)
    print(f"Hecho en {time.time() - t:.0f} s", flush=True)


if __name__ == "__main__":
    main()
