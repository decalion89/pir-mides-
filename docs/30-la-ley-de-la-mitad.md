# 30 — La ley de la mitad de la señal

> **Pregunta.** En los docs. 28 y 29 aparecía siempre lo mismo: los errores de posición pequeños no fabrican ningún hueco, y por encima de un umbral fabrican huecos cada vez más significativos. El umbral no dependía de cuántos muones hubiera. ¿Por qué? ¿Hay una regla general?
>
> **La ley.**
> - Sea s la huella esperada de un hueco y r el residuo que deja un modelo erróneo. Los dos van en unidades de σ y sin la parte que absorben las molestias del ajuste (normalización, gradientes de aceptancia).
> - Llamemos **ρ = ⟨r, s⟩ / |s|²** a la fracción de la señal del hueco que el error imita.
> - Sea Z_real = |s| la significación que tendría un hueco real.
>
> | Tipo de búsqueda | Qué fabrica un error de modelo | Probabilidad, con ruido, de "descubrir" el hueco falso |
> |---|---|---|
> | **Hueco vacío** (contraste fijo: aire) | Un hueco falso **si y solo si ρ > ½**; Δχ² = Z_real²(1 − 2ρ) | **P = Φ(Z_real · (ρ − ½))** |
> | **Contraste libre** (se ajusta "un exceso del X %") | Siempre un exceso falso, de amplitud **â = ρ** y significación **Z_falso = ρ · Z_real** | crece sin límite con los datos |
>
> **Consecuencias.**
> 1. **ρ no depende de la exposición.** Con ruido de Poisson, r, s y σ² crecen igual con el tiempo de medida. Multiplicar los datos por 10 000 deja ρ igual (comprobado: varía < 1 %).
> 2. **Ley del todo o nada.** Al acumular datos, P tiende a 0 si ρ < ½ y a 1 si ρ > ½. Medir más no corrige un error de geometría: solo decide en qué lado del umbral cae, cada vez con más certeza.
> 3. **Las búsquedas de huecos vacíos tienen una zona segura.** Las de contraste libre (las de "exceso del X %", y casi todas las de densidad en volcanes, minas y presas) no la tienen: cualquier error correlacionado con la plantilla produce un falso exceso cuya significación crece como √N.
> 4. **Una prueba para distinguir lo real de lo falso.** Un hueco real da la misma amplitud desde todos los detectores. Uno falso da amplitudes ρ distintas, porque ρ depende de la geometría de cada detector. La concordancia de amplitudes entre detectores es, por tanto, una prueba directa contra los artefactos de modelo.

Archivos: [`simulador/ley_media_senal.py`](../simulador/ley_media_senal.py), [`resultados/38_ley_media_senal.json`](../resultados/38_ley_media_senal.json); prueba en [`tests/test_simulador.py`](../tests/test_simulador.py).

## Derivación (dos líneas)
Tras perfilar las molestias (proyección lineal P⊥), se define Δχ²(a) = |r − a s|² − |r|² = a²|s|² − 2a⟨r, s⟩.
- **Con a = 1** (hueco vacío): Δχ² = |s|²(1 − 2ρ). Es negativo si y solo si ρ > ½.
- **Con a libre:** â = ρ y Δχ²_min = −ρ²|s|². Es la fórmula del **sesgo por variable omitida** de la regresión lineal, aplicada a la muografía.
- **Con ruido n** (de varianza unidad por casilla): ⟨n, s⟩ ~ N(0, |s|²). Por tanto P(Δχ² < 0) = P(⟨n, s⟩ > |s|²(½ − ρ)) = Φ(|s|(ρ − ½)).
- **Invariancia:** si las cuentas escalan con λ y σ² = N, entonces r/σ y s/σ escalan con √λ, y ρ es un cociente que no depende de λ. El sistemático relativo del 2 % rompe esto ligeramente, porque pesa más en las casillas con muchas cuentas.

## Comprobación numérica (detectores de la Cámara de la Reina, Gran Vacío como hueco buscado)
Simulación con 16 subrayos por casilla, suavizado por dispersión múltiple y aceptancia de cada detector. Error de posición este-oeste δ.

**ρ(δ) por detector** (tabla completa en el JSON):

