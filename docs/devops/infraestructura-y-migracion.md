# KUME — Infraestructura cloud y migración local

**Fecha:** 1 de noviembre de 2026
**Actualización:** 2 de noviembre de 2026 — autenticación con secrets, sin recuperación por correo.
**Estado:** arquitectura confirmada; infraestructura básica probada por Maxi; despliegue del producto y migración local pendientes.

## Arquitectura

La modalidad inicial utiliza una VM Linux de Oracle Cloud Infrastructure Always Free. Docker Compose ejecuta API Node.js/Fastify y PostgreSQL en contenedores separados, con volúmenes persistentes para base y archivos. Prisma gestiona acceso y migraciones. Se conservan las operaciones y reglas del diseño aprobado; se amplía autenticación.

Oracle es infraestructura para nuestras imágenes, no una sustitución de la API ni de PostgreSQL. No se usan Oracle Database, Supabase ni Edge Functions como backend del producto.

El proxy HTTPS de la VM Oracle sirve el frontend React/Vite compilado y reenvía `/api/v1` a Fastify, bajo un mismo origen; decisión confirmada el 2 de noviembre en reemplazo de Cloudflare Pages. No publicar directamente el puerto Fastify ni `/health` en Internet. Una instancia y un proceso backend por entorno, con sesiones en memoria: cada reinicio requiere nuevo login. En intranet se conserva el esquema. Ver [diseño de autenticación](../technical/autenticacion-prototipo.md).

## Condiciones operativas

- Objetivo de costo total USD 0, sin presupuesto pago preaprobado ni activación automática de Pay As You Go.
- Comprobar condiciones Always Free y cuotas reales; distinguir recursos gratuitos de los créditos temporales de prueba.
- Una VM inicialmente; no separar servicios en dos VM sin evidencia de necesidad.
- Verificar recursos existentes y volúmenes de intentos anteriores antes de crear infraestructura; no borrarlos sin autorización.
- Oracle puede no tener capacidad para el shape solicitado y puede recuperar instancias consideradas inactivas. Free Tier no incluye SLA.
- Se aceptan pausas/demoras durante demo y piloto con mensajes claros; revisar continuidad antes del uso administrativo diario.
- No calcular consumo anual para el MVP. Comprobar el espacio necesario para desplegar y cumplir respaldos; evaluar migración si los límites comprometen el uso.
- Datos y archivos privados, HTTPS, autorización del backend, secretos protegidos y PostgreSQL sin exposición pública.
- Cuenta y recuperación bajo control de KUME, con Maxi como administrador técnico. Verificar que el control institucional esté efectivamente resuelto; no registrar datos de tarjeta, claves o correos personales en el repositorio.

## Operación posterior registrada

El [registro de instalación y funcionamiento](operacion-oracle.md) documenta la
landing y backend instalados, acceso personal por túnel comprobado y pendientes.
No reemplaza las condiciones para piloto real de este documento.
Consultas locales: [script de administración](administracion-oracle.md).
Gestión explícita de migraciones de esquema: [motor kume-admin](migraciones-admin.md),
implementación local pendiente de validación en Oracle. No sustituye el traslado
completo ni las pruebas de restauración de esta guía.

## Evidencia de validación básica

Resultados aportados por Maxi desde la VM el 1 de noviembre de 2026:

| Comprobación | Resultado |
|---|---|
| Host | kume-backend |
| Región indicada | Brasil Southeast; verificar identificador y región del despliegue final |
| Shape seleccionado | E2.1.Micro indicado como Always Free; confirmar elegibilidad de recursos finales |
| Sistema | Canonical Ubuntu 24.04 Minimal; terminal reportó 24.04.5 LTS |
| Arquitectura | x86_64 |
| Acceso | SSH con usuario ubuntu y sudo sin contraseña comprobados |
| Memoria y disco antes de Docker | 952 MiB RAM, sin swap, raíz de 45 GB con unos 43 GB libres |
| Docker y Compose | hello-world correcto; Compose reportó v5.6.1 |
| PostgreSQL de prueba | postgres:17-bookworm, volumen persistente y sin puerto publicado |
| Persistencia | Registro ficticio conservado tras recrear el contenedor de PostgreSQL |
| API temporal | Node 22, Fastify 5 y pg 8 consultando PostgreSQL por red Compose |
| Acceso de prueba | Solo loopback de la VM, puerto 3000 |
| Consulta | status ok y mensaje Persistencia OK |
| RAM en reposo | API 112.3 MiB; PostgreSQL 32.07 MiB; no se aportó RAM final del host |

Estas imágenes y versiones describen el smoke test, no fijan versiones de producción. La API temporal en la carpeta remota de prueba no es KUME ni usa Prisma. No se instaló el producto en los repositorios por esta prueba.

