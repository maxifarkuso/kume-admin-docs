# Diseño técnico — 002

Bash conserva consultas y delega el grupo migraciones a Python estándar (sin
nuevas dependencias de producción). CLI, política de etapas, almacenamiento y
adaptador Git/Docker/PostgreSQL separados en scripts/kume_migrations.

Configuración JSON local privada con destino explícito; nunca DATABASE_URL.
El motor no imprime salida bruta de colaboradores: conserva código y etapa,
filtra solo metadatos conocidos. DATABASE_URL se analiza dentro del backend y
contenedor temporal; compara servidor, puerto, base y usuario sin contraseña.
DNS debe apuntar a la IP del contenedor PostgreSQL en la red aprobada. Solo esquema
public; rechazar options. Fijar identidad física de base, contenedores y releases
al preparar y compararla entre etapas para no usar respaldo de otro destino.

Locks exclusivos flock no bloqueantes: journal del administrador y deployment.lock
backend existente, orden fijo. No crear el lock de despliegue si falta. Para
workflows que no cooperan, el operador confirma una ventana sin despliegues ni
escrituras y mantiene esa exclusión externamente; leer pending no elimina carreras.
No afirmar coordinación universal. Revalidar tras confirmación y antes de SQL.

Operaciones en ~/.local/share/kume-admin/migrations, directorios 0700, archivos
0600. Journal JSON con reemplazo atómico y fsync. Registrar intención antes de
cada efecto; si termina abruptamente queda running, tratado como incierto.
Cada invocación toma locks. Respaldos exclusivos y nunca reemplazados. Revalidar
hash antes de uso. Imagen local resuelta desde backend actual, --pull=never,
384 MiB RAM/swap total, red explícita, sin puertos/socket, prisma montado readonly.
Archivos de Prisma extraídos del commit a snapshot privado; comparar checksums
con Git y journal en cada etapa. No ejecutar scripts del repositorio.

npm install --ignore-scripts con versión exacta de Prisma del proyecto (6.19.0
para esta entrega). Si npm anuncia approve-scripts en su lista de comandos, aprobar exclusivamente prisma
y @prisma/engines; reconstruir solo ambos paquetes. Verificar versión efectiva.
Sin instalación de herramientas en host ni actualización del producto.

Historia leída por SQL constante: comparar nombres/checksums y finalización con
archivos aprobados; fallos o divergencias bloquean. SQL de verificación inicial y final locales
aprobados por SHA-256, ejecutado con transacción de solo lectura; debe devolver
únicamente ok. No constituye validación universal de cualquier esquema.
Inicialización requiere ausencia total de historial, base no vacía y primera
migración explícita. Después de SQL incierto permite solo verificar y registrar,
nunca reejecutar desde el journal. Resolve exige verificación exitosa anterior,
repetida inmediatamente antes de registrar. Una inicialización fallida exige
investigación manual; no hay reparación o restauración automática.

Retirada verifica ID y etiqueta propios; nunca limpia por nombre genérico.
Reversión de herramienta: volver a la instalación anterior conservada, sin cambiar
base. Revertir código no revierte SQL; recuperación de datos requiere plan y
restauración explícitos, fuera de esta feature.

## Corrección UID y recuperación explícita — 9 de noviembre

La cuenta operativa puede tener UID/GID distintos a la imagen. Docker run y exec
Prisma fijan los del operador no root, con HOME propio en /tmp, y verifican lectura
del snapshot antes de instalar o escribir. No ampliar 0700/0600 ni escribir el bind.
Para contenedores antiguos, exec fija usuario/HOME sin recrear servicios.

habilitar-reintento es una acción sin SQL de escritura. Solo admite un migrate
deploy incierto, preparado correcto y ausencia de inicialización/resolve. Requiere
un SELECT de recuperación privado aprobado por SHA-256, en flags separados para
conservar la configuración inmutable. Lo ejecuta READ ONLY antes/después de la
confirmación, compara historia y verifica respaldo/fuente/destino. Agrega evento y
evidencia ligados al índice del intento incierto y pendientes actuales. No cambia
ese evento a éxito ni desbloquea operaciones ajenas. El siguiente aplicar consume
la habilitación al registrar una nueva intención; antes relee el inspector y hash.
Una aplicación parcial o semántica no demostrada por la inspección sigue bloqueada.
El operador es responsable de revisar el inspector contra todos los efectos SQL.
