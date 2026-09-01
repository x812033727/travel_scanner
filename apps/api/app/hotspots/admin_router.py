from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import AdminUser
from app.db import get_session
from app.destinations.catalog import DESTINATIONS, destination_for_id
from app.hotspots.guides import (
    GuideCandidate,
    YouTubeGuideProvider,
    canonical_external_url,
    discover_guides,
    guide_coverage,
    guide_quota_status,
    save_candidates,
)
from app.hotspots.ranking import calculate_depth_value
from app.i18n import LOCALES, Locale
from app.infra import get_redis
from app.models import AdminAuditLog, HotspotGuide, HotspotSignal, TravelHotspot
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
    destination_id: str | None = Field(default=None, min_length=2, max_length=64)

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


class GuideReviewRequest(BaseModel):
    ids: list[UUID] = Field(min_length=1, max_length=100)
    action: Literal["approve", "reject", "disable"]
    reason: str | None = Field(default=None, max_length=500)
    locale: Locale | None = None


class GuideDiscoverRequest(BaseModel):
    hotspot_ids: list[UUID] = Field(min_length=1, max_length=10)
    locales: list[Locale] = Field(default_factory=lambda: list(LOCALES), min_length=1, max_length=5)


class ManualGuideRequest(BaseModel):
    hotspot_id: UUID
    locale: Locale
    content_type: Literal["article", "video"]
    url: str = Field(min_length=12, max_length=2048)
    title: str | None = Field(default=None, max_length=500)
    creator_name: str | None = Field(default=None, max_length=255)
    summary: str | None = Field(default=None, max_length=500)


@router.get("/candidates")
async def list_hotspot_candidates(
    user: AdminUser,
    session: Session,
    city_code: Annotated[str | None, Query(min_length=3, max_length=3)] = None,
    destination_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    role: Annotated[str | None, Query(pattern="^(primary|secondary|extension)$")] = None,
    parent_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    origin: Annotated[str | None, Query(max_length=32)] = None,
    status: Annotated[str | None, Query(max_length=24)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
) -> dict[str, object]:
    _ = user
    filters = []
    if city_code:
        filters.append(TravelHotspot.city_code == city_code.upper())
    if destination_id:
        filters.append(TravelHotspot.destination_id == destination_id.casefold())
    if role:
        role_ids = [item.id for item in DESTINATIONS if item.role == role]
        filters.append(TravelHotspot.destination_id.in_(role_ids))
    if parent_id:
        child_ids = [
            item.id for item in DESTINATIONS if item.parent_destination_id == parent_id.casefold()
        ]
        filters.append(TravelHotspot.destination_id.in_(child_ids))
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
                "destination_id": hotspot.destination_id,
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
                **(
                    {
                        "destination_role": profile.role,
                        "parent_destination_id": profile.parent_destination_id,
                    }
                    if (profile := destination_for_id(hotspot.destination_id))
                    else {"destination_role": "primary", "parent_destination_id": None}
                ),
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
    target_destination = (
        destination_for_id(payload.destination_id) if payload.destination_id else None
    )
    if payload.destination_id and target_destination is None:
        raise AppError(422, "unsupported_destination", "目前不支援這個目的地")
    for hotspot in rows:
        if payload.action != "update":
            hotspot.review_status = status
            hotspot.review_reason = payload.reason
        hotspot.reviewed_at = now
        hotspot.reviewed_by_user_id = user.id
        if target_destination:
            hotspot.destination_id = target_destination.id
            hotspot.city_code = target_destination.code
            hotspot.city_name = target_destination.city
            hotspot.country_name = target_destination.country_label
            country_codes = {
                "Japan": "JP",
                "South Korea": "KR",
                "Thailand": "TH",
                "Taiwan": "TW",
                "Singapore": "SG",
                "Hong Kong": "HK",
                "Vietnam": "VN",
            }
            hotspot.country_code = country_codes[target_destination.country]
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
                "destination_id": payload.destination_id,
                "depth_score": float(rows[0].depth_score)
                if rows[0].depth_score is not None
                else None,
            },
        )
    )
    await session.commit()
    return {"updated": len(rows), "status": status}


