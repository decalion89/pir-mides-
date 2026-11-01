"""La ley de la mitad de la señal: cuándo un error de modelo fabrica un hueco.

Sea r el residuo (datos − modelo erróneo) y s la huella de un hueco, ambos en unidades de σ y
proyectados fuera de las molestias (normalización, gradientes). Con Δχ²(a) = |r − a s|² − |r|²:
- hueco VACÍO (contraste fijo, a = 1): Δχ² = |s|²(1 − 2ρ), con ρ = ⟨r, s⟩/|s|². Se "detecta" un
  hueco falso si y solo si ρ > 1/2.
- contraste LIBRE (a ajustado, como al dar "un exceso del X %"): â = ρ y Δχ²_min = −ρ²|s|²,
  es decir Z_falso = |ρ| · Z_real.
Si las cuentas esperadas escalan con la exposición λ y el ruido es de Poisson, r, s y σ² escalan
como λ y ρ no cambia: el umbral no depende de cuántos datos se tomen.

Este guion lo comprueba con los detectores de la Cámara de la Reina (rayos submuestreados 4×4 por
casilla, suavizado por dispersión múltiple, aceptancia real de los hodoscopios):
A. ρ(δ) para la hipótesis "Gran Vacío" con errores este-oeste (corrige el doc. 29, que usaba un
   rayo por casilla y aceptancia plana para KEK);
B. invariancia de ρ con la exposición (×0,01 a ×100), con y sin el sistemático del 2 %;
C. Monte Carlo con ruido de Poisson: amplitud ajustada y Z del hueco falso frente a ρ y ρ·Z_real.

Uso: PYTHONPATH=. python ley_media_senal.py → ../resultados/38_ley_media_senal.json
"""
from __future__ import annotations

import dataclasses
import json
import os

import numpy as np
from scipy.ndimage import gaussian_filter

from piramide import cobertura as cb
from piramide import geometria as g
from piramide import muones as mu

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUB = 4
DETECTORES = ("KEK H1 (2016-17)", "KEK H2 (2017)", "Nagoya NE1 (2016)", "Nagoya NE2 (2016)")


class Mapa:
    """Cuentas esperadas por casilla con SUB×SUB rayos por casilla y suavizado SIGMA_RES."""

    def __init__(self, c: cb.Campana, origen, ref):
        self.c, self.o = c, np.asarray(origen, float)
        t = np.arange(-c.tan_max + cb.PASO_TAN / 2, c.tan_max, cb.PASO_TAN)
        self.n = n = t.size
        e1, e2, e3 = cb._ejes(c.eje)
        off = (np.arange(SUB) + 0.5) / SUB - 0.5
        TX, TY = np.meshgrid(t, t, indexing="xy")
        sx = TX[..., None, None] + off[None, None, :, None] * cb.PASO_TAN
        sy = TY[..., None, None] + off[None, None, None, :] * cb.PASO_TAN
        sx, sy = np.broadcast_arrays(sx, sy)
        d = sx[..., None] * e1 + sy[..., None] * e2 + e3
        d /= np.linalg.norm(d, axis=-1, keepdims=True)
        self.dirs = d.reshape(-1, 3)
        self.X0 = cb.opacidad_total(self.o, self.dirs, ref)
        self.cos = self.dirs[:, 2]
        ang = (cb.PASO_TAN ** 2 / (1 + TX ** 2 + TY ** 2) ** 1.5)
        if c.separacion_planos > 0:
            fx = np.clip(1 - c.separacion_planos * np.abs(TX) / c.lado_m, 0, 1)
            fy = np.clip(1 - c.separacion_planos * np.abs(TY) / c.lado_m, 0, 1)
            aeff = fx * fy
        else:
            aeff = np.ones_like(ang)
        bc = TX[..., None] * e1 + TY[..., None] * e2 + e3
        bc /= np.linalg.norm(bc, axis=-1, keepdims=True)
        self.expo = ang * aeff * c.area_m2 * 1e4 * c.dias * 86400.0 * np.clip(bc @ e3, 0, None)
        self.ok = bc[..., 2] > cb.COS_CENIT_MIN
        self.N0 = self.cuentas(self.X0)

    def cuentas(self, X):
        F = mu.flujo_integral(mu.energia_minima(X), self.cos).reshape(self.n, self.n, SUB * SUB).mean(-1)
        N = np.where(self.ok, F * self.expo, 0.0)
        return gaussian_filter(N, cb.SIGMA_RES, mode="nearest", truncate=3.0).reshape(-1)

    def huella(self, caja):
        L = caja.longitud_en_rayos(self.o, self.dirs)
        if not np.any(L > 0):
            return np.zeros_like(self.N0)
        return self.cuentas(np.maximum(self.X0 - mu.DENSIDAD_MATRIZ * L * 100.0, 0)) - self.N0


def proyector(N_mod, t, ok, sig):
    TX, TY = np.meshgrid(t, t, indexing="xy")
    B = np.stack([N_mod, N_mod * TX.reshape(-1), N_mod * TY.reshape(-1)], 1)[ok] / sig[:, None]
    Q, _ = np.linalg.qr(B)
    return lambda v: v - Q @ (Q.T @ v)


