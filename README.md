# Proyecto Pirámides

**¿Cómo se construyó la Gran Pirámide y qué es el Gran Vacío que hay dentro?** Una investigación abierta que va de la historia documentada a la física cuantitativa, con código reproducible y predicciones que se pueden comprobar.

Estado de la evidencia: octubre de 2026.

![Corte de la pirámide con las hipótesis sobre el Gran Vacío y los puestos de detector](figuras/04a_corte_hipotesis.png)

## Qué es nuevo y qué no (búsqueda bibliográfica del 01/11/2026)
| Aportación | Estado |
|---|---|
| Reanálisis del mapa de residuos de Alvarez (1970): estructura espacial y mapa de exclusión con sus datos (docs/19–20) | **No encontrado publicado.** El único trabajo cercano (Gutowski et al. 2017, estudiantes del CERN) compara un perfil acimutal, no el mapa |
| Mapa de lo explorado y lo inexplorado en la Gran Pirámide con todas las campañas publicadas (docs/17) | **No encontrado publicado.** Nadie ha cuantificado la cobertura; EGP (2022) propone un sistema nuevo, no un balance de lo hecho |
| Detectores de muones en la Cámara Subterránea y los pasajes bajo la base de Keops (docs/17, 22) | **No encontrado publicado.** No he visto ninguna medición ni propuesta |
| Medir Kefrén desde la cámara de Belzoni (docs/18) | **Ya existe:** el proyecto ScIDEP lo está preparando (arXiv:2503.21959). Lo nuestro es solo la cuantificación de la cobertura y de las orientaciones |
| Microgravimetría sobre las caras de la Gran Pirámide (docs/21) | **Ya existe la idea:** Pašteka et al. 2022 para el Gran Vacío; hubo un estudio de gravedad en 1986. Lo nuestro es el mapa de cobertura de la base y su combinación con los muones |
| Reconstrucción del experimento de Alvarez con un modelo moderno (docs/18) | Parcialmente: Gutowski et al. 2017 compararon un modelo sencillo con sus datos |

"No encontrado" no significa "seguro que no existe": puede haber trabajos no indexados, en otros idiomas o sin publicar.

## Resultados principales

### 1. Una sola rampa con esquinas va justa; los sistemas en paralelo dejan margen → [docs/07](docs/07-resultados-construccion.md) y [docs/12](docs/12-la-fisica-de-la-esquina.md)
Simulamos hilada a hilada 10 métodos de elevación en cientos de escenarios con parámetros inciertos. El tiempo que un trineo cargado tarda en girar cada esquina sale de la física (doc. 12):
- **Una sola rampa con esquinas** (zigzag, espiral o la rampa interna de Houdin): mediana de **20–23 años**. Acaba dentro del reinado de Keops (~27 años) en el **74–85 %** de los escenarios, pero en ≤ 20 años solo en el 29–49 %. Es posible, pero ocuparía casi todo el reinado.
- **Sistemas en paralelo** (varias rampas, rampa recta y luego zigzag, o rampa recta y luego palancas): viables en el **100 %** de los escenarios en ≤ 27 años (96–100 % en ≤ 20 años), con ~5000 personas.
- El tiempo de giro es una **estimación** (el pivote dura segundos; el resto es una suposición sobre parar y arrancar): hay que **medirlo**.
- **Rampa recta hasta la cima**: necesitaría más volumen que la propia pirámide.
- **La mano de obra no era el problema; el flujo, sí.**
- ⚠️ **Corrección**: una versión anterior afirmaba que una sola rampa con esquinas era imposible (0 %). Esa conclusión venía de suponer giros de 2–15 min. La física da 0,3–2,8 min, y la retiramos.

### 2. Las vigas de granito no obligan a nada → [docs/08 §3](docs/08-gran-vacio-y-experimento-decisivo.md)
Para subir las ~43 vigas de 25–80 t de la Cámara del Rey hay tres métodos físicamente viables: rampa, contrapeso y palancas. La idea de que el Gran Vacío fuera una galería de contrapeso es **coherente** (el volumen alcanza para vigas de 60 t), pero **no necesaria**.

### 3. El Gran Vacío: qué se puede saber y cómo → [docs/08](docs/08-gran-vacio-y-experimento-decisivo.md)
- Nuestro modelo de muones reproduce los datos de ScanPyramids: tasas, excesos del 5–11 % y significaciones correctas hasta un factor ~2.
- **Con los detectores de 2017 era casi imposible distinguir** si el Vacío es horizontal, inclinado, una galería de contrapeso o varias cámaras. Eso explica por qué sigue sin resolverse.
- **Descartado**: un simple hueco de descarga pegado a la Gran Galería (29σ) y la rampa interna abierta de Houdin (17–32σ).
- **El experimento decisivo**: un detector de 1 m² en la **Cámara del Rey**, accesible al público, lo resolvería en **≤ 2 meses**; en la **Cámara de Campbell** bastarían ~1–5 días. Damos la imagen que debería verse con cada hipótesis.

