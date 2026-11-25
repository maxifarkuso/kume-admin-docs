# CU2 — Especificación funcional y aceptación

La [regla aprobada](../../functional/softwareclock/sincronizar-empleado.md) define la fuente del horario inicial. La ubicación precisa, textos secundarios y controles se proponen para revisión. Se conservan las reglas de [Personal](../005-staff/spec.md) y del [sistema visual](../../ui/sistema-visual.md).

En Datos de la ficha activa, mostrar el botón «Sincronizar empleado con Clock», el estado del vínculo y, si corresponde, el turno informado por Clock. Una ficha inactiva permite consultar el vínculo histórico. El rol de la ficha es informativo y la sincronización lo conserva. El horario personal se propone cuando la ficha es elegible para Horario laboral. En el diálogo, mostrar el origen y la observación del vínculo, el resultado de resolución y las acciones disponibles.

| Estado | Comportamiento |
| --- | --- |
| Sin vínculo / vinculado | Preparar consulta. Si ya existe vínculo, mostrar turno externo actual y última sincronización. |
| Consultando / guardando | Estado anunciado, confirmación deshabilitada durante la operación. Cancelar la vista previa antes de guardar. |
| Coincidencia única | Confirmación de identidad con documento y nombre externo. |
| Horario inicial disponible | Editor con días, bloques, pausas y vigencia. Permitir confirmar identidad sola o guardar también el horario validado. |
| Horario pendiente de configurar/vincular | Mostrar el motivo y acceso a Horarios laborales. Permitir confirmar solo la identidad y volver a la preparación cuando el catálogo esté listo. |
| Horario propio definido | Mostrar el turno actual y el origen histórico del horario como datos distintos. Omitir el editor inicial. |
| Requiere revisión | Explicar ausencia, cambios de identidad o discrepancias de documento. Guardado bloqueado. |
| Error o conflicto | Conservar registro previo y borrador local para revisión. Ofrecer preparar una vista nueva con confirmación explícita. |

Diálogo con foco inicial, navegación por teclado, mensajes asociados a campos y retorno del foco al botón. Los estados se expresan con texto además del color.

| ID | Criterio |
| --- | --- |
| CU2-01 | Una lectura completa, documento único y confirmación persisten el vínculo. Formatos equivalentes conservan el documento externo exacto, incluidos ceros. |
| CU2-02 | Sin coincidencia o con documento inválido o discrepante, se indica revisión. La similitud del nombre y la coincidencia del código de asistencia carecen de efecto. |
| CU2-03 | Una asignación inequívoca y una definición completa precargan una sola vez. Editar apertura o pausa y confirmar una fecha guarda exactamente la versión validada y su procedencia. Cancelar descarta las escrituras. |
| CU2-04 | Turno faltante, ambiguo, código vacío sin resolución fiable o solo un par de horas dejan pendiente el horario. Identidad y referencia externa pueden guardarse. El acceso al catálogo indica la acción siguiente. |
| CU2-05 | Una vez resuelto el catálogo, administración puede iniciar otra preparación para la ficha vinculada sin horario. Solo la acción explícita puede crear la primera vigencia. |
| CU2-06 | Resincro con otro turno conserva horario, origen histórico, roles, asignaciones y datos personales. |
| CU2-07 | Cambio de documento, identidad incompatible o duplicación en otra ficha exige revisión, preserva historial y bloquea nuevas importaciones cuando el vínculo ya no es apto. |
| CU2-08 | Vencimiento, cambio concurrente, error del proveedor y errores de guardado preservan datos anteriores. Repetir una confirmación idéntica produce un único resultado, horario y evento de auditoría. |
| CU2-09 | Operaciones autorizadas solo desde administración y sobre ficha activa para escritura. CU3 obtiene un vínculo apto y el documento exacto sin buscar de nuevo al empleado. |
