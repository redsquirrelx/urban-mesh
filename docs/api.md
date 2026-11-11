# Referencia API HTTP

**Versión:** 1.4. **Base local:** `http://localhost:8000`. El esquema OpenAPI se publica en `/openapi.json` y la documentación interactiva en `/docs`.

| Método | Recurso | Objetivo |
|---|---|---|
| GET | `/health` | Estado lógico |
| GET | `/routes`, `/routes/{route_id}` | Catálogo de rutas |
| POST | `/journeys/search` | Opciones de trayecto |
| POST | `/fares/quote` | Tarifa de autobús |
| POST / GET | `/tickets`, `/tickets/{ticket_id}` | Emisión y consulta |
| GET | `/stations/{station_id}/bicycles` | Bicicletas operativas |
| POST / GET | `/rides`, `/rides/{ride_id}` | Alquiler |
| PATCH | `/rides/{ride_id}/finish` | Cierre |
| POST | `/rides/{ride_id}/settle` | Cobro |
| GET | `/stops/{stop_id}/departures` | Tablero |
| POST | `/alerts/disruptions` | Avisos por interrupción |
| GET | `/reports/ridership` | Abordajes por ruta |
| POST / GET | `/maintenance/work-orders` | Mantenimiento |
| GET | `/telemetry/sensors/{sensor_id}` | Lectura de sensor |
| POST | `/telemetry/sensors/{sensor_id}/assess` | Clasificación |
| GET | `/telemetry/quality/{sensor_id}` | Resultado almacenado |
| POST / GET | `/telemetry/custody`, `/telemetry/custody/export` | Custodia |
| GET | `/reports/telemetry` | Estadística no destructiva |
| POST | `/operations/retention/run` | Retención programada |
| GET / POST | `/inventory` | Listado y registro |
| GET / PATCH / DELETE | `/inventory/{sku}` y `/inventory/{sku}/stock` | Catálogo y existencias |
| GET | `/inventory/{sku}/average-rating` | Valoraciones |
| POST | `/purchases/total` | Cotización de compra |
| POST | `/procurement/checkout` | Orden y cobro |
| GET | `/procurement/discount-preview` | Descuento |
| GET | `/admin/low-stock` | Estado del depósito |
| POST | `/passwords/validate` | Validación de credencial |
| GET / POST | `/riders` | Cuentas |
| GET | `/riders/{rider_id}` | Consultar cuenta |

## Ejemplos

### Buscar trayecto

```bash
curl -X POST http://localhost:8000/journeys/search -H 'Content-Type: application/json' \
  -d '{"origin":"CENTRO","destination":"PUERTO","rider_id":"u-001","rides_last_month":3,"travel_day":"2026-11-11"}'
```

### Crear una pieza

```bash
curl -X POST http://localhost:8000/inventory -H 'Content-Type: application/json' \
  -d '{"sku":"BOLT-20","name":"Tornillo M20","price_cents":180,"stock":6,"ratings":[4.0,5.0]}'
```

### Total de materiales

```json
{"lines":[{"sku":"CHAIN-01","quantity":2},{"sku":"BRAKE-02","quantity":3}]}
```

Respuesta esperada: `{"total_cents":8298}`.

## Errores

Para recursos inexistentes se usa `404`. Validaciones de esquema, rangos o negocio se reflejan en `422`. Conflictos como alquiler duplicado, bloqueo no confirmado o cuenta duplicada retornan `409`. Un error HTTP conserva una estructura JSON con `detail` explicativo. Véase [requisitos](requirements.md).

## Operaciones complementarias

| Método | Recurso | Propósito |
|---|---|---|
| POST | `/inventory/{sku}/ratings` | Registrar una valoración |
| GET | `/procurement/orders/{order_id}` | Consultar una orden de compra |
| GET | `/telemetry/sensors` | Enumerar sensores disponibles |
| GET | `/maintenance/assets/{asset_id}/work-orders` | Órdenes por activo |
| PATCH | `/riders/{rider_id}/email` | Modificar correo del pasajero |
| POST | `/inventory/{sku}/release` | Liberar una reserva |
| GET | `/reports/ridership/export` | Exportación CSV de abordajes |
| GET | `/engagement/campaigns` | Campañas pendientes |

Las capacidades y códigos de error se detallan en REQ-068–REQ-075.

## Cotizaciones y excepciones operacionales

| Método | Recurso | Propósito |
|---|---|---|
| POST | `/procurement/quotes` | Presupuesto de abastecimiento |
| GET | `/procurement/quotes/{quote_id}` | Consultar presupuesto |
| GET | `/telemetry/exceptions` | Excepciones de calidad autorizadas |

Estos flujos se rigen por REQ-076–REQ-079 y por CT-009/CT-012.
