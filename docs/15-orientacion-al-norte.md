# 15 — ¿Cómo encontraron el norte? Y por qué las estrellas no pueden fechar las pirámides

> **Resumen.** Las pirámides de la IV dinastía están orientadas al norte con errores de solo unos minutos de arco, y esos errores **derivan con el tiempo**: de −20′ en Meidum a +12,4′ en Micerino. Spence (*Nature* 2000) lo atribuyó al "tránsito simultáneo" de Kochab y Mizar, y dedujo que la cronología convencional debía retrasarse ~100 años.
>
> Reproducimos su resultado (−92 a −102 años) y después ajustamos **todos los pares** de estrellas brillantes circumpolares, 92 en total:
> - **15 pares ajustan igual de bien** (Δχ² < 2,3);
> - **cada uno implica un desfase de cronología distinto, de −228 a +132 años**;
> - una simple tendencia lineal ajusta igual de bien que cualquier par;
> - Kochab–Mizar queda en el puesto 27.
>
> **Conclusión**: la deriva apunta a un método estelar, pero **los datos no identifican las estrellas ni pueden fechar las pirámides**. La corrección de la cronología egipcia propuesta a partir de estas orientaciones no está justificada.

Archivos:
- código: [`simulador/piramide/orientacion.py`](../simulador/piramide/orientacion.py), [`simulador/estudio_orientacion.py`](../simulador/estudio_orientacion.py);
- resultados: [`resultados/17_orientacion_pares.json`](../resultados/17_orientacion_pares.json).

## 1. Datos
Errores de orientación de Spence (2000), recogidos en Magli (arXiv:physics/0407108). Positivo es hacia el este.

| Pirámide | Error | Inicio aproximado (cronología convencional) |
|---|---|---|
| Meidum | −20′ ± 1 | ~2600 a. C. |
| Acodada | −17,3′ ± 0,2 | ~2595 |
| Roja | −8,7′ ± 0,2 | ~2585 |
| Keops | −3,4′ ± 0,2 | ~2585 |
| Kefrén | −6,0′ ± 0,2 | ~2555 |
| Micerino | +12,4′ ± 1 | ~2530 |

## 2. Modelo
Para cada par de estrellas (A, B) y cada año:
- calculamos el instante en que A y B tienen el mismo acimut cerca del norte, es decir, cuando una plomada las cubre a la vez;
- ese acimut común es el error de orientación;
- cada día hay dos configuraciones, A encima o B encima, que dan errores de signo opuesto.

Se ajusta un desfase de cronología ΔT, propagando la incertidumbre de la fecha de cada pirámide a través de la pendiente de la curva. El ajuste se hace con dos reglas:
- la misma configuración para todas las pirámides;
- o permitiendo que cada pirámide use la configuración que mejor encaje, como hizo Spence para explicar Kefrén.

**Validación**: con Kochab–Mizar obtenemos ΔT = −92 a −102 años, la misma corrección que publicó Spence (Keops hacia 2467–2480 a. C.).

## 3. Resultados
| Modelo | χ² (6 pirámides) | Desfase de cronología |
|---|---|---|
| Mejor par (ψ UMa + γ UMa) | 28,1 | +76 años |
| Phecda + Megrez (Belmonte 2001) | 28,1 | −12 años |
| ζ Dra + δ Cyg | 28,4 | −228 años |
| Kochab + Mizar (Spence 2000) | 39,1 (puesto 27 de 92) | −92 años |
| Tendencia lineal cualquiera | 25,9 | — |
| Constante, sin deriva | 3306 | — |

Con cambio de configuración permitido, 22 pares quedan a Δχ² < 2,3 del mejor, con ΔT entre −238 y +250 años. La tendencia lineal, con Kefrén reflejado, da χ² = 8,6.

## 4. Interpretación
1. **La deriva es real y fuerte**: χ² = 3306 sin deriva frente a ~26 con ella. Un método solar como el del equinoccio (Dash) no produce esa deriva secular, así que esto apoya el uso de estrellas circumpolares. También cabe un método solar con un sesgo que cambiara con la práctica de cada generación de constructores, pero no hay pruebas de ello.
2. **Las estrellas concretas no se pueden identificar**: cualquier par circumpolar genera una deriva casi lineal de ~0,3–0,5′ por año en esa época, y el punto de cruce depende del par.
3. **No se puede fechar con este método**: el desfase ΔT abarca más de 350 años según el par elegido. Para fechar haría falta saber, por otra vía, qué estrellas usaron; por ejemplo, un texto.
4. **Kefrén sigue siendo una anomalía**: hace falta una configuración opuesta o una medición revisada.

## 5. Predicción comprobable (P11)
Si la deriva continuó en la V dinastía con la misma práctica, las pirámides siguientes deberían tener errores de este orden:

| Pirámide | Inicio aproximado | Error predicho |
|---|---|---|
| Userkaf | ~2494 a. C. | **+23′ a +31′** |
| Sahure | ~2487 | **+25′ a +34′** |
| Neferirkare | ~2475 | **+29′ a +40′** |
| Niuserre | ~2445 | **+38′ a +54′** |

Mediciones modernas y precisas de estas pirámides, de la calidad de las de Dash en Giza, confirmarían o refutarían que fue el mismo método.
