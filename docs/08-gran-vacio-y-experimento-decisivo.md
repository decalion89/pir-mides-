# 08 — El Gran Vacío: qué puede ser y cómo averiguarlo

> **Resumen.** Los datos de 2017 no bastan para saber qué es el Gran Vacío. Desde la Cámara de la Reina, un corredor horizontal, uno inclinado, una galería de contrapeso y varias cámaras apiladas producen **casi la misma señal**. Nuestro modelo, validado con los datos publicados, calcula qué vería un detector desde otros puntos. **Un detector de muones de 1 m² en la Cámara del Rey, que es accesible al público, distinguiría entre esas hipótesis en días o semanas.** Desde la Cámara de Campbell, la más alta de las cámaras de descarga, bastarían ~1–5 días. Abajo están las predicciones concretas de cada hipótesis, para que la medición pueda confirmarlas o refutarlas.

Archivos: [`simulador/piramide/vacio.py`](../simulador/piramide/vacio.py), [`resultados/04_gran_vacio.json`](../resultados/04_gran_vacio.json), figuras `04a`, `04b` y `04c`.

## 1. Qué se sabe (Morishima et al., *Nature* 2017)
- El exceso de muones es **> 10σ** con tres técnicas independientes.
- Mide **más de 30 m** de largo, tiene una sección "comparable a la Gran Galería" y está **encima de la Gran Galería**.
- Su centro está a 40–50 m del suelo de la Cámara de la Reina. Empieza casi en el centro de la pirámide y se extiende hacia el norte.
- Los autores dicen expresamente que puede ser **horizontal o inclinado**, y **una o varias estructuras**.

## 2. Hipótesis
| | Hipótesis | Qué sería |
|---|---|---|
| H1 | Corredor horizontal | La versión horizontal publicada |
| H2 | Corredor inclinado 26° | La versión inclinada publicada, una "segunda Gran Galería" |
| H3 | **Galería de contrapeso** (tipo Houdin) | Galería inclinada cuyo extremo alto llega a la cota de las cámaras de descarga y se une a ellas por un pasaje. Sería infraestructura para subir las vigas de granito |
| H4 | Zona de relleno suelto | Un volumen ancho de baja densidad, no un hueco limpio |
| H5 | Tres cámaras apiladas | Huecos bajos superpuestos, como las cámaras de descarga |
| H6 | Hueco de descarga pegado al techo de la Gran Galería | La explicación estructural "obvia" |

A cada hipótesis le ajustamos su forma y su posición para que imite lo mejor posible la señal de 2017. Después medimos cuánto difiere aún de lo observado:

| Hipótesis | Diferencia que queda con los datos de 2017 | Veredicto |
|---|---|---|
| H1 | 0σ (es la referencia) | compatible |
| H2 | 4,1σ | **no descartable** (hay tensión leve) |
| H3 | 4,9σ | **no descartable** (hay tensión leve) |
| H5 | 2,4σ | **no descartable** |
| H4 | 13σ | descartada *si* la sección estrecha publicada es correcta |
| H6 | 29σ | **descartada**: el Vacío está ~20 m por encima de la Gran Galería, no pegado a ella |

**Por qué el Vacío no es simplemente un hueco de descarga sobre la Gran Galería:** un hueco así tendría que estar justo encima del techo, como el corredor de la cara norte sobre la entrada o las cámaras de descarga sobre la Cámara del Rey. El observado está mucho más arriba.

## 3. ¿Lo exige la física de las vigas de granito? (`granito.py`)

Unas ~43 vigas de **25–80 t** se colocaron entre ~49 y ~61 m. El núcleo tardó **~1,2–3 años** en subir de 43 a 66 m, según el modelo de construcción. Comparamos tres métodos:

| Viga | Rampa: personas (longitud del equipo en 4 filas) | Contrapeso necesario (optimista–pesimista) | Palancas simultáneas | Días con palancas desde 43 m |
|---|---|---|---|---|
| 25 t | 218 (55 m) | 54–127 t | 7 | ~15 |
| 40 t | 349 (87 m) | 87–204 t | 10 | ~15 |
| 60 t | 523 (131 m) | 130–305 t | 15 | ~15 |
| 80 t | 698 (175 m) | 173–407 t | 20 | ~15 |

- **Rampa recta hasta 61 m**: ~0,53 millones de m³, el **20 % del volumen** de la pirámide. Es grande pero posible; se parece a lo que propuso Lehner.
- **Zigzag por una cara**: a esa altura, el tramo útil mide ~123 m. Un equipo de 60–80 t en 4 filas no cabe; con 8 filas sí.
- **Contrapeso**: un Vacío de 1,6 × 8 × 30 m admite ~340 t de lastre llenándolo al 40 %, y ~680 t al 80 %. **Basta para vigas de 60 t** incluso con supuestos pesimistas.
- **Palancas acompañando la subida**: las 43 vigas suman ~420 días de trabajo en serie, o ~70 días con 6 equipos en paralelo. **Caben de sobra en la ventana** de ~1–3 años.

