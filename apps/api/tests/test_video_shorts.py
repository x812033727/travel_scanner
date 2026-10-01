"""Shorts on the server (docs/videos/SHORTS.md): the rules as pure functions, then the same
rules through the database. SQLite stands in for PostgreSQL here; the migration and the
routes against the real one are in test_migration_0109_video_shorts.py and
test_video_shorts_integration.py, which CI runs."""

from __future__ import annotations

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
from sqlalchemy import event, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.config import Settings
from app.db import Base, get_session
from app.models import (
    AdminAuditLog,
    ProviderConfig,
    User,
    VideoProject,
    VideoReview,
    VideoToolToken,
    VideoYoutubeConnection,
)
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api as automation_api
from app.video_automation import judge as judging
from app.video_automation.models import VideoAutomationSettings, VideoDramaSeries
from app.video_media.models import VideoMediaJob
from app.video_reviews import admin_service
from app.video_reviews.schemas import DecisionIn, DropIn, ProjectIn, ReviewIn, ReviewOut
from app.video_reviews.storage import ReviewStore
from app.video_shorts import admin_api, costs, overview, rules, slots
from app.video_shorts import settings as shorts_settings
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import (
    DEFAULT_DAILY_PATTERN,
    DEFAULT_SLOT_TIMES,
    VideoShortsCost,
    VideoShortsMetric,
    VideoShortsSettings,
    VideoShortsSlot,
)
from app.video_shorts.schemas import (
    CostIn,
    CostPatch,
    SettingsSave,
    SettingsWrite,
    SlotPatch,
)
from app.video_speech import admin_api as speech_api

TAIPEI = "Asia/Taipei"
FIRST_DAY = date(2026, 10, 5)
# The evening before the run's first day, Taipei time.
NOW = datetime(2026, 10, 4, 12, 0, tzinfo=UTC)
SHA = "f" * 64
CHANNEL = "UC" + "x" * 22


class Clock(datetime):
    """The clock the code reads, standing at NOW: the run these tests build starts the next
    day, and a test that read the real clock would fail once that day had come."""

    @classmethod
    def now(cls, tz: Any = None) -> Clock:
        moment = NOW if tz is not None else NOW.replace(tzinfo=None)
        return cls.fromisoformat(moment.isoformat())


@pytest.fixture(autouse=True)
def the_clock_stands_at_now(monkeypatch: pytest.MonkeyPatch) -> None:
    for module in (admin_service, slots, costs, shorts_settings, overview):
        monkeypatch.setattr(module, "datetime", Clock)


def at(day: int, hour: int = 11, minute: int = 30) -> datetime:
    """A moment of the run in UTC: day 1 at 11:30 is the first slot, 19:30 in Taipei."""
    return datetime(2026, 10, 5, hour, minute, tzinfo=UTC) + timedelta(days=day - 1)


# --- the calendar -------------------------------------------------------------------------------


def test_the_default_pace_is_120_slots_in_three_thirties() -> None:
    plans = rules.build_slots(FIRST_DAY, DEFAULT_DAILY_PATTERN, DEFAULT_SLOT_TIMES, TAIPEI)
    assert len(plans) == 120
    assert [sum(1 for plan in plans if plan.phase == phase) for phase in (1, 2, 3)] == [30, 45, 45]
    assert plans[0].starts_at == at(1), "19:30 in Taipei is 11:30 UTC"
    assert len({plan.starts_at for plan in plans}) == 120
    by_day: dict[int, list[datetime]] = {}
    for plan in plans:
        by_day.setdefault(plan.day, []).append(plan.starts_at)
    assert max(by_day) == 90 and all(len(by_day[day]) == 1 for day in range(1, 31))
    assert by_day[31] == [at(31, 4, 30), at(31)], "two a day: 12:30 is added, earliest first"
    assert len(by_day[32]) == 1 and len(by_day[33]) == 2
    assert rules.pattern_days(DEFAULT_DAILY_PATTERN) == 90


def test_a_pattern_takes_the_slot_times_in_the_order_they_are_listed() -> None:
    plans = rules.build_slots(
        FIRST_DAY, [{"days": 2, "counts": [1, 3]}], ["08:00", "21:15", "12:00"], TAIPEI
    )
    assert [plan.starts_at.astimezone(UTC).strftime("%d %H:%M") for plan in plans] == [
        "05 00:00",
        "06 00:00",
        "06 04:00",
        "06 13:15",
    ]
    assert rules.build_slots(FIRST_DAY, [{"days": 3, "counts": [0]}], ["08:00"], TAIPEI) == []


# --- where a Short stands -----------------------------------------------------------------------


def test_a_short_s_state_follows_its_life() -> None:
    state = rules.shorts_state
    facts = rules.ShortFacts()
    assert state(facts, NOW) == "making"
    assert state(replace(facts, pending_reviews=1), NOW) == "needs_you"
    assert state(replace(facts, blocked=True), NOW) == "needs_you"
    approved = replace(facts, package_approved=True)
    assert state(approved, NOW) == "library"
    assert state(replace(approved, missed_slots=1), NOW) == "missed"
    assert state(replace(approved, slot_status="assigned", missed_slots=1), NOW) == "slotted"
    assert state(replace(approved, slot_status="locked"), NOW) == "slotted"
    on_youtube = replace(
        approved, slot_status="locked", youtube_video_id="a" * 11, youtube_publish_at=at(1)
    )
    assert state(on_youtube, NOW) == "scheduled"
    assert state(replace(on_youtube, sync_done=True), NOW) == "scheduled"
    assert state(replace(on_youtube, sync_done=False), NOW) == "slotted", "the run did not finish"
    assert state(replace(approved, slot_status="scheduled"), NOW) == "scheduled"
    assert state(on_youtube, at(1)) == "published"
    assert state(replace(approved, slot_status="published"), NOW) == "published"
    assert state(replace(on_youtube, dropped=True), at(2)) == "dropped"


def test_what_waits_for_the_owner_is_never_hidden_behind_its_slot() -> None:
    waiting = rules.ShortFacts(package_approved=True, slot_status="assigned", pending_reviews=1)
    assert rules.shorts_state(waiting, NOW) == "needs_you"
    public = replace(waiting, youtube_video_id="a" * 11, youtube_publish_at=at(1))
    assert rules.shorts_state(public, at(2)) == "published", "what is public stays public"


# --- giving Shorts their slots ------------------------------------------------------------------


def _slot(day: int, status: str = "open", **fields: Any) -> rules.SlotFacts:
    return rules.SlotFacts(id=uuid4(), starts_at=at(day), status=status, **fields)


def _short(slug: str, line: str = "lab", day: int = 0, **fields: Any) -> rules.LibraryShort:
    return rules.LibraryShort(
        slug=slug, line=line, approved_at=NOW + timedelta(hours=day), **fields
    )


def test_an_approved_short_goes_to_its_own_slot_then_its_topic_s_then_the_earliest_open() -> None:
    held = _slot(5, "assigned", project_slug="mine")
    planned = _slot(4, "planned", topic_slug="receipt")
    first = _slot(2)
    taken = _slot(1, "assigned", project_slug="other")
    for_cut = _slot(3, line="cut")
    every = [held, planned, first, taken, for_cut]
    assert rules.assign_slot(every, _short("mine"), NOW) == held
    assert rules.assign_slot(every, _short("new", topic_slug="receipt"), NOW) == planned
    assert rules.assign_slot(every, _short("new"), NOW) == first
    assert rules.assign_slot([taken, for_cut], _short("new"), NOW) is None, "kept for another line"
    assert rules.assign_slot([taken, for_cut], _short("new", "cut"), NOW) == for_cut
    assert rules.assign_slot([first], _short("new"), at(2)) is None, "its time has come"
    public = _slot(1, "published", project_slug="mine")
    assert rules.assign_slot([public, first], _short("mine"), at(1, 12)) == public, (
        "approved again after it went public, it takes no second slot"
    )
    missed = _slot(1, "missed", project_slug="mine")
    assert rules.assign_slot([missed, first], _short("mine"), NOW) == first, (
        "a slot it missed is a record, and it is given the next"
    )
    assert rules.assign_slot([_slot(2, "skipped")], _short("new"), NOW) is None


def test_a_slot_is_locked_a_day_ahead_and_an_empty_one_takes_from_the_library() -> None:
    mine = _slot(1, "assigned", project_slug="mine")
    gone = _slot(2, "assigned", project_slug="dropped")
    empty = _slot(3, line="cut")
    far = _slot(9)
    library = [_short("lab-early", "lab", 1), _short("cut-late", "cut", 2)]
    # Day 3's slot is 71.5 hours away: a lock window of 72 reaches it, 24 only reaches day 1.
    changes = rules.lock_due([far, empty, gone, mine], library, ["mine"], NOW, 72)
    assert [(change.status, change.project_slug) for change in changes] == [
        ("locked", "mine"),
        ("locked", "lab-early"),
        ("locked", "cut-late"),
    ], "earliest slot first; a Short that is not ready is replaced; nothing beyond the window"
    assert [change.slot_id for change in changes] == [mine.id, gone.id, empty.id]
    day_ahead = rules.lock_due([far, empty, gone, mine], library, ["mine"], NOW, 24)
    assert [change.slot_id for change in day_ahead] == [mine.id]


def test_the_library_gives_the_slot_s_line_first_and_an_uploaded_short_before_the_audit() -> None:
    slot = _slot(1, line="cut")
    library = [
        _short("lab", "lab", 0),
        _short("cut", "cut", 5),
        _short("uploaded", "lab", 9, uploaded=True),
    ]
    assert rules.lock_due([slot], library, [], NOW, 24)[0].project_slug == "cut"
    before_audit = rules.lock_due([slot], library, [], NOW, 24, prefer_uploaded=True)
    assert before_audit[0].project_slug == "uploaded", "only a file on YouTube can go out"


