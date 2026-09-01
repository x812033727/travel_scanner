from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import load_runtime_settings
from app.config import get_settings
from app.db import get_session
from app.hotspots.service import hotspot_facets, list_rankings

router = APIRouter(prefix="/hotspots", tags=["hotspots"])
Session = Annotated[AsyncSession, Depends(get_session)]


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
    q: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    city_code: Annotated[str | None, Query(min_length=3, max_length=3)] = None,
    country_code: Annotated[str | None, Query(min_length=2, max_length=2)] = None,
    category: Annotated[str | None, Query(min_length=2, max_length=32)] = None,
    after_rank: Annotated[int | None, Query(ge=0)] = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
    style: Literal["all", "deep"] = "all",
) -> dict[str, Any]:
    return await list_rankings(
        session,
        q=q,
        city_code=city_code,
        country_code=country_code,
        category=category,
        after_rank=after_rank,
        limit=limit,
        style=style,
    )


@router.get("/facets")
async def hotspots_facets(session: Session) -> dict[str, Any]:
    return await hotspot_facets(session)


@router.get("/for-planner")
async def hotspots_for_planner(
    session: Session,
    city_code: Annotated[str, Query(min_length=3, max_length=3)],
    interests: Annotated[str | None, Query(max_length=200)] = None,
    limit: Annotated[int, Query(ge=1, le=12)] = 8,
    style: Literal["all", "deep"] = "all",
    days: Annotated[int | None, Query(ge=1, le=30)] = None,
) -> dict[str, Any]:
    requested = {item.strip().casefold() for item in (interests or "").split(",") if item.strip()}
    result = await list_rankings(session, city_code=city_code, limit=50, style=style)
    items = result["items"]
    if style == "deep" and days == 1:
        items = [item for item in items if item["depth_kind"] != "day_trip"]
    if requested:
        matched = [item for item in items if item["category"] in requested]
        unmatched = [item for item in items if item["category"] not in requested]
        items = matched + unmatched
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
        }
        for item in items[:limit]
    ]
    return {
        "city_code": city_code.upper(),
        "observed_on": result["observed_on"],
        "style": style,
        "days": days,
        "recommendations": recommendations,
        "planner_note": "熱門度只作候選訊號，仍須配合營業時間、距離與旅客偏好排程",
    }
