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


class FakeMiniMax:
    name = "minimax"
    model = "MiniMax-M3"

    def __init__(self) -> None:
        self.calls = 0
        self.closed = False

    async def structured(self, schema: Any, *_args: Any) -> tuple[Any, dict[str, int]]:
        self.calls += 1
        return schema(title="from MiniMax"), {"input_tokens": 7, "output_tokens": 3}

    async def close(self) -> None:
        self.closed = True


def _provider(agent: FakeAgent, fallback: FakeMiniMax | None = None) -> Any:
    return SubscriptionResearchProvider(
        _settings(),
        "claude-opus-5-5",
        240,
        fallback=(lambda: fallback) if fallback is not None else None,
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
async def test_when_no_account_can_serve_the_call_goes_to_minimax(code: str) -> None:
    agent = FakeAgent(AppError(429, code, "every account is at its cap"))
    minimax = FakeMiniMax()
    provider = _provider(agent, minimax)
    answer, usage = await provider.structured(Answer, "answer", "Write.", {})
    assert answer.title == "from MiniMax" and usage == {"input_tokens": 7, "output_tokens": 3}
    assert (provider.name, provider.model, provider.served_by) == (
        "minimax",
        "MiniMax-M3",
        "minimax",
    )
    await provider.structured(Answer, "answer", "Again.", {})
    assert len(agent.calls) == 1 and minimax.calls == 2, "the rest of the run stays on MiniMax"
    await provider.close()
    assert minimax.closed


@pytest.mark.asyncio
async def test_a_run_that_started_and_failed_is_reported_not_retried_elsewhere() -> None:
    minimax = FakeMiniMax()
    failed = AppError(502, "subscription_run_failed", "claude run failed: overloaded")
    with pytest.raises(AppError) as error:
        await _provider(FakeAgent(failed), minimax).structured(Answer, "answer", "Write.", {})
    assert error.value.code == "subscription_run_failed" and minimax.calls == 0
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
