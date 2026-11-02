# 24 — ¿Hay algo más en los datos de 2017 además del Gran Vacío?

> **Pregunta.** Todos los análisis de los datos de KEK de 2017 (los 679 puntos de la figura 4 de datos extendidos de Morishima et al.) se han centrado en el Gran Vacío. Hasta donde sabemos, nadie ha publicado una búsqueda de **otra** señal en lo que sobra después de restarlo. Es la idea de los "8 minutos de arco" de Kepler: mirar lo que el mejor modelo no explica.
>
> **Respuesta: no hay una segunda anomalía.**
> - El exceso más fuerte está en el detector H2, en 6 puntos seguidos (tanθx ≈ 0,20–0,25; tanθy ≈ 0,48–0,64), con una significación global p = 0,031.
> - Contando que se buscaron excesos y déficits, queda en ≈ 1,9σ.
> - Sobre todo, **el otro detector (H1), 2,9 m al este, no lo confirma** en la dirección que correspondería por paralaje, para ninguna distancia supuesta del objeto (de −0,5 a +1,5 frente a ~5 en H2). Un hueco real lo verían ambos.
> - El déficit más fuerte no es significativo (p = 0,66).

Archivos: [`simulador/anomalias_kek.py`](../simulador/anomalias_kek.py), [`resultados/29_anomalias_kek.json`](../resultados/29_anomalias_kek.json).

## Método
1. **Ajuste de partida:** el mejor ajuste del Gran Vacío a los datos de KEK (corredor inclinado 26°, con la posición del detector libre; doc. 11).
2. **Residuos:** r = (dato − ajuste)/σ, donde σ incluye el error estadístico y un 0,5 % de sistemático.
3. **Máscara del artefacto en cruz** del hodoscopio, que el propio artículo de 2017 describe: |Δx| ≤ 2 canales. Quedan 639 puntos.
4. **Búsqueda:** máximo de Σr/√n en ventanas de 3 a 10 puntos consecutivos de cada corte, para excesos y déficits por separado.
5. **Hipótesis nula:** un proceso AR(1) gaussiano por corte, con la autocorrelación (0,09) y la dispersión (1,24) observadas. Se hacen 5 000 simulaciones y el valor p es global (todas las posiciones, anchuras y cortes).
6. **Robustez:** quitar el primer corte de cada detector, donde cae la rama Δy = 0 del artefacto, no cambia el resultado.
7. **Prueba de paralaje:** para cada distancia supuesta del candidato, se mira la dirección correspondiente vista desde H1.

## Resultados
| | Valor | p global | Detector | tanθx | tanθy |
|---|---|---|---|---|---|
| Exceso más fuerte | 5,46 | 0,031 | H2 | 0,20–0,25 | 0,48–0,64 |
| Déficit más fuerte | 4,09 | 0,66 | H2 | 0,43–0,45 | 0,16–0,32 |
| Mediana / percentil 95 / percentil 99 del máximo nulo (excesos) | 4,29 / 5,31 / 5,85 | | | | |

**Paralaje.** Si el candidato estuviera a 20, 30, 40 o 50 m por encima de H2, H1 lo vería con una suma normalizada de −0,5, +1,5, +0,7 o +0,1. En H2, los cortes vecinos dan +2,4 (el de encima) y −0,5 (el de debajo). La señal es propia de H2 y de dos cortes contiguos, compatible con una fluctuación o con un sistemático de ese detector.

## Qué significa
- Los datos de KEK de 2017, tal como se publicaron, **no contienen una segunda estructura detectable** además del Gran Vacío en la zona que cubren (por encima de la Cámara de la Reina, |tanθ| ≲ 0,8–1,2).
- Concuerda con el documento 17: esa zona ya es de las mejor exploradas de la pirámide. Lo que queda por explorar está en la base, que KEK no ve.

## Límites
- Los datos son una digitalización de la figura publicada, no los mapas originales.
- La búsqueda es en una dimensión, a lo largo de cada corte. Una estructura alargada en la dirección de Δy repartiría su señal entre cortes y se vería peor.
- No se han incluido aquí los perfiles de las emulsiones de Nagoya, que cubren la misma zona con otra geometría.
