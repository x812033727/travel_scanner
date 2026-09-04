from typing import Any
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.auth.router import update_me, user_response
from app.auth.schemas import CURRENCIES, UserPreferencesUpdate, normalize_currency
from app.destinations.catalog import DESTINATIONS
from app.models import User


class _StubSession:
    """Stand in for the AsyncSession: record the commit, serve no identities."""

    def __init__(self) -> None:
        self.commits = 0

    async def commit(self) -> None:
        self.commits += 1


def _user(**overrides: Any) -> User:
    fields: dict[str, Any] = {
        "id": uuid4(),
        "email": "traveller@example.com",
        "password_hash": "hashed",
        "is_active": True,
        "is_admin": False,
        "auth_version": 1,
        "preferred_locale": "zh-TW",
        "preferred_currency": "TWD",
    }
    fields.update(overrides)
    return User(**fields)


@pytest.fixture(autouse=True)
def _no_identity_lookup(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _none(*_: object, **__: object) -> list[Any]:
        return []

    monkeypatch.setattr("app.auth.router.active_identities", _none)


def test_a_preference_update_must_carry_at_least_one_field() -> None:
    # An empty PATCH used to be impossible because the locale was required; now
    # that both fields are optional it has to be rejected explicitly.
    with pytest.raises(ValidationError):
        UserPreferencesUpdate()

    assert UserPreferencesUpdate(preferred_currency="JPY").preferred_locale is None
    assert UserPreferencesUpdate(preferred_locale="ja").preferred_currency is None


def test_an_unsupported_currency_is_rejected_at_the_edge() -> None:
    with pytest.raises(ValidationError):
        UserPreferencesUpdate(preferred_currency="EUR")
    with pytest.raises(ValidationError):
        UserPreferencesUpdate(preferred_currency="twd")


def test_every_destination_is_priced_in_a_currency_a_member_can_pick() -> None:
    # A destination quoted in a currency outside the list would leave its trip
    # ledger with no honest default.
    assert {profile.currency for profile in DESTINATIONS} <= set(CURRENCIES)


def test_a_currency_written_before_this_list_existed_falls_back() -> None:
    assert normalize_currency("JPY") == "JPY"
    assert normalize_currency("EUR") == "TWD"
    assert normalize_currency(None) == "TWD"


@pytest.mark.asyncio
async def test_setting_the_currency_leaves_the_locale_alone() -> None:
    user = _user(preferred_locale="ja", preferred_currency="TWD")
    session = _StubSession()

    result = await update_me(
        UserPreferencesUpdate(preferred_currency="JPY"), user, session  # type: ignore[arg-type]
    )

    assert user.preferred_currency == "JPY"
    assert user.preferred_locale == "ja"
    assert result.preferred_currency == "JPY"
    assert session.commits == 1


@pytest.mark.asyncio
async def test_setting_the_locale_leaves_the_currency_alone() -> None:
    user = _user(preferred_locale="zh-TW", preferred_currency="KRW")
    session = _StubSession()

    await update_me(
        UserPreferencesUpdate(preferred_locale="ko"), user, session  # type: ignore[arg-type]
    )

    assert user.preferred_locale == "ko"
    assert user.preferred_currency == "KRW"


@pytest.mark.asyncio
async def test_the_profile_reports_the_stored_currency() -> None:
    user = _user(preferred_currency="THB")

    response = await user_response(_StubSession(), user)  # type: ignore[arg-type]

    assert response.preferred_currency == "THB"
    # A row that predates the column defaults rather than failing the response model.
    legacy = _user(preferred_currency="EUR")
    assert (await user_response(_StubSession(), legacy)).preferred_currency == "TWD"  # type: ignore[arg-type]
