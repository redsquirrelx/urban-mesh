# ADR 0012 — Semántica homogénea de API

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

Los canales publican errores de estado y validaciones verificables.

## Decisión

Los recursos inexistentes se traducen a `404`, entradas inválidas a `422` y conflictos a `409`.

## Consecuencias

Los clientes interoperan sin conocer excepciones o respuestas internas.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
