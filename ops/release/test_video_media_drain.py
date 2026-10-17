"""Offline media deploy barrier tests; fake Docker, DB and Redis, never a vendor call."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import video_media_host_patch as media_patch
import video_stage_host_patch as stage_patch

SCRIPT = Path(__file__).with_name("video_media_drain.sh")
BASH = shutil.which("bash") if os.name == "posix" else None
NONCE = "12345678-1234-1234-1234-123456789abc"
SHA = "a" * 40


class HostPatchTests(unittest.TestCase):
    @staticmethod
    def stage_patched() -> str:
        original = (
            "#!/usr/bin/env bash\n"
            "rollback() {\n"
            + stage_patch.ROLLBACK_ANCHOR
            + "}\n"
            + stage_patch.NO_ROLLBACK_ANCHOR
            + stage_patch.NORMAL_ANCHOR
            + "  false\nfi\n"
        )
        return stage_patch.patch_script(original)

    def test_incremental_patch_guards_both_up_sites_and_prebuilds(self) -> None:
        before = self.stage_patched()
        after = media_patch.patch_script(before)
        self.assertEqual(after.count(media_patch.HELPER_LITERAL), 3)
        self.assertEqual(after.count(stage_patch.HELPER_LITERAL), 2)
        self.assertEqual(after.count("compose up --no-build -d"), 2)
        self.assertEqual(after.count("compose build"), 2)
        self.assertEqual(after.count("compose up --build -d"), 0)
        normal = after[after.index("VIDEO_MEDIA_DRAIN_NONCE=$VIDEO_STAGE_DRAIN_NONCE") :]
        self.assertLess(
            normal.index(f"{media_patch.HELPER_LITERAL} --precheck"),
            normal.index("compose build"),
        )
        self.assertLess(
            normal.index("compose build"),
            normal.index(f"{stage_patch.HELPER_LITERAL} --normal"),
        )
        self.assertLess(
            normal.index(f"{stage_patch.HELPER_LITERAL} --normal"),
            normal.index(f"{media_patch.HELPER_LITERAL} --normal"),
        )
        self.assertLess(
            normal.index(f"{media_patch.HELPER_LITERAL} --normal"),
            normal.index("compose up --no-build -d"),
        )
        self.assertIn("VIDEO_MEDIA_DRAIN_READY_FILE", after)
        self.assertIn("API may be stopped", after)
        with self.assertRaisesRegex(ValueError, "already mentions"):
            media_patch.patch_script(after)
        if BASH:
            subprocess.run([BASH, "-n"], input=after, text=True, check=True)

    def test_unpatched_or_drifted_stage_script_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "not the reviewed"):
            media_patch.patch_script(stage_patch.NORMAL_ANCHOR)
        changed = self.stage_patched().replace(
            "compose up --build -d", "compose up -d", 1
        )
        with self.assertRaisesRegex(ValueError, "reviewed"):
            media_patch.patch_script(changed)

    @unittest.skipUnless(os.name == "posix", "installer requires Linux flock")
    def test_install_refuses_stage_helper_drift_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            host = root / "deploy.sh"
            host.write_text(self.stage_patched(), encoding="utf-8")
            host.chmod(0o700)
            stage_helper = root / "stage.sh"
            stage_helper.write_text("wrong", encoding="utf-8")
            stage_helper.chmod(0o700)
            old = host.read_bytes()
            with self.assertRaisesRegex(ValueError, "not the reviewed bytes"):
                media_patch.install(
                    host,
                    hashlib.sha256(old).hexdigest(),
                    stage_helper=stage_helper,
                    helper=root / "media.sh",
                    lock=root / "deploy.lock",
                )
            self.assertEqual(host.read_bytes(), old)
            self.assertFalse((root / "media.sh").exists())

    @unittest.skipUnless(os.name == "posix", "installer requires Linux flock")
    def test_install_refuses_new_media_helper_drift_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            host = root / "deploy.sh"
            host.write_text(self.stage_patched(), encoding="utf-8")
            host.chmod(0o700)
            stage_helper = root / "stage.sh"
            stage_helper.write_bytes(
                Path(stage_patch.__file__).with_name("video_stage_drain.sh").read_bytes()
            )
            stage_helper.chmod(0o700)
            old = host.read_bytes()
            with (
                patch.object(media_patch, "HELPER_SHA256", "0" * 64),
                self.assertRaisesRegex(ValueError, "media helper bytes"),
            ):
                media_patch.install(
                    host,
                    hashlib.sha256(old).hexdigest(),
                    stage_helper=stage_helper,
                    helper=root / "media.sh",
                    lock=root / "deploy.lock",
                )
            self.assertEqual(host.read_bytes(), old)
            self.assertFalse((root / "media.sh").exists())

    @unittest.skipUnless(os.name == "posix", "installer requires Linux flock")
    def test_install_pins_media_helper_and_reads_back_host_script(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            host = root / "deploy.sh"
            host.write_text(self.stage_patched(), encoding="utf-8")
            host.chmod(0o700)
            stage_helper = root / "stage.sh"
            stage_helper.write_bytes(
                Path(stage_patch.__file__).with_name("video_stage_drain.sh").read_bytes()
            )
            stage_helper.chmod(0o700)
            old = host.read_bytes()
            helper = root / "media.sh"
            backup = media_patch.install(
                host,
                hashlib.sha256(old).hexdigest(),
                stage_helper=stage_helper,
                helper=helper,
                lock=root / "deploy.lock",
            )
            self.assertEqual(backup.read_bytes(), old)
            self.assertEqual(helper.read_bytes(), SCRIPT.read_bytes())
            self.assertEqual(host.read_bytes(), media_patch.patch_script(old.decode()).encode())
            self.assertEqual(host.stat().st_mode & 0o777, 0o700)
            self.assertEqual(helper.stat().st_mode & 0o777, 0o700)


@unittest.skipUnless(BASH, "Linux bash required for host helper fake-Docker tests")
class MediaDrainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self._put("api-id", "api-one\n")
        self._put("running", "true")
        self._put("exit-code", "0")
        self._put("version", "0.52.4|None|1|auto|None")
        self._put("git-head", SHA)
        for index in (1, 2, 3):
            self._put(f"queued-{index}", "0")
            self._put(f"locks-{index}", "")
        self.marker = self.root / "video-api-drain.pending"
        self.ready = self.root / f"video-api-drain.ready.{NONCE}"
        fake = self.bin / "docker"
        fake.write_text(
            """#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' "$*" >> "$FAKE_ROOT/calls"
