"""Extrae los puntos de las emulsiones de Nagoya (Extended Data Fig. 2, Morishima et al. 2017).

La figura del PDF de arXiv:1711.01576 (página 9) es una imagen rasterizada por posición
(NE1, NE2). En los paneles "difference" hay dos series:
  rojo  = datos − simulación con las estructuras internas  -> el Gran Vacío
  negro = simulación con − simulación sin estructuras        -> la Gran Galería (conocida)
Cada punto es una cruz (barra horizontal = anchura del bin, vertical = error). Se localizan
las cruces como intersecciones de un tramo horizontal largo y uno vertical del mismo color.

    python extraer_datos_emulsiones.py ruta/a/1711.01576.pdf

Escribe datos/scanpyramids_2017/emulsiones_diferencias.csv con:
    posicion, ty_min, ty_max, serie (vacio|galeria), tanx, valor_px, error_px
(valor y error en píxeles verticales, hacia arriba; basta para ajustar el centro de cada pico).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

SALIDA = Path(__file__).resolve().parent.parent / "datos" / "scanpyramids_2017" / "emulsiones_diferencias.csv"
RANGO_X = {"NE1": (-0.1, 0.6), "NE2": (-0.5, 0.2)}      # extremos del eje tanθx de cada columna
CORTES = [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)]


def imagenes(pdf: str):
    import pymupdf as fitz
    doc = fitz.open(pdf)
    p = doc[8]
    out = []
    for im in p.get_images(full=True):
        pix = fitz.Pixmap(doc, im[0])
        if pix.n > 3:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3]
        out.append(a.astype(int))
    return out      # [NE1, NE2]


def tramos(mask: np.ndarray, eje: int) -> np.ndarray:
    """Longitud del tramo contiguo de `mask` que contiene cada píxel, a lo largo de `eje`."""
    m = mask if eje == 1 else mask.T
    L = np.zeros(m.shape, int)
    for i in range(m.shape[0]):
        fila = m[i]
        if not fila.any():
            continue
        d = np.diff(np.concatenate([[0], fila.astype(int), [0]]))
        ini, fin = np.where(d == 1)[0], np.where(d == -1)[0]
        for a, b in zip(ini, fin):
            L[i, a:b] = b - a
    return L if eje == 1 else L.T


def cruces(mask: np.ndarray, min_h: int, min_v: int):
    h = tramos(mask, 1)
    v = tramos(mask, 0)
    cand = (h >= min_h) & (v >= min_v)
    ys, xs = np.where(cand)
    puntos = []
    usados = np.zeros(len(xs), bool)
    for i in range(len(xs)):
        if usados[i]:
            continue
        cerca = (np.abs(xs - xs[i]) <= 4) & (np.abs(ys - ys[i]) <= 4)
        usados |= cerca
        xc, yc = xs[cerca].mean(), ys[cerca].mean()
        col = mask[:, int(round(xc))]
        # extensión vertical de la barra de error en esa columna
        y0 = int(round(yc))
        a = y0
        while a > 0 and col[a - 1]:
            a -= 1
        b = y0
        while b < len(col) - 1 and col[b + 1]:
            b += 1
        puntos.append((xc, yc, (b - a) / 2))
    return puntos


def extraer(pdf: str) -> list[dict]:
    filas = []
    for nombre, a in zip(("NE1", "NE2"), imagenes(pdf)):
        H, W, _ = a.shape
        negro = a.sum(2) < 150
        filas_marco = np.where(negro.sum(1) > 0.6 * W)[0]
        cols_marco = np.where(negro.sum(0) > 0.3 * H)[0]
        x0, x1 = cols_marco.min() + 1, cols_marco.max() - 1
        # agrupar filas de marco en líneas y tomar los paneles "difference" (2º de cada pareja)
        lineas = [filas_marco[0]]
        for r in filas_marco[1:]:
            if r - lineas[-1] > 5:
                lineas.append(r)
        # orden: techo flujo, separador, suelo diferencia, (siguiente)...
        paneles = [(lineas[i + 1], lineas[i + 2]) for i in range(0, len(lineas) - 2, 3)]
        lo, hi = RANGO_X[nombre]
        for (ya, yb), (t0, t1) in zip(paneles, CORTES):
            sub = a[ya + 4:yb - 3, x0 + 4:x1 - 3]
            rojo = (sub[..., 0] > 190) & (sub[..., 1] < 90) & (sub[..., 2] < 90)
            neg = sub.sum(2) < 150
            for serie, mask in (("vacio", rojo), ("galeria", neg)):
                for (xc, yc, e) in cruces(mask, 18, 5):
                    xpix = xc + x0 + 4
                    tanx = lo + (xpix - cols_marco.min()) / (cols_marco.max() - cols_marco.min()) * (hi - lo)
                    filas.append(dict(posicion=nombre, ty_min=t0, ty_max=t1, serie=serie,
                                      tanx=round(tanx, 4), valor_px=round(sub.shape[0] - yc, 1),
                                      error_px=round(e, 1)))
    return filas


if __name__ == "__main__":
    filas = extraer(sys.argv[1])
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SALIDA, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print(f"{len(filas)} puntos -> {SALIDA}")
