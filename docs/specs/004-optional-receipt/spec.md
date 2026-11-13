# Comprobante opcional

Solicitud de Maxi del 13 de noviembre de 2026: permitir crear gastos sin comprobante y adjuntarlo posteriormente. Si se adjunta, conservar validaciones, privacidad y compensaciones. Mostrar Sin comprobante y ocultar enlaces a archivos ausentes. Anulados siguen siendo de solo lectura.

Diseño técnico: receipt nullable en DTO, creación opcional, upsert del primer archivo en operación existente con versionado; base ya permite ausencia. Plan: actualizar contrato y reglas, adaptar aplicación/persistencia/HTTP y UI, probar casos con/sin archivo y errores. Sin migración nueva ni despliegue automático.

## Evidencia local

67 pruebas backend y 33 frontend correctas; lint y builds completos correctos. DTO y esquemas comprobados contra el contrato canónico local usando --contract. Referencias inmutables de consumidores aún conservan la revisión anterior: falta commit canónico y sincronización antes de publicar, sin afirmar contract:check ordinario actualizado. Sin commits, push, migraciones ni despliegue en esta tarea. Riesgo: desplegar frontend/backend coordinadamente por receipt nullable. Reversión: no volver a clientes que exigen archivo mientras existan gastos sin comprobante; conservar datos y archivos.
