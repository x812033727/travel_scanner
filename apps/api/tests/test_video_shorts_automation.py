"""Shorts phase two on the server (docs/videos/SHORTS.md §排片與時段, ticket
video-shorts-automation-api): the topic library, the owner's material, the worker's next job,
the weekly plan and the weekly report. The rules first as pure functions, then through the
database; SQLite stands in for PostgreSQL, and the migration against the real one is in
test_migration_0117_video_shorts_topics.py, which CI runs."""

from __future__ import annotations

import hashlib
import json
from collections.abc import AsyncIterator
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import event, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.db import Base, get_session
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation.models import VideoAutomationSettings
from app.video_media.storage import MediaStore
from app.video_shorts import admin_automation_api, jobs, plan, reports, rules, slots, topics
from app.video_shorts.assets import AssetPart, upload_part
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import (
    VideoShortsAsset,
    VideoShortsCost,
    VideoShortsMetric,
    VideoShortsReport,
    VideoShortsSettings,
    VideoShortsSlot,
    VideoShortsTopic,
)
from app.video_shorts.schemas import (
    CampaignIn,
    DoneIn,
    PlanIn,
    ReportIn,
    SettingsWrite,
    TopicBrief,
    TopicIn,
    TopicPatch,
)
from app.video_speech import admin_api as speech_api

REPO = Path(__file__).resolve().parents[3]
CAMPAIGN = REPO / "docs" / "videos" / "ai-shorts" / "campaign" / "campaign.json"
TAIPEI = "Asia/Taipei"
# Monday 5 October 2026, 09:00 in Taipei; the run's first Short goes public the next day.
NOW = datetime(2026, 10, 5, 1, 0, tzinfo=UTC)
FIRST_DAY = date(2026, 10, 6)
SUBJECT = {"a": {"provider": "claude_code", "model": "claude-sonnet-5"}}
WHOLE = {
    "test_protocol": {
        "setup": "同一模型、兩種問法",
        "input": "湯 85 元 × 2",
        "condition_a": "直接問",
        "condition_b": "先驗算再答",
        "runs": "各一次、零重試",
        "scoring": "總額 275 元",
        "failure_path": "照實保留",
    },
    "truth_check": ["85 × 2 + 45 × 3 − 30 = 275"],
    "acceptance": ["原始兩組回答有留存"],
}
PNG = b"\x89PNG\r\n\x1a\n" + b"\0" * 200


# --- what a topic needs -------------------------------------------------------------------------


def _settle(status: str = "idea", line: str = "lab", **fields: Any) -> tuple[str, list[str]]:
    values: dict[str, Any] = {
        "brief": WHOLE,
        "source_slug": None,
        "assets_needed": [],
        "assets": [],
    }
    values.update(fields)
    return topics.settle(status, line=line, **values)


def test_an_experiment_is_ready_only_with_its_seven_fields_truth_and_acceptance() -> None:
    assert _settle() == ("ready", [])
    gaps = {**WHOLE, "test_protocol": {**WHOLE["test_protocol"], "scoring": " "}}
    status, why = _settle(brief=gaps)
    assert status == "idea" and why == ["測試規格缺 scoring"]
    status, why = _settle(brief={"test_protocol": WHOLE["test_protocol"]})
    assert status == "idea" and why == ["缺真值核對", "缺完成條件"]
    assert _settle(brief={})[0] == "idea"
    assert _settle(line="cut", brief={})[0] == "idea", "a highlight needs its source video"
    assert _settle(line="cut", brief={}, source_slug="ai-model-choice") == ("ready", [])


def test_material_and_missing_tools_hold_a_complete_topic_back() -> None:
    needed = [{"key": "photos", "label": "三張景點照片", "count": 3}]
    status, why = _settle(assets_needed=needed, assets=[topics.AssetFacts("photos")])
    assert status == "needs_assets" and why == ["缺素材：三張景點照片（還差 2 個）"]
    full = [topics.AssetFacts("photos")] * 3
    assert _settle(assets_needed=needed, assets=full) == ("ready", [])
    status, why = _settle(
        brief={**WHOLE, "requires": ["vision"]}, assets_needed=needed, assets=full
    )
    assert status == "needs_assets" and "視覺模型" in why[0], "the photos alone are not enough"
    assert _settle(brief={**WHOLE, "requires": ["image_generation"]}) == ("ready", [])
    assert topics.is_paid("lab", {"requires": ["image_generation"]})
    assert topics.is_paid("drama", {}) and not topics.is_paid("lab", WHOLE)


def test_a_topic_the_worker_took_or_that_was_given_up_keeps_its_status() -> None:
    for status in ("making", "made", "dropped"):
        assert _settle(status, brief={})[0] == status


def test_a_derived_slug_stays_inside_eighty_characters_and_starts_with_a_letter() -> None:
    assert topics.derived_slug("ai-model-choice", "cut-1") == "ai-model-choice-cut-1"
    assert topics.derived_slug("2026-recap", "cut-1") == "s-2026-recap-cut-1"
    long = topics.derived_slug("a" * 80, "cut-2")
    assert len(long) <= 80 and long.endswith("-cut-2")
    assert long != topics.derived_slug("a" * 79 + "b", "cut-2")


# --- the next job, as a rule --------------------------------------------------------------------


def _slot(day: int, topic: str | None = None, status: str = "planned") -> rules.SlotFacts:
    return rules.SlotFacts(
        id=UUID(int=day),
        starts_at=datetime(2026, 10, 5, 11, 30, tzinfo=UTC) + timedelta(days=day),
        status=status,
        topic_slug=topic,
    )


