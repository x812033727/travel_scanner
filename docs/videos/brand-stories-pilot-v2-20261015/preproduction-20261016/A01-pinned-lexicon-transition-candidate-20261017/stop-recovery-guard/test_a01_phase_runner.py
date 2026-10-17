"""Local byte-tree and one-off preflight checks; Docker is never contacted."""

import hashlib
import io
import json
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
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


class MediaFenceJobsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fenced = {"id": runner.FENCED_MEDIA_JOB_ID,
                       "slug": "google-project-suncatcher-prototype-what-it-tests",
                       "request_hash": "1" * 64, "kind": "image", "provider": "minimax",
                       "model": "image-01", "status": "queued"}
        self.media = {**self.fenced, "vendor_ref": None, "submitted_at": None}
        self.code = {"jobs_sha256": "2" * 64,
                     "dispatch_fence_sha256": "3" * 64,
                     "dispatch_fence_cli_sha256": "4" * 64}
        self.manifest = {"fenced_media_job": self.fenced, "api_container_id": "5" * 64,
                         "api_image_id": "sha256:" + "6" * 64, "api_code": self.code,
                         "media_dispatch_fence_sha256": "7" * 64}
        self.receipt = {
            "schema_version": 1, "enforced": True,
            "operator_lock_expected": True,
            "media_lock_absent": False, "active_media_count": 1,
            "fence_sha256": self.manifest["media_dispatch_fence_sha256"],
            "fence_path": runner.FENCE_PATH_PREFIX + self.fenced["id"] + ".json",
            "job": self.media,
            "code": {key: self.code[key] for key in ("jobs_sha256", "dispatch_fence_sha256")},
        }

    def _run(self, media: list[dict], *, receipt: dict | None = None,
             api_id: str | None = None, api_image: str | None = None,
             source_sha: str | None = None) -> dict:
        db = {"stage": 0, "a01": 0, "media": media}
        hashes = {path: self.code[key] for key, path in runner.API_SOURCE_PATHS.items()}

        def fake_command(*args: str, **_kwargs: object) -> str:
            if args[:4] == ("docker", "inspect", "--format", "{{.Image}}"):
                return api_image or self.manifest["api_image_id"]
            if args[:4] == ("docker", "exec", self.manifest["api_container_id"], "python"):
                self.assertEqual(args[-3:], ("--job-id", self.fenced["id"],
                                             "--expect-operator-lock"))
                return json.dumps(self.receipt if receipt is None else receipt)
            self.fail(f"unexpected command: {args}")

        with patch.object(runner, "sql", return_value=json.dumps(db)), \
             patch.object(runner, "container_id", return_value=api_id or self.manifest["api_container_id"]), \
             patch.object(runner, "running", return_value=True), \
             patch.object(runner, "worker_file", side_effect=lambda path, _: source_sha or hashes[path]), \
             patch.object(runner, "held_nonce") as held, \
             patch.object(runner, "command", side_effect=fake_command):
            result = runner.jobs(self.manifest)
            self.assertEqual(held.call_count, 2)
            return result

    def test_zero_media_jobs_preserves_original_path_without_fence(self) -> None:
        with patch.object(runner, "sql", return_value=json.dumps(
            {"stage": 0, "a01": 0, "media": []})), \
             patch.object(runner, "container_id", side_effect=AssertionError("API queried")):
            self.assertEqual(runner.jobs({"fenced_media_job": None})["media"], [])
            with self.assertRaisesRegex(RuntimeError, "disappeared or changed status"):
                runner.jobs(self.manifest)

    def test_running_stage_job_remains_hard_block(self) -> None:
        with patch.object(runner, "sql", return_value=json.dumps(
            {"stage": 1, "a01": 0, "media": []})):
            with self.assertRaisesRegex(RuntimeError, "stage job not settled"):
                runner.jobs({"fenced_media_job": None})

    def test_only_exact_queued_row_with_live_api_receipt_passes(self) -> None:
        self.assertEqual(self._run([self.media])["media"], [self.media])

    def test_second_row_or_submitted_or_hash_drift_refused(self) -> None:
        for media in ([self.media, {**self.media, "id": "8" * 36}],
                      [{**self.media, "status": "submitted"}],
                      [{**self.media, "request_hash": "9" * 64}]):
            with self.subTest(media=media), self.assertRaisesRegex(RuntimeError, "single fenced"):
                self._run(media)

    def test_missing_fence_receipt_or_api_identity_refused(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "API container ID/state drift"):
            self._run([self.media], api_id="8" * 64)
        with self.assertRaisesRegex(RuntimeError, "API image ID drift"):
            self._run([self.media], api_image="sha256:" + "8" * 64)
        with self.assertRaisesRegex(RuntimeError, "source drift"):
            self._run([self.media], source_sha="8" * 64)
        with self.assertRaisesRegex(RuntimeError, "receipt drift"):
            self._run([self.media], receipt={**self.receipt, "enforced": False})
        with self.assertRaisesRegex(RuntimeError, "receipt drift"):
            self._run([self.media], receipt={**self.receipt, "fence_sha256": "8" * 64})
        with self.assertRaisesRegex(RuntimeError, "receipt drift"):
            self._run([self.media], receipt={**self.receipt, "media_lock_absent": True})
        with self.assertRaisesRegex(RuntimeError, "receipt drift"):
            self._run([self.media], receipt={**self.receipt, "operator_lock_expected": False})
        with self.assertRaisesRegex(RuntimeError, "receipt drift"):
            self._run([self.media], receipt={**self.receipt, "active_media_count": 2})


class HeldNonceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.redis_id = "a" * 64
        self.nonce = b"b" * 64
        self.script = b"#!/bin/bash\nexit 0\n"
        self.private_dir = "/root/mokaair-a01-media-fence-123456789abc"
        self.script_path = self.private_dir + "/monitor-lock.sh"
        self.receipt_path = self.private_dir + "/nonce-receipt.json"
        self.argv = ("/bin/bash", self.script_path, "--receipt", self.receipt_path,
                     "--redis-container-id", self.redis_id)
        self.execstart = ("{ path=/bin/bash ; argv[]=" + " ".join(self.argv)
                          + " ; ignore_errors=no ; }")
        self.manifest = {"redis_container_id": self.redis_id,
                         "redis_image_id": "sha256:" + "c" * 64,
                         "nonce_sha256": hashlib.sha256(self.nonce).hexdigest(),
                         "nonce_receipt_path": self.receipt_path,
                         "nonce_watcher_pid": 1234,
                         "nonce_watcher_script_path": self.script_path,
                         "nonce_watcher_script_sha256": hashlib.sha256(self.script).hexdigest(),
                         "nonce_watcher_execstart_sha256":
                         hashlib.sha256(self.execstart.encode()).hexdigest()}

    def _watcher(self, heartbeat: dict, *, pid: str = "1234",
                 script: bytes | None = None, execstart: str | None = None,
                 cmdline: bytes | None = None) -> None:
        script_bytes = self.script if script is None else script
        proc_bytes = ("\0".join(self.argv) + "\0").encode() if cmdline is None else cmdline
        parent = SimpleNamespace(st_mode=stat.S_IFDIR | 0o700, st_uid=0)
        script_info = SimpleNamespace(st_mode=stat.S_IFREG | 0o700, st_uid=0,
                                      st_nlink=1, st_size=len(script_bytes))
        outputs = ["active", pid, self.execstart if execstart is None else execstart]
        with patch.object(runner, "command", side_effect=outputs), \
             patch.object(Path, "lstat", return_value=parent), \
             patch.object(runner.os, "open", return_value=3), \
             patch.object(runner.os, "fstat", return_value=script_info), \
             patch.object(runner.os, "read", return_value=script_bytes), \
             patch.object(runner.os, "close"), \
             patch.object(Path, "read_bytes", return_value=proc_bytes), \
             patch.object(runner, "private_json", return_value=(heartbeat,
                                                                  SimpleNamespace(st_mtime=time.time()))):
            runner.nonce_watcher(self.manifest, self.redis_id)

    def _verify(self, redis_reads: list[bytes]) -> None:
        with patch.object(runner, "container_id", return_value=self.redis_id), \
             patch.object(runner, "running", return_value=True), \
             patch.object(runner, "command", return_value=self.manifest["redis_image_id"]), \
             patch.object(runner, "private_receipt", return_value=({}, self.nonce)), \
             patch.object(runner, "redis_private_read", side_effect=redis_reads) as redis, \
             patch.object(runner, "nonce_watcher") as watcher:
            runner.held_nonce(self.manifest)
            self.assertEqual([call.args[1] for call in redis.call_args_list], ["GET", "PTTL"])
            watcher.assert_called_once_with(self.manifest, self.redis_id)

    def test_exact_nonce_no_expiry_and_watcher_required(self) -> None:
        self._verify([self.nonce, b"-1"])
        for values, message in (([b"d" * 64, b"-1"], "ownership drift"),
                                ([self.nonce, b"100"], "gained expiry")):
            with self.subTest(values=values), self.assertRaisesRegex(RuntimeError, message):
                self._verify(values)

    def test_watcher_fresh_heartbeat_and_active_pid_required(self) -> None:
        heartbeat = {"schema_version": 1, "job_id": runner.FENCED_MEDIA_JOB_ID,
                     "redis_container_id": self.redis_id,
                     "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "checks": 10, "nonce_sha256": self.manifest["nonce_sha256"],
                     "owned": True, "no_expiry": True}
        self._watcher(heartbeat)
        stale = {**heartbeat, "checked_at_utc": "2020-01-01T00:00:00Z"}
        with self.assertRaisesRegex(RuntimeError, "heartbeat stale"):
            self._watcher(stale)
        with self.assertRaisesRegex(RuntimeError, "watcher PID drift"):
            self._watcher(heartbeat, pid="4321")
        with self.assertRaisesRegex(RuntimeError, "watcher script SHA drift"):
            self._watcher(heartbeat, script=b"#!/bin/bash\nexit 1\n")
        with self.assertRaisesRegex(RuntimeError, "watcher ExecStart drift"):
            self._watcher(heartbeat, execstart=self.execstart.replace("/bin/bash", "/bin/sh"))
        with self.assertRaisesRegex(RuntimeError, "watcher process command drift"):
            self._watcher(heartbeat, cmdline=b"/bin/bash\0wrong-script\0")

    def test_private_receipt_hash_mode_and_nonce_binding(self) -> None:
        receipt = {"schema_version": 1, "job_id": runner.FENCED_MEDIA_JOB_ID,
                   "key": runner.MEDIA_LOCK_KEY, "nonce": self.nonce.decode("ascii"),
                   "durable": True, "waitaof_local": 1}
        raw = json.dumps(receipt).encode()
        manifest = {**self.manifest,
                    "nonce_receipt_path": "/root/mokaair-a01-media-fence-123456789abc/nonce-receipt.json",
                    "nonce_receipt_sha256": hashlib.sha256(raw).hexdigest()}
        directory = SimpleNamespace(st_mode=stat.S_IFDIR | 0o700, st_uid=0)
        file_info = SimpleNamespace(st_mode=stat.S_IFREG | 0o600, st_uid=0,
                                    st_nlink=1, st_size=len(raw))
        with patch.object(Path, "lstat", return_value=directory), \
             patch.object(runner.os, "open", return_value=3), \
             patch.object(runner.os, "fstat", return_value=file_info), \
             patch.object(runner.os, "read", return_value=raw), \
             patch.object(runner.os, "close"):
            self.assertEqual(runner.private_receipt(manifest)[1], self.nonce)
            with self.assertRaisesRegex(RuntimeError, "receipt SHA drift"):
                runner.private_receipt({**manifest, "nonce_receipt_sha256": "0" * 64})


        wrong_mode = SimpleNamespace(st_mode=stat.S_IFREG | 0o644, st_uid=0,
                                     st_nlink=1, st_size=len(raw))
        with patch.object(Path, "lstat", return_value=directory), \
             patch.object(runner.os, "open", return_value=3), \
             patch.object(runner.os, "fstat", return_value=wrong_mode), \
             patch.object(runner.os, "close"):
            with self.assertRaisesRegex(RuntimeError, "ownership, mode or size drift"):
                runner.private_receipt(manifest)

    def test_redis_read_never_echoes_nonce_on_error(self) -> None:
        failure = subprocess.CompletedProcess(("docker", "exec"), 1, self.nonce, self.nonce)
        with patch.object(runner.subprocess, "run", return_value=failure):
            with self.assertRaisesRegex(RuntimeError, "private Redis nonce read failed") as caught:
                runner.redis_private_read(self.redis_id, "GET")
            self.assertNotIn(self.nonce.decode(), str(caught.exception))


class CutoverHoldTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = "/root/mokaair-a01-media-fence-123456789abc"
        self.manifest = {
            "expected_head": "a" * 40,
            "cutover_handoff_path": self.directory + "/handoff.json",
            "nonce_receipt_path": self.directory + "/nonce-receipt.json",
            "fenced_media_job": {"id": runner.FENCED_MEDIA_JOB_ID},
            "redis_container_id": "b" * 64,
            "redis_image_id": "sha256:" + "c" * 64,
            "api_container_id": "d" * 64,
            "api_image_id": "sha256:" + "e" * 64,
            "nonce_watcher_unit": runner.NONCE_WATCHER_UNIT,
            "nonce_watcher_pid": 1234,
            "nonce_watcher_script_path": self.directory + "/monitor-lock.sh",
            "nonce_watcher_script_sha256": "1" * 64,
            "nonce_watcher_execstart_sha256": "2" * 64,
            "nonce_sha256": "3" * 64,
            "nonce_receipt_sha256": "4" * 64,
            "nonce_heartbeat_path": str(runner.NONCE_HEARTBEAT),
            "media_dispatch_fence_sha256": "5" * 64,
            "api_code": {"dispatch_fence_cli_sha256": "6" * 64},
        }
        self.hold_record = {
            "target": self.manifest["expected_head"],
            "release_dir": self.directory,
            "owner": runner.CUTOVER_HOLD_OWNER,
            "phases": runner.CUTOVER_HOLD_PHASES,
            "created_at": "2026-10-17T16:00:00+00:00",
        }
        self.hold_raw = ("owned by A01\n" + json.dumps(self.hold_record) + "\n").encode()
        self.handoff = {
            "schema_version": 1,
            "target_sha": self.manifest["expected_head"],
            "plan_sha256": "7" * 64,
            "job_id": runner.FENCED_MEDIA_JOB_ID,
            "redis_id": self.manifest["redis_container_id"],
            "redis_image": self.manifest["redis_image_id"],
            "api_id": self.manifest["api_container_id"],
            "api_image": self.manifest["api_image_id"],
            "watcher_unit": self.manifest["nonce_watcher_unit"],
            "watcher_main_pid": self.manifest["nonce_watcher_pid"],
            "nonce_watcher_script_path": self.manifest["nonce_watcher_script_path"],
            "nonce_watcher_script_sha256": self.manifest["nonce_watcher_script_sha256"],
            "nonce_watcher_execstart_sha256": self.manifest["nonce_watcher_execstart_sha256"],
            "nonce_sha256": self.manifest["nonce_sha256"],
            "nonce_receipt_sha256": self.manifest["nonce_receipt_sha256"],
            "nonce_receipt_path": self.manifest["nonce_receipt_path"],
            "nonce_heartbeat_path": self.manifest["nonce_heartbeat_path"],
            "nonce_retained": True,
            "hold_path": str(runner.CUTOVER_HOLD_PATH),
            "hold_release_dir": self.directory,
            "hold_sha256": hashlib.sha256(self.hold_raw).hexdigest(),
            "hold_owner": runner.CUTOVER_HOLD_OWNER,
            "hold_phases": runner.CUTOVER_HOLD_PHASES,
            "hold_created_at": self.hold_record["created_at"],
            "marker_sha256": self.manifest["media_dispatch_fence_sha256"],
            "dispatch_fence_cli_sha256": self.manifest["api_code"]["dispatch_fence_cli_sha256"],
        }

    def verify(self, *, handoff: dict | None = None, hold_raw: bytes | None = None,
               mode: int = 0o644, pinned_handoff_sha256: str | None = None) -> dict:
        handoff_raw = (json.dumps(self.handoff if handoff is None else handoff) + "\n").encode()
        hold_bytes = self.hold_raw if hold_raw is None else hold_raw
        manifest = {**self.manifest,
                    "cutover_handoff_sha256": (pinned_handoff_sha256
                                                or hashlib.sha256(handoff_raw).hexdigest())}
        directory = SimpleNamespace(st_mode=stat.S_IFDIR | 0o700, st_uid=0)
        handoff_info = SimpleNamespace(st_mode=stat.S_IFREG | 0o600, st_uid=0,
                                       st_nlink=1, st_size=len(handoff_raw))
        hold_info = SimpleNamespace(st_mode=stat.S_IFREG | mode, st_uid=0,
                                    st_nlink=1, st_size=len(hold_bytes))
        with patch.object(Path, "lstat", return_value=directory), \
             patch.object(runner.os, "open", side_effect=[3, 4]), \
             patch.object(runner.os, "fstat", side_effect=[handoff_info, hold_info]), \
             patch.object(runner.os, "read", side_effect=[handoff_raw, hold_bytes]), \
             patch.object(runner.os, "close"), \
             patch.object(runner.hold, "verify", return_value=self.hold_record) as upstream:
            result = runner.verify_cutover_hold(manifest)
            upstream.assert_called_once_with(self.directory, manifest["expected_head"],
                                             hold_path=runner.CUTOVER_HOLD_PATH)
            return result

    def test_exact_handoff_and_same_hold_are_accepted(self) -> None:
        self.assertEqual(self.verify()["hold_sha256"], self.handoff["hold_sha256"])

    def test_changed_hold_bytes_or_mode_are_refused(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "hold bytes changed"):
            self.verify(hold_raw=self.hold_raw + b"tampered")
        with self.assertRaisesRegex(RuntimeError, "hold ownership, mode"):
            self.verify(mode=0o600)

    def test_handoff_cannot_name_another_release_or_nonce(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "handoff identity"):
            self.verify(handoff={**self.handoff, "hold_release_dir": "/root/other"})
        with self.assertRaisesRegex(RuntimeError, "handoff identity"):
            self.verify(handoff={**self.handoff, "nonce_sha256": "0" * 64})

    def test_handoff_sha_and_target_are_pinned(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "handoff SHA drift"):
            self.verify(pinned_handoff_sha256="0" * 64)
        with self.assertRaisesRegex(RuntimeError, "handoff identity"):
            self.verify(handoff={**self.handoff, "target_sha": "0" * 40})

    def test_handoff_owner_phases_and_creation_time_are_pinned(self) -> None:
        changed = (
            ("hold_owner", "another-owner", "handoff identity"),
            ("hold_phases", ["api-drain", "nonce", "deploy"], "handoff identity"),
            ("hold_created_at", "2026-10-18T16:00:00+00:00", "hold metadata drift"),
        )
        for field, value, message in changed:
            with self.subTest(field=field), self.assertRaisesRegex(RuntimeError, message):
                self.verify(handoff={**self.handoff, field: value})
        with self.assertRaisesRegex(RuntimeError, "creation time invalid"):
            self.verify(handoff={**self.handoff, "hold_created_at": "not-a-time"})

    def test_rebound_hold_sha_cannot_hide_metadata_drift(self) -> None:
        changes = (
            ("target", "0" * 40),
            ("owner", "another-owner"),
            ("phases", ["api-drain", "nonce", "deploy"]),
            ("created_at", "2026-10-18T16:00:00+00:00"),
        )
        for field, value in changes:
            record = {**self.hold_record, field: value}
            raw = ("owned by A01\n" + json.dumps(record) + "\n").encode()
            rebound = {**self.handoff, "hold_sha256": hashlib.sha256(raw).hexdigest()}
            with self.subTest(field=field), self.assertRaisesRegex(RuntimeError,
                                                                   "hold metadata drift"):
                self.verify(handoff=rebound, hold_raw=raw)


class PhaseHoldRoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = {"expected_head": "a" * 40}

    def test_fenced_listener_and_later_phase_reuse_cutover_hold(self) -> None:
        fenced = {**self.manifest, "fenced_media_job": {"id": runner.FENCED_MEDIA_JOB_ID}}
        with patch.object(runner, "verify_cutover_hold") as cutover, \
             patch.object(runner.hold, "acquire") as acquire, \
             patch.object(runner.hold, "verify") as legacy:
            for phase in ("listener", "manual", "facts", "panel"):
                runner.ensure_phase_hold(fenced, phase)
            self.assertEqual(cutover.call_count, 4)
            acquire.assert_not_called()
            legacy.assert_not_called()

    def test_unfenced_listener_acquires_only_ordinary_hold(self) -> None:
        with patch.object(Path, "exists", return_value=False), \
             patch.object(runner, "verify_cutover_hold") as cutover, \
             patch.object(runner.hold, "acquire", return_value="created") as acquire, \
             patch.object(runner.hold, "verify") as legacy:
            runner.ensure_phase_hold(self.manifest, "listener")
            acquire.assert_called_once_with(str(runner.RELEASE), self.manifest["expected_head"],
                                            "codex-a01-round12-review",
                                            ["listener", "manual", "facts", "panel"])
            cutover.assert_not_called()
            legacy.assert_not_called()

    def test_unfenced_listener_refuses_existing_hold(self) -> None:
        with patch.object(Path, "exists", return_value=True), \
             patch.object(runner.hold, "acquire") as acquire:
            with self.assertRaisesRegex(RuntimeError, "another release hold exists"):
                runner.ensure_phase_hold(self.manifest, "listener")
            acquire.assert_not_called()

    def test_unfenced_later_phase_verifies_only_ordinary_hold(self) -> None:
        with patch.object(runner, "verify_cutover_hold") as cutover, \
             patch.object(runner.hold, "acquire") as acquire, \
             patch.object(runner.hold, "verify") as legacy:
            runner.ensure_phase_hold(self.manifest, "manual")
            legacy.assert_called_once_with(str(runner.RELEASE), self.manifest["expected_head"])
            cutover.assert_not_called()
            acquire.assert_not_called()


