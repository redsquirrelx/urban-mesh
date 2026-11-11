# Requisitos funcionales

Este documento define el comportamiento esperado de la API y de los contratos de negocio de UrbanMesh. Los identificadores REQ son estables y se usan en revisiones de cambio, casos de prueba y trazabilidad. Las respuestas HTTP son JSON salvo que se indique otro formato. Los importes monetarios se expresan en **centavos enteros (PEN)**.

Los criterios se aplican tanto a la API como a los casos de uso nombrados. Una operación sin datos devuelve una colección vacía cuando corresponde; los recursos inexistentes devuelven `404`, las entradas inválidas `422` y los conflictos de estado `409`.

## REQ-001: Estado del servicio

La API debe permitir consultar la disponibilidad lógica.

- `GET /health` responde `200`.
- La respuesta incluye `status: ok`.

## REQ-002: Listar rutas

La API debe listar las rutas de transporte activas.

- `GET /routes` responde `200` y una lista.
- Cada ruta contiene `route_id`, `stops`, `hop_minutes` y `base_fare_cents`.
- Sin rutas, la respuesta es una lista vacía.

## REQ-003: Consultar ruta por identificador

La API debe encontrar una ruta registrada.

- `GET /routes/{route_id}` responde `200` cuando existe.
- Una ruta desconocida responde `404`.

## REQ-004: Buscar viajes

La búsqueda de viajes debe usar origen, destino, pasajero y fecha.

- `POST /journeys/search` recibe `origin`, `destination`, `rider_id`, `rides_last_month`, `travel_day`.
- Solo devuelve rutas que recorren el origen antes que el destino.
- Origen igual a destino devuelve `[]`.

## REQ-005: Ordenar opciones por duración

El resultado de la búsqueda debe ser determinista.

- Las opciones se ordenan por `travel_minutes` ascendente y luego `route_id`.
- La duración suma exclusivamente los tramos entre las paradas indicadas.

## REQ-006: Separar planificación de campañas

La planificación de recorridos no debe añadir información publicitaria.

- `POST /journeys/search` devuelve alternativas con `annotation` vacío, sin importar la frecuencia de viaje.
- La elegibilidad comercial se determina por `CampaignService`, no por `JourneyPlanner`.

## REQ-007: Cotizar un trayecto

El sistema debe cotizar tarifas en centavos enteros.

- `POST /fares/quote` recibe `route_id`, `rider_id`, `peak` y `concession`.
- La base de `R-01` es `280` centavos; el recargo punta es `75` y la concesión descuenta `90` sin permitir negativos.
- La cotización incluye `reference_id`, `rider_id`, `amount_cents` y `currency: PEN`.

## REQ-008: Manejar rutas inexistentes en tarifas

La cotización debe rechazar rutas no registradas.

- Una ruta inexistente en `POST /fares/quote` responde `404`.
- Un pasajero vacío responde `422`.

## REQ-009: Cotizaciones sin registro regulatorio implícito

Consultar una tarifa es una operación de cálculo.

- `FareQuoteService.quote` no produce entradas en `AuditSink`.
- Las evaluaciones regulatorias se registran explícitamente mediante `RegulatoryAuditService`.

## REQ-010: Emitir billetes

La API debe crear billetes a partir de tarifas confirmadas.

- `POST /tickets` responde `201` con `ticket_id`, `route_id`, `rider_id`, `amount_cents` e `issued_on`.
- El billete se recupera por `GET /tickets/{ticket_id}`.

## REQ-011: No programar ofertas al emitir billetes

La emisión de billetes y las campañas deben operar de manera independiente.

- `TicketIssuer.issue` guarda el billete pero no encola promociones.
- La campaña se planifica por `CampaignService.schedule` según elegibilidad de engagement.

## REQ-012: Consultar billete no registrado

La consulta debe distinguir billetes inexistentes.

- `GET /tickets/{ticket_id}` responde `404` si no existe.
- La consulta no altera el almacenamiento.