def test_an_empty_library_misses_the_slot_and_nothing_is_published_late() -> None:
    assert [
        (change.status, change.project_slug, change.note)
        for change in rules.lock_due([_slot(1)], [], [], NOW, 24)
    ] == [("missed", None, "片庫是空的")]
    close = at(1) - timedelta(minutes=4)
    held = _slot(1, "locked", project_slug="mine")
    late = rules.lock_due([held, _slot(2, "scheduled", project_slug="ok")], [], ["mine"], close, 24)
    assert [(change.status, change.project_slug) for change in late] == [("missed", "mine")]
    assert rules.lock_due([held], [], ["mine"], close - timedelta(minutes=2), 24) == []


def test_missed_days_are_counted_back_from_the_latest_day_with_slots() -> None:
    days = [
        _slot(1, "published"),
        _slot(2, "missed"),
        _slot(3, "missed"),
        replace(_slot(3, "published"), starts_at=at(3, 4, 30)),
        _slot(4, "skipped"),
        _slot(5, "missed"),
        _slot(6),
    ]
    assert rules.missed_days_in_a_row(days, at(5, 12), TAIPEI) == 3
    assert rules.missed_days_in_a_row(days, at(1, 12), TAIPEI) == 0
    assert rules.missed_days_in_a_row([], NOW, TAIPEI) == 0


def test_the_library_covers_the_coming_days_it_can_fill() -> None:
    ahead = [
        _slot(1, "assigned", project_slug="a"),
        _slot(2),
        _slot(3),
        replace(_slot(3), starts_at=at(3, 4, 30)),
        _slot(4),
    ]
    assert rules.stock_cover(ahead, 0, NOW, TAIPEI) == 1, "day 1 is filled already"
    assert rules.stock_cover(ahead, 1, NOW, TAIPEI) == 2
    assert rules.stock_cover(ahead, 2, NOW, TAIPEI) == 2, "day 3 needs two"
    assert rules.stock_cover(ahead, 4, NOW, TAIPEI) == 4
    assert rules.stock_cover([], 3, NOW, TAIPEI) is None


# --- the budget ---------------------------------------------------------------------------------


def _cost(day: int, amount: str | None, status: str = "confirmed") -> rules.CostFacts:
    return rules.CostFacts(at(day), status, Decimal(amount) if amount is not None else None)


def _budget(lines: list[rules.CostFacts], now: datetime | None = None) -> rules.BudgetState:
    window = rules.budget_window(now or at(10), FIRST_DAY, TAIPEI)
    return rules.budget_state(lines, window, limit=3000, soft=2400, total_limit=9000)


def test_the_periods_are_the_run_s_own_thirty_days() -> None:
    start = datetime(2026, 10, 4, 16, 0, tzinfo=UTC)
    first = rules.budget_window(at(10), FIRST_DAY, TAIPEI)
    assert (first.period_start, first.period_end) == (start, start + timedelta(days=30))
    second = rules.budget_window(at(40), FIRST_DAY, TAIPEI)
    assert second.period_start == start + timedelta(days=30) and second.total_start == start
    before = rules.budget_window(NOW, FIRST_DAY, TAIPEI)
    just_after = NOW + timedelta(seconds=1)
    assert before.period_end == just_after, "a line entered this instant counts"
    assert before.period_start == just_after - timedelta(days=30)
    assert before.total_start == just_after - timedelta(days=90)
    assert rules.budget_window(NOW, None, TAIPEI) == before
    entered_now = rules.budget_state(
        [rules.CostFacts(NOW, "confirmed", Decimal("5"))],
        before,
        limit=3000,
        soft=2400,
        total_limit=9000,
    )
    assert entered_now.spent == Decimal("5")


def test_paid_work_stops_at_the_soft_limit_and_whenever_an_amount_is_unknown() -> None:
    fine = _budget([_cost(2, "1000"), _cost(3, "1399.99", "reserved")])
    assert fine.paid_work_allowed and fine.reason is None
    assert (fine.spent, fine.reserved) == (Decimal("1000"), Decimal("1399.99"))
    soft = _budget([_cost(2, "1000"), _cost(3, "1400", "reserved")])
    assert not soft.paid_work_allowed and "2,400" in str(soft.reason)
    hard = _budget([_cost(2, "3000")])
    assert not hard.paid_work_allowed and "上限 NT$3,000" in str(hard.reason)
    unknown = _budget([_cost(2, "1"), _cost(3, None, "unknown")])
    assert not unknown.paid_work_allowed and unknown.unknown == 1
    assert "不知道金額" in str(unknown.reason)


def test_a_new_period_starts_clean_and_the_run_s_total_still_counts() -> None:
    earlier = [_cost(2, "2900"), _cost(20, "2900"), _cost(35, "100")]
    second = _budget(earlier, at(40))
    assert second.spent == Decimal("100") and second.total_spent == Decimal("5900")
    assert second.paid_work_allowed
    over = _budget([*earlier, _cost(36, "2000"), _cost(61, "1100")], at(62))
    assert over.total_spent == Decimal("9000") and not over.paid_work_allowed
    assert "上限 NT$9,000" in str(over.reason)


def test_narration_is_priced_from_the_list_by_the_day_it_was_made() -> None:
    assert costs.narration_price("gemini-3.8-flash-tts", date(2026, 10, 5)) == Decimal("0.000225")
    assert costs.narration_price("gemini-3.8-flash-tts", date(2027, 1, 1)) == Decimal("0.00045")
    assert costs.narration_price("gemini-3.8-flash-lite-tts", date(2026, 12, 31)) == Decimal(
        "0.00015"
    )
    assert costs.narration_price("some-other-voice", date(2026, 10, 5)) is None
    assert costs.to_ntd(Decimal("0.0093"), Decimal("32.5")) == Decimal("0.30")


# --- the consent --------------------------------------------------------------------------------


def _scope(**changes: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "channel_id": CHANNEL,
        "channel_title": "Mokaair",
        "lines": ["lab", "cut"],
        "max_per_day": 2,
        "slot_times": ["19:30", "12:30"],
        "timezone": TAIPEI,
    }
    values.update(changes)
    return rules.consent_scope(**values)


def test_the_wording_names_the_scope_and_its_hash_changes_with_it() -> None:
    text = rules.consent_text(_scope())
    assert "Mokaair" in text and CHANNEL in text
    assert "實測、長片精華" in text and "漫劇" not in text.split("\n")[1]
    assert "一天最多 2 支" in text and "12:30、19:30" in text
    assert "私人" in text and "撤回" in text and "90 天" in text
    assert rules.consent_sha256(text) == rules.consent_sha256(rules.consent_text(_scope()))
    assert rules.consent_sha256(text) != rules.consent_sha256(
        rules.consent_text(_scope(max_per_day=3))
    )


def test_a_consent_covers_a_narrower_scope_and_no_wider_one() -> None:
    granted = _scope()
    assert rules.scope_problems(granted, _scope()) == []
    assert rules.scope_problems(granted, _scope(lines=["lab"])) == []
    assert rules.scope_problems(granted, _scope(max_per_day=1)) == []
    assert rules.scope_problems(granted, _scope(channel_title="Renamed")) == []
    assert rules.scope_problems(granted, _scope(channel_id="UC" + "y" * 22)) == ["連結的頻道換了"]
    assert rules.scope_problems(granted, _scope(lines=["lab", "cut", "drama"])) == [
        "多了內容線：漫劇直式短篇"
    ]
    assert rules.scope_problems(granted, _scope(max_per_day=3)) == ["每天上限調高了"]
    assert rules.scope_problems(granted, _scope(slot_times=["19:30", "13:00"])) == ["公開時間改了"]
    assert rules.scope_problems(granted, _scope(timezone="Asia/Tokyo")) == ["公開時間改了"]


def test_a_consent_holds_for_ninety_days_and_warns_a_week_before() -> None:
    granted = _scope()
    expires = NOW + timedelta(days=rules.CONSENT_DAYS)

    def state(now: datetime, current: dict[str, Any] | None = granted, on: bool = True) -> str:
        return rules.consent_state(
            autopublish=on, granted=granted, expires_at=expires, current=current, now=now
        )[0]

    assert state(NOW) == "valid"
    assert state(expires - timedelta(days=7)) == "expiring"
    assert state(expires) == "expired"
    assert state(NOW, _scope(max_per_day=3)) == "invalid"
    assert state(NOW, None) == "invalid", "no channel is linked any more"
    assert state(NOW, on=False) == "invalid", "a changed setting switched it off"
    none = rules.consent_state(
        autopublish=False, granted=None, expires_at=None, current=granted, now=NOW
    )
    assert none == ("none", None)
    assert rules.autopublish_state("none", False) == "off"
    assert rules.autopublish_state("valid", False) == "on"
    assert rules.autopublish_state("valid", True) == "paused"
    assert rules.autopublish_state("expiring", False) == "expiring"
    assert rules.autopublish_state("expired", True) == "expired"


# --- what the endpoints take --------------------------------------------------------------------


def _settings(**changes: Any) -> dict[str, Any]:
    values = shorts_settings.settings_values(_row()).model_dump()
    values.update(changes)
    return values


def _row(**fields: Any) -> VideoShortsSettings:
    """A settings row with the defaults the database would give it."""
    row = VideoShortsSettings(id=1)
    for column in VideoShortsSettings.__table__.columns:
        default = column.default
        if default is not None and getattr(row, column.name) is None:
            value = default.arg
            setattr(row, column.name, value(None) if callable(value) else value)
    for name, value in fields.items():
        setattr(row, name, value)
    return row


