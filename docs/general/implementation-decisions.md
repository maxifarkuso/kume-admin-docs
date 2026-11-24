# KUME — Decisiones para la implementación

Fecha: 2 de noviembre de 2026. Origen: rondas GrillMe con Maxi, Q1–Q12. Estado: reglas consolidadas confirmadas expresamente por Maxi el 2 de noviembre de 2026. No acredita implementación.

## Preparación del servidor local — 16 de noviembre de 2026

Maxi solicita documentar el camino de migración desde Oracle y crear una skill
interna para retomarlo. Equipo de referencia: Lenovo Tiny M910q i5-6500T,
8 GB RAM y SSD 256 GB, Ubuntu Server 24.04 LTS AMD64 sin escritorio, hasta cinco
personas con actividad baja y sin UPS inicialmente. No confirma compra ni
instalación; capacidad pendiente de comprobación. No cambia las cuentas aprobadas.

Camino acordado: preparación e instalación automatizable por etapas, copia de
ensayo con restauración comprobada y corte definitivo posterior coordinado,
conservando Oracle para recuperación. Para actualizaciones, partir de GitHub
como constructor y descarga/activación manual en intranet, con diseño concreto
pendiente; no requiere habilitar acceso remoto ni un runner local.

El [plan de servidor local](../devops/plan-servidor-local.md) es la fuente de
etapas, configuración, estimación preliminar y pendientes; la
[skill kume-local](../../.agents/skills/kume-local/SKILL.md) permite retomarlo.
La independencia cloud corresponde al núcleo administrativo: nuevas consultas
a SoftwareClock, si se incorpora, requieren internet. Se conservan sus reglas.

Estado: documentación y skill preparadas; scripts, workflows, respaldo externo,
ensayo y ejecución pendientes. Impacto futuro en FE/BE y operación, sin cambio
de OpenAPI ni esquema por este plan. No autoriza operaciones sobre Oracle,
despliegue, retiro de infraestructura, commit ni push.

## Continuidad y personal — 13 de noviembre de 2026

Maxi confirma que el único desarrollo funcional pendiente para la primera versión es personal: fichas, asignaciones a cursos y talleres y documentos. Esta actualización sustituye los estados históricos que todavía presentan todo el producto como pendiente; no acredita pruebas integradas, despliegue ni preparación operativa.

Tras revisar la documentación con GrillMe, Maxi aprueba usar `version` común a la ficha, sus asignaciones y sus documentos. Aunque inicialmente el sistema lo utilizará una sola persona, se conserva el control optimista para contemplar crecimiento de uso.

- Cada modificación de datos, estado, asignaciones o documentos incrementa la versión de la ficha propietaria.
- Una escritura basada en una versión anterior se rechaza sin sobrescribir cambios; la interfaz conserva el borrador y solicita revisar la información vigente. No renovar la versión ni reintentar automáticamente para eludir el conflicto.
- La inactivación debe detectar asignaciones agregadas después de leer la ficha y exigir revisión antes de retirarlas.
- Se mantienen los campos, reglas de asignación, archivos privados y restricciones de fichas inactivas ya aprobados.

Estado posterior: especificaciones, plan y contrato canónico publicados; backend/frontend implementados en ramas `feat/staff`, con consumidores sincronizados a `ca6503acea54d0c9d3e779d888ede6f3365f2ace`. El contrato ya expresa el versionado de personal. Ver [evidencia, commits y límites](../specs/005-staff/implementation.md). Pendientes integración, migración, comprobación PostgreSQL y despliegue; las pruebas locales no acreditan funcionamiento productivo.

## Actualización de continuidad — 5 de noviembre de 2026

Maxi informa que auth foundation está mergeado y desplegado en frontend y backend; aún no realizó pruebas funcionales. No se acredita verificación funcional en esta reorganización.

La decisión Q6 y los pendientes de sesiones/alojamiento de la ronda original son históricos: fueron resueltos por el [diseño de autenticación del 2 de noviembre](../technical/autenticacion-prototipo.md), que define sesiones en memoria, cookie y frontend/API bajo un mismo origen HTTPS en Oracle. No reabrirlos por leer la tabla original. El resto de los pendientes conserva su evidencia y estado registrados; esta actualización no los da por completados.

