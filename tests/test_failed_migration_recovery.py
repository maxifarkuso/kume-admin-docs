"""Recovery policy with controlled collaborators, without an operational database."""

import copy
import hashlib
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import unittest
import test_oracle_migrations as original
from kume_migrations.storage import MigrationError
from kume_migrations.workflow import check_history


class FailedMigrationRecoveryTests(unittest.TestCase):
    setUp = original.WorkflowTests.setUp
    prepared = original.WorkflowTests.prepared
    failed_deploy = original.WorkflowTests.failed_deploy

    def failed_migration(self):
        self.failed_deploy()
        self.runtime.rows = [
            dict(
                id="first",
                migration_name="001_schema",
                checksum="a" * 64,
                finished=True,
                rolled_back=False,
            ),
            dict(
                id="failed",
                migration_name="002_seed",
                checksum="b" * 64,
                finished=False,
                rolled_back=False,
            ),
        ]
        self.workflow.migration = "002_seed"

    def test_resolve_preserves_history_and_requires_inspected_retry_then_apply(self):
        self.failed_migration()
        original = copy.deepcopy(self.runtime.rows)
        self.workflow.execute("recuperar-fallida")
        self.assertEqual(
            self.runtime.rows, [original[0], {**original[1], "rolled_back": True}]
        )
        self.assertEqual(self.journal.outcome("aplicar"), "uncertain")
        self.assertEqual(self.journal.outcome("recuperar-fallida"), "success")
        self.assertFalse(self.workflow.retry_authorized())
        self.assertEqual(self.runtime.calls.count("deploy"), 1)
        self.assertEqual(
            self.journal.value["artifacts"]["failed_migration_recovery"]["attempt"],
            original[-1],
        )
        self.assertIn("recovery_verification", self.journal.value["artifacts"])
        with self.assertRaises(MigrationError):
            self.workflow.execute("aplicar")
        self.workflow.execute("habilitar-reintento")
        self.workflow.execute("aplicar")
        self.assertEqual(self.journal.outcome("aplicar"), "success")
        self.assertEqual(self.runtime.rows[1], {**original[1], "rolled_back": True})
        self.assertEqual(check_history(self.runtime.rows, self.runtime.migrations), [])

    def test_rejects_completed_reverted_foreign_or_divergent_attempt(self):
        for changes in (
            dict(finished=True),
            dict(rolled_back=True),
            dict(migration_name="foreign"),
            dict(checksum="x" * 64),
            dict(id=""),
        ):
            self.failed_migration_fixture(changes)
            with self.assertRaises(MigrationError):
                self.workflow.execute("recuperar-fallida")
            self.assertNotIn("resolve", self.runtime.calls)

    def failed_migration_fixture(self, changes=None):
        # Each subcase uses a fresh journal, never mutates production evidence.
        self.journal.value["events"] = []
        self.journal.value["artifacts"] = {}
        self.runtime.rows = []
        self.runtime.calls = []
        self.failed_migration()
        self.runtime.rows[-1].update(changes or {})

    def test_rejects_other_pending_migrations_and_invalid_prefix(self):
        for migrations in (
            {"001_schema": "a" * 64, "002_seed": "b" * 64, "003_extra": "c" * 64},
            {"000_missing": "c" * 64, "001_schema": "a" * 64, "002_seed": "b" * 64},
        ):
            self.failed_migration_fixture()
            self.runtime.migrations = migrations
            with self.assertRaises(MigrationError):
                self.workflow.execute("recuperar-fallida")
            self.assertNotIn("resolve", self.runtime.calls)

    def test_active_migrator_failed_inspection_backup_or_verifier_blocks_resolve(self):
        for collaborator in (
            "idle",
            "verify_retry",
            "check_backup",
            "check_recovery_verification",
        ):
            self.failed_migration_fixture()
            self.runtime.fail = collaborator
            with self.assertRaises(MigrationError):
                self.workflow.execute("recuperar-fallida")
            self.assertNotIn("resolve", self.runtime.calls)
            self.assertIsNone(self.journal.outcome("recuperar-fallida"))
            self.runtime.fail = None

    def test_cancellation_and_changes_during_confirmation_never_resolve(self):
        self.failed_migration()
        self.workflow.confirm = lambda prompt: "no"
        with self.assertRaises(MigrationError):
            self.workflow.execute("recuperar-fallida")
        self.assertNotIn("resolve", self.runtime.calls)

        def changed(prompt):
            self.runtime.rows[-1] = {**self.runtime.rows[-1], "checksum": "x" * 64}
            return prompt.split(": ", 1)[1].strip()

        self.workflow.confirm = changed
        with self.assertRaises(MigrationError):
            self.workflow.execute("recuperar-fallida")
        self.assertNotIn("resolve", self.runtime.calls)

    def test_uncertain_resolve_never_repeats_and_blocks_apply_or_retry(self):
        self.failed_migration()
        self.runtime.fail = "resolve"
        with self.assertRaises(MigrationError):
            self.workflow.execute("recuperar-fallida")
        self.assertEqual(self.journal.outcome("recuperar-fallida"), "uncertain")
        self.runtime.fail = None
        for action in ("recuperar-fallida", "habilitar-reintento", "aplicar"):
            with self.assertRaises(MigrationError):
                self.workflow.execute(action)
        self.assertEqual(self.runtime.calls.count("resolve"), 1)

    def test_unexpected_resolve_result_is_uncertain(self):
        self.failed_migration()
        with patch.object(self.runtime, "prisma"):
            with self.assertRaises(MigrationError):
                self.workflow.execute("recuperar-fallida")
        self.assertEqual(self.journal.outcome("recuperar-fallida"), "uncertain")
        self.assertNotIn("recovery_verification", self.journal.value["artifacts"])

    def test_history_accepts_rolled_back_attempt_before_success_but_not_divergence(
        self,
    ):
        self.failed_migration()
        self.runtime.rows[-1]["rolled_back"] = True
        self.assertEqual(
            check_history(self.runtime.rows, self.runtime.migrations), ["002_seed"]
        )
        for changes in (
            dict(finished=True),
            dict(checksum="x" * 64),
            dict(migration_name="001_schema"),
        ):
            rows = copy.deepcopy(self.runtime.rows)
            rows[-1].update(changes)
            with self.assertRaises(MigrationError):
                check_history(rows, self.runtime.migrations)

    def test_normal_success_running_and_exceptional_initialization_cannot_recover(self):
        self.failed_migration()
        for outcome in ("running", "success"):
            self.journal.record("aplicar", outcome)
            with self.assertRaises(MigrationError):
                self.workflow.execute("recuperar-fallida")
        self.journal.record("aplicar", "uncertain")
        self.journal.record("inicializar", "uncertain")
        with self.assertRaises(MigrationError):
            self.workflow.execute("recuperar-fallida")
        self.assertNotIn("resolve", self.runtime.calls)


