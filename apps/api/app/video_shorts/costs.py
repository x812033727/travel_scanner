"""The ledger of what Shorts cost (docs/videos/SHORTS.md §花費與預算).

Three kinds of line: what the tool reported with an approved final cut (narration seconds,
model calls), what the owner enters by hand, and reservations a paid job makes before it
runs. A reservation and its outcome are one row, found by its key; a report sent twice for
the same cut is entered once.

``record_usage`` and ``record_media`` write on the caller's session and leave the commit to
it: what is rolled back should not be counted. They never flush the caller's pending rows
(``no_autoflush``), and they open no savepoint.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, cast
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.crawlers.fx import FxRateError, FxRateProvider
from app.infra import get_redis
from app.models import AdminAuditLog, User
from app.video_automation.usage import SUBSCRIPTION_PROVIDERS
from app.video_media.meter import spend_by_slug
from app.video_shorts import rules
from app.video_shorts.errors import ShortsRefused
from app.video_shorts.models import VideoShortsCost, VideoShortsSettings
from app.video_shorts.schemas import (
    BudgetOut,
    CostIn,
    CostOut,
    CostPatch,
    CostsOut,
    PeriodTotal,
    UsageReport,
)
from app.video_speech.gemini import DEFAULT_GEMINI_TTS_MODEL

# Gemini's price list as read on 2026-09-28 (ai.google.dev/gemini-api/docs/pricing): speech
# comes back as 25 audio tokens a second, at USD 9 (Flash) and 6 (Flash-Lite) per million
# through 2026, and twice that from 2027-01-01. US dollars per second of audio, by the day
# the price starts. The text sent in is a hundredth of it and is left out.
NARRATION_USD_PER_SECOND: dict[str, tuple[tuple[date, Decimal], ...]] = {
    "gemini-3.8-flash-tts": (
        (date(2026, 1, 1), Decimal("0.000225")),
        (date(2027, 1, 1), Decimal("0.00045")),
    ),
    "gemini-3.8-flash-lite-tts": (
        (date(2026, 1, 1), Decimal("0.00015")),
        (date(2027, 1, 1), Decimal("0.0003")),
    ),
}
# A voice that runs on the machine that made the Short costs nothing.
FREE_NARRATION = frozenset({"windows", "local", "files"})
# Used only when the rate service does not answer and the ledger holds no earlier rate; the
# line says so in its note.
FALLBACK_NTD = {"USD": Decimal("32")}
CENT = Decimal("0.01")
LIST_LIMIT = 200


def narration_price(model: str, day: date) -> Decimal | None:
    """US dollars per second of narration on ``day``, or None for a model with no listed
    price."""
    prices = NARRATION_USD_PER_SECOND.get(model)
    if prices is None:
        return None
    started = [price for starts, price in prices if starts <= day]
    return started[-1] if started else prices[0][1]


def to_ntd(amount: Decimal, rate: Decimal) -> Decimal:
    return (amount * rate).quantize(CENT, rounding=ROUND_HALF_UP)


async def lookup_rate(currency: str) -> Decimal | None:
    """Today's rate to New Taiwan dollars, or None when the rate service does not answer."""
    if currency == "TWD":
        return Decimal(1)
    try:
        snapshot = await FxRateProvider(get_settings(), get_redis()).rate(currency, "TWD")
    except FxRateError:
        return None
    return snapshot.rate


async def rate_for(session: AsyncSession, currency: str) -> tuple[Decimal | None, str | None]:
    """The rate a line is converted at, and a note when it is not today's: the ledger's last
    rate for the currency, or the fixed fallback."""
    rate = await lookup_rate(currency)
    if rate is not None:
        return rate, None
    with session.no_autoflush:
        earlier = await session.scalar(
            select(VideoShortsCost.fx_rate)
            .where(VideoShortsCost.currency == currency, VideoShortsCost.fx_rate.is_not(None))
            .order_by(VideoShortsCost.occurred_at.desc())
            .limit(1)
        )
    if earlier is not None:
        return Decimal(earlier), "匯率服務沒有回應，用帳上最近一次的匯率"
    fallback = FALLBACK_NTD.get(currency)
    if fallback is not None:
        return fallback, f"匯率服務沒有回應，用備用匯率 {fallback}"
    return None, None


def usage_key(slug: str, sha: str, category: str) -> str:
    return f"usage:{slug}:{sha[:16]}:{category}"


