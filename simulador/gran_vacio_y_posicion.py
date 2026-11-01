"""¿Puede un error en la posición de los detectores de la Cámara de la Reina fabricar el Gran Vacío?

Se simulan (Asimov) las cuentas de NE1, NE2 y KEK H1 con las estructuras conocidas y SIN Gran
Vacío. Se analizan con los detectores desplazados δ (error común: la misma referencia topográfica
equivocada para todos), con normalización y gradientes lineales libres por detector (perfilados).
Para cada caso:
- Δχ² de la hipótesis "Gran Vacío" en su posición publicada;
- la caja del tamaño del Gran Vacío que más mejora el ajuste en una rejilla sobre la Gran Galería,
  por detector y en el ajuste conjunto (¿triangulan las señales falsas en el mismo sitio?);
- χ² de fondo y número de casillas (¿delata el mal ajuste el error de posición?).
Δχ² en unidades calibradas (factor de Nagoya 0,437 en σ; docs/17). Señal real: 13,7σ (Δχ² ≈ 188).

Con el argumento `fino`: barrido fino (0,1–1,2 m, este y oeste) para los hodoscopios KEK H1 y H2, que
están casi bajo el eje de la Gran Galería; se da la señal falsa como fracción de la que daría un
Gran Vacío real en el mismo detector (independiente de la calibración).

Uso: PYTHONPATH=. python gran_vacio_y_posicion.py [fino]
     → ../resultados/37_gran_vacio_y_posicion.json  (o 37b_..._fino.json)
"""
import json
import os
import sys

import numpy as np

from piramide import cobertura as cb
from piramide import geometria as g
from piramide import muones as mu

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F2 = 0.437 ** 2
DETECTORES = ("Nagoya NE1 (2016)", "Nagoya NE2 (2016)", "KEK H1 (2016-17)")


def copia(c, origen=None):
    return cb.Campana(c.nombre, c.familia, c.origen if origen is None else origen, c.eje, c.tan_max, c.area_m2, c.dias)


def huella(camp, caja):
    p = camp._pre
    D = p["dirs"].reshape(-1, 3)
    L = caja.longitud_en_rayos(camp.origen, D)
    X0 = p["X0"].reshape(-1)
    X1 = np.maximum(X0 - mu.DENSIDAD_MATRIZ * L * 100.0, 0)
    cos = p["cos"].reshape(-1)
    r = mu.flujo_integral(mu.energia_minima(X1), cos) / np.maximum(mu.flujo_integral(mu.energia_minima(X0), cos), 1e-300)
    return p["N0"].reshape(-1) * (r - 1)


