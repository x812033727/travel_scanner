from unittest.mock import AsyncMock

import pytest

from app.admin import dashboard_router


@pytest.mark.asyncio
async def test_dashboard_counts_every_pending_catalog_type(monkeypatch: pytest.MonkeyPatch) -> None:
    counts = {
        "users": 1,
        "hotspots_public": 984,
        "hotspots_pending": 124,
        "foods_public": 87,
        "foods_pending": 13,
        "merchants_pending": 245,
        "merchants_missing_area": 133,
        "merchants_missing_category": 0,
        "guides_pending": 427,
        "hotspots_total": 1200,
        "foods_total": 150,
        "merchants_total": 600,
        "hotspots_missing_location": 41,
        "hotels_total": 32,
        "hotels_pending": 5,
        "hotels_without_options": 2,
    }
    dashboard_counts = AsyncMock(
        return_value=counts
    )
    monkeypatch.setattr(dashboard_router, "_dashboard_counts", dashboard_counts)
    monkeypatch.setattr(dashboard_router, "can_deploy_user", lambda _user: False)

    result = await dashboard_router.dashboard(object(), object())  # type: ignore[arg-type]

    assert result["counts"]["foods_pending"] == 13
    assert {
        (item["id"], item["href"], item["count_key"])
        for item in result["quick_actions"]
    } >= {
        ("review_foods", "/admin/foods?tab=review&section=dishes", "foods_pending"),
        ("review_guides", "/admin/hotspots?tab=content&section=guides", "guides_pending"),
        ("review_hotels", "/admin/hotels?tab=review&section=products", "hotels_pending"),
    }
    assert result["counts"]["hotels_total"] == 32
    assert result["counts"]["hotels_pending"] == 5
    dashboard_counts.assert_awaited_once()
