import json
from typing import Annotated, Any, Literal

import httpx
import pytest
from pydantic import BaseModel, Field

from app.ai.structured_output import (
    anthropic_output_text,
    ensure_response_completed,
    extract_json_document,
    gemini_response_schema,
    responses_output_text,
    schema_instructions,
)

PAYLOAD = '{"article_queries": ["Asakusa guide"], "video_queries": []}'


@pytest.mark.parametrize(
    "text",
    [
        PAYLOAD,
        f"```json\n{PAYLOAD}\n```",
        f"```\n{PAYLOAD}\n```",
        f"  ```json\n{PAYLOAD}\n```  ",
        f"Here is the plan:\n```json\n{PAYLOAD}\n```\nLet me know if you need more.",
        f"```json\n{PAYLOAD}",
        f"Sure! {PAYLOAD} Hope this helps.",
    ],
)
def test_extract_json_document_recovers_the_object(text: str) -> None:
    assert json.loads(extract_json_document(text)) == json.loads(PAYLOAD)


def test_responses_output_text_reads_message_items_and_skips_reasoning() -> None:
    body = {
        "output": [
            {"type": "reasoning", "id": "rs_1", "summary": []},
            {"type": "message", "content": [{"type": "output_text", "text": '{"a": 1}'}]},
        ]
    }
    assert responses_output_text(body) == '{"a": 1}'
    assert responses_output_text({"output_text": "direct"}) == "direct"


def test_responses_output_text_rejects_refusals_and_empty_bodies() -> None:
    refusal = {"output": [{"type": "message", "content": [{"type": "refusal", "refusal": "no"}]}]}
    with pytest.raises(ValueError, match="拒絕"):
        responses_output_text(refusal)
    with pytest.raises(ValueError, match="沒有回傳"):
        responses_output_text({"output": [{"type": "reasoning"}]})


def test_ensure_response_completed_names_the_reason() -> None:
    ensure_response_completed({"status": "completed"})
    ensure_response_completed({})
    with pytest.raises(ValueError, match="max_output_tokens"):
        ensure_response_completed(
            {"status": "incomplete", "incomplete_details": {"reason": "max_output_tokens"}}
        )


def test_anthropic_output_text_joins_blocks_and_rejects_truncation() -> None:
    blocks = {"content": [{"type": "text", "text": "{"}, {"type": "text", "text": "}"}]}
    assert anthropic_output_text(blocks) == "{}"
    truncated = {"stop_reason": "max_tokens", "content": [{"type": "text", "text": "{"}]}
    with pytest.raises(ValueError, match="max_tokens"):
        anthropic_output_text(truncated)
    with pytest.raises(ValueError, match="沒有回傳"):
        anthropic_output_text({"content": []})
    declined = {
        "stop_reason": "refusal",
        "stop_details": {"type": "refusal", "category": "bio", "explanation": None},
        "content": [{"type": "text", "text": "{"}],
    }
    with pytest.raises(ValueError, match=r"拒絕回應 \(bio\)"):
        anthropic_output_text(declined)


def test_anthropic_output_text_rejects_a_refusal_even_with_partial_text() -> None:
    declined = {
        "stop_reason": "refusal",
        "stop_details": {"type": "refusal", "category": "cyber", "explanation": "..."},
        "content": [{"type": "text", "text": '{"summary": "'}],
    }
    with pytest.raises(ValueError, match=r"拒絕回應 \(cyber\)"):
        anthropic_output_text(declined)
    with pytest.raises(ValueError, match=r"拒絕回應 \(refusal\)"):
        anthropic_output_text({"stop_reason": "refusal", "stop_details": None, "content": []})


def test_schema_instructions_embed_the_schema_and_forbid_fences() -> None:
    class Plan(BaseModel):
        article_queries: list[str]

    text = schema_instructions(Plan)
    assert "article_queries" in text
    assert "code fences" in text


def test_gemini_response_schema_inlines_refs_and_drops_unsupported_keywords() -> None:
    class Leg(BaseModel):
        mode: Literal["walk", "transit"] = "walk"
        note: str | None = Field(default=None, max_length=40, pattern=r"^[^\n]*$")

    class Plan(BaseModel):
        headline: str = Field(description="Short headline")
        legs: list[Leg] = Field(default_factory=list, max_length=5)
        budget: int | None = Field(default=None, ge=0)
        cities: list[str]

    schema = gemini_response_schema(Plan)
    serialized = json.dumps(schema)
    for banned in (
        "$ref",
        "$defs",
        "title",
        "default",
        "pattern",
        "maxItems",
        "maxLength",
        "minimum",
        "additionalProperties",
        "anyOf",
    ):
        assert banned not in serialized, banned
    assert schema["type"] == "object"
    assert schema["propertyOrdering"] == ["headline", "legs", "budget", "cities"]
    assert schema["required"] == ["headline", "cities"]
    assert schema["properties"]["headline"] == {
        "type": "string",
        "description": "Short headline",
    }
    leg = schema["properties"]["legs"]["items"]
    assert leg["type"] == "object"
    assert leg["properties"]["mode"] == {"type": "string", "enum": ["walk", "transit"]}
    assert leg["properties"]["note"] == {"type": "string", "nullable": True}
    assert schema["properties"]["budget"] == {"type": "integer", "nullable": True}
    assert schema["properties"]["cities"] == {"type": "array", "items": {"type": "string"}}


