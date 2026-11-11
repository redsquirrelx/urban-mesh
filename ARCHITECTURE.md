# Arquitectura de UrbanMesh

**Estado:** Aprobada. **Estilo:** Clean Architecture con puertos y adaptadores. **Alcance:** `src/urbanmesh/`.

## Regla de dependencias

Las dependencias de código apuntan hacia el centro: **presentación → aplicación → dominio**. La infraestructura implementa contratos declarados en la aplicación y puede depender del dominio, pero las reglas de negocio no dependen de infraestructura, presentación o formatos de proveedor. La raíz `bootstrap.py` vincula implementaciones concretas.

```text
                    ┌────────────────────────────────────┐
 HTTP / CLI          │   presentation                      │
                    └───────────────┬────────────────────┘
                                    │
                    ┌───────────────▼────────────────────┐
                    │ application · use cases · ports     │
                    └───────────────┬────────────────────┘
                                    │
                    ┌───────────────▼────────────────────┐
                    │ domain · entities · policies        │
                    └────────────────────────────────────┘
                    infrastructure ──implements──► ports
                    bootstrap ──composes──► adapters/cases
```

## Límites funcionales

Planificación de rutas, tarifas, emisión de billetes, promociones, cumplimiento regulatorio, despacho de alertas, mantenimiento, turnos, reportes, calidad, calibración, custodia, retención, inventario y facturación tienen propietarios de decisiones separados. Una aplicación puede orquestarlos sin absorber sus políticas.

## Reglas normativas

La referencia detallada es [AR-001–AR-012](docs/architecture/03-layer-rules.md). Los límites de responsabilidad son [OWN-001–OWN-022](docs/architecture/02-functional-ownership.md). Los contratos sustituibles se describen en [CT-001–CT-012](docs/architecture/05-ports-and-substitution.md). Las invariantes de negocio se encuentran en [INV-001–INV-013](docs/architecture/06-business-invariants.md).

## Documentos complementarios

- [Contexto](docs/architecture/01-system-context.md)
- [Flujos](docs/architecture/04-runtime-flows.md)
- [Datos y retención](docs/architecture/07-data-lifecycle.md)
- [Atributos de calidad](docs/architecture/08-quality-attributes.md)
- [Verificación](docs/architecture/09-verification.md)
- [Operación](docs/architecture/10-deployment.md)
- [Motivos de cambio](docs/architecture/11-change-drivers.md)
- [Matriz de trazabilidad](docs/traceability.md)

Las decisiones locales que modifican un contrato, un límite o una política funcional se registran en `docs/adr/` antes de su publicación.