def media_key(slug: str) -> str:
    return f"media:{slug}"


async def _by_keys(session: AsyncSession, keys: Sequence[str]) -> dict[str, VideoShortsCost]:
    """The lines that carry these keys: the stored ones, and the ones this session has added
    and not written yet, which a query that does not flush cannot see."""
    wanted = set(keys)
    with session.no_autoflush:
        rows = await session.scalars(
            select(VideoShortsCost).where(VideoShortsCost.dedupe_key.in_(list(keys)))
        )
        found = {str(row.dedupe_key): row for row in rows}
    for pending in session.new:
        if isinstance(pending, VideoShortsCost) and pending.dedupe_key in wanted:
            found[str(pending.dedupe_key)] = pending
    return found


def _line(
    *,
    slug: str,
    category: str,
    key: str,
    now: datetime,
    amount: Decimal | None,
    currency: str,
    rate: Decimal | None,
    units: dict[str, Any],
    note: str | None,
) -> VideoShortsCost:
    known = amount is not None and rate is not None
    return VideoShortsCost(
        occurred_at=now,
        project_slug=slug,
        category=category,
        amount=amount if known else None,
        currency=currency,
        fx_rate=rate if known else None,
        amount_ntd=to_ntd(cast(Decimal, amount), cast(Decimal, rate)) if known else None,
        status="confirmed" if known else "unknown",
        source="auto",
        units=units,
        note=note,
        dedupe_key=key,
    )


async def record_usage(
    session: AsyncSession,
    slug: str,
    payload: dict[str, Any],
    sha: str,
    now: datetime | None = None,
) -> list[VideoShortsCost]:
    """Enter what an approved final cut's ``payload.usage`` reports, once per cut.

    Narration is priced from the vendor's list; a voice the list does not know is entered
    as unknown rather than as nothing. Model calls on the subscription accounts cost nothing
    more and are entered at zero with their counts; calls a vendor bills are unknown until
    the owner enters the amount.
    """
    try:
        report = UsageReport.model_validate(payload.get("usage"))
    except ValidationError:
        return []
    moment = now or datetime.now(UTC)
    keys = {
        category: usage_key(slug, sha, category) for category in ("narration", "models", "checks")
    }
    entered = await _by_keys(session, list(keys.values()))
    lines: list[VideoShortsCost] = []
    narration = report.narration
    if (
        narration is not None
        and (narration.seconds or narration.characters)
        and keys["narration"] not in entered
    ):
        units = narration.model_dump(exclude_none=True)
        provider = (narration.provider or "gemini").lower()
        if provider in FREE_NARRATION:
            lines.append(
                _line(
                    slug=slug,
                    category="narration",
                    key=keys["narration"],
                    now=moment,
                    amount=Decimal(0),
                    currency="TWD",
                    rate=Decimal(1),
                    units=units,
                    note="這台電腦上的語音，沒有花費",
                )
            )
        else:
            price = (
                narration_price(narration.model or DEFAULT_GEMINI_TTS_MODEL, moment.date())
                if provider == "gemini"
                else None
            )
            rate, rate_note = await rate_for(session, "USD") if price is not None else (None, None)
            amount = (
                (Decimal(str(narration.seconds)) * price).quantize(Decimal("0.0001"))
                if price is not None
                else None
            )
            note = (
                f"旁白 {narration.seconds:g} 秒，照 Gemini 的價目估算"
                if price is not None
                else f"{provider} 的旁白沒有列在價目裡，請補上金額"
            )
            lines.append(
                _line(
                    slug=slug,
                    category="narration",
                    key=keys["narration"],
                    now=moment,
                    amount=amount,
                    currency="USD",
                    rate=rate,
                    units=units,
                    note="；".join(part for part in (note, rate_note) if part),
                )
            )
    if report.stages and keys["models"] not in entered:
        billed = sorted(
            stage
            for stage, usage in report.stages.items()
            if usage.calls and (usage.provider or "claude_code") not in SUBSCRIPTION_PROVIDERS
        )
        units = {
            stage: usage.model_dump(exclude_none=True) for stage, usage in report.stages.items()
        }
        lines.append(
            _line(
                slug=slug,
                category="models",
                key=keys["models"],
                now=moment,
                amount=None if billed else Decimal(0),
                currency="TWD",
                rate=None if billed else Decimal(1),
                units=units,
                note=(
                    f"{'、'.join(billed)} 走的是計費的 API，請補上金額"
                    if billed
                    else "模型呼叫走訂閱帳號，不算新增花費"
                ),
            )
        )
    if report.checks and keys["checks"] not in entered:
        lines.append(
            _line(
                slug=slug,
                category="checks",
                key=keys["checks"],
                now=moment,
                amount=Decimal(0),
                currency="TWD",
                rate=Decimal(1),
                units=dict(report.checks),
                note="旁白檢查與政策判斷的次數；算在全站共用的額度裡",
            )
        )
    for line in lines:
        session.add(line)
    return lines


