# 29 — ¿Pudo un error de posición fabricar el Gran Vacío?

> **Pregunta.** El doc. 28 mostró que un detector de muones mal situado puede "descubrir" cámaras que no existen. ¿Es inmune a ese efecto el mayor hallazgo de las pirámides en un siglo, el Gran Vacío de Keops (Morishima et al. 2017)?
>
> **Corregido el 01/11/2026 (doc. 30).** La primera versión trazaba un solo rayo por casilla y daba a KEK la aceptancia plana de una emulsión. Se ha rehecho con 16 subrayos por casilla, suavizado por dispersión múltiple y la aceptancia real de los hodoscopios ([`resultados/38_ley_media_senal.json`](../resultados/38_ley_media_senal.json)). Ahora las curvas son suaves. Las conclusiones se mantienen, pero los umbrales cambian:
> - KEK H1: 0,54 m hacia el oeste y 0,75 m hacia el este (antes "~0,7 m");
> - NE2: ~1,2 m hacia el oeste (antes "no hasta >1,2 m").
>
> **Respuesta: sí, con un margen de ~1,8 veces.**
> 1. **Con la precisión declarada del modelo (~30 cm),** ningún detector de la Cámara de la Reina fabrica una señal en la posición del Gran Vacío. El mejor falso hueco llega como mucho al 9 % de la señal real y aparece a ≥ 9 m.
> 2. **El detector más vulnerable es el hodoscopio KEK en H1,** casi debajo del eje de la Gran Galería (a 0,3 m). Con un error este-oeste de **≥ 0,54 m** (oeste) o **≥ 0,75 m** (este) entre detector y modelo, el hueco vacío falso **en la posición del Gran Vacío** mejora el ajuste.
> 3. **NE1, a 5,8 m del eje, es inmune:** ρ ≤ 0,19 hasta 1,2 m de error. **NE2, a 4,5 m,** solo lo fabrica con ~1,2 m de error hacia el oeste. **H2** nunca supera ρ = 0,12. En el ajuste conjunto con un mismo error para todos, la hipótesis "Gran Vacío" no se ve favorecida hasta ~3 m de error. Para entonces el mal ajuste del resto del mapa es ~30 veces mayor que la falsa señal.
> 4. **El análisis del CEA, desde fuera y sin restar ningún modelo, es inmune por construcción.**
>
> **El mecanismo.** El Gran Vacío está encima de la Gran Galería y es paralelo a ella. Desde abajo, su imagen es una franja estrecha norte-sur, igual que el borde de la galería. Si el detector está desplazado respecto al modelo de la galería, la galería mal colocada deja una franja de exceso de muones a un lado. Para un detector justo debajo del eje, esa franja cae donde estaría un vacío paralelo y encima.
>
> **Regla de diseño (paralaje):** para buscar un vacío paralelo a un hueco conocido, conviene que algún detector esté desplazado lateralmente varios metros del eje de ese hueco. Así la señal real y el artefacto de posición caen en sitios distintos. ScanPyramids lo cumplió con NE1/NE2, y por eso su resultado es robusto aunque KEK H1, solo, no lo sería frente a errores de ~0,5–0,75 m.

Archivos:
- **cifras vigentes:** [`simulador/ley_media_senal.py`](../simulador/ley_media_senal.py) y [`resultados/38_ley_media_senal.json`](../resultados/38_ley_media_senal.json);
- **versión inicial (un rayo por casilla, superada):** [`simulador/gran_vacio_y_posicion.py`](../simulador/gran_vacio_y_posicion.py), [`resultados/37_gran_vacio_y_posicion.json`](../resultados/37_gran_vacio_y_posicion.json) (barrido grueso, error común) y [`resultados/37b_gran_vacio_y_posicion_fino.json`](../resultados/37b_gran_vacio_y_posicion_fino.json).

## Método
1. **Datos simulados:** cuentas esperadas (Asimov, sin ruido) de NE1, NE2, KEK H1 y KEK H2, con todas las estructuras conocidas y **sin Gran Vacío**. Las posiciones son las publicadas: NE1 a 5,8 m al este del eje de la galería, NE2 a 4,5 m al oeste y H1 en la esquina sureste de la Cámara de la Reina (Morishima et al. 2017).
2. **Análisis:** con el detector desplazado δ respecto al modelo. Es equivalente a tener el modelo de las estructuras internas desplazado −δ. La normalización y dos gradientes lineales de aceptancia se dejan libres (perfilados).
3. **Hipótesis probadas:**
   - el Gran Vacío en su posición publicada (horizontal, 1,6 × 30 × 8 m, centro (7,3; 17; 63) m);
   - la mejor caja de su tamaño en una rejilla alrededor.
