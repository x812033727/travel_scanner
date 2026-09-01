from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Annotated, Literal, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query
from pydantic import BaseModel, Field, model_validator
from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas import ProviderSettingsUpdate
from app.admin.service import load_runtime_settings, update_provider_settings
from app.auth.service import AdminUser
from app.db import get_session
from app.hotspots.service import PUBLIC_REVIEW_STATUSES
from app.i18n import Locale
from app.infra import get_redis
from app.models import (
    AdminAuditLog,
    FoodMerchant,
    FoodMerchantSource,
    RestaurantEditorialProfile,
    RestaurantEditorialSource,
    RestaurantPlace,
    TravelHotspot,
)
from app.problems import AppError
from app.restaurants.editorial import (
    validate_claims,
    validate_editorial_url,
    validate_profile_evidence,
)
from app.restaurants.google import (
    GoogleRestaurantProvider,
    RestaurantProviderError,
    RestaurantProviderNotConfigured,
    RestaurantQuotaExceeded,
)
from app.restaurants.imports import PLACE_ID_RE, resolve_maps_input
from app.restaurants.service import (
    build_place_maps_url,
    haversine_km,
    refresh_restaurant_identity,
    save_restaurant_identity,
)

router = APIRouter(
    prefix="/admin/hotspots/restaurants",
    tags=["admin restaurant sources"],
)
Session = Annotated[AsyncSession, Depends(get_session)]
RedisDep = Annotated[Redis, Depends(get_redis)]


class RestaurantImportPreviewRequest(BaseModel):
    value: str = Field(min_length=2, max_length=4096)
    hotspot_id: UUID | None = None
    query: str | None = Field(default=None, min_length=2, max_length=255)
    locale: Locale = "zh-TW"


class RestaurantImportCommitRequest(BaseModel):
    hotspot_id: UUID
    place_id: str = Field(min_length=15, max_length=255)
    locale: Locale = "zh-TW"

    @model_validator(mode="after")
    def validate_place_id(self) -> RestaurantImportCommitRequest:
        if not PLACE_ID_RE.fullmatch(self.place_id):
            raise ValueError("invalid Google Place ID")
        return self


class RestaurantEditorialSourcePayload(BaseModel):
    source_type: Literal["merchant_official", "official_tourism"]
    source_title: str = Field(min_length=1, max_length=255)
    source_url: str = Field(min_length=8, max_length=2048)
    claims: list[Literal["display_name", "address", "official_website", "coordinates"]] = Field(
        min_length=1, max_length=4
    )


class RestaurantEditorialPayload(BaseModel):
    display_name: str = Field(min_length=1, max_length=255)
    local_name: str | None = Field(default=None, max_length=255)
    address: str | None = Field(default=None, max_length=1000)
    official_website_url: str | None = Field(default=None, max_length=2048)
    ride_latitude: float | None = Field(default=None, ge=-90, le=90)
    ride_longitude: float | None = Field(default=None, ge=-180, le=180)
    review_status: Literal["pending", "approved", "rejected", "disabled"] = "pending"
    sources: list[RestaurantEditorialSourcePayload] = Field(min_length=1, max_length=10)

    @model_validator(mode="after")
    def validate_coordinate_pair(self) -> RestaurantEditorialPayload:
        if (self.ride_latitude is None) != (self.ride_longitude is None):
            raise ValueError("ride coordinates must be provided together")
        return self


class RestaurantAutomationPayload(BaseModel):
    enabled: bool


async def _hotspot_for_import(
    session: AsyncSession, hotspot_id: UUID | None
) -> TravelHotspot | None:
    if hotspot_id is None:
        return None
    hotspot = await session.get(TravelHotspot, hotspot_id)
    if (
        hotspot is None
        or not hotspot.is_active
        or hotspot.review_status not in PUBLIC_REVIEW_STATUSES
    ):
        raise AppError(404, "hotspot_not_found", "找不到這個景點")
    return hotspot


