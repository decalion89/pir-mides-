# Resultado del censo de "ceguera al ritmo": el corpus completo (225 artículos)

**Población:** todos los artículos de *Scientific Reports* de 2020–2025 en acceso abierto con "archaeolog*", "ancient", "prehistoric" o "archaeometr*" en el título: 225, según la consulta de Europe PMC de [`PROTOCOLO.md`](PROTOCOLO.md). Cuarenta se revisaron en la primera muestra aleatoria ([`RESULTADO.md`](RESULTADO.md)) y los 185 restantes en este censo ([`PROTOCOLO_CENSO.md`](PROTOCOLO_CENSO.md), registrado antes de leerlos).

**Proceso:**
1. Cribado por cuatro revisores independientes, uno por bloque, con los criterios del protocolo.
2. Verificación propia. Comprobamos las citas en el texto completo y **recalculamos con código propio todos los casos FALLA y CONDICIONAL** ([`simulador/censo/`](../simulador/censo), resultados 52–55). En los casos PASA aceptamos la clasificación tras comprobar las citas.

## Resultado (225 artículos)
| | k / n | % (IC 95 % de Clopper-Pearson) |
|---|---|---|
| **Aplicables**: la conclusión depende de un mecanismo con ritmo físico comprobable | **21 / 225** | **9 %** (6–14 %) |
| **No superan la comprobación** (FALLA + CONDICIONAL) | **9 / 21** | **43 %** (22–66 %) |
| FALLA | 3 / 21 | 14 % (3–36 %) |
| CONDICIONAL | 6 / 21 | 29 % |
| PASA | 10 / 21 | 48 % (26–70 %) |
| INDETERMINADO | 2 / 21 | |
| *Sensibilidad: incluyendo los 11 casos límite* | 10 / 32 | 31 % (16–50 %) |

## Los nueve que no superan la comprobación
| Clase | Artículo | Qué falla (verificado con código propio) |
|---|---|---|
| **FALLA** | Cal orgánica de Padmanabhapuram (PMC8225893, 2021) | El CO₂ del extracto carbonata ≤ 0,2 % de la cal (×570) ([doc. 41](../docs/41-la-cal-organica.md)) |
| **FALLA** | Erosión de tells en Irak con RUSLE (Forti et al., PMC10195873, 2023) | K = 0,30 en escala de EE. UU. con R en SI: la erosión absoluta queda ×7,6 (5,2–13,8). La clase "extrema" supondría perder ~20 m en 2 000 años en montículos de 23 m. El mapa relativo se mantiene |
| **FALLA** | Mercurio de los embalses de Tikal (Lentz et al., PMC7316703, 2020) | El agua tendría ~11–17 % de la guía de la OMS ([doc. 39](../docs/39-el-mercurio-de-tikal.md)) |
| CONDICIONAL | Filtro de zeolita de Tikal (PMC7582844) | Solo con agua remansada delante del filtro ([doc. 38](../docs/38-el-filtro-de-tikal.md)) |
| CONDICIONAL | Radiocarbono en paleosuelos (PMC10167333) | El carbono disuelto solo basta con parámetros extremos. **Además, error de unidades: carbono moderno infravalorado ×3–72** ([doc. 40](../docs/40-el-carbono-moderno-de-los-paleosuelos.md)) |
| CONDICIONAL | Fueguinos y grasa parda (Watanabe et al., PMC8639971, 2021) | La grasa parda humana da ~1 W frente a ~42 W necesarios. Con la capacidad humana medida sería FALLA (99,9 %); con una capacidad generosa, ≥ 3 en el 83 % |
| CONDICIONAL | Esferas de metal en vidrio romano (PMC8160351, 2021) | La aglomeración coloidal tardaría ~10⁶ h frente a fusiones de 3–48 h, y el cobre es sólido a 900 °C. Solo es viable con chatarra gruesa que se hunde |
| CONDICIONAL | Lajia, flujo de lodo por terremoto (PMC11109126, 2024) | Exige loess saturado (1,5–4 m de agua; 120–920 años de recarga natural). Hoy lo satura el riego; no se muestra que lo estuviera hace 4 000 años |
| CONDICIONAL | Vitamina D en el pelo (PMC11760916, 2025) | Con 38 442 pg/mg, el pelo se llevaría ~50 % del recambio diario y tendría ~1 300 veces la concentración de la sangre. Más que pérdida de peso, apunta a un problema de medida |

## Errores numéricos o de unidades encontrados de paso
Aparecieron en 5 de los 32 artículos aplicables o límite:
- tabla 2 de los paleosuelos (×3–72);
- factor K de RUSLE (×7,6);
- etiqueta "m³/h/cm²" de los molinos de Sistán (imposible: ~1 000 m/s);
- incoherencias entre corriente y ritmo de corrosión en las tablas de las monedas y de las puntas de lanza con polianilina.

## Interpretación
- **Lo que no se puede caer en este error:** el 91 % del corpus, porque mide composición, ADN, formas o fechas.
- **Lo que sí:** en el ~9 % que basa su conclusión en un mecanismo con ritmo físico, **4 de cada 10 (22–66 %) no superan una comprobación de orden de magnitud hecha con sus propios números** sin un supuesto que no declaran. 1 de cada 7 la falla de plano.
- **Es la medida del corpus completo, no de una muestra.** El intervalo refleja la incertidumbre de clasificación y de muestreo de una población mayor. Para extenderlo a otras revistas habría que repetirlo en ellas.
- **Prior publicado:** no hemos encontrado críticas publicadas de ninguno de los 9 casos, salvo la objeción cualitativa de Siegel al almacenamiento de Djoser, que no está en este corpus.