La validación básica no acredita rendimiento bajo carga, persistencia tras reinicio de VM, archivos del producto, HTTPS, autenticación, aislamiento de demo, respaldos, restauración ni migración a intranet.

## Requisitos antes del piloto real

1. Construir imagen de la API real y fijar dependencias y versiones compatibles; ejecutar migraciones Prisma controladas.
2. Implementar y verificar el diseño técnico y el contrato API/OpenAPI documentados para la [autenticación confirmada](../technical/autenticacion-prototipo.md): Maxi y Vicky, mismos permisos, hashes en secrets sin tabla de usuarios, cambios manuales de contraseña, cierre y expiración tras 8 horas de inactividad y límites temporales por cuenta y por IP. No incluir recuperación por correo. Conservar reglas funcionales.
3. Configurar HTTPS, origen del frontend, certificados y proxy, sin publicar PostgreSQL ni archivos por rutas públicas sin autorización.
4. Verificar persistencia de base y archivos, carga/descarga de documentos y operaciones representativas; medir recursos y fallos por memoria. No equiparar swap con RAM.
5. Separar demo ficticia y piloto real en datos, archivos y credenciales.
6. Automatizar respaldo consistente diario de base, archivos y configuración (incluido el archivo de usuarios en secrets, no sesiones ni contadores), cifrado y fuera de Oracle; retención 30 días, alertas a Maxi y claves recuperables por KUME.
7. Probar restauración en entorno vacío y programar verificación trimestral. Google Drive institucional es candidato; mecanismo, capacidad gratuita y alertas aún pendientes.

## Migración completa a un entorno local

La migración es una alternativa si los límites o condiciones cloud comprometen el uso. Su preparación documental es parte del MVP; ejecutar y validar el despliegue local completo corresponde al momento de decidir el traslado.

### Preparación

- Elegir equipo del instituto, sistema operativo soportado, arquitectura, memoria, disco, red y responsable de mantenimiento. El equipo debe estar encendido durante el uso.
- Reutilizar Docker Compose e imágenes compatibles; permitir despliegue local en Windows o Linux tras verificar condiciones de operación. No asumir instalaciones ya probadas.
- Preparar almacenamiento persistente y PostgreSQL privado en red interna. Servir también el frontend dentro del instituto.
- Establecer nombre interno, HTTPS y confianza de certificados en las computadoras usuarias, sin abrir acceso remoto a la intranet.
- Identificar dependencias de autenticación, CDN y otros servicios externos. La operación diaria y los cambios manuales de contraseña deben funcionar sin cloud ni correo; documentar dependencias de internet para respaldos externos. Trasladar secrets de manera protegida y comprobar el acceso de Maxi y Vicky.

### Ensayo y traslado

1. Inventariar versiones, migraciones, configuración, cuentas, claves necesarias y volúmenes, sin exponer secretos.
2. Exportar una copia consistente de PostgreSQL y archivos y restaurarla en destino aislado, verificando integridad. No asumir que un dump incluye documentos.
3. Comprobar gastos/totales/anulados, rubros, personal, cursos, talleres, asignaciones, archivos y hashes, CSV y acceso de ambas cuentas.
4. Probar persistencia y arranque después de reinicio y acceso desde otra computadora de la LAN. Verificar operación diaria sin cloud en una prueba controlada.
5. Para el corte definitivo, acordar una ventana, bloquear escrituras en origen, generar respaldo final y restaurar/validar en destino antes de habilitar usuarios. No aceptar escrituras simultáneas en dos instalaciones.
6. Conservar origen y respaldo para volver atrás. Si ya hubo escrituras locales, reconciliar o transferir esos cambios antes de reabrir Oracle; no descartar trabajo restaurando simplemente una copia anterior.
7. Mantener copias cifradas fuera del equipo local, retención y alertas, con restauración comprobada.
8. Retirar Oracle solo por decisión expresa y después de validar destino y recuperación; no borrar VM ni discos automáticamente.

### Aceptación

La migración se considera completada después de comprobar integridad, cuentas, archivos, funcionamiento desde LAN, persistencia, operación diaria sin cloud y restauración, y obtener aceptación de Maxi para uso real. Documentar encendido, mantenimiento, acceso y recuperación para KUME.

## Referencias oficiales

Las condiciones de los proveedores deben volver a verificarse al aprovisionar:

- [Oracle Always Free](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm).
- [Preguntas frecuentes de Oracle Free Tier](https://www.oracle.com/cloud/free/faq/).
- [Instalación oficial de Docker en Ubuntu](https://docs.docker.com/engine/install/ubuntu/).

Fuentes del proyecto: [alcance](../functional/alcance-prototipo.md), [stack](../technical/stack-tecnologico.md), [API](../technical/api-design.md), [base](../technical/backend/database-design.md) y [OpenAPI](../../openapi.yaml).
