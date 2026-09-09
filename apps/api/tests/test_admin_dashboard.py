from unittest.mock import AsyncMock

import pytest

from app.admin import dashboard_router


@pytest.mark.asyncio
async def test_dashboard_counts_every_pending_catalog_type(monkeypatch: pytest.MonkeyPatch) -> None:
    count = AsyncMock(
        side_effect=[1, 984, 124, 87, 13, 245, 133, 0, 427, 1200, 150, 600, 41, 32, 5, 2]
    )
    monkeypatch.setattr(dashboard_router, "_count", count)
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
    # Every hotel metric must carry a hotel-only SQL predicate, not a mixed-service count.
    for call in count.call_args_list[-3:]:
        assert str(call.args[2].compile(compile_kwargs={"literal_binds": True})) == (
            "travel_service_products.kind = 'hotel'"
        )
