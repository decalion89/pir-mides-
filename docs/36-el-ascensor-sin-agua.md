# 36 — El "ascensor hidráulico" de Djoser: el problema no es cuánta agua había, sino dónde guardarla

> **El artículo.** Landreau et al. (*PLOS ONE* 19:e0306690, 2024; eco mundial) proponen que la pirámide escalonada de Djoser se levantó con un flotador en el pozo norte, un pozo de 7 × 7 m y 28 m de profundidad.
> - **Agua necesaria:** sus propios cálculos dan hasta **18 Mm³** en 20–30 años.
> - **Aporte:** el Wadi Taflah podría aportar **4–54 Mm³** en ese periodo, en riadas episódicas.
> - **Conclusión de los autores:** comparando esos totales, el agua bastaría "con valores intermedios".
> - **Lo que dejan fuera:** su suplemento dice que las cifras *"do not account for water losses caused by infiltration and other factors"*. La evaporación no aparece en el artículo.
>
> **Lo que nadie había calculado: un balance hídrico día a día.** El agua llega en riadas y hay que guardarla hasta usarla. Lo simulamos con:
> - riadas de Poisson con el aporte que dan los autores;
> - su embalse de Gisr el-Mudir (220 000–440 000 m³, 1–2 m de profundidad) y la Deep Trench;
> - evaporación de 1,5–2,7 m/año e infiltración de 0,1–3 m/año.
>
> **Resultados.**
> 1. **Con los elementos que proponen los autores, el ascensor solo recibe el 27 % de su propia demanda** (mediana; 12–55 %). **Ni una sola de 1 500 simulaciones llega al 90 %.** Ni siquiera **sin** evaporación ni infiltración se llega: 37 % (16–72 %).
> 2. **El cuello de botella es el almacenamiento, no el volumen total:**
>    - una riada de un desierto llena el embalse en horas y **la mitad del agua se desborda** (mediana del 48 %);
>    - un embalse lleno de 1–2 m de profundidad **se seca en 4–30 meses** solo por evaporación e infiltración;
>    - el ascensor solo tendría agua en ~27 % de los días.
> 3. **La hipótesis solo funciona si se cumplen tres condiciones a la vez:**
>    - **un embalse profundo y estanco de escala de millones de m³** (por ejemplo, todo el Foso Seco lleno de agua, algo que el artículo no propone como embalse);
>    - **el uso optimizado del flotador** (rampas al principio y elevar e izar en cada ciclo, que los autores sugieren como posibilidad);
>    - **≥ 1–2 riadas al año** durante 20–30 años, en una meseta desértica.
>
>    Con las tres, se cubre el 88–99 %.
>
> **Conclusión.** El balance de volúmenes totales del artículo no basta para sostener la hipótesis. Para ser viable necesita un depósito de millones de m³ que retuviera agua durante décadas, y eso deja huella: **sedimentos lacustres laminados en el fondo del Foso Seco**. Es una predicción concreta y comprobable con un sondeo, en línea con lo que piden los propios autores en su respuesta de 2025.

Archivos: [`simulador/saqqara_balance_hidrico.py`](../simulador/saqqara_balance_hidrico.py), [`resultados/45_saqqara_balance.json`](../resultados/45_saqqara_balance.json).

## Datos del artículo (texto principal y suplemento S2)
| Magnitud | Valor |
|---|---|
| Agua para el ascensor (cota superior, flotador solo al llenar) | 18 Mm³; 0,6–0,9 Mm³/año durante 20–30 años |
| Ahorros posibles | Uso doble: −2/3. Rampa de 5–10 m: −25–43 %. Los primeros 20 m con rampas: "a few million" |
| Aporte de la cuenca de Abusir | 7 500–68 000 m³/año |
| Aporte del Wadi Taflah (si se desvía) | 0,2–1,8 Mm³/año (4–54 Mm³ en 20–30 años) |
| Una riada en Abusir | 75 000–225 000 m³ (50 mm de lluvia, escorrentía del 30 %) |
| Embalse de Gisr el-Mudir | 220 000–440 000 m³ con 1–2 m de profundidad |
| Deep Trench | > 14 000 m³; 27 m de profundidad, 3 m de ancho |
| Pérdidas | "no account for water losses caused by infiltration and other factors"; la evaporación no aparece |

