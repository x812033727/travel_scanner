"""Read back what the Jev shadow run recorded, so a threshold can be set on evidence.

``execute_ai_search`` writes a ``jev_shadow`` block into each run's ``result_json``
while ``JEV_SHADOW_GUIDE_ASSESSMENT=shadow``: for every candidate, what Jev answered
and what the live ``relevance_score >= 60`` rule decided. This prints the only numbers
that should be allowed to move a threshold -- overall agreement, and agreement split
by language, because TypeSafe says accuracy is best in English and says nothing about
the other four locales this product ships in.

Nothing here writes. The disagreement lists are for reading by hand: a model that
agrees 95% of the time can still be wrong in one direction only, and the rate alone
will not show that.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from sqlalchemy import select

from app.ai.jev import USD_PER_INPUT_TOKEN
from app.db import SessionFactory
from app.models import HotspotGuideAISearchRun


def _tally() -> dict[str, int]:
    return {"rows": 0, "agreed": 0, "jev_only": 0, "shipped_only": 0}


def _record(tally: dict[str, int], row: dict[str, Any]) -> None:
    tally["rows"] += 1
    jev = bool(row.get("jev_accepted"))
    shipped = bool(row.get("shipped_accepted"))
    if jev == shipped:
        tally["agreed"] += 1
    elif jev:
        tally["jev_only"] += 1
    else:
        tally["shipped_only"] += 1


def _rate(tally: dict[str, int]) -> dict[str, Any]:
    rows = tally["rows"]
    return {
        **tally,
        "agreement": round(tally["agreed"] / rows, 4) if rows else None,
    }


async def report_jev_shadow(*, limit: int = 200, examples: int = 20) -> dict[str, Any]:
    """Summarise the shadow rows across the most recent runs that carry any."""
    async with SessionFactory() as session:
        runs = (
            await session.scalars(
                select(HotspotGuideAISearchRun)
                .where(HotspotGuideAISearchRun.result_json.is_not(None))
                .order_by(HotspotGuideAISearchRun.created_at.desc())
                .limit(limit)
            )
        ).all()

    overall = _tally()
    by_requested: dict[str, dict[str, int]] = defaultdict(_tally)
    by_detected: dict[str, dict[str, int]] = defaultdict(_tally)
    tiers: dict[str, int] = defaultdict(int)
    disagreements: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    runs_seen = 0
    calls = 0
    input_tokens = 0

    for run in runs:
        result = run.result_json or {}
        shadow_by_locale = result.get("jev_shadow")
        if not isinstance(shadow_by_locale, dict):
            continue
        runs_seen += 1
        for locale, block in shadow_by_locale.items():
            if not isinstance(block, dict):
                continue
            usage = block.get("usage") or {}
            calls += int(usage.get("calls", 0))
            input_tokens += int(usage.get("input_tokens", 0))
            if block.get("errors"):
                errors.append({"run_id": str(run.id), "locale": locale, "errors": block["errors"]})
            for row in block.get("rows") or []:
                if not isinstance(row, dict):
                    continue
                _record(overall, row)
                _record(by_requested[locale], row)
                _record(by_detected[str(row.get("detected_locale") or "unknown")], row)
                tiers[str(row.get("jev_tier") or "unknown")] += 1
                if bool(row.get("jev_accepted")) != bool(row.get("shipped_accepted")):
                    if len(disagreements) < examples:
                        disagreements.append({"run_id": str(run.id), **row})

    return {
        "runs_with_shadow_rows": runs_seen,
        "overall": _rate(overall),
        # The split that decides whether JEV_CJK_AUTOPILOT_ENABLED may ever be turned on.
        "by_requested_locale": {key: _rate(value) for key, value in sorted(by_requested.items())},
        "by_detected_locale": {key: _rate(value) for key, value in sorted(by_detected.items())},
        "tiers": dict(sorted(tiers.items())),
        "cost": {
            "calls": calls,
            "input_tokens": input_tokens,
            "usd": round(input_tokens * USD_PER_INPUT_TOKEN, 6),
        },
        "errors": errors,
        "disagreements": disagreements,
    }
