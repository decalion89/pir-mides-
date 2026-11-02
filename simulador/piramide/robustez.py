"""¿Resiste el experimento decisivo un análisis honesto?

Tres mejoras respecto a vacio.py:

1. **Ajuste conjunto**: cada hipótesis puede moverse (dy, dz) y cambiar su parámetro de forma
   para imitar a la vez lo que se ve desde la Cámara de la Reina (2017) y desde el puesto
   nuevo. Solo cuenta como "descartada" si ninguna de sus variantes encaja.
2. **Sistemáticos correlacionados**: en cada puesto se ajustan libremente una normalización
   global y dos gradientes lineales (en tanθx y tanθy), con una restricción gaussiana de
   ±5 %. Así se cubren errores en el flujo absoluto, la densidad media o la forma exterior.
3. **Prueba a ciegas**: se generan datos simulados con ruido a partir de una hipótesis
   "verdadera" desplazada al azar y con sección ±15 %, a veces con física distinta de la del modelo (espectro
   de Gaisser, caliza de 2,35 g/cm3, cámaras conocidas desplazadas), y se comprueba si el
   análisis elige la hipótesis correcta.

La exposición se multiplica por FACTOR_EXPOSICION = 0,25, equivalente al factor de
realismo 0,5 sobre la significación usado en vacio.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import itertools

import numpy as np

from . import geometria as g
from . import muones as mu
from . import vacio as v

FACTOR_EXPOSICION = v.FACTOR_REALISMO ** 2
F_SIS_BIN = 0.02
SIGMA_NUISANCE = 0.05
PASO = 0.03
DESPL = (-3.0, -1.5, 0.0, 1.5, 3.0)
ESCALAS = (0.75, 1.0, 1.25)
COS_CENIT_MIN = np.cos(np.radians(70.0))   # se descartan direcciones a más de 70° del cenit      # la sección del Vacío solo se conoce "comparable a la Galería"


def escalar_seccion(cajas: list[g.Caja], s: float) -> list[g.Caja]:
    """Multiplica la altura de la sección de cada caja por `s` (tamaño del hueco incierto)."""
    return [g.Caja(c.nombre, c.centro, (c.tam[0], c.tam[1], c.tam[2] * s), c.inclinacion, c.rumbo,
                   c.delta_densidad, c.tipo, c.nota) for c in cajas]


@dataclass
class PuestoMedida:
    clave: str
    origen: np.ndarray
    eje: np.ndarray
    rejilla: mu.Rejilla
    dias: float
    area: float

    def tx_ty(self):
        TX, TY = np.meshgrid(self.rejilla.tx, self.rejilla.ty, indexing="xy")
        return TX.reshape(-1), TY.reshape(-1)

    def base_nuisance(self) -> np.ndarray:
        """Funciones suaves que absorben errores sistemáticos (n_bins, 4).

        tanθx, tanθy: gradientes (alineación, forma exterior);
        opacidad normalizada y cosθ cenital: error en el espectro y en la pérdida de energía,
        que dependen del espesor atravesado y del ángulo. La propia pirámide, con espesores
        muy distintos en cada dirección, permite calibrarlos ("autocalibración").
        """
        if getattr(self, "_base", None) is None:
            tx, ty = self.tx_ty()
            d = self.rejilla.direcciones(self.eje)
            X = mu.opacidad(self.origen, d, g.estructuras_conocidas())
            xn = (X - X.mean()) / (X.std() + 1e-9)
            cz = (d[:, 2] - d[:, 2].mean()) / (d[:, 2].std() + 1e-9)
            self._base = np.stack([tx, ty, xn, cz], axis=1)
        return self._base


def puestos_estandar(dias_kc: float = 60.0, dias_d5: float = 7.0) -> dict[str, PuestoMedida]:
    P = {p.clave: p for p in v.puestos_candidatos()}
    qc = P["QC"]
    rq = mu.Rejilla.cuadrada(-0.8, 0.8, -0.2, 1.2, PASO)
    rk = mu.Rejilla.cuadrada(-0.7, 0.7, -0.7, 0.7, PASO)
    return {
        "QC": PuestoMedida("QC", qc.origen, qc.eje, rq, v.DIAS_QC_2017, v.AREA_QC_2017),
        "KC": PuestoMedida("KC", P["KC"].origen, P["KC"].eje, rk, dias_kc, 1.0),
        "D5": PuestoMedida("D5", P["D5"].origen, P["D5"].eje, rk, dias_d5, 1.0),
    }


def cuentas(pu: PuestoMedida, cajas: list[g.Caja], referencia: list[g.Caja] | None = None):
    """Cuentas esperadas (suavizadas con la resolución) por bin."""
    ref = g.estructuras_conocidas() if referencia is None else referencia
    d = pu.rejilla.direcciones(pu.eje)
    f = mu.flujo(pu.origen, d, ref + cajas)
    e3 = pu.eje / np.linalg.norm(pu.eje)
    expo = (pu.rejilla.angulo_solido_bin() * pu.area * 1e4 * pu.dias * 86400.0
            * np.clip(d @ e3, 0, None) * FACTOR_EXPOSICION)
    expo = np.where(d[:, 2] >= COS_CENIT_MIN, expo, 0.0)   # el flujo casi horizontal es poco fiable
    n = (f * expo).reshape(pu.rejilla.forma)
    sig = 0.02 / PASO            # ~20 mrad de resolución
    return mu.suavizar(n, sig).reshape(-1)


@dataclass
class Biblioteca:
    """Mapas precalculados de cada hipótesis en una rejilla de variantes."""
    puestos: dict[str, PuestoMedida]
    hipotesis: list[v.Hipotesis]
    variantes: dict[str, list[tuple[float, float, float]]] = field(default_factory=dict)
    mapas: dict[str, dict[str, np.ndarray]] = field(default_factory=dict)   # h -> puesto -> (n_var, n_bins)

    @classmethod
    def construir(cls, hipotesis, puestos, despl=DESPL, factores=(0.85, 1.0, 1.15), escalas=ESCALAS):
        b = cls(puestos, hipotesis)
        for h in hipotesis:
            vs = []
            if h.rango:
                lo, hi = h.rango
                base = h.parametro
                if h.clave in ("H1", "H2", "H3"):      # parámetro = cota: desplazar ±1,5 m
                    ps = [base - 1.5, base, base + 1.5]
                else:                                  # parámetro de forma: escalar
                    ps = [base * f for f in factores]
                ps = [min(max(p, lo), hi) for p in ps]
            else:
                ps = [h.parametro]
            for p, dy, dz, e in itertools.product(ps, despl, despl, escalas):
                if not h.movil and (dy or dz):
                    continue
                vs.append((p, h.dy + dy, h.dz + dz, e))
            b.variantes[h.clave] = vs
            b.mapas[h.clave] = {k: np.array([cuentas(pu, escalar_seccion(h.cajas(*var[:3]), var[3]))
                                             for var in vs])
                                for k, pu in puestos.items()}
        return b


def chi2_perfilado(datos: np.ndarray, modelos: np.ndarray, *bases: np.ndarray,
                   f_sis: float = F_SIS_BIN, sigma_nuis: float = SIGMA_NUISANCE,
                   sigma_espectro: float = 0.10) -> np.ndarray:
    """χ² de los datos frente a cada modelo (filas), perfilando los sistemáticos.

    modelo' = modelo · (1 + α + Σ_k β_k·b_k), con α y los dos primeros β ~ N(0, sigma_nuis)
    y los términos de espectro (columnas 3-4 de base_nuisance) ~ N(0, sigma_espectro).
    `bases` puede ser (tx, ty) o una matriz (n_bins, k) de base_nuisance().
    """
    if len(bases) == 1 and np.ndim(bases[0]) == 2:
        B = bases[0]
    else:
        B = np.stack(bases, axis=1)
    k = B.shape[1]
    sig = [sigma_nuis] * (1 + min(k, 2)) + [sigma_espectro] * max(k - 2, 0)
    P = np.diag(1.0 / np.array(sig) ** 2)
    out = np.empty(modelos.shape[0])
    for i, M in enumerate(modelos):
        var = np.maximum(M + (f_sis * M) ** 2, 1.0)
        w = 1.0 / var
        A = np.column_stack([M] + [M * B[:, j] for j in range(k)])
        r = datos - M
        AtW = A.T * w
        th = np.linalg.solve(AtW @ A + P, AtW @ r)
        res = r - A @ th
        out[i] = float(np.sum(w * res ** 2) + th @ P @ th)
    return out


def ajustar(datos: dict[str, np.ndarray], bib: Biblioteca, usar: tuple[str, ...]) -> dict[str, float]:
    """χ² mínimo de cada hipótesis sobre los puestos `usar`."""
    res = {}
    for h in bib.hipotesis:
        tot = None
        for k in usar:
            c = chi2_perfilado(datos[k], bib.mapas[h.clave][k], bib.puestos[k].base_nuisance())
            tot = c if tot is None else tot + c
        res[h.clave] = float(np.min(tot))
    return res


def generar_verdad(h: v.Hipotesis, puestos: dict[str, PuestoMedida], dy: float, dz: float,
                   fisica: str = "nominal", escala: float = 1.0) -> dict[str, np.ndarray]:
    """Mapas 'verdaderos' de la hipótesis h desplazada, con física posiblemente alterada."""
    ref = None
    if fisica == "gaisser":
        mu.configurar(espectro="gaisser")
    elif fisica in ("perturbado+", "perturbado-"):
        mu.configurar(espectro="reyna_perturbado",
                      perturbacion=(0.9, 0.05) if fisica == "perturbado+" else (1.1, -0.05))
    elif fisica == "densidad":
        mu.configurar(densidad=2.35)
    elif fisica == "estructuras":
        ref = [v.desplazar(c, 1.0, 0.5) for c in g.estructuras_conocidas()]
    try:
        cajas = escalar_seccion(h.cajas(h.parametro, h.dy + dy, h.dz + dz), escala)
        return {k: cuentas(pu, cajas, ref) for k, pu in puestos.items()}
    finally:
        mu.configurar(espectro="reyna", densidad=g.DENSIDAD_CALIZA)


def con_ruido(verdad: dict[str, np.ndarray], puestos, rng: np.random.Generator) -> dict[str, np.ndarray]:
    out = {}
    for k, n in verdad.items():
        tx, ty = puestos[k].tx_ty()
        a, b, c = rng.normal(0, 0.03, 3)
        m = n * (1 + a + b * tx + c * ty) * (1 + rng.normal(0, F_SIS_BIN, n.size))
        out[k] = m + rng.normal(0, np.sqrt(np.maximum(m, 1.0)))
    return out


def z_asimov(bib: Biblioteca, verdad: dict[str, np.ndarray], clave_verdad: str,
             usar: tuple[str, ...]) -> dict[str, float]:
    """Separación (σ) entre la verdad y la mejor variante de cada otra hipótesis, sin ruido."""
    chi = ajustar(verdad, bib, usar)
    base = chi[clave_verdad]
    return {k: float(np.sqrt(max(c - base, 0.0))) for k, c in chi.items() if k != clave_verdad}


def prueba_a_ciegas(bib: Biblioteca, n: int = 40, usar=("QC", "KC"), fisica: str = "nominal",
                    semilla: int = 7) -> dict:
    """Matriz de confusión: fila = hipótesis verdadera, columna = hipótesis elegida."""
    rng = np.random.default_rng(semilla)
    claves = [h.clave for h in bib.hipotesis]
    M = np.zeros((len(claves), len(claves)), int)
    margenes = {k: [] for k in claves}
    for i, h in enumerate(bib.hipotesis):
        for _ in range(n):
            dy, dz = rng.uniform(-1.5, 1.5, 2) if h.movil else (0.0, 0.0)
            esc = rng.uniform(0.85, 1.15)
            verdad = generar_verdad(h, bib.puestos, dy, dz, fisica, esc)
            datos = con_ruido(verdad, bib.puestos, rng)
            chi = ajustar(datos, bib, usar)
            orden = sorted(chi, key=chi.get)
            M[i, claves.index(orden[0])] += 1
            margenes[h.clave].append(chi[orden[1]] - chi[orden[0]] if orden[0] == h.clave
                                     else -(chi[h.clave] - chi[orden[0]]))
    return dict(claves=claves, matriz=M, acierto=float(np.trace(M) / M.sum()),
                margen_mediano={k: float(np.median(x)) for k, x in margenes.items()})