def test_the_defaults_are_the_pilot_s_pace_and_the_owner_s_choices() -> None:
    values = shorts_settings.settings_values(_row())
    assert values.lines == ["lab", "cut", "drama"]
    assert values.weekly_quota == {"lab": 5, "cut": 2, "drama": 0}
    assert (values.stock_days, values.lock_hours, values.max_per_day) == (5, 24, 2)
    assert (values.upload_ahead_days, values.seconds_min, values.seconds_max) == (10, 25, 55)
    assert values.voice.name == "Sulafat" and values.timezone == TAIPEI
    assert (values.budget_ntd_30d, values.budget_soft_ntd, values.budget_total_ntd) == (
        3000,
        2400,
        9000,
    )
    assert values.auto_approve is True and values.enabled is False and values.locales == []


@pytest.mark.parametrize(
    ("changes", "problem"),
    [
        ({"max_per_day": 1}, "more a day than max_per_day"),
        ({"slot_times": ["19:30"]}, "more a day than there are slot_times"),
        ({"slot_times": ["19:30", "19:30"]}, "slot_times must not repeat"),
        ({"slot_times": ["19:30", "25:00"]}, "slot_times"),
        ({"timezone": "Asia/Taipeii"}, "is not a timezone"),
        ({"seconds_min": 60, "seconds_max": 55}, "seconds_min must not exceed"),
        ({"budget_soft_ntd": 3001}, "budget_soft_ntd must not exceed"),
        ({"daily_pattern": [{"days": 400, "counts": [1]}]}, "daily_pattern"),
        ({"daily_pattern": [{"days": 30, "counts": [0]}]}, "publishes nothing"),
        ({"lines": ["lab"], "weekly_quota": {"lab": 5, "cut": 2}}, "weekly_quota names cut"),
        ({"lines": []}, "lines"),
        ({"locales": ["en", "en"]}, "locales must not repeat"),
    ],
)
def test_settings_that_do_not_hold_together_are_refused(
    changes: dict[str, Any], problem: str
) -> None:
    with pytest.raises(ValidationError, match=problem):
        SettingsWrite.model_validate(_settings(**changes))


def test_a_save_lays_what_was_sent_over_what_is_stored() -> None:
    current = _settings()
    merged = SettingsSave(stock_days=7, lines=["cut", "lab"]).merged_over(current)
    assert merged["stock_days"] == 7 and merged["lock_hours"] == 24
    assert SettingsWrite.model_validate(merged).lines == ["lab", "cut"], "kept in one order"
    assert SettingsSave().merged_over(current) == current


def test_a_slot_change_and_a_ledger_line_carry_what_they_need() -> None:
    with pytest.raises(ValidationError, match="move needs starts_at"):
        SlotPatch(action="move")
    with pytest.raises(ValidationError, match="assign needs project_slug"):
        SlotPatch(action="assign")
    with pytest.raises(ValidationError):
        SlotPatch(action="move", starts_at=datetime(2026, 10, 9, 19, 30))  # no timezone
    with pytest.raises(ValidationError, match="a confirmed line needs an amount"):
        CostIn(category="tool")
    with pytest.raises(ValidationError, match="an unknown line carries no amount"):
        CostIn(category="tool", status="unknown", amount=Decimal(0))
    assert CostIn(category="tool", status="unknown").amount is None
    with pytest.raises(ValidationError):
        CostIn(category="tool", amount=Decimal("-1"))


# --- through the database -----------------------------------------------------------------------

MODELS = (
    User,
    VideoProject,
    VideoReview,
    VideoToolToken,
    VideoYoutubeConnection,
    AdminAuditLog,
    VideoMediaJob,
    VideoAutomationSettings,
    VideoDramaSeries,
    VideoShortsSettings,
    VideoShortsSlot,
    VideoShortsMetric,
    VideoShortsCost,
    # The VPS uploader's settings row: the sender reads it (vps_settings.resolve) before it sends.
    ProviderConfig,
)


@dataclass
class Site:
    factory: async_sessionmaker[AsyncSession]
    owner: User
    token: VideoToolToken
    store: ReviewStore

    def session(self) -> AsyncSession:
        return self.factory()


@pytest.fixture
async def site(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> AsyncIterator[Site]:
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
        await session.commit()
    # The rate service is another host's: every test reads the same rates without it.
    monkeypatch.setattr(costs, "lookup_rate", rate_of)
    yield Site(
        factory,
        owner,
        token,
        ReviewStore(tmp_path / "reviews", max_file_bytes=10**8, max_total_bytes=10**9),
    )
    for model in MODELS:
        event.remove(model, "load", restore_utc)
        event.remove(model, "refresh", restore_utc)
    await engine.dispose()


async def rate_of(currency: str) -> Decimal | None:
    return Decimal(1) if currency == "TWD" else Decimal("32.5")


async def link_channel(site: Site, *, audited: bool = False, channel: str = CHANNEL) -> None:
    async with site.session() as session:
        row = await session.get(VideoYoutubeConnection, 1)
        if row is None:
            row = VideoYoutubeConnection(id=1)
            session.add(row)
        row.channel_id = channel
        row.channel_title = "Mokaair"
        row.audited = audited
        await session.commit()


@pytest.fixture(autouse=True)
def every_channel_row_is_linked(monkeypatch: pytest.MonkeyPatch) -> None:
    """The grant is encrypted with the site's key; here a row with a channel id is linked."""
    monkeypatch.setattr(shorts_settings, "linked", lambda row: bool(row.channel_id))


def _qa(sha: str = SHA, **changes: Any) -> dict[str, Any]:
    report: dict[str, Any] = {
        "ok": True,
        "final_sha256": sha,
        "kind": "shorts",
        "line": "lab",
        "items": [{"id": name, "ok": True, "detail": ""} for name in judging.SHORTS_QA_ITEMS],
    }
    report.update(changes)
    return report


def _package(sha: str) -> dict[str, Any]:
    return {
        "ok": True,
        "final_sha256": sha,
        "kind": "shorts",
        "items": [{"id": name, "ok": True} for name in judging.SHORTS_PACKAGE_ITEMS],
    }


USAGE = {
    "narration": {
        "seconds": 40,
        "characters": 268,
        "calls": 14,
        "provider": "gemini",
        "model": "gemini-3.8-flash-tts",
    },
    "stages": {"writer": {"calls": 2, "provider": "claude_code"}, "verifier": {"calls": 1}},
    "checks": {"transcribe": 14, "judge": 1, "policy": 1},
}


async def report_short(
    site: Site, slug: str, line: str = "lab", *, video_format: str = "shorts", **fields: Any
) -> None:
    async with site.session() as session:
        await admin_service.upsert_project(
            session,
            site.store,
            slug,
            ProjectIn(
                title=f"Short {slug}",
                stage="final",
                format=video_format,  # type: ignore[arg-type]
                shorts_line=line,  # type: ignore[arg-type]
                shorts_series="daily",
                **fields,
            ),
        )


async def submit(
    site: Site, slug: str, gate: str, payload: dict[str, Any], sha: str = SHA
) -> ReviewOut:
    async with site.session() as session:
        return await admin_service.submit_review(
            session,
            site.store,
            slug,
            ReviewIn(gate=gate, content_sha256=sha, summary=f"{gate} of {slug}", payload=payload),  # type: ignore[arg-type]
            site.token,
        )


async def approved_short(site: Site, slug: str, line: str = "lab", sha: str = SHA) -> UUID:
    """A Short whose cut and package passed; return the final review's approved identity."""
    await report_short(site, slug, line)
    final = await submit(site, slug, "final", {"qa": _qa(sha)}, sha)
    assert final.status == "approved"
    package = await submit(
        site, slug, "publish", {"package": _package(sha), "final_review_id": str(final.id)}, sha
    )
    assert package.status == "approved"
    return final.id


async def rows(site: Site, model: Any, *order: Any) -> list[Any]:
    async with site.session() as session:
        return list(await session.scalars(select(model).order_by(*order)))


async def start(site: Site, first_day: date = FIRST_DAY, now: datetime = NOW) -> Any:
    async with site.session() as session:
        return await slots.start_campaign(session, site.owner, first_day, now)


@pytest.mark.asyncio
async def test_a_short_whose_twelve_checks_passed_is_approved_as_it_arrives(site: Site) -> None:
    await report_short(site, "receipt-total")
    review = await submit(site, "receipt-total", "final", {"qa": _qa(), "usage": USAGE})
    assert review.status == "approved"
    assert review.note == "Shorts 自動品管 12 項全過，依設定自動核准"
    audit = [row for row in await rows(site, AdminAuditLog) if row.actor_user_id is None]
    assert [(row.action, row.metadata_json["gate"]) for row in audit] == [
        ("video_review_auto_approved", "final")
    ]
    package = await submit(
        site, "receipt-total", "publish",
        {"package": _package(SHA), "final_review_id": str(review.id)},
    )
    assert package.status == "approved"
    assert package.note == "Shorts 上傳包 4 項齊全，依設定自動核准"
    async with site.session() as session:
        view = await admin_service.project_view(session, "receipt-total")
    assert (view.format, view.shorts_line, view.shorts_series) == ("shorts", "lab", "daily")
    assert view.shorts_state == "library" and view.slot_at is None
    assert view.ready_to_upload, "a Short waits for no decision on the language panel"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "report",
    [
        _qa(kind="episode"),
        {key: value for key, value in _qa().items() if key != "kind"},
        _qa(final_sha256="0" * 64),
        _qa(ok=False),
        _qa(items=_qa()["items"][:-1]),
        {
            "ok": True,
            "final_sha256": SHA,
            "items": [{"id": name, "ok": True} for name in judging.QA_ITEMS],
        },
    ],
    ids=["another-kind", "no-kind", "another-cut", "not-ok", "an-item-short", "a-long-video-s"],
)
async def test_a_report_that_is_not_a_passing_short_s_waits_for_the_owner(
    site: Site, report: dict[str, Any]
) -> None:
    await report_short(site, "receipt-total")
    review = await submit(site, "receipt-total", "final", {"qa": report, "usage": USAGE})
    assert review.status == "pending"
    assert await rows(site, VideoShortsCost) == [], "nothing is entered before an approval"
    async with site.session() as session:
        view = await admin_service.project_view(session, "receipt-total")
    assert view.shorts_state == "needs_you"


