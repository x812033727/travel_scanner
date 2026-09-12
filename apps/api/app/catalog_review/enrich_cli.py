"""Run the merchant enrichment mode of the catalog review from the api container.

The admin page starts the same run through the API; this is for an operator who wants a
dry-run inventory first, or who runs the batch in chunks over SSH the way
``review-pending-guides`` is run. It creates the run through ``create_run`` — same
idempotency, same snapshot, same budgets — and then executes the worker inline instead
of waiting for the RQ queue, so it needs no worker container and prints the result.

The idempotency key is derived from the actor, the arguments and the UTC date, so a
retried invocation returns (and, when it stopped early, resumes) the run it already paid
for instead of snapshotting and searching everything again.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import func, select

from app.admin.service import load_runtime_settings
from app.catalog_review.jobs import ENRICH_BATCH_SIZE, ENRICH_MODE, _run
from app.catalog_review.repository import entity_snapshot, publication_gaps
from app.catalog_review.service import (
    StartRequest,
    _pending_merchants_for_enrichment,
    create_run,
    get_run,
    item_corrections,
    prepare_resume,
    run_items,
    run_view,
)
from app.db import SessionFactory, engine
from app.foods.place_matching import SKIPPED_COUNTRIES
from app.infra import get_redis
from app.models import User
from app.problems import AppError

KEY_PREFIX = "cli-enrich-"


def enrichment_idempotency_key(actor_id: UUID, request: StartRequest, day: date) -> str:
    material = json.dumps(
        {
            "actor": str(actor_id),
            "destination_ids": list(request.destination_ids),
            "limit": request.limit,
            "max_calls": request.max_calls if "max_calls" in request.model_fields_set else None,
            "identify": request.identify_places,
            "day": day.isoformat(),
        },
        sort_keys=True,
    )
    return KEY_PREFIX + hashlib.sha256(material.encode("utf-8")).hexdigest()[:32]


def build_request(
    *,
    destination_ids: list[str],
    limit: int | None,
    max_calls: int | None,
    identify: bool,
) -> StartRequest:
    values: dict[str, Any] = {
        "mode": ENRICH_MODE,
        "scope": "foods",
        "destination_ids": list(destination_ids),
        "identify_places": identify,
    }
    if limit is not None:
        values["limit"] = limit
    if max_calls is not None:
        values["max_calls"] = max_calls
    return StartRequest.model_validate(values)


async def _admin_user(session: Any, email: str) -> User | None:
    user: User | None = await session.scalar(
        select(User).where(func.lower(User.email) == email.casefold())
    )
    if user is None or not (user.is_admin and user.is_active):
        return None
    return user


async def _inventory(session: Any, request: StartRequest) -> dict[str, Any]:
    merchants = await _pending_merchants_for_enrichment(
        session, destination_ids=request.destination_ids, limit=request.limit
    )
    by_destination: Counter[str] = Counter()
    gaps: Counter[str] = Counter()
    korea = 0
    no_place_id = 0
    for merchant in merchants:
        by_destination[merchant.destination_id] += 1
        if merchant.country_code.upper() in SKIPPED_COUNTRIES:
            korea += 1
        elif not merchant.google_place_id:
            no_place_id += 1
        for gap in publication_gaps("merchant", await entity_snapshot(session, merchant)):
            gaps[gap] += 1
    batches = math.ceil(len(merchants) / ENRICH_BATCH_SIZE)
    return {
        "dry_run": True,
        "pending": len(merchants),
        "by_destination": dict(sorted(by_destination.items())),
        "no_place_id": no_place_id,
        "kr": korea,
        "gaps": dict(sorted(gaps.items())),
        "estimated_gemini_calls": 2 * batches,
        "estimated_google_calls": no_place_id if request.identify_places else 0,
        "max_calls": request.max_calls,
    }


async def enrich_food_merchants(
    *,
    actor_email: str,
    destination_ids: list[str],
    limit: int | None,
    max_calls: int | None,
    identify: bool,
    dry_run: bool,
    idempotency_key: str | None,
) -> dict[str, Any]:
    request = build_request(
        destination_ids=destination_ids, limit=limit, max_calls=max_calls, identify=identify
    )
    try:
        async with SessionFactory() as session:
            user = await _admin_user(session, actor_email)
            if user is None:
                return {"error": "actor_not_admin", "email": actor_email}
            settings = await load_runtime_settings(session)
            if dry_run:
                return await _inventory(session, request)
            key = idempotency_key or enrichment_idempotency_key(
                user.id, request, datetime.now(UTC).date()
            )
            try:
                run, created = await create_run(session, settings, user.id, request, key)
            except AppError as exc:
                return {"error": exc.code, "detail": exc.detail, "idempotency_key": key}
            resumed = False
            if not created:
                view = await run_view(session, run, settings)
                if not view["can_resume"]:
                    return {
                        "run": view,
                        "created": False,
                        "resumed": False,
                        "idempotency_key": key,
                    }
                run = await prepare_resume(
                    session, run.id, user.id, scope="foods", settings=settings
                )
                resumed = True
            run_id = run.id
        await _run(run_id)
        async with SessionFactory() as session:
            run = await get_run(session, run_id)
            view = await run_view(session, run, settings)
            kinds: Counter[str] = Counter(
                str(entry.get("kind"))
                for item in await run_items(session, run_id, scope="foods")
                for entry in item_corrections(item)
            )
        return {
            "run": view,
            "created": created,
            "resumed": resumed,
            "idempotency_key": key,
            "corrections_by_kind": dict(sorted(kinds.items())),
        }
    finally:
        try:
            await get_redis().aclose()
        finally:
            get_redis.cache_clear()
            await engine.dispose()
