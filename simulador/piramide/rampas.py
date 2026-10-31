"""Modelos de elevación de bloques.

Cada modelo responde, para una hilada a la altura z:
- segmentos(z):  lista de (longitud m, pendiente) del viaje cargado desde la cantera;
- giros(z):      nº de giros de 90° en el recorrido (180° cuentan como 2);
- carriles(z):   nº de carriles de subida que funcionan en paralelo;
- volumen_aux(z): volumen acumulado de estructuras auxiliares (rampas) para llegar a z;
- elevaciones(z): nº de elevaciones con palanca por bloque (métodos de palancas);
- columnas(z):    nº de columnas de palancas en paralelo.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from . import geometria as g

TAN_CONTENCION = 3.0      # muros de contención de la rampa (~72°)


def _lado(z):
    return float(g.lado(z))


def _integral_tramos(z0: float, z1: float, pendiente: float, resta: float, minimo: float) -> float:
    """∫_{z0}^{z1} dz / (pendiente · max(lado(z) - resta, minimo)), en forma cerrada.

    Es el número de tramos (y por tanto de giros) de una rampa que sube con `pendiente`
    apoyada en caras cuya longitud útil es lado(z) - resta.
    """
    if z1 <= z0:
        return 0.0
    L0, H = g.LADO_BASE, g.ALTURA
    # altura a la que la longitud útil cae al mínimo
    z_m = H * (1.0 - (resta + minimo) / L0)
    total = 0.0
    a, b = z0, min(z1, z_m)
    if b > a:
        fa = L0 * (1 - a / H) - resta
        fb = L0 * (1 - b / H) - resta
        total += (H / (pendiente * L0)) * math.log(fa / fb)
    a = max(z0, z_m)
    if z1 > a:
        total += (z1 - a) / (pendiente * minimo)
    return total


@dataclass
class Modelo:
    nombre: str = "modelo"
    clave: str = "?"
    descripcion: str = ""

    def segmentos(self, z, p):
        raise NotImplementedError

    def giros(self, z):
        return 0.0

    def carriles(self, z):
        return 1

    def volumen_aux(self, z):
        return 0.0

    def elevaciones(self, z, p):
        return 0.0

    def columnas(self, z):
        return 0.0

    def tramo_horizontal(self, z):
        """Distancia media desde la cabeza de la rampa hasta el punto de colocación."""
        return 0.35 * _lado(z)


@dataclass
class RampaRecta(Modelo):
    pendiente: float = 0.10
    ancho: float = 12.0
    nombre: str = "Rampa recta frontal"
    clave: str = "recta"
    descripcion: str = "Una rampa perpendicular a una cara, que se recrece con la pirámide."

    def segmentos(self, z, p):
        return [(p.distancia_cantera, 0.0), (z / self.pendiente, self.pendiente),
                (self.tramo_horizontal(z), 0.0)]

    def carriles(self, z):
        return max(1, int(self.ancho // 6.0))

    def volumen_aux(self, z):
        s, w = self.pendiente, self.ancho
        return w * z ** 2 / (2 * s) + z ** 3 / (3 * s * TAN_CONTENCION)


@dataclass
class _RampaSobreCaras(Modelo):
    """Rampa apoyada en las caras: sección de relleno ~ ½·w²·tan(cara)."""
    pendiente: float = 0.10
    ancho: float = 5.0
    n_rampas: int = 1            # rampas independientes en paralelo (una por cara como máximo)

    def _seccion(self):
        return 0.5 * self.ancho ** 2 * g.TAN_CARA + 1.0 * self.ancho   # cuña + firme

    def volumen_aux(self, z):
        return self.n_rampas * (z / self.pendiente) * self._seccion()

    def carriles(self, z):
        return self.n_rampas * max(1, int(self.ancho // 6.0))


@dataclass
class Zigzag(_RampaSobreCaras):
    nombre: str = "Rampa en zigzag sobre una cara"
    clave: str = "zigzag"
    descripcion: str = "Tramos de ida y vuelta apoyados en una cara (modelo tipo Lehner)."

    def segmentos(self, z, p):
        return [(p.distancia_cantera, 0.0), (z / self.pendiente, self.pendiente),
                (self.tramo_horizontal(z), 0.0)]

    def giros(self, z):
        # nº de revueltas: integral de dz / (pendiente · longitud del tramo a esa altura)
        return 2.0 * _integral_tramos(0.0, z, self.pendiente, 2 * self.ancho, 8.0)  # 180° = 2 giros


@dataclass
class Espiral(_RampaSobreCaras):
    nombre: str = "Rampa en espiral exterior"
    clave: str = "espiral"
    descripcion: str = "Envuelve las cuatro caras apoyada en ellas (modelo tipo Dunham)."

    def segmentos(self, z, p):
        return [(p.distancia_cantera, 0.0), (z / self.pendiente, self.pendiente),
                (self.tramo_horizontal(z), 0.0)]

    def giros(self, z):
        return _integral_tramos(0.0, z, self.pendiente, 0.0, 8.0)


@dataclass
class Interna(Modelo):
    """Rampa recta exterior hasta z_cambio y túnel interior en espiral (Houdin 2007)."""
    z_cambio: float = 43.0
    pendiente_ext: float = 0.10
    ancho_ext: float = 12.0
    pendiente_int: float = 0.07
    retranqueo: float = 12.0
    nombre: str = "Rampa interna (Houdin)"
    clave: str = "interna"
    descripcion: str = ("Rampa exterior hasta ~43 m y después un túnel interior en espiral de un "
                        "solo carril, con giros en muescas de las esquinas.")

    def _ext(self):
        return RampaRecta(self.pendiente_ext, self.ancho_ext)

    def segmentos(self, z, p):
        if z <= self.z_cambio:
            return self._ext().segmentos(z, p)
        s = self._ext().segmentos(self.z_cambio, p)[:2]
        return s + [((z - self.z_cambio) / self.pendiente_int, self.pendiente_int),
                    (self.tramo_horizontal(z), 0.0)]

    def giros(self, z):
        if z <= self.z_cambio:
            return 0.0
        return _integral_tramos(self.z_cambio, z, self.pendiente_int, 2 * self.retranqueo, 6.0)

    def carriles(self, z):
        # un solo carril; los equipos vacíos bajan por el mismo túnel: capacidad ~ mitad
        return self._ext().carriles(z) if z <= self.z_cambio else 0.5

    def volumen_aux(self, z):
        return self._ext().volumen_aux(min(z, self.z_cambio))


@dataclass
class Aristas(Modelo):
    """Cuatro carriles helicoidales integrados en las aristas (inspirado en Rosell Roig)."""
    pendiente: float = 0.12
    nombre: str = "Rampas integradas en las aristas"
    clave: str = "aristas"
    descripcion: str = ("Cuatro carriles helicoidales formados dejando sin colocar bloques del "
                        "borde y rellenándolos al final; un carril por arista.")

    def segmentos(self, z, p):
        return [(p.distancia_cantera, 0.0), (z / self.pendiente, self.pendiente),
                (self.tramo_horizontal(z), 0.0)]

    def giros(self, z):
        return _integral_tramos(0.0, z, self.pendiente, 0.0, 6.0)

    def carriles(self, z):
        return 4

    def volumen_aux(self, z):
        # el volumen omitido se rellena al final: cuenta como trabajo de relleno
        return (z / self.pendiente) * 3.0 * 2.0 * 0.6


@dataclass
class Palancas(Modelo):
    """Rampa recta baja hasta z_cambio y, por encima, elevación hilada a hilada con palancas
    en columnas repartidas por el perímetro (Heródoto, 'máquinas de maderos cortos')."""
    z_cambio: float = 0.0
    separacion_columnas: float = 6.0
    pendiente_ext: float = 0.10
    ancho_ext: float = 12.0
    nombre: str = "Palancas hilada a hilada"
    clave: str = "palancas"
    descripcion: str = "Bloques subidos escalón a escalón con palancas por las caras."

    def segmentos(self, z, p):
        if self.z_cambio > 0:
            s = RampaRecta(self.pendiente_ext, self.ancho_ext).segmentos(min(z, self.z_cambio), p)[:2]
        else:
            s = [(p.distancia_cantera, 0.0)]
        return s + [(self.tramo_horizontal(z), 0.0)]

    def carriles(self, z):
        return max(1, int(self.ancho_ext // 6.0)) if self.z_cambio > 0 else 4

    def volumen_aux(self, z):
        return RampaRecta(self.pendiente_ext, self.ancho_ext).volumen_aux(min(z, self.z_cambio)) \
            if self.z_cambio > 0 else 0.0

    def elevaciones(self, z, p):
        return max(0.0, z - self.z_cambio) / p.altura_hilada

    def columnas(self, z):
        return max(1.0, 4.0 * _lado(z) / self.separacion_columnas)


@dataclass
class Hibrido(Modelo):
    """Un modelo por debajo de z_cambio y otro por encima."""
    inferior: Modelo = None
    superior: Modelo = None
    z_cambio: float = 45.0
    nombre: str = "Híbrido"
    clave: str = "hibrido"

    def _m(self, z):
        return self.inferior if z <= self.z_cambio else self.superior

    def segmentos(self, z, p):
        if z <= self.z_cambio:
            return self.inferior.segmentos(z, p)
        base = self.inferior.segmentos(self.z_cambio, p)[:-1]
        sup = self.superior.segmentos(z, p)
        # el modelo superior empieza en la plataforma z_cambio: quitamos su tramo inicial
        if self.superior.elevaciones(z, p) > 0:
            resto = []          # por encima del cambio se sube con palancas: sin más rampa
        else:
            resto = [(L * (1 - self.z_cambio / z) if s > 0 else 0.0, s) for (L, s) in sup[1:-1]]
        return base + resto + [sup[-1]]

    def giros(self, z):
        if z <= self.z_cambio:
            return self.inferior.giros(z)
        return self.superior.giros(z) - self.superior.giros(self.z_cambio)

    def carriles(self, z):
        return self._m(z).carriles(z)

    def volumen_aux(self, z):
        v = self.inferior.volumen_aux(min(z, self.z_cambio))
        if z > self.z_cambio:
            v += self.superior.volumen_aux(z) - self.superior.volumen_aux(self.z_cambio)
        return v

    def elevaciones(self, z, p):
        return self.superior.elevaciones(z, p) if z > self.z_cambio else 0.0

    def columnas(self, z):
        return self.superior.columnas(z) if z > self.z_cambio else 0.0


def catalogo() -> list[Modelo]:
    return [
        RampaRecta(),
        Zigzag(),
        Zigzag(n_rampas=4, nombre="Zigzag en las 4 caras", clave="zigzag4"),
        Espiral(),
        Espiral(n_rampas=4, nombre="4 espirales exteriores", clave="espiral4"),
        Interna(),
        Aristas(),
        Palancas(),
        Hibrido(inferior=RampaRecta(), superior=Zigzag(), z_cambio=45.0,
                nombre="Híbrido: recta hasta 45 m + zigzag", clave="recta+zigzag"),
        Hibrido(inferior=RampaRecta(), superior=Palancas(z_cambio=45.0), z_cambio=45.0,
                nombre="Híbrido: recta hasta 45 m + palancas", clave="recta+palancas"),
    ]
