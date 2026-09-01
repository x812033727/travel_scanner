from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser
from app.db import get_session
from app.hotspots.ranking import calculate_depth_value
from app.models import AdminAuditLog, HotspotSignal, TravelHotspot
from app.problems import AppError

router = APIRouter(prefix="/admin/hotspots", tags=["admin hotspots"])
Session = Annotated[AsyncSession, Depends(get_session)]


class HotspotReviewRequest(BaseModel):
    ids: list[UUID] = Field(min_length=1, max_length=100)
    action: Literal["approve", "reject", "disable", "update"]
    reason: str | None = Field(default=None, max_length=500)
    is_deep_travel: bool | None = None
    depth_kind: Literal["urban_local", "day_trip"] | None = None
    locality_score: int | None = Field(default=None, ge=0, le=100)
    distinctiveness_score: int | None = Field(default=None, ge=0, le=100)
    feasibility_score: int | None = Field(default=None, ge=0, le=100)
    evidence_score: int | None = Field(default=None, ge=0, le=100)
    depth_reason: str | None = Field(default=None, max_length=1000)
    access_minutes: int | None = Field(default=None, ge=1, le=90)
    recommended_duration_minutes: int | None = Field(default=None, ge=30, le=480)

    @model_validator(mode="after")
    def validate_depth(self) -> HotspotReviewRequest:
        if self.is_deep_travel:
            required = (
                self.depth_kind,
                self.locality_score,
                self.distinctiveness_score,
                self.feasibility_score,
                self.evidence_score,
                self.depth_reason,
                self.access_minutes,
                self.recommended_duration_minutes,
            )
            if any(value is None for value in required):
                raise ValueError("深度景點必須填寫類型、四項評分、理由、交通與停留時間")
            if self.depth_kind == "urban_local" and (self.access_minutes or 0) > 45:
                raise ValueError("市區在地景點交通時間不得超過 45 分鐘")
            score = calculate_depth_value(
                locality=self.locality_score or 0,
                distinctiveness=self.distinctiveness_score or 0,
                feasibility=self.feasibility_score or 0,
                evidence=self.evidence_score or 0,
            )
            if score < 70:
                raise ValueError("深度價值分數必須至少 70")
        return self


@router.get("/candidates")
async def list_hotspot_candidates(
    user: AdminUser,
    session: Session,
    city_code: Annotated[str | None, Query(min_length=3, max_length=3)] = None,
    origin: Annotated[str | None, Query(max_length=32)] = None,
    status: Annotated[str | None, Query(max_length=24)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
) -> dict[str, object]:
    _ = user
    filters = []
    if city_code:
        filters.append(TravelHotspot.city_code == city_code.upper())
    if origin:
        filters.append(TravelHotspot.origin == origin)
    if status:
        filters.append(TravelHotspot.review_status == status)
    total = int(await session.scalar(select(func.count(TravelHotspot.id)).where(*filters)) or 0)
    rows = list(
        (
            await session.scalars(
                select(TravelHotspot)
                .where(*filters)
                .order_by(TravelHotspot.updated_at.desc(), TravelHotspot.name)
                .offset((page - 1) * limit)
                .limit(limit)
            )
        ).all()
    )
    items = []
    for hotspot in rows:
        pageviews = await session.scalar(
            select(HotspotSignal.value)
            .where(
                HotspotSignal.hotspot_id == hotspot.id,
                HotspotSignal.metric == "pageviews_30d",
            )
            .order_by(HotspotSignal.observed_on.desc())
            .limit(1)
        )
        items.append(
            {
                "id": str(hotspot.id),
                "name": hotspot.name,
                "qid": hotspot.wikidata_item_id,
                "city_code": hotspot.city_code,
                "city_name": hotspot.city_name,
                "category": hotspot.category,
                "origin": hotspot.origin,
                "status": hotspot.review_status,
                "reason": hotspot.review_reason,
                "distance_km": float(hotspot.discovery_distance_km)
                if hotspot.discovery_distance_km is not None
                else None,
                "pageviews_30d": int(pageviews) if pageviews is not None else None,
                "source_urls": hotspot.source_urls,
                "is_active": hotspot.is_active,
                "is_deep_travel": hotspot.is_deep_travel,
                "depth_kind": hotspot.depth_kind,
                "depth_score": float(hotspot.depth_score)
                if hotspot.depth_score is not None
                else None,
                "depth_reason": hotspot.metadata_json.get("depth_reason"),
                "access_minutes": hotspot.metadata_json.get("access_minutes"),
                "recommended_duration_minutes": hotspot.metadata_json.get(
                    "recommended_duration_minutes"
                ),
                "depth_components": hotspot.metadata_json.get("depth_components"),
            }
        )
    return {"items": items, "total": total, "page": page, "pages": (total + limit - 1) // limit}


@router.post("/review")
async def review_hotspot_candidates(
    payload: HotspotReviewRequest,
    user: AdminUser,
    session: Session,
) -> dict[str, int | str]:
    rows = list(
        (
            await session.scalars(select(TravelHotspot).where(TravelHotspot.id.in_(payload.ids)))
        ).all()
    )
    if len(rows) != len(set(payload.ids)):
        raise AppError(404, "hotspot_not_found", "部分景點候選不存在")
    status = {
        "approve": "approved",
        "reject": "rejected",
        "disable": "disabled",
        "update": rows[0].review_status,
    }[payload.action]
    now = datetime.now(UTC)
    for hotspot in rows:
        if payload.action != "update":
            hotspot.review_status = status
            hotspot.review_reason = payload.reason
        hotspot.reviewed_at = now
        hotspot.reviewed_by_user_id = user.id
        if payload.action != "update":
            hotspot.is_active = payload.action == "approve"
        if payload.is_deep_travel is False:
            hotspot.is_deep_travel = False
            hotspot.depth_kind = None
            hotspot.depth_score = None
            metadata = dict(hotspot.metadata_json)
            for key in (
                "depth_reason",
                "access_minutes",
                "recommended_duration_minutes",
                "depth_components",
            ):
                metadata.pop(key, None)
            hotspot.metadata_json = metadata
        elif payload.is_deep_travel:
            components = {
                "locality": payload.locality_score,
                "distinctiveness": payload.distinctiveness_score,
                "feasibility": payload.feasibility_score,
                "evidence": payload.evidence_score,
            }
            hotspot.is_deep_travel = True
            hotspot.depth_kind = payload.depth_kind
            hotspot.depth_score = Decimal(
                str(
                    calculate_depth_value(
                        locality=payload.locality_score or 0,
                        distinctiveness=payload.distinctiveness_score or 0,
                        feasibility=payload.feasibility_score or 0,
                        evidence=payload.evidence_score or 0,
                    )
                )
            )
            hotspot.metadata_json = {
                **hotspot.metadata_json,
                "depth_reason": payload.depth_reason,
                "access_minutes": payload.access_minutes,
                "recommended_duration_minutes": payload.recommended_duration_minutes,
                "depth_components": components,
            }
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="hotspot_candidates_reviewed",
            target=f"hotspots:{len(rows)}",
            metadata_json={
                "action": payload.action,
                "ids": [str(item.id) for item in rows],
                "reason": payload.reason,
                "is_deep_travel": payload.is_deep_travel,
                "depth_kind": payload.depth_kind,
                "depth_score": float(rows[0].depth_score)
                if rows[0].depth_score is not None
                else None,
            },
        )
    )
    await session.commit()
    return {"updated": len(rows), "status": status}
