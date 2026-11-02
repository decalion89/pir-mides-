# 42 — El dogma de la escala: lo que ocurre en la probeta no es lo que ocurrió en el objeto

> **El dogma.** Muchas conclusiones de la arqueometría pasan de un experimento de laboratorio (miligramos en un calorímetro, una probeta de pasta de cal, un electrodo de 1 cm²) a un objeto real (un cerebro dentro de un cráneo, un muro de un metro, una punta de lanza) sin comprobar si los dos sistemas son **semejantes**. En ingeniería química nadie pasa del matraz a la planta sin igualar los números adimensionales. En arqueometría casi nunca se hace.
>
> **La transpolación.** Para los procesos de difusión y conducción, la semejanza exige el mismo **número de Fourier**, Fo = D·t/L². Un fenómeno que tarda t en una probeta de tamaño ℓ tarda t·(L/ℓ)² en un objeto de tamaño L. Los ritmos escalan al revés.
>
> **Lo que sale con nuestros casos** ([`simulador/ley_escala.py`](../simulador/ley_escala.py), [`resultados/51_ley_escala.json`](../resultados/51_ley_escala.json)):
>
> | Extrapolación | Factor de escala (L/ℓ)² | Consecuencia |
> |---|---|---|
> | **Cerebro de Herculano:** fragmento de calorímetro (0,5–5 mm) → cabeza (7–8 cm de radio) | ~3 000 (1 000–43 000) | El ritmo de 1 000 K/s del calorímetro equivale a ~0,3 K/s en el cráneo. **Coincide con el modelo térmico completo del doc. 35**: una sola ley predice el error |
> | **Cal orgánica:** pasta a los 7 días (probetas de 5–20 mm) → muro de 0,5–1 m | ~3 600 (1 100–18 500) | 7 días de probeta equivalen a **~70 años** de muro. Carbonatar el núcleo lleva ~175 años con cal aérea y ~2 000 años con cal hidráulica, aun con aditivos que dupliquen la velocidad. La "carbonatación más rápida" del laboratorio no explica la durabilidad del núcleo de los muros a la escala de vida del edificio |
> | **Polianilina:** inhibidor disuelto en el electrolito → recubrimiento sobre el objeto | (configuración) | El aporte de inhibidor no es comparable: es ilimitado en la disolución y finito en el recubrimiento. Sin espesor ni duración no se puede cuantificar |

## Qué es nuevo y qué no
- **No es nuevo:**
  - la semejanza dimensional, que es ingeniería de libro;
  - la dependencia de la escala en la meteorización mineral (Malmström et al.: en el campo es órdenes de magnitud más lenta que en el laboratorio);
  - las críticas a los ensayos de envejecimiento acelerado en conservación.
- **No lo hemos encontrado (búsqueda del 02/11/2026):** una comprobación sistemática de semejanza dimensional aplicada a las inferencias de mecanismo de la arqueometría.
- **La prueba que convierte esto en algo más que una idea:** la segunda auditoría aleatoria ([`auditoria_aleatoria/PROTOCOLO_ESCALA.md`](../auditoria_aleatoria/PROTOCOLO_ESCALA.md)).

## Límites
- **Fourier solo vale para procesos controlados por difusión o conducción.** Las reacciones limitadas por la cinética (Damköhler) o por el aporte requieren otras comparaciones.
- **Los coeficientes de carbonatación** son de la literatura general: ~1 mm/√día para la cal aérea, y 2–5 veces menos para la hidráulica.
