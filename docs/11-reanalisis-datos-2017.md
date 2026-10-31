# 11 — Reanálisis independiente de los datos publicados del Gran Vacío

> **Resumen.** Extrajimos de la versión arXiv del artículo de *Nature* (2017) los datos que publicó ScanPyramids:
> - **679 puntos** de los hodoscopios de KEK, leídos de los vectores del PDF;
> - los perfiles de las **emulsiones de Nagoya**, leídos de la imagen.
>
> Con ellos ajustamos, con nuestro propio modelo, la posición, el tamaño y la **inclinación** del Vacío. Hasta donde sabemos, es el primer reanálisis independiente de esos datos.
>
> **Resultados**:
> - Nuestra geometría reproduce la calibración de ScanPyramids.
> - El Vacío está sobre el eje de la Gran Galería, a ~56–63 m de altura, con una sección del orden de la de la Galería: ~9–21 m² según el conjunto de datos.
> - **Su inclinación no se puede fijar de forma robusta con los datos publicados**:
>   - las emulsiones prefieren un Vacío horizontal o poco inclinado;
>   - KEK prefiere uno inclinado, pero en una posición incompatible con la de las emulsiones;
>   - el ajuste conjunto se resume en el §5.
>
> Por el camino detectamos y corregimos un error propio que había producido una "inclinación de 18° a 4–6σ" falsa. Lo documentamos abajo.

## 1. Datos
| Fuente | Qué es | Cómo se extrajo | Archivo |
|---|---|---|---|
| Extended Data Fig. 4 | Cociente entre datos y simulación con las estructuras conocidas. KEK, posiciones H1 y H2 de la Cámara de la Reina, 9 cortes | Vectores del PDF: 679 puntos con su barra de error. Los ejes se calibran con las marcas mayores, y los valores de Δx salen enteros, lo que confirma la calibración | [`extraer_datos_kek.py`](../simulador/extraer_datos_kek.py), [`datos/scanpyramids_2017/kek_cortes.csv`](../datos/scanpyramids_2017/kek_cortes.csv) |
| Extended Data Fig. 2 | Perfiles "diferencia". Emulsiones NE1 (nicho este) y NE2 (esquina suroeste), 4 cortes en tanθy. En rojo, el Vacío (datos − simulación); en negro, la Gran Galería simulada | Imagen de 1367 × 3086 px: las cruces se detectan como intersecciones de tramos de color | [`extraer_datos_emulsiones.py`](../simulador/extraer_datos_emulsiones.py), [`datos/scanpyramids_2017/emulsiones_diferencias.csv`](../datos/scanpyramids_2017/emulsiones_diferencias.csv) |

Para reproducirlo: descarga `https://arxiv.org/pdf/1711.01576` y ejecuta los dos extractores sobre el PDF.

## 2. Validación: nuestra geometría coincide con la de ScanPyramids
- **Posiciones de las emulsiones.** Ajustando solo la señal simulada de la Gran Galería (la curva negra), recuperamos NE1 a **+5,7 m** y NE2 a **−4,3 m** del eje de la Galería. El artículo da **+5,8 m** y **−4,5 m**.
- **Ángulos de la Galería.** Coinciden en los 8 paneles: por ejemplo, NE1 da 0,263 → 0,338 en el modelo frente a 0,255 → 0,338 en la figura.
- **KEK.** Los datos piden claramente una estructura: el χ² pasa de 2284 sin Vacío a ~1100–1370 con él, para 679 puntos.

## 3. Qué dicen los datos sobre el Vacío
Modelo: un corredor recto, con posición, longitud, sección e inclinación libres. Se añade un emborronamiento angular libre (dispersión múltiple en la roca, que sale de ~0,03) y una línea base por panel.

En cada panel de las emulsiones, la escala de la señal del Vacío se fija con la de la Gran Galería simulada del mismo panel, y así se conserva la información de amplitud. Los errores se reescalan con el χ²/ndf de cada conjunto de datos (3,9 para las emulsiones y 1,7 para KEK).

- **Posición este-oeste** (emulsiones): **sobre el eje de la Gran Galería**, x = 7,1–7,5 m frente a 7,3 m.
- **Altura**: las emulsiones solas sitúan el centro a **~61–62,5 m**, unos 40 m sobre la Cámara de la Reina, lo que coincide con el "40–50 m" publicado. El ajuste conjunto con KEK lo baja a 56–59 m, y KEK sola a 47–54 m (47,5 m en su mejor ajuste, a 26°). Parámetros de las emulsiones: `resultados/18_ajuste_emulsiones.json`.
- **Sección**: las emulsiones solas dan **~19–21 m²** (unos 10 m de alto por 2 m de ancho) y el ajuste conjunto con KEK **~9–11 m²**. Es del orden de la Gran Galería (~13 m²), como dice el artículo, pero el valor exacto depende del conjunto de datos. *(Corregido: una versión anterior decía 10–13 m², resumiendo ajustes hechos antes de corregir la extracción.)* La proporción entre alto y ancho no queda determinada: hay ajustes igual de buenos con 8–11 × 1,4–2 m y con 2,5 × 4 m.