@router.post("/imports/preview")
async def preview_restaurant_import(
    payload: RestaurantImportPreviewRequest,
    user: AdminUser,
    session: Session,
    redis: RedisDep,
) -> dict[str, object]:
    del user
    hotspot = await _hotspot_for_import(session, payload.hotspot_id)
    settings = await load_runtime_settings(session)
    try:
        resolution = await resolve_maps_input(payload.value)
        place_ids = [resolution.place_id] if resolution.place_id else []
        query = payload.query or resolution.suggested_query
        if not place_ids:
            if not query:
                raise AppError(
                    422,
                    "restaurant_import_query_required",
                    "網址中沒有 Place ID，請補上店名或地址以執行免費 IDs Only 搜尋",
                )
            provider = GoogleRestaurantProvider(redis, settings, locale=payload.locale)
            place_ids = list(
                await provider.search_ids_only(
                    query,
                    latitude=float(hotspot.latitude)
                    if hotspot and hotspot.latitude is not None
                    else None,
                    longitude=float(hotspot.longitude)
                    if hotspot and hotspot.longitude is not None
                    else None,
                )
            )
    except RestaurantProviderNotConfigured as exc:
        raise AppError(503, "restaurant_google_not_configured", "Google Places 尚未設定") from exc
    except RestaurantProviderError as exc:
        raise AppError(503, "restaurant_provider_unavailable", "Google IDs Only 搜尋失敗") from exc
    return {
        "source": resolution.source,
        "expanded_url": resolution.expanded_url,
        "query_used": query if not resolution.place_id else None,
        "pricing": {
            "sku": "Text Search Essentials (IDs Only)",
            "billing": "no_charge",
            "provider_display_fields_requested": False,
        },
        "candidates": [
            {"place_id": place_id, "maps_url": build_place_maps_url(place_id)}
            for place_id in place_ids
        ],
    }


@router.post("/imports", status_code=201)
async def commit_restaurant_import(
    payload: RestaurantImportCommitRequest,
    user: AdminUser,
    session: Session,
    redis: RedisDep,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=255)],
) -> dict[str, object]:
    hotspot = await _hotspot_for_import(session, payload.hotspot_id)
    assert hotspot is not None
    cache_key = (
        "restaurant-import:v1:"
        + hashlib.sha256(f"{user.id}:{idempotency_key}".encode()).hexdigest()
    )
    try:
        cached = await redis.get(cache_key)
        if cached and cached != "pending":
            raw = cached.decode() if isinstance(cached, bytes) else str(cached)
            return cast(dict[str, object], json.loads(raw))
        if not await redis.set(cache_key, "pending", ex=300, nx=True):
            raise AppError(409, "restaurant_import_in_progress", "相同匯入正在處理中")
    except RedisError as exc:
        raise AppError(
            503,
            "restaurant_import_idempotency_unavailable",
            "目前無法安全保證匯入不重複，請稍後再試",
        ) from exc
    settings = await load_runtime_settings(session)
    provider = GoogleRestaurantProvider(redis, settings, locale=payload.locale)
    try:
        snapshot = await provider.details(payload.place_id)
    except RestaurantQuotaExceeded as exc:
        await redis.delete(cache_key)
        raise AppError(429, "restaurant_google_budget_exhausted", "餐廳確認額度已用完") from exc
    except RestaurantProviderNotConfigured as exc:
        await redis.delete(cache_key)
        raise AppError(503, "restaurant_google_not_configured", "Google Places 尚未設定") from exc
    except RestaurantProviderError as exc:
        await redis.delete(cache_key)
        raise AppError(503, "restaurant_provider_unavailable", "目前無法確認餐廳資料") from exc
    if snapshot is None or not snapshot.qualified:
        await redis.delete(cache_key)
        raise AppError(
            422,
            "restaurant_threshold_not_met",
            "店家必須至少 3.8 顆星且有 1,000 則評論，並仍在營業",
        )
    if (
        snapshot.latitude is None
        or snapshot.longitude is None
        or hotspot.latitude is None
        or hotspot.longitude is None
    ):
        await redis.delete(cache_key)
        raise AppError(422, "restaurant_location_unavailable", "店家或景點缺少可比對座標")
    distance_km = haversine_km(
        float(hotspot.latitude),
        float(hotspot.longitude),
        snapshot.latitude,
        snapshot.longitude,
    )
    if distance_km > 10:
        await redis.delete(cache_key)
        raise AppError(422, "restaurant_outside_hotspot_radius", "店家距離景點超過 10 公里")
    place = await save_restaurant_identity(
        session,
        hotspot.id,
        payload.place_id,
        run_id=None,
        radius_meters=10_000,
    )
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="restaurant_place_imported",
            target=f"restaurant-place:{place.id}",
            metadata_json={
                "hotspot_id": str(hotspot.id),
                "idempotency_key": idempotency_key,
                "threshold_verified_live": True,
            },
        )
    )
    await session.commit()
    response: dict[str, object] = {
        "place_id": place.google_place_id,
        "maps_url": place.generated_maps_url,
        "threshold": {"rating": snapshot.rating, "review_count": snapshot.review_count},
        "distance_km": round(distance_km, 2),
        "persistence": "Only Place ID and the app-generated Maps URL were saved.",
    }
    try:
        await redis.set(
            cache_key,
            json.dumps(response, ensure_ascii=False),
            ex=86_400,
        )
    except RedisError:
        pass
    return response


