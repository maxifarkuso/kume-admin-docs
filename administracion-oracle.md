# Administración de consulta en Oracle

Script: [scripts/oracle-admin.sh](scripts/oracle-admin.sh).
Estado real reportado: [operación instalada](operacion-oracle.md).

Ejecutarlo en la VM como el usuario de despliegue, sin sudo global. Requiere Bash
4 o superior, Python 3.9 o superior, curl, Docker y herramientas estándar de Linux.
En Oracle se comprobaron Python 3.12.3 y curl 8.5.0.
Solo las consultas Docker usan sudo; no modifica permisos o pertenencia a grupos.

Desde un checkout de este repositorio fijado a una revisión revisada:

```bash
bash scripts/oracle-admin.sh
```

Abre un menú; elegí el número de una consulta, o 0 para salir. También admite una
consulta directa, sin menú:

```bash
bash scripts/oracle-admin.sh memoria
bash scripts/oracle-admin.sh estados
```

No usar `curl | bash`. La [instalación paso a paso](#instalación-comprobada-y-repetible)
se realiza por separado del script, con revisión y checksum. No hace falta actualizar
el frontend/backend ni publicar otra release para usarlo.

Habilidad versionada: [kume-admin](.agents/skills/kume-admin/SKILL.md). Guía al agente
para instalar o revalidar esta utilidad, incluyendo su adaptación a otra máquina.
La fuente propietaria de los comandos y evidencias sigue siendo este documento.

## Consultas y comandos equivalentes

| Opción         | Qué consulta                                             | Comando principal                          |
| -------------- | -------------------------------------------------------- | ------------------------------------------ |
| memoria        | RAM y swap; mirar available, no solo free                | free -h                                    |
| disco          | Sistemas de archivos / y /srv                            | df -h / /srv                               |
| contenedores   | Todos los contenedores, incluso detenidos                | sudo docker ps -a con columnas filtradas   |
| imagenes       | Imágenes, tag, ID local y tamaño                         | sudo docker image ls                       |
| usuario        | Seleccionar contenedor activo y consultar UID/GID/grupos | sudo docker ps y docker exec CONTENEDOR id |
| consumo        | Una muestra de RAM/CPU por contenedor activo             | sudo docker stats --no-stream              |
| espacio-docker | Uso de imágenes, contenedores, volúmenes y caché         | sudo docker system df                      |
| volumenes      | Inventario de volúmenes                                  | sudo docker volume ls                      |
| redes          | Inventario de redes                                      | sudo docker network ls                     |
| rutas          | Frontend estático, enlace current y backend              | readlink -f y rutas conocidas              |
| estados        | current/previous/pending y coherencia básica con rutas   | Python leyendo JSON conocido               |
| servicios      | Servicio KUME y unidad nginx predeterminada              | systemctl show sin logs                    |
| salud          | SQL del backend y respuesta HTTP del frontend            | curl a loopback, con timeout               |
| puertos        | Listeners TCP                                            | ss -lnt                                    |

Los códigos de salida de las consultas se conservan. Uso inválido: 2.
Estado ausente/incoherente o pendiente: 1. El menú muestra fallos y permite seguir;
una consulta fallida no se convierte en una recuperación automática.

## Usuario efectivo en un contenedor

```bash
kume-admin usuario
```

La opción obtiene los nombres de contenedores activos mediante docker ps y abre
un selector numérico; 0 o cancelar vuelve sin ejecutar nada. Luego ejecuta
únicamente sudo docker exec CONTENEDOR id, con el nombre seleccionado como
argumento, sin un shell intermedio ni un comando arbitrario.

id muestra UID, GID y grupos, incluidos nombres cuando la imagen puede resolverlos;
por ejemplo uid=1000(node). No usa --user para forzar root u otra identidad.
Es el usuario efectivo del nuevo proceso id, normalmente el usuario configurado
para exec; no demuestra el usuario del proceso principal si el entrypoint cambia
privilegios al arrancar. La opción crea ese proceso breve de consulta en el
contenedor, sin modificar archivos o configuración.

No incluye contenedores detenidos ni los arranca. Si el contenedor se detiene
entre listado y selección, o la imagen no incluye id, informa el error de Docker;
no reinicia, instala herramientas o cambia de usuario como alternativa.

Esta opción es posterior a la copia instalada inicialmente en Oracle. Actualizar
la utilidad desde una revisión aprobada con su checksum nuevo antes de usarla;
la instalación histórica documentada conserva su commit y huella originales.

## Rutas que utiliza

- Archivos estáticos: /srv/kume-frontend/releases; enlace /srv/kume-frontend/current.
- Estado del frontend: $HOME/.local/share/kume-frontend/state.json.
- Backend: $HOME/kume-backend/releases; estado $HOME/kume-backend/state.json.
- Backend real: http://127.0.0.1:3001/health.
- Frontend: http://127.0.0.1:8080/.

Son las ubicaciones del entorno de esta sesión. Si otro entorno utiliza rutas
alternativas, revisar el script antes de usarlo; no buscar automáticamente por
el disco ni abrir archivos privados para deducirlas. Ejecutar con sudo global
cambiaría HOME, por lo que el script lo rechaza.

## Qué permite comprobar y qué no

estados muestra únicamente IDs current/previous y si pending está presente.
No imprime campos adicionales o cuerpos de transacciones desconocidos. Revisa
que current del frontend sea el enlace relativo esperado, que exista su site y
que exista el directorio registrado para el backend. Es una lectura momentánea:
un pipeline en curso puede producir un estado pendiente o una discrepancia temporal.
No toma locks, crea archivos o modifica/reconcilia el estado.

El JSON registra una entrega, pero no prueba por sí solo su funcionamiento, su
checksum, la identidad de una imagen Docker o el resultado de GitHub Actions.
No reemplaza las verificaciones portables del backend por comparar tags/IDs entre
runner y Oracle. Para verificar publicación: revisar también ejecución Actions,
servicio, listeners y salud. La prueba de navegador por túnel es independiente.

salud acepta exclusivamente el JSON esperado del backend real con HTTP 200,
status ok y database ok; un 503 es fallo aunque el servidor responda. No imprime
cuerpos inesperados. Para frontend muestra estado HTTP y Content-Type, sin cuerpo
ni cookies: no comprueba todo el contenido de la landing o sus assets.

El script no inspecciona variables de contenedores, runtime.env, claves, logs o
configuraciones privadas. No incluye rm, prune, down, migraciones, rollback,
reinicios ni limpieza de imágenes. Espacio «reclaimable» no autoriza a borrarlo;
volumen presente no acredita restauración. No cambia red, servicios o credenciales.

## Comprobaciones del script

- bash -n, ShellCheck 0.10.0 y shfmt 3.12.0: correctos.
- Nueve pruebas aisladas con estados sintéticos y Docker/HTTP simulados: correctas.
  Incluyen selección por nombre, cancelación/EOF y errores de exec sin reintentos.
  Verifican filtrado, no mutación, rechazo de comandos, enlaces incoherentes,
  pending y fallos HTTP/SQL sin exposición de cuerpos.
- CI Oracle administration checks repite esas verificaciones sin secrets ni
  conexión a Oracle. Las herramientas de lint se descargan solo en el runner,
  con versiones y checksums fijados; no se instalan en la VM.

Las pruebas automatizadas anteriores son aisladas. Posteriormente Maxi instaló
la utilidad en Oracle y confirmó sus consultas reales y acceso desde una nueva
sesión; ver el procedimiento y la evidencia siguientes.

## Instalación comprobada y repetible

Estado: instalada y comprobada por Maxi en Oracle el 4 de noviembre de 2026.
Ejecutar un comando por vez en la terminal de la máquina destino, como usuario de
despliegue; explicar y esperar su resultado antes del siguiente. Mantener abierta
la sesión actual mientras se comprueba el acceso desde otra sesión.

### 1. Revisar destino y dependencias

En otra máquina, confirmar primero que se trate de Linux con Bash y las
herramientas requeridas. No instalar paquetes o conceder acceso Docker por
inferencia:

```bash
uname -s
```

```bash
command -v bash python3 curl sha256sum install free df ss systemctl sudo docker
```

Consultar versiones, no solo presencia, antes de usar un destino diferente:

```bash
python3 --version
```

```bash
curl --version
```

Confirmar Bash 4 o superior con bash --version. La referencia comprobada de curl
es 8.5.0; revisar la compatibilidad de sus opciones de tiempo/tamaño si se usa
otra versión, sin instalar o actualizar paquetes automáticamente.

Comprobar el destino evita reemplazar una instalación previa a ciegas:

```bash
ls -ld "$HOME/.local/bin" "$HOME/.local/bin/kume-admin"
```

En la instalación original no existían. Si ya existe el script, registrar su
huella y revisar diferencias antes de decidir una actualización; conservarlo.
Crear solo la carpeta propia, sin sudo:

```bash
install -d -m 0700 "$HOME/.local/bin"
```

### 2. Descargar la revisión aprobada, sin ejecutarla

Versión efectivamente instalada: commit de docs
`28d2460a0f75beac01bf7b02edec5b037e104054`, merge del
[PR #2](https://github.com/maxifarkuso/kume-admin-docs/pull/2).
Su SHA-256 de archivo es:

```text
5d3c4dcfb526d7679c31b4a1b830ea79868612e24daeca112f29fca3c1a294a8
```

La URL siguiente queda fijada a esa revisión; no descarga main mutable. En una
actualización futura usar la revisión revisada correspondiente y verificar su
huella esperada por separado; no reutilizar este checksum si el script cambió.
Si ya existe kume-admin.download de un intento anterior, revisarlo antes de
reemplazarlo.

```bash
curl --fail --location --connect-timeout 5 --max-time 30 \
  --output "$HOME/.local/bin/kume-admin.download" \
  https://raw.githubusercontent.com/maxifarkuso/kume-admin-docs/28d2460a0f75beac01bf7b02edec5b037e104054/scripts/oracle-admin.sh
```

### 3. Verificar e instalar la copia

```bash
sha256sum "$HOME/.local/bin/kume-admin.download"
```

Comparar la huella completa con la esperada; si difiere, detenerse sin ejecutar o
instalar el archivo. La instalación original coincidió. Como comprobación
adicional de sintaxis (no ejecuta el cuerpo):

```bash
bash -n "$HOME/.local/bin/kume-admin.download"
```

Copiar con permisos solo para el usuario actual, sin sudo:

```bash
install -m 0700 "$HOME/.local/bin/kume-admin.download" "$HOME/.local/bin/kume-admin"
```

Comprobar propietario y permisos, sin ampliar permisos del backend:

```bash
stat -c '%a %U:%G %n' "$HOME/.local/bin" "$HOME/.local/bin/kume-admin"
```

Esperado: 700 y usuario/grupo del operador; en Oracle, ubuntu:ubuntu.
Las comprobaciones adicionales de sintaxis y stat de este procedimiento son
recomendaciones reproducibles; no confundirlas con salidas aportadas durante la
instalación original, donde se verificaron checksum, ejecución y consultas.

### 4. Validar sin depender del PATH

Primero la ayuda, que no consulta Docker o los servicios:

```bash
"$HOME/.local/bin/kume-admin" --help
```

Después cada consulta por separado:

```bash
"$HOME/.local/bin/kume-admin" estados
```

```bash
"$HOME/.local/bin/kume-admin" salud
```

```bash
"$HOME/.local/bin/kume-admin" contenedores
```

No usar sudo global. Revisar cada salida: estados coherentes y sin pending,
salud HTTP/SQL correcta y contenedores esperados. Otras consultas pueden funcionar
aunque todavía falten servicios en una máquina nueva; no inventar un despliegue
ni crear state.json para silenciar ese fallo.

### 5. Habilitar el comando corto y comprobar persistencia de sesión

```bash
command -v kume-admin
```

La primera sesión de Oracle no lo encontró: la carpeta se había creado después
de iniciar sesión. Se agregó temporalmente al PATH, conservando sus entradas:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Esto solo afecta esa terminal; no modifica perfiles o servicios. Verificar el
comando corto y el menú:

```bash
command -v kume-admin
```

```bash
kume-admin
```

Antes de editar perfiles, inspeccionar si Ubuntu ya configura la carpeta:

```bash
grep -n -C 3 '\.local/bin' "$HOME/.profile" "$HOME/.bashrc"
```

En Oracle ya existía este bloque en ~/.profile:

```sh
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
```

No se editaron .profile o .bashrc ni se duplicó esa configuración. Se abrió una
**segunda conexión SSH**, sin cerrar la original, y se ejecutó:

```bash
command -v kume-admin
```

Resultado comprobado: /home/ubuntu/.local/bin/kume-admin. Eso verifica el PATH en
sesiones nuevas, no persistencia de los servicios tras reiniciar la máquina.
En otro sistema, si falta la configuración, identificar primero el shell y qué
perfil de login carga; agregar una única regla equivalente al perfil correcto,
revisando el contenido existente. No sobrescribir perfiles ni agregarla a varios
archivos a ciegas. No es necesario reiniciar la VM para esta comprobación.

## Resultado real y reproducción en otra máquina

Maxi confirmó ayuda, estados, salud, Docker, menú y posteriormente todas las
consultas. El frontend y backend tenían current definido y pending/previous null;
backend HTTP 200 con status/database ok; frontend HTTP 200 text/html.
PostgreSQL activo/healthy, backend activo y API temporal detenida y conservada.
Las imágenes Docker existentes se conservaron; una imagen guardada no es un
contenedor ejecutándose y puede compartir capas con otras versiones.

Para migrar esta **utilidad** a una máquina local:

1. Inventariar sistema operativo, usuario, permisos, shell, Docker y servicios.
2. Comparar las rutas/puertos de la sección «Rutas que utiliza» con el destino.
   El script actual tiene esas rutas y nombres de servicio fijados. No funcionará
   sin adaptación si el backend, webroot o puertos cambian.
3. Si hay diferencias, preparar un cambio revisado del script en este repositorio,
   ejecutar sus comprobaciones y obtener un nuevo commit/checksum antes de
   instalarlo. No editar el archivo verificado y seguir atribuyéndole su huella.
4. Repetir descarga, verificación, instalación y prueba en una sesión nueva.
5. Registrar por consulta qué quedó comprobado, ausente o pendiente en destino.

El script es para Linux; Windows nativo/PowerShell no ofrece las mismas
herramientas. WSL o una VM Linux solo son alternativas después de verificar
systemd, acceso a Docker, rutas y conectividad reales. No asumir equivalencia
con Oracle ni abrir puertos para compensar diferencias.

Instalar esta utilidad **no migra** base, archivos, cuentas, frontend/backend,
HTTPS, respaldos o datos. Para la migración completa seguir
[infraestructura y migración](infraestructura-y-migracion.md), que mantiene sus
propios requisitos, coordinación y pruebas de recuperación.

## Actualización y retirada

Una copia en ~/.local/bin no se actualiza al cambiar main en GitHub. Registrar
commit/checksum y validar cada nueva descarga antes de reemplazarla, conservando
la copia anterior cuando se actualice. Retirar esta utilidad consiste en retirar
su archivo, tras confirmarlo, sin tocar servicios o estados; no es necesario
limpiar Docker, reiniciar o volver a publicar la aplicación.
