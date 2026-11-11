# Abastecimiento de depósitos

**Referencia:** requisitos en `docs/requirements.md`, mapa de propiedad en AC-102 y reglas de dependencias en AC-103.

Inventario registra piezas y aplica validaciones; el total de compra multiplica precio por cantidad; las reservas usan el API público; órdenes y facturación se coordinan desde aplicación. La confirmación de compra y el procesador de pago se invocan por interfaces.

La integración externa se realiza mediante contratos de aplicación. Los handlers de HTTP son adaptadores y no definen políticas propias.
