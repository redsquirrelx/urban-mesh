# ADR 0010 — Taxonomía compartida de calidad

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

Las reglas de calidad se ejecutan sobre sensores de flota y estaciones.

## Decisión

El contrato es `accepted`, `hold` o `rejected`; límites 20 y 60 inclusivos.

## Consecuencias

Un proveedor puede cambiar de algoritmo sin cambiar a consumidores.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
