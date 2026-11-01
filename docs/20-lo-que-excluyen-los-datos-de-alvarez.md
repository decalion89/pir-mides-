# 20 — Lo que excluyen de verdad los datos de Alvarez

> **Resumen.** Los documentos 18 y 19 respondían a "¿qué afirmó Alvarez?" y a "¿esconden sus residuos una cámara?". Este responde a una pregunta más útil: **¿en qué puntos de Kefrén descartan sus datos reales una cámara, y con qué confianza?** Para cada posición predecimos la huella de una cámara en los 801 bins de su figura 10 y la comparamos con los residuos publicados.
> - **Al 95 % de confianza**, los datos excluyen una cámara del tamaño de la del Rey en el **22 % del volumen** de Kefrén; a 5σ, en el 12 %.
> - **Dentro del cono de 35°** que analizó Alvarez, la excluyen en el 95 % de su volumen al 95 %, pero solo en el 58 % a 5σ. Su afirmación ("en cualquier punto del cono") se sostiene con el criterio habitual de exclusión, no con el de descubrimiento.
> - **Fuera de ese cono**, en la franja de 35–45° que nadie había analizado, sus datos excluyen además un **6,5 % del volumen total**. Es exploración nueva a partir de datos de 1969.
> - **El mejor "candidato"** (Δχ² = −12, 3,5σ local) tiene una significación global de **0,85σ** (p = 0,40) y salta de sitio con cambios de 3° en la alineación. **No hay ninguna cámara en los datos de Alvarez.**

Archivos:
- código: [`simulador/exclusion_alvarez.py`](../simulador/exclusion_alvarez.py), [`simulador/significacion_global_alvarez.py`](../simulador/significacion_global_alvarez.py), [`simulador/figuras_exclusion_alvarez.py`](../simulador/figuras_exclusion_alvarez.py);
- resultados: [`resultados/24_exclusion_alvarez.json`](../resultados/24_exclusion_alvarez.json) y `.npz`;
- figura: `figuras/11_exclusion_datos_alvarez.png`.

## 1. Método
1. **Modelo del experimento.** Detector en la Cámara de Belzoni y rejilla fina uniforme en ángulo (0,25°), agrupada en los bins de 3° × 3° de Alvarez.
   - **Aceptancia:** se anula a ~45° en dirección este-oeste y a ~43° en norte-sur. La forma norte-sur se ajusta a las predicciones publicadas por Alvarez (su figura 9), y queda dentro de un ~25 % en las filas del borde.
   - **Normalización:** ~1600 muones en un bin central, como dice el artículo. El total en los bins válidos sale ~605 000 (Alvarez seleccionó ~650 000).
2. **Huella** de una cámara en cada bin: s = (N_con − N_sin)/√N_sin.
3. **Comparación con los datos:** Δχ² = [Σ(r − s)² − Σr²]/κ, sumando sobre los 801 bins de la figura 10.
   - r son los residuos publicados.
   - κ = 1,34 es su varianza, que infla los errores para tener en cuenta los sistemáticos con estructura espacial (doc. 19).
   - Δχ² ≥ 3,84 excluye la cámara al 95 %, Δχ² ≥ 25 la excluye a ~5σ, y Δχ² < 0 significa que los datos la prefieren.
4. **Solo cuentan las posiciones en que la caja cabe entera** dentro de la pirámide.
5. **Significación global del mejor candidato.** Se generan 5000 mapas de residuos simulados con la misma correlación espacial, dispersión y redondeo que los datos (doc. 19), y en cada uno se busca el mínimo de Δχ² en las 4 409 posiciones.

## 2. Resultados (rejilla de 8 m)
| Hueco | Excluido al 95 % | Excluido a 5σ | Dentro del cono, al 95 % / a 5σ | Fuera del cono, al 95 % (fracción del total) |
|---|---|---|---|---|
| Del tamaño de la Cámara del Rey | **22 %** | 12 % | 95 % / 58 % | **+6,5 %** |
| Cubo de 8 m | 24 % | 19 % | 99,7 % / 92 % | +7,8 % |

**Robustez.** Las cuatro variantes (alineación de los residuos ±1 fila y posición alternativa de la Cámara de Belzoni) dan entre el 23 % y el 26 % del volumen excluido al 95 % para la cámara tipo Rey. Ese rango incluye todas las posiciones; el 22 % del cuadro solo cuenta las cajas que caben enteras. La parte excluida fuera del cono va del 8 % al 9 % del volumen exterior al cono.

### El mejor "candidato" no es una cámara
| Variante | Posición del mínimo (x, y, z) | Δχ² |
|---|---|---|
| Nominal | (16, 40, 84) m | −12,2 |
| Residuos desplazados una fila al norte | (−24, −16, 36) m | −10,4 |
| Residuos desplazados una fila al sur | (40, 40, 68) m | −9,7 |
| Cámara de Belzoni en la posición alternativa | (−32, −8, 84) m | −10,7 |

| Hipótesis | Δχ² mínimo | σ local | p global | σ global | Mediana del mínimo en mapas nulos |
|---|---|---|---|---|---|
| Cámara tipo Rey | −12,2 | 3,5 | **0,40** | **0,85** | −11,3 |
| Cubo de 8 m | −12,1 | 3,5 | 0,23 | 1,2 | −9,4 |

En un mapa de residuos con la estructura de los de Alvarez, el mejor candidato **típico** ya tiene Δχ² ≈ −11. El observado es normal. Además cambia de sitio con la alineación, cosa que no haría una cavidad real.

![Exclusión con los datos de Alvarez](../figuras/11_exclusion_datos_alvarez.png)

## 3. Qué cambia respecto a los documentos 18 y 19
- **El 19 % de Alvarez no era un techo, sino una estimación razonable con criterio de exclusión.** Con sus datos reales, al 95 % se excluye el ~22 %. Con criterio de descubrimiento (5σ) baja al 12 %, en línea con la lectura pesimista del documento 18.
- **Hay exploración nueva sin medir nada.** Sus datos cubren al 95 % un 6,5 % adicional del volumen fuera de su cono.
- **Los residuos estructurados producen "candidatos" de ~3,5σ local de forma rutinaria.** Cualquier análisis futuro, incluido uno moderno desde la Cámara de Belzoni (P13), debe calibrar su significación global con nulas que conserven la correlación espacial. Si no, encontrará "cámaras" donde no las hay.

## 4. Límites
- **El modelo de aceptancia es aproximado.** Coincide con la figura 9 dentro de un ~25 % en los bordes, con diferencias mayores en algunos bins del borde este. En la franja de 35–45° esto afecta a la sensibilidad.
- **No se rehace el ajuste de Alvarez.** Su ajuste tenía parámetros libres (una variación norte-sur de sensibilidad, entre otros) que podrían haber absorbido parte de la señal de una cámara grande y difusa. La exclusión supone que la huella de la cámara no se habría absorbido, lo que es razonable para cámaras compactas y optimista para estructuras muy extensas.
- **Los residuos están redondeados a σ enteras.** Al tratarlos como continuos se pierde algo de información.
- **La rejilla es de 8 m**, y las fracciones tienen un error de ~±1–2 puntos.

## Referencias
- Alvarez, L. W. et al. (1970). *Search for hidden chambers in the pyramids*. Science 167, 832–839 (figuras 8–10, p. 836).
