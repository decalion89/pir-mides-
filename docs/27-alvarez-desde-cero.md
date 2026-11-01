# 27 — Alvarez desde cero: reconstruir el experimento de 1969 sin usar su modelo

> **Objetivo.** El artículo sobre Alvarez (docs/19–20) usaba su predicción de 1969 como plantilla, porque no sabíamos reproducir su instrumento. Aquí intentamos lo que el artículo daba por imposible: **reconstruir desde cero la pirámide, la posición del detector y su aceptancia, y ajustar directamente sus 649 034 muones medidos** (figura 8).
>
> **Resultados.**
> 1. **Reconstrucción.** Usamos nuestro modelo de la pirámide con el remate de caliza original arriba y las caras retranqueadas ~6 m por debajo de ~90 m. Le sumamos una aceptancia separable en este-oeste y norte-sur, que es la propia de dos planos con rendijas, y dos términos de dependencia angular. **Dentro del cono de 35° ajusta sus cuentas con χ²/casilla = 1,4**, frente a 0,93 con el modelo de Alvarez. Fuera de él, en los bordes del detector, no lo conseguimos.
> 2. **Triangulación del detector.** Con sus datos, nuestro modelo sitúa el detector a **11–12 m al este y 4–5 m al norte** del centro. Alvarez, con su modelo, obtuvo 13,5 m al este; la topografía, 15,6 m al este y 4 m al norte.
> 3. **Exclusión independiente.** Dentro del cono, una cámara del tamaño de la del Rey queda excluida al 95 % en el **85 %** de las posiciones (con la plantilla de Alvarez, 95 %). **Su conclusión de 1969 se reproduce sin usar su modelo.**
> 4. **Un falso candidato, y la lección.** El modelo propio "encuentra" una cámara en (24, 16, 60) m con Δχ² = −43, que ninguna de 1 000 simulaciones de azar iguala. **Es un artefacto:**
>    - con la plantilla de Alvarez ese punto queda *excluido* (Δχ² = +8,8);
>    - con el modelo propio, la señal cambia de −43 a −25 y a +4 al mover el detector de (12, 5) a (13,5; 4) y a (15,5; 4) m.
>
>    Un modelo imperfecto de la pirámide o del instrumento produce "cámaras" que superan cualquier prueba estadística de ruido. **Solo las detectan las comprobaciones cruzadas con otro modelo y con otras suposiciones.**

Archivos: [`simulador/alvarez_independiente/`](../simulador/alvarez_independiente/), [`resultados/35_reanalisis_independiente_alvarez.json`](../resultados/35_reanalisis_independiente_alvarez.json).

## Pasos y cifras
| Modelo (cuentas de la fig. 8, 801 casillas) | χ² |
|---|---|
| Pirámide plana × aceptancia separable (control) | 21 769 |
| Nuestro modelo × aceptancia separable, detector en (15,5; 4) m | 7 446 |
| … detector triangulado en (12, 5, −6) m | 6 751 |
| … + remate y caras retranqueadas 6 m por debajo de 90 m | 5 511 |
| … + dos términos radiales (r², r⁴) | 2 307 |
| Plantilla de Alvarez × aceptancia separable (referencia) | 845 |

**Dónde queda el desajuste.** Cerca de las aristas de la pirámide el desajuste no es mayor que en el resto (6,5 frente a 7,0 por casilla), así que la geometría está bien. Está en los bordes del detector: 12–23 por casilla con tanθ > 0,8, frente a 1,9–4 en el centro.

**Solo en la zona central:**

| | Nuestro modelo, χ²/casilla | Plantilla de Alvarez, χ²/casilla |
|---|---|---|
| tanθ < 0,6 | 1,47 | 0,95 |
| tanθ < 0,7 (≈ cono de 35°) | 1,39 | 0,93 |
| tanθ < 0,8 | 1,40 | 0,97 |

**La prueba del candidato** (Δχ² en el punto y tres vecinos):

| Análisis | (24, 16, 60) | (24, 8, 60) | (16, 16, 52) | (32, 24, 68) |
|---|---|---|---|---|
| Plantilla de Alvarez | **+8,8** | +80 | +62 | +37 |
| Propio, detector (12, 5, −6), retranqueo 6 m bajo 90 m | −43,5 | +40 | +46 | +17 |
| Propio, retranqueo 4 m bajo 100 m | −27,8 | +61 | +46 | −6 |
| Propio, retranqueo 8 m bajo 80 m | −40,1 | +35 | +48 | +6 |
| Propio, sin remate | −36,9 | +36 | +48 | +6 |
| Propio, detector (13,5; 4; −3) | −24,5 | +67 | +55 | +59 |
| Propio, detector (15,5; 4; −0,5) | **+4,2** | +81 | +21 | +65 |

## Qué significa
- **Para Kefrén:** la conclusión negativa de Alvarez se sostiene también con un análisis completamente independiente, dentro del cono que él estudió.
- **Para quien vuelva a medir (ScIDEP, P13):** la parte más difícil no es la estadística, sino el modelo de la pirámide y del instrumento. Un error de unos metros en la posición del detector, o una geometría de la superficie mal descrita, produce falsas cámaras muy significativas. Recomendamos dos cosas: comprobar cada candidato con modelos y suposiciones alternativas, y medir la posición del detector con precisión topográfica.
- **Para el método:** este falso positivo es exactamente el tipo de error que convierte un buen análisis en un falso descubrimiento. Lo dejamos escrito por eso.

## Límites
- La reconstrucción es aproximada: el remate y el retranqueo están descritos con dos parámetros, y no hay heterogeneidades del núcleo de roca.
- Fuera de tanθ ≈ 0,8 no conseguimos reproducir el instrumento.
- La significación global del análisis independiente no es fiable, precisamente porque el modelo tiene errores sistemáticos que la nula no representa.