if [[ $1 == compose && $* == *'ps --all -q api'* ]]; then
  if [[ ! -e "$FAKE_ROOT/api-absent" ]]; then cat "$FAKE_ROOT/api-id"; fi
elif [[ $1 == inspect && $* == *'.HostConfig.LogConfig.Type'* ]]; then
  printf 'json-file\\n'
elif [[ $1 == inspect ]]; then
  printf '%s|%s|false|null|["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]\\n' \\
    "$(cat "$FAKE_ROOT/running")" "$(cat "$FAKE_ROOT/exit-code")"
elif [[ $1 == compose && $* == *'exec -T postgres psql'* ]]; then
  n=1
  [[ ! -e "$FAKE_ROOT/queued-index" ]] || n=$(( $(cat "$FAKE_ROOT/queued-index") + 1 ))
  printf '%s' "$n" > "$FAKE_ROOT/queued-index"
  [[ ! -e "$FAKE_ROOT/db-error" ]] || exit 91
  cat "$FAKE_ROOT/queued-$n"
elif [[ $1 == compose && $* == *'exec -T redis sh -c'* ]]; then
  n=1
  [[ ! -e "$FAKE_ROOT/locks-index" ]] || n=$(( $(cat "$FAKE_ROOT/locks-index") + 1 ))
  printf '%s' "$n" > "$FAKE_ROOT/locks-index"
  [[ ! -e "$FAKE_ROOT/redis-error" ]] || exit 92
  cat "$FAKE_ROOT/locks-$n"
elif [[ $1 == compose && $* == *'exec -T api python -c'* ]]; then
  cat "$FAKE_ROOT/version"
elif [[ $1 == logs && $* == *'--tail 1'* ]]; then
  [[ ${4:-} == "$(cat "$FAKE_ROOT/api-id")" ]] || exit 99
  [[ ! -e "$FAKE_ROOT/prelog-error" ]] || exit 97
  printf 'INFO:     Started server process [1]\\n'
