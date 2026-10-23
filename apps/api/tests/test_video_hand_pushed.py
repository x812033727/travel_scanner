"""A film pushed by hand waits for the owner at every gate (ticket
2026-10-11-hand-driven-film-approved-on-its; owner, 2026-10-17).

`claude-code-mods-delivery-check-tutorial` was pushed stage by stage by one agent session and
approved on arrival at its outline, audio and final gates on that session's own reviews.
`review-push` now marks a video the worker did not make `hand_pushed`, and the server applies
none of its automatic approvals to such a submission, whatever the checks say.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.models import VideoProject, VideoReview, VideoToolToken
from app.video_reviews import admin_service
from app.video_reviews.schemas import ReviewIn
from app.video_reviews.storage import ReviewStore

PICK = {
    "choice": "B",
    "probabilities": {"A": 0.26, "B": 0.74},
    "options": {"A": {"stance": 0.9, "demo": 0.4}, "B": {"stance": 0.81, "demo": 0.92}},
    "advice": 0.05,
}


def _site(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every automatic rule would approve: only the hand-pushed mark can hold a review back."""
    now = datetime.now(UTC)
    project = VideoProject(id=uuid4(), slug="v", title="t", stage="outline", checklist=[])
    decided = VideoReview(
        id=uuid4(),
        project_id=project.id,
        gate="audio",
        subject=None,
        status="approved",
        content_sha256="a" * 64,
        summary="旁白",
        payload={},
        files=[],
        created_at=now,
        decided_at=now,
    )
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=[decided]))
    monkeypatch.setattr(admin_service, "auto_picks_outline", AsyncMock(return_value=True))
    monkeypatch.setattr(admin_service, "auto_approves_audio", AsyncMock(return_value=True))
    monkeypatch.setattr(admin_service, "auto_approves_storyboard", AsyncMock(return_value=True))
    monkeypatch.setattr(admin_service, "auto_approves_final", AsyncMock(return_value=True))
    monkeypatch.setattr(admin_service, "compilation_slugs", AsyncMock(return_value=set()))


def _outline(**extra: object) -> ReviewIn:
    return ReviewIn(
        gate="outline",
        content_sha256="c" * 64,
        summary="大綱",
        payload={"options": [{"key": "A"}, {"key": "B"}], "pick": PICK, **extra},
    )


async def _submit(tmp_path: Path, review: ReviewIn) -> tuple[str, str | None]:
    store = ReviewStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    session = AsyncMock()
    session.add = MagicMock()
    token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")
    out = await admin_service.submit_review(session, store, "v", review, token)
    return out.status, out.note


@pytest.mark.asyncio
async def test_a_hand_pushed_outline_waits_for_the_owner_even_when_jev_s_pick_passes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _site(monkeypatch)
    assert await _submit(tmp_path, _outline(hand_pushed=True)) == ("pending", None)


@pytest.mark.asyncio
async def test_the_worker_s_own_outline_is_still_approved_on_arrival(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _site(monkeypatch)
    status, note = await _submit(tmp_path, _outline())
    assert status == "approved"
    assert note is not None and "依設定自動核准" in note


@pytest.mark.asyncio
@pytest.mark.parametrize("mark", [False, "true", 1, None])
async def test_only_a_true_mark_holds_a_review(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, mark: object
) -> None:
    _site(monkeypatch)
    status, _ = await _submit(tmp_path, _outline(hand_pushed=mark))
    assert status == "approved", mark


@pytest.mark.asyncio
async def test_a_hand_pushed_narration_waits_for_the_owner_even_when_its_check_passes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _site(monkeypatch)
    audio = ReviewIn(
        gate="audio",
        content_sha256="d" * 64,
        summary="旁白",
        payload={"check": {"ok": True}, "hand_pushed": True},
    )
    assert await _submit(tmp_path, audio) == ("pending", None)
