import json

import pytest
from pydantic import BaseModel

from app.ai.structured_output import (
    anthropic_output_text,
    ensure_response_completed,
    extract_json_document,
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


def test_schema_instructions_embed_the_schema_and_forbid_fences() -> None:
    class Plan(BaseModel):
        article_queries: list[str]

    text = schema_instructions(Plan)
    assert "article_queries" in text
    assert "code fences" in text
