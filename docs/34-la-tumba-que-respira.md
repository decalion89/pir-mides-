# 34 — La tumba del Primer Emperador no puede estar sellada (si el mercurio sale de ella)

> **Pregunta.** Sima Qian (siglo I a. C.) escribió que la cámara funeraria de Qin Shi Huang tenía ríos y mares de mercurio. En 2016 un lidar midió mercurio atómico sobre el túmulo, con una emisión estimada de **~5×10⁻⁸ kg/s, unos 4 g al día** (Duan, Zhang y Svanberg, *Sci. Rep.* 2020). ¿Puede ese mercurio venir de la cámara, a ~30 m bajo el suelo y con un túmulo de 50 m encima? ¿Por qué camino?
>
> **Respuesta.**
> - **No puede salir por difusión a través de la tierra.**
>   - El flujo medido es **19–2 170 veces** (mediana 163) mayor que el máximo que permite la difusión desde una cámara saturada de vapor de mercurio. En 200 000 combinaciones de parámetros, ninguna basta.
>   - Ni siquiera un canal de **aire libre** con la superficie de todo el techo basta en el 88 % de los casos.
> - **La emisión del propio suelo del túmulo,** con 190 ppb de mercurio, se queda corta en un factor de 9 a 220. Haría falta un ritmo medio de ~1 400 ng/m²/h, propio de terrenos mineros.
> - **Lo que sí basta es que la tumba "respire":** que intercambie aire con la atmósfera por grietas. Haría falta un caudal de **~460 m³/día de aire saturado** (145–1 460). El bombeo barométrico del volumen del palacio subterráneo, es decir, cómo entra y sale el aire al subir y bajar la presión atmosférica, da ~1 400 m³/día. **Basta en el 93 % de los casos.**
>
> **Consecuencia.** Si el lidar mide bien y el mercurio viene de la tumba, **el palacio subterráneo no es una cápsula sellada**. Renovaría su aire en una escala de **~1–9 años**, con entrada de oxígeno y humedad. Eso importa para el estado de su contenido y para cualquier decisión sobre abrirla.
>
> **Prueba barata y decisiva:**
> - si la tumba respira, la emisión de mercurio debe **subir cuando baja la presión atmosférica**;
> - si la fuente es el suelo superficial, debe seguir al sol y a la temperatura del suelo.
>
> Basta con un analizador de mercurio portátil y un barómetro sobre el túmulo durante 2–4 semanas.

Archivos: [`simulador/qin_mercurio.py`](../simulador/qin_mercurio.py), [`resultados/42_qin_mercurio.json`](../resultados/42_qin_mercurio.json).

## Datos
| Magnitud | Valor | Fuente |
|---|---|---|
| Emisión de Hg del túmulo | 5×10⁻⁸ kg/s (incertidumbre ~×2) | Duan, Zhang y Svanberg 2020 (lidar DIAL, julio–agosto de 2016) |
| Mercurio en el aire sobre el túmulo | hasta 27 ng/m³ (fondo 5–10) | ídem |
| Cámara central | ~80 × 50 × 15 m; techo a ~30 m bajo el suelo circundante | ídem (de estudios geofísicos chinos) |
| Palacio subterráneo | ~140 × 110 × 30 m | ídem |
| Túmulo | ~380 × 330 m, ~50 m de alto | ídem |
| Hg en el suelo | media ~190–205 ppb, máximos de 1 440–2 204 ppb | Chang y Li 1983/85; Jin et al. 2008 (citados en Duan et al.) |

## Física
1. **Vapor saturado.** Si hay mercurio líquido expuesto, el aire de la cámara se satura: **C_sat ≈ 9,4 mg/m³** a 15 °C (8,1–11,0 mg/m³ entre 13 y 17 °C). Para reponer lo que sale bastan **~1–14 m² de mercurio expuesto**. La medición no puede distinguir unos charcos de unos "ríos".
2. **Difusión (cota superior).** F ≤ D_ef · C_sat · A / L, con:
   - A = 4 000–15 400 m² (de la cámara central a todo el palacio);
   - L = 30–80 m de tierra;
   - D_ef de Millington–Quirk, con porosidad 0,30–0,45 y saturación de agua 0,3–0,8: D_ef ≈ 2×10⁻⁸ … 1×10⁻⁶ m²/s.

   Es una cota generosa: supone estado estacionario y nada de adsorción, cuando el mercurio se adsorbe con fuerza en el suelo.
