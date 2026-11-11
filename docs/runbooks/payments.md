# Runbook — Sustitución de pagos

Traducir el payload externo a `PaymentReceipt` en el adaptador. Comprobar importes no negativos y `accepted`, y validar con `SandboxPaymentGateway` antes del paso a un proveedor distinto.

## Verificaciones

Consultar los criterios pertinentes de `docs/requirements.md` y las reglas de `docs/architecture/03-layer-rules.md`. Conservar la separación entre casos de uso, mecanismos externos y presentación.
