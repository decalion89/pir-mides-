# Proyecto Pirámides

**¿Cómo se construyó la Gran Pirámide y qué es el Gran Vacío que hay dentro?** Una investigación abierta que va de la historia documentada a la física cuantitativa, con código reproducible y predicciones que se pueden comprobar.

Estado de la evidencia: octubre de 2026.

![Corte de la pirámide con las hipótesis sobre el Gran Vacío y los puestos de detector](figuras/04a_corte_hipotesis.png)

## Resultados principales

### 1. Ninguna rampa única con esquinas basta → [docs/07](docs/07-resultados-construccion.md)
Simulamos hilada a hilada 10 métodos de elevación en 600 escenarios con parámetros inciertos:
- **Rampas de un solo carril** con esquinas (zigzag, espiral, rampa interna de Houdin): tardarían **70–91 años** de mediana, cuando Keops reinó unos 27. Fallan en el **100 %** de los escenarios.
- **Rampa recta hasta la cima**: necesitaría más volumen que la propia pirámide.
- **Métodos viables**:
  - rampa recta hasta 45 m (dos tercios del volumen) y **palancas** por encima, en el 100 % de los escenarios y con ~5000 personas;
  - **varias rampas** en las caras o aristas, en el 37 % de los escenarios.
- **El parámetro que lo decide todo es cuánto tarda un trineo cargado en girar una esquina** (ρ = 0,97). Se puede medir con un experimento sencillo.
- **La mano de obra no era el problema; el flujo, sí.**

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

### 6. Predicciones registradas → [PREDICCIONES.md](PREDICCIONES.md)
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
| [ARTICULO.md](ARTICULO.md) | Borrador de preprint |
| [FUENTES](docs/FUENTES.md) | Bibliografía |

## Reproducir
```bash
pip install -r requirements.txt
python -m pytest -q tests                      # 18 pruebas
cd simulador && python ejecutar_todo.py        # ~5 min: resultados 01-04 y figuras
python ejecutar_profundo.py                    # ~12 min: robustez, prueba a ciegas, aristas
```

Estructura:
- `simulador/piramide/`:
  - `geometria.py`: forma de la pirámide y estructuras internas;
  - `muones.py`: modelo de muografía;
  - `fisica.py`, `rampas.py`, `obra.py`, `montecarlo.py`: construcción;
  - `granito.py`: vigas de la Cámara del Rey;
  - `vacio.py`: hipótesis sobre el Gran Vacío y diseño de la medición;
  - `robustez.py`: ajuste conjunto, sistemáticos perfilados y prueba a ciegas;
  - `aristas_muones.py`: huella de las rampas integradas en las aristas.
- `datos/piramide_keops.json`: cada valor con su fuente.

## Honestidad
- **No afirmamos haber descubierto qué es el Gran Vacío.** Mostramos por qué no se ha podido saber y **qué medición concreta lo resolvería**, con las predicciones escritas de antemano.
- Los modelos son simplificados: posiciones internas con ±1–2 m de error, sin simulación completa con Geant4 y un modelo de flujo medio. Todas las limitaciones están en [docs/06](docs/06-metodo-y-validacion.md).
- Las ideas de partida no son nuestras: vienen de Houdin, Lehner, Rosell Roig y ScanPyramids. Lo que aportamos es el **marco cuantitativo y abierto** que las pone a prueba juntas.
