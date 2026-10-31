# 07 — Resultados: ¿cómo se pudieron subir 2,3 millones de bloques a tiempo?

Archivos: [`resultados/02_construccion.json`](../resultados/02_construccion.json), figuras [`02_construccion_anios.png`](../figuras/02_construccion_anios.png) y [`02b_tiempo_de_giro.png`](../figuras/02b_tiempo_de_giro.png). Método en [06](06-metodo-y-validacion.md).

## Resultado principal
Monte Carlo de 600 escenarios, con 20 parámetros inciertos. "Viable" significa terminar en ≤ 20 años con ≤ 25 000 personas y sin que las rampas superen el 50 % del volumen de la pirámide.

| Modelo | P(viable) | Años (mediana, rango 10–90 %) con 25 000 personas | Comentario |
|---|---|---|---|
| Rampa recta frontal hasta la cima | **0 %** | 8,6 (6,6–11,6) | Es rápida, pero la rampa tendría **1,85 veces el volumen de la pirámide** |
| Zigzag sobre una cara | **0 %** | 91 (53–155) | Un solo carril y ~70 giros |
| Espiral exterior (una) | **0 %** | 91 (53–155) | Igual: un carril con giros |
| Rampa interna de Houdin | **0 %** | 70 (44–115) | Túnel de un carril con giros |
| Zigzag en las 4 caras / 4 espirales / rampas en las aristas | **37 %** | 23 (13–39) | Viables solo si girar una esquina cuesta ≤ ~6 min |
| Recta hasta 45 m + zigzag | 4 % | 36 (23–56) | El tramo alto, de un carril, frena toda la obra |
| Palancas hilada a hilada | **100 %** | 7,5 (5,5–10,5) | Requiere caras escalonadas accesibles durante la obra |
| **Recta hasta 45 m + palancas** | **100 %** | 8,3 (6,5–11,1) | Bastan **~5100 personas** para acabar en 20 años |

## Cinco conclusiones

1. **Una sola rampa con esquinas no basta.** Cada giro de 90° de un trineo cargado ocupa la esquina varios minutos y limita el flujo a un bloque cada pocos minutos por carril. Con 2,3 millones de bloques eso supone **más de 40 años** en todos los escenarios simulados. Coincide de forma independiente con Rosell Roig (2025/2026), que estima ~50 años para una rampa única.
   - **Consecuencia:** la rampa interna de Houdin, tal como se propuso (un solo carril), **no cuadra con los tiempos**.
2. **El parámetro decisivo es el tiempo de giro.** La correlación de rangos entre el tiempo de giro y los años de obra es de **0,97** en los modelos con esquinas.
   - Las rampas en las aristas o en las cuatro caras terminan en 20 años solo si el giro dura **≤ 6,3 min**.
   - El zigzag de una cara y la rampa interna exigirían giros de **≤ 1,5 min**, lo que es poco realista con equipos de 20–25 personas.
   - **Esto se puede medir con arqueología experimental:** basta un trineo de 2,5 t, un equipo y una esquina de rampa de 3–4 m de ancho. Ver [PREDICCIONES](../PREDICCIONES.md).
3. **La mano de obra no es el cuello de botella.** Con los métodos viables bastan **~5000–9000 personas** para la obra en sí. Es coherente con un núcleo permanente de unos miles más una rotación amplia dedicada al apoyo (comida, agua, barcos, herramientas), como muestran el pueblo de los obreros y el diario de Merer.
   - **El problema real era el flujo**, no la fuerza bruta.
4. **Dos tercios (67 %) del volumen están por debajo de 45 m.** Una rampa recta y ancha hasta esa altura (~0,22 millones de m³, el 9 % del volumen) resuelve la mayor parte de la obra. El "misterio" se concentra en el tercio superior.
5. **Hay dos familias viables, con firmas distintas en la piedra:**
   - **Rampas múltiples en las caras o aristas**: deberían dejar bloques de relleno en las aristas y muescas en las esquinas, como la que señaló Bob Brier en lo alto de la arista noreste.
   - **Palancas**: no dejan huella interna, pero requieren caras escalonadas durante la obra y que el revestimiento se colocara al final.

   La muografía de las aristas, desde el exterior y a baja altura, podría distinguirlas.

## Límites
- Es un modelo de **flujo medio**, no de agentes individuales: no modela atascos, accidentes, el clima ni la crecida del Nilo.
- No incluye el transporte fluvial del revestimiento de Tura ni del granito de Asuán. El diario de Merer indica que iban por un circuito logístico aparte.
- La viabilidad de las palancas depende de dos datos poco medidos: el tiempo de elevación (8–30 min por hilada y bloque) y la posibilidad de trabajar en las caras durante la obra.
