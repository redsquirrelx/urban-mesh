# AC-109 — Verificación

## Estrategia

Las pruebas unitarias validan reglas deterministas, las pruebas de aplicación utilizan dobles de puertos, y las pruebas HTTP comprueban códigos y payloads. Las integraciones verifican que adaptadores alternativos respeten las mismas firmas y semánticas.

## Matriz por dimensión

- **Capas:** inspeccionar imports y dependencias alcanzables; tomar `bootstrap.py` como única excepción de ensamblaje.
- **Responsabilidades:** comparar cada servicio con OWN-001–OWN-020 y los efectos que realmente produce en un flujo.
- **Contratos:** probar sustitución de tarifa, pago, sensor, reparación y custodia con implementaciones equivalentes.
- **Invariantes:** cubrir límites 0, 8 caracteres, 20/60 de calidad, tiempo negativo y falta de stock.
- **Completitud:** contrastar los handlers publicados con los escenarios y códigos de `docs/requirements.md`.

## Comandos

```bash
python -m pip install -e '.[dev]'
pytest -q
python -m compileall -q src
```

Los snapshots de memoria usados en fixtures pueden leerse directamente desde tests; ese permiso no se extiende al código de producción.
