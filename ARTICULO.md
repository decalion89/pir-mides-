# Flujo, granito y muones: un marco cuantitativo y abierto para la construcción de la Gran Pirámide y la identidad del Gran Vacío

*Borrador de preprint — octubre de 2026. Código y datos en este repositorio.*

## Resumen
Presentamos un marco reproducible que une tres cosas:
1. un modelo de **flujo de construcción**, hilada a hilada, para la Gran Pirámide de Keops;
2. un análisis mecánico de la elevación de las **vigas de granito** de la Cámara del Rey;
3. un **modelo directo de muografía**, validado con las mediciones publicadas por ScanPyramids.

Resultados principales:
- **Construcción.** El tiempo de giro en las esquinas controla la viabilidad de las rampas (ρ = 0,97). Lo calculamos desde la física: 0,8–2,8 min parando y pivotando, o 0,3 min con un poste de reenvío como los de Hatnub, a cambio de equipos 1,4–1,9 veces mayores. Con esos tiempos, **una sola rampa con esquinas** es posible pero justa: mediana de 20–23 años, y termina en ≤ 27 años en el 74–85 % de los escenarios. **Los sistemas en paralelo** son viables en el 96–100 %. Una primera versión, que suponía giros de 2–15 min, concluyó erróneamente que una sola rampa era imposible. La mano de obra necesaria (~5000–9000 personas) no es el factor limitante.
- **Vigas de granito.** Tres métodos son físicamente viables para subirlas: rampa, contrapeso en galería y palancas que acompañan la subida del núcleo. Por tanto, las vigas **no implican** que el Gran Vacío fuera una galería de contrapeso, aunque esa hipótesis es mecánicamente coherente.
- **Gran Vacío.**
  - Con la geometría de los detectores de 2017, las hipótesis horizontal, inclinada, de contrapeso y de cámaras apiladas son casi indistinguibles: tras ajustarlas, difieren 2,4–4,9σ de la referencia.
  - Quedan excluidos un hueco estructural pegado a la Gran Galería (29σ) y una rampa interna abierta tipo Houdin (17–32σ).
  - Un detector de 1 m² en la **Cámara del Rey**, de acceso público, separaría todas las hipótesis a 5σ en ≤ 2 meses. En la **Cámara de Campbell** bastarían ~1–5 días.
  - Publicamos las firmas esperadas para cada hipótesis como predicciones registradas.
- **Robustez.** Repetimos el análisis con un ajuste conjunto: cada hipótesis tiene 225 variantes de posición, forma y sección, y se ajustan sistemáticos de normalización, gradiente y espectro. En pruebas a ciegas con física alterada (flujo ±10 %, densidad, geometría desplazada), 60 días en la Cámara del Rey identifican la hipótesis correcta en el 96–98,5 % de los casos. La hipótesis de la galería de contrapeso es la más sensible a errores de flujo, y fijamos condiciones previas para poder afirmarla.
- **Reanálisis de los datos publicados.** Digitalizamos los 679 puntos de KEK y los perfiles de las emulsiones de Nagoya. Nuestra geometría recupera las posiciones de los detectores publicadas, con un error de 0,2 m. El Vacío queda sobre el eje de la Gran Galería, a ~60–65 m de altura, con una sección de ~10–13 m². Su inclinación no se puede fijar de forma robusta: los dos conjuntos de datos son mutuamente incompatibles bajo un corredor recto único. Un fallo de extracción produjo al principio una inclinación falsa de 18°; lo documentamos.
- **Huella de las rampas.** Si se usaron rampas integradas en las aristas, su relleno, si es ≥ 5 % menos denso, sería visible desde el exterior en ~30–300 días.

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
- Robustez y prueba a ciegas: [docs/09](docs/09-robustez-y-prueba-a-ciegas.md).
- Qué cambiaría cada resultado: [docs/10](docs/10-que-cambiaria-la-historia.md).
- Reanálisis de los datos de 2017: [docs/11](docs/11-reanalisis-datos-2017.md).
- Predicciones registradas: [PREDICCIONES.md](PREDICCIONES.md).

## 5. Discusión
- **Qué es nuevo.** No lo son las hipótesis: Houdin, Lehner, Rosell Roig y ScanPyramids las propusieron antes. Lo nuevo es:
  1. haberlas puesto en **un mismo marco cuantitativo y abierto**;
  2. haber identificado el **tiempo de giro** como el parámetro que decide la viabilidad de las rampas, y haberlo estimado desde la física;
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
