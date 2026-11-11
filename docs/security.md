# Seguridad y tratamiento de datos

La ejecución local utiliza datos de demostración; no se deben registrar credenciales reales en el repositorio. Los endpoints de cuentas y operaciones requieren autenticación y autorización antes de su despliegue público. La validación de contraseñas descrita en REQ corresponde a un prechequeo de formato, no a almacenamiento de secretos.

Las identificaciones de pasajero y recibos no deben trasladar payloads de proveedor a dominio. Los adaptadores de pago son reemplazables, y los logs de auditoría y custodia se generan mediante puertos establecidos. No se expone almacenamiento mutable de inventario o sesiones como contrato público.
