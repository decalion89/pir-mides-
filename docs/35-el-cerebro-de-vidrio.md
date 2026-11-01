# 35 — El "cerebro de vidrio" de Herculano no pudo enfriarse a 1 000 K/s

> **Corregido el 01/11/2026 tras una revisión adversaria independiente.**
> - Se retira la atribución a Morton-Hayward et al. 2020 de un argumento sobre el ritmo de enfriamiento. Su texto completo (leído) no habla de enfriamiento: argumenta temperaturas más bajas (carbón a 240–370 °C) y la inestabilidad de los ácidos grasos.
> - Se responde al argumento de la fragmentación, que el propio artículo propone (§2b).
> - La energía para secar y calentar el cerebro es 2,96 MJ, no "~3,3 MJ". Los tiempos ya usaban el valor correcto.
> - Se sustituye la prueba propuesta, porque el material no se puede volver a medir tras el primer barrido.

> **El artículo.** Giordano et al. (*Scientific Reports* 15:5955, 2025; doi:10.1038/s41598-025-88894-5) tuvo eco mundial. Según los autores:
> - unos fragmentos vítreos negros de 0,5–5 mm, sacados del **interior del cráneo** de una víctima del Vesubio, son el cerebro convertido en vidrio;
> - el material pasó a vidrio a ~510 °C;
> - el cerebro se calentó por encima de 510 °C bajo una nube de ceniza diluida que duró "minutos";
> - al disiparse la nube, se enfrió *"at rates comparable with our experimental 1000 K s⁻¹"*.
>
> Citan para ese ritmo un estudio sobre partículas de ceniza que caen **libres en el aire** (Thomas y Sparks 1992). Después, depósitos de 315–465 °C enterraron el cuerpo.
>
> **Lo que dice la física, con los propios parámetros del artículo.**
> 1. **El enfriamiento dentro de un cráneo es de 0,1–1,7 K/s, no de 1 000 K/s:** entre 600 y 12 500 veces más lento. Ni siquiera un fragmento suelto en aire quieto llega a 1 000 K/s: da 17–720 K/s según su tamaño (5 a 0,5 mm).
> 2. **Con un ritmo físicamente posible, su propia cinética da una temperatura ficticia de ~405–440 °C, no 510 °C.** Esos valores se solapan con la temperatura de los depósitos que enterraron el cuerpo. Su argumento para descartar 420 °C ("comparable o menor que la temperatura de los depósitos") deja entonces de funcionar.
> 3. **Secar y calentar el cerebro por encima de 510 °C** exige **3–40 minutos** de exposición plena a una nube de 550–750 °C. Eso sin contar el límite de la conducción a través del cuero cabelludo y el hueso. Está al límite, o fuera, de una nube que dura "minutos".
> 4. **Con su propia energía de activación (390 kJ/mol), el material se ablanda en 0,4 s a 465 °C, en 3 min a 400 °C y en 13,5 h a 350 °C.** Para que el vidrio sobreviviera al enterramiento, el entorno del cráneo tuvo que quedarse por debajo de ~330–350 °C, el extremo inferior del intervalo. Además, a esas temperaturas el vidrio **se recuece en minutos u horas**: su temperatura ficticia actual reflejaría el enterramiento, no el paso de la nube.
>
> **Conclusión.** La medición calorimétrica puede ser correcta. Lo que no se sostiene físicamente es la historia térmica que se deduce de ella. Hay además un problema de método: los dos inicios (420 °C a 0,42 K/s y 510 °C a 1 000 K/s) son la transición vítrea del material **a cada ritmo de calentamiento**, de ahí sale precisamente su energía de activación. No miden el ritmo natural de enfriamiento. La equivalencia con 1 000 K/s es una suposición ("balanced thermal history"), no una medida.

Borrador de comentario en inglés: [`preprint/herculano/comment_en.md`](../preprint/herculano/comment_en.md), con la figura [`fig1_cooling.png`](../preprint/herculano/fig1_cooling.png).

Archivos: [`simulador/herculano_vidrio.py`](../simulador/herculano_vidrio.py), [`resultados/44_herculano_vidrio.json`](../resultados/44_herculano_vidrio.json).

