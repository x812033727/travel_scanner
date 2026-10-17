#!/usr/bin/env python3
"""Exact B25 STOP/quiet probe, intended for stdin in the *existing* video-worker.

This file is only a reviewed local candidate.  A host operator must separately
approve and stage any production use.  It never deletes STOP, LEASE or media
records, sends requests, or starts another worker/container.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

SLUG = "story-adapt-seiko-quartz-astron"
WORK_BASE = Path("/var/lib/mokaair/video-work")
WORKER_UID = 1001
STOP_REASON = "a01_cutover_b25_producer_pause"
MAX_JSON = 10_000_000
CHAPTER_KEYS = ("hook", "origin", "idea", "engine", "turn", "now")


class Stop(RuntimeError):
    """A failed precondition; do not repair or remove a producer's records."""


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise Stop(reason)


def directory(path: Path, *, uid: int) -> int:
    info = path.lstat()
    require(stat.S_ISDIR(info.st_mode) and not path.is_symlink(), "directory_drift")
    require(info.st_uid == uid, "directory_owner_drift")
    return os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)


def child_directory(parent_fd: int, name: str, *, uid: int) -> int:
    info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    require(stat.S_ISDIR(info.st_mode), f"directory_drift:{name}")
    require(info.st_uid == uid, f"directory_owner_drift:{name}")
    return os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)


