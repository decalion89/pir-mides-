# 26 — El límite físico del método del gnomon

> **Pregunta.** ¿Pudieron orientarse todas las pirámides con el sol, marcando la sombra de un palo a la misma longitud por la mañana y por la tarde (el "círculo indio")? Glen Dash (2017) propuso este método, en otoño, para Keops.
>
> **Respuesta.** El único error sistemático del método procede del cambio de declinación del sol entre las dos observaciones, y **en Giza no puede superar ~5,8′**: es máximo cerca de los equinoccios y crece un poco cuanto más bajo está el sol al observar. Solo **Keops (−3,4′)** y, justo en el límite, **Kefrén (−6,0′)** caen dentro. **La Roja (−8,7′), la Acodada (−17,3′), Meidum (−20,6′), Micerino (+12,4′) y las de la dinastía V (17–30′) no** pueden explicarse con ese error sistemático.
>
> **Consecuencia.** El gnomon no puede ser el **único** método de toda la serie, salvo que los errores de ejecución fueran de 10–30′. En ese caso, la precisión de Keops sería en parte suerte. Lo que encaja es o bien un **método estelar**, cuyo error cambia con la precesión y explica la deriva del documento 15, o bien un **cambio de método o una mejora clara de la técnica entre la pirámide Roja y Keops**, justo cuando la precisión salta de −8,7′ a −3,4′.

Archivos: [`simulador/metodo_gnomon.py`](../simulador/metodo_gnomon.py), [`resultados/32_metodo_gnomon.json`](../resultados/32_metodo_gnomon.json).

## Método
- **Posición del sol:** declinación con la serie de Spencer, que varía de forma continua a lo largo del día, y latitud de Giza (29,98° N).
- **Simulación del método:** para cada día del año y cada altura del sol al observar (15° a 60°), se buscan los dos instantes en que el sol tiene esa altura y se toma la bisectriz de las dos sombras.
- **Error:** la desviación de esa línea respecto al meridiano (+ = el extremo norte va hacia el este).
- **Comprobación:** en otoño el error sale hacia el oeste (−5,7′ a 15° de altura el 22 de septiembre) y en primavera hacia el este, como encontró Dash. Keops se reproduce, por ejemplo, observando a 15–20° de altura a finales de julio.

## Resultados
| Altura del sol al observar | Error máximo (en el equinoccio) |
|---|---|
| 15° | 5,8′ |
| 30° | 5,1′ |
| 45° | 4,6′ |
| 60° | 4,3′ |

| Pirámide | Error medido (Spence 2000) | ¿Dentro del límite del gnomon? |
|---|---|---|
| Keops | −3,4′ | Sí |
| Kefrén | −6,0′ | En el límite |
| Roja | −8,7′ | No |
| Acodada | −17,3′ | No |
| Meidum | −20,6′ | No |
| Micerino | +12,4′ | No |
| Sahure / Neferirkara / Unas | −23′ / +30′ / +17,1′ | No |

## Límites
- **Solo se modela el error sistemático** del método. Los errores de ejecución (penumbra de la sombra, verticalidad del palo, trazado de la bisectriz y su traslado a la obra) se suman y podrían ser mayores. Pero si fueran de 10–30′, la precisión de 3′ de Keops sería difícil de explicar sin suerte.
- **Con alturas por debajo de 15°** el límite crece un poco, aunque la sombra se vuelve muy larga y difusa.
- **Hay otras variantes solares** (orto y ocaso en el equinoccio, sombra de mediodía) con errores distintos; no se han modelado aquí.
- **El resultado no elige un método**, pero sí descarta que el gnomon por sí solo explique la serie completa.
