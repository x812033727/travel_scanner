from datetime import date
from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.auth.service import CurrentUser
from app.config import get_settings
from app.db import get_session
from app.destinations.catalog import DESTINATIONS, destination_for_code, destination_for_id
from app.hotspots.areas import area_by_code
from app.hotspots.cities import CITY_BY_DESTINATION_ID
from app.hotspots.guides import canonical_external_url, list_guides, resolve_guide_open
from app.hotspots.maps import build_map_links
from app.hotspots.places import place_detail_payload
from app.hotspots.service import hotspot_facets, list_rankings, load_hotspot_names
from app.i18n import Locale, current_locale
from app.infra import enforce_named_rate_limit, get_redis
from app.localized_names import item_names
from app.locations.coordinates import has_durable_coordinates
from app.models import HotspotPlaceProfile, TravelHotspot, TripPlanItem
from app.problems import AppError
from app.trips.router import load_items, owned_trip, persist_system_schedule_change

router = APIRouter(prefix="/hotspots", tags=["hotspots"])
Session = Annotated[AsyncSession, Depends(get_session)]
RequestLocale = Annotated[Locale, Depends(current_locale)]


class HotspotTripSelectionRequest(BaseModel):
    trip_id: UUID
    version: int = Field(ge=1)
    day_date: date


def _resolve_destination(
    city_code: str | None, destination_id: str | None
) -> tuple[str | None, str | None]:
    by_code = destination_for_code(city_code) if city_code else None
    by_id = destination_for_id(destination_id) if destination_id else None
    if city_code and by_code is None:
        raise AppError(422, "unsupported_city_code", "目前不支援這個城市代碼")
    if destination_id and by_id is None:
        raise AppError(422, "unsupported_destination", "目前不支援這個目的地")
    if by_code and by_code.role == "extension" and not destination_id:
        raise AppError(422, "destination_id_required", "延伸城市請使用 destination_id")
    if by_code and by_id and by_code.id != by_id.id:
        raise AppError(422, "destination_mismatch", "city_code 與 destination_id 不一致")
    selected = by_id or by_code
    return (city_code.upper() if city_code else None, selected.id if selected else None)


def _resolve_area(destination_id: str | None, area: str | None) -> str | None:
    # Area codes are only unique inside a city ("old-town" exists in several), so an
    # area filter is meaningless without the destination that scopes it.
    if not area:
        return None
    city = CITY_BY_DESTINATION_ID.get(destination_id) if destination_id else None
    if city is None:
        raise AppError(422, "area_requires_destination", "篩選區域時必須同時指定目的地")
    if area_by_code(city.code, area) is None:
        raise AppError(422, "unsupported_area", "這個目的地沒有這個區域")
    return area


@router.get("/sources")
async def hotspot_sources(session: Session) -> dict[str, Any]:
    runtime = await load_runtime_settings(session)
    settings = get_settings()
    return {
        "collection_interval_seconds": settings.hotspot_collection_interval_seconds,
        "sources": [
            {
                "id": "curated_catalog",
                "name": "Mokaair 精選主檔",
                "status": "ready",
                "purpose": "建立景點識別、別名、城市與分類；只作冷啟動基準",
                "persistence": "景點主檔與基準分數",
            },
            {
                "id": "wikimedia_discovery",
                "name": "Wikipedia + Wikidata 探索",
                "status": "ready" if settings.hotspot_discovery_enabled else "disabled",
                "purpose": "每週探索鄰近條目，以 Wikidata 類型、名稱與座標分級發布",
                "persistence": "保存 QID、分類、距離、來源與審核狀態",
            },
            {
                "id": "wikimedia_pageviews",
                "name": "Wikimedia Analytics",
                "status": "ready" if settings.hotspot_wikimedia_enabled else "disabled",
                "purpose": "比較最近 30 天與前 30 天的公開頁面瀏覽趨勢",
                "persistence": "只保存每日彙總數字與來源日期",
            },
            {
                "id": "google_places",
                "name": "Google Places",
                "status": (
                    "ready"
                    if runtime.google_maps_api_key and runtime.hotspot_place_enrichment_enabled
                    else "not_configured"
                ),
                "purpose": "補齊地圖、地址、營業時間與官方網站",
                "persistence": "Place ID 長期保存；地點內容最長快取 30 天並標示來源",
            },
            {
                "id": "youtube_guides",
                "name": "YouTube 景點介紹",
                "status": "ready"
                if runtime.hotspot_guide_youtube_enabled and runtime.hotspot_guide_youtube_api_key
                else "not_configured",
                "purpose": "依目前語系探索景點影片，管理員核准後才公開",
                "persistence": "保存官方 metadata，最遲 30 天內刷新或刪除",
            },
            {
                "id": "brave_guides",
                "name": "Brave 多語文章搜尋",
                "status": "ready"
                if runtime.hotspot_guide_brave_enabled and runtime.hotspot_guide_brave_api_key
                else "not_configured",
                "purpose": "依目前語系探索旅遊文章，管理員核准後才公開",
                "persistence": "只保存標題、短摘要、來源與 canonical URL",
            },
            {
                "id": "reddit_discussions",
                "name": "Reddit 討論",
                "status": "requires_agreement",
                "purpose": "取得適用商業授權後，才加入貼文數與互動量等彙總訊號",
                "persistence": "目前不蒐集使用者內容",
            },
        ],
    }


