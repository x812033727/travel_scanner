import json

import httpx
import pytest
from pydantic import ValidationError

from app.config import get_settings
from app.hotspots.ai_search import (
    AnthropicResearchProvider,
    QueryPlan,
    ResponsesResearchProvider,
    _candidate_metadata,
    configured_research_providers,
    estimate_calls,
    research_provider,
    summarize_provider_error,
)
from app.hotspots.guides import GuideCandidate
from app.problems import AppError


def test_estimate_calls_obeys_depth_and_selected_sources() -> None:
    assert estimate_calls(5, ["article", "video"], "deep") == {
        "ai": 10,
        "brave": 25,
        "gemini": 25,
        "youtube": 25,
    }
    assert estimate_calls(2, ["article"], "economy") == {
        "ai": 4,
        "brave": 2,
        "gemini": 2,
        "youtube": 0,
    }


def test_query_plan_rejects_model_generated_urls() -> None:
    plan = QueryPlan.model_validate(
        {
            "article_queries": ["Tokyo guide", "https://model.invalid/invented"],
            "video_queries": ["東京 旅行"],
        }
    )
    assert plan.article_queries == ["Tokyo guide"]


def test_ai_assessment_payload_never_exposes_a_candidate_url() -> None:
    payload = _candidate_metadata(
        GuideCandidate(
            content_type="article",
            provider="brave",
            locale="en",
            title="A real guide",
            creator_name="Publisher",
            canonical_url="https://publisher.example/real-guide",
        ),
        "c0",
    )
    assert payload["candidate_id"] == "c0"
    assert not any("url" in key for key in payload)
    assert "publisher.example" not in json.dumps(payload)


