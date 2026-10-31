"""Modelo directo de muografía (radiografía con muones cósmicos).

Para cada dirección vista desde un detector se calcula la opacidad (g/cm2) atravesada,
la energía mínima que necesita un muón para cruzarla y el flujo integral de muones que
llega. Comparando el flujo "con" y "sin" una estructura hipotética se obtiene el exceso
relativo y la significación estadística esperada para una exposición dada.

Simplificaciones (documentadas en docs/06):
- espectro de Reyna (2006) a nivel del mar (empalmado con Gaisser por encima de 2 TeV);
- pérdida de energía continua dE/dX = a + bE (roca estándar), sin dispersión múltiple;
- densidad uniforme de caliza 2,2 g/cm3 salvo estructuras explícitas.
Con estas aproximaciones el modelo reproduce el orden de magnitud de las tasas y de los
excesos publicados por ScanPyramids (ver tests/test_muones.py y docs/06).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import geometria as g

A_PERDIDA = 2.17e-3      # GeV por g/cm2 (ionización, roca estándar)
B_PERDIDA = 4.0e-6       # cm2/g (radiativa)
E_UMBRAL_DETECTOR = 0.5  # GeV: muones muy lentos no atraviesan el detector/blindaje


_REYNA = (0.00253, 0.2455, 1.288, -0.2555, 0.0209)


def gaisser_diferencial(E: np.ndarray, cos_t: np.ndarray) -> np.ndarray:
    """Espectro de Gaisser (1990), cm^-2 s^-1 sr^-1 GeV^-1. Sobreestima por debajo de ~20 GeV."""
    c = np.clip(cos_t, 0.05, 1.0)
    return 0.14 * E ** -2.7 * (1.0 / (1.0 + 1.1 * E * c / 115.0)
                               + 0.054 / (1.0 + 1.1 * E * c / 850.0))


def reyna_diferencial(p: np.ndarray, cos_t: np.ndarray) -> np.ndarray:
    """Espectro de Reyna (2006, hep-ph/0604145), cm^-2 s^-1 sr^-1 GeV^-1.

    I(p, θ) = cos^3 θ · I_V(p cos θ), con I_V = c1 p^-(c2 + c3 y + c4 y^2 + c5 y^3), y = log10 p.
    Válido ~1-2000 GeV y para todos los ángulos cenitales; por encima se empalma con Gaisser.
    """
    c = np.clip(cos_t, 0.05, 1.0)
    q = np.asarray(p, float) * c
    y = np.log10(np.maximum(q, 1e-3))
    c1, c2, c3, c4, c5 = _REYNA
    iv = c1 * q ** -(c2 + c3 * y + c4 * y ** 2 + c5 * y ** 3)
    return c ** 3 * iv


def espectro(E: np.ndarray, cos_t: np.ndarray) -> np.ndarray:
    """Espectro usado: Reyna hasta 2 TeV, Gaisser reescalado por encima."""
    E = np.asarray(E, float)
    r = reyna_diferencial(E, cos_t)
    E0 = np.full_like(E, 2000.0)
    esc = reyna_diferencial(E0, cos_t) / gaisser_diferencial(E0, cos_t)
    return np.where(E <= 2000.0, r, gaisser_diferencial(E, cos_t) * esc)


class _TablaFlujo:
    """Tabla precalculada de log I(>E, cosθ) para interpolar rápido."""

    def __init__(self):
        self.logE = np.linspace(np.log(0.1), np.log(2e4), 260)
        self.cos = np.linspace(0.05, 1.0, 96)
        Eg = np.exp(np.linspace(np.log(0.1), np.log(1e6), 3000))
        logI = np.empty((self.logE.size, self.cos.size))
        for j, c in enumerate(self.cos):
            f = espectro(Eg, np.full_like(Eg, c))
            # integral acumulada desde arriba (trapecios en E)
            seg = 0.5 * (f[1:] + f[:-1]) * np.diff(Eg)
            acum = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
            logI[:, j] = np.interp(self.logE, np.log(Eg), np.log(acum + 1e-300))
        self.logI = logI

    def __call__(self, Emin: np.ndarray, cos_t: np.ndarray) -> np.ndarray:
        le = np.clip(np.log(np.maximum(Emin, 0.1)), self.logE[0], self.logE[-1])
        cc = np.clip(cos_t, self.cos[0], self.cos[-1])
        fi = (le - self.logE[0]) / (self.logE[1] - self.logE[0])
        fj = (cc - self.cos[0]) / (self.cos[1] - self.cos[0])
        i0 = np.clip(fi.astype(int), 0, self.logE.size - 2)
        j0 = np.clip(fj.astype(int), 0, self.cos.size - 2)
        di, dj = fi - i0, fj - j0
        L = self.logI
        v = (L[i0, j0] * (1 - di) * (1 - dj) + L[i0 + 1, j0] * di * (1 - dj)
             + L[i0, j0 + 1] * (1 - di) * dj + L[i0 + 1, j0 + 1] * di * dj)
        return np.exp(v)


_TABLA: _TablaFlujo | None = None


def flujo_integral(Emin, cos_t):
    global _TABLA
    if _TABLA is None:
        _TABLA = _TablaFlujo()
    return _TABLA(np.asarray(Emin, float), np.asarray(cos_t, float))


def energia_minima(X_gcm2: np.ndarray) -> np.ndarray:
    """Energía mínima (GeV) para atravesar una opacidad X (g/cm2)."""
    X = np.asarray(X_gcm2, float)
    return E_UMBRAL_DETECTOR + (A_PERDIDA / B_PERDIDA) * np.expm1(B_PERDIDA * X)


@dataclass
class Rejilla:
    """Rejilla angular en (tanθx, tanθy): x = este, y = norte."""
    tx: np.ndarray
    ty: np.ndarray

    @classmethod
    def cuadrada(cls, tx_min, tx_max, ty_min, ty_max, paso):
        tx = np.arange(tx_min + paso / 2, tx_max, paso)
        ty = np.arange(ty_min + paso / 2, ty_max, paso)
        return cls(tx, ty)

    @property
    def paso(self):
        return float(self.tx[1] - self.tx[0]) if self.tx.size > 1 else 0.05

    def direcciones(self, eje=(0.0, 0.0, 1.0)) -> np.ndarray:
        """Direcciones unitarias (hacia el cielo) de cada bin.

        `eje` es el vector al que apunta el telescopio; tanθx se mide a lo largo de la
        horizontal perpendicular al eje (o del este si el eje es vertical) y tanθy a lo
        largo de la tercera dirección (norte si el eje es vertical).
        """
        e3 = np.asarray(eje, float)
        e3 = e3 / np.linalg.norm(e3)
        if abs(e3[2]) > 0.999:
            e1, e2 = np.array([1.0, 0, 0]), np.array([0, 1.0, 0])
        else:
            e1 = np.cross([0, 0, 1.0], e3)
            e1 /= np.linalg.norm(e1)
            e2 = np.cross(e3, e1)
        TX, TY = np.meshgrid(self.tx, self.ty, indexing="xy")
        d = TX[..., None] * e1 + TY[..., None] * e2 + e3
        return (d / np.linalg.norm(d, axis=-1, keepdims=True)).reshape(-1, 3)

    def angulo_solido_bin(self) -> np.ndarray:
        TX, TY = np.meshgrid(self.tx, self.ty, indexing="xy")
        p = self.paso
        return (p * p / (1.0 + TX ** 2 + TY ** 2) ** 1.5).reshape(-1)

    @property
    def forma(self):
        return (self.ty.size, self.tx.size)


def opacidad(origen: np.ndarray, dirs: np.ndarray, estructuras: list[g.Caja],
             densidad: float = g.DENSIDAD_CALIZA, actual: bool = True) -> np.ndarray:
    """Opacidad (g/cm2) a lo largo de cada rayo, dentro de la pirámide.

    `actual=True` usa la forma de hoy (sin revestimiento ni cúspide), que es la que ven
    los detectores.
    """
    L = g.longitud_en_piramide(origen, dirs, actual=actual)
    X = densidad * L
    for c in estructuras:
        X = X + c.delta_densidad * c.longitud_en_rayos(origen, dirs)
    return np.maximum(X, 0.0) * 100.0      # t/m3 * m = g/cm3 * 100 cm


def flujo(origen, dirs, estructuras) -> np.ndarray:
    """Flujo integral por dirección; cero para direcciones por debajo del horizonte."""
    X = opacidad(origen, dirs, estructuras)
    f = flujo_integral(energia_minima(X), dirs[:, 2])
    return np.where(dirs[:, 2] > 0.02, f, 0.0)


@dataclass
class ResultadoMapa:
    rejilla: Rejilla
    flujo_ref: np.ndarray          # cm^-2 s^-1 sr^-1 por bin
    flujo_hip: np.ndarray
    cuentas_ref: np.ndarray        # muones esperados por bin
    cuentas_hip: np.ndarray

    @property
    def exceso(self) -> np.ndarray:
        with np.errstate(divide="ignore", invalid="ignore"):
            e = np.where(self.flujo_ref > 0, self.flujo_hip / self.flujo_ref - 1.0, 0.0)
        return e.reshape(self.rejilla.forma)

    def significacion(self, f_sis: float = 0.0, sigma_bins: float = 0.0) -> float:
        """Significación (σ) con que se distingue `hipótesis` de `referencia`.

        χ² = Σ (N_hip - N_ref)² / (N_ref + (f_sis·N_ref)²), sumado sobre bins, tras
        suavizar ambos mapas con la resolución angular (`sigma_bins`). `f_sis` es un error
        sistemático relativo por bin (modelo de flujo, densidad, geometría exterior).
        """
        n0 = suavizar(self.cuentas_ref.reshape(self.rejilla.forma), sigma_bins).reshape(-1)
        n1 = suavizar(self.cuentas_hip.reshape(self.rejilla.forma), sigma_bins).reshape(-1)
        var = n0 + (f_sis * n0) ** 2
        m = var > 0
        return float(np.sqrt(np.sum((n1[m] - n0[m]) ** 2 / var[m])))


def suavizar(mapa: np.ndarray, sigma_bins: float) -> np.ndarray:
    """Suavizado gaussiano separable (resolución angular del detector)."""
    if sigma_bins <= 0:
        return mapa
    r = int(np.ceil(3 * sigma_bins))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma_bins) ** 2)
    k /= k.sum()
    pad = np.pad(mapa, r, mode="edge")
    tmp = np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 0, pad)
    return np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 1, tmp)


def mapa(origen: np.ndarray, rejilla: Rejilla, referencia: list[g.Caja],
         hipotesis: list[g.Caja], area_m2: float = 1.0, dias: float = 100.0,
         eficiencia: float = 1.0, eje=(0.0, 0.0, 1.0),
         alternativa: list[g.Caja] | None = None) -> ResultadoMapa:
    """Cuentas esperadas para `referencia + hipotesis` frente a `referencia (+ alternativa)`.

    Si se da `alternativa`, el mapa de referencia es `referencia + alternativa`: sirve para
    medir cuánto se distinguen dos hipótesis entre sí desde un punto de observación.
    """
    d = rejilla.direcciones(eje)
    base = referencia + (alternativa or [])
    f0 = flujo(origen, d, base)
    f1 = flujo(origen, d, referencia + hipotesis)
    e3 = np.asarray(eje, float) / np.linalg.norm(eje)
    expo = rejilla.angulo_solido_bin() * area_m2 * 1e4 * dias * 86400.0 * eficiencia
    expo = expo * np.clip(d @ e3, 0, None)     # proyección del área del detector plano
    return ResultadoMapa(rejilla, f0, f1, f0 * expo, f1 * expo)
