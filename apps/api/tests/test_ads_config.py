"""Article-page advertising stays off until every identifier is present and valid."""

from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.admin.service import PROVIDER_DEFINITIONS, _configured
from app.ads import router as ads_router
from app.ads.service import DISABLED, adsense_config
from app.config import Settings, get_settings
from app.problems import AppError, app_error_handler

PUBLISHER_ID = "ca-pub-4140966684432854"
SLOT_ID = "1234567890"


def settings_with(**overrides: Any) -> Settings:
    return get_settings().model_copy(update=overrides)


def active_settings(**overrides: Any) -> Settings:
    return settings_with(**{
        "adsense_enabled": True,
        "adsense_publisher_id": PUBLISHER_ID,
        "adsense_slot_id": SLOT_ID,
        **overrides,
    })


@pytest.fixture
async def ads_api(monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[tuple]:
    loaded = AsyncMock(return_value=get_settings())
    monkeypatch.setattr(ads_router, "load_runtime_settings", loaded)
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)
    app.include_router(ads_router.router, prefix="/api/v1")
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        yield client, loaded


def test_default_settings_leave_advertising_off() -> None:
    base = get_settings()
    assert base.adsense_enabled is False
    assert base.adsense_publisher_id is None and base.adsense_slot_id is None
    assert base.adsense_cmp_enabled is False
    assert adsense_config(base, tracking_allowed=True) == DISABLED


@pytest.mark.parametrize(
    "publisher_id",
    ["", "pub-4140966684432854", "ca-pub-414096668443285", "ca-pub-41409666844328540",
     "ca-pub-414096668443285x", "CA-PUB-4140966684432854", " ca-pub-4140966684432854 "],
)
def test_invalid_publisher_id_never_reaches_a_reader(publisher_id: str) -> None:
    settings = active_settings(adsense_publisher_id=publisher_id)
    config = adsense_config(settings, tracking_allowed=True)
    # A surrounding-whitespace value is the one shape that is trimmed rather than refused.
    expected = publisher_id.strip() == PUBLISHER_ID
    assert config["enabled"] is expected
    assert config["publisher_id"] == (PUBLISHER_ID if expected else None)


@pytest.mark.parametrize("slot_id", ["", "123456789", "12345678901", "12345678ab", "abcdefghij"])
def test_invalid_slot_id_never_reaches_a_reader(slot_id: str) -> None:
    settings = active_settings(adsense_slot_id=slot_id)
    assert adsense_config(settings, tracking_allowed=True) == DISABLED


@pytest.mark.parametrize(
    ("publisher_id", "slot_id"),
    [
        ("ca-pub-４１４０９６６６８４４３２８５４", SLOT_ID),
        (PUBLISHER_ID, "１２３４５６７８９０"),
        (PUBLISHER_ID, "١٢٣٤٥٦٧٨٩٠"),
    ],
)
def test_non_ascii_digits_are_refused_rather_than_lighting_the_card_green(
    publisher_id: str, slot_id: str
) -> None:
    """Python's `\\d` matches full-width and Arabic-Indic digits; JavaScript's does not. A
    zh-TW or ja IME produces full-width digits without the typist noticing, so `\\d` here would
    store an id the web side then rejects — a green card and not one reader served an ad."""
    settings = active_settings(adsense_publisher_id=publisher_id, adsense_slot_id=slot_id)
    assert adsense_config(settings, tracking_allowed=True) == DISABLED


def test_switch_off_hides_identifiers_even_when_both_are_filled_in() -> None:
    assert adsense_config(active_settings(adsense_enabled=False), tracking_allowed=True) == DISABLED


def test_valid_configuration_returns_both_identifiers() -> None:
    assert adsense_config(active_settings(), tracking_allowed=True) == {
        "enabled": True,
        "publisher_id": PUBLISHER_ID,
        "slot_id": SLOT_ID,
        # Off until the owner says a certified consent message is published: without one,
        # the page must force non-personalised ads.
        "cmp_enabled": False,
    }