@router.get("/guides")
async def list_guide_candidates(
    user: AdminUser,
    session: Session,
    hotspot_id: UUID | None = None,
    locale: Locale | None = None,
    type: Literal["article", "video"] | None = None,
    status: Annotated[str | None, Query(max_length=24)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> dict[str, object]:
    _ = user
    filters = []
    if hotspot_id:
        filters.append(HotspotGuide.hotspot_id == hotspot_id)
    if locale:
        filters.append(HotspotGuide.locale == locale)
    if type:
        filters.append(HotspotGuide.content_type == type)
    if status:
        filters.append(HotspotGuide.review_status == status)
    total = int(await session.scalar(select(func.count(HotspotGuide.id)).where(*filters)) or 0)
    rows = (
        await session.execute(
            select(HotspotGuide, TravelHotspot.name)
            .join(TravelHotspot, TravelHotspot.id == HotspotGuide.hotspot_id)
            .where(*filters)
            .order_by(HotspotGuide.updated_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
    ).all()
    return {
        "items": [
            {
                "id": str(guide.id),
                "hotspot_id": str(guide.hotspot_id),
                "hotspot_name": name,
                "type": guide.content_type,
                "provider": guide.provider,
                "locale": guide.locale,
                "title": guide.title,
                "creator_name": guide.creator_name,
                "url": guide.canonical_url,
                "thumbnail_url": guide.thumbnail_url,
                "view_count": guide.view_count,
                "language_confidence": float(guide.language_confidence),
                "status": guide.review_status,
                "reason": guide.review_reason,
                "last_verified_at": guide.last_verified_at,
                "metadata_expires_at": guide.metadata_expires_at,
            }
            for guide, name in rows
        ],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.post("/guides/review")
async def review_guides(
    payload: GuideReviewRequest,
    user: AdminUser,
    session: Session,
) -> dict[str, int | str]:
    rows = list(
        (await session.scalars(select(HotspotGuide).where(HotspotGuide.id.in_(payload.ids)))).all()
    )
    if len(rows) != len(set(payload.ids)):
        raise AppError(404, "hotspot_guide_not_found", "部分介紹候選不存在")
    status = {"approve": "approved", "reject": "rejected", "disable": "disabled"}[payload.action]
    now = datetime.now(UTC)
    for guide in rows:
        guide.review_status = status
        guide.review_reason = payload.reason
        guide.reviewed_at = now
        guide.reviewed_by_user_id = user.id
        if payload.locale:
            guide.locale = payload.locale
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="hotspot_guides_reviewed",
            target=f"hotspot-guides:{len(rows)}",
            metadata_json={
                "action": payload.action,
                "ids": [str(row.id) for row in rows],
                "locale": payload.locale,
            },
        )
    )
    await session.commit()
    return {"updated": len(rows), "status": status}


@router.post("/guides/discover")
async def discover_guide_candidates(
    payload: GuideDiscoverRequest,
    user: AdminUser,
    session: Session,
) -> dict[str, object]:
    _ = user
    settings = await load_runtime_settings(session)
    hotspots = list(
        (
            await session.scalars(
                select(TravelHotspot).where(TravelHotspot.id.in_(payload.hotspot_ids))
            )
        ).all()
    )
    if len(hotspots) != len(set(payload.hotspot_ids)):
        raise AppError(404, "hotspot_not_found", "部分景點不存在")
    reports = []
    for hotspot in hotspots:
        reports.append(
            {
                "hotspot_id": str(hotspot.id),
                **await discover_guides(
                    session,
                    settings,
                    hotspot,
                    payload.locales,
                    redis=get_redis(),
                ),
            }
        )
    return {"reports": reports}


@router.post("/guides/manual")
async def add_manual_guide(
    payload: ManualGuideRequest,
    user: AdminUser,
    session: Session,
) -> dict[str, object]:
    hotspot = await session.get(TravelHotspot, payload.hotspot_id)
    if hotspot is None:
        raise AppError(404, "hotspot_not_found", "找不到這個景點")
    settings = await load_runtime_settings(session)
    if payload.content_type == "video":
        if not settings.hotspot_guide_youtube_api_key:
            raise AppError(
                503, "hotspot_guide_youtube_not_configured", "尚未設定 YouTube Data API key"
            )
        provider = YouTubeGuideProvider(settings.hotspot_guide_youtube_api_key)
        try:
            candidate = await provider.import_video(payload.url, payload.locale)
        finally:
            await provider.close()
    else:
        url = canonical_external_url(payload.url)
        if not payload.title or not payload.creator_name:
            raise AppError(422, "hotspot_guide_metadata_required", "手動文章需要標題與網站名稱")
        candidate = GuideCandidate(
            content_type="article",
            provider="manual",
            locale=payload.locale,
            title=payload.title,
            creator_name=payload.creator_name,
            canonical_url=url,
            summary=payload.summary,
            language_confidence=Decimal("1.000"),
        )
    created = await save_candidates(session, hotspot.id, [candidate])
    await session.commit()
    return {"created": created}


@router.get("/guides/coverage")
async def hotspot_guide_coverage(user: AdminUser, session: Session) -> dict[str, object]:
    _ = user
    result = await guide_coverage(session)
    result["quotas"] = await guide_quota_status(get_redis(), await load_runtime_settings(session))
    return result
