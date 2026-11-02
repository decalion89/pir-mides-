# Resultado de la segunda auditoría aleatoria: el dogma de la escala

Protocolo y muestra registrados antes de leer ningún artículo: [`PROTOCOLO_ESCALA.md`](PROTOCOLO_ESCALA.md) y [`muestra_escala.csv`](muestra_escala.csv), commit `9663ecc`.

**Proceso:**
1. Cribado de los 40 artículos por dos revisores independientes (1–20 y 21–40).
2. Verificación propia: comprobamos en el texto completo descargado que las citas en que se basa cada clasificación existen.

## Resultado
| | k / n | % | IC 95 % (Clopper-Pearson) |
|---|---|---|---|
| **Aplicables** (conclusión sobre un objeto real apoyada en un experimento a otra escala, con transporte, calor o reacción por medio) | **3 / 40** | 7,5 % | 1,6–20,4 % |
| Aplicables contando el caso límite n.º 7 (carbonización de pepitas) | 4 / 40 | 10 % | 2,8–23,7 % |
| **IGNORA Y CAMBIA** entre los aplicables | **0 / 3** | 0 % | 0–71 % |
| IGNORA, NO CAMBIA | 2 / 3 | | |
| LA TRATA | 1 / 3 | | |

| N.º | Artículo | Clase | Motivo |
|---|---|---|---|
| 18 | Paraloid B-72 sobre monedas de bronce (PMC11742038) | IGNORA, NO CAMBIA | Ensayos de 1 h en salmuera. La longitud de transporte es el espesor de la película, igual en el fragmento que en la moneda. Las conclusiones son comparaciones entre tratamientos en el mismo ensayo. Los "dos años" vienen de un envejecimiento real, no extrapolado |
| 38 | Consolidantes de terpenos para la madera de Oseberg (PMC9985608) | IGNORA, NO CAMBIA (límite) | Cubos de 2 cm durante 2 semanas, frente a piezas de 2–15 cm de grosor: factor de Fourier de 1 a 56. El artículo ya reconoce que la penetración en el núcleo es pobre y solo afirma algo cualitativo ("promising"). Si se leyera como "2 semanas bastan", cambiaría para piezas de más de ~3,5 cm |
| 39 | Ondulaciones de travertino y caudal del acueducto Anio Novus (PMC8786873) | LA TRATA | Pasa de las leyes de laboratorio al acueducto mediante el número de Reynolds de cizalla (Re* ≈ 2 565, dentro del intervalo de calibración) |

## Interpretación honesta
- **El dogma de la escala existe, pero en esta muestra es raro.** Solo 3 de cada 40 artículos de arqueología de *Sci. Rep.* hacen una extrapolación de este tipo con un proceso de transporte por medio, y ninguno la hace de forma que cambie su conclusión.
- **Nuestros tres casos anteriores** (Herculano, la cal orgánica y la polianilina) son reales, pero no representativos. Salieron de búsquedas dirigidas, y la muestra aleatoria no los respalda como patrón frecuente.
- **La mayor parte del corpus no puede caer en este error,** porque mide composición, genética, morfometría o fechas en el propio objeto.
- **Con 3 casos aplicables el intervalo de la tasa es enorme** (0–71 %). Lo único firme es que el tipo de artículo vulnerable es poco frecuente (≤ ~20 %).
- **Comparación con la primera auditoría:** el error de ritmo ("ceguera al ritmo") aparece con más frecuencia que el de escala. Entre los artículos con un mecanismo de ritmo, 3 de 7 no superaron la comprobación sin supuestos.
