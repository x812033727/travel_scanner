from unittest.mock import AsyncMock

import pytest

from app.admin import dashboard_router


@pytest.mark.asyncio
async def test_dashboard_counts_every_pending_catalog_type(monkeypatch: pytest.MonkeyPatch) -> None:
    count = AsyncMock(side_effect=[1, 984, 124, 87, 13, 245, 133, 0, 427])
    monkeypatch.setattr(dashboard_router, "_count", count)
    monkeypatch.setattr(dashboard_router, "can_deploy_user", lambda _user: False)

    result = await dashboard_router.dashboard(object(), object())  # type: ignore[arg-type]

    assert result["counts"]["foods_pending"] == 13
    assert {
        (item["id"], item["href"], item["count_key"])
        for item in result["quick_actions"]
    } >= {
        ("review_foods", "/admin/foods#dishes", "foods_pending"),
        ("review_guides", "/admin/hotspots#guides", "guides_pending"),
    }
