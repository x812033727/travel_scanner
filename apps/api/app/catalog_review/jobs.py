"""Leased, resumable catalog jobs; every Gemini request reserves its budget first."""

from __future__ import annotations

import asyncio
import logging
from collections import Counter
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID, uuid4

from redis import Redis as SyncRedis
from rq import Queue
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.catalog_review.budget import run_call_limit
from app.catalog_review.enrichment import (
    VerifiedCandidate,
    load_enrichment_taxonomy,
    merchant_prompt_context,
    verify_candidates,
)
from app.catalog_review.errors import CatalogAssessmentError, safe_error_diagnostics
from app.catalog_review.evidence import MAX_URLS, fetch_sources, normalize_source_url
from app.catalog_review.provider import CatalogGeminiProvider, VerifiedEnrichment
from app.catalog_review.repository import (
    ENTITY_TYPES,
    entity_snapshot,
    fingerprint,
    import_draft,
    load_entity,
    make_review_item,
    publication_gaps,
    source_urls,
    trusted_hosts,
)
from app.catalog_review.schemas import (
    CatalogKind,
    EnrichmentAssessment,
    EvidenceSource,
    ReviewCandidate,
)
from app.catalog_review.scope import SCOPE_KINDS, request_scope, scope_counts
from app.config import Settings, get_settings
from app.db import SessionFactory, engine
from app.destinations.catalog import DESTINATIONS, destination_for_id
from app.foods.place_matching import SKIPPED_COUNTRIES, match_merchant_places
from app.hotspots.guides import consume_search_budget
from app.infra import get_redis
from app.models import (
    CatalogReviewItem,
    CatalogReviewRun,
    FoodCategory,
    FoodDestination,
    FoodMerchant,
)
from app.problems import AppError

logger = logging.getLogger(__name__)
LEASE_SECONDS = 300
HEARTBEAT_SECONDS = 60
REVIEW_BATCH_SIZE = 8
MAX_CONSECUTIVE_PROVIDER_FAILURES = 3
DISCOVERY_DESTINATION_BATCH_SIZE = 1
TARGET_COUNTS: dict[str, int] = {"hotspot": 40, "food": 20, "merchant": 40}
TOKEN_KEYS = ("input_tokens", "output_tokens", "thought_tokens")
ENRICH_MODE = "enrich_merchants"
#: Five merchants share one grounded search: ~30 grounding chunks per answer leave about
#: six pages each, and one structured call reads them all back.
ENRICH_BATCH_SIZE = 5
IDENTIFY_CHUNK_SIZE = 10
#: Per merchant: its own cited pages first, then what the search found.
ENRICH_OWN_SOURCES = 5
ENRICH_OFFICIAL_SOURCES = 3
ENRICH_LISTING_SOURCES = 2
ENRICH_STOP_OUTCOMES = frozenset({"usage_guard", "not_configured", "lease_lost"})
STALE_MERCHANT_REASON = "店家已不在待審狀態，未再補資料。"
NO_PAGES_REASON = "搜尋未找到可獨立核對的官網或觀光局頁面。"


class LeaseLost(Exception):
    """Another worker or an administrator owns this run now."""


