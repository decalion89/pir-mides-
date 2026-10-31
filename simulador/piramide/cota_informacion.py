"""Cota de Cramér–Rao: la mejor precisión posible sobre la forma del Gran Vacío.

Para unos datos de recuento (Poisson) con valor esperado μ_i(θ) en cada bin, la información de
Fisher es
    F_jk = Σ_i (∂μ_i/∂θ_j)(∂μ_i/∂θ_k) / Var_i,      Var_i = μ_i + (f·μ_i)²,
y para CUALQUIER estimador insesgado, Var(θ̂_j) ≥ (F⁻¹)_jj (Cramér 1946, Rao 1945). Es un
límite del experimento, no de un análisis concreto: ningún método puede hacerlo mejor.

Parámetros:
- del Vacío: posición (y, z), longitud, alto, ancho e inclinación;
- de ruido: normalización, dos gradientes y dos términos espectrales, con restricciones
  gaussianas; se marginan, es decir, se tratan como desconocidos.

Se calcula para el puesto de 2017 (Cámara de la Reina) y para los propuestos (Cámara del Rey,
Cámara de Campbell), con la misma exposición efectiva y el mismo corte de cenit que robustez.py.
"""
from __future__ import annotations

import numpy as np

from . import robustez as rb
from .reanalisis import Corredor

NOMBRES = ("y", "z", "largo", "alto", "ancho", "inclinacion")
PASOS = (0.5, 0.5, 1.0, 0.3, 0.1, 1.0)


def cajas(v):
    y, z, L, h, w, a = v
    return [Corredor(7.3, y, z, L, h, ancho=w, inclinacion=a).caja()]


def fisher(pu: rb.PuestoMedida, v0, f_sis: float = rb.F_SIS_BIN,
           sigma_nuis: float = rb.SIGMA_NUISANCE, sigma_espectro: float = 0.10):
    mu0 = rb.cuentas(pu, cajas(v0))
    J = []
    for j, h in enumerate(PASOS):
        vp, vm = list(v0), list(v0)
        vp[j] += h
        vm[j] -= h
        J.append((rb.cuentas(pu, cajas(vp)) - rb.cuentas(pu, cajas(vm))) / (2 * h))
    B = pu.base_nuisance()
    J += [mu0] + [mu0 * B[:, k] for k in range(B.shape[1])]       # normalización y 4 términos
    J = np.array(J)
    var = np.maximum(mu0 + (f_sis * mu0) ** 2, 1.0)
    F = (J / var) @ J.T
    prior = [0.0] * len(PASOS) + [sigma_nuis, sigma_nuis, sigma_nuis, sigma_espectro, sigma_espectro]
    for k, s in enumerate(prior):
        if s > 0:
            F[k, k] += 1.0 / s ** 2
    return F


def sigmas(F, extra_fijos=()):
    """Errores marginales (raíz de la diagonal de F⁻¹) de los parámetros del Vacío."""
    idx = [i for i in range(F.shape[0]) if i not in extra_fijos]
    C = np.linalg.inv(F[np.ix_(idx, idx)])
    d = dict(zip([i for i in idx], np.sqrt(np.diag(C))))
    return {NOMBRES[i]: float(d[i]) for i in range(len(NOMBRES)) if i in d}


def combinar(*Fs):
    """Información de varios puestos con los mismos parámetros del Vacío y ruidos independientes."""
    n = len(PASOS)
    tot = np.zeros((n, n))
    for F in Fs:
        # marginalizar los ruidos de cada puesto (complemento de Schur) antes de sumar
        A, Bm, D = F[:n, :n], F[:n, n:], F[n:, n:]
        tot += A - Bm @ np.linalg.solve(D, Bm.T)
    return tot
