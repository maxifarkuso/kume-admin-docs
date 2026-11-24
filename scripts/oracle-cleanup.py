#!/usr/bin/env python3
"""Depuración de Kume en Oracle. Ejecutar como usuario de despliegue."""

import argparse
import fcntl
import json
import os
import re
import subprocess
from pathlib import Path


RELEASE = re.compile(r"[0-9a-f]{40}-[1-9][0-9]*-[1-9][0-9]*")
REVISION = re.compile(r"[0-9a-f]{40}")
CHECKOUTS = ("migrations-payment-records", "migrations-staff-001", "migrations-ec3a784")
SMOKE_API = "kume-infra-test-api-1"
DOCKER = ("sudo", "-n", "docker")


def capture(*args):
    return subprocess.check_output(args, text=True).strip()


def require_directory(path):
    if path.resolve() != path or not path.is_dir():
        raise ValueError(f"Directorio ausente o inesperado: {path}")


def read_releases(root, state_file):
    require_directory(root / "releases")
    state = json.loads(state_file.read_text(encoding="utf-8"))
    current, previous = state["current"], state["previous"]
    if state["pending"] is not None or current is None or current == previous:
        raise ValueError(f"Estado de despliegue incoherente o pendiente: {root}")
    retained = {release for release in (current, previous) if release is not None}
    for release in retained:
        if not isinstance(release, str) or not RELEASE.fullmatch(release):
            raise ValueError(f"Identificador de release inválido: {root}")
        require_directory(root / "releases" / release)
    return current, retained


def old_releases(root, retained):
    for path in sorted((root / "releases").iterdir()):
        if not RELEASE.fullmatch(path.name) or path.name in retained:
            continue
        require_directory(path)
        yield path


def old_images(current, retained):
    tags = {release.split("-")[0] for release in retained}
    protected = {
        capture(*DOCKER, "image", "inspect", "--format", "{{.Id}}", f"kume-backend:{tag}")
        for tag in tags
    }
    active = capture(*DOCKER, "inspect", "--format", "{{.Image}}", "kume-backend-api-1")
    expected = capture(*DOCKER, "image", "inspect", "--format", "{{.Id}}",
                       f"kume-backend:{current.split('-')[0]}")
    if active != expected:
        raise ValueError("La imagen del contenedor activo difiere de current.")
    rows = capture(*DOCKER, "image", "ls", "--no-trunc", "--format",
                   "{{.Repository}} {{.Tag}} {{.ID}}", "kume-backend")
    for row in rows.splitlines():
        repository, tag, image_id = row.split()
        if repository == "kume-backend" and REVISION.fullmatch(tag):
            if tag not in tags and image_id not in protected:
                yield f"{repository}:{tag}"


def migration_checkouts(backend):
    if capture(*DOCKER, "ps", "-aq", "--filter", "label=kume.migration"):
        raise ValueError("Hay contenedores de migración. Revisá sus operaciones antes de continuar.")
    for name in CHECKOUTS:
        path = backend / name
        if not path.exists() and not path.is_symlink():
            continue
        require_directory(path)
        require_directory(path / ".git")
        if capture("git", "-C", str(path), "status", "--porcelain",
                   "--untracked-files=all", "--ignored"):
            raise ValueError(f"El checkout contiene archivos locales o ignorados: {path}")
        yield path


def smoke_container():
    rows = capture(*DOCKER, "ps", "-a", "--filter", f"name=^/{SMOKE_API}$", "--format",
                   "{{.Names}} {{.State}} {{.Image}}")
    if rows:
        if rows != f"{SMOKE_API} exited node:22-bookworm-slim":
            raise ValueError("La API de prueba no coincide con el contenedor detenido documentado.")
        return SMOKE_API
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aplicar", action="store_true", help="ejecutar la limpieza")
    parser.add_argument("--migraciones", action="store_true",
                        help="incluir los tres checkouts temporales documentados")
    parser.add_argument("--smoke-test", action="store_true",
                        help="incluir el contenedor detenido de la API de prueba")
    options = parser.parse_args()

    if os.geteuid() == 0:
        raise ValueError("Ejecutá el script como usuario de despliegue, sin sudo global.")
    home = Path.home()
    backend = home / "kume-backend"
    frontend = Path("/srv/kume-frontend")
    admin = home / ".local/bin/kume-admin"

    with (backend / "deployment.lock").open("rb") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError("El lock del backend está ocupado.") from None

        frontend_state = home / ".local/share/kume-frontend/state.json"
        backend_state = backend / "state.json"
        current_fe, retained_fe = read_releases(frontend, frontend_state)
        current_be, retained_be = read_releases(backend, backend_state)
        site = frontend / "releases" / current_fe / "site"
        require_directory(site)
        if (frontend / "current").readlink() != site.relative_to(frontend):
            raise ValueError("El enlace activo del frontend difiere de current.")

        frontend_paths = list(old_releases(frontend, retained_fe))
        backend_paths = list(old_releases(backend, retained_be))
        images = list(old_images(current_be, retained_be))
        checkouts = list(migration_checkouts(backend)) if options.migraciones else []
        smoke = smoke_container() if options.smoke_test else None

        print("Aplicación" if options.aplicar else "Vista previa", flush=True)
        for item in [*frontend_paths, *backend_paths, *images, *checkouts]:
            print(f"Retirar {item}", flush=True)
        if smoke:
            print(f"Retirar {smoke}", flush=True)
        if not any((frontend_paths, backend_paths, images, checkouts, smoke)):
            print("Sin candidatos dentro del alcance seleccionado.", flush=True)
        subprocess.run([admin, "salud"], check=True)
        if not options.aplicar:
            return

        if (read_releases(frontend, frontend_state) != (current_fe, retained_fe)
                or read_releases(backend, backend_state) != (current_be, retained_be)
                or (frontend / "current").readlink() != site.relative_to(frontend)):
            raise ValueError("Cambió el estado del despliegue durante el inventario.")

        remove = ("rm", "-rf", "--one-file-system", "--")
        if frontend_paths:
            subprocess.run(["sudo", "-n", *remove, *frontend_paths], check=True)
        if backend_paths or checkouts:
            subprocess.run([*remove, *backend_paths, *checkouts], check=True)
        if images:
            subprocess.run([*DOCKER, "image", "rm", *images], check=True)
        if smoke:
            subprocess.run([*DOCKER, "rm", smoke], check=True)
        subprocess.run([admin, "salud"], check=True)
        subprocess.run([admin, "disco"], check=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Depuración interrumpida: {error}") from None
