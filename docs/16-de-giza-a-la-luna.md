# 16 — De Giza a la Luna: lo que las pirámides enseñan para construir fuera de la Tierra

> **Resumen.**
> - **La energía.** La energía mecánica total para construir la Gran Pirámide, elevando y arrastrando 5,7 millones de toneladas, fue de unos **2,5 GWh**. Es lo que produce una central de 100 MW en **~25 horas**.
> - **El rozamiento.** El **77 % se fue en vencer el rozamiento** del arrastre y solo el 23 % en elevar. Por eso la arena humedecida y las pistas preparadas fueron la tecnología clave.
> - **El tiempo.** El trabajo mecánico puro equivale a ~2 años de 5000 personas. El resto de los ~20 años fue cantería, logística y organización.
> - **En la Luna.** Las mismas cuentas para un blindaje de 50 000 m³ dan solo **4–6 MWh** de trabajo mecánico, el 97 % por rozamiento: 1–2 robots de 500 W en 2 años.
> - **La lección.** Construir con material local **no es un problema de energía**. Es un problema de rozamiento, de flujo (las esquinas) y de procesado del material.

Código: [`simulador/piramide/luna.py`](../simulador/piramide/luna.py).

## 1. El presupuesto energético de la Gran Pirámide
| Concepto | Valor |
|---|---|
| Masa colocada (2,6 millones de m³ × 2,2 t/m³) | 5,7 × 10⁹ kg |
| Elevar hasta el centro de masas (H/4 = 36,6 m) | 570 MWh |
| Arrastrar 450 m de llano más la rampa (μ = 0,15) | 1900 MWh |
| **Total** | **~2,5 GWh** |
| En jornadas humanas de trabajo mecánico (75 W × 10 h) | 3,3 millones, unos 2 años para 5000 personas |

**Implicaciones.**
1. **Ninguna energía misteriosa.** La Gran Pirámide cabe en un día de una central pequeña. No hace falta ninguna tecnología perdida para explicarla.
2. **El problema era el rozamiento.** Pasar de μ = 0,3 en arena seca a 0,15 en arena húmeda ahorraba cerca de 1 GWh, el equivalente a millones de jornadas de trabajo.
3. **El problema real era el tiempo y la organización**, no la fuerza. Coincide con el modelo de flujo (docs 07 y 12): el límite lo ponen los carriles y las esquinas.

## 2. La misma física en la Luna
Ejemplo: un blindaje contra la radiación de 50 000 m³ de regolito (~1,8 t/m³), con elevación media de 3 m y acarreo medio de 200 m. Es aproximadamente la capa de 3 m que necesitaría un asentamiento pequeño.

| | Luna (g = 1,62) | La misma obra en la Tierra |
|---|---|---|
| Trabajo mecánico, μ = 0,4 | 3,8 MWh | 23 MWh |
| Trabajo mecánico, μ = 0,6 | 5,7 MWh | 35 MWh |
| Robots de 500 W útiles, 35 % del tiempo activo, 2 años | **1–2** | — |

## 3. Cinco lecciones de Giza para construir en la Luna
1. **Reducir el rozamiento vale más que tener más potencia.** En la Luna no hay agua para humedecer la arena, así que su equivalente son ruedas, raíles o trineos sobre superficies compactadas. Es lo primero que hay que optimizar, porque el rozamiento es más del 95 % del trabajo.
2. **Usar material basto dentro y procesado solo fuera.** La pirámide tiene un núcleo de piedra basta y solo un revestimiento fino de caliza fina de Tura. Sinterizar o fundir regolito para hacer bloques cuesta mucha más energía que moverlo. Cada 0,1 kWh por kg de procesado supone ~9 GWh para estos 50 000 m³, que es **más de 1000 veces el coste de transporte**. Diseño recomendado: núcleo de regolito suelto o en sacos y una capa exterior procesada lo más fina posible.
3. **Flujo en paralelo, no fuerza.** El cuello de botella de una rampa con esquinas (docs 07 y 12) se repite con robots: un único camino de acceso con giros limita el ritmo, sea cual sea la potencia de cada robot. Conviene diseñar varios accesos o accesos sin giros.
4. **La mayor parte de la masa, abajo.** Dos tercios del volumen de una pirámide están en su tercio inferior. Las formas bajas y anchas minimizan la energía de elevación y facilitan el acceso por varios lados.
5. **Organizar antes que construir.** Lo que hizo posible la pirámide fue la logística (el diario de Merer, el pueblo de los obreros), no una máquina. Para una base lunar, el diseño logístico (rutas, ritmos, mantenimiento) pesará más que la potencia de cada robot.

## 4. Limitaciones
- Es un presupuesto de primer orden: no incluye la excavación ni el procesado, que son dominantes, ni la eficiencia de los motores. Los valores de rozamiento del regolito y de procesado son ilustrativos.
- Lo que hace es mostrar **dónde está el coste**. No sustituye un diseño de ingeniería.
