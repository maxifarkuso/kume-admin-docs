# KUME — Stack tecnológico

**Fecha inicial:** 29 de octubre de 2026
**Actualización:** 2 de noviembre de 2026
**Estado:** stack conservado; ejecución inicial cloud en Oracle y alternativa local confirmadas.

## Tecnologías aprobadas

| Componente | Tecnología | Propósito |
|---|---|---|
| Frontend | React + TypeScript + Vite | Interfaz web orientada a computadoras. |
| Backend | Node.js + TypeScript + Fastify | Servicio de aplicación y API REST aprobada. |
| Base de datos | PostgreSQL | Persistencia independiente del proveedor cloud. |
| Acceso a datos y migraciones | Prisma | Acceso a PostgreSQL y gestión de estructura. |
| Archivos | Volumen persistente del servidor | Comprobantes y documentos privados, servidos mediante la API autorizada. |
| Ejecución | Docker Compose | Contenedores separados para API y base y volúmenes persistentes. |
| Infraestructura inicial | Oracle Cloud Infrastructure Always Free | Una VM Linux elegible para la modalidad gratuita. |
| Alternativa futura | Equipo local del instituto | Misma arquitectura desplegada en intranet, con migración de datos, archivos, cuentas y configuración. |

Oracle aloja nuestros servicios; no se sustituye PostgreSQL por Oracle Database. Supabase y sus funciones no forman parte del stack elegido. El contrato funcional de API se conserva y la ampliación de autenticación está documentada en OpenAPI; su implementación y verificación siguen pendientes.

## Condiciones de ejecución

- Uso inicial cloud mediante HTTPS, desde distintas computadoras, sin servicios locales para la usuaria.
- Frontend compilado servido por el proxy HTTPS de la misma VM Oracle; API bajo `/api/v1` en el mismo origen. Sustituye Cloudflare Pages por decisión del 2 de noviembre. En intranet se conserva este esquema.
- Una VM inicialmente, PostgreSQL en red interna y archivos en volumen independiente de la imagen de API. No publicar 5432.
- Ubuntu 24.04 LTS oficial y arquitectura compatible con el shape. La VM de prueba es x86_64; verificar imágenes por arquitectura si se cambia a ARM.
- Cuentas individuales para Vicky y Maxi con los mismos permisos, hashes en secrets del servidor y sin tabla de usuarios, registro público ni recuperación por correo. Cambios manuales de contraseña; cierre manual, expiración tras 8 horas de inactividad y pausas temporales por intentos fallidos por cuenta y por IP. Ver [autenticación](autenticacion-prototipo.md). Sesiones en memoria de un único proceso Fastify y cookie HttpOnly; reiniciar exige nuevo login. Diseño completo: scrypt de node:crypto, parámetros y secrets documentados; pausa de 15 minutos tras 5 fallos por cuenta o 20 por IP en ventana de 15 minutos. Implementación pendiente; no se asume Supabase Auth.
- Piloto con datos reales y demo separada con datos ficticios, archivos y credenciales aislados.
- Configuración sin rutas absolutas específicas de Windows o Linux; secretos fuera del código y navegador.
- Objetivo de costo total USD 0, sin pagos automáticos. Comprobar Always Free, cuotas y persistencia; los créditos promocionales no aseguran gratuidad continua.
- No hacer dimensionamiento anual para el MVP. Evaluar intranet si los límites comprometen el uso. La continuidad gratuita no tiene disponibilidad garantizada.
- Respaldos diarios cifrados fuera de Oracle, retención de 30 días, alertas y restauraciones comprobadas, según el [alcance](../functional/alcance-prototipo.md).

## Portabilidad a intranet

Mantener Docker Compose, PostgreSQL, Prisma y el almacenamiento por claves relativas. Preparar exportación y restauración consistente de base, archivos, cuentas y configuración. La implementación local completa se realizará cuando se decida migrar; no se considera probada todavía.

El destino será un equipo del instituto encendido durante el uso, con acceso solo desde su intranet y sin dependencia cloud para el funcionamiento diario. Windows y Linux son alternativas a evaluar al elegir equipo y operación. Definir HTTPS, nombre interno y respaldos en el destino; el login y el cambio manual de contraseñas no requieren correo. Ver [infraestructura y migración](../devops/infraestructura-y-migracion.md).

## Estado de los repositorios y versiones

En la confirmación inicial, frontend y backend estaban vacíos; verificar su estado actual antes de implementar. La API temporal de infraestructura no es implementación de KUME.

- Frontend: https://github.com/maxifarkuso/kume-admin-fe
- Backend: https://github.com/maxifarkuso/kume-admin-be
- Documentación: https://github.com/maxifarkuso/kume-admin-docs

Las versiones del producto se fijarán al inicializar los repositorios, verificando compatibilidad y soporte. Las imágenes Node 22 y PostgreSQL 17 usadas en el smoke test son evidencia de prueba, no fijación definitiva del stack. Contrato de autenticación incorporado a OpenAPI; diseño de credenciales y umbrales completo; pendientes implementación, respaldo y restauración, concurrencia, HTTPS y despliegue final.
