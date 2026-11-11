# AC-110 — Despliegue y operación

El despliegue de desarrollo usa `uvicorn urbanmesh.presentation.api:app`. La instancia crea servicios con `bootstrap.build_services()`. No se requieren variables de entorno para las operaciones locales. Los repositorios de memoria están asociados al proceso y se reinicializan al reiniciar la aplicación.

Para entornos distribuidos deben implementarse los puertos con almacenamiento persistente y comunicación resiliente. Los cambios de proveedor no deben requerir modificaciones en `application/` ni `domain/`.

Los trabajos de retención se ejecutan mediante comandos explícitos con fecha límite y registro operacional. La limpieza no puede ser efecto incidental de consultas de reportes. Las notificaciones del transporte HTTP no modifican el formato de intercambio entre casos de uso y adaptadores.