3. **Suelo.** Superficie del túmulo ~125 000 m², con 10–100 ng/m²/h, el intervalo típico de suelos con 0,1–1 µg/g según las síntesis de Gustin, Eckley et al.
4. **Advección.** Caudal necesario Q = F / C_sat. Bombeo barométrico: oscilaciones de presión del 1–2 % cada 3–7 días. En cada ciclo sale y entra esa fracción del volumen conectado.

## Resultados (Monte Carlo, 200 000 combinaciones; mediana e intervalo del 90 %)
| | Valor |
|---|---|
| Flujo máximo por difusión | 3×10⁻¹⁰ kg/s (3×10⁻¹¹ – 2×10⁻⁹) |
| Lidar / difusión | **163** (19 – 2 170); P(la difusión basta) = 0 |
| Lidar / canal de aire libre | 2,8 (0,7 – 11); P(basta) = 12 % |
| Lidar / suelo típico | 45 (9 – 220); P(basta) ≈ 0 |
| Caudal de aire saturado necesario | **460 m³/día** (145 – 1 460) |
| Bombeo barométrico del palacio (40 000 m³ de aire por ciclo) | 1 390 m³/día (840 – 2 380); P(basta) = **93 %** |
| Bombeo de la cámara central sola | 180 m³/día; P(basta) = 11 % |
| Renovación del aire del palacio | ~1 000 días (320 – 3 200) |
| Mercurio perdido en 2 200 años | 3,5 t (1,1 – 11) |
| Años para perder 100 t | ~60 000 (20 000 – 200 000) |

## Revisión con la presión real de la campaña (doc. añadido el 01/11/2026)
El Monte Carlo suponía oscilaciones de presión del 1–2 % cada 3–7 días. Con la presión real medida en Jinghe (WMO 57131, a 27 km) durante la campaña del lidar (24 jul – 12 ago 2016), ese supuesto resulta **optimista para el verano** ([`simulador/qin_presion_prerregistro.py`](../simulador/qin_presion_prerregistro.py), [`resultados/43_qin_prerregistro.json`](../resultados/43_qin_prerregistro.json)):
- **Rango de presión:** 998–1 009 hPa. Es una variación máxima del 1,1 % en 20 días, con desviación típica de 2,2 hPa.
- **Bombeo del palacio con solo la parte sinóptica:** ~**330 m³/día**, por debajo de los ~460 necesarios (0,7 veces).
- **Bombeo incluida la marea barométrica diaria** (2–3 hPa al día): ~**1 850 m³/día** (4 veces lo necesario). Pero la marea solo produce intercambio neto si el aire expulsado en cada ciclo (~0,2–0,3 % del volumen, ~1 000 m³) sale del todo del sistema de grietas y no vuelve a entrar. Eso depende del volumen de las grietas, que desconocemos.
- **El tiro térmico** tampoco ayuda en verano: el aire del túmulo (~15 °C) es más frío y denso que el exterior (30–35 °C) y se queda quieto. En invierno es al revés.

**Por tanto, la vía (a) sigue siendo la única que puede llegar al flujo medido, pero en verano va justa.** Esto da una predicción nueva: **si la tumba respira, en invierno debe emitir bastante más que en verano** (más bombeo sinóptico y tiro térmico a favor). Si una campaña invernal mide el mismo flujo o menos, la vía (a) pierde fuerza.

## Autocomprobación: ¿sobrestima el lidar el flujo?
Hacemos un balance de masa con los datos del propio artículo: flujo = exceso de concentración × viento × sección de la pluma.
- **Datos:** exceso de 12–18 ng/m³ (22–23 sobre el túmulo frente a un fondo de 5–10) y viento de 2,3–2,7 m/s en la cima.
- **Pluma:** de 10–30 m de alto (los autores suponen ~20 m) y de 150–380 m de ancho.
- **Resultado:** el balance da **1–3,5×10⁻⁷ kg/s**, 2–7 veces *más* que el 5×10⁻⁸ publicado. El valor publicado es conservador.

