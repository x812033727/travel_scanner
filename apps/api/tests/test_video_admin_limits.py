"""The two video limits the admin can set: Gemini narration per month and Jev calls per day."""

import pytest

from app.admin.schemas import ProviderSettingsUpdate
from app.admin.service import (
    PROVIDER_DEFINITIONS,
    _validate_provider_values,
    apply_runtime_overrides,
)
from app.ai.jev import consume_jev_call
from app.config import Settings
from app.models import ProviderConfig
from app.problems import AppError

GEMINI_LIMIT = "video_speech_gemini_monthly_character_limit"
JEV_BUDGET = "jev_daily_call_budget"


def test_each_limit_sits_on_the_card_whose_key_it_spends() -> None:
    owners = {
        field: [name for name, item in PROVIDER_DEFINITIONS.items() if field in item.config_fields]
        for field in (GEMINI_LIMIT, JEV_BUDGET)
    }
    assert owners == {GEMINI_LIMIT: ["azure_speech"], JEV_BUDGET: ["ai_vendors"]}


@pytest.mark.parametrize("value", [0, 1, 300_000, 100_000_000])
def test_the_gemini_month_accepts_zero_through_the_settings_ceiling(value: int) -> None:
    update = ProviderSettingsUpdate(config={GEMINI_LIMIT: value})
    assert _validate_provider_values("azure_speech", {}, update) == {GEMINI_LIMIT: value}


@pytest.mark.parametrize("value", [-1, 100_000_001, "many"])
def test_the_gemini_month_refuses_values_outside_the_settings_range(value: object) -> None:
    with pytest.raises(AppError) as error:
        _validate_provider_values(
            "azure_speech", {}, ProviderSettingsUpdate(config={GEMINI_LIMIT: value})
        )
    assert error.value.status == 422
    assert error.value.code == "provider_setting_invalid"


@pytest.mark.parametrize("value", [1, 200, 5_000])
def test_the_jev_day_accepts_one_through_five_thousand(value: int) -> None:
    update = ProviderSettingsUpdate(config={JEV_BUDGET: value})
    assert _validate_provider_values("ai_vendors", {}, update) == {JEV_BUDGET: value}


@pytest.mark.parametrize("value", [0, -1, 5_001])
def test_the_jev_day_refuses_zero_and_values_past_the_ceiling(value: int) -> None:
    # Zero is refused rather than read as "unlimited": every Jev caller treats a spent
    # budget as a reason to stop, so a zero here would silently switch Jev off.
    with pytest.raises(AppError) as error:
        _validate_provider_values(
            "ai_vendors", {}, ProviderSettingsUpdate(config={JEV_BUDGET: value})
        )
    assert error.value.code == "provider_setting_invalid"


def test_saved_limits_override_the_environment_even_on_a_disabled_speech_card() -> None:
    base = Settings()
    assert (base.video_speech_gemini_monthly_character_limit, base.jev_daily_call_budget) == (
        300_000,
        200,
    )
    rows = [
        ProviderConfig(provider="azure_speech", enabled=False, config={GEMINI_LIMIT: 120_000}),
        ProviderConfig(provider="ai_vendors", enabled=True, config={JEV_BUDGET: 40}),
    ]
    effective = apply_runtime_overrides(base, rows)
    assert effective.video_speech_gemini_monthly_character_limit == 120_000
    assert effective.jev_daily_call_budget == 40


class CountingRedis:
    """Runs the budget script's arithmetic in Python; fakeredis ships without Lua."""

    def __init__(self) -> None:
        self.counts: dict[str, int] = {}
        self.budgets: list[str] = []

    async def eval(self, _script: str, _keys: int, key: str, budget: str) -> int:
        self.budgets.append(budget)
        if self.counts.get(key, 0) >= int(budget):
            return -1
        self.counts[key] = self.counts.get(key, 0) + 1
        return self.counts[key]


@pytest.mark.asyncio
async def test_the_saved_jev_day_is_the_one_the_calls_are_counted_against() -> None:
    redis = CountingRedis()
    rows = [ProviderConfig(provider="ai_vendors", enabled=True, config={JEV_BUDGET: 2})]
    effective = apply_runtime_overrides(Settings(), rows)
    spent = [await consume_jev_call(redis, effective) for _ in range(3)]  # type: ignore[arg-type]
    assert spent == [True, True, False]
    assert redis.budgets == ["2", "2", "2"]