![Lo que vería cada detector según cada hipótesis](figuras/04b_mapas_exceso.png)

### 4. La prueba más dura: ajuste conjunto y prueba a ciegas → [docs/09](docs/09-robustez-y-prueba-a-ciegas.md)
Cada hipótesis rival puede moverse ±3 m y cambiar su sección ×0,75–1,25 para imitar los datos. Los errores sistemáticos de flujo, densidad y geometría se ajustan libremente. Con esas reglas, en experimentos simulados a ciegas:
- **Solo con los datos de 2017**: el análisis acierta a menudo, pero con un margen de ~2σ. Insuficiente.
- **Con 60 días en la Cámara del Rey**: acierta el **96–98,5 %** con física realista alterada (flujo ±10 %, caliza de 2,35, cámaras desplazadas 1 m), con márgenes de ~4,3–5,6σ.
- **Advertencia**: la conclusión más espectacular, la galería de contrapeso, es la más sensible a errores de flujo. Las condiciones para afirmarla están en la predicción P7.

![Prueba a ciegas](figuras/05a_prueba_a_ciegas.png)

### 5. Qué cambiaría la historia → [docs/10](docs/10-que-cambiaria-la-historia.md)
Si el Vacío resultara ser una **galería de contrapeso**, sería la prueba más antigua conocida de elevación con contrapesos a gran escala. Se adelantaría unos 350 años al primer cigoñal conocido (Mesopotamia, ~2200 a. C.) y unos 1000 años a su llegada a Egipto (~1550 a. C.). Cualquier otro resultado también cerraría una pregunta abierta desde 2017.

### 6. Reanálisis independiente de los datos publicados en 2017 → [docs/11](docs/11-reanalisis-datos-2017.md)
Extrajimos de la figura del artículo los **679 puntos reales de KEK** y los perfiles de las **emulsiones de Nagoya**, y ajustamos el Vacío con nuestro propio modelo:
- **Validación**: nuestra geometría recupera las posiciones de los detectores publicadas (+5,7/−4,3 m frente a +5,8/−4,5 m).
- **Lo robusto**: el Vacío está cerca del eje de la Gran Galería (las emulsiones lo sitúan a +0,2 m y KEK a ~1,7 m al este), a ~47–63 m de altura, con una sección de ~8–21 m² según el conjunto de datos, comparable a la de la Galería.
- **La inclinación no se puede fijar** con los datos públicos:
  - las emulsiones prefieren horizontal o poco inclinado;
  - KEK prefiere inclinado;
  - bajo un mismo corredor, recto o compuesto, los dos conjuntos son incompatibles (Δχ² ≈ 78). Ninguna forma lo arregla, así que es un sistemático y no la geometría.
- **Un error nuestro, contado**: una primera versión daba "18° a 4–6σ" por un fallo de extracción, y lo detectamos y corregimos.

Conclusión: las figuras publicadas no deciden la forma del Vacío. La cota de Cramér–Rao ([docs/13](docs/13-limite-de-informacion.md)) indica que los **datos completos de 2017, analizados en estéreo**, darían un indicio de ~3σ. Hace falta medir desde la Cámara del Rey para llegar a 4–9σ.

### 7. Los canales de la Gran Pirámide → [docs/14](docs/14-canales-estrellas-o-proporciones.md)
Recalculamos con precisión (catálogo de Yale, precesión IAU 2006) a qué estrellas apuntaban los cuatro canales:
- **Los dos canales del Rey dan fechas en tensión**: Alnitak 2497 ± 41 a. C. y Thuban 2338 ± 53 a. C. (2,4σ).
- **La alineación con cuatro estrellas no es especial**: con estrellas de V ≤ 3,0, los ángulos reales no la producen, y el 27 % de los ángulos al azar sí.
- **Las pendientes n/11** (7/11, 9/11, 11/11) encajan, pero con la corrección justa p = 16 %: **no es significativo**.
- **Medición que lo decide**: el tramo alto del canal norte de la Cámara de la Reina (P10).

### 8. La orientación al norte → [docs/15](docs/15-orientacion-al-norte.md) (v2, revisada)
Con los datos de la tabla de Spence (2000) y solo estrellas visibles:
- **La deriva es real**.
- **Sin el "cambio de configuración" de Kefrén, nada encaja**.
- **Con ese cambio**, Kochab + Mizar es el mejor par con fechas históricamente plausibles y reproduce la fecha de Spence (Keops hacia el 2478 a. C.). Pero una recta genérica ajusta igual, y **la fecha de Spence choca con el radiocarbono**: la datación astronómica no se sostiene.
- **Unas no encaja**: el método habría cambiado en la V dinastía.
- *Una versión anterior, con fechas erróneas y estrellas bajo el horizonte, decía lo contrario. La hemos corregido.*

