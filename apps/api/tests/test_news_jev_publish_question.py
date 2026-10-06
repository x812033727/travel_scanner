"""What the news publish question puts on the wire to Jev (task 2026-10-06-news-jev-publish-...).

The act threshold was tuned on answers to the bare statement: the criteria used to travel under
keys Jev ignores. These tests pin that the publish question still goes out without criteria,
with the statement unchanged, while the duplicate question keeps its documented criteria.
"""

from __future__ import annotations

import json
from typing import Any, cast

import httpx
import pytest

from app.ai.jev import JevClient
from app.config import get_settings
from app.news_automation import ai
from app.news_automation.models import NewsAutomationSettings, NewsCandidate
from tests.test_news_pipeline import JEV_PUBLISH_ANSWER, news_document

STATEMENT = (
    "This localized news article is accurate, sufficiently important, "
    "fully supported by its listed sources, safe for general readers, "
    "not investment or purchasing advice, and ready to publish."
)


def recording_jev(monkeypatch: pytest.MonkeyPatch, answer: dict[str, Any]) -> list[dict[str, Any]]:
    """The real JevClient over a fake transport; returns each request body it sent."""
    bodies: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        bodies.append(json.loads(request.content))
        return httpx.Response(200, json=answer)

    client = JevClient(
        "jev-test-key",
        "https://jev.example/v1",
        "jev-test",
        10.0,
        client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )

    async def quota(*_args: Any) -> bool:
        return True

    monkeypatch.setattr(ai, "jev_client", lambda _environment: client)
    monkeypatch.setattr(ai, "consume_jev_call", quota)
    return bodies


@pytest.mark.asyncio
async def test_the_publish_question_goes_to_jev_without_criteria(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bodies = recording_jev(monkeypatch, JEV_PUBLISH_ANSWER)
    decisions = await ai.jev_assessments(
        cast(Any, None),
        get_settings(),
        NewsAutomationSettings(jev_act_confidence=0.5),
        NewsCandidate(vertical="ai", evidence_hash="e" * 64),
        {"zh-TW": news_document("Model release")},
        locales=("zh-TW",),
    )
    assert len(bodies) == 1
    question = bodies[0]["questions"]["publish"]
    assert question == {"type": "noul", "instructions": STATEMENT}
    assert bodies[0]["state"]["evidence_sha256"] == "e" * 64
    assert [decision.tier for decision in decisions] == ["act"]


@pytest.mark.asyncio
async def test_the_duplicate_question_keeps_its_documented_criteria(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bodies = recording_jev(
        monkeypatch, {"answers": {"duplicate": {"type": "noul", "noul": 0.1}}, "usage": {}}
    )
    await ai.jev_duplicate_check(
        cast(Any, None),
        get_settings(),
        "Introducing GPT-6.1 Sol",
        "GPT-6.1 Sol is the latest model family in the GPT-6 series.",
        ["GPT-6 Sol and Luna launch: API price cuts, available in Codex"],
    )
    criteria = bodies[0]["questions"]["duplicate"]["criteria"]
    assert set(criteria) == {"true", "false"}
