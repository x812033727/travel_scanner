"""Run earlier news candidates that old rules or old models stopped through today's pipeline.

    python -m app.news_automation.backfill_cli --since 2026-09-15            # what would run
    python -m app.news_automation.backfill_cli --since 2026-09-15 --apply --actor-email <admin>

The owner asked on 2026-09-26 to "backfill" the days the automation produced nothing: 201
candidates had stopped because evidence from one website was not enough (the rule until
2026-09-25), or because MiniMax's drafts, checks or translations failed. Their evidence is
still stored, so each one is reopened as a new draft (status ``discovered``) and queued; the
current pipeline decides what happens to it, including the owner's confirmation for a story
that may not go out on its own. Candidates a person rejected for editorial reasons are not
in the pool: their error code is the hold they were rejected from, not one of these.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from collections import Counter
from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionFactory, engine
from app.models import User
from app.news_automation import jobs
from app.news_automation.models import NewsCandidate, NewsEvidence
from app.news_automation.service import audit
from app.news_automation.sources_cli import admin_actor

# The stops that say nothing about the story itself: the old evidence rule and the model
# failures of the MiniMax days.
BACKFILL_STOPS = frozenset(
    {
        "news_evidence_insufficient",
        "news_verification_failed",
        "news_locale_review_failed",
        "news_hard_checks_failed",
        "news_claim_source_invalid",
    }
)
BACKFILL_STATUSES = frozenset({"rejected", "needs_redraft"})


async def backfill_pool(
    session: AsyncSession, *, since: date, limit: int | None = None
) -> list[tuple[NewsCandidate, bool]]:
    """Candidates to reopen, with whether each has a first-party page, best first.

    Stories with a first-party page come first, since only those may publish on their own;
    then the newest.
    """
    rows = list(
        await session.scalars(
            select(NewsCandidate).where(
                NewsCandidate.status.in_(BACKFILL_STATUSES),
                NewsCandidate.error_code.in_(BACKFILL_STOPS),
                NewsCandidate.source_published_at
                >= datetime(since.year, since.month, since.day, tzinfo=UTC),
            )
        )
    )
    first_party = set(
        await session.scalars(
            select(NewsEvidence.candidate_id).where(
                NewsEvidence.candidate_id.in_([row.id for row in rows]),
                NewsEvidence.role == "evidence",
                NewsEvidence.is_first_party.is_(True),
            )
        )
    )
    ranked = sorted(
        rows,
        key=lambda row: (
            row.id not in first_party,
            -(row.source_published_at.timestamp() if row.source_published_at else 0),
        ),
    )
    chosen = ranked[:limit] if limit is not None else ranked
    return [(row, row.id in first_party) for row in chosen]


def reopen(session: AsyncSession, actor: User, row: NewsCandidate, reason: str) -> None:
    """Send a stopped candidate back to drafting, with an audit row saying why."""
    audit(
        session,
        actor,
        "news_candidate_reopened",
        f"news-candidate:{row.id}",
        reason=reason,
        previous_status=row.status,
        previous_error_code=row.error_code,
    )
    row.status = "discovered"
    row.error_code = None
    row.error_detail = None
    row.human_decision = None
    row.human_reason = reason
    row.retry_count += 1


async def run(
    *, since: date, limit: int | None, apply: bool, actor_email: str | None, reason: str
) -> dict[str, Any]:
    try:
        async with SessionFactory() as session:
            pool = await backfill_pool(session, since=since, limit=limit)
            report: dict[str, Any] = {
                "since": since.isoformat(),
                "candidates": len(pool),
                "first_party": sum(1 for _row, first in pool if first),
                "by_vertical": dict(Counter(row.vertical for row, _first in pool)),
                "by_stop": dict(Counter(str(row.error_code) for row, _first in pool)),
                "sample": [
                    {
                        "published": row.source_published_at.date().isoformat()
                        if row.source_published_at
                        else None,
                        "vertical": row.vertical,
                        "first_party": first,
                        "title": row.source_title[:90],
                    }
                    for row, first in pool[:10]
                ],
                "applied": False,
            }
            if not apply or not pool:
                return report
            if not actor_email:
                raise SystemExit("--actor-email is required with --apply")
            actor = await admin_actor(session, actor_email)
            if actor is None:
                raise SystemExit("The actor must be an active administrator")
            queued: list[tuple[Any, int]] = []
            for row, _first in pool:
                reopen(session, actor, row, reason)
                queued.append((row.id, row.retry_count))
            await session.commit()
        # Queued only once every reopen is saved, so no job runs on a half-reopened batch.
        for candidate_id, retry_count in queued:
            jobs.enqueue_candidate(candidate_id, retry_count=retry_count)
        report["applied"] = True
        return report
    finally:
        await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--since",
        required=True,
        type=date.fromisoformat,
        help="Oldest source publication date to reopen (YYYY-MM-DD)",
    )
    parser.add_argument("--limit", type=int, help="At most this many, best first")
    parser.add_argument("--apply", action="store_true", help="Reopen and queue; list otherwise")
    parser.add_argument("--actor-email", help="Administrator the audit rows are recorded for")
    parser.add_argument(
        "--reason",
        default="Backfill: stopped by a rule or model the pipeline no longer uses",
        help="Recorded on each candidate and its audit row",
    )
    args = parser.parse_args()
    report = asyncio.run(
        run(
            since=args.since,
            limit=args.limit,
            apply=args.apply,
            actor_email=args.actor_email,
            reason=args.reason,
        )
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