### 9. De Giza a la Luna → [docs/16](docs/16-de-giza-a-la-luna.md)
- **La energía**: construir la Gran Pirámide costó unos **2,5 GWh** de trabajo mecánico, lo que produce una central de 100 MW en ~25 horas. El **77 % se fue en rozamiento**.
- **El cuello de botella**: el problema nunca fue la energía, sino el rozamiento, el flujo y la organización.
- **La lección para la Luna**: núcleo basto y revestimiento fino, menos rozamiento antes que más potencia, y vías en paralelo.

### 10. El mapa de lo inexplorado → [docs/17](docs/17-mapa-de-lo-inexplorado.md)
Mapa de sensibilidad muográfica de la Gran Pirámide, construido con las 14 campañas publicadas (2016–2020) y calibrado con sus significaciones. Que sepamos, es el primero desde el de Alvarez para Kefrén (1970):
- **En el 59–66 % del volumen podría haber un hueco de 8 m de lado sin que ningún detector lo hubiera visto a 5σ** (72–73 % para 5 m).
- La base es lo menos explorado: en los 20 m inferiores, ≥ 94 %. Ningún detector interior la ha tenido nunca en su campo de visión.
- **Un detector de 1 m² en la Cámara Subterránea durante 100 días pasaría la cobertura para huecos de 8 m del 34 % al 53 %.** Ningún otro puesto accesible se le acerca.

### 11. Kefrén: el experimento inacabado de Alvarez → [docs/18](docs/18-kefren-el-experimento-inacabado-de-alvarez.md)
Reconstruimos la medición de muones de Luis Alvarez de 1968–69 en la pirámide de Kefrén:
- **El modelo es compatible con lo que afirmó.** Su cono de 35° es el 19–20 % del volumen; él dio 19 %. Una cámara del tamaño de la del Rey se detecta en el 62–92 % del cono (lectura optimista).
- **Kefrén está casi sin explorar.** Solo el 3–13 % de su volumen está explorado a 5σ para cámaras de ese tamaño.
- **Se puede ampliar desde el mismo sitio, como ya prepara el proyecto ScIDEP.** Cinco exposiciones de emulsión en la Cámara de Belzoni (~6 meses) llevarían la cobertura total del ~20 % al ~60 %; una sola cenital, al 31–35 %. Además resolverían la posible cámara que unos estudiantes (CERN *Beamline for Schools*) creyeron ver en los datos de Alvarez.

### 12. Los datos de Alvarez, 56 años después → [docs/19](docs/19-los-datos-de-alvarez-reanalizados.md)
Transcribimos y reanalizamos el mapa de residuos que Alvarez publicó en 1970: 801 casillas, medido menos predicho.
- **Tienen estructura espacial clara** (p < 0,0005). Su exceso de χ² (905 para ~750) se debe a errores sistemáticos con correlación espacial, no a ruido.
- **No hay ninguna agrupación significativa** que indique una cámara oculta: la mayor da p = 0,03–0,04, y ninguna pasa de ~2σ al contar que se buscó de seis maneras.
- La pista de los estudiantes del CERN (acimut 62–72°) no aparece.
- **Comprobación con las cuentas en bruto (figs. 8 y 9, 1 800 casillas transcritas y verificadas):** un reanálisis con estadística de Poisson da la misma exclusión (26 % al 95 %) y ningún candidato significativo (p = 0,44). Un reajuste totalmente independiente de Alvarez no es posible: las zonas muertas de su detector no se pueden imitar con una corrección suave.

### 13. Lo que excluyen de verdad los datos de Alvarez → [docs/20](docs/20-lo-que-excluyen-los-datos-de-alvarez.md)
Comparamos cada posible cámara con los 801 residuos reales publicados en 1970.
- **Al 95 % de confianza, una cámara del tamaño de la del Rey queda excluida en el 25 % de Kefrén** (11 % a 5σ nominal). De ese volumen, **un ~7 % está fuera del cono de 35° y nadie lo había analizado.**
- El mejor "candidato" (3,5σ local nominal; 2,4σ calibrado) tiene p global = 0,61, o 0,20 con la alineación desplazada. **No hay ninguna cámara en los datos de Alvarez**, y la cámara que propusieron los estudiantes del CERN queda excluida al 95 %.
- *Corregido el 01/11/2026 tras una revisión independiente: posición del detector según el propio Alvarez (15,5 m al este, 4 m al norte), regla de "cabe entera" en el código y nula con correlación de largo alcance.*

