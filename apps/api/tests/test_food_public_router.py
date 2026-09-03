from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import pytest
from sqlalchemy import select
from sqlalchemy.dialects import postgresql

from app.foods.publication import merchant_is_publishable, publishable_merchant_filters
from app.foods.router import food_categories, food_merchants
from app.foods.schemas import MerchantCard, MerchantListResponse
from app.foods.service import (
    _decode_cursor,
    _encode_cursor,
    destination_country_code,
    localized_name,
)
from app.models import FoodMerchant
from app.problems import AppError


def _verified_merchant(**overrides: Any) -> FoodMerchant:
    values: dict[str, Any] = {
        "slug": "seoul-test",
        "destination_id": "seoul",
        "country_code": "KR",
        "name": "Test",
        "local_name": "테스트",
        "latitude": Decimal("37.5"),
        "longitude": Decimal("127.0"),
        "coordinate_source_type": "official_tourism",
        "coordinate_source_url": "https://english.visitseoul.net/restaurants",
        "naver_map_url": "https://map.naver.com/p/entry/place/13543735",
        "map_match_status": "verified",
        "review_status": "approved",
        "is_active": True,
        "verified_at": datetime.now(UTC),
    }
    values.update(overrides)
    return FoodMerchant(**values)


def test_publishable_filters_compile_to_the_shared_publication_rules() -> None:
    statement = select(FoodMerchant).where(*publishable_merchant_filters())
    sql = str(
        statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
    )
    assert "review_status = 'approved'" in sql
    assert "map_match_status = 'verified'" in sql
    assert "https://map.naver.com/p/entry/place/" in sql
    assert "https://map.naver.com/v5/entry/place/" in sql
    assert "btrim(food_merchants.google_place_id)" in sql
    assert "'official_tourism'" in sql and "'admin_verified'" in sql
    assert "EXISTS (SELECT food_merchant_sources.id" in sql
    assert "is_current IS true" in sql


def test_merchant_is_publishable_mirrors_the_sql_rules() -> None:
    assert merchant_is_publishable(_verified_merchant(), has_current_source=True)
    assert not merchant_is_publishable(_verified_merchant(), has_current_source=False)
    assert not merchant_is_publishable(
        _verified_merchant(naver_map_url="https://map.naver.com/p/search/test"),
        has_current_source=True,
    )
    assert not merchant_is_publishable(
        _verified_merchant(coordinate_source_type="manual"), has_current_source=True
    )
    assert merchant_is_publishable(
        _verified_merchant(country_code="JP", naver_map_url=None, google_place_id="ChIJ123"),
        has_current_source=True,
    )
    assert not merchant_is_publishable(
        _verified_merchant(country_code="JP", naver_map_url=None, google_place_id=" "),
        has_current_source=True,
    )


def test_localized_name_falls_back_in_order() -> None:
    names = {"zh-TW": "新宿", "en": "Shinjuku", "ja": "新宿", "ko": "신주쿠", "zh-CN": "新宿"}
    assert localized_name(names, "ko") == "신주쿠"
    assert localized_name({"zh-TW": "新宿", "en": "Shinjuku"}, "ja") == "Shinjuku"
    assert localized_name({"zh-TW": "新宿"}, "ja") == "新宿"
    assert localized_name({"ko": "신주쿠"}, "ja") == "신주쿠"
    assert localized_name({}, "ja") == ""


def test_cursor_round_trip_and_rejection() -> None:
    assert _decode_cursor(None) == 0
    assert _decode_cursor(_encode_cursor(40)) == 40
    with pytest.raises(AppError) as excinfo:
        _decode_cursor("not-a-cursor!")
    assert excinfo.value.code == "invalid_food_cursor"


def test_destination_country_code_uses_the_catalog() -> None:
    assert destination_country_code("seoul") == "KR"
    assert destination_country_code("tainan") == "TW"
    assert destination_country_code("atlantis") is None


@pytest.mark.asyncio
async def test_public_merchant_routes_reject_unknown_destinations() -> None:
    with pytest.raises(AppError) as excinfo:
        await food_merchants(object(), "zh-TW", destination_id="atlantis")  # type: ignore[arg-type]
    assert excinfo.value.code == "unsupported_destination"
    with pytest.raises(AppError):
        await food_categories(object(), "zh-TW", destination_id="atlantis")  # type: ignore[arg-type]


def test_merchant_list_response_accepts_the_service_shape() -> None:
    card = MerchantCard.model_validate(
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "slug": "seoul-test",
            "name": "Test",
            "local_name": "테스트",
            "destination_id": "seoul",
            "destination_name": "首爾",
            "country_code": "KR",
            "area": {"id": "a", "slug": "seoul-myeongdong", "name": "明洞", "local_name": "명동"},
            "categories": [{"slug": "home-style", "name": "定食／家常菜", "is_primary": True}],
            "signature_dishes": [],
            "address": None,
            "latitude": 37.5,
            "longitude": 127.0,
            "coordinate_source": {
                "type": "official_tourism",
                "url": "https://x",
                "verified_at": None,
            },
            "official_website_url": None,
            "map_links": [
                {
                    "provider": "naver",
                    "label": "Naver Map",
                    "url": "https://map.naver.com/p/entry/place/1",
                    "primary": True,
                }
            ],
            "verified_at": None,
            "sources": [],
        }
    )
    response = MerchantListResponse(
        total=1,
        has_more=False,
        next_cursor=None,
        items=[card],
        facets={"areas": [], "unassigned_area_count": 0, "categories": []},
    )
    assert response.items[0].area is not None
    assert response.items[0].area.slug == "seoul-myeongdong"
    assert response.facets.unassigned_area_count == 0
