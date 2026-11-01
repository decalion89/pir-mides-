# 39 — El mercurio de los embalses de Tikal no hacía el agua imbebible

> **El artículo.** Lentz et al. (*Sci. Rep.* 10:10316, 2020) tuvo eco mundial y lo vincularon al abandono de Tikal. Hallan mercurio en los sedimentos de los embalses del Templo y del Palacio: 25 muestras superan el *"toxic effect threshold (TET) … 1.0 µg/g"* y 5 lo superan más de 10 veces. El mercurio viene sobre todo del **cinabrio (HgS)** de pinturas y rituales. Concluyen que los embalses estaban *"seriously compromised as sources of drinking water"* y que la élite *"likely were fed foods laced with mercury at every meal"*.
>
> **El paso que falta.** El TET es un umbral para **organismos que viven en el sedimento**, no para el agua de beber. Además, el HgS es prácticamente insoluble. La pregunta es cuánto mercurio pasa del sedimento al agua y de ahí a quien la bebe.
>
> **Resultado** (Monte Carlo, 200 000 casos):
> - **Hipótesis generosas:** el mercurio disuelto se reparte según el coeficiente sedimento-agua (log Kd = 4,5–6); se añaden las partículas en suspensión (5–100 mg/L); se beben y cocinan 3–5 L al día; y se trata todo el Hg como si fuera tan absorbible como el inorgánico soluble.
> - **Con las muestras más contaminadas** (10–30 µg/g), el agua tiene **1,0 µg/L** de Hg (0,26–2,4). Es el **17 %** de la guía de la OMS para agua potable (6 µg/L), y **ningún caso la supera**. La ingesta es el **3 %** de la tolerable de la OMS (máximo 8 %).
> - **Con el sedimento típico por encima del TET** (1–10 µg/g), el agua tiene 0,17 µg/L: el 3 % de la guía y el 0,6 % de la ingesta tolerable.
>
> **Conclusión.** Por mercurio, el agua habría cumplido la norma actual de la OMS para agua potable. Que un sedimento supere un umbral ecológico no convierte el agua en veneno. Las otras pruebas del artículo son independientes del mercurio y pueden seguir siendo válidas: las cianobacterias productoras de microcistinas y los fosfatos.

Archivos: [`simulador/tikal_mercurio.py`](../simulador/tikal_mercurio.py), [`resultados/48_tikal_mercurio.json`](../resultados/48_tikal_mercurio.json).

## Qué queda fuera, y podría cambiar algo
- **Metilmercurio en peces.** En un embalse con materia orgánica, parte del Hg inorgánico se metila y se acumula en los peces. Si la élite comía peces de esos embalses, esa vía podría ser relevante. El artículo no la plantea ni la mide.
- **Las cianobacterias** (*Planktothrix*, *Microcystis*) son un argumento distinto, basado en ADN, y podrían bastar por sí solas para hacer el agua peligrosa. No las evaluamos aquí.

## Qué es nuevo y qué no
- **No es nuevo:** los datos de sedimento y la discusión de si esos embalses se usaban para beber. En la nota de prensa de la universidad los autores dicen que es "possible but unlikely" que se bebiera de ellos, mientras que el artículo afirma que el agua de la élite "almost certainly came from" esos embalses.
- **No lo hemos encontrado publicado (búsqueda extendida del 01/11/2026):** una estimación de la concentración en el agua y de la dosis, comparada con la guía y la ingesta tolerable de la OMS.

## Límites
- **El Kd del mercurio** depende de su especie química y del carbono orgánico. Usamos un intervalo amplio, y el término de las partículas en suspensión, que es el que domina, no depende de él.
- **Las muestras más altas no están acotadas por arriba en el texto principal.** Con 100 µg/g el agua llegaría a ~3–8 µg/L, cerca de la guía. Con la información del artículo, eso sería un caso extremo, no la norma.