## REQ-013: Listar bicicletas disponibles

La API debe consultar estaciones sin exponer almacenamiento.

- `GET /stations/{station_id}/bicycles` responde una lista de bicicletas operativas.
- Una estación sin bicicletas responde `[]`.

## REQ-014: Activar un alquiler

La activación requiere una bicicleta operativa y bloqueo confirmado.

- `POST /rides` responde `201` con `ride_id`, `rider_id`, `bike_id`, `started_at` y `ended_at: null`.
- Una bicicleta inexistente responde `404` y una no operativa `409`.

## REQ-015: Evitar alquileres duplicados

El identificador de alquiler debe ser único.

- Un segundo `POST /rides` con el mismo `ride_id` responde `409`.
- La primera sesión permanece intacta después del rechazo.

## REQ-016: Respetar fallo de apertura

El sistema no debe iniciar alquileres sin confirmación del dispositivo.

- Si `LockGateway.unlock` retorna `False`, la activación falla con `409`.
- No se guarda la sesión cuando la cerradura no se abre.

## REQ-017: Finalizar un alquiler

El cierre de alquiler debe actualizar una sesión activa.

- `PATCH /rides/{ride_id}/finish` responde el alquiler con `ended_at`.
- Una sesión inexistente responde `404` y una ya cerrada `409`.

## REQ-018: Validar cronología del alquiler

Una sesión no puede terminar antes de comenzar.

- `ended_at` debe ser estrictamente posterior a `started_at`.
- Un instante igual o anterior responde `422` y conserva la sesión activa.

## REQ-019: Respetar fallo de cierre

El estado de finalización requiere confirmar el bloqueo de la bicicleta.

- Si `LockGateway.lock` retorna `False`, el cierre responde `409`.
- El alquiler permanece activo después de la falla.

## REQ-020: Tarifa plana sustituible

La tarifa plana produce un cobro final no negativo.

- `FlatFarePolicy(250).quote(ride)` devuelve `amount_cents = 250`.
- El `reference_id` corresponde a `ride_id` y el pasajero al alquiler.

## REQ-021: Tarifa por minutos sustituible

Cada minuto de alquiler iniciado debe cobrarse.

- `MinuteFarePolicy(unlock_cents=100, minute_cents=20)` cobra `140` por una sesión de `61` segundos.
- Una duración positiva inferior a 60 segundos se cobra como un minuto.

## REQ-022: Tarifa promocional sustituible

Una política promocional debe proporcionar la cifra final a cobrar.

- Sobre tarifa base `250` con descuento `50`, `PromotionalFarePolicy` debe devolver `200`, no `-50`.
- La cotización final es no negativa y se procesa como cualquier `FarePolicy`.

## REQ-023: Consumir políticas de tarifa por puerto

El cálculo del importe es intercambiable.

- `SettlementService` acepta cualquier implementación de `FarePolicy` sin consultar el tipo concreto.
- No convierte deltas de una política específica ni requiere estructuras auxiliares.

## REQ-024: Liquidar pagos confirmados

El servicio debe devolver el recibo estable del cobro.

- `POST /rides/{ride_id}/settle` devuelve `receipt_reference` cuando el cobro es aceptado.
- La fuente del resultado es `PaymentReceipt.external_reference`.
- Un alquiler inexistente devuelve `404` y uno sin finalizar `422`.

## REQ-025: Rechazar liquidaciones denegadas

Un rechazo de pago no es una confirmación exitosa.

- Si `PaymentReceipt.accepted` es `False`, la liquidación no devuelve recibo exitoso.
- El importe de la transacción no puede ser negativo.

## REQ-026: Sustituir procesadores de pago

El cobro no depende del JSON de un procesador específico.

- `ProcessorPaymentAdapter` y `SandboxPaymentGateway` devuelven `PaymentReceipt`.
- El mismo caso de uso debe aceptar cualquiera sin cambiar líneas de su implementación.

## REQ-027: Mostrar tablero de salidas

