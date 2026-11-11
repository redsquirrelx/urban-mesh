# Desarrollo local

## Entorno

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
uvicorn urbanmesh.presentation.api:app --reload
```

Los adaptadores locales se ensamblan en `src/urbanmesh/bootstrap.py`. La API predeterminada usa datos en memoria y no necesita secretos. La CLI se ejecuta con `urbanmesh routes`, `urbanmesh inventory`, `urbanmesh stations` o `urbanmesh ridership`.

## Reglas para nuevos casos de uso

1. Definir el requisito observable en `docs/requirements.md`.
2. Elegir el propietario de la política en `docs/architecture/02-functional-ownership.md`.
3. Declarar un puerto si se necesita un servicio externo.
4. Implementar decisiones puras en dominio; coordinar efectos en aplicación.
5. Implementar el adaptador de infraestructura y enlazarlo en `bootstrap.py`.
6. Mantener serialización y códigos HTTP en presentación.
7. Incorporar pruebas de dominio, contrato y API.

## Estructura de fuentes

`domain` es independiente de mecanismos externos; `application` usa puertos; `infrastructure` implementa esos puertos; `presentation` adapta HTTP/CLI. `modules` conserva APIs públicas de funciones de abastecimiento que consumen integraciones internas.

## Convenciones

El dinero se maneja con enteros en centavos; instantes con zona horaria; parámetros y rutas en `snake_case`; errores de negocio mediante `domain.errors`; respuestas HTTP según los códigos publicados. Las vistas de repositorio son snapshots, no referencias editables.
