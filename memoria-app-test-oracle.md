# KUME — Memoria de la app de prueba en Oracle

**Registro:** 3 de noviembre de 2026. Pruebas originales realizadas el 1 de noviembre.
**Estado:** smoke test comprobado por Maxi; memoria guardada antes de que elimine el contenido de `~/kume-infra-test` para preparar el backend MVP. La eliminación y el despliegue real todavía no fueron verificados.

## Qué era esta app

Prueba aislada de infraestructura: Fastify consultando PostgreSQL por la red de Docker Compose. No era el backend de KUME, no usaba Prisma, no tenía autenticación, HTTPS ni archivos del producto. No copiar su usuario superadministrador o instalación de dependencias al arrancar a producción.

Los documentos vigentes prevalecen para el MVP: [infraestructura](infraestructura-y-migracion.md), [stack](stack-tecnologico.md), [autenticación](autenticacion-prototipo.md), [arquitectura backend](backend-architecture.md) y [guía de desarrollo](development-guide.md). El diseño posterior aloja frontend y API bajo el mismo proxy HTTPS en Oracle; no usa recuperación de contraseña por correo. Esta memoria no revierte esas decisiones.

## Instancia y acceso conocidos

- Host: `kume-backend`; región indicada por Maxi: Brasil Southeast. IP pública no registrada: consultar la instancia actual en Oracle.
- Shape seleccionado E2.1.Micro, señalado por Maxi como Always Free; verificar recursos y elegibilidad actuales.
- Imagen final: Canonical Ubuntu 24.04 Minimal, build indicado `2026.10.27-0`; terminal reportó Ubuntu 24.04.5 LTS, arquitectura `x86_64`.
- Usuario SSH: `ubuntu`, con `sudo -n true` correcto. No se necesita contraseña de root ni contraseña cloud para sudo en esta imagen.
- Clave privada local referida como `ssh-key-2026-11-01.key`; el nombre no implica que esté disponible en cualquier computadora. No subirla a Git ni compartir su contenido.
- RAM: 952 MiB, sin swap. Disco raíz de 45 GB, aproximadamente 43 GB libres antes de instalar imágenes.
- Docker Engine instalado desde repositorio oficial; servicio habilitado y hello-world correcto. Compose reportó `v5.6.1`.
- Antes se probaron Oracle Linux y CentOS Stream 8. No retomar esas imágenes por inercia; pueden existir instancias/discos anteriores consumiendo cuota. No borrarlos sin revisar y autorizar.

Desde la computadora que tiene la clave:

```bash
ssh -i "ssh-key-2026-11-01.key" ubuntu@IP_PUBLICA
```

Sustituir IP_PUBLICA. Verificar huella del servidor antes de aceptar una nueva conexión. Si SSH rechaza la clave por permisos abiertos, en Linux/macOS/WSL restringirla con `chmod 600 ssh-key-2026-11-01.key`; en Windows revisar sus ACL. La clave privada no se descarga posteriormente desde el detalle de la VM.

## Arrancar cuando la carpeta y archivos todavía existen

Dentro de la VM:

```bash
cd ~/kume-infra-test
sudo docker compose -f compose.yaml -f compose.api.yaml up -d
sudo docker compose -f compose.yaml -f compose.api.yaml ps
```

La primera vez descarga imágenes e instala las dependencias del servidor temporal. Esperar el inicio de Fastify antes de consultar:

```bash
curl --fail --max-time 10 http://127.0.0.1:3000/health
sudo docker compose -f compose.yaml -f compose.api.yaml logs --tail=50 -f api
```

Ctrl+C sale de los logs sin detener contenedores. La respuesta verificada fue:

```json
{"status":"ok","database":"Persistencia OK"}
```

El puerto 3000 se publicó solo en loopback. No se abrió acceso OCI ni PostgreSQL a internet. Para consultar desde la computadora del operador sin abrir puertos, puede usarse un túnel SSH local en otra terminal:

```bash
ssh -i "ssh-key-2026-11-01.key" -N -L 13000:127.0.0.1:3000 ubuntu@IP_PUBLICA
```

