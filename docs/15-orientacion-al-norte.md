# 15 — ¿Cómo encontraron el norte? (versión 2, revisada)

> ⚠️ **Esta versión sustituye a la anterior.** Una revisión independiente encontró dos errores en la primera:
> 1. usamos fechas comprimidas para las pirámides de Esnofru (la Roja, en el mismo año que Keops);
> 2. no exigimos que las estrellas fueran **visibles**: muchos pares "equivalentes" necesitaban una estrella bajo el horizonte.
>
> Con los datos de la tabla 1 de Spence (2000) y solo alineaciones observables, la conclusión cambia.

> **Resumen (v2).** Las orientaciones de la IV dinastía **derivan con el tiempo**: χ² = 3320 sin deriva.
> - **Sin cambio de configuración**, ningún par de estrellas ni ninguna recta las explica: χ² ≈ 199 con 6 pirámides, por culpa de Kefrén.
> - **Con la regla de Spence**, que permite a Kefrén usar la configuración opuesta, el mejor par dentro de una cronología plausible (±100 años) es **Kochab + Mizar**: χ² = 12,3, con un desfase de **−74 años**, el mismo que publicó Spence. El siguiente par plausible queda a Δχ² ≈ 10.
> - **Pero** una tendencia lineal genérica con Kefrén reflejado ajusta igual (χ² = 11,4), y otro par (η UMa + Kochab) ajusta igual con un desfase de +472 años, que el radiocarbono excluye.
>
> **Conclusión**: los datos son **compatibles** con un método estelar y con el par de Spence, pero no **demuestran** su fecha. Además, el radiocarbono (Bronk Ramsey et al., *Science* 2010: Zoser entre 2691 y 2625 a. C.) solo admite desfases de unos −15 a +51 años, y **la corrección de Spence (−74) cae fuera**. Dentro de esa ventana, el mejor par (β UMa + η Dra) ajusta claramente peor (Δχ² ≈ 10). **La datación astronómica de las pirámides no se sostiene con estos datos.**

Archivos:
- código: [`simulador/piramide/orientacion.py`](../simulador/piramide/orientacion.py), [`simulador/estudio_orientacion.py`](../simulador/estudio_orientacion.py);
- resultados: [`resultados/17_orientacion_pares.json`](../resultados/17_orientacion_pares.json).

## 1. Datos (Spence 2000, tabla 1)
Orientación del **lado este** (positivo es hacia el este). Los lados oeste y este difieren hasta 5,5′ (en la Acodada), así que los errores de ±0,2′ son optimistas. Para Unas, Spence no da margen de error; adoptamos 1′, y la conclusión no cambia con valores razonables. "Con cambio" significa que el código permite a cada pirámide usar cualquiera de las dos configuraciones; en los mejores ajustes solo cambia Kefrén. Fecha de acceso al trono según von Beckerath, con Esnofru según Stadelmann. Se supone que la orientación se hizo en el año 2 del reinado.

| Pirámide | Error | Fecha de la orientación | Años antes (+) o después (−) de Keops |
|---|---|---|---|
| Meidum | −20,6′ ± 1,0 | 2598 a. C. | +46 |
| Acodada | −17,3′ ± 0,2 | 2583 | +31 |
| Roja | −8,7′ ± 0,2 | 2572 | +20 |
| Keops | −3,4′ ± 0,2 | 2552 | 0 |
| Kefrén | −6,0′ ± 0,2 | 2520 | −32 |
| Micerino | +12,4′ ± 1,0 | 2487 | −65 |
| Sahure | −23′ ± 10 | 2444 | −108 |
| Neferirkare | +30′ ± 10 | 2431 | −121 |
| Unas | +17,1′ | 2315 | −237 |

## 2. Método
Para cada par de estrellas (V ≤ 3,5) se calcula el acimut en que **las dos comparten la plomada cerca del norte**, con **ambas al menos a 5° sobre el horizonte**, y cómo cambia con la precesión (IAU 2006) y los movimientos propios. Después se ajusta un desfase de cronología ΔT entre −500 y +500 años, descartando los ajustes que tocan el borde. La incertidumbre de cada fecha se propaga a través de la pendiente de la curva.

En total, 219 pares tienen alineaciones observables cerca del norte.

## 3. Resultados (6 pirámides de la IV dinastía)
| Modelo | χ² | ΔT | Comentario |
|---|---|---|---|
| Sin deriva (constante) | 3320 | — | Descartado: la deriva es real |
| Recta, misma configuración | 199,2 | — | Kefrén no encaja |
| Cualquier par, misma configuración | ≥ 199,2 | — | Ningún par lo arregla |
| η UMa + Kochab, con cambio | 11,8 | +472 | Keops hacia el 3020 a. C.: excluido por el radiocarbono |
| **Kochab + Mizar, con cambio (Spence)** | **12,3** | **−74** | **Keops orientada hacia el 2478 a. C., como Spence** |
| ε UMa + Kochab, con cambio | 17,2 | −462 | Implausible |
| β UMa + η Dra, con cambio | 22,2 | −2 | El siguiente con cronología plausible: Δχ² ≈ 10 peor |
| Recta con Kefrén reflejado | 11,4 | — | Igual de buena que Kochab + Mizar |

## 4. La V dinastía como prueba (retrodicción, no predicción)
Con Kochab + Mizar (ΔT = −74), el modelo da:

| Pirámide | Modelo | Medido | ¿Encaja? |
|---|---|---|---|
| Sahure | ±29′ | −23′ ± 10 | Sí, con la configuración opuesta, como dijo Spence |
| Neferirkare | ±33′ | +30′ ± 10 | Sí |
| Unas | ±68′ | +17,1′ | **No** |

Si el método fue el mismo, **había cambiado hacia la época de Unas**, unos 240 años después de Keops.

*(Una versión anterior de este documento "predecía" para la V dinastía errores de +23′ a +54′. Era incorrecta: esos valores ya estaban publicados en la tabla de Spence y no encajan con aquella extrapolación. La retiramos.)*

## 5. Conclusión honesta
1. La deriva de la orientación es real y apoya un método estelar.
2. Con la regla de cambio de configuración, el par de Spence es el mejor dentro de una cronología plausible, y su fecha (Keops hacia el 2478 a. C.) se reproduce.
3. Pero no queda demostrado: una recta genérica con Kefrén reflejado ajusta igual, y la conclusión depende de aceptar esa regla y la ventana de cronología. **Fechar las pirámides con su orientación sigue siendo una hipótesis, no un resultado.**
