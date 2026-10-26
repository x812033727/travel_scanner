"""The video tool reads back a video's live review attachments (``review-files``)."""

from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.config import Settings
from app.db import get_session
from app.models import VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_reviews import admin_api, admin_service, tool_files
from app.video_reviews.storage import ReviewStore
from app.video_speech import admin_api as speech_api


def _put(store: ReviewStore, slug: str, body: bytes) -> str:
    sha = hashlib.sha256(body).hexdigest()
    store.put_part(slug, sha, index=0, count=1, size=len(body), data=body)
    return sha


def _review(
    gate: str, status: str, *files: tuple[str, str, str], payload: dict[str, Any] | None = None
) -> Any:
    return SimpleNamespace(
        id=uuid4(),
        gate=gate,
        status=status,
        payload=payload or {},
        files=[
            {"role": role, "sha256": sha, "content_type": kind, "size": 1}
            for role, sha, kind in files
        ],
    )


@pytest.fixture
def store(tmp_path: Path) -> ReviewStore:
    return ReviewStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)


@pytest.mark.asyncio
async def test_only_a_pending_or_approved_review_s_files_are_read_back(
    monkeypatch: pytest.MonkeyPatch, store: ReviewStore
) -> None:
    final = _put(store, "v", b"approved final")
    dub = _put(store, "v", b"pending dub")
    rejected = _put(store, "v", b"rejected cut")
    superseded = _put(store, "v", b"old captions")
    unlisted = _put(store, "v", b"nobody lists me")
    reviews = [
        _review("languages", "pending", ("dub_en", dub, "audio/mp4")),
        _review("publish", "approved", ("final", final, "video/mp4")),
        _review("final", "rejected", ("final", rejected, "video/mp4")),
        _review("languages", "superseded", ("captions_en", superseded, "application/x-subrip")),
    ]
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=object()))
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=reviews))

    path, kind = await tool_files.file_for_tool(AsyncMock(), store, "v", final)
    assert (path.read_bytes(), kind) == (b"approved final", "video/mp4")
    path, kind = await tool_files.file_for_tool(AsyncMock(), store, "v", dub)
    assert (path.read_bytes(), kind) == (b"pending dub", "audio/mp4")
    for sha in (rejected, superseded, unlisted, "A" * 64, "../etc"):
        with pytest.raises(AppError) as refused:
            await tool_files.file_for_tool(AsyncMock(), store, "v", sha)
        assert refused.value.code == "video_review_file_not_found", sha
    assert [(row["gate"], row["role"]) for row in tool_files.listing(reviews)] == [
        ("languages", "dub_en"),
        ("publish", "final"),
    ]


@pytest.mark.asyncio
async def test_an_owner_renewal_keeps_the_reviews_it_retains_readable(
    monkeypatch: pytest.MonkeyPatch, store: ReviewStore
) -> None:
    old_cut = _put(store, "v", b"old final")
    old_dub = _put(store, "v", b"old dub")
    stray = _put(store, "v", b"an unrelated superseded file")
    old_final = _review("final", "superseded", ("final", old_cut, "video/mp4"))
    old_languages = _review("languages", "superseded", ("dub_en", old_dub, "audio/mp4"))
    unrelated = _review("languages", "superseded", ("dub_ja", stray, "audio/mp4"))
    retained = {"retained_review_ids": [str(old_final.id), str(old_languages.id)]}
    renewal = _review("final", "pending", payload={admin_service.RENEWAL_KEY: retained})
    reviews = [renewal, unrelated, old_languages, old_final]
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=object()))
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=reviews))

    path, kind = await tool_files.file_for_tool(AsyncMock(), store, "v", old_dub)
    assert (path.read_bytes(), kind) == (b"old dub", "audio/mp4")
    path, _ = await tool_files.file_for_tool(AsyncMock(), store, "v", old_cut)
    assert path.read_bytes() == b"old final"
    with pytest.raises(AppError):
        await tool_files.file_for_tool(AsyncMock(), store, "v", stray)
    assert [(row["gate"], row["status"]) for row in tool_files.listing(reviews)] == [
        ("languages", "superseded"),
        ("final", "superseded"),
    ]

    # A rejected renewal retains nothing: its old reviews go back to unreadable.
    renewal.status = "rejected"
    with pytest.raises(AppError):
        await tool_files.file_for_tool(AsyncMock(), store, "v", old_dub)


@pytest.mark.asyncio
async def test_a_listed_file_whose_bytes_left_the_store_is_not_found(
    monkeypatch: pytest.MonkeyPatch, store: ReviewStore
) -> None:
    gone = "c" * 64
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=object()))
    monkeypatch.setattr(
        admin_service,
        "_reviews",
        AsyncMock(return_value=[_review("publish", "approved", ("final", gone, "video/mp4"))]),
    )
    with pytest.raises(AppError) as missing:
        await tool_files.file_for_tool(AsyncMock(), store, "v", gone)
    assert missing.value.code == "video_review_file_not_found"


def _app() -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.tool_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    return app


@pytest.mark.asyncio
async def test_the_tool_route_serves_byte_ranges_uncached_and_needs_the_tool_token(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    final = tmp_path / "final.mp4"
    final.write_bytes(bytes(range(200)))
    lookup = AsyncMock(return_value=(final, "video/mp4"))
    monkeypatch.setattr(tool_files, "file_for_tool", lookup)
    limit = AsyncMock()
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", limit)

    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    app = _app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        anonymous = await client.get(f"/api/v1/video/reviews/v/files/{'a' * 64}")
        token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")
        app.dependency_overrides[speech_api.video_tool] = lambda: token
        ranged = await client.get(
            f"/api/v1/video/reviews/v/files/{'a' * 64}", headers={"Range": "bytes=10-19"}
        )
    assert anonymous.status_code == 401
    assert ranged.status_code == 206 and ranged.content == bytes(range(10, 20))
    assert ranged.headers["cache-control"] == "private, no-store"
    assert ranged.headers["etag"] == f'"{"a" * 64}"'
    assert lookup.await_args is not None and lookup.await_args.args[2:] == ("v", "a" * 64)
    assert limit.await_args is not None and limit.await_args.args[0] == "video_review_download"
