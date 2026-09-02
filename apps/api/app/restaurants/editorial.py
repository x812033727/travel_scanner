from __future__ import annotations

import ipaddress
from collections import defaultdict
from decimal import Decimal
from typing import Any
from urllib.parse import urlencode, urlparse
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    FoodMerchant,
    FoodMerchantSource,
    RestaurantEditorialProfile,
    RestaurantEditorialSource,
    RestaurantPlace,
)
from app.problems import AppError

EDITORIAL_CLAIMS = frozenset({"display_name", "address", "official_website", "coordinates"})
BLOCKED_SOURCE_HOSTS = frozenset(
    {
        "google.com",
        "www.google.com",
        "maps.google.com",
        "maps.app.goo.gl",
        "goo.gl",
        "map.naver.com",
    }
)


def validate_editorial_url(value: str) -> str:
    candidate = value.strip()
    parsed = urlparse(candidate)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise AppError(422, "restaurant_source_url_invalid", "來源必須是公開 HTTPS 網址")
    if parsed.port not in {None, 443}:
        raise AppError(422, "restaurant_source_url_invalid", "來源網址不可使用自訂連接埠")
    host = parsed.hostname.casefold().rstrip(".")
    if (
        host in BLOCKED_SOURCE_HOSTS
        or ".google." in host
        or host.startswith("google.")
        or host.endswith(".naver.com")
    ):
        raise AppError(
            422,
            "restaurant_source_provider_owned",
            "Google／地圖頁不可當成 Mokaair 自有編輯資料來源",
        )
    if host in {"localhost", "localhost.localdomain"}:
        raise AppError(422, "restaurant_source_url_private", "來源網址不可指向內部網路")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise AppError(422, "restaurant_source_url_private", "來源網址不可指向內部網路")
    return candidate


def validate_claims(claims: list[str]) -> list[str]:
    normalized = list(dict.fromkeys(item.strip() for item in claims if item.strip()))
    if not normalized or any(item not in EDITORIAL_CLAIMS for item in normalized):
        raise AppError(422, "restaurant_source_claims_invalid", "來源佐證欄位不完整或不支援")
    return normalized


def validate_profile_evidence(
    *,
    display_name: str,
    address: str | None,
    official_website_url: str | None,
    ride_latitude: float | Decimal | None,
    ride_longitude: float | Decimal | None,
    sources: list[dict[str, Any]],
) -> None:
    if (ride_latitude is None) != (ride_longitude is None):
        raise AppError(422, "restaurant_coordinate_pair_required", "叫車座標必須同時提供經緯度")
    required = {"display_name"}
    if address:
        required.add("address")
    if official_website_url:
        validate_editorial_url(official_website_url)
        required.add("official_website")
    if ride_latitude is not None:
        required.add("coordinates")
    supported: set[str] = set()
    for source in sources:
        validate_editorial_url(str(source["source_url"]))
        supported.update(validate_claims(list(source.get("claims") or [])))
    missing = sorted(required - supported)
    if missing:
        raise AppError(
            422,
            "restaurant_source_evidence_missing",
            f"以下欄位缺少官方來源佐證：{', '.join(missing)}",
        )
    if not display_name.strip():
        raise AppError(422, "restaurant_editorial_name_required", "請輸入可由來源佐證的店名")


def build_uber_url(
    latitude: float | Decimal,
    longitude: float | Decimal,
    name: str,
) -> str:
    query = urlencode(
        {
            "action": "setPickup",
            "pickup": "my_location",
            "dropoff[latitude]": str(latitude),
            "dropoff[longitude]": str(longitude),
            "dropoff[nickname]": name,
        }
    )
    return f"https://m.uber.com/ul/?{query}"


