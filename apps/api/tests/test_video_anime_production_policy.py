"""The explicit native profile preserves authored long anime without changing drama gates."""

from __future__ import annotations

import copy
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
import sqlalchemy as sa
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import SessionFactory
from app.db import engine as postgres_engine
from app.models import User, VideoToolToken
from app.video_automation import judge
from app.video_automation import series as service
from app.video_automation import settings as settings_service
from app.video_automation.anime_policy import (
    ANIME_REQUIRED_VERDICTS,
    LONG_ANIME_POLICY,
    AnimeRuntimeSpec,
    anime_chapter_problem,
    anime_episode_problem,
    is_closed_anime_finale,
)
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaSeries,
)
from app.video_automation.schemas import (
    SeriesDocSubmitIn,
    SeriesEpisodeEditIn,
    SeriesIn,
    SeriesPatch,
)

WHEN = datetime(2026, 10, 2, tzinfo=UTC)
SOURCE = Path(__file__).resolve().parents[3] / "docs/videos/series-plans/borrowed-dawn"
RUNTIME = {
    "body_target_seconds": 1320,
    "op_ed_budget_seconds": 180,
    "broadcast_slot_seconds": 1800,
    "slot_reserve_seconds": 300,
}


def request(**changes: Any) -> dict[str, Any]:
    return {
        "slug": "borrowed-dawn-production",
        "title": "借來的黎明",
        "premise": "原創異世界群像",
        "kind": "series",
        "category": "anime",
        "style_preset": "anime-2d",
        "genre": "custom",
        "lead": "ensemble",
        "tone": "no-romance",
        "target_minutes": 22,
        "planned_episodes": 120,
        "episodes_per_chapter": 12,
        "open_ended": False,
        "hands_off": False,
        "compilation": False,
        "production_policy": LONG_ANIME_POLICY,
        "runtime_spec": copy.deepcopy(RUNTIME),
        **changes,
    }


def row(**changes: Any) -> VideoDramaSeries:
    return VideoDramaSeries(
        **request(),
        id=uuid4(),
        aspects=["world", "structure"],
        status="paused",
        planning_only=False,
        force_next=False,
        created_at=WHEN,
        updated_at=WHEN,
        **changes,
    )


def source_episodes() -> list[dict[str, Any]]:
    return [
        episode
        for season in range(1, 11)
        for episode in json.loads((SOURCE / f"season-{season:02}.json").read_text())["episodes"]
    ]


def cached_rows(series: VideoDramaSeries) -> list[VideoDramaEpisode]:
    return [
        VideoDramaEpisode(
            id=uuid4(),
            series_id=series.id,
            number=episode["number"],
            chapter_number=service.chapter_of(series, episode["number"]),
            title=episode["title"],
            logline=episode["logline"],
            status="ready",
            beats={key: value for key, value in copy.deepcopy(episode).items() if key != "number"},
        )
        for episode in source_episodes()
    ]


def approved_source_docs() -> list[VideoDramaDoc]:
    episodes = source_episodes()
    return [
        doc("setting", json.loads((SOURCE / "setting.json").read_text())),
        doc("outline", json.loads((SOURCE / "outline.json").read_text())),
        *[
            doc("chapter", {"episodes": episodes[index * 12 : (index + 1) * 12]}, chapter=index + 1)
            for index in range(10)
        ],
    ]


def doc(
    kind: str, body: dict[str, Any] | None = None, *, status: str = "approved", chapter: int = 0
) -> VideoDramaDoc:
    return VideoDramaDoc(
        id=uuid4(),
        kind=kind,
        version=1,
        chapter_number=chapter,
        body_json=body or {},
        body_md="# draft",
        status=status,
        created_at=WHEN,
    )


def test_runtime_and_native_request_preserve_22_body_30_slot_and_ensemble() -> None:
    payload = SeriesIn.model_validate(request())
    assert payload.target_minutes == 22 and payload.lead == "ensemble"
    assert payload.runtime_spec and payload.runtime_spec.model_dump() == RUNTIME
    summary = service.summary_view(row(), [], [])
    assert summary.production_policy == LONG_ANIME_POLICY
    assert summary.runtime_spec == RUNTIME and summary.category == "anime"
    assert summary.status == "paused" and summary.chapters == 10


