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

- [ ] Validar definitivamente la ampliación OpenAPI y su compatibilidad en ambos consumidores.
- [ ] Fijar commit canónico autorizado y regenerar snapshots/manifiestos sin pendingContract.
- [ ] Comprobar generación determinista de DTO y esquemas HTTP.

## Backend — AC1–AC5, AC7–AC8, AC10–AC12

- [ ] Completar y revisar migraciones de schema, restricciones y carga inicial.
- [ ] Contrastar siete cursos y tres talleres, días, turnos y Maternal sin nombre interno.
- [ ] Aplicar migraciones en base vacía de prueba y comprobar segunda ejecución sin duplicados ni restablecer ediciones.
- [ ] Completar dominio, casos de uso y puerto de persistencia con tests de invariantes y concurrencia lógica.
- [ ] Verificar escrituras atómicas y guardas de asignaciones con evidencia apropiada; no inferir carreras reales desde mocks.
- [ ] Revisar las doce operaciones HTTP, autorización y traducción de errores.
- [ ] Completar formato, lint, tipos, unitarias, build, validación Prisma y contrato.

## Frontend — AC1–AC9, AC12

- [ ] Completar listados, filtros, paginación, detalle/edición y formularios.
- [ ] Verificar baja confirmada y reactivación con versión capturada.
- [ ] Probar conservación del borrador y manejo del conflicto sin cambiar versión silenciosamente.
- [ ] Probar estados de carga/vacío/error, reintento y sesión perdida.
- [ ] Completar formato, lint, tipos, unitarias, build y contrato.

## Estado del trabajo previo a este hito documental

Hay código local en curso en ramas feat/courses-workshops de backend y frontend, sin commit ni publicación. No se declara terminado. La generación Prisma devolvió 403 al descargar desde binaries.prisma.sh; falta habilitar ese dominio. Se ejecutaron unitarias del backend en una revisión intermedia: 43 pruebas pasaron; no acreditan el estado final ni migraciones. Se detectaron fallas de comprobación en frontend y limitaciones por cliente Prisma sin generar; quedan pendientes de repetición y cierre. Ningún dato de producción fue migrado por este trabajo.

## Entrega y operación

- [ ] Actualizar evidencia sobre la revisión final y enlazar AC con pruebas.
- [ ] Con autorización expresa, generar commits por hito, subir ramas y abrir PR; no merge automático.
- [ ] Comprobar CI remoto y coordinar versiones de backend/frontend.
- [ ] Verificar proxy/cuerpo DELETE, base real y recuperación antes del despliegue.
- [ ] Verificar asignaciones cuando se implemente su módulo; no declarar integración por anticipado.
