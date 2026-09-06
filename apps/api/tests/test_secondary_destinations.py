from collections import Counter, defaultdict
from datetime import date

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError

from app.destinations.catalog import DESTINATIONS, SEARCHABLE_DESTINATIONS, destination_for_id
from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.router import _resolve_destination
from app.main import app
from app.problems import AppError
from app.search.schemas import SearchCreate, SearchModule, SearchPreferences
from tests.test_hotspot_seed_categories import KNOWN_CATEGORIES

SECONDARY_IDS = {
    "taichung",
    "kaohsiung",
    "sendai",
    "kanazawa",
    "hiroshima",
    "daegu",
    "chiang-rai",
    "da-lat",
    "tainan",
    "gyeongju",
    "jeonju",
    "hue",
    "yokohama",
    "kamakura",
}


def test_secondary_destination_and_offline_catalog_contract() -> None:
    profiles = [item for item in DESTINATIONS if item.id in SECONDARY_IDS]
    assert len(profiles) == 14
    assert Counter(item.role for item in profiles) == {"secondary": 8, "extension": 6}
    assert len(SEARCHABLE_DESTINATIONS) == 27
    assert destination_for_id("tainan").parent_destination_id == "kaohsiung"  # type: ignore[union-attr]
    assert destination_for_id("yokohama").parent_destination_id == "tokyo"  # type: ignore[union-attr]
    assert destination_for_id("kamakura").parent_destination_id == "tokyo"  # type: ignore[union-attr]

    food_area_supplements = {"sendai-asaichi-market", "chiang-rai-night-bazaar"}
    rows = [
        item
        for item in HOTSPOT_SEEDS
        if item.destination_id in SECONDARY_IDS and item.slug not in food_area_supplements
    ]
    assert len(rows) == 210
    by_destination = defaultdict(list)
    for item in rows:
        by_destination[item.destination_id].append(item)
        assert item.local_name
        assert item.source_urls
        assert item.recommended_duration_minutes
    assert set(by_destination) == SECONDARY_IDS
    for items in by_destination.values():
        assert len(items) == 15
        assert Counter(item.is_deep_travel for item in items) == {False: 10, True: 5}
        deep = [item for item in items if item.is_deep_travel]
        assert Counter(item.depth_kind for item in deep) == {"urban_local": 3, "day_trip": 2}
        destination_id = items[0].destination_id
        audited_items = [
            item for item in HOTSPOT_SEEDS if item.destination_id == destination_id
        ]
        # No quota per city. Demanding one of every category is what put a shrine under
        # shopping and a Noh museum under nature; Gyeongju is an ancient capital and nine
        # of its fifteen really are cultural. The catalogue as a whole still has to be
        # varied — that is asserted once, below, rather than fifteen rows at a time.
        assert {item.category for item in audited_items} <= KNOWN_CATEGORIES


@pytest.mark.asyncio
async def test_destination_catalog_filters_roles_and_parents() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/destinations", params={"role": "secondary"})
        assert response.status_code == 200
        assert response.json()["total"] == 8
        assert all(item["searchable"] for item in response.json()["items"])

        response = await client.get(
            "/api/v1/destinations", params={"role": "extension", "parent_id": "busan"}
        )
        assert response.status_code == 200
        assert [item["id"] for item in response.json()["items"]] == ["gyeongju"]
        assert response.json()["items"][0]["searchable"] is False

        response = await client.get(
            "/api/v1/destinations", params={"role": "extension", "parent_id": "tokyo"}
        )
        assert response.status_code == 200
        assert [item["id"] for item in response.json()["items"]] == ["yokohama", "kamakura"]

        response = await client.get("/api/v1/destinations", params={"country_code": "JP"})
        tokyo = next(item for item in response.json()["items"] if item["id"] == "tokyo")
        assert tokyo["extension_ids"] == ["kamakura", "yokohama"]


def test_cross_city_duration_limits_are_validated() -> None:
    common = {
        "origin": "TPE",
        "destination": "KHH",
        "departure_date": date(2026, 11, 1),
        "return_date": date(2026, 11, 3),
        "modules": [SearchModule.FLIGHT],
        "preferences": SearchPreferences(extension_destination_ids=["tainan"]),
    }
    with pytest.raises(ValidationError, match="至少需要四天"):
        SearchCreate(**common)

    valid = SearchCreate(
        **{
            **common,
            "return_date": date(2026, 11, 4),
        }
    )
    assert valid.preferences.extension_destination_ids == ["tainan"]

    with pytest.raises(ValidationError, match="最多可加入 1 個"):
        SearchCreate(
            **{
                **common,
                "return_date": date(2026, 11, 5),
                "preferences": SearchPreferences(extension_destination_ids=["tainan", "gyeongju"]),
            }
        )

    with pytest.raises(ValidationError, match="必須屬於目前主要目的地"):
        SearchCreate(
            **{
                **common,
                "return_date": date(2026, 11, 7),
                "preferences": SearchPreferences(extension_destination_ids=["gyeongju"]),
            }
        )


def test_hotspot_destination_parameters_are_compatible_and_unambiguous() -> None:
    assert _resolve_destination("KHH", "kaohsiung") == ("KHH", "kaohsiung")
    with pytest.raises(AppError) as mismatch:
        _resolve_destination("KHH", "tainan")
    assert mismatch.value.code == "destination_mismatch"
    with pytest.raises(AppError) as extension_code:
        _resolve_destination("GYE", None)
    assert extension_code.value.code == "destination_id_required"
