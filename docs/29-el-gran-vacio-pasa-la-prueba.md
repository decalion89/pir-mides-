# 29 — ¿Pudo un error de posición fabricar el Gran Vacío?

> **Pregunta.** El doc. 28 mostró que un detector de muones mal situado puede "descubrir" cámaras que no existen. ¿Es inmune a ese efecto el mayor hallazgo de las pirámides en un siglo, el Gran Vacío de Keops (Morishima et al. 2017)?
>
> **Respuesta: sí, con un margen de ~2 veces.**
> 1. **Con la precisión declarada del modelo (~30 cm),** ningún detector de la Cámara de la Reina fabrica una señal en la posición del Gran Vacío. El mejor falso hueco llega como mucho al 9 % de la señal real y aparece a ≥ 9 m.
> 2. **El detector más vulnerable es el hodoscopio KEK en H1,** casi debajo del eje de la Gran Galería (a 0,3 m). Con un error este-oeste de **~0,7 m** entre detector y modelo, aparece un hueco falso **exactamente donde está el Gran Vacío**, con el 44 % de la señal real.
> 3. **Los detectores de Nagoya están a 5,8 m (NE1) y 4,5 m (NE2) del eje.** Hasta 1,2 m de error nunca producen un hueco falso en esa posición: sus artefactos aparecen a 6–13 m. En el ajuste conjunto con un mismo error para todos, la hipótesis "Gran Vacío" no se ve favorecida hasta ~3 m de error. Para entonces el mal ajuste del resto del mapa es ~30 veces mayor que la falsa señal.
> 4. **El análisis del CEA, desde fuera y sin restar ningún modelo, es inmune por construcción.**
>
> **El mecanismo.** El Gran Vacío está encima de la Gran Galería y es paralelo a ella. Desde abajo, su imagen es una franja estrecha norte-sur, igual que el borde de la galería. Si el detector está desplazado respecto al modelo de la galería, la galería mal colocada deja una franja de exceso de muones a un lado. Para un detector justo debajo del eje, esa franja cae donde estaría un vacío paralelo y encima.
>
> **Regla de diseño (paralaje):** para buscar un vacío paralelo a un hueco conocido, conviene que algún detector esté desplazado lateralmente varios metros del eje de ese hueco. Así la señal real y el artefacto de posición caen en sitios distintos. ScanPyramids lo cumplió con NE1/NE2, y por eso su resultado es robusto aunque KEK H1, solo, no lo sería frente a errores de ~0,7 m.

Archivos: [`simulador/gran_vacio_y_posicion.py`](../simulador/gran_vacio_y_posicion.py), [`resultados/37_gran_vacio_y_posicion.json`](../resultados/37_gran_vacio_y_posicion.json) (barrido grueso, error común), [`resultados/37b_gran_vacio_y_posicion_fino.json`](../resultados/37b_gran_vacio_y_posicion_fino.json) (barrido fino por detector).

## Método
1. **Datos simulados:** cuentas esperadas (Asimov, sin ruido) de NE1, NE2, KEK H1 y KEK H2, con todas las estructuras conocidas y **sin Gran Vacío**. Las posiciones son las publicadas: NE1 a 5,8 m al este del eje de la galería, NE2 a 4,5 m al oeste y H1 en la esquina sureste de la Cámara de la Reina (Morishima et al. 2017).
2. **Análisis:** con el detector desplazado δ respecto al modelo. Es equivalente a tener el modelo de las estructuras internas desplazado −δ. La normalización y dos gradientes lineales de aceptancia se dejan libres (perfilados).
3. **Hipótesis probadas:**
   - el Gran Vacío en su posición publicada (horizontal, 1,6 × 30 × 8 m, centro (7,3; 17; 63) m);
   - la mejor caja de su tamaño en una rejilla alrededor.
4. **Escala:** Δχ² relativo a la señal que daría un Gran Vacío real en ese mismo detector y sin error. Así el resultado no depende de la calibración absoluta de cada experimento.

## Resultados del barrido fino (error este-oeste; negativo = falsa detección)
Δχ² relativo de la hipótesis "Gran Vacío" en su posición publicada:

