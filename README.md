# KUME Admin — Documentación

Documentación del sistema administrativo de KUME: gastos pagados, comprobantes, personal, asignaciones y documentos privados.

## Lectura inicial

1. [Instrucciones para agentes](AGENTS.md).
2. [Decisiones de implementación y pendientes](implementation-decisions.md).
3. [Alcance del prototipo](alcance-prototipo.md) y [stack aprobado](stack-tecnologico.md).
4. [Guía de desarrollo](development-guide.md).

## Arquitectura y contratos

- [Frontend](frontend-architecture.md): React, TypeScript, Vite y organización por funcionalidades.
- [Backend](backend-architecture.md): Node.js, Fastify y arquitectura limpia con dominio independiente.
- [API](api-design.md) y [OpenAPI canónico](openapi.yaml).
- [Base de datos](database-design.md): PostgreSQL y Prisma.
- [Infraestructura y migración](infraestructura-y-migracion.md).
- [Estado del diseño de pantallas](continuacion-diseno-pantallas.md).

## Estado

Reglas de arquitectura aprobadas. Implementación del producto pendiente. Sesiones sin definir; concurrencia optimista aprobada, pendiente de ampliar contrato y base. Pruebas unitarias frontend/backend en la primera etapa; Playwright posterior. El diseño de pantallas sigue en curso.

Los comandos y estructuras descritos son objetivos de inicialización, no código ejecutable ya disponible. No incluir datos reales ni secretos.

## Repositorios

- [Frontend](https://github.com/maxifarkuso/kume-admin-fe).
- [Backend](https://github.com/maxifarkuso/kume-admin-be).
- [Documentación](https://github.com/maxifarkuso/kume-admin-docs).

Documentación se mantiene directamente en main. Frontend y backend usarán ramas cortas y PR con CI una vez inicializados. Ver la guía de desarrollo para fijar revisiones de documentación y contrato.
