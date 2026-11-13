# KUME — Decisiones para la implementación

Fecha: 2 de noviembre de 2026. Origen: rondas GrillMe con Maxi, Q1–Q12. Estado: reglas consolidadas confirmadas expresamente por Maxi el 2 de noviembre de 2026. No acredita implementación.

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
