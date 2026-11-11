# AC-108 — Atributos de calidad

## Sustituibilidad

La instalación utiliza memoria durante el desarrollo, pero debe poder incorporar almacenamiento SQL, una pasarela de pagos alternativa, un dispositivo de otra marca o una cola de reparación distinta sin cambiar código de casos de uso. Los contratos CT-001–CT-012 forman la condición mínima.

## Mantenibilidad

Políticas con motivos de cambio diferentes permanecen separadas: normas laborales, promociones, regulación, reglas tarifarias, mantenimiento, entrega de avisos, purga y generación de reportes. Un cambio de campaña no modifica el algoritmo de rutas; una actualización del gateway no cambia liquidación.

## Integridad

Los importes se expresan en centavos enteros; todas las reservas y actualizaciones respetan el stock disponible; cada operación con efectos persistentes valida precondiciones antes de guardar. Los endpoints ofrecen errores coherentes y no exponen detalles de proveedores.

## Observabilidad

Los errores de dominio se transforman a respuestas HTTP uniformes. Los eventos de auditoría y custodia se registran únicamente mediante operaciones correspondientes; los reportes carecen de efectos secundarios.

## Escalabilidad

Los adaptadores en memoria son de alcance local. Repositorios persistentes deberán conservar los mismos contratos y las garantías de consistencia ante concurrencia.
