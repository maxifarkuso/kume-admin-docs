# Registro de pagos — especificación funcional

Fecha: 8 de noviembre de 2026. Responsable funcional: Maxi.
Estado: especificación e implementación local preparadas. Maxi solicitó avanzar con especificación técnica, plan e implementación y aprobó versionado de gastos/rubros, cambios de contrato, America/Montevideo y @fastify/multipart. La autorización inicial de solo especificación quedó ampliada por esas decisiones. No acredita despliegue, verificación integrada ni aprobación del paso 4.

Ver [diseño técnico](technical-spec.md), [plan](plan.md), [tareas](tasks.md) y [evidencia de implementación](implementation.md).

## Problema y objetivo

La secretaria necesita consolidar los gastos ya pagados de KUME, conocer el total por período y rubro y recuperar el comprobante de cada registro. En este módulo, «pago» significa un gasto realizado; no representa cobranzas a familias.

## Alcance y fuentes

Incluye registro, consulta, edición, anulación y restauración de gastos, consulta y reemplazo de comprobantes, filtros, total y CSV. La administración de rubros es una dependencia funcional: deben existir rubros activos para registrar gastos. Su CRUD y carga inicial se mantienen según el alcance vigente; el versionado de gastos y rubros se amplía según la aprobación posterior de Maxi.

Las reglas pertenecen al [alcance](../../functional/alcance-prototipo.md), el comportamiento HTTP al [diseño de API](../../technical/api-design.md) y los campos y operaciones exactos al [OpenAPI canónico](../../../openapi.yaml). La persistencia sigue el [diseño de base](../../technical/backend/database-design.md). No se añaden endpoints, campos ni migraciones en esta entrega.

## Flujos y criterios de aceptación

| ID   | Escenario                 | Resultado observable                                                                                                                                                                                 |
| ---- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AC1  | Abrir Gastos              | Mes actual y gastos activos por defecto; listado paginado, total del período y estados de carga, vacío y error.                                                                                      |
| AC2  | Registrar un pago         | Fecha de pago, importe UYU positivo con dos decimales, destinatario, concepto, rubro activo y exactamente un comprobante obligatorio. La fecha no puede ser futura.                                  |
| AC3  | Validar formulario        | Se aplican límites y formatos canónicos; errores junto al campo y valores conservados para corregir. No se guarda sin comprobante válido.                                                            |
| AC4  | Adjuntar archivo          | Se admite PDF, JPG o PNG de hasta 10 MB. Se comprueban tamaño, extensión, MIME y firma real; un archivo rechazado no deja un gasto creado.                                                           |
| AC5  | Guardar                   | Se impide duplicar envíos mientras se procesa. Al completar, se vuelve al listado conservando filtros y página; si queda fuera del filtro, se ofrece «Ver gasto».                                    |
| AC6  | Consultar detalle         | Se muestran datos, rubro, estado y metadatos del comprobante. Desde listado y detalle se abre el comprobante en pestaña nueva y se permite descargarlo con sesión válida.                            |
| AC7  | Editar                    | Solo un gasto activo admite cambios; los campos omitidos se conservan. Puede conservar su rubro desactivado, pero no seleccionar otro rubro inactivo.                                                |
| AC8  | Reemplazar comprobante    | Acción independiente desde el detalle, con confirmación y las mismas validaciones. Un fallo conserva el comprobante vigente; no se elimina antes del commit. No se mantiene historial de reemplazos. |
| AC9  | Anular                    | Tras confirmar se conserva el gasto y su archivo; deja de sumar en los totales y queda en solo lectura.                                                                                              |
| AC10 | Restaurar                 | El gasto vuelve a activo y vuelve a sumar cuando coincide con los filtros. No se crea un registro nuevo.                                                                                             |
| AC11 | Filtrar                   | Selector de mes o fechas desde/hasta, rubro y estado activo/anulado/todos. Se aplican filtros por fecha de pago, no por fecha de compra ni de carga.                                                 |
| AC12 | Totalizar                 | El total abarca todo el conjunto filtrado, independientemente de la página, y excluye siempre anulados. Un filtro de solo anulados produce total cero.                                               |
| AC13 | Exportar                  | El CSV incluye todo el conjunto filtrado sin paginación, incluidos anulados si el filtro los contempla. Columnas y codificación según API; el importe se conserva sin pérdida de precisión.          |
| AC14 | Rubro desactivado         | Los gastos históricos conservan su asociación y pueden consultarse; el rubro no se ofrece para nuevos gastos.                                                                                        |
| AC15 | Error o sesión vencida    | Se informa el problema en español sin detalles internos. No se comunica éxito sin confirmación del servidor ni se reenvía automáticamente una escritura de resultado incierto.                       |
| AC16 | Acceso a datos y archivos | Tanto Maxi como Vicky requieren sesión y conservan los mismos permisos. Se aplica la protección de origen y cabecera existente en escrituras; los archivos no tienen acceso público.                 |

## Experiencia de uso

Se reutilizan los bocetos G01–G05 y las decisiones de [continuidad de pantallas](../../ui/continuacion-diseno-pantallas.md): formularios en páginas completas, confirmaciones de anulación y reemplazo, y consulta de anulados sin edición hasta restaurar. Los textos visibles son en español y el diseño prioriza escritorio. Esta especificación no completa los pendientes visuales ni el prototipo interactivo.

Ejemplo ficticio: una compra del 31 de octubre pagada el 2 de noviembre por UYU 1250,50 suma en noviembre. Si se anula, sigue siendo consultable y deja de sumar; al restaurarla vuelve a integrar el total de noviembre.

## Integridad y verificación futura

La creación debe coordinar gasto, metadatos y archivo sin registros incompletos tras un error. El reemplazo confirma primero la referencia nueva y luego limpia el archivo anterior; una limpieza fallida se registra para recuperación, preservando el archivo vigente. El procedimiento propietario está en el diseño de API.

Antes de implementar deben prepararse pruebas de importes exactos, límites temporales, totales entre páginas y estados, rubros inactivos, validación y fallos de archivos, anulación/restauración, filtros y CSV, y autorización de datos y descargas. Los respaldos deben incluir base y archivos; definir esta necesidad no acredita su funcionamiento.

## Decisiones y pendientes

- Control de concurrencia resuelto posteriormente: versión de gastos/rubros y 409 `VERSION_CONFLICT` aprobados el 8 de noviembre; incluye el reemplazo de comprobantes. Contrato local ampliado; sincronización inmutable pendiente.
- Dinero y fechas resueltos: centésimos bigint en el núcleo, texto decimal en HTTP y día de negocio America/Montevideo.
- Referencia canónica inmutable, verificación integrada y despliegue pendientes; ver evidencia de implementación.

## Fuera de alcance

Cobranzas, cuotas, sueldos, deudas, vencimientos, pagos parciales, otras monedas, catálogo de proveedores, importación histórica o masiva y exportación Excel. La implementación fue solicitada posteriormente; versionado, contratos y dependencia multipart fueron aprobados expresamente después. No se autorizaron despliegue, migraciones de producción, commit ni push en esta entrega.