## 1. Cinética del propio artículo
Los inicios de la relajación son 420 °C (C-DSC, 0,42 K/s) y 510 °C (F-DSC, 1 000 K/s). Con ln q = cte − (E/R)/T_f (Moynihan et al. 1976), salen:
- **E = 390 kJ/mol**, el valor que dan los autores (390,1);
- la temperatura ficticia en función del ritmo de enfriamiento:

| Ritmo de enfriamiento | 0,01 K/s | 0,1 K/s | 1 K/s | 10 K/s | 100 K/s | 1 000 K/s |
|---|---|---|---|---|---|---|
| T_f | 384 °C | 406 °C | 429 °C | 454 °C | 481 °C | 510 °C |

## 2. ¿A qué ritmo puede enfriarse el contenido de un cráneo?
**Modelo:** conducción radial en una esfera (7 cm de cerebro + 6,5 mm de hueso), que parte entera a 560 °C. Es la hipótesis más favorable para un enfriamiento rápido. En la superficie hay convección y radiación (ε = 0,9) hacia un ambiente a 40 °C, que es "the temperature immediately returned to ambient conditions".

| Hipótesis | Borde del cerebro | A 1 cm del hueso | Centro |
|---|---|---|---|
| Realista (k = 0,2 W/m·K, h = 10 W/m²K) | 0,41 K/s | 0,12 K/s | — |
| Generosa (k = 0,5, h = 25) | 0,74 K/s | 0,25 K/s | 0,08 K/s |
| Muy generosa (k = 1,0, h = 100: viento fuerte) | 1,7 K/s | 0,57 K/s | 0,17 K/s |

El ritmo se mide al cruzar 510 °C.

**Cota superior: un fragmento suelto en aire quieto**, sin cráneo (lo que describe la referencia 50 del artículo), con Nu = 2 y radiación:

| Tamaño | 0,5 mm | 1 mm | 2 mm | 5 mm |
|---|---|---|---|---|
| Ritmo a 510 °C | 720 K/s | 210 K/s | 66 K/s | 17 K/s |

Con viento fuerte (h = 200 W/m²K), un fragmento de 1 mm llega a 330 K/s.

**Resultado:** los fragmentos estaban dentro del cráneo, y allí el ritmo es **~0,1–2 K/s**. Aun suponiendo que el cerebro se hubiera fragmentado y los trozos quedaran expuestos al aire, solo los de ≤ 0,5 mm se acercarían a 1 000 K/s. Los fragmentos medidos miden 0,5–5 mm.

## 2b. ¿Y si el cerebro se fragmentó?
**Lo que dice el propio artículo:** el cerebro estaba *"severely damaged and disaggregated in small sub-centimetric pieces … favouring the heat exchange during cooling"*. Es su respuesta implícita al problema del enfriamiento. Hay que examinarla:
- **Fragmentos expuestos al aire libre:** se enfriarían a 17–720 K/s según el tamaño. Su propia cinética daría entonces T_f = **460–506 °C**, por encima del intervalo de los depósitos. En ese caso, el punto 2 de este documento no se sostendría.
- **Pero los fragmentos estaban dentro del cráneo:** *"sampled intact, directly from within the skull"*. Un fragmento dentro de una cavidad cerrada intercambia calor con gas y hueso que están a su misma temperatura. El calor tiene que salir igualmente a través del cráneo, así que los fragmentos se enfrían al ritmo de la cavidad (~0,1–2 K/s), por pequeños que sean.
- **El artículo usa la protección del cráneo en una sola dirección:** dice que *"the thick bones of the skull and spine … may have helped to prevent complete devolatilization"* durante el calentamiento. Esa misma protección frena el enfriamiento.
- **Conclusión:** el argumento de la temperatura ficticia vale si los fragmentos se enfriaron dentro del cráneo cerrado, que es donde se encontraron. Si el cráneo estuvo abierto y los fragmentos quedaron expuestos, deja de valer. Los puntos 3 (tiempo de calentamiento) y 4 (supervivencia durante el enterramiento) no dependen de esto.

## 3. ¿Cuánto tarda en calentarse el cerebro por encima de 510 °C?
**Planteamiento:** el cerebro pesa ~1,35 kg, con un 77 % de agua. Hay que calentar y evaporar el agua y llevar el resto a 510 °C: ~2,96 MJ. Se supone que **toda** la potencia que entra por la cabeza (convección + radiación de la nube, sobre 0,06–0,12 m²) llega al cerebro, sin límite de conducción. Es una cota inferior del tiempo.

