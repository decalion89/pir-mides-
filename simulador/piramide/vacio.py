"""¿Qué es el Gran Vacío? Hipótesis rivales y el experimento que las distingue.

Idea central: los datos de 2017 (detectores bajo el Vacío, en la Cámara de la Reina, y
fuera de la cara norte) solo miden la opacidad integrada a lo largo de cada línea de
visión. Hipótesis muy distintas (un corredor horizontal, uno inclinado, una galería de
contrapeso, una zona de relleno suelto, varias cámaras apiladas) pueden producir
prácticamente LA MISMA señal desde la Cámara de la Reina. Aquí:

1. se define cada hipótesis como un conjunto de cajas;
2. se ajusta su parámetro libre para que reproduzca la señal observada desde la Cámara de
   la Reina (exceso suavizado ~ el de la hipótesis publicada);
3. se calcula, para cada posición candidata de un detector nuevo, cuántos días de
   exposición hacen falta para distinguir cada par de hipótesis a 5σ.

El resultado es un diseño de experimento: dónde medir, cuánto tiempo y qué esperar ver.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from . import geometria as g
from . import muones as mu

ANCHO_GG, ALTO_GG = 1.6, 8.0          # sección "comparable a la Gran Galería"
SIGMA_RES = 1.0                       # resolución angular en bins de 0.02 (~20 mrad)
FACTOR_REALISMO = 0.5                 # ver docs/06: el modelo sobreestima Z ~x2 en la QC


def _caja(nombre, centro, tam, incl=0.0, dd=-g.DENSIDAD_CALIZA, nota=""):
    return g.Caja(nombre, tuple(centro), tuple(tam), inclinacion=incl, delta_densidad=dd,
                  tipo="hipótesis", nota=nota)


def _galeria_inclinada(nombre, y_sur, z_sur, largo, ancho=ANCHO_GG, alto=ALTO_GG,
                       angulo=g.ANG_ASC, nota=""):
    """Galería que sube hacia el sur con extremo superior (sur) en (y_sur, z_sur)."""
    a = math.radians(angulo)
    cy = y_sur + 0.5 * largo * math.cos(a)
    cz = z_sur - 0.5 * largo * math.sin(a)
    return _caja(nombre, (g.X_PASAJES, cy, cz), (ancho, largo, alto), incl=angulo, nota=nota)


@dataclass
class Hipotesis:
    clave: str
    nombre: str
    descripcion: str
    construir: callable          # parámetro libre -> list[Caja]
    parametro: float             # valor inicial / ajustado
    rango: tuple[float, float] | None = None   # si se ajusta a la señal de la QC
    predice: str = ""
    movil: bool = True           # ¿se permite desplazarla (dy, dz) en el ajuste?
    dy: float = 0.0
    dz: float = 0.0
    z_residual_qc: float = float("nan")   # σ de discrepancia con lo observado tras ajustar

    def cajas(self, p=None, dy=None, dz=None) -> list[g.Caja]:
        p = self.parametro if p is None else p
        dy = self.dy if dy is None else dy
        dz = self.dz if dz is None else dz
        return [desplazar(c, dy, dz) for c in self.construir(p)]


def desplazar(c: g.Caja, dy: float, dz: float) -> g.Caja:
    x, y, z = c.centro
    return g.Caja(c.nombre, (x, y + dy, z + dz), c.tam, c.inclinacion, c.rumbo,
                  c.delta_densidad, c.tipo, c.nota)


def hipotesis_base() -> list[Hipotesis]:
    H = []
    H.append(Hipotesis(
        "H1", "Corredor horizontal (ScanPyramids 2017)",
        "Un único corredor horizontal de sección similar a la Gran Galería, ~30 m.",
        lambda z: [_caja("H1", (g.X_PASAJES, 17.0, z), (ANCHO_GG, 30.0, ALTO_GG))],
        63.0, (50.0, 75.0),
        predice="Bordes nítidos y horizontales; sin conexión con otras cámaras."))
    H.append(Hipotesis(
        "H2", "Corredor inclinado 26° (ScanPyramids 2017)",
        "Paralelo a la Gran Galería, unos 20 m por encima.",
        lambda z: [_caja("H2", (g.X_PASAJES, 17.0, z), (ANCHO_GG, 30.0, ALTO_GG), incl=g.ANG_ASC)],
        63.0, (50.0, 75.0),
        predice="Galería gemela de la Gran Galería: pendiente idéntica, ~20 m más arriba."))
    H.append(Hipotesis(
        "H3", "Galería de contrapeso (tipo Houdin)",
        "Galería inclinada 26° cuyo extremo alto (sur) llega a la altura de la última cámara "
        "de descarga y se une a la pila de la Cámara del Rey por un pasaje horizontal.",
        lambda zs: [_galeria_inclinada("H3 galería", 0.0, zs, 32.0),
                    _caja("H3 pasaje", (g.X_PASAJES - 1.0, -4.5, zs - ALTO_GG / 2 + 1.0),
                          (1.5, 9.0, 2.0))],
        70.0, (60.0, 80.0),
        predice="Extremo sur alto a la cota de las cámaras de descarga (~64-68 m) y un pasaje "
                "hacia ellas; el Vacío debe ser inclinado."))
    H.append(Hipotesis(
        "H4", "Zona de relleno poco denso",
        "No es un hueco limpio sino un volumen amplio (6 m x 12 m x 30 m) de relleno suelto, "
        "como el que queda al cerrar un espacio de trabajo de obra.",
        lambda dd: [_caja("H4", (g.X_PASAJES, 17.0, 63.0), (6.0, 30.0, 12.0), dd=dd)],
        -0.4, (-2.2, -0.05),
        predice="Exceso difuso, bordes suaves, más ancho visto de lado que desde abajo."))
    H.append(Hipotesis(
        "H5", "Tres cámaras apiladas",
        "Tres huecos bajos superpuestos (como las cámaras de descarga), 1,6 m x 30 m x h.",
        lambda h: [_caja(f"H5 cámara {i + 1}", (g.X_PASAJES, 17.0, 57.0 + 5.5 * i), (ANCHO_GG, 30.0, h))
                   for i in range(3)],
        2.5, (0.5, 4.0),
        predice="Visto de lado, tres franjas horizontales separadas ~5 m."))
    H.append(Hipotesis(
        "H6", "Hueco de descarga pegado a la Gran Galería",
        "Un hueco estructural justo encima del techo de la Gran Galería (a ~2 m).",
        lambda _: [_galeria_inclinada("H6", -0.6 + 1.0, 42.0 + ALTO_GG + 2.0 + 4.0, 32.0)],
        0.0, None, movil=False,
        predice="Debería verse ~20 m más bajo de lo observado en 2017."))
    return H


# --- Observación de referencia: la Cámara de la Reina ------------------------------------
def rejilla_qc() -> mu.Rejilla:
    return mu.Rejilla.cuadrada(-0.8, 0.8, -0.2, 1.2, 0.02)


def firma_qc(cajas: list[g.Caja], dias: float = 98.0, area: float = 0.45):
    det = g.detectores_publicados()["Cámara de la Reina (NE/H)"]
    return mu.mapa(det, rejilla_qc(), g.estructuras_conocidas(), cajas, area_m2=area, dias=dias)


def pico_suavizado(res: mu.ResultadoMapa, sigma_bins: float = 2.5) -> float:
    return float(mu.suavizar(res.exceso, sigma_bins).max())


DIAS_QC_2017 = 240.0      # NE1 (98 d) + NE2 (140 d) con 0,45 m2; KEK aporta más
AREA_QC_2017 = 0.45


def chi2_qc(cajas_hip: list[g.Caja], cajas_obs: list[g.Caja], f_sis: float = 0.02) -> float:
    det = g.detectores_publicados()["Cámara de la Reina (NE/H)"]
    r = mu.mapa(det, rejilla_qc(), g.estructuras_conocidas(), cajas_hip,
                area_m2=AREA_QC_2017, dias=DIAS_QC_2017, alternativa=cajas_obs)
    return (r.significacion(f_sis=f_sis, sigma_bins=SIGMA_RES) * FACTOR_REALISMO) ** 2


def ajustar_a_observacion(h: Hipotesis, observada: list[g.Caja]) -> Hipotesis:
    """Ajusta (parámetro de forma, dy, dz) para imitar lo observado desde la QC.

    "Observado" = mapa esperado del Vacío publicado (Asimov). Tras el ajuste,
    `z_residual_qc` dice cuántas σ separan la hipótesis de los datos de 2017: si es < ~3,
    los datos de 2017 NO pueden descartarla.
    """
    from scipy.optimize import minimize

    lo, hi = h.rango if h.rango else (h.parametro, h.parametro)
    escala = max(hi - lo, 1e-9)

    def f(v):
        p = min(max(h.parametro + v[0] * escala, lo), hi) if h.rango else h.parametro
        dy, dz = (v[1] * 10.0, v[2] * 10.0) if h.movil else (0.0, 0.0)
        return chi2_qc(h.cajas(p, dy, dz), observada)

    v0 = np.zeros(3)
    if not h.rango and not h.movil:
        h.z_residual_qc = math.sqrt(f(v0))
        return h
    best = None
    for arranque in ([0, 0, 0], [0.15, 0, 0], [-0.15, 0, 0], [0, 0.3, 0], [0, 0, 0.3], [0, 0, -0.3]):
        r = minimize(f, np.array(arranque, float), method="Nelder-Mead",
                     options=dict(xatol=1e-3, fatol=1e-3, maxiter=250))
        if best is None or r.fun < best.fun:
            best = r
    v = best.x
    if h.rango:
        h.parametro = min(max(h.parametro + v[0] * escala, lo), hi)
    if h.movil:
        h.dy, h.dz = v[1] * 10.0, v[2] * 10.0
    h.z_residual_qc = math.sqrt(max(best.fun, 0.0))
    return h


# --- Posiciones candidatas para un detector nuevo ----------------------------------------
@dataclass
class Puesto:
    clave: str
    nombre: str
    origen: np.ndarray
    eje: np.ndarray
    acceso: str


def puestos_candidatos() -> list[Puesto]:
    est = {c.nombre: c for c in g.estructuras_conocidas()}
    qc = est["Cámara de la Reina"]
    kc = est["Cámara del Rey"]
    d1 = est["Cámara de descarga 1"]
    d5 = est["Cámara de descarga 5"]
    bv = np.array([g.X_PASAJES, 17.0, 63.0])

    def hacia(o, objetivo=bv):
        v = objetivo - o
        return v / np.linalg.norm(v)

    P = []
    o = np.array([qc.centro[0], qc.centro[1] - 2.0, qc.centro[2] - qc.tam[2] / 2 + 0.3])
    P.append(Puesto("QC", "Cámara de la Reina (como en 2017)", o, np.array([0, 0, 1.0]),
                    "Accesible; ya usado por Nagoya y KEK."))
    o = np.array([g.X_PASAJES, -0.6, 42.5])
    P.append(Puesto("GG", "Cabeza de la Gran Galería", o, hacia(o),
                    "Accesible al público; justo debajo del extremo sur del Vacío."))
    o = np.array([kc.centro[0] + 3.0, kc.centro[1] + 2.0, kc.centro[2] - kc.tam[2] / 2 + 0.3])
    P.append(Puesto("KC", "Cámara del Rey (esquina NE)", o, hacia(o),
                    "Accesible; mira hacia arriba y al norte."))
    o = np.array([d1.centro[0] + 3.0, d1.centro[1] + 2.0, d1.centro[2] - 0.2])
    P.append(Puesto("D1", "Cámara de Davison (1ª de descarga)", o, hacia(o),
                    "Acceso restringido por el pasaje desde la cabeza de la Gran Galería."))
    o = np.array([d5.centro[0] + 3.0, d5.centro[1] + 2.0, d5.centro[2] - 0.2])
    P.append(Puesto("D5", "Cámara de Campbell (5ª de descarga)", o, hacia(o),
                    "Acceso restringido por el túnel de Vyse; a la cota del Vacío: lo ve de lado."))
    o = np.array([g.X_PASAJES, g.SEMILADO + 20.0, 2.0])
    P.append(Puesto("N", "Exterior, frente a la cara norte (como CEA)", o,
                    hacia(o), "Exterior; sin restricciones de espacio."))
    z = 30.0
    o = np.array([g.SEMILADO * (1 - z / g.ALTURA) + 1.0, 17.0, z])
    P.append(Puesto("E", "Exterior, sobre los escalones de la cara este (z=30 m)", o, hacia(o),
                    "Exterior; vista lateral perpendicular al eje del Vacío."))
    return P


def rejilla_puesto() -> mu.Rejilla:
    return mu.Rejilla.cuadrada(-0.7, 0.7, -0.7, 0.7, 0.02)


def matriz_discriminacion(hips: list[Hipotesis], puesto: Puesto, dias: float = 100.0,
                          area: float = 1.0, f_sis: float = 0.02):
    """Z (σ) con que el puesto distingue cada par de hipótesis tras `dias` con `area` m2."""
    ref = g.estructuras_conocidas()
    n = len(hips)
    Z = np.zeros((n, n))
    rej = rejilla_puesto()
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            r = mu.mapa(puesto.origen, rej, ref, hips[i].cajas(), area_m2=area, dias=dias,
                        eje=puesto.eje, alternativa=hips[j].cajas())
            Z[i, j] = r.significacion(f_sis=f_sis, sigma_bins=SIGMA_RES) * FACTOR_REALISMO
    return Z


def dias_para_5_sigma(hip_a: Hipotesis, hip_b: Hipotesis, puesto: Puesto, area: float = 1.0,
                      f_sis: float = 0.02, max_dias: float = 3650.0) -> float:
    """Días de exposición necesarios para separar a 5σ (inf si los sistemáticos lo impiden)."""
    ref = g.estructuras_conocidas()
    rej = rejilla_puesto()

    def Z(d):
        r = mu.mapa(puesto.origen, rej, ref, hip_a.cajas(), area_m2=area, dias=d,
                    eje=puesto.eje, alternativa=hip_b.cajas())
        return r.significacion(f_sis=f_sis, sigma_bins=SIGMA_RES) * FACTOR_REALISMO

    if Z(max_dias) < 5.0:
        return math.inf
    lo, hi = 0.1, max_dias
    for _ in range(40):
        m = math.sqrt(lo * hi)
        if Z(m) >= 5.0:
            hi = m
        else:
            lo = m
    return hi


# --- Prueba de la rampa interna de Houdin con los datos de 2017 --------------------------
def rampa_interna_houdin(z0: float = 43.0, z_fin: float = 130.0, pendiente: float = 0.07,
                         retranqueo: float = 12.0, ancho: float = 2.6, alto: float = 2.6) -> list[g.Caja]:
    """Túnel en espiral a `retranqueo` m de las caras, subiendo con `pendiente` (Houdin 2007).

    Se genera tramo a tramo: sur (hacia el este), este (hacia el norte), norte (hacia el
    oeste), oeste (hacia el sur), con el semilado reduciéndose al subir.
    """
    cajas = []
    z = z0
    ang = math.degrees(math.atan(pendiente))
    # (signo_x, signo_y de la cara, rumbo, inclinación con la convención de Caja)
    caras = [("S", 90.0, +ang), ("E", 0.0, -ang), ("N", 90.0, -ang), ("O", 0.0, +ang)]
    i = 0
    while z < z_fin:
        a = g.SEMILADO * (1 - z / g.ALTURA) - retranqueo
        if a < 4.0:
            break
        largo = 2 * a
        dz = largo * pendiente
        zc = z + dz / 2
        cara, rumbo, incl = caras[i % 4]
        cen = {"S": (0.0, -a, zc), "E": (a, 0.0, zc), "N": (0.0, a, zc), "O": (-a, 0.0, zc)}[cara]
        cajas.append(g.Caja(f"Rampa interna tramo {i + 1} ({cara})", cen, (ancho, largo, alto),
                            inclinacion=incl, rumbo=rumbo, tipo="hipótesis"))
        z += dz
        i += 1
    return cajas


def visibilidad_rampa_interna(z0: float = 43.0, ancho: float = 2.6, alto: float = 2.6) -> dict:
    """Z con que la rampa de Houdin se habría visto desde la QC con la exposición de 2017."""
    det = g.detectores_publicados()["Cámara de la Reina (NE/H)"]
    rej = mu.Rejilla.cuadrada(-1.2, 1.2, -1.2, 1.2, 0.02)
    r = mu.mapa(det, rej, g.estructuras_conocidas(), rampa_interna_houdin(z0, ancho=ancho, alto=alto),
                area_m2=AREA_QC_2017, dias=DIAS_QC_2017)
    ex = mu.suavizar(r.exceso, 2.5)
    lim = 1.0
    TX, TY = np.meshgrid(rej.tx, rej.ty)
    dentro = (np.abs(TX) <= lim) & (np.abs(TY) <= lim)
    # significación solo en la aceptancia típica |tan θ| <= 1
    n0 = r.cuentas_ref.reshape(rej.forma)[dentro]
    n1 = r.cuentas_hip.reshape(rej.forma)[dentro]
    z_acc = float(np.sqrt(np.sum((n1 - n0) ** 2 / (n0 + (0.02 * n0) ** 2))) * FACTOR_REALISMO)
    return dict(exceso_max_suavizado=float(ex.max()), exceso_max_en_aceptancia=float(ex[dentro].max()),
                z_aceptancia=z_acc, mapa=r)
