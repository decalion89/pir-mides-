"""Extrae los datos reales de KEK (Extended Data Fig. 4 de Morishima et al., Nature 2017).

Lee los vectores del PDF de arXiv:1711.01576 (página 10): para cada panel calibra los ejes con
las etiquetas de las marcas y recupera cada punto (centro y barra de error) a partir de los
cuatro segmentos con que ROOT dibuja un punto con error.

    python extraer_datos_kek.py ruta/a/1711.01576.pdf

Escribe datos/scanpyramids_2017/kek_cortes.csv con columnas:
    detector, dy_min, dy_max, dx, cociente, error
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import numpy as np
import pymupdf as fitz

SALIDA = Path(__file__).resolve().parent.parent / "datos" / "scanpyramids_2017" / "kek_cortes.csv"


# Rangos de Δy de cada panel, de arriba abajo (las etiquetas están dibujadas como trazos,
# no como texto; se leen en la figura).
CORTES = {"H1": [(72, 95), (48, 71), (24, 47), (0, 23)],
          "H2": [(64, 79), (48, 63), (32, 47), (16, 31), (0, 15)]}


def extraer(pdf: str, pagina: int = 9) -> list[dict]:
    doc = fitz.open(pdf)
    p = doc[pagina]
    dibujos = p.get_drawings()
    marcos = [d["rect"] for d in dibujos
              if len(d["items"]) == 1 and d["items"][0][0] == "re" and d["rect"].width > 80]
    segs = [(i[1].x, i[1].y, i[2].x, i[2].y) for d in dibujos for i in d["items"] if i[0] == "l"]
    puntos = []
    for d in dibujos:
        its = d["items"]
        if len(its) == 4 and all(i[0] == "l" for i in its):
            vert = [i for i in its if abs(i[1].x - i[2].x) < 1e-3]
            hor = [i for i in its if abs(i[1].y - i[2].y) < 1e-3]
            if len(vert) == 2 and len(hor) == 2:
                ys = [q.y for i in vert for q in (i[1], i[2])]
                puntos.append((vert[0][1].x, 0.5 * (hor[0][1].y + hor[1][1].y), min(ys), max(ys)))
    filas = []
    for det in ("H1", "H2"):
        col = sorted([m for m in marcos if (m.x0 < p.rect.width / 2) == (det == "H1")], key=lambda m: m.y0)
        for m, (dy0, dy1) in zip(col, CORTES[det]):
            # marcas mayores (6,4 pt) en el borde inferior e izquierdo
            mx = sorted({round(s[0], 3) for s in segs if abs(s[0] - s[2]) < 1e-2
                         and min(abs(s[1] - m.y1), abs(s[3] - m.y1)) < 0.3
                         and m.x0 - 0.5 < s[0] < m.x1 + 0.5 and 5 < abs(s[3] - s[1]) < 10})
            my = sorted({round(s[1], 3) for s in segs if abs(s[1] - s[3]) < 1e-2
                         and min(abs(s[0] - m.x0), abs(s[2] - m.x0)) < 0.3
                         and m.y0 - 0.5 < s[1] < m.y1 + 0.5 and 5 < abs(s[2] - s[0]) < 10})
            x0v = -30.0 if det == "H1" else -20.0
            vx = [x0v + 10 * k for k in range(len(mx))]
            paso_y = 0.1 if len(my) >= 4 else 0.2
            vy = [1.2 - paso_y * k for k in range(len(my))]        # de arriba abajo
            bx = np.polyfit(vx, mx, 1)
            by = np.polyfit(vy, my, 1)
            for (x, y, y0, y1) in puntos:
                if m.x0 < x < m.x1 and m.y0 < y < m.y1:
                    filas.append(dict(detector=det, dy_min=dy0, dy_max=dy1,
                                      dx=round((x - bx[1]) / bx[0], 2),
                                      cociente=round((y - by[1]) / by[0], 4),
                                      error=round(abs((y1 - y0) / 2 / by[0]), 4)))
    return sorted(filas, key=lambda f: (f["detector"], f["dy_min"], f["dx"]))


if __name__ == "__main__":
    filas = extraer(sys.argv[1])
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SALIDA, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print(f"{len(filas)} puntos -> {SALIDA}")