| Nube | ε = 0,3, h = 30 | ε = 1, h = 100 |
|---|---|---|
| 550 °C | 20–39 min | 6–12 min |
| 650 °C | 14–29 min | 4–9 min |
| 750 °C | 11–22 min | 3–7 min |

Una nube diluida de "minutos" está en el límite, en el mejor de los casos.

## 4. ¿Sobrevive el vidrio al enterramiento?
Con E = 390 kJ/mol y τ ≈ (RT²/E)/q en el inicio medido:

| Depósito | Tiempo para ablandarse | Recocido si T_f = 510 °C | Recocido si T_f = 430 °C |
|---|---|---|---|
| 465 °C | 0,4 s | 0,06 s | 2 s |
| 400 °C | 3 min | 1,4 s | 43 s |
| 350 °C | 13,5 h | 22 s | 12 min |
| 315 °C | 50 días | 3,5 min | 1,8 h |

El recocido se calcula con el modelo de Tool–Narayanaswamy–Moynihan, con x = 0,5.

- **Los depósitos de Herculano tardaron días o semanas en enfriarse.** Para que el material no volviera a ablandarse, el entorno del cráneo tuvo que quedarse por debajo de ~330–350 °C.
- **A esas temperaturas, cualquier temperatura ficticia original se recuece en minutos u horas.** La señal calorimétrica actual no puede registrar el paso de la nube.

## 5. Qué queda en pie y qué no
- **No discutimos:** que el material sea vítreo, ni las medidas de DSC.
- **Lo que no se sostiene:** que de esas medidas se deduzca un enfriamiento de ~1 000 K/s y una temperatura ficticia natural de 510 °C. Tampoco que el escenario de la nube diluida sea "the only possible scenario". La física del calor dentro de un cráneo lo impide por 3–4 órdenes de magnitud.
- **Alternativas compatibles con la física:**
  - un sólido vítreo formado por **pirólisis lenta** (carbonización) del tejido, a temperaturas de enterramiento de ~300–350 °C y durante horas o días;
  - un vidrio cuya historia de enfriamiento real (~0,1–1 K/s) da T_f ≈ 405–430 °C.

  El artículo dice que *"subsequent upscans at the same rates did not exhibit any thermal events"*: el material se transforma en el primer barrido. Por eso no sirve el método clásico de igualación de áreas, que necesita volver a medir la misma muestra. La prueba posible es medir solo el primer barrido sobre varios fragmentos nuevos, a varios ritmos de calentamiento, y compararlos con vidrios de referencia de tejido preparados con ritmos de enfriamiento conocidos. Así se mide la T_f natural en lugar de suponerla.

## Qué es nuevo y qué no
- **No es nuevo:**
  - **Morton-Hayward et al. (2020, *STAR* 6:87–95)**, en respuesta a Petrone et al. (*NEJM* 2020), argumentaron temperaturas más bajas (carbón a 240–370 °C) y la inestabilidad de los ácidos grasos a esas temperaturas. No tratan el ritmo de enfriamiento.
  - Que los flujos piroclásticos se enfriaron despacio lo dicen los propios Giordano et al., y por eso proponen la nube previa.
  - Mauro dudó de que el tejido aguantara >510 °C. Otros dudan de que el material sea cerebro.
- **No lo hemos encontrado publicado** (búsqueda extendida del 01/11/2026; texto completo de Morton-Hayward et al. 2020 leído en White Rose):
  - un cálculo de transferencia de calor para el cráneo, aplicado al escenario de la nube de 2025;
  - la temperatura ficticia que corresponde a ritmos físicamente posibles;
  - el análisis de supervivencia y recocido con la propia cinética del artículo.

## Límites
- **Propiedades térmicas del tejido (seco o carbonizado) y del hueso:** se usan intervalos amplios. El resultado es robusto porque la diferencia es de 3–4 órdenes de magnitud.
- **Extrapolación cinética:** la ley de Arrhenius sale de solo dos puntos, y el valor de x de TNM no se conoce (se usa 0,5). Los tiempos de ablandamiento y recocido valen como órdenes de magnitud.
- **Geometría:** no sabemos si el cráneo estaba roto ni cuánta parte de la cabeza quedó expuesta. Ninguno de los dos casos lleva a 1 000 K/s dentro del cráneo.
