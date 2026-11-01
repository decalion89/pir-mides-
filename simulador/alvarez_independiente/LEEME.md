# Reanálisis independiente de Alvarez (1970) — scripts exploratorios

Se ejecutan desde `simulador/` con `PYTHONPATH=. python alvarez_independiente/<script>.py`. Ver docs/27.
- `reconstruccion.py`: pirámide con remate y caras retranqueadas, aceptancia separable, términos radiales y diagnóstico del residuo.
- `triangulacion.py`: posición del detector que mejor ajusta las cuentas.
- `exclusion_independiente.py`: búsqueda de cámaras en el cono con el modelo propio (→ resultados/35_*.json).
- `prueba_del_candidato.py`: el "candidato" frente a la plantilla de Alvarez y a cambios del modelo.
