"""Microgravimetría: ¿qué huecos de la base de la Gran Pirámide vería un estudio de gravedad?

Un hueco de volumen V en caliza de 2,2 t/m³ es un déficit de masa; su efecto en la componente
vertical de la gravedad se calcula con la fórmula exacta del prisma rectangular (Nagy 1966;
Plouff 1976). 1 µGal = 1e-8 m/s².

Estaciones accesibles consideradas (todas existen hoy; algunas requieren permiso):
- anillo exterior a ras de suelo, a 2 m de la base, cada 5 m;
- escalones de las caras a 5, 10, 15 y 20 m de altura, cada 5 m (sobre la superficie actual);
- corredor descendente (desde la entrada hasta la Cámara Subterránea) y Cámara Subterránea;
- túnel de al-Mamún; corredor y Cámara de la Reina; Gran Galería; Cámara del Rey.

Ruido por estación: instrumento moderno (~1–2 µGal de repetibilidad) + heterogeneidad de los
bloques y errores del modelo de masas de la propia pirámide. Se usan 3 µGal (nominal) y 6 µGal
(pesimista), y se elimina en cada grupo de estaciones una tendencia lineal (para no confundir un
hueco con un gradiente de densidad a gran escala).
"""
from __future__ import annotations

import math

import numpy as np

from . import geometria as g

G = 6.674e-11
UGAL = 1e-8


def gz_prisma(est: np.ndarray, centro, lados, drho_kgm3: float) -> np.ndarray:
    """Componente vertical (hacia abajo positiva = atracción) del prisma en cada estación (m/s²).

    Fórmula de Nagy (1966) para un prisma alineado con los ejes. `est` (n, 3).
    """
    c = np.asarray(centro, float)
    h = np.asarray(lados, float) / 2
    x = np.stack([c[0] - h[0] - est[:, 0], c[0] + h[0] - est[:, 0]], 1)
    y = np.stack([c[1] - h[1] - est[:, 1], c[1] + h[1] - est[:, 1]], 1)
    z = np.stack([c[2] - h[2] - est[:, 2], c[2] + h[2] - est[:, 2]], 1)   # z hacia arriba
    tot = np.zeros(len(est))
    for i in range(2):
        for j in range(2):
            for k in range(2):
                xi, yj, zk = x[:, i], y[:, j], z[:, k]
                r = np.sqrt(xi ** 2 + yj ** 2 + zk ** 2) + 1e-9
                s = (-1) ** (i + j + k)
                with np.errstate(divide="ignore", invalid="ignore"):
                    t = (xi * np.log(np.abs(yj + r) + 1e-12) + yj * np.log(np.abs(xi + r) + 1e-12)
                         - zk * np.arctan(xi * yj / np.where(np.abs(zk) < 1e-12, 1e-12, zk * r)))
                tot += s * t
    # con z hacia arriba, una masa por encima de la estación tira hacia arriba (gz negativo)
    return -G * drho_kgm3 * tot


def _a_lo_largo(p0, p1, paso):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    n = max(int(np.linalg.norm(p1 - p0) // paso) + 1, 2)
    return np.linspace(p0, p1, n)


def estaciones() -> dict[str, np.ndarray]:
    L = g.SEMILADO
    E = {}
    # anillo exterior
    s = np.arange(-L - 2, L + 2.01, 5.0)
    ring = [np.c_[s, np.full_like(s, -L - 2), np.full_like(s, 0.3)],
            np.c_[s, np.full_like(s, L + 2), np.full_like(s, 0.3)],
            np.c_[np.full_like(s, -L - 2), s, np.full_like(s, 0.3)],
            np.c_[np.full_like(s, L + 2), s, np.full_like(s, 0.3)]]
    E["anillo exterior"] = np.vstack(ring)
    # escalones de las caras (superficie actual, ~1 m dentro de la cara original)
    esc = []
    for zz in (5.0, 10.0, 15.0, 20.0):
        m = g.lado(zz) / 2 - g.RETRANQUEO_ACTUAL
        t = np.arange(-m + 2, m - 1.99, 5.0)
        esc += [np.c_[t, np.full_like(t, -m), np.full_like(t, zz)], np.c_[t, np.full_like(t, m), np.full_like(t, zz)],
                np.c_[np.full_like(t, -m), t, np.full_like(t, zz)], np.c_[np.full_like(t, m), t, np.full_like(t, zz)]]
    E["escalones (5–20 m)"] = np.vstack(esc)
    P = g._puntos_clave()
    est = {c.nombre: c for c in g.estructuras_conocidas()}
    # corredor descendente hasta el nivel de la cámara subterránea (≈ −27 m)
    cd, sd = math.cos(math.radians(g.ANG_DESC)), math.sin(math.radians(g.ANG_DESC))
    fin = P["entrada"] + ((P["entrada"][2] + 27.0) / sd) * np.array([0, -cd, -sd])
    E["corredor descendente"] = _a_lo_largo(P["entrada"], fin, 3.0)
    E["Cámara Subterránea"] = np.array([[x, y, -29.0] for x in (-4.0, 0.0, 4.0, 8.0) for y in (-6.0, -3.0, 0.0)])
    E["túnel de al-Mamún"] = _a_lo_largo([g.X_PASAJES - 4.0, g.SEMILADO * (1 - 7 / g.ALTURA), 7.5],
                                         [g.X_PASAJES, P["union"][1], P["union"][2]], 3.0)
    qc = est["Cámara de la Reina"]
    E["corredor y Cámara de la Reina"] = np.vstack([
        _a_lo_largo([g.X_PASAJES, P["base_gg"][1], P["base_gg"][2] - 0.3],
                    [g.X_PASAJES, qc.centro[1] + 2.6, P["base_gg"][2] - 0.3], 3.0),
        np.array([[qc.centro[0] + dx, qc.centro[1] + dy, qc.centro[2] - 2.6] for dx in (-2, 2) for dy in (-2, 2)])])
    E["Gran Galería"] = _a_lo_largo(P["base_gg"], P["cima_gg"], 3.0)
    kc = est["Cámara del Rey"]
    E["Cámara del Rey"] = np.array([[kc.centro[0] + dx, kc.centro[1] + dy, kc.centro[2] - 2.6]
                                    for dx in (-4, 0, 4) for dy in (-2, 2)])
    return E


def _sin_tendencia(v: np.ndarray, est: np.ndarray) -> np.ndarray:
    """Quita la mejor tendencia lineal (a + b·x + c·y + d·z) de un grupo de estaciones."""
    A = np.c_[np.ones(len(est)), est - est.mean(0)]
    coef, *_ = np.linalg.lstsq(A, v, rcond=None)
    return v - A @ coef


def z_gravedad(centro, lados, grupos: dict[str, np.ndarray], sigma_ugal: float,
               drho=-2200.0) -> float:
    """Significación (σ) del hueco combinando todos los grupos, tras quitar tendencias."""
    z2 = 0.0
    for est in grupos.values():
        v = gz_prisma(est, centro, lados, drho) / UGAL
        if len(est) >= 6:
            v = _sin_tendencia(v, est)
        z2 += float(np.sum((v / sigma_ugal) ** 2))
    return math.sqrt(z2)
