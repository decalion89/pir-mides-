# 09 — ¿Resiste el experimento decisivo? Ajuste conjunto y prueba a ciegas

> ⚠️ **Nota de la revisión independiente.** Estas pruebas a ciegas son **optimistas por construcción**:
> - los sistemáticos que se inyectan tienen la misma forma que los que el ajuste absorbe;
> - las "verdades" se generan dentro del rango de la biblioteca de variantes y solo con las formas H1–H5.
>
> Los "márgenes" son la raíz de la mediana de Δχ² entre hipótesis no anidadas, no significaciones gaussianas. Hay que leer los porcentajes como un **límite superior** de lo alcanzable.

> ⚠️ **Nota (doc. 13).** Aquí la Cámara de la Reina se modela como **un solo** detector. Con la configuración estéreo real de 2017 (NE1 + NE2, separadas 10,3 m), los datos completos identificarían la hipótesis correcta ~92 % de las veces, con un margen de ~3σ: más de lo que se dice aquí, aunque sigue sin ser decisivo. La Cámara de Campbell no aporta nada si el Vacío es horizontal, por el corte de cenit de 70°. **La Cámara del Rey es el puesto robusto.**

Archivos:
- código: [`simulador/piramide/robustez.py`](../simulador/piramide/robustez.py) y [`simulador/ejecutar_profundo.py`](../simulador/ejecutar_profundo.py);
- datos: [`resultados/05_robustez.json`](../resultados/05_robustez.json);
- figuras: [`05a`](../figuras/05a_prueba_a_ciegas.png) y [`05b`](../figuras/05b_acierto_vs_dias.png).

El documento 08 decía que un detector en la Cámara del Rey distinguiría las hipótesis. Aquí ponemos esa afirmación a prueba con un análisis mucho más duro.

## 1. Qué se endurece
1. **Las hipótesis rivales tienen todas las oportunidades de imitar los datos.** Cada una se representa con 225 variantes:
   - 3 valores de su parámetro de forma o cota;
   - posición desplazada ±3 m en norte-sur y en altura;
   - sección ×0,75–1,25, porque solo sabemos que es "comparable a la Gran Galería".

   Una hipótesis solo cuenta como descartada si **ninguna** de sus variantes encaja a la vez con lo visto desde la Cámara de la Reina en 2017 y desde el puesto nuevo.
2. **Sistemáticos correlacionados.** En cada puesto se ajustan libremente:
   - una normalización global (±5 %);
   - dos gradientes angulares (±5 %);
   - dos términos de espectro (±10 %), uno proporcional al espesor de roca y otro al ángulo cenital.

   Las cámaras conocidas ofrecen espesores muy distintos, así que la propia pirámide sirve para **autocalibrar** el flujo. Además hay un 2 % de error independiente por bin y una exposición efectiva de solo el 25 % de la nominal.
3. **Corte de cenit a 70°.** Los modelos de flujo casi horizontal no son fiables. La primera versión de esta prueba lo demostró: con el espectro de Gaisser, que no vale cerca del horizonte, el análisis fallaba en el 60 % de los casos.
4. **Prueba a ciegas.** Para cada hipótesis se generan 40 experimentos simulados:
   - la "verdad" se desplaza al azar ±1,5 m y su sección varía ±15 %;
   - se añaden ruido estadístico, sistemáticos aleatorios y, en algunos escenarios, **física distinta de la del análisis**.

   Después se comprueba qué hipótesis elige el análisis.

## 2. Resultados

### Separación esperada (sin ruido) entre la verdad y la mejor variante de la hipótesis rival
| Verdad | Solo 2017 (Cámara de la Reina) | + Cámara del Rey, 60 d | + Cámara de Campbell, 7 d |
|---|---|---|---|
| H1 horizontal | 2,3σ | **9,6σ** | 4,8σ |
| H2 inclinado | 2,6σ | **5,9σ** | **8,1σ** |
| H3 contrapeso | 2,4σ | **5,7σ** | **7,9σ** |
| H4 relleno | 11,4σ | 19,4σ | 12,0σ |
| H5 cámaras apiladas | 2,8σ | **10,2σ** | 6,0σ |

### Prueba a ciegas (200 experimentos por escenario)
| Escenario | Acierto | Margen mediano del par más difícil (H2 frente a H3) |
|---|---|---|
| Solo datos de 2017 | 89,5 % | ~2,2σ |
| + Cámara del Rey 60 d | **98,0 %** | ~5,0σ |
| ídem, flujo −10 % e índice +0,05 | **97,5 %** | ~4,4σ |
| ídem, flujo +10 % e índice −0,05 | **98,5 %** | ~5,6σ |
| ídem, caliza de 2,35 g/cm³ en vez de 2,2 | **98,0 %** | ~4,3σ |
| ídem, cámaras conocidas desplazadas 1 m | **96,0 %** | ~4,4σ (8 de 40 casos H3 se leen como H2) |
| ídem, espectro de Gaisser (caso extremo) | 82,5 % | H2 se lee como H3 en 35 de 40 casos |
| + Cámara de Campbell 7 d | **97,5 %** | ~5,1σ |

### Acierto según los días en la Cámara del Rey (1 m²)
| Días | 3 | 7 | 14 | 30 | 60 | 120 |
|---|---|---|---|---|---|---|
| Acierto | 94,7 % | 97,3 % | 98,7 % | 98,7 % | 98,7 % | 98,0 % |

## 3. Cómo leerlo
- **Con los datos de 2017, el análisis acierta a menudo, pero sin certeza.** El margen típico es de ~2σ, lo que no basta para afirmar nada. Así se entiende que ScanPyramids haya sido prudente.
- **Con la Cámara del Rey, el acierto sube al 96–98,5 % y el margen se acerca a 5σ** en todas las variaciones realistas de la física. Más allá de unas dos semanas de exposición, el acierto apenas mejora: el límite lo ponen los sistemáticos, no la estadística.
- **La conclusión más llamativa, H3 (contrapeso), es también la más delicada.** Con un error de flujo grosero, como usar Gaisser fuera de su validez, un corredor inclinado simple puede parecer una galería de contrapeso. Antes de proclamar H3 hay que hacer tres cosas:
  1. medir el flujo a cielo abierto con el mismo detector;
  2. usar la geometría láser exacta de las cámaras conocidas, porque un desplazamiento de 1 m ya degrada la separación H2/H3;
  3. confirmar con un segundo puesto, por ejemplo la Cámara de Campbell.

## 4. Límites que siguen ahí
- No hay simulación completa de transporte (Geant4). La dispersión múltiple y las fluctuaciones de pérdida de energía no están modeladas.
- La biblioteca de variantes es una rejilla: un análisis real ajustaría los parámetros de forma continua.
- La geometría interna es aproximada (±1–2 m). Hemos visto que eso importa para el par H2/H3.