@pytest.mark.parametrize(
    "changes",
    [
        {"production_policy": None},
        {"production_policy": "fake"},
        {"runtime_spec": None},
        {"category": None},
        {"kind": "one-off"},
        {"kind": "story"},
        {"genre": "xianxia-bonds"},
        {"style_preset": "cinematic-3d"},
        {"lead": "male"},
        {"hands_off": True},
        {"compilation": True},
        {"total_minutes": 120},
        {"target_minutes": 21},
        {"slug": None},
        {"title": None},
        {"premise": None},
        {"planning_only": False},
        {"planning_spec": {}},
        {"status": "active"},
    ],
)
def test_new_contract_cannot_be_enabled_partially(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        SeriesIn.model_validate(request(**changes))


@pytest.mark.parametrize(
    "changes",
    [
        {"body_target_seconds": 480},
        {"body_target_seconds": 1860},
        {"body_target_seconds": 1321},
        {"body_target_seconds": "1320"},
        {"body_target_seconds": 1320.0},
        {"body_target_seconds": True},
        {"op_ed_budget_seconds": -1},
        {"op_ed_budget_seconds": 301},
        {"slot_reserve_seconds": 901},
        {"broadcast_slot_seconds": 1799},
        {"broadcast_slot_seconds": 3601},
        {"invented_budget": 10},
    ],
)
def test_runtime_seconds_are_strict_and_budgeted(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        AnimeRuntimeSpec.model_validate({**RUNTIME, **changes})


@pytest.mark.parametrize("minutes", [9, 20, 22, 30])
def test_ordinary_drama_still_stops_at_eight(minutes: int) -> None:
    assert SeriesIn(premise="普通漫劇", target_minutes=8).target_minutes == 8
    with pytest.raises(ValidationError):
        SeriesIn(premise="普通漫劇", target_minutes=minutes)


def test_explainer_and_story_caps_are_not_widened() -> None:
    assert (
        SeriesIn(
            kind="one-off", premise="為何", style_preset="flat-explainer", target_minutes=20
        ).target_minutes
        == 20
    )
    with pytest.raises(ValidationError):
        SeriesIn(kind="one-off", premise="為何", style_preset="flat-explainer", target_minutes=21)
    with pytest.raises(ValidationError):
        SeriesIn.model_validate({"kind": "story", "target_minutes": 21, "premise": "故事"})


def test_all_120_authored_beats_validate_without_fake_retention_fields() -> None:
    episodes = source_episodes()
    assert len(episodes) == 120
    assert anime_chapter_problem(row(), episodes) is None
    assert episodes[-1]["tension"][-1] == 2
    assert is_closed_anime_finale(row(), episodes[-1])
    assert not service.retention_required(row())
    assert all("hook_type" not in episode and "satisfaction" not in episode for episode in episodes)
    for chapter in range(10):
        payload = SeriesDocSubmitIn(
            kind="chapter",
            chapter_number=chapter + 1,
            body_md="# source draft",
            body_json={"episodes": episodes[chapter * 12 : (chapter + 1) * 12]},
        )
        assert service.doc_problem(row(), payload) is None


@pytest.mark.parametrize(
    "mutation",
    [
        "early-closure",
        "low-end",
        "six-score",
        "float-score",
        "one-event",
        "no-stakes",
        "same-events",
        "bad-state",
        "missing-consequence",
        "missing-payoffs",
        "empty-cast",
    ],
)
def test_narrative_mutations_are_rejected(mutation: str) -> None:
    episode = copy.deepcopy(source_episodes()[0])
    if mutation == "early-closure":
        episode["closed_ending"] = True
    elif mutation == "low-end":
        episode["tension"][-1] = 2
    elif mutation == "six-score":
        episode["tension"][0] = 6
    elif mutation == "float-score":
        episode["tension"][0] = 4.0
    elif mutation == "one-event":
        episode["high_tension"].pop()
    elif mutation == "no-stakes":
        episode["high_tension"][0]["stakes"] = " "
    elif mutation == "same-events":
        episode["high_tension"][1]["event"] = episode["high_tension"][0]["event"]
    elif mutation == "bad-state":
        del episode["state"]["evidence"]
    elif mutation == "missing-consequence":
        del episode["consequence"]
    elif mutation == "missing-payoffs":
        del episode["general_payoffs"]
    else:
        episode["characters"] = []
    assert anime_episode_problem(row(), episode)


def test_quiet_ending_requires_exact_closed_series_finale() -> None:
    finale = copy.deepcopy(source_episodes()[-1])
    assert anime_episode_problem(row(), finale) is None
    for changes in ({"open_ended": True}, {"planned_episodes": 121}):
        series = row()
        for key, value in changes.items():
            setattr(series, key, value)
        assert not is_closed_anime_finale(series, finale)
        assert anime_episode_problem(series, finale)
    finale["closed_ending"] = False
    assert anime_episode_problem(row(), finale)


def test_four_episode_payoffs_include_previous_chapter_context() -> None:
    episodes = copy.deepcopy(source_episodes()[9:14])
    for episode in episodes:
        episode["payoffs"] = []
        episode["general_payoffs"] = []
    assert anime_chapter_problem(row(), episodes[3:]) is None
    assert "completed payoff" in str(anime_chapter_problem(row(), episodes[3:], episodes[:3]))
    episodes[-1]["general_payoffs"] = ["修復完成並留下接替能力"]
    episodes[0]["general_payoffs"] = ["前一場救援完成"]
    assert anime_chapter_problem(row(), episodes[3:], episodes[:3]) is None


def test_reverse_previous_chapter_cannot_hide_cross_chapter_debt() -> None:
    episodes = copy.deepcopy(source_episodes()[:24])
    for episode in episodes[9:15]:
        episode["payoffs"] = []
        episode["general_payoffs"] = []
    for previous in (episodes[:12], list(reversed(episodes[:12]))):
        assert "completed payoff" in str(anime_chapter_problem(row(), episodes[12:], previous))


def test_chapter_references_must_belong_to_reviewed_setting() -> None:
    payload = SeriesDocSubmitIn(
        kind="chapter",
        chapter_number=1,
        body_md="# source",
        body_json={"episodes": source_episodes()[:12]},
    )
    assert "unknown character" in str(service.doc_problem(row(), payload, [doc("setting")]))


@pytest.mark.asyncio
async def test_create_stays_paused_and_owner_start_planning_is_explicit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = MagicMock()
    session.scalar = AsyncMock(return_value=None)
    created = await service.add_series(
        session, User(id=uuid4()), SeriesIn.model_validate(request())
    )
    assert created.status == "paused" and not created.hands_off and not created.planning_only
    assert (
        service.next_job_for(created, [], [], VideoAutomationSettings(), started_this_month=0)
        is None
    )
    assert service.patch_problem(created, {"status": "active"}, []) is None
    session.commit = AsyncMock()
    monkeypatch.setattr(service, "_series", AsyncMock(return_value=created))
    monkeypatch.setattr(service, "_docs", AsyncMock(return_value=[]))
    monkeypatch.setattr(service, "_episodes", AsyncMock(return_value=[]))
    monkeypatch.setattr(service, "series_view", AsyncMock())
    await service.patch_series(
        session, User(id=uuid4()), created.slug, SeriesPatch(status="active")
    )
    assert created.status == "setting"
    job = service.next_job_for(created, [], [], VideoAutomationSettings(), started_this_month=0)
    assert job and job.kind == "setting"


@pytest.mark.asyncio
async def test_outline_approval_pauses_again_and_resume_waits_for_approved_cores(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    series = row()
    series.status = "outline"
    session = MagicMock()
    monkeypatch.setattr(service, "_episodes", AsyncMock(return_value=[]))
    outline = json.loads((SOURCE / "outline.json").read_text())
    await service._apply_approval(session, series, doc("outline", outline))  # noqa: SLF001
    assert series.status == "paused"
    refusal = service.patch_problem(series, {"status": "active"}, [doc("setting", status="review")])
    assert refusal and refusal.code == "video_series_not_planned"
    assert (
        service.patch_problem(series, {"status": "active"}, [doc("setting"), doc("outline")])
        is None
    )
    assert (
        service.next_job_for(
            series,
            [doc("setting"), doc("outline")],
            [],
            VideoAutomationSettings(),
            started_this_month=0,
        )
        is None
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"hands_off": True},
        {"compilation": True},
        {"target_minutes": 8},
        {"planned_episodes": 121},
        {"open_ended": True},
        {"style_preset": "cinematic-3d"},
        {"genre": "xianxia-bonds"},
    ],
)
def test_existing_patch_cannot_change_the_explicit_profile(changes: dict[str, Any]) -> None:
    refusal = service.patch_problem(row(), changes)
    assert refusal and refusal.code == "video_anime_contract_fixed"
    assert service.patch_problem(row(), {"title": "新名稱", "note": "待審"}) is None


@pytest.mark.parametrize(
    "changes",
    [
        {"production_policy": None},
        {"runtime_spec": RUNTIME},
        {"category": "anime"},
        {"planning_only": False},
        {"planning_spec": {}},
    ],
)
def test_patch_never_accepts_policy_or_unlock_flags(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        SeriesPatch.model_validate(changes)


def test_policy_aware_judge_checks_consequences_and_final_closure() -> None:
    coverage = {
        "hook": "有",
        "conflict": "有",
        "turn": "有",
        "closure": "有",
        "high_tension": ["有", "有"],
        "consequences": "有",
    }
    payload = {"coverage": coverage, "continuity_problems": [], "similar_works": []}
    assert judge.script_check_passed(
        payload, retention_required=True, production_policy=LONG_ANIME_POLICY, closed_finale=True
    )
    assert not judge.script_check_passed(
        payload, retention_required=False, production_policy=LONG_ANIME_POLICY
    )
    assert not judge.script_check_passed(payload, retention_required=True)
    coverage["closure"] = "弱"
    assert not judge.script_check_passed(
        payload, retention_required=False, production_policy=LONG_ANIME_POLICY, closed_finale=True
    )


def test_native_doc_verdicts_need_payoff_schedule_and_real_high_tension() -> None:
    for kind, required in ANIME_REQUIRED_VERDICTS.items():
        payload: dict[str, Any] = {
            "verdicts": dict.fromkeys(required, "有"),
            "problems": [],
            "similar_works": [],
        }
        assert judge.series_doc_passed(payload, kind, production_policy=LONG_ANIME_POLICY)
        payload["verdicts"].pop(required[-1])
        assert not judge.series_doc_passed(payload, kind, production_policy=LONG_ANIME_POLICY)


@pytest.mark.asyncio
async def test_profile_always_keeps_owner_document_and_script_review() -> None:
    series = row()
    series.hands_off = True  # Corrupt in-memory flags must not enable an auto-approval shortcut.
    session = MagicMock()
    session.scalar = AsyncMock(return_value=series)
    assert await settings_service.hands_off_series(session, series.slug) is None
    judge_payload = {
        "verdicts": dict.fromkeys(ANIME_REQUIRED_VERDICTS["setting"], "有"),
        "problems": [],
        "similar_works": [],
    }
    payload = SeriesDocSubmitIn(kind="setting", body_md="# authored", judge=judge_payload)
    assert service.auto_doc_status(series, payload, 1, 0) == ("review", None)


@pytest.mark.asyncio
async def test_profile_ignores_global_media_auto_approval_switches() -> None:
    settings = VideoAutomationSettings(auto_approve_storyboard=True, auto_pick_look=True)
    session = MagicMock()
    session.scalar = AsyncMock(side_effect=[settings, row()])
    assert not await settings_service.auto_approves_storyboard(session, {}, row().slug)
    session.scalar = AsyncMock(side_effect=[settings, row()])
    assert not await settings_service.auto_picks_look(session, {}, row().slug)


@pytest.mark.parametrize(
    "mutation",
    [
        "early-closure",
        "missing-events",
        "missing-state",
        "missing-consequence",
        "fake-number",
        "missing-payoff-window",
    ],
)
@pytest.mark.asyncio
async def test_native_episode_edit_revalidates_full_cached_chapter_before_mutation(
    mutation: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    series = row()
    episodes = cached_rows(series)
    target = episodes[118]
    beats = copy.deepcopy(target.beats)
    if mutation == "early-closure":
        beats["closed_ending"] = True
    elif mutation == "missing-events":
        beats.pop("high_tension")
    elif mutation == "missing-state":
        beats.pop("state")
    elif mutation == "missing-consequence":
        beats.pop("consequence")
    elif mutation == "fake-number":
        beats["number"] = 120
    else:
        for episode in episodes[115:118]:
            episode.beats["payoffs"] = []
            episode.beats["general_payoffs"] = []
        beats["payoffs"] = []
        beats["general_payoffs"] = []
    before = copy.deepcopy(target.beats)
    session = MagicMock(commit=AsyncMock())
    monkeypatch.setattr(service, "_series", AsyncMock(return_value=series))
    monkeypatch.setattr(service, "_episode", AsyncMock(return_value=target))
    monkeypatch.setattr(service, "_episodes", AsyncMock(return_value=episodes))
    monkeypatch.setattr(service, "_docs", AsyncMock(return_value=approved_source_docs()))
    with pytest.raises(service.SeriesRefused) as refusal:
        await service.edit_episode(
            session, User(id=uuid4()), series.slug, 119, SeriesEpisodeEditIn(beats=beats)
        )
    assert refusal.value.code == "video_anime_episode_invalid"
    assert target.beats == before
    session.add.assert_not_called()
    session.commit.assert_not_awaited()


def test_cached_chapter_checks_both_boundaries_and_allows_valid_owner_edit() -> None:
    series = row()
    episodes = cached_rows(series)
    assert (
        service.anime_cached_chapter_problem(
            series, episodes, 12, approved_source_docs(), {"title": "新標題"}
        )
        is None
    )
    for episode in episodes[9:14]:
        episode.beats["payoffs"] = []
        episode.beats["general_payoffs"] = []
    # The first crossing window E10..E13 includes an already populated next chapter.
    assert "completed payoff" in str(
        service.anime_cached_chapter_problem(
            series, list(reversed(episodes)), 12, approved_source_docs()
        )
    )


@pytest.mark.parametrize("source_bad", [False, True])
@pytest.mark.asyncio
async def test_native_start_refuses_bad_cached_or_approved_source_beats_before_queueing(
    source_bad: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    series = row()
    series.status = "active"
    episodes = cached_rows(series)
    docs = approved_source_docs()
    if source_bad:
        docs[-1].body_json["episodes"][10]["closed_ending"] = True
    else:
        episodes[118].beats.pop("consequence")
    session = MagicMock(commit=AsyncMock(), scalar=AsyncMock())
    monkeypatch.setattr(service, "_series", AsyncMock(return_value=series))
    monkeypatch.setattr(service, "_episode", AsyncMock(return_value=episodes[118]))
    monkeypatch.setattr(service, "_episodes", AsyncMock(return_value=episodes))
    monkeypatch.setattr(service, "_docs", AsyncMock(return_value=docs))
    with pytest.raises(service.SeriesRefused) as refusal:
        await service.start_episode(
            session, VideoToolToken(id=uuid4()), series.slug, 119, "bad-119"
        )
    assert refusal.value.code == "video_anime_episode_invalid"
    session.scalar.assert_not_awaited()
    session.add.assert_not_called()
    session.commit.assert_not_awaited()


@pytest.mark.parametrize(
    "changes",
    [
        {"production_policy": None},
        {"runtime_spec": None},
        {"category": None},
        {"hands_off": True},
        {"compilation": True},
        {"target_minutes": 21},
        {"lead": "male"},
        {"planning_only": True},
    ],
)
def test_model_checks_reject_raw_sql_profile_bypasses(changes: dict[str, Any]) -> None:
    engine = sa.create_engine("sqlite://")
    try:
        cast(sa.Table, VideoDramaSeries.__table__).create(engine)
        with Session(engine) as session:
            series = row()
            session.add(series)
            session.commit()
            assignments = ", ".join(f"{key}=:{key}" for key in changes)
            with pytest.raises(IntegrityError):
                session.execute(sa.text(f"UPDATE video_drama_series SET {assignments}"), changes)
            session.rollback()
            assert session.get(VideoDramaSeries, series.id).target_minutes == 22
    finally:
        engine.dispose()


@pytest.mark.skipif(os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL")
@pytest.mark.asyncio(loop_scope="module")
async def test_native_create_and_source_draft_round_trip_remain_paused() -> None:
    await postgres_engine.dispose(close=False)
    slug = f"anime-it-{uuid4().hex[:12]}"
    owner_id = uuid4()
    try:
        async with SessionFactory() as session:
            owner = User(id=owner_id, email=f"{slug}@example.com", password_hash="unused")
            session.add(owner)
            await session.commit()
            created = await service.create_series(
                session, owner, SeriesIn.model_validate(request(slug=slug))
            )
            assert created.status == "paused" and created.runtime_spec == RUNTIME
            assert not created.docs and not created.episodes
            submitted = await service.submit_doc(
                session,
                slug,
                SeriesDocSubmitIn(
                    kind="chapter",
                    chapter_number=1,
                    body_md="# preserved source draft",
                    body_json={"episodes": source_episodes()[:12]},
                ),
            )
            assert submitted.status == "review"
            reread = await service.series_view(session, slug)
            assert reread.status == "paused" and len(reread.docs) == 1
            assert not reread.episodes
            assert reread.lead == "ensemble" and reread.target_minutes == 22
            assert reread.runtime_spec == RUNTIME and reread.category == "anime"
            with pytest.raises(service.SeriesRefused, match="設定集與總綱"):
                await service.patch_series(session, owner, slug, SeriesPatch(status="active"))
    finally:
        async with SessionFactory() as session:
            await session.execute(sa.delete(VideoDramaSeries).where(VideoDramaSeries.slug == slug))
            await session.execute(sa.delete(User).where(User.id == owner_id))
            await session.commit()
        await postgres_engine.dispose()
