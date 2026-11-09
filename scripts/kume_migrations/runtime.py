"""Git, Docker and PostgreSQL adapters. Never forward raw collaborator output."""

import hashlib
import json
import os
import re
import shutil
import subprocess
from contextlib import nullcontext
from pathlib import Path

from .storage import MigrationError, digest, private_file, require

CONNECTION_SCRIPT = """const u = new URL(process.env.DATABASE_URL);
if (!['postgres:', 'postgresql:'].includes(u.protocol)) process.exit(2);
if ((u.searchParams.get('schema') || 'public') !== 'public' || u.searchParams.has('options')) process.exit(2);
console.log(JSON.stringify({server:u.hostname,port:u.port||'5432',
database:decodeURIComponent(u.pathname.slice(1)),user:decodeURIComponent(u.username)}));"""
HISTORY_SQL = """SELECT COALESCE(json_agg(row_to_json(m)), '[]'::json)::text FROM
(SELECT migration_name, checksum, finished_at IS NOT NULL AS finished,
 rolled_back_at IS NOT NULL AS rolled_back FROM public._prisma_migrations
 ORDER BY started_at, id) m;"""


class Commands:
    def run(
        self,
        arguments,
        *,
        input=None,
        output=None,
        input_file=None,
        accepted_codes=(0,),
    ):
        try:
            with input_file.open("rb") if input_file else nullcontext(None) as stream:
                result = subprocess.run(
                    arguments,
                    input=input,
                    stdin=stream,
                    stdout=output or subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=600,
                    check=False,
                )
        except subprocess.TimeoutExpired as error:
            raise MigrationError(
                "Tiempo agotado; inspeccionar resultado antes de continuar", 124
            ) from error
        if result.returncode not in accepted_codes:
            raise MigrationError(
                "Falló colaborador; salida privada omitida", result.returncode
            )
        return (result.stdout or b"").decode()