def _facts(**changes: Any) -> jobs.JobFacts:
    values: dict[str, Any] = {
        "now": NOW,
        "timezone": TAIPEI,
        "enabled": True,
        "paused": False,
        "lines": ("lab", "cut", "drama"),
        "weekly_quota": {"lab": 5, "cut": 2, "drama": 0},
        "campaign_start": FIRST_DAY,
        "stock_days": 5,
        "cover": 10,
        "reported_weeks": frozenset(),
        "open_slots": 0,
        "last_plan_at": None,
        "last_brief_at": NOW - timedelta(hours=1),
        "pool": {"lab": 20},
        "owner_ideas": 0,
        "planned": [_slot(1, "receipt"), _slot(2, "poster")],
        "topics": {
            "receipt": jobs.TopicFacts("receipt", "lab", "ready"),
            "poster": jobs.TopicFacts("poster", "lab", "ready"),
        },
        "started_this_month": 0,
        "max_per_month": 60,
        "paid_allowed": True,
        "subject_chosen": True,
    }
    values.update(changes)
    return jobs.JobFacts(**values)


def test_nothing_is_given_while_shorts_are_off() -> None:
    decision = jobs.next_job_for(_facts(enabled=False, open_slots=5))
    assert decision.kind is None and decision.holds == ("Shorts 的自動製作關著",)


def test_last_week_s_report_comes_first_from_monday_on() -> None:
    monday = datetime(2026, 10, 12, 1, 0, tzinfo=UTC)
    decision = jobs.next_job_for(_facts(now=monday, open_slots=5, last_brief_at=None))
    assert (decision.kind, decision.report_week) == ("report", date(2026, 10, 5))
    wednesday = monday + timedelta(days=2)
    assert jobs.next_job_for(_facts(now=wednesday)).kind == "report", "a missed Monday"
    written = frozenset({date(2026, 10, 5)})
    assert jobs.next_job_for(_facts(now=monday, reported_weeks=written)).kind is None
    # The run began on Tuesday the 6th: the week before it has nothing to report.
    assert jobs.next_job_for(_facts()).kind == "make"
    assert jobs.next_job_for(_facts(now=monday, campaign_start=None)).kind is None


def test_a_plan_on_monday_or_when_the_library_runs_low() -> None:
    assert jobs.next_job_for(_facts(open_slots=6)).kind == "plan", "Monday"
    tuesday = NOW + timedelta(days=1)
    assert jobs.next_job_for(_facts(now=tuesday, open_slots=6)).kind == "make"
    assert jobs.next_job_for(_facts(now=tuesday, open_slots=6, cover=4)).kind == "plan"
    assert jobs.next_job_for(_facts(now=tuesday, open_slots=6, cover=None)).kind == "make"
    assert jobs.next_job_for(_facts(open_slots=0)).kind == "make", "nothing left to plan"
    just = _facts(open_slots=6, last_plan_at=NOW - timedelta(hours=2))
    assert jobs.next_job_for(just).kind == "make", "a plan that left slots open waits"
    later = _facts(open_slots=6, last_plan_at=NOW - jobs.PLAN_EVERY)
    assert jobs.next_job_for(later).kind == "plan"


def test_an_empty_pool_asks_for_topics_rather_than_a_plan() -> None:
    decision = jobs.next_job_for(_facts(open_slots=6, pool={}, last_brief_at=None))
    assert decision.kind == "brief" and decision.extra == {"have": 0, "want": 14}
    assert decision.holds == ("題庫沒有可以排的題目，先補題",)


def test_topics_are_asked_for_while_the_pool_is_short_of_two_weeks() -> None:
    assert jobs.next_job_for(_facts(pool={"lab": 13}, last_brief_at=None)).kind == "brief"
    assert jobs.next_job_for(_facts(pool={"lab": 14}, last_brief_at=None)).kind == "make"
    assert jobs.next_job_for(_facts(pool={"lab": 13})).kind == "make", "asked an hour ago"
    stale = NOW - jobs.BRIEF_EVERY
    assert jobs.next_job_for(_facts(pool={"lab": 13}, last_brief_at=stale)).kind == "brief"
    ideas = _facts(pool={"lab": 30}, owner_ideas=1, last_brief_at=None)
    assert jobs.next_job_for(ideas).kind == "brief", "the owner's idea is completed"
    narrow = _facts(lines=("lab",), weekly_quota={"lab": 3}, pool={"lab": 6, "cut": 9})
    assert jobs.next_job_for(replace(narrow, last_brief_at=None)).kind == "make"


def test_the_earliest_planned_slot_whose_topic_has_no_short_is_made() -> None:
    decision = jobs.next_job_for(_facts())
    assert (decision.kind, decision.slot_id, decision.topic_slug) == (
        "make",
        UUID(int=1),
        "receipt",
    )
    past = _facts(now=_slot(1).starts_at)
    assert jobs.next_job_for(past).topic_slug == "poster", "a slot whose time came is gone"
    made = _facts(topics={**_facts().topics, "receipt": jobs.TopicFacts("receipt", "lab", "made")})
    assert jobs.next_job_for(made).topic_slug == "poster"
    gone = jobs.TopicFacts("receipt", "lab", "making", project_dropped=True)
    assert jobs.next_job_for(_facts(topics={**_facts().topics, "receipt": gone})).topic_slug == (
        "poster"
    )
    resumed = jobs.TopicFacts("receipt", "lab", "making")
    again = jobs.next_job_for(_facts(topics={**_facts().topics, "receipt": resumed}))
    assert again.topic_slug == "receipt", "a worker that lost its place picks it up"
    off_line = _facts(lines=("cut",), weekly_quota={"cut": 2}, pool={"cut": 9})
    assert jobs.next_job_for(off_line).kind is None
    assert jobs.next_job_for(_facts(planned=[])).kind is None


