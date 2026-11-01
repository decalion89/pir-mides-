# 17 — ¿Cuánto de la Gran Pirámide se ha explorado de verdad? Mapa de sensibilidad muográfica

> **Resumen.** Desde 2015, la muografía encontró dos huecos en la Gran Pirámide: el Gran Vacío y el corredor de la cara norte (NFC). La pregunta inversa no se había contestado de forma cuantitativa, que sepamos: **¿en qué partes de la pirámide se puede afirmar que NO hay otro hueco, y de qué tamaño?**
>
> Modelamos las 14 campañas publicadas (2016–2020), con las posiciones, áreas y días de los artículos, y las calibramos con las significaciones publicadas del Gran Vacío. Para cada punto calculamos si un hueco cúbico extra habría dado ≥ 5σ (sensibilidad de descubrimiento):
> - **En el 59–66 % del volumen podría haber un hueco cúbico de 8 m (512 m³, más que la Cámara del Rey) sin que ningún detector lo hubiera visto.** El intervalo depende del corte en ángulo cenital (70°–85°; §5). Para 5 m, el 72–73 %.
> - **La base es la parte menos explorada**: en los 20 m inferiores, un hueco de 8 m no se habría detectado en el **94–99 %** del volumen. Ningún detector **interior** ha tenido esa zona en su campo de visión. Los de 2016–17 están en la Cámara de la Reina, a 21 m, y miran hacia arriba; los de 2019 miran hacia el NFC con una aceptancia estrecha. Solo los dos telescopios exteriores de 2017 la rozan, en direcciones casi horizontales a través de 100–200 m de roca, donde llegan muy pocos muones.
> - **Un detector en la Cámara Subterránea**, excavada en la roca ~30 m bajo la base, es el puesto accesible que más cubre. Con 1 m² de emulsión durante 100 días y la aceptancia de los análisis publicados (|tanθ| ≤ 1), el volumen explorado para huecos de 8 m pasaría del **34 % al 53 %**: casi un 30 % de lo hoy inexplorado. Las Cámaras del Rey o de Campbell no añaden casi nada, porque miran a zonas ya cubiertas.
>
> No hemos encontrado ninguna medición de muones publicada desde la Cámara Subterránea de Keops. El precedente directo es de L. Alvarez et al. (*Science*, 1970). Midieron la pirámide de Kefrén con detectores en la Cámara de Belzoni, en su base, mirando hacia arriba, y dieron la fracción del volumen explorada (~19 % según la crónica de APS News). Este trabajo extiende esa idea a Keops con las campañas modernas.

Archivos:
- código: [`simulador/piramide/cobertura.py`](../simulador/piramide/cobertura.py), [`simulador/estudio_cobertura.py`](../simulador/estudio_cobertura.py), [`simulador/estudio_cobertura_robustez.py`](../simulador/estudio_cobertura_robustez.py), [`simulador/figuras_cobertura.py`](../simulador/figuras_cobertura.py);
- resultados: [`resultados/19_cobertura.json`](../resultados/19_cobertura.json) (y `.npz` con el mapa completo), [`resultados/20_cobertura_robustez.json`](../resultados/20_cobertura_robustez.json);
- figuras: `figuras/08a_mapa_exclusion_cortes.png`, `figuras/08b_volumen_sin_explorar.png`.

## 1. Por qué esta pregunta importa
Un resultado negativo bien medido vale tanto como un descubrimiento. Decir "no hay más cámaras" sin decir **dónde se ha mirado y con qué sensibilidad** no es ciencia. Y al revés: saber dónde no se ha mirado dice exactamente dónde medir a continuación. En física de partículas se hace así, aunque allí "exclusión" suele significar un 95 % de confianza (~2σ). Aquí usamos el criterio más exigente de 5σ, el de un descubrimiento claro, y damos también el de 3σ.

## 2. Método
1. **Rejilla**: el interior de la pirámide original, en celdas de 4 m (40 387 puntos libres de estructuras conocidas, 2,58 millones de m³).
2. **Hipótesis**: en cada punto, un cubo de aire de lado s = 2, 3, 5, 8 o 12 m.
3. **Señal**: para cada campaña, el modelo de muones del proyecto (docs/06) calcula el cambio de cuentas en cada bin angular (0,02 en tanθ), con 2 % de sistemático por bin y resolución de ~20 mrad. Cada bin se traza con hasta 6 × 6 subrayos, para no saltarse huecos más estrechos que un bin. **Este fallo existía en la primera versión del cálculo y lo corregimos**: a 125 m de distancia, un bin mide 2,5 m, y el Gran Vacío, con 1,6 m de ancho, quedaba entre dos rayos.
4. **Referencia**: las estructuras conocidas, más el NFC y el Gran Vacío. La pregunta es si habría **otro** hueco.
5. **Calibración**: la significación del modelo se multiplica por un factor por familia de detector, para que reproduzca lo publicado sobre el Gran Vacío:
   - emulsiones de Nagoya (13,7σ en NE1, 12,7σ en NE2): **×0,44** (el modelo es optimista dentro de la pirámide, como ya se vio en docs/06);
   - telescopios de CEA (5,8σ combinado): **×2,6** (el modelo es pesimista desde fuera).
   
   Los hodoscopios de KEK y las emulsiones de 2019 usan el factor de Nagoya; los telescopios de CEA de 2019 usan el de CEA. Las cifras publicadas proceden de un solo corte del mapa, mientras que el modelo usa el mapa entero. Por eso la calibración tiende a **rebajar** la sensibilidad modelada. El efecto es pequeño: sin calibrar sale 68 % frente a 66 %.