class Runtime:
    def __init__(self, config, journal, commands=None):
        self.config = config
        self.journal = journal
        self.commands = commands or Commands()

    def docker(self, *arguments, **kwargs):
        return self.commands.run(["sudo", "docker", *arguments], **kwargs)

    def inspect(self, container, template):
        return self.docker("inspect", "--format", template, container).strip()

    def git(self, *arguments):
        return self.commands.run(
            ["git", "-C", self.config["checkout"], *arguments]
        ).strip()

    def source(self):
        config = self.config
        require(
            self.git("rev-parse", "HEAD") == config["revision"],
            "Revisión de checkout incorrecta",
        )
        require(
            not self.git("status", "--porcelain", "--untracked-files=all"),
            "Checkout con cambios locales",
        )
        require(
            self.git("remote", "get-url", "origin") == config["repository"],
            "Origen no aprobado",
        )
        package = json.loads(self.git("show", "HEAD:package.json"))
        versions = [
            package.get(section, {}).get("prisma")
            for section in ("dependencies", "devDependencies")
        ]
        require(
            "6.19.0" in versions and all(v in (None, "6.19.0") for v in versions),
            "El proyecto no fija Prisma 6.19.0",
        )
        paths = self.git("ls-tree", "-r", "HEAD", "--", "prisma").splitlines()
        checksums = {}
        for line in paths:
            metadata, name = line.split("\t")
            require(
                metadata.startswith("100644 blob ")
                or metadata.startswith("100755 blob "),
                "Prisma contiene enlaces o entradas no regulares",
            )
            require(
                re.fullmatch(r"prisma/[A-Za-z0-9_./-]+", name)
                and ".." not in Path(name).parts,
                "Ruta Prisma inválida",
            )
            content = self.commands.run(
                ["git", "-C", config["checkout"], "show", f"HEAD:{name}"]
            )
            checksums[name] = hashlib.sha256(content.encode()).hexdigest()
        require("prisma/schema.prisma" in checksums, "Falta schema.prisma")
        migrations = {
            Path(name).parent.name: checksum
            for name, checksum in checksums.items()
            if re.fullmatch(r"prisma/migrations/[A-Za-z0-9_-]+/migration.sql", name)
        }
        require(migrations, "Sin migraciones aprobadas")
        return checksums, dict(sorted(migrations.items()))

    def snapshot(self):
        checksums, migrations = self.source()
        root = self.journal.directory / "source"
        root.mkdir(mode=0o700)
        for name, checksum in checksums.items():
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            content = self.commands.run(
                ["git", "-C", self.config["checkout"], "show", f"HEAD:{name}"]
            )
            target.write_text(content)
            target.chmod(0o600)
            require(digest(target) == checksum, "Snapshot no coincide")
        self.journal.artifact("source", checksums)
        self.journal.artifact("migrations", migrations)

    def check_snapshot(self):
        checksums, migrations = self.source()
        require(
            checksums == self.journal.value["artifacts"].get("source"), "Fuente cambió"
        )
        for name, checksum in checksums.items():
            path = self.journal.directory / "source" / name
            private_file(path)
            require(digest(path) == checksum, "Snapshot alterado")
        return migrations

    def connection(self, container):
        identity = json.loads(
            self.docker("exec", container, "node", "-e", CONNECTION_SCRIPT)
        )
        expected = {
            key: self.config[key] for key in ("server", "port", "database", "user")
        }
        require(identity == expected, "Conexión no coincide con destino aprobado")
        address = self.docker(
            "exec",
            container,
            "node",
            "-e",
            "require('dns').lookup(process.argv[1],{family:4},(e,a)=>{if(e)process.exit(1);console.log(a)})",
            self.config["server"],
        ).strip()
        database_address = self.inspect(
            self.config["postgres"],
            '{{(index .NetworkSettings.Networks "'
            + self.config["network"]
            + '").IPAddress}}',
        )
        require(
            address == database_address and address,
            "DNS no apunta a PostgreSQL aprobado",
        )

    def preflight(self):
        config = self.config
        require(os.uname().nodename == config["host"], "Host incorrecto")
        private_file(Path(config["runtime_env"]))
        self._verification_query("verification_sql", "verification_sha256")
        self._verification_query(
            "initial_verification_sql", "initial_verification_sha256"
        )
        for key in ("backend_state", "frontend_state"):
            state = json.loads(Path(config[key]).read_text())
            require(
                state["pending"] is None
                and re.fullmatch(
                    r"[0-9a-f]{40}-[1-9][0-9]*-[1-9][0-9]*", state["current"]
                ),
                "Estado pendiente o inválido",
            )
        backend_state = json.loads(Path(config["backend_state"]).read_text())
        backend_root = Path(config["backend_state"]).parent
        require(
            (backend_root / "releases" / backend_state["current"]).is_dir(),
            "Release backend ausente",
        )
        frontend_state = json.loads(Path(config["frontend_state"]).read_text())
        webroot = Path(config["webroot"])
        link = webroot / "current"
        require(
            link.is_symlink()
            and link.readlink() == Path("releases") / frontend_state["current"] / "site"
            and link.resolve()
            == webroot / "releases" / frontend_state["current"] / "site"
            and link.is_dir(),
            "Release frontend incoherente",
        )
        require(
            self.inspect(config["backend"], "{{.State.Running}}") == "true",
            "Backend inactivo",
        )
        require(
            self.inspect(config["postgres"], "{{.State.Health.Status}}") == "healthy",
            "PostgreSQL no saludable",
        )
        image = self.inspect(config["backend"], "{{.Image}}")
        require(re.fullmatch(r"sha256:[0-9a-f]{64}", image), "Imagen local inválida")
        self.docker("image", "inspect", "--format", "{{.Id}}", image)
        self.connection(config["backend"])
        node = self.docker("exec", config["backend"], "node", "--version").strip()
        npm = self.docker("exec", config["backend"], "npm", "--version").strip()
        require(
            re.fullmatch(r"v(18|20|22|24)\.\d+\.\d+", node)
            and re.fullmatch(r"(9|10|11)\.\d+\.\d+", npm),
            "Node/npm sin compatibilidad admitida",
        )
        available = next(
            int(line.split()[1])
            for line in Path("/proc/meminfo").read_text().splitlines()
            if line.startswith("MemAvailable:")
        )
        require(available >= 512 * 1024, "RAM disponible insuficiente (mínimo 512 MiB)")
        require(
            shutil.disk_usage(self.journal.directory).free >= 1024**3,
            "Espacio libre insuficiente (mínimo 1 GiB)",
        )
        self.source()
        identity = {
            "backend": self.inspect(config["backend"], "{{.Id}}"),
            "postgres": self.inspect(config["postgres"], "{{.Id}}"),
            "backend_release": backend_state["current"],
            "frontend_release": frontend_state["current"],
            "postgres_system": self.sql(
                "SELECT system_identifier::text FROM pg_control_system();"
            ),
        }
        require(
            re.fullmatch(r"[0-9]+", identity["postgres_system"]),
            "Identidad PostgreSQL inválida",
        )
        recorded = self.journal.value["artifacts"].get("identity")
        require(
            recorded is None or recorded == identity,
            "Destino o releases cambiaron desde preparación",
        )
        return {
            "image": image,
            "node": node,
            "npm": npm,
            "prisma": "6.19.0",
            "identity": identity,
        }

    def prepare(self):
        versions = self.preflight()
        self.snapshot()
        self.journal.artifact("identity", versions["identity"])
        name = "kume-migrations-" + self.journal.directory.name
        self.journal.artifact("container_name", name)
        container = self.docker(
            "run",
            "--detach",
            "--rm",
            "--name",
            name,
            "--label",
            "kume.migration=" + self.journal.directory.name,
            "--pull=never",
            "--memory=384m",
            "--memory-swap=384m",
            "--network",
            self.config["network"],
            "--env-file",
            self.config["runtime_env"],
            "--mount",
            f"type=bind,src={self.journal.directory}/source/prisma,dst=/migration,readonly",
            "--entrypoint",
            "sleep",
            versions["image"],
            "infinity",
        ).strip()
        require(re.fullmatch(r"[0-9a-f]{64}", container), "ID temporal inválido")
        self.journal.artifact("container", container)
        self.journal.artifact("versions", versions)
        self.connection(container)
        self.docker(
            "exec",
            container,
            "npm",
            "install",
            "--prefix",
            "/tmp/kume-prisma",
            "--ignore-scripts",
            "--no-audit",
            "--no-fund",
            "--save-exact",
            "prisma@6.19.0",
        )
        # npm 11.17 prints normal help with status 1. Accept that status only
        # for this read-only probe, and require recognizable command help.
        capabilities = self.docker(
            "exec", container, "npm", "--help", accepted_codes=(0, 1)
        )
        require(
            re.search(r"\bnpm\s+<command>", capabilities)
            and all(
                re.search(r"\b" + command + r"\b", capabilities)
                for command in ("install", "rebuild")
            ),
            "Ayuda npm no reconocida; preparación detenida",
        )
        if re.search(r"\bapprove-scripts\b", capabilities):
            self.docker(
                "exec",
                container,
                "npm",
                "--prefix",
                "/tmp/kume-prisma",
                "approve-scripts",
                "prisma@6.19.0",
                "@prisma/engines@6.19.0",
            )
        self.docker(
            "exec",
            container,
            "npm",
            "--prefix",
            "/tmp/kume-prisma",
            "rebuild",
            "prisma",
            "@prisma/engines",
            "--ignore-scripts=false",
            "--foreground-scripts",
        )
        version = self.prisma("--version")
        require(
            re.search(r"prisma\s*:\s*6\.19\.0(?:\s|$)", version),
            "Versión efectiva Prisma incorrecta",
        )

    def container(self):
        artifacts = self.journal.value["artifacts"]
        container = artifacts.get("container")
        # A crash after docker run may precede persistence of its ID: inspect name,
        # but trust it only after checking the operation label.
        candidate = container or artifacts.get("container_name")
        require(candidate, "No hay contenedor propio registrado")
        actual = self.inspect(candidate, "{{.Id}}")
        require(not container or actual == container, "Identidad temporal cambió")
        label = self.inspect(candidate, '{{index .Config.Labels "kume.migration"}}')
        require(
            label == self.journal.directory.name, "Contenedor ajeno: retirada rechazada"
        )
        return actual

    def prisma(self, *arguments):
        return self.docker(
            "exec",
            self.container(),
            "/tmp/kume-prisma/node_modules/.bin/prisma",
            *arguments,
        )

    def sql(self, statement):
        return self.docker(
            "exec",
            "-i",
            self.config["postgres"],
            "psql",
            "-X",
            "-v",
            "ON_ERROR_STOP=1",
            "-U",
            self.config["user"],
            "-d",
            self.config["database"],
            "-Atq",
            input=statement.encode(),
        ).strip()

    def history(self):
        exists = self.sql(
            "SELECT to_regclass('public._prisma_migrations') IS NOT NULL;"
        )
        require(exists in ("t", "f"), "Respuesta SQL inválida")
        return json.loads(self.sql(HISTORY_SQL)) if exists == "t" else []

    def tables(self):
        return self.sql(
            "SELECT count(*) FROM pg_tables WHERE schemaname='public' AND tablename <> '_prisma_migrations';"
        )

    def backup(self):
        estimate = int(self.sql("SELECT pg_database_size(current_database());"))
        require(
            shutil.disk_usage(self.journal.directory).free
            >= estimate * 2 + 256 * 1024**2,
            "Espacio insuficiente para respaldo",
        )
        path = self.journal.directory / "pre-migration.dump"
        with path.open("xb") as stream:
            path.chmod(0o600)
            self.docker(
                "exec",
                self.config["postgres"],
                "pg_dump",
                "-Fc",
                "-U",
                self.config["user"],
                "-d",
                self.config["database"],
                output=stream,
            )
            stream.flush()
            os.fsync(stream.fileno())
        require(path.stat().st_size > 0, "Respaldo vacío")
        self.check_backup_index(path)
        self.journal.artifact(
            "backup",
            {
                "path": str(path),
                "sha256": digest(path),
                "index_readable": True,
                "restoration_verified": False,
            },
        )

    def check_backup_index(self, path):
        private_file(path)
        self.docker(
            "exec",
            "-i",
            self.config["postgres"],
            "pg_restore",
            "--list",
            input_file=path,
        )

    def check_backup(self):
        backup = self.journal.value["artifacts"].get("backup")
        require(backup and backup["index_readable"], "Falta respaldo comprobado")
        path = Path(backup["path"])
        require(
            path == self.journal.directory / "pre-migration.dump",
            "Ruta respaldo inválida",
        )
        private_file(path)
        require(digest(path) == backup["sha256"], "Respaldo alterado")
        self.check_backup_index(path)

    def verify(self):
        self._verify_file("verification_sql", "verification_sha256")

    def verify_initial(self):
        self._verify_file("initial_verification_sql", "initial_verification_sha256")

    def _verification_query(self, path_key, checksum_key):
        path = Path(self.config[path_key])
        private_file(path)
        require(digest(path) == self.config[checksum_key], "Verificación no aprobada")
        query = path.read_text()
        # psql meta-commands can escape the read-only server transaction.
        require(
            "\\" not in query
            and ";" not in query.strip().rstrip(";")
            and query.lstrip().upper().startswith("SELECT "),
            "Verificación requiere un único SELECT sin metacomandos",
        )
        return query

    def _verify_file(self, path_key, checksum_key):
        query = self._verification_query(path_key, checksum_key)
        result = self.docker(
            "exec",
            "-i",
            "--env",
            "PGOPTIONS=-c default_transaction_read_only=on",
            self.config["postgres"],
            "psql",
            "-X",
            "-v",
            "ON_ERROR_STOP=1",
            "-Atq",
            "-U",
            self.config["user"],
            "-d",
            self.config["database"],
            input=(
                "BEGIN READ ONLY;\n" + query.strip().rstrip(";") + "\n;\nROLLBACK;\n"
            ).encode(),
        ).strip()
        require(result == "ok", "Verificación no satisfactoria")

    def remove(self):
        self.docker("stop", self.container())
