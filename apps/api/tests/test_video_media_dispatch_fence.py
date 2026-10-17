"""An incident-specific queued job cannot resume by deleting or corrupting its marker."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from app.video_media import dispatch_fence, dispatch_fence_cli, dispatch_fence_cutover
from app.video_media.models import VideoMediaJob


def _job(**changes: Any) -> VideoMediaJob:
    fields = {
        "id": dispatch_fence.PINNED_JOB_ID,
        "slug": "google-project-suncatcher-prototype-what-it-tests",
        "kind": "image",
        "purpose": "keyframe",
        "provider": "minimax",
        "model": "image-01",
        "request": {},
        "request_hash": "52b39c04a45f39b4101bcd7e401c31cd0e6083f3c8390b729afd2a83569379e6",
        "status": "queued",
        "attempts": 1,
        "polls": 0,
        "seconds": 0,
        "usd_estimate": 0.0035,
        **changes,
    }
    return VideoMediaJob(**fields)


def _install(root: Path, job: VideoMediaJob) -> tuple[Path, bytes]:
    path = dispatch_fence.fence_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = dispatch_fence_cli.canonical_manifest(job).encode("utf-8")
    path.write_bytes(data)
    return path, data


def test_exact_regular_marker_matches_current_row_and_survives_process_restart(
    tmp_path: Path,
) -> None:
    job = _job()
    path, data = _install(tmp_path, job)
    digest = hashlib.sha256(data).hexdigest()
    assert dispatch_fence.inspect_installed_fence(job, tmp_path) == digest
    # A new ORM object/runtime after a restart reads the same host-persisted marker.
    assert dispatch_fence.inspect_installed_fence(_job(), tmp_path) == digest
    assert path.read_bytes() == data


@pytest.mark.parametrize(
    ("replacement", "reason"),
    [
        (b"{", "marker_invalid_json"),
        (b"[]", "marker_not_object"),
        (b'{"version":1,"version":1}', "marker_duplicate_key"),
        (b"x" * 4097, "marker_not_bounded_regular_file"),
    ],
)
def test_malformed_marker_fails_closed(
    tmp_path: Path, replacement: bytes, reason: str
) -> None:
    path, _ = _install(tmp_path, _job())
    path.write_bytes(replacement)
    with pytest.raises(dispatch_fence.DispatchFenceError, match=reason):
        dispatch_fence.inspect_installed_fence(_job(), tmp_path)


@pytest.mark.parametrize(
    "field,value", [("slug", "other"), ("request_hash", "a" * 64), ("model", "other")]
)
def test_mismatched_marker_fails_closed(tmp_path: Path, field: str, value: str) -> None:
    path, _ = _install(tmp_path, _job())
    marker = json.loads(path.read_text(encoding="utf-8"))
    marker[field] = value
    path.write_text(json.dumps(marker), encoding="utf-8")
    with pytest.raises(dispatch_fence.DispatchFenceError, match="marker_mismatch"):
        dispatch_fence.inspect_installed_fence(_job(), tmp_path)


def test_missing_marker_and_changed_job_are_both_refused(tmp_path: Path) -> None:
    job = _job()
    with pytest.raises(dispatch_fence.DispatchFenceError, match="marker_directory_missing"):
        dispatch_fence.inspect_installed_fence(job, tmp_path)
    path, _ = _install(tmp_path, job)
    path.unlink()
    with pytest.raises(dispatch_fence.DispatchFenceError, match="marker_missing"):
        dispatch_fence.inspect_installed_fence(job, tmp_path)
    _install(tmp_path, job)
    with pytest.raises(dispatch_fence.DispatchFenceError, match="job_no_longer_unsubmitted"):
        dispatch_fence.inspect_installed_fence(_job(status="submitted"), tmp_path)
    with pytest.raises(dispatch_fence.DispatchFenceError, match="job_identity_changed"):
        dispatch_fence.inspect_installed_fence(_job(slug="other"), tmp_path)


@pytest.mark.asyncio
async def test_cli_proposes_validates_and_checks_without_advancing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    job = _job()
    active_count = [1]
    lock_present = [0]

    class ReadSession:
        async def __aenter__(self) -> ReadSession:
            return self

        async def __aexit__(self, *_args: Any) -> None:
            return None

        async def execute(self, _statement: Any) -> Any:
            return SimpleNamespace(one_or_none=lambda: (job, active_count[0]))

    monkeypatch.setattr(dispatch_fence_cli, "SessionFactory", ReadSession)
    monkeypatch.setattr(
        dispatch_fence_cli,
        "get_settings",
        lambda: SimpleNamespace(video_work_dir=str(tmp_path), redis_url="redis://unused"),
    )

    class ReadRedis:
        async def __aenter__(self) -> ReadRedis:
            return self

        async def __aexit__(self, *_args: Any) -> None:
            return None

        async def exists(self, _key: str) -> int:
            return lock_present[0]

    monkeypatch.setattr(
        dispatch_fence_cli,
        "Redis",
        SimpleNamespace(from_url=lambda *_args, **_kw: ReadRedis()),
    )
    proposed = await dispatch_fence_cli.run(
        argparse.Namespace(action="propose", job_id=dispatch_fence.PINNED_JOB_ID)
    )
    assert isinstance(proposed, str)
    path = dispatch_fence.fence_path(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_bytes(proposed.encode("utf-8"))
    validated = await dispatch_fence_cli.run(
        argparse.Namespace(action="validate", job_id=job.id, manifest=path)
    )
    checked = await dispatch_fence_cli.run(argparse.Namespace(action="check", job_id=job.id))
    assert isinstance(validated, dict) and isinstance(checked, dict)
    assert validated["enforced"] is False and checked["enforced"] is True
    assert validated["media_lock_absent"] is None and checked["media_lock_absent"] is True
    assert checked["active_media_count"] == 1
    assert checked["fence_sha256"] == hashlib.sha256(proposed.encode("utf-8")).hexdigest()
    assert checked["job"] == {
        "id": str(job.id),
        "slug": job.slug,
        "request_hash": job.request_hash,
        "kind": job.kind,
        "provider": job.provider,
        "model": job.model,
        "status": "queued",
        "vendor_ref": None,
        "submitted_at": None,
    }
    assert len(checked["code"]["jobs_sha256"]) == 64
    assert len(checked["code"]["dispatch_fence_sha256"]) == 64
    assert len(checked["code"]["admin_api_sha256"]) == 64
    assert checked["b25_direct_intake"] == {
        "slug": "story-adapt-seiko-quartz-astron",
        "compiled_guard": True,
    }
    lock_present[0] = 1
    held = await dispatch_fence_cli.run(
        argparse.Namespace(action="check", job_id=job.id, expect_operator_lock=True)
    )
    assert isinstance(held, dict)
    assert held["media_lock_absent"] is False and held["operator_lock_expected"] is True
    with pytest.raises(dispatch_fence.DispatchFenceError, match="media_job_lock_present"):
        await dispatch_fence_cli.run(argparse.Namespace(action="check", job_id=job.id))
    active_count[0] = 2
    with pytest.raises(dispatch_fence.DispatchFenceError, match="active_media_count_changed"):
        await dispatch_fence_cli.run(
            argparse.Namespace(action="check", job_id=job.id, expect_operator_lock=True)
        )


@pytest.mark.asyncio
async def test_cli_rejects_missing_or_wrong_job_without_a_fence_read(tmp_path: Path) -> None:
    with pytest.raises(dispatch_fence.DispatchFenceError, match="wrong_job_id"):
        await dispatch_fence_cli.run(argparse.Namespace(action="check", job_id=uuid4()))
    with pytest.raises(dispatch_fence.DispatchFenceError, match="marker_directory_missing"):
        dispatch_fence.inspect_installed_fence(_job(), tmp_path)


def test_b25_cli_receipt_fails_closed_when_compiled_refusal_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(dispatch_fence_cli, "refuse_b25_cutover_media", lambda _slug: None)
    with pytest.raises(dispatch_fence.DispatchFenceError, match="b25_direct_guard_missing"):
        dispatch_fence_cli.b25_guard_receipt()


class FakeCutoverRedis:
    def __init__(self, *, waitaof_local: int = 1) -> None:
        self.value: bytes | None = None
        self.waitaof_local = waitaof_local
        self.calls: list[tuple[str, Any]] = []

    def client(self) -> FakeCutoverRedis:
        self.calls.append(("client", None))
        return self

    async def aclose(self) -> None:
        return None

    async def __aenter__(self) -> FakeCutoverRedis:
        return self

    async def __aexit__(self, *_args: Any) -> None:
        return None

    async def set(self, key: str, value: str, *, nx: bool) -> bool:
        self.calls.append(("set", (key, value, nx)))
        if self.value is not None:
            return False
        self.value = value.encode("ascii")
        return True

    async def execute_command(self, name: str, *args: Any) -> list[int]:
        self.calls.append((name, args))
        return [self.waitaof_local, 0]

    async def get(self, key: str) -> bytes | None:
        self.calls.append(("get", key))
        return self.value

    async def ttl(self, key: str) -> int:
        self.calls.append(("ttl", key))
        return -1

    async def eval(self, script: str, count: int, key: str, nonce: str) -> int:
        self.calls.append(("eval", (script, count, key)))
        if self.value != nonce.encode("ascii"):
            return 0
        self.value = None
        return 1


@pytest.mark.asyncio
async def test_cutover_nonce_set_and_waitaof_share_one_connection() -> None:
    redis = FakeCutoverRedis()
    nonce = "a" * 64
    receipt, code = await dispatch_fence_cutover.acquire(redis, nonce=nonce)  # type: ignore[arg-type]
    assert code == 0 and receipt["durable"] is True and receipt["waitaof_local"] == 1
    assert receipt["nonce"] == nonce
    assert [name for name, _ in redis.calls[:4]] == ["client", "set", "WAITAOF", "get"]
    assert redis.calls[1][1] == (dispatch_fence_cutover.KEY, nonce, True)
    assert redis.calls[2][1] == (1, 0, dispatch_fence_cutover.WAITAOF_TIMEOUT_MS)
    assert (await dispatch_fence_cutover.inspect(redis, receipt))["owned"] is True  # type: ignore[arg-type]
    assert (await dispatch_fence_cutover.release(redis, receipt))["released_own_nonce"] is True  # type: ignore[arg-type]
    assert redis.value is None


@pytest.mark.asyncio
async def test_cutover_nx_refuses_overwrite_and_cas_never_deletes_another_nonce() -> None:
    redis = FakeCutoverRedis()
    receipt, code = await dispatch_fence_cutover.acquire(redis, nonce="a" * 64)  # type: ignore[arg-type]
    assert code == 0
    with pytest.raises(dispatch_fence_cutover.CutoverLockError, match="lock_already_exists"):
        await dispatch_fence_cutover.acquire(redis, nonce="b" * 64)  # type: ignore[arg-type]
    redis.value = b"b" * 64
    with pytest.raises(dispatch_fence_cutover.CutoverLockError, match="nonce_lost_or_replaced"):
        await dispatch_fence_cutover.release(redis, receipt)  # type: ignore[arg-type]
    assert redis.value == b"b" * 64


@pytest.mark.asyncio
async def test_cutover_waitaof_failure_returns_recovery_nonce_but_refuses_release() -> None:
    redis = FakeCutoverRedis(waitaof_local=0)
    receipt, code = await dispatch_fence_cutover.acquire(redis, nonce="a" * 64)  # type: ignore[arg-type]
    assert code == 3 and receipt["durable"] is False and receipt["nonce"] == "a" * 64
    assert redis.value == b"a" * 64
    with pytest.raises(dispatch_fence_cutover.CutoverLockError, match="acquire_not_durable"):
        await dispatch_fence_cutover.release(redis, receipt)  # type: ignore[arg-type]


@pytest.mark.skipif(os.name == "nt", reason="the cutover helper runs in Linux containers")
@pytest.mark.asyncio
async def test_cutover_cli_creates_private_receipt_before_set_without_printing_nonce(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redis = FakeCutoverRedis()
    path = Path("/tmp") / f"a01-media-cutover-test-{uuid4()}.json"
    monkeypatch.setenv("REDIS_URL", "redis://unused")
    monkeypatch.setattr(
        dispatch_fence_cutover,
        "Redis",
        SimpleNamespace(from_url=lambda *_args, **_kw: redis),
    )
    try:
        safe, code = await dispatch_fence_cutover.run("acquire", path)
        assert code == 0 and isinstance(safe, dict)
        receipt = json.loads(path.read_text(encoding="utf-8"))
        assert path.stat().st_mode & 0o077 == 0
        assert receipt["nonce"] not in json.dumps(safe)
        assert receipt["durable"] is True and redis.value == receipt["nonce"].encode("ascii")
    finally:
        path.unlink(missing_ok=True)
