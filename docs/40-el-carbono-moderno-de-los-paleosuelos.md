# 40 — Paleosuelos del Oligoceno: el carbono moderno está infravalorado entre 3 y 70 veces por un error de unidades

> **Cómo apareció.** Es el artículo n.º 38 de la [muestra aleatoria](../auditoria_aleatoria/PROTOCOLO.md) (corpus de 225 artículos de *Sci. Rep.*, muestra de 40 con semilla fija, protocolo registrado antes de leer ninguno). No lo elegimos nosotros. Lo marcó el cribado, y lo verificamos en la fuente.
>
> **El artículo.** Broz et al. (*Sci. Rep.* 13:7476, 2023, *"Accumulation of radiocarbon in ancient landscapes: A small but significant input of unknown origin"*) estudian paleosuelos de 28–33 millones de años en el este de Oregón. Encuentran radiocarbono (edades aparentes de 11 000–30 000 años) y concluyen, con un modelo de mezcla de dos componentes, que *"modern C may compose ~0.5–2.4% of the total organic C pool"*.
>
> **El error.** Con ese modelo, en el que el carbono viejo está "muerto" (FM ≈ 0, como el propio artículo comprueba con la ordenada en el origen) y el moderno tiene FM ≈ 1, la fracción moderna del carbono orgánico es **FM**. Pero la columna *"Modern C (%)"* de la tabla 2 es exactamente **100 × FM × TOC (wt%)**, con el TOC de la tabla 1. Coincide en las 10 muestras, con diferencias de ≤ 0,03. Esa magnitud no es un porcentaje del carbono orgánico. Tampoco es el porcentaje de la roca, que sería 100 veces menor.
>
> | Muestra | Publicado | 100·FM·TOC | **Fracción moderna real (FM)** | Infravaloración |
> |---|---|---|---|---|
> | Lakim 0 cm | 1,70 % | 1,72 | **5,7 %** | ×3,4 |
> | Lakim 25 cm | 1,56 % | 1,58 | **13,6 %** | ×8,7 |
> | Lakim 100 cm | 2,36 % | 2,39 | **18,1 %** | ×7,7 |
> | Luca 22 cm | 0,32 % | 0,32 | **23,2 %** | ×72 |
> | TC 0 cm | 0,47 % | 0,48 | **2,8 %** | ×6,0 |
> | TC 100 cm | 0,71 % | 0,71 | **6,2 %** | ×8,7 |
>
> Tabla completa en el JSON. **El carbono moderno es el 2,4–23 % del carbono orgánico, no el 0,5–2,4 %.** El título, *"a small but significant input"*, queda corto: en algunas muestras es casi una cuarta parte.
>
> **Consecuencia para el mecanismo.** Los autores atribuyen el aporte sobre todo a la *"infiltration of dissolved organic carbon"*. Corregida, la cantidad que hay que explicar es de ~60–450 g de C moderno por m² en el primer metro (mediana de 160). El carbono disuelto que puede infiltrarse en el tiempo que esa roca ha estado cerca de la superficie (100–400 años, con la erosión de 4,94 mm/año del artículo) da ~4–200 g/m² (mediana de 29). El cociente es de **5,9 en la mediana** (0,6–57). Basta en el 10 % de los casos, y es ≥ 3 en el 69 %. Según el protocolo, el mecanismo queda **CONDICIONAL**: solo funciona si la infiltración, el carbono disuelto y la retención están a la vez en lo alto de sus intervalos, en una ladera sin vegetación de arcillas expansivas, y el artículo no lo justifica.

Archivos: [`simulador/paleosuelo_radiocarbono.py`](../simulador/paleosuelo_radiocarbono.py), [`resultados/49_paleosuelo_radiocarbono.json`](../resultados/49_paleosuelo_radiocarbono.json).

## Qué no se discute
Las medidas de radiocarbono y de carbono orgánico, y la conclusión cualitativa de que hay carbono reciente en rocas muy antiguas. De hecho, la corrección la refuerza: hay más carbono moderno del que dicen.

## Qué es nuevo
- **No hemos encontrado corrección ni comentario publicados** (búsqueda del 01/11/2026 en la revista y en los repositorios de las universidades).
- **El error de la tabla 2** y su efecto en el resumen.
- **El balance de carbono disuelto frente al tiempo de exposición.**

## Límites
- **Si el componente moderno tiene FM > 1** (carbono de las bombas atómicas, ~1,05–1,2), la fracción moderna es FM/1,1, apenas menor. No cambia la conclusión.
- **Los parámetros del aporte de carbono disuelto** (lluvia, infiltración, concentración, retención) son intervalos de la literatura, no medidas del sitio.