Luego consultar `http://127.0.0.1:13000/health` desde esa computadora. El túnel es una opción documentada, no una prueba ejecutada en la sesión.

## Archivos para reconstruir el smoke test

Estos son los archivos usados, reconstruidos desde los comandos de la conversación. Crear solo en una carpeta de prueba identificada, sin sobrescribir un MVP o secretos existentes. No ejecutar contra una base con datos reales.

### Estructura

```text
~/kume-infra-test/
  .env                   # Contraseña aleatoria; nunca guardar en Git
  compose.yaml
  compose.api.yaml
  api-test/
    package.json
    server.js
    node_modules/        # Generado por el contenedor
    package-lock.json   # Generado al resolver las dependencias
```

Las versiones transitivas exactas de npm no se capturaron en esta memoria; una reinstalación desde cero puede resolver versiones distintas dentro de los rangos. Preservar el lockfile original si se requiere reproducirlas exactamente.

### Carpeta y secreto

```bash
mkdir -p ~/kume-infra-test
cd ~/kume-infra-test
umask 077
test -e .env || printf 'POSTGRES_PASSWORD=%s\n' "$(openssl rand -hex 24)" > .env
mkdir -p api-test
```

No regenerar `.env` si se reutiliza el volumen original: cambiar la variable no cambia automáticamente la contraseña de un PostgreSQL ya inicializado. Esta memoria no conserva el secreto original ni necesita hacerlo para recrear una prueba vacía con otro volumen.

### compose.yaml

```yaml
services:
  db:
    image: postgres:17-bookworm
    restart: unless-stopped
    environment:
      POSTGRES_DB: kume_test
      POSTGRES_USER: kume_test
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Falta la contraseña}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U kume_test -d kume_test"]
      interval: 10s
      timeout: 5s
      retries: 10
    mem_limit: 256m

volumes:
  postgres_data:
```

### api-test/package.json

```json
{
  "private": true,
  "type": "module",
  "dependencies": {
    "fastify": "^5.0.0",
    "pg": "^8.0.0"
  }
}
```

### api-test/server.js

```javascript
import Fastify from 'fastify';
import pg from 'pg';

const app = Fastify({ logger: true });
const pool = new pg.Pool({ max: 2 });

app.get('/health', async () => {
  const result = await pool.query(
    'SELECT message FROM infrastructure_check WHERE id = 1'
  );
  return { status: 'ok', database: result.rows[0]?.message };
});

await app.listen({ host: '0.0.0.0', port: 3000 });
```

### compose.api.yaml

```yaml
services:
  api:
    image: node:22-bookworm-slim
    working_dir: /app
    command: sh -c "npm install --omit=dev --no-audit --no-fund && node server.js"
    environment:
      PGHOST: db
      PGDATABASE: kume_test
      PGUSER: kume_test
      PGPASSWORD: ${POSTGRES_PASSWORD:?Falta la contraseña}
      NODE_OPTIONS: --max-old-space-size=128
    volumes:
      - ./api-test:/app
    ports:
      - "127.0.0.1:3000:3000"
    depends_on:
      db:
        condition: service_healthy
    mem_limit: 256m
```

El contenedor temporal instala paquetes con su usuario predeterminado y puede dejar archivos propiedad de root en `api-test`. No usar este patrón de arranque ni copiar esos permisos al despliegue final.

## Inicializar el dato ficticio y comprobar persistencia

Después de escribir los archivos:

```bash
sudo docker compose -f compose.yaml -f compose.api.yaml up -d db
sudo docker compose -f compose.yaml -f compose.api.yaml ps
```

Cuando PostgreSQL aparezca healthy:

```bash
sudo docker compose -f compose.yaml -f compose.api.yaml exec -T db psql -U kume_test -d kume_test <<'SQL'
CREATE TABLE IF NOT EXISTS infrastructure_check (
  id integer PRIMARY KEY,
  message text NOT NULL
);
INSERT INTO infrastructure_check VALUES (1, 'Persistencia OK')
ON CONFLICT (id) DO UPDATE SET message = EXCLUDED.message;
SQL
sudo docker compose -f compose.yaml -f compose.api.yaml up -d
```