elif [[ $1 == logs && $* == *'--since '* ]]; then
  [[ ${4:-} == "$(cat "$FAKE_ROOT/api-id")" ]] || exit 99
  [[ ${3:-} =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{9}Z$ ]] || exit 99
  [[ $(tail -n 1 "$FAKE_ROOT/video-api-drain.pending") == "$3" ]] || exit 99
  [[ ! -e "$FAKE_ROOT/postlog-error" ]] || exit 98
  [[ ! -e "$FAKE_ROOT/stale-logs" ]] || exit 0
  if [[ -e "$FAKE_ROOT/reordered-logs" ]]; then
    printf 'INFO:     Finished server process [1]\\n'
    printf 'INFO:     Application shutdown complete.\\n'
    exit 0
  fi
  [[ -e "$FAKE_ROOT/missing-lifespan" ]] || printf 'INFO:     Application shutdown complete.\\n'
  [[ -e "$FAKE_ROOT/missing-finish" ]] || printf 'INFO:     Finished server process [1]\\n'
elif [[ $1 == container && $2 == stop ]]; then
  [[ $* == *'--signal=SIGTERM --timeout=-1'* ]] || exit 93
  : > "$FAKE_ROOT/stop-called"
  [[ ! -e "$FAKE_ROOT/stop-error" ]] || exit 94
  printf false > "$FAKE_ROOT/running"
  if [[ -e "$FAKE_ROOT/stop-exit-code" ]]; then
    cat "$FAKE_ROOT/stop-exit-code" > "$FAKE_ROOT/exit-code"
  else
    printf 143 > "$FAKE_ROOT/exit-code"
  fi
  cat "$FAKE_ROOT/api-id"
else
  exit 95
