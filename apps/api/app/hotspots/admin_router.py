from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser
from app.db import get_session
from app.models import AdminAuditLog, HotspotSignal, TravelHotspot
from app.problems import AppError

router = APIRouter(prefix="/admin/hotspots", tags=["admin hotspots"])
Session = Annotated[AsyncSession, Depends(get_session)]


class HotspotReviewRequest(BaseModel):
    ids: list[UUID] = Field(min_length=1, max_length=100)
    action: Literal["approve", "reject", "disable"]
    reason: str | None = Field(default=None, max_length=500)


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
    status = {"approve": "approved", "reject": "rejected", "disable": "disabled"}[payload.action]
    now = datetime.now(UTC)
    for hotspot in rows:
        hotspot.review_status = status
        hotspot.review_reason = payload.reason
        hotspot.reviewed_at = now
        hotspot.reviewed_by_user_id = user.id
        hotspot.is_active = payload.action == "approve"
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="hotspot_candidates_reviewed",
            target=f"hotspots:{len(rows)}",
            metadata_json={
                "action": payload.action,
                "ids": [str(item.id) for item in rows],
                "reason": payload.reason,
            },
        )
    )
    await session.commit()
    return {"updated": len(rows), "status": status}
