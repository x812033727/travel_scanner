"""A settings card must not look verified when nothing has ever verified it."""

from __future__ import annotations

import pytest

from app.admin.service import (
    CONNECTION_TESTED_PROVIDERS,
    LOCAL_ONLY_PROVIDERS,
    PROVIDER_DEFINITIONS,
    card_state,
)
from app.config import Settings, get_settings


def _settings(**overrides: object) -> Settings:
    return get_settings().model_copy(update=overrides)


def test_every_provider_is_classified_as_testable_or_local() -> None:
    """A new provider has to be filed deliberately, not default into looking verified."""
    assert CONNECTION_TESTED_PROVIDERS.isdisjoint(LOCAL_ONLY_PROVIDERS)
    assert CONNECTION_TESTED_PROVIDERS | LOCAL_ONLY_PROVIDERS == set(PROVIDER_DEFINITIONS)


def test_a_key_nobody_has_tested_is_not_ready() -> None:
    settings = _settings(google_maps_api_key="a-real-looking-key")
    configured, status, message = card_state(
        "google_maps", settings, enabled=True, last_test_status=None, last_test_message=None
    )
    assert configured is True, "the key is there; the card just cannot claim it works"
    assert status == "unverified"
    assert "尚未執行連線測試" in message


def test_a_key_that_passed_its_test_is_ready() -> None:
    settings = _settings(google_maps_api_key="a-real-looking-key")
    _, status, _ = card_state(
        "google_maps", settings, enabled=True, last_test_status="success", last_test_message=None
    )
    assert status == "ready"


def test_a_failed_test_still_wins_over_unverified() -> None:
    settings = _settings(google_maps_api_key="a-real-looking-key")
    configured, status, message = card_state(
        "google_maps", settings, enabled=True, last_test_status="failed", last_test_message="401"
    )
    assert (configured, status) == (False, "error")
    assert "401" in message


def test_a_card_with_no_key_is_still_not_configured() -> None:
    settings = _settings(google_maps_api_key=None)
    configured, status, _ = card_state(
        "google_maps", settings, enabled=True, last_test_status=None, last_test_message=None
    )
    assert (configured, status) == (False, "not_configured")


def test_a_local_only_card_is_never_unverified() -> None:
    """Runtime settings have no upstream to call, so a test would prove nothing."""
    _, status, _ = card_state(
        "layout", _settings(), enabled=True, last_test_status=None, last_test_message=None
    )
    assert status != "unverified"


@pytest.mark.parametrize("provider", ["naver_maps", "ekispert", "odsay"])
def test_providers_that_must_be_tested_keep_their_own_status(provider: str) -> None:
    settings = _settings(
        naver_maps_client_id="id",
        naver_maps_client_secret="secret",
        ekispert_api_key="key",
        odsay_api_key="key",
    )
    configured, status, _ = card_state(
        provider, settings, enabled=True, last_test_status=None, last_test_message=None
    )
    assert (configured, status) == (False, "test_required")


def test_a_disabled_card_says_so_before_anything_else() -> None:
    settings = _settings(google_maps_api_key="a-real-looking-key")
    configured, status, message = card_state(
        "google_maps", settings, enabled=False, last_test_status=None, last_test_message=None
    )
    assert (configured, status) == (False, "disabled")
    assert message == "已由管理後台停用"
