"""Composition root for the explicit migrations CLI."""

import argparse
import json
import os
import re
import signal
import sys
from pathlib import Path

from .runtime import Runtime
from .storage import Journal, MigrationError, locks, private_file, require
from .workflow import ACTIONS, Workflow

FIELDS = {
    "host",
    "backend",
    "postgres",
    "network",
    "server",
    "port",
    "database",
    "user",
    "revision",
    "repository",
    "checkout",
    "runtime_env",
    "backend_state",
    "frontend_state",
    "webroot",
    "deployment_lock",
    "verification_sql",
    "verification_sha256",
    "initial_migration",
    "initial_verification_sql",
    "initial_verification_sha256",
}
PATHS = {
    "checkout",
    "runtime_env",
    "backend_state",
    "frontend_state",
    "webroot",
    "deployment_lock",
    "verification_sql",
    "initial_verification_sql",
}


def load_config(path):
    private_file(path)
    config = json.loads(path.read_text())
    require(
        set(config) == FIELDS
        and all(isinstance(value, str) and value for value in config.values()),
        "Configuración incompleta o con campos desconocidos",
    )
    for key, value in config.items():
        require(
            not any(ord(char) < 32 for char in value),
            "Caracteres de control en configuración",
        )
        if key in PATHS:
            require(
                Path(value).is_absolute()
                and Path(value).resolve() == Path(value)
                and "," not in value,
                "Ruta absoluta canónica requerida",
            )
        elif key == "repository":
            require(
                re.fullmatch(
                    r"git@github\.com:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.git", value
                ),
                "Usar origen SSH configurado, sin tokens",
            )
        elif key == "revision":
            require(re.fullmatch(r"[0-9a-f]{40}", value), "SHA completo requerido")
        elif key in ("verification_sha256", "initial_verification_sha256"):
            require(
                re.fullmatch(r"[0-9a-f]{64}", value),
                "Checksum de verificación requerido",
            )
        else:
            require(
                re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", value),
                "Identificador de destino inválido",
            )
    require(config["port"] == "5432", "Esta entrega admite PostgreSQL interno en 5432")
    backend_root = Path(config["backend_state"]).parent
    require(
        Path(config["deployment_lock"]) == backend_root / "deployment.lock",
        "Lock no pertenece al backend",
    )
    require(
        not Path(config["checkout"]).is_relative_to(backend_root / "releases"),
        "Usar checkout separado de releases",
    )
    return config


def interrupted(signum, frame):
    raise KeyboardInterrupt


def main(arguments=None):
    parser = argparse.ArgumentParser(
        description="Migraciones explícitas; sin Oracle ni despliegues automáticos. Ver docs/devops/migraciones-admin.md."
    )
    parser.add_argument("action", choices=ACTIONS)
    parser.add_argument(
        "--config", type=Path, required=True, help="JSON privado del destino aprobado"
    )
    parser.add_argument(
        "--operacion",
        required=True,
        help="ID único; conservar para inspección y reanudación",
    )
    args = parser.parse_args(arguments)
    os.umask(0o077)
    signal.signal(signal.SIGTERM, interrupted)
    try:
        require(os.geteuid() != 0, "Ejecutar como usuario operativo, sin sudo global")
        config = load_config(args.config)
        root = Path.home() / ".local/share/kume-admin/migrations"
        with locks(root, Path(config["deployment_lock"])):
            journal = Journal(root, args.operacion, config)
            Workflow(Runtime(config, journal), journal).execute(args.action)
        return 0
    except MigrationError as error:
        print(str(error), file=sys.stderr)
        return error.code if error.code > 0 else 128 - error.code
    except KeyboardInterrupt:
        print(
            "Interrumpido: inspeccionar journal y destino antes de continuar",
            file=sys.stderr,
        )
        return 130
    except (OSError, ValueError, KeyError, TypeError, StopIteration):
        print(
            "Archivo, respuesta o configuración inválidos; detalles privados omitidos",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