class RecoveryAdapterTests(unittest.TestCase):
    setUp = original.AdapterTests.setUp

    def test_idle_tools_and_database_checked_without_exposing_process_arguments(self):
        with patch.object(self.runtime, "container", return_value="own"), patch.object(
            self.runtime, "docker", return_value="COMMAND\nsleep\n"
        ), patch.object(self.runtime, "sql", return_value="t"):
            self.runtime.ensure_idle()
        for processes, database in (
            ("COMMAND\nsleep\nnode\n", "t"),
            ("COMMAND\nsleep\n", "f"),
        ):
            with patch.object(
                self.runtime, "container", return_value="own"
            ), patch.object(
                self.runtime, "docker", return_value=processes
            ), patch.object(
                self.runtime, "sql", return_value=database
            ):
                with self.assertRaises(MigrationError):
                    self.runtime.ensure_idle()

    def test_approved_recovery_verifier_replaces_only_execution_not_original_config(
        self,
    ):
        path = self.root / "recovery.sql"
        path.write_text("SELECT 'ok' WHERE 1=1;")
        path.chmod(0o600)
        self.runtime.config = dict(
            postgres="fixture-db", user="fixture", database="fixture"
        )
        self.journal.artifact(
            "recovery_verification",
            {
                "path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            },
        )
        with patch.object(self.runtime, "docker", return_value="ok") as docker:
            self.runtime.verify()
        self.assertIn("WHERE 1=1", docker.call_args.kwargs["input"].decode())
        path.write_text("SELECT 'changed';")
        with patch.object(self.runtime, "docker") as docker:
            with self.assertRaises(MigrationError):
                self.runtime.verify()
            docker.assert_not_called()

    def test_recovery_cli_requires_all_flags_and_rejects_wrong_action(self):
        entry = Path(__file__).resolve().parents[1] / "scripts/oracle-migrations.py"
        arguments = [
            sys.executable,
            str(entry),
            "recuperar-fallida",
            "--config",
            "/fixture.json",
            "--operacion",
            "fixture",
        ]
        for extra in (
            [],
            ["--migracion", "002_seed"],
            ["--migracion", "../bad"],
            ["--verificacion-sql", "relative.sql"],
        ):
            result = subprocess.run(arguments + extra, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)


class RecoveryAdditionalBoundaries(unittest.TestCase):
    setUp = original.WorkflowTests.setUp
    prepared = original.WorkflowTests.prepared
    failed_deploy = original.WorkflowTests.failed_deploy
    failed_migration = FailedMigrationRecoveryTests.failed_migration

    def test_resolve_failure_after_actual_metadata_change_remains_uncertain(self):
        self.failed_migration()
        original_prisma = self.runtime.prisma

        def interrupted(*args):
            original_prisma(*args)
            raise KeyboardInterrupt

        with patch.object(self.runtime, "prisma", side_effect=interrupted):
            with self.assertRaises(KeyboardInterrupt):
                self.workflow.execute("recuperar-fallida")
        self.assertTrue(self.runtime.rows[-1]["rolled_back"])
        self.assertEqual(self.journal.outcome("recuperar-fallida"), "uncertain")
        with self.assertRaises(MigrationError):
            self.workflow.execute("habilitar-reintento")

    def test_final_verifier_changed_during_confirmation_prevents_resolve(self):
        self.failed_migration()

        def changed(prompt):
            self.runtime.fail = "check_recovery_verification"
            return prompt.split(": ", 1)[1].strip()

        self.workflow.confirm = changed
        with self.assertRaises(MigrationError):
            self.workflow.execute("recuperar-fallida")
        self.assertNotIn("resolve", self.runtime.calls)

    def test_recovery_does_not_modify_config_backup_or_uncertain_apply_event(self):
        self.failed_migration()
        config = copy.deepcopy(self.journal.value["config"])
        backup = copy.deepcopy(self.journal.value["artifacts"]["backup"])
        events = copy.deepcopy(self.journal.value["events"])
        self.workflow.execute("recuperar-fallida")
        self.assertEqual(self.journal.value["config"], config)
        self.assertEqual(self.journal.value["artifacts"]["backup"], backup)
        self.assertEqual(self.journal.value["events"][: len(events)], events)
        self.assertEqual(self.runtime.calls.count("backup"), 1)
