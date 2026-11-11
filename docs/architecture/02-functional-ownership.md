# AC-102 — Propiedad funcional y separación de responsabilidades

**Estado:** Aprobado. Cada decisión funcional posee un responsable inequívoco, incluso si diversos casos de uso comparten los mismos puertos.

| ID | Responsabilidad y propietario | Componente responsable | Límite explícito |
|---|---|---|---|
| OWN-001 | Selección de trayectos y duración | `application/journeys/planner.py` | No determina audiencias, campañas o textos comerciales |
| OWN-002 | Elegibilidad y texto de ofertas | `application/engagement/` | No modifica rutas, tarifas o billetes |
| OWN-003 | Cálculo de precios | `application/fares/quote.py`, `domain/policies/pricing.py` | No clasifica eventos de cumplimiento regulatorio |
| OWN-004 | Evaluación y registro regulatorio | `application/operations/audits.py` | Se invoca como responsabilidad independiente |
| OWN-005 | Emisión y almacenamiento de billetes | `application/ticketing/issuer.py` | No decide promociones ni encola campañas |
| OWN-006 | Distribución de avisos de interrupción | `application/alerts/dispatcher.py` | No prioriza ni genera órdenes de mantenimiento |
| OWN-007 | Clasificación y orden de reparación | `application/operations/work_orders.py`, `application/maintenance/` | No pertenece al despachador de pasajeros |
| OWN-008 | Cálculo de tableros de salida | `application/schedules/boards.py` | No verifica horas de trabajo del conductor |
| OWN-009 | Cumplimiento de turnos | `application/operations/crew.py` | Decide banderas laborales y cambios de normativa |
| OWN-010 | Estadísticas de abordajes | `application/reporting/ridership.py` | Consultas de solo lectura; no realizan purgas |
| OWN-011 | Activación/cierre de alquileres | `application/rides/service.py` | Coordina cerraduras sin gestionar cobros |
| OWN-012 | Liquidación de pagos | `application/payments/settlement.py` | Consume recibos normalizados sin campos de proveedor |
| OWN-013 | Normalización de sensores | `application/telemetry/calibration.py`, `application/telemetry/processing.py` | No depende de perfiles específicos del fabricante |
| OWN-014 | Reglas de clasificación de calidad | `domain/policies/quality.py`, `application/telemetry/quality.py` | No decide el canal o urgencia de una notificación |
| OWN-015 | Custodia y formato de intercambio | `application/telemetry/custody.py` | Exporta con un port sin leer estructura de almacenamiento |
| OWN-016 | Retención y eliminación programada | `application/operations/retention.py` | Nunca está implícita en lecturas de reporte |
| OWN-017 | Catálogo de repuestos e invariantes de stock | `application/inventory/catalog.py` | El contrato público oculta almacenamiento |
| OWN-018 | Pedido de repuestos y pago | `application/procurement/checkout.py` | Notificación y cobro dependen de puertos |
| OWN-019 | Entrega de notificaciones de sensores | `application/telemetry/notifications.py` | La prioridad pertenece a `application/telemetry/urgency.py` |
| OWN-020 | Recomendaciones y confirmaciones | `domain/`, `application/engagement/`, infraestructura | Las políticas no conocen motores analíticos ni plantillas HTTP |

| OWN-021 | Cotización de abastecimiento | `application/procurement/quote.py` | Cálculo sin reserva, notificación ni pago |
| OWN-022 | Consulta de excepciones de calidad | `application/telemetry/exceptions.py` | Consulta por puerto, control de operador requerido |

## Criterio de cohesión

Un componente puede realizar varias etapas mecánicas que contribuyan al mismo objetivo: buscar, validar y guardar un billete; o reunir, ordenar y devolver horarios. Eso no implica varias responsabilidades. Una separación se exige cuando la unidad decide políticas diferentes que cambian por autoridades distintas (tarifas, campañas, cumplimiento, mantenimiento, retención, turnos) o introduce efectos externos que son propiedad de un servicio vecino.

## Orquestación aceptada

`application/workflows.py` coordina varios casos de uso ya especializados. La composición y delegación de etapas no asigna al orquestador los criterios internos de cada política. Los conectores de infraestructura tienen responsabilidades técnicas (persistir, enviar, traducir), no autoridad sobre decisiones de negocio.
