# ADR 0006 — Propietarios de decisiones operacionales

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

Planificación, tarifas, campañas, auditoría, mantenimiento, turnos y reportes tienen políticas diferentes.

## Decisión

Aplicar OWN-001–OWN-020 y dejar que los workflows coordinen servicios sin tomar sus decisiones.

## Consecuencias

Los cambios de política se concentran en el componente encargado.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
