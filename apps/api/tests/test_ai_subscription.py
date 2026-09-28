"""Claude on the host's subscription accounts: which calls go there, and what if none can."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel

from app.admin_ai_accounts.agent import AgentRunResult
from app.admin_ai_accounts.schemas import AgentOverview
from app.ai import subscription
from app.ai.subscription import (
    SubscriptionResearchProvider,
    run_seconds,
    subscription_summary,
    vendor_ready,
)
from app.config import Settings
from app.hotspots.ai_search import configured_research_providers, research_provider
from app.problems import AppError

HMAC = "h" * 40


def _settings(**changes: Any) -> Settings:
    values: dict[str, Any] = {
        "anthropic_connection": "subscription",
        "anthropic_api_key": None,
        "openai_api_key": None,
        "minimax_api_key": "mm-key",
        "hotspot_guide_gemini_api_key": None,
        "ai_accounts_enabled": True,
        "ai_accounts_agent_hmac_key": HMAC,
    }
    values.update(changes)
    return Settings(**values)


class Answer(BaseModel):
    title: str


class FakeAgent:
    """Answers each run_prompt call from a script: text for a reply, AppError to refuse."""

    def __init__(self, *replies: str | AppError) -> None:
        self.replies = list(replies)
        self.calls: list[dict[str, Any]] = []

    async def run_prompt(self, **kwargs: Any) -> AgentRunResult:
        self.calls.append(kwargs)
        reply = self.replies.pop(0)
        if isinstance(reply, AppError):
            raise reply
        return AgentRunResult(
            text=reply,
            slot="b",
            model=kwargs["model"],
            input_tokens=100,
            output_tokens=20,
            duration_ms=900,
        )


def _provider(agent: FakeAgent, model: str = "claude-opus-5-5") -> Any:
    return SubscriptionResearchProvider(
        _settings(),
        model,
        240,
        agent=agent,  # type: ignore[arg-type]
    )


def test_claude_is_ready_on_the_agent_alone_and_the_others_still_need_their_keys() -> None:
    settings = _settings()
    assert vendor_ready(settings, "anthropic") is True
    assert configured_research_providers(settings) == {
        "minimax": True,
        "openai": False,
        "anthropic": True,
        "gemini": False,
    }
    assert vendor_ready(_settings(ai_accounts_enabled=False), "anthropic") is False
    keyed = _settings(anthropic_connection="api_key", anthropic_api_key="sk-ant")
    assert vendor_ready(keyed, "anthropic") is True
    assert vendor_ready(_settings(anthropic_connection="api_key"), "anthropic") is False


def test_research_provider_hands_claude_to_the_subscription_with_its_feature_model() -> None:
    provider = research_provider(_settings(), "anthropic", model="claude-opus-5-5")
    assert isinstance(provider, SubscriptionResearchProvider)
    assert (provider.name, provider.model) == ("anthropic", "claude-opus-5-5")
    keyed = research_provider(
        _settings(anthropic_connection="api_key", anthropic_api_key="sk-ant"), "anthropic"
    )
    assert not isinstance(keyed, SubscriptionResearchProvider)
    with pytest.raises(AppError) as missing:
        research_provider(_settings(ai_accounts_enabled=False), "anthropic")
    assert missing.value.code == "hotspot_guide_ai_provider_not_configured"


@pytest.mark.asyncio
async def test_openai_can_use_codex_subscription_without_an_api_key() -> None:
    settings = _settings(openai_connection="subscription")
    assert vendor_ready(settings, "openai")
    provider = research_provider(settings, "openai", model="gpt-6-sol")
    assert isinstance(provider, SubscriptionResearchProvider)
    assert (provider.name, provider.model) == ("openai", "gpt-6-sol")
    agent = FakeAgent('{"title": "Codex answer"}')
    provider._agent = agent  # type: ignore[assignment]
    answer, usage = await provider.structured(Answer, "answer", "Write.", {})
    assert answer.title == "Codex answer" and usage["input_tokens"] == 100
    assert agent.calls[0]["tool"] == "codex"
    assert provider.served_by == "codex:b"
    assert not vendor_ready(_settings(openai_connection="api_key"), "openai")


@pytest.mark.asyncio
async def test_a_subscription_answer_is_parsed_like_an_api_answer() -> None:
    agent = FakeAgent('```json\n{"title": "Hello"}\n```')
    provider = _provider(agent)
    answer, usage = await provider.structured(Answer, "answer", "Write a title.", {"q": "頁面"})
    assert answer.title == "Hello" and usage == {"input_tokens": 100, "output_tokens": 20}
    assert provider.served_by == "claude:b"
    call = agent.calls[0]
    assert call["model"] == "claude-opus-5-5" and call["prompt"] == '{"q": "頁面"}'
    assert "Write a title." in call["system"] and '"title"' in call["system"], "schema is inlined"
    # No cap since 2026-09-26: an account takes runs until its window is full.
    assert call["max_usage_percent"] == 100
    assert call["timeout_seconds"] == 300 and call["queue_seconds"] == subscription.QUEUE_SECONDS


@pytest.mark.asyncio
async def test_an_answer_off_the_schema_gets_one_repair_round() -> None:
    agent = FakeAgent('{"name": "wrong"}', '{"title": "Fixed"}')
    answer, usage = await _provider(agent).structured(Answer, "answer", "Write.", {})
    assert answer.title == "Fixed" and usage["input_tokens"] == 200
    assert len(agent.calls) == 2 and agent.calls[1]["prompt"] != agent.calls[0]["prompt"]


@pytest.mark.parametrize(
    "code",
    [
        "subscription_quota_paused",
        "subscription_not_signed_in",
        "subscription_busy",
        "ai_accounts_agent_unavailable",
    ],
)
@pytest.mark.asyncio
async def test_when_no_account_can_serve_the_call_waits_and_never_leaves_the_model(
    code: str,
) -> None:
    """The owner's rule of 2026-09-28: the chosen model or nothing, never MiniMax."""
    agent = FakeAgent(AppError(429, code, "every account is at its cap"), '{"title": "later"}')
    provider = _provider(agent, "claude-fable-5-1")
    with pytest.raises(AppError) as waiting:
        await provider.structured(Answer, "answer", "Write.", {})
    assert waiting.value.code == code and code in subscription.WAIT_CODES
    assert (provider.name, provider.model, provider.served_by) == (
        "anthropic",
        "claude-fable-5-1",
        None,
    )
    answer, _usage = await provider.structured(Answer, "answer", "Again.", {})
    assert answer.title == "later" and provider.served_by == "claude:b"
    assert [call["model"] for call in agent.calls] == ["claude-fable-5-1"] * 2