## Acuerdos

| Pregunta | Acuerdo |
|---|---|
| Q1 | Frontend por funcionalidades: app, features y shared; límites explícitos. |
| Q2 | Backend modular con arquitectura limpia, dominio y aplicación independientes, persistencia detrás de interfaces y TypeScript strict. |
| Q3 | OpenAPI de docs como contrato canónico; tipos generados y consumidores fijados a revisión identificable. |
| Q4 | Autonomía interna; consulta para dependencias de producción no acordadas, stack, contratos públicos, permisos y operaciones destructivas. |
| Q5 | React Router, TanStack Query, React Hook Form y Zod. Estado local por defecto. |
| Q6 | Se pospone diseño de sesiones; no se adopta la recomendación de cookies ni mecanismo alternativo. |
| Q7 | Control optimista de concurrencia; no sobrescribir silenciosamente cambios ajenos. |
| Q8 | Unitarias frontend/backend; Vitest y React Testing Library. Formato, lint, tipos y build en CI. Playwright posterior. Integración pendiente. |
| Q9 | TypeBox/JSON Schema en límite HTTP de Fastify, con tipos inferidos y verificación frente a OpenAPI. |
| Q10 | Guías completas en docs y AGENTS breves por repositorio, accesibles con un solo checkout mediante revisión fijada. |
| Q11 | Ramas cortas y PR a main en código; docs directo a main. Sin commit/push automático salvo solicitud. |
| Q12 | npm, lockfile por repo, npm ci y versiones soportadas/compatibles fijadas al inicializar. |

## Documentos propietarios

- docs/technical/frontend/frontend-architecture.md: organización, React, estado, formularios, accesibilidad y tests FE.
- docs/technical/backend/backend-architecture.md: capas, puertos, dominio, persistencia, transacciones y pruebas BE.
- docs/technical/development-guide.md: sincronización entre repositorios, comandos objetivo, Git y entrega.
- AGENTS.md de cada repositorio: instrucciones operativas y referencias.

Se conservan docs/functional/alcance-prototipo.md, docs/technical/stack-tecnologico.md, docs/technical/api-design.md, openapi.yaml, docs/technical/backend/database-design.md, docs/devops/infraestructura-y-migracion.md y docs/ui/continuacion-diseno-pantallas.md como fuentes funcionales y operativas. Se conservan sin cambios funcionales en esta incorporación. Las guías nuevas explicitan las ampliaciones técnicas aprobadas que todavía deben propagarse.

## Pendientes explícitos y momento de resolución

| Pendiente | Antes de |
|---|---|
| Mecanismo de sesión, transporte, revocación, expiración, recuperación y protección CSRF cuando corresponda | Implementar autenticación; ampliar API y base. No asumir cookies, JWT ni proveedor. |
| Alojamiento final de frontend, topología de orígenes, HTTPS y política CORS | Diseñar transporte de sesión y desplegar. Cloudflare Pages sigue siendo opción conversada. |
| Campo/token de versión, recursos afectados, protocolo y respuesta de conflicto | Implementar concurrencia; actualizar OpenAPI, base y consumidores juntos. |
| Aislamiento/bloqueo para operaciones entre filas | Implementar asignaciones, inactivaciones y modificación de turnos de manera atómica. |
| Versiones de Node, React, Fastify, Prisma, PostgreSQL y herramientas; generador y verificador de contratos | Inicializar repositorios y CI, verificando soporte y compatibilidad. |
| Representación decimal exacta del núcleo y definición del día del negocio | Implementar dinero y reglas temporales, sin depender de tipos Prisma. |
| Librería visual/estilos | Implementar UI sobre diseños aprobados; no elegida en Q5. |
| Pruebas de integración y futura adopción de Playwright | Siguiente decisión de estrategia de pruebas. No dar por verificada integración con unitarias. |
| Catálogos, login/recuperación, prototipo, docs/ui/screen-design.md y backlog | Aprobar implementación de pantallas correspondientes. Paso 4 sigue en curso. |
| Correo, respaldos, alertas y restauración real | Piloto con datos reales, manteniendo costo cero y requisitos ya acordados. |

