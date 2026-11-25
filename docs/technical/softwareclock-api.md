# SoftwareClock — Hallazgos de integración

> **Continuación por caso de uso:** [CU1 horarios](../functional/softwareclock/sincronizar-horarios.md), [CU2 empleado](../functional/softwareclock/sincronizar-empleado.md), [CU3 horas](../functional/softwareclock/registro-horas.md). [Índice y prompts](../functional/softwareclock/README.md). La documentación anterior conserva evidencia y contexto; los turnos ya tienen muestra de respuesta documentada.

Fecha: 16 de noviembre de 2026. Evidencia: colección adjunta `Clock Api V.1.0.0.postman_collection.json` (actualizada el 12/10/2025), pruebas ejecutadas por Maxi y ejemplo ficticio de respuesta. No se reproducen credenciales, tokens ni datos reales. No se guardó la colección privada en el repositorio.

## Estado de validación

**Autenticación y consulta de asistencias confirmadas por Maxi con HTTP 200.** Conectividad básica viable; no equivale a integración implementada ni validación completa del proveedor. El prototipo no realiza solicitudes reales.

| Evidencia | Resultado y alcance |
| --- | --- |
| Maxi habilitó «API Software Clock» | Aparecieron creación de usuario API y descarga de colección Postman |
| Maxi creó un usuario API | Credenciales empleadas posteriormente con éxito |
| GET `https://api.portalcliente.softwareclock.com/api/ClockApiUser` | 404 en la prueba de Maxi; no usar esa URL para esta colección |
| GET `https://api.portalempleado.softwareclock.com/api/ClockApiUser`, Basic | 200; cuerpo con `code`, `message` y `token` |
| GET `/api/Attendance/getAttendances?start=2026-11-01&end=2026-11-16`, Bearer | 200 y respuesta larga, según Maxi; no se inspeccionó la respuesta real completa |
| Paginación en esa prueba | Maxi observó una única respuesta sin paginación visible; no demuestra ausencia de límite/truncamiento en otros períodos |
| Swagger accesible desde las herramientas del agente | Falló; los hechos anteriores provienen de la colección y las pruebas del usuario, no del Swagger leído |

## URL y autenticación

Base comprobada para esta colección:

```text
https://api.portalempleado.softwareclock.com/
```

Mantener la barra final al sustituir `{{URL_API}}api/...` en Postman. No confundir la versión de la colección `V.1.0.0` con un segmento de ruta: los endpoints comprobados llevan `/api/`, sin `/v1/`.

1. GET `/api/ClockApiUser` con HTTP Basic, usuario y contraseña del usuario API.
2. JSON de respuesta contiene `token`. El script de Postman ejecuta `pm.collectionVariables.set("TOKEN", jsonData.token)`.
3. Las consultas de asistencias usan `Authorization: Bearer <token>`.

Las variables de la colección vienen vacías: `URL_API`, `USERNAME`, `PASSWORD`, `TOKEN`, `COMPANY_NAME`. No se comprobó un uso de `COMPANY_NAME` para las dos llamadas anteriores. La clave/token de la sección «Servicios externos» no fue necesaria en las pruebas; su relación con esta API sigue sin verificar.

La colección incluye para sucursales una cabecera adicional `token`; no generalizar esa particularidad ni dar ese endpoint por probado. Su comportamiento debe revisarse cuando se use.

### Reproducción local sin credenciales en el archivo

Comandos Bash para ejecutar en la computadora autorizada. Usuario y contraseña se leen de forma interactiva; el token queda en un archivo temporal con permisos restringidos y no se imprime. Se requiere `python3`. Ejecutar por separado para poder revisar errores.

```bash
read -r -p 'Usuario API: ' CLOCK_API_USERNAME
# curl pide la contraseña de forma interactiva; no agregarla al comando.
CLOCK_AUTH_FILE=$(mktemp)
chmod 600 "$CLOCK_AUTH_FILE"
curl --fail-with-body --silent --show-error \
  --request GET \
  --url 'https://api.portalempleado.softwareclock.com/api/ClockApiUser' \
  --basic --user "$CLOCK_API_USERNAME" \
  --header 'Accept: application/json' \
  --output "$CLOCK_AUTH_FILE"
```

Después de confirmar que la autenticación terminó correctamente:

```bash
CLOCK_HEADER_FILE=$(mktemp)
chmod 600 "$CLOCK_HEADER_FILE"
python3 - "$CLOCK_AUTH_FILE" "$CLOCK_HEADER_FILE" <<'PY'
import json, sys
with open(sys.argv[1]) as source:
    token = json.load(source)['token']
if not isinstance(token, str) or not token or '\r' in token or '\n' in token:
    raise ValueError('Token inválido')
with open(sys.argv[2], 'w') as target:
    target.write('Authorization: Bearer ' + token + '\n')
PY
# Evitar una respuesta con datos personales en pantalla o en un directorio público.
CLOCK_ATTENDANCES_FILE=$(mktemp)
chmod 600 "$CLOCK_ATTENDANCES_FILE"
curl --fail-with-body --silent --show-error --get \
  --url 'https://api.portalempleado.softwareclock.com/api/Attendance/getAttendances' \
  --header "@$CLOCK_HEADER_FILE" \
  --header 'Accept: application/json' \
  --data-urlencode 'document=11111111' \
  --data-urlencode 'start=2026-11-01' \
  --data-urlencode 'end=2026-11-16' \
  --output "$CLOCK_ATTENDANCES_FILE"
# document=11111111 es un valor ficticio: reemplazar localmente.
# Inspeccionar localmente CLOCK_ATTENDANCES_FILE. No subir su contenido real al repositorio.
rm -f "$CLOCK_AUTH_FILE" "$CLOCK_HEADER_FILE"
unset CLOCK_API_USERNAME
# Eliminar CLOCK_ATTENDANCES_FILE al terminar su revisión local.
```

No ejecutar con `set -x` ni registrar respuestas de autenticación. En producto, usuario, contraseña y token se administrarán en backend; nunca en código de MagicPath, navegador, `VITE_*`, repositorio o logs.

## Consultas relevantes de la colección

| Método y ruta externa | Parámetros o utilidad | Evidencia |
| --- | --- | --- |
| GET `/api/Attendance/getAttendances` | `branchName`, `groupName`, `document`, `start`, `end`; fechas documentadas Y-m-d | Consulta por fechas probada por Maxi; filtros restantes pendientes |
| GET `/api/Employees/employees` | `branchName`, `groupName` | Maxi aporta un registro anonimizado el 23/11; estructura exterior/cobertura y filtros pendientes |
| GET `/api/Employees/employee-by-rut` | `document` | Documentada, no probada |
| GET `/api/Reports/getAttendancesRecords` | `branchName`, `groupName`, `document`, `start`, `end` | Documentada, semántica de salida no examinada |
| GET `/api/Employees/getEmployeeAbsences` | `document`, `filterFrom`, `filterTo` | Documentada, no probada; no confundir falta de marca con ausencia |
| GET `/api/EmployeesWorkShifts/getWorkShifts` | Turnos de Clock | Maxi comprobó GET sin parámetros con Bearer, HTTP 200 y `code: 200`; cobertura e identidad pendientes |
| GET `/api/Branches/branches` y `/api/Groups/groups` | Sucursales y grupos | Documentadas, no probadas |
| POST `/api/Attendance/add` | Escritura de asistencia | Existe en colección; fuera de esta etapa, no se ejecutó |

La colección no contiene respuestas de ejemplo ni esquemas de salida, expiración documentada, renovación, límites o contrato de errores suficiente para cerrar la integración.

## Forma observada mediante ejemplo ficticio

```json
{
  "message": "Assists were obtained correctly.",
  "attendances": [{
    "code": 1234,
    "external_id": null,
    "document": "11111111",
    "full_name": "Juanita González",
    "group": "Docente",
    "device": "Redmi",
    "issued": "2026-11-02 12:52:00",
    "geo_fencing": "-",
    "face_id": "0 %",
    "created": "2026-11-02 12:52:49",
    "created_by": "Empleado"
  }]
}
```

| Campo | Lectura y límite |
| --- | --- |
| `issued` | Candidato a fecha/hora efectiva de la marca; usar para ordenar/agrupar después de confirmar zona horaria |
| `created` | Candidato a momento de registro/subida; no acredita por sí solo un motivo de retraso |
| `document` | Candidato a vínculo con la cédula de KUME; definir normalización, duplicados y manejo de no vinculados |
| `code` | Candidato a identificador estable; comprobar unicidad, alcance por empresa y persistencia tras correcciones |
| `external_id` | Viene nulo en el ejemplo; semántica desconocida |
| Otros metadatos | Nombre, grupo, dispositivo, ubicación/validación y creador; no determinan entrada/salida |

