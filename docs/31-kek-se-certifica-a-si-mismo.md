# 31 — Los datos de KEK descartan el mecanismo del falso vacío

> **Pregunta.** La ley de la mitad (doc. 30) dice que el hodoscopio KEK H1 fabricaría un Gran Vacío falso si su simulación de normalización estuviera desplazada ≥ 0,54 m (oeste) o ≥ 0,75 m (este) respecto a los datos. Hasta ahora solo podíamos citar la precisión declarada del modelo (~30 cm). ¿Lo dicen también los propios datos publicados? ¿Y explica ese desplazamiento la tensión entre KEK y las emulsiones de Nagoya (Δχ² ≈ 70, doc. 11)?
>
> **Respuesta.**
> 1. **Los datos de KEK fijan el registro entre datos y simulación con mucha precisión.** Un desplazamiento δ dejaría en el cociente "datos / simulación" un residuo con la forma de la Gran Galería, y los datos no lo muestran. El χ² de KEK es mínimo en δ ≈ 0–0,08 m y sube **+63 a +0,25 m y +265 a −0,25 m** (errores ya reescalados).
>    - Estadísticamente, |δ| < 0,1 m a 5σ.
>    - Con margen para nuestro modelo simplificado de la galería, |δ| ≲ 0,25 m.
>
>    En los dos casos el desplazamiento queda **muy por debajo del umbral de 0,54 m**. La señal del Gran Vacío en KEK no puede ser un artefacto de ese tipo, y no por la precisión que declaran los autores, sino **por sus propios datos**.
> 2. **La tensión KEK–emulsiones no se explica así.** Con δ libre, el mejor ajuste conjunto sigue en δ = 0 y la tensión sigue en Δχ² ≈ 66–70. Su origen está en otra parte. Las candidatas que quedan:
>    - la posición absoluta del hodoscopio, que desplaza datos y simulación a la vez;
>    - una forma del Vacío más compleja que las probadas;
>    - errores de extracción en las figuras;
>    - la normalización de las emulsiones.

Archivos: [`simulador/tension_kek_normalizacion.py`](../simulador/tension_kek_normalizacion.py), [`resultados/39_tension_kek_normalizacion.json`](../resultados/39_tension_kek_normalizacion.json), [`resultados/log_tension_kek.txt`](../resultados/log_tension_kek.txt).

## Método
1. **Datos:** los 679 cocientes de KEK (H1 y H2) y los perfiles de las emulsiones, como en el doc. 11.
2. **Modelo del cociente de KEK:** R = I(detector en p, con el Vacío) / I(detector en p + δ, sin el Vacío).
   - Con δ = 0 es el modelo del doc. 11.
   - Con δ ≠ 0, la simulación que normaliza "ve" la pirámide desde un sitio equivocado.
3. **Barrido:** δ este-oeste de −1,5 a +1,5 m (cada 0,25 m), para dos posiciones del detector (nominal y 1 m al oeste, la preferida en el doc. 11).
4. **Ajustes para cada δ:** KEK sola y conjunto con las emulsiones, con un corredor de posición, tamaño e inclinación libres.
   - Tensión = χ²_conjunto − χ²_emulsiones solas − χ²_KEK sola, con los errores reescalados como en el doc. 11.
   - En dos casos el ajuste de KEK sola se quedó en un mínimo local peor que la parte de KEK del ajuste conjunto. Se usa el menor de los dos.

## Resultados (χ² con los errores reescalados)
| Detector | δ = −0,5 m | −0,25 m | **0** | +0,25 m | +0,5 m |
|---|---|---|---|---|---|
| Nominal: KEK sola | 1 151 | 929 | **663** | 726 | 1 053 |
| Nominal: conjunto | 1 631 | 1 162 | **812** | 982 | 1 303 |
| 1 m al oeste: KEK sola | 1 386 | 808 | **668** | 840 | 1 091 |
| 1 m al oeste: conjunto | 1 598 | 967 | **807** | 1 095 | 1 389 |

- **Ajuste parabólico cerca de δ = 0:** vértice en +0,08 m (nominal) y −0,01 m (1 m al oeste), con σ = 0,02 m. El límite a 5σ (Δχ² = 25) es ±0,10 m.
- **Tensión mínima:** 66 (mejor ajuste conjunto, 807, en δ = 0 con el detector 1 m al oeste). Es la misma que sin δ.
- **Ningún δ ≠ 0 reduce la tensión:** todos la aumentan, a entre 80 y 400.

## Por qué el límite es tan fuerte
- **La Gran Galería está casi justo encima de H1 y es muy contrastada:** un hueco de 8,6 m de alto bajo ~10 m de roca.
- **Desplazarla 25 cm en la simulación** cambia el cociente en sus bordes en varios por ciento.
- **Los datos de KEK tienen errores de ~1 % por punto**, en cientos de puntos que cruzan esos bordes.

Por eso el mismo detector que sería el más vulnerable a un falso vacío (doc. 30) es también el que mejor certifica que no lo hay.

## Límites
- **La galería modelada es una caja horizontal,** no la galería inclinada real. La forma exacta del residuo y, por tanto, el límite de 0,1 m son aproximados. Por eso damos también el límite conservador de ~0,25 m, donde Δχ² ya es ≥ 63.
- **Solo se ha barrido la dirección este-oeste,** la sensible según el doc. 30. Un error norte-sur o vertical no fabricaba el Vacío en el doc. 29.
- **Datos leídos de las figuras,** no los originales.

## Qué significa
- **Para el Gran Vacío:** queda descartado con los datos publicados, y no solo con la precisión declarada, el mecanismo por el que un error de modelo fabricaría la señal en el detector más expuesto. Sumado a NE1, NE2 y al análisis sin modelo del CEA, la existencia del Vacío es robusta frente a este tipo de error.
- **Para la tensión del doc. 11:** se descarta una de las tres explicaciones que propusimos (residuos de las estructuras conocidas en la normalización de KEK). Las otras dos siguen abiertas.
- **Para la muografía en general:** una estructura conocida y contrastada cerca de la línea de visión actúa como **regla de calibración**: los datos fijan su propio registro. Es el complemento práctico de la ley de la mitad. La misma estructura que puede fabricar falsos huecos permite demostrar que no lo ha hecho.
