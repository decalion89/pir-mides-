# 06 — Método y validación del simulador

Todo el código está en [`simulador/`](../simulador) y se reproduce con:

```bash
pip install -r requirements.txt
cd simulador && python ejecutar_todo.py        # ~20 min; --rapido para una versión corta
cd .. && python -m pytest -q tests             # 14 pruebas
```

## 1. Geometría (`geometria.py`)

- La pirámide es un sólido convexo: 4 caras a 51,84°, base de 230,33 m y altura original de 146,6 m. Para la muografía se usa la forma **actual**, cortada a 138,5 m y con ~1 m perdido en cada cara con el revestimiento.
- Las cámaras y corredores conocidos se reconstruyen encadenando longitudes y pendientes clásicas (Petrie, Maragioglio & Rinaldi). La reconstrucción da resultados coherentes con hechos independientes: la Cámara de la Reina cae sobre el eje este-oeste y el suelo de la Cámara del Rey a 43 m, al sur del centro.
  - Incertidumbre: ±1–2 m. Ver [`datos/piramide_keops.json`](../datos/piramide_keops.json).
- Cada estructura es un **paralelepípedo orientado** con su diferencia de densidad respecto a la caliza:
  - −2,2 t/m³ si es aire;
  - +0,55 t/m³ si es granito (bloque de la Cámara del Rey);
  - un valor intermedio si es relleno suelto.

## 2. Muografía (`muones.py`)

Para cada dirección vista desde un detector se calcula:

1. **La opacidad X** (g/cm²): densidad × longitud dentro de la pirámide, menos lo que atraviesa huecos y más lo que atraviesa granito.
2. **La energía mínima** para cruzarla: E_min = 0,5 GeV + (a/b)·(e^{bX} − 1), con a = 2,17 MeV·cm²/g y b = 4·10⁻⁶ cm²/g (roca estándar).
3. **El flujo integral** por encima de E_min, con el espectro de **Reyna (2006)**, que reproduce los ~70 muones/(m²·s·sr) verticales por encima de 1 GeV.
4. **Las cuentas esperadas** para un área, un tiempo de exposición y una rejilla angular (tanθx, tanθy).

La **significación** con que se distinguen dos configuraciones es:

χ² = Σ (N₁ − N₀)² / (N₀ + (0,02·N₀)²)

Tiene un 2 % de error sistemático por bin, suavizado con la resolución angular (~20 mrad), y se multiplica por un **factor de realismo de 0,5**.

### Validación frente a los datos publicados de ScanPyramids

| Magnitud | Modelo | Publicado | Comentario |
|---|---|---|---|
| Trazas en NE1 (98 días, 0,45 m², \|tanθ\|<1) | 5,3 millones | 4,4 millones | El modelo da un 20 % más; la diferencia es compatible con eficiencias y cortes |
| Exceso del Gran Vacío visto desde la Cámara de la Reina | 8,6 % (suavizado) | 5,2–11 % (KEK) | ✔ |
| Significación del Gran Vacío desde la Cámara de la Reina | 17σ | 13,7σ (NE1) | El modelo es algo optimista |
| Significación desde el exterior norte (2 × 0,25 m², ~60 días) | 2,8σ | 5,8σ (CEA) | El modelo es pesimista |
| Corredor de la cara norte visto desde el corredor descendente | 28 % de exceso, ≫10σ | ≫10σ | ✔ |

**Conclusión**: el modelo reproduce las tasas y los excesos medidos. Sus **significaciones son correctas hasta un factor ~2**, en ambos sentidos según el caso. Por eso, en los tiempos de exposición que damos ("días para 5σ"), la incertidumbre es de un factor ~4.

### Limitaciones conocidas
- No hay dispersión múltiple, fluctuaciones de pérdida de energía ni ruido de fondo de baja energía. Esto afecta sobre todo a las direcciones casi horizontales, que son las más largas.
- El sistemático del 2 % se trata como independiente bin a bin. Un sistemático **correlacionado**, como un error en la forma exterior, degradaría la sensibilidad a estructuras grandes y difusas más que a corredores nítidos.
- Las posiciones internas son aproximadas en ±1–2 m. No cambian las conclusiones cualitativas, pero sí los números exactos.

