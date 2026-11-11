# ADR 0007 — Separación de retención y reportes

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

La autoridad para borrar datos no es la misma que autoriza visualización histórica.

## Decisión

Solo operaciones explícitas de `RetentionService` pueden borrar; las consultas no modifican los datos.

## Consecuencias

Los reportes se mantienen reproducibles mientras el estado no cambie.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
