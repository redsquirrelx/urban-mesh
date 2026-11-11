# AC-103 — Reglas normativas de Clean Architecture

**Estado:** Aprobado. **Alcance:** todo `src/urbanmesh/` salvo las excepciones indicadas.

## AR-001 — Independencia de dominio

**DEBE:** `domain/` depender únicamente de código del propio dominio y biblioteca estándar. **NO DEBE:** importar `application/`, `infrastructure/`, `presentation/` ni construir adaptadores concretos, aun si lo hace a través de un helper. Los valores de dominio no incorporan HTML ni campos específicos de un procesador.

## AR-002 — Independencia de casos de uso

**DEBE:** `application/` recibir puertos declarados en `application/ports.py` o contratos de dominio. **NO DEBE:** importar, construir o anotar como colaborador obligatorio un adaptador concreto de `infrastructure/`, ni acceder a sus atributos internos. `bootstrap.py` es la excepción autorizada para enlazar implementaciones.

## AR-003 — Aislamiento de infraestructura

**NO DEBE:** `infrastructure/` importar formatos, plantillas o módulos de `presentation/`. El renderizado HTML, la estructura JSON de HTTP y los códigos de estado pertenecen a `presentation/`. Un gateway maneja transporte o persistencia, no formato de UI.

## AR-004 — Raíz única de composición

**DEBE:** el ensamblaje de dependencias concretas de los casos de uso suceder en `bootstrap.py`. `presentation/` usa el grafo ya compuesto; no crea repositorios ni procesadores desde endpoints. Las pruebas pueden ensamblar dobles de forma aislada.

## AR-005 — Encapsulación de subsistemas públicos

**DEBE:** todo consumidor exterior a `modules/inventory/` usar el API pública de `modules/inventory/api.py` o un puerto acordado. **NO DEBE:** leer o modificar `modules/inventory/_store.py` y `STOCK` desde pedidos, facturación u otros módulos. El mismo criterio se aplica a almacenamiento privado de adaptadores.

## AR-006 — Dependencias acíclicas entre funciones

**NO DEBE:** existir ciclo de dependencia estática o alcanzable en ejecución entre `modules/inventory`, `modules/orders` y `modules/billing`. Las políticas compartidas se elevan hacia el dominio o se coordinan desde aplicación.

## AR-007 — Ocultamiento del estado mutable

**NO DEBE:** ningún componente exterior al adaptador manipular atributos `_items`, `_rides`, `_records`, `tickets`, `events` u otros contenedores concretos para simular un método del puerto. Las colecciones devueltas por consultas son snapshots que no permiten modificar almacenamiento interno.

## AR-008 — Neutralidad de pagos

**DEBE:** `PaymentGateway.capture` entregar `PaymentReceipt` y la liquidación consumir solamente el contrato estable. **NO DEBE:** el caso de uso consumir diccionarios con `paid`, `id`, `amount` u otra estructura de proveedor.

## AR-009 — Neutralidad de dispositivos

**DEBE:** los lectores de telemetría implementar `SensorReader.read`; el procesamiento dependerá solo de esa operación y de una política de calibración inyectada. **NO DEBE:** inspeccionar propiedades exclusivas de un fabricante, por ejemplo `calibration_profile`.

## AR-010 — Sustitución de políticas

**DEBE:** las variantes de `FarePolicy.quote` entregar una cotización final no negativa y las variantes de `QualityRule.assess` usar los mismos estados. Una política puede tener fórmulas distintas sin cambiar la semántica del puerto.

## AR-011 — Efectos de lectura

**NO DEBE:** un servicio de reporte borrar, depurar, reservar, cobrar ni actualizar entidades solo por responder una consulta. Las tareas de retención y mantenimiento son comandos independientes.

## AR-012 — Contratos HTTP

**DEBE:** el adaptador HTTP transformar errores de dominio en códigos públicos documentados y preservar la semántica de lectura, creación y eliminación. La validación transversal se documenta en `docs/requirements.md` y las decisiones de negocio no pertenecen a handlers HTTP.

## Excepciones y alcance

- `tests/**` puede usar adaptadores y estado privado para preparar fixtures, no como práctica de producción.
- `bootstrap.py` construye adaptadores y casos de uso.
- Las referencias a implementaciones en documentación no son dependencias en tiempo de ejecución.
- No se deduce incumplimiento solo de nombres de paquetes: se comprueba la importación real, el acceso, el flujo ejecutable y el contrato relacionado.
