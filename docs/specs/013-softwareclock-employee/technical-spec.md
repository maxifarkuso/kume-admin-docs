# CU2 — Propuesta técnica

## Límites e identidad

CU0 provee el cliente backend de solo lectura y la configuración de conexión. Elegir la conexión del lado servidor y separar su identificador lógico/empresa de la generación de credenciales. Validar que el alcance corresponde a la empresa esperada. Consultar `GET /api/Employees/employee-by-rut?document=…` con la cédula normalizada. La cédula es única por empresa. Validar el objeto, sus tipos y la coincidencia del documento. La respuesta semántica `code: 404` y `message: "Empleado no encontrado."` se clasifica como ausencia tanto con HTTP 200 como con HTTP 404. Otros errores se conservan como fallas del proveedor.

Reutilizar la cédula validada de Personal. Propuesta de comparación: recortar espacios y quitar únicamente los separadores de presentación admitidos (espacios, puntos y guiones), exigir dígitos y conservar ceros, sin completar ni recalcular el documento externo. Validar formatos y tipos reales antes de adoptar la regla. Guardar por separado el texto exacto recibido y la clave normalizada. Usar nombres solo en la vista previa. `id` es candidato a clave de identidad, sujeto a confirmación de estabilidad, unicidad, alcance y representación. `code` es metadata de empleado y se mantiene separado del código de asistencia. Un ID inválido o con representación numérica sin precisión suficiente bloquea la vinculación. La validación de identidad externa es condición de habilitación, incluso con una coincidencia documental.

Para la resincro exigir misma identidad validada, alcance y documento normalizado, y una observación única. Un cambio en el valor exacto usado como filtro exige revalidación explícita. Si cambia la cédula en Personal o se confirma evidencia fiable de discrepancia, suspender la aptitud para nuevas importaciones. CU3 comprueba también el documento vigente en cada lectura del vínculo. Un timeout, empleado no encontrado o respuesta inválida conserva el último vínculo y se informa como problema de consulta o revisión según la evidencia. Si una preparación detecta una discrepancia concluyente, registrar en una transacción versionada la suspensión y su auditoría, sin sustituir los datos confirmados. Revalidar la versión de ficha y vínculo antes de registrar la suspensión. Una revisión posterior puede validar nuevamente la misma identidad o reemplazarla mediante una operación administrativa explícita a diseñar. Preservar la revisión y la vigencia de cada identidad, incluidas las importaciones realizadas con ella.

## Resolución del horario

CU1 aporta la correspondencia vigente dentro de la misma conexión/empresa y su definición local versionada. Exigir una asociación confirmada e inequívoca. Un código no vacío es evidencia solo según las garantías validadas por CU1. Para códigos vacíos o duplicados, requerir evidencia adicional validada del proveedor o una correspondencia explícita que pueda verificarse contra la asignación individual. El texto del turno se conserva para presentación. Devolver `missingReference`, `ambiguousReference` o `missingDefinition` cuando corresponda.

La definición estructurada incluye días de semana, intervalos locales y pausas explícitas (lista vacía si se confirmó que no hay pausas). Usar el mismo modelo e invariantes que el horario propio de [010](../010-time-records/technical-spec.md). Acordar soporte nocturno antes de habilitarlo. Confirmar fecha civil de inicio en America/Montevideo, con validación de rangos, solapes, pausas y vigencias. Si corresponde impacto retroactivo, reutilizar la vista de afectados y confirmación de 010 antes de guardar. La copia editada queda versionada como horario personal, con un origen histórico inmutable. La sincronización posterior consulta la existencia de cualquier horario personal definido y omite la preparación del inicial en ese caso.

## Contrato HTTP propuesto

Rutas relativas a `/api/v1/staff-members/{staffMemberId}`. Requieren sesión y guardas vigentes de mutación, autorización y validación backend. Respuestas privadas sin caché. Mantener los DTO generados de FE sujetos a la futura actualización canónica.

| Método y recurso | Solicitud y respuesta |
| --- | --- |
| GET `/clock-link` | 200 con estado `unlinked\|linked\|needsReview`, versión del vínculo, observación, referencia externa actual, resolución del horario y referencia histórica si existe. El documento de consulta exacto queda disponible por puerto interno de CU3. |
| POST `/clock-sync-previews` | Recibe `staffVersion`. Devuelve 201 con `previewId`, `expiresAt`, versiones observadas, candidato mínimo si es único, disposición de identidad y estado del horario. Incluir borrador estructurado solo si es elegible. Un resultado de revisión es una vista informativa sin capacidad de confirmación. |
| POST `/clock-sync-previews/{previewId}/confirmation` | Recibe `staffVersion` y decisión `linkOnly\|linkAndInitializeSchedule`. Solo la segunda recibe borrador con `effectiveFrom`, días, bloques, pausas y constancia de vista de impacto cuando corresponda. El servidor obtiene identidad, conexión y procedencia de la vista previa. Devuelve 200 con vínculo, nueva versión de ficha y revisión del horario si se creó. |

Códigos propuestos a reconciliar con el esquema de errores vigente: 400 validación del cuerpo, 401 sesión, 403 autorización, 404 ficha/vista fuera de alcance, 409 `VERSION_CONFLICT` o `CLOCK_LINK_CONFLICT`, 410 vista vencida, 422 horario inválido o decisión no aplicable, 502 respuesta de Clock inválida, 503 indisponibilidad, 504 timeout. Exponer mensajes sanitizados. Diferenciar conflicto local de problema de Clock.

