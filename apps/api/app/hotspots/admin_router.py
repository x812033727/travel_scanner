from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated, Any, Literal, cast
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header, Query
from pydantic import BaseModel, Field, model_validator
from redis import Redis as SyncRedis
from redis.asyncio import Redis
from rq import Queue, Retry
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.listing import (
    COUNTRY_ORDER,
    HOTSPOT_CATEGORY_ORDER,
    country_name_for,
    country_rank,
    destination_rank,
    ranked,
)
from app.admin.service import load_runtime_settings
from app.auth.service import AdminUser
from app.config import get_settings
from app.db import escape_like, get_session
from app.destinations.catalog import DESTINATIONS, destination_for_id
from app.hotspots.ai_search import (
    AIProviderName,
    ContentType,
    SearchDepth,
    ai_quota_status,
    configured_research_providers,
    consume_ai_run,
    estimate_calls,
    research_model,
)
from app.hotspots.guides import (
    GuideCandidate,
    YouTubeGuideProvider,
    canonical_external_url,
    discover_guides,
    guide_coverage,
    guide_quota_status,
    save_candidates,
)
from app.hotspots.maps import has_exact_map_identity
from app.hotspots.place_tasks import enqueue_place_enrichment_run
from app.hotspots.places import (
    RunMode,
    canonical_official_website,
    enrichment_targets,
    place_summary_payload,
    profile_overview,
    run_payload,
)
from app.hotspots.ranking import calculate_depth_value
from app.i18n import LOCALES, Locale, current_locale
from app.infra import get_redis
from app.locations.coordinates import (
    has_durable_coordinates,
    is_durable_coordinate_source,
    valid_coordinate_pair,
)
from app.locations.google_match import preview_google_place_match
from app.models import (
    AdminAuditLog,
    HotspotGuide,
    HotspotGuideAISearchRun,
    HotspotPlaceEnrichmentRun,
    HotspotPlaceProfile,
    HotspotSignal,
    TravelHotspot,
)
from app.problems import AppError

router = APIRouter(prefix="/admin/hotspots", tags=["admin hotspots"])
Session = Annotated[AsyncSession, Depends(get_session)]
RedisDep = Annotated[Redis, Depends(get_redis)]
RequestLocale = Annotated[Locale, Depends(current_locale)]


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
    google_place_id: str | None = Field(default=None, max_length=255)
    naver_map_url: str | None = Field(
        default=None,
        pattern=r"^https://map\.naver\.com/(?:p|v5)/entry/place/",
        max_length=2048,
    )
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    coordinate_source_type: (
        Literal["curated", "wikidata", "official_tourism", "merchant_official", "admin_verified"]
        | None
    ) = None
    coordinate_source_url: str | None = Field(default=None, pattern=r"^https://", max_length=2048)
    map_match_status: Literal["unverified", "verified", "ambiguous", "disabled"] | None = None

    @model_validator(mode="after")
    def validate_depth(self) -> HotspotReviewRequest:
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("緯度與經度必須同時提供")
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


def _validate_hotspot_location(
    *,
    country_code: str,
    latitude: float | Decimal | None,
    longitude: float | Decimal | None,
    coordinate_source_type: str | None,
    coordinate_source_url: str | None,
    google_place_id: str | None,
    naver_map_url: str | None,
) -> None:
    if not has_exact_map_identity(country_code, google_place_id, naver_map_url):
        provider = "Naver 精準地點頁" if country_code == "KR" else "Google Place ID"
        raise AppError(422, "exact_map_identity_required", f"核准前必須提供{provider}")
    if not valid_coordinate_pair(latitude, longitude):
        raise AppError(422, "permanent_coordinates_required", "核准前必須提供永久 WGS84 座標")
    if not is_durable_coordinate_source(coordinate_source_type, coordinate_source_url):
        raise AppError(422, "coordinate_source_required", "核准前必須提供可稽核的永久座標來源")


class GuideReviewRequest(BaseModel):
    ids: list[UUID] = Field(min_length=1, max_length=100)
    action: Literal["approve", "reject", "disable"]
    reason: str | None = Field(default=None, max_length=500)
    locale: Locale | None = None


class GoogleMapCandidateRequest(BaseModel):
    query: str = Field(min_length=2, max_length=255)
    country_code: str = Field(min_length=2, max_length=2)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @model_validator(mode="after")
    def validate_coordinate_pair(self) -> GoogleMapCandidateRequest:
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("緯度與經度必須同時提供")
        return self


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


