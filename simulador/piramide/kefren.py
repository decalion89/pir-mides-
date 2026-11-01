"""La pirámide de Kefrén y el experimento de Alvarez (1968–1969).

Alvarez et al., Science 167, 832–839 (1970):
- dos pares de cámaras de chispas de 1,8 × 1,8 m (≈ 4 m² de área sensible, separadas 0,3 m),
  con 1,2 m de hierro, en la esquina sureste de la Cámara de Belzoni, "just below the base of
  the pyramid, near its center";
- algo más de un millón de muones en varios meses; sensibilidad hasta ~45° del cenit;
- conclusión: "no doubt that we could detect a King's Chamber anywhere above the Belzoni
  Chamber within a cone of half-angle 35 degrees from the vertical"; ese cono "is 19 percent
  of the pyramid's volume"; "we now hope to rearrange the equipment so that we can look through
  the remaining 81 percent".

Geometría de Kefrén: lado original 215,25 m (410 codos), altura original 143,5 m (274 codos);
hoy ~136,4 m. La Cámara de Belzoni (14,15 × 5 m) está excavada en la roca bajo la base, casi
en el eje vertical; aquí se toma su esquina sureste en (5, −1,5) m y el detector a ras de la
base (el aire de la cámara queda por encima).
"""
from __future__ import annotations

import math

import numpy as np

from . import cobertura as cb
from . import geometria as g

LADO = 215.25
ALTURA = 143.5
ALTURA_ACTUAL = 136.4
SEMI = LADO / 2
TAN_CARA = ALTURA / SEMI
DENSIDAD = 2.2
ORIGEN_ALVAREZ = np.array([5.0, -1.5, -0.5])


def longitud(origen: np.ndarray, dirs: np.ndarray) -> np.ndarray:
    """Longitud de cada semirrecta dentro de la Kefrén actual (Cyrus-Beck, como en Keops)."""
    o = np.asarray(origen, float)
    k = TAN_CARA
    n = np.array([[k, 0, 1], [-k, 0, 1], [0, k, 1], [0, -k, 1], [0, 0, -1], [0, 0, 1]], float)
    c = np.array([ALTURA, ALTURA, ALTURA, ALTURA, 0.0, ALTURA_ACTUAL])
    nd = dirs @ n.T
    holgura = c - n @ o
    with np.errstate(divide="ignore", invalid="ignore"):
        t = holgura[None, :] / nd
    t_sal = np.min(np.where(nd > 1e-12, t, np.inf), axis=1)
    t_ent = np.max(np.where(nd < -1e-12, t, -np.inf), axis=1)
    fuera = np.any((np.abs(nd) <= 1e-12) & (holgura[None, :] < 0), axis=1)
    L = np.clip(t_sal - np.maximum(t_ent, 0.0), 0.0, None)
    L[fuera] = 0.0
    L[~np.isfinite(L)] = 0.0
    return L


def opacidad(origen, dirs):
    """g/cm²: caliza de Kefrén + roca madre si el detector está bajo la base."""
    X = DENSIDAD * longitud(origen, dirs) * 100.0
    z0 = float(origen[2])
    if z0 < 0:
        X = X + cb.DENSIDAD_ROCA_MADRE * (-z0) / np.clip(dirs[:, 2], 1e-6, None) * 100.0
    return X


def voxeles(paso: float = 4.0) -> np.ndarray:
    xs = np.arange(-SEMI + paso / 2, SEMI, paso)
    zs = np.arange(paso / 2, ALTURA_ACTUAL, paso)
    P = np.array([(x, y, z) for z in zs for y in xs for x in xs])
    lim = SEMI * (1 - P[:, 2] / ALTURA)
    return P[(np.abs(P[:, 0]) <= lim) & (np.abs(P[:, 1]) <= lim)]


def fraccion_en_cono(P: np.ndarray, origen=ORIGEN_ALVAREZ, semiangulo=35.0) -> float:
    v = P - origen
    cosz = v[:, 2] / np.linalg.norm(v, axis=1)
    return float(np.mean(cosz >= math.cos(math.radians(semiangulo))))


def camara_del_rey(centro) -> g.Caja:
    """Hueco del tamaño de la Cámara del Rey (10,47 E-O × 5,23 N-S × 5,84 m)."""
    return g.Caja("cámara tipo Rey", tuple(centro), (10.47, 5.23, 5.84))


def campana_alvarez(dias: float) -> cb.Campana:
    # 1,8 × 1,8 m, planos a 0,3 m: área efectiva casi plana hasta tanθ = 1 (45°)
    return cb.Campana("Alvarez 1968-69 (Belzoni)", "alvarez", ORIGEN_ALVAREZ.copy(),
                      np.array([0, 0, 1.0]), 1.0, 3.24, dias, separacion_planos=0.3, lado_m=1.8,
                      referencia="Alvarez+1970")


def eventos_en_cono(c: cb.Campana, semiangulo=35.0) -> float:
    p = c._pre
    cos = p["cos"]
    return float(p["N0"][cos >= math.cos(math.radians(semiangulo))].sum())


def campanas_propuestas(area_m2: float = 2.0, dias: float = 180.0) -> list[cb.Campana]:
    """Emulsiones modernas en la Cámara de Belzoni: una cenital y cuatro inclinadas 45°."""
    o = ORIGEN_ALVAREZ.copy()
    C = [cb.Campana("Belzoni, cenital", "nagoya", o, np.array([0, 0, 1.0]), 1.0, area_m2, dias,
                    referencia="propuesta")]
    for nom, d in (("norte", (0, 1)), ("sur", (0, -1)), ("este", (1, 0)), ("oeste", (-1, 0))):
        eje = np.array([d[0], d[1], 1.0])
        C.append(cb.Campana(f"Belzoni, inclinada 45° al {nom}", "nagoya", o, eje / np.linalg.norm(eje),
                            1.0, area_m2, dias, referencia="propuesta"))
    return C