async def editorial_by_google_place_id(
    session: AsyncSession,
    place_ids: list[str],
) -> dict[str, dict[str, Any]]:
    if not place_ids:
        return {}
    rows = (
        await session.execute(
            select(RestaurantPlace, RestaurantEditorialProfile)
            .join(
                RestaurantEditorialProfile,
                RestaurantEditorialProfile.restaurant_place_id == RestaurantPlace.id,
            )
            .where(
                RestaurantPlace.google_place_id.in_(place_ids),
                RestaurantEditorialProfile.review_status == "approved",
            )
        )
    ).all()
    profile_ids = [profile.id for _, profile in rows]
    sources = list(
        (
            await session.scalars(
                select(RestaurantEditorialSource)
                .where(RestaurantEditorialSource.profile_id.in_(profile_ids))
                .order_by(RestaurantEditorialSource.source_type, RestaurantEditorialSource.id)
            )
        ).all()
    )
    sources_by_profile: dict[UUID, list[dict[str, Any]]] = defaultdict(list)
    for source in sources:
        sources_by_profile[source.profile_id].append(
            {
                "type": source.source_type,
                "title": source.source_title,
                "url": source.source_url,
                "claims": source.claims_json,
                "verified_at": source.last_verified_at.isoformat(),
            }
        )
    result: dict[str, dict[str, Any]] = {}
    for place, profile in rows:
        uber_url = None
        if profile.ride_latitude is not None and profile.ride_longitude is not None:
            uber_url = build_uber_url(
                profile.ride_latitude,
                profile.ride_longitude,
                profile.display_name,
            )
        result[place.google_place_id] = {
            "name": profile.display_name,
            "local_name": profile.local_name,
            "address": profile.address,
            "official_website_url": profile.official_website_url,
            "uber_url": uber_url,
            "ride_location": (
                {
                    "latitude": float(profile.ride_latitude),
                    "longitude": float(profile.ride_longitude),
                }
                if profile.ride_latitude is not None and profile.ride_longitude is not None
                else None
            ),
            "source_kind": "restaurant_editorial",
            "sources": sources_by_profile.get(profile.id, []),
            "verified_at": profile.verified_at.isoformat() if profile.verified_at else None,
        }

    remaining = [place_id for place_id in place_ids if place_id not in result]
    if not remaining:
        return result
    merchants = list(
        (
            await session.scalars(
                select(FoodMerchant).where(
                    FoodMerchant.google_place_id.in_(remaining),
                    FoodMerchant.review_status == "approved",
                    FoodMerchant.is_active.is_(True),
                    FoodMerchant.map_match_status == "verified",
                )
            )
        ).all()
    )
    merchant_ids = [merchant.id for merchant in merchants]
    merchant_sources = list(
        (
            await session.scalars(
                select(FoodMerchantSource)
                .where(
                    FoodMerchantSource.merchant_id.in_(merchant_ids),
                    FoodMerchantSource.is_current.is_(True),
                )
                .order_by(FoodMerchantSource.source_scope, FoodMerchantSource.id)
            )
        ).all()
    )
    sources_by_merchant: dict[UUID, list[dict[str, Any]]] = defaultdict(list)
    for merchant_source in merchant_sources:
        sources_by_merchant[merchant_source.merchant_id].append(
            {
                "type": merchant_source.source_type,
                "scope": merchant_source.source_scope,
                "title": merchant_source.source_title,
                "url": merchant_source.source_url,
                "claims": merchant_source.claims_json,
                "verified_at": merchant_source.last_verified_at.isoformat(),
            }
        )
    for merchant in merchants:
        assert merchant.google_place_id is not None
        uber_url = None
        if merchant.latitude is not None and merchant.longitude is not None:
            uber_url = build_uber_url(merchant.latitude, merchant.longitude, merchant.name)
        result[merchant.google_place_id] = {
            "name": merchant.name,
            "local_name": merchant.local_name,
            "address": merchant.address,
            "official_website_url": merchant.official_website_url,
            "uber_url": uber_url,
            "ride_location": (
                {
                    "latitude": float(merchant.latitude),
                    "longitude": float(merchant.longitude),
                }
                if merchant.latitude is not None and merchant.longitude is not None
                else None
            ),
            "source_kind": "food_merchant",
            "sources": sources_by_merchant.get(merchant.id, []),
            "verified_at": merchant.verified_at.isoformat() if merchant.verified_at else None,
        }
    return result