def test_privacy_signal_disables_advertising_entirely() -> None:
    assert adsense_config(active_settings(), tracking_allowed=False) == DISABLED
    # A consent message is not an exception to this: a browser asking not to be tracked is
    # not asked again by a banner, it simply gets no advertising.
    with_cmp = active_settings(adsense_cmp_enabled=True)
    assert adsense_config(with_cmp, tracking_allowed=False) == DISABLED


async def test_endpoint_is_anonymous_and_never_cached(ads_api) -> None:
    client, loaded = ads_api
    loaded.return_value = active_settings()
    response = await client.get("/api/v1/ads/config")
    assert response.status_code == 200
    assert response.json() == {
        "enabled": True,
        "publisher_id": PUBLISHER_ID,
        "slot_id": SLOT_ID,
        "cmp_enabled": False,
    }
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["referrer-policy"] == "no-referrer"


@pytest.mark.parametrize("headers", [{"dnt": "1"}, {"sec-gpc": "1"}])
async def test_endpoint_reports_off_for_a_privacy_signalling_browser(ads_api, headers) -> None:
    client, loaded = ads_api
    loaded.return_value = active_settings()
    response = await client.get("/api/v1/ads/config", headers=headers)
    assert response.json() == DISABLED
    assert PUBLISHER_ID not in response.text and SLOT_ID not in response.text


async def test_endpoint_reports_off_by_default(ads_api) -> None:
    client, _ = ads_api
    assert (await client.get("/api/v1/ads/config")).json()["enabled"] is False


def test_adsense_is_its_own_provider_not_part_of_analytics() -> None:
    definition = PROVIDER_DEFINITIONS["adsense"]
    assert definition.enabled_field == "adsense_enabled"
    assert definition.config_fields == (
        "adsense_publisher_id", "adsense_slot_id", "adsense_cmp_enabled",
    )
    # Both identifiers are printed into the page for every reader, so neither is a secret.
    assert definition.secret_fields == ()
    assert PROVIDER_DEFINITIONS["analytics"].enabled_field == "analytics_enabled"


def test_card_status_matches_what_a_reader_would_actually_be_served() -> None:
    configured, state, detail = _configured("adsense", active_settings())
    assert (configured, state) == (True, "ready") and PUBLISHER_ID in detail
    configured, state, detail = _configured("adsense", settings_with())
    assert (configured, state) == (False, "not_configured") and "尚未啟用" in detail
    # Switched on but unusable is the case a NAVITIME fallback would have mislabelled.
    configured, state, detail = _configured("adsense", active_settings(adsense_slot_id=None))
    assert (configured, state) == (False, "not_configured")
    assert "slot ID" in detail and "NAVITIME" not in detail


def test_a_certified_consent_message_is_what_allows_personalised_ads() -> None:
    """The flag is the owner asserting that a Google-certified message is published in their
    AdSense account. Nothing else may turn personalisation on: the page forces
    non-personalised ads whenever it is false, because serving personalised ads in the EEA,
    the UK or Switzerland without a certified CMP is what the policy forbids."""
    assert adsense_config(active_settings(), tracking_allowed=True)["cmp_enabled"] is False
    with_cmp = adsense_config(active_settings(adsense_cmp_enabled=True), tracking_allowed=True)
    assert with_cmp["cmp_enabled"] is True
    # It cannot resurrect an otherwise unusable configuration.
    assert adsense_config(
        active_settings(adsense_enabled=False, adsense_cmp_enabled=True), tracking_allowed=True,
    ) == DISABLED


def test_card_says_which_kind_of_advertising_is_being_served() -> None:
    _, _, without = _configured("adsense", active_settings())
    _, _, with_message = _configured("adsense", active_settings(adsense_cmp_enabled=True))
    assert "只投放非個人化廣告" in without
    assert "同意訊息已啟用" in with_message
