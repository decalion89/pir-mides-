"""¿Dejaron huella las rampas integradas en las aristas? (predicción P6)

Si la pirámide se subió por cuatro carriles helicoidales formados dejando sin colocar
bloques cerca de las caras (modelo tipo Rosell Roig), esos carriles se rellenaron al final.
Un relleno colocado deprisa y sin trabar suele ser algo menos denso (más juntas, más mortero
o cascote). Aquí se calcula si un detector de muones EXTERIOR, al pie de una cara, vería
esas bandas helicoidales, en función del déficit de densidad del relleno.

Si se usaron palancas o rampas exteriores desmontadas, no hay bandas: la medición separa
las dos familias de métodos que el modelo de construcción deja como viables.
"""
from __future__ import annotations

import numpy as np

from . import geometria as g
from . import muones as mu
from . import robustez as rb
from .vacio import rampa_interna_houdin


def carriles_aristas(delta_densidad: float, pendiente: float = 0.12, retranqueo: float = 4.0,
                     ancho: float = 3.9, alto: float = 4.2) -> list[g.Caja]:
    """Cuatro hélices desfasadas una cara, desde la base hasta ~130 m."""
    cajas = []
    for k in range(4):
        cajas += rampa_interna_houdin(z0=0.0, z_fin=130.0, pendiente=pendiente, retranqueo=retranqueo,
                                      ancho=ancho, alto=alto, cara_inicial=k,
                                      delta_densidad=delta_densidad, nombre=f"Carril {k + 1}")
    return cajas


def puesto_exterior(cara: str = "E", distancia: float = 15.0, elevacion_grados: float = 45.0):
    """Detector al pie del centro de una cara, mirando hacia la pirámide y hacia arriba."""
    s = g.SEMILADO + distancia
    o = {"E": np.array([s, 0, 1.0]), "N": np.array([0, s, 1.0]),
         "O": np.array([-s, 0, 1.0]), "S": np.array([0, -s, 1.0])}[cara]
    horiz = -o.copy()
    horiz[2] = 0
    horiz /= np.linalg.norm(horiz)
    e = np.radians(elevacion_grados)
    eje = np.array([horiz[0] * np.cos(e), horiz[1] * np.cos(e), np.sin(e)])
    return o, eje


def significacion(delta_densidad: float, dias: float = 100.0, area: float = 1.0,
                  elevacion: float = 45.0, distancia: float = 15.0) -> dict:
    o, eje = puesto_exterior("E", distancia, elevacion)
    rej = mu.Rejilla.cuadrada(-0.8, 0.8, -0.8, 0.8, rb.PASO)
    pu = rb.PuestoMedida("ext", o, eje, rej, dias, area)
    n0 = rb.cuentas(pu, [])
    n1 = rb.cuentas(pu, carriles_aristas(delta_densidad))
    chi = rb.chi2_perfilado(n1, n0[None, :], pu.base_nuisance())[0]
    ex = (n1 / np.maximum(n0, 1e-9) - 1).reshape(rej.forma)
    return dict(delta_densidad=delta_densidad, Z=float(np.sqrt(chi)), exceso_max=float(ex.max()),
                cuentas_totales=float(n0.sum()), mapa_exceso=ex, rejilla=rej)