@router.put("/places/{place_id}/editorial")
async def put_restaurant_editorial(
    place_id: str,
    payload: RestaurantEditorialPayload,
    user: AdminUser,
    session: Session,
) -> dict[str, object]:
    place = await session.scalar(
        select(RestaurantPlace).where(RestaurantPlace.google_place_id == place_id)
    )
    if place is None:
        raise AppError(404, "restaurant_place_not_found", "找不到這個餐飲地點")
    source_values = [
        {
            "source_url": validate_editorial_url(source.source_url),
            "claims": validate_claims(list(source.claims)),
        }
        for source in payload.sources
    ]
    validate_profile_evidence(
        display_name=payload.display_name,
        address=payload.address,
        official_website_url=payload.official_website_url,
        ride_latitude=payload.ride_latitude,
        ride_longitude=payload.ride_longitude,
        sources=source_values,
    )
    profile = await session.scalar(
        select(RestaurantEditorialProfile).where(
            RestaurantEditorialProfile.restaurant_place_id == place.id
        )
    )
    if profile is None:
        profile = RestaurantEditorialProfile(
            restaurant_place_id=place.id,
            display_name=payload.display_name.strip(),
        )
        session.add(profile)
        await session.flush()
    profile.display_name = payload.display_name.strip()
    profile.local_name = payload.local_name.strip() if payload.local_name else None
    profile.address = payload.address.strip() if payload.address else None
    profile.official_website_url = (
        validate_editorial_url(payload.official_website_url)
        if payload.official_website_url
        else None
    )
    profile.ride_latitude = (
        Decimal(str(payload.ride_latitude)) if payload.ride_latitude is not None else None
    )
    profile.ride_longitude = (
        Decimal(str(payload.ride_longitude)) if payload.ride_longitude is not None else None
    )
    profile.review_status = payload.review_status
    if payload.review_status == "approved":
        profile.verified_at = datetime.now(UTC)
        profile.verified_by_user_id = user.id
    else:
        profile.verified_at = None
        profile.verified_by_user_id = None
    await session.execute(
        delete(RestaurantEditorialSource).where(RestaurantEditorialSource.profile_id == profile.id)
    )
    for source in payload.sources:
        session.add(
            RestaurantEditorialSource(
                profile_id=profile.id,
                source_type=source.source_type,
                source_title=source.source_title.strip(),
                source_url=validate_editorial_url(source.source_url),
                claims_json=validate_claims(list(source.claims)),
                last_verified_at=datetime.now(UTC),
            )
        )
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="restaurant_editorial_updated",
            target=f"restaurant-place:{place.id}",
            metadata_json={
                "review_status": payload.review_status,
                "source_count": len(payload.sources),
            },
        )
    )
    await session.commit()
    return {
        "place_id": place.google_place_id,
        "review_status": profile.review_status,
        "verified_at": profile.verified_at,
        "source_count": len(payload.sources),
    }


