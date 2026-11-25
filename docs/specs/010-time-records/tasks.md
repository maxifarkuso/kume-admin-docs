# Registro de horas — Tareas y evidencia

Fecha: 23 de noviembre de 2026. Funcional cerrado; diseño técnico propuesto; producto sin implementación acreditada por esta iniciativa.

## Preparación

- [x] Q1–Q31 documentados y cierre funcional confirmado expresamente por Maxi.
- [x] Interfaz inicial aprobada y fuentes/capturas conservadas; no se modificó MagicPath en esta etapa.
- [x] Especificación funcional con AC01–AC24 y ejemplos preparada.
- [x] Propuesta técnica y plan preparados, con contratos/esquema aún no canónicos.
- [ ] Revisar formalización del algoritmo, recurso de versión, protocolo de vista previa y propuesta HTTP/base.
- [x] Autorización expresa del contrato local el 25/11 y ampliación aditiva de OpenAPI.
- [ ] Publicar revisión inmutable y fijarla en ambos consumidores; generación local de prueba no sustituye el paso de publicación.

## Validación externa de Clock

Pruebas en cuenta autorizada, lectura solamente. No incorporar credenciales, respuestas reales con datos personales o tokens a docs/tests. Los dos HTTP 200 existentes son evidencia de Maxi del 16/11, no resultado de una nueva ejecución del agente.

| ID | Comprobación | Evidencia de salida | Estado |
| --- | --- | --- | --- |
| V01 | Filtro document y pertenencia a empresa | Mismo período de dos documentos, verificar aislamiento y relación cédula/ficha sin registrar PII | Pendiente |
| V02 | Zona/precisión de issued y created | Documento del proveedor o contraste controlado con marca conocida; límites de día/mes | Pendiente |
| V03 | Identidad code y cambios | Reconsultar mismo registro, comprobar estabilidad/alcance y diferencia frente a external_id; no escribir por API para probar | Pendiente |
| V04 | Cobertura/rango/paginación | Extremos inclusivos/exclusivos, mes con volumen conocido, orden, límites y posible truncamiento | Pendiente |
| V05 | Token | Expiración/renovación/revocación y alcance de usuario API; errores sanitizados | Pendiente |
| V06 | Envelope y fallos | Tipos/null, vacío válido, error con HTTP 200, 401/403/429/timeout; documentar lo real y simular fallos no reproducibles sin perturbar servicio | Pendiente |
| V07 | Llegada tardía/modificación | Contrato de sincronización offline/cambios y ausencia de borrado por omisión; muestra controlada o documentación oficial | Pendiente |

Bloqueos: V01/V02/V03/V04 determinan vínculo, tiempo, unicidad e integridad de importación. V05/V06 determinan operación segura. V07 impide afirmar reconciliación completa de cambios del proveedor. No convertir falta de evidencia en «API sin paginación» o «code único».

## Vinculación previa a la importación real

- [x] Registro de empleado anonimizado inspeccionado: identificadores, documento y referencia de turno documentados; sin datos reales ni token guardados.
- [x] Diseño propuesto de vínculo persistente y diagramas de secuencia preparados en [mapeo](../../technical/softwareclock-employee-mapping.md).
- [ ] Validar estructura exterior/cobertura de Employees y estabilidad/alcance de id y code.
- [x] Primer hito CU2 para vínculo y revalidación aprobado y presente en los checkouts FE/BE; la inicialización de horario es un hito distinto.
- [ ] Probar filtro document de asistencias con la identidad vinculada; no asumir filtro por id.
- [x] Inspeccionar muestra de respuesta getWorkShifts: array code/name/type, sin bloques estructurados y con códigos vacíos repetidos.
- [ ] Confirmar identidad/alcance de turnos y posible endpoint de detalle; relación V4 observada no prueba unicidad.
- [ ] Diseñar botón Sincronizar empleado con Clock y vista administrativa de importación, códigos ambiguos, reimportación y configuración local sin alterar horarios definidos.
- [ ] Coordinar con CU2 la copia inicial desde el workshift estructurado y la lectura del vínculo validado.

## Backend

- [ ] Inspeccionar repositorio BE e instrucciones vigentes, fijar revisión documental y conservar stack/dependencias.
- [ ] Implementar núcleo temporal y matching conforme revisión; pruebas de intervalos, truncamiento y parciales.
- [ ] Horarios precargados solo inicialmente, vigencias, excepciones, margen y vista previa con confirmación/versiones.
- [ ] Migración aditiva y auditoría; vínculo estable de eventos y revisiones inmutables; importaciones idempotentes.
- [ ] Coordinación con egreso/cédula y revisiones históricas sin reactivar ficha.
- [ ] Adaptador Clock por puertos, token backend, validación de respuesta, límites y fallos seguros.
- [ ] Importación fuera de transacción de red y aplicación atómica sin sobrescribir edición concurrente.
- [ ] Comandos de asignación/completar faltantes/confirmaciones; impedir editar originales.
- [ ] Rutas canónicas autenticadas, protección de comandos, problem+json y contract check.

## Frontend

