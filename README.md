# UrbanMesh

UrbanMesh es la plataforma municipal para coordinar el transporte público, la micromovilidad, la telemetría de la flota, el mantenimiento y el abastecimiento de depósitos. Expone una API HTTP y herramientas de línea de comandos, y mantiene las reglas de negocio separadas de los mecanismos de almacenamiento y comunicación.

## Capacidades

- Consultas de rutas, viajes, tarifas, billetes y tableros de salida.
- Bicicletas compartidas, alquileres, cobros y confirmaciones.
- Incidentes de servicio, notificaciones, órdenes de mantenimiento y turnos.
- Lecturas de sensores, clasificación de calidad, custodia y retención.
- Inventario de repuestos, reservas, órdenes de compra y promociones.
- Reportes, auditoría operativa y cuentas de pasajeros.

## Inicio rápido

Requiere Python 3.11 o superior.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn urbanmesh.presentation.api:app --reload
```

En otra terminal:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/routes
curl http://localhost:8000/inventory
urbanmesh routes
pytest -q
```

La configuración local utiliza adaptadores en memoria y datos de muestra; no requiere credenciales ni servicios de terceros. La persistencia en memoria no proporciona durabilidad entre procesos.

## Guía documental

- [Arquitectura](ARCHITECTURE.md) y [reglas normativas](docs/architecture/03-layer-rules.md)
- [Requisitos funcionales](docs/requirements.md) con criterios verificables
- [Responsabilidades](docs/architecture/02-functional-ownership.md)
- [Puertos y contratos](docs/architecture/05-ports-and-substitution.md)
- [Invariantes](docs/architecture/06-business-invariants.md)
- [Referencia API](docs/api.md)
- [Decisiones](docs/adr/README.md)
- [Trazabilidad](docs/traceability.md)
- [Desarrollo y verificación](docs/development.md)

## Organización

`src/urbanmesh/domain/` contiene entidades y políticas puras; `application/` coordina casos de uso y declara puertos; `infrastructure/` implementa conectores y repositorios; `presentation/` contiene los adaptadores HTTP y CLI. `bootstrap.py` es la raíz de composición. `modules/` expone las interfaces públicas de las funciones de aprovisionamiento conservadas por integraciones internas.

Para despliegues de varias instancias, los adaptadores de memoria deben sustituirse por implementaciones persistentes de los puertos establecidos.
