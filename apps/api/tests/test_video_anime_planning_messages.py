"""The discussion worker cannot spend on an imported planning-only series."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import cast
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models import User
from app.video_automation import messages, series
from app.video_automation.models import VideoDramaMessage, VideoDramaSeries
from app.video_automation.schemas import MessageAnswerIn, MessageIn, SeriesContextOut

WHEN = datetime(2026, 10, 2, tzinfo=UTC)


def _series(slug: str, *, planning_only: bool) -> VideoDramaSeries:
    return VideoDramaSeries(
        id=uuid4(),
        slug=slug,
        title=slug,
        premise="Original fantasy",
        kind="series",
        planning_only=planning_only,
        category="anime" if planning_only else None,
        target_minutes=22 if planning_only else 8,
        planned_episodes=120,
        episodes_per_chapter=12,
        tone="no-romance",
        style_preset="anime-2d",
        genre="custom",
        lead="male",
        aspects=[],
        open_ended=False,
        status="paused" if planning_only else "active",
        hands_off=False,
        compilation=False,
        force_next=False,
        created_at=WHEN,
        updated_at=WHEN,
    )


@pytest.mark.asyncio
async def test_posting_to_planning_doc_does_not_queue_a_paid_discussion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = MagicMock()
    session.commit = AsyncMock()
    monkeypatch.setattr(
        series, "_series", AsyncMock(return_value=_series("plan", planning_only=True))
    )
    with pytest.raises(messages.MessageRefused) as caught:
        await messages.post_message(
            session, User(id=uuid4()), "plan", MessageIn(subject="setting", body="請改寫")
        )
    assert (caught.value.status, caught.value.code) == (409, "video_series_planning_only")
    session.add.assert_not_called()
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_direct_reply_to_an_old_queued_message_is_refused_without_writes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    row = VideoDramaMessage(
        id=uuid4(),
        series_id=uuid4(),
        author="owner",
        subject="setting",
        body_md="請改写",
        answered_at=None,
        created_at=WHEN,
    )
    session = MagicMock()
    session.scalar = AsyncMock(return_value=row)
    session.commit = AsyncMock()
    monkeypatch.setattr(
        series, "_series_by_id", AsyncMock(return_value=_series("plan", planning_only=True))
    )
    with pytest.raises(messages.MessageRefused) as caught:
        await messages.answer_message(session, row.id, MessageAnswerIn(reply_md="新版企劃"))
    assert (caught.value.status, caught.value.code) == (409, "video_series_planning_only")
    assert row.answered_at is None
    session.add.assert_not_called()
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_discussion_selector_skips_old_planning_messages_without_blocking_ordinary_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db = create_async_engine("sqlite+aiosqlite://")
    try:
        async with db.begin() as connection:
            await connection.run_sync(cast(sa.Table, VideoDramaSeries.__table__).create)
            await connection.run_sync(cast(sa.Table, VideoDramaMessage.__table__).create)
        factory = async_sessionmaker(db, expire_on_commit=False)
        async with factory() as session:
            plan, ordinary = (
                _series("plan", planning_only=True),
                _series("normal", planning_only=False),
            )
            session.add_all([plan, ordinary])
            await session.flush()
            blocked = VideoDramaMessage(
                id=uuid4(),
                series_id=plan.id,
                author="owner",
                subject="setting",
                body_md="Old imported message",
                created_at=WHEN,
            )
            allowed = VideoDramaMessage(
                id=uuid4(),
                series_id=ordinary.id,
                author="owner",
                subject="setting",
                body_md="Please discuss",
                created_at=WHEN + timedelta(seconds=1),
            )
            session.add_all([blocked, allowed])
            await session.commit()
            monkeypatch.setattr(messages, "_target", AsyncMock(return_value=(None, None, None)))
            monkeypatch.setattr(messages, "_thread", AsyncMock(return_value=[allowed]))
            monkeypatch.setattr(series, "_docs", AsyncMock(return_value=[]))
            monkeypatch.setattr(series, "_episodes", AsyncMock(return_value=[]))
            monkeypatch.setattr(
                series,
                "context_view",
                AsyncMock(
                    return_value=SeriesContextOut(
                        series=series.summary_view(ordinary, [], []),
                        setting=None,
                        outline=None,
                        chapter=None,
                        chapter_number=None,
                        chapter_range=None,
                        episode=None,
                        episodes=[],
                        recaps=[],
                        mysteries=[],
                    )
                ),
            )
            selected = await messages.next_message(session)
            assert selected.job and selected.job.message.id == allowed.id
            assert selected.job.series.slug == ordinary.slug
            assert blocked.answered_at is None
            await session.delete(allowed)
            await session.commit()
            assert (await messages.next_message(session)).job is None
    finally:
        await db.dispose()
