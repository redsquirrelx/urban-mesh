# Micromovilidad

**Referencia:** requisitos en `docs/requirements.md`, mapa de propiedad en AC-102 y reglas de dependencias en AC-103.

El alquiler tiene comienzo y fin validados. La cerradura confirma acciones antes de persistir estados. Los precios provienen de `FarePolicy` con montos finales; liquidación consume `PaymentReceipt` e ignora esquemas de proveedor. Mantenimiento recibe reportes por `RepairQueue`.

La integración externa se realiza mediante contratos de aplicación. Los handlers de HTTP son adaptadores y no definen políticas propias.
