# Paso a paso — tablas de gastos y comprobantes

Preparado el 8 de noviembre de 2026. Procedimiento pendiente de ejecución en Oracle.
Ejecutar como ubuntu, un comando por vez, revisar su resultado antes de continuar.
No compartir runtime.env, contraseñas, URLs completas de base, claves ni logs privados.

## Revisiones identificadas

- Motor kume-admin: commit de docs `3c262bd2a92702228515d6ef7596d136e5df29a1`.
- Backend: `caf0259f7aa55a99ccc7a19062fb58a57ec1b561`, rama
  `feat/payment-records`, consultada al preparar esta guía; todavía fuera de main.
- Archivo: `prisma/migrations/20261108170000_payment_records/migration.sql`.
- Crea **category, expense y receipt**; `receipe` no es el nombre del comprobante.
- Crea constraints, índices, triggers y rubros iniciales; no solo tablas vacías.

Revisar y aprobar ese SQL antes de aplicarlo. No sustituir el SHA por HEAD/main ni
usar el viejo checkout ec3a784: no contiene esta migración. Aplicar el esquema no
publica el backend/frontend de gastos ni configura almacenamiento de comprobantes.

## 1. Revalidar la VM y la ventana

Primero:

```bash
hostname
```

Después, por separado: `id -un`, `kume-admin estados`, `kume-admin memoria` y
`kume-admin contenedores`. Confirmar la VM esperada, usuario ubuntu, estados
coherentes sin pending y PostgreSQL healthy. No usar sudo global.

Coordinar una ventana sin escrituras ni despliegues. Comprobar los workflows
realmente instalados: el lock backend no excluye actores que no lo respetan.
No detener ni reiniciar servicios por inferencia.

Inspeccionar la historia sin mostrar datos de negocio (los nombres siguientes
son los históricos; usarlos solo si el inventario los confirma):

```bash
sudo docker exec kume-infra-test-db-1 psql -X -v ON_ERROR_STOP=1 -U kume_test -d kume_test -c 'SELECT migration_name, checksum, finished_at IS NOT NULL AS finished, rolled_back_at IS NOT NULL AS rolled_back FROM public._prisma_migrations ORDER BY started_at, id;'
```

Deben figurar las dos migraciones de catálogos, terminadas, sin reversión y con
checksums compatibles con el commit elegido. Si falta el historial o hay un error,
detenerse e inspeccionar; **no usar resolve/inicializar como atajo** para gastos.
Si payment_records ya figura aplicada, comprobar esquema y no volver a ejecutar SQL.

## 2. Obtener el motor completo sin reemplazar la copia instalada

Desde un acceso Git ya configurado, clonar docs en un directorio nuevo:

```bash
git clone --no-checkout https://github.com/maxifarkuso/kume-admin-docs.git "$HOME/kume-admin-docs-migrations"
```

Si falta acceso, detenerse: no crear credenciales ni pedir tokens. Si el directorio
existe, inspeccionarlo; no borrarlo ni sobrescribirlo. Fijar el commit de motor
indicado al inicio:

```bash
git -C "$HOME/kume-admin-docs-migrations" checkout --detach 3c262bd2a92702228515d6ef7596d136e5df29a1
```

Comprobar `git rev-parse HEAD`, revisar los archivos y ejecutar
por separado `bash -n scripts/oracle-admin.sh` y las dos ayudas desde ese checkout.

Usar la ruta versionada `bash "$HOME/kume-admin-docs-migrations/scripts/oracle-admin.sh"`
durante este procedimiento. No basta con descargar solamente oracle-admin.sh: necesita
oracle-migrations.py y el paquete kume_migrations de la misma revisión. La copia
histórica de ~/.local/bin/kume-admin puede seguir siendo la versión de consultas.

## 3. Obtener el SQL en un checkout separado

Con la deploy key de solo lectura ya configurada y el host SSH ya conocido:

```bash
GIT_SSH_COMMAND="ssh -i $HOME/.ssh/kume-backend-github -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes" git clone --no-checkout git@github.com:maxifarkuso/kume-admin-be.git "$HOME/kume-backend/migrations-payment-records"
```

Luego:

```bash
git -C "$HOME/kume-backend/migrations-payment-records" checkout --detach caf0259f7aa55a99ccc7a19062fb58a57ec1b561
```

Comprobar revisión y limpieza por separado:

```bash
git -C "$HOME/kume-backend/migrations-payment-records" rev-parse HEAD
```

```bash
git -C "$HOME/kume-backend/migrations-payment-records" status --short
```

Inspeccionar migration.sql y su SHA-256. No modificar ese checkout para adaptar
la base ni ejecutar npm en el host. No crear claves/known_hosts automáticamente.

## 4. Preparar verificación y configuración privadas