### 14. Otra sonda: la gravedad ve lo que los muones no ven → [docs/21](docs/21-gravedad-y-muones.md)
Un hueco de 8 m es un déficit de ~1 100 toneladas, y eso se nota en la gravedad desde cualquier dirección. La idea de medir gravedad en las caras ya la estudiaron Pašteka et al. (2022) para el Gran Vacío; lo nuevo aquí es el mapa de la base y su combinación con los muones.
- **La gravedad, medida desde los escalones de las caras, cubre el 52 % de la base** (0–20 m), donde los muones cubren el 2 %.
- **Muones actuales + Cámara Subterránea + microgravimetría: 79 % del volumen explorado** para huecos de 8 m (70 % con ruido pesimista), frente al 34 % de hoy.
- Queda sin cubrir un anillo a 40–75 m del eje en los 40 m inferiores.

### 15. Hasta dónde se puede explorar sin tocar una piedra → [docs/22](docs/22-plan-completo-de-exploracion.md)
Combinando todas las sondas desde puntos ya accesibles, se puede pasar del **34 % al ~85 %** del volumen explorado para huecos de 8 m. El orden: muones desde la Cámara Subterránea, gravedad en los escalones, muones en los pasajes bajo la base y telescopios exteriores. El ~15 % restante, la base de los lados este y oeste, no se alcanza sin un acceso nuevo: multiplicar el área de los telescopios exteriores por 16 apenas ayuda.

### 16. ¿Una ley de aprendizaje? Un techo, no una curva → [docs/23](docs/23-ley-de-aprendizaje.md)
Ritmo de construcción (m³/año) de todas las pirámides del Reino Antiguo frente a la experiencia acumulada. **No se cumple la ley de Wright.** Snefru multiplicó por 4–13 el ritmo de Djoser en una generación, y tres reinados seguidos se mantuvieron en ~85 000–150 000 m³/año (~340 m³/día). Después el ritmo cae ×6–90 justo cuando la experiencia es máxima. La "tecnología" no se perdió: se alcanzó el límite del Estado y luego se redirigió. Es una regularidad sugerente con solo 4 puntos, no una ley.

### 17. ¿Hay algo más en los datos de 2017? → [docs/24](docs/24-busqueda-de-anomalias-en-kek.md)
Búsqueda de una segunda señal en los residuos de KEK tras restar el Gran Vacío, con nula correlacionada y significación global. El mejor candidato (p = 0,031; ≈ 1,9σ contando excesos y déficits) **no lo confirma el segundo detector** por paralaje. No hay una segunda anomalía en esos datos.

### 18. Una teoría propia, puesta a prueba y refutada → [docs/25](docs/25-teoria-del-cuello-de-botella.md)
Propusimos que el techo histórico (~340 m³/día) lo fijaba un límite físico de las rampas. Con el simulador original parecía encajar, pero un Monte Carlo mostró que la coincidencia dependía de un solo parámetro, el tiempo de giro. Con la física de las esquinas del documento 12, las rampas permiten 2–5 veces más. **La teoría queda refutada.** La causa del techo sigue abierta: o el modelo sobrestima la productividad, o el límite era organizativo o económico.

### 19. El límite físico del gnomon → [docs/26](docs/26-el-limite-del-gnomon.md)
El método solar de las sombras iguales tiene en Giza un error sistemático máximo de ~5,8′. Solo Keops (−3,4′) y Kefrén (−6,0′, en el límite) caben dentro; las otras siete pirámides (8,7–30′) no. El gnomon no puede ser el único método de la serie. Encaja mejor un método estelar o un cambio de técnica entre la pirámide Roja y Keops.

### 20. Alvarez desde cero → [docs/27](docs/27-alvarez-desde-cero.md)
Reconstruimos la pirámide (con su remate y su revestimiento perdido), la posición del detector y su aceptancia, y ajustamos los 649 034 muones medidos en 1969 **sin usar el modelo de Alvarez**.
- Dentro de su cono, el ajuste es casi tan bueno como el suyo (χ²/casilla 1,4 frente a 0,93), y su conclusión negativa se reproduce: 85 % del cono excluido al 95 %.
- El modelo propio produjo una "cámara" muy significativa (Δχ² = −43) que resultó ser un artefacto: desaparece al mover el detector a su posición topográfica y el modelo de Alvarez la excluye.

### 21. Cuándo fabrica un detector una cámara que no existe → [docs/28](docs/28-falsas-camaras.md)
Con un experimento numérico calculamos cuánto error en la posición del detector hace falta para "descubrir" una cámara inexistente. Sale un umbral de ~1–1,5 m de error horizontal: por encima, la falsa señal crece con el número de muones. Con 10⁸ muones y 2 m de error aparece una cámara falsa a ~30σ. El simulador reproduce el falso candidato real de los datos de Alvarez (−46 frente a −43). La hipótesis inicial, una ley de potencias, era incorrecta.

