"""What the semantic duplicate check compares a candidate with, and a person's answer to it.

The pipeline sends these titles to Jev; the admin detail shows the closest few so an
editor can answer an uncertain check. Both import it from here because the pipeline
already imports the service module.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from difflib import SequenceMatcher
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.guides.models import GuideArticle, GuideSearchEntry
from app.news_automation.ai import MAX_DUPLICATE_TITLES
from app.news_automation.models import NewsAssessment, NewsCandidate

# Published news the duplicate check compares against.
DUPLICATE_WINDOW = timedelta(days=30)
# Provider of the duplicate assessment an editor records with "not a duplicate".
HUMAN_PROVIDER = "human"
# The hold for a check Jev could not settle; the only one an editor can answer.
DUPLICATE_UNCERTAIN = "news_duplicate_uncertain"


async def known_titles(session: AsyncSession, candidate: NewsCandidate) -> list[str]:
    """Recent news titles of the same vertical: published articles first, including the
    ones written by hand, then other automation candidates."""

    cutoff = datetime.now(UTC).date() - DUPLICATE_WINDOW
    published: dict[UUID, str] = {}
    rows = await session.execute(
        select(GuideSearchEntry.article_id, GuideSearchEntry.locale, GuideSearchEntry.title)
        .join(GuideArticle, GuideArticle.id == GuideSearchEntry.article_id)
        .where(
            GuideArticle.slug.like(f"{candidate.vertical}-news-%"),
            GuideArticle.is_active.is_(True),
            GuideArticle.news_date >= cutoff,
            GuideSearchEntry.locale.in_(("en", "zh-TW")),
        )
        .order_by(GuideArticle.news_date.desc(), GuideArticle.id)
        .limit(80)
    )
    for article_id, locale, title in rows:
        if article_id == candidate.guide_article_id:
            continue
        # Sources are mostly English, so the English title is the closer comparison.
        if locale == "en" or article_id not in published:
            published[article_id] = title
    candidates = await session.scalars(
        select(NewsCandidate.source_title)
        .where(
            NewsCandidate.id != candidate.id,
            NewsCandidate.vertical == candidate.vertical,
            NewsCandidate.status.in_(("manual_review", "shadow_review", "published")),
        )
        .order_by(NewsCandidate.created_at.desc())
        .limit(30)
    )
    titles = list(dict.fromkeys([*list(published.values())[:40], *candidates]))
    return titles[:MAX_DUPLICATE_TITLES]


def closest_titles(title: str, titles: list[str], limit: int = 5) -> list[str]:
    """The titles most alike ``title`` by characters, closest first.

    Jev only answers "duplicate or not", never which article it matched, so this is the
    editor's shortlist for checking an uncertain answer by eye.
    """

    wanted = title.casefold()
    ranked = sorted(
        titles,
        key=lambda other: SequenceMatcher(None, wanted, other.casefold()).ratio(),
        reverse=True,
    )
    return ranked[:limit]


async def similar_titles(
    session: AsyncSession, candidate: NewsCandidate, limit: int = 5
) -> list[str]:
    return closest_titles(candidate.source_title, await known_titles(session, candidate), limit)


async def cleared_by_editor(session: AsyncSession, candidate: NewsCandidate) -> bool:
    """An editor answered "not a duplicate" for this candidate's current evidence."""

    return (
        await session.scalar(
            select(NewsAssessment.id)
            .where(
                NewsAssessment.candidate_id == candidate.id,
                NewsAssessment.assessment_type == "duplicate",
                NewsAssessment.provider == HUMAN_PROVIDER,
                NewsAssessment.verdict == "pass",
                NewsAssessment.evidence_hash == candidate.evidence_hash,
            )
            .limit(1)
        )
    ) is not None
