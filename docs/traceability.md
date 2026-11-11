# Matriz de trazabilidad

Esta matriz une requisitos públicos, propietarios y puntos de entrada previstos (rutas de código relativas a `src/urbanmesh/`). La referencia de implementación identifica dónde se mantienen contratos y flujos en producción; el requisito prevalece para definir el resultado observable.

| Requisito | Propietario funcional | Código de referencia (relativo a `src/urbanmesh/`) |
|---|---|---|
| REQ-001 | Plataforma | `presentation/api.py` |
| REQ-002 | Transporte | `presentation/api.py`, `infrastructure/storage/memory.py` |
| REQ-003 | Transporte | `presentation/api.py`, `infrastructure/storage/memory.py` |
| REQ-004 | Planificación | `application/journeys/planner.py` |
| REQ-005 | Planificación | `application/journeys/planner.py` |
| REQ-006 | Planificación / engagement | `application/journeys/planner.py`, `application/engagement/offers.py` |
| REQ-007 | Tarifas | `application/fares/quote.py`, `domain/policies/pricing.py` |
| REQ-008 | Tarifas | `application/fares/quote.py`, `presentation/api.py` |
| REQ-009 | Tarifas / auditoría | `application/fares/quote.py`, `application/operations/audits.py` |
| REQ-010 | Billetes | `application/ticketing/issuer.py` |
| REQ-011 | Billetes / campañas | `application/ticketing/issuer.py`, `application/engagement/campaigns.py` |
| REQ-012 | Billetes | `application/ticketing/issuer.py`, `presentation/api.py` |
| REQ-013 | Micromovilidad | `infrastructure/storage/memory.py`, `presentation/api.py` |
| REQ-014 | Alquileres | `application/rides/service.py`, `presentation/api.py` |
| REQ-015 | Alquileres | `application/rides/service.py`, `presentation/api.py` |
| REQ-016 | Alquileres | `application/rides/service.py`, `presentation/api.py` |
| REQ-017 | Alquileres | `application/rides/service.py`, `presentation/api.py` |
| REQ-018 | Alquileres | `application/rides/service.py`, `presentation/api.py` |
| REQ-019 | Alquileres | `application/rides/service.py`, `presentation/api.py` |
| REQ-020 | Políticas tarifarias | `domain/policies/pricing.py` |
| REQ-021 | Políticas tarifarias | `domain/policies/pricing.py` |
| REQ-022 | Políticas tarifarias | `domain/policies/pricing.py` |
| REQ-023 | Sustitución de tarifa | `application/payments/settlement.py`, `application/ports.py` |
| REQ-024 | Liquidación de pagos | `application/payments/settlement.py`, `infrastructure/gateways/payments.py` |
| REQ-025 | Liquidación de pagos | `application/payments/settlement.py`, `infrastructure/gateways/payments.py` |
| REQ-026 | Liquidación de pagos | `application/payments/settlement.py`, `infrastructure/gateways/payments.py` |
| REQ-027 | Tablero de salidas | `application/schedules/boards.py` |
| REQ-028 | Tableros / personal | `application/schedules/boards.py`, `application/operations/crew.py` |
| REQ-029 | Alertas | `application/alerts/dispatcher.py` |
| REQ-030 | Alertas / reparación | `application/alerts/dispatcher.py`, `application/operations/work_orders.py` |
| REQ-031 | Reportes de abordajes | `application/reporting/ridership.py` |
| REQ-032 | Reportes de abordajes | `application/reporting/ridership.py` |
| REQ-033 | Mantenimiento | `application/maintenance/triage.py`, `application/ports.py` |
| REQ-034 | Mantenimiento | `application/maintenance/triage.py`, `application/ports.py` |
| REQ-035 | Mantenimiento | `application/maintenance/triage.py`, `application/ports.py` |
| REQ-036 | Lecturas y calibración | `application/telemetry/processing.py`, `application/telemetry/calibration.py` |
| REQ-037 | Lecturas y calibración | `application/telemetry/processing.py`, `application/telemetry/calibration.py` |
| REQ-038 | Lecturas y calibración | `application/telemetry/processing.py`, `application/telemetry/calibration.py` |
| REQ-039 | Calidad | `domain/policies/quality.py`, `application/telemetry/quality.py` |
| REQ-040 | Calidad | `domain/policies/quality.py`, `application/telemetry/quality.py` |
| REQ-041 | Calidad | `domain/policies/quality.py`, `application/telemetry/quality.py` |
| REQ-042 | Urgencia / mensajes | `application/telemetry/notifications.py`, `application/telemetry/urgency.py` |
| REQ-043 | Custodia | `application/telemetry/custody.py`, `application/ports.py` |
| REQ-044 | Custodia | `application/telemetry/custody.py`, `application/ports.py` |
| REQ-045 | Custodia | `application/telemetry/custody.py`, `application/ports.py` |
| REQ-046 | Reporte de telemetría | `application/reporting/telemetry.py` |
| REQ-047 | Retención | `application/operations/retention.py` |
| REQ-048 | Inventario | `application/inventory/catalog.py`, `infrastructure/storage/memory.py` |
| REQ-049 | Inventario | `application/inventory/catalog.py`, `infrastructure/storage/memory.py` |
| REQ-050 | Inventario | `application/inventory/catalog.py`, `infrastructure/storage/memory.py` |
| REQ-051 | Inventario | `application/inventory/catalog.py`, `infrastructure/storage/memory.py` |
| REQ-052 | Inventario | `application/inventory/catalog.py`, `infrastructure/storage/memory.py` |
| REQ-053 | Inventario | `application/inventory/catalog.py`, `infrastructure/storage/memory.py` |
| REQ-054 | Inventario | `application/inventory/catalog.py`, `infrastructure/storage/memory.py` |
| REQ-055 | Inventario | `application/inventory/catalog.py`, `infrastructure/storage/memory.py` |
| REQ-056 | Inventario | `application/inventory/catalog.py`, `infrastructure/storage/memory.py` |
| REQ-057 | Abastecimiento | `application/procurement/checkout.py` |
| REQ-058 | Abastecimiento | `application/procurement/checkout.py` |
| REQ-059 | Promociones | `application/procurement/preview.py`, `infrastructure/gateways/promotions.py` |
| REQ-060 | Administración | `presentation/admin.py`, `application/inventory/catalog.py` |
| REQ-061 | Validación de credenciales | `domain/policies/validation.py` |
| REQ-062 | Pasajeros | `application/users/accounts.py` |
| REQ-063 | Pasajeros | `application/users/accounts.py` |
| REQ-064 | Encapsulación de inventario | `modules/inventory/api.py`, `modules/billing/service.py` |
| REQ-065 | Dependencias de módulos | `modules/inventory/allocator.py`, `modules/orders/service.py` |
| REQ-066 | Turnos | `application/operations/crew.py`, `application/schedules/boards.py` |
| REQ-067 | Informes / retención | `application/reporting/telemetry.py`, `application/operations/retention.py` |
| REQ-068 | Valoraciones de piezas | `application/inventory/catalog.py`, `presentation/api.py` |
| REQ-069 | Pedidos de suministros | `application/procurement/checkout.py`, `presentation/api.py` |
| REQ-070 | Listado de sensores | `infrastructure/gateways/sensors.py`, `presentation/api.py` |
| REQ-071 | Mantenimiento por activo | `application/maintenance/triage.py`, `presentation/api.py` |
| REQ-072 | Cuentas de pasajeros | `application/users/accounts.py`, `presentation/api.py` |
| REQ-073 | Reservas de stock | `application/inventory/allocator.py`, `presentation/api.py` |
| REQ-074 | Exportaciones | `application/reporting/ridership.py`, `presentation/api.py` |
| REQ-075 | Campañas | `application/engagement/campaigns.py`, `presentation/api.py` |
| REQ-076 | Presupuestos de compra | `application/procurement/quote.py`, `presentation/api.py` |
| REQ-077 | Consulta de presupuestos | `application/procurement/quote.py`, `infrastructure/storage/quotes.py` |
| REQ-078 | Excepciones de calidad | `application/telemetry/exceptions.py`, `presentation/api.py` |
| REQ-079 | Sustitución de calidad | `application/telemetry/quality.py`, `application/ports.py` |

## Dependencias documentales

- OWN-001–OWN-022 en `architecture/02-functional-ownership.md` establecen qué decisiones corresponde conservar juntas.
- AR-001–AR-012 en `architecture/03-layer-rules.md` indican dependencias y efectos permitidos.
- CT-001–CT-012 en `architecture/05-ports-and-substitution.md` establecen semántica sustituible.
- INV-001–INV-013 en `architecture/06-business-invariants.md` dan límites y restricciones de negocio.

La validación funcional utiliza escenarios y estados límite, además de la mera presencia de una ruta HTTP.
