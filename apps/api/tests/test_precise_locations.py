from __future__ import annotations

from decimal import Decimal
from typing import Any

import fakeredis.aioredis
import pytest

from app.config import Settings
from app.foods.admin_router import _validate_publishable_merchant
from app.locations import google_match
from app.locations.coordinates import has_durable_coordinates, valid_coordinate_pair
from app.problems import AppError


def test_publishable_merchant_requires_exact_provider_identity_and_durable_source() -> None:
    result = _validate_publishable_merchant(
        country_code="HK",
        latitude=Decimal("22.246700"),
        longitude=Decimal("114.175700"),
        coordinate_source_type="official_tourism",
        coordinate_source_url="https://www.discoverhongkong.com/",
        google_place_id="ChIJ-ocean-park",
        naver_map_url=None,
    )
    assert result is None
    assert has_durable_coordinates(
        Decimal("22.246700"),
        Decimal("114.175700"),
        "official_tourism",
        "https://www.discoverhongkong.com/",
    )

    with pytest.raises(AppError) as missing_identity:
        _validate_publishable_merchant(
            country_code="HK",
            latitude=22.2467,
            longitude=114.1757,
            coordinate_source_type="official_tourism",
            coordinate_source_url="https://www.discoverhongkong.com/",
            google_place_id=None,
            naver_map_url=None,
        )
    assert missing_identity.value.code == "exact_map_identity_required"

    with pytest.raises(AppError) as search_only_naver:
        _validate_publishable_merchant(
            country_code="KR",
            latitude=37.5701,
            longitude=126.9996,
            coordinate_source_type="official_tourism",
            coordinate_source_url="https://english.visitseoul.net/",
            google_place_id=None,
            naver_map_url="https://map.naver.com/p/search/test",
        )
    assert search_only_naver.value.code == "exact_map_identity_required"


def test_coordinate_validation_rejects_missing_non_finite_and_out_of_range_values() -> None:
    assert valid_coordinate_pair(22.2467, 114.1757)
    assert not valid_coordinate_pair(None, 114.1757)
    assert not valid_coordinate_pair(float("nan"), 114.1757)
    assert not valid_coordinate_pair(91, 114.1757)
    assert not valid_coordinate_pair(22.2467, 181)


@pytest.mark.parametrize(
    ("source_type", "source_url"),
    [
        ("official_tourism", "http://www.discoverhongkong.com/"),
        ("google_places", "https://maps.google.com/"),
    ],
)
def test_publishable_merchant_rejects_non_https_or_transient_coordinate_sources(
    source_type: str,
    source_url: str,
) -> None:
    with pytest.raises(AppError) as error:
        _validate_publishable_merchant(
            country_code="HK",
            latitude=22.2467,
            longitude=114.1757,
            coordinate_source_type=source_type,
            coordinate_source_url=source_url,
            google_place_id="ChIJ-ocean-park",
            naver_map_url=None,
        )
    assert error.value.code == "coordinate_source_required"


@pytest.mark.asyncio
async def test_google_match_explicitly_reports_unavailable_without_a_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def runtime_settings(_session: object) -> Settings:
        return Settings(google_maps_api_key=None)

    monkeypatch.setattr(google_match, "load_runtime_settings", runtime_settings)
    result = await google_match.preview_google_place_match(
        object(),  # type: ignore[arg-type]
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        query="Ocean Park Hong Kong",
        country_code="HK",
    )
    assert result["configured"] is False
    assert result["candidates"] == []
    assert result["reason"] == "google_places_not_configured"


@pytest.mark.asyncio
async def test_google_match_marks_provider_coordinates_as_transient(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def runtime_settings(_session: object) -> Settings:
        return Settings(google_maps_api_key="key")

    class FakeGoogleTravelService:
        configured = True

        def __init__(self, *args: object, **kwargs: object) -> None:
            pass

        async def search_place(self, *args: object, **kwargs: object) -> dict[str, Any]:
            return {
                "id": "ChIJ-ocean-park",
                "displayName": {"text": "Ocean Park Hong Kong"},
                "formattedAddress": "Aberdeen, Hong Kong",
                "location": {"latitude": 22.2467, "longitude": 114.1757},
                "googleMapsUri": "https://maps.google.com/example",
            }

    monkeypatch.setattr(google_match, "load_runtime_settings", runtime_settings)
    monkeypatch.setattr(google_match, "GoogleTravelService", FakeGoogleTravelService)
    result = await google_match.preview_google_place_match(
        object(),  # type: ignore[arg-type]
        fakeredis.aioredis.FakeRedis(decode_responses=True),
        query="Ocean Park Hong Kong",
        country_code="HK",
    )
    candidate = result["candidates"][0]
    assert candidate["place_id"] == "ChIJ-ocean-park"
    assert candidate["suggested_status"] == "unverified"
    assert candidate["temporary_match_coordinates"]["usage"] == "comparison_only"
    assert candidate["temporary_match_coordinates"]["expires_in_days"] == 30
    assert "plus_code_global" not in candidate["temporary_match_coordinates"]
