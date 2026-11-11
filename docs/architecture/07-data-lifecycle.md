# AC-107 — Datos, custodia y retención

## Propiedad de conjuntos de datos

Las rutas y paradas pertenecen al catálogo de transporte; los alquileres a micromovilidad; billetes a emisión; estados de reparación a mantenimiento; lecturas a telemetría; eventos de custodia a cumplimiento; piezas y existencias al catálogo de depósitos. Cada repositorio ofrece consultas por puerto y ninguna capa externa accede a su representación interna.

## Política de retención

Las lecturas de sensores se conservan como mínimo 180 días salvo una orden de eliminación autorizada. Una ejecución explícita `POST /operations/retention/run` calcula el límite con el parámetro `as_of` y aplica la purga. La consulta `GET /reports/telemetry` no purga. Lo mismo rige para `GET /reports/ridership`, que puede contar registros históricos sin eliminarlos.

## Exportación de custodia

El exportador obtiene los eventos mediante `CustodySink.list_events()` y genera columnas `recorded_on,sensor_id,action,actor` en orden de inserción. La disposición CSV está en la lógica de intercambio, no en el repositorio ni en el transporte HTTP. No deben intercambiarse referencias mutables a la lista interna del adaptador.

## Efectos y auditoría

La emisión de billetes, los cobros y las reservas pueden generar eventos explícitos de auditoría mediante un orquestador. La mera consulta de una tarifa no registra cumplimiento; dicho análisis corresponde al servicio regulatorio. Los informes no alteran el conjunto reportado.
