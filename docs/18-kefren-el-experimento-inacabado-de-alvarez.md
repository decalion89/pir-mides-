# 18 — Kefrén: el experimento inacabado de Alvarez

> **Resumen.** En 1968–69, Luis Alvarez (premio Nobel de Física en 1968) puso detectores de muones en la Cámara de Belzoni, bajo el centro de la pirámide de Kefrén. Concluyó que no había cámaras del tamaño de la del Rey dentro de un cono de 35° alrededor de la vertical, que es "el 19 % del volumen de la pirámide". Escribió que esperaba "reorganizar el equipo para mirar a través del 81 % restante". No hemos encontrado que ese segundo experimento se publicara nunca.
>
> Reconstruimos su experimento con el modelo de muones del proyecto:
> 1. **El modelo es compatible con lo que afirmó Alvarez.** Su cono contiene el 20,4 % del volumen si el detector está a ras de la base; él dio 19 %. Con unos 700 000 muones en el cono, como en su análisis, el modelo sin calibrar detecta una cámara del tamaño de la del Rey en el 68 % del cono a ≥ 5σ y en el 94 % a ≥ 3σ. No es una validación en sentido estricto: en Kefrén no hay ninguna cavidad conocida con la que comprobarlo, y la afirmación de Alvarez salía de su propia simulación.
> 2. **El 19 % es el techo de lo que él afirmó.** Con criterio de 5σ, lo explorado para cámaras del tamaño de la del Rey está entre el **3 %** (lectura pesimista, análisis tipo Nagoya) y el **15 %** (lectura optimista, el modelo tal cual). Para huecos de 5 m, menos del 4 %. Fuera del cono de 35° (≈ 80 % del volumen) **no hay ninguna afirmación publicada de sensibilidad**.
> 3. **El experimento se puede ampliar desde el mismo sitio.** Cinco exposiciones de emulsión moderna en la Cámara de Belzoni (2 m² × 180 días cada una: una cenital y cuatro inclinadas 45° hacia cada cara) llevarían la cobertura total para cámaras del tamaño de la del Rey del ~20 % al **~61 %**. Ese techo lo fija la geometría (con el corte de 70° del cenit), no la estadística. Los 20 m inferiores seguirían sin explorar, como en Keops.

Archivos:
- código: [`simulador/piramide/kefren.py`](../simulador/piramide/kefren.py), [`simulador/estudio_kefren.py`](../simulador/estudio_kefren.py), [`simulador/estudio_kefren_variantes.py`](../simulador/estudio_kefren_variantes.py), [`simulador/figuras_kefren.py`](../simulador/figuras_kefren.py);
- resultados: [`resultados/21_kefren.json`](../resultados/21_kefren.json), [`resultados/22_kefren_variantes.json`](../resultados/22_kefren_variantes.json);
- figura: `figuras/09_kefren_alvarez.png`.

## 1. El experimento de 1968–69 (Alvarez et al., *Science* 167, 832–839, 1970)
- **Detector**: dos cámaras de chispas de 1,8 × 1,8 m (≈ 4 m², cada una formada por dos módulos de 0,9 × 1,8 m), separadas 0,3 m, con contadores de centelleo y 1,2 m de hierro. Estaba en la esquina sureste de la Cámara de Belzoni, "justo debajo de la base de la pirámide, cerca de su centro".
- **Datos**: "más de un millón" de muones en varios meses, en bins de 3° × 3°, hasta ~45° del cenit. El análisis del cono de 35° (su figura 13) usa unos 700 000.
- **Método**: comparar con una pirámide simulada de densidad uniforme. Las cuatro aristas y el remate de caliza original se ven con claridad.
- **Conclusión**: "no tenemos duda de que detectaríamos una Cámara del Rey en cualquier punto por encima de la Cámara de Belzoni dentro de un cono de 35°". Ese cono es "el 19 % del volumen de la pirámide".

