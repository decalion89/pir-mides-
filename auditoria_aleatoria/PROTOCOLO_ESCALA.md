# Protocolo de la segunda auditoría aleatoria: el dogma de la escala (registrado antes de leer ningún artículo)

**Fecha de registro:** 2 de noviembre de 2026. Este archivo y la muestra se suben a git **antes** de leer ninguno de los artículos de la muestra.

## Pregunta
En una muestra aleatoria de artículos de ciencia arqueológica, ¿qué fracción de las conclusiones que **pasan de un experimento o una medida a pequeña escala a un objeto, un sitio o un proceso a escala real** comprueba la semejanza (números adimensionales: Fourier, Damköhler, Biot, Péclet...)? ¿Y qué fracción **cambia** al aplicar la ley de escala?

## Muestra
- **Corpus:** el mismo que en [`PROTOCOLO.md`](PROTOCOLO.md), 225 artículos.
- **Muestra:** se excluyen los 40 de la primera muestra y se sacan 40 de los 185 restantes con `random.seed(20261102)` y `random.sample` en Python. Están en [`muestra_escala.csv`](muestra_escala.csv).

## Paso 1: aplicabilidad
Un artículo es **aplicable** si:
1. Una conclusión sobre un objeto, un sitio o un proceso real se apoya en un experimento, un ensayo o una medida hechos a otra escala espacial o temporal: probetas, réplicas, polvo, fragmentos, ensayos acelerados, modelos reducidos, simulaciones de laboratorio...
2. Esa diferencia de escala puede afectar a la conclusión porque hay un proceso de transporte, calor o reacción por medio.

## Paso 2: comprobación
Para cada artículo aplicable:
- se identifica el número adimensional pertinente;
- se calcula el factor de escala entre el experimento y el objeto, con intervalos;
- se indica si el artículo trata la escala.

Clasificación:
- **IGNORA Y CAMBIA:** no trata la escala, y aplicarla cambia la conclusión en un factor ≥ 3 en el ≥ 90 % de los casos.
- **IGNORA, NO CAMBIA:** no la trata, pero no altera la conclusión.
- **LA TRATA:** la justifica o la corrige.
- **INDETERMINADO:** faltan datos.

## Paso 3: resultado
Fracciones con intervalos de Clopper-Pearson. Sin sustituciones. Decisiones razonadas por escrito.