La API publica salidas estimadas en un punto.

- `GET /stops/{stop_id}/departures?minute=100` devuelve ruta y `departure_minute`.
- Un minuto fuera de `0..1439` responde `422`.
- Las entradas se ordenan por salida y ruta.

## REQ-028: Separar tablero de cumplimiento laboral

Las consultas de horarios son lecturas sin decisiones laborales.

- Consultar salidas no añade entradas a `ShiftFlags`, sin importar `hours_on_duty`.
- `CrewCompliance.check` es responsable de las banderas de turnos.

## REQ-029: Notificar interrupciones

Las incidencias deben enviarse solo a pasajeros suscritos.

- `POST /alerts/disruptions` responde el número de destinatarios afectados.
- La misma interrupción no genera avisos a rutas no suscritas.

## REQ-030: Separar avisos y reparación

La distribución de alertas no crea órdenes de reparación.

- `AlertDispatcher.dispatch` solo envía mensajes y contabiliza destinatarios.
- Una orden de reparación se genera por `WorkOrderService` o el flujo de mantenimiento.

## REQ-031: Consultar abordajes sin efectos laterales

Los reportes de abordajes deben ser de solo lectura.

- `GET /reports/ridership?as_of=YYYY-MM-DD` responde cantidades agrupadas por ruta.
- La consulta no ejecuta `delete_before` ni altera registros, independientemente de su fecha.

## REQ-032: Conservar historial de abordajes

Los reportes deben contar todos los registros hasta la fecha solicitada.

- Se incluyen abordajes anteriores a 30 días siempre que precedan o coincidan con `as_of`.
- No se borran registros para preparar el reporte.

## REQ-033: Crear trabajo de mantenimiento

El registro de campo debe generar una tarea con prioridad y fecha.

- `POST /maintenance/work-orders` responde `201`.
- El resultado contiene `asset_id`, `description`, `priority` y `opened_on`.

## REQ-034: Sustituir cola de mantenimiento

Las colas alternativas deben poder sustituirse sin cambiar al consumidor.

- `MaintenanceTriage.report` usa exclusivamente `RepairQueue.enqueue`.
- Una implementación que no tenga la propiedad `tickets` funciona correctamente.

## REQ-035: Consultar tareas de mantenimiento

La API debe listar el trabajo registrado.

- `GET /maintenance/work-orders` devuelve lista; si no existen entradas devuelve `[]`.
- La lectura no cambia la cola.

## REQ-036: Leer telemetría de sensores

La API proporciona una lectura numérica calibrada.

- `GET /telemetry/sensors/{sensor_id}` responde `sensor_id`, `value`, `unit`, `captured_at`.
- Un sensor inexistente responde `404`, no un error genérico del servidor.

## REQ-037: Sustituir lector de sensores

Los lectores de fabricantes distintos deben soportar el mismo caso de uso.

- `TelemetryProcessor` solo necesita `SensorReader.read`.
- `PartnerSensorReader` puede reemplazar `FleetSensorReader` sin atributos adicionales.

## REQ-038: Calibrar mediante política independiente

La normalización de mediciones pertenece a una política aislada.

- Un multiplicador `1.05` se inyecta mediante `CalibrationPolicy`, no mediante `reader.calibration_profile`.
- El lector no decide el factor de corrección que aplica el procesador.

## REQ-039: Clasificar calidad en límites

Los umbrales de clasificación son inclusivos.

- Valor `19.99` → `accepted`; `20` → `hold`; `59.99` → `hold`; `60` → `rejected`.
- La clasificación se aplica de igual forma en revisión y reglas directas.

## REQ-040: Mantener taxonomía común de calidad

Las reglas intercambiables deben devolver estados equivalentes.

- Toda implementación de `QualityRule.assess` devuelve `accepted`, `hold` o `rejected`.
- Los códigos propietarios `PASS` y `FAIL` no cruzan el puerto.

## REQ-041: Registrar resultado de calidad

