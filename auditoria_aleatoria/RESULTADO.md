# Resultado de la auditoría aleatoria de "ceguera al ritmo"

Protocolo y muestra registrados antes de leer ningún artículo: [`PROTOCOLO.md`](PROTOCOLO.md), [`muestra.csv`](muestra.csv) (commit `4de6779`).

**Proceso:**
1. Cribado de los 40 artículos por dos revisores independientes, de 20 en 20, con los criterios del protocolo.
2. Verificación propia en la fuente de los artículos marcados como aplicables:
   - los dos casos que no pasan los recalculamos con código propio;
   - en los que pasan, aceptamos la clasificación del cribado tras leer sus afirmaciones.

## Aplicabilidad
| | n |
|---|---|
| Muestra | 40 (el n.º 40 es la nota de retractación del n.º 39; el n.º 7 es una nota de corrección) |
| **Aplicables** | **7** (17,5 %; IC 95 % de Clopper-Pearson: 7,3–32,8 %) |
| No aplicables | 33. Sobre todo ADN antiguo, filogenias, procedencia, clasificación por imagen y caracterización química sin mecanismo de ritmo |

## Clasificación de los aplicables
| N.º | Artículo | Clase | Motivo |
|---|---|---|---|
| 6 | Cal orgánica de Padmanabhapuram (Shivakumar et al. 2021, PMC8225893) | **FALLA** | El CO₂ del extracto fermentado carbonata como mucho el 0,17 % de la cal (máximo 1,7 %). La "carbonatación interna" afirmada exige ×130–7 000 más ([doc. 41](../docs/41-la-cal-organica.md)) |
| 16 | Filtro de zeolita de Tikal (Tankersley et al. 2020, PMC7582844) | CONDICIONAL | Viable solo con agua remansada delante del filtro o con desvío de las crecidas ([doc. 38](../docs/38-el-filtro-de-tikal.md)) |
| 38 | Radiocarbono en paleosuelos (Broz et al. 2023, PMC10167333) | CONDICIONAL, **más un error aritmético** | La infiltración de carbono disuelto solo basta con parámetros favorables. Además, la tabla 2 infravalora el carbono moderno ×3–72 ([doc. 40](../docs/40-el-carbono-moderno-de-los-paleosuelos.md)) |
| 15 | Calcitonina del mejillón (PMC7200681) | INDETERMINADO | La dosis usada (10 µM) es ~10³–10⁶ veces la fisiológica típica de las hormonas peptídicas, pero no hay medidas en el mejillón. La conclusión es prudente ("candidate"). Caso límite de aplicabilidad |
| 20 | Ácidos biliares en Pompeya (PMC7878498) | PASA | Detectables tras ~1 940 años, como en la literatura. La conclusión secundaria sobre la microbiota depende de pérdidas no selectivas |
| 33 | Cámara magmática del Bushveld (PMC9485162) | PASA | Solidificación (~180–500 mil años) y ritmo de llenado (~0,4–1,1 km³/año) compatibles. Es geología; entró en el corpus por la palabra "ancient" del título |
| 39 | Polianilina sobre puntas de lanza de acero (PMC10966001, retractado) | PASA | Ritmos de corrosión plausibles. Las tablas son incoherentes entre sí, pero en el sentido de más protección. Se aplica a objetos que no se ensayaron |

## Tasas (entre los aplicables)
| | k / n | % | IC 95 % (Clopper-Pearson) |
|---|---|---|---|
| FALLA o CONDICIONAL | 3 / 7 | 43 % | 10–82 % |
| Solo FALLA | 1 / 7 | 14 % | 0,4–58 % |
| Sin el caso límite n.º 15: FALLA o CONDICIONAL | 3 / 6 | 50 % | 12–88 % |

## Interpretación
- **Lo que se puede afirmar:** en una muestra aleatoria de *Scientific Reports* (2020–2025), unos **2 de cada 10** artículos de arqueología o temas afines basan su conclusión en un mecanismo con ritmo físico comprobable. De ellos, **cerca de la mitad** (IC del 10 % al 82 %) no superan sin supuestos adicionales una comprobación de orden de magnitud hecha con sus propios números. Uno de cada siete la falla de plano.
- **Lo que no se puede afirmar:** una tasa precisa. Con 7 casos el intervalo es muy ancho. Para acotarlo a ±15 puntos harían falta ~40 artículos aplicables, es decir, una muestra de ~230, prácticamente todo el corpus.
- **Hallazgos colaterales verificados:**
  - un error aritmético publicado (n.º 38);
  - una afirmación de mecanismo imposible por estequiometría (n.º 6).

  En ninguno de los dos casos hemos encontrado corrección ni crítica publicada.
