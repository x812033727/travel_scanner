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


def gemini_output_text(body: dict[str, Any]) -> str:
    """Join the text parts of a generateContent body, refusing blocked or truncated answers.

    A truncated answer is the failure mode that matters most here: MAX_TOKENS on a
    thinking model yields valid-looking JSON that stops mid-array, which would import as
    a short list rather than an error.
    """
    feedback = body.get("promptFeedback")
    if isinstance(feedback, dict) and feedback.get("blockReason"):
        raise ValueError(f"AI 拒絕回應（{feedback['blockReason']}）")
    entries = body.get("candidates")
    first = entries[0] if isinstance(entries, list) and entries else None
    if not isinstance(first, dict):
        raise ValueError("AI 沒有回傳內容")
    reason = first.get("finishReason")
    if reason not in (None, "STOP"):
        raise ValueError(f"AI 回應未完成（{reason}）")
    content = first.get("content")
    parts = content.get("parts") if isinstance(content, dict) else None
    text = "".join(
        str(part.get("text") or "")
        for part in (parts if isinstance(parts, list) else [])
        if isinstance(part, dict)
    ).strip()
    if not text:
        raise ValueError("AI 沒有回傳內容")
    return text


# Keys Gemini's OpenAPI-subset ``responseSchema`` understands. Everything else from a
# pydantic JSON Schema (``$defs``, ``additionalProperties``, ``title``, ``default``,
# ``pattern``, ``maxItems``, ``format``…) either is rejected with a bare
# INVALID_ARGUMENT or is silently ignored, so it is dropped and left to pydantic,
# which still validates the reply afterwards.
_GEMINI_SCALAR_KEYS = ("type", "description", "enum", "nullable")


def gemini_response_schema(model_type: type[BaseModel]) -> dict[str, Any]:
    """Reduce a pydantic model's JSON Schema to the subset Gemini accepts as a schema."""
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
        converted = {key: node[key] for key in _GEMINI_SCALAR_KEYS if key in node}
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
