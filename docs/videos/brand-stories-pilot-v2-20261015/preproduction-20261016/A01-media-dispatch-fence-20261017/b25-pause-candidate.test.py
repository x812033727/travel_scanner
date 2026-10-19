"""Disposable Linux tests for the exact B25 producer pause candidate."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent


def module(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    assert spec and spec.loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


worker = module("b25_worker", "b25-worker-pause.py")
host = module("b25_host", "b25-host-pause-candidate.py")


class WorkerProbeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name) / "video-work"
        self.project = self.base / worker.SLUG
        self.media = self.project / "media"
        self.media.mkdir(parents=True)
        self.uid = os.geteuid()
        (self.project / "auto.json").write_text(
            json.dumps({"slug": worker.SLUG, "story": {"chapters": {}}})
        )
        (self.project / "state.json").write_text(json.dumps({"runs": []}))
        chapters = self.project / "story" / "chapters"
        chapters.mkdir(parents=True)
        for key in worker.CHAPTER_KEYS:
            (chapters / f"{key}.json").write_text(json.dumps({"key": key, "scenes": []}))
        (self.media / "jobs.json").write_text(json.dumps({"jobs": {}}))
        (self.media / "ledger.json").write_text(json.dumps({"entries": []}))

    def quiet(self):
        return worker.snapshot(self.base, uid=self.uid)

    def stop(self):
        return worker.place_stop(self.base, uid=self.uid)

    def test_only_exact_b25_stop_created_and_fsynced(self) -> None:
        sibling = self.base / "unrelated-video"
        sibling.mkdir()
        self.assertFalse(self.quiet()["worker_quiet"])
        receipt = self.stop()
        self.assertTrue((self.project / "STOP").is_file())
        self.assertFalse((sibling / "STOP").exists())
        self.assertEqual(receipt["stop_sha256"], self.quiet()["stop_sha256"])
        self.assertTrue(self.quiet()["worker_quiet"])
        with self.assertRaisesRegex(worker.Stop, "stop_already_exists"):
            self.stop()

    def test_lease_pending_job_and_reservation_each_refuse_quiet(self) -> None:
        (self.project / "LEASE").write_text("held")
        self.stop()  # STOP asks the live holder to finish; it never removes its lease.
        self.assertTrue(self.quiet()["lease_present"])
        self.assertFalse(self.quiet()["worker_quiet"])
        (self.project / "LEASE").unlink()
        (self.media / "jobs.json").write_text(json.dumps({"jobs": {"key": {"job_id": "j"}}}))
        self.assertEqual(self.quiet()["pending_jobs"], 1)
        self.assertFalse(self.quiet()["worker_quiet"])
        (self.media / "jobs.json").write_text(json.dumps({"jobs": {}}))
        (self.media / "ledger.json").write_text(json.dumps({"entries": [{"status": "reserved"}]}))
        self.assertEqual(self.quiet()["reserved_entries"], 1)
        self.assertFalse(self.quiet()["worker_quiet"])

    def test_foreign_stop_wrong_identity_or_symlink_stops(self) -> None:
        (self.project / "STOP").write_text("owner hold")
        with self.assertRaisesRegex(worker.Stop, "foreign_or_invalid_stop"):
            self.quiet()
        with self.assertRaisesRegex(worker.Stop, "stop_already_exists"):
            self.stop()
        (self.project / "STOP").unlink()
        (self.project / "auto.json").write_text(
            json.dumps({"slug": "other", "story": {"chapters": {}}})
        )
        with self.assertRaisesRegex(worker.Stop, "wrong_project:auto.json"):
            self.stop()
        (self.project / "auto.json").unlink()
        (self.project / "auto.json").symlink_to(self.project / "state.json")
        with self.assertRaises(OSError):
            self.stop()

    def test_real_journal_shape_and_chapter_proof_required(self) -> None:
        (self.project / "state.json").write_text(json.dumps({"slug": worker.SLUG}))
        with self.assertRaisesRegex(worker.Stop, "state_runs_shape"):
            self.stop()
        (self.project / "state.json").write_text(json.dumps({"runs": []}))
        (self.project / "story" / "chapters" / "hook.json").write_text(
            json.dumps({"key": "wrong", "scenes": []})
        )
        with self.assertRaisesRegex(worker.Stop, "chapter_key_drift:hook"):
            self.stop()
        (self.project / "story" / "chapters" / "hook.json").unlink()
        with self.assertRaises(FileNotFoundError):
            self.stop()

    def test_missing_or_malformed_ledger_never_reports_quiet(self) -> None:
        self.stop()
        (self.media / "ledger.json").unlink()
        with self.assertRaises(FileNotFoundError):
            self.quiet()
        (self.media / "ledger.json").write_text("[]")
        with self.assertRaisesRegex(worker.Stop, "json_shape"):
            self.quiet()

    def test_nonregular_ledger_is_refused_without_blocking(self) -> None:
        self.stop()
        (self.media / "ledger.json").unlink()
        os.mkfifo(self.media / "ledger.json")
        with self.assertRaisesRegex(worker.Stop, "not_regular"):
            self.quiet()


class HostSurveyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.plan = {
            "schema_version": 1,
            "b25_slug": host.SLUG,
            "worker_id": "1" * 64,
            "worker_image": "sha256:" + "2" * 64,
            "video_work_volume": "travel_scanner_video_work",
            "video_work_mount": "/var/lib/docker/volumes/travel_scanner_video_work/_data",
            "worker_probe_sha256": host.sha(host.WORKER_PROBE.read_bytes()),
            "expected_exact_media_job_id": host.JOB_ID,
        }

    def test_plan_requires_exact_worker_source_and_job(self) -> None:
        path = self.root / "plan.json"
        raw = json.dumps(self.plan, sort_keys=True).encode()
        path.write_bytes(raw)
        self.assertEqual(host.load_plan(path, host.sha(raw)), self.plan)
        with self.assertRaisesRegex(host.Stop, "plan_hash_drift"):
            host.load_plan(path, "a" * 64)
        altered = {**self.plan, "expected_exact_media_job_id": "other"}
        raw = json.dumps(altered).encode()
        path.write_bytes(raw)
        with self.assertRaisesRegex(host.Stop, "wrong_exact_job"):
            host.load_plan(path, host.sha(raw))

    def test_db_requires_only_exact_legacy_job_and_no_stage(self) -> None:
        class Fake:
            def __init__(self, row):
                self.row = row

            def run(self, argv, *, data=None):
                return json.dumps(self.row).encode()

        exact = {"active_media": [{"id": host.JOB_ID, "slug": host.JOB_SLUG, "status": "queued"}], "active_stage": 0}
        self.assertEqual(host.Survey(self.plan, Fake(exact)).db(), exact)
        with self.assertRaisesRegex(host.Stop, "active_media_job_drift"):
            host.Survey(self.plan, Fake({**exact, "active_media": exact["active_media"] + [{"id": "b25"}]})).db()
        with self.assertRaisesRegex(host.Stop, "active_stage_job"):
            host.Survey(self.plan, Fake({**exact, "active_stage": 1})).db()

    def test_worker_rejects_identity_volume_and_user_drift(self) -> None:
        class Fake:
            def __init__(self, record):
                self.record = record

            def run(self, argv, *, data=None):
                if argv[1:3] == ["compose", "-f"]:
                    return ("1" * 64).encode()
                return json.dumps([self.record]).encode()

        record = {
            "Id": "1" * 64,
            "Image": "sha256:" + "2" * 64,
            "State": {"Running": True},
            "Config": {
                "Hostname": "video-worker",
                "User": "pwuser",
                "Env": [f"VIDEO_WORKDIR={host.MOUNT_DEST}"],
                "Labels": {"com.docker.compose.project": "travel_scanner", "com.docker.compose.service": "video-worker"},
            },
            "Mounts": [{"Destination": host.MOUNT_DEST, "Type": "volume", "RW": True,
                        "Name": "travel_scanner_video_work", "Source": self.plan["video_work_mount"]}],
        }
        host.Survey(self.plan, Fake(record)).worker()
        record["Config"]["User"] = "root"
        with self.assertRaisesRegex(host.Stop, "worker_user_drift"):
            host.Survey(self.plan, Fake(record)).worker()
        record["Config"]["User"] = "pwuser"
        record["Config"]["Env"].append("VIDEO_WORKDIR=/other")
        with self.assertRaisesRegex(host.Stop, "worker_workdir_drift"):
            host.Survey(self.plan, Fake(record)).worker()
        record["Config"]["Env"].pop()
        record["Mounts"][0]["Source"] = "/wrong/mount"
        with self.assertRaisesRegex(host.Stop, "video_work_volume_drift"):
            host.Survey(self.plan, Fake(record)).worker()

    def test_two_samples_under_four_locks_stay_candidate_and_detect_drift(self) -> None:
        locks = tuple(self.root / f"lock-{n}" for n in range(4))
        for path in locks:
            path.touch()
        with patch.object(host, "LOCKS", locks), patch.object(host, "HOLD", self.root / "hold"):
            fds = host.acquire_four_locks()
            try:
                sample = {"stop_sha256": "a" * 64, "file_sha256": {"jobs.json": "b" * 64}}

                class Fake:
                    def __init__(self):
                        self.calls = 0

                    def one_quiet_sample(self):
                        self.calls += 1
                        return sample.copy()

                survey = Fake()
                with patch.object(host.time, "sleep"):
                    result = host.verify_under_locks(survey, fds, expected_stop_sha="a" * 64)
                self.assertEqual(survey.calls, 2)
                self.assertFalse(result["production_ready"])
                self.assertFalse(result["direct_api_intake_fenced"])
                with self.assertRaisesRegex(host.Stop, "stop_hash_drift"):
                    with patch.object(host.time, "sleep"):
                        host.verify_under_locks(survey, fds, expected_stop_sha="c" * 64)
                (self.root / "hold").write_text("foreign")
                with self.assertRaisesRegex(host.Stop, "deployment_hold_present"):
                    with patch.object(host.time, "sleep"):
                        host.verify_under_locks(survey, fds, expected_stop_sha="a" * 64)
                digest = host.sha((self.root / "hold").read_bytes())
                with patch.object(host.time, "sleep"):
                    self.assertFalse(
                        host.verify_under_locks(
                            survey, fds, expected_stop_sha="a" * 64,
                            expected_hold_sha=digest,
                        )["production_ready"]
                    )
                (self.root / "hold").write_text("changed")
                with self.assertRaisesRegex(host.Stop, "hold_hash_drift"):
                    with patch.object(host.time, "sleep"):
                        host.verify_under_locks(
                            survey, fds, expected_stop_sha="a" * 64,
                            expected_hold_sha=digest,
                        )
            finally:
                host.release_locks(fds)

    def test_verify_never_creates_an_absent_release_lock(self) -> None:
        locks = tuple(self.root / f"lock-{n}" for n in range(4))
        for path in locks[:2]:
            path.touch()
        with patch.object(host, "LOCKS", locks):
            with self.assertRaisesRegex(host.Stop, "release_lock_busy_or_unsafe"):
                host.acquire_four_locks()
        self.assertFalse(locks[2].exists())
        self.assertFalse(locks[3].exists())

    def test_verify_cli_absent_lock_is_read_only_and_stops(self) -> None:
        locks = tuple(self.root / f"cli-lock-{n}" for n in range(4))
        plan_path = self.root / "plan.json"
        raw = json.dumps(self.plan, sort_keys=True).encode()
        plan_path.write_bytes(raw)
        argv = [
            "b25-host-pause-candidate.py", "--plan", str(plan_path),
            "--expected-plan-sha256", host.sha(raw), "--verify",
            "--expected-stop-sha256", "a" * 64,
        ]
        with (
            patch.object(host, "LOCKS", locks),
            patch.object(host.os, "geteuid", return_value=0),
            patch.object(sys, "argv", argv),
            redirect_stderr(io.StringIO()) as stderr,
        ):
            self.assertEqual(host.main(), 3)
        self.assertIn("release_lock_busy_or_unsafe", stderr.getvalue())
        self.assertTrue(all(not path.exists() for path in locks))


if __name__ == "__main__":
    unittest.main()
