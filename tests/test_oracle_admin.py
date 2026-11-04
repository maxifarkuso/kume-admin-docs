"""Read-only admin checks: no Docker daemon, sudo or Oracle connection."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/oracle-admin.sh"
FRONTEND = "a" * 40 + "-1-1"
BACKEND = "b" * 40 + "-2-1"


class AdminTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.control = self.base / "control"
        self.backend = self.base / "backend"
        self.webroot = self.base / "public"
        self.control.mkdir()
        (self.backend / "releases" / BACKEND).mkdir(parents=True)
        (self.webroot / "releases" / FRONTEND / "site").mkdir(parents=True)
        (self.webroot / "current").symlink_to(f"releases/{FRONTEND}/site")
        for root, identifier in ((self.control, FRONTEND), (self.backend, BACKEND)):
            (root / "state.json").write_text(
                json.dumps(
                    {
                        "current": identifier,
                        "previous": None,
                        "pending": None,
                        "unexpected_secret": "DO_NOT_PRINT",
                    }
                )
            )

    def states(self):
        return subprocess.run(
            [
                "bash",
                "-c",
                'source "$1"; shift; show_states "$@"',
                "--",
                str(SCRIPT),
                str(self.control),
                str(self.backend),
                str(self.webroot),
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )

    def test_coherent_states_are_filtered_and_unchanged(self):
        before = (self.control / "state.json").read_bytes()
        result = self.states()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(FRONTEND, result.stdout)
        self.assertIn(BACKEND, result.stdout)
        self.assertNotIn("DO_NOT_PRINT", result.stdout)
        self.assertEqual((self.control / "state.json").read_bytes(), before)
        self.assertEqual(set(self.control.iterdir()), {self.control / "state.json"})

    def test_pending_unknown_fields_are_not_printed_or_recovered(self):
        state = {
            "current": FRONTEND,
            "previous": None,
            "pending": {"unknown": "DO_NOT_PRINT"},
        }
        (self.control / "state.json").write_text(json.dumps(state))
        result = self.states()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("DO_NOT_PRINT", result.stdout)
        self.assertEqual(json.loads((self.control / "state.json").read_text()), state)

    def test_wrong_link_missing_and_invalid_state_fail_without_mutation(self):
        link = self.webroot / "current"
        link.unlink()
        result = self.states()
        self.assertEqual(result.returncode, 1)
        self.assertFalse(link.exists())
        (self.control / "state.json").write_text(
            '{"current": "../../DO_NOT_PRINT", "previous": null, "pending": null}'
        )
        self.assertNotIn("DO_NOT_PRINT", self.states().stdout)
        (self.control / "state.json").unlink()
        self.assertEqual(self.states().returncode, 1)
        self.assertFalse((self.control / "state.json").exists())

    def test_unknown_commands_and_extra_arguments_are_rejected(self):
        for arguments in (("prune",), ("imagenes", "--all")):
            result = subprocess.run(
                ["bash", str(SCRIPT), *arguments],
                capture_output=True,
                text=True,
                timeout=5,
            )
            self.assertEqual(result.returncode, 2)

    def test_docker_menu_uses_only_inventory_commands(self):
        expected = {
            "contenedores": "ps",
            "imagenes": "image",
            "consumo": "stats",
            "espacio-docker": "system",
            "volumenes": "volume",
            "redes": "network",
        }
        for option, command in expected.items():
            with self.subTest(option=option):
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        'source "$1"; sudo() { printf "%s\\n" "$@"; }; run_query "$2"',
                        "--",
                        str(SCRIPT),
                        option,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.splitlines()[:2], ["docker", command])
                self.assertFalse(
                    set(result.stdout.splitlines())
                    & {"prune", "rm", "stop", "restart", "down"}
                )

    def test_health_filters_bodies_and_fails_on_sql_http_or_malformed_response(self):
        responses = (
            ('{"status":"ok","database":"ok"}\n200', 0),
            ('{"secret":"DO_NOT_PRINT"}\n503', 1),
            ('{"status":"ok","database":"DO_NOT_PRINT"}\n200', 1),
            ("DO_NOT_PRINT\n200", 1),
        )
        command = """source "$1"; fixture_response=$2; curl() { case "${!#}" in *3001/health) printf '%s' "$fixture_response";; *) printf 'HTTP 200 - text/html\\n';; esac; }; check_health"""
        for response, code in responses:
            with self.subTest(response=response):
                result = subprocess.run(
                    ["bash", "-c", command, "--", str(SCRIPT), response],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertNotIn("DO_NOT_PRINT", result.stdout + result.stderr)

    def container_user(self, names, selection, exec_code=0, list_code=0):
        command = """source "$1"; names=$2; exec_code=$3; list_code=$4
sudo() {
    if [[ $1 == docker && $2 == ps ]]; then
        printf '%s' "$names"
        return "$list_code"
    fi
    printf 'EXEC_ARG:%s\\n' "$@"
    return "$exec_code"
}
run_query usuario"""
        return subprocess.run(
            [
                "bash",
                "-c",
                command,
                "--",
                str(SCRIPT),
                names,
                str(exec_code),
                str(list_code),
            ],
            input=selection,
            capture_output=True,
            text=True,
            timeout=5,
        )

    def test_container_selector_executes_only_id_in_chosen_running_container(self):
        result = self.container_user("backend-one\ndatabase-one\n", "2\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        executed = [
            line.removeprefix("EXEC_ARG:")
            for line in result.stdout.splitlines()
            if line.startswith("EXEC_ARG:")
        ]
        self.assertEqual(executed, ["docker", "exec", "database-one", "id"])
        self.assertNotIn("--user", executed)
        result = self.container_user("cancelar\n", "1\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("EXEC_ARG:cancelar", result.stdout)

    def test_container_selector_cancel_empty_and_invalid_choice(self):
        for names, selection in (
            ("", ""),
            ("backend-one\n", "0\n"),
            ("backend-one\n", "2\n"),
            ("backend-one\n", ""),
        ):
            with self.subTest(names=names, selection=selection):
                result = self.container_user(names, selection)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn("EXEC_ARG:", result.stdout)
        result = self.container_user("backend-one\n", "99\n1\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.count("EXEC_ARG:docker"), 1)
        self.assertIn("EXEC_ARG:backend-one", result.stdout)

    def test_container_selector_propagates_docker_failures_without_retry(self):
        result = self.container_user("backend-one\n", "1\n", exec_code=126)
        self.assertEqual(result.returncode, 126)
        self.assertEqual(result.stdout.count("EXEC_ARG:docker"), 1)
        result = self.container_user("", "1\n", list_code=1)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("EXEC_ARG:", result.stdout)
