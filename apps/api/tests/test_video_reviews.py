"""/admin/videos: the review file store, the decision rules, and who may call what."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.auth.service import current_user
from app.config import Settings
from app.db import get_session
from app.models import User, VideoReview, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_reviews import admin_api, admin_service
from app.video_reviews.schemas import DecisionIn, ReviewIn
from app.video_reviews.storage import PART_BYTES, ReviewStore, StorageRefused
from app.video_speech import admin_api as speech_api


def _store(root: Path, **limits: int) -> ReviewStore:
    return ReviewStore(
        root,
        max_file_bytes=limits.get("max_file_bytes", 50_000_000),
        max_total_bytes=limits.get("max_total_bytes", 100_000_000),
    )


def _parts(data: bytes) -> list[bytes]:
    return [data[start : start + PART_BYTES] for start in range(0, len(data), PART_BYTES)]


def test_parts_arrive_in_any_order_and_the_last_one_assembles_and_verifies(tmp_path: Path) -> None:
    store = _store(tmp_path)
    data = bytes(range(256)) * (PART_BYTES // 256 * 2 + 3)
    sha = hashlib.sha256(data).hexdigest()
    chunks = _parts(data)
    assert len(chunks) == 3
    first = store.put_part("ai-model-choice", sha, index=2, count=3, size=len(data), data=chunks[2])
    assert (first.received, first.complete) == ([2], False)
    assert store.path("ai-model-choice", sha) is None
    store.put_part("ai-model-choice", sha, index=0, count=3, size=len(data), data=chunks[0])
    done = store.put_part("ai-model-choice", sha, index=1, count=3, size=len(data), data=chunks[1])
    assert done.complete
    path = store.path("ai-model-choice", sha)
    assert path is not None and path.read_bytes() == data
    assert not (tmp_path / "ai-model-choice" / ".parts").joinpath(sha).exists()
    again = store.put_part("ai-model-choice", sha, index=0, count=3, size=len(data), data=b"")
    assert again.complete, "a finished file is not uploaded twice"


def test_parts_that_do_not_add_up_to_the_hash_are_thrown_away(tmp_path: Path) -> None:
    store = _store(tmp_path)
    data = b"preview"
    with pytest.raises(StorageRefused) as mismatch:
        store.put_part("v", "0" * 64, index=0, count=1, size=len(data), data=data)
    assert mismatch.value.code == "video_review_hash_mismatch"
    assert store.path("v", "0" * 64) is None
    sha = hashlib.sha256(data).hexdigest()
    with pytest.raises(StorageRefused) as short:
        store.put_part("v", sha, index=0, count=1, size=len(data), data=data[:3])
    assert short.value.code == "video_review_bad_part"
    with pytest.raises(StorageRefused) as count:
        store.put_part("v", sha, index=0, count=2, size=len(data), data=data)
    assert count.value.code == "video_review_bad_part"


def test_names_limits_and_the_total_cap_are_enforced(tmp_path: Path) -> None:
    store = _store(tmp_path, max_file_bytes=1_000_000, max_total_bytes=1_000_010)
    for slug in ("../etc", "UPPER", "a" * 81, ""):
        with pytest.raises(StorageRefused):
            store.put_part(slug, "a" * 64, index=0, count=1, size=1, data=b"x")
    with pytest.raises(StorageRefused) as not_hex:
        store.path("ok", "../../secret")
    assert not_hex.value.code == "video_review_bad_hash"
    with pytest.raises(StorageRefused) as too_big:
        store.put_part("ok", "a" * 64, index=0, count=1, size=1_000_001, data=b"x")
    assert too_big.value.status == 413
    first = b"a" * 1_000_000
    store.put_part(
        "ok", hashlib.sha256(first).hexdigest(), index=0, count=1, size=len(first), data=first
    )
    second = b"b" * 20
    with pytest.raises(StorageRefused) as full:
        store.put_part(
            "ok", hashlib.sha256(second).hexdigest(), index=0, count=1, size=20, data=second
        )
    assert full.value.status == 507


def test_only_files_a_live_review_shows_are_kept(tmp_path: Path) -> None:
    store = _store(tmp_path)
    names = []
    for body in (b"old cut", b"new cut", b"sheet"):
        sha = hashlib.sha256(body).hexdigest()
        store.put_part("v", sha, index=0, count=1, size=len(body), data=body)
        names.append(sha)
    reviews = [
        VideoReview(status="superseded", files=[{"sha256": names[0]}]),
        VideoReview(status="pending", files=[{"sha256": names[1]}, {"sha256": names[2]}]),
    ]
    assert admin_service.kept_files(reviews) == {names[1], names[2]}
    assert store.keep_only("v", admin_service.kept_files(reviews)) == [names[0]]
    assert store.path("v", names[1]) is not None and store.path("v", names[0]) is None


def _review(
    gate: str, status: str = "pending", payload: dict[str, Any] | None = None
) -> VideoReview:
    return VideoReview(gate=gate, status=status, payload=payload or {}, files=[])


def test_decisions_need_a_pending_review_a_reason_to_reject_and_an_outline_choice() -> None:
    outline = _review("outline", payload={"options": [{"key": "A"}, {"key": "B"}, {"key": "C"}]})
    assert admin_service.outline_choices(outline.payload) == ["A", "B", "C"]
    approve = DecisionIn(decision="approve")
    assert "選一個大綱" in (admin_service.decision_problem(outline, approve) or "")
    assert (
        admin_service.decision_problem(outline, DecisionIn(decision="approve", choice="B")) is None
    )
    assert admin_service.decision_problem(outline, DecisionIn(decision="approve", choice="D"))
    assert "原因" in (
        admin_service.decision_problem(_review("final"), DecisionIn(decision="reject")) or ""
    )
    assert (
        admin_service.decision_problem(
            _review("final"), DecisionIn(decision="reject", note="片頭太長")
        )
        is None
    )
    assert admin_service.decision_problem(_review("audio", "superseded"), approve)
    assert admin_service.decision_problem(_review("publish"), approve) is None


def test_a_review_payload_is_capped() -> None:
    body = {"gate": "final", "content_sha256": "a" * 64, "summary": "成片"}
    ReviewIn.model_validate({**body, "payload": {"text": "字" * 1000}})
    with pytest.raises(ValueError):
        ReviewIn.model_validate({**body, "payload": {"text": "字" * 100_000}})


def _app(user: User | None = None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.tool_router, prefix="/api/v1")
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    if user is not None:
        app.dependency_overrides[current_user] = lambda: user
    return app


@pytest.mark.asyncio
async def test_admin_routes_need_content_capabilities(monkeypatch: pytest.MonkeyPatch) -> None:
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    monkeypatch.setattr(admin_service, "list_projects", AsyncMock(return_value=[]))
    decide = AsyncMock()
    monkeypatch.setattr(admin_service, "decide", decide)
    app = _app(viewer)
    review = f"/api/v1/admin/videos/v/reviews/{uuid4()}/decision"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        nobody = await client.get("/api/v1/admin/videos")
        viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
        listed = await client.get("/api/v1/admin/videos")
        refused = await client.post(review, json={"decision": "approve"})
    assert nobody.status_code == 403 and listed.status_code == 200
    assert refused.status_code == 403, "a viewer can read but not decide"
    decide.assert_not_awaited()


@pytest.mark.asyncio
async def test_pipeline_routes_need_a_video_tool_token() -> None:
    app = _app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/video/reviews/v")
        admin = await client.get("/api/v1/admin/videos")
    assert response.status_code == 401
    assert admin.status_code == 401


@pytest.mark.asyncio
async def test_uploaded_parts_land_in_the_configured_store(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    app = _app()
    token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")
    app.dependency_overrides[speech_api.video_tool] = lambda: token
    body = b"narration preview"
    sha = hashlib.sha256(body).hexdigest()
    url = f"/api/v1/video/reviews/ai-model-choice/files/{sha}"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        done = await client.put(
            url, params={"part": 0, "parts": 1, "size": len(body)}, content=body
        )
        wrong = await client.put(
            f"/api/v1/video/reviews/ai-model-choice/files/{'b' * 64}",
            params={"part": 0, "parts": 1, "size": len(body)},
            content=body,
        )
    assert done.status_code == 200 and done.json() == {"received": [0], "complete": True}
    assert (tmp_path / "ai-model-choice" / sha).read_bytes() == body
    assert wrong.status_code == 422 and wrong.json()["code"] == "video_review_hash_mismatch"


@pytest.mark.asyncio
async def test_a_preview_is_served_with_byte_ranges_and_never_cached(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    preview = tmp_path / "preview.mp4"
    preview.write_bytes(bytes(range(200)))
    monkeypatch.setattr(
        admin_service, "file_for_admin", AsyncMock(return_value=(preview, "video/mp4"))
    )

    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    app = _app(owner)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            f"/api/v1/admin/videos/v/files/{'a' * 64}", headers={"Range": "bytes=10-19"}
        )
    assert response.status_code == 206
    assert response.content == bytes(range(10, 20))
    assert response.headers["content-type"] == "video/mp4"
    assert response.headers["cache-control"] == "private, no-store"
