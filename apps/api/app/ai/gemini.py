"""Structured JSON calls to the Gemini API.

Kept out of ``app.hotspots`` so any future generator (food merchants, for instance) can
import it without dragging the hotspot package along. This is the ungrounded path: no
search tool, so a response schema is allowed. The grounded article search in
``app.hotspots.guides`` deliberately sends no schema, because Gemini returns empty
grounding metadata when the two are combined.
"""

from __future__ import annotations

import json
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from app.ai.structured_output import extract_json_document, gemini_output_text

TModel = TypeVar("TModel", bound=BaseModel)


class GeminiStructuredProvider:
    name = "gemini"

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        timeout_seconds: float,
        max_output_tokens: int,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.max_output_tokens = max_output_tokens
        self._external_client = client
        self._client = client or httpx.AsyncClient(timeout=timeout_seconds)

    async def close(self) -> None:
        if self._external_client is None:
            await self._client.aclose()

    async def _send(
        self,
        instructions: str,
        turns: list[dict[str, Any]],
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        response = await self._client.post(
            f"{self.base_url}/v1beta/models/{self.model}:generateContent",
            headers={"x-goog-api-key": self.api_key, "Content-Type": "application/json"},
            json={
                "system_instruction": {"parts": [{"text": instructions}]},
                "contents": turns,
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "responseSchema": schema,
                    "temperature": 0.2,
                    "maxOutputTokens": self.max_output_tokens,
                },
            },
        )
        response.raise_for_status()
        body = response.json()
        return body if isinstance(body, dict) else {}

    async def structured(
        self,
        model_type: type[TModel],
        response_schema: dict[str, Any],
        instructions: str,
        payload: dict[str, Any],
    ) -> tuple[TModel, dict[str, int]]:
        """Ask for one JSON document, repairing once if the first reply fails validation."""
        turns: list[dict[str, Any]] = [
            {"role": "user", "parts": [{"text": json.dumps(payload, ensure_ascii=False)}]}
        ]
        usage: dict[str, int] = {"input_tokens": 0, "output_tokens": 0, "thought_tokens": 0}
        previous = ""
        for attempt in range(2):
            body = await self._send(instructions, turns, response_schema)
            metadata = body.get("usageMetadata")
            if isinstance(metadata, dict):
                usage["input_tokens"] += int(metadata.get("promptTokenCount") or 0)
                usage["output_tokens"] += int(metadata.get("candidatesTokenCount") or 0)
                usage["thought_tokens"] += int(metadata.get("thoughtsTokenCount") or 0)
            document = extract_json_document(gemini_output_text(body))
            try:
                return model_type.model_validate_json(document), usage
            except ValidationError:
                if attempt == 1:
                    raise
                previous = document
                turns = [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": json.dumps(payload, ensure_ascii=False)
                                + "\nRepair the previous invalid JSON and match the schema"
                                + f" exactly: {previous}"
                            }
                        ],
                    }
                ]
        raise ValueError("Gemini structured output validation failed")
