# Diseño técnico — Gastos: vencimiento opcional

Agregar dueDate opcional y nullable como fecha civil, sin limitarla al pasado ni relacionarla con fecha de pago. PATCH omitido conserva valor y null borra. Filtros inclusivos dueDateFrom/dueDateTo combinados con los actuales, excluyen registros sin vencimiento cuando están activos. Listado, total y CSV usan los mismos filtros. Migración aditiva nullable, sin ejecutar en producción.

Mantener límites por funcionalidades y capas. OpenAPI canónico y tipos/esquemas generados en consumidores; UI en español. Coordinar frontend y backend cuando cambia el contrato.
