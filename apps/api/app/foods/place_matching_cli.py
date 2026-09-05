"""CLI entry point for bulk food merchant Place ID matching."""

from __future__ import annotations

from typing import Any

from app.admin.service import load_runtime_settings
from app.db import SessionFactory
from app.foods.place_matching import match_merchant_places, summarize, unmatched_merchants
from app.infra import get_redis


async def match_food_merchant_places(
    destination_ids: list[str],
    limit: int | None,
    apply: bool,
) -> dict[str, Any]:
    async with SessionFactory() as session:
        settings = await load_runtime_settings(session)
        merchants = await unmatched_merchants(
            session,
            destination_ids=tuple(destination_ids),
            limit=limit,
        )
        reports = await match_merchant_places(
            session, get_redis(), settings, merchants, apply=apply
        )
    report = summarize(reports)
    report["applied"] = apply
    return report
