# ADR 0011 — Responsabilidades de entrega y prioridad

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

El texto transportado y su urgencia tienen distintos propietarios.

## Decisión

La política de prioridad es `NoticePriority`, mientras `TelemetryNoticeService` solo envía el resultado.

## Consecuencias

Un cambio normativo de alertas no requiere editar conectores de mensajes.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
