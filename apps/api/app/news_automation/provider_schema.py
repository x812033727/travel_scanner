"""JSON Schemas that every news-stage provider accepts.

The news stages ask a model for a whole ``GuideDocument``. Its pydantic schema uses
optional properties, a ``oneOf`` block union with a ``discriminator``, string and
number bounds and ``maxItems``. Over raw HTTP, OpenAI strict Structured Outputs wants
every property listed in ``required`` and rejects ``oneOf``; Anthropic structured
outputs rejects ``minLength``/``maxLength``, ``minimum``/``maximum`` and complex array
bounds. Their SDKs rewrite schemas before sending them; the shared adapters in
``app.hotspots.ai_search`` post ``model_json_schema()`` as it is.

``ProviderReply`` models therefore publish a reduced schema, which is also the one the
adapters embed in the system prompt. Nothing is lost: pydantic validates the reply
against the full model afterwards, and every dropped bound is appended to the
field's description so the model still reads it.
"""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, ConfigDict

# Bounds neither provider enforces through the schema. Pydantic still does.
MOVED_TO_DESCRIPTION = frozenset(
    {
        "minLength",
        "maxLength",
        "pattern",
        "minimum",
        "maximum",
        "exclusiveMinimum",
        "exclusiveMaximum",
        "multipleOf",
        "minItems",
        "maxItems",
        "uniqueItems",
    }
)
# Annotations that carry no constraint once every property is required.
DROPPED = frozenset({"default", "title", "discriminator", "examples"})
# String formats both providers document.
PORTABLE_FORMATS = frozenset({"date", "date-time", "time"})


def portable_json_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Rewrite a pydantic JSON Schema into the subset both strict providers accept."""

    def properties(values: dict[str, Any]) -> dict[str, Any]:
        return {name: convert(child) for name, child in values.items()}

    def convert(node: Any) -> Any:
        if isinstance(node, list):
            return [convert(item) for item in node]
        if not isinstance(node, dict):
            return node
        if "$ref" in node:
            # OpenAI rejects sibling keywords beside a reference.
            return {"$ref": node["$ref"]}
        converted: dict[str, Any] = {}
        notes: list[str] = []
        for key, value in node.items():
            if key in DROPPED:
                continue
            if key in MOVED_TO_DESCRIPTION or (key == "format" and value not in PORTABLE_FORMATS):
                notes.append(f"{key}={json.dumps(value, ensure_ascii=False)}")
            elif key == "oneOf":
                converted["anyOf"] = convert(value)
            elif key == "const":
                converted["enum"] = [value]
            elif key in {"properties", "$defs"}:
                converted[key] = properties(value)
            else:
                converted[key] = convert(value)
        if node.get("type") == "object" or "properties" in node:
            if node.get("additionalProperties", False) is not False:
                raise ValueError("an open or map-typed object has no portable schema")
            converted["additionalProperties"] = False
            converted["required"] = list(converted.get("properties", {}))
        if notes:
            description = str(converted.get("description") or "").strip()
            suffix = "Constraints: " + ", ".join(notes) + "."
            converted["description"] = f"{description} {suffix}".strip()
        return converted

    result = convert(schema)
    assert isinstance(result, dict)
    return result


class ProviderReply(BaseModel):
    """A structured reply from a writing or checking model.

    Validation is the ordinary pydantic validation of the subclass; only the schema
    handed to providers changes.
    """

    model_config = ConfigDict(extra="forbid")

    @classmethod
    def model_json_schema(cls, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return portable_json_schema(super().model_json_schema(*args, **kwargs))
