"""The single definition of a merchant that may appear on public surfaces.

Both the dish cards and the merchant directory must agree on who is "verified":
approved, active, exact map identity, durable coordinates and at least one
current source. ``publishable_merchant_filters`` expresses that in SQL so lists
can filter and count in the database; ``merchant_is_publishable`` re-checks the
same rules on loaded rows as defence in depth.
"""

from __future__ import annotations

from sqlalchemy import and_, exists, func, or_, select
from sqlalchemy.sql import ColumnElement

from app.hotspots.maps import EXACT_NAVER_PLACE_PREFIXES, has_exact_map_identity
from app.locations.coordinates import DURABLE_COORDINATE_SOURCES, has_durable_coordinates
from app.models import FoodMerchant, FoodMerchantSource

PUBLIC_MERCHANT_STATUS = "approved"


def publishable_merchant_filters() -> list[ColumnElement[bool]]:
    naver_exact = or_(
        *[FoodMerchant.naver_map_url.like(f"{prefix}%") for prefix in EXACT_NAVER_PLACE_PREFIXES]
    )
    google_exact = and_(
        FoodMerchant.google_place_id.is_not(None),
        func.btrim(FoodMerchant.google_place_id) != "",
    )
    exact_identity = or_(
        and_(FoodMerchant.country_code == "KR", naver_exact),
        and_(FoodMerchant.country_code != "KR", google_exact),
    )
    current_source = exists(
        select(FoodMerchantSource.id).where(
            FoodMerchantSource.merchant_id == FoodMerchant.id,
            FoodMerchantSource.is_current.is_(True),
        )
    )
    return [
        FoodMerchant.review_status == PUBLIC_MERCHANT_STATUS,
        FoodMerchant.is_active.is_(True),
        FoodMerchant.map_match_status == "verified",
        FoodMerchant.latitude.is_not(None),
        FoodMerchant.longitude.is_not(None),
        FoodMerchant.latitude.between(-90, 90),
        FoodMerchant.longitude.between(-180, 180),
        FoodMerchant.coordinate_source_type.in_(sorted(DURABLE_COORDINATE_SOURCES)),
        FoodMerchant.coordinate_source_url.like("https://%"),
        exact_identity,
        current_source,
    ]


def merchant_is_publishable(merchant: FoodMerchant, *, has_current_source: bool) -> bool:
    return (
        merchant.review_status == PUBLIC_MERCHANT_STATUS
        and merchant.is_active
        and merchant.map_match_status == "verified"
        and has_current_source
        and has_exact_map_identity(
            merchant.country_code, merchant.google_place_id, merchant.naver_map_url
        )
        and has_durable_coordinates(
            merchant.latitude,
            merchant.longitude,
            merchant.coordinate_source_type,
            merchant.coordinate_source_url,
        )
    )
