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
)
from app.hotspots.guides import GuideCandidate
from app.problems import AppError


def test_estimate_calls_obeys_depth_and_selected_sources() -> None:
    assert estimate_calls(5, ["article", "video"], "deep") == {
        "ai": 10,
        "brave": 25,
        "youtube": 25,
    }
    assert estimate_calls(2, ["article"], "economy") == {
        "ai": 4,
        "brave": 2,
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
