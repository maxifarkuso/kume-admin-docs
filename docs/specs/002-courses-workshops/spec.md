# Cursos y talleres — especificación funcional

Fecha: 7 de noviembre de 2026. Responsable funcional: Maxi.
Estado: alcance solicitado; control optimista aprobado expresamente en esta sesión. Especificación, plan e implementación aprobados expresamente por Maxi en esta sesión. No acredita implementación terminada, despliegue ni aprobación del paso 4 de pantallas.

## Problema y objetivo

La navegación autenticada existe, pero los catálogos de cursos y talleres siguen pendientes. La secretaria y Maxi necesitan consultar y administrar los destinos que posteriormente utilizarán las asignaciones de personal. La instalación debe disponer de los catálogos iniciales sin cargarlos a mano ni depender del navegador.

Ambos usuarios conservan los mismos permisos. Todas las operaciones requieren sesión válida y las escrituras mantienen la protección de origen y cabecera del sistema.

## Alcance

Crear, listar, consultar, editar, desactivar y reactivar cursos y talleres. La baja es lógica; se conserva identidad y datos. No existe eliminación física en este bloque.

El curso contiene nombre formal, nivel, nombre interno opcional, días y turnos. El taller contiene nombre, días y turnos; no tiene nivel ni nombre interno. Los límites exactos y la representación JSON pertenecen a OpenAPI; el alcance funcional y los datos iniciales pertenecen a `docs/functional/alcance-prototipo.md`.

## Flujos y criterios de aceptación

| ID   | Escenario                                       | Resultado observable                                                                                                                                                                                                           |
| ---- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AC1  | Abrir un catálogo                               | Activos por defecto; orden por nombre; estados de carga, vacío y error con reintento.                                                                                                                                          |
| AC2  | Consultar o filtrar                             | Filtro activos/inactivos/todos, paginación y detalle por identidad; cursos admiten búsqueda por nombre formal o interno. Filtros y página se conservan tras errores.                                                           |
| AC3  | Crear                                           | Datos válidos generan un registro activo con versión inicial 1. Nombres vacíos o solo espacios, días/turnos vacíos, duplicados o desconocidos impiden guardar.                                                                 |
| AC4  | Editar                                          | Los campos omitidos se conservan. `null` limpia únicamente el nombre interno opcional. Se validan las mismas reglas que al crear. Unicidad sin distinguir mayúsculas ni espacios exteriores, también para registros inactivos. |
| AC5  | Desactivar                                      | Confirmación previa en UI; se conserva el registro. Si tiene asignaciones en cualquier turno, se bloquea la baja sin retirar asignaciones automáticamente.                                                                     |
| AC6  | Reactivar                                       | El registro vuelve a estar disponible para nuevas asignaciones. No se recrea ni recupera asignaciones retiradas.                                                                                                               |
| AC7  | Modificar turnos                                | No se permite quitar un turno ocupado. Cambiar los días del taller afecta a todos los días cubiertos por su asignación actual; no se administran días por persona.                                                             |
| AC8  | Dos usuarios modifican el mismo registro        | La primera escritura aceptada incrementa versión; la siguiente con versión anterior recibe 409. No hay sobrescritura ni reintento automático con una versión nueva.                                                            |
| AC9  | Conflicto o falla al guardar                    | Se mantienen los valores escritos y se informa el problema. El usuario puede cancelar y volver a consultar antes de reaplicar sus cambios conscientemente.                                                                     |
| AC10 | Instalar una base vacía                         | La migración carga los siete cursos y tres talleres definidos en el alcance, con días y ambos turnos. Maternal lleva nombre interno nulo.                                                                                      |
| AC11 | Volver a ejecutar migraciones aplicadas         | No se duplican catálogos ni se sobreescriben nombres, días, turnos, estado o versiones editados por los usuarios.                                                                                                              |
| AC12 | Acceso no autorizado o escritura sin protección | Se aplican las respuestas de autenticación y protección existentes; ningún catálogo se expone como endpoint público.                                                                                                           |

## Experiencia de uso

Pantallas accesibles desde Cursos y Talleres en el menú existente. Formularios con etiquetas, selección múltiple de días/turnos y acciones Guardar/Cancelar. Guardado en curso impide duplicar envíos. La baja requiere confirmación y explica que las asignaciones bloquean la operación. No se descarta un borrador por una actualización automática del listado.

Esta especificación define comportamiento; no sustituye una aprobación visual de los marcos pendientes en `docs/ui/continuacion-diseno-pantallas.md`. El detalle de registro puede presentarse en la edición con todos sus campos; no exige una pantalla adicional.

## Fuera de alcance

CRUD de personal y asignaciones, historial de responsables, horarios exactos de talleres, inscripción de alumnos, gastos/rubros, importación masiva, publicación y operación sobre datos reales. No se amplía el versionado a otros recursos en esta entrega.

## Fuentes de verdad

Desde la raíz de kume-admin-docs: `docs/functional/alcance-prototipo.md`, `openapi.yaml`, `docs/technical/api-design.md`, `docs/technical/backend/database-design.md` y `docs/general/implementation-decisions.md`.