## Criterio para retomar

Leer primero este registro y los documentos de la tarea. No reabrir acuerdos sin incompatibilidad o evidencia concreta. Resolver pendientes cuando bloqueen la operación que se va a implementar; no rellenarlos silenciosamente. Actualizar este registro al acordarlos, distinguiendo aprobado, implementado y verificado.

## Cursos y talleres — 7 de noviembre de 2026

Maxi solicita comenzar los CRUDs por cursos y talleres, incluida la carga inicial por base de datos ya definida en el alcance. Aprueba expresamente añadir `version` a ambos recursos, exigirla al editar/desactivar/reactivar y devolver 409 ante versión obsoleta. Alcance limitado a estos dos catálogos; el pendiente de versionado de otros recursos se conserva.

Estado: decisión aprobada; contrato local ampliado y especificaciones preparadas; código en curso, verificación final y despliegue pendientes. No acredita aprobación de los marcos de catálogos ni finalización del paso 4.

Impacto: `openapi.yaml`, [API](../technical/api-design.md), [base](../technical/backend/database-design.md), consumidores backend/frontend y sus DTO. Es una ampliación incompatible para escrituras sin versión; antes de publicar se requiere revisión canónica inmutable, regeneración de consumidores y despliegue coordinado. No hay autorización implícita de commit, push, merge ni migración de producción.

[Especificación funcional](../specs/002-courses-workshops/spec.md), [técnica](../specs/002-courses-workshops/technical-spec.md), [plan](../specs/002-courses-workshops/plan.md) y [tareas/evidencia](../specs/002-courses-workshops/tasks.md). La integración y coordinación real con asignaciones sigue pendiente de su implementación y comprobación.

### Evidencia de implementación local de catálogos

Backend `1c477d2` y frontend `e40b0d4` en ramas `feat/courses-workshops`. Pasaron 49 pruebas de backend y 14 de frontend, comprobaciones de tipos, lint y contrato. El frontend también compiló con Vite. Backend compiló TypeScript con un cliente Prisma local sin motor generado con herramientas oficiales; `npm run build` completo con motor nativo sigue bloqueado por 403 en esta instancia. No confundir esa compilación parcial con validación del artefacto de producción.

Maxi instruyó diferir la ejecución de migraciones hasta antes del despliegue. No se ejecutaron migraciones ni ensayos de concurrencia PostgreSQL. Sin push, PR, merge ni despliegue. Detalle y límites en [implementación](../specs/002-courses-workshops/implementation.md). Los consumidores fijan el contrato aprobado en `1e650636705371f09be51a8c77a67f39e5251ba3`; esta actualización solo registra evidencia posterior.

## Registro de pagos — 8 de noviembre de 2026

Maxi solicita especificación técnica, plan e implementación del módulo de gastos pagados. Tras la etapa inicial de solo especificación, aprueba expresamente:

- Agregar `version` a gastos y rubros, exigirla al editar y cambiar estado, y al reemplazar comprobantes; responder 409 con `VERSION_CONFLICT` ante versión obsoleta. La autorización anterior de no cambiar contratos queda sustituida para estas operaciones.
- Usar America/Montevideo para el día de negocio, la validación de fecha no futura y el mes inicial.
- Incorporar el plugin oficial `@fastify/multipart` al backend para cargas de comprobantes; versión instalada y fijada 10.1.8, compatible con Fastify 5.

El núcleo usa centésimos bigint y texto decimal en los límites, sin aritmética binaria para importes. El versionado comienza en 1 y se incrementa atómicamente por escritura aceptada, incluso acciones de estado ya coincidente. Reemplazar comprobante incrementa la versión del gasto y conserva la respuesta de metadatos existente; consultar de nuevo el gasto antes de otra escritura.