El análisis debe conservar el último estado de cada sensor.

- `POST /telemetry/sensors/{sensor_id}/assess` devuelve `sensor_id`, `classification` y `value`.
- `GET /telemetry/quality/{sensor_id}` devuelve el último resultado y responde `404` si no existe.

## REQ-042: Separar notificación y urgencia

La prioridad del aviso se determina mediante política específica.

- `TelemetryNoticeService` recibe una clasificación de prioridad o invoca `NoticePriority`, no compara umbrales numéricos por su cuenta.
- Un cambio en reglas de urgencia no requiere modificar el adaptador de entrega.

## REQ-043: Registrar eventos de custodia

Las operaciones de equipos generan eventos auditables.

- `POST /telemetry/custody` responde `201`.
- El evento incluye `sensor_id`, `action`, `actor` y `recorded_on`.

## REQ-044: Exportar cadena de custodia

El exportador debe construir un formato estable.

- `GET /telemetry/custody/export` responde `rows`, lista de filas CSV.
- Cada fila ordena `recorded_on,sensor_id,action,actor`.
- Una lista vacía produce `rows: []`.

## REQ-045: Sustituir almacén de custodia

El exportador debe funcionar con cualquier `CustodySink`.

- Solo usa `CustodySink.list_events()`; el almacén no está obligado a tener atributo `.events`.
- La exportación conserva el orden lógico del snapshot entregado.

## REQ-046: Consultar informe de sensores sin purgar

La estadística de telemetría es de solo lectura.

- `GET /reports/telemetry?as_of=YYYY-MM-DD` devuelve `older_records`.
- No borra mediciones de más de 180 días ni cambia el estado del almacén.

## REQ-047: Ejecutar retención explícita

La purga se invoca solo desde operaciones.

- `POST /operations/retention/run?as_of=YYYY-MM-DD&days=180` devuelve `deleted`.
- Borra solo registros anteriores al límite indicado.
- El parámetro `days` debe ser positivo o responde `422`.

## REQ-048: Listar inventario

La API debe devolver repuestos registrados.

- `GET /inventory` responde `200` y una lista.
- Cuando no existen repuestos devuelve `[]`.

## REQ-049: Consultar repuesto por SKU

Un repuesto puede consultarse mediante su código.

- `GET /inventory/{sku}` devuelve `sku`, `name`, `price_cents`, `stock`, `ratings`.
- Un SKU desconocido responde `404`.

## REQ-050: Crear repuesto válido

El almacén debe poder registrar nuevas piezas.

- `POST /inventory` responde `201` si el registro es válido.
- Acepta `stock=0` y `price_cents=0`.
- La creación se refleja en el siguiente listado.

## REQ-051: Validar repuestos al crearlos

El catálogo rechaza entradas inválidas.

- El nombre no puede ser blanco; el precio y stock no pueden ser negativos.
- Cada valoración debe ser numérica entre `0` y `5`.
- Un error de validación responde `422`.

## REQ-052: Modificar stock sin negativos

La actualización de existencias mantiene su invariante.

- `PATCH /inventory/{sku}/stock` acepta `0`.
- Un valor negativo responde `422` y deja el stock anterior sin cambiar.
- Un SKU desconocido responde `404`.

## REQ-053: Eliminar un repuesto

La eliminación retira el registro del catálogo.

- `DELETE /inventory/{sku}` responde `204` para registros existentes.
- Después del borrado, `GET /inventory/{sku}` responde `404`.
- El SKU desaparece de `GET /inventory` y del repositorio.

## REQ-054: Calcular promedio de valoraciones

El promedio es la media aritmética sin truncamiento.

- `GET /inventory/{sku}/average-rating` devuelve `average`.
- Para las valoraciones `[4.0,5.0]`, `average` es `4.5`.
- Sin valoraciones, el promedio es `0.0`.

## REQ-055: Calcular coste total de compras

El importe de una compra se obtiene por suma de líneas.

