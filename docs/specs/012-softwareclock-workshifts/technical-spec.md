# CU1 — Propuesta técnica

## Lectura mediante CU0

En `kume-admin-be` main, revisión `c9279b3`, composición ya instancia `ClockClient` mediante `configureSoftwareClock` y lo entrega a `createApp`. La lista de rutas de lectura ya incluye `/api/EmployeesWorkShifts/getWorkShifts`. Reutilizar esa instancia mediante inyección explícita en el adaptador del puerto de catálogo. CU1 aporta su decodificador a `ClockClient.read(path, decode, signal)`; el cliente compartido conserva credenciales, transporte, límites y clasificación de fallos. La configuración revisada aún no activa renovación por rechazo de Bearer. CU1 no agrega otra política de renovación. Esta inspección de código acredita infraestructura disponible, con verificación operativa pendiente. [Diseño de CU0](../011-softwareclock-auth/technical-spec.md).

En infraestructura, validar la respuesta desde `unknown`. La [ficha Swagger](../../technical/softwareclock-api.md#ficha-swagger-de-getworkshifts-aportada-por-maxi) documenta HTTP 200 con `GetWorkShiftsDto`. El cliente compartido exige HTTP 200 antes de decodificar. El decodificador de CU1 exige además `code: 200` numérico y `work_shifts` como array, según la [respuesta de Maxi](../../technical/softwareclock-api.md#lectura-real-de-catálogo-aportada-por-maxi). Aceptar `message: null` o texto y descartar su contenido. Rechazar un código distinto, incluso el cero del ejemplo Swagger, hasta contar con evidencia que justifique admitirlo. Un array vacío válido se distingue de un error, una colección nula o un campo ausente.

Cada fila documenta `code`, `name` y `type` como textos anulables. Conservar los textos exactos y la multiplicidad. Un código nulo, vacío u omitido se trata como ausente para sugerir correspondencias. Si falta nombre o tipo, o alguno es nulo, mostrar la fila como pendiente sin habilitar confirmación. Una forma exterior inesperada, una fila con tipos incompatibles o un límite superado invalidan la vista entera. Distinguir nulo, omisión y texto vacío al registrar observaciones. Fijar límites de filas y tamaño de campos con evidencia. Usar la ruta fija sin parámetros declarados. Si la prueba autorizada devuelve 400 o 404, aclarar con el proveedor la resolución de empresa antes de introducir una cabecera o parámetro. Un 400, 401, 404 o 500 externo termina la consulta con fallo y conserva el catálogo. El 401 documentado no distingue token vencido de falta de autorización.

## Modelo persistente propuesto

| Unidad | Responsabilidad |
| --- | --- |
| `workshift_reference` | UUID local, etiqueta local inicializada desde el nombre al crear, versión y datos de auditoría. Incluye `localStartTime` y `localEndTime`, horas locales anulables de KUME. |
| `clock_workshift_correspondence` | Conexión KUME, UUID de referencia local y observación externa vigente `(code, name, type)` exacta. Una correspondencia vigente por referencia y conexión, y un solo destino vigente por tupla distinguible dentro de la conexión. |
| Vista previa | ID opaco, cuenta KUME, conexión, alcance y generación de configuración, versiones, fecha de consulta y vencimiento, filas con identificadores efímeros y conteos. Contexto temporal del servidor, sin secretos. |
| Confirmación e historial | ID de vista previa único, decisiones normalizadas, resultado y actor/fecha. Registrar metadatos anteriores y nuevos para altas y cambios de correspondencia, sin guardar el cuerpo crudo ni datos ajenos al caso. |

La conexión identifica la cuenta/empresa configurada, con ID interno independiente de secretos. Cambiar de empresa invalida vistas previas y mantiene las correspondencias aisladas. Rotar credenciales de la misma cuenta no reasigna identidades. Usar igualdad exacta de tuplas para comparar contenido, con representación sin ambigüedad y comparación coherente entre aplicación y persistencia. Si se usa huella para indexar, verificar la tupla exacta. Una huella detecta observaciones repetidas y carece de autoridad para identificar un turno en Clock. El UUID local es la identidad durable.

## Horas locales y precarga personal propuesta

Persistir inicio y fin como `TIME WITHOUT TIME ZONE` de precisión de minuto. Ambos quedan nulos al crear una referencia desde Clock. Proponer edición como un par completo o ambos vacíos, con formato `HH:mm` y fin posterior al inicio para el primer alcance de un bloque diurno. Los turnos que cruzan medianoche requieren una regla explícita antes de admitirse. La edición local usa la versión de la referencia. La confirmación de catálogo conserva ambos campos y solo escribe metadatos externos en una vinculación.

Si el workshift de una maestra se resuelve de forma inequívoca a una referencia KUME con las dos horas, proponer ese par como bloque inicial editable al importar la ficha, siempre que todavía no tenga horario propio. Copiar los valores tras confirmación, sin vínculo vivo. Los días y la vigencia provienen de la configuración personal confirmada. Las pausas se completan si corresponden. Una referencia sin par completo o sin correspondencia inequívoca deja la precarga pendiente. Conservar la precarga desde cursos aprobada y revisar cómo presentar ambas fuentes si difieren. El flujo de ficha pertenece a su propia entrega y los horarios existentes se conservan.

## Reglas de comparación

1. Clasificar primero la multiplicidad de la tupla completa. Las tuplas indistinguibles quedan pendientes, incluso si antes eran únicas. Duplicar el código con otra tupla se indica por separado.
2. Una tupla única con correspondencia vigente exacta se informa como observación repetida. No crea otra referencia, reactiva vínculos históricos ni modifica el catálogo. Esta regla describe igualdad observada, con identidad externa aún sin verificar.
3. Una tupla única sin correspondencia vigente exige una decisión explícita. Código no vacío, único en la consulta y con un único candidato vigente del mismo alcance puede sugerir un destino. Un código compuesto solo por espacios cuenta como ausente para sugerencias. Con duplicados o código ausente se habilita búsqueda manual en el catálogo. Si se confirma sustituir una observación vigente, mostrar antes y después y conservar la anterior en historial. Si la observación ya tiene otro destino vigente, rechazar el cruce. Una referencia solo puede recibir una fila por confirmación.
4. Las ausencias se muestran solo al comparar consultas válidas de alcance identificable e igual. Son informativas. Capturas con cobertura no demostrada no justifican bajas.

Ejemplo ficticio. La primera consulta trae dos filas sin código, «Turno A» y «Turno B», ambas de tipo Fijo. Se crean dos UUID. En una segunda consulta el orden se invierte y «Turno B» pasa a «Turno B revisado». A se muestra como repetida. B queda sin correspondencia exacta hasta que administración la vincula al segundo UUID. La etiqueta local y cualquier configuración de B se conservan. Si además llegan dos copias idénticas de A, se muestra la multiplicidad y la correspondencia previa se conserva sin aplicarla a ninguna copia.

## Contrato HTTP propuesto para revisión

| Operación candidata | Entrada y salida |
| --- | --- |
| GET `/api/v1/workshift-references` | Listado local con UUID, etiqueta local, horas locales opcionales, metadatos externos vigentes y versión, aunque Clock esté desconectado. |
| POST `/api/v1/workshift-import-previews` | Consulta Clock desde backend para la conexión configurada. Devuelve ID de vista, vencimiento, fecha y filas con ID efímero, clasificación, motivos y candidatos. |
| POST `/api/v1/workshift-import-previews/{previewId}/confirmation` | Recibe decisiones por ID de fila, acción `create` o `link` y, para `link`, UUID destino y versión observada. Omitir una fila elegible equivale a dejarla pendiente. Exigir al menos una decisión aplicable. Una vista sin cambios se cierra sin confirmar. Devuelve el resultado persistido con recuentos y referencias afectadas. |

Usar guardas de sesión y de mutación vigentes. Maxi confirmó que su cuenta y la de Vicky tienen el mismo acceso para listar, preparar y confirmar importaciones, sin roles adicionales. Cada vista previa pertenece a la cuenta que la preparó. Verificar autorización en cada operación, también en reintentos. El servidor obtiene el contexto de conexión y reconstruye las escrituras desde la vista previa. Un 401/403 de Clock se representa como fallo de integración, sin alterar la sesión KUME. Usar `application/problem+json` según [diseño de API](../../technical/api-design.md). Proponer 404 para vista ajena o inexistente, 410 para vencida, 400 para estructura inválida, 422 para decisiones inválidas, 409 para conflicto de versión o confirmación previa distinta, 502 para respuesta externa inválida o denegada, 503 para indisponibilidad o cuota, y 504 para timeout. Revisar códigos, límites y retención al aprobar el contrato.

## Confirmación y concurrencia

La llamada externa termina antes de crear la vista previa. Capturar catálogo, correspondencias y revisión coherente por conexión en una transacción breve. La confirmación se limita a la instantánea revisada y no vuelve a consultar al proveedor. En una sola transacción, serializar confirmaciones por conexión, verificar cuenta, generación de configuración, vigencia, revisión del catálogo, versiones de destinos y restricciones. Aplicar cambios, avanzar revisión si cambia el catálogo y persistir auditoría y resultado juntos. Ante conflicto, revertir todo y pedir otra vista previa. Cualquier futura edición local relevante debe participar en el mismo control de versión. El repositorio de escritura de CU1 se restringe a sus propios recursos, sin acceso de escritura a horarios de maestras.

El ID de vista previa es la clave de una única confirmación. Si ya se confirmó, consultar primero el resultado, previa comprobación de autorización y propiedad. El mismo conjunto de decisiones, sin importar su orden, devuelve el resultado guardado durante su retención, incluso si la vista temporal venció. Un conjunto distinto genera conflicto. Limitar el plazo de vista, volumen y retención de confirmaciones según el uso revisado. Tras purgar la vista o su resultado, el ID no habilita una nueva confirmación.

[Especificación](spec.md) · [Plan](plan.md) · [Tareas](tasks.md)
