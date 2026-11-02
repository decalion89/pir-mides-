# Protocolo de la auditoría aleatoria de "ceguera al ritmo" (registrado antes de abrir ningún artículo)

**Fecha de registro:** 1 de noviembre de 2026. Este archivo, el corpus y la muestra se suben a git **antes** de leer ninguno de los artículos de la muestra.

## Pregunta
En una muestra aleatoria de artículos de ciencia arqueológica, ¿qué fracción de las inferencias de mecanismo **que dependen de un ritmo físico** falla una comprobación de orden de magnitud con la geometría y los parámetros del propio artículo?

## Corpus
- **Consulta en Europe PMC:** `JOURNAL:"Sci Rep" AND (TITLE:archaeolog* OR TITLE:ancient OR TITLE:prehistoric OR TITLE:archaeometr*) AND OPEN_ACCESS:y AND PUB_YEAR:[2020 TO 2025]`.
- **Lista completa:** [`corpus.csv`](corpus.csv), ordenada por PMCID.
- **Muestra:** 40 artículos, `random.seed(20261101)` y `random.sample` en Python, guardados en [`muestra.csv`](muestra.csv).

## Paso 1: aplicabilidad (cribado)
Un artículo es **aplicable** si cumple las dos condiciones:
1. Infiere un **mecanismo físico, químico o biológico** (transporte, calor, flujo, almacenamiento, ingesta, degradación, emisión...) a partir de una medida, y la conclusión depende de que ese mecanismo actúe con cierta magnitud o en cierto tiempo.
2. Da, o permite obtener de fuentes estándar, los números necesarios para un cálculo de orden de magnitud: geometría, tiempos, concentraciones, flujos.

**No son aplicables**, entre otros:
- ADN antiguo, filogenias e isótopos de procedencia, salvo si infieren un mecanismo con ritmo;
- dataciones, tipologías y morfometría;
- teledetección sin mecanismo.

## Paso 2: comprobación
Para cada artículo aplicable se calcula el ritmo o la cantidad que exige el mecanismo y el máximo físico, con Monte Carlo sobre intervalos de parámetros justificados. El resultado se clasifica así:
- **FALLA:** el cociente afirmación / límite es ≥ 3 en el ≥ 90 % de los casos, o la conclusión principal no se sostiene.
- **CONDICIONAL:** solo se sostiene con un supuesto que el artículo no declara o no justifica.
- **PASA:** el mecanismo es físicamente posible con los parámetros del artículo.
- **INDETERMINADO:** faltan datos.

Se registra también si la objeción ya estaba publicada (búsqueda en internet).

## Paso 3: resultado
Se informará de:
- la fracción de artículos aplicables, con intervalo de confianza;
- la fracción que FALLA o es CONDICIONAL entre los aplicables, con intervalo de Clopper-Pearson.

No se sustituirán artículos de la muestra. Las decisiones de clasificación se razonarán por escrito. Los casos ya auditados que caigan en la muestra se contarán con su clasificación revisada.
