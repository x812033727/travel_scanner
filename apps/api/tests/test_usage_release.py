from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.models import UsageAccount, UsageReservation
from app.usage.service import release_reservation


def fixture(status: str = "reserved") -> tuple[UsageAccount, UsageReservation]:
    user_id, account_id = uuid4(), uuid4()
    account = UsageAccount(id=account_id, user_id=user_id, remaining_uses=5, reserved_uses=2)
    reservation = UsageReservation(
        id=uuid4(),
        user_id=user_id,
        account_id=account_id,
        idempotency_key=f"key-{uuid4()}",
        operation="travel_search",
        summary="TPE → NRT",
        uses=2,
        status=status,
        resource_id=uuid4(),
    )
    return account, reservation


def session_for(account: UsageAccount, reservation: UsageReservation) -> AsyncMock:
    """A session that answers the two reads `release_reservation` makes, in order."""
    session = AsyncMock()
    session.scalar = AsyncMock(side_effect=[reservation, account])
    session.add = lambda *args, **kwargs: None
    session.execute = AsyncMock(return_value=SimpleNamespace(scalar_one_or_none=lambda: None))
    return session


@pytest.mark.asyncio
async def test_a_reserved_hold_goes_back_to_the_account() -> None:
    account, reservation = fixture()
    await release_reservation(session_for(account, reservation), reservation, "cancelled")
    assert reservation.status == "released"
    assert account.reserved_uses == 0
    # A release is not a refund: the uses were never spent, so the balance is untouched.
    assert account.remaining_uses == 5


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["committed", "released"])
async def test_a_hold_that_is_already_settled_is_left_exactly_as_it_is(status: str) -> None:
    """Cancelling twice, or cancelling the instant the worker charges, must not double-release.

    This is what makes `POST /searches/{id}/cancel` safe to call from a cancel button, a
    timeout and a retry of either without the three of them having to coordinate.
    """
    account, reservation = fixture(status)
    before = (account.reserved_uses, account.remaining_uses)
    await release_reservation(session_for(account, reservation), reservation, "cancelled")
    assert reservation.status == status
    assert (account.reserved_uses, account.remaining_uses) == before