6. **Criterio**: un hueco cuenta como **detectable** si la combinación de todas las campañas (suma en cuadratura) da **≥ 5σ** (nominal) o **≥ 3σ** (optimista).

### Validación
| Comprobación | Modelo | Publicado |
|---|---|---|
| Gran Vacío, CEA G1 (Alhazen) y G2 (Brahic) por separado | 4,3σ y 3,7σ | 5,0σ y 3,7σ |
| Gran Vacío, KEK H1 y H2 | 21σ y 21σ | "> 10σ" en casi todos los cortes |
| NFC desde las emulsiones del corredor descendente (2019) | 40–84σ | "muy por encima de 10σ" |
| NFC desde los telescopios exteriores de 2017 | ~2,7σ | no se informó en 2017 (coherente) |

### Campañas modeladas
| Campaña | Lugar | Área | Días | Fuente |
|---|---|---|---|---|
| Nagoya NE1, NE2 | Cámara de la Reina (nicho este; esquina suroeste) | 0,45 m² | 98; 140 | Morishima et al., *Nature* 2017 |
| KEK H1, H2 | Cámara de la Reina | 1,44 m² (dos planos a 1,5 m y 1,0 m) | ~150; ~240 | ídem |
| CEA G1, G2 | Exterior, a 17 y 23 m de la cara norte | 0,25 m² | 60 | ídem |
| Nagoya EM1–EM4 | Corredor descendente | 0,225 m² por unidad | 79–211 | Procureur et al., *Nat. Commun.* 2023 |
| Nagoya EM5–EM7 | Túnel de al-Mamún | 4 × 0,075 m² | 272 | ídem |
| CEA Joliot, Degennes, Charpak | Corredor descendente y cruce con el ascendente | 0,25–1 m² | 140–158 | ídem |

No se modela la primera campaña de CEA de 2016: un telescopio durante 3 meses, apuntando a la misma zona. Su efecto sería pequeño.

## 3. Resultados (corte nominal de 70° en ángulo cenital)
### Volumen sin explorar (fracción del volumen libre donde un cubo de ese lado NO se habría detectado)
| Lado del cubo | 2 m | 3 m | 5 m | 8 m | 12 m |
|---|---|---|---|---|---|
| ≥ 5σ | 99 % | 96 % | **73 %** | **66 %** | 63 % |
| ≥ 3σ | 98 % | 88 % | 69 % | 65 % | 62 % |

La fracción apenas baja de 8 m a 12 m. Lo que queda sin explorar es sobre todo una cuestión de **geometría**, no de sensibilidad. El 85 % del volumen inexplorado para huecos de 8 m (1,7 millones de m³) está por debajo de 40 m.

### Por alturas (cubo de 5 m, ≥ 5σ)
| Altura | 0–20 m | 20–40 m | 40–60 m | 60–80 m | > 80 m |
|---|---|---|---|---|---|
| Sin explorar | 99 % | 91 % | 67 % | 21 % | 3 % |
| Peso en el volumen total | 36 % | 26 % | 18 % | 11 % | 9 % |

**Comprobación geométrica, sin modelo de flujo.** Basta mirar qué direcciones caen dentro de la aceptancia de cada detector:
- **Detectores interiores:** ninguno tiene en su campo el **98,5 %** de los 20 m inferiores, con cualquier corte de cenit.
- **Todas las campañas, exteriores incluidas:** la fracción de la pirámide fuera del campo de todas ellas depende del corte. Es del 67 % a 70°, el 49 % a 80° y el 36 % a 85°.

La diferencia la ponen los telescopios exteriores de CEA mirando casi en horizontal. Por eso la afirmación robusta se hace en términos de **sensibilidad**, no de campo de visión.

### Dónde medir después (1 m² de emulsión, 100 días, |tanθ| ≤ 1 en cada puesto)
| Puesto | Volumen nuevo explorado, huecos de 8 m | Huecos de 5 m |
|---|---|---|
| **Cámara Subterránea** | **+20 %** del volumen total (34 % → 53 %; el 29 % de lo hoy inexplorado) | +2 % |
| Cámara Subterránea, 4 m² durante 1 año | +23 % | **+17 %** (27 % → 43 %) |
| Exterior oeste / sur / este (a 15 m de la base) | +6 % / +7 % / +5 % | +2 % |
| Cámara del Rey, Cámara de Campbell, cabeza de la Gran Galería | ~0 % | ~0 % |

