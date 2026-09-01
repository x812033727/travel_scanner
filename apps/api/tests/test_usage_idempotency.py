from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from app.models import UsageAccount, UsageReservation
from app.problems import AppError
from app.usage.service import reserve_use


def reservation_fixture(
    *, resource_id: UUID | None = None
) -> tuple[UsageAccount, UsageReservation]:
    user_id = uuid4()
    account_id = uuid4()
    account = UsageAccount(
        id=account_id,
        user_id=user_id,
        remaining_uses=3,
        reserved_uses=0,
    )
    reservation = UsageReservation(
        id=uuid4(),
        user_id=user_id,
        account_id=account_id,
        idempotency_key="same-request-key",
        operation="public_airline_fare_search",
        summary="fare search",
        uses=4,
        status="committed",
        resource_id=resource_id,
    )
    return account, reservation


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["reserved", "committed", "released"])
async def test_reserve_use_rejects_keys_without_a_replayable_resource(status: str) -> None:
    account, reservation = reservation_fixture()
    reservation.status = status
    session = AsyncMock()
    session.scalar = AsyncMock(side_effect=[account, reservation])

    with pytest.raises(AppError) as captured:
        await reserve_use(
            session,
            account.user_id,
            reservation.idempotency_key,
            reservation.operation,
            reservation.summary,
        )

    assert captured.value.status == 409
    assert captured.value.code == "idempotency_result_unavailable"


@pytest.mark.asyncio
async def test_reserve_use_allows_replay_when_the_result_resource_exists() -> None:
    resource_id = uuid4()
    account, reservation = reservation_fixture(resource_id=resource_id)
    session = AsyncMock()
    session.scalar = AsyncMock(side_effect=[account, reservation])

    existing, created = await reserve_use(
        session,
        account.user_id,
        reservation.idempotency_key,
        reservation.operation,
        reservation.summary,
    )

    assert existing is reservation
    assert existing.resource_id == resource_id
    assert existing.uses == 4
    assert created is False
    session.get.assert_not_awaited()
