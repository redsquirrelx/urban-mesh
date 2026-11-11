# AC-104 — Flujos de ejecución

## Viaje en autobús

1. Presentación valida una petición de origen, destino y pasajero.
2. `JourneyPlanner` consulta `RouteSource` y devuelve opciones ordenadas por tiempo.
3. `FareQuoteService` obtiene tarifa base y aplica `bus_fare`.
4. `TicketIssuer` almacena el billete mediante `TicketStore`.
5. Si procede una oferta, un servicio independiente de engagement la programa.
6. Cumplimiento regulatorio registra evaluaciones mediante su caso de uso propio.

## Alquiler de bicicleta

1. `RideService.start` comprueba disponibilidad, solicita la apertura del bloqueo y persiste un alquiler activo.
2. `RideService.finish` confirma cierre y duración válida, solicita cierre de bloqueo y persiste finalización.
3. `SettlementService.settle` obtiene la cotización final del `FarePolicy` elegido y pide `PaymentGateway.capture`.
4. El gateway devuelve un `PaymentReceipt` normalizado; el caso de uso evalúa `accepted` y devuelve `external_reference`.

## Incidencia de flota

El despacho de alertas informa a pasajeros suscritos. La clasificación de urgencia y creación de tarea se realiza por un flujo operacional distinto. Los reportes de abordajes consultan snapshots sin depurarlos.

## Sensor y cadena de custodia

El lector devuelve una `SensorReading`; una política de calibración normaliza unidades; la regla de calidad devuelve `accepted`, `hold` o `rejected`; la política de urgencia determina la prioridad de la notificación. El registro de custodia se almacena mediante puerto y el exportador consume snapshots. La retención se invoca exclusivamente por un comando operacional explícito.

## Abastecimiento

El catálogo valida repuestos y cantidades; el asignador reserva unidades mediante interfaces públicas; compras registra pedidos y cobra por un puerto de pago; las notificaciones se solicitan a servicios de comunicación. Los informes de almacén no modifican disponibilidad.
