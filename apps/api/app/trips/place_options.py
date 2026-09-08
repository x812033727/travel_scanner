"""Read-only catalogue discovery for one insertion point in a private trip.

Browsing never calls a map provider. Catalogue records are rechecked when added,
so a card withdrawn after discovery cannot be published through the editor.
"""

from __future__ import annotations

import math
from typing import Any, Literal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.destinations.catalog import destination_for_id, match_destination
from app.foods.publication import publishable_merchant_filters
from app.hotspots.maps import build_map_links
from app.hotspots.service import load_hotspot_names
from app.localized_names import item_names, resolve_localized_name
from app.locations.coordinates import has_durable_coordinates
from app.models import (
    FoodFavorite,
    FoodMerchant,
    FoodMerchantFavorite,
    FoodMerchantFood,
    HotspotFavorite,
    RestaurantFavorite,
    RestaurantPlace,
    TravelHotspot,
    TripPlan,
)
from app.problems import AppError

Point = tuple[float, float]
Kind = Literal["hotspot", "merchant"]


def distance_km(first: Point, second: Point) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (*first, *second))
    haversine = (
        math.sin((lat2 - lat1) / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    )
    return 6371 * 2 * math.asin(min(1, math.sqrt(haversine)))


def rank_options(
    options: list[dict[str, Any]],
    *,
    source: str,
    origin: Point | None,
    following: Point | None,
    radius_km: int,
    q: str,
    kind: str,
    offset: int,
    limit: int,
) -> dict[str, Any]:
    query = q.strip().casefold()
    selected = []
    for option in options:
        if source == "favorites" and not option["is_saved"]:
            continue
        if kind != "all" and option["kind"] != kind:
            continue
        if query and query not in option["search_text"].casefold():
            continue
        point = (option["item"]["latitude"], option["item"]["longitude"])
        distance = distance_km(origin, point) if origin is not None else None
        if source != "favorites" and distance is not None and distance > radius_km:
            # Favourites are useful in a different part of town even when the
            # nearby list is deliberately narrow.
            if source != "discover" or not option["is_saved"]:
                continue
        detour = distance or 0.0
        if origin is not None and following is not None:
            detour = max(
                0.0, detour + distance_km(point, following) - distance_km(origin, following)
            )
        selected.append(
            {
                **option,
                "distance_km": round(distance, 2) if distance is not None else None,
                "_distance": distance or 0.0,
                "_detour": round(detour, 3),
            }
        )
    selected.sort(
        key=lambda option: (
            not option["is_saved"] if source == "discover" else False,
            option["_detour"],
            option["_distance"],
            option["title"].casefold(),
            option["key"],
        )
    )
    return {
        "items": [
            {
                key: value
                for key, value in option.items()
                if not key.startswith("_") and key != "search_text"
            }
            for option in selected[offset : offset + limit]
        ],
        "total": len(selected),
        "next_offset": offset + limit if offset + limit < len(selected) else None,
        "context": "nearby" if origin is not None else "destination",
    }


async def catalog_option(
    session: AsyncSession,
    row: TravelHotspot | FoodMerchant,
    *,
    locale: str,
    names: dict[str, str] | None = None,
    saved: bool = False,
    publication_checked: bool = False,
) -> dict[str, Any] | None:
    hotspot = isinstance(row, TravelHotspot)
    if not row.is_active or row.review_status != "approved" or row.map_match_status != "verified":
        return None
    if not has_durable_coordinates(
        row.latitude, row.longitude, row.coordinate_source_type, row.coordinate_source_url
    ):
        return None
    if (
        not isinstance(row, TravelHotspot)
        and not publication_checked
        and await session.scalar(
            select(FoodMerchant.id).where(
                FoodMerchant.id == row.id, *publishable_merchant_filters()
            )
        )
        is None
    ):
        return None
    if names is None:
        names = (
            (await load_hotspot_names(session, [row])).get(row.id, {})
            if isinstance(row, TravelHotspot)
            else row.names_json or {}
        )
    destination = destination_for_id(row.destination_id)
    city = (
        row.city_name
        if isinstance(row, TravelHotspot)
        else destination.city
        if destination
        else row.destination_id
    )
    links = build_map_links(
        name=row.name,
        local_name=(
            str(row.metadata_json.get("local_name") or "")
            if isinstance(row, TravelHotspot)
            else row.local_name
        ),
        city_name=city,
        country_code=row.country_code,
        latitude=row.latitude,
        longitude=row.longitude,
        google_place_id=row.google_place_id,
        naver_map_url=row.naver_map_url,
        map_match_status=row.map_match_status,
    )
    if not links:
        return None
    kind = "hotspot" if hotspot else "merchant"
    title = resolve_localized_name(names, locale, fallback=row.name)
    metadata = row.metadata_json if isinstance(row, TravelHotspot) else {}
    assert row.latitude is not None and row.longitude is not None
    try:
        duration = max(20, min(540, int(metadata.get("recommended_duration_minutes") or 60)))
    except (TypeError, ValueError):
        duration = 60
    provider = "naver_local" if row.country_code == "KR" else "google_places"
    return {
        "key": f"{kind}:{row.id}",
        "kind": kind,
        "id": str(row.id),
        "title": title,
        "subtitle": city,
        "destination_id": row.destination_id,
        "is_saved": saved,
        "search_text": " ".join([row.name, city, *names.values()]),
        "item": {
            "item_type": "activity" if hotspot else "custom",
            "title": title,
            "location_name": title,
            "names": item_names(title=names, location_name=names),
            "latitude": float(row.latitude),
            "longitude": float(row.longitude),
            "location_source": "hotspot_catalog" if hotspot else "food_merchant_catalog",
            "location_provider": provider,
            "provider_place_id": row.google_place_id if row.country_code != "KR" else None,
            "duration_minutes": duration,
            "fixed_time": False,
            "locked": False,
            "is_estimated": False,
            "is_skipped": False,
            "data": {
                "source_mode": "manual",
                "selection_source": "place_browser",
                "catalog_selection": {"kind": kind, "id": str(row.id)},
                f"{kind}_id": str(row.id),
                "map_links": links,
                "naver_maps_url": row.naver_map_url if row.country_code == "KR" else None,
                "place_provider": provider,
                "needs_place_confirmation": False,
                "place_match_status": "confirmed",
                "coordinate_source_type": row.coordinate_source_type,
                "coordinate_source_url": row.coordinate_source_url,
            },
        },
    }


async def resolve_catalog_selection(
    session: AsyncSession,
    selection: object,
    locale: str,
) -> dict[str, Any]:
    if not isinstance(selection, dict) or selection.get("kind") not in {"hotspot", "merchant"}:
        raise AppError(422, "itinerary_candidate_invalid", "無法辨識所選地點")
    try:
        item_id = UUID(str(selection.get("id")))
    except ValueError as exc:
        raise AppError(422, "itinerary_candidate_invalid", "無法辨識所選地點") from exc
    row = (
        await session.get(TravelHotspot, item_id)
        if selection["kind"] == "hotspot"
        else await session.get(FoodMerchant, item_id)
    )
    option = await catalog_option(session, row, locale=locale) if row is not None else None
    if option is None:
        raise AppError(422, "place_not_found", "所選地點已無法加入，請選擇其他地點")
    item: dict[str, Any] = option["item"]
    return item


async def list_place_options(
    session: AsyncSession,
    trip: TripPlan,
    *,
    locale: str,
    source: str,
    origin: Point | None,
    following: Point | None,
    radius_km: int,
    q: str,
    kind: str,
    all_cities: bool,
    offset: int,
    limit: int,
) -> dict[str, Any]:
    saved_hotspots = set(
        await session.scalars(
            select(HotspotFavorite.hotspot_id).where(HotspotFavorite.user_id == trip.user_id)
        )
    )
    saved_merchants = set(
        await session.scalars(
            select(FoodMerchantFavorite.merchant_id).where(
                FoodMerchantFavorite.user_id == trip.user_id
            )
        )
    )
    # A saved Google restaurant can refer to the same reviewed merchant. Match
    # its permanent identity without fetching or persisting provider display data.
    saved_place_ids = (
        select(RestaurantPlace.google_place_id)
        .join(RestaurantFavorite, RestaurantFavorite.restaurant_place_id == RestaurantPlace.id)
        .where(
            RestaurantFavorite.user_id == trip.user_id,
            RestaurantPlace.is_suppressed.is_(False),
            RestaurantPlace.identity_status.not_in(("moved", "not_found")),
        )
    )
    saved_merchants.update(
        await session.scalars(
            select(FoodMerchant.id).where(FoodMerchant.google_place_id.in_(saved_place_ids))
        )
    )
    # A saved dish resolves to actual published merchants, never a dish pin.
    saved_merchants.update(
        await session.scalars(
            select(FoodMerchantFood.merchant_id)
            .join(FoodFavorite, FoodFavorite.food_id == FoodMerchantFood.food_id)
            .where(FoodFavorite.user_id == trip.user_id)
        )
    )
    destination = match_destination(trip.destination_name or "")
    hotspots_query = select(TravelHotspot).where(
        TravelHotspot.is_active.is_(True),
        TravelHotspot.review_status == "approved",
        TravelHotspot.map_match_status == "verified",
    )
    merchants_query = select(FoodMerchant).where(*publishable_merchant_filters())
    if source == "favorites":
        hotspots_query = hotspots_query.where(TravelHotspot.id.in_(saved_hotspots))
        merchants_query = merchants_query.where(FoodMerchant.id.in_(saved_merchants))
    if not (source == "favorites" and all_cities):
        if destination is not None:
            hotspots_query = hotspots_query.where(TravelHotspot.destination_id == destination.id)
            merchants_query = merchants_query.where(FoodMerchant.destination_id == destination.id)
        elif origin is None:
            return {"items": [], "total": 0, "next_offset": None, "context": "destination"}
        else:
            # Unknown destination: constrain the catalogue read to the reference
            # point's neighbourhood before computing spherical distances.
            lat, lon = origin
            delta = radius_km / 110
            lng_delta = delta / max(0.01, math.cos(math.radians(lat)))
            hotspots_query = hotspots_query.where(
                TravelHotspot.latitude.between(lat - delta, lat + delta),
                TravelHotspot.longitude.between(lon - lng_delta, lon + lng_delta),
            )
            merchants_query = merchants_query.where(
                FoodMerchant.latitude.between(lat - delta, lat + delta),
                FoodMerchant.longitude.between(lon - lng_delta, lon + lng_delta),
            )
    hotspots = list(await session.scalars(hotspots_query)) if kind != "merchant" else []
    merchants = list(await session.scalars(merchants_query)) if kind != "hotspot" else []
    names = await load_hotspot_names(session, hotspots)
    options = []
    catalog_rows: list[TravelHotspot | FoodMerchant] = [*hotspots, *merchants]
    for row in catalog_rows:
        option = await catalog_option(
            session,
            row,
            locale=locale,
            names=names.get(row.id) if isinstance(row, TravelHotspot) else row.names_json,
            saved=row.id in (saved_hotspots if isinstance(row, TravelHotspot) else saved_merchants),
            publication_checked=True,
        )
        if option is not None:
            options.append(option)
    return rank_options(
        options,
        source=source,
        origin=origin,
        following=following,
        radius_km=radius_km,
        q=q,
        kind=kind,
        offset=offset,
        limit=limit,
    )
