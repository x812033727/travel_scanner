from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, Literal, cast
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, StrictInt, model_validator
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.catalog_review.errors import ERROR_CODES
from app.catalog_review.repository import (
    ENTITY_TYPES,
    Entity,
    entity_snapshot,
    fingerprint,
    load_entity,
    make_review_item,
    publication_gaps,
)
from app.catalog_review.schemas import EvidenceSource, ReviewAssessment
from app.config import Settings
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


class StartRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["review_pending", "discover_new"]
    prior_review_run_id: UUID | None = None
    requested_counts: dict[str, StrictInt] = Field(default_factory=lambda: dict(COUNTS))
    max_calls: int = Field(default=80, ge=1, le=80)

    @model_validator(mode="after")
    def validate_counts(self) -> StartRequest:
        if (
            set(self.requested_counts) != set(COUNTS)
            or any(
                isinstance(value, bool) or not 0 <= value <= 100
                for value in self.requested_counts.values()
            )
            or not 1 <= sum(self.requested_counts.values()) <= 100
        ):
            raise ValueError("新增目標須包含三種類型，合計 1 至 100 筆")
        return self


class ApplyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    item_ids: list[UUID] = Field(min_length=1, max_length=100)
    action: Literal["approve", "reject", "keep_pending"]
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


def allowed_actions(item: CatalogReviewItem) -> list[str]:
    if item.status != "assessed":
        return []
    actions = ["keep_pending"]
    if item.decision == "approve" and not item.gaps_json:
        actions.insert(0, "approve")
    if item.decision == "reject" and (item.assessment_json or {}).get("evidence"):
        actions.insert(0, "reject")
    return actions


def item_view(item: CatalogReviewItem) -> dict[str, Any]:
    # Legacy batches recorded only the exception class. Do not invent a more
    # specific cause or expose arbitrary stored diagnostics to the browser.
    code = (item.assessment_json or {}).get("code")
    error_code = (
        code if item.status == "error" and isinstance(code, str) and code in ERROR_CODES else None
    )
    return {
        "id": str(item.id),
        "kind": item.kind,
        "entity_id": str(item.entity_id),
        "name": item.name,
        "destination_id": item.destination_id,
        "phase": item.phase,
        "decision": item.decision,
        "reason": item.reason or "",
        "evidence": (item.assessment_json or {}).get("evidence", []),
        "gaps": item.gaps_json or [],
        "allowed_actions": allowed_actions(item),
        "applied_action": item.applied_action,
        "status": item.status,
        "confidence": (item.assessment_json or {}).get("confidence"),
        "error_code": error_code,
    }


async def run_items(session: AsyncSession, run_id: UUID) -> list[CatalogReviewItem]:
    return list(
        (
            await session.scalars(
                select(CatalogReviewItem)
                .where(CatalogReviewItem.run_id == run_id)
                .order_by(CatalogReviewItem.created_at, CatalogReviewItem.id)
            )
        ).all()
    )


def snapshot_review_complete(items: list[CatalogReviewItem]) -> bool:
    return all(item.status in {"assessed", "applied", "stale"} for item in items)


async def run_view(session: AsyncSession, run: CatalogReviewRun) -> dict[str, Any]:
    items = await run_items(session, run.id)
    created = (run.result_json or {}).get("created_counts", {})
    usage = run.usage_json or {}
    review_complete = run.status not in ACTIVE and snapshot_review_complete(items)
    return {
        "id": str(run.id),
        "version": run.version,
        "mode": run.mode,
        "phase": run.phase,
        "status": run.status,
        "model": run.model,
        "requested_counts": (run.request_json or {}).get("requested_counts", COUNTS),
        "counts": {
            "total": len(items),
            "assessed": sum(item.status in {"assessed", "applied", "stale"} for item in items),
            "approved": sum(item.decision == "approve" for item in items),
            "rejected": sum(item.decision == "reject" for item in items),
            "needs_review": sum(item.decision == "needs_review" for item in items),
            "created": sum(created.values()),
            "duplicates": int((run.result_json or {}).get("duplicates", 0)),
            "failed": sum(item.status == "error" for item in items),
            "applied": sum(item.status == "applied" for item in items),
        },
        "usage": {
            "calls": int(usage.get("calls", 0)),
            "input_tokens": int(usage.get("input_tokens", 0)),
            "output_tokens": int(usage.get("output_tokens", 0)),
            "thought_tokens": int(usage.get("thought_tokens", 0)),
        },
        "error_code": run.error_code,
        "error_message": run.error_message,
        "created_at": run.created_at,
        "completed_at": run.completed_at,
        "review_complete": review_complete,
        "can_resume": (
            (
                run.status in {"partial", "failed"}
                or (
                    run.status in ACTIVE
                    and run.lease_until is not None
                    and utc(run.lease_until) < datetime.now(UTC)
                )
                or (
                    run.status == "queued"
                    and run.lease_until is None
                    and run.updated_at is not None
                    and utc(run.updated_at) < datetime.now(UTC) - timedelta(minutes=5)
                )
            )
            and int(usage.get("calls", 0)) < int(run.request_json.get("max_calls", 80))
        ),
    }


