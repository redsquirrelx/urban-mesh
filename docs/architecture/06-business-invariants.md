# AC-106 — Invariantes operativas

| ID | Invariante |
|---|---|
| INV-001 | El dinero es entero en centavos y los totales son no negativos |
| INV-002 | Una cotización de tarifa es final, no un delta de descuento |
| INV-003 | Ningún alquiler se abre dos veces con el mismo identificador |
| INV-004 | Un alquiler finaliza después de su inicio y no puede cerrarse dos veces |
| INV-005 | La confirmación de cerradura es requerida antes de persistir el estado |
| INV-006 | Una misma entidad de stock nunca tiene existencias negativas |
| INV-007 | Compra total = suma del precio unitario por cantidad válida |
| INV-008 | Las valoraciones están en 0..5; el promedio es aritmético sin truncamiento |
| INV-009 | La contraseña es válida si y solo si es cadena con al menos 8 caracteres |
| INV-010 | Las categorías de calidad son `accepted`, `hold`, `rejected` |
| INV-011 | Los umbrales de calidad son inclusivos: 20 → hold, 60 → rejected |
| INV-012 | Consultas e informes no realizan eliminación ni cambios en estado |
| INV-013 | La eliminación de un SKU retira el registro del catálogo, no solo pone stock a cero |

Las operaciones deben conservar las invariantes ante entradas límite y ante la sustitución de los adaptadores. Las validaciones de HTTP son un mecanismo de entrada adicional, no reemplazan la política de aplicación o dominio.
