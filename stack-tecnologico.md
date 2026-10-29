# KUME — Stack tecnológico

**Fecha:** 29 de octubre de 2026  
**Estado:** aprobado.

## Tecnologías aprobadas

| Componente | Tecnología | Propósito |
|---|---|---|
| Frontend | React + TypeScript + Vite | Interfaz web, desarrollo y compilación del frontend. |
| Backend | Node.js + TypeScript + Fastify | Servicio de aplicación y API. |
| Base de datos | PostgreSQL | Persistencia de los datos del sistema. |
| Acceso a datos y migraciones | Prisma | Acceso a PostgreSQL y gestión de cambios en su estructura. |
| Archivos | Almacenamiento local persistente | Conservación de comprobantes de gastos y documentos del personal. |
| Ejecución | Docker Compose | Ejecución local de los servicios de la aplicación. |

## Condiciones de ejecución

- Aplicación local en una computadora, accesible desde el navegador.
- Instalación inicial en Windows, con compatibilidad con Linux.
- Configuración sin depender de rutas específicas de un sistema operativo.
- Base de datos y archivos persistentes al reiniciar o actualizar contenedores.
- Sin despliegue en la nube ni autenticación en el prototipo.
- Los respaldos y la restauración incluirán tanto la base de datos como los archivos, según el [alcance del prototipo](alcance-prototipo.md).

## Situación inicial de los repositorios

Según confirmación del responsable del proyecto, los repositorios de frontend y backend están vacíos. No hay código existente que imponga limitaciones al stack aprobado.

- Frontend: https://github.com/maxifarkuso/kume-admin-fe
- Backend: https://github.com/maxifarkuso/kume-admin-be
- Documentación: https://github.com/maxifarkuso/kume-admin-docs

## Definiciones posteriores

Las versiones concretas de las herramientas se fijarán al inicializar los proyectos, verificando su compatibilidad. El diseño de la base de datos, la API, el almacenamiento y los respaldos corresponde a los próximos pasos del alcance.
