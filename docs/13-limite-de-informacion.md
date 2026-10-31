# 13 — El límite de la información: qué pueden decir los datos de 2017 y qué no

> **Resumen.** Calculamos la **cota de Cramér–Rao**: la mejor precisión que **cualquier** análisis puede alcanzar con un experimento dado. Sale que los datos completos de 2017, con las dos emulsiones de Nagoya en estéreo, contienen información para fijar la inclinación del Vacío a ±2,5–3,3° **si su forma fuera exactamente un corredor recto**.
>
> Cuando se permite que la forma real difiera (prueba a ciegas con 225 variantes por hipótesis), esos datos eligen la hipótesis correcta el **92 %** de las veces, pero con un margen típico de solo **~3σ**. Con 60 días en la Cámara del Rey, el acierto sube al 98,5 % y el margen a **4,3–9σ**.
>
> **Consecuencia práctica:** antes de medir de nuevo, un **análisis estéreo de los mapas originales de 2017** podría dar ya un indicio fuerte, sin coste.

Archivos:
- código: [`simulador/piramide/cota_informacion.py`](../simulador/piramide/cota_informacion.py), [`simulador/cota_cramer_rao.py`](../simulador/cota_cramer_rao.py), [`simulador/prueba_estereo_2017.py`](../simulador/prueba_estereo_2017.py);
- resultados: [`resultados/12_cramer_rao.json`](../resultados/12_cramer_rao.json), [`resultados/13_estereo_2017.json`](../resultados/13_estereo_2017.json).

## 1. La cota
Para datos de recuento con valor esperado μ_i(θ), la información de Fisher es

F_jk = Σ_i ∂_j μ_i · ∂_k μ_i / (μ_i + (f·μ_i)²).

Ningún estimador insesgado puede tener una varianza menor que (F⁻¹)_jj. Es un límite del **experimento**, no de un análisis concreto.

- **Parámetros del Vacío**: y, z, longitud, alto, ancho e inclinación.
- **Ruidos**, que se marginan: normalización, dos gradientes y dos términos espectrales, con las restricciones de robustez.py.
- **Exposición**: la efectiva (×0,25), con el corte de cenit de 70°.

| Vacío verdadero | 2017: NE1 + NE2 (estéreo) | 2017 + Cámara del Rey 60 d | 2017 + Campbell 7 d |
|---|---|---|---|
| Horizontal | σ(incl.) ≥ 2,5° | ≥ 1,1° | ≥ 2,5° (Campbell no aporta nada) |
| Inclinado 13° | ≥ 3,3° | ≥ 1,6° | ≥ 1,8° |
| Inclinado 26° | ≥ 3,0° | ≥ 1,9° | ≥ 1,9° |

## 2. La realidad: la prueba a ciegas con la configuración estéreo
| Datos | Acierto | Margen mediano (σ): H1 / H2 / H3 / H5 |
|---|---|---|
| 2017 estéreo | 92,5 % | 3,0 / 2,7 / 3,0 / 3,1 |
| 2017 estéreo, flujo −10 % e índice +0,05 | 92,0 % | 2,5 / 2,3 / 2,7 / 3,0 |
| 2017 estéreo, cámaras desplazadas 1 m | 92,0 % | 2,2 / 3,3 / 2,6 / 4,2 |
| 2017 estéreo + Cámara del Rey 60 d | **98,5 %** | **8,0 / 4,3 / 4,6 / 9,2** |

La cota de Cramér–Rao es optimista porque supone que conocemos la familia exacta de formas. La prueba a ciegas, que deja que cada hipótesis se desplace y cambie de sección, da el margen realista: **~3σ con los datos de 2017**.

## 3. Lo que corrige y lo que añade
- **Corrige** nuestras afirmaciones de los docs 08 y 09, según las cuales desde la Cámara de la Reina era "casi imposible" decidir. Allí modelamos **un solo** detector en la Cámara de la Reina. Con la configuración estéreo real de 2017, los datos completos sí apuntarían a la hipótesis correcta en ~9 de cada 10 casos, aunque sin margen suficiente para afirmarlo.
- **Corrige** la recomendación sobre la Cámara de Campbell. Desde ella, un Vacío horizontal se ve casi en horizontal, y con el corte de cenit de 70° no aporta información. **La Cámara del Rey es el puesto robusto.**
- **Añade un paso previo y gratuito**: un análisis estéreo completo de los mapas originales de 2017 (NE1 + NE2), que solo ScanPyramids puede hacer porque solo ellos tienen los datos.

## 4. Por qué no coincide con nuestro reanálisis de las figuras (doc. 11)
Las figuras publicadas resumen los mapas en **4 cortes** de tanθy de 0,25 y en bins de 0,025 en tanθx, y nosotros los leemos en píxeles. Se pierde la mayor parte de la información 2D y de la amplitud absoluta. Además, hay una tensión sin resolver entre KEK y las emulsiones (Δχ² ≈ 78). Por eso nuestro reanálisis no puede alcanzar la cota.