Estado: contrato local ampliado e implementación local en curso. No acredita migraciones aplicadas, pruebas PostgreSQL, despliegue ni finalización del paso 4. La revisión inmutable y sincronización de consumidores quedan pendientes de un commit canónico autorizado; no inventar un SHA para el contrato modificado.

Impacto: OpenAPI, API, base, consumidores frontend/backend y volumen privado de comprobantes. Cambio incompatible con clientes que escriben sin versión; requiere despliegue coordinado. No se autorizaron commit, push, merge ni despliegue. Evidencia y límites en [implementación](../specs/003-payment-records/implementation.md).

## Interfaz general — 13 de noviembre de 2026

Maxi aprobó dirección B institucional y la maqueta de Gastos con sus ajustes finales, y pidió publicar todos los acuerdos como regla general de interfaz del sistema. La fuente propietaria es [Reglas generales de interfaz](../ui/sistema-visual.md); incluye componentes, estados, accesibilidad, ingreso desde centésimos y alcance transversal. Esta decisión resuelve la dirección visual pendiente de Q5 sin elegir librerías visuales o nuevas dependencias.

Estado: diseño aprobado y publicación documental autorizada. Implementación del frontend, plan de extensión y verificaciones de producto pendientes. No cierra el paso 4 ni autoriza despliegue. Los controles de revisión de la maqueta no forman parte de la UI final.

## Comprobante opcional — 13 de noviembre de 2026

Maxi aprueba registrar gastos sin comprobante. POST exige solo data; receipt es opcional. Las respuestas de gastos mantienen receipt, con null si no hay archivo. PUT de comprobante permite adjuntar el primero o reemplazar el existente, conserva archivo obligatorio en esa operación y versión del gasto. Sin cambios de esquema ni migraciones: la relación ya era opcional. Despliegue coordinado frontend/backend; clientes anteriores que asumen receipt no nulo requieren actualización.


## Gastos: vencimiento opcional — 16 de noviembre de 2026

Agregar dueDate opcional y nullable como fecha civil, sin limitarla al pasado ni relacionarla con fecha de pago. PATCH omitido conserva valor y null borra. Filtros inclusivos dueDateFrom/dueDateTo combinados con los actuales, excluyen registros sin vencimiento cuando están activos. Listado, total y CSV usan los mismos filtros. Migración aditiva nullable, sin ejecutar en producción.

Solicitud aprobada; implementación y verificación en branch separado. Ver [especificación](../specs/007-expense-due-date/spec.md). No acredita despliegue.

## Gastos: destinatario y comentario opcionales — 16 de noviembre de 2026

payee y description se pueden omitir o enviar vacíos. Se normalizan a «Sin destinatario» y «Sin comentario» antes de persistir; las columnas NOT NULL y CHECK existentes se conservan. PATCH omitido conserva valor; vacío lo reemplaza por el predeterminado.

Solicitud aprobada; implementación y verificación en branch separado. Ver [especificación](../specs/006-expense-optional-fields/spec.md). No acredita despliegue.


## Personal: nuevos roles — 16 de noviembre de 2026

Eliminar assistant / Auxiliar. Incorporar cleaningAssistant / Auxiliar de limpieza, classroomAssistant / Auxiliar de sala, classroomLead / Encargada de sala y director / Directora. Conservar teacher y workshopInstructor. Maxi confirma que aún no existen fichas; no se requiere compatibilidad histórica ni reasignación de datos. Migración cambia CHECK, sin borrar ni modificar fichas y falla si aparecen roles retirados.

Solicitud aprobada; implementación y verificación en branch separado. Ver [especificación](../specs/009-staff-roles/spec.md). No acredita despliegue.

## Registro de horas y SoftwareClock — 16 de noviembre de 2026

Maxi aprueba las [reglas funcionales](../functional/registro-horas.md) y autoriza el prototipo en MagicPath y su documentación. Esto amplía la exclusión histórica de CLOCK para investigación y diseño; no habilita la pestaña en Personal V1 ni autoriza implementación o despliegue. Se conserva el sistema visual aprobado.

