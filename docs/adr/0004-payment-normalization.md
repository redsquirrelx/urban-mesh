# ADR 0004 — Recibo de pago independiente del proveedor

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

El proveedor de cobro puede cambiar de formato y estado de aprobación.

## Decisión

Cada adaptador traduce la respuesta externa a `PaymentReceipt`; el servicio consume `accepted` y `external_reference`.

## Consecuencias

Las respuestas `paid` o `id` quedan confinadas dentro del adaptador.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
