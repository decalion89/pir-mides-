"""El problema de las vigas de granito de la Cámara del Rey.

~43 vigas de granito de Asuán de 25-80 t (Lehner 1997; Houdin da un máximo de ~62 t)
forman el techo de la Cámara del Rey y de las cámaras de descarga, entre ~49 y ~61 m de
altura. Tuvieron que colocarse mientras el núcleo subía de ~43 a ~66 m. Aquí se comparan
tres formas de subirlas con física elemental:

M1  arrastrarlas por una rampa hasta su cota;
M2  un contrapeso que desciende por una galería inclinada (hipótesis tipo Houdin);
M3  dejarlas en la plataforma a 43 m y subirlas con palancas hilada a hilada a la vez
    que crece el núcleo ("acompañar la subida").

La pregunta clave para el Gran Vacío es: ¿obliga la física a usar una galería de contrapeso?
Si M1 o M3 son viables, la existencia del Vacío NO se deduce de las vigas, y su identidad
tiene que decidirse midiendo (ver vacio.py).
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from . import geometria as g
from .fisica import G, fuerza_arrastre

Z_SUELO_KC = 43.0
Z_VIGAS = (48.8, 51.5, 54.6, 57.7, 60.8)     # techo de la KC y techos de las cámaras 1-4
VIGAS_POR_NIVEL = (9, 9, 9, 8, 8)            # ~43 vigas en total (aprox.)
MASAS_T = (25.0, 40.0, 60.0, 80.0)           # rango de la literatura


@dataclass
class Equipo:
    masa_t: float
    pendiente: float
    mu: float
    fuerza_hombre: float = 280.0
    filas: int = 4                 # cuerdas en paralelo (Djehutihotep: 4 filas)
    metros_por_hombre_fila: float = 1.0

    @property
    def fuerza(self) -> float:
        return fuerza_arrastre(self.masa_t, self.pendiente, self.mu)

    @property
    def hombres(self) -> int:
        return math.ceil(self.fuerza / self.fuerza_hombre)

    @property
    def longitud_equipo(self) -> float:
        return self.hombres / self.filas * self.metros_por_hombre_fila


def volumen_rampa_recta(z: float, pendiente: float = 0.10, ancho: float = 15.0,
                        tan_muro: float = 3.0) -> float:
    s = pendiente
    return ancho * z ** 2 / (2 * s) + z ** 3 / (3 * s * tan_muro)


def contrapeso_necesario(masa_t: float, pendiente_viga: float, mu_viga: float,
                         angulo_galeria: float = g.ANG_ASC, mu_carro: float = 0.10,
                         eficiencia_reenvio: float = 0.55, ayuda_humana_kN: float = 0.0) -> float:
    """Masa de contrapeso (t) que, bajando por la galería, arrastra la viga.

    Equilibrio: M·g·(sin α − μc·cos α)·η + F_humana ≥ m·g·(μ cos β + sin β).
    η es la eficiencia del reenvío de la cuerda (rodillo o viga engrasada; sin poleas en el
    Reino Antiguo: η ~ e^{-μ·π} ~ 0,4-0,7).
    """
    a = math.radians(angulo_galeria)
    tiro = fuerza_arrastre(masa_t, pendiente_viga, mu_viga) - ayuda_humana_kN * 1000
    empuje_por_t = 1000 * G * (math.sin(a) - mu_carro * math.cos(a)) * eficiencia_reenvio
    if empuje_por_t <= 0:
        return math.inf
    return max(tiro, 0.0) / empuje_por_t / 1.0


def capacidad_galeria(ancho: float = 1.6, alto: float = 8.0, largo: float = 30.0,
                      llenado: float = 0.4, densidad: float = g.DENSIDAD_CALIZA) -> float:
    """Toneladas de lastre que caben en un carro que ocupe la galería (fracción `llenado`)."""
    return ancho * alto * largo * llenado * densidad


def palancas_por_hilada(masa_t: float, carga_por_palanca_t: float = 2.0) -> int:
    """Palancas simultáneas para levantar un extremo de la viga (mitad de la masa)."""
    return math.ceil(0.5 * masa_t / carga_por_palanca_t)


def dias_m3_por_viga(masa_t: float, z_final: float, altura_hilada: float = 0.7,
                     horas_por_elevacion_extremo: float = 3.0, horas_dia: float = 10.0) -> float:
    """Días de trabajo para subir una viga desde 43 m hasta z_final con palancas,
    calzando primero un extremo y luego el otro en cada hilada."""
    n = max(0.0, z_final - Z_SUELO_KC) / altura_hilada
    return n * 2 * horas_por_elevacion_extremo / horas_dia


def tabla_metodos(mu: float = 0.15, pendiente: float = 0.10) -> list[dict]:
    filas = []
    for m in MASAS_T:
        e = Equipo(m, pendiente, mu)
        z = Z_VIGAS[-1]
        filas.append(dict(
            masa_t=m,
            hombres_rampa=e.hombres,
            longitud_equipo_m=e.longitud_equipo,
            tramo_zigzag_disponible_m=float(g.lado(z)) - 2 * 6.0,
            tramo_interno_disponible_m=float(g.lado(z)) - 2 * 12.0,
            contrapeso_t_optimista=contrapeso_necesario(m, math.tan(math.radians(g.ANG_ASC)), 0.10,
                                                        eficiencia_reenvio=0.7),
            contrapeso_t_pesimista=contrapeso_necesario(m, math.tan(math.radians(g.ANG_ASC)), 0.20,
                                                        mu_carro=0.15, eficiencia_reenvio=0.4),
            palancas_simultaneas=palancas_por_hilada(m),
            dias_palancas_hasta_61m=dias_m3_por_viga(m, z),
        ))
    return filas


def resumen(anios_ventana: float) -> dict:
    """Comparación global con la ventana de tiempo en que el núcleo pasa de 43 a 66 m."""
    v_rampa_61 = volumen_rampa_recta(61.0)
    total_vigas = sum(VIGAS_POR_NIVEL)
    dias_m3 = sum(n * dias_m3_por_viga(60.0, z) for n, z in zip(VIGAS_POR_NIVEL, Z_VIGAS))
    return dict(
        vigas=total_vigas,
        volumen_rampa_recta_hasta_61m_m3=v_rampa_61,
        fraccion_volumen_piramide=v_rampa_61 / g.VOLUMEN_TOTAL,
        ventana_anios=anios_ventana,
        dias_palancas_en_serie=dias_m3,
        dias_palancas_6_en_paralelo=dias_m3 / 6.0,
        capacidad_vacio_t_llenado_40=capacidad_galeria(),
        capacidad_vacio_t_llenado_80=capacidad_galeria(llenado=0.8),
    )
