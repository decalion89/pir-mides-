"""De Giza a la Luna: el presupuesto energético de construir con bloques locales.

1. ¿Cuánta energía mecánica costó la Gran Pirámide? Hay que elevar cada bloque hasta su hilada
   y arrastrarlo desde la cantera.
2. ¿Qué cambia en la Luna?
   - La gravedad es 1/6 de la terrestre: elevar y arrastrar cuesta menos.
   - No hay agua para lubricar el arrastre: el rozamiento del regolito seco es alto.
   - Trabajan robots con potencia limitada y noches de 14 días.
3. ¿Qué lecciones del modelo de construcción se trasladan? Sobre todo, el cuello de botella de
   las esquinas y el valor de las vías en paralelo.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import geometria as g

G_TIERRA = 9.81
G_LUNA = 1.62
KWH = 3.6e6


@dataclass
class Obra:
    nombre: str
    volumen_m3: float
    altura_media_m: float        # altura media a la que hay que subir la masa
    distancia_m: float           # recorrido horizontal medio desde la cantera
    densidad: float              # t/m³ del material colocado
    mu: float                    # rozamiento del arrastre
    gravedad: float = G_TIERRA

    @property
    def masa_kg(self) -> float:
        return self.volumen_m3 * self.densidad * 1000

    def energia_elevar_J(self) -> float:
        return self.masa_kg * self.gravedad * self.altura_media_m

    def energia_arrastre_J(self) -> float:
        # rampa + llano: el rozamiento actúa a lo largo de todo el recorrido
        L = self.distancia_m + self.altura_media_m / 0.1      # rampa del 10 % hasta la altura media
        return self.mu * self.masa_kg * self.gravedad * L

    def energia_total_J(self) -> float:
        return self.energia_elevar_J() + self.energia_arrastre_J()


def gran_piramide(mu: float = 0.15) -> Obra:
    # el centro de masas de una pirámide está a H/4 de la base
    return Obra("Gran Pirámide", g.VOLUMEN_TOTAL, g.ALTURA / 4, 450.0, 2.2, mu)


def jornadas_humanas(E_J: float, potencia_W: float = 75.0, horas: float = 10.0, eficiencia: float = 1.0) -> float:
    return E_J / (potencia_W * horas * 3600 * eficiencia)


def blindaje_lunar(volumen_m3: float = 50_000.0, mu: float = 0.5) -> Obra:
    """Blindaje de regolito contra la radiación (~3 m de espesor) sobre una base lunar.

    Regolito apilado o sinterizado a ~1,8 t/m³; altura media de elevación de 3 m; acarreo
    medio de 200 m; arrastre en seco con μ ~0,4-0,6.
    """
    return Obra("Blindaje lunar", volumen_m3, 3.0, 200.0, 1.8, mu, G_LUNA)


def robots_necesarios(obra: Obra, anios: float, potencia_util_W: float = 500.0,
                      fraccion_tiempo: float = 0.35) -> float:
    """Robots de potencia mecánica útil dada para terminar en `anios`.

    `fraccion_tiempo` descuenta las noches lunares de 14 días, el mantenimiento, la carga de
    baterías y los desplazamientos en vacío.
    """
    segundos = anios * 365.25 * 86400 * fraccion_tiempo
    return obra.energia_total_J() / (potencia_util_W * segundos)
