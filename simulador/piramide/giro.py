"""Física del giro de un trineo cargado en la esquina de una rampa.

El modelo de construcción (obra.py) mostró que el tiempo de giro en las esquinas decide si
una rampa de un solo carril termina a tiempo. Aquí se estima ese tiempo desde la física para
dos técnicas:

A. PARAR Y PIVOTAR: el equipo se detiene, el trineo se gira 90° con palancas y el equipo se
   recoloca alrededor de la esquina antes de volver a tirar. El giro ocupa la esquina:
     t = t_parada + t_pivote + t_recolocación + t_arranque
   El pivote necesita vencer el par de rozamiento de los patines, T ≈ μ·m·g·l/4.

B. POSTE DE REENVÍO (flujo continuo): un poste fijo en la esquina interior desvía la cuerda,
   como los agujeros de poste de la rampa de Hatnub (reinado de Keops), y el trineo sigue
   avanzando guiado por el bordillo. El precio es el rozamiento de la cuerda en el poste
   (cabrestante): la fuerza se multiplica por e^{μ_c·θ}, con θ = π/2. El equipo tiene que ser
   ese factor mayor, y la separación entre trineos crece con él. La esquina solo queda ocupada
   mientras el trineo la recorre: (ancho + largo del trineo) / v.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from .fisica import G

HOMBRE_W = 75.0       # potencia sostenida por persona (W)


@dataclass
class Trineo:
    masa_t: float = 2.6
    largo: float = 2.5          # m de patín en contacto
    mu: float = 0.15            # rozamiento de los patines


def par_pivote(tr: Trineo) -> float:
    """Par (N·m) para girar el trineo sobre su centro: carga repartida a lo largo de los patines."""
    return tr.mu * tr.masa_t * 1000 * G * tr.largo / 4


def tiempo_parar_y_pivotar(tr: Trineo, equipo: int, metros_por_hombre: float = 0.5,
                           v_andar: float = 1.0, palanqueros: int = 6, sobrecarga_s: float = 60.0) -> float:
    """Segundos que la esquina queda ocupada con la técnica A."""
    trabajo = par_pivote(tr) * math.pi / 2
    t_pivote = trabajo / (palanqueros * HOMBRE_W)          # tiempo físico mínimo
    t_recolocar = equipo * metros_por_hombre / v_andar      # el equipo rodea la esquina
    return t_pivote + t_recolocar + sobrecarga_s            # parar, calzar, tensar y arrancar


def factor_cabrestante(mu_cuerda: float, angulo: float = math.pi / 2) -> float:
    """Multiplicador de fuerza de una cuerda que roza un poste fijo (ecuación de Euler-Eytelwein)."""
    return math.exp(mu_cuerda * angulo)


def ocupacion_con_poste(tr: Trineo, ancho_rampa: float, v: float) -> float:
    """Segundos que la esquina queda ocupada con la técnica B."""
    return (ancho_rampa + tr.largo) / v


def comparar(ancho_rampa: float = 4.0, v: float = 0.35, equipo: int = 23) -> dict:
    tr = Trineo()
    return dict(
        par_pivote_Nm=par_pivote(tr),
        pivote_min=tiempo_parar_y_pivotar(tr, equipo) / 60,
        pivote_min_rapido=tiempo_parar_y_pivotar(tr, equipo, sobrecarga_s=30) / 60,
        pivote_min_lento=tiempo_parar_y_pivotar(tr, equipo, sobrecarga_s=150) / 60,
        poste_ocupacion_min=ocupacion_con_poste(tr, ancho_rampa, v) / 60,
        poste_factor_equipo_mu02=factor_cabrestante(0.2),
        poste_factor_equipo_mu04=factor_cabrestante(0.4),
    )