def test_pause_the_month_s_cap_the_budget_and_the_subject_hold_back_making() -> None:
    paused = jobs.next_job_for(_facts(paused=True))
    assert paused.kind is None and paused.holds == ("Shorts 暫停中，不開始新的製作",)
    assert jobs.next_job_for(_facts(paused=True, open_slots=6)).kind == "plan", "planning goes on"
    full = jobs.next_job_for(_facts(started_this_month=60))
    assert full.kind is None and "每月上限 60 支" in full.holds[0]
    resumed = {**_facts().topics, "poster": jobs.TopicFacts("poster", "lab", "making")}
    assert jobs.next_job_for(_facts(started_this_month=60, topics=resumed)).topic_slug == (
        "poster"
    ), "a Short already started is finished"
    paid = {**_facts().topics, "receipt": jobs.TopicFacts("receipt", "lab", "ready", paid=True)}
    budget = _facts(topics=paid, paid_allowed=False, budget_reason="這 30 天已經花了 NT$3,000")
    decision = jobs.next_job_for(budget)
    assert decision.topic_slug == "poster", "free work goes on"
    assert decision.holds == ("「receipt」要花錢：這 30 天已經花了 NT$3,000",)
    unchosen = jobs.next_job_for(_facts(subject_chosen=False))
    assert unchosen.kind is None and "受測模型" in unchosen.holds[0]
    cut = {**_facts().topics, "poster": jobs.TopicFacts("poster", "cut", "ready")}
    assert jobs.next_job_for(_facts(subject_chosen=False, topics=cut)).topic_slug == "poster"


# --- the plan, as a rule ------------------------------------------------------------------------


def _plan(items: list[tuple[int, str]], **changes: Any) -> list[str]:
    slots_by_id = {UUID(int=day): _slot(day, status="open") for day in range(1, 15)}
    values: dict[str, Any] = {
        "slots": slots_by_id,
        "topics": {
            slug: plan.PlanTopic(slug, line, "ready", slug == "paid")
            for slug, line in [
                ("a", "lab"),
                ("b", "lab"),
                ("c", "cut"),
                ("d", "cut"),
                ("e", "cut"),
                ("paid", "lab"),
            ]
        },
        "planned_elsewhere": set(),
        "lines": ["lab", "cut", "drama"],
        "quota": {"lab": 2, "cut": 2, "drama": 0},
        "existing": {},
        "now": NOW,
        "timezone": TAIPEI,
        "window_end": datetime(2026, 10, 18, 16, 0, tzinfo=UTC),
        "paid_allowed": True,
    }
    values.update(changes)
    return plan.plan_problems([(UUID(int=day), slug) for day, slug in items], **values)


def test_a_plan_fills_open_slots_with_topics_that_can_be_made() -> None:
    assert _plan([(1, "a"), (2, "b"), (3, "c")]) == []
    assert _plan([]) == []
    assert _plan([(1, "a"), (1, "b")]) == [f"時段 {UUID(int=1)} 排了兩次"]
    assert _plan([(1, "a"), (2, "a")]) == ["題目 a 排了兩次"]
    assert _plan([(1, "zzz")]) == ["找不到題目 zzz"]
    taken = {UUID(int=1): replace(_slot(1, status="open"), topic_slug="x", status="planned")}
    assert "已經有題目或影片" in _plan([(1, "a")], slots=taken)[0]
    assert "不在這次排片的範圍" in _plan([(14, "a")])[0], "past the end of next week"
    assert "已經排在別的時段" in _plan([(1, "a")], planned_elsewhere={"a"})[0]
    idea = {"a": plan.PlanTopic("a", "lab", "idea", False)}
    assert _plan([(1, "a")], topics=idea) == ["題目 a 還不能做（idea）"]
    assert "內容線沒有開" in _plan([(1, "c")], lines=["lab"])[0]
    assert "要花錢" in _plan([(1, "paid")], paid_allowed=False)[0]


def test_a_week_holds_each_line_to_its_quota_and_lends_the_rest_to_experiments() -> None:
    # Tuesday 6 to Sunday 11 October is one week, Monday 12 the next.
    assert _plan([(1, "a"), (2, "b"), (3, "paid")]) == [], "lab takes the quota cut left"
    over = _plan([(1, "c"), (2, "d"), (3, "e")])
    assert over == ["2026-10-05 那一週長片精華排了 3 支，超過每週配額 2 支"]
    total = _plan([(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "paid")])
    assert total == ["2026-10-05 那一週排了 5 支，超過各內容線配額合計 4 支"]
    assert _plan([(1, "a"), (2, "b"), (7, "c"), (8, "d"), (9, "paid")]) == [], "two weeks"
    held = {(date(2026, 10, 5), "cut"): 2}
    assert "超過每週配額" in _plan([(1, "c")], existing=held)[0]


# --- through the database -----------------------------------------------------------------------

MODELS = (
    User,
    VideoProject,
    VideoReview,
    VideoToolToken,
    AdminAuditLog,
    VideoAutomationSettings,
    VideoShortsSettings,
    VideoShortsSlot,
    VideoShortsMetric,
    VideoShortsCost,
    VideoShortsTopic,
    VideoShortsAsset,
    VideoShortsReport,
)


@dataclass
class Site:
    factory: async_sessionmaker[AsyncSession]
    owner: User
    token: VideoToolToken
    store: MediaStore

    def session(self) -> AsyncSession:
        return self.factory()