def main():
    C = {c.nombre: c for c in cb.campanas_publicadas()}
    ref = g.estructuras_conocidas()
    bv = g.anomalias_detectadas()[1]
    cx, cy, cz = bv.centro
    cajas = [g.Caja("c", (x, y, z), bv.tam) for x in np.arange(-6.0, 21.0, 3.0)
             for y in np.arange(cy - 16, cy + 17, 4.0) for z in np.arange(cz - 12, cz + 13, 4.0)]
    verdad = {k: cb.preparar(copia(C[k]), ref) for k in DETECTORES}
    S_bv = {k: huella(verdad[k], bv) for k in DETECTORES}
    S = {k: np.array([huella(verdad[k], c) for c in cajas]) for k in DETECTORES}
    out = dict(senal_real_dchi2=round(13.7 ** 2, 1), centro_gran_vacio=list(map(float, bv.centro)),
               tam_gran_vacio=list(map(float, bv.tam)), cajas_en_rejilla=len(cajas), casos=[])
    for direc, u in (("este", (1, 0, 0)), ("norte", (0, 1, 0)), ("arriba", (0, 0, 1))):
        for d in (0.0, 0.5, 1.0, 2.0, 3.0):
            if d == 0.0 and direc != "este":
                continue
            caso = dict(direccion=direc, delta_m=d, detectores={})
            tot_bv, tot_rej, tot_fondo, tot_n = 0.0, np.zeros(len(cajas)), 0.0, 0
            for k in DETECTORES:
                c0 = verdad[k]
                N_true = c0._pre["N0"].reshape(-1)
                t = c0._pre["t"]
                TX, TY = np.meshgrid(t, t, indexing="xy")
                mod = cb.preparar(copia(C[k], c0.origen + d * np.array(u, float)), ref)
                N_mod = mod._pre["N0"].reshape(-1)
                ok = (N_true > 5) & (N_mod > 5)
                sig = np.sqrt(N_true + (cb.F_SIS * N_true) ** 2)[ok]
                B = np.stack([N_mod, N_mod * TX.reshape(-1), N_mod * TY.reshape(-1)], 1)[ok] / sig[:, None]
                Q, _ = np.linalg.qr(B)
                perp = lambda v: v - Q @ (Q.T @ v)
                r = perp((N_true[ok] - N_mod[ok]) / sig)
                Sp = np.array([perp(s[ok] / sig) for s in S[k]])
                rej = (np.sum((r[None] - Sp) ** 2, 1) - np.sum(r ** 2)) * F2
                sb = perp(S_bv[k][ok] / sig)
                dbv = float(np.sum((r - sb) ** 2) - np.sum(r ** 2)) * F2
                fondo = float(np.sum(r ** 2)) * F2
                i = int(np.argmin(rej))
                caso["detectores"][k] = dict(casillas=int(ok.sum()), chi2_fondo=round(fondo, 1),
                                             dchi2_gran_vacio=round(dbv, 1), dchi2_mejor_caja=round(float(rej[i]), 1),
                                             donde=[round(float(x), 1) for x in cajas[i].centro])
                tot_bv += dbv
                tot_rej += rej
                tot_fondo += fondo
                tot_n += int(ok.sum())
            i = int(np.argmin(tot_rej))
            caso["conjunto"] = dict(casillas=tot_n, chi2_fondo=round(tot_fondo, 1), dchi2_gran_vacio=round(tot_bv, 1),
                                    dchi2_mejor_caja=round(float(tot_rej[i]), 1),
                                    donde=[round(float(x), 1) for x in cajas[i].centro])
            out["casos"].append(caso)
            print(json.dumps(caso, ensure_ascii=False), flush=True)
    with open(os.path.join(RAIZ, "resultados", "37_gran_vacio_y_posicion.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False, allow_nan=False)


def barrido_fino():
    C = {c.nombre: c for c in cb.campanas_publicadas()}
    ref = g.estructuras_conocidas()
    bv = g.anomalias_detectadas()[1]
    cx, cy, cz = bv.centro
    cajas = [g.Caja("c", (x, y, z), bv.tam) for x in np.arange(cx - 6, cx + 6.1, 1.0)
             for y in np.arange(cy - 8, cy + 8.1, 4.0) for z in np.arange(cz - 8, cz + 8.1, 4.0)]
    out = dict(precision_modelo_interno_m=0.30, nota="Morishima et al. 2017: 'precision of approximately 30 cm'",
               detectores={})
    for k in ("KEK H1 (2016-17)", "KEK H2 (2017)", "Nagoya NE1 (2016)", "Nagoya NE2 (2016)"):
        c0 = cb.preparar(copia(C[k]), ref)
        N_true = c0._pre["N0"].reshape(-1)
        t = c0._pre["t"]
        TX, TY = np.meshgrid(t, t, indexing="xy")
        s_bv = huella(c0, bv)
        S = np.array([huella(c0, c) for c in cajas])
        filas = []
        for d in (-1.2, -0.9, -0.7, -0.5, -0.3, 0.3, 0.5, 0.7, 0.9, 1.2):
            mod = cb.preparar(copia(C[k], c0.origen + np.array([d, 0.0, 0.0])), ref)
            N_mod = mod._pre["N0"].reshape(-1)
            ok = (N_true > 5) & (N_mod > 5)
            sig = np.sqrt(N_true + (cb.F_SIS * N_true) ** 2)[ok]
            B = np.stack([N_mod, N_mod * TX.reshape(-1), N_mod * TY.reshape(-1)], 1)[ok] / sig[:, None]
            Q, _ = np.linalg.qr(B)
            perp = lambda v: v - Q @ (Q.T @ v)
            r = perp((N_true[ok] - N_mod[ok]) / sig)
            ref_real = float(np.sum(perp(s_bv[ok] / sig) ** 2))      # Δχ² de un Gran Vacío real (sin error)
            dbv = float(np.sum((r - perp(s_bv[ok] / sig)) ** 2) - np.sum(r ** 2))
            rej = np.array([np.sum((r - perp(x[ok] / sig)) ** 2) - np.sum(r ** 2) for x in S])
            i = int(np.argmin(rej))
            filas.append(dict(delta_este_m=d, chi2_fondo_rel=round(float(np.sum(r ** 2)) / ref_real, 3),
                              dchi2_gran_vacio_rel=round(dbv / ref_real, 3),
                              mejor_caja_rel=round(float(rej[i]) / ref_real, 3),
                              donde=[round(float(x), 1) for x in cajas[i].centro],
                              distancia_al_gran_vacio_m=round(float(np.linalg.norm(np.subtract(cajas[i].centro, bv.centro))), 1)))
            print(k, filas[-1], flush=True)
        out["detectores"][k] = dict(distancia_este_al_eje_galeria_m=round(float(c0.origen[0] - 7.3), 2), filas=filas)
    with open(os.path.join(RAIZ, "resultados", "37b_gran_vacio_y_posicion_fino.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    barrido_fino() if "fino" in sys.argv[1:] else main()
