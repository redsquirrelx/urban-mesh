# Transporte público

**Referencia:** requisitos en `docs/requirements.md`, mapa de propiedad en AC-102 y reglas de dependencias en AC-103.

El catálogo posee rutas y duraciones; `JourneyPlanner` solo decide rutas viables y orden; las campañas pertenecen a engagement; precios a tarifas; normativa a operaciones. El workflow `BookCommute` enlaza opciones, cotización y emisión mediante servicios ya especializados.

La integración externa se realiza mediante contratos de aplicación. Los handlers de HTTP son adaptadores y no definen políticas propias.