Por tanto, la vía (c) solo funcionaría si el **exceso mismo** no fuera real. Con la precisión declarada (±5 ng/m³), cada medida del exceso tiene 2,4–3,6σ. Hay varias exploraciones en dos emplazamientos, pero no se publica la serie completa. **El punto débil de la conclusión es la realidad del exceso, no el modelo de pluma.** Una medición independiente lo resolvería: un analizador puntual en la cima, o cámaras de flujo (P15).

## Qué significa
1. **La lectura habitual no se sostiene físicamente.** Se suele decir que el mercurio "se escapa lentamente a través del suelo". La difusión no puede producir el flujo medido.
2. **Tres posibilidades, y solo tres:**
   - **(a) la tumba respira:** hay intercambio de aire por grietas, movido por la presión atmosférica o la temperatura;
   - **(b) hay una fuente cerca de la superficie** mucho más rica que el suelo medio, como mercurio caído o vertido en el túmulo durante su construcción o en saqueos antiguos;
   - **(c) el lidar sobrestima el flujo en ≥ 10–100 veces.** El cálculo del flujo supone una pluma de ~20 m de alto.
3. **Los "ríos de mercurio" no quedan confirmados ni descartados.** Al ritmo medido se habrían perdido ~1–11 t en 2 200 años, así que unas 100 t seguirían ahí durante decenas de miles de años. Pero basta una superficie de unos pocos m² para explicar la emisión.

## Predicciones que distinguen (a), (b) y (c)
| Medición | (a) respira | (b) fuente superficial | (c) error del lidar |
|---|---|---|---|
| Hg en el aire o en el gas del suelo frente a la presión | **Sube cuando baja la presión** (retraso de horas) | Sin relación | — |
| Ciclo diario | Débil | **Fuerte** (sol, temperatura del suelo) | — |
| Perfil vertical del gas del suelo (sondas a 1–5 m) | **Crece con la profundidad** | Máximo cerca de la superficie | — |
| Cámaras de flujo sobre el túmulo | Puntos de salida localizados (grietas) | Repartido según el Hg del suelo | Flujo total ≪ 5×10⁻⁸ kg/s |
| Radón como trazador | Mismo ritmo barométrico que el Hg | Desacoplado | — |

La prueba (a) solo necesita un analizador portátil de mercurio (tipo Lumex) y un barómetro durante 2–4 semanas. No hay que excavar nada.

## Qué es nuevo y qué no
- **No es nuevo:**
  - la anomalía de mercurio en el suelo (años 80);
  - la medición con lidar (2020);
  - la idea de que el mercurio sale "por grietas", que el resumen de Duan et al. menciona de pasada.
- **No lo hemos encontrado publicado (búsqueda del 01/11/2026):**
  - la comparación cuantitativa con el límite de difusión;
  - la conclusión de que solo la advección (una tumba que respira) es compatible con el flujo medido;
  - la estimación del caudal (~460 m³/día);
  - la prueba barométrica para distinguir las hipótesis.

## Límites
- **Todo depende del flujo del lidar.** Viene de una campaña de tres semanas en verano y de un modelo de pluma. La conclusión es condicional: *si* el flujo es correcto y viene de la tumba, entonces respira.
- **Los ritmos de emisión de suelos con 0,1–1 µg/g varían mucho** con la humedad y la luz. Los puntos calientes (2 204 ppb) podrían cerrar parte de la diferencia de la vía (b).
- **La geometría de la cámara viene de prospecciones geofísicas resumidas en fuentes secundarias.** La profundidad se discute entre 20 y 50 m. Aun con L = 20 m, la difusión se queda corta en un factor ≥ 10.
- **El bombeo barométrico supone que el aire del palacio está conectado con el exterior por un camino permeable.** Es justo lo que se quiere probar.
