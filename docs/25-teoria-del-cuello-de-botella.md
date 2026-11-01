# 25 — Una teoría propia: el cuello de botella de las rampas

> **Teoría.** El techo de ~340 m³ de piedra al día que se repite en tres reinados (Snefru, Keops y Kefrén; doc. 23) **no lo ponía la riqueza del Estado ni el número de obreros, sino un límite físico de la logística**: cuántos trineos caben a la vez en las rampas y cuánto tarda cada uno en subir y girar.
>
> **Primera prueba.** El simulador de construcción del proyecto (doc. 07) se hizo días antes y para otra cosa. Con sus parámetros nominales, sin ajustarlos a este dato, los sistemas de rampas múltiples o híbridos tienen techos de **101 000–162 000 m³/año** (277–445 m³/día), y el techo histórico observado es de **85 000–150 000 m³/año**. Por encima de ~10 000 obreros, añadir gente no cambia el ritmo de esos sistemas: el límite son los carriles.
>
> **Estado:** compatible, no demostrada. Los parámetros del simulador, sobre todo el tiempo de giro en las esquinas, son inciertos, y la saturación por obreros es en parte una propiedad del modelo.

Archivos: [`simulador/teoria_cuello_de_botella.py`](../simulador/teoria_cuello_de_botella.py), [`resultados/30_cuello_de_botella.json`](../resultados/30_cuello_de_botella.json).

## Techos de cada sistema (geometría de Keops, 300 días de trabajo al año)
| Sistema de rampas | Techo (m³/año) | m³/día | Años mínimos para Keops |
|---|---|---|---|
| Una rampa en zigzag o en espiral | 41 000 | 111 | 63 (incompatible con el reinado) |
| Rampa interna (Houdin) | 52 000 | 144 | 50 (incompatible) |
| **Recta hasta 45 m + zigzag** | **101 000** | **277** | **26** |
| **Cuatro rampas (zigzag, espiral o aristas)** | **162 000** | **445** | **16** |
| Rampa recta frontal | 390 000 | 1 070 | 7 (descartada por volumen, doc. 07) |
| Palancas hilada a hilada | 930 000 | 2 550 | 3 (techo irreal: no limitada por carriles) |
| **Observado (Snefru, Keops, Kefrén)** | **85 000–150 000** | **~340** | **Keops: 23–27 años de reinado** |

## Predicciones arriesgadas (si la teoría es correcta)
1. **Ninguna pirámide grande se levantó más rápido que ~160 000 m³/año.** Keops necesitó ≥ 16 años y Kefrén ≥ 14. Encaja con sus reinados, de 23–27 y 24–26 años.
2. **Dentro de cada obra, el ritmo dependía de la altura y no del número de obreros.** Las hiladas bajas, más anchas, se pondrían más deprisa; las altas, más despacio, porque las rampas son más largas.
3. **La prueba decisiva: las marcas de obra fechadas de la pirámide Roja de Snefru.** Hay bloques con fechas pintadas en la base y en hiladas superiores. El tiempo entre ellas debe coincidir con lo que predice el cuello de botella para esas hiladas, o refutará la teoría. **Es la siguiente prueba**, y requiere localizar con precisión las fechas y alturas publicadas (Stadelmann; Krauss).
4. **Las otras pirámides** (la Roja y Kefrén) deberían tener techos parecidos a los de Keops con sus propias geometrías. Para comprobarlo hay que generalizar el simulador a otras pendientes y alturas.

## Por qué importa
Si se confirma, la pregunta "¿por qué nadie construyó más grande ni más rápido?" tendría una respuesta física y no solo económica. El límite estaba en la **ingeniería del transporte**, no en el número de brazos. Y el abandono de las pirámides gigantes tras Kefrén sería una decisión consciente de no seguir pagando una obra que, por mucha gente que se pusiera, no podía ir más deprisa.
