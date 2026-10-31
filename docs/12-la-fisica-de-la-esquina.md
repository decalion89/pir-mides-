# 12 — La física de la esquina: una conclusión que tuvimos que corregir

> **Resumen.** Nuestra conclusión más fuerte sobre la construcción era que *"ninguna rampa de un solo carril con esquinas termina a tiempo"*. Descansaba en una suposición que no habíamos comprobado: que girar un trineo en una esquina cuesta 2–15 minutos, con 5 como valor más probable. Al calcularlo desde la física, el giro cuesta **0,8–2,8 min** si se para y pivota, o **0,3 min** de ocupación de la esquina si se usa un **poste de reenvío**. En este segundo caso el equipo tiene que ser 1,4–1,9 veces mayor.
>
> Con esos valores, **una sola rampa con esquinas es posible, pero justa**: ocuparía casi todo el reinado de Keops. Los sistemas en paralelo siguen dejando años de margen. Retiramos la afirmación anterior.

Archivos: [`simulador/piramide/giro.py`](../simulador/piramide/giro.py), [`simulador/estudio_giros.py`](../simulador/estudio_giros.py), [`resultados/10_giros.json`](../resultados/10_giros.json), [`figuras/07_giros.png`](../figuras/07_giros.png).

## 1. Dos técnicas, dos físicas
**A. Parar y pivotar.**
- El equipo se detiene, el trineo se gira 90° con palancas y el equipo rodea la esquina antes de volver a tirar.
- Par de rozamiento de los patines: T ≈ μ·m·g·l/4 ≈ **2400 N·m** para un bloque de 2,6 t con μ = 0,15 y patines de 2,5 m.
- Girarlo 90° cuesta ~3,8 kJ. Seis palanqueros lo hacen en **~8 s**.
- **Lo lento no es girar**: es recolocar al equipo, unos 12 s para 23 personas, y sobre todo parar, calzar, tensar y arrancar (30–150 s).
- **Total: 0,8–2,8 min por esquina.**

**B. Poste de reenvío.**
- Un poste fijo en la esquina interior desvía la cuerda y el trineo avanza sin detenerse, guiado por el bordillo.
- Es la técnica que sugieren los **agujeros de poste de la rampa de Hatnub**, fechada en el reinado de Keops.
- El precio es el rozamiento de la cuerda contra el poste (ecuación del cabrestante): la fuerza se multiplica por e^{μ_c·π/2}, es decir **×1,4–1,9** con μ_c = 0,2–0,4.
- Hacen falta equipos mayores, y los trineos tienen que ir más separados.
- La esquina solo queda ocupada lo que el trineo tarda en recorrerla: **~0,3 min**.

## 2. Qué cambia en el veredicto
Monte Carlo de 400 escenarios ([`10_giros.json`](../resultados/10_giros.json)):

| Modelo | Suposición inicial (2–15 min) | Parar y pivotar | Poste de reenvío |
|---|---|---|---|
| Zigzag o espiral, un carril | 0 % / 0 % | 29 % / 74 % | 41 % / 80 % |
| Rampa interna de Houdin | 0 % / 0 % | 37 % / 85 % | 49 % / 85 % |
| Aristas, 4 carriles | 35 % / 59 % | 100 % / 100 % | 100 % / 100 % |
| Recta + zigzag | 6 % / 23 % | 98 % / 100 % | 96 % / 100 % |
| Recta + palancas | 100 % / 100 % | 100 % / 100 % | 100 % / 100 % |

*(Porcentaje de escenarios que terminan en ≤ 20 años / en ≤ 27 años, la duración del reinado.)*

La mediana de una sola rampa con esquinas queda en **20–23 años**. Es compatible con el diario de Merer, que muestra la obra todavía activa en el año 27 de Keops. Pero no deja margen para nada más: el templo, la calzada o las pirámides de las reinas.

## 3. El experimento que lo decide
Es arqueología experimental, sin permisos de Egipto, con un museo o una universidad. Los criterios están fijados **antes** de medir.

**Montaje**
- Un trineo de madera con un bloque de ~2,5 t.
- Una pista de tafla (arcilla) humedecida, con una pendiente del 10 %.
- Una esquina de 90° en una plataforma de 4 m de ancho.
- Un equipo de 20–25 personas.

**Medidas (10 repeticiones de cada)**
1. Fuerza de arrastre en recto, para obtener μ.
2. Tiempo que la esquina queda ocupada con la técnica A (parar y pivotar).
3. Tiempo de ocupación y fuerza adicional con la técnica B (poste de madera de ~25 cm). De ahí sale el rozamiento de la cuerda, μ_c.

**Criterios de decisión** (salen del simulador con los parámetros centrales):

| Resultado | Consecuencia |
|---|---|
| Técnica A en ≤ 1,55 min por esquina | Una sola rampa en zigzag termina en ≤ 20 años |
| Técnica A en ≤ 2,1 min (≤ 2,5 min para la rampa interna) | Una sola rampa termina dentro del reinado, en ≤ 27 años |
| Técnica B con μ_c ≤ 0,4 | Una sola rampa con postes termina en ≤ 20 años (19,5 años con μ_c = 0,4) |
| Técnica A en > 2,5 min y técnica B con μ_c > 0,5 | La rampa única queda descartada: hizo falta un sistema en paralelo |
| Rampas en las aristas | Viables si el giro dura ≤ 6,3 min (20 años) o ≤ 8,5 min (27 años) |

**Huella arqueológica que se puede buscar.** Si se usó la técnica B, en las esquinas de las rampas, o en las esquinas de la propia pirámide si las rampas iban apoyadas en ella, debería haber **agujeros de poste**. Son del mismo tipo que los de Hatnub.

## 4. Lo que aprendimos
Una conclusión "100 % segura" de un modelo es tan buena como su suposición más débil. El análisis de sensibilidad (ρ = 0,97) nos había dicho **cuál** era esa suposición. Lo que no habíamos hecho era **calcularla** en lugar de suponerla.