@pytest.mark.asyncio
async def test_the_switch_off_leaves_every_short_to_the_owner(site: Site) -> None:
    async with site.session() as session:
        row = await shorts_settings.settings_row(session)
        row.auto_approve = False
        await session.commit()
    await report_short(site, "receipt-total")
    review = await submit(site, "receipt-total", "final", {"qa": _qa(), "usage": USAGE})
    assert review.status == "pending"
    async with site.session() as session:
        decided = await admin_service.decide(
            session, "receipt-total", review.id, site.owner, DecisionIn(decision="approve")
        )
    assert decided.status == "approved"
    lines = await rows(site, VideoShortsCost, VideoShortsCost.category)
    assert [line.category for line in lines] == ["checks", "models", "narration"], (
        "the owner's approval enters the usage too"
    )


@pytest.mark.asyncio
async def test_a_long_video_is_judged_as_it_always_was(site: Site) -> None:
    async with site.session() as session:
        await admin_service.upsert_project(
            session, site.store, "tutorial", ProjectIn(title="Tutorial", stage="final")
        )
    long_report = {
        "ok": True,
        "final_sha256": SHA,
        "items": [{"id": name, "ok": True} for name in judging.QA_ITEMS],
    }
    assert (await submit(site, "tutorial", "final", {"qa": _qa()})).status == "pending"
    async with site.session() as session:
        await admin_service.upsert_project(
            session, site.store, "tutorial-two", ProjectIn(title="Tutorial 2", stage="final")
        )
    passed = await submit(site, "tutorial-two", "final", {"qa": long_report, "usage": USAGE})
    assert passed.status == "approved" and passed.note == judging.QA_AUTO_APPROVED_NOTE
    assert await rows(site, VideoShortsCost) == [], "the ledger is the Shorts'"
    async with site.session() as session:
        view = await admin_service.project_view(session, "tutorial-two")
    assert (view.format, view.shorts_line, view.shorts_state, view.slot_at) == (
        "slides",
        None,
        None,
        None,
    )


@pytest.mark.asyncio
async def test_the_card_pipeline_only_makes_shorts(site: Site) -> None:
    async with site.session() as session:
        with pytest.raises(AppError) as refused:
            await admin_service.upsert_project(
                session,
                site.store,
                "no-line",
                ProjectIn(title="No line", stage="final", format="shorts"),
            )
    assert refused.value.code == "video_shorts_line_missing"
    await report_short(site, "vertical", "drama", video_format="drama", source_slug="episode-3")
    async with site.session() as session:
        # A report that leaves the Shorts fields out keeps them.
        view = await admin_service.upsert_project(
            session, site.store, "vertical", ProjectIn(title="Vertical", stage="final")
        )
    assert (view.format, view.shorts_line, view.source_slug) == ("drama", "drama", "episode-3")
    with pytest.raises(ValidationError):
        ProjectIn(title="x", stage="final", shorts_line="travel")  # type: ignore[arg-type]


# --- the ledger ---------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_the_usage_of_a_final_cut_is_entered_once(site: Site) -> None:
    await report_short(site, "receipt-total")
    payload = {"qa": _qa(), "usage": USAGE}
    await submit(site, "receipt-total", "final", payload)
    await submit(site, "receipt-total", "final", payload)
    async with site.session() as session:
        again = await costs.record_usage(session, "receipt-total", payload, SHA)
        await session.commit()
    assert again == []
    lines = {line.category: line for line in await rows(site, VideoShortsCost)}
    assert sorted(lines) == ["checks", "models", "narration"]
    narration = lines["narration"]
    assert (narration.status, narration.source, narration.currency) == ("confirmed", "auto", "USD")
    price = costs.narration_price("gemini-3.8-flash-tts", NOW.date())
    assert price is not None
    spent = (Decimal(40) * price).quantize(Decimal("0.0001"))
    assert narration.amount == spent, "40 seconds at the list's price"
    assert narration.fx_rate == Decimal("32.5")
    assert narration.amount_ntd == costs.to_ntd(spent, Decimal("32.5"))
    assert narration.units == USAGE["narration"]
    assert narration.dedupe_key == f"usage:receipt-total:{SHA[:16]}:narration"
    assert (lines["models"].amount_ntd, lines["models"].status) == (Decimal(0), "confirmed")
    assert "訂閱帳號" in str(lines["models"].note)
    assert lines["checks"].units == USAGE["checks"]
    # Another cut of the same Short is another entry.
    other = "e" * 64
    await submit(site, "receipt-total", "final", {"qa": _qa(other), "usage": USAGE}, other)
    assert len(await rows(site, VideoShortsCost)) == 6


@pytest.mark.asyncio
async def test_what_cannot_be_priced_is_unknown_and_not_zero(site: Site) -> None:
    await report_short(site, "receipt-total")
    usage = {
        "narration": {"seconds": 38.5, "characters": 250, "provider": "azure"},
        "stages": {"writer": {"calls": 2, "provider": "anthropic", "output_tokens": 900}},
    }
    await submit(site, "receipt-total", "final", {"qa": _qa(), "usage": usage})
    lines = {line.category: line for line in await rows(site, VideoShortsCost)}
    assert {line.status for line in lines.values()} == {"unknown"}
    assert all(line.amount is None and line.amount_ntd is None for line in lines.values())
    assert "writer" in str(lines["models"].note)
    await report_short(site, "local-voice")
    local = {"narration": {"seconds": 30, "characters": 200, "provider": "windows"}}
    other = "d" * 64
    await submit(site, "local-voice", "final", {"qa": _qa(other), "usage": local}, other)
    async with site.session() as session:
        free = await session.scalar(
            select(VideoShortsCost).where(VideoShortsCost.project_slug == "local-voice")
        )
    assert free is not None and (free.status, free.amount_ntd) == ("confirmed", Decimal(0))


@pytest.mark.asyncio
async def test_a_payload_without_usage_or_with_a_broken_one_enters_nothing(site: Site) -> None:
    await report_short(site, "receipt-total")
    await submit(site, "receipt-total", "final", {"qa": _qa(), "usage": {"narration": "lots"}})
    other = "e" * 64
    await submit(site, "receipt-total", "final", {"qa": _qa(other)}, other)
    assert await rows(site, VideoShortsCost) == []


