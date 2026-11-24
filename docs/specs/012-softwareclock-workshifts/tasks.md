# CU1 — Tareas

- [x] Revisar checkout, fuentes del caso y código del conector CU0. Registrar investigación pública y limitaciones en [hallazgos de API](../../technical/softwareclock-api.md).
- [x] Documentar vista previa, primera importación, reimportación, invariantes y criterios de aceptación propuestos.
- [x] Inspeccionar el OpenAPI aportado por Maxi y registrar qué componentes aparecen y qué operaciones faltan.
- [x] Registrar la ficha Swagger de getWorkShifts, sin parámetros declarados, el esquema del 200 y los errores documentados.
- [x] Registrar la lectura de Maxi con Bearer sin parámetros, coincidencia con su backoffice, HTTP 200, `code: 200`, `message: null` y `work_shifts`.
- [ ] **Investigación en paralelo · CA2, CA3 y CA5.** Confirmar cobertura, paginación, tipos/nulos de filas, alcance en otras conexiones y estabilidad de códigos. Preguntar si hay un GET de detalle de turnos con clave estable, días/bloques/pausas/vigencias y si depende del plan o permisos. Si existe, obtener esquema o muestra anonimizada y verificar enlace con el catálogo. Probar solo lecturas autorizadas.
- [x] Fijar el alcance de catálogo e importación y especificar la edición de inicio y fin en OpenAPI. La revisión del flujo de precarga personal pertenece a su propia entrega.
- [ ] **CA1, CA5, CA8, CA11.** Integrar lector de catálogo con `ClockClient`. Probar HTTP 200 con código JSON 200 y mensaje nulo, HTTP 200 con código JSON distinto de 200, array vacío válido, colección nula o ausente, error de envoltorio, código de turno nulo o ausente, nombre o tipo faltante, tipo inesperado, respuesta que excede límites, fallo de red, HTTP 400/401/404/500 de Clock y pausa por cuota con fixtures. Verificar sesión y ausencia de secretos en respuestas y logs.
- [ ] **CA2–CA4, CA6–CA10, CA12.** Implementar casos de vista previa y confirmación, repositorio y migración revisable. Probar código vacío, códigos repetidos, tuplas idénticas, orden invertido, renombre, cambio de código, sustitución y reaparición histórica. Probar aislamiento de conexiones, dos confirmaciones concurrentes, reenvío, vencimiento, reversión ante fallo intermedio y preservación de horarios y versiones personales.
- [ ] **CA1–CA12.** Implementar pantalla con confirmación explícita, conflictos y estados accesibles. Verificar flujo desde Administración con doble de Clock y luego lectura real autorizada. Registrar por separado evidencia local, de persistencia y del proveedor.

## Escenario de verificación

Usar datos ficticios y el mismo envoltorio observado por Maxi. En cada consulta exitosa el doble de Clock devuelve HTTP 200, `code: 200`, `message: null` y las filas en `work_shifts`. Antes de empezar, guardar el estado y las versiones de los horarios personales y sus excepciones.

| Paso | Entrada o acción | Resultado esperado |
| --- | --- | --- |
| 1 | Llegan `("", "Turno A", "Fijo")`, `("", "Turno B", "Fijo")` y `("X1", "Turno C", "Libre")`. | Tres filas pendientes de decisión independiente. Confirmar las tres altas genera tres UUID y cero bloques calculables. |
| 2 | Llegan las mismas filas en orden inverso. | Tres observaciones repetidas, confirmación deshabilitada y cero cambios de correspondencia. |
| 3 | B cambia a «Turno B revisado». C no aparece en una consulta comparable. | A permanece repetida. B requiere decisión. C se conserva y se informa como no observada. |
| 4 | Vincular «Turno B revisado» al UUID de B y reenviar la misma confirmación. | Se guarda una sola actualización de metadatos y un único resultado de confirmación. La etiqueta local de B y sus horas locales se conservan, incluso si fueron cargadas antes de preparar la vista previa. |
| 5 | Otra vista previa de la revisión anterior intenta crear o vincular la misma observación modificada. | Conflicto de revisión, sin cambios parciales. |
| 6 | Clock responde HTTP 200 con `code: 0`, y después responde HTTP 200 con `code: 200` y `work_shifts: []`. | La primera consulta falla. La segunda muestra catálogo externo vacío. Ambas conservan las tres referencias locales. |
| 7 | Comparar horarios personales, excepciones y versiones con el estado inicial. | Coincidencia exacta y cero órdenes de recálculo. |

[Plan](plan.md) · [Criterios](spec.md#criterios-de-aceptación-propuestos)