### 22. ¿Pudo un error de posición fabricar el Gran Vacío? → [docs/29](docs/29-el-gran-vacio-pasa-la-prueba.md)
Aplicamos la misma prueba a los detectores de la Cámara de la Reina. **El Gran Vacío pasa la prueba.**
- **Con la precisión declarada del modelo (~30 cm)** no se fabrica ninguna señal en su posición.
- **El detector más expuesto** es KEK H1, casi bajo el eje de la Gran Galería. Necesitaría 0,54–0,75 m de error para producir un vacío falso justo allí.
- **Los de Nagoya**, desplazados 4,5–5,8 m del eje, necesitan ~1,2 m de error (NE2) o no lo fabrican nunca en ±1,2 m (NE1).

De aquí sale una regla de diseño: la paralaje lateral protege frente a los vacíos falsos paralelos a un hueco conocido.

### 23. La ley de la mitad de la señal → [docs/30](docs/30-la-ley-de-la-mitad.md)
Una regla general detrás de los docs. 27–29. Si un error de modelo imita una fracción ρ de la señal de un hueco:
- **Hueco vacío:** se "descubre" uno falso si y solo si **ρ > ½**, con probabilidad **Φ(Z_real(ρ − ½))**.
- **Contraste libre** (análisis de "exceso del X %"): siempre aparece un exceso falso con **Z_falso = ρ·Z_real**.

ρ no depende de la cantidad de datos (comprobado de ×0,01 a ×100, y con Monte Carlo de Poisson). Por eso más estadística no arregla un error de geometría.

Las matemáticas son conocidas (sesgo por variable omitida). Su formulación y uso en muografía no los hemos encontrado publicados.

### 24. Los datos de KEK descartan el falso vacío → [docs/31](docs/31-kek-se-certifica-a-si-mismo.md)
Reajustamos los 679 puntos publicados de KEK dejando libre un desplazamiento δ entre los datos y su simulación de normalización. Los datos lo fijan en |δ| < 0,1 m a 5σ (≲ 0,25 m con margen para nuestro modelo), muy por debajo de los 0,54 m que harían falta para fabricar el Gran Vacío. La señal de KEK no es ese artefacto.

En cambio, ese δ no explica la tensión entre KEK y las emulsiones (sigue en Δχ² ≈ 66), así que esa explicación queda descartada.

### 25. Ningún parámetro de KEK explica la tensión → [docs/32](docs/32-sistematicos-de-kek.md)
Probamos la posición este-oeste y vertical, la separación H1–H2 y la escala angular de los hodoscopios. La tensión KEK–emulsiones no baja de ~58 con valores plausibles, ni de ~53 con valores extremos. Las emulsiones son el conjunto que "no cabe".

Dos cosas más:
- La altura del Vacío que da KEK depende casi por completo de la separación H1–H2: es la paralaje.
- Corregimos una propuesta del doc. 31. La Gran Galería no puede fijar la posición absoluta de KEK, porque se cancela en sus cocientes.

### 26. ¿A cuántos metros está el Gran Vacío? → [docs/33](docs/33-a-cuantos-metros-esta-el-gran-vacio.md)
Con posteriores de su geometría (emulsiones, KEK y conjunto), medimos cuánta piedra separa el Vacío de los espacios accesibles.
- **Ninguno está a menos de 5 m** con probabilidad apreciable (≤ 15 %). Una confirmación con endoscopio como la del corredor norte no es posible.
- **Lo más cercano, de forma robusta, es la pared norte de las cámaras de descarga 4 y 5:** ~8 m, y < 10 m con una probabilidad del 86–99,8 % en los tres análisis.
- **Hallazgo de método:** los datos publicados solo miran hacia el norte. El extremo sur lo fija una frase del artículo, y con ella coincide con el final de la Gran Galería.

### 27. La tumba del Primer Emperador respira → [docs/34](docs/34-la-tumba-que-respira.md)
Un lidar midió en 2016 que del túmulo de Qin Shi Huang salen ~4 g de mercurio al día (Duan et al. 2020).
- **La difusión a través de la tierra desde la cámara se queda corta** en un factor de 19 a 2 170 (mediana 163), y ninguna de 200 000 combinaciones de parámetros basta.
- **El suelo contaminado del túmulo,** con ritmos típicos, se queda corto de 9 a 220 veces.
- **Lo que basta es que el palacio subterráneo intercambie aire con la atmósfera** (~460 m³/día, bombeo barométrico).

Si el flujo es correcto y viene de la tumba, **no está sellada**. Prueba barata: la emisión debe subir cuando baja la presión.