fi
""",
            encoding="utf-8",
        )
        fake.chmod(0o755)
        git = self.bin / "git"
        git.write_text(
            "#!/usr/bin/env bash\n"
            '[[ $* == "rev-parse HEAD" ]] || exit 96\n'
            'cat "$FAKE_ROOT/git-head"\n',
            encoding="utf-8",
        )
        git.chmod(0o755)

    def _put(self, name: str, value: str) -> None:
        (self.root / name).write_text(value, encoding="utf-8")

    def run_guard(self, mode: str = "--normal") -> subprocess.CompletedProcess[str]:
        env = {
            **os.environ,
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "FAKE_ROOT": str(self.root),
            "VIDEO_MEDIA_GUARD_REPO": str(self.root),
            "VIDEO_MEDIA_GUARD_COMPOSE_FILE": "docker-compose.prod.yml",
            "VIDEO_MEDIA_DRAIN_MARKER": str(self.marker),
            "VIDEO_MEDIA_DRAIN_NONCE": NONCE,
            "VIDEO_MEDIA_DRAIN_LOCAL_SHA": SHA,
            "VIDEO_MEDIA_DRAIN_READY_FILE": str(self.ready),
        }
        return subprocess.run(
            [BASH, str(SCRIPT), mode], env=env, capture_output=True, text=True, check=False
        )

    def test_existing_queued_job_refuses_before_api_stop(self) -> None:
        self._put("queued-1", "1")
        result = self.run_guard("--precheck")
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn("1 queued media job", result.stderr)
        self.assertFalse((self.root / "stop-called").exists())
        self.assertFalse(self.marker.exists())
        self.assertFalse(self.ready.exists())

    def test_arrival_after_first_precheck_refuses_before_sigterm(self) -> None:
        self._put("queued-2", "1")
        result = self.run_guard()
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertFalse((self.root / "stop-called").exists())
        self.assertFalse(self.marker.exists())

    def test_arrival_during_sigterm_is_a_hard_poststop_hold(self) -> None:
        self._put("queued-3", "1")
        result = self.run_guard()
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertTrue((self.root / "stop-called").exists())
        self.assertTrue(self.marker.exists())
        self.assertFalse(self.ready.exists())
        self.assertIn("queued media job", result.stderr)

    def test_unresolved_redis_lock_refuses_before_stop_or_after_stop(self) -> None:
        self._put("locks-1", "video-media:lock:old-id")
        result = self.run_guard()
        self.assertEqual(result.returncode, 3)
        self.assertFalse((self.root / "stop-called").exists())
        self._put("locks-1", "")
        self._put("locks-3", "video-media:lock:interrupted-id")
        (self.root / "queued-index").unlink()
        (self.root / "locks-index").unlink()
        result = self.run_guard()
        self.assertEqual(result.returncode, 3)
        self.assertTrue(self.marker.exists())
        self.assertFalse(self.ready.exists())

    def test_sigterm_error_keeps_marker_and_blocks_a_second_signal(self) -> None:
        self._put("stop-error", "1")
        result = self.run_guard()
        self.assertEqual(result.returncode, 3)
        self.assertTrue(self.marker.exists())
        self.assertFalse(self.ready.exists())
        self._put("stop-error", "")
        again = self.run_guard()
        self.assertEqual(again.returncode, 3)
        self.assertEqual((self.root / "calls").read_text().count("container stop"), 1)

    def test_missing_lifespan_completion_holds_stopped_api(self) -> None:
        self._put("missing-lifespan", "1")
        result = self.run_guard()
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn("graceful completion lines missing", result.stderr)
        self.assertTrue(self.marker.exists())
        self.assertFalse(self.ready.exists())
        self.assertEqual((self.root / "exit-code").read_text(), "143")

    def test_stale_or_reordered_completion_logs_hold_stopped_api(self) -> None:
        for flag in ("stale-logs", "reordered-logs", "missing-finish"):
            with self.subTest(flag=flag):
                self._put(flag, "1")
                result = self.run_guard()
                self.assertEqual(result.returncode, 3, result.stderr)
                self.assertIn("graceful completion lines missing", result.stderr)
                self.assertTrue(self.marker.exists())
                self.assertFalse(self.ready.exists())
                (self.root / flag).unlink()
                self.marker.unlink()
                self._put("running", "true")
                (self.root / "queued-index").unlink()
                (self.root / "locks-index").unlink()

    def test_wrong_signal_exit_status_holds_stopped_api(self) -> None:
        for code in ("0", "137"):
            with self.subTest(code=code):
                self._put("stop-exit-code", code)
                result = self.run_guard()
                self.assertEqual(result.returncode, 3, result.stderr)
                self.assertIn("API did not exit cleanly", result.stderr)
                self.assertTrue(self.marker.exists())
                self.assertFalse(self.ready.exists())
                self.marker.unlink()
                self._put("running", "true")
                (self.root / "queued-index").unlink()
                (self.root / "locks-index").unlink()

    def test_unreadable_logs_refuse_before_api_stop(self) -> None:
        self._put("prelog-error", "1")
        result = self.run_guard()
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertFalse((self.root / "stop-called").exists())
        self.assertFalse(self.marker.exists())

    def test_clean_drain_records_receipt_for_rollback(self) -> None:
        result = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.marker.exists())
        self.assertEqual(self.ready.read_text(), f"{SHA}\napi-one\n")
        self.assertIn("--timeout=-1", (self.root / "calls").read_text())
        # A failed compose may leave no API container. Only this same nonce's
        # normal receipt authorizes rollback through that zero-container state.
        self._put("api-absent", "1")
        (self.root / "queued-index").unlink()
        (self.root / "locks-index").unlink()
        rollback = self.run_guard("--rollback")
        self.assertEqual(rollback.returncode, 0, rollback.stderr)
        self.assertIn("zero-API=1", rollback.stdout)

    def test_rollback_accepts_only_same_stopped_api_after_normal_receipt(self) -> None:
        normal = self.run_guard()
        self.assertEqual(normal.returncode, 0, normal.stderr)
        (self.root / "queued-index").unlink()
        (self.root / "locks-index").unlink()
        rollback = self.run_guard("--rollback")
        self.assertEqual(rollback.returncode, 0, rollback.stderr)
        self.assertIn("zero-API=0", rollback.stdout)
        self.assertEqual((self.root / "calls").read_text().count("container stop"), 1)

    def test_rollback_requires_matching_receipt_and_original_checkout(self) -> None:
        missing = self.run_guard("--rollback")
        self.assertEqual(missing.returncode, 3)
        self.assertFalse((self.root / "stop-called").exists())
        self.ready.write_text(f"{SHA}\napi-one\n", encoding="utf-8")
        self._put("git-head", "b" * 40)
        wrong = self.run_guard("--rollback")
        self.assertEqual(wrong.returncode, 3)
        self.assertFalse((self.root / "stop-called").exists())

    def test_version_drift_refuses_before_api_stop(self) -> None:
        self._put("version", "0.52.4|None|2|auto|None")
        result = self.run_guard()
        self.assertEqual(result.returncode, 3)
        self.assertFalse((self.root / "stop-called").exists())
        self.assertFalse(self.marker.exists())


if __name__ == "__main__":
    unittest.main()