@router.get("/places/{place_id}/editorial")
async def get_restaurant_editorial(
    place_id: str,
    user: AdminUser,
    session: Session,
) -> dict[str, object]:
    del user
    place = await session.scalar(
        select(RestaurantPlace).where(RestaurantPlace.google_place_id == place_id)
    )
    if place is None:
        raise AppError(404, "restaurant_place_not_found", "找不到這個餐飲地點")
    profile = await session.scalar(
        select(RestaurantEditorialProfile).where(
            RestaurantEditorialProfile.restaurant_place_id == place.id
        )
    )
    if profile is None:
        return {
            "place_id": place.google_place_id,
            "maps_url": place.generated_maps_url,
            "profile": None,
        }
    sources = list(
        (
            await session.scalars(
                select(RestaurantEditorialSource)
                .where(RestaurantEditorialSource.profile_id == profile.id)
                .order_by(RestaurantEditorialSource.created_at)
            )
        ).all()
    )
    return {
        "place_id": place.google_place_id,
        "maps_url": place.generated_maps_url,
        "profile": {
            "display_name": profile.display_name,
            "local_name": profile.local_name,
            "address": profile.address,
            "official_website_url": profile.official_website_url,
            "ride_latitude": float(profile.ride_latitude)
            if profile.ride_latitude is not None
            else None,
            "ride_longitude": float(profile.ride_longitude)
            if profile.ride_longitude is not None
            else None,
            "review_status": profile.review_status,
            "sources": [
                {
                    "source_type": source.source_type,
                    "source_title": source.source_title,
                    "source_url": source.source_url,
                    "claims": source.claims_json,
                    "last_verified_at": source.last_verified_at,
                }
                for source in sources
            ],
        },
    }


@router.get("/editorial-coverage")
async def restaurant_editorial_coverage(
    user: AdminUser,
    session: Session,
    status: Annotated[str | None, Query(max_length=24)] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
) -> dict[str, object]:
    del user
    rows = (
        await session.execute(
            select(RestaurantPlace, RestaurantEditorialProfile)
            .outerjoin(
                RestaurantEditorialProfile,
                RestaurantEditorialProfile.restaurant_place_id == RestaurantPlace.id,
            )
            .where(RestaurantPlace.is_suppressed.is_(False))
            .order_by(RestaurantEditorialProfile.updated_at.desc().nullslast(), RestaurantPlace.id)
            .limit(limit)
        )
    ).all()
    items: list[dict[str, object]] = []
    for place, profile in rows:
        item_status = profile.review_status if profile else "missing"
        if status and status != item_status:
            continue
        source_count = 0
        if profile:
            source_count = int(
                await session.scalar(
                    select(func.count(RestaurantEditorialSource.id)).where(
                        RestaurantEditorialSource.profile_id == profile.id
                    )
                )
                or 0
            )
        items.append(
            {
                "place_id": place.google_place_id,
                "maps_url": place.generated_maps_url,
                "identity_status": place.identity_status,
                "identity_checked_at": place.identity_checked_at,
                "review_status": item_status,
                "display_name": profile.display_name if profile else None,
                "official_website_url": profile.official_website_url if profile else None,
                "has_ride_coordinates": bool(profile and profile.ride_latitude is not None),
                "source_count": source_count,
            }
        )
    merchant_rows = list(
        (
            await session.execute(
                select(
                    FoodMerchant.id,
                    FoodMerchant.country_code,
                    FoodMerchant.official_website_url,
                )
            )
        ).all()
    )
    merchant_context_ids = set(
        (
            await session.scalars(
                select(FoodMerchantSource.merchant_id).where(
                    FoodMerchantSource.source_scope == "destination_context",
                    FoodMerchantSource.is_current.is_(True),
                )
            )
        ).all()
    )
    merchant_direct_ids = set(
        (
            await session.scalars(
                select(FoodMerchantSource.merchant_id).where(
                    FoodMerchantSource.source_scope.in_(
                        ("merchant_listing", "merchant_website", "coordinates")
                    ),
                    FoodMerchantSource.is_current.is_(True),
                )
            )
        ).all()
    )
    merchant_country_coverage: dict[str, dict[str, int | str]] = {}
    for merchant_id, country_code, official_website_url in merchant_rows:
        country = merchant_country_coverage.setdefault(
            country_code,
            {
                "country_code": country_code,
                "total": 0,
                "destination_context": 0,
                "direct_merchant_evidence": 0,
                "official_website": 0,
            },
        )
        country["total"] = int(country["total"]) + 1
        if merchant_id in merchant_context_ids:
            country["destination_context"] = int(country["destination_context"]) + 1
        if merchant_id in merchant_direct_ids:
            country["direct_merchant_evidence"] = int(country["direct_merchant_evidence"]) + 1
        if official_website_url:
            country["official_website"] = int(country["official_website"]) + 1
    merchant_total = len(merchant_rows)
    merchant_context = len(merchant_context_ids)
    merchant_direct = len(merchant_direct_ids)
    return {
        "items": items,
        "restaurant_places": {
            "listed": len(items),
            "approved": sum(item["review_status"] == "approved" for item in items),
            "missing": sum(item["review_status"] == "missing" for item in items),
        },
        "food_merchants": {
            "total": merchant_total,
            "destination_context": merchant_context,
            "direct_merchant_evidence": merchant_direct,
            "official_website": sum(bool(row.official_website_url) for row in merchant_rows),
            "by_country": [
                merchant_country_coverage[country_code]
                for country_code in sorted(merchant_country_coverage)
            ],
            "disclosure": (
                "Destination context proves only the official regional food guide exists; "
                "it does not prove the guide lists that merchant."
            ),
        },
    }


