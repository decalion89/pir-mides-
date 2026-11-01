# 41 — La cal "orgánica" de Padmanabhapuram: el CO₂ del extracto no puede carbonatar el mortero

> **Cómo apareció.** Es el artículo n.º 6 de la [muestra aleatoria](../auditoria_aleatoria/RESULTADO.md). Lo marcó el cribado, y lo verificamos en la fuente y con código propio.
>
> **El artículo.** Shivakumar, Selvaraj y Dhassaih (*Sci. Rep.* 11:13261, 2021) preparan pastas de cal hidráulica NHL 2.5 con extractos vegetales fermentados, según una receta antigua del palacio de Padmanabhapuram (India). Afirman que el CO₂ de la fermentación (*"96,000 and 90,000 ppm on 4th day"*) produce la carbonatación interna: *"Supply of CO₂ has initiated the internal carbonation of the lime putty"*. Con ello se resolvería que *"internal core mortars remain un-carbonated for decades"*, y una *"higher carbonation rate … is the main reason behind longevity of the structure"*.
>
> **La comprobación.** Comparamos los moles de CO₂ que puede llevar el extracto con los moles de cal que habría que carbonatar.
> - **La cal:** Ca(OH)₂ es el 30–60 % de la NHL 2.5, es decir, 4–8 mol por kg de cal.
> - **El extracto:** 0,68–0,74 L por kg de cal, con el CO₂ disuelto en equilibrio con el espacio de cabeza medido (3,6–9,6 % de CO₂), hasta 10 veces sobresaturado. Para dar el máximo posible, se suma además la fermentación de **todo** el azúcar residual medido (16–6 867 µg/mL).
> - **Resultado:** el extracto puede carbonatar el **0,17 %** de la cal (mediana; 0,04–0,8 %; máximo absoluto 1,7 %). Con solo el CO₂ disuelto, el 0,08 %.
> - **Cociente:** carbonatación completa / máximo posible = **570** (130–2 450). Es ≥ 3 en el 100 % de los casos.
>
> Además, a pH ~12,5 la pasta de cal no permite que siga la fermentación. El CO₂ que aporta el extracto llega una sola vez, al mezclar. Los ppm medidos son concentraciones en el espacio de cabeza del fermentador, no cantidades de CO₂.
>
> **Conclusión.** Los carbonatos (calcita, aragonito, vaterita) observados por DRX en probetas pequeñas de laboratorio se explican por la carbonatación normal con el aire. El mecanismo propuesto, el CO₂ del extracto carbonatando el núcleo de muros de metros de espesor, es imposible por estequiometría en un factor de varios cientos. Los aditivos orgánicos pueden influir de otras maneras (forma de los cristales, porosidad, repelencia al agua), pero no aportando el CO₂.

Archivos: [`simulador/cal_organica.py`](../simulador/cal_organica.py), [`resultados/50_cal_organica.json`](../resultados/50_cal_organica.json).

## Qué es nuevo y qué no
- **No es nuevo:** que los aditivos orgánicos cambian las propiedades del mortero de cal, ampliamente documentado.
- **No lo hemos encontrado publicado (búsqueda del 01/11/2026):** un balance de masa del CO₂ aportado por los extractos frente a la cal disponible, ni una crítica de este artículo ni del siguiente de los mismos autores (*Buildings* 2022), que repite la idea de la absorción "interna" de carbono.

## Límites
- **El contenido de Ca(OH)₂ de la NHL 2.5 varía según el fabricante.** Con un 15 %, el máximo posible subiría a ~3 %, y seguiría muy lejos de una carbonatación completa.
- **No se considera CO₂ procedente del metabolismo de microorganismos dentro del mortero.** A pH 12,5 es despreciable.