@pytest.mark.asyncio
async def test_a_rate_the_service_cannot_give_falls_back_and_says_so(
    site: Site, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def silent(currency: str) -> Decimal | None:
        return Decimal(1) if currency == "TWD" else None

    monkeypatch.setattr(costs, "lookup_rate", silent)
    await report_short(site, "receipt-total")
    await submit(site, "receipt-total", "final", {"qa": _qa(), "usage": USAGE})
    async with site.session() as session:
        first = await session.scalar(
            select(VideoShortsCost).where(VideoShortsCost.category == "narration")
        )
        assert first is not None and first.fx_rate == Decimal("32")
        assert "備用匯率" in str(first.note)
        first.fx_rate = Decimal("31.25")
        await session.commit()
        rate, note = await costs.rate_for(session, "USD")
        assert rate == Decimal("31.25") and "最近一次" in str(note)
        assert await costs.rate_for(session, "EUR") == (None, None)
        with pytest.raises(ShortsRefused) as refused:
            await costs.add_manual(
                session, site.owner, CostIn(category="tool", amount=Decimal(5), currency="EUR")
            )
        assert refused.value.code == "video_shorts_rate_unavailable"
        given = await costs.add_manual(
            session,
            site.owner,
            CostIn(category="tool", amount=Decimal(5), currency="EUR", fx_rate=Decimal("35.2")),
        )
    assert given.amount_ntd == 176.0


@pytest.mark.asyncio
async def test_a_reservation_becomes_the_confirmed_line_in_the_same_row(site: Site) -> None:
    async with site.session() as session:
        held = await costs.reserve(
            session,
            key="image:receipt:1",
            slug="receipt",
            category="image",
            amount=Decimal("0.134"),
            now=at(2),
        )
        again = await costs.reserve(
            session,
            key="image:receipt:1",
            slug="receipt",
            category="image",
            amount=Decimal("9"),
            now=at(2),
        )
        await session.commit()
        assert again is held and held.status == "reserved"
        assert held.amount_ntd == Decimal("4.36")
        done = await costs.confirm(session, "image:receipt:1", Decimal("0.2"))
        await session.commit()
        assert done is held and (done.status, done.amount_ntd) == ("confirmed", Decimal("6.50"))
        assert await costs.confirm(session, "image:receipt:2") is None
        await costs.reserve(
            session,
            key="clip:receipt:1",
            slug="receipt",
            category="clip",
            amount=Decimal("1.2"),
            now=at(2),
        )
        await session.commit()
        assert await costs.release(session, "clip:receipt:1") is True
        assert await costs.release(session, "image:receipt:1") is False, "it was spent"
        await session.commit()
    lines = await rows(site, VideoShortsCost)
    assert [(line.dedupe_key, line.status) for line in lines] == [("image:receipt:1", "confirmed")]


@pytest.mark.asyncio
async def test_the_owner_enters_corrects_and_removes_their_own_lines(site: Site) -> None:
    async with site.session() as session:
        fee = await costs.add_manual(
            session,
            site.owner,
            CostIn(category="subscription", amount=Decimal("20"), currency="USD", note="訂閱"),
            at(2),
        )
        assert (fee.amount_ntd, fee.fx_rate, fee.source) == (650.0, 32.5, "manual")
        unknown = await costs.add_manual(
            session,
            site.owner,
            CostIn(category="tool", status="unknown", note="還沒收到帳單"),
            at(3),
        )
        assert (unknown.status, unknown.amount, unknown.amount_ntd) == ("unknown", None, None)
        row = await shorts_settings.settings_row(session)
        assert not (await costs.budget(session, row, at(4))).paid_work_allowed
        filled = await costs.update_cost(
            session, site.owner, unknown.id, CostPatch(amount=Decimal("300"))
        )
        assert (filled.status, filled.currency, filled.amount_ntd) == ("confirmed", "TWD", 300.0)
        state = await costs.budget(session, row, at(4))
        assert state.paid_work_allowed and state.spent == Decimal("950.00")
        back = await costs.update_cost(session, site.owner, unknown.id, CostPatch(status="unknown"))
        assert (back.status, back.amount) == ("unknown", None)
        await costs.delete_cost(session, site.owner, unknown.id)
        held = await costs.reserve(
            session, key="image:x:1", slug="x", category="image", amount=Decimal(1), now=at(3)
        )
        await session.commit()
        with pytest.raises(ShortsRefused) as reserved:
            await costs.update_cost(session, site.owner, held.id, CostPatch(amount=Decimal(2)))
        assert reserved.value.code == "video_shorts_cost_reserved"
        with pytest.raises(ShortsRefused) as automatic:
            await costs.delete_cost(session, site.owner, held.id)
        assert automatic.value.code == "video_shorts_cost_automatic"
        with pytest.raises(ShortsRefused) as missing:
            await costs.delete_cost(session, site.owner, uuid4())
        assert missing.value.status == 404
        view = await costs.costs_view(session, row, now=at(4))
        row.campaign_start = FIRST_DAY
        running = await costs.costs_view(session, row, now=at(4))
    assert [item.category for item in view.items] == ["image", "subscription"]
    assert (view.budget.spent_ntd, view.budget.reserved_ntd) == (650.0, 32.5)
    assert [period.lines for period in view.periods] == [0, 0, 2], (
        "before the run, the three thirties up to now"
    )
    assert [period.lines for period in running.periods] == [2, 0, 0], "then the run's own"
    assert running.periods[0].start == datetime(2026, 10, 4, 16, 0, tzinfo=UTC)
    assert (running.periods[0].spent_ntd, running.periods[0].reserved_ntd) == (650.0, 32.5)
    actions = [row.action for row in await rows(site, AdminAuditLog, AdminAuditLog.created_at)]
    assert actions == [
        "video_shorts_cost_added",
        "video_shorts_cost_added",
        "video_shorts_cost_updated",
        "video_shorts_cost_updated",
        "video_shorts_cost_deleted",
    ]


@pytest.mark.asyncio
async def test_a_line_without_an_amount_cannot_pass_for_a_confirmed_one(site: Site) -> None:
    async with site.session() as session:
        session.add(
            VideoShortsCost(
                occurred_at=NOW,
                category="tool",
                currency="TWD",
                status="confirmed",
                source="manual",
            )
        )
        with pytest.raises(IntegrityError):
            await session.commit()


# --- the run ------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_starting_the_run_builds_the_calendar_and_slots_what_is_in_the_library(
    site: Site,
) -> None:
    await approved_short(site, "second", "cut", "b" * 64)
    await approved_short(site, "first", "lab", "a" * 64)
    async with site.session() as session:
        for slug, hours in (("first", 3), ("second", 1)):
            review = await session.scalar(
                select(VideoReview)
                .join(VideoProject, VideoProject.id == VideoReview.project_id)
                .where(VideoProject.slug == slug, VideoReview.gate == "publish")
            )
            assert review is not None
            review.decided_at = NOW - timedelta(hours=hours)
        await session.commit()
    started = await start(site)
    assert (started.campaign_start, started.last_day) == (FIRST_DAY, date(2027, 1, 2))
    assert (started.slots, started.assigned) == (120, 2)
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    assert [(slot.project_slug, slot.status) for slot in calendar[:3]] == [
        ("first", "assigned"),
        ("second", "assigned"),
        (None, "open"),
    ], "in the order they were approved"
    assert [slot.phase for slot in calendar[29:31]] == [1, 2]
    async with site.session() as session:
        view = await admin_service.project_view(session, "first")
        assert (view.shorts_state, view.slot_at) == ("slotted", at(1))
        assert (await shorts_settings.settings_row(session)).campaign_start == FIRST_DAY
    audit = [row for row in await rows(site, AdminAuditLog) if "campaign" in row.action]
    assert audit[0].metadata_json == {
        "first_day": "2026-10-05",
        "last_day": "2027-01-02",
        "slots": 120,
        "assigned": 2,
        "rebuilt": False,
    }


@pytest.mark.asyncio
async def test_the_run_can_be_rebuilt_until_a_slot_was_acted_on(site: Site) -> None:
    await approved_short(site, "first")
    await start(site)
    later = await start(site, FIRST_DAY + timedelta(days=7))
    assert (later.slots, later.assigned) == (120, 1)
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    assert len(calendar) == 120 and calendar[0].starts_at == at(8)
    assert calendar[0].project_slug == "first"
    with pytest.raises(ShortsRefused) as past:
        await start(site, FIRST_DAY, at(1))
    assert past.value.code == "video_shorts_campaign_past"
    async with site.session() as session:
        slot = await session.get(VideoShortsSlot, calendar[0].id)
        assert slot is not None
        slot.status = "locked"
        await session.commit()
    with pytest.raises(ShortsRefused) as running:
        await start(site, FIRST_DAY + timedelta(days=14))
    assert running.value.code == "video_shorts_campaign_running"
    assert len(await rows(site, VideoShortsSlot)) == 120


@pytest.mark.asyncio
async def test_an_approved_package_takes_the_short_to_the_earliest_open_slot(site: Site) -> None:
    await start(site)
    first_final_id = await approved_short(site, "one", sha="a" * 64)
    second_final_id = await approved_short(site, "two", sha="b" * 64)
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    assert [slot.project_slug for slot in calendar[:3]] == ["one", "two", None]
    # Resending a package does not take a second slot. The synthetic scheduled slot below
    # has no YouTube ID or active upload; an updated package must preserve its existing slot.
    await submit(
        site, "one", "publish",
        {"package": _package("a" * 64), "final_review_id": str(first_final_id)}, "a" * 64,
    )
    async with site.session() as session:
        held = await session.get(VideoShortsSlot, calendar[1].id)
        assert held is not None
        held.status = "scheduled"
        await session.commit()
    again = await submit(
        site, "two", "publish",
        {"package": _package("c" * 64), "final_review_id": str(second_final_id)}, "c" * 64,
    )
    assert again.status == "approved"
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    assert [(slot.project_slug, slot.status) for slot in calendar[:3]] == [
        ("one", "assigned"),
        ("two", "scheduled"),
        (None, "open"),
    ]
    async with site.session() as session:
        held = await session.get(VideoShortsSlot, calendar[1].id)
        assert held is not None
        held.status = "assigned"
        await session.commit()
    async with site.session() as session:
        await admin_service.drop_project(
            session, site.store, "one", site.owner, DropIn(note="重做")
        )
        view = await admin_service.project_view(session, "one")
    assert view.shorts_state == "dropped"
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    assert [(slot.project_slug, slot.status) for slot in calendar[:2]] == [
        (None, "open"),
        ("two", "assigned"),
    ], "a dropped Short leaves its slot"


@pytest.mark.asyncio
async def test_a_short_holds_one_slot_and_keeps_the_ones_it_missed_as_a_record(
    site: Site,
) -> None:
    await start(site)
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    async with site.session() as session:
        first = await session.get(VideoShortsSlot, calendar[0].id)
        second = await session.get(VideoShortsSlot, calendar[1].id)
        third = await session.get(VideoShortsSlot, calendar[2].id)
        assert first is not None and second is not None and third is not None
        first.project_slug, first.status = "mine", "missed"
        second.project_slug, second.status = "mine", "assigned"
        await session.commit()
        held = await slots.holds(session, ["mine", "nobody"])
        assert held == {"mine": slots.Hold(at(2), "assigned", 1)}
        third.project_slug, third.status = "mine", "locked"
        with pytest.raises(IntegrityError):
            await session.commit()


# --- locking ------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_the_due_slots_are_locked_filled_or_missed(site: Site) -> None:
    await link_channel(site)
    await start(site)
    await approved_short(site, "one", sha="a" * 64)
    await approved_short(site, "spare", sha="b" * 64)
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    async with site.session() as session:
        second = await session.get(VideoShortsSlot, calendar[1].id)
        assert second is not None
        # The spare goes back to the library, and its slot stands empty.
        second.project_slug, second.status = None, "open"
        await session.commit()
        early = await slots.lock_due_slots(session, NOW - timedelta(days=1))
        assert early == [], "a day and a half ahead is outside the window"
        first = await slots.lock_due_slots(session, NOW)
        await session.commit()
        assert [(change.status, change.project_slug) for change in first] == [("locked", "one")]
        next_day = await slots.lock_due_slots(session, NOW + timedelta(days=1))
        await session.commit()
        assert [(change.status, change.project_slug, change.note) for change in next_day] == [
            ("missed", "one", "時段到了，這支還沒有排上 YouTube"),
            ("locked", "spare", "從片庫補上"),
        ]
        third = await slots.lock_due_slots(session, NOW + timedelta(days=2))
        await session.commit()
        assert [(change.status, change.project_slug) for change in third] == [
            ("missed", "spare"),
            ("locked", "one"),
        ], "the Short that missed its slot is back in the library and is given the next"
        view = await admin_service.project_view(session, "spare")
        assert view.shorts_state == "missed" and view.slot_at is None
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    assert [(slot.status, slot.project_slug) for slot in calendar[:4]] == [
        ("missed", "one"),
        ("missed", "spare"),
        ("locked", "one"),
        ("open", None),
    ]
    assert calendar[2].locked_at == NOW + timedelta(days=2)


