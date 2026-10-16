"""Offline worker drain tests. No Docker daemon, host or vendor calls."""

from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("video_worker_drain.sh")
WORKER = Path(__file__).parents[1] / "video" / "worker.sh"
BASH = shutil.which("bash")
NONCE = "11111111-2222-3333-4444-555555555555"
SHA = "a" * 40


def wait_for(path: Path, *, seconds: float = 6) -> bool:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if path.exists():
            return True
        time.sleep(0.05)
    return path.exists()


@unittest.skipUnless(sys.platform == "linux" and BASH, "Linux bash required")
class WorkerProcessTests(unittest.TestCase):
    def test_preexisting_drain_starts_idle_without_login_or_paid_child(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            work = root / "work"
            work.mkdir()
            (work / "STOP").write_text(f"deploy-video-worker:{NONCE}\n")
            (work / "DEPLOY_DRAIN").write_text(f"{NONCE}\n")
            node = bin_dir / "node"
            node.write_text(
                "#!/bin/sh\n"
                "case \"$1\" in *sync-docs.mjs) exit 0;; esac\n"
                "touch \"$FAKE_WORKER_ROOT/unexpected-node\"\nexit 99\n",
                encoding="utf-8",
            )
            node.chmod(0o755)
            worker = root / "worker.sh"
            worker.write_text(
                WORKER.read_text(encoding="utf-8").replace(
                    "cd /opt/mokaair || exit 1", f'cd "{root}" || exit 1'
                ),
                encoding="utf-8",
            )
            proc = subprocess.Popen(
                ["sh", str(worker)],
                env={
                    **os.environ,
                    "PATH": f"{bin_dir}:{os.environ['PATH']}",
                    "FAKE_WORKER_ROOT": str(root),
                    "VIDEO_WORKDIR": str(work),
                    "HOME": str(root / "home"),
                },
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            try:
                self.assertTrue(wait_for(work / "DEPLOY_DRAIN.ready"))
                self.assertFalse((root / "unexpected-node").exists())
                os.kill(proc.pid, signal.SIGTERM)
                self.assertEqual(proc.wait(timeout=6), 143)
            finally:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait(timeout=6)

    def test_stop_waits_for_both_paid_children_and_no_new_work_starts(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            work = root / "work"
            work.mkdir()
            home = root / "home"
            (home / ".mokaair").mkdir(parents=True)
            (home / ".mokaair" / "video-tool.json").write_text("paired")
            node = bin_dir / "node"
            node.write_text(
                "#!/usr/bin/env python3\n"
                "import os, pathlib, sys, time\n"
                "root = pathlib.Path(os.environ['FAKE_WORKER_ROOT'])\n"
                "if sys.argv[1].endswith('sync-docs.mjs'): sys.exit(0)\n"
                "name = 'shorts' if 'shorts' in sys.argv[1] else 'auto'\n"
                "(root / (name + '.started')).write_text('1')\n"
                "while not (root / (name + '.release')).exists(): time.sleep(.05)\n"
                "(root / (name + '.completed')).write_text('1')\n",
                encoding="utf-8",
            )
            node.chmod(0o755)
            worker = root / "worker.sh"
            worker.write_text(
                WORKER.read_text(encoding="utf-8").replace(
                    "cd /opt/mokaair || exit 1", f'cd "{root}" || exit 1'
                ),
                encoding="utf-8",
            )
            env = {
                **os.environ,
                "PATH": f"{bin_dir}:{os.environ['PATH']}",
                "FAKE_WORKER_ROOT": str(root),
                "VIDEO_WORKDIR": str(work),
                "HOME": str(home),
                "VIDEO_WORKER_INTERVAL_SECONDS": "30",
                "VIDEO_SHORTS_KNOCK_SECONDS": "30",
            }
            proc = subprocess.Popen(
                ["sh", str(worker)], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True,
            )
            try:
                self.assertTrue(wait_for(root / "auto.started"))
                self.assertTrue(wait_for(root / "shorts.started"))
                (work / "STOP").write_text(f"deploy-video-worker:{NONCE}\n")
                (work / "DEPLOY_DRAIN").write_text(f"{NONCE}\n")
                (root / "auto.release").touch()
                self.assertTrue(wait_for(root / "auto.completed"))
                time.sleep(0.25)
                self.assertFalse((work / "DEPLOY_DRAIN.ready").exists())
                (root / "shorts.release").touch()
                self.assertTrue(wait_for(work / "DEPLOY_DRAIN.ready"))
                self.assertTrue((root / "shorts.completed").exists())
                self.assertEqual((work / "DEPLOY_DRAIN.ready").read_text().splitlines()[0], NONCE)
                os.kill(proc.pid, signal.SIGTERM)
                self.assertEqual(proc.wait(timeout=6), 143)
                self.assertTrue((work / "STOP").exists())
                self.assertTrue((work / "DEPLOY_DRAIN").exists())
            finally:
                if proc.poll() is None:
                    (root / "auto.release").touch()
                    (root / "shorts.release").touch()
                    proc.kill()
                    proc.wait(timeout=6)


@unittest.skipUnless(sys.platform == "linux" and BASH, "Linux bash required")
class HostGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.work = self.root / "work"
        self.work.mkdir()
        self.marker = self.root / "video-worker-drain.pending"
        self.receipt = self.root / f"video-worker-drain.ready.{NONCE}"
        self.put("id", "worker-one")
        self.put("running", "true")
        self.put("exit", "0")
        self.put("top", "PID PPID COMMAND\n100 0 docker-init\n101 100 sh\n102 101 sleep\n")
        self.put("exec-ids", "[]")
        fake = self.bin / "docker"
        fake.write_text(
            """#!/usr/bin/env python3
import os, pathlib, sys
r = pathlib.Path(os.environ['FAKE_DOCKER_ROOT'])
w = r / 'work'
a = sys.argv[1:]
(r / 'calls').open('a').write(' '.join(a) + '\\n')
def read(name): return (r / name).read_text().strip()
def has(name): return (r / name).exists()
def result(value): print(value); sys.exit(0)
if a[0] == 'compose' and 'ps' in a:
    if not has('absent'): result(read('id'))
    result('')
if a[0] == 'compose' and 'exec' in a:
    sys.exit(1 if has('legacy') else 0)
if a[0] == 'inspect':
    fmt = a[2]
    if 'ExecIDs' in fmt: result(read('exec-ids'))
    if 'State.Pid' in fmt: result('100')
    if 'ExitCode' in fmt and 'Config.Cmd' in fmt:
        result(read('running') + '|' + read('exit') + '|false|["/usr/local/bin/video-worker"]')
    if 'ExitCode' in fmt: result(read('running') + '|' + read('exit') + '|false')
    result(read('running') + '|false')
if a[0] == 'top': result((r / 'top').read_text().rstrip())
if a[:2] == ['container', 'stop']:
    if has('stop-error'): sys.exit(1)
    (r / 'stop-called').write_text('1')
    (r / 'running').write_text('false')
    (r / 'exit').write_text('143')
    result(read('id'))
if a[0] == 'exec':
    nonce = os.environ['VIDEO_WORKER_DRAIN_NONCE']
    if 'boot=$(cat' in a[-1]:
        expected = nonce + '\\nboot\\nstarted-' + read('id') + '\\n'
        good = (w / 'STOP').exists() and (w / 'DEPLOY_DRAIN').read_text() == nonce + '\\n'
        good = good and (w / 'DEPLOY_DRAIN.ready').exists() and (w / 'DEPLOY_DRAIN.ready').read_text() == expected
        sys.exit(0 if good else 1)
    if 'VIDEO_DRAIN_NONCE' in ' '.join(a) and 'printf' in a[-1]:
        if (w / 'DEPLOY_DRAIN').exists(): sys.exit(1)
        if not (w / 'STOP').exists(): (w / 'STOP').write_text('deploy-video-worker:' + nonce + '\\n')
        (w / 'DEPLOY_DRAIN').write_text(nonce + '\\n')
        if not has('no-ack'):
            (w / 'DEPLOY_DRAIN.ready').write_text(nonce + '\\nboot\\nstarted-' + read('id') + '\\n')
        sys.exit(0)
    if (w / 'DEPLOY_DRAIN').exists(): result((w / 'DEPLOY_DRAIN').read_text().strip())
    result('')
sys.exit(98)
""",
            encoding="utf-8",
        )
        fake.chmod(0o755)
        git = self.bin / "git"
        git.write_text(f"#!/bin/sh\nprintf '%s\\n' {SHA}\n", encoding="utf-8")
        git.chmod(0o755)

    def put(self, name: str, value: str = "1") -> None:
        (self.root / name).write_text(value, encoding="utf-8")

    def guard(self, mode: str = "--normal") -> subprocess.CompletedProcess[str]:
        env = {
            **os.environ,
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "FAKE_DOCKER_ROOT": str(self.root),
            "VIDEO_WORKER_GUARD_REPO": str(self.root),
            "VIDEO_WORKER_DRAIN_MARKER": str(self.marker),
            "VIDEO_WORKER_DRAIN_NONCE": NONCE,
            "VIDEO_WORKER_DRAIN_LOCAL_SHA": SHA,
            "VIDEO_WORKER_DRAIN_READY_FILE": str(self.receipt),
            "VIDEO_WORKER_DRAIN_WAIT_SECONDS": "1",
        }
        return subprocess.run([BASH, str(SCRIPT), mode], env=env, capture_output=True, text=True)

    def test_old_worker_refuses_without_touching_stop(self) -> None:
        self.put("legacy")
        outcome = self.guard("--precheck")
        self.assertEqual(outcome.returncode, 3, outcome.stderr)
        self.assertIn("lacks drain protocol", outcome.stderr)
        self.assertFalse(self.marker.exists())
        self.assertFalse((self.work / "STOP").exists())

    def test_active_call_times_out_without_term_or_retry(self) -> None:
        self.put("no-ack")
        outcome = self.guard()
        self.assertEqual(outcome.returncode, 3, outcome.stderr)
        self.assertIn("did not acknowledge", outcome.stderr)
        self.assertTrue(self.marker.exists())
        self.assertTrue((self.work / "STOP").exists())
        self.assertFalse((self.root / "stop-called").exists())
        again = self.guard()
        self.assertEqual(again.returncode, 3)
        self.assertIn("previous worker drain", again.stderr)

    def test_manual_exec_or_unknown_process_holds_without_term(self) -> None:
        for flag, value in (
            ("exec-ids", '["manual"]'),
            ("top", "PID PPID COMMAND\n100 0 docker-init\n101 100 sh\n102 101 node\n"),
            ("top", "PID PPID COMMAND\n"),
            ("top", "PID PPID COMMAND\n100 0 docker-init\n101 100 sh\n102 101 sleep\n103 101 sleep\n"),
            ("top", "PID PPID COMMAND\n100 0 docker-init\n101 100 sh\n201 1 sleep\n"),
        ):
            with self.subTest(flag=flag):
                self.put(flag, value)
                outcome = self.guard()
                self.assertEqual(outcome.returncode, 3, outcome.stderr)
                self.assertTrue(self.marker.exists())
                self.assertFalse((self.root / "stop-called").exists())
                self.marker.unlink()
                (self.work / "DEPLOY_DRAIN").unlink()
                (self.work / "DEPLOY_DRAIN.ready").unlink()
                (self.work / "STOP").unlink()
                self.put("exec-ids", "[]")
                self.put("top", "PID PPID COMMAND\n100 0 docker-init\n101 100 sh\n102 101 sleep\n")

    def test_clean_stop_preserves_owner_stop_and_receipts(self) -> None:
        (self.work / "STOP").write_text("owner hold\n")
        outcome = self.guard()
        self.assertEqual(outcome.returncode, 0, outcome.stderr)
        self.assertEqual((self.work / "STOP").read_text(), "owner hold\n")
        self.assertEqual(self.receipt.read_text(), f"{SHA}\n{NONCE}\nworker-one\n")
        self.assertFalse(self.marker.exists())
        self.assertEqual(self.put_called("stop-called"), "1")
        self.assertIn("--timeout=-1", (self.root / "calls").read_text())

    def put_called(self, name: str) -> str:
        return (self.root / name).read_text()

    def test_rollback_requires_same_nonce_and_live_ack_or_refuses_zero_worker(self) -> None:
        self.assertEqual(self.guard().returncode, 0)
        self.put("id", "worker-two")
        self.put("running", "true")
        self.put("exit", "0")
        stale = self.guard("--rollback")
        self.assertEqual(stale.returncode, 3)
        self.assertTrue(self.marker.exists())
        self.marker.unlink()  # isolate the next condition in the offline fake
        (self.work / "DEPLOY_DRAIN.ready").write_text(f"{NONCE}\nboot\nstarted-worker-two\n")
        clean = self.guard("--rollback")
        self.assertEqual(clean.returncode, 0, clean.stderr)
        self.put("absent")
        absent = self.guard("--rollback")
        self.assertEqual(absent.returncode, 3)
        self.assertIn("no worker", absent.stderr)


if __name__ == "__main__":
    unittest.main()