- `POST /purchases/total` recibe `lines` con `sku` y `quantity`.
- Total = suma de `price_cents * quantity`.
- Una lista vacía devuelve `0`.
- Dos piezas de `1299` y tres de `1900` dan `8298` centavos.

## REQ-056: Validar líneas de compra

Una compra no debe aceptar cantidades o repuestos inválidos.

- `quantity <= 0` devuelve `422`.
- Un SKU desconocido devuelve `404`.
- No se modifica el inventario al cotizar el total.

## REQ-057: Registrar compra de suministros

La plataforma admite solicitudes de compra de repuestos.

- `POST /procurement/checkout` responde `201` con `receipt_reference` si el pago fue aceptado.
- El pedido se almacena y el importe cobrado se calcula como cantidad por precio unitario.

## REQ-058: Separar compras, avisos y gateways

La compra delega confirmaciones y cobros en contratos estables.

- `SupplyCheckout` no instancia un procesador específico ni determina el formato del correo.
- Un cambio del gateway de pago no requiere editar `SupplyCheckout`.

## REQ-059: Previsualizar promociones

El cálculo de descuento debe ser determinista e inyectable.

- `GET /procurement/discount-preview` devuelve `discount_cents`.
- La promoción `CIVIC5` descuenta hasta `500` centavos sin exceder el subtotal.
- El caso de uso obtiene promociones por puerto, no crea un catálogo concreto.

## REQ-060: Consultar productos bajos de stock

El operador puede consultar repuestos bajo un umbral.

- `GET /admin/low-stock?threshold=4` devuelve lista `skus`.
- La consulta consume una interfaz de inventario, sin acceder a `_items`.
- La consulta no modifica reservas ni existencias.

## REQ-061: Validar contraseñas

Se exige una longitud mínima para credenciales de pasajeros.

- `POST /passwords/validate` devuelve `{"valid":true}` para cadenas de 8 caracteres o más.
- Una cadena de 7 caracteres devuelve `{"valid":false}`.
- Un dato que no sea cadena devuelve `{"valid":false}`.

## REQ-062: Listar y consultar pasajeros

La API administra cuentas de pasajeros.

- `GET /riders` devuelve una lista con `rider_id`, `email` y `active`.
- `GET /riders/{rider_id}` devuelve `404` para ID desconocido.

## REQ-063: Registrar pasajeros

La API admite registro de nuevos pasajeros.

- `POST /riders` responde `201` con una cuenta válida.
- Un identificador duplicado responde `409` y email vacío `422`.

## REQ-064: Respetar acceso público a inventario

Los módulos vecinos acceden al stock mediante operaciones públicas.

- `modules/orders` y `modules/billing` no consultan ni importan `modules/inventory/_store.py`.
- La reserva solo usa un método público de inventario o un puerto de aplicación.

## REQ-065: Mantener dependencias funcionales acíclicas

Las funciones de inventario, pedidos y facturación no forman ciclos.

- Un recorrido de dependencias entre `modules/inventory`, `modules/orders` y `modules/billing` no vuelve al nodo de origen.
- Los flujos de compra se orquestan por aplicación.

## REQ-066: Controlar prioridad laboral en su servicio

El cumplimiento de turnos decide las banderas de exceso laboral.

- `CrewCompliance.check(driver_id, 9)` devuelve `excess_hours` y registra la bandera.
- `DepartureBoardService.build` no asume esta responsabilidad.

## REQ-067: Distinguir informes y retención

La lectura de los reportes no inicia operaciones destructivas.

- Los informes pueden ejecutarse repetidamente con resultados iguales ante un estado inmutable.
- Solo `RetentionService.prune` puede iniciar eliminaciones de registros por antigüedad.

## Convenciones del contrato

- Los instantes se comunican en ISO 8601 y las fechas en `YYYY-MM-DD`.
- Las operaciones de lectura no producen escrituras como efecto lateral.
- Los servicios aceptan adaptadores alternativos que respeten sus puertos.
- Las reglas de dependencias están detalladas en `docs/architecture/03-layer-rules.md` y los contratos en `docs/architecture/05-ports-and-substitution.md`.

