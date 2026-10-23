"""What the semantic duplicate check compares a candidate with, and a person's answer to it.

The pipeline sends these titles to Jev; the admin detail shows the closest few so an
editor can answer an uncertain check, and the review judge is given the closest ones
when it answers in the owner's place. All import it from here because the pipeline
already imports the service module.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from difflib import SequenceMatcher
from uuid import UUID

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.guides.models import GuideArticle, GuideSearchEntry
from app.news_automation.ai import MAX_DUPLICATE_TITLES
from app.news_automation.models import VERTICALS, NewsAssessment, NewsCandidate

# Published news the duplicate check compares against.
DUPLICATE_WINDOW = timedelta(days=30)
# Provider of the duplicate assessment an editor records with "not a duplicate".
HUMAN_PROVIDER = "human"
# The hold for a check Jev could not settle; the only one an editor can answer.
DUPLICATE_UNCERTAIN = "news_duplicate_uncertain"
# Candidates whose titles a new candidate is compared with. The first four are
# pipeline.ACTIVE_STATUSES (a test keeps them equal; pipeline imports this module).
KNOWN_STATUSES = (
    "drafting",
    "verifying",
    "locale_review",
    "jev_review",
    "manual_review",
    "shadow_review",
    "published",
)

# Two indexed, time-bounded pools are screened locally before any cross-category
# titles join the existing single Jev call. These are row caps, not model-call caps.
MAX_CROSS_PUBLISHED_ROWS = 160  # At most 80 articles with en and zh-TW titles.
MAX_CROSS_CANDIDATES = 60
MAX_CROSS_MATCHES = 8
_LATIN = re.compile(r"[a-z0-9]+")
_CJK_WORD = re.compile(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]+")
_TITLE_FILLER = frozenset(
    {
        "a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on", "the",
        "to", "with", "ai", "model", "models", "new",
    }
)
_EVENT_CUES = {
    "launch": frozenset(
        {
            "launch", "launches", "launched", "release", "releases", "released",
            "unveil", "unveils", "unveiled", "debut", "debuts", "debuted",
            "推出", "發布", "发表", "發表", "上线", "上線",
        }
    ),
    "price": frozenset(
        {
            "price", "prices", "pricing", "cost", "costs", "cut", "cuts",
            "discount", "降價", "降价", "調價", "调价", "調降", "调降",
        }
    ),
    "safety": frozenset(
        {
            "privacy", "lawsuit", "breach", "leak", "safety", "隱私",
            "隐私", "訴訟", "诉讼", "外洩", "泄露",
        }
    ),
}


@dataclass(frozen=True)
class CrossCategoryMatch:
    kind: str
    id: UUID
    vertical: str
    title: str
    similarity: float
    rationale: str
    slug: str | None = None

    def audit_json(self) -> dict[str, str | float]:
        result: dict[str, str | float] = {
            "kind": self.kind,
            "id": str(self.id),
            "vertical": self.vertical,
            "title": self.title,
            "similarity": round(self.similarity, 3),
            "rationale": self.rationale,
        }
        if self.slug is not None:
            result["slug"] = self.slug
        return result


@dataclass(frozen=True)
class KnownStories:
    titles: list[str]
    cross_category_matches: list[CrossCategoryMatch]


def _event_cues(title: str) -> set[str]:
    folded = unicodedata.normalize("NFKC", title).casefold()
    words = set(_LATIN.findall(folded))
    return {
        kind
        for kind, cues in _EVENT_CUES.items()
        if any(cue in words if cue.isascii() else cue in folded for cue in cues)
    }


def _title_terms(title: str) -> set[str]:
    folded = unicodedata.normalize("NFKC", title).casefold()
    terms = set(_LATIN.findall(folded)) - _TITLE_FILLER
    for word in _CJK_WORD.findall(folded):
        terms.update(word[index : index + 2] for index in range(len(word) - 1))
    return terms


def has_cjk_title(title: str) -> bool:
    return _CJK_WORD.search(title) is not None


def _cross_title_match(source: str, other: str) -> tuple[float, str] | None:
    source_cues, other_cues = _event_cues(source), _event_cues(other)
    if source_cues and other_cues and source_cues.isdisjoint(other_cues):
        return None  # A launch and a later price or privacy event are separate news.
    source_terms, other_terms = _title_terms(source), _title_terms(other)
    common = source_terms & other_terms
    if len(common) < 2 or len(common) / max(1, min(len(source_terms), len(other_terms))) < 0.5:
        return None
    source_folded = unicodedata.normalize("NFKC", source).casefold()
    other_folded = unicodedata.normalize("NFKC", other).casefold()
    likeness = SequenceMatcher(None, source_folded, other_folded).ratio()
    if likeness < 0.45:
        return None
    shared = ", ".join(sorted(common)[:5])
    shared_event = source_cues & other_cues
    event_hint = f" and both signal {', '.join(sorted(shared_event))}" if shared_event else ""
    return likeness, f"Titles share {shared}{event_hint}; event identity needs semantic review"


async def known_stories(session: AsyncSession, candidate: NewsCandidate) -> KnownStories:
    """Bounded same-category context plus plausible cross-category event matches.

    A lexical hit is only a reason to compare; it never rejects a candidate or
    declares two events identical. Jev still receives at most its old title cap.
    """

    cutoff = datetime.now(UTC).date() - DUPLICATE_WINDOW
    cross_verticals = tuple(vertical for vertical in VERTICALS if vertical != candidate.vertical)
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
            # In flight counts too: with several news workers, two outlets' versions of
            # one story could otherwise be drafted side by side.
            NewsCandidate.status.in_(KNOWN_STATUSES),
        )
        .order_by(NewsCandidate.created_at.desc())
        .limit(30)
    )

    matches: list[CrossCategoryMatch] = []
    if cross_verticals:
        cross_rows = await session.execute(
            select(
                GuideArticle.id,
                GuideArticle.slug,
                GuideSearchEntry.locale,
                GuideSearchEntry.title,
            )
            .join(GuideSearchEntry, GuideSearchEntry.article_id == GuideArticle.id)
            .where(
                or_(
                    *(GuideArticle.slug.like(f"{vertical}-news-%") for vertical in cross_verticals)
                ),
                GuideArticle.is_active.is_(True),
                GuideArticle.news_date >= cutoff,
                GuideSearchEntry.locale.in_(("en", "zh-TW")),
            )
            .order_by(GuideArticle.news_date.desc(), GuideArticle.id)
            .limit(MAX_CROSS_PUBLISHED_ROWS)
        )
        # Pick the language closest to the incoming source; compare at most one
        # published title per article, even when both locale search rows exist.
        cross_articles: dict[UUID, tuple[str, str, str]] = {}
        prefer = "zh-TW" if has_cjk_title(candidate.source_title) else "en"
        for article_id, slug, locale, title in cross_rows:
            if article_id == candidate.guide_article_id:
                continue
            if article_id not in cross_articles or locale == prefer:
                cross_articles[article_id] = (slug, locale, title)
        for article_id, (slug, _locale, title) in cross_articles.items():
            match = _cross_title_match(candidate.source_title, title)
            if match is not None:
                vertical = slug.split("-news-", 1)[0]
                matches.append(
                    CrossCategoryMatch(
                        "published_article", article_id, vertical, title, *match, slug
                    )
                )
        cross_candidates = await session.execute(
            select(
                NewsCandidate.id,
                NewsCandidate.vertical,
                NewsCandidate.source_title,
                NewsCandidate.guide_article_id,
            )
            .where(
                NewsCandidate.id != candidate.id,
                NewsCandidate.vertical.in_(cross_verticals),
                NewsCandidate.status.in_(KNOWN_STATUSES),
                NewsCandidate.created_at >= datetime.now(UTC) - DUPLICATE_WINDOW,
                or_(
                    NewsCandidate.guide_article_id.is_(None),
                    NewsCandidate.guide_article_id != candidate.guide_article_id,
                ),
            )
            .order_by(NewsCandidate.created_at.desc())
            .limit(MAX_CROSS_CANDIDATES)
        )
        for candidate_id, vertical, title, guide_article_id in cross_candidates:
            if guide_article_id in cross_articles:
                continue  # Already represented by the published article's identity.
            match = _cross_title_match(candidate.source_title, title)
            if match is not None:
                matches.append(
                    CrossCategoryMatch("candidate", candidate_id, vertical, title, *match)
                )
    matches.sort(key=lambda match: match.similarity, reverse=True)
    matches = matches[:MAX_CROSS_MATCHES]
    titles = list(
        dict.fromkeys(
            [*(match.title for match in matches), *list(published.values())[:40], *candidates]
        )
    )
    return KnownStories(titles[:MAX_DUPLICATE_TITLES], matches)


async def known_titles(session: AsyncSession, candidate: NewsCandidate) -> list[str]:
    return (await known_stories(session, candidate)).titles


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
    """An editor, or the judge in the owner's place, answered "not a duplicate" for this
    candidate's current evidence."""

    return (
        await session.scalar(
            select(NewsAssessment.id)
            .where(
                NewsAssessment.candidate_id == candidate.id,
                NewsAssessment.verdict == "pass",
                NewsAssessment.evidence_hash == candidate.evidence_hash,
                or_(
                    and_(
                        NewsAssessment.assessment_type == "duplicate",
                        NewsAssessment.provider == HUMAN_PROVIDER,
                    ),
                    # "pass" is a verdict the judge stores for one answer only: distinct.
                    NewsAssessment.assessment_type == "judge",
                ),
            )
            .limit(1)
        )
    ) is not None
