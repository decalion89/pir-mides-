# Registro de predicciones

Predicciones concretas y comprobables, escritas **antes** de que existan las mediciones que las pondrían a prueba. El historial de git les pone fecha. Si una medición futura las contradice, este registro lo dejará claro y el modelo se corregirá públicamente.

Fecha de registro: **31 de octubre de 2026**. Las cifras salen de `simulador/ejecutar_todo.py` (versión de este commit).

## P1 — Un detector en la Cámara del Rey decide la forma del Gran Vacío
- **Medición:** un detector de muones de ~1 m², mirando hacia el Gran Vacío, durante **≤ 2 meses** (hasta ~7 meses en el caso pesimista de nuestro modelo).
- **Qué debe verse según cada hipótesis:**
  - **horizontal (H1):** franja corta entre tanθy ≈ −0,2 y +0,45;
  - **inclinado 26° (H2) o galería de contrapeso (H3):** franja larga que llega hasta tanθy ≳ 0,65;
  - **cámaras apiladas (H5):** franja interrumpida en tramos;
  - **relleno suelto (H4):** mancha ancha y difusa.
- **Qué la refutaría:** que con esa exposición la medición no separe al menos H1 de H2 a 5σ, salvo por sistemáticos mayores del 2 % por bin.

## P2 — Desde la Cámara de Campbell bastan unos días
- **Medición:** 1 m² en la quinta cámara de descarga, durante **~1–5 días**, separa todos los pares de hipótesis a 5σ (hasta ~3 semanas en el caso pesimista).
- **Firma propia de H3:** solo la galería de contrapeso produce un exceso adicional **cerca del detector**, al norte y por encima, por el pasaje que la uniría con la pila de cámaras.

## P3 — El Gran Vacío no es un hueco de descarga pegado a la Gran Galería
- Esa configuración ya es incompatible con los datos de 2017: **29σ** en nuestro modelo.
- Cualquier medición nueva debería situar el Vacío **~20 m por encima** del techo de la Gran Galería.

## P4 — La rampa interna de Houdin no existe como túnel abierto
- Un túnel de 1,8–2,6 m de sección a ~12 m de las caras habría producido en los datos de la Cámara de la Reina de 2017 un **anillo de excesos de 2,6–6 %** cerca de |tanθ| ≈ 1, con una significación de **17–32σ**.
- **Qué la refutaría:** que un reanálisis de la periferia de esos datos, o una muografía nueva desde el exterior a la altura de 40–90 m, mostrara ese anillo.

## P5 — (REVISADA el 31/10/2026, ver docs/12) El tiempo de giro decide si bastaba una sola rampa
> **Revisión.** La versión original decía que "una rampa de un solo carril con esquinas no construye la pirámide a tiempo". Según una estimación mecánica, el giro cuesta 0,3–2,8 min, y con eso una sola rampa es posible pero justa. Los criterios de decisión actualizados están en docs/12, §3. El texto original se conserva debajo como registro.
- Con el tiempo de giro medido en un experimento real, el modelo da **más de 20 años** (con 25 000 personas y parámetros centrales) para cualquier rampa de un carril (zigzag, espiral o interna), salvo que el giro dure **≤ 1,5 min**.
- **Experimento barato que lo decide:** un trineo de 2,5 t sobre una pista húmeda, con un equipo de ~20–25 personas y una esquina de 90° en una rampa de 3–4 m de ancho. Se mide el tiempo que la esquina queda ocupada por cada trineo.
- **Umbrales que fija el modelo:**
  - si el giro dura **≤ 6,3 min**, las rampas en las aristas o en las cuatro caras son viables en 20 años;
  - si dura más, solo lo son los métodos sin esquinas (rampa recta baja + palancas).

## P6 — Si hubo rampas en las aristas, quedaron huellas medibles desde fuera
- **Medición:** un detector de 1 m² a 15 m del pie de una cara, inclinado 45°, que vea la franja exterior de la pirámide.
- **Predicción:** si se usaron rampas integradas en las aristas y se rellenaron con bloques al menos un **5 % menos densos** que el núcleo, se verán bandas helicoidales a **5σ en unos 300 días** (4,3σ en 100 días). Con un 9 % menos de densidad bastan 30 días.
  - Cifras exactas en `resultados/06_aristas.json`.
