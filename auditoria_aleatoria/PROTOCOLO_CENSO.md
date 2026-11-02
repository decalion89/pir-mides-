# Protocolo del censo de "ceguera al ritmo" (registrado antes de leer los artículos del censo)

**Fecha de registro:** 2 de noviembre de 2026.

## Objetivo
Medir con precisión la tasa de inferencias de mecanismo que no superan una comprobación de ritmo en el corpus completo. La primera auditoría aleatoria ([`RESULTADO.md`](RESULTADO.md)) solo encontró 7 artículos aplicables entre 40, con un IC del 10–82 %.

## Población
Los 185 artículos del corpus ([`corpus.csv`](corpus.csv)) que no estaban en la primera muestra, listados en [`censo.csv`](censo.csv) en 4 bloques. Se incluyen los 40 de la auditoría de escala, que allí se cribaron con otro criterio. Junto con la primera muestra, se cubre el corpus entero (225).

## Criterios
**Los mismos que en [`PROTOCOLO.md`](PROTOCOLO.md):** aplicabilidad, comprobación y las clases FALLA / CONDICIONAL / PASA / INDETERMINADO, con el umbral ≥ 3 en el ≥ 90 % de los casos.

**Además:**
- Los casos ya analizados (Tikal, filtro y mercurio, si están en el corpus) se cuentan con su clasificación revisada.
- **Verificación:** se recalcula con código propio todo caso propuesto como FALLA o CONDICIONAL. En los casos PASA se comprueban las citas en el texto completo.
- **Resultado:** tasa sobre los 225 (primera muestra + censo), con IC de Clopper-Pearson. No hay sustituciones.
