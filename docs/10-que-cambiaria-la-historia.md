# 10 — Qué cambiaría la historia y cómo llegar ahí

## Lo que está en juego
Con la medición que proponemos en la Cámara del Rey, cada resultado posible enseña algo distinto:

| Si la medición dice... | Significaría |
|---|---|
| **H3, galería de contrapeso** | **La prueba más antigua conocida de elevación de cargas con contrapeso a gran escala.** Hoy, la primera imagen de un dispositivo de contrapeso, el cigoñal o *shaduf*, es un sello acadio de hacia 2200 a. C. En Egipto no aparece hasta la XVIII dinastía, hacia 1550 a. C. Una galería de contrapeso en Keops, hacia 2560 a. C., adelantaría esa tecnología unos 350 años en el mundo y unos 1000 en Egipto, y en una escala de decenas de toneladas. Además explicaría cómo se subieron las vigas de granito de la Cámara del Rey. |
| **H2, "segunda Gran Galería" inclinada** | Un espacio monumental gemelo de la Gran Galería y nunca visto. Abriría la pregunta de su función: ritual, de obra o funeraria. Sería el mayor hallazgo arquitectónico en la pirámide desde el siglo XIX. |
| **H1, corredor horizontal** | Un corredor horizontal sobre la Gran Galería. Encajaría mejor con un acceso o un espacio de obra que con un sistema de elevación. Descartaría la hipótesis del contrapeso. |
| **H5, cámaras apiladas** | Un sistema de descarga desconocido sobre la Gran Galería, comparable a las cámaras sobre la Cámara del Rey. Cambiaría lo que sabemos de la ingeniería estructural de la pirámide. |
| **H4, relleno suelto** | No hay espacio vacío: es una huella de la obra, por ejemplo un espacio de trabajo rellenado. Menos espectacular, pero cerraría el debate. |

En cualquiera de los casos, la pregunta abierta desde 2017 quedaría resuelta.

## Otro resultado que ya cambia el relato habitual
Del modelo de construcción ([07](07-resultados-construccion.md)) sale una conclusión firme: **con una sola rampa no daba tiempo.** Ninguna rampa de un solo carril con esquinas (zigzag, espiral o la rampa interna de Houdin) termina la obra en el reinado de Keops en ninguno de los 600 escenarios. Lo que limitaba no era la fuerza, ni el número de obreros: eran **los giros en las esquinas**.

La pirámide se construyó con un sistema **en paralelo**:
- o varios carriles a la vez, si girar una esquina costaba menos de ~6 min;
- o una rampa baja y palancas.

Ambas familias se pueden distinguir midiendo:
- **El tiempo de giro**, con arqueología experimental: un trineo de 2,5 t, un equipo de unas 20 personas y una esquina.
- **Muografía exterior de las aristas**: un detector de 1 m² al pie de una cara vería los carriles rellenos a 5σ en unos 300 días si el relleno es un ~5 % menos denso, o en 30 días si lo es un ~9 %. Ver la [figura 06](../figuras/06_huella_aristas.png) y `resultados/06_aristas.json`.

## Hoja de ruta para hacerlo realidad
1. **Simulación completa con Geant4** de los puestos KC (Cámara del Rey) y D5 (Cámara de Campbell), usando la geometría láser de ScanPyramids. El objetivo es confirmar los tiempos de exposición.
2. **Propuesta técnica** (borrador listo: [PROPUESTA_SCANPYRAMIDS_en.md](../PROPUESTA_SCANPYRAMIDS_en.md)): puesto, detector y exposición, con las firmas esperadas de cada hipótesis y el criterio de decisión registrado de antemano. Está en [PREDICCIONES.md](../PREDICCIONES.md).
3. **Contacto con los equipos de muografía**: Universidad de Nagoya (emulsiones), KEK (centelleadores), CEA (Micromegas), HIP Institute y Universidad de El Cairo. Las mediciones en la pirámide necesitan permiso del **Consejo Supremo de Antigüedades de Egipto**, y solo pueden hacerlas equipos autorizados.
4. **Experimento del tiempo de giro**, lo que se puede hacer fuera de Egipto: con un museo, una universidad o un grupo de arqueología experimental.
5. **Publicación del preprint** ([ARTICULO.md](../ARTICULO.md)) con el código abierto, para que otros lo revisen y lo critiquen.

## Lo que no podemos hacer nosotros
No podemos medir dentro de la pirámide. El paso que cambiaría la historia depende de que un equipo autorizado ejecute la medición. Nuestro trabajo consiste en hacer que esa medición sea **evidente, barata y difícil de ignorar**: un puesto público, detectores que ya existen, unas semanas de exposición y predicciones escritas antes de medir.
