"""Planificador de la obra hilada a hilada.

Para cada hilada se calcula el ritmo máximo de bloques/día que permiten:
  (a) los carriles de subida (separación entre equipos y giros),
  (b) la superficie de colocación disponible arriba,
  (c) la mano de obra total (ley de Little: personas = ritmo × tiempo de ciclo × equipo),
y el ritmo efectivo es el mínimo. Se suman los tiempos y se añade el desmontaje final de
las estructuras auxiliares.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math

import numpy as np

from . import geometria as g
from .fisica import Parametros, fuerza_arrastre
from .rampas import Modelo
from .giro import Trineo, factor_cabrestante, ocupacion_con_poste, tiempo_parar_y_pivotar


@dataclass
class ResultadoObra:
    modelo: str
    anios: float
    personas: float
    volumen_aux: float
    cuello: dict = field(default_factory=dict)       # nº de hiladas limitadas por cada causa
    perfil_z: np.ndarray | None = None
    perfil_dias: np.ndarray | None = None
    perfil_ritmo: np.ndarray | None = None
    perfil_personas: dict | None = None
    equipo_max: int = 0


def simular(modelo: Modelo, p: Parametros, personas: float = 25000.0,
            guardar_perfil: bool = False) -> ResultadoObra:
    capas = g.capas(p.altura_hilada, p.volumen_bloque)
    N_prod = personas * (1.0 - p.fraccion_apoyo)
    seg_h = p.horas_dia * 3600.0
    total_dias = 0.0
    cuello = {"carriles": 0, "colocación": 0, "mano de obra": 0}
    zs, dias_l, ritmos = [], [], []
    pers = {"arrastre": [], "colocación": [], "cantera": [], "rampas": [], "palancas": []}
    v_prev = 0.0
    equipo_max = 0
    for c in capas:
        z = c.z1
        segs = modelo.segmentos(z, p)
        pend_max = max(s for _, s in segs)
        F = fuerza_arrastre(p.masa_bloque, pend_max, p.mu)
        n_h = max(1, math.ceil(F / p.fuerza_hombre))
        L_tot = sum(L for L, _ in segs)
        giros = modelo.giros(z)
        # tiempo que cada giro ocupa la esquina y retraso que añade al viaje (giro.py)
        if giros > 0 and p.tecnica_giro == "poste":
            n_h = math.ceil(n_h * factor_cabrestante(p.mu_cuerda))
            t_giro_s = ocupacion_con_poste(Trineo(p.masa_bloque, p.largo_trineo, p.mu),
                                           getattr(modelo, "ancho", 4.0), p.v_cargado)
            retraso_giro = 0.0
        elif giros > 0 and p.tecnica_giro == "pivote":
            t_giro_s = tiempo_parar_y_pivotar(Trineo(p.masa_bloque, p.largo_trineo, p.mu), n_h,
                                              p.metros_por_hombre, p.v_vacio,
                                              sobrecarga_s=p.sobrecarga_giro_s)
            retraso_giro = t_giro_s
        else:
            t_giro_s = p.t_giro_min * 60
            retraso_giro = t_giro_s
        equipo_max = max(equipo_max, n_h)
        t_sub = L_tot / p.v_cargado + giros * retraso_giro + p.t_carga_min * 60
        t_baj = L_tot / p.v_vacio
        ciclo = t_sub + t_baj                                        # s
        # (a) capacidad de carriles
        esp = n_h * p.metros_por_hombre + 4.0 + p.holgura_trineos
        q_carril = p.v_cargado / esp                                  # trineos/s
        if giros > 0:
            q_carril = min(q_carril, 1.0 / t_giro_s)
        q_lanes = modelo.carriles(z) * q_carril * seg_h
        # métodos de palancas: cada columna sube un bloque por t_palanca
        elev = modelo.elevaciones(z, p)
        if elev > 0:
            q_lanes = min(q_lanes, modelo.columnas(z) * seg_h / (p.t_palanca_min * 60))
        # (b) colocación
        equipos = max(1.0, c.area / p.area_por_equipo)
        q_coloc = equipos * seg_h / (p.t_colocar_min * 60)
        # (c) mano de obra por bloque y día (personas·día / bloque)
        a_arr = ciclo * n_h / seg_h
        a_col = p.t_colocar_min * 60 * p.equipo_colocacion / seg_h
        a_can = p.volumen_bloque / p.prod_cantera
        v_aux = modelo.volumen_aux(z)
        a_ram = max(v_aux - v_prev, 0.0) / p.prod_rampa / max(c.bloques, 1e-9)
        a_pal = elev * p.t_palanca_min * 60 * p.equipo_palanca / seg_h
        a_tot = a_arr + a_col + a_can + a_ram + a_pal
        q_lab = N_prod / a_tot
        opciones = {"carriles": q_lanes, "colocación": q_coloc, "mano de obra": q_lab}
        causa = min(opciones, key=opciones.get)
        q = opciones[causa]
        cuello[causa] += 1
        dias = c.bloques / q
        total_dias += dias
        v_prev = v_aux
        if guardar_perfil:
            zs.append(z)
            dias_l.append(dias)
            ritmos.append(q)
            for k, a in zip(pers, (a_arr, a_col, a_can, a_ram, a_pal)):
                pers[k].append(a * q / (1 - p.fraccion_apoyo))
    # desmontaje de rampas al final (mismo rendimiento que construirlas)
    total_dias += v_prev / (p.prod_rampa * N_prod)
    r = ResultadoObra(modelo.nombre, total_dias / p.dias_anio, personas, v_prev, cuello,
                      equipo_max=equipo_max)
    if guardar_perfil:
        r.perfil_z = np.array(zs)
        r.perfil_dias = np.array(dias_l)
        r.perfil_ritmo = np.array(ritmos)
        r.perfil_personas = {k: np.array(v) for k, v in pers.items()}
    return r


def personas_para(modelo: Modelo, p: Parametros, anios_objetivo: float = 20.0,
                  max_personas: float = 2e5) -> float:
    """Mano de obra mínima (personas en total, con apoyo) para acabar en `anios_objetivo`.
    Devuelve inf si ni con `max_personas` se consigue (cuello no laboral)."""
    if simular(modelo, p, max_personas).anios > anios_objetivo:
        return math.inf
    lo, hi = 1000.0, max_personas
    for _ in range(22):
        m = math.sqrt(lo * hi)
        if simular(modelo, p, m).anios <= anios_objetivo:
            hi = m
        else:
            lo = m
    return hi