- **Si no se ven bandas** con 300 días, las rampas en las aristas solo siguen siendo posibles con un relleno casi idéntico al núcleo. Entonces ganan peso las palancas o las rampas exteriores desmontadas.

## P7 — Condiciones para afirmar que el Gran Vacío es una galería de contrapeso (H3)
La prueba a ciegas ([docs/09](docs/09-robustez-y-prueba-a-ciegas.md)) muestra que H3 es la conclusión más sensible a errores de modelado. **No debe afirmarse** hasta cumplir estas cuatro condiciones:
1. un margen de **≥ 5σ frente a H2** en el ajuste conjunto con la Cámara de la Reina;
2. el flujo calibrado a cielo abierto con el mismo detector;
3. la geometría láser de las cámaras conocidas, con un error < 0,5 m;
4. confirmación desde un segundo puesto (Cámara de Campbell o cabeza de la Gran Galería).

## P9 — Los datos completos de 2017 ya contienen un indicio (doc. 13)
Un análisis estéreo de los mapas 2D originales de las emulsiones NE1 + NE2 debería:
- preferir la forma correcta del Vacío con un margen de **~2–3σ**, sin llegar a 5σ;
- fijar su altura con una precisión de **≤ 1 m** (cota de Cramér–Rao: σ(z) ≥ 0,5–0,6 m).

**Qué la refutaría**: un análisis completo que diera márgenes ≥ 5σ (los datos tendrían más información de la que modelamos), o una altura indeterminada a más de ±3 m (tendrían mucha menos).

## P8 — Posición del Gran Vacío según los datos publicados (reanálisis, docs/11)
Cualquier medición nueva debería encontrar el centro del Vacío:
- **cerca del plano vertical del eje de la Gran Galería**: las emulsiones lo sitúan a +0,2–0,3 m y KEK, que tiene un sistemático sin resolver, a ~1,7 m al este. Por eso el margen es de ±2 m (corregido el 31/10/2026; antes decía ±0,5 m);
- a una altura de **~47–63 m** (emulsiones 61–62,5 m; conjunto 56–59 m; KEK sola 47–54 m, con su mejor ajuste en 47,5 m);
- con una sección de **~8–21 m²** (las emulsiones solas dan ~20 m², el ajuste conjunto con KEK ~10 m²).

**Qué la refutaría**: un centro desplazado más de 3 m al este o al oeste del eje, o una sección menor de 5 m².

## P10 — Los canales siguen proporciones n/11, no las estrellas del reinado de Keops (doc. 14)
Una medición precisa (±0,2°) del tramo alto, hoy sin medir, del canal norte de la Cámara de la Reina debería dar **39,29° ± 0,3°** (pendiente 9/11), y no 39,8–39,9° (Kochab culminando en 2589–2566 a. C.). El canal sur de la Reina, medido en toda su longitud con láser, debería dar 39,29° y no 38,9–39,0° (Sirio en el reinado).

**Qué la refutaría**: ángulos de 39,8–39,9° (norte) y 38,9–39,0° (sur) en ambos canales a la vez. Eso apoyaría la orientación estelar en la época de Keops.

## P11 — RETIRADA (31/10/2026, revisión independiente)
> La versión original "predecía" errores de orientación de +23′ a +54′ para las pirámides de la V dinastía. Esos valores **ya estaban publicados** en la tabla 1 de Spence (2000): Sahure −23′ ± 10, Neferirkare +30′ ± 10, Unas +17,1′. No encajan con aquella extrapolación lineal, así que no era una predicción y además era errónea. Ver docs/15 (v2): con el par de Spence, Sahure y Neferirkare encajan y Unas no.

