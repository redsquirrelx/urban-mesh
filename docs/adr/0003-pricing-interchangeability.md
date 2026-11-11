# ADR 0003 — Políticas tarifarias sustituibles

**Estado:** Aprobada. **Ámbito:** UrbanMesh 1.4.

## Contexto

La organización ofrece tarifa plana, por minutos y promocional bajo un único contrato.

## Decisión

Cada `FarePolicy.quote` genera `FareQuote` con precio final no negativo. Ningún consumidor interpreta deltas particulares.

## Consecuencias

Una política promocional se sustituye sin editar liquidación o checkout.

## Verificación

El diseño y sus restricciones se verifican mediante los requisitos de `docs/requirements.md`, las reglas de `docs/architecture/03-layer-rules.md`, los propietarios de `docs/architecture/02-functional-ownership.md` y los contratos de `docs/architecture/05-ports-and-substitution.md`.
