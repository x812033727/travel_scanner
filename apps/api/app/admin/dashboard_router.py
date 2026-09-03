from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AdminUser, can_deploy_user
from app.db import get_session
from app.foods.publication import publishable_merchant_filters
from app.models import (
    FoodMerchant,
    FoodMerchantCategory,
    HotspotGuide,
    TravelFood,
    TravelHotspot,
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
            "merchants_pending": await _count(
                session, FoodMerchant, FoodMerchant.review_status == "pending"
            ),
            "merchants_missing_area": await _count(
                session,
                FoodMerchant,
                *publishable_merchant_filters(),
                FoodMerchant.area_id.is_(None),
            ),
            "merchants_missing_category": await _count(
                session,
                FoodMerchant,
                *publishable_merchant_filters(),
                FoodMerchant.id.not_in(select(FoodMerchantCategory.merchant_id)),
            ),
            "guides_pending": await _count(
                session, HotspotGuide, HotspotGuide.review_status == "pending"
            ),
        },
        "quick_actions": [
            {"id": "review_hotspots", "href": "/admin/hotspots", "count_key": "hotspots_pending"},
            {"id": "review_merchants", "href": "/admin/foods", "count_key": "merchants_pending"},
            {
                "id": "categorise_merchants",
                "href": "/admin/foods?taxonomy=missing_area",
                "count_key": "merchants_missing_area",
            },
            {"id": "manage_users", "href": "/admin/users", "count_key": "users"},
        ],
        "can_deploy": can_deploy_user(user),
    }
