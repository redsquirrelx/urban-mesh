# Telemetría y calidad

**Referencia:** requisitos en `docs/requirements.md`, mapa de propiedad en AC-102 y reglas de dependencias en AC-103.

Un `SensorReader` devuelve `SensorReading` sin atributos específicos de fabricante. Una `CalibrationPolicy` normaliza la lectura; una `QualityRule` produce estados aceptados, en retención o rechazados. Custodia exporta snapshots; informes son de solo lectura y retención es explícita.

La integración externa se realiza mediante contratos de aplicación. Los handlers de HTTP son adaptadores y no definen políticas propias.
