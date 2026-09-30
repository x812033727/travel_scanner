"""Shorts against PostgreSQL: from a pushed final cut to a locked slot, the consent, the
ledger and the sidebar's count.

The Shorts' settings are one row and the calendar is one table, so everything here runs in
a transaction that is rolled back: the commits inside are savepoints, and the database the
other tests share is left as it was.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin import operations_service
from app.admin.service import encrypt_secrets
from app.db import SessionFactory, engine
from app.models import (
    AdminAuditLog,
    User,
    VideoProject,
    VideoReview,
    VideoToolToken,
    VideoYoutubeConnection,
)
from app.video_automation import judge as judging
from app.video_reviews import admin_service as service
from app.video_reviews.schemas import ProjectIn, ReviewIn
from app.video_reviews.storage import ReviewStore
from app.video_shorts import costs, overview, slots
from app.video_shorts import settings as shorts_settings
from app.video_shorts.models import (
    VideoShortsCost,
    VideoShortsMetric,
    VideoShortsSettings,
    VideoShortsSlot,
)
from app.video_shorts.schemas import CostIn, SlotPatch
from app.video_speech.gemini import DEFAULT_GEMINI_TTS_MODEL

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

CHANNEL = "UC" + "s" * 22
USAGE = {
    "narration": {"seconds": 40, "characters": 268, "provider": "gemini"},
    "stages": {"writer": {"calls": 2, "provider": "claude_code"}},
}


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


@asynccontextmanager
async def rolled_back() -> AsyncIterator[AsyncSession]:
    async with engine.connect() as connection:
        transaction = await connection.begin()
        session = AsyncSession(
            bind=connection, expire_on_commit=False, join_transaction_mode="create_savepoint"
        )
        try:
            for model in (VideoShortsSlot, VideoShortsCost, VideoShortsMetric, VideoShortsSettings):
                await session.execute(delete(model))
            await session.execute(delete(VideoYoutubeConnection))
            await session.commit()
            yield session
        finally:
            await session.close()
            await transaction.rollback()


def _report(items: tuple[str, ...], sha: str) -> dict[str, Any]:
    return {
        "ok": True,
        "final_sha256": sha,
        "kind": "shorts",
        "items": [{"id": name, "ok": True} for name in items],
    }


async def _approved(
    session: AsyncSession, store: ReviewStore, token: VideoToolToken, slug: str, line: str
) -> None:
    sha = uuid4().hex * 2
    await service.upsert_project(
        session,
        store,
        slug,
        ProjectIn(title=slug, stage="final", format="shorts", shorts_line=line),  # type: ignore[arg-type]
    )
    final = await service.submit_review(
        session,
        store,
        slug,
        ReviewIn(
            gate="final",
            content_sha256=sha,
            summary="成片",
            payload={"qa": _report(judging.SHORTS_QA_ITEMS, sha), "usage": USAGE},
        ),
        token,
    )
    package = await service.submit_review(
        session,
        store,
        slug,
        ReviewIn(
            gate="publish",
            content_sha256=sha,
            summary="上傳包",
            payload={
                "package": _report(judging.SHORTS_PACKAGE_ITEMS, sha),
                "final_review_id": str(final.id),
            },
        ),
        token,
    )
    assert (final.status, package.status) == ("approved", "approved")


@pytest.mark.asyncio(loop_scope="module")
async def test_a_short_goes_from_a_pushed_cut_to_a_locked_slot(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(costs, "lookup_rate", AsyncMock(return_value=Decimal("32.5")))
    store = ReviewStore(tmp_path, max_file_bytes=10_000, max_total_bytes=50_000)
    tag = uuid4().hex[:10]
    first, second = f"short-{tag}-a", f"short-{tag}-b"
    now = datetime.now(UTC)
    first_day = (now + timedelta(days=2)).date()
    async with rolled_back() as session:
        owner = User(email=f"shorts-{uuid4()}@example.com", password_hash="unused")
        token = VideoToolToken(name="it", token_hash=uuid4().hex * 2, token_prefix="mkv_it")
        session.add_all([owner, token])
        session.add(
            VideoYoutubeConnection(
                id=1,
                channel_id=CHANNEL,
                channel_title="Mokaair",
                audited=False,
                secret_config_encrypted=encrypt_secrets(
                    {"refresh_token": "r", "client_secret": "s"}
                ),
            )
        )
        await session.commit()
        before = (await operations_service._live_pending_counts(session))["video_reviews_pending"]  # noqa: SLF001

        await _approved(session, store, token, first, "lab")
        listed = await service.list_projects(session, shorts="only", state="library")
        assert [item.slug for item in listed] == [first]
        assert first not in [
            item.slug for item in await service.list_projects(session, shorts="exclude")
        ]
        ledger = list(
            await session.scalars(
                select(VideoShortsCost).where(VideoShortsCost.project_slug == first)
            )
        )
        assert sorted(line.category for line in ledger) == ["models", "narration"]
        narration = next(line for line in ledger if line.category == "narration")
        price = costs.narration_price(DEFAULT_GEMINI_TTS_MODEL, now.date())
        assert price is not None
        spent = (Decimal(40) * price).quantize(Decimal("0.0001"))
        assert narration.amount == spent
        assert narration.amount_ntd == costs.to_ntd(spent, Decimal("32.5"))

        started = await slots.start_campaign(session, owner, first_day, now)
        assert (started.slots, started.assigned) == (120, 1)
        await _approved(session, store, token, second, "cut")
        calendar = list(
            await session.scalars(select(VideoShortsSlot).order_by(VideoShortsSlot.starts_at))
        )
        assert [slot.project_slug for slot in calendar[:3]] == [first, second, None]
        assert calendar[0].starts_at.tzinfo is not None
        view = await service.project_view(session, second)
        assert (view.shorts_state, view.slot_at) == ("slotted", calendar[1].starts_at)

        # A Short holds one slot: the database refuses a second, whatever the code did.
        savepoint = await session.begin_nested()
        calendar[2].project_slug, calendar[2].status = first, "locked"
        with pytest.raises(IntegrityError):
            await session.flush()
        await savepoint.rollback()
        await session.refresh(calendar[2])

        moved = await slots.patch_slot(
            session,
            owner,
            calendar[2].id,
            SlotPatch(action="assign", project_slug=first),
            now,
        )
        assert moved.project_slug == first
        await session.refresh(calendar[0])
        assert (calendar[0].project_slug, calendar[0].status) == (None, "open")

        offer = shorts_settings.consent_view(
            await shorts_settings.settings_row(session),
            await shorts_settings.channel_facts(session),
            now,
        ).offer
        assert offer is not None and offer.scope["channel_id"] == CHANNEL
        granted = await shorts_settings.grant_autopublish(session, owner, offer.text_sha256, now)
        assert granted.consent.state == "valid"

        due = calendar[1].starts_at - timedelta(hours=23)
        changes = await slots.lock_due_slots(session, due)
        await session.commit()
        assert [(change.status, change.project_slug) for change in changes] == [
            ("missed", None),
            ("locked", second),
        ], "the first slot was emptied and the library is empty; the second is locked"

        top = await overview.overview(session, due)
        assert top.autopublish == "on"
        kinds = [need.kind for need in top.needs]
        assert kinds == ["worker", "upload"], "no knock yet, and two files to upload"
        assert top.needs[1].count == 2
        assert (top.campaign.slots, top.campaign.missed) == (120, 1)
        counted = await operations_service._live_pending_counts(session)  # noqa: SLF001
        waiting = await session.scalar(
            select(func.count()).select_from(VideoReview).where(VideoReview.status == "pending")
        )
        assert counted["video_reviews_pending"] == int(waiting or 0) + 2
        assert counted["video_reviews_pending"] == before + 2

        await costs.add_manual(session, owner, CostIn(category="tool", status="unknown"), due)
        stopped = await overview.overview(session, due)
        assert not stopped.budget.paid_work_allowed and "budget" in [
            need.kind for need in stopped.needs
        ]
        actions = set(
            await session.scalars(
                select(AdminAuditLog.action).where(AdminAuditLog.actor_user_id == owner.id)
            )
        )
        assert actions == {
            "video_shorts_campaign_started",
            "video_shorts_slot_changed",
            "video_shorts_autopublish_granted",
            "video_shorts_cost_added",
        }
    # Nothing of it is left for the tests that share the database.
    async with SessionFactory() as session:
        left = await session.scalars(
            select(VideoProject.slug).where(VideoProject.slug.in_([first, second]))
        )
        assert list(left) == []
        held = await session.scalars(
            select(VideoShortsSlot.id).where(VideoShortsSlot.project_slug.in_([first, second]))
        )
        assert list(held) == []


@pytest.mark.asyncio(loop_scope="module")
async def test_the_calendar_reads_local_days_from_aware_moments() -> None:
    now = datetime.now(UTC)
    first_day: date = (now + timedelta(days=3)).date()
    async with rolled_back() as session:
        owner = User(email=f"shorts-{uuid4()}@example.com", password_hash="unused")
        session.add(owner)
        await session.commit()
        await slots.start_campaign(session, owner, first_day, now)
        week = await slots.list_slots(session, first_day, first_day + timedelta(days=6))
        assert [slot.local_date for slot in week.slots] == [
            first_day + timedelta(days=index) for index in range(7)
        ]
        assert {slot.local_time for slot in week.slots} == {"19:30"}
        assert week.timezone == "Asia/Taipei"
        assert len((await slots.list_slots(session)).slots) == 120
        assert await overview.owner_needs_count(session, now) >= 2, "no consent, no channel"