| Detector (distancia al eje) | −1,2 m | −0,9 m | −0,7 m | −0,5 m | −0,3 m | +0,3 m | +0,5 m | +0,7 m | +0,9 m | +1,2 m |
|---|---|---|---|---|---|---|---|---|---|---|
| KEK H1 (0,3 m) | **−0,63** | **−0,60** | **−0,44** | +0,17 | +0,33 | +1,06 | +1,12 | +1,18 | **−0,33** | **−0,35** |
| KEK H2 (3,2 m) | +1,12 | +1,07 | +1,05 | +1,03 | +1,01 | +1,08 | +1,26 | +1,59 | +2,09 | +2,88 |
| NE1 (5,8 m) | +1,04 | +1,01 | +1,00 | +1,00 | +1,00 | +1,00 | +0,99 | +0,99 | +0,98 | +0,97 |
| NE2 (4,5 m) | +0,48 | +1,11 | +1,29 | +1,18 | +1,10 | +0,93 | +0,90 | +0,90 | +0,97 | +1,27 |

- Un valor de +1 significa que el modelo erróneo rechaza el Gran Vacío tan bien como el correcto.
- Un valor negativo significa que el error fabrica un Gran Vacío.

**Solo KEK H1 lo fabrica, y solo con errores ≥ 0,7 m.** Con −0,7 m, la mejor caja de toda la rejilla cae exactamente en la posición publicada.

Mal ajuste del resto del mapa en ese caso: χ² de fondo = 1,2 veces la señal real. Tras ajustar el falso hueco quedaría un residuo de ~0,8 veces la señal real, visible como estructura sin explicar. Los autores informan de que el modelo elimina con éxito las estructuras conocidas en el mapa de KEK. Eso también indica que no hubo un desajuste de ese tamaño.

## Ajuste conjunto con un error común (barrido grueso hacia el este)
Si la misma referencia topográfica estuviera equivocada para NE1, NE2 y H1:

| δ | Δχ² del Gran Vacío (conjunto) | Mejor caja falsa | χ² de fondo |
|---|---|---|---|
| 0,5 m | +2 252 (rechazado) | +294 (ninguna) | 2 047 |
| 1 m | +58 | −572 en (9, 25, 75) m | 5 331 |
| 2 m | +161 | +7 | 8 048 |
| 3 m | +3 | −302 en (9, 17, 63) m | 9 822 |

Unidades: calibradas a Nagoya.
- **La paralaje entre detectores** impide que los artefactos de cada uno triangulen en el mismo punto, salvo con errores de metros.
- **Con errores de metros**, el mal ajuste global es enorme.

## Límites
- **Geometría simplificada:** la Gran Galería se modela como una caja horizontal, no inclinada 26° con muros en voladizo. El mecanismo de la franja paralela es general, pero los umbrales (0,7 m) son aproximados, quizá en un factor ~1,5.
- **Solo se prueban traslaciones.** Un error de orientación de 10 mrad, como el que declaran para las emulsiones, equivale a ~0,15 m a la altura de la galería. Está por debajo del umbral.
- **Datos sin ruido:** el ruido estadístico solo añade fluctuaciones simétricas.
- **Los Δχ² absolutos de KEK** usan la calibración de Nagoya y están sobrestimados. Por eso las conclusiones se dan en valores relativos.

## Qué aporta
- **La primera cuantificación, que sepamos, del margen** del Gran Vacío frente a errores de posición entre detector y modelo. El artículo original declara la precisión del modelo (~30 cm), pero no cuánto error haría falta para fabricar la señal. Aquí sale ~0,7 m para el detector más vulnerable y >1,2 m para los demás.
- **Una regla de diseño para futuras campañas,** como las que buscan prolongaciones del Gran Vacío o del corredor norte: un detector bajo el eje de un hueco conocido es el más expuesto a falsos vacíos paralelos a él, y la paralaje lateral de varios metros es la protección.
- **Un control negativo útil:** la misma herramienta que reprodujo un falso candidato real en los datos de Alvarez (doc. 28) no logra fabricar el Gran Vacío con errores realistas. Eso refuerza el hallazgo de ScanPyramids, no lo debilita.

## Referencias
- Morishima, K. et al. (2017). *Discovery of a big void in Khufu's Pyramid by observation of cosmic-ray muons*. Nature 552, 386–390 (arXiv:1711.01576). Contiene las posiciones de NE1/NE2/H1/H2, la precisión del modelo (~30 cm, levantamiento de Dormion) y las significaciones (13,7σ NE1, 12,7σ NE2, 5,8σ CEA).