Para la recreación de prueba, aceptando la interrupción de la base ficticia:

```bash
sudo docker compose -f compose.yaml -f compose.api.yaml up -d --force-recreate db
```

Esperar healthy antes de verificar:

```bash
sudo docker compose -f compose.yaml -f compose.api.yaml exec -T db \
  psql -U kume_test -d kume_test -c 'SELECT * FROM infrastructure_check;'
curl --fail --max-time 10 http://127.0.0.1:3000/health
sudo docker stats --no-stream
free -h
```

Resultado histórico: registro `1 | Persistencia OK`, consulta HTTP correcta, API 112.3 MiB/256 MiB y PostgreSQL 32.07 MiB/256 MiB en reposo, CPU alrededor de 0 %. La salida final de memoria del host no fue aportada. No acredita carga real ni memoria del backend con Prisma.

## Retirar la prueba antes de borrar la carpeta

Maxi manifestó que borrará el contenido para preparar el backend MVP. No se ejecutó ninguna eliminación desde esta sesión. Antes de borrar, estando aún presentes los dos Compose:

```bash
cd ~/kume-infra-test
sudo docker compose -f compose.yaml -f compose.api.yaml ps
sudo docker compose -f compose.yaml -f compose.api.yaml down
```

`down` detiene y elimina contenedores y la red del proyecto; conserva el volumen nombrado. Así se libera el puerto 3000 sin borrar datos de base. Si se necesita preservar exactamente la prueba, guardar también sus archivos y `.env` en una ubicación protegida antes del borrado; no publicar el secreto.

Borrar una carpeta **no detiene contenedores ni elimina imágenes o volúmenes Docker**. Por defecto el proyecto se llamó `kume-infra-test` y el volumen `kume-infra-test_postgres_data`; comprobar etiquetas reales antes de operar. `restart: unless-stopped` en la base puede mantenerla o arrancarla de nuevo si no fue detenida explícitamente.

No usar `down -v`, `docker volume prune` ni borrados globales como limpieza automática. Eliminar el volumen de prueba requiere comprobar que solo contiene datos ficticios y una decisión explícita; no es necesario para liberar el puerto.

Si la carpeta ya se borró, inspeccionar antes de actuar:

```bash
sudo docker ps -a --filter label=com.docker.compose.project=kume-infra-test
sudo docker volume ls --filter label=com.docker.compose.project=kume-infra-test
```

No generar nuevos secretos y asumir que servirán para ese volumen antiguo. No recrear automáticamente la API si sus archivos bind-mount fueron eliminados. Confirmar identidad y estado de contenedores antes de detenerlos por nombre o ID.

## Paso al MVP

- Usar un proyecto Compose y volúmenes explícitamente separados de la prueba. No reutilizar la base `kume_test` como base del producto ni su usuario superadministrador como cuenta de aplicación.
- Si se conserva el nombre de carpeta, fijar un nombre de proyecto nuevo para evitar reutilización accidental de recursos anteriores.
- Inspeccionar el código real de `maxifarkuso/kume-admin-be`, su README, Dockerfile, Compose y migraciones antes de indicar comandos de despliegue. No asumir que siguen vacíos.
- Conservar Docker Engine, Compose, acceso SSH y la VM; borrar el directorio de prueba no exige reinstalarlos.
- No abrir 3000/5432 directamente a internet. El diseño vigente usa proxy HTTPS y secretos de autenticación del MVP, no esta API sin login.
- Pendientes del MVP se determinan por los documentos actuales; esta memoria no afirma despliegue, respaldo o migración completados.

## Cómo retomar en otra sesión

Leer este archivo para recuperar la app de prueba, e infraestructura/stack/autenticación y código actual para publicar el MVP. No confundir la memoria documental con una habilidad instalada: `kume-infra` quedó preparada localmente pero su instalación en la cuenta no se completó. Esta memoria en GitHub es el registro persistente y accesible entre sesiones.
