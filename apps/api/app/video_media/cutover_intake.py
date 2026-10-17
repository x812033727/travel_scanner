"""Root-owned, on-volume gate for paid media intake during the A01 cutover.

The API's video-work mount is read-only. A bootstrap marker must be installed
*before* this code is deployed; missing or invalid files refuse paid intake.
Arming is monotonic: a durable, no-clobber ``armed.json`` is written before
``PAUSED_ALL``, and its presence permanently invalidates ``BOOTSTRAP_ALLOW``.
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from redis.asyncio import Redis

from app.video_media.dispatch_fence import PINNED_JOB_ID

A01_SLUG = "story-rolling-suitcase-v2"
INTAKE_DIR = Path(".a01-paid-intake")
MARKER = "marker.json"
ARMED = "armed.json"
NONCE_KEY = f"video-media:lock:{PINNED_JOB_ID}"
MAX_BYTES = 4096
ROOT_UID = 0
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
STATES = {"BOOTSTRAP_ALLOW", "PAUSED_ALL", "ALLOW_A01_ONLY"}


class IntakeFenceError(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class IntakeState:
    state: str
    bootstrap_id: str
    plan_sha256: str | None
    target_sha: str | None
    nonce_sha256: str | None
    marker_sha256: str
    armed_sha256: str | None


def canonical_json(value: dict[str, Any]) -> bytes:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (rendered + "\n").encode("utf-8")


def _directory(path: Path) -> None:
    try:
        info = path.lstat()
    except OSError as error:
        raise IntakeFenceError("directory_missing_or_unreadable") from error
    if not stat.S_ISDIR(info.st_mode):
        raise IntakeFenceError("directory_not_real")
    if path.name == INTAKE_DIR.name and os.name == "posix":
        if info.st_uid != ROOT_UID or stat.S_IMODE(info.st_mode) != 0o755:
            raise IntakeFenceError("directory_owner_or_mode")


def _read_file(path: Path) -> tuple[dict[str, Any], str]:
    try:
        if not stat.S_ISREG(path.lstat().st_mode):
            raise IntakeFenceError("file_not_bounded_regular")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_CLOEXEC", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_BYTES:
                raise IntakeFenceError("file_not_bounded_regular")
            if os.name == "posix" and (
                info.st_uid != ROOT_UID or stat.S_IMODE(info.st_mode) != 0o644
            ):
                raise IntakeFenceError("file_owner_or_mode")
            data = os.read(fd, MAX_BYTES + 1)
        finally:
            os.close(fd)
    except OSError as error:
        raise IntakeFenceError("file_missing_or_unreadable") from error
    if len(data) != info.st_size:
        raise IntakeFenceError("file_changed_during_read")

    def unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise IntakeFenceError("duplicate_key")
            value[key] = item
        return value

    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=unique_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise IntakeFenceError("invalid_json") from error
    if not isinstance(value, dict) or data != canonical_json(value):
        raise IntakeFenceError("noncanonical_object")
    return value, hashlib.sha256(data).hexdigest()


def _optional_armed(path: Path) -> tuple[dict[str, Any], str] | None:
    try:
        path.lstat()
    except FileNotFoundError:
        return None
    except OSError as error:
        raise IntakeFenceError("armed_unreadable") from error
    return _read_file(path)


def _is_hex(value: Any, pattern: re.Pattern[str]) -> bool:
    return isinstance(value, str) and bool(pattern.fullmatch(value))


def inspect_intake(video_work_dir: str | Path) -> IntakeState:
    """Read exact file bytes on each request; never cache a past allow decision."""
    root = Path(video_work_dir)
    _directory(root)
    folder = root / INTAKE_DIR
    _directory(folder)
    marker, marker_sha = _read_file(folder / MARKER)
    if set(marker) != {
        "schema_version",
        "state",
        "bootstrap_id",
        "plan_sha256",
        "target_sha",
        "nonce_sha256",
    } or type(marker["schema_version"]) is not int or marker["schema_version"] != 1:
        raise IntakeFenceError("marker_schema")
    state = marker["state"]
    if (
        not isinstance(state, str)
        or state not in STATES
        or not _is_hex(marker["bootstrap_id"], HEX64)
    ):
        raise IntakeFenceError("marker_identity")
    armed = _optional_armed(folder / ARMED)
    if state == "BOOTSTRAP_ALLOW":
        if any(marker[key] is not None for key in ("plan_sha256", "target_sha", "nonce_sha256")):
            raise IntakeFenceError("bootstrap_fields")
        if armed is not None:
            raise IntakeFenceError("bootstrap_rollback_refused")
        armed_sha = None
    else:
        if not _is_hex(marker["plan_sha256"], HEX64) or not _is_hex(
            marker["target_sha"], HEX40
        ):
            raise IntakeFenceError("cutover_identity")
        if armed is None:
            raise IntakeFenceError("armed_missing")
        armed_value, armed_sha = armed
        if armed_value != {
            "schema_version": 1,
            "bootstrap_id": marker["bootstrap_id"],
            "plan_sha256": marker["plan_sha256"],
            "target_sha": marker["target_sha"],
        }:
            raise IntakeFenceError("armed_mismatch")
        if state == "PAUSED_ALL" and marker["nonce_sha256"] is not None:
            raise IntakeFenceError("paused_nonce")
        if state == "ALLOW_A01_ONLY" and not _is_hex(marker["nonce_sha256"], HEX64):
            raise IntakeFenceError("allow_nonce_missing")
    return IntakeState(
        state=state,
        bootstrap_id=marker["bootstrap_id"],
        plan_sha256=marker["plan_sha256"],
        target_sha=marker["target_sha"],
        nonce_sha256=marker["nonce_sha256"],
        marker_sha256=marker_sha,
        armed_sha256=armed_sha,
    )


async def enforce_paid_intake(
    video_work_dir: str | Path, slug: str, redis: Redis
) -> IntakeState:
    receipt = inspect_intake(video_work_dir)
    if receipt.state == "BOOTSTRAP_ALLOW":
        return receipt
    if receipt.state == "PAUSED_ALL" or slug != A01_SLUG:
        raise IntakeFenceError("cutover_paused")
    try:
        async with redis.pipeline(transaction=True) as pipe:
            pipe.get(NONCE_KEY)
            pipe.ttl(NONCE_KEY)
            nonce, ttl = await asyncio.wait_for(pipe.execute(), timeout=5)
    except Exception as error:  # noqa: BLE001 - Redis failure must never open paid intake
        raise IntakeFenceError("nonce_unavailable") from error
    if isinstance(nonce, str):
        try:
            nonce = nonce.encode("ascii")
        except UnicodeEncodeError as error:
            raise IntakeFenceError("nonce_drift") from error
    if (
        not isinstance(nonce, bytes)
        or not hmac.compare_digest(hashlib.sha256(nonce).hexdigest(), receipt.nonce_sha256 or "")
        or ttl != -1
    ):
        raise IntakeFenceError("nonce_drift")
    return receipt
