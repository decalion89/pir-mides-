# 28 — Cuándo fabrica un detector de muones una cámara que no existe

> **Pregunta.** En el reanálisis independiente de Alvarez (doc. 27), un error de ~3,6 m en la posición del detector fabricó una "cámara" con Δχ² = −43. ¿Hay una regla general? ¿Con qué precisión hay que conocer la posición de un detector para no inventar cavidades, y cómo cambia eso con la cantidad de datos?
>
> **Hipótesis inicial (incorrecta).** Esperábamos una ley de potencias: falsa señal ∝ N·δ², de modo que la precisión necesaria mejoraría como N^(−1/2).
>
> **Lo que muestra el experimento numérico.**
> 1. **Hay un umbral, no una ley de potencias.** Con errores horizontales de hasta ~1 m no aparece ninguna falsa cámara del tamaño de la del Rey, **tenga el experimento los muones que tenga**.
> 2. **Por encima del umbral, la falsa señal crece en proporción al número de muones.** Con 65 millones de muones, 2 m de error fabrican una "cámara" con Δχ² ≈ −700 a −940 (~26–30σ). Con 3,5 m, ~−4 000.
> 3. **Los errores verticales no fabrican cámaras** con esta geometría.
> 4. **Validación con datos reales:** con 0,65 millones de muones y 3,5 m de error hacia el norte, el simulador da Δχ² = −46. El falso candidato real del doc. 27 dio −43, con un error de 3,6 m.
>
> **Regla práctica:** en un experimento como el de Alvarez o el de ScIDEP, la posición horizontal del detector debe conocerse **mejor que ~1 m** respecto a un modelo fiel de la superficie de la pirámide. Por encima de eso, más estadística no ayuda: fabrica falsos descubrimientos más significativos.

Archivos: [`simulador/ley_falso_hueco.py`](../simulador/ley_falso_hueco.py), [`resultados/36_ley_falso_hueco.json`](../resultados/36_ley_falso_hueco.json).

## Método
1. **Datos simulados:** cuentas esperadas (sin ruido) de Kefrén **sin ninguna cámara**, vistas desde (15,5; 4; −0,5) m, con N = 6,5 × 10⁵, 6,5 × 10⁶ o 6,5 × 10⁷ muones dentro del cono de 35°.
2. **Análisis:** con el modelo desplazado δ = 0,25–3,5 m hacia el este, el norte o abajo, con las mismas correcciones del instrumento que en el doc. 27 (aceptancia separable y dos términos radiales), ajustadas por máxima verosimilitud.
3. **Búsqueda:** se prueba una cámara del tamaño de la del Rey en cada posición del cono (rejilla de 8 m) y se anota el mejor Δχ². Si es negativo, es una "cámara" falsa.

## Resultados (mejor Δχ² de una cámara inexistente; negativo = falsa detección)
| N | Dirección | δ = 0,25 m | 0,5 m | 1 m | 2 m | 3,5 m |
|---|---|---|---|---|---|---|
| 6,5 × 10⁵ | norte | — | — | +0,1 | −9 | **−46** |
| 6,5 × 10⁶ | este | +38 | +35 | +12 | −69 | −356 |
| 6,5 × 10⁶ | norte | +34 | +29 | +1 | −94 | −463 |
| 6,5 × 10⁷ | este | +376 | +352 | +126 | **−695** | −3 545 |
| 6,5 × 10⁷ | norte | +336 | +285 | +16 | **−939** | −4 662 |
| cualquiera | abajo | > 0 | > 0 | > 0 | > 0 | > 0 |

El χ² del fondo (sin cámara) crece como N·δ², como se espera de un sesgo sistemático. Pero una cámara solo "mejora" el ajuste cuando el patrón del error se parece a su huella, y eso ocurre a partir de ~1–1,5 m.

## Por qué importa
- **Para ScIDEP y cualquier medición nueva en Giza:** con 10⁸ muones, un error de posición de 2 m daría una "cámara" a ~30σ. Hay que medir la posición del detector con topografía de precisión, por debajo de ~1 m, y modelar la superficie de la pirámide con la misma precisión. Si la posición se ajusta a partir de los propios datos, como hizo Alvarez y como hicimos en el doc. 27, cualquier imperfección del modelo desplaza la posición ajustada y puede producir el mismo efecto.
- **Para la muografía en general** (volcanes, reactores, minas): la regla cualitativa es la misma. El umbral concreto depende de la geometría y del tamaño de la cavidad buscada, y debería calcularse en cada caso con un experimento numérico como este.

## Límites y honestidad
- Es un resultado numérico para una geometría (Kefrén desde la Cámara de Belzoni) y un tamaño de cavidad. El valor del umbral no es universal.
- Los datos simulados no tienen ruido. Con ruido, las fluctuaciones añaden falsos candidatos débiles también por debajo del umbral.
- La hipótesis inicial (precisión ∝ N^(−1/2)) era incorrecta, y así queda escrito. Lo que sí escala con N es la intensidad de la falsa señal una vez superado el umbral.
- Que los muógrafos deben alinear bien sus detectores es conocido. Lo nuevo aquí es la cuantificación para esta geometría y su validación con un falso positivo real en datos históricos.
