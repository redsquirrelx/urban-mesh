# ADR 0009 — Encapsulación del inventario de depósitos

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

Los distintos flujos usan inventario sin conocer sus representaciones mutables.

## Decisión

Proveer métodos públicos/puertos para consultar y reservar; prohibir uso de `_store` por pedidos y facturación.

## Consecuencias

Se preservan invariantes y se evita acoplamiento circular.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
