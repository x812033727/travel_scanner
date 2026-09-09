import json
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from redis.exceptions import RedisError
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser, can_deploy_user
from app.db import get_session
from app.infra import get_redis
from app.models import (
    FoodMerchant,
    FoodMerchantCategory,
    HotspotGuide,
    TravelFood,
    TravelHotspot,
    TravelServiceProduct,
    User,
)

router = APIRouter(prefix="/admin/dashboard", tags=["admin dashboard"])
Session = Annotated[AsyncSession, Depends(get_session)]


def _count_value(model: type[Any], *criteria: Any) -> Any:
    return select(func.count()).select_from(model).where(*criteria).scalar_subquery()


async def _live_dashboard_counts(session: AsyncSession) -> dict[str, int]:
    statement = select(
        _count_value(User).label("users"),
        _count_value(
            TravelHotspot,
            TravelHotspot.is_active.is_(True),
            TravelHotspot.review_status.in_(("approved", "auto_approved")),
        ).label("hotspots_public"),
        _count_value(TravelHotspot, TravelHotspot.review_status == "pending").label(
            "hotspots_pending"
        ),
        _count_value(
            TravelFood,
            TravelFood.is_active.is_(True),
            TravelFood.review_status == "approved",
        ).label("foods_public"),
        _count_value(TravelFood, TravelFood.review_status == "pending").label("foods_pending"),
        _count_value(FoodMerchant, FoodMerchant.review_status == "pending").label(
            "merchants_pending"
        ),
        _count_value(FoodMerchant, FoodMerchant.area_id.is_(None)).label(
            "merchants_missing_area"
        ),
        _count_value(
            FoodMerchant,
            FoodMerchant.id.not_in(select(FoodMerchantCategory.merchant_id)),
        ).label("merchants_missing_category"),
        _count_value(HotspotGuide, HotspotGuide.review_status == "pending").label(
            "guides_pending"
        ),
        _count_value(TravelHotspot).label("hotspots_total"),
        _count_value(TravelFood).label("foods_total"),
        _count_value(FoodMerchant).label("merchants_total"),
        _count_value(
            TravelHotspot,
            or_(TravelHotspot.latitude.is_(None), TravelHotspot.longitude.is_(None)),
        ).label("hotspots_missing_location"),
        _count_value(
            TravelServiceProduct, TravelServiceProduct.kind == "hotel"
        ).label("hotels_total"),
        _count_value(
            TravelServiceProduct,
            TravelServiceProduct.kind == "hotel",
            TravelServiceProduct.status == "pending",
        ).label("hotels_pending"),
        _count_value(
            TravelServiceProduct,
            TravelServiceProduct.kind == "hotel",
            ~TravelServiceProduct.hotel_options.any(),
        ).label("hotels_without_options"),
    )
    row = (await session.execute(statement)).mappings().one()
    return {key: int(value or 0) for key, value in row.items()}


async def _dashboard_counts(session: AsyncSession) -> dict[str, int]:
    cache_key = "admin:dashboard:counts:v2"
    redis = get_redis()
    try:
        cached = await redis.get(cache_key)
        if cached:
            parsed = json.loads(cached)
            if isinstance(parsed, dict):
                return {str(key): int(value) for key, value in parsed.items()}
    except (RedisError, TypeError, ValueError):
        pass
    counts = await _live_dashboard_counts(session)
    try:
        await redis.set(cache_key, json.dumps(counts, separators=(",", ":")), ex=15)
    except RedisError:
        pass
    return counts


@router.get("")
async def dashboard(user: AdminUser, session: Session) -> dict[str, Any]:
    return {
        "counts": await _dashboard_counts(session),
        "quick_actions": [
            {
                "id": "review_hotspots",
                "href": "/admin/hotspots?tab=review&section=manual",
                "count_key": "hotspots_pending",
            },
            {
                "id": "review_foods",
                "href": "/admin/foods?tab=review&section=dishes",
                "count_key": "foods_pending",
            },
            {
                "id": "review_merchants",
                "href": "/admin/foods?tab=review&section=merchants",
                "count_key": "merchants_pending",
            },
            {
                "id": "review_guides",
                "href": "/admin/hotspots?tab=content&section=guides",
                "count_key": "guides_pending",
            },
            {
                "id": "categorise_merchants",
                "href": "/admin/foods?tab=catalog&section=merchants&taxonomy=missing_area",
                "count_key": "merchants_missing_area",
            },
            {"id": "manage_users", "href": "/admin/users", "count_key": "users"},
            {
                "id": "review_hotels",
                "href": "/admin/hotels?tab=review&section=products",
                "count_key": "hotels_pending",
            },
        ],
        "can_deploy": can_deploy_user(user),
    }
