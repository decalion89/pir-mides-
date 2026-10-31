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
> **Revisión.** La versión original decía que "una rampa de un solo carril con esquinas no construye la pirámide a tiempo". Calculado desde la física, el giro cuesta 0,3–2,8 min, y con eso una sola rampa es posible pero justa. Los criterios de decisión actualizados están en docs/12, §3. El texto original se conserva debajo como registro.
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
- **en el plano vertical del eje de la Gran Galería**, a ±0,5 m;
- a una altura de **~56–66 m**;
- con una sección de **~10–13 m²**.

**Qué la refutaría**: un centro desplazado más de 1,5 m al este o al oeste del eje, o una sección menor de 6 m².

## P10 — Los canales siguen proporciones n/11, no las estrellas del reinado de Keops (doc. 14)
Una medición precisa (±0,2°) del tramo alto, hoy sin medir, del canal norte de la Cámara de la Reina debería dar **39,29° ± 0,3°** (pendiente 9/11), y no 39,8–39,9° (Kochab culminando en 2589–2566 a. C.). El canal sur de la Reina, medido en toda su longitud con láser, debería dar 39,29° y no 38,9–39,0° (Sirio en el reinado).

**Qué la refutaría**: ángulos de 39,8–39,9° (norte) y 38,9–39,0° (sur) en ambos canales a la vez. Eso apoyaría la orientación estelar en la época de Keops.