No aparece un tipo explícito de entrada/salida en el ejemplo. Tampoco offset de zona horaria: no interpretar automáticamente como UTC ni usar la zona del servidor. America/Montevideo es la referencia de negocio KUME, pero no confirma la semántica temporal del proveedor.

La [FAQ oficial de SoftwareClock](https://softwareclock.com/faqs/) declara marcas offline que se suben al recuperar conexión con su fecha/hora original. Esto justifica volver a importar y reevaluar; no se probó experimentalmente en esta sesión.

## Pendientes de integración

- Comprobar filtro `document`, límites de fecha, extremos inclusivos, orden, cobertura completa y volúmenes. La respuesta larga no prueba integridad ni ausencia de truncamiento.
- Confirmar duración, expiración, renovación y revocación del token; permisos y alcance por empresa. No fijar una duración de token a partir de un solo ejemplo.
- Probar 401/403, expiración, 429, timeout, errores de proveedor y respuestas inesperadas sin revelar secretos.
- Validar esquema y tipos reales con una muestra anonimizada suficiente; detectar respuesta de error aunque HTTP sea 200.
- Confirmar identidad estable para importaciones idempotentes; documentar modificaciones/eliminaciones y reimportación de marcas tardías.
- Definir relación cédula/documento y horarios históricos con [reglas funcionales](../functional/registro-horas.md).
- Incorporar adaptador backend y caché; definir persistencia, contrato interno y coordinación FE/BE en una etapa posterior. No están implementados por crear la maqueta.

## Continuidad tras aprobación de interfaz

Maxi aprobó la interfaz el 16/11/2026 y pidió consolidar decisiones para comenzar especificaciones y conexión. La [guía de preparación](registro-horas-preparacion.md) vincula validaciones del proveedor con los diseños funcional, técnico, contractual y de pruebas necesarios. Los HTTP 200 registrados siguen siendo pruebas manuales del usuario, no conexión incorporada al producto. No se necesita repetir la investigación de autenticación desde cero.

## Validación pendiente para iniciativa 010

El cierre funcional del 23/11/2026 no modifica las evidencias de este documento. La [matriz V01–V07](../specs/010-time-records/tasks.md) organiza validaciones reales de documento, tiempo, identidad, cobertura, token, errores y cambios tardíos. No hubo nuevas llamadas autenticadas al proveedor durante esta preparación documental.

## Respuesta de empleados — 23/11/2026

Maxi aporta un objeto anonimizado con `id`, `code`, `document`, nombres, `external_id` nulo y `workshiftCode`/`workShiftName`. [Mapeo propuesto, secuencias y consulta de turnos](softwareclock-employee-mapping.md). No se confirmó estabilidad/alcance de identificadores; la respuesta de turnos se registra a continuación; no confundir código de empleado con código de asistencia. El objeto individual no acredita ausencia de paginación.

## Catálogo de turnos recibido — 23/11/2026

Maxi comparte array de getWorkShifts con `code`, `name`, `type`, incluidos códigos vacíos para varios turnos. Tipos Fijo/Libre y referencia V4 coincidente con la muestra de empleado. No hay bloques/días/pausas/vigencias estructurados en esa respuesta. Se confirma forma de esta muestra, no estabilidad de identidad ni ausencia de endpoints adicionales. [Diseño de importación administrativa y secuencias](../functional/softwareclock/sincronizar-horarios.md). No usar nombres como reglas de cálculo ni código vacío como clave única.

## Investigación de detalle estructurado de turnos — 23/11/2026

- La colección histórica documentada en este repositorio registra el GET de catálogo y una operación de asignación de escritura. El adjunto privado no estaba disponible para revisar parámetros ni el inventario completo. La muestra del GET acredita solo un catálogo descriptivo.
- La portada pública apunta a `/swagger/v1/swagger.json`. La lectura directa de ese documento devolvió HTTP 403 desde este entorno y la herramienta web tampoco accedió al JSON. La leyenda «No operations defined in spec!» de la portada indexada no permite concluir que la API carece de operaciones. [Swagger UI del proveedor](https://api.portalempleado.softwareclock.com/) · [Documento Swagger](https://api.portalempleado.softwareclock.com/swagger/v1/swagger.json).
- La búsqueda de `getWorkShifts` y de detalle de horarios y planificación en el sitio oficial no aportó un contrato público adicional. SoftwareClock describe planificación y edición de horarios en el producto. Esa funcionalidad de interfaz no acredita que la API exponga los datos. [FAQ oficial](https://softwareclock.com/faqs/).

### OpenAPI aportado por Maxi

El adjunto «Texto pegado.txt» es un JSON de OpenAPI 3.0.1, título `Clock API`, versión `v1`. En `paths` solo aparece GET `/api/ClockApiUser`. El documento incluye componentes de turnos, pero no los vincula a una operación de catálogo o detalle.

| Componente | Datos documentados |
| --- | --- |
| `GetWorkShiftsDto` | Objeto con `code` entero, `message` de texto anulable y `work_shifts` como array anulable de `WorkShiftGetAllDto`. |
| `WorkShiftGetAllDto` | `code`, `name` y `type` de texto anulable. Sin identificador adicional, días, bloques, pausas ni vigencias. |
| `EmployeeDailyReportDto` | Incluye `shift_start`, `shift_end` y campos de pausas en un DTO diario. El adjunto no documenta una operación que lo devuelva ni una relación con los turnos del catálogo. |

Los dos componentes de catálogo carecen de lista `required`. El `code` entero del envoltorio es distinto del `code` descriptivo de cada turno.

### Ficha Swagger de getWorkShifts aportada por Maxi

La operación se describe como un listado de turnos por nombre de empresa. Swagger indica «No parameters». No especifica cómo se resuelve la empresa. No agregar un parámetro o cabecera de empresa por inferencia ni dar por hecho que el Bearer es el único dato que determina el alcance.

| HTTP | Interpretación documentada |
| --- | --- |
| 200 | Objeto con `code`, `message` y `work_shifts`. Cada turno incluye `code`, `name` y `type`. |
| 400 | Falta el nombre de empresa. |
| 401 | Falta el token o la llamada no está autorizada. |
| 404 | Empresa o servidor de empresa no encontrado. |
| 500 | Error interno del proveedor. |

### Lectura real de catálogo aportada por Maxi

En la prueba del 23/11/2026, Maxi llamó al GET con el Bearer generado para su cuenta, sin enviar nombre de empresa. Recibió HTTP 200 con JSON que contiene `code: 200`, `message: null` y `work_shifts` con diez filas, cuatro con código de turno vacío. Los turnos coincidieron con su backoffice. Se comprobó el alcance para esa conexión. La vinculación de empresa con la credencial es consistente con el resultado, y queda por confirmar su comportamiento con otras cuentas o permisos. Se registra evidencia resumida sin copiar el catálogo real.

El `code: 0` de los ejemplos generados de Swagger aparece tanto en el 200 como en los errores. CU1 toma como criterio de éxito conservador el par observado HTTP 200 y `code: 200` con un catálogo válido. El 401 genérico tampoco acredita una señal de expiración apta para renovar.

**Resultado:** el envoltorio y la llamada sin parámetros quedaron comprobados para esa conexión. Cada turno observado contiene solo `code`, `name` y `type`. Días, bloques, pausas y vigencias siguen sin verificarse en una lectura de detalle. Quedan pendientes cobertura, paginación, estabilidad de códigos y semántica de respuestas distintas. La llamada autenticada fue realizada por Maxi. [Tareas CU1](../specs/012-softwareclock-workshifts/tasks.md).

## Uso de referencias en CU2 — 24/11/2026

[CU2](../functional/softwareclock/sincronizar-empleado.md) propone el horario inicial desde la definición estructurada que KUME asocia con el workshift asignado. La evidencia del proveedor se limita a la asignación y al catálogo descriptivo. La cobertura del listado de empleados, identidad estable y eficacia del filtro de asistencias por documento siguen pendientes de validación.

## Consulta de empleado por cédula — 25/11/2026

Maxi comprobó `GET /api/Employees/employee-by-rut?document=…`. La coincidencia devuelve un objeto con `document` textual y `id` y `code` numéricos en el ejemplo. La ausencia devuelve el JSON `{"message":"Empleado no encontrado.","code":404}`. El estado HTTP de la ausencia no figura en la evidencia aportada. Maxi confirma la unicidad de cédula por empresa. La estabilidad del identificador sigue pendiente de verificación.
