#!/usr/bin/env bash
# Administración local de KUME. Ejecutar como usuario de despliegue, sin sudo global.
set -euo pipefail

show_states() {
  python3 - "$1" "$2" "$3" <<'PY'
import json
import re
import sys
from pathlib import Path

control, backend, webroot = map(Path, sys.argv[1:])
release_id = re.compile(r"[0-9a-f]{40}-[1-9][0-9]*-[1-9][0-9]*")
failed = False
for label, filename in (("Frontend", control / "state.json"), ("Backend", backend / "state.json")):
    print(f"\n{label}: {filename}")
    try:
        if filename.stat().st_size > 1024 * 1024:
            raise ValueError("Archivo de estado excesivo")
        state = json.loads(filename.read_text(encoding="utf-8"))
        current, previous = state["current"], state["previous"]
        for identifier in (current, previous):
            if identifier is not None and (not isinstance(identifier, str) or not release_id.fullmatch(identifier)):
                raise ValueError("Identificador de release inválido")
        pending = state["pending"] is not None
        print(json.dumps({"current": current, "previous": previous, "pending": {"present": True} if pending else None}, indent=2))
        if pending or current is None:
            raise ValueError("Sin release actual o con transacción pendiente; revisar despliegue")
        if label == "Frontend":
            expected = webroot / "releases" / current / "site"
            link = webroot / "current"
            if not link.is_symlink() or link.readlink() != Path("releases") / current / "site":
                raise ValueError("El enlace current no coincide con el estado")
            if link.resolve() != expected or not expected.is_dir():
                raise ValueError("Falta la release o hay enlaces inesperados")
        elif not (backend / "releases" / current).is_dir():
            raise ValueError("No existe el directorio de la release backend")
        print("Registro y ruta de release coherentes; no es una comprobación de integridad ni de CI.")
    except (OSError, ValueError, KeyError, TypeError):
        print("Estado ausente, inválido, pendiente o incoherente. No se modificó ningún archivo.")
        failed = True
sys.exit(1 if failed else 0)
PY
}

show_paths() {
  printf 'Frontend: /srv/kume-frontend/releases (archivos estáticos)\n'
  printf 'Enlace activo: /srv/kume-frontend/current\n'
  if [[ -L /srv/kume-frontend/current ]]; then
    readlink -f -- /srv/kume-frontend/current || return
  else
    printf 'Todavía no hay enlace current.\n'
  fi
  printf 'Control del frontend: %s/.local/share/kume-frontend\n' "$HOME"
  printf 'Backend: %s/kume-backend/releases\n' "$HOME"
  printf 'Los archivos de estado se consultan con la opción estados.\n'
}

check_health() {
  printf 'Backend real: /health interno (un 503 es fallo de dependencia).\n'
  curl --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 10 \
    --max-filesize 65536 --write-out '\n%{http_code}' http://127.0.0.1:3001/health |
    python3 -c '
import json, sys
try:
    body, status = sys.stdin.read(65537).rsplit("\n", 1)
    if status != "200" or json.loads(body) != {"status": "ok", "database": "ok"}:
        raise ValueError("Salud no disponible")
    print("Backend: HTTP 200, status=ok, database=ok")
except (ValueError, TypeError):
    print("Backend: fallo HTTP, SQL o respuesta inesperada; cuerpo omitido", file=sys.stderr)
    sys.exit(1)
' || return
  printf '\nFrontend (solo HTTP; para contenido/integridad usar el despliegue):\n'
  curl --noproxy '*' --fail --silent --show-error --connect-timeout 5 --max-time 10 \
    --output /dev/null --write-out 'HTTP %{http_code} — %{content_type}\n' \
    http://127.0.0.1:8080/
}

show_container_user() {
  local listing
  listing=$(sudo docker ps --format '{{.Names}}') || return
  if [[ -z $listing ]]; then
    printf 'No hay contenedores activos.\n'
    return
  fi
  local -a containers=()
  mapfile -t containers <<<"$listing"
  local container
  local PS3=$'\nElegí un contenedor activo (0 para cancelar): '
  select container in "${containers[@]}" '(cancelar)'; do
    if [[ $REPLY == 0 || $container == '(cancelar)' ]]; then return; fi
    if [[ -z $container ]]; then
      printf 'Elegí un número de la lista.\n' >&2
      continue
    fi
    printf 'Usuario efectivo de docker exec id en %s (sin --user):\n' "$container"
    sudo docker exec "$container" id || return
    return
  done
  return 0
}

