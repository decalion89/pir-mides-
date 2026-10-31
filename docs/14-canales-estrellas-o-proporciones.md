# 14 — Los canales de la Gran Pirámide: ¿estrellas o proporciones?

> **Resumen.** Recalculamos con astronomía de precisión a qué estrellas apuntaban los cuatro canales de la Gran Pirámide y en qué fecha. Usamos el catálogo de Yale con movimientos propios, la precesión IAU 2006 y la refracción. Encontramos tres cosas:
> 1. **Las fechas de alineación no coinciden entre sí ni con el reinado de Keops.** Alnitak da 2497 ± 41 a. C. y Thuban 2338 ± 53 a. C., una diferencia de 2,4σ entre los dos canales mejor medidos. Thuban queda a 4,7σ del reinado (~2589–2566 a. C.).
> 2. **La alineación simultánea con cuatro estrellas no es significativa.** Con la misma tolerancia, cuatro ángulos al azar la consiguen el 59 % de las veces.
> 3. **Los cuatro ángulos encajan con pendientes n/11** (7/11, 9/11 y 11/11), el mismo denominador que la cara de la pirámide (14/11). Si ese denominador se fija de antemano a partir de la cara, la probabilidad de que sea casualidad es del 1,3 %. Si se busca el mejor entre 5 y 16, es del 16 %: sugerente, no demostrado.
>
> Proponemos una medición que distingue entre estrellas y proporciones en el tramo no medido del canal norte de la Cámara de la Reina.

Archivos:
- código: [`simulador/piramide/astronomia.py`](../simulador/piramide/astronomia.py), [`simulador/estudio_canales.py`](../simulador/estudio_canales.py), [`simulador/estudio_pendientes.py`](../simulador/estudio_pendientes.py);
- resultados: `resultados/14_canales_estelares.json`, `15_pendientes_canales.json`, `16_angulos_predichos_estrellas.json`;
- catálogo: [`datos/estrellas/bsc5.dat.gz`](../datos/estrellas) (Yale BSC5, Hoffleit & Warren 1991, vía Harvard TDC).

## 1. La hipótesis
Trimble y Badawy (1964) propusieron que los canales de la Cámara del Rey apuntaban:
- al sur, a Orión (Osiris);
- al norte, a las estrellas circumpolares "imperecederas".

Bauval (1993) añadió los de la Cámara de la Reina:
- al sur, a Sirio (Isis);
- al norte, a Kochab.

Y fechó las cuatro alineaciones hacia el 2450–2475 a. C.

## 2. Método
- **Datos**: ángulos medidos por Gantenbrink con el robot Upuaut, con su incertidumbre (1σ):

| Canal | Ángulo | σ |
|---|---|---|
| Rey sur | 45,0° | 0,2° |
| Rey norte | 32,6° | 0,3° |
| Reina sur | 39,61° | 1° (él declaró ±2°) |
| Reina norte | ~39,1° | 1,5° (estimado) |

- **Cálculo**:
  - movimiento propio lineal y precesión IAU 2006;
  - paso por el meridiano en Giza (φ = 29,979°), con refracción.
- **Validación**: Thuban sale como estrella polar hacia el 2800 a. C. (δ = 89,90°), como se conoce.

## 3. Fechas en que cada estrella culminaba a lo largo de su canal
| Canal | Estrella | Fecha |
|---|---|---|
| Rey sur | Alnitak (ζ Ori, V = 2,05) | **2497 ± 41 a. C.** |
| Rey norte | Thuban (α Dra, V = 3,65) | **2338 ± 53 a. C.** (o 3257 a. C.) |
| Reina sur | Sirio | 2369 ± 333 a. C. |
| Reina norte | Kochab (β UMi) | 2369 ± 446 a. C. |

Reinado de Keops: ~2589–2566 a. C. (cronología convencional). La fecha de Alnitak coincide con la datación astronómica de Spence (*Nature* 2000), unos 2480 a. C., pero la de Thuban no coincide con ninguna.

## 4. ¿Podría ser casualidad?
- **Hay muchas estrellas candidatas.** Entre 2700 y 2400 a. C. encajan con el canal sur del Rey 5 estrellas de V ≤ 3: Mintaka, Alnilam, Alnitak, ε Sco y λ Sgr. Con el sur de la Reina encajan 11.
- **Monte Carlo.** Se pregunta si existe un año, entre 3500 y 1500 a. C., en que los 4 canales tengan a la vez una estrella de V ≤ límite dentro de su tolerancia:
  - con V ≤ 2,5 o V ≤ 3,0, los ángulos reales **no lo consiguen**, porque al canal norte del Rey no le corresponde ninguna estrella brillante;
  - con V ≤ 3,7, que es lo necesario para incluir a Thuban, sí lo consiguen, **pero también el 59 % de los conjuntos de ángulos al azar**.
- **Conclusión**: la alineación estelar simultánea **no es estadísticamente significativa**.

## 5. Las proporciones de la propia pirámide
La cara de la pirámide sube 14 por cada 11 de avance, que es el seked de 5½ palmos. Los canales:

| Canal | Medido | Pendiente n/11 | Ángulo n/11 |
|---|---|---|---|
| Rey sur | 45,00° | 11/11 | 45,00° |
| Rey norte | 32,47° de media (Gantenbrink) | 7/11 | **32,47°** |
| Reina sur | 39,61° | 9/11 | 39,29° |
| Reina norte | ~39,1° | 9/11 | 39,29° |

En términos egipcios, serían sekeds de 7 palmos, 11 palmos y 8,56 palmos. La probabilidad de que cuatro ángulos al azar (25–50°) encajen así con n/11 es:
- **1,3 %** con el 11 fijado por la cara;
- **16 %** buscando el mejor denominador entre 5 y 16. El 11 y el 14 encajan los dos.

## 6. Veredicto honesto
- **Lo que queda debilitado**: la idea de que los canales se orientaron con precisión hacia cuatro estrellas concretas en la época de Keops. Las fechas no cuadran, y la coincidencia es la que cabe esperar por azar.
- **Lo que gana peso, sin estar demostrado**: que los ángulos salen del sistema de proporciones de la obra (n/11). Eso no excluye un simbolismo general del cielo del norte y del sur.
- **Sigue abierta** la función de los canales y de las "puertas" de la Cámara de la Reina.

## 7. La medición que lo decide (P10)
Un robot que mida con láser el tramo alto del canal norte de la Cámara de la Reina, el que Gantenbrink no pudo recorrer, distinguiría las hipótesis:
- **proporciones (9/11)**: 39,29°;
- **Kochab en el reinado de Keops**: 39,8–39,9°;
- **canal sur de la Reina**: 39,29° (proporciones) frente a 38,9–39,0° (Sirio en el reinado).

Bastaría una precisión de **±0,2°**.
