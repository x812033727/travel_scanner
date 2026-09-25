import json

import httpx
import pytest
from pydantic import BaseModel

from app.ai import catalog
from app.config import Settings
from app.hotspots.ai_search import AnthropicResearchProvider
from app.news_automation.service import model_options as news_model_options

# What an Anthropic request here may carry. Claude Opus 5.5 answers 400 to temperature,
# top_p, top_k, a disabled or budgeted `thinking`, and a forced `tool_choice`.
ANTHROPIC_REQUEST_KEYS = {"model", "max_tokens", "system", "messages", "output_config"}


def test_every_catalog_id_is_a_valid_model_id_and_unique_per_vendor() -> None:
    for vendor, entries in catalog.MODEL_CATALOG.items():
        ids = [entry.id for entry in entries]
        assert len(ids) == len(set(ids)), vendor
        for entry in entries:
            assert catalog.valid_model_id(entry.id), entry.id
            assert entry.label
            assert entry.capabilities


def test_shipped_defaults_are_in_the_catalog() -> None:
    settings = Settings()
    for field, value in (
        ("openai_model", settings.openai_model),
        ("anthropic_model", settings.anthropic_model),
        ("minimax_model", settings.minimax_model),
        ("hotspot_guide_gemini_model", settings.hotspot_guide_gemini_model),
        ("gemini_model", settings.gemini_model),
        ("jev_model", settings.jev_model),
    ):
        assert value in [entry.id for entry in catalog.model_options(field)], field


def test_field_options_only_offer_models_the_code_path_can_drive() -> None:
    for field in ("openai_model", "minimax_model", "hotspot_guide_ai_openai_model"):
        assert all(
            "responses_json_schema_strict" in entry.capabilities
            for entry in catalog.model_options(field)
        )
    for field in ("anthropic_model", "hotspot_guide_ai_anthropic_model"):
        assert all(
            "anthropic_structured_output" in entry.capabilities
            for entry in catalog.model_options(field)
        )
    assert all(
        "gemini_grounded" in entry.capabilities
        for entry in catalog.model_options("hotspot_guide_gemini_model")
    )
    for field in ("gemini_model", "hotspot_guide_ai_gemini_model"):
        assert all(
            "gemini_structured" in entry.capabilities for entry in catalog.model_options(field)
        )
    assert "hotspot_guide_ai_gemini_model" in catalog.OPTIONAL_MODEL_FIELDS
    assert catalog.field_options(("ai_planner_mode", "openai_model")).keys() == {"openai_model"}
    assert catalog.field_options(("route_cache_ttl_seconds",)) == {}


def test_model_id_pattern_matches_the_security_audit_rule() -> None:
    assert catalog.valid_model_id("gpt-5.6-terra")
    assert catalog.valid_model_id("ft:gpt-5.6-terra:org:abc")
    assert catalog.valid_model_id("models_v2")
    assert not catalog.valid_model_id("")
    assert not catalog.valid_model_id("gpt/../admin")
    assert not catalog.valid_model_id("model name")
    assert not catalog.valid_model_id("a" * 129)


def test_model_label_falls_back_to_the_raw_id() -> None:
    assert catalog.model_label("gemini", "gemini-3.8-flash") == "Gemini 3.8 Flash"
    assert catalog.model_label("gemini", "gemini-9-custom") == "gemini-9-custom"


def test_jev_options_cannot_be_offered_to_a_generating_code_path() -> None:
    """Jev returns decisions, never prose; no generating field may list its models."""
    assert all(
        "jev_structured_decision" in entry.capabilities
        for entry in catalog.model_options("jev_model")
    )
    for field in (
        "openai_model",
        "anthropic_model",
        "minimax_model",
        "gemini_model",
        "hotspot_guide_gemini_model",
    ):
        assert all(
            "jev_structured_decision" not in entry.capabilities
            for entry in catalog.model_options(field)
        ), field


def test_news_offers_claude_opus_5_5_for_writing_and_fact_checking() -> None:
    offered = [option.value for option in news_model_options()["anthropic"]]
    assert offered[0] == "claude-opus-5-5"
    assert "claude-opus-5" in offered


class _Reply(BaseModel):
    value: str


@pytest.mark.asyncio
async def test_the_anthropic_request_is_one_opus_5_5_accepts_and_thinking_is_skipped() -> None:
    sent: list[dict[str, object]] = []

    def answer(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(
            200,
            json={
                # Opus 5.5 always thinks; the block comes back with empty text by default.
                "content": [
                    {"type": "thinking", "thinking": "", "signature": "sig"},
                    {"type": "text", "text": '{"value": "ok"}'},
                ],
                "stop_reason": "end_turn",
                "usage": {"input_tokens": 12, "output_tokens": 3},
            },
        )

    client = httpx.AsyncClient(transport=httpx.MockTransport(answer))
    provider = AnthropicResearchProvider(
        "https://api.anthropic.test/v1", "test-key", "claude-opus-5-5", 5.0, 32_000, client
    )
    try:
        reply, usage = await provider.structured(_Reply, "reply", "Answer.", {"q": "ping"})
    finally:
        await client.aclose()

    assert reply.value == "ok"
    assert usage == {"input_tokens": 12, "output_tokens": 3}
    assert set(sent[0]) <= ANTHROPIC_REQUEST_KEYS
    assert sent[0]["model"] == "claude-opus-5-5"