async def record_media(
    session: AsyncSession, slug: str, now: datetime | None = None
) -> VideoShortsCost | None:
    """Copy what the media jobs of this Short have cost so far (images, clips, music) into
    its one ledger line, updating the line when more was generated since."""
    with session.no_autoflush:
        spend = (await spend_by_slug(session, [slug])).get(slug)
    if spend is None or spend.usd <= 0:
        return None
    moment = now or datetime.now(UTC)
    amount = Decimal(str(spend.usd)).quantize(Decimal("0.0001"))
    key = media_key(slug)
    line = (await _by_keys(session, [key])).get(key)
    if line is not None and line.amount == amount and line.status == "confirmed":
        return line
    rate, rate_note = await rate_for(session, "USD")
    units = {"clip_seconds": spend.clip_seconds}
    note = "；".join(part for part in ("圖片、片段與音樂，抄自媒體工作的紀錄", rate_note) if part)
    if line is None:
        line = _line(
            slug=slug,
            category="media",
            key=key,
            now=moment,
            amount=amount,
            currency="USD",
            rate=rate,
            units=units,
            note=note,
        )
        session.add(line)
        return line
    known = rate is not None
    line.amount = amount if known else None
    line.fx_rate = rate
    line.amount_ntd = to_ntd(amount, cast(Decimal, rate)) if known else None
    line.status = "confirmed" if known else "unknown"
    line.units = units
    line.note = note
    return line


# --- reservations -------------------------------------------------------------------------------


async def reserve(
    session: AsyncSession,
    *,
    key: str,
    slug: str | None,
    category: str,
    amount: Decimal,
    currency: str = "USD",
    note: str | None = None,
    now: datetime | None = None,
) -> VideoShortsCost:
    """Set an amount aside before a paid job runs; asking again with the same key returns
    the line that is there."""
    line = (await _by_keys(session, [key])).get(key)
    if line is not None:
        return line
    rate, rate_note = await rate_for(session, currency)
    if rate is None:
        raise ShortsRefused(
            502, "video_shorts_rate_unavailable", f"讀不到 {currency} 的匯率，這筆先不預留"
        )
    line = VideoShortsCost(
        occurred_at=now or datetime.now(UTC),
        project_slug=slug,
        category=category,
        amount=amount,
        currency=currency,
        fx_rate=rate,
        amount_ntd=to_ntd(amount, rate),
        status="reserved",
        source="auto",
        note="；".join(part for part in (note, rate_note) if part) or None,
        dedupe_key=key,
    )
    session.add(line)
    return line


async def confirm(
    session: AsyncSession, key: str, amount: Decimal | None = None
) -> VideoShortsCost | None:
    """The job ran: its reservation becomes the confirmed line, with the amount it came to
    when that differs. The same row, so nothing is counted twice."""
    line = (await _by_keys(session, [key])).get(key)
    if line is None:
        return None
    if amount is not None and line.fx_rate is not None:
        line.amount = amount
        line.amount_ntd = to_ntd(amount, Decimal(line.fx_rate))
    line.status = "confirmed"
    return line


async def release(session: AsyncSession, key: str) -> bool:
    """The job failed before it cost anything: its reservation is removed."""
    line = (await _by_keys(session, [key])).get(key)
    if line is None or line.status != "reserved":
        return False
    await session.delete(line)
    return True


# --- the owner's lines --------------------------------------------------------------------------


def cost_out(line: VideoShortsCost) -> CostOut:
    return CostOut(
        id=line.id,
        occurred_at=line.occurred_at,
        project_slug=line.project_slug,
        category=line.category,
        amount=float(line.amount) if line.amount is not None else None,
        currency=line.currency,
        fx_rate=float(line.fx_rate) if line.fx_rate is not None else None,
        amount_ntd=float(line.amount_ntd) if line.amount_ntd is not None else None,
        status=cast(Any, line.status),
        source=cast(Any, line.source),
        units=line.units,
        note=line.note,
        created_at=line.created_at,
    )


