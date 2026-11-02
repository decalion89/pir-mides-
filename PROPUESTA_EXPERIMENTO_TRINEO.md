# Propuesta: ¿cuánto tarda un trineo de 2,5 toneladas en girar una esquina?

**Para:** grupos de arqueología experimental, departamentos de ingeniería o historia antigua, museos y parques arqueológicos.
**De:** Proyecto Pirámides (abierto e independiente): https://github.com/decalion89/pir-mides-
**Duración estimada:** 2–3 días de trabajo de campo · **Coste:** madera, cuerda, un bloque de piedra o de hormigón de ~2,5 t, arcilla y agua.

## La pregunta
¿Bastaba **una sola rampa** para construir la Gran Pirámide, o hicieron falta **varias a la vez**? Nuestro modelo de construcción (2,3 millones de bloques, simulados hilada a hilada en cientos de escenarios) muestra que la respuesta depende casi por completo de un solo número: **cuánto tiempo bloquea una esquina un trineo cargado al girar**. Ese número nunca se ha medido.

## El experimento
1. **Pista**:
   - 30 m de arcilla compactada y humedecida (tafla), con un 10 % de pendiente;
   - una esquina de 90° sobre una plataforma de 4 m de ancho;
   - bordillo exterior de madera o piedra.
2. **Trineo**: de madera, con patines de ~2,5 m, cargado con ~2,5 t.
3. **Equipo**: 20–25 personas en dos o cuatro filas de cuerda.
4. **Medidas**, con 10 repeticiones de cada una:
   - fuerza de arrastre en recto, con un dinamómetro en la cuerda, para obtener el coeficiente de rozamiento;
   - **técnica A, parar y pivotar**: el tiempo que la esquina queda ocupada, desde que el trineo entra en la plataforma hasta que sale por el otro lado;
   - **técnica B, poste de reenvío**: un poste de madera de ~25 cm en la esquina interior, como los agujeros de poste de la rampa de Hatnub (época de Keops). Se mide el tiempo de ocupación y la fuerza extra en la cuerda, de la que sale el rozamiento cuerda-poste.

## Criterios de decisión, fijados antes de medir
| Resultado | Qué significaría |
|---|---|
| Técnica A en ≤ 2,1 min por esquina | Una sola rampa en zigzag o espiral pudo construir la pirámide dentro del reinado de Keops (~27 años) |
| Técnica B con rozamiento cuerda-poste ≤ 0,4 | Una sola rampa con postes pudo terminarla en ≤ 20 años |
| Técnica A en > 2,5 min **y** técnica B con rozamiento > 0,5 | Una sola rampa no bastaba: hubo varias rampas a la vez, o palancas en la parte alta |

Los umbrales salen del simulador abierto (`simulador/estudio_giros.py`, `docs/12`). Cualquiera puede reproducirlos.

## Qué se publica
- Datos brutos (vídeos con marcas de tiempo y lecturas del dinamómetro).
- Coautoría para el equipo que haga la medición.
- El resultado, **sea cual sea**: incluido el caso en que contradiga nuestro modelo.

## Seguridad
Se trabaja con cargas de varias toneladas. Hacen falta un responsable de seguridad, calzos, una zona de exclusión alrededor del trineo y cuerdas certificadas, con margen de carga de al menos ×5.