## Persistencia, versiones y auditoría

| Recurso | Datos propuestos |
| --- | --- |
| Vínculo vigente e historial | UUID KUME, ficha, conexión/empresa, ID externo validado, código empleado, documento exacto y normalizado, estado, código/nombre de turno actuales, referencia CU1 nullable, observación y versión positiva. Mantener revisiones históricas inmutables, actor y vigencia de identidad para CU3. |
| Vista previa temporal | ID opaco, actor/sesión, ficha, conexión/generación, snapshot mínimo de candidato, versiones de ficha/vínculo/catálogo/definición/horario y fecha de caducidad. Acceso restringido, purga y retención a acordar. |
| Horario personal | Revisión inmutable con vigencia, bloques y pausas confirmados; origen con alcance, ID y revisión CU1, referencia externa observada y revisión del vínculo. El origen debe poder leerse incluso después de editar el catálogo. |
| Auditoría y recibo de confirmación | Evento con actor, fecha, entidad, operación, motivo codificado, revisiones anterior/nueva y correlación opaca. Recibo con vista, huella protegida de la decisión y resultado mínimo. Evitar payloads, nombres, documentos o secretos en auditoría general y logs. |

Constraints propuestos: un vínculo vigente por ficha y alcance, una identidad externa vigente por alcance, y una inicialización única por ficha. Mantener FKs a ficha y revisiones, con conservación de historia. Imponer vigencias compatibles en el módulo de horarios. Versionar vínculo por separado y comparar/incrementar la versión de ficha de Personal una vez por confirmación aplicada. Cambios de catálogo/definición relevantes participan en el mismo control de versiones.

La consulta externa termina antes de persistir la vista. Al confirmar, en una transacción corta, comprobar propiedad y vigencia, generación de conexión, actividad de la ficha, versiones y restricciones. Serializar la primera creación con las demás escrituras de horario y mantener orden de bloqueo acordado. Guardar vínculo, horario opcional, auditoría y recibo juntos. Ante fallo, revertir toda la operación. Un reenvío idéntico autorizado recupera el resultado ya guardado, incluso si venció la vista, dentro del plazo retenido del recibo. Una decisión distinta sobre una vista consumida genera conflicto. No hay reintento automático con versiones nuevas. El alcance, TTL y plazos son decisiones pendientes.

## Integración entre casos

- **CU0** autentica y ejecuta GET con el conector compartido. CU2 implementaría su adaptador de empleados detrás de un puerto. Las respuestas externas permanecen `unknown` hasta su validación.
- **CU1** mantiene catálogo, correspondencias y definición estructurada. CU2 consume una lectura versionada. El par opcional existente constituye información insuficiente.
- **CU2** coordina vínculo, observación y copia inicial. Resincro de identidad apta actualiza únicamente código de empleado admitido, referencia de turno, metadatos de observación, versiones y auditoría.
- **CU3** recibe por puerto interno conexión, revisión de vínculo e identidad vigentes y el documento exacto. Registra la revisión usada en cada importación y vuelve a comprobar aptitud antes de persistir resultados de una consulta en curso. Valida en entorno autorizado la efectividad de `document` en `getAttendances` antes de importar, sin asumir un filtro por ID. Usa el horario personal vigente para el día.

FE compone la acción en Personal, con cliente HTTP fuera de la vista, TanStack Query para estado remoto y borrador local de formulario. BE separa reglas, caso de uso, adaptadores y composición según arquitectura vigente. OpenAPI, permisos, migraciones y ejecución operativa requieren las aprobaciones correspondientes.

## Contrato del primer hito aprobado

El primer hito publica en OpenAPI las tres operaciones de ficha: `GET /clock-link`, `POST /clock-sync-previews` y `POST /clock-sync-previews/{previewId}/confirmation`. El cuerpo de preparación y confirmación lleva `staffVersion`. La vista previa devuelve una coincidencia revisable con identificador y vencimiento de 15 minutos, o un motivo de revisión sin identificador confirmable. El horario queda pendiente. El contrato de edición de horario de esta especificación corresponde al segundo hito.

La conexión lógica de CU0 es fija en KUME y Clock determina la empresa por el token. Configurar `CLOCK_EMPLOYEE_LOOKUP_EVIDENCE` como `<conexión>:<referencia-de-evidencia>` para el alcance de la conexión con autorización operativa. Maxi acepta la estabilidad del ID como supuesto operativo sin prueba en otro entorno. La variable de evidencia del listado anterior deja de habilitar CU2. Al faltar evidencia para la búsqueda por cédula o el cliente CU0, la ficha oculta la acción y el backend rechaza mutaciones.

La vista previa queda en memoria del proceso backend y se borra al confirmar o expirar. Está asociada a la cuenta, ficha, versión y conexión del proceso. Un reinicio requiere preparar otra vista si todavía no se confirmó. La revisión persistida registra el actor, la observación, la fecha y el identificador opaco de confirmación que permite reproducir el resultado de una operación aplicada. La revisión de cédula de Personal aumenta al cambiar el documento canónico. Una revisión posterior del vínculo requiere confirmación aun si Personal recupera una cédula previa. Un cambio a otra identidad sigue fuera del primer hito.
