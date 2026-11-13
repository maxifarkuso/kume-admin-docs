# Personal — Diseño técnico

Fecha: 13 de noviembre de 2026. Diseño para implementación autorizada; contrato canónico en kume-admin-docs/openapi.yaml.

## Contrato y compatibilidad

StaffMember y StaffMemberSummary exponen version positiva, inicial 1. PATCH exige version y al menos un campo editable. Baja exige endDate/version; reactivación y DELETE documental/asignación exigen JSON {"version":1}. POST documento exige multipart name, version y file, una vez cada uno y en cualquier orden. POST asignación exige version de staffMemberId; PUT exige version de la propietaria original y, si cambia staffMemberId, targetStaffVersion de la receptora. Ambas fichas se versionan una vez al transferir. No se aceptan transferencias sobre fichas inactivas. Tras mutar documentos/asignaciones o recibir 204, consultar ficha para obtener versión actual; no avanzar versiones por cálculo local. 409 VERSION_CONFLICT frente a versión antigua, DUPLICATE_NIC para cédula repetida, ASSIGNMENT_OCCUPIED para destino/turno ocupado; consultar asignaciones filtradas para identificar ocupante y ofrecer ficha. Mantener errores 404/422/413/415 y protección de sesión/origen existentes.

Cambio incompatible de escrituras de personal: sincronizar contrato inmutable, generar tipos y adaptar consumidores antes del despliegue coordinado. No modifica gastos ni catálogos. El detalle incluye documentos y asignaciones actuales; sus listados específicos siguen paginados.

## Backend y persistencia

Módulo staff con dominio puro, aplicación/puertos, HTTP y persistencia. La ficha es raíz transaccional de datos, estado, asignaciones y documentos. El puerto change bloquea fichas en orden UUID estable, lee/valida versión dentro de la transacción y ejecuta una intención validada por el dominio/aplicación. Transferencia bloquea propietaria original y receptora; comprobar de nuevo propietario para impedir carrera. Inactivar elimina asignaciones y cambia estado/egreso bajo ese mismo bloqueo.

Las asignaciones bloquean destinos anterior/nuevo en orden tipo/UUID, compartiendo filas con cambios/bajas de catálogos; validar activo, turno y ocupación dentro de la transacción. Baja de personal bloquea también destinos de sus asignaciones. Índices únicos parciales (course_id,shift)/(workshop_id,shift), FK restrictivas, XOR destino, estado/egreso coherentes y checks de texto/roles/turnos/archivos. Reutilizar catalog_assignments_blocked ya existente: la nueva tabla activa su comprobación real. No cambiar versiones de catálogos al asignar: sus bloqueos protegen invariantes; versión de ficha detecta cambios visibles.

Migración aditiva crea staff_member, assignment y staff_document, sin reset ni borrado de datos preexistentes. Prisma/SQL solo en infraestructura; sin tipos ORM en dominio o aplicación. Validar fechas civiles reales y cédula normalizada a dígitos con dígito verificador uruguayo; no guardar cédulas duplicadas por puntuación. Teléfono obligatorio libre, email opcional válido. No registrar datos personales.

Extraer el adaptador de archivos existente a infraestructura compartida y conectarlo desde composition. Mismo volumen privado y claves UUID opacas; sin dependencia de staff en internals de expenses. La carga ocurre antes de abrir transacción SQL; en fallo/versión antigua eliminar el nuevo archivo, registrar limpieza fallida. Borrar fila documental e incrementar versión en commit antes de eliminar contenido. Descarga comprueba pertenencia documento/ficha y sesión. Nunca publicar storageKey.

## Frontend

Feature staff con API validada con Zod y DTO generados, formularios React Hook Form/Zod, páginas listado/editor/detalle y componentes de asignaciones/documentos. URL conserva búsqueda, estado y página. Capturar versión al abrir formulario/confirmación o seleccionar archivo; consultas en segundo plano no la reemplazan. Conflicto conserva borrador y selección; recargar exige descartar explícitamente. Después de éxito invalidar staff, assignments y catálogos afectados. Ver conflictos con enlace a ficha ocupante y regreso a original. Sin reintentos automáticos de escrituras.

Reutilizar cliente autorizado, Dialog, Notice, FileField, Icon y protección de navegación. Visual vigente institucional, textos españoles, filtros 44 px, acciones visibles, foco y mensajes asociados. Formularios en páginas completas; baja/retirada/eliminación con confirmaciones. Documentos inactivos solo consultables/descargables.

## Verificación, riesgos y reversión

Riesgo alto: datos personales, archivos y transacciones. Unitarias de fechas/cédula/reglas, coordinación mediante dobles, conflictos, compensación y comportamiento UI. Ejecutar formato/lint/tipos/tests/build/contract:check de cada repo. Comprobar SQL estáticamente y Prisma validate; no atribuir prueba PostgreSQL a mocks. Ensayos reales de carreras, migración, proxy, navegador y restauración se registran por separado. Sin dependencias nuevas ni pruebas de integración obligatorias no acordadas.

Reversión de código: artefacto anterior compatible, conservar tablas/archivos; no migración down destructiva. Aplicación productiva y respaldo/ventana son tarea autorizable aparte; no ejecutar Oracle ni desplegar.