class GuideAISearchRequest(BaseModel):
    hotspot_id: UUID
    locales: list[Locale] = Field(default_factory=lambda: list(LOCALES), min_length=1, max_length=5)
    content_types: list[ContentType] = Field(
        default_factory=lambda: cast(list[ContentType], ["article", "video"]),
        min_length=1,
        max_length=2,
    )
    provider: AIProviderName = "minimax"
    depth: SearchDepth = "deep"
    only_missing: bool = True
    custom_instructions: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def unique_scope(self) -> GuideAISearchRequest:
        self.locales = list(dict.fromkeys(self.locales))
        self.content_types = list(dict.fromkeys(self.content_types))
        if self.custom_instructions:
            self.custom_instructions = self.custom_instructions.strip() or None
        return self


class PlaceEnrichmentRunRequest(BaseModel):
    scope: Literal["all", "country", "hotspots"] = "all"
    mode: RunMode = "missing_or_expired"
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    hotspot_ids: list[UUID] = Field(default_factory=list, max_length=450)
    confirm_usage: bool = False

    @model_validator(mode="after")
    def validate_scope(self) -> PlaceEnrichmentRunRequest:
        if self.scope == "country" and not self.country_code:
            raise ValueError("國家範圍需要 country_code")
        if self.scope == "hotspots" and not self.hotspot_ids:
            raise ValueError("指定景點範圍需要 hotspot_ids")
        self.hotspot_ids = list(dict.fromkeys(self.hotspot_ids))
        return self


class PlaceProfileUpdateRequest(BaseModel):
    action: Literal["approve", "reject", "save", "refresh"]
    google_place_id: str | None = Field(default=None, max_length=255)
    official_website_url: str | None = Field(default=None, max_length=2048)
    official_website_source_url: str | None = Field(default=None, max_length=2048)
    reason: str | None = Field(default=None, max_length=500)


class PlaceProfileReviewRequest(BaseModel):
    ids: list[UUID] = Field(min_length=1, max_length=100)
    action: Literal["approve", "reject"]
    reason: str | None = Field(default=None, max_length=500)


def _ai_search_payload(run: HotspotGuideAISearchRun) -> dict[str, object]:
    return {
        "run_id": str(run.id),
        "hotspot_id": str(run.hotspot_id),
        "status": run.status,
        "progress": run.progress,
        "current": run.progress_json,
        "provider": run.provider,
        "model": run.model,
        "depth": run.depth,
        "locales": run.requested_locales,
        "content_types": run.content_types,
        "only_missing": run.only_missing,
        "query_plan": run.query_plan_json,
        "usage": run.usage_json,
        "result": run.result_json,
        "error_code": run.error_code,
        "retryable": run.error_code
        in {"ai_search_failed", "queue_unavailable", "provider_unavailable"},
        "created_at": run.created_at,
        "started_at": run.started_at,
        "completed_at": run.completed_at,
    }


