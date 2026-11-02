# 22 — Hasta dónde se puede explorar la Gran Pirámide sin tocar una piedra

> **Resumen.** Juntamos todas las sondas estudiadas y preguntamos qué parte del volumen se puede explorar para un hueco de 8 m (≥ 5σ) desde puntos que ya son accesibles, y qué queda fuera del alcance de la física no destructiva.
>
> | Paso | Volumen explorado | Base (0–20 m) |
> |---|---|---|
> | Hoy (14 campañas de muones, 2016–2020) | 34 % | 2 % |
> | + muones desde la Cámara Subterránea (1 m² × 100 d) | 53 % | — |
> | + microgravimetría en escalones, anillo y corredores (σ = 3 µGal) | 79 % | 63 % |
> | + muones en los pasajes bajo la base (corredor descendente en la roca y pasaje ciego sur; 4 × 1 m² × 100 d) | **84,5 %** | **70 %** |
> | + telescopios exteriores de 4–16 m² durante 1 año (corte de 80°) | ~86–88 % | ~72 % |
>
> **El ~12–15 % restante** está en la base de los lados este y oeste, a 40–75 m del eje. Ahí no hay ningún pasaje por debajo, la gravedad desde las caras no llega y los muones desde fuera topan con su límite: **multiplicar el área de los telescopios por 16 apenas mejora la cobertura**. Esa zona está limitada por la geometría y los sistemáticos, no por la estadística. Explorarla de verdad exigiría un acceso nuevo, como una perforación de pequeño diámetro para introducir un detector, o técnicas que hoy no existen.

Archivos:
- código: [`simulador/estudio_anillo.py`](../simulador/estudio_anillo.py), [`simulador/estudio_pasajes_bajos.py`](../simulador/estudio_pasajes_bajos.py);
- resultados: [`resultados/26_anillo.json`](../resultados/26_anillo.json), [`resultados/27_pasajes_bajos.json`](../resultados/27_pasajes_bajos.json).

## 1. Telescopios exteriores contra el anillo inferior
Un telescopio por cara, a 15 m de la base y a ras de suelo, apunta al centro del anillo inexplorado de esa cara (a 55 m del eje y 20 m de altura), con |tanθ| ≤ 0,6 y un año de exposición.

| Área por cara | Del anillo restante (cenit ≤ 70°) | Total | Del anillo restante (cenit ≤ 80°) | Total |
|---|---|---|---|---|
| 1 m² | 13 % | 81 % | 26 % | 84 % |
| 4 m² | 15 % | 82 % | 33 % | 86 % |
| 16 m² | 15 % | 82 % | 36 % | 86 % |

La cobertura casi no crece con el área. Mirando casi en horizontal a través de 100–200 m de piedra, un hueco de 8 m cambia el flujo menos que el 2 % de sistemático por bin, y el corte de cenit deja fuera las direcciones más bajas. Esto concuerda con el planteamiento del proyecto EGP (Bross et al. 2022), que propone telescopios de decenas de m² **en muchas posiciones** a lo largo de cada cara y un análisis tomográfico completo, no un solo punto de vista.

## 2. Muones desde los pasajes bajo la base
El corredor descendente sigue unos 30 m dentro de la roca hasta la Cámara Subterránea, y de esta sale hacia el sur un pasaje ciego de ~16 m. Son los únicos lugares accesibles por debajo de la pirámide.

| Puesto (1 m² × 100 d, mirando hacia arriba) | Del anillo restante |
|---|---|
| Corredor descendente a −5 m (y ≈ 58 m) | 2 % |
| Corredor descendente a −15 m (y ≈ 38 m) | 6 % |
| Corredor descendente a −25 m (y ≈ 18 m) | 9 % |
| Pasaje ciego al sur (y ≈ −23 m, z ≈ −28 m) | 18 % |
| **Los cuatro** | **28 %** (total 84,5 %) |

Lo que queda después: este 29 %, oeste 39 %, norte 15 %, sur 17 %.

## 3. Qué significa
- **Con lo que ya existe** (pasajes, cámaras, escalones y suelo alrededor) y técnicas probadas (emulsiones de Nagoya, gravímetros modernos), se puede explorar **~85 % de la Gran Pirámide** para huecos del tamaño de una cámara. Hoy está explorado el 34 %.
- **El orden con más rendimiento:**
  1. Cámara Subterránea (muones);
  2. escalones de las caras (gravedad);
  3. pasaje ciego sur y corredor descendente bajo (muones);
  4. telescopios exteriores.
- **El último ~15 % no es accesible sin crear un acceso nuevo.** Decirlo también es un resultado: marca el límite de lo que se puede conocer sin tocar el monumento.

## 4. Límites
- Todos los números heredan las suposiciones de los documentos 17 y 21: modelo de muones simplificado, 2 % de sistemático por bin, corte de cenit, 3 µGal por estación de gravedad y posiciones aproximadas de los pasajes.
- Los porcentajes de este documento usan la calibración conservadora (×0,44) para todas las emulsiones y telescopios propuestos.
- No se ha optimizado la orientación de cada detector. Inclinar los de los pasajes hacia los lados este y oeste podría cubrir algo más.