async def _priced(
    session: AsyncSession, amount: Decimal | None, currency: str, given: Decimal | None
) -> tuple[Decimal | None, Decimal | None, str | None]:
    """The rate and the New Taiwan dollar amount of an owner's line."""
    if amount is None:
        return None, None, None
    if given is not None:
        return given, to_ntd(amount, given), None
    rate, note = await rate_for(session, currency)
    if rate is None:
        raise ShortsRefused(
            422,
            "video_shorts_rate_unavailable",
            f"讀不到 {currency} 的匯率，請自己填匯率（一單位換多少新台幣）",
        )
    return rate, to_ntd(amount, rate), note


async def add_manual(
    session: AsyncSession, actor: User, payload: CostIn, now: datetime | None = None
) -> CostOut:
    rate, amount_ntd, rate_note = await _priced(
        session, payload.amount, payload.currency, payload.fx_rate
    )
    line = VideoShortsCost(
        occurred_at=payload.occurred_at or now or datetime.now(UTC),
        project_slug=payload.project_slug,
        category=payload.category,
        amount=payload.amount,
        currency=payload.currency,
        fx_rate=rate,
        amount_ntd=amount_ntd,
        status=payload.status,
        source="manual",
        note="；".join(part for part in (payload.note, rate_note) if part) or None,
        created_by_user_id=actor.id,
    )
    session.add(line)
    await session.flush()
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_shorts_cost_added",
            target=f"video_shorts_cost:{line.id}",
            metadata_json={
                "category": line.category,
                "status": line.status,
                "currency": line.currency,
                "amount": str(line.amount) if line.amount is not None else None,
                "slug": line.project_slug,
            },
        )
    )
    await session.commit()
    return cost_out(line)


async def _line_for_update(session: AsyncSession, cost_id: UUID) -> VideoShortsCost:
    line = await session.scalar(
        select(VideoShortsCost).where(VideoShortsCost.id == cost_id).with_for_update()
    )
    if line is None:
        raise ShortsRefused(404, "video_shorts_cost_not_found", "找不到這一筆花費")
    return line


async def update_cost(
    session: AsyncSession, actor: User, cost_id: UUID, payload: CostPatch
) -> CostOut:
    """Correct a line: an unknown one gets its amount, a mistyped one its right figure.
    A reservation is the job's to settle and is left alone."""
    line = await _line_for_update(session, cost_id)
    if line.status == "reserved":
        raise ShortsRefused(
            409, "video_shorts_cost_reserved", "這一筆是預留的，工作做完會自己轉成確認的金額"
        )
    sent = payload.model_dump(exclude_unset=True)
    status = sent.get("status") or ("confirmed" if sent.get("amount") is not None else line.status)
    amount = sent["amount"] if "amount" in sent else line.amount
    if status == "unknown":
        amount = None
    elif amount is None:
        raise ShortsRefused(422, "video_shorts_cost_needs_amount", "確認的花費要有金額")
    currency = sent.get("currency") or line.currency
    given = sent.get("fx_rate")
    if given is None and currency == line.currency and line.fx_rate is not None:
        given = Decimal(line.fx_rate)
    rate, amount_ntd, rate_note = await _priced(session, amount, currency, given)
    line.status = status
    line.amount = amount
    line.currency = currency
    line.fx_rate = rate
    line.amount_ntd = amount_ntd
    if sent.get("category"):
        line.category = sent["category"]
    if sent.get("occurred_at"):
        line.occurred_at = sent["occurred_at"]
    if "note" in sent or rate_note:
        line.note = "；".join(part for part in (sent.get("note") or line.note, rate_note) if part)
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_shorts_cost_updated",
            target=f"video_shorts_cost:{line.id}",
            metadata_json={
                "changed": sorted(sent),
                "status": line.status,
                "amount": str(line.amount) if line.amount is not None else None,
            },
        )
    )
    await session.commit()
    return cost_out(line)