## 3. Construcción (`fisica.py`, `rampas.py`, `obra.py`, `montecarlo.py`)

### Física del arrastre
- **Fuerza para arrastrar un trineo**: F = m·g·(μ·cosθ + sinθ).
- **Calibración con la pintura de Djehutihotep** (172 hombres para ~58 t en llano): si cada persona tira con 200–350 N, el rozamiento es **μ ≈ 0,06–0,11**, coherente con la arena húmeda o una pista preparada (Fall et al. 2014). En el Monte Carlo se usa μ entre 0,08 y 0,30, con moda 0,15.

### Planificador hilada a hilada (210 hiladas de 0,7 m)
Para cada hilada, el ritmo de bloques al día es el **mínimo** de tres límites:

1. **Carriles**: el flujo de trineos por carril es la velocidad dividida por la separación entre equipos. Si hay giros, cada esquina atiende un trineo cada `t_giro` (un trineo cargado ocupa la esquina mientras gira).
2. **Colocación**: los equipos de colocación que caben en la superficie de la hilada.
3. **Mano de obra**: por la ley de Little, personas = ritmo × tiempo de ciclo × tamaño del equipo, sumando:
   - arrastre;
   - colocación;
   - cantera (0,3–1 m³ por persona y día);
   - construcción de rampas (1–4 m³ por persona y día);
   - elevaciones con palanca.

   Además se reserva un 30–50 % de la plantilla para apoyo: comida, agua, herramientas y barcos.

Al final se añade el **desmontaje de las rampas**.

### Modelos
| Clave | Modelo |
|---|---|
| `recta` | Una rampa frontal que crece con la pirámide |
| `zigzag` / `zigzag4` | Zigzag apoyado en una cara / en las cuatro |
| `espiral` / `espiral4` | Una espiral exterior / cuatro en paralelo |
| `interna` | Rampa exterior hasta 43 m + túnel interior en espiral (Houdin) |
| `aristas` | Cuatro carriles helicoidales integrados en las aristas (inspirado en Rosell Roig 2026) |
| `palancas` | Elevación hilada a hilada con palancas por las caras |
| `recta+zigzag`, `recta+palancas` | Híbridos: rampa recta hasta 45 m (67 % del volumen) y otro método por encima |

### Monte Carlo
Se toman 600 muestras de 20 parámetros inciertos, con distribuciones triangulares cuyos rangos están en `fisica.RANGOS`.

Un modelo se considera **viable** si cumple las dos condiciones:
- termina en ≤ 20 años con ≤ 25 000 personas;
- sus rampas no superan el 50 % del volumen de la pirámide.

## 4. Vigas de granito (`granito.py`)
Se comparan tres maneras de subir las vigas de granito hasta su altura:
- **Rampa**: tamaño y longitud del equipo de arrastre, y volumen de la rampa.
- **Contrapeso** en una galería inclinada: lastre necesario frente a lo que cabe en un vacío como el observado.
- **Palancas acompañando la subida del núcleo**: días por viga, comparados con el tiempo que tarda el núcleo en subir de 43 a 66 m.

## 5. Gran Vacío (`vacio.py`)
1. **Seis hipótesis** (H1–H6), cada una como un conjunto de cajas.
2. **Ajuste a los datos de 2017.** Para cada hipótesis se ajustan su parámetro de forma y su posición (dy, dz) hasta que su mapa visto desde la Cámara de la Reina se parezca lo más posible al del Vacío publicado. Se usan los datos esperados (Asimov), con la exposición de 2017. `Z_residual_QC` mide cuánto difiere todavía: si es < ~3–4σ, los datos de 2017 **no** pueden descartar esa hipótesis.
3. **Siete puestos posibles** para un detector nuevo. Para cada uno se calcula la significación con que separaría cada par de hipótesis en 100 días con 1 m², y los días necesarios para llegar a 5σ.
4. **Prueba independiente de la rampa interna de Houdin**: ¿se habría visto en los datos de la Cámara de la Reina de 2017?
