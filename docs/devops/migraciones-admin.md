# Migraciones de base con kume-admin

Estado: implementación local; no instalada ni verificada en Oracle. La
[spec 002](../specs/002-admin-migrations/spec.md) y su
[diseño](../specs/002-admin-migrations/technical-spec.md) definen esta ampliación.
Oracle es el host; la base sigue siendo PostgreSQL. Consultas anteriores conservan
su contrato de lectura. Ninguna migración se ejecuta al abrir el menú.

## Antes de operar

Obtener autorización expresa para el destino y SQL de esta sesión. Esta entrega
solo autoriza desarrollo y pruebas locales. Revalidar host, usuario, estados,
backend, PostgreSQL, red y recursos; los nombres/SHA de la sesión histórica no
son descubrimiento del entorno actual. Ejecutar como usuario operativo, sin sudo
global. Python 3.9+, Git, Docker, sudo ya autorizado, Bash y acceso SSH configurado.
La utilidad no crea claves, acepta hosts desconocidos, clona, instala paquetes en
el host ni modifica permisos del repositorio. Si falta acceso, detenerse.

Preparar por separado un checkout limpio de un SHA completo aprobado del backend,
con origin SSH configurado; conservar cualquier checkout con cambios. No usar una
release activa. El paquete prisma del package.json debe fijar exactamente 6.19.0.
No se actualiza por avisos. Se extraen de Git los archivos Prisma al snapshot de
la operación; no se ejecutan scripts de ese checkout. Revisar schema, SQL y
checksums antes de aprobar. El origen declarado no prueba la firma o aprobación
del commit: esa revisión es responsabilidad del operador.

Coordinar una ventana sin despliegues ni escrituras de usuarios. Verificar qué
workflows instalados respetan realmente el deployment.lock del backend. El motor
lo toma exclusivo y no bloqueante, junto con su lock global, y rechaza pending;
no coordina pipelines/manuales que ignoren ese lock. No basta con mirar pending
una vez. Suspender externamente esos actores y mantener la ventana hasta terminar;
la frase de confirmación registra la declaración del operador, no la verifica.
No se detienen servicios ni se cambian permisos automáticamente.

## Configuración privada

Crear fuera del checkout un JSON de propietario operativo y modo 0600. El ejemplo
es ficticio; sustituir cada destino después de inspeccionarlo. No incluir URL de
base, contraseña, token, valores de runtime.env o claves. Rutas absolutas canónicas,
sin enlaces simbólicos en los archivos privados. El lock debe existir junto al
estado backend; no crearlo para evitar un error.

```json
{
  "host": "vm-fixture",
  "backend": "fixture-api-1",
  "postgres": "fixture-db-1",
  "network": "fixture_default",
  "server": "db",
  "port": "5432",
  "database": "fixture",
  "user": "fixture",
  "revision": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "repository": "git@github.com:example/fixture-backend.git",
  "checkout": "/home/operator/fixture-migrations",
  "runtime_env": "/home/operator/fixture-backend/shared/runtime.env",
  "backend_state": "/home/operator/fixture-backend/state.json",
  "frontend_state": "/home/operator/.local/share/fixture-frontend/state.json",
  "webroot": "/srv/fixture-frontend",
  "deployment_lock": "/home/operator/fixture-backend/deployment.lock",
  "verification_sql": "/home/operator/final-verification.sql",
  "verification_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "initial_verification_sql": "/home/operator/schema-verification.sql",
  "initial_verification_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
  "initial_migration": "202601010001_schema"
}
```

Los dos verificadores son archivos locales privados, revisados y aprobados por
SHA-256. Cada uno contiene un único SELECT que devuelve solamente la fila `ok`
si cumple todas sus condiciones; cualquier otro resultado falla. No usar el
trivial SELECT 'ok' como prueba de un esquema. El inicial comprueba estructura,
columnas, defaults, restricciones, índices, triggers y conservación de las tablas
previas según el SQL específico. El final comprueba historia y datos esperados
según [alcance](../functional/alcance-prototipo.md) y
[base](../technical/backend/database-design.md), sin duplicar esos valores en el
administrador. Se ejecutan en transacción READ ONLY con PGOPTIONS; no admiten
metacomandos ni varias sentencias. No usar funciones con efectos externos.
Son código aprobado, no una entrada SQL no confiable.

