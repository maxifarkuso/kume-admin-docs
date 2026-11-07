# Cursos y talleres — especificación técnica

Fecha: 7 de noviembre de 2026. Estado: diseño para implementación y revisión; no evidencia de ejecución en PostgreSQL.

## Contrato HTTP y concurrencia

Se conservan rutas y verbos canónicos de cursos y talleres. GET de colección/detalle devuelve versión; POST de creación devuelve 201 y Location; PATCH devuelve 200 con el recurso actualizado. POST y DELETE sobre `/deactivation` desactivan y reactivan respectivamente y mantienen 204 sin cuerpo de respuesta.

La ampliación aprobada exige `version` entero positivo en PATCH y en el cuerpo JSON de ambas acciones de estado. PATCH necesita al menos un campo editable además de versión. La creación no acepta una versión elegida por el cliente. Campos omitidos no cambian; el nombre interno admite null.

Ejemplo de modificación: `PATCH /api/v1/courses/{courseId}` con `{"version":1,"internalName":"Kiru"}`. Ejemplo de baja: `POST /api/v1/courses/{courseId}/deactivation` con `{"version":2}`. La reactivación usa DELETE en esa misma ruta, también con cuerpo `{"version":3}`. Verificar que el proxy y el cliente preserven ese cuerpo antes de publicar.

Toda escritura aceptada incrementa la versión una vez, incluidas acciones sobre un estado ya coincidente. Repetir una petición con versión antigua devuelve 409, incluso si su intención coincide con el estado actual; no se promete idempotencia de reintentos de escritura. El cliente debe consultar de nuevo tras una respuesta perdida antes de decidir repetir.

`VERSION_CONFLICT` identifica una versión obsoleta mediante Problem Details y estado 409. Se distinguen ausencia de recurso (404), unicidad o asignaciones bloqueantes (409), reglas de negocio inválidas (422) y petición estructuralmente malformada (400), conforme la política común. No revelar errores SQL ni datos internos.

Listados con page=1, pageSize=25 y máximo 100; estado active por defecto. Orden estable por nombre y luego identidad. Búsqueda de cursos por nombre formal o interno; no agregar un filtro de búsqueda de talleres que no figura en contrato. Query HTTP se adapta sin relajar la configuración global de autenticación.

## Backend y persistencia

Módulo `catalogs`: dominio puro para invariantes compartidas; aplicación para casos de uso y puerto de persistencia; infraestructura Prisma; adaptador Fastify/TypeBox. Composición inyecta implementaciones. El núcleo no importa Prisma, Fastify, TypeBox ni configuración. No se incorporan dependencias de producción nuevas.

Tablas separadas `course` y `workshop`, con UUID, campos canónicos, arrays de días/turnos, estado lógico, timestamps y versión inicial 1. Migraciones aditivas, checks de valores y arrays no vacíos/sin repetidos, índices únicos normalizados para nombre y nombre interno no nulo, actualización de updated_at por trigger.

La escritura bloquea la fila destino, lee estado/versionado dentro de esa transacción, compara la versión recibida y actualiza con condición de versión e incremento. Las lecturas y escrituras de una misma operación comparten transacción real. Una consulta previa fuera de transacción no protege la operación.

Para reglas de asignaciones se valida, bajo el mismo bloqueo, que no existan responsables al desactivar ni turnos ocupados entre los retirados. Una guarda SQL puede reforzar estas invariantes, pero no sustituye la coordinación entre operaciones. Como el módulo de asignaciones todavía no existe, no crear personal ficticio ni declarar probada la integración. La futura creación/cambio de asignación debe bloquear la misma fila destino, validar activo/turno y escribir en la misma transacción. Al afectar varios destinos, bloquearlos en orden estable de tipo e identidad para reducir interbloqueos. Este acuerdo debe propagarse a la especificación de asignaciones antes de habilitarla.

La integridad real frente a carreras necesita pruebas PostgreSQL; dobles de repositorio solo verifican el caso de uso. El protocolo documentado no acredita que una feature futura lo cumpla.

## Carga inicial por base de datos

Dos migraciones ordenadas: creación de esquema y restricciones; inserción de los registros definidos en el alcance. Los valores exactos están en `docs/functional/alcance-prototipo.md` y `docs/technical/backend/database-design.md`; las pruebas deben contrastar la migración contra esas fuentes.

Prisma registra la migración aplicada y no vuelve a ejecutar sus INSERT. No usar upsert de arranque que restaure valores originales sobre ediciones, ni carga desde frontend. Fallas de unicidad en una instalación preexistente requieren reconciliación explícita: no ignorar conflictos ni marcar migraciones como aplicadas sin comprobar su estado. No ejecutar seed/reset ni migraciones en producción desde una PR.

## Frontend

Feature `catalogs` con cliente HTTP, formularios y páginas, conectada desde app. DTO generados desde OpenAPI; respuestas externas validadas en el límite. TanStack Query para estado remoto, React Hook Form y Zod para formularios. No almacenar sesión ni catálogos en localStorage.

Query keys incluyen tipo, estado, búsqueda y página. Tras éxito invalidar el catálogo correspondiente. Una edición conserva la versión capturada al abrir el formulario, aunque se refresque el listado; no reemplazarla automáticamente para esquivar conflictos. Mantener borrador y error hasta acción explícita. Una recarga deliberada puede cancelar el borrador antes de consultar el registro vigente. Respetar el cierre de sesión y cancelación de consultas del sistema existente.

Textos españoles, nombres técnicos ingleses, etiquetas y controles nativos accesibles. Acciones pendientes deshabilitadas, errores visibles y confirmación de baja. No introducir librería visual ni dar por aprobado el diseño pendiente.

## Coordinación de repositorios

La fuente del contrato es kume-admin-docs. La adición de versión es un cambio incompatible para clientes que escribían sin ella; coordinar frontend/backend. Antes de publicar: incorporar el contrato a un commit canónico autorizado, sincronizar revisión y hashes en ambos consumidores, regenerar DTO/esquemas, ejecutar controles y acordar despliegue compatible.

Ambos consumidores fijan el contrato del commit canónico 1e650636705371f09be51a8c77a67f39e5251ba3 con hashes y tipos regenerados, sin pendingContract. Ese commit contiene la revisión aprobada y este registro posterior no cambia su contrato. Maxi autorizó los commits; la publicación remota y el despliegue siguen pendientes.

## Verificación y reversión

Unitarias: normalización, campos obligatorios, arrays inválidos, null/omisión, estado, versión antigua y propagación de conflictos/fallas. Frontend: validación, carga/vacío/error, filtros, confirmaciones, petición con versión, conservación del borrador y no reintento automático. Contrato: validar OpenAPI y comparar métodos, rutas, cuerpos, parámetros, respuestas y tipos generados.

Controles: formato, lint con límites, tipos, unitarias, build y contract:check de ambos repositorios; validar schema y revisar SQL. Registrar por separado la ejecución real de migraciones, persistencia, proxy y concurrencia. No incorporar Playwright ni declarar acordada una suite de integración nueva: usar la política de pruebas vigente.

Riesgo alto por persistencia y concurrencia. Reversión: retirar rutas y pantallas de esta feature y volver al artefacto anterior; conservar tablas/datos. No generar down destructivo. Respaldar antes de aplicar migraciones en instalación existente. Si se reabre escritura con una versión anterior de la aplicación, comprobar compatibilidad y evitar dos versiones escribiendo sin el mismo protocolo.