def read_regular(parent_fd: int, name: str, *, uid: int, limit: int = MAX_JSON) -> bytes:
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
    try:
        info = os.fstat(fd)
        require(stat.S_ISREG(info.st_mode), f"not_regular:{name}")
        require(info.st_uid == uid, f"file_owner_drift:{name}")
        require(0 < info.st_size <= limit, f"file_size_drift:{name}")
        data = bytearray()
        while len(data) <= limit:
            chunk = os.read(fd, min(65536, limit + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
        require(len(data) == info.st_size, f"file_changed:{name}")
        return bytes(data)
    finally:
        os.close(fd)


def read_json(parent_fd: int, name: str, *, uid: int) -> tuple[dict[str, Any], str]:
    data = read_regular(parent_fd, name, uid=uid)
    value = json.loads(data)
    require(isinstance(value, dict), f"json_shape:{name}")
    return value, hashlib.sha256(data).hexdigest()


def stop_payload(now: dt.datetime) -> bytes:
    require(now.tzinfo is not None, "clock_not_utc")
    return (
        json.dumps(
            {
                "schema_version": 1,
                "slug": SLUG,
                "reason": STOP_REASON,
                "created_at_utc": now.astimezone(dt.UTC).isoformat(),
            },
            sort_keys=True,
        )
        + "\n"
    ).encode()


def _stop_state(project_fd: int, *, uid: int) -> tuple[bool, str | None]:
    try:
        content = read_regular(project_fd, "STOP", uid=uid, limit=2048)
    except FileNotFoundError:
        return False, None
    try:
        data = json.loads(content)
    except json.JSONDecodeError as error:
        raise Stop("foreign_or_invalid_stop") from error
    require(
        isinstance(data, dict)
        and set(data) == {"schema_version", "slug", "reason", "created_at_utc"}
        and data.get("schema_version") == 1
        and data.get("slug") == SLUG
        and data.get("reason") == STOP_REASON
        and isinstance(data.get("created_at_utc"), str),
        "foreign_or_invalid_stop",
    )
    return True, hashlib.sha256(content).hexdigest()


def _exists(parent_fd: int, name: str) -> bool:
    try:
        os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        return True
    except FileNotFoundError:
        return False


def identity(project_fd: int, *, uid: int) -> dict[str, str]:
    hashes: dict[str, str] = {}
    auto, hashes["auto.json"] = read_json(project_fd, "auto.json", uid=uid)
    require(auto.get("slug") == SLUG, "wrong_project:auto.json")
    require(isinstance(auto.get("story"), dict), "story_state_missing")
    # state.json is the generic stage journal: {runs: [...]}, without a slug.
    journal, hashes["state.json"] = read_json(project_fd, "state.json", uid=uid)
    require(
        isinstance(journal.get("runs"), list)
        and all(isinstance(run, dict) for run in journal["runs"]),
        "state_runs_shape",
    )
    story_fd = child_directory(project_fd, "story", uid=uid)
    try:
        chapters_fd = child_directory(story_fd, "chapters", uid=uid)
        try:
            for key in CHAPTER_KEYS:
                chapter, digest = read_json(chapters_fd, f"{key}.json", uid=uid)
                require(chapter.get("key") == key, f"chapter_key_drift:{key}")
                hashes[f"story/chapters/{key}.json"] = digest
        finally:
            os.close(chapters_fd)
    finally:
        os.close(story_fd)
    return hashes


def snapshot(base: Path = WORK_BASE, *, uid: int = WORKER_UID) -> dict[str, Any]:
    require(os.geteuid() == uid, "wrong_worker_uid")
    base_fd = directory(base, uid=uid)
    try:
        project_fd = child_directory(base_fd, SLUG, uid=uid)
        try:
            hashes = identity(project_fd, uid=uid)
            owned_stop, stop_sha = _stop_state(project_fd, uid=uid)
            lease_present = _exists(project_fd, "LEASE")
            media_fd = child_directory(project_fd, "media", uid=uid)
            try:
                jobs, hashes["jobs.json"] = read_json(media_fd, "jobs.json", uid=uid)
                ledger, hashes["ledger.json"] = read_json(media_fd, "ledger.json", uid=uid)
            finally:
                os.close(media_fd)
            require(isinstance(jobs.get("jobs"), dict), "jobs_shape")
            require(isinstance(ledger.get("entries"), list), "ledger_shape")
            require(all(isinstance(row, dict) for row in ledger["entries"]), "ledger_row_shape")
            pending = len(jobs["jobs"])
            reserved = sum(row.get("status") == "reserved" for row in ledger["entries"])
            return {
                "schema_version": 1,
                "slug": SLUG,
                "stop_owned": owned_stop,
                "stop_sha256": stop_sha,
                "lease_present": lease_present,
                "pending_jobs": pending,
                "reserved_entries": reserved,
                "file_sha256": hashes,
                "worker_quiet": owned_stop and not lease_present and pending == 0 and reserved == 0,
            }
        finally:
            os.close(project_fd)
    finally:
        os.close(base_fd)


def place_stop(
    base: Path = WORK_BASE,
    *,
    uid: int = WORKER_UID,
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    """Create only B25/STOP; an existing file is left intact and is a stop."""
    require(os.geteuid() == uid, "wrong_worker_uid")
    base_fd = directory(base, uid=uid)
    try:
        project_fd = child_directory(base_fd, SLUG, uid=uid)
        try:
            identity(project_fd, uid=uid)
            require(not _exists(project_fd, "STOP"), "stop_already_exists")
            data = stop_payload(now or dt.datetime.now(dt.UTC))
            fd = os.open(
                "STOP",
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | os.O_NOFOLLOW,
                0o600,
                dir_fd=project_fd,
            )
            try:
                os.fchmod(fd, 0o600)
                offset = 0
                while offset < len(data):
                    written = os.write(fd, data[offset:])
                    require(written > 0, "stop_short_write")
                    offset += written
                os.fsync(fd)
            finally:
                os.close(fd)
            os.fsync(project_fd)
            owned, digest = _stop_state(project_fd, uid=uid)
            require(owned and digest == hashlib.sha256(data).hexdigest(), "stop_readback_failed")
            return {"schema_version": 1, "slug": SLUG, "pause_requested": True, "stop_sha256": digest}
        finally:
            os.close(project_fd)
    finally:
        os.close(base_fd)


def main() -> int:
    try:
        require(os.environ.get("VIDEO_WORKDIR") == str(WORK_BASE), "video_workdir_drift")
        if sys.argv[1:] == ["inspect"]:
            output = snapshot()
        elif sys.argv[1:] == ["pause"]:
            output = place_stop()
        else:
            raise Stop("invalid_mode")
        print(json.dumps(output, sort_keys=True))
        return 0
    except (Stop, OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "STOP", "reason": str(exc) if isinstance(exc, Stop) else type(exc).__name__}), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
