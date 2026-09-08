from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser, can_deploy_user
from app.db import get_session
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


async def _count(session: AsyncSession, model: type[Any], *criteria: Any) -> int:
    value = await session.scalar(select(func.count()).select_from(model).where(*criteria))
    return int(value or 0)


@router.get("")
async def dashboard(user: AdminUser, session: Session) -> dict[str, Any]:
    return {
        "counts": {
            "users": await _count(session, User),
            "hotspots_public": await _count(
                session,
                TravelHotspot,
                TravelHotspot.is_active.is_(True),
                TravelHotspot.review_status.in_(("approved", "auto_approved")),
            ),
            "hotspots_pending": await _count(
                session, TravelHotspot, TravelHotspot.review_status == "pending"
            ),
            "foods_public": await _count(
                session,
                TravelFood,
                TravelFood.is_active.is_(True),
                TravelFood.review_status == "approved",
            ),
            "foods_pending": await _count(
                session, TravelFood, TravelFood.review_status == "pending"
            ),
            "merchants_pending": await _count(
                session, FoodMerchant, FoodMerchant.review_status == "pending"
            ),
            # Count every merchant the quick-action list shows, not only publishable
            # ones, so the badge never reads 0 while the linked list has rows.
            "merchants_missing_area": await _count(
                session,
                FoodMerchant,
                FoodMerchant.area_id.is_(None),
            ),
            "merchants_missing_category": await _count(
                session,
                FoodMerchant,
                FoodMerchant.id.not_in(select(FoodMerchantCategory.merchant_id)),
            ),
            "guides_pending": await _count(
                session, HotspotGuide, HotspotGuide.review_status == "pending"
            ),
            "hotspots_total": await _count(session, TravelHotspot),
            "foods_total": await _count(session, TravelFood),
            "merchants_total": await _count(session, FoodMerchant),
            "hotspots_missing_location": await _count(
                session, TravelHotspot,
                or_(TravelHotspot.latitude.is_(None), TravelHotspot.longitude.is_(None))
            ),
            "hotels_total": await _count(
                session, TravelServiceProduct, TravelServiceProduct.kind == "hotel"
            ),
            "hotels_pending": await _count(
                session, TravelServiceProduct,
                TravelServiceProduct.kind == "hotel", TravelServiceProduct.status == "pending"
            ),
            "hotels_without_options": await _count(
                session, TravelServiceProduct,
                TravelServiceProduct.kind == "hotel", ~TravelServiceProduct.hotel_options.any()
            ),
        },
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
