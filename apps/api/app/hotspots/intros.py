"""First-party introduction paragraphs: one per hotspot per locale.

A hotspot's "introduction" used to mean a link out to somebody else's article or
video. This is the other kind: a short paragraph Mokaair wrote itself, saying what
the place is and when to go. Drafts arrive from the AI job or from an administrator
typing one, and only an ``approved`` row is ever shown to a reader.

The one rule worth stating twice: a draft never silently replaces an approved
paragraph. Someone read that text and said yes to it; a later generation run that
quietly overwrote it would undo a review nobody asked to redo.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any, Literal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.i18n import LOCALES, Locale
from app.models import HotspotIntro, TravelHotspot
from app.problems import AppError

# Long enough for a paragraph in any of the five locales, short enough that a
# runaway model cannot fill a card with an essay.
INTRO_BODY_MAX_CHARS = 1500

# The only cross-locale fallback: the two Chinese writings say the same thing, so a
# reader of one can be shown the other. An English reader is never shown Japanese.
INTRO_FALLBACK: dict[str, tuple[Locale, ...]] = {
    "zh-CN": ("zh-TW",),
    "zh-TW": ("zh-CN",),
}

PUBLIC_INTRO_STATUS = "approved"
IntroSource = Literal["ai", "manual"]


def clean_intro_body(body: str) -> str:
    text = body.strip()
    if not text:
        raise AppError(422, "hotspot_intro_body_required", "介紹內容不可以是空的")
    if len(text) > INTRO_BODY_MAX_CHARS:
        raise AppError(
            422,
            "hotspot_intro_body_required",
            f"介紹內容最多 {INTRO_BODY_MAX_CHARS} 個字",
        )
    return text


async def upsert_hotspot_intro_draft(
    session: AsyncSession,
    *,
    hotspot_id: UUID,
    locale: Locale,
    body: str,
    source: IntroSource = "ai",
    ai_provider: str | None = None,
    ai_model: str | None = None,
    generated_at: datetime | None = None,
    metadata: Mapping[str, Any] | None = None,
    replace_approved: bool = False,
) -> tuple[HotspotIntro, bool]:
    """Store a draft for one hotspot and locale. Returns ``(row, written)``.

    This is the seam the AI generation job writes through.

    - Nothing stored yet: insert as ``pending``.
    - A ``pending``, ``rejected`` or ``disabled`` row: replaced and moved back to
      ``pending``, because a fresh draft deserves a fresh look.
    - An ``approved`` row: left exactly as it is and returned with
      ``written=False``, unless ``replace_approved`` says otherwise — and even then
      the text that was approved is kept in ``metadata_json["previous_body"]`` so a
      reviewer can put it back.
    """

    text = clean_intro_body(body)
    row = await session.scalar(
        select(HotspotIntro).where(
            HotspotIntro.hotspot_id == hotspot_id, HotspotIntro.locale == locale
        )
    )
    stamped = generated_at or datetime.now(UTC)
    extra = dict(metadata or {})
    if row is None:
        row = HotspotIntro(
            hotspot_id=hotspot_id,
            locale=locale,
            body=text,
            review_status="pending",
            source=source,
            ai_provider=ai_provider,
            ai_model=ai_model,
            generated_at=stamped if source == "ai" else None,
            metadata_json=extra,
        )
        session.add(row)
        await session.flush()
        return row, True
    if row.review_status == PUBLIC_INTRO_STATUS and not replace_approved:
        return row, False
    if row.review_status == PUBLIC_INTRO_STATUS:
        extra["previous_body"] = row.body
    row.body = text
    row.review_status = "pending"
    row.review_reason = None
    row.source = source
    row.ai_provider = ai_provider
    row.ai_model = ai_model
    row.generated_at = stamped if source == "ai" else None
    row.reviewed_at = None
    row.reviewed_by_user_id = None
    row.metadata_json = {**row.metadata_json, **extra}
    await session.flush()
    return row, True


def intro_payload(row: HotspotIntro) -> dict[str, Any]:
    return {"body": row.body, "locale": row.locale, "source": row.source}


async def load_public_intros(
    session: AsyncSession, hotspot_ids: Sequence[UUID], locale: Locale
) -> dict[UUID, dict[str, Any]]:
    """Approved paragraphs for a page of hotspots, in the reader's locale.

    Only zh-CN and zh-TW stand in for each other; every other locale either has an
    approved paragraph or gets nothing.
    """

    if not hotspot_ids:
        return {}
    wanted: tuple[Locale, ...] = (locale, *INTRO_FALLBACK.get(locale, ()))
    rows = (
        await session.scalars(
            select(HotspotIntro).where(
                HotspotIntro.hotspot_id.in_(hotspot_ids),
                HotspotIntro.locale.in_(wanted),
                HotspotIntro.review_status == PUBLIC_INTRO_STATUS,
            )
        )
    ).all()
    by_hotspot: dict[UUID, dict[str, HotspotIntro]] = defaultdict(dict)
    for row in rows:
        by_hotspot[row.hotspot_id][row.locale] = row
    intros: dict[UUID, dict[str, Any]] = {}
    for hotspot_id, per_locale in by_hotspot.items():
        for candidate in wanted:
            if candidate in per_locale:
                intros[hotspot_id] = intro_payload(per_locale[candidate])
                break
    return intros


async def intro_coverage(session: AsyncSession, hotspot_id: UUID) -> list[dict[str, Any]]:
    """One entry per site locale, so an editor can see what is missing."""

    rows = {
        row.locale: row
        for row in (
            await session.scalars(select(HotspotIntro).where(HotspotIntro.hotspot_id == hotspot_id))
        ).all()
    }
    coverage: list[dict[str, Any]] = []
    for locale in LOCALES:
        row = rows.get(locale)
        coverage.append(
            {
                "locale": locale,
                "id": str(row.id) if row else None,
                "status": row.review_status if row else None,
                "body": row.body if row else None,
                "source": row.source if row else None,
                "updated_at": row.updated_at.isoformat() if row else None,
            }
        )
    return coverage


async def intro_targets(
    session: AsyncSession,
    *,
    locales: Sequence[Locale],
    limit: int,
    destination_id: str | None = None,
    category: str | None = None,
    force: bool = False,
) -> list[tuple[TravelHotspot, list[Locale]]]:
    """Public hotspots that still need a draft, with the locales each one is missing.

    The generation job asks this rather than working from a hotspot list, so a run
    that is interrupted and restarted does not re-draft what already landed. With
    ``force`` every requested locale counts as missing.
    """

    # Imported here, not at module scope: service imports this module for the
    # ranking payload, and a top-level import back would close the cycle.
    from app.hotspots.service import PUBLIC_REVIEW_STATUSES

    wanted = [locale for locale in locales if locale in LOCALES]
    if not wanted or limit <= 0:
        return []
    query = select(TravelHotspot).where(
        TravelHotspot.is_active.is_(True),
        TravelHotspot.review_status.in_(PUBLIC_REVIEW_STATUSES),
    )
    if destination_id:
        query = query.where(TravelHotspot.destination_id == destination_id)
    if category:
        query = query.where(TravelHotspot.category == category)
    hotspots = list((await session.scalars(query.order_by(TravelHotspot.name))).all())
    if not hotspots:
        return []
    settled: dict[UUID, set[str]] = defaultdict(set)
    if not force:
        for hotspot_id, locale in (
            await session.execute(
                select(HotspotIntro.hotspot_id, HotspotIntro.locale).where(
                    HotspotIntro.hotspot_id.in_([item.id for item in hotspots]),
                    HotspotIntro.review_status.in_(("pending", PUBLIC_INTRO_STATUS)),
                )
            )
        ).all():
            settled[hotspot_id].add(locale)
    targets: list[tuple[TravelHotspot, list[Locale]]] = []
    for hotspot in hotspots:
        missing = [locale for locale in wanted if locale not in settled[hotspot.id]]
        if missing:
            targets.append((hotspot, missing))
        if len(targets) >= limit:
            break
    return targets


async def intro_status_counts(session: AsyncSession) -> dict[str, int]:
    """How many drafts sit in each state, for the review queue's header."""

    rows = (
        await session.execute(
            select(HotspotIntro.review_status, func.count(HotspotIntro.id)).group_by(
                HotspotIntro.review_status
            )
        )
    ).all()
    return {str(status): int(count) for status, count in rows}