El motor admite Node 18/20/22/24 y npm 9/10/11 como candidatos; la ejecución efectiva
de Prisma debe confirmar compatibilidad. Resuelve la imagen local desde backend,
verifica que tenga Node/npm y exige RAM disponible mínima de 512 MiB y 1 GiB libre,
además de espacio para dos veces el tamaño actual de base más 256 MiB. Estos umbrales
son conservadores, no aseguran ausencia de OOM. No crea swap. Instala Prisma
6.19.0 exclusivamente en /tmp del contenedor, con install scripts deshabilitados;
detecta approve-scripts mediante npm --help y, si está disponible, aprueba solamente
prisma y @prisma/engines. Para npm previo usa rebuild explícito de ambos paquetes.
Un fallo de capacidades/versiones aborta; no instala otra versión como alternativa.

## Etapas explícitas

Usar un ID nuevo por operación, conservar el mismo ID y el mismo JSON entre etapas.
Los comandos siguientes son una secuencia de referencia; en una terminal del usuario
explicar y ejecutar uno por vez, esperando su resultado. No copiar toda la secuencia
contra Oracle sin revisión y autorización.

```bash
kume-admin migraciones --help
kume-admin migraciones diagnostico --config /ruta/privada/destino.json --operacion cambio-001
kume-admin migraciones preparar --config /ruta/privada/destino.json --operacion cambio-001
kume-admin migraciones respaldo --config /ruta/privada/destino.json --operacion cambio-001
kume-admin migraciones estado --config /ruta/privada/destino.json --operacion cambio-001
kume-admin migraciones aplicar --config /ruta/privada/destino.json --operacion cambio-001
kume-admin migraciones verificar --config /ruta/privada/destino.json --operacion cambio-001
kume-admin migraciones retirar --config /ruta/privada/destino.json --operacion cambio-001
```

Diagnóstico/estado inspeccionan identidad, fuentes, tablas e historia SQL; no crean
herramientas ni aplican SQL. Crean solo el directorio local operativo y sus locks.
Muestran pendientes comparando nombres/checksums/finalización del historial con el
commit aprobado; una migración fallida, revertida o divergente exige investigación.
No se usa el código 1 de Prisma migrate status como sinónimo universal de pendientes.

Preparar solicita confirmación y crea un contenedor temporal --rm, --pull=never,
384 MiB de RAM y swap total limitado a lo mismo, sin puertos ni socket Docker.
Recibe runtime.env sin imprimirlo y monta el snapshot Prisma readonly. La conexión
se parsea dentro de backend y herramientas, mostrando solo identidad aprobada;
DNS debe coincidir con la IP de PostgreSQL en la red configurada. Esta entrega
admite únicamente el esquema public y rechaza el parámetro de conexión options.
Conserva IDs de contenedores, releases y system_identifier de PostgreSQL: un cambio
entre etapas bloquea la operación. El usuario SQL necesita poder leer pg_control_system;
si no puede, falla sin conceder privilegios.

Respaldo crea pre-migration.dump con modo 0600 y creación exclusiva. Valida tamaño,
índice con pg_restore --list y SHA-256. **No prueba restauración**, no incluye archivos
del producto ni sustituye copias cifradas externas. Un dump parcial queda conservado
como evidencia fallida y nunca habilita escrituras.

Aplicar exige respaldo intacto, historia coherente, confirmación literal con
acción/host/base/revisión/ventana y revalidación antes de migrate deploy. Comprueba
historia completa y verificador final. Si no hay pendientes en una segunda llamada
tras éxito, informa sin volver a escribir. Una base pública no vacía sin historial
no entra en deploy automático. Los datos de carga inicial provienen de las migraciones.