@router.get("/candidates")
async def list_hotspot_candidates(
    user: AdminUser,
    session: Session,
    locale: RequestLocale,
    city_code: Annotated[str | None, Query(min_length=3, max_length=3)] = None,
    destination_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    role: Annotated[str | None, Query(pattern="^(primary|secondary|extension)$")] = None,
    parent_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    origin: Annotated[str | None, Query(max_length=32)] = None,
    status: Annotated[str | None, Query(max_length=24)] = None,
    country_code: Annotated[str | None, Query(min_length=2, max_length=2)] = None,
    category: Annotated[str | None, Query(max_length=32, pattern="^[a-z_]+$")] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 30,
) -> dict[str, object]:
    _ = user
    # Keyed by dimension so each facet can drop only its own filter.
    filters: dict[str, Any] = {}
    if city_code:
        filters["city_code"] = TravelHotspot.city_code == city_code.upper()
    if destination_id:
        filters["destination_id"] = TravelHotspot.destination_id == destination_id.casefold()
    if role:
        role_ids = [item.id for item in DESTINATIONS if item.role == role]
        filters["role"] = TravelHotspot.destination_id.in_(role_ids)
    if parent_id:
        child_ids = [
            item.id for item in DESTINATIONS if item.parent_destination_id == parent_id.casefold()
        ]
        filters["parent_id"] = TravelHotspot.destination_id.in_(child_ids)
    if origin:
        filters["origin"] = TravelHotspot.origin == origin
    if status:
        filters["status"] = TravelHotspot.review_status == status
    if country_code:
        filters["country_code"] = TravelHotspot.country_code == country_code.upper()
    if category:
        filters["category"] = TravelHotspot.category == category
    where = list(filters.values())

    def without(dimension: str) -> list[Any]:
        return [clause for key, clause in filters.items() if key != dimension]

    total = int(await session.scalar(select(func.count(TravelHotspot.id)).where(*where)) or 0)
    rows = list(
        (
            await session.scalars(
                select(TravelHotspot)
                .where(*where)
                .order_by(
                    country_rank(TravelHotspot.country_code),
                    TravelHotspot.country_code,
                    destination_rank(TravelHotspot.destination_id),
                    TravelHotspot.destination_id,
                    TravelHotspot.name,
                )
                .offset((page - 1) * limit)
                .limit(limit)
            )
        ).all()
    )
    country_rows = (
        await session.execute(
            select(
                TravelHotspot.country_code,
                func.min(TravelHotspot.country_name).label("country_name"),
                func.count(TravelHotspot.id).label("count"),
            )
            .where(*without("country_code"))
            .group_by(TravelHotspot.country_code)
        )
    ).all()
    category_rows = (
        await session.execute(
            select(TravelHotspot.category, func.count(TravelHotspot.id).label("count"))
            .where(*without("category"))
            .group_by(TravelHotspot.category)
        )
    ).all()
    facets = {
        "countries": [
            {
                "code": row.country_code,
                "name": country_name_for(row.country_code, locale, row.country_name),
                "count": int(row.count),
            }
            for row in ranked(country_rows, "country_code", COUNTRY_ORDER)
        ],
        "categories": [
            {"code": row.category, "count": int(row.count)}
            for row in ranked(category_rows, "category", HOTSPOT_CATEGORY_ORDER)
        ],
    }
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
                "country_code": hotspot.country_code,
                "country_name": hotspot.country_name,
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
                "google_place_id": hotspot.google_place_id,
                "naver_map_url": hotspot.naver_map_url,
                "map_match_status": hotspot.map_match_status,
                "map_verified_at": hotspot.map_verified_at,
                "latitude": float(hotspot.latitude) if hotspot.latitude is not None else None,
                "longitude": float(hotspot.longitude) if hotspot.longitude is not None else None,
                "coordinate_source_type": hotspot.coordinate_source_type,
                "coordinate_source_url": hotspot.coordinate_source_url,
                "coordinate_verified_at": hotspot.coordinate_verified_at,
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
    return {
        "items": items,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "facets": facets,
    }


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
    if len(rows) > 1 and (payload.google_place_id or payload.naver_map_url):
        raise AppError(422, "bulk_map_identity_not_allowed", "單一地圖識別只能套用至一筆景點")
    if payload.google_place_id:
        duplicate = await session.scalar(
            select(TravelHotspot.id).where(
                TravelHotspot.google_place_id == payload.google_place_id,
                TravelHotspot.id.not_in(payload.ids),
            )
        )
        if duplicate:
            raise AppError(409, "hotspot_map_identity_exists", "Google Place ID 已由其他景點使用")
    if payload.naver_map_url:
        duplicate = await session.scalar(
            select(TravelHotspot.id).where(
                TravelHotspot.naver_map_url == payload.naver_map_url,
                TravelHotspot.id.not_in(payload.ids),
            )
        )
        if duplicate:
            raise AppError(409, "hotspot_map_identity_exists", "Naver 地點網址已由其他景點使用")
    for hotspot in rows:
        prospective_country = target_destination.country if target_destination else None
        country_code = hotspot.country_code
        if prospective_country:
            country_code = {
                "Japan": "JP",
                "South Korea": "KR",
                "Thailand": "TH",
                "Taiwan": "TW",
                "Singapore": "SG",
                "Hong Kong": "HK",
                "Vietnam": "VN",
            }[prospective_country]
        google_place_id = (
            payload.google_place_id
            if "google_place_id" in payload.model_fields_set
            else hotspot.google_place_id
        )
        naver_map_url = (
            payload.naver_map_url
            if "naver_map_url" in payload.model_fields_set
            else hotspot.naver_map_url
        )
        latitude = payload.latitude if "latitude" in payload.model_fields_set else hotspot.latitude
        longitude = (
            payload.longitude if "longitude" in payload.model_fields_set else hotspot.longitude
        )
        coordinate_source_type = (
            payload.coordinate_source_type
            if "coordinate_source_type" in payload.model_fields_set
            else hotspot.coordinate_source_type
        )
        coordinate_source_url = (
            payload.coordinate_source_url
            if "coordinate_source_url" in payload.model_fields_set
            else hotspot.coordinate_source_url
        )
        if (latitude is None) != (longitude is None):
            raise AppError(422, "coordinate_pair_required", "緯度與經度必須同時提供")
        map_status = payload.map_match_status or hotspot.map_match_status
        if payload.action == "approve" and map_status != "verified":
            raise AppError(422, "map_verification_required", "核准前必須完成精準地點比對")
        if map_status == "verified":
            _validate_hotspot_location(
                country_code=country_code,
                latitude=latitude,
                longitude=longitude,
                coordinate_source_type=coordinate_source_type,
                coordinate_source_url=coordinate_source_url,
                google_place_id=google_place_id,
                naver_map_url=naver_map_url,
            )
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
        if "google_place_id" in payload.model_fields_set:
            hotspot.google_place_id = payload.google_place_id
        if "naver_map_url" in payload.model_fields_set:
            hotspot.naver_map_url = payload.naver_map_url
        if "latitude" in payload.model_fields_set:
            hotspot.latitude = (
                Decimal(str(payload.latitude)) if payload.latitude is not None else None
            )
        if "longitude" in payload.model_fields_set:
            hotspot.longitude = (
                Decimal(str(payload.longitude)) if payload.longitude is not None else None
            )
        if "coordinate_source_type" in payload.model_fields_set:
            hotspot.coordinate_source_type = payload.coordinate_source_type
        if "coordinate_source_url" in payload.model_fields_set:
            hotspot.coordinate_source_url = payload.coordinate_source_url
        if any(
            field in payload.model_fields_set
            for field in (
                "latitude",
                "longitude",
                "coordinate_source_type",
                "coordinate_source_url",
            )
        ):
            hotspot.coordinate_verified_at = (
                now
                if has_durable_coordinates(
                    latitude,
                    longitude,
                    coordinate_source_type,
                    coordinate_source_url,
                )
                else None
            )
        if payload.map_match_status:
            hotspot.map_match_status = payload.map_match_status
            if payload.map_match_status == "verified":
                hotspot.map_verified_at = now
                hotspot.map_verified_by_user_id = user.id
            else:
                hotspot.map_verified_at = None
                hotspot.map_verified_by_user_id = None
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
                "map_match_status": payload.map_match_status,
                "google_place_id_changed": "google_place_id" in payload.model_fields_set,
                "naver_map_url_changed": "naver_map_url" in payload.model_fields_set,
                "coordinates_changed": bool({"latitude", "longitude"} & payload.model_fields_set),
                "coordinate_source_changed": bool(
                    {"coordinate_source_type", "coordinate_source_url"} & payload.model_fields_set
                ),
                "depth_score": float(rows[0].depth_score)
                if rows[0].depth_score is not None
                else None,
            },
        )
    )
    await session.commit()
    return {"updated": len(rows), "status": status}


