"""Fault-order tests for the host ExecStopPost candidate; no Docker call."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import a01_phase_recover as subject


class RecoverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        base = Path(self.temp.name)
        self.stop = base / "STOP"
        self.stop.write_text("hold\n")
        self.marker = base / "a01-round12-oneoff.json"
        self.id = "a" * 64
        self.label = "listener"
        self.actions: list[str] = []
        self.patches = [
            patch.object(subject, "ONEOFF", self.marker),
            patch.object(subject.a01_stop_guard, "Paths", lambda: SimpleNamespace(stop=self.stop)),
            patch.object(subject.a01_stop_guard, "restore", self.restore),
            patch.object(subject.subprocess, "run", self.docker),
        ]
        for item in self.patches:
            item.start()

    def tearDown(self) -> None:
        for item in reversed(self.patches):
            item.stop()
        self.temp.cleanup()

    def restore(self) -> str:
        self.actions.append("restore")
        return "STOP restored"

    def docker(self, args: tuple[str, ...], **_kwargs: object) -> subprocess.CompletedProcess:
        if args[1] == "ps":
            self.actions.append("list")
            return subprocess.CompletedProcess(args, 0, (self.id + "\n").encode(), b"")
        if args[1] == "inspect" and ".Id" in args[3]:
            self.actions.append("inspect")
            return subprocess.CompletedProcess(args, 0,
                                               (self.id + " true no " + self.label + "\n").encode(), b"")
        if args[1] == "kill":
            self.actions.append("kill")
            return subprocess.CompletedProcess(args, 0, (self.id + "\n").encode(), b"")
        if args[1] == "inspect" and ".State.Running" in args[3]:
            self.actions.append("verify_absent")
            return subprocess.CompletedProcess(args, 1, b"", b"error: no such object: " + self.id.encode())
        self.fail(f"unexpected Docker command: {args}")

    def test_lost_marker_still_kills_labelled_container_before_restore(self) -> None:
        self.assertEqual(subject.main(), 0)
        self.assertEqual(self.actions, ["list", "inspect", "kill", "verify_absent", "restore"])

    def test_truncated_marker_still_kills_labelled_container_before_restore(self) -> None:
        self.marker.write_text('{"container_id":')
        self.assertEqual(subject.main(), 1)
        self.assertEqual(self.actions, ["list", "inspect", "kill", "verify_absent", "restore"])

    def test_fault_test_label_is_recovered(self) -> None:
        self.label = "fault-test"
        self.assertEqual(subject.main(), 0)
        self.assertEqual(self.actions, ["list", "inspect", "kill", "verify_absent", "restore"])

    def test_lowercase_docker_missing_exact_id_is_proof(self) -> None:
        self.assertTrue(subject.absent(1, "error: no such object: " + self.id, self.id))
        self.assertTrue(subject.absent(1, "No such container: " + self.id, self.id))

    def test_missing_other_id_or_daemon_error_is_not_proof(self) -> None:
        with self.assertRaises(RuntimeError):
            subject.absent(1, "error: no such object: " + "b" * 64, self.id)
        with self.assertRaises(RuntimeError):
            subject.absent(1, "Cannot connect to Docker daemon", self.id)

    def test_docker_daemon_error_is_not_proof_container_stopped(self) -> None:
        def daemon_error(args: tuple[str, ...], **_kwargs: object) -> subprocess.CompletedProcess:
            self.actions.append("daemon_error")
            return subprocess.CompletedProcess(args, 1, b"", b"Cannot connect to Docker daemon")

        with patch.object(subject.subprocess, "run", daemon_error):
            self.assertEqual(subject.main(), 1)
        self.assertEqual(self.actions, ["daemon_error", "restore"])

    def test_docker_timeout_still_attempts_stop_restore(self) -> None:
        def docker_timeout(args: tuple[str, ...], **_kwargs: object) -> subprocess.CompletedProcess:
            self.actions.append("daemon_timeout")
            raise subprocess.TimeoutExpired(args, 10)

        with patch.object(subject.subprocess, "run", docker_timeout):
            self.assertEqual(subject.main(), 1)
        self.assertEqual(self.actions, ["daemon_timeout", "restore"])

    def test_restart_policy_drift_is_repaired_before_kill(self) -> None:
        def drift(args: tuple[str, ...], **kwargs: object) -> subprocess.CompletedProcess:
            if args[1] == "inspect" and ".Id" in args[3]:
                self.actions.append("inspect_drift")
                return subprocess.CompletedProcess(args, 0, (self.id + " true always listener\n").encode(), b"")
            if args[1] == "update":
                self.actions.append("update_no")
                return subprocess.CompletedProcess(args, 0, b"", b"")
            if args[1] == "inspect" and "RestartPolicy.Name" in args[3]:
                self.actions.append("verify_no")
                return subprocess.CompletedProcess(args, 0, b"no\n", b"")
            return self.docker(args, **kwargs)

        with patch.object(subject.subprocess, "run", drift):
            self.assertEqual(subject.main(), 0)
        self.assertEqual(self.actions,
                         ["list", "inspect_drift", "update_no", "verify_no", "kill",
                          "verify_absent", "restore"])


if __name__ == "__main__":
    unittest.main()
