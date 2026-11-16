# Diseño técnico — Gastos: destinatario y comentario opcionales

payee y description se pueden omitir o enviar vacíos. Se normalizan a «Sin destinatario» y «Sin comentario» antes de persistir; las columnas NOT NULL y CHECK existentes se conservan. PATCH omitido conserva valor; vacío lo reemplaza por el predeterminado.

Mantener límites por funcionalidades y capas. OpenAPI canónico y tipos/esquemas generados en consumidores; UI en español. Coordinar frontend y backend cuando cambia el contrato.