- [ ] Inspeccionar repositorio FE e instrucciones, sincronizar contrato y tipos generados.
- [ ] Activar pestaña por maestra y adaptar tabla/resumen a intervalos, diferencias y saldo parcial.
- [ ] Horario laboral, precarga editable, vigencias, excepciones y margen general con vista previa retroactiva.
- [ ] Panel administrativo: asignar sin editar originales, completar faltantes, no trabajo con tipo/causa opcional y pausa trabajada sin cambiar referencia.
- [ ] Historial, egreso inclusivo y marca posterior como incidencia excluida.
- [ ] TanStack Query por ficha/mes, actualización al abrir/cambiar mes, último éxito y error con datos conservados.
- [ ] Borradores/versiones, estados accesibles y foco; pruebas Testing Library, formato/lint/tipos/build.

## Integración y entrega

- [ ] Pruebas PostgreSQL de migración/checks y carreras importación/edición/egreso/reproceso.
- [ ] Integración HTTP contra simulador y recorrido real de lectura con Clock, evidencias separadas.
- [ ] Revisión del diseño ampliado frente a interfaz aprobada; cálculo verificado con tabla de ejemplos.
- [ ] Respaldos y recuperación de nuevas tablas; ensayo de reversión sin borrar historial.
- [ ] Publicación de documentos/ramas conforme autorización; registro de commits/PR y checks reales.
- [ ] Migración productiva y despliegue solo en etapa autorizada; comprobar funcionamiento antes de marcar entregada la feature.

## Verificaciones de esta entrega documental

- `git diff --check`: correcto.
- Comprobación local de 14 documentos Markdown modificados/nuevos: bloques de código cerrados, sin marcadores de conflicto ni tokens JWT; 191 enlaces relativos existentes.
- Criterios AC01–AC24 presentes sin omisiones; ejemplos numéricos trazados a las decisiones funcionales.
- `openapi.yaml` sin cambios: la tabla de rutas es una propuesta revisable, no un contrato implementado.
- Revisión documental de coherencia: segundos solo en ejemplos de entrada original, interfaz y cálculos por minutos; la precarga original desde cursos se sustituye para CU2 según decisión del 24/11; ausencia no deducida; originales no editables; pausas confirmadas mantienen referencia prevista.

No se ejecutaron tests de FE/BE, simulaciones de PostgreSQL ni llamadas autenticadas a Clock por escribir estos archivos. Las verificaciones anteriores son documentales, no evidencia de funcionamiento del producto. No hubo commit/push, migraciones ni despliegue en esta preparación.

## Continuación por casos de uso

Ver [índice y prompts de sesiones](../../functional/softwareclock/README.md). Las tareas previas de vinculación corresponden a CU2 y las de catálogo a CU1; se conservan aquí como referencias de dependencia. CU3 no absorbe sus implementaciones ni exige CU1 para operar con horario propio. El objetivo de esta separación es evitar tres clientes/auth distintos y no dar por resueltas validaciones que pertenecen al proveedor.

## Publicación documental solicitada — 23/11/2026

Maxi pidió subir toda la documentación de esta conversación, incluidos tres casos de uso y prompts. Se prepara publicación en main; las menciones anteriores a ausencia de commit/push describen la etapa de preparación. No cambia el estado pendiente de contratos, validaciones reales del proveedor o implementación.

## Continuación del 25/11/2026

| Estado | Alcance |
| --- | --- |
| Aprobado | Q1–Q31, AC25–AC28 y contrato local de las rutas de CU3. El ID de empleado se trata como estable para CU2. |
| Implementado localmente | Navegación de la ficha usando el contrato de CU2 y actualización de caché al confirmar. Cálculo de intervalos por minuto, resumen diario/mensual y resolución de la referencia vigente por fecha como dominio puro, prototipo de matching de cardinalidad máxima y transporte CU0 preparado con decodificador inyectable. El matching y el transporte se ejecutan solo en pruebas. |
| Pendiente | Ruta, consulta mensual e historial persistido, actualización, integración del matching, edición y persistencia de horarios/vigencias y excepciones, auditoría, previsualización, pruebas de concurrencia y migración. La vista actual informa que la consulta aún no está disponible. |

La revisión de V01–V07 mantiene todas las validaciones externas pendientes.
CU0 admite la ruta de asistencia y aporta autenticación compartida,
límite de respuesta, pausa y reintento acotado cuando su contrato reconoce
el rechazo del token. Esa capacidad no establece todavía la señal real de
expiración para asistencias. Los dos resultados por fechas del 16/11 siguen
siendo la evidencia disponible. No se hizo una nueva llamada autenticada
ni se usaron secretos o personas reales.

Verificación local del 25/11: 75 pruebas FE y 159 BE; tipos, lint y
build en ambos. Las pruebas FE verifican la habilitación desde la
confirmación y el acceso a la pestaña durante revalidación. No cubren
lectura de un historial persistido. Los `contract:check` de los
consumidores siguen verificando su referencia fijada anterior. El OpenAPI
local de CU3 se validó por separado con Swagger Parser y generó tipos de
prueba con openapi-typescript; sus diez rutas son aditivas y las 36
existentes conservan su definición. También se revisaron los enlaces
relativos y cercas de los documentos editados.
