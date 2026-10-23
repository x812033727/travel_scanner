"""Offline tests for the host-only RQ drain; no Docker, DB or paid calls."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import video_stage_host_patch as host_patch  # noqa: E402

SCRIPT = Path(__file__).with_name("video_stage_drain.sh")
BASH = shutil.which("bash") if os.name == "posix" else None


class HostPatchTests(unittest.TestCase):
    def test_both_normal_and_rollback_recreation_are_guarded(self) -> None:
        original = (
            host_patch.NO_ROLLBACK_ANCHOR + host_patch.ROLLBACK_ANCHOR + host_patch.NORMAL_ANCHOR
        )
        patched = host_patch.patch_script(original)
        self.assertEqual(patched.count(host_patch.HELPER_LITERAL), 2)
        self.assertIn("/opt/travel-scanner-deploy/video_stage_drain.sh --normal", patched)
        self.assertIn("/opt/travel-scanner-deploy/video_stage_drain.sh --rollback", patched)
        self.assertEqual(
            patched.count(
                "unset VIDEO_STAGE_GUARD_REPO VIDEO_STAGE_GUARD_COMPOSE_FILE VIDEO_STAGE_DRAIN_MARKER"
            ),
            1,
        )
        self.assertLess(
            patched.index("unset VIDEO_STAGE_GUARD_REPO"),
            patched.index("/opt/travel-scanner-deploy/video_stage_drain.sh --normal"),
        )
        self.assertNotIn("\\opt\\travel-scanner-deploy", patched)
        self.assertNotIn("Roll back manually with:", patched)
        self.assertIn(host_patch.ROLLBACK_HOOK, patched)
        self.assertIn(host_patch.NORMAL_HOOK, patched)
        self.assertIn(host_patch.NO_ROLLBACK_HOOK, patched)
        with self.assertRaisesRegex(ValueError, "already mentions"):
            host_patch.patch_script(patched)

    def test_host_drift_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "exactly one"):
            host_patch.patch_script(host_patch.NORMAL_ANCHOR)

    @unittest.skipUnless(BASH, "bash required to exercise rendered host hook")
    def test_normal_refusal_restores_checkout_before_failure_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            helper = root / "refuse-helper"
            helper.write_text(
                "#!/usr/bin/env bash\n"
                'if [[ ${VIDEO_STAGE_GUARD_REPO+x} == x || '
                '${VIDEO_STAGE_GUARD_COMPOSE_FILE+x} == x || '
                '${VIDEO_STAGE_DRAIN_MARKER+x} == x ]]; then\n'
                '  : > "$FAKE_OVERRIDE_WITNESS"\n'
                "fi\nexit 3\n"
            )
            helper.chmod(0o755)
            git = root / "git"
            git.write_text(
                "#!/usr/bin/env bash\n"
                'case "$*" in\n'
                '  "reset --hard "*) [[ ${FAKE_RESET_FAIL:-0} == 1 ]] && exit 96; '
                'printf "%s" "$FAKE_LOCAL_SHA" > "$FAKE_HEAD" ;;\n'
                '  "rev-parse HEAD") cat "$FAKE_HEAD" ;;\n'
                '  "status --porcelain") exit 0 ;;\n'
                '  *) exit 97 ;;\n'
                'esac\n',
            )
            git.chmod(0o755)
            head = root / "head"
            head.write_text("b" * 40)
            hook = host_patch.NORMAL_HOOK.split('log "building and starting')[0]
            hook = hook.replace(host_patch.HELPER_LITERAL, '"$FAKE_HELPER"')
            hook = hook.replace("/run/travel-scanner-deploy", str(root))
            harness = (
                "set -euo pipefail\n"
                f"LOCAL_SHA={'a' * 40}\nBEHIND=1\nLOG_FILE=offline.log\n"
                'log() { printf "%s\\n" "$*"; }\n'
                'fail() { log "FAILED: $*"; exit 1; }\n'
                'ensure_readable() { :; }\n'
                + hook
                + 'printf "COMPOSE_REACHED\\n"\n'
            )
            env = {
                **os.environ,
                "PATH": f"{root}:{os.environ['PATH']}",
                "FAKE_HELPER": str(helper),
                "FAKE_HEAD": str(head),
                "FAKE_LOCAL_SHA": "a" * 40,
                "FAKE_OVERRIDE_WITNESS": str(root / "override-seen"),
                "VIDEO_STAGE_GUARD_REPO": str(root / "wrong-repo"),
                "VIDEO_STAGE_GUARD_COMPOSE_FILE": "wrong-compose.yml",
                "VIDEO_STAGE_DRAIN_MARKER": str(root / "wrong-marker"),
            }
            run = subprocess.run([str(BASH), "-c", harness], env=env, capture_output=True, text=True)
            self.assertEqual(run.returncode, 1, run.stderr)
            self.assertEqual(head.read_text(), "a" * 40)
            self.assertFalse((root / "override-seen").exists())
            self.assertIn("checkout restored to original SHA", run.stdout)
            self.assertIn("worker may be stopped", run.stdout)
            self.assertNotIn("COMPOSE_REACHED", run.stdout)

            head.write_text("b" * 40)
            run = subprocess.run(
                [str(BASH), "-c", harness],
                env={**env, "FAKE_RESET_FAIL": "1"},
                capture_output=True,
                text=True,
            )
            self.assertEqual(run.returncode, 1)
            self.assertEqual(head.read_text(), "b" * 40)
            self.assertIn("checkout reset failed", run.stdout)
            self.assertNotIn("checkout restored", run.stdout)
            self.assertNotIn("COMPOSE_REACHED", run.stdout)

    @unittest.skipUnless(os.name == "posix", "installer uses Linux flock")
    def test_failed_install_restores_original_under_the_same_lock(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            host = root / "deploy-travel-scanner.sh"
            original = (
                "#!/usr/bin/env bash\n"
                "rollback() {\n"
                + host_patch.ROLLBACK_ANCHOR
                + "}\n"
                + host_patch.NO_ROLLBACK_ANCHOR
                + host_patch.NORMAL_ANCHOR
                + "  false\nfi\n"
            ).encode()
            host.write_bytes(original)
            host.chmod(0o700)
            expected = hashlib.sha256(original).hexdigest()
            helper = root / "installed" / "drain.sh"
            lock = root / "deploy.lock"
            write = host_patch._write_atomic
            first_host_write = True

            def interrupted(path: Path, data: bytes, mode: int) -> None:
                nonlocal first_host_write
                if path == host and first_host_write:
                    first_host_write = False
                    write(path, b"truncated", mode)
                    raise OSError("simulated install interruption")
                write(path, data, mode)

            with mock.patch.object(host_patch, "_write_atomic", side_effect=interrupted):
                with self.assertRaisesRegex(OSError, "simulated install interruption"):
                    host_patch.install(host, expected, helper=helper, lock=lock)
            self.assertEqual(host.read_bytes(), original)
            self.assertEqual(host.stat().st_mode & 0o777, 0o700)
            backups = list(root.glob("deploy-travel-scanner.sh.before-video-stage-drain-*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), original)
            self.assertTrue(helper.exists())  # inert while the original script is restored


@unittest.skipUnless(BASH, "bash required for the Linux production helper")
class DrainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        (self.root / "docker-id").write_text("worker-one\n")
        (self.root / "running").write_text("true")
        (self.root / "exit-code").write_text("0")
        (self.root / "running-count").write_text("1")
        (self.root / "stop-delay").write_text("0")
        (self.root / "git-head").write_text("a" * 40)
        self.nonce = "12345678-1234-1234-1234-123456789abc"
        self.ready = self.root / f"video-ai-drain.ready.{self.nonce}"
        fake = self.bin / "docker"
        fake.write_text(
            """#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' "$*" >> "$FAKE_ROOT/calls"