# --- the owner's changes on the calendar --------------------------------------------------------


async def change(site: Site, slot_id: UUID, now: datetime = NOW, **fields: Any) -> Any:
    async with site.session() as session:
        return await slots.patch_slot(session, site.owner, slot_id, SlotPatch(**fields), now)


@pytest.mark.asyncio
async def test_the_owner_moves_fills_empties_and_skips_slots(site: Site) -> None:
    await start(site)
    await approved_short(site, "one", sha="a" * 64)
    await report_short(site, "unfinished")
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    first, second, third = (slot.id for slot in calendar[:3])

    moved = await change(site, second, action="assign", project_slug="one")
    assert (moved.project_slug, moved.status, moved.project_title) == (
        "one",
        "assigned",
        "Short one",
    )
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    assert [(slot.project_slug, slot.status) for slot in calendar[:2]] == [
        (None, "open"),
        ("one", "assigned"),
    ], "a Short holds one slot: giving it another empties the first"

    for slug, code in (
        ("unfinished", "video_shorts_not_ready"),
        ("nobody", "video_shorts_not_found"),
    ):
        with pytest.raises(ShortsRefused) as refused:
            await change(site, first, action="assign", project_slug=slug)
        assert refused.value.code == code

    noon = at(2, 4, 30)
    later = await change(site, second, action="move", starts_at=noon)
    assert (later.starts_at, later.local_time, str(later.local_date)) == (
        noon,
        "12:30",
        "2026-10-06",
    )
    with pytest.raises(ShortsRefused) as taken:
        await change(site, first, action="move", starts_at=noon)
    assert taken.value.code == "video_shorts_slot_taken"
    joined = await change(site, first, action="move", starts_at=at(3, 4, 30))
    assert (str(joined.local_date), joined.local_time) == ("2026-10-07", "12:30")
    with pytest.raises(ShortsRefused) as full:
        await change(site, second, action="move", starts_at=at(3, 2, 0))
    assert full.value.code == "video_shorts_day_full", "day 3 has its slot and the one moved in"
    with pytest.raises(ShortsRefused) as past:
        await change(site, second, action="move", starts_at=NOW - timedelta(hours=1))
    assert past.value.code == "video_shorts_slot_past"

    skipped = await change(site, second, action="skip", note="連假不發")
    assert (skipped.status, skipped.project_slug, skipped.note) == ("skipped", None, "連假不發")
    with pytest.raises(ShortsRefused) as closed:
        await change(site, second, action="assign", project_slug="one")
    assert closed.value.code == "video_shorts_slot_skipped"
    assert (await change(site, second, action="reopen")).status == "open"
    with pytest.raises(ShortsRefused) as not_skipped:
        await change(site, second, action="reopen")
    assert not_skipped.value.code == "video_shorts_slot_not_skipped"

    await change(site, third, action="assign", project_slug="one")
    emptied = await change(site, third, action="clear")
    assert (emptied.status, emptied.project_slug) == ("open", None)
    with pytest.raises(ShortsRefused) as missing:
        await change(site, uuid4(), action="clear")
    assert missing.value.status == 404
    audit = [row for row in await rows(site, AdminAuditLog) if row.action.endswith("slot_changed")]
    assert [row.metadata_json["action"] for row in audit] == [
        "assign",
        "move",
        "move",
        "skip",
        "reopen",
        "assign",
        "clear",
    ]
    assert audit[3].metadata_json["released"] == "one"


@pytest.mark.asyncio
async def test_a_slot_that_is_on_youtube_or_past_is_not_changed_here(site: Site) -> None:
    await start(site)
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    async with site.session() as session:
        for slot, status in zip(calendar[:3], ("scheduled", "published", "missed"), strict=True):
            row = await session.get(VideoShortsSlot, slot.id)
            assert row is not None
            row.status = status
        locked = await session.get(VideoShortsSlot, calendar[3].id)
        assert locked is not None
        locked.status, locked.project_slug, locked.locked_at = "locked", "one", NOW
        await session.commit()
    for slot in calendar[:3]:
        with pytest.raises(ShortsRefused) as fixed:
            await change(site, slot.id, action="skip")
        assert fixed.value.code == "video_shorts_slot_fixed"
    noted = await change(site, calendar[0].id, action="note", note="補發在週末")
    assert (noted.status, noted.note) == ("scheduled", "補發在週末")
    # A locked slot can still be changed; moving it lets the next round lock it again.
    moved = await change(site, calendar[3].id, action="move", starts_at=at(40, 4, 30))
    assert (moved.status, moved.locked_at, moved.phase) == ("assigned", None, 2)


# --- the settings and the consent ---------------------------------------------------------------


@pytest.mark.asyncio
async def test_the_owner_agrees_to_the_wording_they_were_shown(site: Site) -> None:
    async with site.session() as session:
        row = await shorts_settings.settings_row(session)
        nothing = shorts_settings.settings_view(row, await shorts_settings.channel_facts(session))
        assert nothing.consent.state == "none" and nothing.consent.offer is None
        with pytest.raises(ShortsRefused) as unlinked:
            await shorts_settings.grant_autopublish(session, site.owner, "0" * 64, NOW)
        assert unlinked.value.code == "video_shorts_no_channel"
    await link_channel(site)
    async with site.session() as session:
        row = await shorts_settings.settings_row(session)
        channel = await shorts_settings.channel_facts(session)
        offer = shorts_settings.settings_view(row, channel).consent.offer
        assert offer is not None and offer.scope["channel_id"] == CHANNEL
        assert shorts_settings.may_publish(row, channel, NOW) == (False, "還沒有自動上架授權")
        with pytest.raises(ShortsRefused) as stale:
            await shorts_settings.grant_autopublish(session, site.owner, "0" * 64, NOW)
        assert stale.value.code == "video_shorts_consent_stale"
        granted = await shorts_settings.grant_autopublish(
            session, site.owner, offer.text_sha256, NOW
        )
    assert granted.autopublish and granted.consent.state == "valid"
    assert granted.consent.expires_at == NOW + timedelta(days=90)
    assert granted.consent.granted_by_user_id == site.owner.id
    assert granted.consent.text_sha256 == offer.text_sha256
    assert granted.consent.scope == offer.scope
    audit = [row for row in await rows(site, AdminAuditLog) if "autopublish" in row.action]
    assert audit[0].action == "video_shorts_autopublish_granted"
    assert audit[0].actor_user_id == site.owner.id
    assert audit[0].metadata_json["text_sha256"] == offer.text_sha256
    assert UUID(audit[0].metadata_json["consent_id"])
    async with site.session() as session:
        row = await shorts_settings.settings_row(session)
        channel = await shorts_settings.channel_facts(session)
        assert shorts_settings.may_publish(row, channel, NOW) == (True, None)
        late = NOW + timedelta(days=90)
        assert shorts_settings.may_publish(row, channel, late)[0] is False
        await shorts_settings.set_paused(session, site.owner, True, NOW)
        assert shorts_settings.may_publish(row, channel, NOW) == (False, "自動上架暫停中")
        await shorts_settings.set_paused(session, site.owner, True, NOW)
        resumed = await shorts_settings.set_paused(session, site.owner, False)
        assert resumed.paused_at is None and resumed.autopublish
    actions = [row.action for row in await rows(site, AdminAuditLog, AdminAuditLog.created_at)]
    assert actions[-2:] == ["video_shorts_paused", "video_shorts_resumed"], "once each"


async def agree(site: Site, now: datetime = NOW) -> None:
    await link_channel(site)
    async with site.session() as session:
        row = await shorts_settings.settings_row(session)
        channel = await shorts_settings.channel_facts(session)
        offer = shorts_settings.consent_view(row, channel, now).offer
        assert offer is not None
        await shorts_settings.grant_autopublish(session, site.owner, offer.text_sha256, now)


async def save(site: Site, **changes: Any) -> Any:
    async with site.session() as session:
        current = shorts_settings.settings_values(await shorts_settings.settings_row(session))
        payload = SettingsWrite.model_validate({**current.model_dump(), **changes})
        return await shorts_settings.update_settings(session, site.owner, payload)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("changes", "holds"),
    [
        ({"stock_days": 9, "budget_ntd_30d": 5000, "auto_approve": False}, True),
        ({"lines": ["lab", "cut"], "weekly_quota": {"lab": 5, "cut": 2}}, True),
        ({"max_per_day": 3}, False),
        ({"slot_times": ["19:30", "12:00"]}, False),
        ({"timezone": "Asia/Tokyo"}, False),
    ],
    ids=["other-settings", "a-line-less", "more-a-day", "another-time", "another-timezone"],
)
async def test_a_setting_that_widens_the_scope_takes_the_consent_with_it(
    site: Site, changes: dict[str, Any], holds: bool
) -> None:
    await agree(site)
    saved = await save(site, **changes)
    assert saved.autopublish is holds
    assert saved.consent.state == ("valid" if holds else "invalid")
    audit = [row.action for row in await rows(site, AdminAuditLog, AdminAuditLog.created_at)]
    assert ("video_shorts_autopublish_invalidated" in audit) is not holds
    assert "video_shorts_settings_updated" in audit
    if not holds:
        assert "要重新同意" in str(saved.consent.problem)
        async with site.session() as session:
            row = await shorts_settings.settings_row(session)
            channel = await shorts_settings.channel_facts(session)
            assert shorts_settings.may_publish(row, channel, NOW)[0] is False
            offer = shorts_settings.consent_view(row, channel, NOW).offer
            assert offer is not None
            again = await shorts_settings.grant_autopublish(
                session, site.owner, offer.text_sha256, NOW
            )
        assert again.consent.state == "valid"