### Inclinación: perfil de verosimilitud (σ con que se desfavorece cada ángulo frente al mejor ajuste)
| Datos | 0° | 10° | 20° | 26° (paralelo a la Galería) | 35° |
|---|---|---|---|---|---|
| Emulsiones, nominal | 0,4 | 0,9 | 2,2 | **2,8** | 3,9 |
| Emulsiones, sin el corte norte | 0,5 | 1,7 | 2,6 | 3,2 | 4,1 |
| Emulsiones, sin el corte sur | 1,6 | 0,5 | 0,1 | 0,4 | 1,0 |
| Emulsiones, con residuo de la Galería libre | 2,4 | 0,3 | 1,4 | 2,4 | 3,8 |
| KEK solo (posición del detector libre ±1 m) | **4,3** | 2,5 | 1,0 (a 18°) | 0,0 | 1,8 |
| **Conjunto** (mismo corredor para ambos) | 4,0 | 1,3 | 0,0 (a 18°) | 0,7 | 4,0 |

Matiz importante: el mejor ajuste de KEK coloca el corredor ~1,7 m al este del eje y unos 10 m más bajo que las emulsiones. Los dos detectores ven el mismo objeto, así que esa discrepancia apunta a un **sistemático en KEK**: residuos de la Gran Galería en la simulación que sirve de normalización, o la posición exacta de sus detectores. KEK tiene además una base de paralaje corta, de solo 2,9 m frente a los 10,3 m de las emulsiones.

## 4. Un error que encontramos en nuestro propio trabajo
La primera versión del análisis daba **"inclinación de 18°, horizontal descartada a 4–6σ"**, y parecía robusta frente a cinco variaciones. Dos comprobaciones la desmontaron:
1. **Quitando el corte más al norte, la inclinación desaparecía** (3,9°). El resultado dependía casi entero de un solo corte.
2. **Revisión de la extracción.** En 26 de 396 bins había dos candidatos: la cruz de datos y la curva gaussiana roja que los autores superpusieron. El cargador tomaba el primero y a veces cogía la curva. Ahora toma el que tiene la barra de error más larga, que es la cruz auténtica.

Con la corrección, la "inclinación de 18°" desaparece. Lo dejamos escrito porque es exactamente el tipo de error que convierte un análisis serio en un falso descubrimiento.

## 5. Ajuste conjunto
Obligando a los dos detectores a describir **el mismo** corredor (archivos `resultados/09_reanalisis_conjunto_inclinacion.json` y `simulador/reanalisis_conjunto.py`):

- **Inclinación**: preferida de ~10–26°, con la horizontal y los 35° desfavorecidos a ~4σ.
- **Dónde queda el corredor**: a z ≈ 56–58 m, a medio camino entre lo que prefiere cada conjunto de datos.
- **Pero la prueba de coherencia falla.** Por separado, los mínimos (con los errores reescalados) suman ≈ 730. En el ajuste conjunto, el mínimo es 802. Una diferencia de **Δχ² ≈ 70 para unos 6 parámetros compartidos** significa que, bajo un único corredor recto, **los dos conjuntos de datos son incompatibles**.

Por tanto, **no damos por bueno el "4σ contra la horizontal" del ajuste conjunto**. Lo arrastra KEK, que tiene un sistemático sin resolver: su corredor sale desplazado respecto al de las emulsiones. Las explicaciones posibles son tres:
1. el Vacío no es un corredor recto único;
2. hay residuos de las estructuras conocidas en la normalización de KEK;
3. no conocemos bien la posición de sus detectores.

Para resolverlo harían falta los datos originales o, mejor, una medición nueva desde otro ángulo.

### 5b. ¿Explica la forma del Vacío la tensión? No.
Probamos formas compuestas ajustadas a la vez a los dos conjuntos de datos (`simulador/reanalisis_formas.py`, `resultados/11_formas_conjuntas.json`):

| Forma | χ² conjunto | Tensión (frente a la suma de ajustes separados, ≈ 729) |
|---|---|---|
| Corredor recto con inclinación libre | 807,0 | +78 |
| Dos tramos (horizontal + inclinado) | 812,1 | +83 |
| Dos corredores superpuestos | 806,8 | +78 |

Ninguna forma reduce la tensión. Por tanto, **no la causa la geometría del Vacío**, sino un sistemático en alguno de los análisis. El candidato más probable es la normalización de KEK: sus datos están divididos por la simulación de ScanPyramids de las estructuras conocidas, no por la nuestra. También podría ser la posición o la orientación exacta de sus hodoscopios. Solo se puede resolver con los mapas originales: es la primera petición de [la propuesta técnica](../PROPUESTA_SCANPYRAMIDS_en.md).

## 6. Conclusión
- **Lo robusto**:
  - el Vacío existe;
  - está sobre el eje de la Gran Galería, a ~56–63 m de altura (emulsiones solas: 61–62,5 m; conjunto: 56–59 m);
  - tiene una sección parecida a la de la Galería;
  - mide ≥ 30 m.

  Coincide con lo publicado.
- **Lo no robusto: la inclinación.** Las emulsiones apuntan a horizontal o poco inclinado, KEK a inclinado, y la diferencia la marcan los sistemáticos, no la estadística. Esto confirma de forma independiente lo que dijo ScanPyramids ("could be inclined or horizontal"). También confirma nuestra conclusión de los documentos 08 y 09: **desde la Cámara de la Reina no se puede decidir**.
- **Consecuencia práctica**: la medición desde la Cámara del Rey o la de Campbell (P1/P2) sigue siendo el camino. Con ella, la separación entre horizontal e inclinado se consigue en días, no en años.