@pytest.mark.asyncio
async def test_a_run_that_started_and_failed_is_reported_not_retried_elsewhere() -> None:
    failed = AppError(502, "subscription_run_failed", "claude run failed: overloaded")
    with pytest.raises(AppError) as error:
        await _provider(FakeAgent(failed)).structured(Answer, "answer", "Write.", {})
    assert error.value.code == "subscription_run_failed"
    assert "subscription_run_failed" not in subscription.WAIT_CODES
    paused = AppError(429, "subscription_quota_paused", "spent")
    with pytest.raises(AppError):
        await _provider(FakeAgent(paused)).structured(Answer, "answer", "Write.", {})


def test_the_run_limit_leaves_room_for_the_cli_within_the_agents_bounds() -> None:
    assert run_seconds(240) == 300
    assert run_seconds(0.5) >= 30, "the agent refuses a limit under 30 s"
    assert run_seconds(5_000) == subscription.MAX_RUN_SECONDS


def _overview(*slots: dict[str, Any]) -> AgentOverview:
    return AgentOverview.model_validate(
        {
            "slots": [
                {"tool": "claude", "is_default": False, "auth_method": "claude.ai", **slot}
                for slot in slots
            ],
            "defaults": {"claude": "a", "codex": "a"},
            "allowlist_configured": False,
        }
    )


def _usage(percent: float) -> dict[str, Any]:
    return {"source": "snapshot", "windows": [{"window_minutes": 300, "used_percent": percent}]}


def test_the_connection_test_names_the_accounts_that_can_serve_and_why_others_cannot() -> None:
    ready, message = subscription_summary(
        _overview(
            {"slot": "a", "logged_in": True, "usage": _usage(100)},
            {"slot": "b", "logged_in": True, "usage": _usage(15)},
            {"slot": "c", "logged_in": True},
            {"slot": "d", "logged_in": True, "auth_method": "api_key"},
            {"slot": "e", "logged_in": False},
        ),
    )
    assert ready
    assert message.startswith("Claude 訂閱帳號可用：B（已用 15%）、C（用量未知）")
    assert "A 已用滿（100%），等額度重置" in message and "D 是 API 金鑰登入" in message
    ready, message = subscription_summary(_overview({"slot": "a", "logged_in": False}))
    assert not ready and "沒有登入的 Claude 訂閱帳號" in message


@pytest.mark.asyncio
async def test_the_news_stages_run_on_the_subscription_when_claude_is_set_to_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.news_automation import ai as news_ai

    agent = FakeAgent('{"title": "新聞"}')
    monkeypatch.setattr(subscription, "AiAccountsAgentClient", lambda _settings: agent)
    answer, usage, model = await news_ai._structured(
        _settings(), "anthropic", "claude-opus-5-5", Answer, "answer", "Write.", {}
    )
    assert (answer.title, model) == ("新聞", "claude-opus-5-5")
    assert agent.calls[0]["timeout_seconds"] == news_ai.STAGE_TIMEOUT_SECONDS + 60


@pytest.mark.asyncio
async def test_a_full_subscription_is_reported_even_with_a_minimax_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The news pipeline tries later on the same model; MiniMax never takes the call."""

    full = AppError(429, "subscription_quota_paused", "every Claude account is at 100%")
    monkeypatch.setattr(subscription, "AiAccountsAgentClient", lambda _settings: FakeAgent(full))
    settings = _settings()
    assert settings.minimax_api_key
    provider = research_provider(settings, "anthropic", model="claude-opus-5-5")
    assert isinstance(provider, SubscriptionResearchProvider)
    with pytest.raises(AppError) as waiting:
        await provider.structured(Answer, "answer", "Write.", {})
    assert waiting.value.code == "subscription_quota_paused"
    assert (provider.name, provider.model) == ("anthropic", "claude-opus-5-5")
    assert not hasattr(Settings(), "ai_subscription_fallback")