run_query() {
  case "$1" in
  memoria) free -h ;;
  disco) df -h / /srv ;;
  contenedores) sudo docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' ;;
  usuario) show_container_user ;;
  imagenes) sudo docker image ls --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}' ;;
  consumo) sudo docker stats --no-stream --format 'table {{.Name}}\t{{.MemUsage}}\t{{.CPUPerc}}' ;;
  espacio-docker) sudo docker system df ;;
  volumenes) sudo docker volume ls ;;
  redes) sudo docker network ls ;;
  rutas) show_paths ;;
  estados) show_states "$HOME/.local/share/kume-frontend" "$HOME/kume-backend" /srv/kume-frontend ;;
  servicios)
    systemctl --no-pager show kume-frontend.service nginx.service \
      -p Id -p LoadState -p ActiveState -p SubState -p UnitFileState
    ;;
  salud) check_health ;;
  puertos) ss -lnt ;;
  *)
    printf 'Opción desconocida. Usá --help.\n' >&2
    return 2
    ;;
  esac
}

run_migrations() {
  local script_directory
  script_directory=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd) || return
  python3 "$script_directory/oracle-migrations.py" "$@"
}

show_help() {
  cat <<'HELP'
Uso: bash oracle-admin.sh [opción]
Sin opción abre un menú. Las opciones existentes siguen siendo consultas.
Migraciones es un grupo separado con etapas y confirmaciones explícitas.

  memoria         RAM y swap (mirar available, no solo free)
  disco           Espacio de / y /srv
  contenedores    Activos y detenidos, imágenes, estado y puertos
  usuario         Elegir contenedor activo y consultar su identidad con id
  imagenes        Imágenes Docker locales, ID y tamaño
  consumo         Una muestra de RAM/CPU por contenedor activo
  espacio-docker  Imágenes, contenedores, volúmenes y caché; no limpia nada
  volumenes       Volúmenes Docker (presencia no prueba restauración)
  redes           Redes Docker
  rutas           Ubicación frontend/backend y enlace current
  estados         JSON filtrado y coherencia básica de rutas (no prueba CI)
  servicios       Servicio frontend y unidad nginx predeterminada
  salud           Backend interno y respuesta HTTP del frontend
  puertos         Puertos TCP en escucha
  migraciones     Gestión controlada: migraciones --help (requiere motor instalado)

Ejecutar como usuario de despliegue: Docker usa sudo por operación.
Las consultas existentes no leen secrets, entorno de contenedores o logs.
Migraciones usa configuración privada sin mostrar secretos; no restaura ni despliega. No ejecutar con sudo global.
Códigos: 0 consulta correcta; 1 comprobación de estado fallida; 2 uso inválido.
Otros comandos conservan sus códigos de error. En el menú se informa el fallo.
HELP
}

main() {
  if [[ ${1:-} == migraciones ]]; then
    shift
    run_migrations "$@"
    return
  fi
  if (($# > 1)); then
    show_help >&2
    return 2
  fi
  if [[ ${1:-} == --help || ${1:-} == -h ]]; then
    show_help
    return
  fi
  if ((EUID == 0)); then
    printf 'Ejecutá como usuario de despliegue, sin sudo global.\n' >&2
    return 2
  fi
  if (($# == 1)); then
    run_query "$1"
    return
  fi
  local option
  local PS3=$'\nElegí una consulta (0 para salir): '
  select option in memoria disco contenedores usuario imagenes consumo espacio-docker volumenes redes rutas estados servicios salud puertos migraciones salir; do
    if [[ $REPLY == 0 || $option == salir ]]; then return; fi
    if [[ -z $option ]]; then
      printf 'Elegí un número de la lista.\n' >&2
      continue
    fi
    if [[ $option == migraciones ]]; then
      run_migrations --help || printf 'No se pudo abrir la ayuda de migraciones.\n' >&2
      continue
    fi
    if run_query "$option"; then
      printf '\nConsulta terminada.\n'
    else
      local status=$?
      printf '\nConsulta fallida (código %s); no se aplicaron cambios de infraestructura.\n' "$status" >&2
    fi
  done
}

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then main "$@"; fi
