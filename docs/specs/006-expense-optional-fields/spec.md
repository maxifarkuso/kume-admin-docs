# Gastos: destinatario y comentario opcionales

Fecha: 16 de noviembre de 2026. Solicitud aprobada por Maxi.

payee y description se pueden omitir o enviar vacíos. Se normalizan a «Sin destinatario» y «Sin comentario» antes de persistir; las columnas NOT NULL y CHECK existentes se conservan. PATCH omitido conserva valor; vacío lo reemplaza por el predeterminado.

Aceptación: crear, consultar y editar con las nuevas reglas; conservar validaciones y control de versiones existentes. Verificar errores y regresiones pertinentes. Sin despliegue ni ejecución de migraciones.
