#!/usr/bin/env python3
"""Exact B25 worker STOP and repeated quiet survey; LOCAL REVIEW CANDIDATE.

Default is read-only.  --apply-stop only places one B25 project STOP after a
separate site-owner authorization; it never declares the A01 cutover ready.
No API intake fence exists here, so even two quiet surveys cannot exclude a
direct media API client creating a new job after the survey.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
WORKER_PROBE = HERE / "b25-worker-pause.py"
ROOT = Path("/root/travel_scanner")
COMPOSE = ROOT / "docker-compose.prod.yml"
HOLD = Path("/root/travel-scanner-deploy.hold")
SLUG = "story-adapt-seiko-quartz-astron"
JOB_ID = "b721a65d-8c8d-4ae8-834c-391cfc267a6f"
JOB_SLUG = "google-project-suncatcher-prototype-what-it-tests"
MOUNT_DEST = "/var/lib/mokaair/video-work"
LOCKS = (
    Path("/var/lock/travel-scanner-deploy.lock"),
    Path("/root/mokaair-deploy.lock"),
    Path("/run/mokaair-manual-deploy.lock"),
    Path("/run/travel-scanner-deployer/deploy.lock"),
)
HEX64 = re.compile(r"[0-9a-f]{64}\Z")

DB_QUERY = (
    "select json_build_object('active_media',"
    "(select coalesce(json_agg(json_build_object('id',id::text,'slug',slug,"
    "'status',status) order by created_at), '[]'::json) "
    "from video_media_jobs where status in ('queued','submitted')),'active_stage',"
    "(select count(*) from video_stage_jobs where status in ('queued','running')))::text;"
)


class Stop(RuntimeError):
    """A failed proof; never infer authorization or quietly retry."""


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise Stop(reason)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_regular(path: Path, *, max_bytes: int) -> bytes:
    require(path.is_absolute(), "relative_path")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK)
    try:
        info = os.fstat(fd)
        require(stat.S_ISREG(info.st_mode) and 0 < info.st_size <= max_bytes, "unsafe_regular_file")
        data = bytearray()
        while len(data) <= max_bytes:
            chunk = os.read(fd, min(65536, max_bytes + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
        require(len(data) == info.st_size, "file_changed_during_read")
        return bytes(data)
    finally:
        os.close(fd)


def load_plan(path: Path, expected_sha: str) -> dict[str, Any]:
    require(bool(HEX64.fullmatch(expected_sha)), "invalid_plan_sha")
    raw = read_regular(path, max_bytes=4096)
    require(sha(raw) == expected_sha, "plan_hash_drift")
    plan = json.loads(raw)
    require(
        isinstance(plan, dict)
        and set(plan)
        == {
            "schema_version", "b25_slug", "worker_id", "worker_image",
            "video_work_volume", "video_work_mount", "worker_probe_sha256",
            "expected_exact_media_job_id",
        },
        "plan_shape",
    )
    require(plan["schema_version"] == 1 and plan["b25_slug"] == SLUG, "wrong_slug")
    require(plan["expected_exact_media_job_id"] == JOB_ID, "wrong_exact_job")
    require(isinstance(plan["worker_id"], str) and bool(HEX64.fullmatch(plan["worker_id"])), "worker_id_pin")
    require(
        isinstance(plan["worker_image"], str)
        and plan["worker_image"].startswith("sha256:")
        and bool(HEX64.fullmatch(plan["worker_image"][7:])),
        "worker_image_pin",
    )
    require(plan["video_work_volume"] == "travel_scanner_video_work", "volume_name_pin")
    require(
        isinstance(plan["video_work_mount"], str)
        and plan["video_work_mount"].startswith("/var/lib/docker/volumes/travel_scanner_video_work/")
        and "\n" not in plan["video_work_mount"],
        "volume_mount_pin",
    )
    require(
        isinstance(plan["worker_probe_sha256"], str)
        and bool(HEX64.fullmatch(plan["worker_probe_sha256"])),
        "probe_sha_pin",
    )
    return plan


class Command:
    def run(self, argv: list[str], *, data: bytes | None = None) -> bytes:
        result = subprocess.run(
            argv, input=data, capture_output=True, check=False, timeout=45
        )
        if result.returncode != 0:
            # Docker/psql stderr can contain credentials or paths.  Do not print it.
            raise Stop(f"command_failed:{Path(argv[0]).name}:{result.returncode}")
        return result.stdout


class Survey:
    def __init__(self, plan: dict[str, Any], command: Command | None = None) -> None:
        self.plan = plan
        self.command = command or Command()
        self.probe = read_regular(WORKER_PROBE, max_bytes=100_000)
        require(sha(self.probe) == plan["worker_probe_sha256"], "probe_source_drift")

    def cmd(self, *args: str, data: bytes | None = None) -> bytes:
        return self.command.run(list(args), data=data)

    def compose(self, *args: str) -> bytes:
        return self.cmd("docker", "compose", "-f", str(COMPOSE), *args)

    def worker(self) -> None:
        worker_id = self.plan["worker_id"]
        require(
            self.compose("ps", "-q", "video-worker").decode().strip() == worker_id,
            "worker_container_drift",
        )
        data = json.loads(self.cmd("docker", "inspect", worker_id))
        require(isinstance(data, list) and len(data) == 1, "worker_inspect_shape")
        info = data[0]
        require(
            info.get("Id") == worker_id
            and info.get("Image") == self.plan["worker_image"]
            and info.get("State", {}).get("Running") is True,
            "worker_identity_drift",
        )
        labels = info.get("Config", {}).get("Labels", {})
        require(
            labels.get("com.docker.compose.project") == "travel_scanner"
            and labels.get("com.docker.compose.service") == "video-worker",
            "worker_compose_drift",
        )
        require(info.get("Config", {}).get("Hostname") == "video-worker", "worker_hostname_drift")
        require(info.get("Config", {}).get("User") in ("pwuser", "1001"), "worker_user_drift")
        env = info.get("Config", {}).get("Env", [])
        workdir_env = (
            [item for item in env if isinstance(item, str) and item.startswith("VIDEO_WORKDIR=")]
            if isinstance(env, list)
            else []
        )
        require(
            workdir_env == [f"VIDEO_WORKDIR={MOUNT_DEST}"],
            "worker_workdir_drift",
        )
        mounts = [m for m in info.get("Mounts", []) if m.get("Destination") == MOUNT_DEST]
        require(
            len(mounts) == 1
            and mounts[0].get("Type") == "volume"
            and mounts[0].get("RW") is True
            and mounts[0].get("Name") == self.plan["video_work_volume"]
            and mounts[0].get("Source") == self.plan["video_work_mount"],
            "video_work_volume_drift",
        )

    def inside(self, mode: str) -> dict[str, Any]:
        require(mode in ("inspect", "pause"), "invalid_worker_mode")
        self.worker()
        output = self.cmd(
            "docker", "exec", "-i", self.plan["worker_id"], "python3", "-", mode,
            data=self.probe,
        )
        record = json.loads(output)
        require(isinstance(record, dict) and record.get("slug") == SLUG, "worker_probe_shape")
        self.worker()
        return record

    def db(self) -> dict[str, Any]:
        text = self.compose(
            "exec", "-T", "postgres", "psql", "-X", "-q", "-t", "-A",
            "-U", "travel", "-d", "travel_scanner", "-c", DB_QUERY,
        ).decode().strip()
        row = json.loads(text)
        require(isinstance(row, dict) and isinstance(row.get("active_media"), list), "db_shape")
        require(row.get("active_stage") == 0, "active_stage_job")
        require(
            row["active_media"]
            == [{"id": JOB_ID, "slug": JOB_SLUG, "status": "queued"}],
            "active_media_job_drift",
        )
        return row

    def one_quiet_sample(self) -> dict[str, Any]:
        worker = self.inside("inspect")
        require(worker.get("worker_quiet") is True, "b25_worker_not_quiet")
        self.db()
        return worker


def acquire_four_locks() -> list[int]:
    """Take existing release flocks without creating or changing lock files."""
    fds: list[int] = []
    try:
        for path in LOCKS:
            require(path.parent.is_dir() and not path.parent.is_symlink(), "lock_parent_drift")
            fd = os.open(
                path,
                os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW | os.O_NONBLOCK,
            )
            fds.append(fd)
            require(stat.S_ISREG(os.fstat(fd).st_mode), "lock_not_regular")
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fds
    except BaseException:
        release_locks(fds)
        raise Stop("release_lock_busy_or_unsafe") from None


def release_locks(fds: list[int]) -> None:
    for fd in reversed(fds):
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


def verify_lock_fds(fds: list[int]) -> None:
    require(len(fds) == len(LOCKS), "four_locks_required")
    for fd, path in zip(fds, LOCKS, strict=True):
        opened = os.fstat(fd)
        current = path.lstat()
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_ino == current.st_ino
            and opened.st_dev == current.st_dev,
            "release_lock_fd_drift",
        )
        # If a caller hands us the right file descriptor but forgot to lock it,
        # take the flock now; a competing release owner makes this fail closed.
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise Stop("release_lock_busy") from error


def verify_hold(expected_sha: str | None) -> None:
    if expected_sha is None:
        try:
            HOLD.lstat()
        except FileNotFoundError:
            return
        raise Stop("deployment_hold_present")
    require(bool(HEX64.fullmatch(expected_sha)), "expected_hold_sha_invalid")
    require(sha(read_regular(HOLD, max_bytes=4096)) == expected_sha, "hold_hash_drift")


def verify_under_locks(
    survey: Survey,
    fds: list[int],
    *,
    expected_stop_sha: str,
    expected_hold_sha: str | None = None,
    wait: float = 5,
) -> dict[str, Any]:
    """Call twice while the same four release flocks are owned by the caller."""
    verify_lock_fds(fds)
    require(bool(HEX64.fullmatch(expected_stop_sha)), "expected_stop_sha_invalid")
    verify_hold(expected_hold_sha)
    first = survey.one_quiet_sample()
    require(first.get("stop_sha256") == expected_stop_sha, "stop_hash_drift")
    require(1 <= wait <= 30, "quiet_interval_invalid")
    time.sleep(wait)
    verify_lock_fds(fds)
    verify_hold(expected_hold_sha)
    second = survey.one_quiet_sample()
    require(
        second.get("stop_sha256") == expected_stop_sha
        and first.get("file_sha256") == second.get("file_sha256"),
        "producer_files_changed_between_samples",
    )
    return {
        "schema_version": 1,
        "slug": SLUG,
        "worker_quiet_candidate": True,
        "samples": 2,
        "stop_sha256": second["stop_sha256"],
        "file_sha256": second["file_sha256"],
        "direct_api_intake_fenced": False,
        "production_ready": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--expected-plan-sha256", required=True)
    parser.add_argument("--apply-stop", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--expected-stop-sha256")
    parser.add_argument("--expected-hold-sha256")
    args = parser.parse_args()
    try:
        require(not (args.apply_stop and args.verify), "incompatible_modes")
        require(
            args.verify or (args.expected_stop_sha256 is None and args.expected_hold_sha256 is None),
            "proof_pin_requires_verify",
        )
        plan = load_plan(args.plan, args.expected_plan_sha256)
        survey = Survey(plan)
        if not args.apply_stop and not args.verify:
            result = survey.inside("inspect")
            result["production_ready"] = False
            result["dry_run"] = True
        else:
            require(os.geteuid() == 0, "root_required")
            fds = acquire_four_locks()
            try:
                verify_lock_fds(fds)
                verify_hold(None if args.expected_hold_sha256 is None else args.expected_hold_sha256)
                if args.apply_stop:
                    result = survey.inside("pause")
                    result["production_ready"] = False
                    result["worker_quiet_candidate"] = False
                else:
                    require(args.expected_stop_sha256 is not None, "expected_stop_sha_required")
                    result = verify_under_locks(
                        survey, fds, expected_stop_sha=args.expected_stop_sha256,
                        expected_hold_sha=args.expected_hold_sha256,
                    )
            finally:
                release_locks(fds)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (Stop, OSError, ValueError, TypeError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        print(
            json.dumps({"status": "STOP", "production_ready": False,
                        "reason": str(error) if isinstance(error, Stop) else type(error).__name__}),
            file=sys.stderr,
        )
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
