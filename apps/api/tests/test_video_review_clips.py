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
from app.video_reviews.clips import (
    MAX_BACKUP_FILES,
    MAX_BUILD_FILES,
    MAX_CLIP_FILES,
    MAX_KEYFRAME_FILES,
    SubmittedReview,
)
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
    with pytest.raises(ValidationError, match="at most 48 files besides the backup tier's"):
        _review("publish", [*_package(extra=1), _file("clip_s01-t1")])


def test_too_many_clips_or_a_clip_that_is_not_an_mp4_is_refused() -> None:
    clips = [_file(f"clip_s{index:03d}") for index in range(MAX_CLIP_FILES + 1)]
    with pytest.raises(ValidationError, match="at most 120 clips"):
        _review("publish", clips)
    with pytest.raises(ValidationError, match="is an mp4"):
        _review("publish", [_file("clip_s01-t1", "image/png")])


def test_a_package_pushed_by_hand_carries_the_rest_of_the_full_tier_beside_its_48() -> None:
    """review-push from a cloud session (owner, 2026-11-03): keyframes, narration.wav,
    timeline.json and the line recordings ride with the package so the host holds them all."""
    keyframes = [_file(f"kf_ch1-{index:03d}", "image/jpeg") for index in range(MAX_KEYFRAME_FILES)]
    backup = [
        _file("keyframes_manifest", "application/json"),
        _file("full_narration", "audio/wav"),
        _file("full_timeline", "application/json"),
        _file("recordings_manifest", "application/json"),
        *[_file(f"recording_x{index}", "audio/wav") for index in range(MAX_BACKUP_FILES - 4)],
    ]
    review = _review("publish", [*_package(), *keyframes, *backup])
    assert len(review.files) == MAX_REVIEW_FILES + MAX_KEYFRAME_FILES + MAX_BACKUP_FILES
    with pytest.raises(ValidationError, match="at most 400 keyframes"):
        _review("publish", [*keyframes, _file("kf_extra", "image/png")])
    with pytest.raises(ValidationError, match="other backup-tier files"):
        _review("publish", [*backup, _file("recording_y", "audio/wav")])
    with pytest.raises(ValidationError, match="png or a jpeg"):
        _review("publish", [_file("kf_ch1-001", "video/mp4")])
    with pytest.raises(ValidationError, match="at most 48 files besides the backup tier's"):
        _review("publish", [*_package(extra=1), *keyframes[:1]])


def test_a_package_carries_an_imported_dramas_build_data_beside_its_48() -> None:
    """import --publish (owner, 2026-11-05): the cut and dub logs, the music cues and the edit
    table a re-cut needs ride with the package, counted apart from the 48 and the other backup
    tier."""
    build = [
        _file("build_log-final", "text/plain"),
        _file("build_edit-edit-dh-e049", "application/json"),
        _file("build_music-cue-comedy", "audio/mpeg"),
        _file("build_music-cue-rain", "audio/wav"),
        *[_file(f"build_log-dub-x{index}", "text/plain") for index in range(MAX_BUILD_FILES - 4)],
    ]
    review = _review("publish", [*_package(), *build])
    assert len(review.files) == MAX_REVIEW_FILES + MAX_BUILD_FILES
    with pytest.raises(ValidationError, match="at most 40 build files"):
        _review("publish", [*build, _file("build_log-extra", "text/plain")])
    with pytest.raises(ValidationError, match="a build_ file is"):
        _review("publish", [_file("build_music-cue-comedy", "video/mp4")])
    with pytest.raises(ValidationError, match="at most 48 files besides the backup tier's"):
        _review("publish", [*_package(extra=1), *build[:1]])


@pytest.mark.parametrize("gate", ["final", "languages", "storyboard"])
def test_only_the_publish_gate_takes_build_data(gate: str) -> None:
    with pytest.raises(ValidationError, match="only an upload package"):
        _review(gate, [_file("preview"), _file("build_log-final", "text/plain")])


@pytest.mark.parametrize("gate", ["final", "languages", "storyboard"])
def test_only_the_publish_gate_takes_keyframes(gate: str) -> None:
    with pytest.raises(ValidationError, match="only an upload package"):
        _review(gate, [_file("preview"), _file("kf_ch1-001", "image/png")])


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