@router.get("/rankings")
async def hotspot_rankings(
    session: Session,
    locale: RequestLocale,
    q: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    city_code: Annotated[str | None, Query(min_length=3, max_length=3)] = None,
    destination_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    country_code: Annotated[str | None, Query(min_length=2, max_length=2)] = None,
    category: Annotated[str | None, Query(min_length=2, max_length=32)] = None,
    role: Annotated[Literal["primary", "secondary", "extension"] | None, Query()] = None,
    area: Annotated[str | None, Query(min_length=2, max_length=32)] = None,
    after_rank: Annotated[int | None, Query(ge=0)] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    style: Literal["all", "deep"] = "all",
) -> dict[str, Any]:
    resolved_city_code, resolved_destination_id = _resolve_destination(city_code, destination_id)
    resolved_area = _resolve_area(resolved_destination_id, area)
    runtime = await load_runtime_settings(session)
    result = await list_rankings(
        session,
        q=q,
        city_code=resolved_city_code if destination_id is None else None,
        destination_id=resolved_destination_id if destination_id is not None else None,
        country_code=country_code,
        category=category,
        role=role,
        area=resolved_area,
        after_rank=after_rank,
        limit=limit,
        style=style,
        locale=locale,
        places_configured=bool(
            runtime.google_maps_api_key and runtime.hotspot_place_enrichment_enabled
        ),
    )
    for item in result["items"]:
        source_urls = item.pop("source_urls", [])
        item["has_source"] = bool(source_urls)
    return result


@router.get("/facets")
async def hotspots_facets(session: Session, locale: RequestLocale) -> dict[str, Any]:
    return await hotspot_facets(session, locale)


