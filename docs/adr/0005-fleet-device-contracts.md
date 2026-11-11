# ADR 0005 — Aislamiento de equipos de flota

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

Las cerraduras y sensores son reemplazables por operadores de campo.

## Decisión

`LockGateway` devuelve acuse booleano; `SensorReader` entrega mediciones sin exponer configuración propietaria.

## Consecuencias

Cambiar marca de dispositivo no cambia casos de uso.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
