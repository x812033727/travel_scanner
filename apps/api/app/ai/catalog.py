"""Server-curated catalog of the AI models this code base can drive.

The admin page renders model ids as dropdowns from this list so nobody has to type
``gemini-3.8-flash`` by hand, and the same list records which code path each model
can serve: the itinerary planner, the trip parser and the guide search post Responses
JSON Schema requests (OpenAI, MiniMax) or Anthropic structured output; the hotspot
candidate generator sends a Gemini ``responseSchema``; the article search sends a
Gemini ``google_search`` tool without a schema. An id outside the catalog is still
accepted when it matches ``MODEL_ID_PATTERN`` (the admin "custom" option), because
vendors ship models faster than this file changes.

Keep this module free of ``app.*`` imports: ``app.admin.service`` and
``app.hotspots.ai_search`` both import it.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

Vendor = Literal["openai", "anthropic", "minimax", "gemini"]
Capability = Literal[
    "responses_json_schema_strict",
    "anthropic_structured_output",
    "gemini_structured",
    "gemini_grounded",
]
ModelStatus = Literal["stable", "preview", "retired"]

# Security audit R2-25: the Gemini model id is interpolated into the request path, so
# a stored id is limited to the characters a model name can contain.
MODEL_ID_PATTERN = re.compile(r"[A-Za-z0-9._:-]{1,128}")


@dataclass(frozen=True)
class ModelEntry:
    id: str
    label: str
    capabilities: frozenset[Capability]
    note: str | None = None
    status: ModelStatus = "stable"


_RESPONSES: frozenset[Capability] = frozenset({"responses_json_schema_strict"})
_ANTHROPIC: frozenset[Capability] = frozenset({"anthropic_structured_output"})
_GEMINI: frozenset[Capability] = frozenset({"gemini_structured", "gemini_grounded"})

MODEL_CATALOG: dict[Vendor, tuple[ModelEntry, ...]] = {
    "openai": (
        ModelEntry(
            "gpt-6-astra",
            "GPT-6 Astra",
            _RESPONSES,
            "OpenAI 最強模型，成本最高；適合完整行程規劃。",
        ),
        ModelEntry(
            "gpt-5.6-sol",
            "GPT-5.6 Sol",
            _RESPONSES,
            "GPT-5.6 旗艦（別名 gpt-5.6），適合複雜任務。",
        ),
        ModelEntry(
            "gpt-5.6-terra",
            "GPT-5.6 Terra",
            _RESPONSES,
            "目前預設；智慧與成本的平衡。",
        ),
        ModelEntry(
            "gpt-5.6-luna",
            "GPT-5.6 Luna",
            _RESPONSES,
            "最省成本；適合搜尋詞規劃與評選。",
        ),
    ),
    "anthropic": (
        ModelEntry(
            "claude-opus-5",
            "Claude Opus 5",
            _ANTHROPIC,
            "推理最強、成本最高；適合完整行程規劃。",
        ),
        ModelEntry(
            "claude-sonnet-5",
            "Claude Sonnet 5",
            _ANTHROPIC,
            "目前預設；品質與成本的平衡。",
        ),
        ModelEntry(
            "claude-haiku-4-5-20251001",
            "Claude Haiku 4.5",
            _ANTHROPIC,
            "最快、最便宜；適合搜尋詞規劃與評選。",
        ),
    ),
    "minimax": (
        ModelEntry(
            "MiniMax-M3",
            "MiniMax M3",
            _RESPONSES,
            "目前預設；推理模型，思考 tokens 會計入輸出上限，請保留足夠的最大輸出 tokens。",
        ),
        ModelEntry("MiniMax-M2.7", "MiniMax M2.7", _RESPONSES, "前一代旗艦。"),
        ModelEntry(
            "MiniMax-M2.7-highspeed",
            "MiniMax M2.7 Highspeed",
            _RESPONSES,
            "M2.7 的高速版本，回應較快。",
        ),
        ModelEntry("MiniMax-M2.5", "MiniMax M2.5", _RESPONSES, "較舊、較便宜。"),
    ),
    "gemini": (
        ModelEntry(
            "gemini-3.8-flash",
            "Gemini 3.8 Flash",
            _GEMINI,
            "目前預設；能產生景點候選名單，接地列出文章來源時較弱。",
        ),
        ModelEntry("gemini-3.7-flash", "Gemini 3.7 Flash", _GEMINI, "Flash 級，特性同 3.8。"),
        ModelEntry("gemini-3.6-flash", "Gemini 3.6 Flash", _GEMINI, "Flash 級，特性同 3.8。"),
        ModelEntry("gemini-3.5-flash", "Gemini 3.5 Flash", _GEMINI, "前一版預設。"),
        ModelEntry(
            "gemini-3.5-flash-lite",
            "Gemini 3.5 Flash-Lite",
            _GEMINI,
            "最便宜；只建議用在候選名單產生。",
        ),
        ModelEntry(
            "gemini-3.1-pro-preview",
            "Gemini 3.1 Pro Preview",
            _GEMINI,
            "Pro 級預覽版，接地列來源較穩，但可能隨時下線。",
            "preview",
        ),
        ModelEntry(
            "gemini-2.5-pro",
            "Gemini 2.5 Pro",
            _GEMINI,
            "新申請的金鑰無法使用（404）；只保留給舊金鑰。",
            "retired",
        ),
    ),
}

# Settings field -> (vendor, capability the code path behind that field needs).
MODEL_FIELDS: dict[str, tuple[Vendor, Capability]] = {
    "openai_model": ("openai", "responses_json_schema_strict"),
    "anthropic_model": ("anthropic", "anthropic_structured_output"),
    "minimax_model": ("minimax", "responses_json_schema_strict"),
    "hotspot_guide_ai_openai_model": ("openai", "responses_json_schema_strict"),
    "hotspot_guide_ai_anthropic_model": ("anthropic", "anthropic_structured_output"),
    "hotspot_guide_ai_minimax_model": ("minimax", "responses_json_schema_strict"),
    # The same field also drives the schema-bound candidate generator; every Gemini
    # entry carries both capabilities, so the grounded one is the stricter filter.
    "hotspot_guide_gemini_model": ("gemini", "gemini_grounded"),
}

# Empty means "use the planner's model for that vendor".
OPTIONAL_MODEL_FIELDS: frozenset[str] = frozenset(
    {
        "hotspot_guide_ai_openai_model",
        "hotspot_guide_ai_anthropic_model",
        "hotspot_guide_ai_minimax_model",
    }
)


def valid_model_id(value: str) -> bool:
    return MODEL_ID_PATTERN.fullmatch(value) is not None


def model_options(field: str) -> tuple[ModelEntry, ...]:
    """Catalog entries a model field may offer, in catalog order."""
    vendor, capability = MODEL_FIELDS[field]
    return tuple(entry for entry in MODEL_CATALOG[vendor] if capability in entry.capabilities)


def field_options(fields: Iterable[str]) -> dict[str, tuple[ModelEntry, ...]]:
    """Options for the model fields among ``fields``; other fields are left out."""
    return {field: model_options(field) for field in fields if field in MODEL_FIELDS}


def model_label(vendor: Vendor, model_id: str) -> str:
    for entry in MODEL_CATALOG[vendor]:
        if entry.id == model_id:
            return entry.label
    return model_id