## Inicialización excepcional

Solo para una base preexistente cuyo estado haya sido inspeccionado y aprobado,
sin ninguna fila de historial y con primera migración explícita. No generalizar
la conservación de infrastructure_check de la sesión histórica a otras bases.

Después de preparar y respaldar, usar `inicializar` en lugar de aplicar. Confirma
nombre/checksum y ejecuta exactamente el archivo SQL de la primera migración;
comprueba el verificador inicial. Luego `verificar` repite ese verificador y guarda
su evidencia posterior al SQL. Solo entonces `registrar-inicializacion` pide otra
confirmación, repite la verificación y ejecuta resolve --applied para esa primera
migración. Después `aplicar` despliega el resto y usa el verificador final.
No se registra una migración para saltear SQL pendiente, fallos o divergencias.

## Evidencias, interrupción y limpieza

Registros en ~/.local/share/kume-admin/migrations/OPERACION/journal.json, directorios
0700 y archivos 0600: destino, revisión, versiones, snapshot y checksums, contenedor,
respaldo, etapas/fecha/código y resultados. Sin salida bruta de npm/Prisma/SQL ni secrets.
Los códigos positivos de colaboradores se conservan; cancelación/interrupción: 130;
lock ocupado: 75; uso inválido: 2; validación: 1; timeout: 124.

Una intención `running` puede haber ejecutado SQL incluso sin respuesta. Un fallo
de escritura se registra `uncertain`, conservando código. SIGINT/SIGTERM registran
interrupción cuando es posible; SIGKILL puede dejar running. El proceso remoto puede
seguir vivo tras timeout o pérdida de conexión. No reintentar SQL ni asumir rollback.
Inspeccionar historial, esquema, datos y proceso remoto durante la ventana.
Otra operación con escritura incierta bloquea nuevas escrituras, incluso con otro ID.

Si la inicialización quedó entre SQL y resolve, no se repite db execute. Inspeccionar
manualmente efectos completos; solo si el verificador inicial aprobado confirma todo,
`verificar` y `registrar-inicializacion` permiten continuar en el mismo ID. Si falla,
se requiere recuperación manual autorizada. Un resolve o deploy incierto se investiga
manualmente; la utilidad no ofrece un botón para borrar la incertidumbre. No editar
journal para forzar escrituras: conservar evidencia y documentar una decisión de
recuperación separada antes de cualquier intervención.

`retirar` funciona aun si falló la preparación. Detiene únicamente el ID cuyo label
kume.migration coincida con la operación; si se interrumpió antes de persistir el ID,
resuelve el nombre registrado y exige ese mismo label. No usa rm genérico, prune,
reset, db push, down -v, reinicios ajenos ni borrado de checkout/respaldo. No retira
automáticamente el contenedor ante fallo: queda disponible para inspección y retirada
explícita. Si ya no existe, informa fallo sin tocar otros contenedores.

No restaura ni ejecuta workflows. El despliegue backend y luego frontend de la sesión
histórica seguían pendientes: el SQL aplicado no acredita esos despliegues.
Para revertir la utilidad, recuperar su versión anterior conservada; eso no revierte
la base. Restauración y corrección de datos requieren autorización y plan propios.

## Instalación de esta ampliación

La instalación histórica de un único archivo conserva sus checksums y evidencia en
[administración](administracion-oracle.md). Esta versión necesita oracle-admin.sh,
oracle-migrations.py y el paquete kume_migrations juntos en el mismo directorio.
Preparar una carpeta versionada privada con todos esos archivos de un commit revisado,
validar los SHA-256 de cada archivo y ejecutar allí sintaxis, suite y ambas ayudas.
Conservar la instalación anterior antes de cambiar el comando de entrada. No usar el
checksum histórico para estos archivos ni mezclar revisiones del paquete y dispatcher.
La instalación, cambio de PATH y pruebas contra la VM quedan pendientes de sesión
autorizada; no se atribuyen a las pruebas locales de esta entrega.
