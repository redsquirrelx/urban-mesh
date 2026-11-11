# AC-105 — Puertos, contratos y sustituibilidad

**Estado:** Aprobado. Los Protocol de `application/ports.py` definen dependencias estables. Una implementación alternativa es válida si puede sustituirse por inyección sin editar el consumidor, sin consultar tipos concretos y sin modificar los valores semánticos esperados.

| ID | Puerto | Contrato obligatorio |
|---|---|---|
| CT-001 | `RouteSource` | `get`, `all_routes`, `connecting` entregan valores `Route` y duraciones coherentes |
| CT-002 | `BicycleCatalog` | `find` retorna `Bicycle | None`; `available_at` retorna colección separada del almacenamiento |
| CT-003 | `LockGateway` | `unlock/lock -> bool`; `False` significa que el dispositivo no confirmó la acción |
| CT-004 | `RideRepository` | `save` y `find`; la aplicación no conoce tablas, IDs internos ni mapas |
| CT-005 | `FarePolicy` | `quote(Ride) -> FareQuote` final en centavos, `amount_cents >= 0`, referencia correcta; no requiere combinación especial por tipo de política |
| CT-006 | `PaymentGateway` | `capture(FareQuote) -> PaymentReceipt(reference_id, external_reference, amount_cents, accepted)`; no expone respuesta de procesador |
| CT-007 | `RepairQueue` | `enqueue(RepairTicket) -> None`; almacenamiento y estructura mutable son privados |
| CT-008 | `SensorReader` | `read(sensor_id) -> SensorReading`; no se requieren atributos específicos de dispositivo |
| CT-009 | `QualityRule` | `assess(SensorReading) -> str` en `{accepted, hold, rejected}`; mismo umbral y significado acordados |
| CT-010 | `CustodySink` | `append(event)` y `list_events()` devuelven objetos `CustodyEvent`; CSV es responsabilidad del exportador |
| CT-011 | `RetentionStore` | `list_before(cutoff)` no muta; `delete_before(cutoff)` elimina solo al ejecutar comando explícito |
| CT-012 | `InventoryCatalog` | Consultas públicas no exponen `_items`; escritura es atómica respecto del catálogo y aplica invariantes |

## Tarifas

La cotización para una política promocional es el **importe final**, nunca un descuento negativo. Con `discount_cents = 50` y una tarifa base de `250`, la política promocional configurada con dicha base debe devolver `200`. Las políticas alternativas se conectan por el mismo constructor de liquidación sin condicionales por clase.

## Procesadores de pagos

Los adaptadores `ProcessorPaymentAdapter` y `SandboxPaymentGateway` deben ser intercambiables. Para un cargo aprobado de `240`, ambos producen `PaymentReceipt` con `accepted=True`, `amount_cents=240` y referencia externa no vacía. La respuesta de `LocalProcessorClient` (`paid`/`id`) permanece dentro de infraestructura.

## Sensores

`FleetSensorReader` y `PartnerSensorReader` implementan la misma interfaz; la selección de proveedor se hace en composición. El factor de calibración es una política independiente y no un atributo obligatorio del lector. Una sustitución no debe producir `AttributeError`.

## Colas de mantenimiento y cadena de custodia

Los consumidores invocan `RepairQueue.enqueue` y `CustodySink.list_events()`. Nunca utilizan `.tickets`, `.events`, `._items` ni suponen que un repositorio sea in-memory. La serialización de custodia debe funcionar con cualquier implementación de `CustodySink`.

## Garantías de fallo

Los puertos indican fallas a través de sus tipos y excepciones de dominio. Un bloqueo no confirmado aborta la activación/cierre sin persistir un estado contrario a la realidad. Un pago rechazado no se interpreta como aceptado y no se representa como recibo exitoso.

## Cotización de repuestos

Los contratos `PromotionSource`, `DeliveryRateProvider`, `SupplyQuoteStore` y `QuoteIds` se consumen por inyección en `SupplyQuoteService`, sin exponer formato de almacenamiento ni instancia de transporte. Los cambios de precio, promociones y tarifas de envío no deben alterar la API del caso de uso.
