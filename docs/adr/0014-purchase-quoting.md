# ADR 0014 — Cotizaciones y órdenes de aprovisionamiento

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

Cotizar una compra y realizarla son operaciones independientes.

## Decisión

La suma del total multiplica precio por cantidad; consultar un precio no reserva existencias; el checkout coordina pago y entrega con puertos.

## Consecuencias

Los informes y consultas de inventario son solo lectura.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