@pytest.mark.asyncio
async def test_another_channel_or_a_revocation_ends_the_consent(site: Site) -> None:
    await agree(site)
    await link_channel(site, channel="UC" + "y" * 22)
    async with site.session() as session:
        row = await shorts_settings.settings_row(session)
        channel = await shorts_settings.channel_facts(session)
        view = shorts_settings.consent_view(row, channel, NOW)
        assert view.state == "invalid" and "頻道換了" in str(view.problem)
        revoked = await shorts_settings.revoke_autopublish(session, site.owner)
    assert revoked.autopublish is False and revoked.consent.state == "none"
    assert revoked.consent.scope is None and revoked.consent.granted_at is None
    audit = [row.action for row in await rows(site, AdminAuditLog, AdminAuditLog.created_at)]
    assert audit[-1] == "video_shorts_autopublish_revoked"


# --- the lists ----------------------------------------------------------------------------------


async def seed_projects(
    site: Site, count: int, prefix: str, *, days_ago: int = 0, **fields: Any
) -> None:
    """Videos as the site would hold them, the first the newest; a public one went public
    the day before."""
    async with site.session() as session:
        for index in range(count):
            values = {
                "slug": f"{prefix}-{index:03d}",
                "title": f"{prefix} {index}",
                "stage": "final",
                "checklist": [],
                "last_synced_at": NOW - timedelta(days=days_ago, minutes=index),
                **fields,
            }
            if "youtube_video_id" in values:
                values["youtube_publish_at"] = NOW - timedelta(days=1, minutes=index)
            session.add(VideoProject(**values))
        await session.commit()


@pytest.mark.asyncio
async def test_ninety_days_of_shorts_do_not_push_the_other_videos_off_the_list(
    site: Site,
) -> None:
    await seed_projects(site, 205, "short", format="shorts", shorts_line="lab")
    await seed_projects(site, 3, "tutorial", days_ago=30)
    await seed_projects(site, 2, "episode", days_ago=31, format="drama")
    async with site.session() as session:
        every = await admin_service.list_projects(session)
        assert len(every) == 200 and {item.format for item in every} == {"shorts"}, (
            "asked as before, the list is what it was: the newest two hundred"
        )
        others = await admin_service.list_projects(session, shorts="exclude")
        assert [item.slug for item in others] == [
            "tutorial-000",
            "tutorial-001",
            "tutorial-002",
            "episode-000",
            "episode-001",
        ]
        dramas = await admin_service.list_projects(session, shorts="exclude", video_format="drama")
        assert [item.slug for item in dramas] == ["episode-000", "episode-001"]
        cards = await admin_service.list_projects(session, video_format="shorts", limit=5)
        assert [item.slug for item in cards] == [f"short-{index:03d}" for index in range(5)]
        older = await admin_service.list_projects(
            session, shorts="exclude", before=NOW - timedelta(days=30, minutes=1)
        )
        assert [item.slug for item in older] == ["tutorial-002", "episode-000", "episode-001"]


@pytest.mark.asyncio
async def test_the_shorts_tab_gets_what_is_in_hand_and_the_latest_sixty_public(
    site: Site,
) -> None:
    await seed_projects(
        site, 70, "public", format="shorts", shorts_line="cut", youtube_video_id="a" * 11
    )
    await seed_projects(site, 4, "making", format="shorts", shorts_line="lab")
    await seed_projects(site, 1, "vertical", days_ago=1, format="drama", shorts_line="drama")
    await seed_projects(site, 2, "tutorial")
    await approved_short(site, "in-library")
    async with site.session() as session:
        tab = await admin_service.list_projects(session, shorts="only")
        states = [item.shorts_state for item in tab]
        assert states.count("published") == 60 and len(tab) == 66
        assert {item.slug for item in tab if item.shorts_state == "making"} == {
            "making-000",
            "making-001",
            "making-002",
            "making-003",
            "vertical-000",
        }
        assert all(item.shorts_line for item in tab)
        public = [item for item in tab if item.shorts_state == "published"]
        assert [item.slug for item in public[:2]] == ["public-000", "public-001"]
        assert public[-1].slug == "public-059"
        more = await admin_service.list_projects(
            session, shorts="only", state="published", before=public[-1].youtube_publish_at
        )
        assert [item.slug for item in more] == [f"public-{index:03d}" for index in range(60, 70)]
        library = await admin_service.list_projects(session, shorts="only", state="library")
        assert [item.slug for item in library] == ["in-library"]
        few = await admin_service.list_projects(session, shorts="only", state="making", limit=2)
        assert [item.slug for item in few] == ["making-000", "making-001"]
        dramas = await admin_service.list_projects(session, shorts="only", video_format="drama")
        assert [item.slug for item in dramas] == ["vertical-000"]


# --- the top row --------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_before_the_run_nothing_waits_and_the_library_is_a_count(site: Site) -> None:
    await approved_short(site, "one")
    async with site.session() as session:
        view = await overview.overview(session, NOW)
        assert await overview.owner_needs_count(session, NOW) == 0
    assert (view.autopublish, view.needs, view.needs_count) == ("off", [], 0)
    assert (view.stock.count, view.stock.days, view.stock.wanted_days) == (1, None, 5)
    assert view.campaign.start is None and view.campaign.slots == 0
    assert view.channel.linked is False and view.worker_seen_at is None
    assert view.budget.paid_work_allowed and view.budget.limit_ntd == 3000
    assert view.today == [] and view.tomorrow == [] and view.timezone == TAIPEI


@pytest.mark.asyncio
async def test_the_top_row_lists_what_waits_for_the_owner(site: Site) -> None:
    await approved_short(site, "one", sha="a" * 64)
    await approved_short(site, "two", sha="b" * 64)
    await report_short(site, "failed")
    await submit(site, "failed", "final", {"qa": _qa(ok=False)})
    await report_short(site, "stuck")
    async with site.session() as session:
        stuck = await session.scalar(select(VideoProject).where(VideoProject.slug == "stuck"))
        assert stuck is not None
        stuck.stage = "blocked"
        session.add(
            VideoShortsCost(
                occurred_at=NOW, category="tool", currency="USD", status="unknown", source="manual"
            )
        )
        await session.commit()
    await start(site)
    async with site.session() as session:
        view = await overview.overview(session, NOW)
        count = await overview.owner_needs_count(session, NOW)
    kinds = [need.kind for need in view.needs]
    assert kinds == ["consent", "channel", "worker", "review", "blocked", "budget"]
    assert view.needs[0].detail.startswith("還沒有自動上架授權")
    assert {need.slug for need in view.needs if need.slug} == {"failed", "stuck"}
    assert count == 5, "the review is in the sidebar's count already"
    assert view.autopublish == "off" and not view.budget.paid_work_allowed
    assert [slot.project_slug for slot in view.tomorrow] == ["one"]
    assert view.tomorrow[0].local_time == "19:30" and view.today == []
    assert (view.stock.count, view.stock.days) == (0, 2)
    assert (view.campaign.slots, view.campaign.published) == (120, 0)
    assert view.campaign.last_day == date(2027, 1, 2)


@pytest.mark.asyncio
async def test_a_run_in_good_order_asks_only_for_the_files_before_the_audit(site: Site) -> None:
    await approved_short(site, "one", sha="a" * 64)
    await approved_short(site, "two", sha="b" * 64)
    await start(site)
    await agree(site)
    async with site.session() as session:
        row = await shorts_settings.settings_row(session)
        row.last_tick_at = NOW - timedelta(minutes=4)
        await session.commit()
        view = await overview.overview(session, NOW)
    assert [(need.kind, need.count) for need in view.needs] == [("upload", 2)]
    assert view.autopublish == "on" and view.worker_seen_at == NOW - timedelta(minutes=4)
    await link_channel(site, audited=True)
    async with site.session() as session:
        assert (await overview.overview(session, NOW)).needs == []
        quiet = await overview.overview(session, NOW + timedelta(minutes=20))
        assert [need.kind for need in quiet.needs] == ["worker"]
        assert "24 分鐘" in quiet.needs[0].detail
        late = await overview.overview(session, NOW + timedelta(days=84))
        assert late.autopublish == "expiring"
        assert "consent" in [need.kind for need in late.needs]


@pytest.mark.asyncio
async def test_three_days_of_missed_slots_and_an_empty_library_are_said(site: Site) -> None:
    await link_channel(site, audited=True)
    await start(site)
    await agree(site)
    calendar = await rows(site, VideoShortsSlot, VideoShortsSlot.starts_at)
    now = at(3, 13)
    async with site.session() as session:
        for slot in calendar[:3]:
            row = await session.get(VideoShortsSlot, slot.id)
            assert row is not None
            row.status = "missed"
        settings = await shorts_settings.settings_row(session)
        settings.last_tick_at = now
        await session.commit()
        view = await overview.overview(session, now)
    assert [(need.kind, need.count) for need in view.needs] == [("missed", 3), ("stock", 1)]
    assert (view.campaign.missed, view.stock.days) == (3, 0)
    assert [slot.status for slot in view.today] == ["missed"]


