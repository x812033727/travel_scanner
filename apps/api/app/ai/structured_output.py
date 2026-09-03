"""Helpers for reading JSON documents out of LLM responses.

Providers with schema-enforced output (OpenAI, Anthropic) return clean JSON,
but reasoning models such as MiniMax M3 ignore ``text.format`` and wrap the
JSON in a Markdown fence or surround it with prose. These helpers keep every
structured call tolerant of that without weakening validation: whatever is
extracted still has to satisfy the pydantic schema of the caller.
"""

from __future__ import annotations

import json
import re
from typing import Any

from pydantic import BaseModel

_FENCED_BLOCK = re.compile(r"```(?:[A-Za-z0-9_-]+)?[ \t]*\r?\n?(.*?)```", re.DOTALL)


def extract_json_document(text: str) -> str:
    """Return the JSON document embedded in ``text``.

    Handles a closed Markdown fence anywhere in the text, an unterminated fence
    at the start, and prose before or after a top-level object.
    """
    stripped = text.strip()
    fenced = _FENCED_BLOCK.search(stripped)
    if fenced:
        return fenced.group(1).strip()
    if stripped.startswith("```"):
        first_break = stripped.find("\n")
        if first_break != -1:
            stripped = stripped[first_break + 1 :].strip()
            if stripped.endswith("```"):
                stripped = stripped[:-3].strip()
    if stripped[:1] in {"{", "["}:
        return stripped
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end > start:
        return stripped[start : end + 1]
    return stripped


def responses_output_text(body: dict[str, Any]) -> str:
    """Read the text of a Responses API body (REST shape or SDK convenience field).

    Reasoning items carry no ``content`` and are skipped naturally.
    """
    direct = body.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct
    texts: list[str] = []
    for output in body.get("output") or []:
        if not isinstance(output, dict):
            continue
        for item in output.get("content") or []:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "refusal":
                raise ValueError("AI 拒絕回應")
            text = item.get("text")
            if item.get("type") == "output_text" and isinstance(text, str):
                texts.append(text)
    joined = "".join(texts).strip()
    if not joined:
        raise ValueError("AI 沒有回傳內容")
    return joined


def ensure_response_completed(body: dict[str, Any]) -> None:
    """Raise when a Responses API body was cut short (for example by max_output_tokens)."""
    status = body.get("status")
    if status in {None, "completed"}:
        return
    details = body.get("incomplete_details")
    reason = details.get("reason") if isinstance(details, dict) else None
    raise ValueError(f"AI 回應未完成 ({reason or status})")


def anthropic_output_text(body: dict[str, Any]) -> str:
    """Join the text blocks of a Messages API body, refusing truncated answers."""
    if body.get("stop_reason") == "max_tokens":
        raise ValueError("AI 回應未完成 (max_tokens)")
    texts = [
        str(item.get("text"))
        for item in body.get("content") or []
        if isinstance(item, dict) and item.get("type") == "text" and item.get("text")
    ]
    joined = "".join(texts).strip()
    if not joined:
        raise ValueError("AI 沒有回傳內容")
    return joined


def schema_instructions(schema: type[BaseModel]) -> str:
    """Prompt text embedding the JSON Schema, for providers that ignore ``text.format``."""
    return (
        "Respond with exactly one JSON object that matches this JSON Schema. "
        "Do not wrap it in Markdown code fences and do not add commentary or reasoning text.\n"
        + json.dumps(schema.model_json_schema(), ensure_ascii=False)
    )
