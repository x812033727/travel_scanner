"""An imported drama's upload package carries its per-shot clips (``clip_<shot>`` mp4 files).

`import --publish` (tools/video/import/import.mjs) attaches them so the worker can place them in
video_work/<slug>/clips/ and the full-tier Drive backup keeps them (docs/videos/BACKUP.md). They
count apart from the 48 files a review may carry, and only the publish gate takes them.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError

from app.db import get_session
from app.models import VideoToolToken
from app.video_reviews import admin_api, admin_service
from app.video_reviews.clips import MAX_CLIP_FILES, SubmittedReview
from app.video_reviews.schemas import MAX_REVIEW_FILES, ReviewOut
from app.video_speech import admin_api as speech_api

SHA = "a" * 64


def _file(role: str, content_type: str = "video/mp4") -> dict[str, Any]:
    return {"role": role, "sha256": SHA, "size": 1, "content_type": content_type}


def _review(gate: str, files: list[dict[str, Any]]) -> SubmittedReview:
    return SubmittedReview.model_validate(
        {"gate": gate, "content_sha256": SHA, "summary": "上傳包", "files": files}
    )


def _package(extra: int = 0) -> list[dict[str, Any]]:
    """A full package: metadata, cut, thumbnail and 45 language files, 48 in all."""
    files = [
        _file("metadata", "application/json"),
        _file("final"),
        _file("thumbnail", "image/png"),
    ]
    files += [_file(f"captions_x{index}", "application/x-subrip") for index in range(45 + extra)]
    return files


def test_a_package_carries_its_clips_beside_its_own_48_files() -> None:
    clips = [_file(f"clip_s{index:02d}-t1") for index in range(1, MAX_CLIP_FILES + 1)]
    review = _review("publish", [*_package(), *clips])
    assert len(review.files) == MAX_REVIEW_FILES + MAX_CLIP_FILES


def test_clips_never_make_room_for_more_package_files() -> None:
    with pytest.raises(ValidationError, match="at most 48 files besides clips"):
        _review("publish", [*_package(extra=1), _file("clip_s01-t1")])


def test_too_many_clips_or_a_clip_that_is_not_an_mp4_is_refused() -> None:
    clips = [_file(f"clip_s{index:03d}") for index in range(MAX_CLIP_FILES + 1)]
    with pytest.raises(ValidationError, match="at most 120 clips"):
        _review("publish", clips)
    with pytest.raises(ValidationError, match="is an mp4"):
        _review("publish", [_file("clip_s01-t1", "image/png")])


@pytest.mark.parametrize("gate", ["final", "languages", "storyboard"])
def test_only_the_publish_gate_takes_clips(gate: str) -> None:
    with pytest.raises(ValidationError, match="only an upload package"):
        _review(gate, [_file("preview"), _file("clip_s01-t1")])


@pytest.mark.asyncio
async def test_the_tool_route_takes_a_package_with_its_clips_and_refuses_them_elsewhere(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answer = ReviewOut(
        id=uuid4(),
        gate="publish",
        content_sha256=SHA,
        summary="上傳包",
        payload={},
        files=[],
        status="pending",
        choice=None,
        note=None,
        decided_at=None,
        created_at=datetime.now(UTC),
    )
    submitted = AsyncMock(return_value=answer)
    monkeypatch.setattr(admin_service, "submit_review", submitted)
    monkeypatch.setattr(admin_api, "_store", AsyncMock(return_value=object()))
    app = FastAPI()
    app.include_router(admin_api.tool_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")
    app.dependency_overrides[speech_api.video_tool] = lambda: token
    clips = [_file(f"clip_s{index:02d}-t1") for index in range(1, 41)]
    body = {
        "gate": "publish",
        "content_sha256": SHA,
        "summary": "上傳包",
        "files": [*_package(), *clips],
    }
    route = "/api/v1/video/reviews/v/reviews"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        refused = await client.post(route, json={**body, "gate": "final"})
        taken = await client.post(route, json=body)
    assert refused.status_code == 422
    assert taken.status_code == 201
    assert submitted.await_count == 1 and submitted.await_args is not None
    payload = submitted.await_args.args[3]
    assert isinstance(payload, SubmittedReview) and len(payload.files) == 88