## Modelo
Paso diario durante 20–30 años.
- **Riadas:** procesos de Poisson de 0,5–5 al año, con volúmenes exponenciales y media anual igual al aporte de los autores.
- **Embalse:** el agua que no cabe se pierde por rebose. El área mojada decrece con el volumen (orillas en pendiente: A ∝ √V), lo que favorece a la hipótesis.
- **Pérdidas:** evaporación de 1,5–2,7 m/año (aguas abiertas en el Egipto actual: ~2–2,7 m/año en el lago Nasser y ~1,8–2,2 m/año en El Cairo; se acepta algo menos por un clima algo más húmedo) e infiltración de 0,1–3 m/año (fondo con limo o con gravas).
- **Suministro:** la Deep Trench se rellena desde el embalse y alimenta al ascensor con una demanda constante.

Monte Carlo de 1 500 casos para cada demanda.

## Resultados
| Demanda | Cubierta, con pérdidas | Cubierta, sin pérdidas | P(≥ 90 %) con / sin pérdidas | Rebose | Evaporación | Infiltración |
|---|---|---|---|---|---|---|
| La de los autores (18 Mm³) | **27 %** (12–55 %) | 37 % (16–72 %) | **0 %** / 0 % | 48 % | 11 % | 3 % |
| Optimizada (6 Mm³) | 50 % (23–85 %) | 81 % (43–99 %) | 2 % / 33 % | 52 % | 19 % | 5 % |

**Fracción cubierta según el número de riadas al año** (valores centrales: aporte de 0,63 Mm³/año, evaporación de 2,1 m/año, infiltración de 0,5 m/año):

| Embalse / demanda | 0,25 | 0,5 | 1 | 2 | 5 |
|---|---|---|---|---|---|
| Gisr el-Mudir / autores | 7 % | 12 % | 22 % | 34 % | 53 % |
| Gisr el-Mudir / optimizada | 14 % | 23 % | 41 % | 60 % | 84 % |
| Foso Seco entero (3,5 Mm³, 20 m) / autores | 39 % | 50 % | 62 % | 66 % | 74 % |
| Foso Seco entero / optimizada | 63 % | 73 % | 88 % | 94 % | 99 % |

**Embalse lleno de Gisr el-Mudir sin nuevos aportes:** se seca en 4–15 meses con 1 m de profundidad y en 8–30 meses con 2 m.

## Predicción comprobable
Si el ascensor funcionó, el sistema tuvo que retener agua durante décadas en un depósito profundo de millones de m³. **En el fondo del Foso Seco o de la Deep Trench debe haber limos lacustres laminados**, con capas anuales o por riada. Las gravas de riada sueltas no bastan. Si un sondeo no los encuentra, la hipótesis pierde su único escenario viable.

## Qué es nuevo y qué no
- **No es nuevo:**
  - las objeciones arqueológicas (Monnier, Budka, Kuraszkiewicz: bloques pequeños, falta de pruebas, esfuerzo excesivo);
  - el cálculo del agua necesaria, que es de los propios autores.
- **No lo hemos encontrado publicado (búsqueda extendida del 01/11/2026):**
  - un balance hídrico con almacenamiento, rebose, evaporación e infiltración;
  - el resultado de que el volumen total no es la restricción, sino el almacenamiento;
  - las tres condiciones necesarias para que la hipótesis funcione.

## Límites
- **El clima del Imperio Antiguo es incierto.** Si hubo varias riadas al año y la evaporación era menor, la hipótesis mejora. Por eso damos las curvas en función del número de riadas.
- **La geometría de los depósitos es la del artículo.** Si existieran depósitos estancos mayores sin descubrir, el resultado cambiaría. Esa es justo la predicción.
- **Demanda constante.** Concentrar la obra justo después de las riadas ayudaría algo, pero no al ritmo de una obra de 20–30 años con riadas aleatorias.
