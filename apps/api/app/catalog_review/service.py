from __future__ import annotations

from collections.abc import Collection
from datetime import UTC, datetime, timedelta
from typing import Any, Literal, cast
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, model_validator
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.catalog_review.budget import DEFAULT_MAX_CALLS, MAX_CONFIGURED_CALLS, run_call_limit
from app.catalog_review.errors import ERROR_CODES
from app.catalog_review.repository import (
    ENTITY_TYPES,
    Entity,
    entity_snapshot,
    fingerprint,
    load_entity,
    make_review_item,
    publication_gaps,
    trusted_hosts,
)
from app.catalog_review.schemas import EnrichmentAssessment, EvidenceSource, ReviewAssessment
from app.catalog_review.scope import SCOPE_KINDS, CatalogScope, request_scope, scope_counts
from app.config import Settings
from app.destinations.catalog import destination_for_id
from app.foods.enrichment import (
    EnrichmentOrigin,
    apply_merchant_enrichment,
    proposal_from_corrections,
)
from app.models import (
    AdminAuditLog,
    CatalogReviewItem,
    CatalogReviewRun,
    FoodLocalization,
    FoodMerchant,
    TravelFood,
)
from app.problems import AppError

ACTIVE = {"queued", "running"}
COUNTS = {"hotspot": 40, "food": 20, "merchant": 40}
LEGACY_OMISSION_REASON = "Gemini 未回傳此候選的評估；保留待審。"
ENRICH_MODE = "enrich_merchants"
#: Items of an enrichment run keep this phase; the run itself moves identify → enrich.
ENRICH_PHASE = "enrich_merchants"
ENRICH_ONLY_FIELDS = ("destination_ids", "limit", "identify_places")
MAX_ENRICH_LIMIT = 500


class StartRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["review_pending", "discover_new", "enrich_merchants"]
    scope: CatalogScope = "all"
    prior_review_run_id: UUID | None = None
    requested_counts: dict[str, StrictInt] = Field(default_factory=lambda: dict(COUNTS))
    max_calls: StrictInt = Field(default=DEFAULT_MAX_CALLS, ge=1, le=MAX_CONFIGURED_CALLS)
    # Enrichment only: which pending merchants to snapshot, and whether to spend Google
    # Text Search calls on the rows that still lack a Place ID.
    destination_ids: list[str] = Field(default_factory=list, max_length=20)
    limit: StrictInt | None = Field(default=None, ge=1, le=MAX_ENRICH_LIMIT)
    identify_places: StrictBool = True

    @model_validator(mode="after")
    def validate_counts(self) -> StartRequest:
        if self.mode == ENRICH_MODE:
            self.destination_ids = list(
                dict.fromkeys(item.strip().casefold() for item in self.destination_ids)
            )
            unknown = [item for item in self.destination_ids if destination_for_id(item) is None]
            if unknown:
                raise ValueError(f"未知的目的地：{', '.join(unknown)}")
        elif self.destination_ids or self.limit is not None or not self.identify_places:
            raise ValueError("僅補齊店家資料模式可設定 destination_ids、limit 或 identify_places")
        if "requested_counts" not in self.model_fields_set:
            self.requested_counts = scope_counts(self.scope)
        if (
            set(self.requested_counts) != set(COUNTS)
            or any(
                isinstance(value, bool) or not 0 <= value <= 100
                for value in self.requested_counts.values()
            )
            or not 1 <= sum(self.requested_counts.values()) <= 100
        ):
            raise ValueError("新增目標須包含三種類型，合計 1 至 100 筆")
        if any(
            value and kind not in SCOPE_KINDS[self.scope]
            for kind, value in self.requested_counts.items()
        ):
            raise ValueError("新增目標不可包含審核範圍以外的類型")
        return self


def request_document(payload: StartRequest, *, exclude: Collection[str] = ()) -> dict[str, Any]:
    """The request as it is hashed and stored.

    Review and discovery hashes must stay byte-identical to what older runs stored, or an
    honest retry of an old request would be refused as an idempotency conflict; so the
    enrichment-only fields exist in the document only for the enrichment mode.
    """
    document = payload.model_dump(mode="json", exclude=set(exclude))
    if payload.mode != ENRICH_MODE:
        for key in ENRICH_ONLY_FIELDS:
            document.pop(key, None)
    return document


class ResumeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expected_version: StrictInt = Field(ge=1)
    max_calls: StrictInt = Field(ge=1, le=MAX_CONFIGURED_CALLS)


class ApplyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    item_ids: list[UUID] = Field(min_length=1, max_length=100)
    action: Literal["approve", "reject", "keep_pending", "apply_corrections"]
    expected_version: int = Field(ge=1)


def utc(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def record_assessment(
    item: CatalogReviewItem, assessment: ReviewAssessment, sources: list[EvidenceSource]
) -> None:
    """A model recommendation is not an identity/coordinate verification operation."""
    if assessment.candidate_id != str(item.id):
        raise ValueError("assessment id does not match snapshot item")
    by_url = {source.url: source for source in sources if source.fetched and source.trusted}
    valid_citations = [
        entry
        for entry in assessment.evidence
        if entry.url in by_url and entry.quote.strip() and entry.quote in by_url[entry.url].text
    ]
    gaps = publication_gaps(item.kind, item.snapshot_json)
    if not valid_citations:
        gaps.append("missing_verified_source_evidence")
    if assessment.confidence < 0.9:
        gaps.append("low_assessment_confidence")
    item.assessment_json = assessment.model_dump(mode="json")
    item.evidence_json = [source.model_dump(mode="json", exclude={"text"}) for source in sources]
    item.gaps_json = list(dict.fromkeys(gaps))
    decision = assessment.decision
    # Even a forged/future worker response cannot bypass these publication gates.
    if not valid_citations or assessment.confidence < 0.9 or (decision == "approve" and gaps):
        decision = "needs_review"
    item.decision = decision
    item.reason = assessment.reason
    item.assessment_json["evidence"] = [entry.model_dump() for entry in valid_citations]
    item.status = "assessed"
    item.assessed_at = datetime.now(UTC)


def record_enrichment(
    item: CatalogReviewItem,
    assessment: EnrichmentAssessment,
    corrections: list[dict[str, Any]],
    sources: list[EvidenceSource],
    *,
    identify: dict[str, Any] | None = None,
) -> None:
    """Store what the server could re-check; an enrichment never approves or rejects.

    ``corrections`` are the entries ``verified_corrections`` accepted, each with its
    ``kind``; the stored ``evidence`` list is derived from them so the existing evidence
    column keeps rendering. ``identify`` records what the Google phase did for this row.
    """
    if assessment.candidate_id != str(item.id):
        raise ValueError("assessment id does not match snapshot item")
    evidence = list(
        {
            (str(entry["source_url"]), str(entry["quote"])): {
                "url": str(entry["source_url"]),
                "quote": str(entry["quote"]),
            }
            for entry in corrections
        }.values()
    )[:10]
    item.assessment_json = {
        "candidate_id": assessment.candidate_id,
        "decision": "needs_review",
        "confidence": assessment.confidence,
        "reason": assessment.reason,
        "corrections": [dict(entry) for entry in corrections],
        "evidence": evidence,
        "identify": dict(identify or {}),
    }
    item.evidence_json = [source.model_dump(mode="json", exclude={"text"}) for source in sources]
    item.gaps_json = publication_gaps(item.kind, item.snapshot_json)
    item.decision = "needs_review"
    item.reason = assessment.reason
    item.status = "assessed"
    item.assessed_at = datetime.now(UTC)


def item_corrections(item: CatalogReviewItem) -> list[dict[str, Any]]:
    """The verified corrections of an enrichment item; review items store a dict here."""
    corrections = (item.assessment_json or {}).get("corrections")
    if not isinstance(corrections, list):
        return []
    return [entry for entry in corrections if isinstance(entry, dict)]


def is_legacy_missing_assessment(item: CatalogReviewItem) -> bool:
    """Recognize only the old adapter's synthetic omission, not a model's uncertainty."""
    assessment = item.assessment_json or {}
    confidence = assessment.get("confidence")
    return (
        item.status == "assessed"
        and item.applied_action is None
        and item.decision == "needs_review"
        and item.reason == LEGACY_OMISSION_REASON
        and assessment.get("candidate_id") == str(item.id)
        and assessment.get("decision") == "needs_review"
        and isinstance(confidence, (int, float))
        and not isinstance(confidence, bool)
        and confidence == 0
        and assessment.get("reason") == LEGACY_OMISSION_REASON
        and assessment.get("evidence") == []
        and assessment.get("corrections") == {}
    )


def allowed_actions(item: CatalogReviewItem) -> list[str]:
    if item.status != "assessed" or is_legacy_missing_assessment(item):
        return []
    if item.phase == ENRICH_PHASE:
        # Enrichment fills fields; approving or rejecting stays with the ordinary review.
        return ["apply_corrections", "keep_pending"] if item_corrections(item) else ["keep_pending"]
    actions = ["keep_pending"]
    if item.decision == "approve" and not item.gaps_json:
        actions.insert(0, "approve")
    if item.decision == "reject" and (item.assessment_json or {}).get("evidence"):
        actions.insert(0, "reject")
    return actions


def item_view(item: CatalogReviewItem) -> dict[str, Any]:
    missing = is_legacy_missing_assessment(item)
    # Legacy batches recorded only the exception class. Do not invent a more
    # specific cause or expose arbitrary stored diagnostics to the browser.
    code = (item.assessment_json or {}).get("code")
    error_code = (
        "catalog_response_ids_invalid"
        if missing
        else code
        if item.status == "error" and isinstance(code, str) and code in ERROR_CODES
        else None
    )
    return {
        "id": str(item.id),
        "kind": item.kind,
        "entity_id": str(item.entity_id),
        "name": item.name,
        "destination_id": item.destination_id,
        "phase": item.phase,
        "decision": None if missing else item.decision,
        "reason": item.reason or "",
        "evidence": (item.assessment_json or {}).get("evidence", []),
        "gaps": item.gaps_json or [],
        "allowed_actions": allowed_actions(item),
        "applied_action": item.applied_action,
        "status": "error" if missing else item.status,
        "confidence": None if missing else (item.assessment_json or {}).get("confidence"),
        "error_code": error_code,
        "corrections": [
            {key: entry.get(key) for key in ("field", "value", "source_url", "quote", "kind")}
            for entry in item_corrections(item)
        ],
        "identify": (item.assessment_json or {}).get("identify") or None,
    }


async def run_items(
    session: AsyncSession, run_id: UUID, *, scope: CatalogScope = "all"
) -> list[CatalogReviewItem]:
    return list(
        (
            await session.scalars(
                select(CatalogReviewItem)
                .where(
                    CatalogReviewItem.run_id == run_id,
                    CatalogReviewItem.kind.in_(SCOPE_KINDS[scope]),
                )
                .order_by(CatalogReviewItem.created_at, CatalogReviewItem.id)
            )
        ).all()
    )


def snapshot_review_complete(items: list[CatalogReviewItem]) -> bool:
    return all(
        item.status in {"assessed", "applied", "stale"} and not is_legacy_missing_assessment(item)
        for item in items
    )


def resumable_state(run: CatalogReviewRun, status: str) -> bool:
    """Stopped work or an orphan is recoverable, but a live worker never is."""
    now = datetime.now(UTC)
    return (
        status in {"partial", "failed"}
        or (run.status in ACTIVE and run.lease_until is not None and utc(run.lease_until) < now)
        or (
            run.status == "queued"
            and run.lease_until is None
            and run.updated_at is not None
            and utc(run.updated_at) < now - timedelta(minutes=5)
        )
    )


async def run_view(
    session: AsyncSession, run: CatalogReviewRun, settings: Settings | None = None
) -> dict[str, Any]:
    scope = request_scope(run.request_json)
    items = await run_items(session, run.id, scope=scope)
    created = (run.result_json or {}).get("created_counts", {})
    usage = run.usage_json or {}
    missing_ids = {item.id for item in items if is_legacy_missing_assessment(item)}
    legacy_partial = run.status == "completed" and bool(missing_ids)
    status = "partial" if legacy_partial else run.status
    review_complete = run.status not in ACTIVE and snapshot_review_complete(items)
    return {
        "id": str(run.id),
        "scope": scope,
        "version": run.version,
        "mode": run.mode,
        "phase": run.phase,
        "status": status,
        "model": run.model,
        "max_calls": run_call_limit(run.request_json),
        "can_extend_budget": (
            settings is not None
            and resumable_state(run, status)
            and settings.catalog_review_max_calls
            > max(run_call_limit(run.request_json), int(usage.get("calls", 0)))
        ),
        "requested_counts": (run.request_json or {}).get("requested_counts", scope_counts(scope)),
        "counts": {
            "total": len(items),
            "assessed": sum(
                item.status in {"assessed", "applied", "stale"} and item.id not in missing_ids
                for item in items
            ),
            "approved": sum(item.decision == "approve" for item in items),
            "rejected": sum(item.decision == "reject" for item in items),
            "needs_review": sum(
                item.decision == "needs_review" and item.id not in missing_ids for item in items
            ),
            "created": sum(created.get(kind, 0) for kind in SCOPE_KINDS[scope]),
            "duplicates": int((run.result_json or {}).get("duplicates", 0)),
            "failed": sum(item.status == "error" or item.id in missing_ids for item in items),
            "applied": sum(item.status == "applied" for item in items),
        },
        "usage": {
            "calls": int(usage.get("calls", 0)),
            "input_tokens": int(usage.get("input_tokens", 0)),
            "output_tokens": int(usage.get("output_tokens", 0)),
            "thought_tokens": int(usage.get("thought_tokens", 0)),
        },
        "error_code": "catalog_response_ids_invalid" if legacy_partial else run.error_code,
        "error_message": (
            "部分候選尚未取得 Gemini 評估，請明確續跑以補齊缺漏。"
            if legacy_partial
            else run.error_message
        ),
        "enrichment": (
            {
                "identify": (run.result_json or {}).get("identify"),
                "items_with_corrections": sum(bool(item_corrections(item)) for item in items),
                "corrections": sum(len(item_corrections(item)) for item in items),
            }
            if run.mode == ENRICH_MODE
            else None
        ),
        "created_at": run.created_at,
        "completed_at": run.completed_at,
        "review_complete": review_complete,
        "can_resume": (
            resumable_state(run, status)
            and int(usage.get("calls", 0)) < run_call_limit(run.request_json)
        ),
    }


async def get_run(
    session: AsyncSession, run_id: UUID, *, lock: bool = False, scope: CatalogScope | None = None
) -> CatalogReviewRun:
    statement = select(CatalogReviewRun).where(CatalogReviewRun.id == run_id)
    if lock:
        statement = statement.with_for_update()
    run = await session.scalar(statement)
    if run is None:
        raise AppError(404, "catalog_run_not_found", "找不到這次目錄審核")
    if scope is not None and request_scope(run.request_json) != scope:
        raise AppError(409, "catalog_scope_mismatch", "此工作不屬於目前審核範圍，請回工作歷史查看")
    return run


async def overview(
    session: AsyncSession, settings: Settings, scope: CatalogScope | None = None
) -> dict[str, Any]:
    pending = {}
    for kind, model in ENTITY_TYPES.items():
        if kind not in SCOPE_KINDS[scope or "all"]:
            pending[kind] = 0
            continue
        pending[kind] = int(
            await session.scalar(
                select(func.count()).select_from(model).where(model.review_status == "pending")
            )
            or 0
        )
    pending["total"] = sum(pending.values())
    history = select(CatalogReviewRun)
    if scope is not None:
        history = history.where(
            func.coalesce(CatalogReviewRun.request_json["scope"].as_string(), "all") == scope
        )
    rows = list(
        (
            await session.scalars(history.order_by(CatalogReviewRun.created_at.desc()).limit(20))
        ).all()
    )
    views = [await run_view(session, row, settings) for row in rows]
    active_run = await session.scalar(
        select(CatalogReviewRun).where(CatalogReviewRun.status.in_(ACTIVE)).limit(1)
    )
    if (
        active_run is not None
        and (scope is None or request_scope(active_run.request_json) == scope)
        and all(row.id != active_run.id for row in rows)
    ):
        views.insert(0, await run_view(session, active_run, settings))
    configured = bool(settings.hotspot_guide_gemini_api_key)
    can_discover = any(
        view["mode"] == "review_pending"
        and view["review_complete"]
        and view["scope"] == (scope or "all")
        for view in views
    )
    reasons = []
    if not configured:
        reasons.append("gemini_not_configured")
    if active_run is not None:
        reasons.append("catalog_run_in_progress")
    return {
        "configured": configured,
        "scope": scope,
        "active_run": {
            "id": str(active_run.id),
            "scope": request_scope(active_run.request_json),
            "status": active_run.status,
        }
        if active_run is not None
        else None,
        "model": settings.hotspot_guide_gemini_model,
        "daily_call_limit": settings.hotspot_guide_gemini_daily_search_budget,
        "run_call_limit": settings.catalog_review_max_calls,
        "pending_counts": pending,
        "can_start_review": configured and active_run is None,
        "can_start_discovery": configured and active_run is None and can_discover,
        "can_start_enrichment": configured and active_run is None and scope == "foods",
        "blocking_reasons": reasons,
        "runs": views,
    }


async def _pending_merchants_for_enrichment(
    session: AsyncSession, *, destination_ids: list[str], limit: int | None
) -> list[FoodMerchant]:
    statement = select(FoodMerchant).where(FoodMerchant.review_status == "pending")
    if destination_ids:
        statement = statement.where(FoodMerchant.destination_id.in_(destination_ids))
    statement = statement.order_by(
        FoodMerchant.destination_id,
        FoodMerchant.display_order,
        FoodMerchant.name,
        FoodMerchant.id,
    )
    if limit:
        statement = statement.limit(limit)
    return list((await session.scalars(statement)).all())


async def _apply_corrections(
    session: AsyncSession,
    run: CatalogReviewRun,
    item: CatalogReviewItem,
    merchant: FoodMerchant,
    actor_id: UUID,
) -> dict[str, Any]:
    """Write an enrichment item's verified corrections through the shared merchant writer.

    The writer refuses anything the admin editor would refuse; a refusal skips this one
    item with the writer's error code and leaves the other selected items untouched.
    """
    corrections = item_corrections(item)
    skipped: dict[str, Any] = {
        "id": str(item.id),
        "action": "apply_corrections",
        "status": "skipped",
    }
    try:
        proposal = proposal_from_corrections(corrections)
    except AppError as exc:
        return {**skipped, "reason": exc.code}
    except ValueError:
        return {**skipped, "reason": "catalog_corrections_invalid"}
    try:
        # The writer validates before its first write, so a refusal leaves nothing
        # behind; a SAVEPOINT here would flush the caller's pending rows first.
        outcome = await apply_merchant_enrichment(
            session,
            merchant,
            proposal,
            actor_id=actor_id,
            origin=EnrichmentOrigin(kind="catalog_review", reference=f"{run.id}/{item.id}"),
            evidence=[
                {
                    "field": entry.get("field"),
                    "source_url": entry.get("source_url"),
                    "quote": entry.get("quote"),
                }
                for entry in corrections
            ],
            trusted_hosts=await trusted_hosts(session),
        )
    except AppError as exc:
        return {**skipped, "reason": exc.code}
    item.applied_action = "apply_corrections"
    item.status = "applied"
    return {
        "id": str(item.id),
        "action": "apply_corrections",
        "status": "applied",
        "reason": item.reason,
        "changes": dict(outcome.applied),
        "skipped_fields": dict(outcome.skipped),
    }


async def _serialize_starts(session: AsyncSession) -> None:
    # A database transaction lock also covers concurrent requests from other processes.
    if session.get_bind().dialect.name == "postgresql":
        await session.execute(text("SELECT pg_advisory_xact_lock(793654312)"))


async def create_run(
    session: AsyncSession,
    settings: Settings,
    actor_id: UUID,
    payload: StartRequest,
    idempotency_key: str,
) -> tuple[CatalogReviewRun, bool]:
    await _serialize_starts(session)
    request_json = request_document(payload)
    request_json["max_calls_source"] = (
        "explicit" if "max_calls" in payload.model_fields_set else "configured_default"
    )
    digest = fingerprint(request_json)
    existing = await session.scalar(
        select(CatalogReviewRun).where(
            CatalogReviewRun.actor_user_id == actor_id,
            CatalogReviewRun.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        legacy_request = {
            key: value for key, value in request_json.items() if key != "max_calls_source"
        }
        legacy_retry = "max_calls_source" not in (existing.request_json or {}) and (
            existing.request_hash == fingerprint(legacy_request)
            or (
                payload.scope == "all"
                and "scope" not in (existing.request_json or {})
                and existing.request_hash
                == fingerprint(
                    {key: value for key, value in legacy_request.items() if key != "scope"}
                )
            )
        )
        if existing.request_hash != digest and not legacy_retry:
            raise AppError(409, "idempotency_conflict", "相同冪等鍵不能建立不同的審核工作")
        return existing, False
    if not settings.hotspot_guide_gemini_api_key:
        raise AppError(422, "gemini_not_configured", "請先在後台設定 Gemini API Key")
    maximum = (
        payload.max_calls
        if "max_calls" in payload.model_fields_set
        else settings.catalog_review_max_calls
    )
    if maximum > settings.catalog_review_max_calls:
        raise AppError(422, "validation_error", "本批呼叫上限超過目前後台設定，請重新整理")
    # Hash the submitted request, not the mutable setting. Retrying an uncertain
    # start returns the original run even if the default was changed meanwhile.
    request_json["max_calls"] = maximum
    if await session.scalar(
        select(CatalogReviewRun.id).where(CatalogReviewRun.status.in_(ACTIVE)).limit(1)
    ):
        raise AppError(409, "catalog_run_in_progress", "已有目錄審核執行中，請先查看或續跑")
    if payload.mode == "discover_new":
        if payload.prior_review_run_id is None:
            raise AppError(422, "catalog_review_required", "新增前必須先完成既有待審資料的評估")
        prior = await get_run(session, payload.prior_review_run_id, scope=payload.scope)
        if (
            prior.mode != "review_pending"
            or prior.status in ACTIVE
            or not (await run_view(session, prior))["review_complete"]
        ):
            raise AppError(409, "catalog_review_incomplete", "前一階段尚未評估完所有快照項目")
    merchants: list[FoodMerchant] = []
    if payload.mode == ENRICH_MODE:
        if payload.scope != "foods":
            raise AppError(422, "catalog_scope_invalid", "補齊店家資料只支援美食範圍")
        merchants = await _pending_merchants_for_enrichment(
            session, destination_ids=payload.destination_ids, limit=payload.limit
        )
        if not merchants:
            raise AppError(422, "catalog_enrichment_nothing_pending", "目前沒有符合條件的待審店家")
    run = CatalogReviewRun(
        id=uuid4(),
        actor_user_id=actor_id,
        idempotency_key=idempotency_key,
        request_hash=digest,
        request_json=request_json,
        mode=payload.mode,
        phase=payload.mode,
        status="queued",
        version=1,
        model=settings.hotspot_guide_gemini_model,
        usage_json={"calls": 0, "input_tokens": 0, "output_tokens": 0},
        result_json={},
    )
    session.add(run)
    await session.flush()
    if payload.mode == "review_pending":
        for kind, model in ENTITY_TYPES.items():
            if kind not in SCOPE_KINDS[payload.scope]:
                continue
            rows = (
                await session.scalars(
                    select(model).where(model.review_status == "pending").order_by(model.id)
                )
            ).all()
            for row in rows:
                await make_review_item(session, run.id, kind, cast(Entity, row), "review_pending")
    elif payload.mode == ENRICH_MODE:
        for merchant in merchants:
            await make_review_item(session, run.id, "merchant", merchant, ENRICH_PHASE)
    session.add(
        AdminAuditLog(
            actor_user_id=actor_id,
            action="catalog_review_requested",
            target=f"catalog-review:{run.id}",
            metadata_json={
                "mode": payload.mode,
                "scope": payload.scope,
                "requested_counts": payload.requested_counts,
                "model": run.model,
                "max_calls": maximum,
                **(
                    {
                        "destination_ids": payload.destination_ids,
                        "limit": payload.limit,
                        "identify_places": payload.identify_places,
                        "snapshot_count": len(merchants),
                    }
                    if payload.mode == ENRICH_MODE
                    else {}
                ),
            },
        )
    )
    await session.commit()
    return run, True


async def prepare_resume(
    session: AsyncSession,
    run_id: UUID,
    actor_id: UUID,
    *,
    scope: CatalogScope | None = None,
    payload: ResumeRequest | None = None,
    settings: Settings | None = None,
) -> CatalogReviewRun:
    await _serialize_starts(session)
    run = await get_run(session, run_id, lock=True, scope=scope)
    view = await run_view(session, run, settings)
    previous_limit = run_call_limit(run.request_json)
    if payload is not None:
        if payload.expected_version != run.version:
            raise AppError(409, "catalog_version_conflict", "工作狀態已改變，請重新讀取審核預覽")
        if settings is None or payload.max_calls > settings.catalog_review_max_calls:
            raise AppError(422, "validation_error", "本批呼叫上限超過目前後台設定，請重新整理")
        if payload.max_calls <= max(previous_limit, int((run.usage_json or {}).get("calls", 0))):
            raise AppError(422, "catalog_run_not_resumable", "新上限必須高於原上限與累計用量")
        if not resumable_state(run, view["status"]):
            raise AppError(
                409, "catalog_run_not_resumable", "只能明確提高已停止或失聯工作的呼叫上限"
            )
    elif not view["can_resume"]:
        raise AppError(409, "catalog_run_not_resumable", "目前工作不能續跑，或已達單次工作呼叫上限")
    if await session.scalar(
        select(CatalogReviewRun.id)
        .where(CatalogReviewRun.id != run_id, CatalogReviewRun.status.in_(ACTIVE))
        .limit(1)
    ):
        raise AppError(409, "catalog_run_in_progress", "已有其他目錄審核執行中")
    if payload is not None:
        run.request_json = {**(run.request_json or {}), "max_calls": payload.max_calls}
    retried_items = 0
    legacy_missing_items = 0
    stale_items = 0
    for item in await run_items(session, run.id, scope=request_scope(run.request_json)):
        missing = is_legacy_missing_assessment(item)
        if missing:
            entity = await load_entity(session, item.kind, item.entity_id, lock=True)
            if (
                entity is None
                or entity.review_status != "pending"
                or fingerprint(await entity_snapshot(session, entity)) != item.snapshot_hash
            ):
                item.status = "stale"
                stale_items += 1
                continue
        if item.status == "error" or missing:
            retried_items += 1
            legacy_missing_items += int(missing)
            item.status = "pending"
            item.decision = None
            item.reason = ""
            item.assessment_json = {}
            item.gaps_json = []
            item.assessed_at = None
    run.status = "queued"
    run.lease_token = None
    run.lease_until = None
    run.error_code = None
    run.error_message = None
    run.completed_at = None
    run.version += 1
    session.add(
        AdminAuditLog(
            actor_user_id=actor_id,
            action="catalog_review_resumed",
            target=f"catalog-review:{run.id}",
            metadata_json={
                "retried_items": retried_items,
                "legacy_missing_items": legacy_missing_items,
                "stale_items": stale_items,
                "previous_max_calls": previous_limit,
                "max_calls": run_call_limit(run.request_json),
                "calls": int((run.usage_json or {}).get("calls", 0)),
            },
        )
    )
    await session.commit()
    return run


async def apply_decisions(
    session: AsyncSession,
    run_id: UUID,
    actor_id: UUID,
    payload: ApplyRequest,
    idempotency_key: str,
    *,
    scope: CatalogScope | None = None,
) -> dict[str, Any]:
    run = await get_run(session, run_id, lock=True, scope=scope)
    receipt_key = fingerprint({"actor": str(actor_id), "key": idempotency_key})
    digest = fingerprint(payload.model_dump(mode="json"))
    receipts = dict((run.result_json or {}).get("apply_receipts", {}))
    prior = receipts.get(receipt_key)
    if prior:
        if prior["request_hash"] != digest:
            raise AppError(409, "idempotency_conflict", "相同冪等鍵不能套用不同結果")
        return {**prior["response"], "run": await run_view(session, run)}
    if run.status in ACTIVE or run.version != payload.expected_version:
        raise AppError(409, "catalog_version_conflict", "工作狀態已改變，請重新讀取審核預覽")
    if len(receipts) >= 1000:
        raise AppError(409, "catalog_receipt_limit", "此工作已達套用次數上限")
    requested = list(dict.fromkeys(payload.item_ids))
    rows = list(
        (
            await session.scalars(
                select(CatalogReviewItem)
                .where(
                    CatalogReviewItem.run_id == run.id,
                    CatalogReviewItem.id.in_(requested),
                    CatalogReviewItem.kind.in_(SCOPE_KINDS[request_scope(run.request_json)]),
                )
                .order_by(CatalogReviewItem.id)
                .with_for_update()
            )
        ).all()
    )
    if len(rows) != len(requested):
        raise AppError(422, "catalog_item_mismatch", "選取項目不屬於這次審核工作")
    outcomes = []
    now = datetime.now(UTC)
    for item in rows:
        reason = ""
        entity = await load_entity(session, item.kind, item.entity_id, lock=True)
        if payload.action not in allowed_actions(item):
            reason = "action_not_allowed"
        elif item.assessed_at is None or utc(item.assessed_at) < now - timedelta(days=7):
            reason = "assessment_expired"
        elif entity is None or entity.review_status != "pending":
            reason = "candidate_no_longer_pending"
        elif fingerprint(await entity_snapshot(session, entity)) != item.snapshot_hash:
            reason = "candidate_changed"
        elif payload.action == "approve" and publication_gaps(
            item.kind, await entity_snapshot(session, entity)
        ):
            reason = "publication_requirements_missing"
        if reason:
            outcomes.append(
                {
                    "id": str(item.id),
                    "action": payload.action,
                    "status": "skipped",
                    "reason": reason,
                }
            )
            continue
        assert entity is not None
        if payload.action == "apply_corrections":
            outcomes.append(
                await _apply_corrections(session, run, item, cast(FoodMerchant, entity), actor_id)
            )
            continue
        entity.review_status = {
            "approve": "approved",
            "reject": "rejected",
            "keep_pending": "pending",
        }[payload.action]
        if payload.action != "keep_pending":
            entity.is_active = payload.action == "approve"
        if isinstance(entity, TravelFood):
            entity.source = "admin"
            # These are the exact localizations included in the assessed snapshot.
            # Mark them reviewed too, so seed reruns cannot silently replace them.
            for localization in (
                await session.scalars(
                    select(FoodLocalization)
                    .where(FoodLocalization.food_id == entity.id)
                    .with_for_update()
                )
            ).all():
                localization.source = "admin"
        elif isinstance(entity, FoodMerchant):
            # This review does NOT vouch for maps or fill verified_at.
            pass
        else:
            entity.review_reason = item.reason
            entity.reviewed_at = now
            entity.reviewed_by_user_id = actor_id
        item.applied_action = payload.action
        item.status = "applied"
        session.add(
            AdminAuditLog(
                actor_user_id=actor_id,
                action="catalog_review_applied",
                target=f"{item.kind}:{item.entity_id}",
                metadata_json={
                    "run_id": str(run.id),
                    "item_id": str(item.id),
                    "action": payload.action,
                    "model": run.model,
                    "reason": item.reason,
                    "evidence": (item.assessment_json or {}).get("evidence", []),
                },
            )
        )
        outcomes.append(
            {
                "id": str(item.id),
                "action": payload.action,
                "status": "applied",
                "reason": item.reason,
            }
        )
    response = {"outcomes": outcomes, "updated": sum(o["status"] == "applied" for o in outcomes)}
    receipts[receipt_key] = {"request_hash": digest, "response": response}
    run.result_json = {**(run.result_json or {}), "apply_receipts": receipts}
    run.version += 1
    await session.commit()
    return {**response, "run": await run_view(session, run)}