class BudgetStopped(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


class ProviderCircuitOpen(Exception):
    """Stop this attempt after repeated provider failures; only API resume may retry."""


def _count(value: Any, default: int = 0) -> int:
    valid = isinstance(value, int) and not isinstance(value, bool) and value >= 0
    return value if valid else default


def _targets(request: dict[str, Any]) -> dict[str, int]:
    scope = request_scope(request)
    raw = request.get("requested_counts", scope_counts(scope))
    if (
        not isinstance(raw, dict)
        or set(raw) != set(TARGET_COUNTS)
        or any(
            not isinstance(value, int) or isinstance(value, bool) or value < 0
            for value in raw.values()
        )
        or not 1 <= sum(raw.values()) <= 100
    ):
        raise ValueError("Invalid discovery target counts")
    if any(value and kind not in SCOPE_KINDS[scope] for kind, value in raw.items()):
        raise ValueError("Discovery target is outside the run scope")
    return cast(dict[str, int], raw)


def _future(stamp: datetime | None) -> bool:
    return stamp is not None and stamp.replace(tzinfo=stamp.tzinfo or UTC) > datetime.now(UTC)


async def _locked_run(session: AsyncSession, run_id: UUID, token: str) -> CatalogReviewRun:
    run = await session.scalar(
        select(CatalogReviewRun)
        .where(
            CatalogReviewRun.id == run_id,
        )
        .with_for_update()
    )
    if (
        run is None
        or run.status != "running"
        or run.lease_token != token
        or not _future(run.lease_until)
    ):
        raise LeaseLost()
    return run


async def _claim_run(run_id: UUID) -> CatalogReviewRun | None:
    async with SessionFactory() as session:
        run = await session.scalar(
            select(CatalogReviewRun)
            .where(
                CatalogReviewRun.id == run_id,
            )
            .with_for_update()
        )
        if run is None or run.status not in {"queued", "running"} or _future(run.lease_until):
            return None
        if run.status == "queued":
            # An explicit API resume permits another bounded attempt at a shortfall.
            run.result_json = {
                **(run.result_json or {}),
                "no_progress_counts": {},
                "consecutive_provider_failures": 0,
            }
        run.status = "running"
        run.lease_token = uuid4().hex
        run.lease_until = datetime.now(UTC) + timedelta(seconds=LEASE_SECONDS)
        run.completed_at = None
        run.error_code = None
        run.error_message = None
        run.version += 1
        await session.commit()
        return run


async def _heartbeat(run_id: UUID, token: str) -> None:
    while True:
        await asyncio.sleep(HEARTBEAT_SECONDS)
        try:
            async with SessionFactory() as session:
                run = await _locked_run(session, run_id, token)
                run.lease_until = datetime.now(UTC) + timedelta(seconds=LEASE_SECONDS)
                await session.commit()
        except Exception:
            # Saves and reservations still check the DB lease before any next effect.
            logger.warning("Catalog review heartbeat stopped for %s", run_id)
            return


async def reserve_call(run_id: UUID, token: str, settings: Settings) -> bool:
    """Commit the per-run call count before HTTP, failing closed on either budget."""
    async with SessionFactory() as session:
        run = await _locked_run(session, run_id, token)
        usage = dict(run.usage_json or {})
        maximum = run_call_limit(run.request_json)
        if _count(usage.get("calls")) >= maximum:
            raise BudgetStopped("catalog_review_call_limit")
        if not await consume_search_budget(
            get_redis(),
            "gemini",
            settings.hotspot_guide_gemini_daily_search_budget,
        ):
            raise BudgetStopped("catalog_review_daily_budget")
        usage["calls"] = _count(usage.get("calls")) + 1
        usage["member_charged"] = False
        run.usage_json = usage
        run.lease_until = datetime.now(UTC) + timedelta(seconds=LEASE_SECONDS)
        await session.commit()
    return True


async def _save_usage(
    run_id: UUID,
    token: str,
    provider: CatalogGeminiProvider,
    saved: dict[str, int],
) -> None:
    totals = {key: _count(provider.usage.get(key)) for key in TOKEN_KEYS}
    async with SessionFactory() as session:
        run = await _locked_run(session, run_id, token)
        usage = dict(run.usage_json or {})
        for key, total in totals.items():
            usage[key] = _count(usage.get(key)) + max(0, total - saved.get(key, 0))
        usage["member_charged"] = False
        run.usage_json = usage
        await session.commit()
    saved.update(totals)


def _source_metadata(sources: list[EvidenceSource]) -> list[dict[str, Any]]:
    return [source.model_dump(exclude={"text"}) for source in sources]


async def _batch_error(
    run_id: UUID,
    token: str,
    item_ids: list[UUID],
    error: Exception,
    sources: dict[UUID, list[EvidenceSource]],
    consecutive_failures: int,
) -> None:
    diagnostic = safe_error_diagnostics(error)
    async with SessionFactory() as session:
        run = await _locked_run(session, run_id, token)
        items = (
            await session.scalars(
                select(CatalogReviewItem)
                .where(
                    CatalogReviewItem.run_id == run_id,
                    CatalogReviewItem.id.in_(item_ids),
                    CatalogReviewItem.status.in_(("pending", "error")),
                )
                .with_for_update()
            )
        ).all()
        for item in items:
            item.status = "error"
            item.reason = "此批 Gemini 評估失敗；可續跑重試，尚未套用任何判斷。"
            item.assessment_json = diagnostic
            item.evidence_json = _source_metadata(sources.get(item.id, []))
        run.result_json = {
            **(run.result_json or {}),
            "last_review_error": diagnostic,
            "consecutive_provider_failures": consecutive_failures,
        }
        await session.commit()


async def _review_items(
    run_id: UUID,
    token: str,
    phase: str,
    provider: CatalogGeminiProvider,
    hosts: set[str],
    saved_usage: dict[str, int],
) -> None:
    # Capture this attempt's work once: a failed batch is retried only on API resume.
    async with SessionFactory() as session:
        run = await _locked_run(session, run_id, token)
        run.phase = phase
        consecutive_failures = _count((run.result_json or {}).get("consecutive_provider_failures"))
        item_ids = list(
            (
                await session.scalars(
                    select(CatalogReviewItem.id)
                    .where(
                        CatalogReviewItem.run_id == run_id,
                        CatalogReviewItem.phase == phase,
                        CatalogReviewItem.kind.in_(SCOPE_KINDS[request_scope(run.request_json)]),
                        CatalogReviewItem.status.in_(("pending", "error")),
                    )
                    .order_by(CatalogReviewItem.id)
                )
            ).all()
        )
        await session.commit()
    if consecutive_failures >= MAX_CONSECUTIVE_PROVIDER_FAILURES:
        raise ProviderCircuitOpen()
    for offset in range(0, len(item_ids), REVIEW_BATCH_SIZE):
        batch_ids = item_ids[offset : offset + REVIEW_BATCH_SIZE]
        sources_by_item: dict[UUID, list[EvidenceSource]] = {}
        try:
            async with SessionFactory() as session:
                await _locked_run(session, run_id, token)
                items = list(
                    (
                        await session.scalars(
                            select(CatalogReviewItem).where(
                                CatalogReviewItem.run_id == run_id,
                                CatalogReviewItem.id.in_(batch_ids),
                                CatalogReviewItem.status.in_(("pending", "error")),
                            )
                        )
                    ).all()
                )
            if not items:
                continue
            urls_by_item = {item.id: source_urls(item.snapshot_json) for item in items}
            urls = list(dict.fromkeys(url for values in urls_by_item.values() for url in values))
            fetched = await fetch_sources(urls, hosts)
            by_url = {normalize_source_url(source.url) or source.url: source for source in fetched}
            for item in items:
                sources_by_item[item.id] = [
                    by_url[key]
                    for url in urls_by_item[item.id]
                    if (key := normalize_source_url(url) or url) in by_url
                ]
            candidates = [
                ReviewCandidate(
                    candidate_id=str(item.id),
                    kind=cast(CatalogKind, item.kind),
                    name=item.name,
                    local_name=str(item.snapshot_json.get("local_name") or ""),
                    destination_id=item.destination_id,
                    data=item.snapshot_json,
                    sources=sources_by_item[item.id],
                )
                for item in items
            ]
            try:
                result = await provider.assess(candidates)
            finally:
                await _save_usage(run_id, token, provider, saved_usage)
            by_id = {assessment.candidate_id: assessment for assessment in result.items}
            if len(by_id) != len(result.items) or set(by_id) != {str(item.id) for item in items}:
                raise CatalogAssessmentError("catalog_response_ids_invalid", retryable=False)
            # Import here: the API service can enqueue jobs without an import cycle.
            from app.catalog_review.service import record_assessment

            async with SessionFactory() as session:
                run = await _locked_run(session, run_id, token)
                current = (
                    await session.scalars(
                        select(CatalogReviewItem)
                        .where(
                            CatalogReviewItem.run_id == run_id,
                            CatalogReviewItem.id.in_([item.id for item in items]),
                            CatalogReviewItem.status.in_(("pending", "error")),
                        )
                        .with_for_update()
                    )
                ).all()
                for item in current:
                    record_assessment(item, by_id[str(item.id)], sources_by_item[item.id])
                run.result_json = {**(run.result_json or {}), "consecutive_provider_failures": 0}
                await session.commit()
            consecutive_failures = 0
        except (BudgetStopped, LeaseLost):
            raise
        except Exception as exc:
            if isinstance(exc, CatalogAssessmentError):
                consecutive_failures += 1
            await _batch_error(run_id, token, batch_ids, exc, sources_by_item, consecutive_failures)
            if consecutive_failures >= MAX_CONSECUTIVE_PROVIDER_FAILURES:
                raise ProviderCircuitOpen() from exc


async def _discovery_context(
    session: AsyncSession,
    kind: CatalogKind,
    *,
    destination_offset: int = 0,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Build a small, rotating discovery prompt for one catalog kind.

    The database remains the authoritative global duplicate guard. Sending every
    name from every catalog table made the production prompt exceed 40k tokens and
    caused grounded discovery to time out before returning usable drafts.
    """
    profiles = list(DESTINATIONS)
    if not profiles:
        return [], []
    start = destination_offset % len(profiles)
    rotated = profiles[start:] + profiles[:start]
    selected = rotated[: min(DISCOVERY_DESTINATION_BATCH_SIZE, len(rotated))]
    selected_ids = {profile.id for profile in selected}

    avoid: set[str] = set()
    food_slugs: dict[UUID, str] = {}
    context_kinds = (kind, "food") if kind == "merchant" else (kind,)
    for entity_kind in context_kinds:
        model = ENTITY_TYPES[entity_kind]
        rows: list[Any] = list((await session.scalars(select(model))).all())
        for row in rows:
            destination_id = getattr(row, "destination_id", None)
            if entity_kind == kind and kind != "food" and destination_id in selected_ids:
                # No public-status filter: rejected/disabled records are dedupe tombstones.
                for field in ("slug", "name", "local_name", "romanized_name"):
                    value = getattr(row, field, None)
                    if isinstance(value, str) and value:
                        avoid.add(value)
            if entity_kind == "food" and row.review_status == "approved" and row.is_active:
                food_slugs[row.id] = row.slug
    foods: dict[str, list[str]] = {}
    food_destinations: dict[UUID, set[str]] = {}
    links = (
        (await session.scalars(select(FoodDestination))).all()
        if kind in {"food", "merchant"}
        else []
    )
    for link in links:
        food_destinations.setdefault(link.food_id, set()).add(link.destination_id)
        if link.food_id in food_slugs:
            foods.setdefault(link.destination_id, []).append(food_slugs[link.food_id])
    if kind == "food":
        for row in (await session.scalars(select(ENTITY_TYPES["food"]))).all():
            row_id = getattr(row, "id", None)
            if not isinstance(row_id, UUID) or not (
                food_destinations.get(row_id, set()) & selected_ids
            ):
                continue
            for field in ("slug", "name", "local_name", "romanized_name"):
                value = getattr(row, field, None)
                if isinstance(value, str) and value:
                    avoid.add(value)
    categories = (
        list(
            (
                await session.scalars(
                    select(FoodCategory.slug).where(
                        FoodCategory.is_active.is_(True),
                    )
                )
            ).all()
        )
        if kind == "merchant"
        else []
    )
    destinations = [
        {
            "id": profile.id,
            "city": profile.city,
            "country": profile.country,
            "areas": list(profile.areas),
            **(
                {
                    "food_slugs": foods.get(profile.id, []),
                    "category_slugs": categories,
                }
                if kind == "merchant"
                else {}
            ),
        }
        for profile in selected
    ]
    return destinations, sorted(avoid)


async def _discover_items(
    run_id: UUID,
    token: str,
    provider: CatalogGeminiProvider,
    saved_usage: dict[str, int],
) -> None:
    async with SessionFactory() as session:
        run = await _locked_run(session, run_id, token)
        consecutive_failures = _count((run.result_json or {}).get("consecutive_provider_failures"))
        await session.commit()
    if consecutive_failures >= MAX_CONSECUTIVE_PROVIDER_FAILURES:
        raise ProviderCircuitOpen()
    for kind in SCOPE_KINDS[request_scope(run.request_json)]:
        while True:
            async with SessionFactory() as session:
                run = await _locked_run(session, run_id, token)
                request = run.request_json or {}
                target = _targets(request)[kind]
                result = run.result_json or {}
                created = _count((result.get("created_counts") or {}).get(kind))
                misses = _count((result.get("no_progress_counts") or {}).get(kind))
                rounds = _count((result.get("discovery_round_counts") or {}).get(kind))
                if created >= target or misses >= 3:
                    break
                run.phase = "discover_new"
                destinations, avoid = await _discovery_context(
                    session,
                    kind,
                    destination_offset=rounds * DISCOVERY_DESTINATION_BATCH_SIZE,
                )
                await session.commit()
            error: Exception | None = None
            try:
                batch = await provider.discover(kind, min(5, target - created), destinations, avoid)
                consecutive_failures = 0
            except (BudgetStopped, LeaseLost):
                raise
            except Exception as exc:
                error = exc
                batch = None
                if isinstance(exc, CatalogAssessmentError):
                    consecutive_failures += 1
            finally:
                await _save_usage(run_id, token, provider, saved_usage)
            async with SessionFactory() as session:
                run = await _locked_run(session, run_id, token)
                added = 0
                duplicates = 0
                for draft in batch.items if batch is not None else []:
                    if draft.kind != kind or added >= min(5, target - created):
                        continue
                    try:
                        async with session.begin_nested():
                            entity = await import_draft(session, draft, run.actor_user_id, run_id)
                            if entity is not None:
                                await make_review_item(session, run_id, kind, entity, "review_new")
                                await session.flush()
                        if entity is not None:
                            added += 1
                        else:
                            duplicates += 1
                    except (AppError, ValueError, IntegrityError) as exc:
                        error = exc
                result = dict(run.result_json or {})
                counts = dict(result.get("created_counts") or {})
                counts[kind] = _count(counts.get(kind)) + added
                no_progress = dict(result.get("no_progress_counts") or {})
                no_progress[kind] = 0 if added else misses + 1
                discovery_rounds = dict(result.get("discovery_round_counts") or {})
                discovery_rounds[kind] = rounds + 1
                result.update(
                    created_counts=counts,
                    no_progress_counts=no_progress,
                    discovery_round_counts=discovery_rounds,
                )
                result["last_discovery_diagnostics"] = dict(
                    getattr(provider, "discovery_diagnostics", {})
                )
                result["duplicates"] = _count(result.get("duplicates")) + duplicates
                if error is not None:
                    result["last_discovery_error"] = safe_error_diagnostics(error)
                result["consecutive_provider_failures"] = consecutive_failures
                run.result_json = result
                # Entity, snapshot and count commit together; retries see all or none.
                await session.commit()
            if consecutive_failures >= MAX_CONSECUTIVE_PROVIDER_FAILURES:
                raise ProviderCircuitOpen() from error


async def _lease_alive(run_id: UUID, token: str) -> bool:
    try:
        async with SessionFactory() as session:
            await _locked_run(session, run_id, token)
    except LeaseLost:
        return False
    return True


def _identify_context(item: CatalogReviewItem, matched_ids: set[str]) -> dict[str, Any]:
    snapshot = item.snapshot_json or {}
    country = str(snapshot.get("country_code") or "").upper()
    return {
        "matched_in_run": str(item.entity_id) in matched_ids,
        "place_id": snapshot.get("google_place_id"),
        "skipped": "kr" if country in SKIPPED_COUNTRIES else None,
    }


async def _identify_items(run_id: UUID, token: str, settings: Settings) -> None:
    """Give the merchants that still lack a Place ID one through the existing matcher.

    Zero Gemini calls: this is Google Text Search, guarded by the same 90% brake and
    the same ownership check as ``match-food-merchant-places``. It writes only
    ``google_place_id``; the snapshot each item carries is refreshed later, right
    before its batch is assessed, so what a human applies against is what Gemini saw.
    """
    async with SessionFactory() as session:
        run = await _locked_run(session, run_id, token)
        run.phase = "identify"
        request = run.request_json or {}
        enabled = request.get("identify_places", True) is not False
        actor_id = run.actor_user_id
        entity_ids = list(
            (
                await session.scalars(
                    select(CatalogReviewItem.entity_id).where(
                        CatalogReviewItem.run_id == run_id,
                        CatalogReviewItem.kind == "merchant",
                        CatalogReviewItem.phase == ENRICH_MODE,
                        CatalogReviewItem.status.in_(("pending", "error")),
                    )
                )
            ).all()
        )
        await session.commit()
    outcomes: Counter[str] = Counter()
    matched: list[str] = []
    stopped: str | None = None if enabled else "disabled"
    if enabled and entity_ids:
        async with SessionFactory() as session:
            merchants = list(
                (
                    await session.scalars(
                        select(FoodMerchant)
                        .where(
                            FoodMerchant.id.in_(entity_ids),
                            FoodMerchant.google_place_id.is_(None),
                            FoodMerchant.review_status == "pending",
                            FoodMerchant.country_code.notin_(tuple(SKIPPED_COUNTRIES)),
                        )
                        .order_by(
                            FoodMerchant.destination_id,
                            FoodMerchant.display_order,
                            FoodMerchant.name,
                        )
                    )
                ).all()
            )

            async def still_leased() -> bool:
                return await _lease_alive(run_id, token)

            for offset in range(0, len(merchants), IDENTIFY_CHUNK_SIZE):
                chunk = merchants[offset : offset + IDENTIFY_CHUNK_SIZE]
                by_slug = {merchant.slug: merchant for merchant in chunk}
                reports = await match_merchant_places(
                    session,
                    get_redis(),
                    settings,
                    chunk,
                    apply=True,
                    actor_id=actor_id,
                    origin="catalog_review",
                    run_id=run_id,
                    should_continue=still_leased,
                )
                for report in reports:
                    outcomes[report.outcome] += 1
                    if report.outcome == "matched" and report.slug in by_slug:
                        matched.append(str(by_slug[report.slug].id))
                    if report.outcome in ENRICH_STOP_OUTCOMES:
                        stopped = report.outcome
                if stopped:
                    break
    if stopped == "lease_lost":
        raise LeaseLost()
    async with SessionFactory() as session:
        run = await _locked_run(session, run_id, token)
        run.result_json = {
            **(run.result_json or {}),
            "identify": {
                "processed": sum(outcomes.values()),
                "outcomes": dict(sorted(outcomes.items())),
                "stopped": stopped,
                "matched_entity_ids": matched,
            },
        }
        await session.commit()


async def _refresh_enrichment_batch(
    session: AsyncSession, run_id: UUID, item_ids: list[UUID]
) -> list[CatalogReviewItem]:
    """Re-snapshot each item from its live merchant, or mark it stale.

    The identify phase and administrators both change merchants after the snapshot was
    taken; assessing a stale snapshot would make ``apply`` refuse every correction with
    ``candidate_changed``.
    """
    items = list(
        (
            await session.scalars(
                select(CatalogReviewItem)
                .where(
                    CatalogReviewItem.run_id == run_id,
                    CatalogReviewItem.id.in_(item_ids),
                    CatalogReviewItem.status.in_(("pending", "error")),
                )
                .with_for_update()
            )
        ).all()
    )
    live: list[CatalogReviewItem] = []
    for item in items:
        entity = await load_entity(session, item.kind, item.entity_id, lock=True)
        if entity is None or entity.review_status != "pending":
            item.status = "stale"
            item.reason = STALE_MERCHANT_REASON
            continue
        data = await entity_snapshot(session, entity)
        item.snapshot_json = data
        item.snapshot_hash = fingerprint(data)
        item.gaps_json = publication_gaps(item.kind, data)
        live.append(item)
    return live


def _enrichment_sources(
    known_urls: list[str],
    pages: list[VerifiedCandidate],
    by_url: dict[str, EvidenceSource],
) -> list[EvidenceSource]:
    own = [
        by_url[key] for url in known_urls if (key := normalize_source_url(url) or url) in by_url
    ][:ENRICH_OWN_SOURCES]
    official = [
        by_url[page.url] for page in pages if page.kind == "official" and page.url in by_url
    ]
    listing = [by_url[page.url] for page in pages if page.kind == "listing" and page.url in by_url]
    merged = [*own, *official[:ENRICH_OFFICIAL_SOURCES], *listing[:ENRICH_LISTING_SOURCES]]
    return list({source.url: source for source in merged}.values())[:10]


async def _enrich_items(
    run_id: UUID,
    token: str,
    provider: CatalogGeminiProvider,
    hosts: set[str],
    saved_usage: dict[str, int],
) -> None:
    """Two Gemini calls per batch: a grounded search, then one structured extraction.

    Between them the server fetches every candidate page and decides, by name and
    location, which page may back which merchant; the model is never asked to attribute
    URLs, and every correction it returns is re-checked against the fetched text.
    """
    async with SessionFactory() as session:
        run = await _locked_run(session, run_id, token)
        run.phase = ENRICH_MODE
        result = run.result_json or {}
        consecutive_failures = _count(result.get("consecutive_provider_failures"))
        matched_ids = {
            str(value) for value in (result.get("identify") or {}).get("matched_entity_ids") or []
        }
        item_ids = list(
            (
                await session.scalars(
                    select(CatalogReviewItem.id)
                    .where(
                        CatalogReviewItem.run_id == run_id,
                        CatalogReviewItem.kind == "merchant",
                        CatalogReviewItem.phase == ENRICH_MODE,
                        CatalogReviewItem.status.in_(("pending", "error")),
                    )
                    .order_by(CatalogReviewItem.id)
                )
            ).all()
        )
        taxonomy = await load_enrichment_taxonomy(session)
        await session.commit()
    if consecutive_failures >= MAX_CONSECUTIVE_PROVIDER_FAILURES:
        raise ProviderCircuitOpen()
    # Import here: the API service can enqueue jobs without an import cycle.
    from app.catalog_review.service import record_enrichment

    for offset in range(0, len(item_ids), ENRICH_BATCH_SIZE):
        batch_ids = item_ids[offset : offset + ENRICH_BATCH_SIZE]
        sources_by_item: dict[UUID, list[EvidenceSource]] = {}
        try:
            async with SessionFactory() as session:
                await _locked_run(session, run_id, token)
                items = await _refresh_enrichment_batch(session, run_id, batch_ids)
                await session.commit()
            if not items:
                continue
            profiles = {item.id: destination_for_id(item.destination_id) for item in items}
            try:
                evidence = await provider.enrich_search(
                    [merchant_prompt_context(item, profiles[item.id]) for item in items]
                )
            finally:
                await _save_usage(run_id, token, provider, saved_usage)
            titles = {str(entry["source_url"]): str(entry.get("title") or "") for entry in evidence}
            known = {item.id: source_urls(item.snapshot_json or {}) for item in items}
            urls = list(
                dict.fromkeys([*titles, *(url for values in known.values() for url in values)])
            )[:MAX_URLS]
            fetched = await fetch_sources(urls, hosts) if urls else []
            by_url = {normalize_source_url(source.url) or source.url: source for source in fetched}
            verified: dict[str, list[VerifiedCandidate]] = {}
            area_slugs: dict[str, list[str]] = {}
            candidates: list[ReviewCandidate] = []
            for item in items:
                snapshot = item.snapshot_json or {}
                pages = verify_candidates(snapshot, fetched, titles, profiles[item.id], hosts)
                verified[str(item.id)] = pages
                area_slugs[str(item.id)] = taxonomy.area_slugs(item.destination_id)
                sources_by_item[item.id] = _enrichment_sources(known[item.id], pages, by_url)
                candidates.append(
                    ReviewCandidate(
                        candidate_id=str(item.id),
                        kind="merchant",
                        name=item.name,
                        local_name=str(snapshot.get("local_name") or ""),
                        destination_id=item.destination_id,
                        data=snapshot,
                        sources=sources_by_item[item.id],
                    )
                )
            results: dict[str, VerifiedEnrichment] = {}
            if any(
                source.fetched and source.text
                for sources in sources_by_item.values()
                for source in sources
            ):
                try:
                    results = await provider.enrich_assess(
                        candidates,
                        verified=verified,
                        area_slugs=area_slugs,
                        catalog=taxonomy.prompt_catalog(
                            {item.destination_id for item in items if item.destination_id}
                        ),
                    )
                finally:
                    await _save_usage(run_id, token, provider, saved_usage)
            async with SessionFactory() as session:
                run = await _locked_run(session, run_id, token)
                current = (
                    await session.scalars(
                        select(CatalogReviewItem)
                        .where(
                            CatalogReviewItem.run_id == run_id,
                            CatalogReviewItem.id.in_([item.id for item in items]),
                            CatalogReviewItem.status.in_(("pending", "error")),
                        )
                        .with_for_update()
                    )
                ).all()
                for item in current:
                    outcome = results.get(str(item.id))
                    identify = _identify_context(item, matched_ids)
                    if outcome is None:
                        record_enrichment(
                            item,
                            EnrichmentAssessment(
                                candidate_id=str(item.id), confidence=0.0, reason=NO_PAGES_REASON
                            ),
                            [],
                            sources_by_item.get(item.id, []),
                            identify=identify,
                        )
                    else:
                        record_enrichment(
                            item,
                            outcome.assessment,
                            outcome.corrections,
                            sources_by_item.get(item.id, []),
                            identify=identify,
                        )
                run.result_json = {
                    **(run.result_json or {}),
                    "consecutive_provider_failures": 0,
                    "last_enrichment_diagnostics": dict(
                        getattr(provider, "enrichment_diagnostics", {})
                    ),
                }
                await session.commit()
            consecutive_failures = 0
        except (BudgetStopped, LeaseLost):
            raise
        except Exception as exc:
            if isinstance(exc, CatalogAssessmentError):
                consecutive_failures += 1
            await _batch_error(run_id, token, batch_ids, exc, sources_by_item, consecutive_failures)
            if consecutive_failures >= MAX_CONSECUTIVE_PROVIDER_FAILURES:
                raise ProviderCircuitOpen() from exc


async def _finish(
    run_id: UUID,
    token: str,
    *,
    error_code: str | None = None,
    error_message: str | None = None,
    failed: bool = False,
) -> None:
    async with SessionFactory() as session:
        run = await _locked_run(session, run_id, token)
        items = (
            await session.scalars(
                select(CatalogReviewItem).where(
                    CatalogReviewItem.run_id == run_id,
                    CatalogReviewItem.kind.in_(SCOPE_KINDS[request_scope(run.request_json)]),
                )
            )
        ).all()
        statuses = dict(Counter(item.status for item in items))
        result = dict(run.result_json or {})
        shortfalls = (
            {
                kind: max(0, target - _count((result.get("created_counts") or {}).get(kind)))
                for kind, target in _targets(run.request_json or {}).items()
            }
            if run.mode == "discover_new"
            else {}
        )
        incomplete = bool(
            error_code
            or statuses.get("pending")
            or statuses.get("error")
            or any(shortfalls.values())
        )
        progressed = any(item.status in {"assessed", "applied", "stale"} for item in items)
        progressed |= any(_count(value) for value in (result.get("created_counts") or {}).values())
        run.status = (
            "failed" if failed and not progressed else "partial" if incomplete else "completed"
        )
        result.update(item_status_counts=statuses, shortfalls=shortfalls)
        run.result_json = result
        run.usage_json = {**(run.usage_json or {}), "member_charged": False}
        run.error_code = error_code or ("catalog_review_incomplete" if incomplete else None)
        run.error_message = error_message or (
            "部分項目待續跑或未找到足夠新候選。" if incomplete else None
        )
        if error_code == "catalog_review_provider_circuit_open":
            for item in items:
                if item.status == "pending":
                    item.reason = "Gemini 連續評估失敗，已暫停後續項目；請確認原因後明確續跑。"
        run.completed_at = datetime.now(UTC)
        run.lease_token = None
        run.lease_until = None
        run.version += 1
        await session.commit()


async def _run(run_id: UUID) -> None:
    run = await _claim_run(run_id)
    if run is None:
        return
    token = cast(str, run.lease_token)
    heartbeat = asyncio.create_task(_heartbeat(run_id, token))
    provider: CatalogGeminiProvider | None = None
    saved_usage: dict[str, int] = {}
    try:
        async with SessionFactory() as session:
            settings = await load_runtime_settings(session)
            hosts = await trusted_hosts(session)
        provider = CatalogGeminiProvider(
            settings,
            lambda: reserve_call(run_id, token, settings),
            trusted_hosts=hosts,
            model=run.model,
        )
        if run.mode == ENRICH_MODE:
            await _identify_items(run_id, token, settings)
            await _enrich_items(run_id, token, provider, hosts, saved_usage)
        else:
            if run.mode == "discover_new":
                await _discover_items(run_id, token, provider, saved_usage)
            phase = "review_new" if run.mode == "discover_new" else "review_pending"
            await _review_items(run_id, token, phase, provider, hosts, saved_usage)
        await _finish(run_id, token)
    except LeaseLost:
        logger.info("Catalog review %s stopped after losing its lease", run_id)
    except BudgetStopped as exc:
        with suppress(LeaseLost):
            await _finish(
                run_id,
                token,
                error_code=exc.code,
                error_message=(
                    "此工作已達累計 Gemini 呼叫上限；進度已保存，"
                    "可在後台調整上限，再明確確認以新上限續跑。"
                    if exc.code == "catalog_review_call_limit"
                    else "Gemini 每日安全預算已用完；進度已保存，可於預算重置後續跑。"
                ),
            )
    except ProviderCircuitOpen:
        with suppress(LeaseLost):
            await _finish(
                run_id,
                token,
                error_code="catalog_review_provider_circuit_open",
                error_message=(
                    "Gemini 連續三批失敗，已停止本次執行並保存進度；"
                    "請查看安全診斷，確認原因後再續跑。"
                ),
            )
    except Exception as exc:
        with suppress(LeaseLost):
            await _finish(
                run_id,
                token,
                error_code=(exc.code if isinstance(exc, AppError) else "catalog_review_failed"),
                error_message="審核工作未完成；已保存進度，可由管理員續跑。",
                failed=True,
            )
    finally:
        heartbeat.cancel()
        with suppress(asyncio.CancelledError):
            await heartbeat
        if provider is not None:
            await provider.close()


def enqueue_catalog_run(run_id: UUID) -> str:
    connection = SyncRedis.from_url(get_settings().redis_url)
    try:
        job = Queue("catalog-review", connection=connection).enqueue(
            "app.catalog_review.jobs.run_catalog_review",
            str(run_id),
            job_timeout=7200,
        )
        return str(job.id)
    finally:
        connection.close()


def run_catalog_review(run_id: str) -> None:
    async def run_and_close_resources() -> None:
        try:
            await _run(UUID(run_id))
        finally:
            try:
                await get_redis().aclose()
            finally:
                get_redis.cache_clear()
                await engine.dispose()

    asyncio.run(run_and_close_resources())
