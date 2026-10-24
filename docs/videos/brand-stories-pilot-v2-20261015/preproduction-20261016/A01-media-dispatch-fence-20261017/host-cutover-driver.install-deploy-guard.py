#!/usr/bin/env python3
"""Dry-run-by-default exact host deploy guard installer and restore helper.

This file is a candidate, not authority to write production. `--apply` needs
separate owner approval naming the exact candidate SHA and live source SHA.
No deploy, container stop, or provider call is performed here.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

LIVE = Path("/root/deploy-travel-scanner.sh")
BACKUP = Path("/root/deploy-travel-scanner.sh.a01-before-c8bb3559")
CANDIDATE = Path(__file__).resolve().parent / "host-cutover-driver.deploy-patched.sh"
ORIGINAL_SHA = "c8bb3559f6b7e25e11c3bdf207c2f8dabd28835119c78494b3c9ad8bb75bd64f"
PATCHED_SHA = "836b953610b4ae17eda6d2056efb1f633827db620d0eb43934312cc19d8ac9c6"
LOCKS = (
    Path("/var/lock/travel-scanner-deploy.lock"),
    Path("/root/mokaair-deploy.lock"),
    Path("/run/mokaair-manual-deploy.lock"),
    Path("/run/travel-scanner-deployer/deploy.lock"),
)
HOLD = Path("/root/travel-scanner-deploy.hold")
WATCHER = "a01-media-dispatch-fence-watch.service"
TICK = "travel-scanner-autodeploy.service"
TIMER = "travel-scanner-autodeploy.timer"


class Stop(RuntimeError):
    pass


def require(value: bool, reason: str) -> None:
    if not value:
        raise Stop(reason)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_regular(path: Path, expected: str) -> tuple[bytes, os.stat_result]:
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and not path.is_symlink(), "script_not_regular")
    require(info.st_uid == 0 and not info.st_mode & 0o022, "script_owner_or_mode_drift")
    if path == LIVE:
        require(stat.S_IMODE(info.st_mode) == 0o700, "live_script_mode_drift")
    content = path.read_bytes()
    require(digest(content) == expected, "script_sha_drift")
    require(b"\r" not in content and content.endswith(b"\n"), "script_not_lf_only")
    return content, info


def check_bash_syntax(path: Path) -> None:
    result = subprocess.run(
        ["/bin/bash", "-n", str(path)], capture_output=True, check=False, timeout=30
    )
    require(result.returncode == 0, "script_bash_syntax_failed")


def unit_field(unit: str, field: str) -> str:
    result = subprocess.run(
        ["/usr/bin/systemctl", "show", unit, f"--property={field}", "--value"],
        capture_output=True,
        check=False,
        timeout=10,
    )
    require(result.returncode == 0, "systemd_readback_failed")
    return result.stdout.decode().strip()


def check_quiet(*, restoring: bool) -> None:
    require(not HOLD.exists() and not HOLD.is_symlink(), "deploy_hold_present")
    for unit in (TIMER, TICK):
        require(unit_field(unit, "LoadState") == "not-found", "autodeploy_unit_present")
        require(unit_field(unit, "ActiveState") == "inactive", "autodeploy_unit_active")
        require(unit_field(unit, "Job") in ("", "0"), "autodeploy_job_pending")
    for unit in (WATCHER,):
        require(unit_field(unit, "ActiveState") == "inactive", "service_active")
        require(unit_field(unit, "Job") in ("", "0"), "service_job_pending")
    if restoring:
        require(
            not Path("/run/a01-media-dispatch-fence/heartbeat.json").exists(),
            "nonce_watcher_heartbeat_present",
        )


def acquire_locks() -> list[int]:
    fds: list[int] = []
    try:
        for path in LOCKS:
            require(
                path.parent.is_dir() and not path.parent.is_symlink(),
                "lock_parent_missing",
            )
            fd = os.open(
                path, os.O_RDWR | os.O_CREAT | os.O_CLOEXEC | os.O_NOFOLLOW, 0o600
            )
            try:
                require(stat.S_ISREG(os.fstat(fd).st_mode), "lock_not_regular")
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BaseException:
                os.close(fd)
                raise
            fds.append(fd)
    except BaseException:
        for fd in reversed(fds):
            os.close(fd)
        raise
    return fds


def write_all(fd: int, data: bytes) -> None:
    view = memoryview(data)
    while view:
        count = os.write(fd, view)
        require(count > 0, "short_write")
        view = view[count:]


def fsync_parent(path: Path) -> None:
    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def create_exact(path: Path, data: bytes, mode: int) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    try:
        os.fchmod(fd, mode)
        write_all(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)
    require(path.read_bytes() == data, "staged_file_readback_failed")
    fsync_parent(path)


def run(*, restoring: bool, apply: bool) -> dict[str, str | bool]:
    require(not (restoring and apply), "restore_requires_separate_fence_retirement")
    source, source_info = read_regular(LIVE, PATCHED_SHA if restoring else ORIGINAL_SHA)
    target, _ = read_regular(
        BACKUP if restoring else CANDIDATE, ORIGINAL_SHA if restoring else PATCHED_SHA
    )
    check_bash_syntax(BACKUP if restoring else CANDIDATE)
    result: dict[str, str | bool] = {
        "mode": "restore" if restoring else "install",
        "dry_run": not apply,
        "live_sha256": digest(source),
        "candidate_sha256": digest(target),
        "backup_path": str(BACKUP),
    }
    if not apply:
        return result
    require(os.geteuid() == 0, "apply_requires_root")
    fds = acquire_locks()
    try:
        check_quiet(restoring=restoring)
        source, source_info = read_regular(
            LIVE, PATCHED_SHA if restoring else ORIGINAL_SHA
        )
        target, _ = read_regular(
            BACKUP if restoring else CANDIDATE,
            ORIGINAL_SHA if restoring else PATCHED_SHA,
        )
        if not restoring:
            require(
                not BACKUP.exists() and not BACKUP.is_symlink(), "backup_already_exists"
            )
            create_exact(BACKUP, source, stat.S_IMODE(source_info.st_mode))
            read_regular(BACKUP, ORIGINAL_SHA)
        temporary = LIVE.with_name(
            f".deploy-travel-scanner.sh.a01-{os.getpid()}.pending"
        )
        require(
            not temporary.exists() and not temporary.is_symlink(), "staging_path_exists"
        )
        create_exact(temporary, target, stat.S_IMODE(source_info.st_mode))
        check_bash_syntax(temporary)
        read_regular(LIVE, PATCHED_SHA if restoring else ORIGINAL_SHA)
        check_quiet(restoring=restoring)
        os.replace(temporary, LIVE)
        fsync_parent(LIVE)
        read_regular(LIVE, ORIGINAL_SHA if restoring else PATCHED_SHA)
        check_bash_syntax(LIVE)
    finally:
        for fd in reversed(fds):
            os.close(fd)
    result["dry_run"] = False
    result["installed_sha256"] = ORIGINAL_SHA if restoring else PATCHED_SHA
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--restore", action="store_true", help="preview guarded restore"
    )
    parser.add_argument(
        "--apply", action="store_true", help="owner-approved exact host write"
    )
    args = parser.parse_args()
    try:
        print(json.dumps(run(restoring=args.restore, apply=args.apply), sort_keys=True))
    except (Stop, OSError, ValueError, subprocess.TimeoutExpired) as error:
        reason = str(error) if isinstance(error, Stop) else type(error).__name__
        print(json.dumps({"status": "STOP", "reason": reason}), file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
