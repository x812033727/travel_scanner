from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.models import UsageAccount, UsageOperationCost, UsagePackage
from app.problems import AppError
from app.usage.schemas import OperationCostsUpdate, UsagePackageInput
from app.usage.service import (
    USAGE_OPERATIONS,
    effective_operation_cost,
    reserve_use,
    seed_usage_packages,
)


def package_payload() -> dict[str, object]:
    return {
        "localized_names": {
            "zh-TW": "測試包",
            "zh-CN": "测试包",
            "en": "Test pack",
            "ja": "テストパック",
            "ko": "테스트 팩",
        },
        "uses": 25,
        "price_twd": 399,
        "display_order": 50,
        "is_active": True,
        "is_featured": False,
    }


def test_usage_setting_schemas_enforce_locales_and_ranges() -> None:
    assert UsagePackageInput.model_validate(package_payload()).uses == 25
    assert OperationCostsUpdate(costs={"travel_search": 0}).costs == {
        "travel_search": 0
    }
    invalid = package_payload()
    invalid["localized_names"] = {"zh-TW": "只有一種"}
    with pytest.raises(ValidationError):
        UsagePackageInput.model_validate(invalid)
    with pytest.raises(ValidationError):
        OperationCostsUpdate(costs={"travel_search": 101})


@pytest.mark.asyncio
@pytest.mark.parametrize("operation", USAGE_OPERATIONS)
async def test_each_supported_operation_reads_its_configured_cost(operation: str) -> None:
    session = AsyncMock()
    session.get = AsyncMock(
        return_value=UsageOperationCost(operation=operation, uses=6)
    )

    assert await effective_operation_cost(session, operation) == 6
    session.get.assert_awaited_once_with(UsageOperationCost, operation)


@pytest.mark.asyncio
async def test_package_seed_does_not_overwrite_admin_values() -> None:
    existing = UsagePackage(
        id=uuid4(),
        code="PACK_10",
        name="管理員方案",
        localized_names={locale: "管理員方案" for locale in ("zh-TW", "zh-CN", "en", "ja", "ko")},
        uses=77,
        price_twd=888,
        display_order=7,
        is_active=False,
        is_featured=False,
        purchasable=False,
    )
    session = AsyncMock()
    session.add = MagicMock()
    session.scalar = AsyncMock(side_effect=[None, existing, None, None])

    await seed_usage_packages(session)

    assert existing.name == "管理員方案"
    assert existing.uses == 77
    assert existing.price_twd == 888
    assert existing.is_active is False
    assert session.add.call_count == 3


@pytest.mark.asyncio
@pytest.mark.parametrize("cost", [0, 4])
async def test_reservation_snapshots_configured_operation_cost(cost: int) -> None:
    user_id = uuid4()
    account = UsageAccount(
        id=uuid4(),
        user_id=user_id,
        remaining_uses=10,
        reserved_uses=0,
    )
    session = AsyncMock()
    session.add = MagicMock()
    session.scalar = AsyncMock(side_effect=[account, None])
    session.get = AsyncMock(
        return_value=UsageOperationCost(operation="travel_search", uses=cost)
    )

    reservation, created = await reserve_use(
        session,
        user_id,
        f"configured-cost-{cost}",
        "travel_search",
        "test search",
    )

    assert created is True
    assert reservation.uses == cost
    assert account.reserved_uses == cost


@pytest.mark.asyncio
async def test_reservation_requires_the_entire_configured_cost() -> None:
    user_id = uuid4()
    account = UsageAccount(
        id=uuid4(),
        user_id=user_id,
        remaining_uses=3,
        reserved_uses=0,
    )
    session = AsyncMock()
    session.add = MagicMock()
    session.scalar = AsyncMock(side_effect=[account, None])
    session.get = AsyncMock(
        return_value=UsageOperationCost(operation="travel_search", uses=4)
    )

    with pytest.raises(AppError) as captured:
        await reserve_use(
            session,
            user_id,
            "insufficient-configured-cost",
            "travel_search",
            "test search",
        )

    assert captured.value.status == 402
    assert captured.value.code == "insufficient_uses"
    assert account.reserved_uses == 0