@pytest.mark.asyncio
async def test_the_numbers_are_listed_as_they_were_stored(site: Site) -> None:
    await seed_projects(
        site, 2, "public", format="shorts", shorts_line="lab", youtube_video_id="a" * 11
    )
    await seed_projects(site, 1, "tutorial", youtube_video_id="b" * 11)
    async with site.session() as session:
        for period, views in (("now", 5200), ("d1", 1200), ("d7", 4100)):
            session.add(
                VideoShortsMetric(
                    project_slug="public-000",
                    youtube_video_id="a" * 11,
                    period=period,
                    source="data_api",
                    captured_at=NOW,
                    views=views,
                    likes=views // 100,
                    comments=3,
                    raw={"viewCount": str(views)},
                )
            )
        session.add(
            VideoShortsMetric(
                project_slug="public-000",
                youtube_video_id="c" * 11,
                period="d1",
                source="data_api",
                captured_at=NOW,
                views=9,
            )
        )
        await session.commit()
        view = await overview.metrics_view(session)
        one = await overview.metrics_view(session, limit=1)
    assert [item.slug for item in view.items] == ["public-000", "public-001"]
    first = view.items[0]
    assert [(shot.period, shot.views, shot.likes) for shot in first.snapshots] == [
        ("d1", 1200, 12),
        ("d7", 4100, 41),
        ("now", 5200, 52),
    ], "in the order of the windows, and only of the video the Short names now"
    assert first.snapshots[0].engaged_views is None and first.snapshots[0].source == "data_api"
    assert view.items[1].snapshots == [] and [item.slug for item in one.items] == ["public-000"]
    assert set(first.model_dump()) == {
        "slug",
        "title",
        "line",
        "series",
        "youtube_video_id",
        "published_at",
        "removed_at",
        "snapshots",
    }, "no score, rank or rate of the site's own"


@pytest.mark.asyncio
async def test_one_snapshot_is_kept_for_a_video_s_window_and_source(site: Site) -> None:
    async with site.session() as session:
        for views in (1, 2):
            session.add(
                VideoShortsMetric(
                    project_slug="x",
                    youtube_video_id="a" * 11,
                    period="d1",
                    source="data_api",
                    captured_at=NOW,
                    views=views,
                )
            )
        with pytest.raises(IntegrityError):
            await session.commit()


# --- the routes ---------------------------------------------------------------------------------

READS = ("overview", "slots", "costs", "metrics", "settings")


def _app(user: User | None, site: Site | None = None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.admin_router, prefix="/api/v1")
    app.include_router(admin_api.tool_router, prefix="/api/v1")

    async def session() -> Any:
        if site is None:
            yield AsyncMock()
            return
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
def runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    """The site's runtime settings, with no vendor key and no Azure voice."""
    settings = Settings(azure_speech_voices="")
    monkeypatch.setattr(admin_api, "load_runtime_settings", AsyncMock(return_value=settings))
    monkeypatch.setattr(admin_api, "configured_providers", lambda _runtime: [])


@pytest.mark.asyncio
async def test_every_route_asks_for_its_capability(site: Site, runtime: None) -> None:
    slot, cost = uuid4(), uuid4()
    manage = [
        ("PATCH", f"slots/{slot}", {"action": "skip"}),
        ("POST", "costs", {"category": "tool", "amount": "5"}),
        ("PATCH", f"costs/{cost}", {"amount": "5"}),
        ("DELETE", f"costs/{cost}", None),
        ("POST", "pause", None),
        ("POST", "resume", None),
    ]
    settings = [
        ("PUT", "settings", {"stock_days": 6}),
        ("POST", "campaign/start", {"first_day": "2030-01-01"}),
        ("POST", "autopublish", {"text_sha256": "0" * 64}),
        ("DELETE", "autopublish", None),
    ]
    base = "/api/v1/admin/video-shorts/"

    async def statuses(user: User | None, calls: list[tuple[str, str, Any]]) -> set[int]:
        app = _app(user, site)
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            return {
                (await client.request(method, base + path, json=body)).status_code
                for method, path, body in calls
            }

    reads = [("GET", path, None) for path in READS]
    assert await statuses(_with_roles(), reads + manage + settings) == {403}
    assert await statuses(_with_roles("viewer"), reads) == {200}
    assert await statuses(_with_roles("viewer"), manage + settings) == {403}
    assert await statuses(_with_roles("content"), settings) == {403}
    assert await statuses(_with_roles("operations"), reads + manage) == {403}
    assert 403 not in await statuses(_with_roles("content"), manage)
    assert 403 not in await statuses(_with_roles("operations"), settings)
    listed = {
        (method, route.path)  # type: ignore[attr-defined]
        for route in admin_api.admin_router.routes
        for method in route.methods  # type: ignore[attr-defined]
    }
    assert len(listed) == len(reads + manage + settings), "a new route is added to this test"


@pytest.mark.asyncio
async def test_the_routes_answer_in_the_owner_s_words(site: Site, runtime: None) -> None:
    await link_channel(site)
    app = _app(_with_roles("owner"), site)
    base = "/api/v1/admin/video-shorts/"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        settings = (await client.get(base + "settings")).json()
        assert settings["consent"]["state"] == "none" and settings["voice"]["name"] == "Sulafat"
        saved = await client.put(base + "settings", json={"stock_days": 7, "max_per_day": 3})
        assert saved.status_code == 200 and saved.json()["stock_days"] == 7
        assert saved.json()["lock_hours"] == 24, "what was not sent stays"
        broken = await client.put(base + "settings", json={"max_per_day": 1})
        assert broken.status_code == 422
        assert broken.json()["code"] == "video_shorts_settings_invalid"
        voiceless = await client.put(
            base + "settings", json={"voice": {"provider": "gemini", "name": "Nobody"}}
        )
        assert voiceless.status_code == 422 and "Nobody" in voiceless.json()["detail"]
        keyless = await client.put(base + "settings", json={"enabled": True})
        assert keyless.status_code == 422 and "金鑰" in keyless.json()["detail"]
        unknown = await client.put(base + "settings", json={"autopublish": True})
        assert unknown.status_code == 422, "the consent has its own route"
        past = await client.post(base + "campaign/start", json={"first_day": "2020-01-01"})
        assert (past.status_code, past.json()["code"]) == (422, "video_shorts_campaign_past")
        started = await client.post(base + "campaign/start", json={"first_day": "2031-03-03"})
        assert started.status_code == 200 and started.json()["slots"] == 120
        calendar = (await client.get(base + "slots?from=2031-03-03&to=2031-03-04")).json()
        assert calendar["timezone"] == TAIPEI
        assert [slot["local_date"] for slot in calendar["slots"]] == ["2031-03-03", "2031-03-04"]
        assert len((await client.get(base + "slots")).json()["slots"]) == 120
        slot = calendar["slots"][0]["id"]
        skipped = await client.patch(base + f"slots/{slot}", json={"action": "skip"})
        assert skipped.status_code == 200 and skipped.json()["status"] == "skipped"
        stale = await client.post(base + "autopublish", json={"text_sha256": "0" * 64})
        assert (stale.status_code, stale.json()["code"]) == (409, "video_shorts_consent_stale")
        offer = (await client.get(base + "settings")).json()["consent"]["offer"]
        agreed = await client.post(base + "autopublish", json={"text_sha256": offer["text_sha256"]})
        assert agreed.status_code == 200 and agreed.json()["autopublish"] is True
        assert (await client.post(base + "pause")).json()["paused_at"] is not None
        top = (await client.get(base + "overview")).json()
        assert top["autopublish"] == "paused" and top["campaign"]["slots"] == 119
        assert (await client.post(base + "resume")).json()["paused_at"] is None
        withdrawn = await client.delete(base + "autopublish")
        assert withdrawn.status_code == 200 and withdrawn.json()["consent"]["state"] == "none"
        added = await client.post(
            base + "costs", json={"category": "tool", "amount": "120", "note": "字型授權"}
        )
        assert added.status_code == 201 and added.json()["amount_ntd"] == 120.0
        line = added.json()["id"]
        fixed = await client.patch(base + f"costs/{line}", json={"amount": "150.5"})
        assert fixed.status_code == 200 and fixed.json()["amount_ntd"] == 150.5
        ledger = (await client.get(base + "costs")).json()
        assert [item["id"] for item in ledger["items"]] == [line]
        assert ledger["budget"]["spent_ntd"] == 150.5
        assert (await client.delete(base + f"costs/{line}")).status_code == 204
        gone = await client.delete(base + f"costs/{line}")
        assert (gone.status_code, gone.json()["code"]) == (404, "video_shorts_cost_not_found")
        assert (await client.get(base + "metrics")).json() == {"items": []}


@pytest.mark.asyncio
async def test_the_tool_reads_the_shorts_settings_with_its_token(site: Site) -> None:
    app = _app(None, site)
    path = "/api/v1/video/automation/shorts/settings"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        assert (await client.get(path)).status_code == 401
        app.dependency_overrides[speech_api.video_tool] = lambda: site.token
        answer = await client.get(path)
    assert answer.status_code == 200
    body = answer.json()
    assert (body["voice"]["name"], body["seconds_min"], body["seconds_max"]) == ("Sulafat", 25, 55)
    assert (body["paused"], body["campaign_start"], body["locales"]) == (False, None, [])
    assert "consent" not in body and "autopublish" not in body


@pytest.mark.asyncio
async def test_the_worker_s_list_takes_the_same_filter(monkeypatch: pytest.MonkeyPatch) -> None:
    listed = AsyncMock(return_value=[])
    monkeypatch.setattr(automation_api, "list_projects", listed)
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(automation_api.tool_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[speech_api.video_tool] = lambda: VideoToolToken(
        id=uuid4(), name="worker", token_hash="h", token_prefix="mkv_w"
    )
    url = "/api/v1/video/automation/videos"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        plain = await client.get(url)
        others = await client.get(url, params={"shorts": "exclude"})
        mine = await client.get(url, params={"shorts": "only", "state": "library", "limit": 5})
        stateless = await client.get(url, params={"state": "library"})
    assert [plain.status_code, others.status_code, mine.status_code] == [200, 200, 200]
    calls = [call.kwargs for call in listed.await_args_list]
    assert calls[0] == {
        "video_format": None,
        "shorts": None,
        "state": None,
        "limit": None,
        "before": None,
    }
    assert calls[1]["shorts"] == "exclude"
    assert (calls[2]["shorts"], calls[2]["state"], calls[2]["limit"]) == ("only", "library", 5)
    assert stateless.status_code == 422
    assert stateless.json()["code"] == "video_shorts_state_needs_only"