4. **Escala:** Δχ² relativo a la señal que daría un Gran Vacío real en ese mismo detector y sin error. Así el resultado no depende de la calibración absoluta de cada experimento.

## Resultados del barrido fino (corregido; error este-oeste; negativo = falsa detección)
Δχ² relativo = 1 − 2ρ de la hipótesis "Gran Vacío" en su posición publicada:

| Detector (distancia al eje) | −1,2 m | −0,9 m | −0,7 m | −0,5 m | −0,3 m | +0,3 m | +0,5 m | +0,7 m | +0,9 m | +1,2 m |
|---|---|---|---|---|---|---|---|---|---|---|
| KEK H1 (0,3 m) | **−1,43** | **−0,88** | **−0,42** | +0,11 | +0,50 | +1,21 | +1,15 | +0,61 | **−1,17** | **−1,58** |
| KEK H2 (3,2 m) | +0,90 | +0,80 | +0,77 | +0,77 | +0,82 | +1,37 | +1,74 | +2,19 | +2,71 | +3,45 |
| NE1 (5,8 m) | +1,38 | +1,19 | +1,12 | +1,06 | +1,03 | +0,98 | +0,97 | +0,96 | +0,95 | +0,93 |
| NE2 (4,5 m) | **−0,04** | +1,05 | +1,43 | +1,25 | +1,12 | +0,98 | +1,03 | +1,15 | +1,35 | +1,82 |

- Un valor de +1 significa que el modelo erróneo rechaza el Gran Vacío tan bien como el correcto.
- Un valor negativo significa que el error fabrica un Gran Vacío.

**Umbrales (ρ = ½):**
- KEK H1: −0,54 m y +0,75 m;
- NE2: −1,19 m;
- NE1 y H2: ninguno en ±1,2 m.

Con la precisión declarada de 30 cm, el detector más expuesto (H1) da ρ = 0,25: un hueco vacío falso empeoraría el ajuste (+0,50).

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
- **El barrido grueso con error común** (tabla anterior) usa todavía la versión de un rayo por casilla. Es orientativo.
- **Geometría simplificada:** la Gran Galería se modela como una caja horizontal, no inclinada 26° con muros en voladizo. El mecanismo de la franja paralela es general, pero los umbrales (0,5–0,75 m) son aproximados, quizá en un factor ~1,5.
- **Solo se prueban traslaciones.** Un error de orientación de 10 mrad, como el que declaran para las emulsiones, equivale a ~0,15 m a la altura de la galería. Está por debajo del umbral.
- **Datos sin ruido:** el ruido estadístico solo añade fluctuaciones simétricas.
- **Los Δχ² absolutos de KEK** usan la calibración de Nagoya y están sobrestimados. Por eso las conclusiones se dan en valores relativos.

## Qué aporta
- **La primera cuantificación, que sepamos, del margen** del Gran Vacío frente a errores de posición entre detector y modelo. El artículo original declara la precisión del modelo (~30 cm), pero no cuánto error haría falta para fabricar la señal. Aquí sale 0,54–0,75 m para el detector más vulnerable, ~1,2 m para NE2 y ninguno en ±1,2 m para NE1 y H2.
- **Una regla de diseño para futuras campañas,** como las que buscan prolongaciones del Gran Vacío o del corredor norte: un detector bajo el eje de un hueco conocido es el más expuesto a falsos vacíos paralelos a él, y la paralaje lateral de varios metros es la protección.
- **Un control negativo útil:** la misma herramienta que reprodujo un falso candidato real en los datos de Alvarez (doc. 28) no logra fabricar el Gran Vacío con errores realistas. Eso refuerza el hallazgo de ScanPyramids, no lo debilita.

## Referencias
- Morishima, K. et al. (2017). *Discovery of a big void in Khufu's Pyramid by observation of cosmic-ray muons*. Nature 552, 386–390 (arXiv:1711.01576). Contiene las posiciones de NE1/NE2/H1/H2, la precisión del modelo (~30 cm, levantamiento de Dormion) y las significaciones (13,7σ NE1, 12,7σ NE2, 5,8σ CEA).
