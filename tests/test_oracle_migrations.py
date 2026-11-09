"""Controlled operational collaborators; no real PostgreSQL, Docker or Oracle."""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from kume_migrations.cli import load_config
from kume_migrations.runtime import Commands, Runtime
from kume_migrations.storage import Journal, MigrationError, locks, private_file
from kume_migrations.workflow import Workflow, check_history


class FakeRuntime:
    def __init__(self, journal):
        self.journal = journal
        self.config = journal.value["config"]
        self.calls = []
        self.rows = []
        self.table_count = "0"
        self.fail = None
        self.migrations = {"001_schema": "a" * 64, "002_seed": "b" * 64}

    def effect(self, name):
        self.calls.append(name)
        if self.fail == name:
            raise MigrationError("Colaborador fallido", 42)

    def preflight(self):
        self.effect("preflight")

    def source(self):
        return {}, self.migrations

    def prepare(self):
        self.effect("prepare")
        self.journal.artifact("migrations", self.migrations)

    def check_snapshot(self):
        self.effect("check_snapshot")
        return self.migrations

    def connection(self, container):
        self.effect("connection")

    def container(self):
        return "own-container"

    def backup(self):
        self.effect("backup")
        self.journal.artifact(
            "backup", {"index_readable": True, "restoration_verified": False}
        )

    def check_backup(self):
        self.effect("check_backup")
        if "backup" not in self.journal.value["artifacts"]:
            raise MigrationError("Sin respaldo")

    def history(self):
        return self.rows

    def tables(self):
        return self.table_count

    def verify(self):
        self.effect("verify")

    def verify_initial(self):
        self.effect("verify")

    def remove(self):
        self.effect("remove")

    def prisma(self, *args):
        name = args[1]
        self.effect(name)
        if name == "execute":
            self.table_count = "2"
        else:
            names = (
                list(self.migrations)
                if name == "deploy"
                else [self.config["initial_migration"]]
            )
            self.rows = [
                {
                    "migration_name": item,
                    "checksum": self.migrations[item],
                    "finished": True,
                    "rolled_back": False,
                }
                for item in names
            ]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.config = dict(
            host="test-host",
            backend="test-api",
            postgres="test-db",
            server="db",
            port="5432",
            database="fixture",
            user="fixture",
            revision="c" * 40,
            initial_migration="001_schema",
        )
        self.journal = Journal(self.root, "operation-one", self.config)
        self.runtime = FakeRuntime(self.journal)
        self.workflow = Workflow(
            self.runtime, self.journal, lambda prompt: prompt.split(": ", 1)[1].strip()
        )
        self.output = patch("builtins.print")
        self.output.start()
        self.addCleanup(self.output.stop)

    def prepared(self):
        self.workflow.execute("preparar")
        self.workflow.execute("respaldo")

    def test_cancel_and_eof_do_not_prepare_or_write(self):
        for response in (
            lambda prompt: "no",
            lambda prompt: (_ for _ in ()).throw(EOFError()),
        ):
            self.workflow.confirm = response
            with self.assertRaises(MigrationError) as error:
                self.workflow.execute("preparar")
            self.assertEqual(error.exception.code, 130)
            self.assertNotIn("prepare", self.runtime.calls)
            self.assertFalse(self.journal.path.exists())

    def test_wrong_target_and_resources_block_before_effects(self):
        self.runtime.fail = "preflight"
        with self.assertRaises(MigrationError):
            self.workflow.execute("preparar")
        self.assertNotIn("prepare", self.runtime.calls)

    def test_tools_failure_is_recorded_and_never_retried(self):
        self.runtime.fail = "prepare"
        with self.assertRaises(MigrationError) as error:
            self.workflow.execute("preparar")
        self.assertEqual(error.exception.code, 42)
        self.assertEqual(self.journal.outcome("preparar"), "failed")
        self.runtime.fail = None
        with self.assertRaises(MigrationError):
            self.workflow.execute("preparar")
        self.assertEqual(self.runtime.calls.count("prepare"), 1)

    def test_backup_failure_prevents_deploy_and_preserves_code(self):
        self.workflow.execute("preparar")
        self.runtime.fail = "backup"
        with self.assertRaises(MigrationError) as error:
            self.workflow.execute("respaldo")
        self.assertEqual(error.exception.code, 42)
        with self.assertRaises(MigrationError):
            self.workflow.execute("aplicar")
        self.assertNotIn("deploy", self.runtime.calls)

    def test_deploy_success_verification_and_second_call_without_writes(self):
        self.prepared()
        self.workflow.execute("aplicar")
        self.workflow.execute("aplicar")
        self.assertEqual(self.runtime.calls.count("deploy"), 1)
        self.assertIn("verify", self.runtime.calls)
        self.assertEqual(self.journal.outcome("aplicar"), "success")
        private_file(self.journal.path)
        self.assertFalse(
            self.journal.value["artifacts"]["backup"]["restoration_verified"]
        )

    def test_failed_deploy_is_uncertain_and_cannot_be_retried(self):
        self.prepared()
        self.runtime.fail = "deploy"
        with self.assertRaises(MigrationError) as error:
            self.workflow.execute("aplicar")
        self.assertEqual(error.exception.code, 42)
        self.assertEqual(self.journal.outcome("aplicar"), "uncertain")
        self.runtime.fail = None
        with self.assertRaises(MigrationError):
            self.workflow.execute("aplicar")
        self.assertEqual(self.runtime.calls.count("deploy"), 1)

    def test_crash_intent_survives_reload_and_blocks_new_operation(self):
        self.prepared()
        self.journal.record("aplicar", "running")
        loaded = Journal(self.root, "operation-one", self.config)
        self.assertEqual(loaded.outcome("aplicar"), "running")
        with self.assertRaises(MigrationError):
            Workflow(self.runtime, loaded).execute("aplicar")
        other = Journal(self.root, "operation-two", self.config)
        with self.assertRaises(MigrationError):
            Workflow(FakeRuntime(other), other).check_other_operations()
        self.assertNotIn("deploy", self.runtime.calls)

    def test_divergent_failed_or_out_of_order_history_blocks_sql(self):
        self.prepared()
        for row in (
            {
                "migration_name": "unknown",
                "checksum": "a" * 64,
                "finished": True,
                "rolled_back": False,
            },
            {
                "migration_name": "001_schema",
                "checksum": "x" * 64,
                "finished": True,
                "rolled_back": False,
            },
            {
                "migration_name": "001_schema",
                "checksum": "a" * 64,
                "finished": False,
                "rolled_back": False,
            },
            {
                "migration_name": "002_seed",
                "checksum": "b" * 64,
                "finished": True,
                "rolled_back": False,
            },
        ):
            self.runtime.rows = [row]
            with self.assertRaises(MigrationError):
                self.workflow.execute("aplicar")
        self.assertNotIn("deploy", self.runtime.calls)

    def test_exceptional_initialization_requires_sql_then_verification_then_resolve(
        self,
    ):
        self.prepared()
        self.runtime.table_count = "1"
        with self.assertRaises(MigrationError):
            self.workflow.execute("aplicar")
        with self.assertRaises(MigrationError):
            self.workflow.execute("registrar-inicializacion")
        self.workflow.execute("inicializar")
        with self.assertRaises(MigrationError):
            self.workflow.execute("registrar-inicializacion")
        self.workflow.execute("verificar")
        self.workflow.execute("registrar-inicializacion")
        self.workflow.execute("aplicar")
        self.assertLess(
            self.runtime.calls.index("execute"), self.runtime.calls.index("resolve")
        )
        self.assertLess(
            self.runtime.calls.index("resolve"), self.runtime.calls.index("deploy")
        )
        self.assertEqual(self.journal.outcome("aplicar"), "success")

    def test_interrupted_initial_sql_can_only_be_inspected_verified_and_registered(
        self,
    ):
        self.prepared()
        self.runtime.table_count = "1"
        self.runtime.fail = "verify"
        with self.assertRaises(MigrationError):
            self.workflow.execute("inicializar")
        self.assertEqual(self.journal.outcome("inicializar"), "uncertain")
        self.runtime.fail = None
        with self.assertRaises(MigrationError):
            self.workflow.execute("inicializar")
        self.workflow.execute("estado")
        self.workflow.execute("verificar")
        self.workflow.execute("registrar-inicializacion")
        self.assertEqual(self.runtime.calls.count("execute"), 1)
        self.assertEqual(self.runtime.calls.count("resolve"), 1)

    def test_interrupt_after_sql_records_uncertainty(self):
        self.prepared()
        with patch.object(self.runtime, "prisma", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.workflow.execute("aplicar")
        self.assertEqual(self.journal.outcome("aplicar"), "uncertain")

    def test_confirmation_revalidates_before_writing(self):
        self.prepared()

        def changed_destination(prompt):
            self.runtime.fail = "preflight"
            return prompt.split(": ", 1)[1].strip()

        self.workflow.confirm = changed_destination
        with self.assertRaises(MigrationError):
            self.workflow.execute("aplicar")
        self.assertNotIn("deploy", self.runtime.calls)

    def test_cleanup_available_after_tool_failure(self):
        self.runtime.fail = "prepare"
        with self.assertRaises(MigrationError):
            self.workflow.execute("preparar")
        self.runtime.fail = None
        self.workflow.execute("retirar")
        self.assertEqual(self.runtime.calls.count("remove"), 1)


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.journal = Journal(self.root, "fixture", {})
        self.runtime = Runtime({}, self.journal)

    def test_nonblocking_lock_excludes_second_process_and_does_not_create_deploy_lock(
        self,
    ):
        deployment = self.root / "deployment.lock"
        with self.assertRaises(FileNotFoundError):
            with locks(self.root, deployment):
                pass
        self.assertFalse(deployment.exists())
        deployment.touch(mode=0o600)
        with locks(self.root, deployment):
            with self.assertRaises(MigrationError) as error:
                with locks(self.root, deployment):
                    pass
            self.assertEqual(error.exception.code, 75)
        with locks(self.root, deployment):
            pass

    def test_cleanup_refuses_foreign_label_and_replaced_id(self):
        self.journal.artifact("container", "a" * 64)
        for results in (("b" * 64,), ("a" * 64, "foreign")):
            with (
                patch.object(self.runtime, "inspect", side_effect=results),
                patch.object(self.runtime, "docker") as docker,
            ):
                with self.assertRaises(MigrationError):
                    self.runtime.remove()
                docker.assert_not_called()
        with (
            patch.object(self.runtime, "inspect", side_effect=("a" * 64, "fixture")),
            patch.object(self.runtime, "docker") as docker,
        ):
            self.runtime.remove()
            docker.assert_called_once_with("stop", "a" * 64)

    def test_backup_corruption_blocks_index_and_use(self):
        path = self.journal.directory / "pre-migration.dump"
        path.write_bytes(b"fixture")
        path.chmod(0o600)
        self.journal.artifact(
            "backup", {"path": str(path), "sha256": "a" * 64, "index_readable": True}
        )
        with patch.object(self.runtime, "docker") as docker:
            with self.assertRaises(MigrationError):
                self.runtime.check_backup()
            docker.assert_not_called()

    def test_private_files_reject_symlinks_and_public_modes(self):
        path = self.root / "private"
        path.write_text("DO_NOT_PRINT")
        path.chmod(0o644)
        with self.assertRaises(MigrationError):
            private_file(path)
        path.chmod(0o600)
        private_file(path)
        alias = self.root / "alias"
        alias.symlink_to(path)
        with self.assertRaises(MigrationError):
            private_file(alias)

    def test_subprocess_failure_hides_secrets_and_preserves_exit(self):
        result = subprocess.CompletedProcess(
            [], 37, stdout=b"DO_NOT_PRINT", stderr=b"PASSWORD"
        )
        with patch("subprocess.run", return_value=result):
            with self.assertRaises(MigrationError) as error:
                Commands().run(["fixture"])
        self.assertEqual(error.exception.code, 37)
        self.assertNotIn("PASSWORD", str(error.exception))
        self.assertNotIn("DO_NOT_PRINT", str(error.exception))

    def test_connection_mismatch_blocks_before_dns_or_sql(self):
        self.runtime.config = dict(
            server="db", port="5432", database="fixture", user="fixture"
        )
        with patch.object(
            self.runtime,
            "docker",
            return_value=json.dumps(
                dict(server="other", port="5432", database="fixture", user="fixture")
            ),
        ) as docker:
            with self.assertRaises(MigrationError):
                self.runtime.connection("fixture")
            self.assertEqual(docker.call_count, 1)

    def test_unsafe_verification_is_rejected_before_sql(self):
        path = self.root / "verify.sql"
        for query in (
            "DELETE FROM fixture;",
            "SELECT 'ok'; DELETE FROM fixture;",
            "SELECT 'ok' \\! env",
        ):
            path.write_text(query)
            path.chmod(0o600)
            self.runtime.config = {
                "verification_sql": str(path),
                "verification_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            with patch.object(self.runtime, "docker") as docker:
                with self.assertRaises(MigrationError):
                    self.runtime.verify()
                docker.assert_not_called()

    def test_configuration_rejects_missing_and_secret_fields(self):
        path = self.root / "config.json"
        path.write_text(json.dumps({"DATABASE_URL": "DO_NOT_PRINT"}))
        path.chmod(0o600)
        with self.assertRaises(MigrationError):
            load_config(path)

    def test_empty_history_has_all_pending(self):
        self.assertEqual(check_history([], {"001": "a"}), ["001"])


class RuntimeBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.backend = self.root / "backend"
        self.frontend = self.root / "frontend"
        self.webroot = self.root / "webroot"
        release = "a" * 40 + "-1-1"
        (self.backend / "releases" / release).mkdir(parents=True)
        (self.frontend).mkdir()
        (self.webroot / "releases" / release / "site").mkdir(parents=True)
        (self.webroot / "current").symlink_to("releases/" + release + "/site")
        for directory in (self.backend, self.frontend):
            (directory / "state.json").write_text(
                json.dumps(dict(current=release, previous=None, pending=None))
            )
        environment = self.root / "runtime.env"
        environment.write_text("DO_NOT_PRINT=fixture")
        environment.chmod(0o600)
        self.config = dict(
            host=os.uname().nodename,
            backend="fixture-api",
            postgres="fixture-db",
            backend_state=str(self.backend / "state.json"),
            frontend_state=str(self.frontend / "state.json"),
            webroot=str(self.webroot),
            runtime_env=str(environment),
        )
        verifier = self.root / "verify.sql"
        verifier.write_text("SELECT 'ok';")
        verifier.chmod(0o600)
        checksum = hashlib.sha256(verifier.read_bytes()).hexdigest()
        self.config.update(
            verification_sql=str(verifier),
            verification_sha256=checksum,
            initial_verification_sql=str(verifier),
            initial_verification_sha256=checksum,
        )
        self.journal = Journal(self.root / "operations", "fixture", self.config)
        self.runtime = Runtime(self.config, self.journal)
        self.original_read = Path.read_text

    def preflight(self, *, memory=600000, free=2 * 1024**3):
        original = self.original_read

        def read(path, *args, **kwargs):
            if str(path) == "/proc/meminfo":
                return f"MemAvailable: {memory} kB\n"
            return original(path, *args, **kwargs)

        def inspect(container, template):
            if template == "{{.State.Running}}":
                return "true"
            if template == "{{.State.Health.Status}}":
                return "healthy"
            return "sha256:" + "a" * 64

        with (
            patch.object(self.runtime, "inspect", side_effect=inspect),
            patch.object(
                self.runtime,
                "docker",
                side_effect=("sha256:" + "a" * 64, "v22.1.0", "10.0.0"),
            ),
            patch.object(self.runtime, "connection"),
            patch.object(self.runtime, "source"),
            patch.object(self.runtime, "sql", return_value="123456"),
            patch.object(Path, "read_text", read),
            patch(
                "kume_migrations.runtime.shutil.disk_usage",
                return_value=type("Usage", (), {"free": free})(),
            ),
        ):
            return self.runtime.preflight()

    def test_resources_are_measured_and_insufficient_memory_or_disk_refused(self):
        for options in ({"memory": 100000}, {"free": 1024}):
            with self.subTest(options=options), self.assertRaises(MigrationError):
                self.preflight(**options)
        self.assertEqual(self.preflight()["prisma"], "6.19.0")

    def test_wrong_host_and_pending_deployment_refused(self):
        self.config["host"] = "another-host"
        with self.assertRaises(MigrationError):
            self.runtime.preflight()
        self.config["host"] = os.uname().nodename
        path = self.frontend / "state.json"
        state = json.loads(path.read_text())
        state["pending"] = {"private": "DO_NOT_PRINT"}
        path.write_text(json.dumps(state))
        with self.assertRaises(MigrationError) as error:
            self.runtime.preflight()
        self.assertNotIn("DO_NOT_PRINT", str(error.exception))

    def test_temporary_container_limits_and_old_npm_only_rebuild_selected_packages(
        self,
    ):
        self.config.update(network="fixture_default")
        self.journal.artifact("container", "a" * 64)

        def docker(*args, **kwargs):
            if args[0] == "run":
                return "a" * 64
            if "--help" in args:
                return "npm <command>\ninstall, rebuild, help"
            return ""

        with (
            patch.object(
                self.runtime,
                "preflight",
                return_value={"image": "sha256:" + "b" * 64, "identity": {}},
            ),
            patch.object(self.runtime, "snapshot"),
            patch.object(self.runtime, "connection"),
            patch.object(self.runtime, "docker", side_effect=docker) as commands,
            patch.object(self.runtime, "prisma", return_value="prisma : 6.19.0\n"),
        ):
            self.runtime.prepare()
        calls = [call.args for call in commands.call_args_list]
        run = calls[0]
        self.assertIn("--pull=never", run)
        self.assertIn("--memory=384m", run)
        self.assertIn("--memory-swap=384m", run)
        self.assertNotIn("--publish", run)
        self.assertFalse(any("docker.sock" in item for item in run))
        install = next(call for call in calls if "install" in call)
        self.assertIn("--ignore-scripts", install)
        rebuild = next(call for call in calls if "rebuild" in call)
        self.assertEqual(
            rebuild[
                rebuild.index("rebuild") + 1 : rebuild.index("--ignore-scripts=false")
            ],
            ("prisma", "@prisma/engines"),
        )

    def test_timeout_is_uncertain_error_without_output(self):
        with patch(
            "subprocess.run",
            side_effect=subprocess.TimeoutExpired(
                ["fixture"], 600, output=b"DO_NOT_PRINT"
            ),
        ):
            with self.assertRaises(MigrationError) as error:
                Commands().run(["fixture"])
        self.assertEqual(error.exception.code, 124)
        self.assertNotIn("DO_NOT_PRINT", str(error.exception))

    def test_snapshot_uses_commit_and_rejects_local_changes(self):
        repository = self.root / "repository"
        repository.mkdir()

        def git(*args):
            return subprocess.run(
                ["git", "-C", str(repository), *args],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

        git("init", "-q")
        git("config", "user.name", "Fixture")
        git("config", "user.email", "fixture@example.invalid")
        git("remote", "add", "origin", "git@github.com:example/fixture.git")
        (repository / "package.json").write_text(
            '{"devDependencies":{"prisma":"6.19.0"}}'
        )
        (repository / "prisma/migrations/001_schema").mkdir(parents=True)
        (repository / "prisma/schema.prisma").write_text("// fixture\n")
        sql = repository / "prisma/migrations/001_schema/migration.sql"
        sql.write_text("SELECT 1;\n")
        git("add", ".")
        git("commit", "-qm", "fixture")
        self.config.update(
            checkout=str(repository),
            repository="git@github.com:example/fixture.git",
            revision=git("rev-parse", "HEAD"),
        )
        self.runtime.snapshot()
        expected = hashlib.sha256(sql.read_bytes()).hexdigest()
        self.assertEqual(self.runtime.check_snapshot(), {"001_schema": expected})
        snapshot = (
            self.journal.directory / "source/prisma/migrations/001_schema/migration.sql"
        )
        snapshot.write_text("SELECT 2;\n")
        with self.assertRaises(MigrationError):
            self.runtime.check_snapshot()
        sql.write_text("SELECT 3;\n")
        with self.assertRaises(MigrationError):
            self.runtime.source()

    def test_changed_physical_destination_is_rejected_between_stages(self):
        identity = self.preflight()["identity"]
        self.journal.artifact("identity", {**identity, "postgres_system": "999"})
        with self.assertRaises(MigrationError):
            self.preflight()

    def test_verification_checksum_is_validated_before_any_database_operation(self):
        Path(self.config["verification_sql"]).write_text("SELECT 'changed';")
        with patch.object(self.runtime, "docker") as docker:
            with self.assertRaises(MigrationError):
                self.runtime.preflight()
            docker.assert_not_called()

    def test_npm_approval_is_restricted_to_two_exact_packages(self):
        self.config.update(network="fixture_default")

        def docker(*args, **kwargs):
            if args[0] == "run":
                return "a" * 64
            if "--help" in args:
                return "npm <command>\ninstall, rebuild, approve-scripts"
            return ""

        with (
            patch.object(
                self.runtime,
                "preflight",
                return_value={"image": "sha256:" + "b" * 64, "identity": {}},
            ),
            patch.object(self.runtime, "snapshot"),
            patch.object(self.runtime, "connection"),
            patch.object(self.runtime, "docker", side_effect=docker) as commands,
            patch.object(self.runtime, "prisma", return_value="prisma : 6.19.0\n"),
        ):
            self.runtime.prepare()
        approval = next(
            call.args
            for call in commands.call_args_list
            if "approve-scripts" in call.args
        )
        self.assertEqual(
            approval[approval.index("approve-scripts") + 1 :],
            ("prisma@6.19.0", "@prisma/engines@6.19.0"),
        )

    def test_prepare_accepts_npm_help_exit_one_with_recognized_commands(self):
        self.config.update(network="fixture_default")

        def command(arguments, **kwargs):
            if "--help" in arguments:
                return subprocess.CompletedProcess(
                    arguments,
                    1,
                    b"npm <command>\ninstall, rebuild, approve-scripts\n",
                    b"",
                )
            output = b"a" * 64 if "run" in arguments else b""
            return subprocess.CompletedProcess(arguments, 0, output, b"")

        with (
            patch.object(
                self.runtime,
                "preflight",
                return_value={"image": "sha256:" + "b" * 64, "identity": {}},
            ),
            patch.object(self.runtime, "snapshot"),
            patch.object(self.runtime, "connection"),
            patch.object(self.runtime, "prisma", return_value="prisma : 6.19.0\n"),
            patch("subprocess.run", side_effect=command) as commands,
        ):
            self.runtime.prepare()
        arguments = [call.args[0] for call in commands.call_args_list]
        self.assertTrue(any("approve-scripts" in args for args in arguments))
        self.assertTrue(any("rebuild" in args for args in arguments))

    def test_npm_help_error_is_not_accepted_as_capability_evidence(self):
        self.config.update(network="fixture_default")

        def command(arguments, **kwargs):
            if "--help" in arguments:
                return subprocess.CompletedProcess(
                    arguments, 1, b"DO_NOT_PRINT", b"PASSWORD"
                )
            return subprocess.CompletedProcess(
                arguments, 0, b"a" * 64 if "run" in arguments else b"", b""
            )

        with (
            patch.object(
                self.runtime,
                "preflight",
                return_value={"image": "sha256:" + "b" * 64, "identity": {}},
            ),
            patch.object(self.runtime, "snapshot"),
            patch.object(self.runtime, "connection"),
            patch("subprocess.run", side_effect=command) as commands,
        ):
            with self.assertRaises(MigrationError) as error:
                self.runtime.prepare()
        self.assertNotIn("DO_NOT_PRINT", str(error.exception))
        self.assertFalse(
            any("rebuild" in call.args[0] for call in commands.call_args_list)
        )

    def test_nonzero_status_remains_an_error_for_writing_commands(self):
        for command in ("install", "approve-scripts", "rebuild"):
            with (
                self.subTest(command=command),
                patch(
                    "subprocess.run",
                    return_value=subprocess.CompletedProcess([], 1, b"", b""),
                ),
            ):
                with self.assertRaises(MigrationError) as error:
                    Commands().run(["npm", command])
                self.assertEqual(error.exception.code, 1)
