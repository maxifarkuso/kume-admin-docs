# Cursos y talleres — tareas y evidencia

Fecha de corte: 7 de noviembre de 2026. Las casillas verificadas describen únicamente evidencia disponible.

## Especificación

- [x] Revisar alcance, carga inicial, API, base, arquitectura y pautas de UI.
- [x] Registrar aprobación expresa de Maxi para versionado de cursos/talleres y conflicto 409.
- [x] Preparar especificación funcional con criterios AC1–AC12.
- [x] Preparar especificación técnica, plan, reversión y tareas.
- [x] Distinguir propuesta aprobada, código en curso y comprobaciones pendientes.
- [x] Obtener aprobación expresa de Maxi para especificaciones, plan e implementación. La aprobación final del paso 4 de diseño conserva su seguimiento propio.

## Contrato y trazabilidad

- [x] Validar OpenAPI y contrastar la ampliación en ambos consumidores; cambio incompatible de escrituras coordinado en la especificación.
- [x] Fijar docs 1e650636705371f09be51a8c77a67f39e5251ba3 y regenerar snapshots/manifiestos sin pendingContract.
- [x] Comprobar generación determinista de DTO y esquemas HTTP.

## Backend — AC1–AC5, AC7–AC8, AC10–AC12

- [x] Completar y revisar migraciones de schema, restricciones y carga inicial; ejecución diferida por Maxi hasta antes del despliegue.
- [x] Contrastar siete cursos y tres talleres, días, turnos y Maternal sin nombre interno.
- [ ] Aplicar migraciones en base vacía de prueba y comprobar segunda ejecución sin duplicados ni restablecer ediciones.
- [x] Completar dominio, casos de uso y puerto de persistencia con tests de invariantes y concurrencia lógica.
- [ ] Verificar escrituras atómicas y guardas de asignaciones con evidencia apropiada; no inferir carreras reales desde mocks.
- [x] Revisar las doce operaciones HTTP, autorización y traducción de errores con repositorio controlado.
- [ ] Completar formato, lint, tipos, unitarias, build, validación Prisma y contrato.

## Frontend — AC1–AC9, AC12

- [x] Completar listados, filtros, paginación, detalle/edición y formularios.
- [x] Implementar baja confirmada y reactivación con versión capturada; probar cuerpo/versionado en adaptador HTTP.
- [x] Probar conservación del borrador y manejo del conflicto sin cambiar versión silenciosamente.
- [x] Probar carga/vacío/error y reintento de catálogos; las pruebas existentes de App cubren pérdida de sesión y limpieza de datos privados.
- [x] Completar formato, lint, tipos, 14 unitarias, build Vite y contrato del frontend.

## Estado de implementación

Código completado y comprometido localmente en feat/courses-workshops (backend 1c477d2, frontend e40b0d4); ver implementation.md para evidencia y límites. Maxi autorizó los commits y aprobó especificaciones, plan e implementación. No se ejecutaron migraciones: quedan diferidas por pedido expreso hasta el momento previo al despliegue. La configuración visible incluye binaries.prisma.sh, pero esta instancia todavía devuelve 403. Se generó un cliente local sin motor con las herramientas oficiales de Prisma 6.19.0 solo para tipos y pruebas; no es un artefacto de producción. No se modificaron dependencias del proyecto para ese procedimiento.

## Entrega y operación

- [x] Actualizar evidencia sobre la revisión final y enlazar AC con pruebas en implementation.md.
- [ ] Con autorización expresa, generar commits por hito, subir ramas y abrir PR; no merge automático.
- [ ] Comprobar CI remoto y coordinar versiones de backend/frontend.
- [ ] Verificar proxy/cuerpo DELETE, base real y recuperación antes del despliegue.
- [ ] Verificar asignaciones cuando se implemente su módulo; no declarar integración por anticipado.
