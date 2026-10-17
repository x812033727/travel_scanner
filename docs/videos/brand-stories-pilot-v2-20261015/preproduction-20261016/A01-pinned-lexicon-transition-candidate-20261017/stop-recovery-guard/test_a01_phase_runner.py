"""Local byte-tree and one-off preflight checks; Docker is never contacted."""

import hashlib
import io
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "ops/release"))
import a01_stop_guard  # noqa: F401,E402 -- pin local module before runner adds /usr/local/sbin
import a01_phase_recover  # noqa: F401,E402 -- exercise the reviewed local recovery parser
import a01_phase_runner as runner


class PayloadTreeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="a01-tree-test-"))
        self.addCleanup(shutil.rmtree, self.root)
        self.payload = self.root / "payload"
        (self.payload / "sub").mkdir(parents=True)
        (self.payload / "sub/file.txt").write_bytes(b"approved")
        self.archive = self.root / "approved.tar.gz"
        with tarfile.open(self.archive, "w:gz") as tar:
            for name in ("payload", "payload/sub"):
                info = tarfile.TarInfo(name)
                info.type = tarfile.DIRTYPE
                tar.addfile(info)
            info = tarfile.TarInfo("payload/sub/file.txt")
            info.size = len(b"approved")
            tar.addfile(info, io.BytesIO(b"approved"))
        self.pins = patch.multiple(
            runner, HOST_PAYLOAD=self.payload, EXPECTED_PAYLOAD_MEMBERS=3,
            EXPECTED_PAYLOAD_FILES=1, EXPECTED_PAYLOAD_SUBDIRS=1,
        )

    def test_host_full_tree_match_and_drift(self) -> None:
        with self.pins:
            expected = runner.reviewed_payload_tree(self.archive)
            self.assertEqual(expected["files"],
                             {"sub/file.txt": hashlib.sha256(b"approved").hexdigest()})
            self.assertEqual(expected["dirs"], ["sub"])
            (self.payload / "sub/file.txt").write_bytes(b"tampered")
            with self.assertRaisesRegex(RuntimeError, "byte drift"):
                runner.reviewed_payload_tree(self.archive)

    def test_extra_file_refused(self) -> None:
        (self.payload / "extra").write_bytes(b"bad")
        with self.pins, self.assertRaisesRegex(RuntimeError, "tree differs"):
            runner.reviewed_payload_tree(self.archive)

    def test_oneoff_verifier_catches_copy_drift(self) -> None:
        base = str(self.payload).replace("\\", "/")
        script = runner.ONEOFF_TREE_VERIFY.replace(
            "/tmp/a01-round12-20261017-fe35369c/payload", base,
        )
        expected = {"files": {"sub/file.txt": hashlib.sha256(b"approved").hexdigest()},
                    "dirs": ["sub"]}
        command = [sys.executable, "-c", script]
        passed = subprocess.run(command, input=json.dumps(expected), text=True,
                                capture_output=True, check=False)
        self.assertEqual(passed.returncode, 0, passed.stderr)
        (self.payload / "sub/file.txt").write_bytes(b"tampered")
        failed = subprocess.run(command, input=json.dumps(expected), text=True,
                                capture_output=True, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("differ", failed.stderr)


class WorkerDrainTests(unittest.TestCase):
    def test_live_auto_node_is_not_quiet(self) -> None:
        rows = [["/usr/bin/docker-init", "--", "/usr/local/bin/video-worker"],
                ["/bin/sh", "/usr/local/bin/video-worker"],
                ["node", "tools/video/cli.mjs", "auto"]]
        with patch.object(runner, "command", return_value=json.dumps(rows)):
            self.assertFalse(runner.worker_quiet("pinned-original"))

    def test_worker_shell_and_sleep_are_quiet(self) -> None:
        rows = [["/usr/bin/docker-init", "--", "/usr/local/bin/video-worker"],
                ["/bin/sh", "/usr/local/bin/video-worker"],
                ["sleep", "300"]]
        with patch.object(runner, "command", return_value=json.dumps(rows)):
            self.assertTrue(runner.worker_quiet("pinned-original"))


class TimeoutTests(unittest.TestCase):
    def test_docker_cli_timeout_is_uncertain_failure(self) -> None:
        with patch.object(runner.subprocess, "run",
                          side_effect=subprocess.TimeoutExpired(("docker", "ps"), 120)):
            with self.assertRaisesRegex(RuntimeError, "timed out.*uncertain"):
                runner.command("docker", "ps")


class ContainerIdentityTests(unittest.TestCase):
    def test_oneoff_is_excluded_by_exact_docker_label_filter(self) -> None:
        original, oneoff = "a" * 64, "b" * 64

        def fake(*args: str, **_kwargs: object) -> str:
            if args[1] == "ps":
                self.assertIn("label=com.docker.compose.oneoff=False", args)
                return original
            if "{{json .Config.Labels}}" in args:
                candidate = args[-1]
                return json.dumps({"com.docker.compose.project": "travel_scanner",
                                   "com.docker.compose.service": "video-worker",
                                   "com.docker.compose.oneoff":
                                   "False" if candidate == original else "True"})
            if "{{.Id}}" in args:
                return args[-1]
            self.fail(f"unexpected command: {args}")

        with patch.object(runner, "command", side_effect=fake):
            self.assertEqual(runner.container_id("video-worker"), original)

    def test_duplicate_originals_refused(self) -> None:
        with patch.object(runner, "command", return_value="a" * 64 + "\n" + "b" * 64):
            with self.assertRaisesRegex(RuntimeError, "no unique original"):
                runner.container_id("video-worker")

    def test_created_oneoff_id_comes_from_exact_name_and_labels(self) -> None:
        identity = "c" * 64

        def fake(*args: str, **_kwargs: object) -> str:
            if args[1] == "ps":
                self.assertIn("label=mokaair.a01.round12=validate", args)
                return identity
            if "{{json .Config.Labels}}" in args:
                return json.dumps({"mokaair.a01.round12": "validate",
                                   "com.docker.compose.project": "travel_scanner",
                                   "com.docker.compose.service": "video-worker",
                                   "com.docker.compose.oneoff": "True"})
            if "{{.Id}}" in args:
                return identity
            if "{{.Name}}" in args:
                return "/mokaair-a01-round12-validate"
            self.fail(f"unexpected command: {args}")

        with patch.object(runner, "command", side_effect=fake):
            self.assertEqual(runner.created_oneoff_id("mokaair-a01-round12-validate", "validate"),
                             identity)


class OneoffStoppedTests(unittest.TestCase):
    def test_auto_removed_oneoff_requires_exact_lowercase_missing_id(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            marker = Path(folder) / "oneoff.json"
            identity = "d" * 64
            marker.write_text(json.dumps({"container_id": identity}))
            result = subprocess.CompletedProcess(("docker", "inspect"), 1, b"",
                                                 ("error: no such object: " + identity).encode())
            with patch.object(runner, "ONEOFF", marker), patch.object(runner.subprocess, "run",
                                                                         return_value=result):
                runner.oneoff_stopped()
            wrong = subprocess.CompletedProcess(("docker", "inspect"), 1, b"",
                                                ("error: no such object: " + "e" * 64).encode())
            with patch.object(runner, "ONEOFF", marker), patch.object(runner.subprocess, "run",
                                                                         return_value=wrong):
                with self.assertRaisesRegex(RuntimeError, "proved absent ID"):
                    runner.oneoff_stopped()


if __name__ == "__main__":
    unittest.main()
