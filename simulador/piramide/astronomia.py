"""Astronomía de los canales de la Gran Pirámide.

¿A qué apuntaban los cuatro canales de la Gran Pirámide y en qué fecha? ¿Es significativo?

- Catálogo: Yale Bright Star Catalogue, 5.ª ed. (Hoffleit & Warren 1991), 9110 estrellas,
  posiciones J2000 y movimientos propios (datos/estrellas/bsc5.dat.gz).
- Movimiento propio lineal; precesión IAU 2006 (Capitaine et al. 2003, ángulos ζ_A, z_A, θ_A).
  Para ±4500 años la precisión es mejor que ~1′, muy por debajo de la incertidumbre de los
  ángulos de los canales.
- Paso por el meridiano en Giza (φ = 29,979° N), con refracción de Bennett.
  Al sur:   h = 90° − φ + δ.
  Al norte: h = 90° + φ − δ (culminación superior entre el cenit y el polo).
"""
from __future__ import annotations

import gzip
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

RUTA = Path(__file__).resolve().parents[2] / "datos" / "estrellas" / "bsc5.dat.gz"
LAT_GIZA = 29.9792
ARCSEC = math.pi / (180 * 3600)

# Ángulos medidos por Gantenbrink (Upuaut), con su incertidumbre (1σ, grados)
CANALES = {
    "Rey sur": dict(angulo=45.0, sigma=0.2, lado="S", fuente="Gantenbrink: media 45° (pendiente 1:1)"),
    "Rey norte": dict(angulo=32.6, sigma=0.3, lado="N", fuente="Gantenbrink: 32,6° del bloque 6 a la salida (media 32,47°)"),
    "Reina sur": dict(angulo=39.61, sigma=1.0, lado="S", fuente="Gantenbrink: 39,6078°, 24 medidas en 28 m (margen declarado ±2°)"),
    "Reina norte": dict(angulo=39.1, sigma=1.5, lado="N", fuente="Gantenbrink: ~39,1° estimado (tramo alto no medido; abajo 33,3-40,1°)"),
}


@dataclass
class Catalogo:
    hr: np.ndarray
    nombre: np.ndarray
    ra: np.ndarray      # rad J2000
    dec: np.ndarray     # rad J2000
    pmra: np.ndarray    # μα·cosδ, arcsec/año
    pmde: np.ndarray    # arcsec/año
    vmag: np.ndarray


def cargar(ruta: Path = RUTA, vmax: float = 6.5) -> Catalogo:
    hr, nom, ra, de, pa, pd, vm = [], [], [], [], [], [], []
    for l in gzip.open(ruta, "rt", encoding="latin1"):
        try:
            rah, ram, ras = int(l[75:77]), int(l[77:79]), float(l[79:83])
            sg = -1 if l[83] == "-" else 1
            ded, dem, des = int(l[84:86]), int(l[86:88]), int(l[88:90])
            v = float(l[102:107])
        except ValueError:
            continue              # entradas sin posición (novas, objetos retirados)
        if v > vmax:
            continue
        hr.append(int(l[0:4]))
        nom.append(l[4:14].strip())
        ra.append(math.radians(15 * (rah + ram / 60 + ras / 3600)))
        de.append(math.radians(sg * (ded + dem / 60 + des / 3600)))
        pa.append(float(l[148:154] or 0))
        pd.append(float(l[154:160] or 0))
        vm.append(v)
    return Catalogo(*(np.array(x) for x in (hr, nom, ra, de, pa, pd, vm)))


def _precesion(T: float) -> np.ndarray:
    """Matriz de precesión J2000 -> época (T en siglos julianos desde J2000), IAU 2006."""
    z1 = (2.650545 + 2306.083227 * T + 0.2988499 * T ** 2 + 0.01801828 * T ** 3
          - 0.000005971 * T ** 4 - 0.0000003173 * T ** 5) * ARCSEC
    z2 = (-2.650545 + 2306.077181 * T + 1.0927348 * T ** 2 + 0.01826837 * T ** 3
          - 0.000028596 * T ** 4 - 0.0000002904 * T ** 5) * ARCSEC
    th = (2004.191903 * T - 0.4294934 * T ** 2 - 0.04182264 * T ** 3
          - 0.000007089 * T ** 4 - 0.0000001274 * T ** 5) * ARCSEC

    def Rz(a):
        c, s = math.cos(a), math.sin(a)
        return np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])

    def Ry(a):
        c, s = math.cos(a), math.sin(a)
        return np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])

    return Rz(-z2) @ Ry(th) @ Rz(-z1)


def declinacion(cat: Catalogo, anio: float) -> np.ndarray:
    """Declinación media de la fecha (grados) en el año astronómico `anio` (−2559 = 2560 a. C.)."""
    dt = anio - 2000.0
    dec = cat.dec + cat.pmde * dt * ARCSEC
    ra = cat.ra + cat.pmra * dt * ARCSEC / np.cos(cat.dec)
    v = np.stack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)])
    w = _precesion(dt / 100.0) @ v
    return np.degrees(np.arcsin(np.clip(w[2], -1, 1)))


def refraccion(h_aparente: float) -> float:
    """Refracción de Bennett (grados) para una altura aparente en grados."""
    return (1.0 / math.tan(math.radians(h_aparente + 7.31 / (h_aparente + 4.4)))) / 60.0


def declinacion_objetivo(angulo: float, lado: str, lat: float = LAT_GIZA) -> float:
    """Declinación que tiene que tener una estrella para culminar a lo largo del canal."""
    h = angulo - refraccion(angulo)       # altura verdadera
    return h - 90.0 + lat if lado == "S" else 90.0 + lat - h


def anio_bc(anio_astronomico: float) -> float:
    return 1 - anio_astronomico


def emparejar(cat: Catalogo, anios: np.ndarray) -> dict:
    """Declinaciones de todas las estrellas en una rejilla de años: (n_anios, n_estrellas)."""
    return np.array([declinacion(cat, a) for a in anios])