def test_gemini_response_schema_covers_the_models_the_features_send() -> None:
    """Every schema-bound Gemini call in the product must survive the conversion."""
    from app.ai.itinerary import AIItineraryDraft
    from app.ai.trip_parser import TripParseDraft
    from app.hotspots.ai_search import AssessmentBatch, QueryPlan

    for model in (AIItineraryDraft, TripParseDraft, QueryPlan, AssessmentBatch):
        schema = gemini_response_schema(model)
        serialized = json.dumps(schema)
        assert schema["type"] == "object" and schema["properties"], model.__name__
        assert "$ref" not in serialized and "pattern" not in serialized, model.__name__


def test_repair_instruction_names_each_failed_field_and_keeps_the_reply() -> None:
    from pydantic import BaseModel, Field, ValidationError

    from app.ai.structured_output import repair_instruction

    class Reply(BaseModel):
        summary: list[str] = Field(max_length=2)
        title: str = Field(max_length=5)

    previous = '{"summary": ["a", "b", "c"], "title": "too long"}'
    try:
        Reply.model_validate_json(previous)
    except ValidationError as error:
        prompt = repair_instruction(previous, error)
    else:
        raise AssertionError("the reply should have failed")
    assert "Repair the previous invalid JSON" in prompt
    assert "- summary: " in prompt and "- title: " in prompt
    assert "at most 5 characters" in prompt
    assert prompt.endswith(previous)


# --- unions (task 2026-09-24-let-gemini-serve-news-stages-without) -----------------------


def _gemini_schema_before_unions(model_type: type[BaseModel]) -> dict[str, Any]:
    """The converter as it was before unions were kept, frozen as the "before" snapshot.

    Every Gemini caller whose schema has no union must still get exactly this.
    """
    schema = model_type.model_json_schema()
    definitions = schema.get("$defs") or {}

    def convert(node: dict[str, Any]) -> dict[str, Any]:
        converted: dict[str, Any]
        if "$ref" in node:
            resolved = dict(definitions[str(node["$ref"]).rsplit("/", 1)[-1]])
            if "description" in node:
                resolved["description"] = node["description"]
            return convert(resolved)
        if "allOf" in node and len(node["allOf"]) == 1:
            merged = {key: value for key, value in node.items() if key != "allOf"}
            return convert({**node["allOf"][0], **merged})
        if "anyOf" in node:
            options = [item for item in node["anyOf"] if item.get("type") != "null"]
            converted = convert(options[0]) if options else {"type": "string"}
            if len(options) != len(node["anyOf"]):
                converted["nullable"] = True
            if "description" in node:
                converted["description"] = node["description"]
            return converted
        converted = {
            key: node[key] for key in ("type", "description", "enum", "nullable") if key in node
        }
        if "const" in node:
            converted["type"] = "string"
            converted["enum"] = [str(node["const"])]
        elif "enum" in converted:
            converted["enum"] = [str(value) for value in converted["enum"]]
            converted.setdefault("type", "string")
        if node.get("type") == "object" or "properties" in node:
            properties = {
                key: convert(value) for key, value in (node.get("properties") or {}).items()
            }
            converted["type"] = "object"
            converted["properties"] = properties
            if node.get("required"):
                converted["required"] = [key for key in node["required"] if key in properties]
            converted["propertyOrdering"] = list(properties)
        elif node.get("type") == "array":
            converted["items"] = convert(node.get("items") or {"type": "string"})
        return converted

    return convert(schema)


def _schemas_without_unions() -> list[type[BaseModel]]:
    """Every model a feature other than the news stages sends through the converter."""
    from app.ai.itinerary import AIItineraryDraft
    from app.ai.trip_parser import TripParseDraft
    from app.catalog_review.provider import _CorrectionSchema, _DiscoveryDataSchema
    from app.catalog_review.schemas import AssessmentBatch as CatalogAssessmentBatch
    from app.catalog_review.schemas import DiscoveryBatch, EnrichmentBatch
    from app.community.translation import TranslatedText
    from app.hotspots.ai_search import AssessmentBatch, QueryPlan
    from app.hotspots.intro_generation import IntroBatch
    from app.video_automation.ai import StageText

    return [
        AIItineraryDraft,
        TripParseDraft,
        CatalogAssessmentBatch,
        _CorrectionSchema,
        EnrichmentBatch,
        DiscoveryBatch,
        _DiscoveryDataSchema,
        TranslatedText,
        QueryPlan,
        AssessmentBatch,
        IntroBatch,
        StageText,
    ]


