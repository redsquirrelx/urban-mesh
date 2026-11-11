# ADR 0001 — Clean Architecture y dirección de dependencias

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

Las reglas de negocio se implementan en `domain/` y `application/`; infraestructuras y canales se conectan desde el exterior.

## Decisión

Aplicar AR-001, AR-002, AR-003 y AR-004 a todo el código de producción. `bootstrap.py` es la única raíz de composición.

## Consecuencias

La evolución de HTTP, memoria o procesadores no debe modificar políticas de negocio.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
