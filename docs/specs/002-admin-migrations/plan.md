# Plan y tareas — 002

Orden: especificación funcional → diseño técnico → plan → implementación → pruebas.
Sin commits ni publicación automáticos.

- [x] Revisar instrucciones, skill local, código, pruebas y operación histórica.
- [x] Definir interfaz, etapas, confirmación, locks y recuperación por inspección.
- [x] Implementar motor separado e integración CLI/menú preservando consultas.
- [x] Probar comportamiento y fallos con colaboradores controlados.
- [x] Actualizar instrucciones, instalación, operación y ayuda.
- [x] Ejecutar suite, sintaxis, lint/formato disponibles, enlaces y revisión de diff.
- [x] Registrar evidencia y límites, sin ejecutar contra Oracle.

No cambia HTTP/OpenAPI ni esquema del producto. No altera fuentes de reglas de
catálogos. Dependencias estándar Bash/Python/Docker/Git; no modifica permisos.

Resultados y pendientes reales: [implementación](implementation.md).

## Seguimiento — 9 de noviembre

- [x] Corregir UID/GID y HOME de herramientas sin ampliar permisos del snapshot.
- [x] Comprobar lectura antes de instalar o ejecutar Prisma.
- [x] Incorporar recuperación explícita para deploy incierto con inspector aprobado.
- [x] Probar límites de permisos, confirmación, evidencia y autorización de un intento.
- [ ] Validar la distribución corregida en la VM durante la sesión guiada.
