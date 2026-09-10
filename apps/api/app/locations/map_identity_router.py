from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Annotated, Any, Literal, cast
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header, Query
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import and_, func, not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import require_capability
from app.db import get_session
from app.destinations.catalog import DESTINATIONS
from app.infra import enforce_named_rate_limit, get_redis
from app.locations.map_identity import CatalogPlace
from app.locations.map_identity_review import (
    BATCH_TTL_SECONDS,
    CATALOG_MODELS,
    CatalogKind,
    CatalogReference,
    IdentityReviewRequest,
    candidate_snapshot,
    item_payload,
    load_catalog_place,
    review_identity,
)
from app.locations.map_identity_tasks import (
    batch_key,
    enqueue_identity_batch,
    identity_batch_job_status,
)
from app.models import AdminAuditLog, FoodMerchant, TravelHotspot, TravelServiceProduct, User
from app.problems import AppError

router = APIRouter(prefix="/admin/map-identities", tags=["admin-map-identities"])
Session = Annotated[AsyncSession, Depends(get_session)]
IdentityReader = Annotated[User, Depends(require_capability("content.read"))]
IdentityManager = Annotated[User, Depends(require_capability("content.manage"))]


class IdentityBatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    targets: list[CatalogReference] = Field(min_length=1, max_length=50)

    @model_validator(mode="after")
    def unique_targets(self) -> IdentityBatchRequest:
        if len({(target.kind, target.id) for target in self.targets}) != len(self.targets):
            raise ValueError("Duplicate catalog targets are not allowed")
        return self


@router.get("")
async def list_identities(
    user: IdentityReader,
    session: Session,
    kind: CatalogKind = "hotspot",
    destination_id: str | None = None,
    missing_status: Literal["missing", "pending", "confirmed", "all"] = "all",
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=50),
) -> dict[str, Any]:
    model = CATALOG_MODELS[kind]
    if kind == "hotel":
        metadata = TravelServiceProduct.facts
        google_id = metadata["google_place_id"].as_string()
        conditions = [
            TravelServiceProduct.kind == "hotel",
            model.destination_id.in_(
                [
                    destination.id
                    for destination in DESTINATIONS
                    if destination.timezone == "Asia/Seoul"
                ]
            ),
        ]
    elif kind == "merchant":
        metadata = FoodMerchant.map_identity_metadata
        google_id = FoodMerchant.google_place_id
        conditions = [FoodMerchant.country_code == "KR"]
    else:
        metadata = TravelHotspot.metadata_json
        google_id = TravelHotspot.google_place_id
        conditions = [TravelHotspot.country_code == "KR"]
    verified = func.coalesce(
        and_(
            metadata["map_identities"]["google_places"]["status"].as_string() == "verified",
            metadata["map_identities"]["google_places"]["place_id"].as_string() == google_id,
        ),
        False,
    )
    pending = func.coalesce(
        metadata["map_identity_review"]["status"].as_string() == "pending", False
    )
    if missing_status == "confirmed":
        conditions.append(verified)
    elif missing_status == "pending":
        conditions.append(pending)
    elif missing_status == "missing":
        conditions.extend([not_(verified), not_(pending)])
    if destination_id:
        conditions.append(model.destination_id == destination_id)
    total = await session.scalar(select(func.count()).select_from(model).where(*conditions))
    rows = (
        await session.scalars(
            select(model)
            .where(*conditions)
            .order_by(model.destination_id, model.id)
            .offset(offset)
            .limit(limit)
        )
    ).all()
    settings = await load_runtime_settings(session)
    return {
        "items": [item_payload(kind, cast(CatalogPlace, row)) for row in rows],
        "total": total or 0,
        "capabilities": {"google_places_configured": bool(settings.google_maps_api_key)},
    }