### 28. El "cerebro de vidrio" de Herculano no pudo enfriarse a 1 000 K/s → [docs/35](docs/35-el-cerebro-de-vidrio.md)
Giordano et al. (2025) dedujeron que el cerebro de una víctima del Vesubio se enfrió a ~1 000 K/s tras pasar por encima de 510 °C.
- **Dentro de un cráneo, la física da 0,1–1,7 K/s.**
- **Con ritmos posibles, su propia cinética da una temperatura ficticia de ~405–440 °C,** que se solapa con la de los depósitos.
- **Con su propia energía de activación, el material se ablanda en 0,4 s a 465 °C y se recuece en minutos a 315–350 °C.**

La historia térmica propuesta no se sostiene.

### 29. El "ascensor hidráulico" de Djoser no tenía dónde guardar el agua → [docs/36](docs/36-el-ascensor-sin-agua.md)
Landreau et al. (2024) compararon el agua total disponible con la necesaria (18 Mm³), sin pérdidas.
- **Con un balance día a día** (riadas episódicas, su embalse, evaporación e infiltración), el ascensor recibe el **27 %** de su propia demanda. Ninguna de 1 500 simulaciones llega al 90 %, ni siquiera sin pérdidas.
- **Lo limita el almacenamiento:** la mitad de cada riada se desborda, y el embalse se seca en meses.
- **Solo funciona** con un depósito profundo de millones de m³, uso optimizado y ≥ 1–2 riadas al año.
- **Predicción:** limos lacustres en el fondo del Foso Seco.

### 30. El patrón común: "ceguera al ritmo" → [preprint/ritmo](preprint/ritmo/rate_blindness_en.pdf)
Los tres casos anteriores (Qin, Herculano, Djoser) fallan igual: razonan con totales, equilibrios o capacidades, e ignoran el ritmo máximo que impone la física (difusión, conducción del calor, almacenamiento entre riadas). Los desajustes van de ×2–9 a ×600–12 500.

Artículo de síntesis en inglés, con figura, para enviarlo con el nombre del autor.

### 31. El plomo de Roma: el efecto sobre el CI está sobrestimado entre 2 y 5 veces → [docs/37](docs/37-el-plomo-de-roma.md)
McConnell et al. (PNAS 2025) calcularon 2,5–3 puntos de CI perdidos en todo el Imperio por el plomo del aire. Para ello tomaron como "aumento" la plombemia **total** que predice una regresión moderna (niños de EE. UU. de 1988–94) y le sumaron una base neolítica.
- Con su propia regresión bien diferenciada salen **1,4 puntos**.
- Con un balance de ingesta (aire, cultivos y suelo) salen **0,6**.
- La regresión se extrapola 10–100 veces por debajo de su rango de calibración.

### 32. Predicciones registradas → [PREDICCIONES.md](PREDICCIONES.md)
Siete predicciones concretas, fechadas en git **antes** de que existan las mediciones que las comprobarán. Incluyen la huella de las rampas en las aristas medible desde fuera (P6) y las condiciones para afirmar la galería de contrapeso (P7).