class PaidDispatchCheckpointTests(unittest.TestCase):
    def test_cutover_hold_drift_prevents_direct_model_phase(self) -> None:
        manifest = {"fenced_media_job": {"id": runner.FENCED_MEDIA_JOB_ID},
                    "driver_container_path": "/tmp/a01-round12-20261017-fe35369c/payload/driver.mjs"}
        before = {"slug": "story-rolling-suitcase-v2", "stage": "blocked"}
        with patch.object(runner, "verify_cutover_hold",
                          side_effect=RuntimeError("cutover hold bytes changed")) as held, \
             patch.object(runner, "jobs") as jobs, \
             patch.object(runner, "direct_node") as direct:
            with self.assertRaisesRegex(RuntimeError, "cutover hold bytes changed"):
                runner.guarded_direct_phase(manifest, before, "oneoff", "listener")
            held.assert_called_once_with(manifest)
            jobs.assert_not_called()
            direct.assert_not_called()

    def test_late_media_fence_drift_prevents_direct_model_phase(self) -> None:
        manifest = {"driver_container_path": "/tmp/a01-round12-20261017-fe35369c/payload/driver.mjs"}
        before = {"slug": "story-rolling-suitcase-v2", "stage": "blocked"}
        with patch.object(runner, "jobs", side_effect=RuntimeError("nonce drift")) as jobs, \
             patch.object(runner, "budget") as budget, \
             patch.object(runner, "direct_node") as direct:
            with self.assertRaisesRegex(RuntimeError, "nonce drift"):
                runner.guarded_direct_phase(manifest, before, "oneoff", "listener")
            jobs.assert_called_once_with(manifest)
            budget.assert_not_called()
            direct.assert_not_called()

    def test_late_checkpoint_rechecks_budget_lease_and_site(self) -> None:
        manifest = {"driver_container_path": "/tmp/a01-round12-20261017-fe35369c/payload/driver.mjs"}
        before = {"slug": "story-rolling-suitcase-v2", "stage": "blocked"}
        with patch.object(runner, "jobs") as jobs, \
             patch.object(runner, "budget") as budget, \
             patch.object(runner, "no_leases") as leases, \
             patch.object(runner, "site_row", return_value=before) as site, \
             patch.object(runner, "direct_node", return_value="finished") as direct:
            self.assertEqual(runner.guarded_direct_phase(manifest, before, "oneoff", "listener"),
                             "finished")
            jobs.assert_called_once_with(manifest)
            budget.assert_called_once_with()
            leases.assert_called_once_with()
            site.assert_called_once_with()
            direct.assert_called_once_with("oneoff", manifest["driver_container_path"],
                                           "--listener", timeout_seconds=3600)


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
