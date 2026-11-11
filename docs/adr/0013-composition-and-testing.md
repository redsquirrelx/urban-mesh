# ADR 0013 — Composición y dobles de integración

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

El conjunto de adaptadores locales puede sustituirse por otros que cumplan Protocol.

## Decisión

Los casos de uso reciben dependencias mediante parámetros; tests construyen fakes para probar contratos.

## Consecuencias

Los cambios de infraestructura no invaden pruebas de dominio.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