Seguir el formato completo de [migraciones-admin.md](migraciones-admin.md#configuración-privada).
Crear archivos 0600 fuera del repositorio y un directorio privado 0700. Completar
host, IDs por nombre, red, rutas y destino después de la comprobación del paso 1.

Para este caso, fijar:

- revision: `caf0259f7aa55a99ccc7a19062fb58a57ec1b561`.
- repository: `git@github.com:maxifarkuso/kume-admin-be.git`.
- checkout: `/home/ubuntu/kume-backend/migrations-payment-records`.
- initial_migration: `202611070001_catalogs`; es un campo del formato, **no ejecutar
  las acciones excepcionales inicializar ni registrar-inicializacion**.
- Los demás valores son los del destino revalidado, no los del ejemplo ficticio.

Preparar un SELECT verificador final aprobado que devuelva solo `ok` cuando sean
correctas las tablas, columnas/tipos/defaults, constraints, índices, triggers, rubros
iniciales e historial completo. Comprobar también que se conservan catálogos y la
tabla de infraestructura previa. No usar SELECT 'ok' sin condiciones. Registrar su
SHA-256 en verification_sha256. El formato también exige initial_verification_sql y
su hash; para este flujo normal pueden apuntar al mismo verificador final, porque
no se utilizarán las acciones de inicialización. El motor valida ambos archivos
antes de escribir. No inventar el hash ni omitir la preparación del verificador.

La configuración real y el SQL final se cierran después de ver el inventario e
historial del paso 1; esta guía no acredita haberlos inspeccionado en la VM.

## 5. Diagnóstico, herramientas y respaldo

Con configuración revisada en `/home/ubuntu/kume-payment-migration.json` y un ID
nuevo `payment-records-001`, ejecutar por separado:

```bash
bash "$HOME/kume-admin-docs-migrations/scripts/oracle-admin.sh" migraciones diagnostico --config "$HOME/kume-payment-migration.json" --operacion payment-records-001
```

El pendiente esperado es **solo 20261108170000_payment_records**. Si hay otros,
detenerse y revisar todos los SQL antes de aprobar un deploy que los aplicaría.

```bash
bash "$HOME/kume-admin-docs-migrations/scripts/oracle-admin.sh" migraciones preparar --config "$HOME/kume-payment-migration.json" --operacion payment-records-001
```

Confirmar el resumen literal tras revisar host/base/revisión y ventana. Preparar
crea herramientas temporales; no debe tocar el backend instalado ni publicar puertos.

```bash
bash "$HOME/kume-admin-docs-migrations/scripts/oracle-admin.sh" migraciones respaldo --config "$HOME/kume-payment-migration.json" --operacion payment-records-001
```

Exigir respaldo CUSTOM no vacío, índice legible y checksum registrados. No equivale
a restauración probada y no respalda archivos de comprobantes. Un error bloquea SQL.

```bash
bash "$HOME/kume-admin-docs-migrations/scripts/oracle-admin.sh" migraciones estado --config "$HOME/kume-payment-migration.json" --operacion payment-records-001
```

## 6. Aplicar y verificar

Solo después de revisar las salidas anteriores y aprobar el SQL:

```bash
bash "$HOME/kume-admin-docs-migrations/scripts/oracle-admin.sh" migraciones aplicar --config "$HOME/kume-payment-migration.json" --operacion payment-records-001
```

El motor pide confirmación, revalida destino/respaldo y ejecuta migrate deploy.
No usa db push, reset ni resolve para gastos. Comprueba historia y verificador final.
Si falla o se interrumpe, inspeccionar journal/historia/esquema/proceso remoto;
no repetir con otro ID ni asumir que el SQL se revirtió.

```bash
bash "$HOME/kume-admin-docs-migrations/scripts/oracle-admin.sh" migraciones verificar --config "$HOME/kume-payment-migration.json" --operacion payment-records-001
```

Inspección complementaria, sin datos de negocio:

```bash
sudo docker exec kume-infra-test-db-1 psql -X -v ON_ERROR_STOP=1 -U kume_test -d kume_test -c '\d public.category' -c '\d public.expense' -c '\d public.receipt'
```

Una segunda llamada a aplicar después de éxito debe informar sin pendientes y sin
repetir escrituras. Conservar el mismo ID y configuración.

## 7. Retirar únicamente herramientas temporales

```bash
bash "$HOME/kume-admin-docs-migrations/scripts/oracle-admin.sh" migraciones retirar --config "$HOME/kume-payment-migration.json" --operacion payment-records-001
```

Conservar journal, dump y checkout. No borrar volúmenes ni restaurar implícitamente.
Desplegar gastos/backend/frontend es un paso posterior y separado; requiere también
el volumen privado de comprobantes y su respaldo, según la
[implementación de pagos](../specs/003-payment-records/implementation.md).

## Incidencia de acceso y actualización — 9 de noviembre

La sesión guiada identificó snapshot 0700/0600 de ubuntu UID/GID 1001 y contenedor
node UID/GID 1000. Preparar no había comprobado lectura; aplicar falló con EACCES
sobre /migration/schema.prisma. Se inspeccionaron dos migraciones antiguas completas
y ausencia de category/expense/receipt/payment_updated_at. Estos resultados son
previos a la recuperación: no registrar la migración como aplicada por esta evidencia.

No repetir con otro ID ni ampliar permisos del snapshot. Actualizar a la revisión
con corrección UID/HOME y habilitar-reintento según la guía propietaria. La revisión
original 3c262bd y la corrección npm 9012f0d son históricas y no corrigen esta incidencia.
Conservar payment-records-002 y su respaldo. Antes de habilitar el reintento deben
confirmarse causa y ausencia de efectos parciales y de procesos migradores activos,
con inspector específico aprobado; después aplicar se ejecuta por separado.