def test_unconfigured_provider_is_explicit_and_never_falls_back() -> None:
    settings = get_settings().model_copy(
        update={"minimax_api_key": None, "openai_api_key": None, "anthropic_api_key": None}
    )
    assert configured_research_providers(settings) == {
        "minimax": False,
        "openai": False,
        "anthropic": False,
    }
    with pytest.raises(AppError) as error:
        research_provider(settings, "minimax")
    assert error.value.code == "hotspot_guide_ai_provider_not_configured"


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ["openai", "minimax"])
async def test_responses_adapter_repairs_invalid_json_once(name: str) -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        body = json.loads(request.content)
        assert request.url.path == "/responses"
        assert body["store"] is False
        assert body["text"]["format"]["type"] == "json_schema"
        if calls == 1:
            return httpx.Response(200, json={"output_text": "not-json"})
        assert "Repair the previous invalid JSON" in body["input"]
        return httpx.Response(
            200,
            json={
                "output_text": '{"article_queries":["Asakusa travel"],"video_queries":[]}',
                "usage": {"input_tokens": 12, "output_tokens": 5},
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = ResponsesResearchProvider(
            name, "https://ai.example", "secret", "research-model", 10, 1000, client
        )
        result, usage = await provider.structured(
            QueryPlan, "query_plan", "Return JSON", {"attraction": "Asakusa"}
        )
    assert calls == 2
    assert result.article_queries == ["Asakusa travel"]
    assert usage == {"input_tokens": 12, "output_tokens": 5}


@pytest.mark.asyncio
async def test_anthropic_adapter_uses_structured_output_without_tools_or_urls() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert request.url.path == "/messages"
        assert "tools" not in body
        assert body["output_config"]["format"]["type"] == "json_schema"
        return httpx.Response(
            200,
            json={
                "content": [
                    {
                        "type": "text",
                        "text": '{"article_queries":[],"video_queries":["浅草 観光"]}',
                    }
                ],
                "usage": {"input_tokens": 8, "output_tokens": 4},
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = AnthropicResearchProvider(
            "https://claude.example", "secret", "claude-model", 10, 1000, client
        )
        result, _ = await provider.structured(
            QueryPlan, "query_plan", "Return JSON", {"attraction": "浅草"}
        )
    assert result.video_queries == ["浅草 観光"]


@pytest.mark.asyncio
async def test_invalid_json_after_one_repair_fails_closed() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"output_text": "still-invalid"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = ResponsesResearchProvider(
            "openai", "https://ai.example", "secret", "model", 10, 1000, client
        )
        with pytest.raises(ValidationError):
            await provider.structured(QueryPlan, "query_plan", "Return JSON", {})


@pytest.mark.asyncio
async def test_minimax_fenced_json_next_to_reasoning_parses_on_the_first_call() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        body = json.loads(request.content)
        assert body["instructions"].startswith("Return JSON")
        assert "article_queries" in body["instructions"]
        assert "code fences" in body["instructions"]
        fenced = (
            "Plan:\n```json\n"
            '{"article_queries": ["淺草寺 旅遊"], "video_queries": ["淺草寺 vlog"]}'
            "\n```"
        )
        return httpx.Response(
            200,
            json={
                "status": "completed",
                "output": [
                    {"type": "reasoning", "id": "rs_1", "summary": []},
                    {"type": "message", "content": [{"type": "output_text", "text": fenced}]},
                ],
                "usage": {"input_tokens": 30, "output_tokens": 20},
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = ResponsesResearchProvider(
            "minimax", "https://api.minimax.io/v1", "secret", "MiniMax-M3", 10, 1000, client
        )
        result, usage = await provider.structured(
            QueryPlan, "query_plan", "Return JSON", {"attraction": "淺草寺"}
        )
    assert calls == 1
    assert result.article_queries == ["淺草寺 旅遊"]
    assert result.video_queries == ["淺草寺 vlog"]
    assert usage == {"input_tokens": 30, "output_tokens": 20}


@pytest.mark.asyncio
async def test_incomplete_response_fails_without_a_repair_round_trip() -> None:
    calls = 0

    def handler(_: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(
            200,
            json={
                "status": "incomplete",
                "incomplete_details": {"reason": "max_output_tokens"},
                "output": [],
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = ResponsesResearchProvider(
            "minimax", "https://ai.example", "secret", "model", 10, 1000, client
        )
        with pytest.raises(ValueError, match="max_output_tokens"):
            await provider.structured(QueryPlan, "query_plan", "Return JSON", {})
    assert calls == 1


def test_summarize_provider_error_is_short_and_never_leaks_the_query_string() -> None:
    request = httpx.Request(
        "GET", "https://www.googleapis.com/youtube/v3/search?key=SECRET-KEY&q=asakusa"
    )
    response = httpx.Response(
        403,
        json={"error": {"message": "The request cannot be completed because quota exceeded."}},
        request=request,
    )
    summary = summarize_provider_error(
        httpx.HTTPStatusError("boom", request=request, response=response)
    )
    assert summary.startswith("HTTP 403 from www.googleapis.com: The request cannot be completed")
    assert "SECRET-KEY" not in summary
    assert "key=" not in summary
    assert len(summary) <= 200

    minimax_request = httpx.Request("POST", "https://api.minimaxi.com/v1/responses")
    minimax = httpx.Response(
        401,
        json={"base_resp": {"status_code": 2049, "status_msg": "invalid api key"}},
        request=minimax_request,
    )
    assert (
        summarize_provider_error(
            httpx.HTTPStatusError("x", request=minimax_request, response=minimax)
        )
        == "HTTP 401 from api.minimaxi.com: 2049 invalid api key"
    )

    with pytest.raises(ValidationError) as error:
        QueryPlan.model_validate_json('{"article_queries": "nope"}')
    validation = summarize_provider_error(error.value)
    assert validation.startswith("AI output failed schema validation (1 errors): article_queries:")
    assert len(validation) <= 200

    assert summarize_provider_error(AppError(404, "hotspot_not_found", "找不到這個景點")) == (
        "找不到這個景點"
    )
    assert len(summarize_provider_error(ValueError("x" * 500))) <= 200
    assert "[redacted]" in summarize_provider_error(
        ValueError("see https://example.com/?key=abc for details")
    )


def test_research_model_prefers_the_feature_override_then_the_planner_model() -> None:
    from app.hotspots.ai_search import research_model

    settings = get_settings().model_copy(
        update={
            "openai_api_key": "sk-test",
            "openai_model": "gpt-planner",
            "hotspot_guide_ai_openai_model": None,
        }
    )
    assert research_model(settings, "openai") == "gpt-planner"
    assert research_provider(settings, "openai").model == "gpt-planner"

    override = settings.model_copy(update={"hotspot_guide_ai_openai_model": "gpt-search"})
    assert research_model(override, "openai") == "gpt-search"
    assert research_provider(override, "openai").model == "gpt-search"

    blank = settings.model_copy(update={"hotspot_guide_ai_openai_model": "   "})
    assert research_model(blank, "openai") == "gpt-planner"


def test_ai_search_overview_lists_the_model_each_vendor_would_use() -> None:
    from app.hotspots.ai_search import ai_search_overview

    settings = get_settings().model_copy(
        update={
            "minimax_api_key": "mm-test",
            "openai_api_key": None,
            "anthropic_api_key": None,
            "minimax_model": "MiniMax-M3",
            "hotspot_guide_ai_minimax_model": "MiniMax-M2.7",
            "hotspot_guide_ai_default_provider": "minimax",
        }
    )
    overview = ai_search_overview(settings)
    assert overview["default_provider"] == "minimax"
    assert overview["providers"] == {"minimax": True, "openai": False, "anthropic": False}
    assert overview["models"] == {
        "minimax": "MiniMax-M2.7",
        "openai": settings.openai_model,
        "anthropic": settings.anthropic_model,
    }


def test_guide_ai_search_request_defaults_the_provider_to_the_admin_setting() -> None:
    from uuid import uuid4

    from app.hotspots.admin_router import GuideAISearchRequest

    assert GuideAISearchRequest(hotspot_id=uuid4()).provider is None
    assert GuideAISearchRequest(hotspot_id=uuid4(), provider="openai").provider == "openai"
