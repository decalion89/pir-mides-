# Datos digitalizados de ScanPyramids (2017)

Proceden de las figuras del artículo:

> K. Morishima et al., *Discovery of a big void in Khufu's Pyramid by observation of cosmic-ray muons*, **Nature** 552, 386–390 (2017). Versión de arXiv: [1711.01576](https://arxiv.org/abs/1711.01576).

| Archivo | Figura | Método |
|---|---|---|
| `kek_cortes.csv` | Extended Data Fig. 4 (hodoscopios de KEK, posiciones H1 y H2) | Vectores del PDF, con [`simulador/extraer_datos_kek.py`](../../simulador/extraer_datos_kek.py) |
| `emulsiones_diferencias.csv` | Extended Data Fig. 2 (emulsiones de Nagoya, NE1 y NE2) | Imagen rasterizada, con [`simulador/extraer_datos_emulsiones.py`](../../simulador/extraer_datos_emulsiones.py) |

Son **lecturas de figuras**, no los datos originales. Pueden contener errores de digitalización:
- en las emulsiones hay que elegir, en cada bin, entre la cruz de datos y la curva ajustada (ver docs/11, §4);
- los valores de las emulsiones están en píxeles: solo valen para comparar formas y posiciones de picos.

Todo el mérito de las mediciones es de los equipos de Nagoya, KEK y CEA.
