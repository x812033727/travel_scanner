from __future__ import annotations

from datetime import UTC, date, datetime
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import BaseModel

from app.config import get_settings
from app.guides.schemas import GuideDocument
from app.news_automation import ai
from app.news_automation.models import NewsAutomationSettings, NewsEvidence
from app.news_automation.policy import document_fingerprint
from app.news_automation.schemas import VerificationResult

SOURCE_URL = "https://official.example/news/release"
SUPPORTED_CLAIM = "According to the announcement, 950 agents worked for 21 hours."


def verification_story(topic_url: str) -> tuple[GuideDocument, list[NewsEvidence]]:
    document = GuideDocument.model_validate(
        {
            "title": "An attributed research announcement",
            "description": "The announcement describes its research results.",
            "hero": {
                "src": "/guides/news-assets/research-hero.webp",
                "alt": "Site-generated research illustration",
                "width": 1200,
                "height": 630,
            },
            "blocks": [
                {"type": "paragraph", "text": SUPPORTED_CLAIM},
                {"type": "link", "text": "Read the announcement", "url": SOURCE_URL},
                {
                    "type": "image",
                    "src": "/guides/news-assets/research-diagram.svg",
                    "alt": "Site-generated diagram",
                    "width": 1200,
                    "height": 675,
                },
                {"type": "link", "text": "Browse the latest topic news", "url": topic_url},
            ],
            "sources": [{"title": "Research announcement", "url": SOURCE_URL}],
        }
    )
    evidence = [
        NewsEvidence(
            role="evidence",
            is_first_party=True,
            url=SOURCE_URL,
            title="Research announcement",
            retrieved_at=datetime(2026, 10, 10, tzinfo=UTC),
            source_date=date(2026, 10, 8),
            content_hash="e" * 64,
            excerpt=SUPPORTED_CLAIM,
        )
    ]
    return document, evidence


def recording_verifier(monkeypatch: pytest.MonkeyPatch) -> tuple[Any, list[dict[str, Any]]]:
    """Reject unsupported links/claims like the production hold, without a model request."""
    payloads: list[dict[str, Any]] = []

    async def structured(
        schema: type[BaseModel],
        schema_name: str,
        instructions: str,
        payload: dict[str, Any],
    ) -> tuple[VerificationResult, dict[str, int]]:
        assert schema is VerificationResult
        assert schema_name == "news_verification"
        assert instructions == ai.VERIFIER_INSTRUCTIONS
        payloads.append(payload)
        supported_urls = {row["url"] for row in payload["evidence"]}
        excerpts = {row["excerpt"] for row in payload["evidence"]}
        unsupported = [
            block
            for block in payload["article"]["blocks"]
            if (block["type"] == "link" and block["url"] not in supported_urls)
            or (block["type"] == "paragraph" and block["text"] not in excerpts)
        ]
        if unsupported:
            corrected = {
                **payload["article"],
                "blocks": [
                    block for block in payload["article"]["blocks"] if block not in unsupported
                ],
            }
            result = VerificationResult(
                verdict="revise",
                issues=["Unsupported authored link or claim"],
                corrected_document=GuideDocument.model_validate(corrected),
            )
        else:
            result = VerificationResult(verdict="pass")
        return result, {"input_tokens": 12, "output_tokens": 3}

    provider = SimpleNamespace(
        model="offline-verifier",
        structured=AsyncMock(side_effect=structured),
        close=AsyncMock(),
    )
    monkeypatch.setattr(ai, "research_provider", Mock(return_value=provider))
    return provider, payloads


@pytest.mark.asyncio
@pytest.mark.parametrize("locale", ["zh-TW", "zh-CN", "en", "ja", "ko"])
@pytest.mark.parametrize("topic", ["ai-news", "tech-news", "crypto"])
async def test_verification_does_not_mistake_site_navigation_for_an_unsupported_news_claim(
    monkeypatch: pytest.MonkeyPatch, locale: str, topic: str
) -> None:
    document, evidence = verification_story(f"https://mokaair.com/{locale}/life/topics/{topic}")
    before = document.model_dump(mode="json")
    fingerprint = document_fingerprint(document)
    provider, payloads = recording_verifier(monkeypatch)

    result, usage, model = await ai.verify_article(
        get_settings(),
        NewsAutomationSettings(verifier_provider="openai", verifier_model="offline-verifier"),
        document,
        evidence,
    )

    assert result.verdict == "pass"
    article = payloads[0]["article"]
    assert article["blocks"] == before["blocks"][:2]
    assert article["hero"] is None
    assert article["title"] == before["title"]
    assert article["description"] == before["description"]
    assert article["sources"] == before["sources"]
    assert payloads[0]["evidence"][0]["url"] == SOURCE_URL
    assert payloads[0]["evidence"][0]["excerpt"] == SUPPORTED_CLAIM
    assert payloads[0]["evidence"][0]["content_sha256"] == "e" * 64
    assert usage == {"input_tokens": 12, "output_tokens": 3}
    assert model == "offline-verifier"
    provider.close.assert_awaited_once()
    # The public document still carries navigation/artwork and keeps its verification identity.
    assert document.model_dump(mode="json") == before
    assert document_fingerprint(document) == fingerprint


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "authored_url",
    [
        "https://unsupported.example/claimed-release",
        "https://mokaair.com/zh-TW/life/topics/ai-news/unsupported-claim",
    ],
)
async def test_verification_still_receives_and_rejects_unsupported_authored_links(
    monkeypatch: pytest.MonkeyPatch, authored_url: str
) -> None:
    document, evidence = verification_story("https://mokaair.com/zh-TW/life/topics/ai-news")
    encoded = document.model_dump(mode="json")
    authored = {"type": "link", "text": "An authored claim", "url": authored_url}
    encoded["blocks"].insert(1, authored)
    document = GuideDocument.model_validate(encoded)
    _, payloads = recording_verifier(monkeypatch)

    result, _, _ = await ai.verify_article(
        get_settings(), NewsAutomationSettings(verifier_provider="openai"), document, evidence
    )

    assert result.verdict == "revise"
    assert authored in payloads[0]["article"]["blocks"]
    assert document.model_dump(mode="json") == encoded


@pytest.mark.asyncio
async def test_verification_still_receives_and_rejects_a_real_unsupported_claim(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document, evidence = verification_story("https://mokaair.com/zh-TW/life/topics/ai-news")
    encoded = document.model_dump(mode="json")
    authored = {"type": "paragraph", "text": "The tool is already proven safe for medical use."}
    encoded["blocks"].insert(1, authored)
    document = GuideDocument.model_validate(encoded)
    fingerprint = document_fingerprint(document)
    _, payloads = recording_verifier(monkeypatch)

    result, _, _ = await ai.verify_article(
        get_settings(), NewsAutomationSettings(verifier_provider="openai"), document, evidence
    )

    assert result.verdict == "revise"
    assert authored in payloads[0]["article"]["blocks"]
    assert document.model_dump(mode="json") == encoded
    assert document_fingerprint(document) == fingerprint
