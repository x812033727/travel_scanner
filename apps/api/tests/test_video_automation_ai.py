"""Running video stages with the owner's models: budgets, failures, the record, and topics."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

import app.video_automation.admin_api as automation_api
import app.video_automation.ai as ai
import app.video_automation.settings as automation_settings
import app.video_automation.topics as topics
import app.video_automation.usage as usage
from app.config import Settings
from app.db import SessionFactory, engine, get_session
from app.models import VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation.models import DEFAULT_STAGE_MODELS, VideoAiRun, VideoAutomationSettings
from app.video_automation.schemas import StageRunIn, UsageView
from app.video_speech import admin_api as speech_api

KEYS = Settings(anthropic_api_key="a", hotspot_guide_gemini_api_key="g")
# The API-key path; the defaults run on the subscription (test_video_automation_subscription.py).
API_MODELS = {
    stage: {"provider": "anthropic", "model": choice["model"]}
    for stage, choice in DEFAULT_STAGE_MODELS.items()
}


def _usage(**changes: int) -> UsageView:
    values = {
        "tokens": 1_000,
        "token_budget": 20_000_000,
        "drafts": 2,
        "draft_budget": 8,
        "calls": 10,
        "failed_calls": 0,
    }
    values.update(changes)
    return UsageView(**values)


class FakeProvider:
    def __init__(self, outcome: Any) -> None:
        self.outcome = outcome
        self.model = "claude-opus-5-5"
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self.closed = False

    async def structured(
        self, schema: Any, name: str, instructions: str, payload: dict[str, Any]
    ) -> tuple[Any, dict[str, int]]:
        self.calls.append((name, instructions, payload))
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return schema(text=self.outcome), {"input_tokens": 1200, "output_tokens": 300}

    async def close(self) -> None:
        self.closed = True


def _session() -> MagicMock:
    session = MagicMock()
    session.commit = AsyncMock()
    return session


def _request(stage: str = "verifier", slug: str = "ai-model-choice") -> StageRunIn:
    return StageRunIn(stage=stage, slug=slug, instructions="Check it.", payload={"claims": []})


@pytest.fixture
def stage(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    state: dict[str, Any] = {"usage": _usage(), "has_draft": False, "provider": FakeProvider("ok")}
    monkeypatch.setattr(ai, "usage_view", AsyncMock(side_effect=lambda *_: state["usage"]))
    monkeypatch.setattr(ai, "slug_has_draft", AsyncMock(side_effect=lambda *_: state["has_draft"]))

    def provider(runtime: Settings, name: str, client: Any = None, **kwargs: Any) -> Any:
        state["asked"] = (name, kwargs)
        return state["provider"]

    monkeypatch.setattr(ai, "research_provider", provider)
    return state


@pytest.mark.asyncio
async def test_a_stage_runs_with_the_model_its_setting_names_and_is_recorded(
    stage: dict[str, Any],
) -> None:
    session = _session()
    row = VideoAutomationSettings(
        stage_models={"verifier": {"provider": "anthropic", "model": "claude-opus-5-5"}},
        monthly_token_budget_millions=20,
        max_drafts_per_month=8,
    )
    token = uuid4()
    out = await ai.run_stage(session, KEYS, row, _request(), token)
    assert out.text == "ok" and out.model == "claude-opus-5-5"
    assert (out.input_tokens, out.output_tokens) == (1200, 300)
    assert out.usage.tokens == 1_000 + 1500 and out.usage.calls == 11
    name, kwargs = stage["asked"]
    assert name == "anthropic" and kwargs["model"] == "claude-opus-5-5"
    assert kwargs["max_output_tokens"] == 16_000
    assert stage["provider"].calls == [("video_verifier", "Check it.", {"claims": []})]
    assert stage["provider"].closed
    recorded = session.add.call_args.args[0]
    assert isinstance(recorded, VideoAiRun)
    assert (recorded.status, recorded.stage, recorded.token_id) == ("ok", "verifier", token)
    assert (recorded.input_tokens, recorded.output_tokens) == (1200, 300)
    session.commit.assert_awaited()


@pytest.mark.asyncio
async def test_a_stage_missing_from_the_settings_uses_the_default_model(
    stage: dict[str, Any],
) -> None:
    empty = VideoAutomationSettings(stage_models={})
    assert ai.stage_choice(empty, "writer") == ("claude_code", "claude-sonnet-5")
    row = VideoAutomationSettings(stage_models=API_MODELS, monthly_token_budget_millions=20)
    await ai.run_stage(_session(), KEYS, row, _request("writer"), None)
    assert stage["asked"][0] == "anthropic"
    assert stage["asked"][1]["model"] == "claude-sonnet-5"


@pytest.mark.asyncio
async def test_budgets_and_missing_keys_stop_a_stage_before_any_model_is_called(
    stage: dict[str, Any],
) -> None:
    row = VideoAutomationSettings(stage_models=API_MODELS, monthly_token_budget_millions=20)
    stage["usage"] = _usage(tokens=20_000_000)
    with pytest.raises(ai.StageFailed) as spent:
        await ai.run_stage(_session(), KEYS, row, _request(), None)
    assert (spent.value.status, spent.value.code) == (429, "video_ai_budget_exhausted")

    stage["usage"] = _usage(drafts=8)
    with pytest.raises(ai.StageFailed) as drafts:
        await ai.run_stage(_session(), KEYS, row, _request("planner", "new-video"), None)
    assert drafts.value.code == "video_ai_budget_exhausted" and "8 支" in drafts.value.detail
    stage["has_draft"] = True
    await ai.run_stage(_session(), KEYS, row, _request("planner", "new-video"), None)

    stage["usage"] = _usage()
    no_openai = VideoAutomationSettings(
        stage_models={"verifier": {"provider": "openai", "model": "gpt-6-astra"}}
    )
    with pytest.raises(ai.StageFailed) as missing:
        await ai.run_stage(_session(), KEYS, no_openai, _request(), None)
    assert (missing.value.status, missing.value.code) == (503, "video_ai_provider_not_configured")
    assert len(stage["provider"].calls) == 1, "only the planner re-run above reached the model"


@pytest.mark.parametrize(
    ("error", "status", "code", "retry"),
    [
        (
            httpx.HTTPStatusError(
                "overloaded",
                request=httpx.Request("POST", "https://x"),
                response=httpx.Response(529, headers={"Retry-After": "12"}),
            ),
            503,
            "video_ai_upstream_busy",
            "12",
        ),
        (
            httpx.HTTPStatusError(
                "bad", request=httpx.Request("POST", "https://x"), response=httpx.Response(400)
            ),
            502,
            "video_ai_upstream_failed",
            None,
        ),
        (httpx.ConnectError("down"), 502, "video_ai_upstream_unreachable", "30"),
        (
            ValueError("AI structured output validation failed"),
            502,
            "video_ai_output_invalid",
            None,
        ),
    ],
)
@pytest.mark.asyncio
async def test_a_failed_call_is_recorded_and_explained(
    stage: dict[str, Any], error: Exception, status: int, code: str, retry: str | None
) -> None:
    stage["provider"] = FakeProvider(error)
    session = _session()
    row = VideoAutomationSettings(stage_models=API_MODELS, monthly_token_budget_millions=20)
    with pytest.raises(ai.StageFailed) as failed:
        await ai.run_stage(session, KEYS, row, _request(), None)
    assert (failed.value.status, failed.value.code, failed.value.retry_after) == (
        status,
        code,
        retry,
    )
    recorded = session.add.call_args.args[0]
    assert (recorded.status, recorded.error_code) == ("failed", code)
    assert stage["provider"].closed


def test_the_month_starts_on_the_first_in_utc_and_budgets_name_the_limit() -> None:
    moment = datetime(2026, 9, 25, 8, 30, tzinfo=UTC)
    assert usage.month_start(moment) == datetime(2026, 9, 1, tzinfo=UTC)
    assert usage.budget_problem(_usage(), new_draft=True) is None
    assert "20,000,000" in (usage.budget_problem(_usage(tokens=20_000_000), new_draft=False) or "")
    assert usage.budget_problem(_usage(drafts=8), new_draft=False) is None
    assert usage.budget_problem(_usage(drafts=8), new_draft=True)


@pytest.mark.asyncio
async def test_web_topics_come_from_the_past_week_within_the_brave_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    budget = {"left": 2}

    async def consume(redis: Any, provider: str, limit: int) -> bool:
        assert provider == "brave"
        budget["left"] -= 1
        return budget["left"] >= 0

    monkeypatch.setattr(topics, "consume_search_budget", consume)
    seen: list[dict[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(dict(request.url.params))
        assert request.headers["X-Subscription-Token"] == "brave-key"
        return httpx.Response(
            200,
            json={
                "web": {
                    "results": [
                        {"url": "https://openai.com/a", "title": "A", "description": "a"},
                        {"url": "http://insecure.example/b", "title": "B"},
                        {"url": "https://openai.com/a", "title": "A again"},
                    ]
                }
            },
        )

    runtime = Settings(hotspot_guide_brave_api_key="brave-key")
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        found, notes = await topics.search_topics(
            runtime, MagicMock(), ["AI", "科技", "AI 工具教學"], client
        )
    assert [topic.url for topic in found] == ["https://openai.com/a"]
    assert all(params["freshness"] == "pw" for params in seen) and len(seen) == 2
    assert notes == ["今天的 Brave 搜尋額度已用完"]
    none, why = await topics.search_topics(Settings(), MagicMock(), ["AI"])
    assert none == [] and why == ["Brave 搜尋沒有設定或已關閉"]


def _app() -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(automation_api.tool_router, prefix="/api/v1")

    async def session() -> Any:
        yield MagicMock(commit=AsyncMock())

    app.dependency_overrides[get_session] = session
    return app


@pytest.mark.asyncio
async def test_the_run_route_needs_a_token_and_passes_refusals_on_with_their_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _app()
    body = {"stage": "writer", "slug": "v", "instructions": "Write.", "payload": {}}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        anonymous = await client.post("/api/v1/video/automation/run", json=body)
    assert anonymous.status_code == 401

    app.dependency_overrides[speech_api.video_tool] = lambda: VideoToolToken(
        id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x"
    )
    monkeypatch.setattr(automation_api, "enforce_named_rate_limit", AsyncMock())
    monkeypatch.setattr(automation_api, "load_runtime_settings", AsyncMock(return_value=KEYS))
    monkeypatch.setattr(
        automation_settings, "settings_row", AsyncMock(return_value=VideoAutomationSettings())
    )
    monkeypatch.setattr(
        automation_api,
        "run_stage",
        AsyncMock(side_effect=ai.StageFailed(503, "video_ai_upstream_busy", "busy", "12")),
    )
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        busy = await client.post("/api/v1/video/automation/run", json=body)
        bad = await client.post("/api/v1/video/automation/run", json={**body, "stage": "boss"})
    assert busy.status_code == 503 and busy.headers["retry-after"] == "12"
    assert busy.json()["code"] == "video_ai_upstream_busy"
    assert bad.status_code == 422, "only the six stages exist"


integration = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


@pytest_asyncio.fixture(loop_scope="module")
async def clean_runs() -> AsyncIterator[str]:
    slug = f"it-{uuid4().hex[:10]}"
    yield slug
    async with SessionFactory() as session:
        await session.execute(delete(VideoAiRun).where(VideoAiRun.slug.like("it-%")))
        await session.commit()
    await engine.dispose()


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_usage_sums_this_months_calls_and_counts_each_drafted_video_once(
    clean_runs: str,
) -> None:
    slug = clean_runs
    now = datetime.now(UTC)
    last_month = usage.month_start(now) - timedelta(days=1)

    def run(stage: str, status: str, tokens: int, when: datetime, name: str = slug) -> VideoAiRun:
        return VideoAiRun(
            slug=name,
            stage=stage,
            provider="anthropic",
            model="claude-sonnet-5",
            status=status,
            input_tokens=tokens,
            output_tokens=0,
            duration_ms=1,
            created_at=when,
        )

    async with SessionFactory() as session:
        before = await usage.usage_view(
            session,
            VideoAutomationSettings(monthly_token_budget_millions=20, max_drafts_per_month=8),
        )
        session.add_all(
            [
                run("planner", "ok", 100, now),
                run("planner", "ok", 100, now),
                run("writer", "ok", 1000, now),
                run("verifier", "failed", 0, now),
                run("planner", "ok", 5000, last_month, f"{slug}-old"),
            ]
        )
        await session.commit()
        after = await usage.usage_view(
            session,
            VideoAutomationSettings(monthly_token_budget_millions=20, max_drafts_per_month=8),
        )
        assert after.tokens - before.tokens == 1200
        assert after.calls - before.calls == 4 and after.failed_calls - before.failed_calls == 1
        assert after.drafts - before.drafts == 1, "two planner runs of one video are one draft"
        assert await usage.slug_has_draft(session, slug)
        assert not await usage.slug_has_draft(session, f"{slug}-old")
        assert isinstance(await topics.site_topics(session), list)
