# Alvarez et al. (1970): matrices de las figuras 8, 9 y 10

Fuente: L. W. Alvarez et al., "Search for hidden chambers in the pyramids", *Science* 167, 832–839 (1970), p. 836.
Transcripción del 01/11/2026 para el Proyecto Pirámides.

## Ficheros

| Fichero | Contenido |
|---|---|
| `fig8_medidos.csv` | Fig. 8: sucesos (muones) observados, sin corregir, en cada bin de 3 × 3 grados (N8). 30 × 30 enteros. |
| `fig9_predichos.csv` | Fig. 9: sucesos predichos por el mejor ajuste en cada bin (N9). 30 × 30 enteros. |
| `fig10_residuos.txt` | Fig. 10: diferencia medido − predicho en desviaciones estándar enteras (29 filas = filas 2–30 de la matriz; formato explicado en su cabecera). |

En los CSV la fila 1 es la de arriba (norte, θ = 45–48°) y la 30 la de abajo (sur, θ = 132–135°). La columna 1 es la de la izquierda (oeste, φ = 45–48°) y la 30 la de la derecha (este, φ = 132–135°). El eje N–S queda entre las columnas 15 y 16, y θ = 90° entre las filas 15 y 16. Las líneas que empiezan por `#` son comentarios.

## Método (Fig. 8 y 9)

1. Se partió de la imagen escaneada de la página (CCITT, 600 ppp) y se enderezó (unos 0,25–0,30°).
2. Se ajustó la rejilla de caracteres de la impresora de líneas: 5 posiciones por columna, con los números alineados a la derecha.
3. Primera lectura con un OCR propio, que compara cada carácter con plantillas de dígitos. La capa OCR del PDF tenía posiciones y valores poco fiables, sobre todo en la Fig. 9, y solo se usó como referencia.
4. Se verificaron a ojo las 1800 casillas, fila a fila, superponiendo la lectura a la imagen. Las casillas dudosas se revisaron ampliadas, entre ellas las filas 15, que el eje θ = 90° atraviesa, y la columna 1 de la Fig. 9, pegada al marco. Esto corrigió 10 casillas de la Fig. 8 y 23 de la Fig. 9, entre ellas varias confusiones 3/8 y 0/3/8.
5. Validación cruzada con la Fig. 10: para cada bin con valor r10 se comprueba |(N8 − N9)/√N9 − r10| ≤ 0,6.

## Resultados de la validación

- Bins con valor en la Fig. 10: 801. La Fig. 10 tiene valor exactamente donde N9 ≥ 2: el N9 mínimo con valor es 2 y el máximo sin valor es 1. Esto confirma que filas y columnas están bien alineadas. La fila 1 vale 0 en las dos matrices, lo que cuadra con que falte en la Fig. 10.
- Discrepancias (> 0,6): 14 con la lectura automática y **2 tras la revisión visual**. En 784 bins |z − r10| ≤ 0,5. Las 2 que quedan se vieron claras en la imagen y se conservan:
  - fila 2, col. 23: N8 = 4, N9 = 2 → z = +1,41, pero la Fig. 10 da −1.
  - fila 30, col. 13: N8 = 5, N9 = 3 → z = +1,15, pero la Fig. 10 da 2.
- Signos dudosos de la Fig. 10: (7, 23) = +3 se confirma (z = +2,51). Para (20, 27) y (27, 14) los datos dan z = −0,63 y −0,60, es decir, −1.
- Sumas: ΣN8 = 649 034 y ΣN9 = 648 132 en los 900 bins. En los 801 bins con valor en la Fig. 10: ΣN8 = 649 011 y ΣN9 = 648 129. Con estos números, Σ(N8 − N9)²/N9 sobre esos 801 bins da 983.

## Casillas dudosas

- Fig. 8 (2, 18): 83 o 81. Fig. 8 (20, 18): 1581 o 1591. En los dos casos las dos lecturas son compatibles con la Fig. 10.
- Fig. 9 (25, 2): 48 o 46, con el dígito emborronado. Las dos lecturas son compatibles con la Fig. 10.
