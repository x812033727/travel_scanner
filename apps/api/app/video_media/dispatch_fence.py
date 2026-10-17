"""Fail-closed dispatch fence for one pre-existing, unsubmitted media job.

This incident-specific pin is intentional. Removing the on-volume marker cannot silently
resume the job: the compiled ID still refuses dispatch until a separately reviewed code
change removes it. The API sees ``video_work_dir`` through its existing read-only mount.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any
from uuid import UUID

from app.video_media.models import VideoMediaJob

PINNED_JOB_ID = UUID("b721a65d-8c8d-4ae8-834c-391cfc267a6f")
PINNED_SLUG = "google-project-suncatcher-prototype-what-it-tests"
PINNED_REQUEST_HASH = "52b39c04a45f39b4101bcd7e401c31cd0e6083f3c8390b729afd2a83569379e6"
PINNED_KIND = "image"
PINNED_PROVIDER = "minimax"
PINNED_MODEL = "image-01"
FENCE_DIR = Path(".ops") / "media-dispatch-fences"
MAX_MANIFEST_BYTES = 4096


class DispatchFenceError(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def fence_path(video_work_dir: str | Path, job_id: UUID = PINNED_JOB_ID) -> Path:
    return Path(video_work_dir) / FENCE_DIR / f"{job_id}.json"


def expected_manifest(job: VideoMediaJob) -> dict[str, str | int]:
    if job.id != PINNED_JOB_ID:
        raise DispatchFenceError("wrong_job_id")
    if (
        job.slug,
        job.request_hash,
        job.kind,
        job.provider,
        job.model,
    ) != (
        PINNED_SLUG,
        PINNED_REQUEST_HASH,
        PINNED_KIND,
        PINNED_PROVIDER,
        PINNED_MODEL,
    ):
        raise DispatchFenceError("job_identity_changed")
    if job.status != "queued" or job.vendor_ref is not None or job.submitted_at is not None:
        raise DispatchFenceError("job_no_longer_unsubmitted")
    return {
        "version": 1,
        "job_id": str(job.id),
        "slug": job.slug,
        "request_hash": job.request_hash,
        "kind": job.kind,
        "provider": job.provider,
        "model": job.model,
        "status": "queued",
    }


def _read_regular_file(path: Path) -> bytes:
    """Read only a bounded regular file; reject symlinks and special files."""
    try:
        flags = (
            os.O_RDONLY
            | getattr(os, "O_BINARY", 0)
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        fd = os.open(path, flags)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_MANIFEST_BYTES:
                raise DispatchFenceError("marker_not_bounded_regular_file")
            data = os.read(fd, MAX_MANIFEST_BYTES + 1)
        finally:
            os.close(fd)
    except FileNotFoundError as error:
        raise DispatchFenceError("marker_missing") from error
    except OSError as error:
        raise DispatchFenceError("marker_unreadable") from error
    if len(data) != info.st_size:
        raise DispatchFenceError("marker_changed_during_read")
    return data


def _strict_json(data: bytes) -> dict[str, Any]:
    def no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise DispatchFenceError("marker_duplicate_key")
            result[key] = value
        return result

    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=no_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DispatchFenceError("marker_invalid_json") from error
    if not isinstance(value, dict):
        raise DispatchFenceError("marker_not_object")
    return value


def inspect_manifest(job: VideoMediaJob, path: Path) -> str:
    """Return raw-file SHA-256 only when every field matches the current DB row."""
    expected = expected_manifest(job)
    data = _read_regular_file(path)
    value = _strict_json(data)
    if value != expected or type(value.get("version")) is not int:
        raise DispatchFenceError("marker_mismatch")
    return hashlib.sha256(data).hexdigest()


def inspect_installed_fence(job: VideoMediaJob, video_work_dir: str | Path) -> str:
    """Require an exact marker on the shared volume for the compiled target ID."""
    if job.id != PINNED_JOB_ID:
        raise DispatchFenceError("wrong_job_id")
    root = Path(video_work_dir)
    for directory in (root, root / ".ops", root / FENCE_DIR):
        try:
            info = directory.lstat()
        except FileNotFoundError as error:
            raise DispatchFenceError("marker_directory_missing") from error
        except OSError as error:
            raise DispatchFenceError("marker_directory_unreadable") from error
        if not stat.S_ISDIR(info.st_mode):
            raise DispatchFenceError("marker_directory_not_real")
    return inspect_manifest(job, fence_path(root))
