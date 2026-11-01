"""¿Qué parte de la Gran Pirámide ya está explorada con muones, y dónde podría quedar algo oculto?

Mapa de exclusión al estilo de la física de partículas. Para cada punto del interior de la
pirámide y cada tamaño de hueco (cubo de lado s), se calcula con qué significación lo habría
visto cada campaña de muografía publicada. Si la combinación supera el umbral, un hueco así
en ese punto **ya habría sido detectado**: está excluido. Lo que queda por debajo del umbral
es volumen **sin explorar** para ese tamaño.

Campañas publicadas que se modelan (posiciones, áreas y días según los artículos):
- Morishima et al., Nature 552 (2017), Methods:
  - Nagoya NE1 (nicho este de la Cámara de la Reina, 5,8 m al este del eje de la Galería),
    98 días, 0,45 m², |tanθ| ≤ 1; Gran Vacío a 13,7σ;
  - Nagoya NE2 (esquina suroeste, 4,5 m al oeste del eje; 1,1 m al sur de NE1), 140 días,
    0,45 m²; 12,7σ;
  - KEK H1 (esquina sureste), 120 × 120 cm, separación de planos 1,5 m, ~150 días
    (agosto 2016 a enero 2017), aceptancia tanθ ≤ 0,8;
  - KEK H2 (2,9 m al oeste de H1), separación 1,0 m, ~240 días, tanθ ≤ 1,2;
  - CEA G1 y G2 (Micromegas de 0,25 m², a 17 y 23 m frente a la cara norte), 4 de mayo a
    3 de julio de 2017; Gran Vacío a 5,8σ combinado.
- Procureur et al., Nat. Commun. 14, 1144 (2023), Methods:
  - Nagoya EM1–EM4 en el corredor descendente: 0,225 m² cada una; 172, 211 (×3), 211 y 79 días;
  - Nagoya EM5–EM7 en el túnel de al-Mamún: 0,075 m² cada una, 272 días;
  - CEA Joliot (0,25 m², 140 días), Degennes (2 × 0,5 m², 140 días) y Charpak
    (2 × 0,5 m², 158 días) en el corredor descendente y la plataforma del cruce con el
    ascendente.

Calibración: la significación del modelo se escala por familia de detector para reproducir
lo publicado sobre el Gran Vacío (Nagoya NE1/NE2 y CEA G1+G2). KEK y las campañas de 2019
usan el factor de su familia (Nagoya para emulsiones y centelleadores interiores, CEA para
Micromegas).

Las posiciones son aproximadas (±1–3 m); los artículos no dan coordenadas exactas para las
campañas de 2019. Donde hay duda se elige la opción **optimista** (más sensibilidad: área
efectiva plana, combinación en cuadratura de todas las campañas, sin ensuciar por estructuras
conocidas cercanas), de modo que el volumen "sin explorar" que se obtiene es una **cota
inferior**.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

import numpy as np
from scipy.ndimage import gaussian_filter

from . import geometria as g
from . import muones as mu

PASO_TAN = 0.02
SIGMA_RES = 1.0                     # bins (~20 mrad: dispersión múltiple en ~100 m de roca)
F_SIS = 0.02                        # sistemático relativo por bin
SUB_MAX = 6                         # subrayos por eje y bin (adaptativo: ≥4 por ancho del hueco)
COS_CENIT_MIN = math.cos(math.radians(70.0))
DENSIDAD_ROCA_MADRE = 2.3           # t/m3, caliza de la meseta (formación Mokattam)

# Significaciones publicadas del Gran Vacío para calibrar
Z_PUB_NE1, Z_PUB_NE2, Z_PUB_CEA = 13.7, 12.7, 5.8


@dataclass
class Campana:
    nombre: str
    familia: str                    # "nagoya" (emulsión/centelleo interior) o "cea"
    origen: np.ndarray
    eje: np.ndarray
    tan_max: float
    area_m2: float
    dias: float
    separacion_planos: float = 0.0  # >0: hodoscopio de dos planos (área efectiva triangular)
    lado_m: float = 1.2
    referencia: str = ""
    # precálculo
    _pre: dict = field(default_factory=dict, repr=False)


def _y_cara(z):
    return g.SEMILADO * (1.0 - z / g.ALTURA)


def _hacia(o, p):
    v = np.asarray(p, float) - np.asarray(o, float)
    return v / np.linalg.norm(v)


def _qc():
    return [c for c in g.estructuras_conocidas() if c.nombre == "Cámara de la Reina"][0]


def campanas_publicadas() -> list[Campana]:
    qc = _qc()
    cx, cy, cz = qc.centro
    suelo = cz - qc.tam[2] / 2
    y_sur = cy - qc.tam[1] / 2
    X = g.X_PASAJES
    arriba = np.array([0, 0, 1.0])
    P = g._puntos_clave()
    nfc = [c for c in g.anomalias_detectadas() if c.nombre.startswith("Corredor de la cara")][0]
    bv = np.array([X, 17.0, 63.0])
    C = []
    # --- 2017, Cámara de la Reina
    C.append(Campana("Nagoya NE1 (2016)", "nagoya", np.array([X + 5.8, y_sur + 2.1, suelo + 0.3]),
                     arriba, 1.0, 0.45, 98, referencia="Morishima+2017"))
    C.append(Campana("Nagoya NE2 (2016)", "nagoya", np.array([X - 4.5, y_sur + 1.0, suelo + 0.3]),
                     arriba, 1.0, 0.45, 140, referencia="Morishima+2017"))
    C.append(Campana("KEK H1 (2016-17)", "nagoya", np.array([X - 0.3, y_sur + 1.0, suelo + 0.3]),
                     arriba, 0.8, 1.44, 150, separacion_planos=1.5, referencia="Morishima+2017"))
    C.append(Campana("KEK H2 (2017)", "nagoya", np.array([X - 3.2, y_sur + 1.0, suelo + 0.3]),
                     arriba, 1.2, 1.44, 240, separacion_planos=1.0, referencia="Morishima+2017"))
    # --- 2017, exterior norte (CEA): a 17 y 23 m de la cara, mirando a la Galería, algo al este
    for nom, d in (("CEA G1 Alhazen (2017)", 17.0), ("CEA G2 Brahic (2017)", 23.0)):
        o = np.array([X + 1.0, g.SEMILADO + d, 1.0])
        C.append(Campana(nom, "cea", o, _hacia(o, bv + np.array([3.0, 0, 0])), 0.6, 0.25, 60,
                         referencia="Morishima+2017"))
    # --- 2019, corredor descendente: emulsiones EM1-EM4 a lo largo del corredor bajo el NFC
    e = P["entrada"]
    cd, sd = math.cos(math.radians(g.ANG_DESC)), math.sin(math.radians(g.ANG_DESC))
    abajo = np.array([0, -cd, -sd])
    for nom, dist, area, dias in (("Nagoya EM1 (2019)", 3.0, 0.225, 172),
                                  ("Nagoya EM2 N/C/S (2019)", 6.0, 0.675, 211),
                                  ("Nagoya EM3 (2019)", 9.0, 0.225, 211),
                                  ("Nagoya EM4 (2019)", 12.0, 0.225, 79)):
        C.append(Campana(nom, "nagoya", e + dist * abajo + np.array([0, 0, -0.4]), arriba, 1.0,
                         area, dias, referencia="Procureur+2023"))
    # túnel de al-Mamún (entrada a ~7 m de altura, algo al oeste de los pasajes)
    o = np.array([X - 4.0, _y_cara(7.0) - 10.0, 7.5])
    C.append(Campana("Nagoya EM5-EM7 (2019, túnel de al-Mamún)", "nagoya", o,
                     _hacia(o, nfc.centro), 1.0, 4 * 0.075, 272, referencia="Procureur+2023"))
    # CEA 2019: corredor descendente y plataforma del cruce con el ascendente
    u = P["union"]
    for nom, area, dias in (("CEA Joliot (2019-20)", 0.25, 140),
                            ("CEA Degennes (2019-20)", 1.0, 140),
                            ("CEA Charpak (2019-20)", 1.0, 158)):
        o = u + np.array([0, 2.0, 0.3])
        C.append(Campana(nom, "cea", o, _hacia(o, nfc.centro), 0.6, area, dias,
                         referencia="Procureur+2023"))
    return C


def campanas_candidatas(area_m2: float = 1.0, dias: float = 100.0) -> list[Campana]:
    """Puestos accesibles donde aún no se ha medido (emulsiones de `area_m2`, `dias`)."""
    est = {c.nombre: c for c in g.estructuras_conocidas()}
    kc, d5 = est["Cámara del Rey"], est["Cámara de descarga 5"]
    arriba = np.array([0, 0, 1.0])
    centro = np.array([0.0, 0.0, 40.0])
    C = []
    # Cámara Subterránea: excavada en la roca ~30 m bajo la base, casi bajo el vértice.
    # Techo a ~ -26,5 m; detector en el suelo, mirando arriba.
    C.append(Campana("Cámara Subterránea", "nagoya", np.array([2.0, -3.0, -27.0]), arriba, 1.3,
                     area_m2, dias, referencia="propuesta"))
    C.append(Campana("Cámara del Rey (cenital)", "nagoya",
                     np.array([kc.centro[0], kc.centro[1], kc.centro[2] - kc.tam[2] / 2 + 0.3]),
                     arriba, 1.3, area_m2, dias, referencia="propuesta"))
    C.append(Campana("Cámara de Campbell (cenital)", "nagoya",
                     np.array([d5.centro[0], d5.centro[1], d5.centro[2] - 0.2]), arriba, 1.3,
                     area_m2, dias, referencia="propuesta"))
    C.append(Campana("Cabeza de la Gran Galería", "nagoya", np.array([g.X_PASAJES, -0.6, 42.5]),
                     arriba, 1.3, area_m2, dias, referencia="propuesta"))
    C.append(Campana("Cámara Subterránea (4 m², 1 año)", "nagoya", np.array([2.0, -3.0, -27.0]),
                     arriba, 1.3, 4.0, 365, referencia="propuesta"))
    for nom, base in (("Exterior sur", (0, -1)), ("Exterior este", (1, 0)),
                      ("Exterior oeste", (-1, 0))):
        o = np.array([base[0] * (g.SEMILADO + 15), base[1] * (g.SEMILADO + 15), 1.0])
        C.append(Campana(nom, "nagoya", o, _hacia(o, centro), 1.0, area_m2, dias,
                         referencia="propuesta"))
    return C


# --- precálculo y significación de un hueco ---------------------------------------------
def _ejes(eje):
    e3 = np.asarray(eje, float) / np.linalg.norm(eje)
    if abs(e3[2]) > 0.999:
        e1, e2 = np.array([1.0, 0, 0]), np.array([0, 1.0, 0])
    else:
        e1 = np.cross([0, 0, 1.0], e3)
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(e3, e1)
    return e1, e2, e3


def opacidad_total(origen, dirs, referencia):
    """Opacidad (g/cm²): pirámide actual + roca madre si el detector está bajo la base."""
    X = mu.opacidad(origen, dirs, referencia)
    z0 = float(origen[2])
    if z0 < 0:
        dz = np.clip(dirs[:, 2], 1e-6, None)
        X = X + DENSIDAD_ROCA_MADRE * (-z0) / dz * 100.0
    return X


def preparar(c: Campana, referencia: list[g.Caja]) -> Campana:
    t = np.arange(-c.tan_max + PASO_TAN / 2, c.tan_max, PASO_TAN)
    e1, e2, e3 = _ejes(c.eje)
    TX, TY = np.meshgrid(t, t, indexing="xy")
    d = TX[..., None] * e1 + TY[..., None] * e2 + e3
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    dirs = d.reshape(-1, 3)
    X0 = opacidad_total(c.origen, dirs, referencia)
    cos = dirs[:, 2]
    F0 = mu.flujo_integral(mu.energia_minima(X0), cos)
    ok = cos > COS_CENIT_MIN
    ang = (PASO_TAN ** 2 / (1 + TX ** 2 + TY ** 2) ** 1.5).reshape(-1)
    if c.separacion_planos > 0:     # hodoscopio: área de solapamiento de los dos planos
        fx = np.clip(1 - c.separacion_planos * np.abs(TX) / c.lado_m, 0, 1)
        fy = np.clip(1 - c.separacion_planos * np.abs(TY) / c.lado_m, 0, 1)
        aeff = (fx * fy).reshape(-1)
    else:
        aeff = np.ones_like(ang)
    expo = ang * aeff * c.area_m2 * 1e4 * c.dias * 86400.0 * np.clip(dirs @ e3, 0, None)
    N0 = np.where(ok, F0 * expo, 0.0)
    n = t.size
    c._pre = dict(t=t, e=(e1, e2, e3), dirs=dirs.reshape(n, n, 3), X0=X0.reshape(n, n),
                  cos=cos.reshape(n, n), N0=N0.reshape(n, n),
                  N0s=gaussian_filter(N0.reshape(n, n), SIGMA_RES, mode="nearest", truncate=3.0))
    return c


def z_hueco(c: Campana, caja: g.Caja) -> float:
    """Significación (σ, sin calibrar) con que la campaña `c` vería el hueco `caja`."""
    p = c._pre
    e1, e2, e3 = p["e"]
    t = p["t"]
    n = t.size
    h = np.asarray(caja.tam) / 2
    esq = np.array([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]) * h
    esq = esq @ caja._R + np.asarray(caja.centro)
    v = esq - c.origen
    w = v @ e3
    if np.all(w <= 0):
        return 0.0
    if np.all(w > 0.05 * np.linalg.norm(v, axis=1)):
        tx, ty = (v @ e1) / w, (v @ e2) / w
        pad = int(3 * SIGMA_RES) + 2
        i0 = max(int(np.floor((tx.min() - t[0]) / PASO_TAN)) - pad, 0)
        i1 = min(int(np.ceil((tx.max() - t[0]) / PASO_TAN)) + pad + 1, n)
        j0 = max(int(np.floor((ty.min() - t[0]) / PASO_TAN)) - pad, 0)
        j1 = min(int(np.ceil((ty.max() - t[0]) / PASO_TAN)) + pad + 1, n)
        if i0 >= n or j0 >= n or i1 <= 0 or j1 <= 0 or i1 <= i0 or j1 <= j0:
            return 0.0
    else:
        i0, i1, j0, j1 = 0, n, 0, n
    # Submuestreo: SUB x SUB rayos por bin, para no "saltarse" huecos más estrechos que un
    # bin (a 125 m, un bin de 0,02 mide 2,5 m). El fondo X0 se toma del centro del bin.
    dist = float(np.linalg.norm(np.asarray(caja.centro) - c.origen))
    bins_ancho = min(caja.tam) / max(dist, 1e-6) / PASO_TAN
    SUB = int(np.clip(math.ceil(4.0 / max(bins_ancho, 1e-6)), 1, SUB_MAX))
    sub = (np.arange(SUB) + 0.5) / SUB - 0.5
    TX = t[i0:i1][None, :, None, None] + PASO_TAN * sub[None, None, None, :]
    TY = t[j0:j1][:, None, None, None] + PASO_TAN * sub[None, None, :, None]
    TX, TY = np.broadcast_arrays(TX, TY)
    D = TX[..., None] * e1 + TY[..., None] * e2 + e3
    D = (D / np.linalg.norm(D, axis=-1, keepdims=True)).reshape(-1, 3)
    L = caja.longitud_en_rayos(c.origen, D)
    if not np.any(L > 0):
        return 0.0
    nb = (j1 - j0, i1 - i0)
    X0 = np.repeat(p["X0"][j0:j1, i0:i1].reshape(-1), SUB * SUB)
    cos = np.repeat(p["cos"][j0:j1, i0:i1].reshape(-1), SUB * SUB)
    X1 = np.maximum(X0 - mu.DENSIDAD_MATRIZ * L * 100.0, 0.0)
    r = mu.flujo_integral(mu.energia_minima(X1), cos) / np.maximum(
        mu.flujo_integral(mu.energia_minima(X0), cos), 1e-300)
    r = r.reshape(nb[0], nb[1], SUB * SUB).mean(axis=2)
    N0 = p["N0"][j0:j1, i0:i1]
    dN = N0 * (r - 1.0)
    # parche con margen para el suavizado
    m = int(3 * SIGMA_RES) + 2
    dNp = np.pad(dN, m)
    dNs = gaussian_filter(dNp, SIGMA_RES, mode="constant", truncate=3.0)
    N0s = np.pad(p["N0s"], m, mode="edge")[j0:j1 + 2 * m, i0:i1 + 2 * m]
    var = N0s + (F_SIS * N0s) ** 2
    ok = var > 0
    return float(math.sqrt(np.sum(dNs[ok] ** 2 / var[ok])))


def cubo(centro, s):
    return g.Caja("hueco", tuple(centro), (s, s, s))


# --- calibración --------------------------------------------------------------------------
def referencia_actual() -> list[g.Caja]:
    """Estructuras conocidas hoy: las clásicas + NFC + Gran Vacío (horizontal)."""
    an = g.anomalias_detectadas()
    return g.estructuras_conocidas() + [an[0], an[1]]


def calibrar(campanas: list[Campana]) -> dict[str, float]:
    """Factores por familia para reproducir la significación publicada del Gran Vacío."""
    ref = g.estructuras_conocidas() + [g.anomalias_detectadas()[0]]
    bv = g.anomalias_detectadas()[1]
    byname = {c.nombre: c for c in campanas}
    zs = {}
    for k in ("Nagoya NE1 (2016)", "Nagoya NE2 (2016)", "CEA G1 Alhazen (2017)",
              "CEA G2 Brahic (2017)", "KEK H1 (2016-17)", "KEK H2 (2017)"):
        c = preparar(replace(byname[k], _pre={}), ref)
        zs[k] = z_hueco(c, bv)
    k_nag = 0.5 * (Z_PUB_NE1 / zs["Nagoya NE1 (2016)"] + Z_PUB_NE2 / zs["Nagoya NE2 (2016)"])
    z_cea = math.hypot(zs["CEA G1 Alhazen (2017)"], zs["CEA G2 Brahic (2017)"])
    k_cea = Z_PUB_CEA / z_cea
    return dict(nagoya=k_nag, cea=k_cea, z_modelo=zs)


# --- mapa de cobertura --------------------------------------------------------------------
def voxeles(paso: float = 4.0):
    """Centros de una rejilla regular dentro de la pirámide original."""
    xs = np.arange(-g.SEMILADO + paso / 2, g.SEMILADO, paso)
    zs = np.arange(paso / 2, g.ALTURA, paso)
    P = np.array([(x, y, z) for z in zs for y in xs for x in xs])
    lim = g.lado(P[:, 2]) / 2
    dentro = (np.abs(P[:, 0]) <= lim) & (np.abs(P[:, 1]) <= lim)
    return P[dentro]


def ocupado_por_conocidas(P, ref) -> np.ndarray:
    m = np.zeros(len(P), bool)
    for c in ref:
        if c.delta_densidad < 0:
            m |= c.contiene(P)
    return m


def z_combinada(campanas: list[Campana], factores: dict, P: np.ndarray, s: float) -> np.ndarray:
    """Z calibrada y combinada en cuadratura para un cubo de lado `s` en cada punto."""
    Z2 = np.zeros(len(P))
    for c in campanas:
        k = factores[c.familia]
        for i, p in enumerate(P):
            z = z_hueco(c, cubo(p, s))
            if z > 0:
                Z2[i] += (k * z) ** 2
    return np.sqrt(Z2)


def en_campo(c: Campana, P: np.ndarray) -> np.ndarray:
    """¿Cae cada punto dentro del campo de visión geométrico de la campaña?

    Solo geometría: dirección dentro de la aceptancia (|tanθx|, |tanθy| ≤ tan_max respecto
    al eje) y a menos de 70° del cenit. No depende del modelo de flujo ni de la calibración.
    """
    e1, e2, e3 = _ejes(c.eje)
    v = P - c.origen
    w = v @ e3
    with np.errstate(divide="ignore", invalid="ignore"):
        tx, ty = (v @ e1) / w, (v @ e2) / w
    cos_z = v[:, 2] / np.linalg.norm(v, axis=1)
    return (w > 0) & (np.abs(tx) <= c.tan_max) & (np.abs(ty) <= c.tan_max) & (cos_z > COS_CENIT_MIN)