| Detector | −0,7 m | −0,5 m | −0,3 m | +0,3 m | +0,5 m | +0,7 m | Umbral ρ = ½ |
|---|---|---|---|---|---|---|---|
| KEK H1 (bajo el eje de la galería) | 0,71 | 0,45 | 0,25 | −0,11 | −0,08 | 0,19 | −0,54 m y +0,75 m |
| KEK H2 | 0,11 | 0,11 | 0,09 | −0,18 | −0,37 | −0,60 | ninguno en ±1,2 m |
| Nagoya NE1 | −0,06 | −0,03 | −0,02 | 0,01 | 0,02 | 0,02 | ninguno en ±1,2 m |
| Nagoya NE2 | −0,21 | −0,12 | −0,06 | 0,01 | −0,01 | −0,07 | −1,19 m |

Un ρ negativo imita una región *más densa*, no un hueco.

**Invariancia con la exposición** (KEK H1):

| | ×0,01 | ×0,1 | ×1 | ×10 | ×100 |
|---|---|---|---|---|---|
| δ = −0,7 m, solo Poisson | 0,717 | 0,712 | 0,711 | 0,711 | 0,711 |
| δ = −0,7 m, con sistemático del 2 % | 0,717 | 0,711 | 0,708 | 0,701 | 0,696 |
| δ = −0,3 m, solo Poisson | 0,257 | 0,254 | 0,254 | 0,254 | 0,254 |

La pequeña variación a ×0,01 viene de las casillas que caen por debajo de 5 cuentas.

**Monte Carlo con ruido de Poisson** (KEK H1, exposición reducida a Z_real ≈ 8,2; 400 réplicas):

| δ | ρ teórico | Amplitud ajustada (media ± desv.) | Z_falso medio / predicho ρ·Z_real | P(hueco vacío falso) simulada / predicha Φ(Z_real(ρ−½)) |
|---|---|---|---|---|
| −0,7 m | 0,714 | 0,719 ± 0,128 | 6,15 / 5,89 | 0,97 / 0,96 |
| −0,3 m | 0,255 | 0,265 ± 0,122 | 2,20 / 2,09 | 0,03 / 0,02 |

Las tres fórmulas se cumplen dentro del error de Monte Carlo.

## Qué explica
- **El umbral sin ley de potencias del doc. 28**, independiente de los muones de Kefrén: es la consecuencia 1.
- **El falso candidato real en los datos de Alvarez (doc. 27):** con 3,6 m de error, ρ > ½ y sale una "cámara" con Δχ² = −43.
- **Por qué el Gran Vacío es robusto (doc. 29):** con 30 cm de precisión, ρ ≤ 0,25 en todos los detectores de la Cámara de la Reina.

## Lo que esto significa para la muografía en general
1. **Hay que publicar ρ, no solo Z.** Una significación de 13σ no dice nada sobre si el hueco es real si no se acota cuánto de su señal puede imitar un error de geometría. Calcular ρ para los errores plausibles cuesta lo mismo que calcular la huella del hueco.
2. **En análisis de contraste libre, la amplitud es el control.** Un exceso con amplitud distinta en cada detector, o muy por debajo de la de un hueco de aire de ese tamaño, es sospechoso aunque su significación sea enorme.
3. **Diseño de campañas:** elegir posiciones donde ρ sea pequeño para los errores esperados. Para huecos paralelos a otros conocidos, eso significa desplazarse lateralmente (doc. 29).

## Qué es nuevo y qué no
- **No es nuevo:** las matemáticas. Es la proyección por mínimos cuadrados generalizados y la fórmula del sesgo por variable omitida, conocidas desde hace décadas.
- **No lo hemos encontrado publicado (búsqueda del 01/11/2026):**
  - su formulación para la muografía como criterio ρ > ½ para huecos vacíos;
  - la consecuencia de que el umbral no depende de la exposición;
  - la fórmula de probabilidad Φ(Z_real(ρ − ½));
  - su aplicación cuantitativa a los detectores del Gran Vacío.
  
  Lo más parecido que hemos visto son estudios de sesgos geométricos de alineamiento en detectores concretos, sin esta ley.
- **Es una herramienta útil, no un cambio de paradigma.** Su valor es práctico: convierte "¿puede ser un artefacto?" en un número que cualquiera puede calcular.

## Límites
- **Aproximación lineal en las molestias.** En los ajustes reales (Poisson, molestias no lineales) la ley es válida a primer orden. El Monte Carlo con Poisson la confirma en este caso.
- **Solo se han probado errores de traslación en la posición**, pero la ley vale para cualquier error de modelo: densidad, espectro, dimensiones de estructuras conocidas. Basta con calcular el r correspondiente.
- **La geometría de la Gran Galería está simplificada** (doc. 29).