@router.get("/for-planner")
async def hotspots_for_planner(
    session: Session,
    locale: RequestLocale,
    city_code: Annotated[str | None, Query(min_length=3, max_length=3)] = None,
    destination_id: Annotated[str | None, Query(min_length=2, max_length=64)] = None,
    interests: Annotated[str | None, Query(max_length=200)] = None,
    limit: Annotated[int, Query(ge=1, le=12)] = 8,
    style: Literal["all", "deep"] = "all",
    days: Annotated[int | None, Query(ge=1, le=30)] = None,
    include_extensions: bool = False,
    extension_ids: Annotated[str | None, Query(max_length=200)] = None,
) -> dict[str, Any]:
    if not city_code and not destination_id:
        raise AppError(422, "destination_required", "必須提供 city_code 或 destination_id")
    resolved_city_code, resolved_destination_id = _resolve_destination(city_code, destination_id)
    runtime = await load_runtime_settings(session)
    requested = {item.strip().casefold() for item in (interests or "").split(",") if item.strip()}
    result = await list_rankings(
        session,
        city_code=resolved_city_code if destination_id is None else None,
        destination_id=resolved_destination_id if destination_id is not None else None,
        limit=50,
        style=style,
        locale=locale,
        places_configured=bool(
            runtime.google_maps_api_key and runtime.hotspot_place_enrichment_enabled
        ),
    )
    items = result["items"]
    if style == "deep" and days == 1:
        items = [item for item in items if item["depth_kind"] != "day_trip"]
    if requested:
        matched = [item for item in items if item["category"] in requested]
        unmatched = [item for item in items if item["category"] not in requested]
        items = matched + unmatched

    def planner_ready(item: dict[str, Any]) -> bool:
        return bool(
            item["map_match_status"] == "verified"
            and has_durable_coordinates(
                item["latitude"],
                item["longitude"],
                item["coordinate_source"].get("type"),
                item["coordinate_source"].get("url"),
            )
            and item["map_links"]
        )

    items = [item for item in items if planner_ready(item)]
    chosen_extensions: list[str] = []
    extension_items: list[dict[str, Any]] = []
    if include_extensions and resolved_destination_id and (days or 0) >= 4:
        allowed = 2 if (days or 0) >= 7 else 1
        explicit = {
            item.strip().casefold() for item in (extension_ids or "").split(",") if item.strip()
        }
        children = [
            item
            for item in DESTINATIONS
            if item.parent_destination_id == resolved_destination_id
            and (not explicit or item.id in explicit)
        ][:allowed]
        for child in children:
            child_result = await list_rankings(
                session,
                destination_id=child.id,
                limit=4,
                style=style,
                locale=locale,
                places_configured=bool(
                    runtime.google_maps_api_key and runtime.hotspot_place_enrichment_enabled
                ),
            )
            child_items = [item for item in child_result["items"] if planner_ready(item)]
            if child_items:
                extension_items.append(child_items[0])
                chosen_extensions.append(child.id)
    if extension_items:
        # Cross-city choices must survive the endpoint limit instead of being
        # hidden behind a full page of primary-destination candidates.
        items = items[: max(0, limit - len(extension_items))] + extension_items
    recommendations = [
        {
            "hotspot_id": item["id"],
            "name": item["name"],
            "names": item["names"],
            "category": item["category"],
            "latitude": item["latitude"],
            "longitude": item["longitude"],
            "coordinate_source": item["coordinate_source"],
            "map_match_status": item["map_match_status"],
            "popularity_score": item["score"],
            "popularity_rank": item["rank"],
            "trend": item["trend_label"],
            "is_estimate": item["is_estimate"],
            "sources": item["sources"],
            "is_deep_travel": item["is_deep_travel"],
            "depth_kind": item["depth_kind"],
            "depth_score": item["depth_score"],
            "depth_reason": item["depth_reason"],
            "access_minutes": item["access_minutes"],
            "recommended_duration_minutes": item["recommended_duration_minutes"],
            "destination_id": item["destination_id"],
            "destination_role": item["destination_role"],
            "parent_destination_id": item["parent_destination_id"],
            "is_cross_city": item["is_cross_city"],
            "map_links": item["map_links"],
        }
        for item in items[:limit]
    ]
    return {
        "city_code": resolved_city_code,
        "destination_id": resolved_destination_id,
        "observed_on": result["observed_on"],
        "style": style,
        "days": days,
        "included_extension_ids": chosen_extensions,
        "recommendations": recommendations,
        "planner_note": "熱門度只作候選訊號，仍須配合營業時間、距離與旅客偏好排程",
    }