## 2. Reconstrucción
- **Geometría de Kefrén**: lado original 215,25 m (410 codos) y altura original 143,5 m. Hoy mide 136,4 m: el vértice está truncado, lo que no cambia la fracción del cono.
- **Detector**: a ras de la base, en (5, −1,5) m. La cámara está excavada en la roca y su suelo queda unos 3–6 m por debajo de la base. Con el vértice del cono a −3 m o a −6 m, el cono sería el 21,5 % o el 22,9 % del volumen. La coincidencia con el 19 % depende, por tanto, de esta suposición.
- **Modelo de flujo**: el mismo que en Keops (docs/06), con caliza de 2,2 t/m³.
- **Exposición**: se ajusta para que el análisis, restringido al cono de 35°, contenga **7 × 10⁵ muones**. Como variante se usa 10⁶.
- **Hueco buscado**: del tamaño de la Cámara del Rey (10,47 × 5,23 × 5,84 m), y también cubos de 8 m y 5 m.
- **Dos lecturas**: **optimista** (el modelo tal cual) y **pesimista** (×0,44, el cociente entre las significaciones publicadas por Nagoya en Keops y las del modelo; docs/17). El factor ×0,44 procede de otro análisis y otro detector: no es una calibración del experimento de Alvarez, sino una forma de acotar el resultado.

### Comparación con Alvarez
| Magnitud | Modelo | Alvarez 1970 |
|---|---|---|
| Volumen dentro del cono de 35° | 20,4 % (detector a ras de la base) | 19 % |
| Cámara del Rey detectable dentro del cono (optimista) | 68 % a ≥ 5σ; 94 % a ≥ 3σ (con 10⁶: 79 % y 97 %) | "en cualquier punto del cono" |
| Lo mismo, pesimista | 11 % a ≥ 5σ; 39 % a ≥ 3σ | — |
| Cámara del Rey a 40 m sobre Belzoni (su figura 11), 10⁶ muones | 11,9σ optimista (5,2σ pesimista) | señal "evidente" |

La lectura optimista es compatible con lo que afirmó Alvarez, sobre todo a 3σ. La pesimista no lo es. La cobertura depende mucho del criterio estadístico, y por eso damos siempre las dos.

## 3. ¿Cuánto de Kefrén está explorado?
| Hueco | Explorado a ≥ 5σ (pesimista / optimista) | A ≥ 3σ |
|---|---|---|
| Del tamaño de la Cámara del Rey | **3 % / 15 %** | 9 % / 21 % |
| Cubo de 8 m | 8 % / 21 % | 18 % / 23 % |
| Cubo de 5 m | 0,5 % / 4 % | 2 % / 11 % |

Con 10⁶ muones en el cono, la cámara del tamaño de la del Rey sube a 4 % / 18 %. Fuera del cono de 35° (≈ 80 % del volumen) no hay ninguna afirmación publicada de sensibilidad. Los datos de Alvarez llegan hasta ~45° del cenit, y Gutowski et al. reanalizaron la banda de 20–40° (§5), pero nadie ha publicado qué se puede descartar ahí.

## 4. Cómo ampliar el experimento
Desde la misma Cámara de Belzoni, con emulsiones modernas analizadas con |tanθ| ≤ 1:

| Configuración | Cámara tipo Rey a ≥ 5σ (pesimista / optimista) | Cubo de 8 m | Cubo de 5 m |
|---|---|---|---|
| Una exposición cenital, 2 m² × 180 días | 32 % / 36 % | 35 % / 37 % | 18 % / 32 % |
| **Cinco exposiciones (cenital + 4 inclinadas 45°), 2 m² × 180 días cada una** | **61 % / 62 %** | 62 % / 63 % | 45 % / 60 % |

**El ~61 % es un techo geométrico.** La unión de los cinco campos de visión, con el corte de 70° del cenit, contiene el 58,7 % del volumen, y el resto lo aportan cajas que asoman en el borde. Dentro de esos campos casi todo queda explorado. Por debajo de 20 m, solo el 8 % del volumen es alcanzable desde Belzoni con ese corte: de ahí que el 88 % de esa franja siga sin explorar. Con un corte de 80° el techo subiría a ~76 %. Para la franja inferior harían falta puestos en los pasajes bajos o fuera de la pirámide, como en Keops.

Las cinco orientaciones usan películas distintas, así que se pueden exponer a la vez si hay película suficiente (Nagoya llegó a tener 8 m² instalados en Keops). Con 10 m² en total, todo el experimento cabe en **unos seis meses**. Combinarlas en cuadratura no cuenta dos veces la estadística, pero sí trata como independientes los sistemáticos del modelo, lo que es algo optimista.