async def get_run(session: AsyncSession, run_id: UUID, *, lock: bool = False) -> CatalogReviewRun:
    statement = select(CatalogReviewRun).where(CatalogReviewRun.id == run_id)
    if lock:
        statement = statement.with_for_update()
    run = await session.scalar(statement)
    if run is None:
        raise AppError(404, "catalog_run_not_found", "找不到這次目錄審核")
    return run


async def overview(session: AsyncSession, settings: Settings) -> dict[str, Any]:
    pending = {}
    for kind, model in ENTITY_TYPES.items():
        pending[kind] = int(
            await session.scalar(
                select(func.count()).select_from(model).where(model.review_status == "pending")
            )
            or 0
        )
    pending["total"] = sum(pending.values())
    rows = list(
        (
            await session.scalars(
                select(CatalogReviewRun).order_by(CatalogReviewRun.created_at.desc()).limit(20)
            )
        ).all()
    )
    views = [await run_view(session, row) for row in rows]
    active = bool(
        await session.scalar(
            select(CatalogReviewRun.id).where(CatalogReviewRun.status.in_(ACTIVE)).limit(1)
        )
    )
    configured = bool(settings.hotspot_guide_gemini_api_key)
    can_discover = any(
        view["mode"] == "review_pending" and view["review_complete"] for view in views
    )
    reasons = []
    if not configured:
        reasons.append("gemini_not_configured")
    if active:
        reasons.append("catalog_run_in_progress")
    return {
        "configured": configured,
        "model": settings.hotspot_guide_gemini_model,
        "daily_call_limit": settings.hotspot_guide_gemini_daily_search_budget,
        "pending_counts": pending,
        "can_start_review": configured and not active,
        "can_start_discovery": configured and not active and can_discover,
        "blocking_reasons": reasons,
        "runs": views,
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
    request_json = payload.model_dump(mode="json")
    digest = fingerprint(request_json)
    existing = await session.scalar(
        select(CatalogReviewRun).where(
            CatalogReviewRun.actor_user_id == actor_id,
            CatalogReviewRun.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        if existing.request_hash != digest:
            raise AppError(409, "idempotency_conflict", "相同冪等鍵不能建立不同的審核工作")
        return existing, False
    if not settings.hotspot_guide_gemini_api_key:
        raise AppError(422, "gemini_not_configured", "請先在後台設定 Gemini API Key")
    if await session.scalar(
        select(CatalogReviewRun.id).where(CatalogReviewRun.status.in_(ACTIVE)).limit(1)
    ):
        raise AppError(409, "catalog_run_in_progress", "已有目錄審核執行中，請先查看或續跑")
    if payload.mode == "discover_new":
        if payload.prior_review_run_id is None:
            raise AppError(422, "catalog_review_required", "新增前必須先完成既有待審資料的評估")
        prior = await get_run(session, payload.prior_review_run_id)
        if (
            prior.mode != "review_pending"
            or prior.status in ACTIVE
            or not (await run_view(session, prior))["review_complete"]
        ):
            raise AppError(409, "catalog_review_incomplete", "前一階段尚未評估完所有快照項目")
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
            rows = (
                await session.scalars(
                    select(model).where(model.review_status == "pending").order_by(model.id)
                )
            ).all()
            for row in rows:
                await make_review_item(session, run.id, kind, cast(Entity, row), "review_pending")
    session.add(
        AdminAuditLog(
            actor_user_id=actor_id,
            action="catalog_review_requested",
            target=f"catalog-review:{run.id}",
            metadata_json={
                "mode": payload.mode,
                "requested_counts": payload.requested_counts,
                "model": run.model,
                "max_calls": payload.max_calls,
            },
        )
    )
    await session.commit()
    return run, True


async def prepare_resume(session: AsyncSession, run_id: UUID, actor_id: UUID) -> CatalogReviewRun:
    await _serialize_starts(session)
    run = await get_run(session, run_id, lock=True)
    if not (await run_view(session, run))["can_resume"]:
        raise AppError(409, "catalog_run_not_resumable", "目前工作不能續跑，或已達單次工作呼叫上限")
    if await session.scalar(
        select(CatalogReviewRun.id)
        .where(CatalogReviewRun.id != run_id, CatalogReviewRun.status.in_(ACTIVE))
        .limit(1)
    ):
        raise AppError(409, "catalog_run_in_progress", "已有其他目錄審核執行中")
    for item in await run_items(session, run.id):
        if item.status == "error":
            item.status = "pending"
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
            metadata_json={},
        )
    )
    await session.commit()
    return run


async def apply_decisions(
    session: AsyncSession, run_id: UUID, actor_id: UUID, payload: ApplyRequest, idempotency_key: str
) -> dict[str, Any]:
    run = await get_run(session, run_id, lock=True)
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
                .where(CatalogReviewItem.run_id == run.id, CatalogReviewItem.id.in_(requested))
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