def rho(N_true, N_mod, s, t, f_sis=cb.F_SIS):
    ok = (N_true > 5) & (N_mod > 5)
    sig = np.sqrt(N_true + (f_sis * N_true) ** 2)[ok]
    P = proyector(N_mod, t, ok, sig)
    r = P((N_true[ok] - N_mod[ok]) / sig)
    sp = P(s[ok] / sig)
    s2 = float(sp @ sp)
    return float(r @ sp) / s2, s2, float(r @ r)


def main():
    C = {c.nombre: c for c in cb.campanas_publicadas()}
    ref = g.estructuras_conocidas()
    bv = g.anomalias_detectadas()[1]
    out = dict(subrayos=SUB * SUB, A={}, B={}, C={})
    deltas = np.round(np.arange(-1.2, 1.21, 0.1), 2)
    # A. ρ(δ) para cada detector (error este-oeste)
    for k in DETECTORES:
        c = C[k]
        verdad = Mapa(c, c.origen, ref)
        t = np.arange(-c.tan_max + cb.PASO_TAN / 2, c.tan_max, cb.PASO_TAN)
        s = verdad.huella(bv)
        filas = []
        for d in deltas:
            if d == 0:
                continue
            m = Mapa(c, c.origen + np.array([d, 0, 0]), ref)
            p, s2, r2 = rho(verdad.N0, m.N0, s, t)
            filas.append(dict(delta_este_m=float(d), rho=round(p, 3), dchi2_vacio_rel=round(1 - 2 * p, 3),
                              z_falso_contraste_libre_rel=round(abs(p), 3), chi2_fondo_rel=round(r2 / s2, 3)))
        out["A"][k] = dict(distancia_este_al_eje_galeria_m=round(float(c.origen[0] - 7.3), 2), filas=filas)
        print(k, [(f["delta_este_m"], f["rho"]) for f in filas], flush=True)
    # B. invariancia con la exposición (KEK H1, δ = −0,7 m y +0,3 m)
    c = C["KEK H1 (2016-17)"]
    t = np.arange(-c.tan_max + cb.PASO_TAN / 2, c.tan_max, cb.PASO_TAN)
    for d in (-0.7, -0.3, 0.3):
        for f_sis in (0.0, cb.F_SIS):
            fila = {}
            for esc in (0.01, 0.1, 1.0, 10.0, 100.0):
                ce = dataclasses.replace(c, dias=c.dias * esc)
                v = Mapa(ce, ce.origen, ref)
                m = Mapa(ce, ce.origen + np.array([d, 0, 0]), ref)
                p, s2, _ = rho(v.N0, m.N0, v.huella(bv), t, f_sis)
                fila[f"x{esc:g}"] = dict(rho=round(p, 4), z_real=round(float(np.sqrt(s2)), 1))
            out["B"][f"delta={d:+.1f}m, sistematico={f_sis:g}"] = fila
            print("B", d, f_sis, {e: x["rho"] for e, x in fila.items()}, flush=True)
    # C. Monte Carlo de Poisson (KEK H1 con exposición reducida para que Z_real ≈ 10)
    rng = np.random.default_rng(38)
    for d in (-0.7, -0.3):
        ce = dataclasses.replace(c, dias=c.dias * 0.02)
        v = Mapa(ce, ce.origen, ref)
        m = Mapa(ce, ce.origen + np.array([d, 0, 0]), ref)
        s = v.huella(bv)
        ok = (v.N0 > 5) & (m.N0 > 5)
        p_teo, s2, _ = rho(v.N0, m.N0, s, t, 0.0)
        a_hat, z_libre, dchi_vacio = [], [], []
        for _ in range(400):
            y = rng.poisson(v.N0[ok]).astype(float)
            sig = np.sqrt(np.maximum(m.N0[ok], 1.0))
            P = proyector(m.N0, t, ok, sig)
            r = P((y - m.N0[ok]) / sig)
            sp = P(s[ok] / sig)
            a = float(r @ sp) / float(sp @ sp)
            a_hat.append(a)
            z_libre.append(a * np.sqrt(float(sp @ sp)))
            dchi_vacio.append(float(sp @ sp) - 2 * float(r @ sp))
        a_hat, z_libre, dchi_vacio = map(np.array, (a_hat, z_libre, dchi_vacio))
        out["C"][f"delta={d:+.1f}m"] = dict(
            rho_teorico=round(p_teo, 3), z_real=round(float(np.sqrt(s2)), 2),
            amplitud_ajustada_media=round(float(a_hat.mean()), 3), amplitud_ajustada_desv=round(float(a_hat.std()), 3),
            z_falso_medio=round(float(z_libre.mean()), 2), z_falso_predicho=round(p_teo * float(np.sqrt(s2)), 2),
            fraccion_hueco_vacio_preferido=round(float(np.mean(dchi_vacio < 0)), 3))
        print("C", d, out["C"][f"delta={d:+.1f}m"], flush=True)
    with open(os.path.join(RAIZ, "resultados", "38_ley_media_senal.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False, allow_nan=False)


if __name__ == "__main__":
    main()
