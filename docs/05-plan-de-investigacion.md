# 05 — Plan de investigación

No podemos excavar en Giza, pero sí podemos hacer **investigación original con datos públicos**. Propuesta por fases:

## Fase 1 — Modelo cuantitativo de construcción (código)
Un simulador en Python que compare los modelos de rampas:
- **Entradas**: geometría de la pirámide capa por capa, tamaño de los bloques, pendiente de la rampa, velocidad de arrastre, fricción (arena seca o húmeda, según Fall et al. 2014) y número de cuadrillas.
- **Salidas**: volumen de cada rampa, años de obra, personas necesarias y cuellos de botella (la cima es estrecha: ¿cuántos bloques caben por día?).
- **Pregunta concreta**: ¿qué modelos de rampa permiten terminar en ≤ 27 años con ≤ 25 000 personas?

## Fase 2 — Logística del diario de Merer
- Reconstruir a partir de los papiros los viajes Tura–Giza: duración, carga por barco y frecuencia.
- Estimar cuántos equipos como el de Merer hacían falta para el revestimiento.

## Fase 3 — Seguimiento de los misterios abiertos
Mantener un registro actualizado de:
- ScanPyramids (Gran Vacío, Micerino, muografía futura).
- El anuncio pendiente de Hawass (2026).
- Nuevas publicaciones sobre rampas, como *npj Heritage Science* o el *Journal of Egyptian Archaeology*.

## Fase 4 — Base de datos de afirmaciones
Una tabla de afirmaciones populares (vídeos y libros) evaluadas con la lista de [04](04-teorias-alternativas.md), con sus fuentes.

## Estructura propuesta del repositorio
```
/README.md
/docs/          ← estos documentos
/simulador/     ← código del modelo de rampas (Fase 1)
/datos/         ← medidas de las pirámides, cronología, datos de Merer
/afirmaciones/  ← base de datos de afirmaciones evaluadas
FUENTES.md
```

## Estado (31 de octubre de 2026)
- [x] **Fase 1, simulador de construcción.** Hecha: ver [07](07-resultados-construccion.md).
- [x] **Gran Vacío: modelo de muografía validado y diseño del experimento decisivo.** Ver [08](08-gran-vacio-y-experimento-decisivo.md).
- [x] **Registro de predicciones.** Ver [PREDICCIONES.md](../PREDICCIONES.md).
- [ ] **Fase 2, logística del diario de Merer** (circuito fluvial de Tura y Asuán).
- [ ] **Simulación con Geant4** de los puestos KC y D5, para confirmar los tiempos de exposición.
- [ ] **Modelo por agentes** de la circulación en rampas y esquinas.
- [x] **Física del giro en las esquinas** y protocolo experimental con criterios de decisión. Ver [12](12-la-fisica-de-la-esquina.md).
- [ ] **Experimento real del tiempo de giro** de un trineo cargado (P5), con un museo o una universidad.
- [x] **Firma muográfica de rampas en las aristas** (P6). Ver [10](10-que-cambiaria-la-historia.md) y `resultados/06_aristas.json`.
- [x] **Reanálisis de los datos publicados de 2017** (KEK y Nagoya). Ver [11](11-reanalisis-datos-2017.md).
- [ ] **Datos originales.** Pedir a ScanPyramids los mapas completos para resolver la tensión entre KEK y las emulsiones.
- [x] **Ajuste conjunto, sistemáticos correlacionados y prueba a ciegas.** Ver [09](09-robustez-y-prueba-a-ciegas.md).
- [ ] **Contacto con equipos de muografía** (ScanPyramids: Universidad de Nagoya, KEK, CEA, HIP Institute; Universidad de El Cairo) para proponer la medición desde la Cámara del Rey.