async def delete_cost(session: AsyncSession, actor: User, cost_id: UUID) -> None:
    """Take out a line the owner entered by mistake; what the site entered itself stays."""
    line = await _line_for_update(session, cost_id)
    if line.source != "manual":
        raise ShortsRefused(
            409, "video_shorts_cost_automatic", "自動記的帳不能刪；金額不對的話改它的金額"
        )
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id,
            action="video_shorts_cost_deleted",
            target=f"video_shorts_cost:{line.id}",
            metadata_json={
                "category": line.category,
                "amount": str(line.amount) if line.amount is not None else None,
                "currency": line.currency,
            },
        )
    )
    await session.delete(line)
    await session.commit()


# --- reading ------------------------------------------------------------------------------------


def _facts(lines: Sequence[VideoShortsCost]) -> list[rules.CostFacts]:
    return [
        rules.CostFacts(
            occurred_at=line.occurred_at,
            status=line.status,
            amount_ntd=Decimal(line.amount_ntd) if line.amount_ntd is not None else None,
        )
        for line in lines
    ]


def budget_out(state: rules.BudgetState, row: VideoShortsSettings) -> BudgetOut:
    return BudgetOut(
        period_start=state.window.period_start,
        period_end=state.window.period_end,
        spent_ntd=float(state.spent),
        reserved_ntd=float(state.reserved),
        unknown=state.unknown,
        limit_ntd=row.budget_ntd_30d,
        soft_ntd=row.budget_soft_ntd,
        total_start=state.window.total_start,
        total_spent_ntd=float(state.total_spent),
        total_limit_ntd=row.budget_total_ntd,
        paid_work_allowed=state.paid_work_allowed,
        reason=state.reason,
    )


async def budget(
    session: AsyncSession, row: VideoShortsSettings, now: datetime | None = None
) -> rules.BudgetState:
    """Where the spending stands: what the top row shows and what a paid job asks first."""
    moment = now or datetime.now(UTC)
    window = rules.budget_window(moment, row.campaign_start, row.timezone)
    lines = list(
        await session.scalars(
            select(VideoShortsCost).where(VideoShortsCost.occurred_at >= window.total_start)
        )
    )
    return rules.budget_state(
        _facts(lines),
        window,
        limit=row.budget_ntd_30d,
        soft=row.budget_soft_ntd,
        total_limit=row.budget_total_ntd,
    )


def period_totals(
    lines: Sequence[VideoShortsCost], window: rules.BudgetWindow
) -> list[PeriodTotal]:
    """The run's three thirty-day blocks, each with its own sums, from the run's start."""
    period = timedelta(days=rules.PERIOD_DAYS)
    totals: list[PeriodTotal] = []
    for index in range(rules.TOTAL_DAYS // rules.PERIOD_DAYS):
        start = window.total_start + index * period
        end = start + period
        inside = [line for line in lines if start <= line.occurred_at < end]
        totals.append(
            PeriodTotal(
                start=start,
                end=end,
                spent_ntd=float(
                    sum(
                        (
                            Decimal(line.amount_ntd or 0)
                            for line in inside
                            if line.status == "confirmed"
                        ),
                        Decimal(0),
                    )
                ),
                reserved_ntd=float(
                    sum(
                        (
                            Decimal(line.amount_ntd or 0)
                            for line in inside
                            if line.status == "reserved"
                        ),
                        Decimal(0),
                    )
                ),
                unknown=sum(1 for line in inside if line.status == "unknown"),
                lines=len(inside),
            )
        )
    return totals


async def costs_view(
    session: AsyncSession,
    row: VideoShortsSettings,
    *,
    limit: int = LIST_LIMIT,
    before: datetime | None = None,
    now: datetime | None = None,
) -> CostsOut:
    moment = now or datetime.now(UTC)
    window = rules.budget_window(moment, row.campaign_start, row.timezone)
    statement = select(VideoShortsCost)
    if before is not None:
        statement = statement.where(VideoShortsCost.occurred_at < before)
    listed = list(
        await session.scalars(
            statement.order_by(
                VideoShortsCost.occurred_at.desc(), VideoShortsCost.created_at.desc()
            ).limit(limit)
        )
    )
    counted = list(
        await session.scalars(
            select(VideoShortsCost).where(VideoShortsCost.occurred_at >= window.total_start)
        )
    )
    state = rules.budget_state(
        _facts(counted),
        window,
        limit=row.budget_ntd_30d,
        soft=row.budget_soft_ntd,
        total_limit=row.budget_total_ntd,
    )
    return CostsOut(
        items=[cost_out(line) for line in listed],
        budget=budget_out(state, row),
        periods=period_totals(counted, window),
    )