Lo que añade la Cámara Subterránea está entre 6 y 58 m de altura (percentiles 5–95), en un radio de ~75 m alrededor del eje: el núcleo de la mitad inferior. Los puestos altos eran los mejores para decidir la forma del Gran Vacío (docs/08), pero no sirven para buscar huecos nuevos, porque miran a la parte ya cubierta.

**Sensibilidad a las suposiciones** (revisión independiente, con una muestra de puntos):
- La ganancia de la Cámara Subterránea cambia ≤ 2 puntos si el detector se desplaza 8 m en horizontal o se baja a −30 m.
- Pierde ~3 puntos si la roca madre pesa 2,6 t/m³ en vez de 2,3.
- Con una aceptancia de 1,3 (la bruta de las películas) sería de ~+28 %.

![Cortes del mapa de sensibilidad](../figuras/08a_mapa_exclusion_cortes.png)
![Volumen sin explorar](../figuras/08b_volumen_sin_explorar.png)

## 4. Robustez
Ver [`resultados/20_cobertura_robustez.json`](../resultados/20_cobertura_robustez.json), calculado con una rejilla de 8 m:

ROBUSTEZ_TABLA

## 5. Límites (lo que este mapa NO dice)
- **No dice que haya cámaras ocultas.** Dice dónde no se puede descartar que las haya. La mayor parte de la pirámide es, casi con seguridad, mampostería maciza.
- **El corte de cenit es una suposición.** Por defecto se descartan las direcciones a más de 70° del cenit: el modelo de flujo es menos fiable cerca del horizonte y los análisis publicados se centran en la zona del Gran Vacío. Ese corte **reduce** la sensibilidad de los telescopios exteriores. Con 80°–85°, lo inexplorado para huecos de 8 m baja al 59–60 %, pero los 20 m inferiores siguen inexplorados en un ≥ 94 %.
- **El modelo es simplificado**: no hay Geant4, la geometría interna tiene ±1–2 m de error y el sistemático del 2 % se trata como independiente bin a bin. Las posiciones de las campañas de 2019 son aproximadas (±2–3 m), porque los artículos no dan coordenadas.
- **No es una cota estricta en ningún sentido.** Unas suposiciones aumentan la sensibilidad modelada:
  - área efectiva plana para los telescopios;
  - suma en cuadratura de todas las campañas, como si se hubieran analizado juntas;
  - un cubo que solapa estructuras conocidas o el aire exterior sigue restando densidad.

  Otras la reducen: el corte de cenit y la calibración con significaciones de un solo corte. Por eso damos el intervalo de §4.
- **Puede haber datos no publicados.** ScanPyramids puede tener mediciones que no conocemos. El mapa se refiere a lo publicado.
- **La Cámara Subterránea tiene sus propios sistemáticos.** La roca madre puede no ser homogénea (fisuras, el "pozo" y el pasaje ciego del sur, el pozo de servicio y la "gruta"). Un sistemático correlacionado a gran escala justo encima del detector degradaría más la sensibilidad que el 2 % independiente que usamos. A favor: las estructuras conocidas que tiene encima servirían de calibración en el propio mapa. El modelo predice el bloque de granito de la Cámara del Rey como déficit de muones a ~23σ, la Gran Galería a ~7σ y la Cámara de la Reina a ~4σ (P12). El corredor descendente y el NFC quedan fuera de su campo de visión.
- **Huecos de otras formas.** Un corredor de 1–2 m de sección y mucha longitud se ve mejor o peor que un cubo según su orientación. El NFC, por ejemplo, se vio a > 10σ con una sección de 2 × 2 m porque se miró a lo largo.

## 6. Qué haría falta
1. **Una campaña de emulsiones en la Cámara Subterránea**, del orden de 1–4 m² durante 3–12 meses. Es el mismo tipo de detector que Nagoya ya instaló en el corredor descendente, que es el acceso a esa cámara. Es la medición con mayor rendimiento científico por coste que hemos encontrado.
2. **Los mapas originales de todas las campañas**, para sustituir este modelo por los datos.
3. **Para la periferia inferior**, que ni la Cámara Subterránea ve, harían falta telescopios exteriores de gran área y larga exposición. Es lo que propone el proyecto EGP (Bross et al. 2022), que es por ahora un estudio de viabilidad, no una medición. Nuestros puestos exteriores de 1 m² × 100 días añaden solo un 5–7 %.

## Referencias
- Alvarez, L. W. et al. (1970). *Search for hidden chambers in the pyramids*. Science 167, 832–839.
- APS News (2019). *This month in physics history: Alvarez and the pyramids* (cifra del ~19 %).
- Bross, A. et al. (2022). *Tomographic muon imaging of the Great Pyramid of Giza*. arXiv:2202.08184.
- Morishima, K. et al. (2017). *Discovery of a big void in Khufu's Pyramid by observation of cosmic-ray muons*. Nature 552, 386–390 (arXiv:1711.01576), Methods.
- Procureur, S., Morishima, K. et al. (2023). *Precise characterization of a corridor-shaped structure in Khufu's Pyramid by observation of cosmic-ray muons*. Nat. Commun. 14, 1144.