@pytest.fixture
async def site(tmp_path: Path) -> AsyncIterator[Site]:
    engine = create_async_engine("sqlite+aiosqlite://")

    # SQLite drops timezone offsets; PostgreSQL hands back aware datetimes.
    def restore_utc(target: Any, _context: Any, *_more: Any) -> None:
        for column in target.__table__.columns:
            value = getattr(target, column.name)
            if isinstance(value, datetime) and value.tzinfo is None:
                setattr(target, column.name, value.replace(tzinfo=UTC))

    for model in MODELS:
        event.listen(model, "load", restore_utc)
        event.listen(model, "refresh", restore_utc)
    async with engine.begin() as db:
        await db.run_sync(
            lambda sync_db: Base.metadata.create_all(
                sync_db, tables=[model.__table__ for model in MODELS]
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    owner = User(id=uuid4(), email="owner@example.test", password_hash="unused", auth_version=1)
    token = VideoToolToken(id=uuid4(), name="tool", token_hash="h" * 64, token_prefix="mkv_test")
    async with factory() as session:
        session.add(User(id=owner.id, email=owner.email, password_hash="unused"))
        session.add(token)
        session.add(VideoAutomationSettings(id=1, channel_stance="只照實寫"))
        await session.commit()
    yield Site(
        factory,
        owner,
        token,
        MediaStore(tmp_path / "media", max_file_bytes=10**8, max_total_bytes=10**9),
    )
    for model in MODELS:
        event.remove(model, "load", restore_utc)
        event.remove(model, "refresh", restore_utc)
    await engine.dispose()


def campaign() -> CampaignIn:
    return CampaignIn.model_validate(json.loads(CAMPAIGN.read_text(encoding="utf-8")))


async def configure(site: Site, **fields: Any) -> None:
    async with site.session() as session:
        row = await session.get(VideoShortsSettings, 1)
        if row is None:
            row = VideoShortsSettings(id=1)
            session.add(row)
        values: dict[str, Any] = {"enabled": True, "subject_models": SUBJECT}
        values.update(fields)
        for name, value in values.items():
            setattr(row, name, value)
        await session.commit()


async def topic(site: Site, slug: str) -> VideoShortsTopic:
    async with site.session() as session:
        row = await session.scalar(select(VideoShortsTopic).where(VideoShortsTopic.slug == slug))
        assert row is not None
        return row


async def start_run(site: Site) -> None:
    async with site.session() as session:
        await slots.start_campaign(session, site.owner, FIRST_DAY, NOW)


async def next_job(site: Site, now: datetime = NOW) -> Any:
    async with site.session() as session:
        return await jobs.next_job(session, now)


@pytest.mark.asyncio
async def test_the_campaign_is_imported_once_with_what_each_topic_needs(site: Site) -> None:
    async with site.session() as session:
        first = await topics.import_campaign(session, site.owner, campaign(), NOW)
    assert (first.created, first.skipped) == (15, 0)
    by_slug = {item.slug: item.status for item in first.items}
    held = {slug for slug, status in by_slug.items() if status == "needs_assets"}
    assert held == {
        "shorts-taiwan-location",
        "shorts-boba-game",
        "shorts-photo-repair",
        "shorts-menu-glare",
        "shorts-sketch-website",
    }
    assert sum(1 for status in by_slug.values() if status == "ready") == 10
    async with site.session() as session:
        again = await topics.import_campaign(session, site.owner, campaign(), NOW)
        count = await session.scalar(select(func.count(VideoShortsTopic.id)))
    assert (again.created, again.skipped, count) == (0, 15, 15)
    receipt = await topic(site, "shorts-receipt-total")
    assert (receipt.origin, receipt.line, receipt.series, receipt.release_order) == (
        "campaign",
        "lab",
        "daily",
        1,
    )
    assert receipt.brief["test_protocol"]["scoring"].startswith("各組兩項")
    assert receipt.brief["truth_check"][0].startswith("85 × 2")
    assert receipt.brief["titles"] and receipt.brief["narration_outline"][0]["voice"]
    location = await topic(site, "shorts-taiwan-location")
    assert location.brief["requires"] == ["vision"]
    assert location.assets_needed[0]["count"] == 3
    async with site.session() as session:
        listed = await topics.list_topics(session)
    assert [item.slug for item in listed][:2] == ["shorts-receipt-total", "shorts-poster-blind"]
    paid = next(item for item in listed if item.slug == "shorts-image-specificity")
    assert paid.paid and paid.status == "ready"
    boba = next(item for item in listed if item.slug == "shorts-boba-game")
    assert boba.waiting_for == [topics.UNSUPPORTED["sandbox"]]


@pytest.mark.asyncio
async def test_the_owner_s_idea_waits_for_the_planner_to_complete_it(site: Site) -> None:
    await configure(site)
    async with site.session() as session:
        idea = await topics.add_idea(
            session, site.owner, TopicIn(title="AI 會不會看懂捷運路線圖？"), NOW
        )
    assert idea.status == "idea" and idea.origin == "owner" and idea.slug.startswith("idea-")
    assert "缺真值核對" in idea.waiting_for
    written = TopicIn(
        slug=idea.slug, title="AI 看懂捷運圖嗎", brief=TopicBrief.model_validate(WHOLE)
    )
    fresh = TopicIn(slug="shorts-new-angle", title="新角度")
    async with site.session() as session:
        out = await topics.write_planner_topics(session, [written, fresh], NOW)
    assert [(item.slug, item.result, item.status) for item in out.items] == [
        (idea.slug, "updated", "ready"),
        ("shorts-new-angle", "created", "idea"),
    ]
    assert (await topic(site, idea.slug)).origin == "owner"
    async with site.session() as session:
        again = await topics.write_planner_topics(session, [written], NOW)
        row = await session.get(VideoShortsSettings, 1)
    assert again.items[0].result == "exists", "a ready topic is not rewritten"
    assert row is not None and row.last_brief_at == NOW


@pytest.mark.asyncio
async def test_the_owner_edits_drops_and_takes_back_a_topic(site: Site) -> None:
    async with site.session() as session:
        await topics.import_campaign(session, site.owner, campaign(), NOW)
        moved = await topics.patch_topic(
            session, site.owner, "shorts-expert-role", TopicPatch(release_order=0), NOW
        )
    assert moved.release_order == 0
    async with site.session() as session:
        assert (await topics.list_topics(session))[0].slug == "shorts-expert-role"
        dropped = await topics.patch_topic(
            session, site.owner, "shorts-expert-role", TopicPatch(dropped=True), NOW
        )
        assert dropped.status == "dropped"
        with pytest.raises(ShortsRefused) as refused:
            await topics.patch_topic(
                session, site.owner, "shorts-expert-role", TopicPatch(title="x"), NOW
            )
        assert refused.value.code == "video_shorts_topic_dropped"
    async with site.session() as session:
        back = await topics.patch_topic(
            session, site.owner, "shorts-expert-role", TopicPatch(dropped=False), NOW
        )
        thin = await topics.patch_topic(
            session, site.owner, "shorts-self-check", TopicPatch(brief=TopicBrief()), NOW
        )
    assert back.status == "ready" and thin.status == "idea"
    await configure(site)
    async with site.session() as session:
        await jobs.start_topic(session, "shorts-expert-role", NOW)
        with pytest.raises(ShortsRefused) as taken:
            await topics.patch_topic(
                session, site.owner, "shorts-expert-role", TopicPatch(title="x"), NOW
            )
        assert taken.value.code == "video_shorts_topic_taken"
        given_up = await topics.patch_topic(
            session, site.owner, "shorts-expert-role", TopicPatch(dropped=True), NOW
        )
        assert given_up.status == "dropped", "a topic in the making can be given up"
        await topics.patch_topic(
            session, site.owner, "shorts-expert-role", TopicPatch(dropped=False), NOW
        )
        again = await jobs.start_topic(session, "shorts-expert-role", NOW)
    assert again.created and again.project_slug == "shorts-expert-role-2"


@pytest.mark.asyncio
async def test_the_owner_s_material_makes_a_topic_ready(site: Site) -> None:
    needs = [{"key": "photo", "label": "自己拍的菜單照片"}]
    async with site.session() as session:
        made = await topics.add_idea(
            session,
            site.owner,
            TopicIn.model_validate(
                {"slug": "menu-photo", "title": "菜單", "brief": WHOLE, "assets_needed": needs}
            ),
            NOW,
        )
    assert made.status == "needs_assets"
    sha = hashlib.sha256(PNG).hexdigest()

    def part(data: bytes = PNG, need: str = "photo", **changes: Any) -> AssetPart:
        values: dict[str, Any] = {
            "sha256": hashlib.sha256(data).hexdigest(),
            "part": 0,
            "parts": 1,
            "size": len(data),
            "data": data,
            "need": need,
            "filename": "menu.png",
            "author": "站主",
            "rights_note": "自己拍的，授權本站使用",
            "taken_on": date(2026, 10, 1),
        }
        values.update(changes)
        return AssetPart(**values)

    async with site.session() as session:
        with pytest.raises(ShortsRefused) as unknown:
            await upload_part(session, site.store, site.owner, "menu-photo", part(need="sketch"))
        assert unknown.value.code == "video_shorts_asset_need_unknown"
        with pytest.raises(ShortsRefused) as unsigned:
            await upload_part(session, site.store, site.owner, "menu-photo", part(author=" "))
        assert unsigned.value.code == "video_shorts_asset_rights_missing"
        text = b"not a picture at all"
        with pytest.raises(ShortsRefused) as wrong:
            await upload_part(session, site.store, site.owner, "menu-photo", part(text))
        assert wrong.value.code == "video_shorts_asset_type"
        assert site.store.path("menu-photo", hashlib.sha256(text).hexdigest()) is None
        out = await upload_part(session, site.store, site.owner, "menu-photo", part(), NOW)
    assert out.complete and out.asset is not None and out.topic is not None
    assert out.topic.status == "ready" and out.topic.waiting_for == []
    assert out.asset.download_path == f"video/media/files/menu-photo/{sha}"
    assert (out.asset.author, out.asset.content_type) == ("站主", "image/png")
    assert site.store.path("menu-photo", sha) is not None
    async with site.session() as session:
        again = await upload_part(session, site.store, site.owner, "menu-photo", part())
        count = await session.scalar(select(func.count(VideoShortsAsset.id)))
    assert again.complete and count == 1, "the same file twice is one asset"


@pytest.mark.asyncio
async def test_photos_alone_do_not_make_an_image_topic_ready(site: Site) -> None:
    async with site.session() as session:
        await topics.import_campaign(session, site.owner, campaign(), NOW)
        for index in range(3):
            data = PNG + bytes([index])
            out = await upload_part(
                session,
                site.store,
                site.owner,
                "shorts-taiwan-location",
                AssetPart(
                    sha256=hashlib.sha256(data).hexdigest(),
                    part=0,
                    parts=1,
                    size=len(data),
                    data=data,
                    need="landmarks",
                    filename=f"{index}.png",
                    author="站主",
                    rights_note="自己拍的",
                ),
                NOW,
            )
    assert out.topic is not None and out.topic.status == "needs_assets"
    assert out.topic.waiting_for == [topics.UNSUPPORTED["vision"]]


async def add_project(site: Site, slug: str, **fields: Any) -> VideoProject:
    async with site.session() as session:
        project = VideoProject(slug=slug, title=f"Video {slug}", stage="publish", **fields)
        session.add(project)
        await session.commit()
        return project


@pytest.mark.asyncio
async def test_public_tutorials_and_approved_episodes_give_topics_once(site: Site) -> None:
    await add_project(
        site,
        "ai-model-choice",
        youtube_video_id="a" * 11,
        youtube_publish_at=NOW - timedelta(days=3),
    )
    await add_project(
        site,
        "scheduled-later",
        youtube_video_id="b" * 11,
        youtube_publish_at=NOW + timedelta(days=3),
    )
    await add_project(
        site, "long-ago", youtube_video_id="c" * 11, youtube_publish_at=NOW - timedelta(days=200)
    )
    episode = await add_project(site, "drama-ep-1", format="drama", series_slug="ghost-story")
    pending = await add_project(site, "drama-ep-2", format="drama")
    async with site.session() as session:
        for project, status in ((episode, "approved"), (pending, "pending")):
            session.add(
                VideoReview(
                    project_id=project.id,
                    gate="final",
                    content_sha256="f" * 64,
                    summary="final",
                    status=status,
                    decided_at=NOW - timedelta(days=1) if status == "approved" else None,
                )
            )
        await session.commit()
        assert await topics.ensure_auto_topics(session, NOW) == 3
        await session.commit()
        assert await topics.ensure_auto_topics(session, NOW) == 0
        rows = sorted(await session.scalars(select(VideoShortsTopic)), key=lambda row: row.slug)
    assert [(row.slug, row.line, row.status, row.origin) for row in rows] == [
        ("ai-model-choice-cut-1", "cut", "ready", "auto"),
        ("ai-model-choice-cut-2", "cut", "ready", "auto"),
        ("drama-ep-1-vertical", "drama", "ready", "auto"),
    ]
    assert rows[0].source_slug == "ai-model-choice" and rows[2].series == "ghost-story"
    assert topics.is_paid(rows[2].line, rows[2].brief)


@pytest.mark.asyncio
async def test_the_week_is_planned_then_made_slot_by_slot(site: Site) -> None:
    await start_run(site)
    async with site.session() as session:
        await topics.import_campaign(session, site.owner, campaign(), NOW)
    await configure(site, last_brief_at=NOW)
    job = await next_job(site)
    assert job.kind == "plan" and job.plan is not None
    window = job.plan.open_slots
    assert len(window) == 13 and window[0].local_date == FIRST_DAY
    assert window[-1].local_date == date(2026, 10, 18)
    assert len(job.plan.topics) == 10 and job.plan.topics[0].slug == "shorts-receipt-total"
    picks = ["shorts-receipt-total", "shorts-poster-blind", "shorts-prompt-check"]
    items = [
        {"slot_id": str(slot.id), "topic_slug": slug}
        for slot, slug in zip(window[:3], picks, strict=True)
    ]
    await configure(site, weekly_quota={"lab": 1, "cut": 1, "drama": 0})
    async with site.session() as session:
        with pytest.raises(ShortsRefused) as over:
            await plan.apply_plan(session, PlanIn.model_validate({"items": items}), NOW)
    assert over.value.code == "video_shorts_plan_invalid" and "配額合計 2 支" in over.value.detail
    await configure(site, weekly_quota={"lab": 5, "cut": 2, "drama": 0})
    async with site.session() as session:
        written = await plan.apply_plan(session, PlanIn.model_validate({"items": items}), NOW)
    assert [slot.topic_slug for slot in written.planned] == picks
    assert {slot.status for slot in written.planned} == {"planned"}
    job = await next_job(site, NOW + timedelta(hours=1))
    assert job.kind == "make" and job.make is not None, "planned an hour ago; the pool is full"
    assert job.make.topic.slug == "shorts-receipt-total" and not job.make.resume
    assert job.make.slot.id == window[0].id and job.make.channel_stance == "只照實寫"
    assert job.make.topic.brief["test_protocol"]["input"].startswith("湯 85 元")
    assert (job.make.line, job.make.project_slug, job.make.source) == ("lab", None, None)
    async with site.session() as session:
        started = await jobs.start_topic(session, "shorts-receipt-total", NOW)
    assert started.created and started.topic.status == "making"
    async with site.session() as session:
        project = await session.scalar(
            select(VideoProject).where(VideoProject.slug == "shorts-receipt-total")
        )
        again = await jobs.start_topic(session, "shorts-receipt-total", NOW)
    assert project is not None and (project.format, project.shorts_line) == ("shorts", "lab")
    assert project.shorts_series == "daily" and not again.created
    job = await next_job(site, NOW + timedelta(hours=1))
    assert job.make is not None and job.make.resume, "the worker picks up what it started"
    assert job.make.project_slug == "shorts-receipt-total"
    async with site.session() as session:
        done = await jobs.finish_topic(session, "shorts-receipt-total", DoneIn(), NOW)
        same = await jobs.finish_topic(session, "shorts-receipt-total", DoneIn(), NOW)
        with pytest.raises(ShortsRefused) as unstarted:
            await jobs.finish_topic(session, "shorts-poster-blind", DoneIn(), NOW)
    assert done.status == same.status == "made" and done.finished_at == NOW
    assert unstarted.value.code == "video_shorts_topic_not_making"
    job = await next_job(site, NOW + timedelta(hours=1))
    assert job.make is not None and job.make.topic.slug == "shorts-poster-blind"
    # Once its package is approved, a Short made from a planned topic takes that topic's slot,
    # not the earliest open one.
    async with site.session() as session:
        await jobs.start_topic(session, "shorts-poster-blind", NOW)
    async with site.session() as session:
        project = await session.scalar(
            select(VideoProject).where(VideoProject.slug == "shorts-poster-blind")
        )
        assert project is not None
        slot = await slots.assign_approved(session, project, NOW)
        assert slot is not None and slot.id == window[1].id
        assert (slot.status, slot.topic_slug) == ("assigned", "shorts-poster-blind")


@pytest.mark.asyncio
async def test_a_start_respects_the_switch_the_pause_the_month_and_the_budget(
    site: Site,
) -> None:
    async with site.session() as session:
        await topics.import_campaign(session, site.owner, campaign(), NOW)

    async def refused(slug: str) -> str:
        async with site.session() as session:
            with pytest.raises(ShortsRefused) as error:
                await jobs.start_topic(session, slug, NOW)
        return error.value.code

    await configure(site, enabled=False)
    assert await refused("shorts-receipt-total") == "video_shorts_off"
    await configure(site, paused_at=NOW)
    assert await refused("shorts-receipt-total") == "video_shorts_paused"
    await configure(site, paused_at=None, max_per_month=0)
    assert await refused("shorts-receipt-total") == "video_shorts_month_full"
    await configure(site, max_per_month=60)
    assert await refused("shorts-taiwan-location") == "video_shorts_topic_not_ready"
    async with site.session() as session:
        session.add(
            VideoShortsCost(occurred_at=NOW, category="image", status="unknown", source="manual")
        )
        await session.commit()
    assert await refused("shorts-image-specificity") == "video_shorts_budget_stops"
    await add_project(site, "shorts-receipt-total", dropped_at=NOW)
    async with site.session() as session:
        started = await jobs.start_topic(session, "shorts-receipt-total", NOW)
    assert started.project_slug == "shorts-receipt-total-2", "a video already has the slug"


@pytest.mark.asyncio
async def test_last_week_s_report_cites_youtube_s_numbers_as_they_were_stored(
    site: Site,
) -> None:
    await start_run(site)
    await configure(site)
    monday = datetime(2026, 10, 12, 2, 0, tzinfo=UTC)
    video = "r" * 11
    await add_project(
        site,
        "shorts-receipt-total",
        format="shorts",
        shorts_line="lab",
        shorts_series="daily",
        youtube_video_id=video,
        youtube_publish_at=datetime(2026, 10, 6, 11, 30, tzinfo=UTC),
    )
    read_at = datetime(2026, 10, 7, 12, 0, tzinfo=UTC)
    async with site.session() as session:
        session.add(
            VideoShortsMetric(
                project_slug="shorts-receipt-total",
                youtube_video_id=video,
                period="d1",
                source="data_api",
                captured_at=read_at,
                views=1234,
                likes=56,
                comments=7,
                avg_view_percent=Decimal("81.50"),
            )
        )
        await session.commit()
    job = await next_job(site, monday)
    assert job.kind == "report" and job.report is not None
    assert (job.report.week_start, job.report.week_end) == (date(2026, 10, 5), date(2026, 10, 11))
    snapshot = job.report.published[0].snapshots[0]
    assert (snapshot.views, snapshot.source, snapshot.captured_at) == (1234, "data_api", read_at)
    body = {
        "week_start": "2026-10-05",
        "body_md": "收據那支照實寫兩組都算對；下週多做台灣日常。",
        "rows": [{"youtube_video_id": video, "period": "d1", "source": "data_api"}],
        "plan": [{"topic_slug": "shorts-taiwan-phrases", "line": "lab", "note": "日常系列"}],
        "provider": "claude_code",
        "model": "claude-sonnet-5",
    }
    async with site.session() as session:
        saved = await reports.save_report(session, ReportIn.model_validate(body), monday)
    assert saved.rows == [
        {
            "slug": "shorts-receipt-total",
            "title": "Video shorts-receipt-total",
            "youtube_video_id": video,
            "period": "d1",
            "source": "data_api",
            "captured_at": read_at.isoformat(),
            "range_start": None,
            "range_end": None,
            "views": 1234,
            "engaged_views": None,
            "likes": 56,
            "comments": 7,
            "shares": None,
            "subscribers_gained": None,
            "avg_view_seconds": None,
            "avg_view_percent": 81.5,
            "stayed_percent": None,
        }
    ], "the values YouTube gave, its source and read time, and nothing computed"
    async with site.session() as session:
        again = await reports.save_report(
            session, ReportIn.model_validate({**body, "body_md": "改寫過"}), monday
        )
        count = await session.scalar(select(func.count(VideoShortsReport.id)))
    assert again.id == saved.id and again.body_md == "改寫過" and count == 1
    assert (await next_job(site, monday)).kind != "report", "the week is written"
    unknown = {**body, "rows": [{"youtube_video_id": video, "period": "d7", "source": "data_api"}]}
    for changes, code in (
        (unknown, "video_shorts_report_row_unknown"),
        ({**body, "week_start": "2026-10-06"}, "video_shorts_report_week"),
        ({**body, "week_start": "2026-10-12"}, "video_shorts_report_week"),
    ):
        async with site.session() as session:
            with pytest.raises(ShortsRefused) as error:
                await reports.save_report(session, ReportIn.model_validate(changes), monday)
        assert error.value.code == code


def test_a_report_cites_snapshots_and_cannot_carry_numbers_of_its_own() -> None:
    row = {"youtube_video_id": "r" * 11, "period": "d1", "source": "data_api", "views": 999}
    with pytest.raises(ValidationError):
        ReportIn.model_validate({"week_start": "2026-10-05", "body_md": "x", "rows": [row]})


def test_the_settings_choose_the_subject_and_the_month_s_cap() -> None:
    values = {
        "enabled": False,
        "lines": ["lab"],
        "weekly_quota": {"lab": 5},
        "daily_pattern": [{"days": 30, "counts": [1]}],
        "slot_times": ["19:30"],
        "timezone": TAIPEI,
        "stock_days": 5,
        "lock_hours": 24,
        "upload_ahead_days": 10,
        "max_per_day": 2,
        "seconds_min": 25,
        "seconds_max": 55,
        "voice": {"provider": "gemini", "name": "Sulafat"},
        "budget_ntd_30d": 3000,
        "budget_soft_ntd": 2400,
        "budget_total_ntd": 9000,
    }
    defaults = SettingsWrite.model_validate(values)
    assert defaults.subject_models == {} and defaults.max_per_month == 60
    chosen = SettingsWrite.model_validate({**values, "subject_models": SUBJECT})
    assert chosen.subject_models["a"].model == "claude-sonnet-5"
    for wrong in ({"subject_models": {"c": SUBJECT["a"]}}, {"max_per_month": 401}):
        with pytest.raises(ValidationError):
            SettingsWrite.model_validate({**values, **wrong})


# --- the routes ---------------------------------------------------------------------------------


def _app(user: User | None, site: Site) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_automation_api.admin_router, prefix="/api/v1")
    app.include_router(admin_automation_api.tool_router, prefix="/api/v1")

    async def session() -> Any:
        async with site.session() as opened:
            yield opened

    app.dependency_overrides[get_session] = session
    if user is not None:
        app.dependency_overrides[current_user] = lambda: user
    return app


def _with_roles(*roles: str) -> User:
    user = User(id=uuid4(), email="someone@example.test", password_hash="unused")
    user._admin_roles_cache = frozenset(roles)  # type: ignore[attr-defined]
    return user


@pytest.fixture
def no_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(admin_automation_api, "enforce_named_rate_limit", AsyncMock())


@pytest.mark.asyncio
async def test_every_tab_route_asks_for_its_capability(site: Site) -> None:
    reads = [("GET", "topics", None), ("GET", "reports", None)]
    manage = [
        ("POST", "topics", {"title": "想法"}),
        ("POST", "topics/import", {"topics": []}),
        ("PATCH", "topics/shorts-receipt-total", {"release_order": 1}),
        ("POST", "topics/shorts-receipt-total/assets?sha256=" + "0" * 64, None),
    ]
    base = "/api/v1/admin/video-shorts/"

    async def statuses(user: User, calls: list[tuple[str, str, Any]]) -> set[int]:
        async with AsyncClient(
            transport=ASGITransport(app=_app(user, site)), base_url="http://test"
        ) as client:
            return {
                (await client.request(method, base + path, json=body)).status_code
                for method, path, body in calls
            }

    assert await statuses(_with_roles(), reads + manage) == {403}
    assert await statuses(_with_roles("viewer"), reads) == {200}
    assert await statuses(_with_roles("viewer"), manage) == {403}
    assert 403 not in await statuses(_with_roles("content"), manage)
    listed = {
        (method, route.path)  # type: ignore[attr-defined]
        for route in admin_automation_api.admin_router.routes
        for method in route.methods  # type: ignore[attr-defined]
    }
    assert len(listed) == len(reads + manage), "a new route is added to this test"


# The worker's paths as the site relays them (apps/web/app/api/video/automation/shorts).
WORKER_ROUTES = {
    ("GET", "/video/automation/shorts/next"),
    ("POST", "/video/automation/shorts/plan"),
    ("POST", "/video/automation/shorts/topics"),
    ("POST", "/video/automation/shorts/report"),
    ("POST", "/video/automation/shorts/{slug}/start"),
    ("POST", "/video/automation/shorts/{slug}/done"),
}


def test_the_worker_s_paths_are_the_ones_the_site_relays() -> None:
    listed = {
        (method, route.path)  # type: ignore[attr-defined]
        for route in admin_automation_api.tool_router.routes
        for method in route.methods  # type: ignore[attr-defined]
    }
    assert listed == WORKER_ROUTES
    relayed = REPO / "apps" / "web" / "app" / "api" / "video" / "automation" / "shorts"
    for _method, path in WORKER_ROUTES:
        folder = path.removeprefix("/video/automation/shorts/").replace("{slug}", "[slug]")
        assert (relayed / folder / "route.ts").is_file(), folder


@pytest.mark.asyncio
async def test_the_worker_reads_and_writes_with_its_token(site: Site, no_rate_limit: None) -> None:
    app = _app(None, site)
    base = "/api/v1/video/automation/shorts/"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        assert (await client.get(base + "next")).status_code == 401
        app.dependency_overrides[speech_api.video_tool] = lambda: site.token
        off = (await client.get(base + "next")).json()
        assert off == {
            "kind": None,
            "holds": ["Shorts 的自動製作關著"],
            "report": None,
            "plan": None,
            "brief": None,
            "make": None,
        }
        missing = await client.post(base + "nothing-here/start")
        assert (missing.status_code, missing.json()["code"]) == (
            404,
            "video_shorts_topic_not_found",
        )
        bad = await client.post(base + "Bad_Slug/done", json={})
        assert bad.status_code == 404
        written = await client.post(
            base + "topics", json={"topics": [{"slug": "shorts-new", "title": "新題"}]}
        )
        assert written.status_code == 200 and written.json()["created"] == 1
        empty = await client.post(base + "plan", json={"items": []})
        assert empty.status_code == 200 and empty.json() == {"planned": []}
        week = await client.post(base + "report", json={"week_start": "2026-10-06", "body_md": "x"})
        assert (week.status_code, week.json()["code"]) == (422, "video_shorts_report_week")