## P12 — Lo que vería un detector en la Cámara Subterránea (doc. 17), registrada el 01/11/2026
Una campaña de emulsiones de **1 m² durante 100 días** en el suelo de la Cámara Subterránea, mirando hacia arriba y analizada con |tanθ| ≤ 1, como los análisis publicados, debería:
1. **ver las estructuras conocidas que tiene encima**, que sirven de calibración en el propio mapa (valores del modelo calibrado, con un margen de un factor ~2): el **bloque de granito de la Cámara del Rey** como déficit de muones a **~23σ**, la **Gran Galería** a **~7σ**, la Cámara de la Reina a ~4σ y la Cámara del Rey a ~4σ. El corredor descendente y el NFC quedan fuera de su campo de visión;
2. tener sensibilidad de **≥ 5σ a huecos cúbicos de 8 m** en ~20 % del volumen total de la pirámide que hoy está inexplorado (el ~29 % de lo inexplorado), entre ~6 y ~58 m de altura y en un radio de ~75 m alrededor del eje;
3. con 4 m² durante 1 año, alcanzar huecos de **5 m** en ~17 % más del volumen total.

No predecimos que haya una cámara. Predecimos **qué zona quedará explorada y con qué sensibilidad**, para que un resultado negativo sea tan informativo como uno positivo.

**Qué la refutaría**: que con esa exposición el granito de la Cámara del Rey no se viera por encima de ~10σ, o la Gran Galería por encima de ~3σ. Eso indicaría que la roca madre degrada la sensibilidad mucho más de lo modelado, y que la cobertura de los puntos 2 y 3 es optimista. (Corregido el 01/11/2026 tras una revisión independiente: la primera versión usaba |tanθ| ≤ 1,3 y daba +28 %.)

## P13 — Kefrén desde la Cámara de Belzoni (doc. 18), registrada el 01/11/2026
Cinco exposiciones de emulsión de 2 m² × 180 días en la Cámara de Belzoni (una cenital y cuatro inclinadas 45° hacia cada cara, analizadas con |tanθ| ≤ 1) deberían:
1. **ver las cuatro aristas y el remate de caliza original** con mucha más claridad que en 1969, como comprobación de la geometría;
2. tener sensibilidad de ≥ 5σ a una cámara del tamaño de la del Rey en el **~60 %** del volumen de Kefrén (hoy, 3–13 % a 5σ), con todo el volumen por encima de ~40 m cubierto. El techo lo fija la geometría con el corte de 70° del cenit;
3. **confirmar la exclusión de la pista de Gutowski et al. (2017)**. Los propios residuos de Alvarez ya excluyen al 95 % una cámara del tamaño de la del Rey a ~30° del cenit entre 20 y 60 m de altura (doc. 20). La exposición cenital la vería a ≥ 7σ en todas las posiciones de ese anillo que caben en la pirámide. (Corregido el 01/11/2026: posición del detector según Alvarez y prueba directa con sus residuos.)

4. **mirar con más cuidado dos direcciones** que destacan, sin llegar a ser significativas (p ≈ 0,03–0,04 con nula correlada; doc. 19), en los residuos publicados por Alvarez: un exceso de muones a ~38° del cenit hacia el oeste-suroeste (acimut ~246°) y un déficit en el borde sur-suroeste. Si no aparecen con la nueva exposición, eran sistemáticos de 1969.

Igual que en P12, no predecimos que haya una cámara: predecimos qué parte quedará explorada.

**Qué la refutaría**: que las aristas, que son contrastes de opacidad mucho mayores que una cámara, no se vieran con claridad. Indicaría que las heterogeneidades del núcleo rocoso de Kefrén dominan y que la cobertura calculada es optimista.

## P14 — Microgravimetría en los escalones de la Gran Pirámide (doc. 21), registrada el 01/11/2026
Un estudio de gravedad con ~660 estaciones en los escalones de las cuatro caras (a 5, 10, 15 y 20 m de altura, cada 5 m), con un ruido total de ≤ 3 µGal por estación, debería:
1. **detectar a ≥ 5σ cualquier hueco de 8 m** en una banda de ~30–40 m de grosor por dentro de las caras en los 20 m inferiores: ~52 % del volumen de esa franja, que hoy está explorada en un 2 %;
2. **ver la huella de las estructuras conocidas cercanas a las caras**, como el corredor descendente y el NFC en la cara norte, como comprobación.

**Qué la refutaría**: que la dispersión de las medidas tras corregir el modelo de masas fuera ≫ 6 µGal. Indicaría que la heterogeneidad de los bloques domina y que la cobertura calculada es optimista. Y como en 1986, una anomalía de gravedad sola no prueba un hueco: hay que confirmarla con muones.
