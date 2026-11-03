# KUME — Decisiones para la implementación

Fecha: 2 de noviembre de 2026. Origen: rondas GrillMe con Maxi, Q1–Q12. Estado: reglas consolidadas confirmadas expresamente por Maxi el 2 de noviembre de 2026. No acredita implementación.

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

- frontend-architecture.md: organización, React, estado, formularios, accesibilidad y tests FE.
- backend-architecture.md: capas, puertos, dominio, persistencia, transacciones y pruebas BE.
- development-guide.md: sincronización entre repositorios, comandos objetivo, Git y entrega.
- AGENTS.md de cada repositorio: instrucciones operativas y referencias.

Se conservan alcance-prototipo.md, stack-tecnologico.md, api-design.md, openapi.yaml, database-design.md, infraestructura-y-migracion.md y continuacion-diseno-pantallas.md como fuentes funcionales y operativas. Se conservan sin cambios funcionales en esta incorporación. Las guías nuevas explicitan las ampliaciones técnicas aprobadas que todavía deben propagarse.

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
| Catálogos, login/recuperación, prototipo, screen-design.md y backlog | Aprobar implementación de pantallas correspondientes. Paso 4 sigue en curso. |
| Correo, respaldos, alertas y restauración real | Piloto con datos reales, manteniendo costo cero y requisitos ya acordados. |

## Criterio para retomar

Leer primero este registro y los documentos de la tarea. No reabrir acuerdos sin incompatibilidad o evidencia concreta. Resolver pendientes cuando bloqueen la operación que se va a implementar; no rellenarlos silenciosamente. Actualizar este registro al acordarlos, distinguiendo aprobado, implementado y verificado.
