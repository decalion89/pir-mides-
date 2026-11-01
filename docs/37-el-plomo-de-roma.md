# 37 — El plomo del aire romano: el efecto sobre el cociente intelectual está sobrestimado unas 2–3 veces

> **Corregido el 01/11/2026 tras una revisión adversaria independiente.**
> - La regresión se calibró con NHANES III, cuya mediana de plomo en el aire es 0,036–0,037 µg/m³ (no 0,011–0,016, que es la de 1999–2008). El aire romano queda unas 35 veces por debajo.
> - Se cita la pendiente que dan los propios Richmond-Bryant et al. para aire con poco plomo: 15,3–16,5 µg/dl por µg/m³.
> - La regresión diferenciada se presenta también como extrapolación, no como "bien aplicada".
> - El balance de ingesta incluye ahora cereales (con el rendimiento romano) y agua de cisterna. El aumento sube de 0,4 a 0,7 µg/dl y la sobrestimación baja de ×2–5 a ×2–3.

> **El artículo.** McConnell et al. (*PNAS* 122:e2419630121, enero de 2025) tuvo eco mundial (Washington Post, Smithsonian, Big Think...). A partir de núcleos de hielo del Ártico y de un modelo atmosférico (FLEXPART) estiman que la minería y la fundición romanas elevaron el plomo del aire europeo **+1,04 ng/m³ de media**. Pasan del aire a la sangre con una regresión moderna:
>
> BLL = exp[1,932 + 0,140 · ln(PbA)], con PbA en µg/m³
>
> La regresión es de Richmond-Bryant et al. 2014, con niños de EE. UU. de 1988–94 (NHANES III). Con ella obtienen un **"aumento" de 2,4 µg/dl** (2,0–5,3) **sobre una base neolítica de 1 µg/dl**, y un déficit de **2,5–3 puntos de CI** en todo el Imperio.
>
> **Lo que encontramos.**
> 1. **Doble contabilidad.** La regresión predice la plombemia **total** de un niño estadounidense de 1988–94, con todas sus fuentes (pintura, polvo, dieta, agua). Es un modelo sin ajustar, y su constante recoge todo lo que no es el aire. Con aire casi limpio (0,03 ng/m³) predice ya 1,6 µg/dl. El artículo toma esa plombemia total como "aumento" debido al aire y le **suma** además la base neolítica.
> 2. **Extrapolación fuera de rango.** Los coeficientes son de NHANES III, con una mediana de plomo en el aire de 0,036–0,037 µg/m³. El aire romano medio, 0,001 µg/m³, queda unas **35 veces por debajo**. En un modelo logarítmico la pendiente se dispara al bajar la concentración: a 1 ng/m³ implica **355 µg/dl por µg/m³**. Las pendientes publicadas son de ~2–9 (OMS/ATSDR, incluidas las vías indirectas) y de **15,3–16,5** para aire con poco plomo según los propios Richmond-Bryant et al. Con 16 µg/dl por µg/m³, 1,04 ng/m³ aportaría 0,017 µg/dl.
> 3. **Su propia regresión, diferenciada** (aire romano menos un fondo natural de 0,01–0,1 ng/m³), da un aumento de **1,0 µg/dl** (0,8–1,2) y un déficit de **1,4 puntos** (1,1–1,6): la mitad. Sigue siendo una extrapolación muy por debajo del rango de calibración, así que es una cota orientativa, no un valor fiable.
> 4. **Con un balance de ingesta desde cero** (inhalación; plomo depositado sobre cereales y verduras, en el suelo y en el agua de cisternas, con el depósito total del propio artículo; factores de pendiente para niños), el aumento es de **0,71 µg/dl** (0,32–1,6) y el déficit de **1,0 puntos** (0,5–1,9). El artículo lo supera **3,4 veces** (1,5–7,5).
>
> **Conclusión.** Que el plomo romano afectara a la población es plausible. Pero el "2,5–3 puntos de CI en todo el Imperio" está sobrestimado unas 2–3 veces por un error de método, no por los datos de hielo, que no discutimos. Cerca de las minas (hasta 157 ng/m³) el efecto pudo ser mayor. La media europea es la que está inflada.

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
- **Rango:** mediana del plomo en el aire de **0,036–0,037 µg/m³** en NHANES III (1988–94), de donde salen los coeficientes usados, y de 0,011–0,016 µg/m³ en 1999–2008. Pendientes a bajo PbA según los autores: 15,3–16,5 µg/dl por µg/m³. Los propios autores advierten que en este modelo la pendiente crece al bajar la concentración.

## 3. Balance de ingesta (Monte Carlo, 200 000 casos)
| Vía | Hipótesis | Resultado (mediana; intervalo del 90 %) |
|---|---|---|
| Inhalación directa | 1–3 µg/dl por µg/m³ × 1,04 ng/m³ | 0,002 µg/dl |
| Depósito | 500–800 kt en 175 años sobre 3–6 millones de km² | 2,3 µg/m²/día |
| Cereal (grano 0,05–0,1 kg/m², interceptación 1–5 %, 30–70 % retenido tras limpiar y moler; 0,15–0,3 kg/día) | — | 8,8 µg/kg (2,9–23); 1,9 µg/día (0,6–5,4) |
| Verduras (interceptación 10–30 %, 1–3 kg/m²; 0,05–0,2 kg/día) | — | 0,55 µg/día (0,18–1,6) |
| Agua de cisterna (depósito ÷ lluvia de 400–900 mm; 0,5–1,5 L/día) | — | 1,3 µg/día (0,6–2,6) |
| Suelo (+1,9 mg/kg con 2–10 cm de mezcla; 50–200 mg/día) | — | 0,24 µg/día |
| De ingesta a sangre | 0,10–0,24 µg/dl por µg/día (ATSDR, niños) | — |
| **Aumento total** | | **0,71 µg/dl** (0,32–1,6) |
| **Déficit de CI** (modelo del artículo) | | **1,0 puntos** (0,5–1,9) |

## 4. Qué es nuevo y qué no
- **No es nuevo:**
  - los registros de hielo y el modelo atmosférico, que no discutimos;
  - las críticas de prensa, como que 3 puntos no es un "declive generalizado" o que el CI no se midió.
- **No lo hemos encontrado publicado (búsqueda extendida del 01/11/2026):**
  - la doble contabilidad de la constante de la regresión;
  - la extrapolación ~35 veces por debajo del rango de calibración, con la pendiente implícita de 355 µg/dl por µg/m³;
  - el balance de ingesta independiente.

## 5. Límites
- **El fondo natural de plomo en el aire** (0,01–0,1 ng/m³) es una suposición. Con un fondo más bajo, la regresión diferenciada da algo más (hasta ~1,2 µg/dl).
- **El balance de ingesta usa promedios europeos.** Cerca de las minas y fundiciones, y con exposición laboral o doméstica (vajilla, agua de tuberías), la plombemia sería mucho mayor. El artículo trata solo la exposición rural por el aire, y es esa la que se critica aquí.
- **Los parámetros de interceptación y dieta son intervalos amplios,** y por eso el intervalo de 1,5–7,5 veces es ancho.
- **A favor del artículo:** sus autores dicen que sus estimaciones son *"probably minimum"*, y el 96 % de los valores de plomo en esmalte dental romano supera 3,4 µg/dl. Pero el esmalte recoge todas las fuentes (vajilla, tuberías, vino), no solo el aire, y por eso no sirve para validar la atribución al aire.
