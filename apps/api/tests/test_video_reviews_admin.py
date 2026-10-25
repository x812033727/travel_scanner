"""/admin/videos: a hands-off series' character sheets are picked even when the judge suggested
none (ticket 2026-10-25-judge-7-judge)."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.models import AdminAuditLog, VideoProject, VideoToolToken
from app.video_automation.models import VideoAutomationSettings, VideoDramaSeries
from app.video_reviews import admin_service
from app.video_reviews.schemas import ReviewIn
from app.video_reviews.storage import ReviewStore

SERIES = "bug-20261022-ab12"


def _series(**fields: Any) -> VideoDramaSeries:
    return VideoDramaSeries(
        id=uuid4(),
        slug=SERIES,
        kind="series",
        genre="custom",
        lead="ensemble",
        planned_episodes=50,
        open_ended=False,
        category="drama",
        style_preset="sticker",
        visual_tier="manga",
        **fields,
    )


def _session(settings: Any, series: VideoDramaSeries | None) -> AsyncMock:
    """A session that answers the two lookups the look rule makes and nothing else."""

    async def scalar(statement: Any) -> Any:
        entity = statement.column_descriptions[0]["entity"]
        if entity is VideoAutomationSettings:
            return settings
        if entity is VideoDramaSeries:
            return series
        return None

    session = AsyncMock()
    session.scalar = AsyncMock(side_effect=scalar)
    session.add = MagicMock()
    return session


# What the worker sent for 千凜 on 2026-10-25: six sheets, none passed the judge, so no
# suggestion. B and C carry the faults the keyframes would inherit; F was never scored.
SHEETS: dict[str, Any] = {
    "subject": "qianlin",
    "character": {"name": "千凜"},
    "options": [
        {
            "key": "A",
            "judge": {"overall": 6.1, "problems": ["appearance: 背景畫成落石鎮 → plain grey"]},
        },
        {"key": "B", "judge": {"overall": 6.29, "problems": ["no_text: 右下角有小字 → no text"]}},
        {"key": "C", "judge": {"overall": 5.8, "problems": ["clean: 左手六指 → correct hands"]}},
        {"key": "D", "judge": {"overall": 5.9, "problems": []}},
        {"key": "E", "judge": {"overall": 4.5, "problems": ["style: 太寫實 → sticker style"]}},
        {"key": "F"},
    ],
    "suggested": None,
}
FALLBACK_NOTE = (
    "judge 沒有推薦達到門檻 7 的設定圖；備援選法選 A：6.1/10，是沒有 no_text、clean 問題的候選裡"
    "最高分（備援門檻 5）。略過：B（no_text: 右下角有小字）、C（clean: 左手六指）、F（沒有分數）"
)


async def _submit_look(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    session: AsyncMock,
    payload: dict[str, Any],
) -> Any:
    project = VideoProject(
        id=uuid4(),
        slug=f"{SERIES}-e005",
        title="第 5 集",
        stage="look",
        checklist=[],
        format="drama",
        series_slug=SERIES,
        episode_number=5,
    )
    monkeypatch.setattr(admin_service, "_project", AsyncMock(return_value=project))
    monkeypatch.setattr(admin_service, "_reviews", AsyncMock(return_value=[]))
    monkeypatch.setattr(admin_service, "compilation_slugs", AsyncMock(return_value=set()))
    store = ReviewStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    token = VideoToolToken(id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x")
    review = ReviewIn(
        gate="look",
        subject="qianlin",
        content_sha256="d" * 64,
        summary="千凜 的設定圖 6 張，judge 沒有推薦",
        payload=payload,
    )
    return await admin_service.submit_review(session, store, project.slug, review, token)


@pytest.mark.asyncio
async def test_a_hands_off_series_gets_the_best_clean_sheet_when_the_judge_suggested_none(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    settings = SimpleNamespace(auto_pick_look=False, judge_min_score=7)
    session = _session(settings, _series(hands_off=True))
    out = await _submit_look(monkeypatch, tmp_path, session, SHEETS)
    assert (out.status, out.choice) == ("approved", "A"), "B scored higher but carries text"
    assert out.note == FALLBACK_NOTE
    assert session.add.call_args.args[0].action == "video_review_auto_approved"

    # The switch alone, on a series that is not hands-off, picks the same way.
    session = _session(SimpleNamespace(auto_pick_look=True, judge_min_score=7), _series())
    again = await _submit_look(monkeypatch, tmp_path, session, SHEETS)
    assert (again.status, again.choice, again.note) == ("approved", "A", FALLBACK_NOTE)


@pytest.mark.asyncio
async def test_the_judge_s_own_suggestion_still_comes_first(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    session = _session(
        SimpleNamespace(auto_pick_look=False, judge_min_score=7), _series(hands_off=True)
    )
    passed = {
        **SHEETS,
        "options": [*SHEETS["options"], {"key": "G", "judge": {"overall": 7.5, "problems": []}}],
        "suggested": "G",
    }
    out = await _submit_look(monkeypatch, tmp_path, session, passed)
    assert (out.status, out.choice) == ("approved", "G")
    assert out.note == "judge 給 G 7.5/10、沒有列出問題，依設定自動選"


@pytest.mark.asyncio
async def test_a_sheet_waits_for_the_owner_when_every_candidate_carries_text(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    session = _session(
        SimpleNamespace(auto_pick_look=False, judge_min_score=7), _series(hands_off=True)
    )
    all_text = {
        **SHEETS,
        "options": [
            {
                "key": key,
                "judge": {"overall": 6.2, "problems": [f"no_text: {key} 角落有字 → no text"]},
            }
            for key in "ABC"
        ],
    }
    out = await _submit_look(monkeypatch, tmp_path, session, all_text)
    assert (out.status, out.choice, out.note) == ("pending", None, None)
    assert not any(
        isinstance(call.args[0], AdminAuditLog) for call in session.add.call_args_list
    ), "nothing was decided, so nothing is logged"


@pytest.mark.asyncio
async def test_a_sheet_waits_for_the_owner_when_the_best_clean_one_is_too_far_under_the_bar(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    session = _session(
        SimpleNamespace(auto_pick_look=False, judge_min_score=7), _series(hands_off=True)
    )
    weak = {
        **SHEETS,
        "options": [
            {"key": "A", "judge": {"overall": 4.9, "problems": []}},
            {"key": "B", "judge": {"overall": 6.5, "problems": ["clean: 臉歪 → straight face"]}},
        ],
    }
    out = await _submit_look(monkeypatch, tmp_path, session, weak)
    assert (out.status, out.choice, out.note) == ("pending", None, None)
    # At exactly the floor it is picked.
    session = _session(
        SimpleNamespace(auto_pick_look=False, judge_min_score=7), _series(hands_off=True)
    )
    weak["options"][0]["judge"]["overall"] = 5
    out = await _submit_look(monkeypatch, tmp_path, session, weak)
    assert (out.status, out.choice) == ("approved", "A")


@pytest.mark.asyncio
async def test_the_fallback_never_picks_without_the_switch_or_a_hands_off_series(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    session = _session(SimpleNamespace(auto_pick_look=False, judge_min_score=7), _series())
    out = await _submit_look(monkeypatch, tmp_path, session, SHEETS)
    assert (out.status, out.choice, out.note) == ("pending", None, None)
    session = _session(None, _series(hands_off=True))
    out = await _submit_look(monkeypatch, tmp_path, session, SHEETS)
    assert out.status == "pending", "no settings row yet: off"


@pytest.mark.asyncio
async def test_the_fallback_never_picks_a_long_anime_s_sheet(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    long_anime = _series(production_policy="long-anime-v1", planning_only=False)
    session = _session(SimpleNamespace(auto_pick_look=True, judge_min_score=7), long_anime)
    out = await _submit_look(monkeypatch, tmp_path, session, SHEETS)
    assert (out.status, out.choice, out.note) == ("pending", None, None)
    hands_off_anime = _series(
        hands_off=True, production_policy="long-anime-v1", planning_only=False
    )
    session = _session(SimpleNamespace(auto_pick_look=False, judge_min_score=7), hands_off_anime)
    out = await _submit_look(monkeypatch, tmp_path, session, SHEETS)
    assert out.status == "pending"