Autenticación Basic y posterior consulta Bearer de asistencias en Portal del Empleado respondieron HTTP 200 en las pruebas ejecutadas por Maxi. [Evidencia, endpoints y límites](../technical/softwareclock-api.md). El agente no realizó esas pruebas con credenciales. No se guardan secretos.

Reglas principales: referencia de cursos KUME, bloques/pausas explícitos, sugerencias sin completar faltantes automáticamente, margen configurable inicial de 60 minutos, correcciones locales solo por administración, motivo siempre opcional e historial. Los contratos internos, persistencia y vigencia histórica se diseñarán antes de implementar. [Maqueta y estado](../ui/maquetas/registro-horas/README.md). Maxi aprobó visualmente la interfaz después de la entrega y solicitó consolidar la documentación para comenzar especificaciones y conexión. [Preparación de la siguiente etapa](../technical/registro-horas-preparacion.md). Contratos internos y persistencia pendientes; sin cambios de OpenAPI ni migraciones. Maxi autorizó posteriormente commit y push de esta documentación.

## Registro de horas: discovery Q1–Q12 — 23 de noviembre de 2026

Maxi aprobó horarios laborales por maestra con bloques semanales, vigencias y excepciones por fecha; los cursos pasan a ser contexto. Un horario retroactivo requiere vista de días afectados y confirmación de recálculo. Se permite asignación administrativa de marcas fuera del margen. Una marca real inequívoca de Clock reemplaza la hora manual usada en KUME, conservando historial; con varias candidatas se mantiene revisión.

Comparación exclusivamente informativa: tiempo adicional registrado, tiempo faltante registrado y saldo neto; sin decisiones de pago. Jornadas incompletas conservan tramos confirmados, saldo pendiente y resumen mensual parcial. Motivo siempre opcional. [Fuente funcional y pendientes](../functional/registro-horas.md). Discovery todavía abierto; sin cambio de OpenAPI, base, código de producto o canvas por esta actualización documental.

## Registro de horas: discovery Q13–Q18 — 23 de noviembre de 2026

Maxi aprueba jornada excepcional antes de calcular saldo de días sin horario; truncar cada marca al minuto para presentación y cálculo conservando original íntegro; acumular adicional y faltante con saldo neto mensual; comparar intervalos respecto del horario previsto incluso si sus duraciones coinciden. No inferir trabajo durante la pausa por tener solo marcas de los extremos: requiere confirmación administrativa. Pendiente precisar efecto de esa confirmación sobre la referencia prevista, para no eliminar el tiempo adicional por cambiar el horario. [Fuente funcional](../functional/registro-horas.md). Sin implementación ni cambio del canvas por registrar las decisiones.

## Registro de horas: discovery Q19–Q26 — 23 de noviembre de 2026

Confirmación de pausa trabajada conserva jornada prevista y diferencia adicional. Editor Horario laboral en la pestaña de horas; herencia inicial editable de cursos, sin vínculo posterior. Marcas Clock inmutables; solo asignar originales y completar faltantes. Confirmación de no trabajo: Licencia / Enfermedad / Otro y causa opcional; las dos primeras no generan faltante y Otro sí. Meses abiertos y ambigüedades solo resueltas automáticamente con combinación única. [Reglas propietarias](../functional/registro-horas.md). Sin implementación, cambios contractuales o cierre del discovery por este registro.

## Registro de horas: discovery Q27–Q31 — 23 de noviembre de 2026

Maxi aprueba margen general con vigencias y confirmación de reproceso histórico, revisión de jornadas anteriores de fichas inactivas sin reactivación, egreso inclusivo y conservación de marcas posteriores como incidencia excluida de cálculo automático. [Reglas funcionales](../functional/registro-horas.md) y [balance para especificar](../technical/registro-horas-preparacion.md). Pendiente presentar consolidación para cierre funcional; validaciones del proveedor siguen abiertas, sin implementación acreditada.

## Registro de horas: cierre funcional y especificaciones — 23 de noviembre de 2026

