"""Video stages on the Claude subscription accounts: the agent call, the record, the pauses."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

import app.video_automation.ai as ai
import app.video_automation.subscription as subscription
from app.admin_ai_accounts.agent import AgentRunResult
from app.config import Settings
from app.problems import AppError
from app.video_automation.models import DEFAULT_STAGE_MODELS, VideoAiRun, VideoAutomationSettings
from app.video_automation.schemas import StageRunIn, UsageView
from app.video_automation.settings import configured_providers, model_options
from app.video_automation.usage import budget_problem

AGENT = Settings(
    ai_accounts_enabled=True,
    ai_accounts_agent_hmac_key="k" * 64,
    ai_accounts_agent_socket="/run/mokaair-ai-accounts/agent.sock",
)


class FakeAgent:
    def __init__(self, outcome: Any) -> None:
        self.outcome = outcome
        self.calls: list[dict[str, Any]] = []

    async def run_prompt(self, **kwargs: Any) -> AgentRunResult:
        self.calls.append(kwargs)
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return AgentRunResult(
            text=self.outcome,
            slot="b",
            model="claude-opus-5-5",
            input_tokens=900,
            output_tokens=100,
            duration_ms=1234,
        )


def test_the_subscription_is_the_default_and_offers_the_claude_models() -> None:
    assert {choice["provider"] for choice in DEFAULT_STAGE_MODELS.values()} == {"claude_code"}
    assert "claude-opus-5-5" in {option.value for option in model_options()["claude_code"]}
    assert "claude_code" in configured_providers(AGENT)
    assert "claude_code" not in configured_providers(Settings())


@pytest.mark.asyncio
async def test_a_stage_is_sent_to_the_agent_with_the_owners_cap_as_json() -> None:
    agent = FakeAgent('{"video": {}}')
    run = await subscription.run_on_subscription(
        AGENT,
        model="claude-opus-5-5",
        instructions="Check it.",
        payload={"claims": "c1｜Go｜https://openai.com/a"},
        max_usage_percent=70,
        client=agent,  # type: ignore[arg-type]
    )
    assert (run.text, run.model, run.input_tokens, run.output_tokens) == (
        '{"video": {}}',
        "claude-opus-5-5",
        900,
        100,
    )
    call = agent.calls[0]
    assert call["max_usage_percent"] == 70 and call["model"] == "claude-opus-5-5"
    assert call["system"].startswith("Check it.") and "JSON object" in call["system"]
    assert call["prompt"] == '{"claims": "c1｜Go｜https://openai.com/a"}', (
        "the payload keeps its text"
    )


@pytest.mark.parametrize(
    ("code", "status", "mapped"),
    [
        ("subscription_quota_paused", 429, "video_ai_subscription_paused"),
        ("subscription_not_signed_in", 409, "video_ai_provider_not_configured"),
        ("ai_accounts_agent_unavailable", 503, "video_ai_upstream_unreachable"),
        ("subscription_run_failed", 502, "video_ai_upstream_failed"),
    ],
)
@pytest.mark.asyncio
async def test_the_agents_refusals_become_the_pipelines_errors(
    code: str, status: int, mapped: str
) -> None:
    agent = FakeAgent(AppError(status, code, "detail from the agent"))
    with pytest.raises(ai.StageFailed) as failed:
        await subscription.run_on_subscription(
            AGENT,
            model="m",
            instructions="i",
            payload={},
            max_usage_percent=80,
            client=agent,  # type: ignore[arg-type]
        )
    assert failed.value.code == mapped


def _usage(**changes: int) -> UsageView:
    values = {"tokens": 0, "token_budget": 1_000_000, "subscription_tokens": 0, "drafts": 0}
    values.update({"draft_budget": 8, "calls": 0, "failed_calls": 0})
    values.update(changes)
    return UsageView(**values)


def test_the_token_budget_limits_api_calls_only() -> None:
    spent = _usage(tokens=1_000_000)
    assert budget_problem(spent, new_draft=False)
    assert budget_problem(spent, new_draft=False, billed=False) is None
    assert budget_problem(_usage(drafts=8), new_draft=True, billed=False), "drafts count on both"


def _request() -> StageRunIn:
    return StageRunIn(stage="verifier", slug="ai-model-choice", instructions="Check.", payload={})


@pytest.mark.asyncio
async def test_a_subscription_stage_is_recorded_apart_from_the_api_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    agent = FakeAgent("text")
    monkeypatch.setattr(ai, "usage_view", AsyncMock(return_value=_usage(tokens=1_000_000)))
    monkeypatch.setattr(ai, "slug_has_draft", AsyncMock(return_value=True))
    monkeypatch.setattr(subscription, "AiAccountsAgentClient", lambda runtime: agent)
    session = MagicMock(commit=AsyncMock())
    # A value left in the retired column is ignored: an account is used until it is full.
    row = VideoAutomationSettings(stage_models={}, subscription_max_usage_percent=65)
    out = await ai.run_stage(session, AGENT, row, _request(), None)
    assert out.provider == "claude_code" and out.model == "claude-opus-5-5"
    assert out.usage.tokens == 1_000_000, "the API budget is untouched"
    assert out.usage.subscription_tokens == 1000
    assert agent.calls[0]["max_usage_percent"] == 100
    recorded = session.add.call_args.args[0]
    assert isinstance(recorded, VideoAiRun)
    assert (recorded.provider, recorded.status, recorded.input_tokens) == ("claude_code", "ok", 900)


@pytest.mark.asyncio
async def test_a_paused_subscription_records_nothing_and_a_missing_agent_says_so(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(ai, "usage_view", AsyncMock(return_value=_usage()))
    monkeypatch.setattr(ai, "slug_has_draft", AsyncMock(return_value=True))
    agent = FakeAgent(AppError(429, "subscription_quota_paused", "all accounts are full"))
    monkeypatch.setattr(subscription, "AiAccountsAgentClient", lambda runtime: agent)
    session = MagicMock(commit=AsyncMock())
    row = VideoAutomationSettings(stage_models={})
    with pytest.raises(ai.StageFailed) as paused:
        await ai.run_stage(session, AGENT, row, _request(), None)
    assert (paused.value.status, paused.value.code) == (429, "video_ai_subscription_paused")
    session.add.assert_not_called()

    with pytest.raises(ai.StageFailed) as missing:
        await ai.run_stage(session, Settings(), row, _request(), None)
    assert missing.value.code == "video_ai_provider_not_configured"
    assert "AI 帳號代理" in missing.value.detail