def _news_replies() -> list[type[BaseModel]]:
    from app.news_automation.schemas import (
        EditorialDraft,
        LocaleReviewResult,
        LocalizedDocument,
        VerificationResult,
    )

    return [EditorialDraft, VerificationResult, LocalizedDocument, LocaleReviewResult]


def _guide_block_types() -> set[str]:
    from app.guides.schemas import GuideDocument

    blocks = GuideDocument.model_json_schema()["properties"]["blocks"]["items"]
    return set(blocks["discriminator"]["mapping"])


def _block_options(schema: dict[str, Any]) -> list[dict[str, Any]]:
    document = schema["properties"].get("document") or schema["properties"]["corrected_document"]
    options: list[dict[str, Any]] = document["properties"]["blocks"]["items"]["anyOf"]
    return options


def test_gemini_schemas_without_unions_are_byte_identical_to_before() -> None:
    for model in _schemas_without_unions():
        before = json.dumps(_gemini_schema_before_unions(model), ensure_ascii=False)
        assert json.dumps(gemini_response_schema(model), ensure_ascii=False) == before, (
            model.__name__
        )
    # The frozen copy is a real "before": it is what told Gemini every block was a heading.
    for model in _news_replies():
        assert gemini_response_schema(model) != _gemini_schema_before_unions(model)


def test_gemini_response_schema_keeps_every_block_of_a_news_document() -> None:
    expected = _guide_block_types()
    assert len(expected) == 13
    for model in _news_replies():
        schema = gemini_response_schema(model)
        options = _block_options(schema)
        kinds = [option["properties"]["type"]["enum"] for option in options]
        assert all(len(kind) == 1 for kind in kinds), model.__name__
        assert {kind[0] for kind in kinds} == expected, model.__name__
        rich = next(o for o in options if o["properties"]["type"]["enum"] == ["rich_paragraph"])
        inlines = rich["properties"]["inlines"]["items"]["anyOf"]
        assert [o["properties"]["type"]["enum"][0] for o in inlines] == [
            "text",
            "code",
            "link",
            "article",
        ]
        heading = next(o for o in options if o["properties"]["type"]["enum"] == ["heading"])
        # Gemini takes an enum on strings only; the level stays a number.
        assert heading["properties"]["level"] == {"type": "integer", "description": "One of: 2, 3."}
        serialized = json.dumps(schema)
        for banned in ("$ref", "$defs", "oneOf", "discriminator", "additionalProperties"):
            assert banned not in serialized, (model.__name__, banned)

        def enums_on_strings(node: Any) -> None:
            if isinstance(node, dict):
                if "enum" in node:
                    assert node.get("type") == "string", node
                for value in node.values():
                    enums_on_strings(value)
            elif isinstance(node, list):
                for value in node:
                    enums_on_strings(value)

        enums_on_strings(schema)


def test_gemini_response_schema_keeps_raw_one_of_and_nullable_unions() -> None:
    class Circle(BaseModel):
        kind: Literal["circle"]
        radius: float

    class Square(BaseModel):
        kind: Literal["square"]
        side: int

    class Drawing(BaseModel):
        shapes: list[Annotated[Circle | Square, Field(discriminator="kind")]]
        focus: Circle | Square | None = Field(default=None, description="The highlighted shape")

    raw = Drawing.model_json_schema()
    assert "oneOf" in raw["properties"]["shapes"]["items"]
    circle = {
        "type": "object",
        "properties": {
            "kind": {"type": "string", "enum": ["circle"]},
            "radius": {"type": "number"},
        },
        "required": ["kind", "radius"],
        "propertyOrdering": ["kind", "radius"],
    }
    square = {
        "type": "object",
        "properties": {"kind": {"type": "string", "enum": ["square"]}, "side": {"type": "integer"}},
        "required": ["kind", "side"],
        "propertyOrdering": ["kind", "side"],
    }
    assert gemini_response_schema(Drawing) == {
        "type": "object",
        "properties": {
            "shapes": {"type": "array", "items": {"anyOf": [circle, square]}},
            "focus": {
                "anyOf": [circle, square],
                "nullable": True,
                "description": "The highlighted shape",
            },
        },
        "required": ["shapes"],
        "propertyOrdering": ["shapes", "focus"],
    }