@router.post("/{hotspot_id}/trip-selections")
async def select_hotspot_for_trip(
    hotspot_id: UUID,
    payload: HotspotTripSelectionRequest,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    hotspot = await session.get(TravelHotspot, hotspot_id)
    if (
        hotspot is None
        or not hotspot.is_active
        or hotspot.review_status not in {"approved", "auto_approved"}
        or hotspot.map_match_status != "verified"
        or not has_durable_coordinates(
            hotspot.latitude,
            hotspot.longitude,
            hotspot.coordinate_source_type,
            hotspot.coordinate_source_url,
        )
    ):
        raise AppError(404, "hotspot_not_found", "找不到可加入行程的景點")
    trip = await owned_trip(session, user.id, payload.trip_id)
    if (
        trip.start_date is None
        or trip.end_date is None
        or not trip.start_date <= payload.day_date <= trip.end_date
    ):
        raise AppError(422, "itinerary_date_out_of_range", "景點日期超出旅程範圍")
    rows = await load_items(session, trip.id)
    position = (
        max(
            (item.position for item in rows if item.day_date == payload.day_date),
            default=-1,
        )
        + 1
    )
    map_links = build_map_links(
        name=hotspot.name,
        local_name=hotspot.metadata_json.get("local_name"),
        city_name=hotspot.city_name,
        country_code=hotspot.country_code,
        latitude=hotspot.latitude,
        longitude=hotspot.longitude,
        google_place_id=hotspot.google_place_id,
        naver_map_url=hotspot.naver_map_url,
        map_match_status=hotspot.map_match_status,
    )
    # The stop keeps every site locale plus the original script, so the plan
    # follows the traveller's language instead of the one used when adding it.
    names = (await load_hotspot_names(session, [hotspot]))[hotspot.id]
    item = TripPlanItem(
        trip_plan_id=trip.id,
        item_type="activity",
        day_date=payload.day_date,
        position=position,
        title=hotspot.name,
        location_name=hotspot.name,
        names_json=item_names(title=names, location_name=names),
        latitude=hotspot.latitude,
        longitude=hotspot.longitude,
        coordinate_source_type=hotspot.coordinate_source_type,
        coordinate_source_url=hotspot.coordinate_source_url,
        coordinate_verified_at=hotspot.coordinate_verified_at,
        provider_place_id=hotspot.google_place_id,
        location_source=hotspot.coordinate_source_type,
        duration_minutes=int(hotspot.metadata_json.get("recommended_duration_minutes") or 90),
        data={
            "hotspot_id": str(hotspot.id),
            "hotspot_slug": hotspot.slug,
            "map_links": map_links,
            "selection_source": "hotspot_card",
        },
    )
    session.add(item)
    rows.append(item)
    return await persist_system_schedule_change(
        session,
        trip,
        user.id,
        payload.version,
        rows,
        warning="景點已加入，請重新計算這一天的路線。",
        target_day=payload.day_date,
    )


@router.get("/{hotspot_id}/place")
async def hotspot_place(
    hotspot_id: UUID,
    user: CurrentUser,
    session: Session,
) -> dict[str, Any]:
    _ = user
    hotspot = await session.get(TravelHotspot, hotspot_id)
    if (
        hotspot is None
        or not hotspot.is_active
        or hotspot.review_status not in {"approved", "auto_approved"}
    ):
        raise AppError(404, "hotspot_not_found", "找不到這個景點")
    profile = await session.scalar(
        select(HotspotPlaceProfile).where(HotspotPlaceProfile.hotspot_id == hotspot.id)
    )
    runtime = await load_runtime_settings(session)
    return place_detail_payload(
        hotspot,
        profile,
        configured=bool(runtime.google_maps_api_key and runtime.hotspot_place_enrichment_enabled),
    )


@router.post("/guides/{guide_id}/open")
async def open_hotspot_guide(
    guide_id: UUID,
    request: Request,
    user: CurrentUser,
    session: Session,
) -> dict[str, str]:
    await enforce_named_rate_limit(
        "hotspot-guide-open-user", str(user.id), limit=120, window_seconds=3_600
    )
    visitor = f"{user.id}|{request.headers.get('user-agent', '')[:200]}"
    return {"url": await resolve_guide_open(session, get_redis(), guide_id, visitor)}


@router.get("/{hotspot_id}/source")
async def hotspot_source(
    hotspot_id: UUID,
    user: CurrentUser,
    session: Session,
) -> dict[str, str]:
    _ = user
    hotspot = await session.get(TravelHotspot, hotspot_id)
    if (
        hotspot is None
        or not hotspot.is_active
        or hotspot.review_status not in {"approved", "auto_approved"}
        or not hotspot.source_urls
    ):
        raise AppError(404, "hotspot_source_not_found", "找不到這個景點來源")
    return {"url": canonical_external_url(hotspot.source_urls[0])}


@router.get("/{hotspot_id}/guides")
async def hotspot_guides(
    hotspot_id: UUID,
    user: CurrentUser,
    session: Session,
    locale: RequestLocale,
    type: Literal["all", "article", "video"] = "all",
    include_other_languages: bool = False,
    limit_per_type: Annotated[int, Query(ge=1, le=10)] = 5,
) -> dict[str, Any]:
    _ = user
    return await list_guides(
        session,
        hotspot_id,
        locale,
        type,
        include_other_languages,
        limit_per_type,
    )
