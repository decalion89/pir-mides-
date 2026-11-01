# 33 — ¿A cuántos metros de piedra está el Gran Vacío de un espacio accesible?

> **Pregunta.** En 2023 el corredor de la cara norte pasó de ser una señal de muones a una imagen real gracias a un endoscopio de 5 mm metido por una junta entre piedras. ¿Se podría hacer lo mismo con el Gran Vacío? ¿Desde dónde, y cuánta piedra habría que atravesar?
>
> **Respuesta.**
> 1. **Ningún espacio accesible está a menos de 5 m del Vacío** con una probabilidad apreciable: como mucho un 15 %, según el conjunto de datos. **Una confirmación con endoscopio como la del corredor norte no es posible** desde los espacios conocidos. Habría que perforar ≥ 5–10 m, y Egipto descartó en 2017 cualquier técnica intrusiva.
> 2. **El espacio accesible más cercano, de forma robusta, es la pared norte de las dos cámaras de descarga superiores** (la 4.ª, de Lady Arbuthnot, y la 5.ª, de Campbell), en su extremo este:
>    - mediana de **7–8 m de piedra**;
>    - a menos de 10 m con una probabilidad del **86–99,8 %** en los tres análisis (emulsiones, KEK y conjunto).
>
>    Es el único punto en que coinciden los tres conjuntos de datos, que discrepan entre sí (docs. 11 y 32).
> 3. **El techo de la Gran Galería**, que sería el sitio "obvio", no es robusto: según KEK el Vacío está a ~7 m, pero según las emulsiones a ~12 m (solo un 17 % de probabilidad de estar a menos de 10 m).
> 4. **Hallazgo de método:** los datos publicados que hemos extraído **solo miran hacia el norte** (tanθy ≥ 0 en las emulsiones y en los cortes de KEK). El extremo sur del Vacío no lo fijan esos datos, sino la frase del artículo *"the structure starts almost at the centre of the Pyramid"*, sacada de la imagen 2D de KEK.
>    - Sin esa información previa, el resultado lo domina la suposición sobre la longitud, y el Vacío parece llegar "a 3 m de la cámara de Campbell".
>    - Con ella, el extremo sur queda en **y ≈ −1 m** (de −4,7 a +1,9 m), justo donde termina la Gran Galería (y = −0,6 m).

Archivos:
- código: [`simulador/acceso_gran_vacio.py`](../simulador/acceso_gran_vacio.py);
- resultados con la información del artículo sobre el extremo sur: [`resultados/41_acceso_gran_vacio.json`](../resultados/41_acceso_gran_vacio.json) y las muestras en [`resultados/41_muestras_gran_vacio.npz`](../resultados/41_muestras_gran_vacio.npz);
- resultados sin esa información (dominados por la suposición previa): [`resultados/41_acceso_gran_vacio_sur_libre.json`](../resultados/41_acceso_gran_vacio_sur_libre.json).

## Método
1. **Posteriores de la geometría del Vacío:** corredor recto con x, y, z, largo, alto, ancho e inclinación. Se obtienen con Metropolis adaptativo (9 000 pasos, 2 500 de calentamiento) sobre tres conjuntos de datos:
   - las emulsiones solas;
   - KEK sola;
   - el ajuste conjunto.

   Los datos son los publicados en 2017 (doc. 11), con los errores reescalados.
2. **Información previa:**
   - límites amplios en todos los parámetros;
   - el extremo sur, en y ∈ [−5, +5] m, por la frase del artículo;
   - el Vacío no puede cortar ningún espacio conocido, porque se habría visto.
3. **Espacios accesibles:** la Gran Galería, la antecámara, la Cámara del Rey y las cinco cámaras de descarga. Todas son accesibles por los túneles de Davison (1765) y Vyse (1837).
4. **Distancia:** para 1 500 muestras de cada posterior, se calcula la distancia mínima entre la superficie del Vacío (puntos cada 0,5 m) y cada espacio. Además, para puntos concretos (el techo de la galería cada metro y la pared norte de las cámaras de descarga), la probabilidad de que el Vacío esté a menos de ℓ metros.

## Resultados (con la información del artículo sobre el extremo sur)
Piedra entre el Vacío y cada espacio: mediana (intervalo del 90 %) y probabilidad de que sea menos de 5 m y de 10 m.

| Espacio | Emulsiones | KEK | Conjunto |
|---|---|---|---|
| Techo de la Gran Galería | 12,0 m (8,5–15,1); 0 % / 17 % | **7,0 m** (3,4–9,9); 15 % / 96 % | 9,7 m (7,3–11,5); 0 % / 61 % |
| Cámara de descarga 4 | 7,9 m (4,8–11,0); 7 % / 86 % | 7,7 m (5,0–9,1); 5 % / **99,8 %** | 8,0 m (5,9–9,4); 2 % / 99 % |
| Cámara de descarga 5 (Campbell) | **7,3 m** (4,2–10,5); 15 % / 90 % | 8,0 m (5,2–9,5); 4 % / 98 % | 8,0 m (6,0–9,3); 2 % / **99,8 %** |
| Cámara del Rey | 15,6 m | 13,5 m | 14,5 m |

**Geometría según cada conjunto** (mediana; intervalo del 90 %):

| | Emulsiones | KEK | Conjunto |
|---|---|---|---|
| Altura del centro (z) | 62,2 m (60,2–64,1) | 50,4 m (45,8–55,3) | 54,0 m (49,1–57,6) |
| Inclinación | 10° (−1 a 21) | 25° (14 a 34) | 21° (11 a 29) |
| Longitud | 35 m (30–38) | 53 m (29–72) | 47 m (30–71) |
| Extremo sur (y) | −1,6 m (−4,7 a 1,9) | −1,0 m (−4,0 a 0,1) | −0,8 m (−3,1 a 0,4) |

## Qué significa
- **Confirmar el Vacío "a la vista", como el corredor norte, no es viable con los espacios accesibles hoy.** Lo protegen al menos 5 m de piedra por todos los lados accesibles. Eso explica, de paso, por qué en 2017 se habló de perforar y no de buscar una junta.
- **El mejor puesto no intrusivo para una nueva medición son las cámaras de descarga superiores:** a ~8 m del Vacío, a su misma altura y con distancia robusta frente a la discrepancia entre conjuntos. Es coherente con el doc. 08, que ya proponía la Cámara de Campbell y la del Rey (P1/P2), y lo cuantifica. *Matiz del doc. 13:* si el Vacío es horizontal, desde Campbell se ve casi de lado, cerca del corte de cenit. La Cámara del Rey sigue siendo el puesto más robusto para distinguir la forma.
- **El extremo sur del Vacío coincide con el final de la Gran Galería** (y ≈ −1 frente a −0,6 m). Es compatible con un espacio que acompaña a la galería en toda su longitud, como un hueco de descarga o de construcción. Pero esta coincidencia depende de la frase del artículo y de la ventana hacia el norte de los datos: es sugerente, no una prueba.

## Límites
- **El extremo sur es información del artículo,** no un ajuste: depende de una frase cualitativa.
- **Corredor recto.** Si el Vacío está formado por varias estructuras, las distancias pueden ser menores en algún punto.
- **Datos leídos de las figuras** y tensión entre conjuntos sin resolver (doc. 32). Por eso se dan los tres posteriores por separado.
- **Geometría aproximada de los espacios conocidos** (±0,3–1 m).
