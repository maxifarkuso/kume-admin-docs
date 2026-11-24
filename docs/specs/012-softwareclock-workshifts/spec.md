# CU1 — Especificación de importación de horarios laborales

Maxi solicitó Administración → Horarios laborales → Importar desde Clock. El [caso de uso](../../functional/softwareclock/sincronizar-horarios.md) define flujo y secuencias. Esta especificación propone comportamiento verificable para revisión. Maxi confirmó acceso equivalente para Vicky y Maxi con sus cuentas KUME. El contrato HTTP, el modelo persistente y el diseño visual requieren revisión antes de implementar.

La entrega propuesta es un catálogo descriptivo local con importación manual y vista previa. Cada referencia tiene identidad propia de KUME. Las etiquetas de Clock se presentan como texto, incluso si contienen horas. Maxi propuso un par de horas locales opcionales y su uso como precarga de una ficha sin horario propio. El flujo de edición y confirmación personal queda en revisión.

## Referencia visual

[Maqueta de MagicPath y copia de referencia](../../ui/maquetas/importar-horarios-clock/README.md). Permite revisar el catálogo, la selección de altas y correspondencias y el resultado de una confirmación con datos ficticios. La edición de horas locales pertenece a una revisión posterior.

## Criterios de aceptación propuestos

| ID | Dado / cuando | Resultado esperado |
| --- | --- | --- |
| CA1 | Administración abre la pantalla y consulta Clock | Ve catálogo local y vista previa con descripción original, propuesta, motivo y fecha. Cancelar no modifica el catálogo. |
| CA2 | Dos filas sin código tienen contenido distinto | Se pueden crear dos referencias distintas, con UUID local. Al repetir la consulta en otro orden, las observaciones únicas ya confirmadas aparecen sin cambio. |
| CA3 | Llegan códigos duplicados, filas idénticas, un nombre cambiado o un código reutilizado con otra descripción | La vista explica la ambigüedad. Cada fila distinguible puede resolverse explícitamente. Las idénticas se muestran agrupadas por cantidad y ninguna genera un vínculo por posición. Un código único con contenido cambiado solo sugiere revisión. |
| CA4 | Se confirma una correspondencia nueva para una referencia con nombre y definición local | Se actualizan los metadatos externos y el historial. UUID, nombre local y definición local se conservan. El nombre externo y el tipo jamás producen bloques ni minutos calculables. |
| CA5 | Clock devuelve una lista vacía, omite una referencia o falla con timeout, 429, respuesta inválida o rechazo de autenticación | La referencia previa y sus datos locales se conservan. Se distingue ausencia en consulta comparable, respuesta vacía y fallo. Un fallo no se presenta como respuesta vacía ni cierra la sesión KUME. |
| CA6 | Se reenvía una confirmación idéntica tras perder la respuesta, o dos administradores confirman la misma versión | El reenvío recupera el resultado previo. La segunda operación incompatible recibe conflicto sin cambios parciales ni reintento automático. |
| CA7 | Antes de importar existen horarios de maestras, excepciones, vigencias e historial | Tras primera importación, reimportación o fallo, sus valores y versiones son idénticos. Tampoco se emiten órdenes de recálculo. |
| CA8 | Se confirma desde otra cuenta, con una vista previa vencida o con filas ajenas a la consulta | Se rechaza con el error correspondiente y se preserva el catálogo. El navegador no recibe token, credenciales ni errores crudos de Clock. |
| CA9 | Se confirma una referencia sin bloques, incluso una de tipo Libre | La referencia es descriptiva. Solo las horas locales cargadas explícitamente pueden proponerse como precarga personal. |
| CA10 | Una persona modifica la correspondencia de una referencia y vuelve a importar | Se conserva el historial de ambas observaciones. Solo la correspondencia vigente habilita «Ya observada»; recuperar una anterior exige revisión. |
| CA11 | El catálogo trae código nulo u omitido, o una fila sin nombre o tipo | El código se trata como ausente para correspondencias. La fila sin nombre o tipo queda visible como pendiente y no se puede confirmar. |
| CA12 | Una referencia tiene inicio y fin locales y se confirma una reimportación | Ambas horas quedan intactas. Las altas desde Clock las inicializan vacías. |

[Propuesta técnica](technical-spec.md) · [Plan](plan.md) · [Tareas](tasks.md)