@router.post("/batches", status_code=202)
async def create_identity_batch(
    payload: IdentityBatchRequest,
    user: IdentityManager,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    redis = get_redis()
    digest = hashlib.sha256(
        json.dumps(payload.model_dump(mode="json"), sort_keys=True).encode()
    ).hexdigest()
    idempotency_digest = hashlib.sha256(idempotency_key.encode()).hexdigest()
    key = f"map-identities:batch-idem:{user.id}:{idempotency_digest}"
    existing = await redis.get(key)
    if existing:
        previous = json.loads(existing)
        if previous["digest"] != digest:
            raise AppError(409, "idempotency_conflict", "相同請求代碼不可用於不同配對批次")
        state = await redis.get(batch_key(previous["id"]))
        if state:
            return dict(json.loads(state))
        raise AppError(409, "map_identity_batch_expired", "配對批次已過期，請建立新批次")
    await enforce_named_rate_limit(
        "map-identities-batch", str(user.id), limit=6, window_seconds=3600
    )
    for target in payload.targets:
        await load_catalog_place(session, target)
    settings = await load_runtime_settings(session)
    if not settings.google_maps_api_key:
        raise AppError(503, "google_maps_not_configured", "Google 地點配對服務尚未設定")
    batch_id = uuid4()
    if not await redis.set(
        key, json.dumps({"id": str(batch_id), "digest": digest}), ex=BATCH_TTL_SECONDS, nx=True
    ):
        raise AppError(409, "map_identity_batch_in_progress", "配對批次正在建立，請稍候")
    state = {
        "id": str(batch_id),
        "status": "queued",
        "total": len(payload.targets),
        "processed": 0,
        "results": [],
        "created_at": datetime.now(UTC).isoformat(),
    }
    await redis.set(batch_key(batch_id), json.dumps(state), ex=BATCH_TTL_SECONDS)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="map_identity.batch_created",
            target=f"map-identity-batch:{batch_id}",
            metadata_json={
                "targets": [target.model_dump(mode="json") for target in payload.targets]
            },
        )
    )
    await session.commit()
    try:
        enqueue_identity_batch(batch_id, user.id, payload.targets)
    except Exception as exc:
        state["status"] = "failed"
        await redis.set(batch_key(batch_id), json.dumps(state), ex=BATCH_TTL_SECONDS)
        raise AppError(503, "map_identity_queue_unavailable", "配對工作暫時無法排程") from exc
    return state


@router.get("/batches/{batch_id}")
async def identity_batch_status(batch_id: UUID, user: IdentityReader) -> dict[str, Any]:
    redis = get_redis()
    raw = await redis.get(batch_key(batch_id))
    if not raw:
        raise AppError(404, "map_identity_batch_not_found", "找不到這個配對批次")
    state = dict(json.loads(raw))
    if state.get("status") in {"queued", "running"} and identity_batch_job_status(batch_id) in {
        "failed",
        "stopped",
        "canceled",
    }:
        state.update({"status": "failed", "error_code": "worker_failed"})
        await redis.set(batch_key(batch_id), json.dumps(state), ex=BATCH_TTL_SECONDS)
    return state


@router.get("/{kind}/{identifier}/candidates")
async def identity_candidates(
    kind: CatalogKind, identifier: UUID, user: IdentityManager, session: Session
) -> dict[str, Any]:
    await enforce_named_rate_limit(
        "map-identities-candidates", str(user.id), limit=30, window_seconds=3600
    )
    settings = await load_runtime_settings(session)
    return await candidate_snapshot(
        session, get_redis(), settings, CatalogReference(kind=kind, id=identifier), user.id
    )


@router.post("/{kind}/{identifier}/review")
async def confirm_identity(
    kind: CatalogKind,
    identifier: UUID,
    payload: IdentityReviewRequest,
    user: IdentityManager,
    session: Session,
) -> dict[str, Any]:
    await enforce_named_rate_limit(
        "map-identities-review", str(user.id), limit=120, window_seconds=3600
    )
    return await review_identity(
        session, get_redis(), CatalogReference(kind=kind, id=identifier), payload, user.id
    )
