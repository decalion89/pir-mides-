# Proyecto Pirámides

**¿Cómo se construyó la Gran Pirámide y qué es el Gran Vacío que hay dentro?** Una investigación abierta que va de la historia documentada a la física cuantitativa, con código reproducible y predicciones que se pueden comprobar.

Estado de la evidencia: octubre de 2026.

![Corte de la pirámide con las hipótesis sobre el Gran Vacío y los puestos de detector](figuras/04a_corte_hipotesis.png)

## Resultados principales

### 1. Una sola rampa con esquinas va justa; los sistemas en paralelo dejan margen → [docs/07](docs/07-resultados-construccion.md) y [docs/12](docs/12-la-fisica-de-la-esquina.md)
Simulamos hilada a hilada 10 métodos de elevación en cientos de escenarios con parámetros inciertos. El tiempo que un trineo cargado tarda en girar cada esquina sale de la física (doc. 12):
- **Una sola rampa con esquinas** (zigzag, espiral o la rampa interna de Houdin): mediana de **20–23 años**. Acaba dentro del reinado de Keops (~27 años) en el **74–85 %** de los escenarios, pero en ≤ 20 años solo en el 29–49 %. Es posible, pero ocuparía casi todo el reinado.
- **Sistemas en paralelo** (varias rampas, rampa recta y luego zigzag, o rampa recta y luego palancas): **96–100 %** viables, con ~5000 personas.
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
- **Lo robusto**: el Vacío está sobre el eje de la Gran Galería (±0,3 m), a ~60–65 m de altura, con una sección de ~10–13 m², comparable a la de la Galería.
- **La inclinación no se puede fijar** con los datos públicos:
  - las emulsiones prefieren horizontal o poco inclinado;
  - KEK prefiere inclinado;
  - bajo un mismo corredor, recto o compuesto, los dos conjuntos son incompatibles (Δχ² ≈ 78). Ninguna forma lo arregla, así que es un sistemático y no la geometría.
- **Un error nuestro, contado**: una primera versión daba "18° a 4–6σ" por un fallo de extracción, y lo detectamos y corregimos.

Conclusión: los datos de 2017 no deciden la forma del Vacío. Hace falta medir desde otro punto.

### 7. Predicciones registradas → [PREDICCIONES.md](PREDICCIONES.md)
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
| [ARTICULO.md](ARTICULO.md) | Borrador de preprint |
| [PROPUESTA_SCANPYRAMIDS_en.md](PROPUESTA_SCANPYRAMIDS_en.md) | Propuesta técnica en inglés para los equipos de muografía: la medición desde la Cámara del Rey |
| [PROPUESTA_EXPERIMENTO_TRINEO.md](PROPUESTA_EXPERIMENTO_TRINEO.md) | Propuesta para museos y universidades: medir cuánto tarda un trineo de 2,5 t en girar una esquina |
| [FUENTES](docs/FUENTES.md) | Bibliografía |

## Reproducir
```bash
pip install -r requirements.txt
python -m pytest -q tests                      # 23 pruebas
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
