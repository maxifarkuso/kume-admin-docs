# Gastos: vencimiento opcional

Fecha: 16 de noviembre de 2026. Solicitud aprobada por Maxi.

Agregar dueDate opcional y nullable como fecha civil, sin limitarla al pasado ni relacionarla con fecha de pago. PATCH omitido conserva valor y null borra. Filtros inclusivos dueDateFrom/dueDateTo combinados con los actuales, excluyen registros sin vencimiento cuando están activos. Listado, total y CSV usan los mismos filtros. Migración aditiva nullable, sin ejecutar en producción.

Aceptación: crear, consultar y editar con las nuevas reglas; conservar validaciones y control de versiones existentes. Verificar errores y regresiones pertinentes. Sin despliegue ni ejecución de migraciones.
