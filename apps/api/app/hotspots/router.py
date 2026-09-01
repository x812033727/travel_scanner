from typing import Annotated, Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.config import get_settings
from app.db import get_session
from app.destinations.catalog import DESTINATIONS, destination_for_code, destination_for_id
from app.hotspots.guides import list_guides, resolve_guide_open
from app.hotspots.service import hotspot_facets, list_rankings
from app.i18n import Locale, current_locale
from app.infra import client_ip, enforce_named_rate_limit, get_redis
from app.problems import AppError

router = APIRouter(prefix="/hotspots", tags=["hotspots"])
Session = Annotated[AsyncSession, Depends(get_session)]
RequestLocale = Annotated[Locale, Depends(current_locale)]


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


@router.get("/sources")
async def hotspot_sources(session: Session) -> dict[str, Any]:
    runtime = await load_runtime_settings(session)
    settings = get_settings()
    return {
        "collection_interval_seconds": settings.hotspot_collection_interval_seconds,
        "sources": [
            {
                "id": "curated_catalog",
                "name": "Travel Scanner 精選主檔",
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
                "status": "on_demand" if runtime.google_maps_api_key else "not_configured",
                "purpose": "使用者查詢時補地點識別與即時顯示，不作長期排行資料庫",
                "persistence": "僅 Place ID 可長期保存",
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
    after_rank: Annotated[int | None, Query(ge=0)] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    style: Literal["all", "deep"] = "all",
) -> dict[str, Any]:
    resolved_city_code, resolved_destination_id = _resolve_destination(city_code, destination_id)
    return await list_rankings(
        session,
        q=q,
        city_code=resolved_city_code if destination_id is None else None,
        destination_id=resolved_destination_id if destination_id is not None else None,
        country_code=country_code,
        category=category,
        role=role,
        after_rank=after_rank,
        limit=limit,
        style=style,
        locale=locale,
    )


@router.get("/facets")
async def hotspots_facets(session: Session) -> dict[str, Any]:
    return await hotspot_facets(session)


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
    requested = {item.strip().casefold() for item in (interests or "").split(",") if item.strip()}
    result = await list_rankings(
        session,
        city_code=resolved_city_code if destination_id is None else None,
        destination_id=resolved_destination_id if destination_id is not None else None,
        limit=50,
        style=style,
        locale=locale,
    )
    items = result["items"]
    if style == "deep" and days == 1:
        items = [item for item in items if item["depth_kind"] != "day_trip"]
    if requested:
        matched = [item for item in items if item["category"] in requested]
        unmatched = [item for item in items if item["category"] not in requested]
        items = matched + unmatched
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
                session, destination_id=child.id, limit=4, style=style, locale=locale
            )
            if child_result["items"]:
                extension_items.append(child_result["items"][0])
                chosen_extensions.append(child.id)
    if extension_items:
        # Cross-city choices must survive the endpoint limit instead of being
        # hidden behind a full page of primary-destination candidates.
        items = items[: max(0, limit - len(extension_items))] + extension_items
    recommendations = [
        {
            "hotspot_id": item["id"],
            "name": item["name"],
            "category": item["category"],
            "latitude": item["latitude"],
            "longitude": item["longitude"],
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


@router.post("/guides/{guide_id}/open")
async def open_hotspot_guide(
    guide_id: UUID,
    request: Request,
    session: Session,
) -> dict[str, str]:
    address = client_ip(request)
    await enforce_named_rate_limit("hotspot-guide-open", address, limit=120, window_seconds=3_600)
    visitor = f"{address}|{request.headers.get('user-agent', '')[:200]}"
    return {"url": await resolve_guide_open(session, get_redis(), guide_id, visitor)}


@router.get("/{hotspot_id}/guides")
async def hotspot_guides(
    hotspot_id: UUID,
    session: Session,
    locale: RequestLocale,
    type: Literal["all", "article", "video"] = "all",
    include_other_languages: bool = False,
    limit_per_type: Annotated[int, Query(ge=1, le=10)] = 5,
) -> dict[str, Any]:
    return await list_guides(
        session,
        hotspot_id,
        locale,
        type,
        include_other_languages,
        limit_per_type,
    )
