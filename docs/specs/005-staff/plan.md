# Personal — Plan de implementación

## Resultado esperado

Completar criterios P01–P08 de spec.md en backend/frontend con contrato fijo, sin desplegar. Dueño transaccional: ficha de personal; archivos en volumen privado.

## Etapas y ubicación

1. Especificación funcional: alcance y aceptación en spec.md. Commit y push por repositorio.
2. Diseño técnico y contrato: technical-spec.md; OpenAPI canónico, API y persistencia en docs. Commit y push antes de consumidores.
3. Plan y tareas: este archivo y tasks.md, referencias a revisión contractual inmutable. Commit y push.
4. Backend: dominio (cédula/fechas/estados), puertos/casos de uso, persistencia transaccional, migración aditiva, adaptador privado compartido y 16 rutas de personal/asignaciones. Regenerar contrato y comprobar auth/límites/compensación.
5. Frontend: API tipada/validada, listado/editor/ficha con pestañas, asignaciones/conflictos y documentos. Capturar versión inicial, conservar borradores y confirmar acciones. Reutilizar interfaz aprobada.
6. Verificación: controles locales y revisión de diff/capas; registrar resultados y límites en implementation.md. Commit y push de implementación por repo; abrir PRs sin merge y consultar CI.

## Impacto y dependencias

Los consumidores fijan SHA del contrato canónico y hashes mediante scripts existentes. Sin dependencias de producción nuevas. Migración crea tablas de personal sin alterar registros existentes. Asignaciones coordinan bloqueos con catálogos existentes; no se desactiva su guarda. Archivos se comparten como adaptador técnico, sin dependencias entre internals de módulos.

## Validación y reversión

Unitarias de reglas y casos de uso, pruebas aisladas de UI y transporte, formatos/lint/tipos/build/contrato y Prisma validate. SQL/carreras reales y piloto pendientes si no se ejecutan explícitamente. Revertir artefactos compatibles conservando base/archivos, sin down destructivo. No aplicar migraciones en Oracle ni desplegar por inferencia.
