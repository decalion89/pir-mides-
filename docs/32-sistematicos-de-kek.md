# 32 — Ningún parámetro del instrumento KEK explica la tensión con las emulsiones

> **Pregunta.** En el ajuste conjunto, los datos publicados de KEK y de las emulsiones de Nagoya son incompatibles bajo un único corredor: Δχ² ≈ 70 (doc. 11). El doc. 31 descartó un desajuste entre los datos de KEK y su simulación. ¿La explica algún otro parámetro del instrumento KEK?
>
> **Una observación previa.** Los cocientes de KEK son "datos / simulación", así que las estructuras conocidas se cancelan. La posición absoluta del detector solo entra a través del Vacío, y mover los dos hodoscopios equivale a mover el Vacío en sentido contrario. Lo confirman los datos: el χ² de KEK sola apenas cambia (651–668) al mover el detector entre −2,5 y +1 m. Por eso la Gran Galería **no** puede fijar la posición absoluta de KEK, como sugerí al final del doc. 31. Esa propuesta era incorrecta.
>
> **Resultado.** Probamos uno a uno los cuatro parámetros, con valores mucho más allá de lo plausible:
> - posición este-oeste;
> - posición vertical;
> - separación H1–H2;
> - escala angular.
>
> **La tensión nunca baja de ~53.** Con márgenes plausibles para cada parámetro baja como mucho de 71 a ~58: unos 6σ para ~7 parámetros compartidos. **La tensión no viene del instrumento KEK.**

Archivos: [`simulador/sistematicos_kek.py`](../simulador/sistematicos_kek.py), [`resultados/40_sistematicos_kek.json`](../resultados/40_sistematicos_kek.json), [`resultados/log_sistematicos_kek.txt`](../resultados/log_sistematicos_kek.txt).

## Resultados
Tensión = χ²_conjunto − χ²_emulsiones solas (78) − χ²_KEK sola, con los errores reescalados como en el doc. 11. Valor nominal: **70,7**.

| Parámetro (nominal) | Valores probados | Tensión mínima (valor) | χ² de KEK sola en ese valor | Rango plausible → tensión |
|---|---|---|---|---|
| Este-oeste común (0) | −2,5 … +1 m | 58,5 (−0,5 m) | 665 (≈ igual) | ±1 m → ≥ 58 |
| Vertical común (0) | −1 … +2 m | 65,6 (+2 m) | 664 | ±0,5 m → ≥ 69 |
| Separación H1–H2 (2,9 m) | 2,3 … 4,0 m | 52,9 (3,5 m) | 670 (peor que 663) | ±0,1 m → ≥ 66 |
| Escala angular (×1) | ×0,85 … ×1,15 | 59,9 (×1,15) | 665 | ±3 % → ≥ 66 |

## Lo que sí se aprende
- **La altura del Vacío que da KEK depende casi por completo de la separación H1–H2.** Con 2,3 / 2,9 / 3,5 / 4,0 m sale z = 40 / 50 / 60 / 68 m: es la paralaje. Los 2,9 m publicados son, por tanto, un dato crítico para la altura que da KEK.
- **Al reducir la tensión, empeoran las emulsiones, no KEK.** En el ajuste conjunto, el χ² de las emulsiones nunca baja de 122, frente a 78 cuando se ajustan solas. KEK, en cambio, se ajusta casi igual de bien en todas las variantes. Las emulsiones son el conjunto que "no cabe".
- **Las emulsiones ya ajustaban mal por sí solas,** con χ²/ndf = 3,9: sus perfiles tienen estructura que ningún corredor describe. Puede venir de nuestra lectura de la figura (en el doc. 11 ya encontramos y corregimos un error de extracción) o de su procesado (normalización, perfil de la galería).

## Conclusión
- **Del lado de KEK quedan descartadas cinco explicaciones:**
  - el desajuste entre datos y simulación (doc. 31);
  - la posición este-oeste;
  - la posición vertical;
  - la paralaje;
  - la escala angular.
- **Lo que queda:**
  - una forma del Vacío más compleja que las tres probadas (doc. 11 §5b);
  - el lado de las emulsiones: nuestra digitalización o su normalización.
- **Prueba decisiva:** los perfiles originales de las emulsiones con sus errores. Es la primera petición de [la propuesta técnica](../PROPUESTA_SCANPYRAMIDS_en.md). Con ellos se sabría en un día si la tensión es real o de nuestra lectura.

## Límites
- **Un parámetro cada vez.** Combinar varios con valores extremos podría bajar algo más la tensión, pero con valores inverosímiles.
- **Datos leídos de las figuras.**
- **Un corredor recto** como forma del Vacío en todos los ajustes.