### Incertidumbre en la posición de la Cámara de Belzoni
Las fuentes no coinciden. Aquí se usa la esquina sureste de la cámara en (5, −1,5) m. Gutowski et al. (arXiv:1712.08590) sitúan el centro de la cámara 13,5 m al este y 4 m al norte del centro de la pirámide, y Wikipedia sitúa los pasajes ~12 m al este del eje. Con la esquina en (19,5; 2) m ([`resultados/22_kefren_variantes.json`](../resultados/22_kefren_variantes.json), rejilla de 6 m):
- el cono es el 19,4 % del volumen;
- lo explorado por Alvarez queda en 3 % (pesimista) y 13 % (optimista);
- la propuesta llega al 59–61 %.

Las conclusiones no cambian.

## 5. Una pista publicada que la propuesta resolvería
Un grupo de estudiantes de secundaria, ganadores del concurso *Beamline for Schools* del CERN en 2016 (Gutowski et al., arXiv:1712.08590, sin revisión por pares), comparó un modelo sencillo con los propios datos de Alvarez, entre 20° y 40° del cenit. Señalan "posiblemente" más muones de lo esperado entre 62° y 72° de acimut, compatible con una cámara del tamaño de la del Rey. También un pico inesperado a 270° y un déficit hacia 192–203°. Es un exceso débil en el mismo conjunto de datos, no un resultado sólido, pero sí una hipótesis concreta que se puede poner a prueba.

Con nuestro modelo en la **lectura pesimista** y 7 × 10⁵ muones, una cámara del tamaño de la del Rey a 30° del cenit daría lo que muestra la tabla. Cada rango junta todos los acimutes y las dos posiciones del detector, y **solo cuenta las posiciones en que la cámara cabe entera dentro de la pirámide**. A partir de ~70 m de altura, el anillo de 30° empieza a salirse.

| Altura sobre Belzoni | Posiciones dentro (de 36) | Datos de Alvarez | Exposición cenital propuesta (2 m² × 180 d) |
|---|---|---|---|
| 20 m | 36 | 8,5–17σ | ≥ 34σ |
| 40 m | 36 | 4,3–9σ | ≥ 16σ |
| 60 m | 36 | 2,7–5,7σ | ≥ 10σ |
| 70 m | 27–36 | 2,2–4,1σ | ≥ 8σ |
| 80 m | 15–20 | 1,8–2,6σ | ≥ 7σ |

**Los datos de 1969 descartan esa cámara hasta unos 30–40 m de altura (a 40 m, solo por poco), pero no a 60–80 m.** La negativa de Alvarez y la pista de los estudiantes podrían ser compatibles si la cámara estuviera alta. Una sola exposición cenital moderna desde el mismo sitio la vería a ≥ 7σ en todas las posiciones de ese anillo que caben en la pirámide, o la descartaría.

![Kefrén: Alvarez frente a la propuesta](../figuras/09_kefren_alvarez.png)

## 6. Límites
- **Modelo simplificado**: sin Geant4 y con densidad uniforme. No incluye las irregularidades del núcleo de roca natural, que en Kefrén es importante: la esquina noroeste está tallada en la roca y la sureste está construida sobre una plataforma. Para un análisis real, esas heterogeneidades serían el principal sistemático, como ya lo fue para Alvarez.
- **Posición del detector**: incierta en ~15 m en horizontal y 3–6 m en vertical según la fuente. Se ha estudiado como variante (§2 y §4) y no cambia las conclusiones.
- **Exposición de 1969**: no se modela su eficiencia real. Se ajusta el número de muones (7 × 10⁵, variante 10⁶), que es lo que fija la estadística. La geometría del detector se simplifica: dos planos a 0,3 m, sin el hierro. Con la pila completa de ~1,8 m, la fracción del cono a ≥ 5σ cambia unos 5 puntos.
- **Corte de cenit**: 70°, como en Keops. Marca el techo de la propuesta (§4).
- **Datos no publicados**: puede haberlos. El mapa se refiere a lo publicado.
- **No dice que haya cámaras en Kefrén.** Dice que la mayor parte de la pirámide no se ha examinado, y cómo examinarla.

## Referencias
- Alvarez, L. W. et al. (1970). *Search for hidden chambers in the pyramids*. Science 167, 832–839.
- Gutowski, B. et al. (2017). *The secret chambers in the Chephren Pyramid*. arXiv:1712.08590 (CERN Beamline for Schools).
- Morishima, K. et al. (2017). Nature 552, 386–390 (factor de Nagoya; docs/17).
