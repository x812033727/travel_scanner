"""The A01 paid-media gate never opens on a missing, rolled-back or unheld state."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import fakeredis
import pytest

from app.video_media import cutover_intake as gate
from app.video_media.jobs import MediaJobFailed, advance_job, submit_job
from app.video_media.models import VideoMediaJob
from app.video_media.schemas import ImageJobIn

BOOTSTRAP_ID = "a" * 64
PLAN_SHA = "b" * 64
TARGET_SHA = "c" * 40
NONCE = b"durable-exact-job-nonce"


def _marker(state: str, *, nonce_sha256: str | None = None) -> dict[str, object]:
    return {
        "schema_version": 1,
        "state": state,
        "bootstrap_id": BOOTSTRAP_ID,
        "plan_sha256": None if state == "BOOTSTRAP_ALLOW" else PLAN_SHA,
        "target_sha": None if state == "BOOTSTRAP_ALLOW" else TARGET_SHA,
        "nonce_sha256": nonce_sha256,
    }


def _install(root: Path, state: str, *, nonce_sha256: str | None = None) -> Path:
    folder = root / gate.INTAKE_DIR
    folder.mkdir(mode=0o755, exist_ok=True)
    path = folder / gate.MARKER
    path.write_bytes(gate.canonical_json(_marker(state, nonce_sha256=nonce_sha256)))
    path.chmod(0o644)
    return path


def _arm(root: Path) -> None:
    path = root / gate.INTAKE_DIR / gate.ARMED
    path.write_bytes(
        gate.canonical_json(
            {
                "schema_version": 1,
                "bootstrap_id": BOOTSTRAP_ID,
                "plan_sha256": PLAN_SHA,
                "target_sha": TARGET_SHA,
            }
        )
    )
    path.chmod(0o644)


@pytest.fixture(autouse=True)
def local_owner(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    if os.name == "posix":
        monkeypatch.setattr(gate, "ROOT_UID", tmp_path.stat().st_uid)


@pytest.mark.asyncio
async def test_bootstrap_requires_explicit_marker_and_cannot_return_after_arming(
    tmp_path: Path,
) -> None:
    redis = fakeredis.aioredis.FakeRedis()
    with pytest.raises(gate.IntakeFenceError):
        await gate.enforce_paid_intake(tmp_path, "another-film", redis)
    marker = _install(tmp_path, "BOOTSTRAP_ALLOW")
    assert (await gate.enforce_paid_intake(tmp_path, "another-film", redis)).state == (
        "BOOTSTRAP_ALLOW"
    )
    _arm(tmp_path)
    with pytest.raises(gate.IntakeFenceError, match="bootstrap_rollback_refused"):
        await gate.enforce_paid_intake(tmp_path, "another-film", redis)
    assert marker.read_bytes() == gate.canonical_json(_marker("BOOTSTRAP_ALLOW"))


@pytest.mark.parametrize(
    "data",
    [b"{", b"[]", b'{"state":"BOOTSTRAP_ALLOW","state":"PAUSED_ALL"}', b"x" * 4097],
)
def test_bad_marker_never_opens(tmp_path: Path, data: bytes) -> None:
    marker = _install(tmp_path, "BOOTSTRAP_ALLOW")
    marker.write_bytes(data)
    with pytest.raises(gate.IntakeFenceError):
        gate.inspect_intake(tmp_path)


@pytest.mark.asyncio
async def test_paused_all_requires_matching_arm_and_denies_every_slug(tmp_path: Path) -> None:
    _install(tmp_path, "PAUSED_ALL")
    with pytest.raises(gate.IntakeFenceError, match="armed_missing"):
        gate.inspect_intake(tmp_path)
    _arm(tmp_path)
    assert gate.inspect_intake(tmp_path).state == "PAUSED_ALL"
    redis = fakeredis.aioredis.FakeRedis()
    for slug in (gate.A01_SLUG, "another-film"):
        with pytest.raises(gate.IntakeFenceError, match="cutover_paused"):
            await gate.enforce_paid_intake(tmp_path, slug, redis)


@pytest.mark.asyncio
async def test_only_a01_with_exact_durable_nonce_can_pass(
    tmp_path: Path
) -> None:
    _install(tmp_path, "ALLOW_A01_ONLY", nonce_sha256=hashlib.sha256(NONCE).hexdigest())
    _arm(tmp_path)
    redis = fakeredis.aioredis.FakeRedis()
    with pytest.raises(gate.IntakeFenceError, match="cutover_paused"):
        await gate.enforce_paid_intake(tmp_path, "another-film", redis)
    with pytest.raises(gate.IntakeFenceError, match="nonce_drift"):
        await gate.enforce_paid_intake(tmp_path, gate.A01_SLUG, redis)
    await redis.set(gate.NONCE_KEY, NONCE, ex=60)
    with pytest.raises(gate.IntakeFenceError, match="nonce_drift"):
        await gate.enforce_paid_intake(tmp_path, gate.A01_SLUG, redis)
    await redis.set(gate.NONCE_KEY, NONCE)
    receipt = await gate.enforce_paid_intake(tmp_path, gate.A01_SLUG, redis)
    assert receipt.state == "ALLOW_A01_ONLY" and receipt.armed_sha256 is not None
    decoded = fakeredis.aioredis.FakeRedis(decode_responses=True)
    await decoded.set(gate.NONCE_KEY, NONCE.decode("ascii"))
    assert (await gate.enforce_paid_intake(tmp_path, gate.A01_SLUG, decoded)).state == (
        "ALLOW_A01_ONLY"
    )
    await redis.delete(gate.NONCE_KEY)
    with pytest.raises(gate.IntakeFenceError, match="nonce_drift"):
        await gate.enforce_paid_intake(tmp_path, gate.A01_SLUG, redis)


def test_symlink_marker_is_refused(tmp_path: Path) -> None:
    marker = _install(tmp_path, "BOOTSTRAP_ALLOW")
    other = tmp_path / "other.json"
    other.write_bytes(marker.read_bytes())
    marker.unlink()
    try:
        marker.symlink_to(other)
    except OSError:
        pytest.skip("symlink creation unavailable")
    with pytest.raises(gate.IntakeFenceError):
        gate.inspect_intake(tmp_path)


@pytest.mark.asyncio
async def test_direct_job_functions_stop_before_session_or_vendor(tmp_path: Path) -> None:
    _install(tmp_path, "PAUSED_ALL")
    _arm(tmp_path)
    ctx = SimpleNamespace(
        runtime=SimpleNamespace(video_work_dir=str(tmp_path)),
        redis=fakeredis.aioredis.FakeRedis(),
    )
    payload = ImageJobIn.model_validate(
        {"slug": "another-film", "purpose": "keyframe", "prompt": "a drawing"}
    )
    with pytest.raises(MediaJobFailed) as submitted:
        await submit_job(ctx, "image", payload)  # type: ignore[arg-type]
    assert (submitted.value.status, submitted.value.code) == (
        423,
        "video_media_cutover_paused",
    )
    job = VideoMediaJob(
        id=uuid4(),
        slug="another-film",
        kind="image",
        purpose="keyframe",
        provider="minimax",
        model="image-01",
        request={},
        request_hash="h",
        status="queued",
        attempts=0,
        polls=0,
        seconds=0,
        usd_estimate=0.0035,
    )
    with pytest.raises(MediaJobFailed) as advanced:
        await advance_job(ctx, job)  # type: ignore[arg-type]
    assert (advanced.value.status, advanced.value.code) == (
        423,
        "video_media_cutover_paused",
    )