@router.post("/map-candidates")
async def hotspot_map_candidates(
    payload: GoogleMapCandidateRequest,
    user: AdminUser,
    session: Session,
) -> dict[str, object]:
    _ = user
    return await preview_google_place_match(
        session,
        get_redis(),
        query=payload.query,
        country_code=payload.country_code,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )


@router.get("/guides")
async def list_guide_candidates(
    user: AdminUser,
    session: Session,
    hotspot_id: UUID | None = None,
    locale: Locale | None = None,
    type: Literal["article", "video"] | None = None,
    status: Annotated[str | None, Query(max_length=24)] = None,
    discovery_method: Literal["standard", "ai_research", "manual"] | None = None,
    ai_provider: AIProviderName | None = None,
    run_id: UUID | None = None,
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
    if discovery_method == "ai_research":
        filters.append(HotspotGuide.metadata_json["discovery_method"].as_string() == "ai_research")
    elif discovery_method == "standard":
        filters.append(
            or_(
                HotspotGuide.metadata_json["discovery_method"].as_string().is_(None),
                HotspotGuide.metadata_json["discovery_method"].as_string() != "ai_research",
            )
        )
    elif discovery_method == "manual":
        filters.append(HotspotGuide.provider == "manual")
    if ai_provider:
        filters.append(HotspotGuide.metadata_json["ai_provider"].as_string() == ai_provider)
    if run_id:
        filters.append(HotspotGuide.metadata_json["ai_search_run_id"].as_string() == str(run_id))
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
                "discovery_method": guide.metadata_json.get("discovery_method", "standard"),
                "ai_search_run_id": guide.metadata_json.get("ai_search_run_id"),
                "ai_provider": guide.metadata_json.get("ai_provider"),
                "ai_model": guide.metadata_json.get("ai_model"),
                "relevance_score": guide.metadata_json.get("relevance_score"),
                "quality_score": guide.metadata_json.get("quality_score"),
                "recommendation_reason": guide.metadata_json.get("recommendation_reason"),
                "search_query": guide.metadata_json.get("search_query"),
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


@router.post("/guides/ai-search", status_code=202)
async def create_guide_ai_search(
    payload: GuideAISearchRequest,
    user: AdminUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, object]:
    existing = await session.scalar(
        select(HotspotGuideAISearchRun).where(
            HotspotGuideAISearchRun.actor_user_id == user.id,
            HotspotGuideAISearchRun.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        return {
            **_ai_search_payload(existing),
            "estimated_calls": estimate_calls(
                len(existing.requested_locales),
                cast(list[ContentType], existing.content_types),
                cast(SearchDepth, existing.depth),
            ),
        }
    hotspot = await session.get(TravelHotspot, payload.hotspot_id)
    if hotspot is None:
        raise AppError(404, "hotspot_not_found", "找不到這個景點")
    settings = await load_runtime_settings(session)
    if not settings.hotspot_guide_ai_search_enabled:
        raise AppError(503, "hotspot_guide_ai_search_disabled", "AI 景點搜尋目前未啟用")
    providers = configured_research_providers(settings)
    if not providers[payload.provider]:
        raise AppError(503, "hotspot_guide_ai_provider_not_configured", "所選 AI 供應商尚未設定")
    required_types = set(payload.content_types)
    if payload.only_missing:
        for content_type in tuple(required_types):
            approved_locales = set(
                (
                    await session.scalars(
                        select(HotspotGuide.locale)
                        .where(
                            HotspotGuide.hotspot_id == payload.hotspot_id,
                            HotspotGuide.content_type == content_type,
                            HotspotGuide.review_status == "approved",
                            HotspotGuide.locale.in_(payload.locales),
                        )
                        .distinct()
                    )
                ).all()
            )
            if approved_locales.issuperset(payload.locales):
                required_types.remove(content_type)
    if "article" in required_types and not (
        settings.hotspot_guide_brave_enabled and settings.hotspot_guide_brave_api_key
    ):
        raise AppError(503, "hotspot_guide_brave_not_configured", "文章搜尋需要 Brave Search 設定")
    if "video" in required_types and not (
        settings.hotspot_guide_youtube_enabled and settings.hotspot_guide_youtube_api_key
    ):
        raise AppError(
            503, "hotspot_guide_youtube_not_configured", "影片搜尋需要 YouTube Data API 設定"
        )
    if not await consume_ai_run(get_redis(), settings):
        raise AppError(429, "hotspot_guide_ai_quota_exhausted", "今日 AI 搜尋執行額度已用完")
    run = HotspotGuideAISearchRun(
        id=uuid4(),
        actor_user_id=user.id,
        hotspot_id=payload.hotspot_id,
        idempotency_key=idempotency_key,
        requested_locales=list(payload.locales),
        content_types=list(payload.content_types),
        provider=payload.provider,
        model=research_model(settings, payload.provider),
        depth=payload.depth,
        only_missing=payload.only_missing,
        custom_instructions=payload.custom_instructions,
        status="queued",
        progress=0,
    )
    session.add(run)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="hotspot_guide_ai_search_started",
            target=f"hotspot-guide-ai-search:{run.id}",
            metadata_json={
                "hotspot_id": str(payload.hotspot_id),
                "provider": payload.provider,
                "depth": payload.depth,
                "locales": payload.locales,
                "content_types": payload.content_types,
            },
        )
    )
    await session.commit()
    try:
        connection = SyncRedis.from_url(get_settings().redis_url)
        queued = Queue("hotspot-guides", connection=connection).enqueue(
            "app.hotspots.ai_tasks.run_hotspot_guide_ai_search",
            str(run.id),
            job_timeout=900,
            retry=Retry(max=2, interval=[30, 120]),
        )
        run.queue_job_id = queued.id
        await session.commit()
    except Exception as exc:
        run.status = "failed"
        run.progress = 100
        run.error_code = "queue_unavailable"
        run.error_message = "AI 景點搜尋佇列暫時無法使用"
        run.completed_at = datetime.now(UTC)
        await session.commit()
        raise AppError(503, "queue_unavailable", "AI 景點搜尋佇列暫時無法使用") from exc
    return {
        **_ai_search_payload(run),
        "estimated_calls": estimate_calls(
            len(payload.locales), payload.content_types, payload.depth
        ),
    }


@router.get("/guides/ai-search/{run_id}")
async def get_guide_ai_search(
    run_id: UUID,
    user: AdminUser,
    session: Session,
) -> dict[str, object]:
    _ = user
    run = await session.get(HotspotGuideAISearchRun, run_id)
    if run is None:
        raise AppError(404, "hotspot_guide_ai_search_not_found", "找不到這次 AI 搜尋")
    return _ai_search_payload(run)


@router.post("/guides/manual")
async def add_manual_guide(
    payload: ManualGuideRequest,
    user: AdminUser,
    session: Session,
    redis: RedisDep,
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
        provider = YouTubeGuideProvider(settings.hotspot_guide_youtube_api_key, redis=redis)
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
    settings = await load_runtime_settings(session)
    result["quotas"] = await guide_quota_status(get_redis(), settings)
    result["ai_search"] = {
        "enabled": settings.hotspot_guide_ai_search_enabled,
        "default_provider": settings.hotspot_guide_ai_default_provider,
        "providers": configured_research_providers(settings),
        "sources": {
            "brave": bool(
                settings.hotspot_guide_brave_enabled and settings.hotspot_guide_brave_api_key
            ),
            "youtube": bool(
                settings.hotspot_guide_youtube_enabled and settings.hotspot_guide_youtube_api_key
            ),
        },
        "quota": await ai_quota_status(get_redis(), settings),
    }
    return result


async def _create_place_run(
    session: AsyncSession,
    *,
    actor_user_id: UUID | None,
    idempotency_key: str,
    mode: RunMode,
    scope: dict[str, object],
    targets: list[TravelHotspot],
) -> HotspotPlaceEnrichmentRun:
    run = HotspotPlaceEnrichmentRun(
        id=uuid4(),
        actor_user_id=actor_user_id,
        idempotency_key=idempotency_key,
        mode=mode,
        scope_json=scope,
        status="queued" if targets else "completed",
        total_count=len(targets),
        estimated_google_calls=len(targets)
        + sum(1 for item in targets if not item.google_place_id),
        result_json={"processed_ids": []},
        completed_at=datetime.now(UTC) if not targets else None,
    )
    session.add(run)
    session.add(
        AdminAuditLog(
            actor_user_id=actor_user_id,
            action="hotspot_place_enrichment_started",
            target=f"hotspot-place-enrichment:{run.id}",
            metadata_json={
                "mode": mode,
                "scope": scope,
                "total": len(targets),
                "estimated_google_calls": run.estimated_google_calls,
            },
        )
    )
    await session.commit()
    if not targets:
        return run
    try:
        jobs = enqueue_place_enrichment_run(run.id, [item.id for item in targets])
        run.progress_json = {"queue_job_ids": jobs}
        await session.commit()
    except Exception as exc:
        run.status = "failed"
        run.error_json = [{"code": "queue_unavailable"}]
        run.completed_at = datetime.now(UTC)
        await session.commit()
        raise AppError(503, "queue_unavailable", "Google 地點資料佇列暫時無法使用") from exc
    return run


@router.post("/place-enrichment/runs", status_code=202)
async def create_place_enrichment_run(
    payload: PlaceEnrichmentRunRequest,
    user: AdminUser,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, Any]:
    existing = await session.scalar(
        select(HotspotPlaceEnrichmentRun).where(
            HotspotPlaceEnrichmentRun.actor_user_id == user.id,
            HotspotPlaceEnrichmentRun.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        return run_payload(existing)
    settings = await load_runtime_settings(session)
    if not settings.hotspot_place_enrichment_enabled or not settings.google_maps_api_key:
        raise AppError(503, "google_maps_not_configured", "Google Maps 地點資料目前未設定")
    if not payload.confirm_usage:
        raise AppError(
            422,
            "google_maps_usage_confirmation_required",
            "請先確認預估 Google API 用量",
        )
    targets = await enrichment_targets(
        session,
        mode=payload.mode,
        country_code=payload.country_code if payload.scope == "country" else None,
        hotspot_ids=payload.hotspot_ids if payload.scope == "hotspots" else None,
    )
    scope: dict[str, object] = {"type": payload.scope}
    if payload.scope == "country":
        scope["country_code"] = cast(str, payload.country_code).upper()
    elif payload.scope == "hotspots":
        scope["hotspot_ids"] = [str(item) for item in payload.hotspot_ids]
    run = await _create_place_run(
        session,
        actor_user_id=user.id,
        idempotency_key=idempotency_key,
        mode=payload.mode,
        scope=scope,
        targets=targets,
    )
    return run_payload(run)


@router.get("/place-enrichment/runs/{run_id}")
async def get_place_enrichment_run(
    run_id: UUID, user: AdminUser, session: Session
) -> dict[str, Any]:
    _ = user
    run = await session.get(HotspotPlaceEnrichmentRun, run_id)
    if run is None:
        raise AppError(404, "hotspot_place_enrichment_not_found", "找不到這次地點資料更新")
    return run_payload(run)


@router.get("/place-profiles")
async def list_place_profiles(
    user: AdminUser,
    session: Session,
    redis: RedisDep,
    q: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    country_code: Annotated[str | None, Query(min_length=2, max_length=2)] = None,
    status: Annotated[str | None, Query(max_length=24)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> dict[str, Any]:
    _ = user
    query = select(TravelHotspot, HotspotPlaceProfile).outerjoin(
        HotspotPlaceProfile, HotspotPlaceProfile.hotspot_id == TravelHotspot.id
    )
    filters: list[Any] = [
        TravelHotspot.is_active.is_(True),
        TravelHotspot.review_status.in_(("approved", "auto_approved")),
    ]
    if q:
        term = f"%{escape_like(q.strip())}%"
        filters.append(
            or_(
                TravelHotspot.name.ilike(term, escape="\\"),
                TravelHotspot.search_text.ilike(term, escape="\\"),
            )
        )
    if country_code:
        filters.append(TravelHotspot.country_code == country_code.upper())
    if status == "missing":
        filters.append(HotspotPlaceProfile.id.is_(None))
    elif status:
        filters.append(HotspotPlaceProfile.match_status == status)
    query = query.where(*filters)
    total = int(await session.scalar(select(func.count()).select_from(query.subquery())) or 0)
    rows = (
        await session.execute(
            query.order_by(TravelHotspot.country_code, TravelHotspot.name)
            .offset((page - 1) * limit)
            .limit(limit)
        )
    ).all()
    settings = await load_runtime_settings(session)
    items = []
    for hotspot, profile in rows:
        items.append(
            {
                "hotspot_id": str(hotspot.id),
                "name": hotspot.name,
                "city_name": hotspot.city_name,
                "country_code": hotspot.country_code,
                "google_place_id": hotspot.google_place_id,
                "place_id_source": profile.place_id_source if profile else "none",
                "match_status": profile.match_status if profile else "missing",
                "match_confidence": (
                    float(profile.match_confidence)
                    if profile and profile.match_confidence is not None
                    else None
                ),
                "candidate": (
                    {
                        "place_id": profile.candidate_place_id,
                        "name": profile.candidate_name,
                        "address": profile.candidate_address,
                    }
                    if profile and profile.candidate_place_id
                    else None
                ),
                "website_review_status": (profile.website_review_status if profile else "none"),
                "provider_website_url": profile.provider_website_uri if profile else None,
                "manual_official_website_url": (
                    profile.manual_official_website_url if profile else None
                ),
                "address": profile.formatted_address if profile else None,
                "refresh_after": profile.provider_refresh_after if profile else None,
                "expires_at": profile.provider_expires_at if profile else None,
                "summary": place_summary_payload(
                    hotspot,
                    profile,
                    configured=bool(settings.google_maps_api_key),
                ),
            }
        )
    return {
        "items": items,
        "total": total,
        "page": page,
        "pages": max(1, (total + limit - 1) // limit),
        "overview": await profile_overview(session, redis, settings),
    }


@router.patch("/{hotspot_id}/place-profile")
async def update_place_profile(
    hotspot_id: UUID,
    payload: PlaceProfileUpdateRequest,
    user: AdminUser,
    session: Session,
) -> dict[str, Any]:
    hotspot = await session.get(TravelHotspot, hotspot_id)
    if hotspot is None:
        raise AppError(404, "hotspot_not_found", "找不到這個景點")
    profile = await session.scalar(
        select(HotspotPlaceProfile).where(HotspotPlaceProfile.hotspot_id == hotspot.id)
    )
    if profile is None:
        profile = HotspotPlaceProfile(
            hotspot_id=hotspot.id,
            place_id_source="legacy" if hotspot.google_place_id else "none",
            match_status="approved" if hotspot.google_place_id else "unmatched",
        )
        session.add(profile)
    needs_refresh = payload.action == "refresh"
    if payload.action == "approve":
        if profile.candidate_place_id:
            hotspot.google_place_id = profile.candidate_place_id
            profile.place_id_source = "manual"
            needs_refresh = True
        profile.match_status = "approved"
        if profile.website_review_status == "pending":
            profile.website_review_status = "approved"
    elif payload.action == "reject":
        if profile.match_status == "pending":
            profile.match_status = "rejected"
        if profile.website_review_status == "pending":
            profile.website_review_status = "rejected"
    elif payload.action == "save":
        if "google_place_id" in payload.model_fields_set:
            previous_place_id = hotspot.google_place_id
            hotspot.google_place_id = (
                payload.google_place_id.strip() if payload.google_place_id else None
            )
            profile.place_id_source = "manual" if hotspot.google_place_id else "none"
            profile.match_status = "approved" if hotspot.google_place_id else "unmatched"
            needs_refresh = bool(hotspot.google_place_id)
            if hotspot.google_place_id != previous_place_id:
                profile.provider_expires_at = datetime.now(UTC)
        if "official_website_url" in payload.model_fields_set:
            profile.manual_official_website_url = (
                canonical_official_website(payload.official_website_url)
                if payload.official_website_url
                else None
            )
            profile.website_review_status = (
                "approved" if profile.manual_official_website_url else "none"
            )
        if "official_website_source_url" in payload.model_fields_set:
            profile.manual_official_website_source_url = (
                canonical_external_url(payload.official_website_source_url)
                if payload.official_website_source_url
                else None
            )
    if payload.action in {"approve", "reject"}:
        profile.candidate_place_id = None
        profile.candidate_name = None
        profile.candidate_address = None
        profile.candidate_latitude = None
        profile.candidate_longitude = None
    profile.review_reason = payload.reason
    profile.reviewed_at = datetime.now(UTC)
    profile.reviewed_by_user_id = user.id
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action=f"hotspot_place_profile_{payload.action}",
            target=f"hotspot:{hotspot.id}",
            metadata_json={"google_place_id": hotspot.google_place_id},
        )
    )
    await session.commit()
    run = None
    if needs_refresh and hotspot.google_place_id:
        run = await _create_place_run(
            session,
            actor_user_id=user.id,
            idempotency_key=f"profile:{hotspot.id}:{uuid4()}",
            mode="force",
            scope={"type": "hotspots", "hotspot_ids": [str(hotspot.id)]},
            targets=[hotspot],
        )
    return {
        "hotspot_id": str(hotspot.id),
        "match_status": profile.match_status,
        "run": run_payload(run) if run else None,
    }


@router.post("/place-profiles/review")
async def review_place_profiles(
    payload: PlaceProfileReviewRequest,
    user: AdminUser,
    session: Session,
) -> dict[str, Any]:
    rows = (
        await session.execute(
            select(TravelHotspot, HotspotPlaceProfile)
            .join(HotspotPlaceProfile, HotspotPlaceProfile.hotspot_id == TravelHotspot.id)
            .where(TravelHotspot.id.in_(payload.ids))
        )
    ).all()
    if len(rows) != len(set(payload.ids)):
        raise AppError(404, "hotspot_place_profile_not_found", "部分地點資料不存在")
    refresh: list[TravelHotspot] = []
    now = datetime.now(UTC)
    for hotspot, profile in rows:
        if payload.action == "approve":
            if profile.candidate_place_id:
                hotspot.google_place_id = profile.candidate_place_id
                profile.place_id_source = "manual"
                refresh.append(hotspot)
            profile.match_status = "approved"
            if profile.website_review_status == "pending":
                profile.website_review_status = "approved"
        else:
            if profile.match_status == "pending":
                profile.match_status = "rejected"
            if profile.website_review_status == "pending":
                profile.website_review_status = "rejected"
        profile.candidate_place_id = None
        profile.candidate_name = None
        profile.candidate_address = None
        profile.candidate_latitude = None
        profile.candidate_longitude = None
        profile.review_reason = payload.reason
        profile.reviewed_at = now
        profile.reviewed_by_user_id = user.id
    await session.commit()
    run = None
    if refresh:
        run = await _create_place_run(
            session,
            actor_user_id=user.id,
            idempotency_key=f"review:{uuid4()}",
            mode="force",
            scope={"type": "hotspots", "hotspot_ids": [str(item.id) for item in refresh]},
            targets=refresh,
        )
    return {"updated": len(rows), "run": run_payload(run) if run else None}
