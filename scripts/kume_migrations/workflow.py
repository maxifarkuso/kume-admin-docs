"""Migration stage policy; runtime effects are supplied by a collaborator."""

import json
import sys

from .storage import MigrationError, private_file, require

ACTIONS = (
    "diagnostico",
    "preparar",
    "respaldo",
    "estado",
    "aplicar",
    "inicializar",
    "registrar-inicializacion",
    "verificar",
    "retirar",
    "habilitar-reintento",
)
WRITES = {"aplicar", "inicializar", "registrar-inicializacion"}


def check_history(history, migrations):
    applied = []
    for row in history:
        name = row["migration_name"]
        require(
            name in migrations and row["checksum"] == migrations[name],
            "Historial divergente",
        )
        require(
            row["finished"] and not row["rolled_back"],
            "Historial fallido o recuperado: inspección manual requerida",
        )
        require(name not in applied, "Historial duplicado")
        applied.append(name)
    require(applied == list(migrations)[: len(applied)], "Historial fuera de secuencia")
    return list(migrations)[len(applied) :]


class Workflow:
    def __init__(self, runtime, journal, confirm=input):
        self.runtime = runtime
        self.journal = journal
        self.confirm = confirm

    def confirmation(self, action):
        config = self.runtime.config
        summary = {
            key: config[key]
            for key in (
                "host",
                "backend",
                "postgres",
                "server",
                "port",
                "database",
                "user",
                "revision",
            )
        }
        print(summary)
        print(
            "Ventana requerida: despliegues y escrituras suspendidos externamente; el lock no coordina actores que lo ignoren."
        )
        print(
            "Respaldo:",
            self.journal.value["artifacts"].get("backup", "todavía no creado"),
        )
        print(
            "Migraciones aprobadas (SHA-256):",
            self.journal.value["artifacts"].get("migrations", {}),
        )
        print(
            "Herramientas:",
            self.journal.value["artifacts"].get("versions", "sin preparar"),
        )
        print(
            "UID/GID de ejecución Prisma:",
            self.journal.value["artifacts"].get("tool_exec_user", "sin comprobar"),
        )
        if action == "inicializar":
            print(
                "SQL excepcional:",
                config["initial_migration"],
                self.journal.value["artifacts"]
                .get("migrations", {})
                .get(config["initial_migration"]),
            )
        phrase = f"{action} {config['host']} {config['database']} {config['revision']} ventana-coordinada"
        try:
            answer = self.confirm("Confirmá escribiendo exactamente: " + phrase + "\n")
        except EOFError:
            answer = ""
        if answer != phrase:
            raise MigrationError("Operación cancelada", 130)

    def execute(self, action):
        require(action in ACTIONS, "Etapa desconocida")
        if action in ("diagnostico", "estado"):
            self.inspect()
            return
        if action == "retirar":
            self.confirmation(action)
            self.stage(action, self.runtime.remove)
            return
        if action == "preparar":
            require(
                self.journal.outcome(action) is None,
                "Preparación previa: inspeccionar y retirar; usar nueva operación",
            )
            self.runtime.preflight()
            self.confirmation(action)
            self.stage(action, self.runtime.prepare)
            return
        require(
            self.journal.outcome("preparar") == "success", "Herramientas no preparadas"
        )
        self.runtime.preflight()
        migrations = self.runtime.check_snapshot()
        self.runtime.connection(self.runtime.container())
        self.runtime.check_tool_access()
        if action == "habilitar-reintento":
            self.authorize_retry(migrations)
            return
        if action == "respaldo":
            require(
                self.journal.outcome(action) is None,
                "Respaldo previo: conservar evidencia; usar nueva operación",
            )
            require(
                not any(self.journal.outcome(step) for step in WRITES),
                "No reemplazar respaldo después de SQL",
            )
            self.confirmation(action)
            self.stage(action, self.runtime.backup)
            return
        if action == "verificar":
            verifier = self.runtime.verify
            if (
                self.journal.outcome("inicializar")
                and self.journal.outcome("registrar-inicializacion") != "success"
            ):
                verifier = self.runtime.verify_initial
            self.stage(action, verifier)
            return
        self.write(action, migrations)

    def stage(self, action, operation):
        self.journal.record(action, "running")
        try:
            operation()
        except BaseException as error:
            code = (
                error.code
                if isinstance(error, MigrationError)
                else 130
                if isinstance(error, KeyboardInterrupt)
                else 1
            )
            try:
                self.journal.record(
                    action, "uncertain" if action in WRITES else "failed", code
                )
            except OSError:
                print(
                    "No se pudo persistir el resultado; conservar running como incierto",
                    file=sys.stderr,
                )
            raise
        self.journal.record(action, "success")
        print("Etapa completada:", action)

    def inspect(self):
        self.runtime.preflight()
        _, migrations = self.runtime.source()
        pending = check_history(self.runtime.history(), migrations)
        print("Migraciones aprobadas pendientes:", pending)
        print("Tablas públicas:", self.runtime.tables())
        print("Etapas registradas:", self.journal.value["events"])
        print(
            "Un estado running/uncertain exige inspección; no acredita fallo ni autoriza reintento."
        )

    def write(self, action, migrations):
        self.check_other_operations()
        if action == "aplicar" and self.journal.outcome(action) == "success":
            require(
                not check_history(self.runtime.history(), migrations),
                "Historial cambió después del deploy",
            )
            print("Sin migraciones pendientes; no se repitió la escritura")
            return
        retry = action == "aplicar" and self.retry_authorized()
        require(
            self.journal.outcome(action) is None or retry,
            "Etapa ya intentada: inspeccionar, sin repetir escritura",
        )
        require(
            self.journal.outcome("aplicar") is None or retry,
            "Deploy previo: se requiere inspección explícita antes de reintentar",
        )
        require(
            self.journal.outcome("registrar-inicializacion")
            not in ("running", "uncertain", "failed"),
            "Registro incierto: inspección manual requerida",
        )
        self.runtime.check_backup()
        pending = check_history(self.runtime.history(), migrations)
        if action == "aplicar":
            if self.journal.outcome("inicializar"):
                require(
                    self.journal.outcome("registrar-inicializacion") == "success",
                    "Inicialización sin registrar",
                )
            require(
                self.runtime.history() or self.runtime.tables() == "0",
                "Base preexistente: requiere inicialización excepcional",
            )
            require(pending, "Sin migraciones pendientes; no se ejecutó deploy")
        elif action == "inicializar":
            require(
                not self.runtime.history() and int(self.runtime.tables()) > 0,
                "Inicialización requiere base preexistente sin historial",
            )
            require(
                self.runtime.config["initial_migration"] == next(iter(migrations)),
                "Debe inicializar la primera migración aprobada",
            )
        elif action == "registrar-inicializacion":
            require(
                self.journal.outcome("inicializar")
                in ("success", "running", "uncertain"),
                "Falta evidencia de ejecución SQL",
            )
            require(
                self.journal.outcome("verificar") == "success",
                "Falta verificación explícita posterior al SQL",
            )
            initial_events = [
                i
                for i, event in enumerate(self.journal.value["events"])
                if event["action"] == "inicializar"
            ]
            verification_events = [
                i
                for i, event in enumerate(self.journal.value["events"])
                if event["action"] == "verificar" and event["outcome"] == "success"
            ]
            require(
                max(verification_events) > max(initial_events),
                "Verificación anterior al SQL",
            )
            require(
                not self.runtime.history(), "Existe historial; no registrar a ciegas"
            )
        self.confirmation(action)
        # Confirmations may be slow: inspect again under the same deployment lock.
        self.runtime.preflight()
        self.runtime.check_snapshot()
        self.runtime.connection(self.runtime.container())
        self.runtime.check_backup()
        require(
            check_history(self.runtime.history(), migrations) == pending,
            "Historial cambió durante confirmación",
        )
        self.runtime.check_tool_access()
        if retry:
            evidence = self.journal.value["artifacts"]["retry"]
            require(
                pending == evidence["pending"],
                "Historial distinto a la inspección de recuperación",
            )
            self.runtime.verify_retry((evidence["path"], evidence["sha256"]))
        if action == "registrar-inicializacion":
            self.runtime.verify_initial()
        self.stage(action, lambda: self.apply(action))

    def retry_authorized(self):
        if (
            self.journal.outcome("aplicar") != "uncertain"
            or self.journal.outcome("habilitar-reintento") != "success"
        ):
            return False
        events = self.journal.value["events"]
        last_apply = max(
            i for i, event in enumerate(events) if event["action"] == "aplicar"
        )
        last_retry = max(
            i
            for i, event in enumerate(events)
            if event["action"] == "habilitar-reintento"
        )
        evidence = self.journal.value["artifacts"].get("retry", {})
        return last_retry > last_apply and evidence.get("apply_event") == last_apply

    def authorize_retry(self, migrations):
        require(
            self.journal.outcome("aplicar") == "uncertain",
            "Solo un deploy incierto admite esta inspección",
        )
        require(
            not any(
                self.journal.outcome(action)
                for action in ("inicializar", "registrar-inicializacion")
            ),
            "La recuperación excepcional no habilita este reintento",
        )
        require(self.runtime.inspection is not None, "Falta inspección SQL aprobada")
        self.check_other_operations()
        self.runtime.check_backup()
        pending = check_history(self.runtime.history(), migrations)
        require(
            pending,
            "Sin pendientes: verificar el deploy ya aplicado, no habilitar reintento",
        )
        self.runtime.verify_retry()
        print("Inspección aprobada (ruta y SHA-256):", self.runtime.inspection)
        self.confirmation("habilitar-reintento")
        self.runtime.preflight()
        self.runtime.check_snapshot()
        self.runtime.connection(self.runtime.container())
        self.runtime.check_tool_access()
        self.runtime.check_backup()
        require(
            check_history(self.runtime.history(), migrations) == pending,
            "Historial cambió durante inspección",
        )
        self.runtime.verify_retry()
        events = self.journal.value["events"]
        last_apply = max(
            i for i, event in enumerate(events) if event["action"] == "aplicar"
        )
        path, checksum = self.runtime.inspection
        evidence = {
            "path": str(path),
            "sha256": checksum,
            "pending": pending,
            "apply_event": last_apply,
        }
        self.stage(
            "habilitar-reintento", lambda: self.journal.artifact("retry", evidence)
        )

    def check_other_operations(self):
        for path in self.journal.directory.parent.glob("*/journal.json"):
            if path == self.journal.path:
                continue
            private_file(path)
            evidence = json.loads(path.read_text())
            # All journals share a host-local root: unresolved writes conservatively
            # block even another configuration, until investigated by the operator.
            for action in WRITES:
                events = [
                    event for event in evidence["events"] if event["action"] == action
                ]
                if events and events[-1]["outcome"] in (
                    "running",
                    "uncertain",
                    "failed",
                ):
                    resolved = action == "inicializar" and any(
                        event["action"] == "registrar-inicializacion"
                        and event["outcome"] == "success"
                        for event in evidence["events"]
                    )
                    require(
                        resolved,
                        "Otra operación tiene escritura incierta: inspección manual requerida",
                    )

    def apply(self, action):
        schema = "--schema=/migration/schema.prisma"
        if action == "aplicar":
            self.runtime.prisma("migrate", "deploy", schema)
        elif action == "inicializar":
            name = self.runtime.config["initial_migration"]
            self.runtime.prisma(
                "db",
                "execute",
                schema,
                "--file=/migration/migrations/" + name + "/migration.sql",
            )
            self.runtime.verify_initial()
        else:
            self.runtime.prisma(
                "migrate",
                "resolve",
                "--applied",
                self.runtime.config["initial_migration"],
                schema,
            )
        migrations = self.journal.value["artifacts"]["migrations"]
        pending = check_history(self.runtime.history(), migrations)
        if action == "aplicar":
            require(not pending, "Deploy no dejó historial completo")
            self.runtime.verify()
        elif action == "registrar-inicializacion":
            require(
                self.runtime.config["initial_migration"] not in pending,
                "No se confirmó registro",
            )
