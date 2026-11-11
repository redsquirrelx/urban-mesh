# AC-101 — Contexto del sistema

**Estado:** Aprobado.

UrbanMesh gestiona operaciones de movilidad para una entidad pública que administra rutas, depósitos de bicicletas, sensores y suministros para la flota. Los pasajeros consultan salidas y viajes, alquilan bicicletas y reciben alertas. Los operadores de transporte administran incidentes y turnos. El equipo de mantenimiento registra reparaciones y solicita repuestos. Los supervisores de telemetría clasifican lecturas y mantienen su cadena de custodia.

## Contextos funcionales

1. **Transporte:** rutas, salidas, planificación, tarifas y billetes.
2. **Micromovilidad:** bicicletas, alquileres, cerraduras, cobro de alquileres.
3. **Operaciones:** incidentes, alertas, turnos, mantenimiento y reportes.
4. **Telemetría:** adquisición, calibración, calidad, cadena de custodia y retención.
5. **Abastecimiento:** catálogo, stock, reserva, compras, facturación y campañas.
6. **Identidad:** cuentas de pasajeros y validación de credenciales.

## Actores y sistemas externos

Los pasajeros utilizan HTTP; operaciones utiliza la API y la CLI; los dispositivos de estación acceden por `LockGateway`; los procesadores de pago por `PaymentGateway`; los dispositivos de medición por `SensorReader`; el almacenamiento y la mensajería por otros puertos. Los mensajes de dispositivos y procesadores no constituyen tipos de dominio.

## Aislamiento de responsabilidades

El hecho de que una reserva origine posteriormente un pago, una notificación o una tarea no transfiere a la planificación la propiedad de la política de cobro, notificación o mantenimiento. Los flujos se coordinan en aplicación; las políticas permanecen en su componente propietario.