## REQ-068: Registrar valoración de un repuesto

La API permite incorporar valoraciones posteriores al alta de productos.

- `POST /inventory/{sku}/ratings` recibe `rating` entre `0` y `5`, responde `201`.
- La valoración se incorpora al historial y afecta al promedio.
- SKU inexistente devuelve `404` y rango inválido `422`.

## REQ-069: Consultar una orden de suministros

Los depósitos consultan órdenes de compra por referencia.

- `GET /procurement/orders/{order_id}` responde `200` con `order_id`, `sku`, `quantity`, `unit_price_cents` y `total_cents`.
- Una orden desconocida responde `404`.

## REQ-070: Listar sensores registrados

El área de flota puede descubrir dispositivos disponibles.

- `GET /telemetry/sensors` responde `200` con una lista de identificadores de sensores.
- Sin dispositivos, devuelve `[]`.

## REQ-071: Consultar trabajos por activo

Mantenimiento filtra las órdenes abiertas por activo.

- `GET /maintenance/assets/{asset_id}/work-orders` devuelve trabajos de dicho activo.
- La respuesta es `[]` si el activo no tiene tareas.

## REQ-072: Modificar correo de pasajero

La API permite actualizar datos de contacto.

- `PATCH /riders/{rider_id}/email` recibe `email` no vacío y responde `200` con la cuenta actualizada.
- Un pasajero desconocido devuelve `404` y un email vacío `422`.

## REQ-073: Cancelar reservas de inventario

Las reservas pueden revertirse de manera explícita.

- `POST /inventory/{sku}/release` recibe una cantidad positiva y repone las unidades reservadas.
- Una cantidad inválida devuelve `422` y SKU desconocido `404`.

## REQ-074: Exportar reporte operacional

Los operadores pueden descargar un resumen normalizado de abordajes.

- `GET /reports/ridership/export?as_of=YYYY-MM-DD` devuelve `text/csv` con `route_id,boardings`.
- La exportación es de solo lectura y no elimina registros.

## REQ-075: Listar campañas programadas

El equipo de engagement puede consultar su cola de campañas.

- `GET /engagement/campaigns` responde lista de `rider_id` y `offer_code`.
- La respuesta es `[]` cuando no existen campañas.

## REQ-076: Cotizar pedidos de suministros sin cobrarlos

Los depósitos pueden calcular un presupuesto antes de iniciar el checkout.

- `POST /procurement/quotes` responde `201` con `quote_id`, `sku`, `quantity`, `subtotal_cents`, `discount_cents`, `delivery_cents`, `total_cents`.
- El subtotal es `price_cents * quantity`; el transporte depende del peso facturable y zona; los descuentos no exceden el subtotal.
- Las cantidades válidas son de 1 a 100; una pieza desconocida responde `404`.

## REQ-077: Recuperar cotizaciones de abastecimiento

La consulta de una cotización no modifica el inventario.

- `GET /procurement/quotes/{quote_id}` devuelve la cotización guardada.
- Un ID desconocido responde `404` y una consulta no reserva piezas ni procesa pagos.

## REQ-078: Consultar excepciones de calidad con autorización

Los operadores consultan exclusivamente lecturas retenidas o rechazadas.

- `GET /telemetry/exceptions?operator=OPERADOR` responde una lista de resultados con `classification` `hold` o `rejected`.
- La ausencia de identificador de operador responde `403`.
- El caso de uso consume `QualityStore.list_all`, no accede a colecciones privadas.

## REQ-079: Sustituir la regla de calidad durante la revisión

La revisión debe tratar todas las reglas acordes al contrato de la misma forma.

- `QualityReviewService.review` siempre llama a `QualityRule.assess`, independientemente de la clase concreta.
- No realiza un `isinstance` especial que apruebe otras implementaciones por defecto.
