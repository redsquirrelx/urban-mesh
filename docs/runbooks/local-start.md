# Runbook — Inicio local

Instalar con `pip install -e ".[dev]"`, ejecutar `uvicorn urbanmesh.presentation.api:app --reload` y validar `GET /health`. Los datos de memoria se restablecen al reiniciar el proceso.

## Verificaciones

Consultar los criterios pertinentes de `docs/requirements.md` y las reglas de `docs/architecture/03-layer-rules.md`. Conservar la separación entre casos de uso, mecanismos externos y presentación.
