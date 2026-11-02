"""Reproduce todos los resultados del proyecto.

    cd simulador && python ejecutar_todo.py [--rapido]

Escribe resultados/*.json y figuras/*.png en la raíz del repositorio.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from piramide import geometria as g, muones as mu, vacio as v, granito as gr
from piramide import montecarlo as mc, obra, rampas
from piramide.fisica import Parametros, mu_desde_djehutihotep

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "resultados"
FIG = RAIZ / "figuras"
RES.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

TINTA, TENUE, REJ = "#1f2933", "#6b7785", "#d9dee4"
COLORES = ["#2f6db3", "#d1495b", "#3a9d5d", "#e0a030", "#7a5195", "#4c4c4c", "#00a6a6",
           "#b56576", "#6d8b74", "#a0522d"]


def guardar(nombre, datos):
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, float) and not math.isfinite(o):
            return None
        raise TypeError(type(o))
    txt = json.dumps(datos, default=conv, ensure_ascii=False, indent=2)
    txt = txt.replace("Infinity", "null").replace("NaN", "null")
    (RES / nombre).write_text(txt, encoding="utf-8")


def estilo(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=TENUE, labelsize=8)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(TENUE)
    ax.grid(color=REJ, lw=0.5)
    ax.set_axisbelow(True)


# 1 -----------------------------------------------------------------------------------------
def validacion():
    ref = g.estructuras_conocidas()
    det = g.detectores_publicados()["Cámara de la Reina (NE/H)"]
    r_tot = mu.mapa(det, mu.Rejilla.cuadrada(-1, 1, -1, 1, 0.02), ref, [], area_m2=0.45, dias=98)
    out = {"muones_NE1_previstos": float(r_tot.cuentas_ref.sum()), "muones_NE1_publicados": 4.4e6}
    bv = g.anomalias_detectadas()[1]
    r = v.firma_qc([bv], dias=98)
    out["exceso_pico_suavizado_BV_QC"] = v.pico_suavizado(r)
    out["exceso_publicado_KEK"] = [0.052, 0.11]
    out["Z_BV_QC_modelo"] = r.significacion(0.02, v.SIGMA_RES) * v.FACTOR_REALISMO
    out["Z_BV_QC_publicado_NE1"] = 13.7
    # exterior norte (CEA): 2 telescopios de 0,25 m2, ~2 meses
    o = np.array([g.X_PASAJES, g.SEMILADO + 20.0, 2.0])
    eje = np.array([g.X_PASAJES, 17.0, 63.0]) - o
    rN = mu.mapa(o, mu.Rejilla.cuadrada(-0.6, 0.6, -0.6, 0.6, 0.01), ref, [bv], area_m2=0.5,
                 dias=60, eje=eje)
    out["Z_BV_exterior_modelo"] = rN.significacion(0.02, 1.0) * v.FACTOR_REALISMO
    out["Z_BV_exterior_publicado"] = 5.8
    nfc = g.anomalias_detectadas()[0]
    d2 = g.detectores_publicados()["Corredor descendente"]
    rn = mu.mapa(d2, mu.Rejilla.cuadrada(-1, 1, -1, 1, 0.02), ref, [nfc], area_m2=0.45, dias=60)
    out["exceso_max_NFC_desde_corredor"] = float(rn.exceso.max())
    out["Z_NFC_modelo"] = rn.significacion(0.02, 1.0) * v.FACTOR_REALISMO
    out["Z_NFC_publicado"] = "> 10"
    p = Parametros()
    out["mu_implicito_Djehutihotep_200N_350N"] = [mu_desde_djehutihotep(200), mu_desde_djehutihotep(350)]
    guardar("01_validacion.json", out)
    return out


# 2 -----------------------------------------------------------------------------------------
def construccion(n):
    res = mc.ejecutar(n=n)
    muestras = res.pop("_muestras")
    tabla = {k: {kk: vv for kk, vv in d.items() if kk not in ("anios", "personas", "vaux")}
             for k, d in res.items()}
    sens = {k: mc.sensibilidad(res[k], muestras) for k in ("aristas", "recta+palancas", "zigzag")}
    base = Parametros()
    perfiles = {}
    for m in rampas.catalogo():
        r = obra.simular(m, base, 25000, guardar_perfil=True)
        z, d = r.perfil_z, r.perfil_dias
        acum = np.cumsum(d) / base.dias_anio
        i43, i66 = np.searchsorted(z, 43.0), np.searchsorted(z, 66.0)
        perfiles[m.clave] = dict(anios=r.anios, cuello=r.cuello, equipo_max=r.equipo_max,
                                 ventana_43_66_anios=float(acum[i66] - acum[i43]))
    guardar("02_construccion.json", dict(n_muestras=n, criterios=dict(
        anios=mc.CRITERIO_ANIOS, personas=mc.CRITERIO_PERSONAS, volumen_aux=mc.CRITERIO_VOLUMEN_AUX),
        modelos=tabla, sensibilidad=sens, parametros_centrales=perfiles))

    # figura: distribución de años por modelo
    fig, ax = plt.subplots(figsize=(9, 4.8))
    claves = list(res.keys())
    datos = [np.clip(res[k]["anios"], 0, 120) for k in claves]
    bp = ax.boxplot(datos, orientation="horizontal", patch_artist=True, widths=0.6, showfliers=False)
    for i, b in enumerate(bp["boxes"]):
        ok = res[claves[i]]["p_viable"] >= 0.5
        b.set(facecolor="#9cc3e6" if ok else "#f1b6bf", edgecolor=TENUE)
    for e in ("whiskers", "caps", "medians"):
        for l in bp[e]:
            l.set_color(TINTA if e == "medians" else TENUE)
    ax.set_yticks(range(1, len(claves) + 1),
                  [f"{res[k]['nombre']}  (P viable {100 * res[k]['p_viable']:.0f}%)" for k in claves],
                  fontsize=8)
    ax.axvline(20, color="#d1495b", lw=1, ls="--")
    ax.axvline(27, color="#d1495b", lw=0.8, ls=":")
    ax.text(20.5, len(claves) + 0.45, "20 años", color="#d1495b", fontsize=8)
    ax.text(27.5, len(claves) + 0.15, "reinado de Keops ~27", color="#d1495b", fontsize=8)
    ax.set_xlabel("Años de obra con 25 000 personas (Monte Carlo, %d muestras)" % n, fontsize=9)
    ax.set_title("¿Qué métodos de elevación permiten construir la Gran Pirámide a tiempo?",
                 fontsize=10, color=TINTA, loc="left")
    estilo(ax)
    fig.tight_layout()
    fig.savefig(FIG / "02_construccion_anios.png", dpi=150)
    plt.close(fig)

    # figura: el parámetro decisivo, el tiempo de giro en las esquinas
    tg = np.linspace(0.5, 15, 59)
    curvas, umbrales = {}, {}
    cat = {m.clave: m for m in rampas.catalogo()}
    for clave in ("zigzag", "interna", "aristas", "recta+zigzag"):
        ys = []
        for t in tg:
            p = Parametros()
            p.t_giro_min = float(t)
            ys.append(obra.simular(cat[clave], p, 25000).anios)
        curvas[clave] = ys
        ok = [t for t, y in zip(tg, ys) if y <= mc.CRITERIO_ANIOS]
        umbrales[clave] = max(ok) if ok else None
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for i, (k, ys) in enumerate(curvas.items()):
        ax.plot(tg, ys, color=COLORES[i], lw=1.8, label=cat[k].nombre)
    ax.axhline(20, color="#d1495b", lw=1, ls="--")
    ax.set_ylim(0, 80)
    ax.set_xlabel("Minutos que tarda un trineo cargado en girar una esquina", fontsize=9)
    ax.set_ylabel("Años de obra (25 000 personas)", fontsize=9)
    ax.set_title("El tiempo de giro decide si las rampas con esquinas son viables", fontsize=10,
                 color=TINTA, loc="left")
    ax.legend(fontsize=8, frameon=False)
    estilo(ax)
    fig.tight_layout()
    fig.savefig(FIG / "02b_tiempo_de_giro.png", dpi=150)
    plt.close(fig)
    datos = json.loads((RES / "02_construccion.json").read_text(encoding="utf-8"))
    datos["t_giro_maximo_para_20_anios_min"] = umbrales
    guardar("02_construccion.json", datos)
    return tabla, perfiles


# 3 -----------------------------------------------------------------------------------------
def granito(ventana):
    tabla = gr.tabla_metodos()
    resumen = gr.resumen(ventana)
    guardar("03_granito.json", dict(tabla=tabla, resumen=resumen))
    return tabla, resumen


# 4 -----------------------------------------------------------------------------------------
def gran_vacio():
    t0 = time.time()
    H = v.hipotesis_base()
    obs = H[0].cajas()
    for h in H:
        v.ajustar_a_observacion(h, obs)
        print(f"   ajuste {h.clave}: Z_residual_QC = {h.z_residual_qc:.2f}  ({time.time() - t0:.0f} s)",
              flush=True)
    P = v.puestos_candidatos()
    matrices = {}
    for pu in P:
        matrices[pu.clave] = v.matriz_discriminacion(H, pu, dias=100.0, area=1.0)
    pares = [("H1", "H2"), ("H1", "H3"), ("H2", "H3"), ("H1", "H4"), ("H1", "H5")]
    idx = {h.clave: i for i, h in enumerate(H)}
    dias = {}
    for clave_p in ("QC", "GG", "KC", "D1", "D5"):
        pu = [p for p in P if p.clave == clave_p][0]
        dias[clave_p] = {f"{a}-{b}": v.dias_para_5_sigma(H[idx[a]], H[idx[b]], pu) for a, b in pares}
    houdin = {}
    for z0 in (0.0, 43.0):
        for w in (1.8, 2.6):
            d = v.visibilidad_rampa_interna(z0, ancho=w, alto=w)
            houdin[f"z0={z0:g}_seccion={w:g}"] = {k: d[k] for k in
                                                   ("exceso_max_suavizado", "exceso_max_en_aceptancia", "z_aceptancia")}
    guardar("04_gran_vacio.json", dict(
        hipotesis=[dict(clave=h.clave, nombre=h.nombre, descripcion=h.descripcion, predice=h.predice,
                        parametro=h.parametro, dy=h.dy, dz=h.dz, z_residual_qc=h.z_residual_qc,
                        cajas=[dict(nombre=c.nombre, centro=c.centro, tam=c.tam,
                                    inclinacion=c.inclinacion, delta_densidad=c.delta_densidad)
                               for c in h.cajas()]) for h in H],
        puestos=[dict(clave=p.clave, nombre=p.nombre, origen=p.origen, eje=p.eje, acceso=p.acceso)
                 for p in P],
        Z_100dias_1m2={k: m for k, m in matrices.items()},
        orden_hipotesis=[h.clave for h in H],
        dias_para_5sigma_1m2=dias,
        rampa_interna_houdin_vista_desde_QC_2017=houdin,
        notas="Z incluye 2% de sistemático por bin, resolución ~20 mrad y factor de realismo 0,5."))
    figuras_vacio(H, P, matrices)
    return H, P, matrices, dias, houdin


def figuras_vacio(H, P, matrices):
    # (a) corte N-S por el eje de los corredores
    fig, ax = plt.subplots(figsize=(10, 6.2))
    s = g.SEMILADO
    ax.add_patch(Polygon([(-s, 0), (s, 0), (0, g.ALTURA)], closed=True, fc="#f3eee4", ec=TENUE, lw=0.8))

    def dibuja(c, color, lw=1.0, ls="-", alpha=0.85, fill=False):
        u, vv, w = c._R
        h = np.array(c.tam) / 2
        pts = []
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            p = np.array(c.centro) + a * h[1] * vv + b * h[2] * w
            pts.append((p[1], p[2]))
        ax.add_patch(Polygon(pts, closed=True, fill=fill, fc=color if fill else "none", ec=color,
                             lw=lw, ls=ls, alpha=alpha))

    for c in g.estructuras_conocidas():
        if c.tipo == "granito":
            dibuja(c, "#9a8c98", lw=0.6, alpha=0.35, fill=True)
        else:
            dibuja(c, TINTA, lw=0.8, fill=True, alpha=0.9)
    for c in g.anomalias_detectadas()[:1]:
        dibuja(c, "#d1495b", lw=1.2, fill=True)
    for i, h in enumerate(H):
        for c in h.cajas():
            dibuja(c, COLORES[i], lw=1.3, ls="-" if i < 3 else "--")
        c0 = h.cajas()[0]
        ax.text(64, 100 - 5.0 * i, f"{h.clave}: {h.nombre}", color=COLORES[i], fontsize=8)
    for p in P:
        if abs(p.origen[1]) < 140 and p.origen[2] < 140:
            ax.plot(p.origen[1], p.origen[2], marker="v", ms=7, color="#e0a030", mec=TINTA, mew=0.5)
            etiqueta = p.clave + (" (proyectado: cara este)" if p.clave == "E" else "")
            ax.annotate(etiqueta, (p.origen[1], p.origen[2]), xytext=(4, -10), textcoords="offset points",
                        fontsize=8, color=TINTA)
    ax.text(88, 24, "NFC (2023)", color="#d1495b", fontsize=8)
    ax.set_xlim(-60, 120)
    ax.set_ylim(0, 105)
    ax.set_aspect("equal")
    ax.set_xlabel("Sur  ←  y (m)  →  Norte", fontsize=9)
    ax.set_ylabel("Altura z (m)", fontsize=9)
    ax.set_title("Corte norte-sur de la Gran Pirámide: hipótesis sobre el Gran Vacío (ajustadas a los "
                 "datos de 2017) y puestos de detector (▼)", fontsize=10, color=TINTA, loc="left")
    estilo(ax)
    fig.tight_layout()
    fig.savefig(FIG / "04a_corte_hipotesis.png", dpi=150)
    plt.close(fig)

    # (b) mapas de exceso: desde la QC (2017) y desde la Cámara del Rey / Campbell
    ref = g.estructuras_conocidas()
    puestos = [p for p in P if p.clave in ("QC", "KC", "D5")]
    sel = H[:5]
    fig, axs = plt.subplots(len(puestos), len(sel), figsize=(13, 8.2))
    for i, pu in enumerate(puestos):
        rej = v.rejilla_qc() if pu.clave == "QC" else v.rejilla_puesto()
        for j, h in enumerate(sel):
            dias = v.DIAS_QC_2017 if pu.clave == "QC" else 100
            r = mu.mapa(pu.origen, rej, ref, h.cajas(), area_m2=1.0, dias=dias, eje=pu.eje)
            ex = mu.suavizar(r.exceso, v.SIGMA_RES)
            ax = axs[i, j]
            im = ax.imshow(100 * ex, origin="lower", cmap="magma", vmin=0, vmax=25,
                           extent=[rej.tx[0], rej.tx[-1], rej.ty[0], rej.ty[-1]], aspect="auto")
            if i == 0:
                ax.set_title(f"{h.clave}", fontsize=9, color=COLORES[j])
            if j == 0:
                ax.set_ylabel(f"{pu.clave}\ntan θy", fontsize=8)
            ax.tick_params(labelsize=6)
    cb = fig.colorbar(im, ax=axs, shrink=0.6)
    cb.set_label("exceso de muones (%)", fontsize=8)
    fig.suptitle("Lo que vería cada detector según la hipótesis. Fila QC: casi idénticas (por eso "
                 "en 2017 no se pudo decidir). Filas KC y D5: claramente distintas.", fontsize=10,
                 color=TINTA, x=0.01, ha="left")
    fig.savefig(FIG / "04b_mapas_exceso.png", dpi=140, bbox_inches="tight")
    plt.close(fig)

    # (c) matriz de discriminación por puesto
    fig, axs = plt.subplots(1, len(P), figsize=(15, 2.9))
    claves = [h.clave for h in H]
    for k, pu in enumerate(P):
        M = np.minimum(matrices[pu.clave], 30)
        ax = axs[k]
        ax.imshow(M, cmap="Blues", vmin=0, vmax=30)
        for a in range(len(H)):
            for b in range(len(H)):
                if a != b:
                    ax.text(b, a, f"{matrices[pu.clave][a, b]:.0f}", ha="center", va="center", fontsize=6,
                            color="white" if M[a, b] > 15 else TINTA)
        ax.set_xticks(range(len(H)), claves, fontsize=6)
        ax.set_yticks(range(len(H)), claves, fontsize=6)
        ax.set_title(pu.clave, fontsize=9)
    fig.suptitle("σ con que cada puesto separa cada par de hipótesis (1 m², 100 días)", fontsize=10,
                 color=TINTA, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(FIG / "04c_matriz_discriminacion.png", dpi=150)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true", help="menos muestras de Monte Carlo")
    a = ap.parse_args()
    t = time.time()
    print("1/4 Validación del modelo de muones...", flush=True)
    val = validacion()
    print(json.dumps({k: (round(x, 3) if isinstance(x, float) else x) for k, x in val.items()},
                     ensure_ascii=False), flush=True)
    print("2/4 Construcción (Monte Carlo)...", flush=True)
    tabla, perfiles = construccion(150 if a.rapido else 600)
    for k, d in tabla.items():
        print(f"   {k:15s} P(viable)={d['p_viable']:.2f}  años med={d['anios_med']:.1f} "
              f"[{d['anios_p10']:.1f}-{d['anios_p90']:.1f}]  personas(20 a) med={d['personas_med']:,.0f}",
              flush=True)
    # ventana conservadora: la más corta entre los modelos viables
    ventana = min(perfiles[k]["ventana_43_66_anios"] for k in ("aristas", "recta+palancas"))
    print("3/4 Vigas de granito...", flush=True)
    granito(ventana)
    print("4/4 Gran Vacío: ajuste, discriminación y rampa interna...", flush=True)
    H, P, M, dias, houdin = gran_vacio()
    for p, d in dias.items():
        print(f"   días para 5σ desde {p}: " + ", ".join(f"{k}: {x:.0f}" if math.isfinite(x) else f"{k}: ∞"
                                                       for k, x in d.items()), flush=True)
    print(f"Hecho en {time.time() - t:.0f} s", flush=True)


if __name__ == "__main__":
    main()
