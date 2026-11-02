# 38 — El "filtro de agua más antiguo de América" (Tikal): viable solo con agua remansada delante del filtro

> **Corregido el 01/11/2026 tras una revisión adversaria independiente. Este caso deja de ser un fallo.** La primera versión exigía tratar el 90 % de **toda** la escorrentía, que es ~3,7 veces el embalse. Basta con tratar el volumen del embalse, 58 000 m³ al año. También suponía, sin decirlo, que no había agua almacenada delante del filtro. Recalculado:
> - **Sin agua almacenada delante:** con filtración lenta harían falta **~550–2 300 m²**, según las horas de lluvia al año (600 a 150; ~1 070 m² con 300 h), y **~660–2 800 t** de material traído desde 30 km. En una parte de los casos la escorrentía anual ni siquiera llega al volumen del embalse.
> - **Con agua remansada delante del filtro** (los muros de piedra seca del propio esquema la retendrían) y filtrado continuo durante la estación de lluvias (120–180 días): bastan **~34–200 m²**. Es plausible.
> - **Conclusión revisada:** el filtro lento que elimina microbios es viable si el agua se remansaba antes de pasar por él. Si el agua le llegaba directamente con cada aguacero, no lo es. Además, el propio artículo ya distingue el cuarzo, que solo aclara, de la zeolita, que adsorbe; esa distinción no es nuestra.
> - **Argumento a favor del escepticismo, solo cualitativo:** un filtro lento depende de una capa biológica que muere si el filtro se seca, y en un clima con estación seca larga se secaría cada año.
>
> El texto que sigue es la versión original, con el objetivo del 90 % de la escorrentía, y se conserva como registro.

> **El artículo.** Tankersley et al. (*Sci. Rep.* 10:18021, 2020) tuvo eco mundial. Según los autores:
> - *"the drinking water in the Corriental reservoir water was filtered through a mixture of zeolite and coarse, sand-sized crystalline quartz"*;
> - la zeolita *"removes harmful microbes as well as dispersed insoluble and soluble toxins"*;
> - el filtro es un **"Hypothetical scheme"**: material *"held behind dry-laid stone walls"*, *"just upstream of, or within the reservoir ingresses"*, *"periodically ejected into the reservoir during flash floods"*;
> - el material venía de una toba a **~30 km**;
> - el embalse tiene ~58 000 m³.
>
> El artículo no da ni el área del filtro ni la cuenca.
>
> **La pregunta de ritmo:** ¿cuánta agua puede pasar por un filtro así? La eliminación de microbios exige filtración **lenta**, a 0,1–0,4 m/h, y la escorrentía tropical llega en aguaceros.
>
> **Resultado** (lluvia horaria estocástica de 1 500 mm/año; cuenca de 5–50 ha; escorrentía del 30–70 %):
> - **Un filtro lento del tamaño de una entrada (50 m²) trata el 2 % del agua (0,7–8 %).** El resto lo desborda.
> - **Tratar el 90 % exige ~6 300 m² de filtro** (1 300–17 000). Eso supone **~7 500 t** de zeolita y cuarzo (1 650–20 800) traídas desde 30 km, y vueltas a traer tras cada riada que lo arrastrara. Una obra así habría dejado una huella arqueológica enorme, y no se conoce.
> - **Un filtro rápido sí sería viable:** ~220 m², ~250 t. Pero solo aclara el agua; no elimina microbios ni compuestos disueltos de forma eficaz.
>
> **Conclusión.** La zeolita en los sedimentos es un dato. Un filtro de entrada para **aclarar** el agua es plausible. Que **purificara** el agua del embalse, eliminando microbios y tóxicos, no lo es por caudal. Además, el agua quedaba meses almacenada al aire libre después de entrar, y allí se volvería a contaminar.

Archivos: [`simulador/tikal_filtro.py`](../simulador/tikal_filtro.py), [`resultados/47_tikal_filtro.json`](../resultados/47_tikal_filtro.json).

## Modelo
- **Lluvia:** 1 500 mm/año repartidos en 300 horas de lluvia, con intensidades exponenciales (media de 5 mm/h).
- **Escorrentía:** C·i·A, con C = 0,3–0,7 y A = 5–50 ha. Da 50 000–420 000 m³/año, es decir, 1–7 veces el volumen del embalse.
- **Filtro de área A_f:** pasa como mucho v·A_f por hora. El exceso lo desborda.
- **Velocidades:** v = 0,1–0,4 m/h para la filtración lenta de arena, la que elimina patógenos por la capa biológica; v = 5–10 m/h para la filtración rápida, que solo clarifica.
- **Masa:** área × 0,5–1 m de lecho × 1,6 t/m³.

## Resultados
| | Filtro lento | Filtro rápido |
|---|---|---|
| Fracción tratada con 50 m² | **1,8 %** (0,7–8,1 %) | 41 % (22–89 %) |
| Área para el 90 % | **6 300 m²** (1 340–16 800) | 220 m² (53–460) |
| Material desde 30 km | **7 500 t** (1 650–20 800) | 245 t (62–610) |

## Qué es nuevo y qué no
- **No es nuevo:** las dudas generales sobre el "primer filtro". Solo hemos encontrado comentarios de blogs.
- **No lo hemos encontrado publicado (búsqueda del 01/11/2026):**
  - el límite de caudal;
  - el área y la masa necesarias;
  - la distinción entre aclarar y purificar según la velocidad de filtración.

## Límites
- **La cuenca y la lluvia horaria** son intervalos típicos de la zona, no datos del artículo.
- **La eliminación de microbios en filtros naturales de zeolita** podría tolerar velocidades algo mayores que las de un filtro lento de arena. Aun con 1 m/h, el área necesaria sería de miles de m².