Maxi confirma cierre de discovery Q1–Q31 y avance con especificaciones/plan, manteniendo validaciones de Clock como pendientes explícitos. [Iniciativa 010](../specs/010-time-records/spec.md), [propuesta técnica](../specs/010-time-records/technical-spec.md), [plan](../specs/010-time-records/plan.md) y [tareas](../specs/010-time-records/tasks.md) preparados. Diseño HTTP, recursos de versión y modelo persistente son propuestas revisables; no se modificó OpenAPI, ejecutó migración ni implementó el producto. No hay validación nueva de Clock ni cierre del paso 4 general por esta confirmación.

## SoftwareClock: separación de casos de uso — 23 de noviembre de 2026

Maxi pide documentar por separado CU1 sincronizar workshifts/horarios, CU2 sincronizar empleado y CU3 registro de horas, con prompts para sesiones independientes. [Índice y fronteras](../functional/softwareclock/README.md). CU2 es dependencia del vínculo para importación real en CU3; CU1 es catálogo descriptivo y no requisito obligatorio para calcular con horario propio. No cambia el cierre Q1–Q31 ni aprueba automáticamente plantillas externas, identidad del proveedor, contratos nuevos o implementación. Tres documentos de casos y tres prompts preparados; conservar fuentes técnicas y propuesta 010 como contexto, sin copiarlas a código por inferencia.

## Publicación documental de SoftwareClock — 23 de noviembre de 2026

Maxi autoriza subir toda la documentación preparada: discovery Q1–Q31, iniciativa 010, hallazgos de empleados/turnos, tres casos de uso y tres prompts. Publicación documental en main; no autoriza por sí misma implementación, cambio de contrato canónico, migraciones ni despliegue. Se verificaron enlaces relativos, Markdown y ausencia de tokens JWT en los archivos modificados.

## Fuente del horario inicial en CU2 — 24 de noviembre de 2026

Maxi aprueba que CU2 use el workshift asignado en Clock y su definición estructurada en KUME para proponer el horario propio inicial. Esta decisión sustituye la precarga desde cursos para CU2. Si falta una correspondencia inequívoca o la definición está incompleta, se puede vincular la identidad con horario pendiente. Administración confirma una copia editable con vigencia y origen histórico. Las sincronizaciones posteriores solo actualizan metadata externa admitida. [Regla funcional](../functional/softwareclock/sincronizar-empleado.md) · [Propuesta de contrato y persistencia](../specs/013-softwareclock-employee/technical-spec.md).

### CU2 · Alcance y habilitación acordados con Maxi

- Primer hito: vinculación de identidad, persistencia de referencia externa y estado de horario pendiente. Segundo hito: propuesta editable cuando CU1 entregue una definición estructurada y KUME disponga del horario propio.
- La confirmación con datos reales requiere evidencia de cobertura suficiente del listado y de estabilidad y unicidad del identificador dentro de la empresa. El desarrollo y las pruebas pueden avanzar con datos ficticios.
- Un cambio de documento o una discrepancia de identidad suspende el uso del vínculo para nuevas importaciones y conserva el historial. El primer hito admite revalidar la misma identidad. Reemplazarla requiere una futura acción administrativa específica y auditada.
- Hasta validar la conexión, ocultar la acción en el entorno real y bloquear preparación y confirmación en backend. Probar el flujo con datos ficticios.
- Revalidar desde «Sincronizar empleado con Clock». Si una cédula corregida coincide de forma única con el mismo identificador en la misma empresa, una confirmación explícita crea una revisión. Las importaciones anteriores conservan su revisión original.
- Maxi aprueba incorporar a OpenAPI la consulta del vínculo, la preparación y la confirmación del primer hito. La consulta respeta el acceso a la ficha. Preparar y confirmar requieren administración y ficha activa. La confirmación verifica versiones y guarda vínculo y auditoría en una transacción. El contrato de horario editable corresponde al segundo hito.
- El token de CU0 determina la empresa. KUME usa una conexión lógica estable y no ofrece seleccionar ni cambiar de empresa en CU2.
- La vista previa vence a los 15 minutos. Cambios de ficha, vínculo o conexión requieren una vista nueva. La repetición de una confirmación aplicada recupera su resultado sin duplicar la auditoría.
