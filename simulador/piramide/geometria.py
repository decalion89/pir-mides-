"""Geometría de la Gran Pirámide de Keops y de sus estructuras internas.

Sistema de coordenadas (metros):
    origen en el centro de la base, x hacia el ESTE, y hacia el NORTE, z hacia ARRIBA.

Las dimensiones exteriores proceden de los levantamientos de Cole (1925) y Dash (2015).
Las posiciones internas son APROXIMADAS (± 1-2 m) y se reconstruyen a partir de las medidas
clásicas de Petrie (1883) y Maragioglio & Rinaldi (1965), encadenando longitudes y
pendientes de los corredores. Las anomalías detectadas con muones (Gran Vacío y corredor de
la cara norte) siguen a Morishima et al. (Nature 2017) y Procureur et al. (Nat. Commun. 2023).
Ver datos/piramide_keops.json para la fuente de cada valor.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math

import numpy as np

# --- Dimensiones exteriores (pirámide original, con revestimiento) -----------------------
LADO_BASE = 230.33          # m, media de los cuatro lados (Cole 1925 / Dash 2015)
ALTURA = 146.6              # m, altura original estimada (hoy ~138.5 m)
SEMILADO = LADO_BASE / 2.0
TAN_CARA = ALTURA / SEMILADO          # pendiente de las caras
ANGULO_CARA = math.degrees(math.atan(TAN_CARA))   # ~51.8 grados

DENSIDAD_CALIZA = 2.2       # t/m3 (densidad aparente con juntas; ScanPyramids usa 2.2)
DENSIDAD_GRANITO = 2.75     # t/m3


def lado(z: float | np.ndarray) -> float | np.ndarray:
    """Lado del cuadrado horizontal de la pirámide a la altura z."""
    return LADO_BASE * (1.0 - np.asarray(z) / ALTURA)


def volumen_entre(z1: float, z2: float) -> float:
    """Volumen (m3) de la pirámide entre las alturas z1 < z2."""
    f = lambda z: -(LADO_BASE ** 2) * ALTURA / 3.0 * (1.0 - z / ALTURA) ** 3
    return f(z2) - f(z1)


VOLUMEN_TOTAL = volumen_entre(0.0, ALTURA)


def fraccion_volumen_bajo(z: float | np.ndarray) -> float | np.ndarray:
    """Fracción del volumen total que queda por debajo de la altura z."""
    return 1.0 - (1.0 - np.asarray(z) / ALTURA) ** 3


def altura_para_fraccion(f: float) -> float:
    """Altura por debajo de la cual queda la fracción f del volumen."""
    return ALTURA * (1.0 - (1.0 - f) ** (1.0 / 3.0))


@dataclass
class Capa:
    indice: int
    z0: float
    z1: float
    volumen: float
    bloques: float          # nº de bloques (puede ser fraccionario: es un promedio)

    @property
    def z_medio(self) -> float:
        return 0.5 * (self.z0 + self.z1)

    @property
    def lado_superior(self) -> float:
        return float(lado(self.z1))

    @property
    def area(self) -> float:
        return float(lado(self.z_medio)) ** 2


def capas(altura_hilada: float = 0.7, volumen_bloque: float = 1.13,
          fraccion_solida: float = 1.0) -> list[Capa]:
    """Divide la pirámide en hiladas horizontales.

    La Gran Pirámide tenía ~210 hiladas de altura variable (0,5-1,5 m); se usa una altura
    media constante. `volumen_bloque` medio de 1,13 m3 reproduce los ~2,3 millones de
    bloques citados habitualmente. `fraccion_solida` < 1 descuenta relleno de cascote.
    """
    n = max(1, int(round(ALTURA / altura_hilada)))
    dz = ALTURA / n
    out = []
    for i in range(n):
        z0, z1 = i * dz, (i + 1) * dz
        v = volumen_entre(z0, z1)
        out.append(Capa(i, z0, z1, v, v * fraccion_solida / volumen_bloque))
    return out


# --- Geometría 3D: cajas orientadas para estructuras internas ----------------------------
@dataclass
class Caja:
    """Paralelepípedo orientado.

    `centro` (x, y, z); `tam` = (ancho E-O, largo a lo largo del eje, alto); el eje largo
    apunta al norte girado `inclinacion` grados (positivo = sube hacia el sur, como la
    Gran Galería) y `rumbo` grados (0 = eje N-S, 90 = eje E-O).
    `delta_densidad` es la diferencia de densidad respecto a la caliza (t/m3):
    -2.2 para un hueco de aire, +0.55 para granito, -0.2 para un relleno más suelto...
    """
    nombre: str
    centro: tuple[float, float, float]
    tam: tuple[float, float, float]
    inclinacion: float = 0.0
    rumbo: float = 0.0
    delta_densidad: float = -DENSIDAD_CALIZA
    tipo: str = "conocida"
    nota: str = ""
    _R: np.ndarray = field(init=False, repr=False)

    def __post_init__(self):
        a = math.radians(self.inclinacion)
        b = math.radians(self.rumbo)
        # ejes locales: u = ancho, v = largo, w = alto
        v = np.array([math.sin(b) * math.cos(a), -math.cos(b) * math.cos(a), math.sin(a)])
        v = -v  # el eje largo apunta al norte cuando rumbo=0; la galería sube hacia el sur
        u = np.array([math.cos(b), math.sin(b), 0.0])
        w = np.cross(u, v)
        w /= np.linalg.norm(w)
        self._R = np.vstack([u, v, w])   # filas = ejes locales

    def longitud_en_rayos(self, origen: np.ndarray, dirs: np.ndarray) -> np.ndarray:
        """Longitud recorrida dentro de la caja por rayos (semirrectas) origen + t*dir, t>0."""
        o = self._R @ (np.asarray(origen, float) - np.asarray(self.centro, float))
        d = dirs @ self._R.T
        h = np.asarray(self.tam, float) / 2.0
        with np.errstate(divide="ignore", invalid="ignore"):
            t1 = (-h - o) / d
            t2 = (h - o) / d
        tmin = np.where(np.isfinite(t1), np.minimum(t1, t2), -np.inf)
        tmax = np.where(np.isfinite(t1), np.maximum(t1, t2), np.inf)
        # rayos paralelos a un par de caras: dentro o fuera según la coordenada
        paralelo = ~np.isfinite(t1)
        fuera = paralelo & (np.abs(o)[None, :] > h[None, :])
        tmin = np.where(paralelo, -np.inf, tmin)
        tmax = np.where(paralelo, np.inf, tmax)
        te = np.max(tmin, axis=1)
        ts = np.min(tmax, axis=1)
        te = np.maximum(te, 0.0)
        L = np.clip(ts - te, 0.0, None)
        L[np.any(fuera, axis=1)] = 0.0
        return L

    def contiene(self, p: np.ndarray) -> np.ndarray:
        q = (np.atleast_2d(p) - np.asarray(self.centro)) @ self._R.T
        return np.all(np.abs(q) <= np.asarray(self.tam) / 2.0, axis=1)


ALTURA_ACTUAL = 138.5      # m: hoy falta la cúspide
RETRANQUEO_ACTUAL = 1.0    # m: espesor medio perdido con el revestimiento (aprox.)


def longitud_en_piramide(origen: np.ndarray, dirs: np.ndarray, actual: bool = False) -> np.ndarray:
    """Longitud de cada semirrecta origen + t·dir (t > 0) dentro de la pirámide.

    La pirámide es la intersección de semiespacios n_i · p <= c_i (4 caras, la base y,
    si `actual`, el corte de la cúspide a 138,5 m con las caras retranqueadas ~1 m por la
    pérdida del revestimiento). Sirve para orígenes interiores y exteriores (recorte de
    Cyrus-Beck de un rayo contra un poliedro convexo).
    """
    o = np.asarray(origen, float)
    k = TAN_CARA
    normales = np.array([[k, 0, 1], [-k, 0, 1], [0, k, 1], [0, -k, 1], [0, 0, -1],
                         [0, 0, 1]], float)
    hc = ALTURA - (k * RETRANQUEO_ACTUAL if actual else 0.0)
    c = np.array([hc, hc, hc, hc, 0.0, ALTURA_ACTUAL if actual else ALTURA])
    nd = dirs @ normales.T
    holgura = c - normales @ o                  # > 0 si el origen está del lado interior
    with np.errstate(divide="ignore", invalid="ignore"):
        t = holgura[None, :] / nd
    t_sal = np.min(np.where(nd > 1e-12, t, np.inf), axis=1)
    t_ent = np.max(np.where(nd < -1e-12, t, -np.inf), axis=1)
    # rayos paralelos a un plano con el origen fuera de él: no entran nunca
    fuera_paralelo = np.any((np.abs(nd) <= 1e-12) & (holgura[None, :] < 0), axis=1)
    L = np.clip(t_sal - np.maximum(t_ent, 0.0), 0.0, None)
    L[fuera_paralelo] = 0.0
    L[~np.isfinite(L)] = 0.0
    return L


# --- Estructuras internas conocidas (aproximadas) ----------------------------------------
X_PASAJES = 7.3          # los corredores van ~7,3 m al este del eje N-S (Petrie)
Z_ENTRADA = 16.9         # altura de la entrada original en la cara norte
ANG_DESC = 26.5          # pendiente del corredor descendente
ANG_ASC = 26.0           # pendiente del ascendente y de la Gran Galería


def _y_cara_norte(z: float) -> float:
    return SEMILADO * (1.0 - z / ALTURA)


def _puntos_clave() -> dict[str, np.ndarray]:
    e = np.array([X_PASAJES, _y_cara_norte(Z_ENTRADA), Z_ENTRADA])
    cd, sd = math.cos(math.radians(ANG_DESC)), math.sin(math.radians(ANG_DESC))
    unión = e + 28.2 * np.array([0, -cd, -sd])          # arranque del ascendente
    ca, sa = math.cos(math.radians(ANG_ASC)), math.sin(math.radians(ANG_ASC))
    base_gg = unión + 39.3 * np.array([0, -ca, sa])     # pie de la Gran Galería
    cima_gg = base_gg + 46.7 * np.array([0, -ca, sa])   # cabeza de la Gran Galería
    suelo_desc = e + (Z_ENTRADA / sd) * np.array([0, -cd, -sd])
    return dict(entrada=e, union=unión, base_gg=base_gg, cima_gg=cima_gg,
                desc_suelo=suelo_desc)


def _caja_entre(nombre, p0, p1, ancho, alto, **kw) -> Caja:
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    L = float(np.linalg.norm(d))
    incl = math.degrees(math.asin(d[2] / L)) if d[1] <= 0 else -math.degrees(math.asin(d[2] / L))
    return Caja(nombre, tuple((p0 + p1) / 2), (ancho, L, alto), inclinacion=incl, **kw)


def estructuras_conocidas() -> list[Caja]:
    p = _puntos_clave()
    est = []
    est.append(_caja_entre("Corredor descendente (parte en mampostería)", p["entrada"],
                           p["desc_suelo"], 1.05, 1.2))
    est.append(_caja_entre("Corredor ascendente", p["union"], p["base_gg"], 1.05, 1.2))
    # Gran Galería: 46,7 m x 8,6 m de alto x 2,06 (arriba ~1,0) m de ancho -> ancho medio 1,5
    gg0, gg1 = p["base_gg"], p["cima_gg"]
    off = np.array([0, 0, 8.6 / 2 - 0.6])
    est.append(_caja_entre("Gran Galería", gg0 + off, gg1 + off, 1.55, 8.6))
    # Corredor horizontal a la Cámara de la Reina (38,7 m al sur desde el pie de la galería)
    y_qc_norte = gg0[1] - 38.7
    est.append(Caja("Corredor de la Cámara de la Reina",
                    (X_PASAJES, (gg0[1] + y_qc_norte) / 2, gg0[2] - 0.6 + 0.6),
                    (1.05, 38.7, 1.2), inclinacion=0.0))
    z_qc = 21.2
    est.append(Caja("Cámara de la Reina", (X_PASAJES - 2.4, y_qc_norte - 5.23 / 2, z_qc + 2.9),
                    (5.75, 5.23, 5.8)))
    # Antecámara y Cámara del Rey (suelo a ~43 m; 10,47 E-O x 5,23 N-S x 5,84 alto)
    z_kc = 43.0
    y_kc_norte = gg1[1] - 8.4
    est.append(Caja("Antecámara y pasaje", (X_PASAJES, (gg1[1] + y_kc_norte) / 2, z_kc + 1.9),
                    (1.05, 8.4, 3.0)))
    xkc = X_PASAJES + 0.5 - 10.47 / 2
    est.append(Caja("Cámara del Rey", (xkc, y_kc_norte - 5.23 / 2, z_kc + 5.84 / 2),
                    (10.47, 5.23, 5.84)))
    # Granito alrededor de la Cámara del Rey (paredes, techo, vigas): +0,55 t/m3
    est.append(Caja("Bloque de granito de la Cámara del Rey",
                    (xkc, y_kc_norte - 5.23 / 2, z_kc + 11.0), (12.5, 7.3, 22.0),
                    delta_densidad=DENSIDAD_GRANITO - DENSIDAD_CALIZA, tipo="granito"))
    # Cinco cámaras de descarga (~1 m de hueco útil cada una)
    for i in range(5):
        est.append(Caja(f"Cámara de descarga {i + 1}",
                        (xkc, y_kc_norte - 5.23 / 2, z_kc + 5.84 + 1.6 + i * 3.1),
                        (10.47, 5.23, 1.0)))
    return est


def anomalias_detectadas() -> list[Caja]:
    """Anomalías publicadas por ScanPyramids (posiciones aproximadas)."""
    p = _puntos_clave()
    y_cara = _y_cara_norte(21.0)
    nfc = Caja("Corredor de la cara norte (NFC, 2023)",
               (X_PASAJES, y_cara - 0.8 - 1.5 - 9.1 / 2, 21.0), (2.0, 9.1, 2.0),
               tipo="anomalía", nota="Procureur et al. 2023: suelo a ~20 m, 2x2 m, 9 m, horizontal")
    # Gran Vacío: centro 40-50 m del suelo de la Cámara de la Reina; empieza casi en el centro
    # de la pirámide y termina hacia el norte (tan θy ~ 0,8 desde la cámara). Sección ~ galería.
    bv_h = Caja("Gran Vacío — hipótesis horizontal (2017)", (X_PASAJES, 17.0, 63.0),
                (1.6, 30.0, 8.0), tipo="anomalía",
                nota="Morishima et al. 2017: >30 m, sección comparable a la Gran Galería")
    bv_i = Caja("Gran Vacío — hipótesis inclinada (2017)", (X_PASAJES, 17.0, 63.0),
                (1.6, 30.0, 8.0), inclinacion=ANG_ASC, tipo="anomalía",
                nota="misma pendiente que la Gran Galería")
    return [nfc, bv_h, bv_i]


def detectores_publicados() -> dict[str, np.ndarray]:
    """Posiciones aproximadas de detectores usados por ScanPyramids."""
    qc = [c for c in estructuras_conocidas() if c.nombre == "Cámara de la Reina"][0]
    cx, cy, cz = qc.centro
    suelo = cz - qc.tam[2] / 2
    return {
        # Nagoya NE1/NE2 y KEK H1/H2: esquinas sur de la Cámara de la Reina
        "Cámara de la Reina (NE/H)": np.array([cx, cy - 2.0, suelo + 0.3]),
        # emulsiones en el corredor descendente bajo el NFC
        "Corredor descendente": np.array([X_PASAJES, _y_cara_norte(Z_ENTRADA) - 6.0,
                                          Z_ENTRADA - 3.0]),
    }
