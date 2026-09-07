"""The order the drafting endpoint does things in, which is the whole of its behaviour here.

A daily budget is an allowance, not a tally of attempts. Charging it for a run that cannot
start — because the vendor the administrator picked has no key — spends quota on nothing,
and twenty presses of a failing button would leave none for the run that finally works.
The guide search endpoint has always checked the vendor first; this one did not.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest

from app.config import Settings
from app.hotspots import admin_router
from app.hotspots.admin_router import IntroGenerateRequest, generate_hotspot_intros
from app.problems import AppError


class FakeSession:
    def __init__(self, hotspot_id: UUID) -> None:
        self.hotspot_id = hotspot_id
        self.added: list[object] = []
        self.commits = 0

    async def get(self, model: type, key: UUID) -> SimpleNamespace | None:
        return SimpleNamespace(id=key) if key == self.hotspot_id else None

    async def scalar(self, statement: object) -> None:
        return None

    def add(self, item: object) -> None:
        self.added.append(item)

    async def commit(self) -> None:
        self.commits += 1


@pytest.fixture
def stack(monkeypatch):
    hotspot_id = uuid4()
    charged: list[str] = []

    async def fake_budget(redis: object, key: str, limit: int) -> bool:
        charged.append(key)
        return True

    monkeypatch.setattr(admin_router, "consume_search_budget", fake_budget)
    monkeypatch.setattr(admin_router, "get_redis", lambda: object())
    return SimpleNamespace(
        hotspot_id=hotspot_id,
        charged=charged,
        session=FakeSession(hotspot_id),
        user=SimpleNamespace(id=uuid4()),
    )


def _settings(**overrides: object) -> Settings:
    base: dict[str, object] = {
        "hotspot_intro_ai_enabled": True,
        "hotspot_intro_ai_default_provider": "minimax",
        "minimax_api_key": None,
        "openai_api_key": None,
        "anthropic_api_key": None,
        "hotspot_guide_gemini_api_key": None,
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_an_unkeyed_vendor_is_refused_without_spending_the_day_s_allowance(
    monkeypatch, stack
) -> None:
    async def runtime(session: object) -> Settings:
        return _settings()

    monkeypatch.setattr(admin_router, "load_runtime_settings", runtime)

    with pytest.raises(AppError) as error:
        await generate_hotspot_intros(
            stack.hotspot_id,
            IntroGenerateRequest(locales=["zh-TW"]),
            stack.user,
            stack.session,
            str(uuid4()),
        )

    assert error.value.status == 503
    assert error.value.code == "hotspot_guide_ai_provider_not_configured"
    assert stack.charged == [], "the run budget must not be charged for a run that cannot start"
    assert stack.session.added == []
    assert stack.session.commits == 0


@pytest.mark.asyncio
async def test_an_explicit_vendor_is_checked_rather_than_the_default(monkeypatch, stack) -> None:
    """Picking Gemini for one run must be judged on Gemini's key, not on the default's."""

    async def runtime(session: object) -> Settings:
        return _settings(minimax_api_key="mm-key")

    monkeypatch.setattr(admin_router, "load_runtime_settings", runtime)

    with pytest.raises(AppError) as error:
        await generate_hotspot_intros(
            stack.hotspot_id,
            IntroGenerateRequest(locales=["zh-TW"], provider="gemini"),
            stack.user,
            stack.session,
            str(uuid4()),
        )

    assert error.value.code == "hotspot_guide_ai_provider_not_configured"
    assert stack.charged == []


@pytest.mark.asyncio
async def test_a_missing_hotspot_is_404_before_anything_is_charged(monkeypatch, stack) -> None:
    async def runtime(session: object) -> Settings:
        return _settings(minimax_api_key="mm-key")

    monkeypatch.setattr(admin_router, "load_runtime_settings", runtime)

    with pytest.raises(AppError) as error:
        await generate_hotspot_intros(
            uuid4(),
            IntroGenerateRequest(locales=["zh-TW"]),
            stack.user,
            stack.session,
            str(uuid4()),
        )

    assert error.value.status == 404
    assert stack.charged == []
