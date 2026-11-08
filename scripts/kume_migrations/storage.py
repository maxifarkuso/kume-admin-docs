"""Private operational evidence and nonblocking coordination."""

import fcntl
import hashlib
import json
import os
import re
import stat
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone


class MigrationError(Exception):
    def __init__(self, message, code=1):
        super().__init__(message)
        self.code = code


def require(condition, message):
    if not condition:
        raise MigrationError(message)


def digest(path):
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def private_file(path):
    mode = path.lstat()
    require(
        stat.S_ISREG(mode.st_mode)
        and mode.st_uid == os.getuid()
        and mode.st_mode & 0o077 == 0,
        "Archivo privado ausente o inseguro",
    )


def private_directory(path):
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    mode = path.lstat()
    require(
        stat.S_ISDIR(mode.st_mode)
        and mode.st_uid == os.getuid()
        and mode.st_mode & 0o077 == 0,
        "Directorio operativo inseguro",
    )


def save_json(path, value):
    descriptor, name = tempfile.mkstemp(dir=path.parent, prefix=".journal-")
    try:
        with os.fdopen(descriptor, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def locks(root, deployment_lock):
    private_directory(root)
    descriptors = []
    try:
        for path, flags in (
            (root / "admin.lock", os.O_CREAT | os.O_RDWR),
            (deployment_lock, os.O_RDONLY),
        ):
            descriptor = os.open(path, flags | os.O_NOFOLLOW, 0o600)
            descriptors.append(descriptor)
            require(stat.S_ISREG(os.fstat(descriptor).st_mode), "Lock inválido")
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise MigrationError(
                    "Operación concurrente: lock ocupado", 75
                ) from error
        yield
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


class Journal:
    def __init__(self, root, operation, config):
        require(
            re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}", operation),
            "Identificador de operación inválido",
        )
        self.directory = root / operation
        private_directory(self.directory)
        self.path = self.directory / "journal.json"
        if self.path.exists():
            private_file(self.path)
            self.value = json.loads(self.path.read_text())
            require(self.value["config"] == config, "Configuración distinta al journal")
        else:
            self.value = {"config": config, "events": [], "artifacts": {}}

    def record(self, action, outcome, code=0):
        self.value["events"].append(
            {
                "action": action,
                "outcome": outcome,
                "code": code,
                "at": datetime.now(timezone.utc).isoformat(),
            }
        )
        save_json(self.path, self.value)

    def outcome(self, action):
        events = [event for event in self.value["events"] if event["action"] == action]
        return events[-1]["outcome"] if events else None

    def artifact(self, key, value):
        self.value["artifacts"][key] = value
        save_json(self.path, self.value)