if [[ $1 == compose && $* == *'ps --all -q video-ai-worker'* ]]; then
  cat "$FAKE_ROOT/docker-id"
elif [[ $1 == inspect ]]; then
  printf '%s|%s|false|null|["python","-m","app.video_automation.run_jobs"]\\n' \\
    "$(cat "$FAKE_ROOT/running")" "$(cat "$FAKE_ROOT/exit-code")"
elif [[ $1 == container && $2 == stop ]]; then
  [[ $* == *'--signal=SIGTERM --timeout=-1'* ]] || exit 91
  sleep "$(cat "$FAKE_ROOT/stop-delay")"
  printf false > "$FAKE_ROOT/running"
  if [[ -e "$FAKE_ROOT/settle-on-stop" ]]; then
    printf 0 > "$FAKE_ROOT/running-count"
  fi
  echo worker-one
elif [[ $1 == compose && $* == *'exec -T postgres psql'* ]]; then
  [[ $* == *"where status = 'running'"* ]] || exit 92
  [[ ! -e "$FAKE_ROOT/db-error" ]] || exit 93
  cat "$FAKE_ROOT/running-count"
else
  exit 94
fi
""",
            encoding="utf-8",
        )
        fake.chmod(0o755)
        fake_git = self.bin / "git"
        fake_git.write_text(
            "#!/usr/bin/env bash\n"
            '[[ $* == "rev-parse HEAD" ]] || exit 95\n'
            'cat "$FAKE_ROOT/git-head"\n',
            encoding="utf-8",
        )
        fake_git.chmod(0o755)

    def run_guard(self, mode: str = "--normal") -> tuple[subprocess.CompletedProcess[str], float]:
        env = {
            **os.environ,
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "FAKE_ROOT": str(self.root),
            "VIDEO_STAGE_GUARD_REPO": str(self.root),
            "VIDEO_STAGE_GUARD_COMPOSE_FILE": "compose.yml",
            "VIDEO_STAGE_DRAIN_MARKER": str(self.root / "drain.pending"),
            "VIDEO_STAGE_DRAIN_NONCE": self.nonce,
            "VIDEO_STAGE_DRAIN_LOCAL_SHA": "a" * 40,
            "VIDEO_STAGE_DRAIN_READY_FILE": str(self.ready),
        }
        started = time.monotonic()
        result = subprocess.run(  # noqa: S603
            [str(BASH), str(SCRIPT), mode], capture_output=True, text=True, env=env, check=False
        )
        return result, time.monotonic() - started

    def calls(self) -> str:
        return (self.root / "calls").read_text(encoding="utf-8")

    def test_job_arriving_after_preflight_finishes_before_recreation(self) -> None:
        # The stage became running after the separate human/timer preflight.
        # The final barrier waits for the RQ horse, then sees the committed reply.
        (self.root / "settle-on-stop").touch()
        (self.root / "stop-delay").write_text("1.1")
        result, duration = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertGreaterEqual(duration, 1.09)
        self.assertIn("worker stopped cleanly; running jobs=0", result.stdout)
        self.assertIn("container stop --signal=SIGTERM --timeout=-1 worker-one", self.calls())
        self.assertFalse((self.root / "drain.pending").exists())
        self.assertEqual(self.ready.read_text(), f"{'a' * 40}\nworker-one\n")

    def test_queued_and_uncertain_do_not_block(self) -> None:
        (self.root / "running").write_text("false")
        (self.root / "running-count").write_text("0")
        result, _ = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("container stop", self.calls())

    def test_stale_running_receipt_fails_closed_after_drain(self) -> None:
        result, _ = self.run_guard()
        self.assertEqual(result.returncode, 3)
        self.assertIn("1 running stage job(s) remain", result.stderr)
        self.assertEqual((self.root / "drain.pending").read_text().strip(), "worker-one")
        # A second invocation must not send RQ the second SIGTERM, which would
        # force-kill a horse still draining after an interrupted deploy shell.
        again, _ = self.run_guard()
        self.assertEqual(again.returncode, 3)
        self.assertIn("previous warm drain is unresolved", again.stderr)
        self.assertEqual(self.calls().count("container stop"), 1)

    def test_db_failure_or_missing_worker_fails_closed(self) -> None:
        (self.root / "db-error").touch()
        result, _ = self.run_guard()
        self.assertEqual(result.returncode, 3)
        self.assertIn("cannot read running", result.stderr)
        (self.root / "drain.pending").unlink()  # isolate the next refusal condition
        (self.root / "docker-id").write_text("")
        result, _ = self.run_guard()
        self.assertEqual(result.returncode, 3)
        self.assertIn("expected one", result.stderr)

    def test_partial_compose_zero_worker_can_rollback_only_after_exact_drain(self) -> None:
        (self.root / "settle-on-stop").touch()
        normal, _ = self.run_guard()
        self.assertEqual(normal.returncode, 0, normal.stderr)
        (self.root / "docker-id").write_text("")  # compose removed worker, then failed
        rollback, _ = self.run_guard("--rollback")
        self.assertEqual(rollback.returncode, 0, rollback.stderr)
        self.assertIn("mode=--rollback; zero-worker=1", rollback.stdout)
        self.assertEqual(self.calls().count("container stop"), 1)

    def test_rollback_drains_recreated_worker_before_old_image(self) -> None:
        (self.root / "settle-on-stop").touch()
        normal, _ = self.run_guard()
        self.assertEqual(normal.returncode, 0, normal.stderr)
        (self.root / "docker-id").write_text("worker-two\n")
        (self.root / "running").write_text("true")
        (self.root / "running-count").write_text("1")
        rollback, _ = self.run_guard("--rollback")
        self.assertEqual(rollback.returncode, 0, rollback.stderr)
        self.assertIn("mode=--rollback; zero-worker=0", rollback.stdout)
        self.assertIn("container stop --signal=SIGTERM --timeout=-1 worker-two", self.calls())

    def test_zero_worker_rollback_requires_receipt_and_running_zero(self) -> None:
        (self.root / "docker-id").write_text("")
        (self.root / "running-count").write_text("0")
        no_receipt, _ = self.run_guard("--rollback")
        self.assertEqual(no_receipt.returncode, 3)
        self.assertIn("no successful normal drain receipt", no_receipt.stderr)
        normal, _ = self.run_guard()
        self.assertEqual(normal.returncode, 3)
        self.assertIn("expected one", normal.stderr)
        self.ready.write_text(f"{'b' * 40}\nworker-one\n")
        wrong_sha, _ = self.run_guard("--rollback")
        self.assertEqual(wrong_sha.returncode, 3)
        self.assertIn("does not match", wrong_sha.stderr)
        self.ready.write_text(f"{'a' * 40}\nworker-one\n")
        (self.root / "running-count").write_text("1")
        running, _ = self.run_guard("--rollback")
        self.assertEqual(running.returncode, 3)
        self.assertIn("1 running stage job", running.stderr)

    def test_rollback_checks_original_checkout_even_with_receipt(self) -> None:
        self.ready.write_text(f"{'a' * 40}\nworker-one\n")
        (self.root / "git-head").write_text("b" * 40)
        result, _ = self.run_guard("--rollback")
        self.assertEqual(result.returncode, 3)
        self.assertIn("rollback checkout is not the original SHA", result.stderr)


if __name__ == "__main__":
    unittest.main()