@router.post("/places/{place_id}/refresh-identity")
async def refresh_place_identity(
    place_id: str,
    user: AdminUser,
    session: Session,
    redis: RedisDep,
) -> dict[str, object]:
    place = await session.scalar(
        select(RestaurantPlace).where(RestaurantPlace.google_place_id == place_id)
    )
    if place is None:
        raise AppError(404, "restaurant_place_not_found", "找不到這個餐飲地點")
    settings = await load_runtime_settings(session)
    provider = GoogleRestaurantProvider(redis, settings)
    try:
        result = await refresh_restaurant_identity(session, provider, place)
    except RestaurantProviderNotConfigured as exc:
        raise AppError(503, "restaurant_google_not_configured", "Google Places 尚未設定") from exc
    except RestaurantProviderError as exc:
        raise AppError(503, "restaurant_provider_unavailable", "Place ID 狀態確認失敗") from exc
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="restaurant_place_identity_refreshed",
            target=f"restaurant-place:{place.id}",
            metadata_json={"status": result.status, "moved_place_id": result.moved_place_id},
        )
    )
    await session.commit()
    return {
        "place_id": place_id,
        "status": result.status,
        "moved_place_id": result.moved_place_id,
        "checked_at": place.identity_checked_at,
        "pricing": "Places IDs Only; tracked separately from paid restaurant calls.",
    }


@router.post("/identity-refreshes")
async def refresh_stale_place_identities(
    user: AdminUser,
    session: Session,
    redis: RedisDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 25,
) -> dict[str, object]:
    settings = await load_runtime_settings(session)
    cutoff = datetime.now(UTC) - timedelta(days=180)
    places = list(
        (
            await session.scalars(
                select(RestaurantPlace)
                .where(
                    or_(
                        RestaurantPlace.identity_checked_at.is_(None),
                        RestaurantPlace.identity_checked_at < cutoff,
                    )
                )
                .order_by(RestaurantPlace.identity_checked_at.asc().nullsfirst())
                .limit(limit)
            )
        ).all()
    )
    provider = GoogleRestaurantProvider(redis, settings)
    counts = {"active": 0, "moved": 0, "not_found": 0, "failed": 0}
    for place in places:
        try:
            result = await refresh_restaurant_identity(session, provider, place)
            counts[result.status] += 1
        except RestaurantProviderError:
            counts["failed"] += 1
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="restaurant_place_identity_batch_refreshed",
            target="restaurant-places",
            metadata_json={"requested": len(places), **counts},
        )
    )
    await session.commit()
    return {"requested": len(places), "counts": counts}


@router.patch("/automation")
async def update_restaurant_automation(
    payload: RestaurantAutomationPayload,
    user: AdminUser,
    session: Session,
    redis: RedisDep,
) -> dict[str, object]:
    await update_provider_settings(
        session,
        "google_maps",
        ProviderSettingsUpdate(config={"restaurant_scan_enabled": payload.enabled}),
        user,
        redis,
    )
    return {
        "enabled": payload.enabled,
        "message": "餐廳自動掃描已啟用" if payload.enabled else "餐廳自動掃描已暫停",
    }