**Conclusión honesta**: los tres métodos son físicamente viables. **Las vigas no demuestran que el Vacío fuera una galería de contrapeso.** La hipótesis H3 es mecánicamente coherente, porque el volumen alcanza y la altura encaja, pero no es necesaria. La única forma de decidir es **medir**.

## 4. El experimento decisivo

Evaluamos siete puestos para un detector nuevo (figura `04a`). Para cada par de hipótesis, la tabla da los **días de exposición con 1 m² hasta alcanzar 5σ**. Incluye un 2 % de sistemático, resolución de ~20 mrad y el factor de realismo de 0,5; el error es de un factor ~4 en los tiempos.

| Puesto | Acceso | H1–H2 | H1–H3 | H2–H3 | H1–H4 | H1–H5 |
|---|---|---|---|---|---|---|
| Cámara de la Reina (como en 2017) | público | 1151 | 173 | ∞ | 11 | ∞ |
| Cabeza de la Gran Galería | público | 5 | 4 | ∞ | 1 | 7 |
| **Cámara del Rey** | **público** | **3** | **3** | **54** | **1** | **14** |
| Cámara de Davison (1ª de descarga) | restringido | 1 | 1 | ∞ | 1 | 4 |
| **Cámara de Campbell (5ª de descarga)** | restringido | **1** | **1** | **5** | **1** | **2** |
| Exterior, cara norte / cara este | libre | no separa en 100 días | | | | |

"∞" significa que el sistemático del 2 % impide llegar a 5σ desde ese puesto, por mucho que se mida.

**Lectura de la tabla:**
1. **Desde la Cámara de la Reina es casi imposible decidir.** Eso explica por qué en 2017 no se pudo saber si el Vacío es horizontal o inclinado.
2. **La Cámara del Rey decide todas las parejas.** Es de acceso público y ya caben en ella los detectores usados en 2017. La pareja más difícil, "inclinado simple" contra "galería de contrapeso", necesita **~2 meses** (hasta ~7 meses en el peor caso del modelo).
3. **La Cámara de Campbell es el puesto óptimo**: está a la altura del Vacío, lo ve de lado y a ~20–30 m. Con ~1 semana bastaría para todo. En 2018 ScanPyramids anunció que quería medir desde las cámaras de descarga; no hemos encontrado resultados publicados.
4. **Desde fuera de la pirámide no se distinguen formas**, solo se detecta que el Vacío existe.

### Qué debería verse en cada caso (figura `04b`)
- **Desde la Cámara del Rey** mirando hacia el Vacío:
  - H1 (horizontal): una franja corta e inclinada entre tanθy ≈ −0,2 y +0,45.
  - H2 y H3: una franja larga que llega hasta tanθy ≳ 0,65.
  - H5: una franja **interrumpida en tramos**.
  - H4: una mancha ancha y difusa.
- **Desde la Cámara de Campbell**:
  - H1: una mancha compacta casi frontal, entre tanθy 0 y 0,3.
  - H2 y H3: una franja larga hasta 0,7.
  - **Solo H3** añade un exceso **cerca del detector**: su pasaje de conexión pasaría a pocos metros, al norte y por encima de las cámaras de descarga.

## 5. Prueba adicional: la rampa interna de Houdin
Si existiera un túnel en espiral de 1,8–2,6 m de sección a ~12 m de las caras, los detectores de la Cámara de la Reina de 2017 lo habrían visto como un **anillo de excesos de 1,6–4 %** cerca de |tanθ| ≈ 1, con una significación de **16–30σ** en el modelo.

Las imágenes publicadas no muestran ese anillo. En 2017, Bob Brier dijo que los datos sugerían que la rampa "no está ahí". Además, el modelo de construcción (doc. 07) muestra que una rampa interna de **un solo carril** no termina la obra a tiempo en ninguna de las 600 simulaciones. La rampa interna queda así **doblemente desfavorecida**. Matiz: si el análisis de 2017 no cubría bien la periferia de la aceptancia, esta prueba es más débil.

## 6. Lo que esto no dice
- No decimos qué es el Vacío. Decimos **cómo averiguarlo** y **qué resultado corresponde a cada hipótesis**.
- Los tiempos dependen de la geometría aproximada (±1–2 m) y de un modelo de flujo sin dispersión múltiple. Antes de pedir tiempo de detector, convendría repetir el cálculo con Geant4, la herramienta de simulación que usan los equipos de ScanPyramids.
