# Administración de consulta en Oracle

Script: [scripts/oracle-admin.sh](scripts/oracle-admin.sh).
Estado real reportado: [operación instalada](operacion-oracle.md).

Ejecutarlo en la VM como el usuario de despliegue, sin sudo global. Requiere Bash,
Python 3, curl, Docker y herramientas estándar que ya se comprobaron en Ubuntu.
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

No usar `curl | bash`. Para instalar una copia cómoda en la VM, primero revisar e
integrar el PR y obtener su revisión exacta; después copiar el archivo a una ruta
propia como ~/.local/bin/kume-admin. Ese paso se realiza guiado, no desde el script.
No hace falta actualizar el frontend/backend ni publicar otra release para usarlo.

## Consultas y comandos equivalentes

| Opción         | Qué consulta                                           | Comando principal                        |
| -------------- | ------------------------------------------------------ | ---------------------------------------- |
| memoria        | RAM y swap; mirar available, no solo free              | free -h                                  |
| disco          | Sistemas de archivos / y /srv                          | df -h / /srv                             |
| contenedores   | Todos los contenedores, incluso detenidos              | sudo docker ps -a con columnas filtradas |
| imagenes       | Imágenes, tag, ID local y tamaño                       | sudo docker image ls                     |
| consumo        | Una muestra de RAM/CPU por contenedor activo           | sudo docker stats --no-stream            |
| espacio-docker | Uso de imágenes, contenedores, volúmenes y caché       | sudo docker system df                    |
| volumenes      | Inventario de volúmenes                                | sudo docker volume ls                    |
| redes          | Inventario de redes                                    | sudo docker network ls                   |
| rutas          | Frontend estático, enlace current y backend            | readlink -f y rutas conocidas            |
| estados        | current/previous/pending y coherencia básica con rutas | Python leyendo JSON conocido             |
| servicios      | Servicio KUME y unidad nginx predeterminada            | systemctl show sin logs                  |
| salud          | SQL del backend y respuesta HTTP del frontend          | curl a loopback, con timeout             |
| puertos        | Listeners TCP                                          | ss -lnt                                  |

Los códigos de salida de las consultas se conservan. Uso inválido: 2.
Estado ausente/incoherente o pendiente: 1. El menú muestra fallos y permite seguir;
una consulta fallida no se convierte en una recuperación automática.

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
- Seis pruebas aisladas con estados sintéticos y Docker/HTTP simulados: correctas.
  Verifican filtrado, no mutación, rechazo de comandos, enlaces incoherentes,
  pending y fallos HTTP/SQL sin exposición de cuerpos.
- CI Oracle administration checks repite esas verificaciones sin secrets ni
  conexión a Oracle. Las herramientas de lint se descargan solo en el runner,
  con versiones y checksums fijados; no se instalan en la VM.

Estas pruebas no acreditan que el script haya sido instalado o ejecutado en Oracle.
