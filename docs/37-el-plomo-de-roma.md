# 37 — El plomo del aire romano: el efecto sobre el cociente intelectual está sobrestimado entre 2 y 5 veces

> **El artículo.** McConnell et al. (*PNAS* 122:e2419630121, enero de 2025) tuvo eco mundial (Washington Post, Smithsonian, Big Think...). A partir de núcleos de hielo del Ártico y de un modelo atmosférico (FLEXPART) estiman que la minería y la fundición romanas elevaron el plomo del aire europeo **+1,04 ng/m³ de media**. Pasan del aire a la sangre con una regresión moderna:
>
> BLL = exp[1,932 + 0,140 · ln(PbA)], con PbA en µg/m³
>
> La regresión es de Richmond-Bryant et al. 2014, con niños de EE. UU. de 1988–94 (NHANES III). Con ella obtienen un **"aumento" de 2,4 µg/dl** (2,0–5,3) **sobre una base neolítica de 1 µg/dl**, y un déficit de **2,5–3 puntos de CI** en todo el Imperio.
>
> **Lo que encontramos.**
> 1. **Doble contabilidad.** La regresión predice la plombemia **total** de un niño estadounidense de 1988–94, con todas sus fuentes (pintura, polvo, dieta, agua). Es un modelo sin ajustar, y su constante recoge todo lo que no es el aire. Con aire casi limpio (0,03 ng/m³) predice ya 1,6 µg/dl. El artículo toma esa plombemia total como "aumento" debido al aire y le **suma** además la base neolítica.
> 2. **Extrapolación fuera de rango.** Los datos de calibración tienen medianas de plomo en el aire de ≥ 0,011–0,016 µg/m³. El aire romano medio, 0,001 µg/m³, queda 10–100 veces por debajo. En un modelo logarítmico la pendiente se dispara al bajar la concentración: a 1 ng/m³ implica **355 µg/dl por µg/m³**, frente a las pendientes establecidas de ~2–9 (OMS/ATSDR, incluidas las vías indirectas).
> 3. **Con su propia regresión bien aplicada,** es decir, la diferencia entre el aire romano y un fondo natural de 0,01–0,1 ng/m³, el aumento es de **1,0 µg/dl** (0,8–1,2) y el déficit de **1,4 puntos** (1,1–1,6): la mitad.
> 4. **Con un balance de ingesta desde cero** (inhalación, más el plomo depositado sobre los cultivos y el suelo con el depósito total del propio artículo, más los factores de pendiente para niños), el aumento es de **0,4 µg/dl** (0,12–1,4) y el déficit de **0,6 puntos** (0,2–1,8). El artículo lo supera **6 veces** (1,7–20).
>
> **Conclusión.** Que el plomo romano afectara a la población es plausible. Pero el "2,5–3 puntos de CI en todo el Imperio" está sobrestimado entre 2 y 5 veces por un error de método, no por los datos de hielo, que no discutimos. Cerca de las minas (hasta 157 ng/m³) el efecto pudo ser mayor. La media europea es la que está inflada.

Archivos: [`simulador/plomo_romano.py`](../simulador/plomo_romano.py), [`resultados/46_plomo_romano.json`](../resultados/46_plomo_romano.json).

## 1. Reproducción del artículo
Con su fórmula se reproducen sus cifras:
- 2,64 µg/dl a 1,04 ng/m³;
- 2,03 µg/dl a 0,16 ng/m³;
- 5,33 µg/dl a 157 ng/m³.

Con "−3,315·ln(BLL + 1)" y la base de 1 µg/dl, un aumento de 2,4 µg/dl da 2,6 puntos. Sus "2,0–5,3 µg/dl" son por tanto la **predicción total** de la regresión, no una diferencia.

## 2. La regresión de origen (Richmond-Bryant et al. 2014, *Environ. Health Perspect.* 122:754)
- **Datos:** participantes de NHANES III (1988–94) y de NHANES 1999–2008, con el plomo del aire medido en monitores de la EPA. Modelo de efectos mixtos ln–ln, *sin covariables demográficas*.
- **Coeficientes:** 1,932 y 0,140 son los de NHANES III para 1–5 años. Con NHANES 1999–2008 la pendiente es casi la mitad (0,076).
- **Rango:** mediana del plomo en el aire de 0,011–0,016 µg/m³ en 1999–2008, y mayor en 1988–94. Los propios autores advierten que en este modelo la pendiente crece al bajar la concentración.

## 3. Balance de ingesta (Monte Carlo, 200 000 casos)
| Vía | Hipótesis | Resultado (mediana; intervalo del 90 %) |
|---|---|---|
| Inhalación directa | 1–3 µg/dl por µg/m³ × 1,04 ng/m³ | 0,002 µg/dl |
| Depósito | 500–800 kt en 175 años sobre 3–6 millones de km² | 2,3 µg/m²/día |
| Plomo en vegetales | interceptación del 5–30 %, 0,5–3 kg/m², pérdida de 3–7 % al día | 4,7 µg/kg (1,3–17) |
| Dieta (0,3–0,6 kg de vegetales/día) | — | 2,1 µg/día (0,6–7,6) |
| Suelo (+1,9 mg/kg con 2–10 cm de mezcla; 50–200 mg/día) | — | 0,24 µg/día |
| De ingesta a sangre | 0,10–0,24 µg/dl por µg/día (ATSDR, niños) | — |
| **Aumento total** | | **0,39 µg/dl** (0,12–1,4) |
| **Déficit de CI** (modelo del artículo) | | **0,6 puntos** (0,2–1,8) |

## 4. Qué es nuevo y qué no
- **No es nuevo:**
  - los registros de hielo y el modelo atmosférico, que no discutimos;
  - las críticas de prensa, como que 3 puntos no es un "declive generalizado" o que el CI no se midió.
- **No lo hemos encontrado publicado (búsqueda extendida del 01/11/2026):**
  - la doble contabilidad de la constante de la regresión;
  - la extrapolación 10–100 veces por debajo del rango de calibración, con la pendiente implícita de 355 µg/dl por µg/m³;
  - el balance de ingesta independiente.

## 5. Límites
- **El fondo natural de plomo en el aire** (0,01–0,1 ng/m³) es una suposición. Con un fondo más bajo, la regresión diferenciada da algo más (hasta ~1,2 µg/dl).
- **El balance de ingesta usa promedios europeos.** Cerca de las minas y fundiciones, y con exposición laboral o doméstica (vajilla, agua de tuberías), la plombemia sería mucho mayor. El artículo trata solo la exposición rural por el aire, y es esa la que se critica aquí.
- **Los parámetros de interceptación y dieta son intervalos amplios,** y por eso el intervalo de 1,7–20 veces es ancho.
