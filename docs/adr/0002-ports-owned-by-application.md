# ADR 0002 — Propiedad de puertos en aplicación

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

Las interfaces para repositorios, medios de pago, sensores y controladores se definen por necesidades de los casos de uso.

## Decisión

Centralizar puertos en `application/ports.py` y mantener los DTO de negocio en `domain/models.py`.

## Consecuencias

Las implementaciones de infraestructura se reemplazan por inyección.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