## La parte histórica
| Archivo | Contenido |
|---|---|
| [01 — Tecnología documentada](docs/01-tecnologia-documentada.md) | Canteras, herramientas, transporte, precisión y mano de obra |
| [02 — ¿Por qué "se perdió"?](docs/02-por-que-se-perdio.md) | No se perdió: se abandonó |
| [03 — Misterios abiertos](docs/03-misterios-abiertos.md) | Lo que de verdad no sabemos (2017–2026) |
| [04 — Teorías alternativas](docs/04-teorias-alternativas.md) | Extraterrestres, Atlántida, geopolímero... evaluadas una a una |
| [05 — Plan de investigación](docs/05-plan-de-investigacion.md) | Líneas de trabajo |
| [06 — Método y validación](docs/06-metodo-y-validacion.md) | Cómo funciona el simulador y contra qué se ha validado |
| [07 — Resultados de construcción](docs/07-resultados-construccion.md) | Qué métodos de elevación son viables |
| [08 — Gran Vacío y experimento decisivo](docs/08-gran-vacio-y-experimento-decisivo.md) | Hipótesis, vigas de granito, diseño de la medición |
| [09 — Robustez y prueba a ciegas](docs/09-robustez-y-prueba-a-ciegas.md) | Ajuste conjunto, sistemáticos y física alterada |
| [10 — Qué cambiaría la historia](docs/10-que-cambiaria-la-historia.md) | Qué significaría cada resultado y hoja de ruta |
| [11 — Reanálisis de los datos de 2017](docs/11-reanalisis-datos-2017.md) | Datos reales de KEK y Nagoya ajustados con nuestro modelo |
| [12 — La física de la esquina](docs/12-la-fisica-de-la-esquina.md) | Corrección de una conclusión y protocolo del experimento del trineo |
| [13 — El límite de la información](docs/13-limite-de-informacion.md) | Cota de Cramér–Rao: qué pueden decir como máximo los datos de 2017 y la Cámara del Rey |
| [14 — Los canales: ¿estrellas o proporciones?](docs/14-canales-estrellas-o-proporciones.md) | Astronomía de precisión y prueba contra el azar de la hipótesis estelar; patrón de pendientes n/11 |
| [15 — ¿Cómo encontraron el norte?](docs/15-orientacion-al-norte.md) | 92 pares de estrellas contra las orientaciones medidas: la deriva es real, pero no sirve para fechar |
| [16 — De Giza a la Luna](docs/16-de-giza-a-la-luna.md) | La Gran Pirámide costó ~2,5 GWh de trabajo mecánico (25 h de una central de 100 MW); lecciones para construir en la Luna |
| [17 — El mapa de lo inexplorado](docs/17-mapa-de-lo-inexplorado.md) | Qué parte de la pirámide han explorado de verdad los muones (59–66 % sin explorar para huecos de 8 m), y dónde medir: la Cámara Subterránea |
| [18 — Kefrén: el experimento inacabado de Alvarez](docs/18-kefren-el-experimento-inacabado-de-alvarez.md) | Reconstrucción de la medición de 1969, cuánto de Kefrén está explorado (3–13 %) y cómo ampliarlo al ~60 % |
| [19 — Los datos de Alvarez, 56 años después](docs/19-los-datos-de-alvarez-reanalizados.md) | Reanálisis del mapa de residuos de 1970: estructura espacial clara y ninguna cámara oculta |
| [20 — Lo que excluyen de verdad los datos de Alvarez](docs/20-lo-que-excluyen-los-datos-de-alvarez.md) | Mapa de exclusión de Kefrén con los residuos reales de 1970: 25 % al 95 %, ~7 % nuevo fuera del cono |
| [21 — Gravedad y muones](docs/21-gravedad-y-muones.md) | Microgravimetría para la base que los muones no ven: plan combinado que cubre el 79 % |
| [22 — Plan completo de exploración](docs/22-plan-completo-de-exploracion.md) | Del 34 % al ~85 % con lo que ya existe; el límite físico del ~15 % restante |
| [23 — ¿Una ley de aprendizaje?](docs/23-ley-de-aprendizaje.md) | Ritmo de construcción por reinado: techo de ~340 m³/día y caída por decisión |
| [24 — Anomalías en los datos de KEK](docs/24-busqueda-de-anomalias-en-kek.md) | Búsqueda de una segunda señal en los residuos de 2017: ninguna confirmada |
| [25 — Teoría del cuello de botella (refutada)](docs/25-teoria-del-cuello-de-botella.md) | Una teoría propia sobre el techo de construcción, y la prueba que la tumba |
| [26 — El límite del gnomon](docs/26-el-limite-del-gnomon.md) | El método solar no puede producir errores de más de ~6′: solo explica Keops y Kefrén |
| [27 — Alvarez desde cero](docs/27-alvarez-desde-cero.md) | Reconstrucción independiente del experimento de 1969 y un falso candidato desmontado |
| [28 — Falsas cámaras](docs/28-falsas-camaras.md) | Regla práctica: la posición del detector debe conocerse mejor que ~1 m o se fabrican cámaras falsas |
| [29 — El Gran Vacío pasa la prueba](docs/29-el-gran-vacio-pasa-la-prueba.md) | Un error de posición no fabrica el Gran Vacío: margen ~1,8× para KEK H1, ~4× o más para Nagoya; regla de la paralaje |
| [30 — La ley de la mitad](docs/30-la-ley-de-la-mitad.md) | Un error de modelo fabrica un hueco vacío si imita más de la mitad de su señal (ρ > ½), sea cual sea la exposición; con contraste libre, Z_falso = ρ·Z_real |
| [31 — KEK se certifica a sí mismo](docs/31-kek-se-certifica-a-si-mismo.md) | Los datos de KEK fijan su registro con la simulación a < 0,1–0,25 m: descartan el falso vacío; la tensión con las emulsiones no viene de ahí |
| [32 — Sistemáticos de KEK](docs/32-sistematicos-de-kek.md) | Ni posición, ni paralaje, ni escala angular de KEK explican la tensión con las emulsiones (≥ 58 con valores plausibles) |
| [33 — A cuántos metros está el Gran Vacío](docs/33-a-cuantos-metros-esta-el-gran-vacio.md) | Ningún espacio accesible a menos de 5 m; lo más cercano, las cámaras de descarga 4–5 (~8 m); sin endoscopio posible |
| [34 — La tumba que respira](docs/34-la-tumba-que-respira.md) | El mercurio medido sobre la tumba de Qin no puede salir por difusión (×163): solo un intercambio de aire (~460 m³/día) lo explica; prueba barométrica |
| [35 — El cerebro de vidrio](docs/35-el-cerebro-de-vidrio.md) | El enfriamiento a 1 000 K/s del cerebro vitrificado de Herculano es imposible dentro de un cráneo (0,1–1,7 K/s); su propia cinética contradice el escenario |
| [36 — El ascensor sin agua](docs/36-el-ascensor-sin-agua.md) | Balance hídrico del ascensor de Djoser: con sus estructuras recibe el 27 % de su demanda; solo es viable con un depósito de Mm³ estanco (predicción: limos lacustres) |
| [37 — El plomo de Roma](docs/37-el-plomo-de-roma.md) | El déficit de CI por plomo romano (PNAS 2025) está sobrestimado ×2–5: doble contabilidad de la constante de la regresión y extrapolación fuera de rango |
| [ARTICULO.md](ARTICULO.md) | Borrador del artículo (en español) |
| [preprint/alvarez/alvarez_reanalysis_en.pdf](preprint/alvarez/alvarez_reanalysis_en.pdf) | **Artículo breve en inglés**: los datos de Alvarez (1970) reanalizados (documentos 19–20) |
| [preprint/preprint_en.pdf](preprint/preprint_en.pdf) | **Preprint en inglés** con todos los resultados, con fuente LaTeX para arXiv |
| [NOTA_TECNICA_cobertura_en.md](NOTA_TECNICA_cobertura_en.md) | **Nota técnica en inglés** para los equipos de muografía: el mapa de sensibilidad y la propuesta de la Cámara Subterránea |
| [PROPUESTA_SCANPYRAMIDS_en.md](PROPUESTA_SCANPYRAMIDS_en.md) | Propuesta técnica en inglés para los equipos de muografía: la medición desde la Cámara del Rey |
| [preprint/arxiv_paquete.zip](preprint/arxiv_paquete.zip) | **Paquete para arXiv** (main.tex + figuras); instrucciones en preprint/arxiv/LEEME.md |
| [envio/correos.md](envio/correos.md) | Borradores de correo para ScanPyramids, el experimento del trineo y el aval de arXiv |
| [PLAN_DE_CONTACTO.md](PLAN_DE_CONTACTO.md) | Qué grupo puede comprobar cada predicción y en qué orden escribirles |
| [PROPUESTA_EXPERIMENTO_TRINEO.md](PROPUESTA_EXPERIMENTO_TRINEO.md) | Propuesta para museos y universidades: medir cuánto tarda un trineo de 2,5 t en girar una esquina |
| [FUENTES](docs/FUENTES.md) | Bibliografía |