def _news_document(summary: str) -> dict[str, Any]:
    return {
        "title": "A model release",
        "description": "What changed and who it affects.",
        "hero": None,
        "blocks": [
            {"type": "summary", "items": [summary, "Second point."]},
            {"type": "heading", "text": "What happened", "level": 2},
            {"type": "paragraph", "text": "A company released a model."},
            {
                "type": "rich_paragraph",
                "inlines": [
                    {"type": "text", "text": "Read "},
                    {"type": "link", "text": "the announcement", "url": "https://example.com/n"},
                ],
            },
            {"type": "list", "items": ["One", "Two"], "ordered": False},
            {
                "type": "table",
                "header": ["Item", "Before", "After"],
                "rows": [["Context", "8k", "32k"]],
                "caption": "",
            },
            {"type": "heading", "text": "Details", "level": 3},
            {"type": "callout", "tone": "info", "title": "", "text": "Check the source."},
            {"type": "code", "language": "bash", "label": "Install", "code": "pip install x"},
            {"type": "link", "text": "Source", "url": "https://example.com/n"},
            {
                "type": "faq",
                "items": [
                    {"question": "What is new?", "answer": "A model."},
                    {"question": "Who is affected?", "answer": "Developers."},
                ],
            },
        ],
        "sources": [{"title": "Announcement", "url": "https://example.com/n", "checked_on": None}],
    }


def _gemini_body(text: str) -> dict[str, Any]:
    return {
        "candidates": [{"content": {"parts": [{"text": text}]}, "finishReason": "STOP"}],
        "usageMetadata": {"promptTokenCount": 120, "candidatesTokenCount": 80},
    }


@pytest.mark.asyncio
async def test_a_gemini_news_stage_sends_every_block_and_parses_the_reply() -> None:
    """The news path end to end on a fake transport: schema out, repair round, document in."""
    from app.hotspots.ai_search import GeminiResearchProvider
    from app.news_automation.schemas import LocalizedDocument

    replies = [
        # A summary item over its 300-character limit: the repair round must fix it.
        json.dumps({"document": _news_document("x" * 301)}),
        json.dumps({"document": _news_document("First point.")}),
    ]
    sent: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(200, json=_gemini_body(replies[len(sent) - 1]))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        provider = GeminiResearchProvider(
            "https://gemini.example", "secret", "gemini-test", 10, 32_000, client
        )
        result, usage = await provider.structured(
            LocalizedDocument, "news_translation", "Translate.", {"locale": "en"}
        )

    assert len(sent) == 2
    schemas = [body["generationConfig"]["responseSchema"] for body in sent]
    assert schemas[0] == schemas[1] == gemini_response_schema(LocalizedDocument)
    assert {o["properties"]["type"]["enum"][0] for o in _block_options(schemas[0])} == (
        _guide_block_types()
    )
    retry = sent[1]["contents"][0]["parts"][0]["text"]
    assert "Repair the previous invalid JSON" in retry
    assert "document.blocks.0.summary.items.0" in retry
    assert [block.type for block in result.document.blocks] == [
        "summary",
        "heading",
        "paragraph",
        "rich_paragraph",
        "list",
        "table",
        "heading",
        "callout",
        "code",
        "link",
        "faq",
    ]
    assert result.document.blocks[6].model_dump()["level"] == 3
    assert usage == {"input_tokens": 240, "output_tokens": 160}


@pytest.mark.asyncio
async def test_other_providers_still_receive_the_news_schema_unchanged() -> None:
    """OpenAI, MiniMax and Claude never see the Gemini conversion: the schema each one is
    sent equals the one taken before any Gemini schema was built, byte for byte."""
    from app.hotspots.ai_search import AnthropicResearchProvider, ResponsesResearchProvider

    sent: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(500)

    for model in _news_replies():
        before = json.dumps(model.model_json_schema(), ensure_ascii=False)
        before_prompt = schema_instructions(model)
        gemini_response_schema(model)
        sent.clear()
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            providers: list[Any] = [
                ResponsesResearchProvider("openai", "https://o.example", "k", "m", 10, 100, client),
                ResponsesResearchProvider(
                    "minimax", "https://m.example", "k", "m", 10, 100, client
                ),
                AnthropicResearchProvider("https://a.example", "k", "m", 10, 100, client),
            ]
            for provider in providers:
                with pytest.raises(httpx.HTTPStatusError):
                    await provider.structured(model, "news", "Write.", {"x": 1})

        openai, minimax, anthropic = sent
        for body in (openai, minimax):
            assert json.dumps(body["text"]["format"]["schema"], ensure_ascii=False) == before
        assert json.dumps(anthropic["output_config"]["format"]["schema"], ensure_ascii=False) == (
            before
        )
        assert minimax["instructions"].endswith(before_prompt)
        assert schema_instructions(model) == before_prompt
        # They keep the reference form with every block as its own definition.
        assert '"$ref": "#/$defs/FaqBlock"' in before and "propertyOrdering" not in before
