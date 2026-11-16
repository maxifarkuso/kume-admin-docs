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

## Extensión aprobada — recuperación de roles

1. Agregar acción explícita, validación de argumentos y selección estricta del intento.
2. Revalidar inspector, identidad, respaldo e inactividad antes de confirmar resolve.
3. Registrar evidencia y comprobar el resultado exacto sin alterar eventos previos.
4. Conservar el verificador final adicional por hash y admitir historia revertida válida.
5. Probar negativos con dobles y reproducir el ciclo en PostgreSQL/Prisma locales.
6. Publicar revisión y checksums; operar Oracle solo desde etapas confirmadas por Maxi.
