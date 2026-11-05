# KUME Admin — Documentación

Documentación del sistema administrativo de KUME: gastos pagados, comprobantes, personal, asignaciones y documentos privados.

## Lectura inicial

1. [Instrucciones para agentes](AGENTS.md).
2. [Decisiones de implementación y pendientes](docs/general/implementation-decisions.md).
3. [Alcance del prototipo](docs/functional/alcance-prototipo.md) y [stack aprobado](docs/technical/stack-tecnologico.md).
4. [Guía de desarrollo](docs/technical/development-guide.md).

## Organización

| Carpeta | Contenido |
|---|---|
| `docs/functional` | Alcance, actores y reglas de negocio. |
| `docs/general` | Acuerdos y decisiones transversales. |
| `docs/technical` | Stack, desarrollo, API y autenticación compartidos por frontend y backend. |
| `docs/technical/backend` | Arquitectura backend y persistencia. |
| `docs/technical/frontend` | Arquitectura frontend. |
| `docs/ui` | Navegación, pantallas, aprobaciones y continuidad del diseño. |
| `docs/devops` | Infraestructura, despliegue, administración y registros de operación. |
| `docs/specs` | Historial de especificaciones por iniciativa; conserva sus rutas actuales. |

En la raíz quedan este índice, `AGENTS.md`, el contrato canónico `openapi.yaml` y la configuración del repositorio. Los scripts, tests, workflows y skills conservan sus carpetas operativas.

## Arquitectura y contratos

- [Frontend](docs/technical/frontend/frontend-architecture.md): React, TypeScript, Vite y organización por funcionalidades.
- [Backend](docs/technical/backend/backend-architecture.md): Node.js, Fastify y arquitectura limpia con dominio independiente.
- [API](docs/technical/api-design.md) y [OpenAPI canónico](openapi.yaml).
- [Autenticación](docs/technical/autenticacion-prototipo.md): decisiones de sesiones, credenciales y criterios de verificación.
- [Base de datos](docs/technical/backend/database-design.md): PostgreSQL y Prisma.
- [Infraestructura y migración](docs/devops/infraestructura-y-migracion.md).
- [Operación instalada y resultados comprobados](docs/devops/operacion-oracle.md).
- [Spec de revisión automática del backend](docs/specs/001-backend-revision/spec.md): mejora separada, pendiente de integración y verificación en Oracle.
- [Script de consulta de Oracle](docs/devops/administracion-oracle.md): recursos, Docker, rutas y estados; instalación comprobada y pasos para otra máquina.
- [SKILL kume-admin](.agents/skills/kume-admin/SKILL.md): guía versionada para instalar, adaptar y revalidar la utilidad.
- [Memoria de la app de prueba Oracle](docs/devops/memoria-app-test-oracle.md): SSH, Compose, reconstrucción y retirada antes de publicar el MVP.
- [Mapa de navegación y pantallas](docs/ui/screen-design.md).
- [Estado del diseño de pantallas](docs/ui/continuacion-diseno-pantallas.md).

## Estado

Actualización del 5 de noviembre de 2026: Maxi informa que auth foundation está mergeado y desplegado tanto en frontend como en backend. **Pruebas funcionales pendientes**; este reporte no acredita verificación funcional ni habilitación del piloto con datos reales.

El [diseño de autenticación](docs/technical/autenticacion-prototipo.md) define sesiones y seguridad. El diseño de pantallas sigue en curso. Conservar las fechas y evidencias de las memorias y especificaciones: sus estados describen el momento registrado y no sustituyen esta actualización. No dar por implementadas las siguientes funcionalidades.

## Consumo desde frontend y backend

Las rutas de las guías cambiaron con esta reorganización. Los consumidores existentes fijados a commits anteriores conservan sus snapshots; al adoptar una nueva revisión deben actualizar las rutas del manifiesto y la sincronización según la [guía de desarrollo](docs/technical/development-guide.md). `openapi.yaml` conserva su ruta y contenido. No se actualizaron los repositorios de código en esta tarea.

## Repositorios

- [Frontend](https://github.com/maxifarkuso/kume-admin-fe).
- [Backend](https://github.com/maxifarkuso/kume-admin-be).
- [Documentación](https://github.com/maxifarkuso/kume-admin-docs).

Documentación se mantiene directamente en main. Frontend y backend usarán ramas cortas y PR con CI una vez inicializados. Ver la guía de desarrollo para fijar revisiones de documentación y contrato.
