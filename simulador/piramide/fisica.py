"""Física del arrastre de bloques y parámetros inciertos con sus fuentes."""
from __future__ import annotations

from dataclasses import dataclass, field, fields
import math

import numpy as np

G = 9.81


def fuerza_arrastre(masa_t: float, pendiente: float, mu: float) -> float:
    """Fuerza (N) para arrastrar un trineo de `masa_t` toneladas a velocidad constante
    por una pendiente `pendiente` (tangente) con coeficiente de rozamiento `mu`."""
    th = math.atan(pendiente)
    return masa_t * 1000.0 * G * (mu * math.cos(th) + math.sin(th))


def mu_desde_djehutihotep(fuerza_hombre: float, hombres: int = 172, masa_t: float = 58.0) -> float:
    """Rozamiento implícito en la pintura de Djehutihotep (172 hombres, coloso de ~58 t, llano)."""
    return hombres * fuerza_hombre / (masa_t * 1000.0 * G)


@dataclass
class Parametros:
    """Valores centrales. `RANGOS` da (mín, moda, máx) para el Monte Carlo."""
    mu: float = 0.15                 # trineo sobre pista preparada y humedecida
    fuerza_hombre: float = 280.0     # N, tracción sostenida por persona
    v_cargado: float = 0.35          # m/s
    v_vacio: float = 1.0             # m/s
    metros_por_hombre: float = 0.5   # m de cuerda por persona (dos o más filas)
    holgura_trineos: float = 6.0     # m extra entre equipos consecutivos
    t_giro_min: float = 5.0          # min por giro de 90° de un trineo cargado
    t_carga_min: float = 10.0        # min de carga + descarga por viaje
    t_colocar_min: float = 25.0      # min por bloque para colocarlo con palancas
    equipo_colocacion: int = 8
    area_por_equipo: float = 40.0    # m2 de superficie de trabajo por equipo de colocación
    t_palanca_min: float = 15.0      # min para subir un bloque una hilada con palancas
    equipo_palanca: int = 6
    prod_cantera: float = 0.5        # m3 de bloque por persona y día
    prod_rampa: float = 2.0          # m3 de rampa (cascote, tafla, adobe) por persona y día
    horas_dia: float = 10.0
    dias_anio: float = 300.0
    fraccion_apoyo: float = 0.4      # panaderos, aguadores, herreros, transporte fluvial...
    distancia_cantera: float = 450.0 # m (cantera de Keops, al sur)
    volumen_bloque: float = 1.13     # m3
    densidad: float = 2.3            # t/m3 del bloque
    altura_hilada: float = 0.7       # m

    @property
    def masa_bloque(self) -> float:
        return self.volumen_bloque * self.densidad

    def muestrear(self, rng: np.random.Generator) -> "Parametros":
        p = Parametros(**{f.name: getattr(self, f.name) for f in fields(self)})
        for k, (a, m, b) in RANGOS.items():
            setattr(p, k, float(rng.triangular(a, m, b)))
        p.equipo_colocacion = int(round(p.equipo_colocacion))
        p.equipo_palanca = int(round(p.equipo_palanca))
        return p


# (mínimo, moda, máximo) y justificación — ver docs/06 para las referencias
RANGOS: dict[str, tuple[float, float, float]] = {
    "mu": (0.08, 0.15, 0.30),            # Djehutihotep implica ~0,06-0,12; Fall 2014: arena húmeda
    "fuerza_hombre": (200.0, 280.0, 350.0),
    "v_cargado": (0.2, 0.35, 0.5),
    "v_vacio": (0.8, 1.0, 1.3),
    "metros_por_hombre": (0.35, 0.5, 0.8),
    "holgura_trineos": (3.0, 6.0, 12.0),
    "t_giro_min": (2.0, 5.0, 15.0),
    "t_carga_min": (5.0, 10.0, 20.0),
    "t_colocar_min": (10.0, 25.0, 45.0),
    "equipo_colocacion": (6.0, 8.0, 12.0),
    "area_por_equipo": (25.0, 40.0, 70.0),
    "t_palanca_min": (8.0, 15.0, 30.0),
    "equipo_palanca": (4.0, 6.0, 10.0),
    "prod_cantera": (0.3, 0.5, 1.0),
    "prod_rampa": (1.0, 2.0, 4.0),
    "horas_dia": (8.0, 10.0, 11.0),
    "dias_anio": (270.0, 300.0, 330.0),
    "fraccion_apoyo": (0.3, 0.4, 0.5),
    "distancia_cantera": (300.0, 450.0, 700.0),
    "volumen_bloque": (1.0, 1.13, 1.3),
}
