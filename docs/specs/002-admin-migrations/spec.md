# 002 — Migraciones controladas con kume-admin

Estado: alcance autorizado para desarrollo local el 7 de noviembre de 2026.
No autoriza ejecución en Oracle, instalación, publicación ni despliegue.

## Comportamiento

Conservar las consultas existentes sin escrituras añadidas. Agregar el grupo
`migraciones` al menú y CLI, con ayuda propia y etapas explícitas: `diagnostico`,
`preparar`, `respaldo`, `estado`, `aplicar`, `inicializar`,
`registrar-inicializacion`, `verificar` y `retirar`.

Identificar host, contenedores, servidor, base, usuario y SHA completo aprobado.
Reutilizar un checkout limpio, separado del directorio de releases, con origen
aprobado y Prisma fijado; no obtener credenciales ni modificar checkouts.
Confirmar destino y ventana coordinada antes de preparar herramientas y escribir
la base. Tomar locks no bloqueantes y revisar estados sin pending, recursos,
configuración privada y procedencia. Crear respaldo CUSTOM privado, comprobar
su índice y checksum antes de aplicar. El índice legible no prueba restauración.

El flujo habitual usa migrate deploy. Una base preexistente sin historial exige
un flujo excepcional: SQL identificado por checksum, confirmación específica,
ejecución, verificación aprobada de solo lectura y registro separado con resolve.
Nunca resolver para ignorar SQL, fallos o historia divergente. Una interrupción
conserva resultado incierto: inspeccionar, sin repetición automática de escrituras.
El verificador debe comprobar estructura y datos que correspondan al proyecto;
los valores de catálogos pertenecen al alcance y diseño de base, no a esta utilidad.

Guardar metadatos sin secretos y preservar códigos de colaboradores. Retirar solo
el contenedor cuya identidad y etiqueta coincidan con la operación, conservando
respaldo, checkout y evidencias. No restaurar ni desplegar implícitamente.

## Aceptación

Pruebas con dobles: cancelación/EOF, destino erróneo, recursos insuficientes,
respaldo/herramientas/migración fallidos, divergencia, inicialización excepcional,
interrupciones, bloqueo y limpieza limitada. Mantener suite de consultas.
No atribuir a esas pruebas PostgreSQL real, restauración o recuperación comprobada.

Fuentes: [administración](../../devops/administracion-oracle.md),
[infraestructura](../../devops/infraestructura-y-migracion.md),
[alcance](../../functional/alcance-prototipo.md) y
[base](../../technical/backend/database-design.md).

## Corrección operativa aprobada — 9 de noviembre de 2026

Maxi solicita corregir el acceso del contenedor al snapshot. El operador Ubuntu
usa UID/GID 1001 y la imagen node usa 1000; 0700/0600 impiden esa lectura. Mantener
el snapshot privado y ejecutar herramientas con UID/GID operativo y HOME temporal,
comprobando acceso antes de SQL. No modificar el usuario de servicios del producto.

Para retomar el deploy afectado, admitir habilitar-reintento tras inspección SQL
específica aprobada por hash y confirmación separada. Conservar el evento incierto,
revalidar identidad/respaldo/historia/fuente y el inspector antes de la siguiente
aplicación. No repetir SQL automáticamente ni habilitar recuperación excepcional
con resolve. El procedimiento propietario está en la guía de migraciones.
