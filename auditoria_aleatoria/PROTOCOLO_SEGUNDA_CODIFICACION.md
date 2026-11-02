# Protocolo de la segunda codificación ciega del censo (registrado antes de recodificar)

**Fecha de registro:** 2 de noviembre de 2026.

## Por qué
El censo ([`RESULTADO_CENSO.md`](RESULTADO_CENSO.md)) lo clasificó un solo codificador por artículo. Sus dos cifras centrales dependen de esa clasificación:
- el 9 % de artículos aplicables depende del criterio de aplicabilidad;
- el 43 % que no supera la comprobación depende de las clases.

Esta segunda codificación mide cuánto se sostienen.

## Datos
- [`clasificacion_corpus.csv`](clasificacion_corpus.csv): la clasificación original de los 225 artículos (censo + primera muestra), consolidada **sin cambios** desde las salidas de los cuatro bloques y de [`RESULTADO.md`](RESULTADO.md).
- [`segunda_codificacion.csv`](segunda_codificacion.csv): los artículos que se recodifican.
  - **Los 32 aplicables o límite**, todos.
  - **40 no aplicables** elegidos al azar entre los 193 (`random.Random(20261103)`), para medir los falsos negativos de aplicabilidad.
  - Total 72, barajados con la misma semilla y en 2 lotes de 36.

## Procedimiento
Dos codificadores nuevos (un lote cada uno), con estas condiciones:
- **Sin acceso** a la clasificación original, a los documentos del repositorio ni a la carpeta `simulador/censo/`.
- Solo reciben los criterios de [`PROTOCOLO.md`](PROTOCOLO.md), la lista del lote y el texto completo de Europe PMC.
- No saben qué fracción del lote es positiva.

**Limitación declarada:** los codificadores son modelos de la misma familia que el primero. El acuerdo mide la reproducibilidad del criterio, no la independencia de un experto humano.

## Medidas
1. **Aplicabilidad** (si / límite / no):
   - κ de Cohen con 3 categorías;
   - κ binaria con "si" frente a "límite o no", y con "si o límite" frente a "no";
   - falsos negativos entre los 40 "no" y su extrapolación a los 193, con IC.
2. **Clase** entre los artículos que ambos consideran aplicables o límite:
   - acuerdo en "no supera" (FALLA + CONDICIONAL) frente a "supera o indeterminado";
   - κ y matriz de confusión.
3. **Tasa corregida:** el 43 % recalculado con cada codificación y con la intersección (solo los casos en que ambas coinciden).

## Desacuerdos
Se publicarán todos.
- Los desacuerdos de clase en los casos FALLA o CONDICIONAL se resolverán con el cálculo propio ya publicado (`simulador/censo/`, documentos 38–41). Si el segundo codificador aporta un argumento nuevo, se recalculará.
- La cifra principal no se cambia sin documentar por qué.