## Reproducir
```bash
pip install -r requirements.txt
python -m pytest -q tests                      # 38 pruebas
cd simulador && python ejecutar_todo.py        # ~5 min: resultados 01-04 y figuras
python ejecutar_profundo.py                    # ~12 min: robustez, prueba a ciegas, aristas
# Reanálisis de los datos publicados (requiere el PDF de arXiv:1711.01576):
python extraer_datos_kek.py 1711.01576.pdf && python extraer_datos_emulsiones.py 1711.01576.pdf
PYTHONPATH=. python reanalisis_emulsiones_inclinacion.py   # y reanalisis_kek_inclinacion.py, reanalisis_conjunto.py
PYTHONPATH=. python estudio_giros.py                      # física del giro (~3 min)
```

Estructura:
- `simulador/piramide/`:
  - `geometria.py`: forma de la pirámide y estructuras internas;
  - `muones.py`: modelo de muografía;
  - `fisica.py`, `rampas.py`, `obra.py`, `montecarlo.py`: construcción;
  - `granito.py`: vigas de la Cámara del Rey;
  - `vacio.py`: hipótesis sobre el Gran Vacío y diseño de la medición;
  - `robustez.py`: ajuste conjunto, sistemáticos perfilados y prueba a ciegas;
  - `aristas_muones.py`: huella de las rampas integradas en las aristas;
  - `reanalisis.py`, `reanalisis_emulsiones.py`: modelo directo de los detectores de KEK y Nagoya para ajustar sus datos publicados.
- `datos/piramide_keops.json`: cada valor con su fuente.

## Honestidad
- **No afirmamos haber descubierto qué es el Gran Vacío.** Mostramos por qué no se ha podido saber y **qué medición concreta lo resolvería**, con las predicciones escritas de antemano.
- Los modelos son simplificados: posiciones internas con ±1–2 m de error, sin simulación completa con Geant4 y un modelo de flujo medio. Todas las limitaciones están en [docs/06](docs/06-metodo-y-validacion.md).
- Las ideas de partida no son nuestras: vienen de Houdin, Lehner, Rosell Roig y ScanPyramids. Lo que aportamos es el **marco cuantitativo y abierto** que las pone a prueba juntas.
