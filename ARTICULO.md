# Flujo, granito y muones: un marco cuantitativo y abierto para la construcción de la Gran Pirámide y la identidad del Gran Vacío

*Borrador de preprint — octubre de 2026. Código y datos en este repositorio.*

## Resumen
Presentamos un marco reproducible que une tres cosas:
1. un modelo de **flujo de construcción**, hilada a hilada, para la Gran Pirámide de Keops;
2. un análisis mecánico de la elevación de las **vigas de granito** de la Cámara del Rey;
3. un **modelo directo de muografía**, validado con las mediciones publicadas por ScanPyramids.

Resultados principales:
- **Construcción.** Un Monte Carlo de 600 escenarios muestra que ninguna rampa de **un solo carril con esquinas** (zigzag, espiral o la rampa interna de Houdin) termina la obra en el reinado de Keops: la mediana es de 70–91 años. El parámetro que lo controla es el **tiempo de giro** en las esquinas (ρ = 0,97). Los métodos viables son dos: rampas múltiples en caras o aristas, solo si el giro dura ≤ 6,3 min, o una rampa recta hasta 45 m seguida de palancas. La mano de obra necesaria (~5000–9000 personas) no es el factor limitante.
- **Vigas de granito.** Tres métodos son físicamente viables para subirlas: rampa, contrapeso en galería y palancas que acompañan la subida del núcleo. Por tanto, las vigas **no implican** que el Gran Vacío fuera una galería de contrapeso, aunque esa hipótesis es mecánicamente coherente.
- **Gran Vacío.**
  - Con la geometría de los detectores de 2017, las hipótesis horizontal, inclinada, de contrapeso y de cámaras apiladas son casi indistinguibles: tras ajustarlas, difieren 2,4–4,9σ de la referencia.
  - Quedan excluidos un hueco estructural pegado a la Gran Galería (29σ) y una rampa interna abierta tipo Houdin (16–30σ).
  - Un detector de 1 m² en la **Cámara del Rey**, de acceso público, separaría todas las hipótesis a 5σ en ≤ 2 meses. En la **Cámara de Campbell** bastarían ~1–5 días.
  - Publicamos las firmas esperadas para cada hipótesis como predicciones registradas.

## 1. Introducción
En la construcción de la Gran Pirámide quedan dos incógnitas principales: el **sistema de elevación de los bloques** y la **función del Gran Vacío** detectado con muones en 2017 (Morishima et al.). El debate se ha basado sobre todo en argumentos cualitativos. Aquí las tratamos como **problemas de cálculo con predicciones comprobables**.

## 2. Métodos
Resumidos en [docs/06](docs/06-metodo-y-validacion.md).
- **Geometría**: sólido convexo con cámaras y corredores como paralelepípedos orientados, a partir de Petrie y de Maragioglio & Rinaldi.
- **Muografía**: espectro de Reyna (2006), pérdida de energía continua en roca estándar y χ² con un 2 % de sistemático por bin.
- **Construcción**: un modelo de flujo con tres límites (carriles, superficie de colocación y mano de obra, esta última por la ley de Little), un Monte Carlo sobre 20 parámetros y rozamiento calibrado con la pintura de Djehutihotep (μ ≈ 0,06–0,11).

## 3. Validación
| | Modelo | Publicado |
|---|---|---|
| Trazas en NE1 (98 días, 0,45 m²) | 5,3 millones | 4,4 millones |
| Exceso del Gran Vacío desde la Cámara de la Reina | 8,6 % | 5,2–11 % |
| Significación desde la Cámara de la Reina | 17σ | 13,7σ |
| Significación desde el exterior norte | 2,8σ | 5,8σ |
| Corredor de la cara norte | ≫10σ | ≫10σ |

El modelo reproduce las tasas y los excesos medidos. Sus significaciones son correctas hasta un factor ~2.

## 4. Resultados
- Construcción: [docs/07](docs/07-resultados-construccion.md).
- Granito y Gran Vacío: [docs/08](docs/08-gran-vacio-y-experimento-decisivo.md).
- Predicciones registradas: [PREDICCIONES.md](PREDICCIONES.md).

## 5. Discusión
- **Qué es nuevo.** No lo son las hipótesis: Houdin, Lehner, Rosell Roig y ScanPyramids las propusieron antes. Lo nuevo es:
  1. haberlas puesto en **un mismo marco cuantitativo y abierto**;
  2. haber identificado el **tiempo de giro** como el parámetro que decide la viabilidad de las rampas;
  3. haber mostrado que la geometría de 2017 **no puede** distinguir las hipótesis sobre el Vacío;
  4. haber **cuantificado** un experimento concreto que sí puede, desde un puesto público, con detectores como los ya usados y en semanas.
- **Qué falta**:
  - simulación completa con Geant4;
  - geometría interna de mayor precisión, con los levantamientos láser de ScanPyramids;
  - un modelo de construcción por agentes;
  - la medición del tiempo de giro con un trineo real.

## Referencias
Ver [docs/FUENTES.md](docs/FUENTES.md). Las principales son:
- Morishima et al., *Nature* 552 (2017);
- Procureur et al., *Nat. Commun.* 14, 1144 (2023);
- Reyna, hep-ph/0604145 (2006);
- Fall et al., *PRL* 112, 175502 (2014);
- Tallet, MIFAO 136 (2017);
- Rosell Roig, arXiv:2511.06112;
- Houdin (2006).
