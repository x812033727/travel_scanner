"""Tests for IndexNow instant indexing notifications and publication hooks."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import httpx
import pytest

from app.guides import indexnow
from app.guides.models import GuideArticle, GuideArticleLocale, GuideArticleRevision
from tests import test_guides as guides

database = guides.database
actor = guides.actor


def test_valid_key_and_public_url_formatting() -> None:
    assert indexnow.valid_key(None) is None
    assert indexnow.valid_key("short") is None
    assert indexnow.valid_key("has space 12345") is None
    assert indexnow.valid_key("  abcd1234efgh5678  ") == "abcd1234efgh5678"

    assert (
        indexnow.guide_public_url("https://mokaair.com/", "zh-TW", "life", "ai-update")
        == "https://mokaair.com/zh-TW/life/ai-update"
    )
    assert (
        indexnow.guide_public_url("https://mokaair.com", "en", "howto", "narita-to-tokyo")
        == "https://mokaair.com/en/guides/howto/narita-to-tokyo"
    )
    assert (
        indexnow.guide_public_url("https://mokaair.com", "ja", "intel", "fare-alert")
        == "https://mokaair.com/ja/guides/intel/fare-alert"
    )


async def test_notify_urls_skips_cleanly_when_unconfigured_or_non_https() -> None:
    res_no_key = await indexnow.notify_urls(
        ["https://mokaair.com/zh-TW/life/demo"], key="", site_url="https://mokaair.com"
    )
    assert res_no_key.accepted is False
    assert res_no_key.skipped_reason == "key_unconfigured"

    res_http = await indexnow.notify_urls(
        ["http://localhost:3000/zh-TW/life/demo"],
        key="abcd1234efgh5678",
        site_url="http://localhost:3000",
    )
    assert res_http.accepted is False
    assert res_http.skipped_reason == "non_https_origin"

    res_bad_endpoint = await indexnow.notify_urls(
        ["https://mokaair.com/zh-TW/life/demo"],
        key="abcd1234efgh5678",
        site_url="https://mokaair.com",
        endpoint="https://evil.example/indexnow",
    )
    assert res_bad_endpoint.accepted is False
    assert res_bad_endpoint.skipped_reason == "invalid_endpoint"


async def test_notify_urls_submits_deduped_same_host_payload_and_handles_errors() -> None:
    captured: list[dict[str, object]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(json.loads(request.content.decode("utf-8")))
        return httpx.Response(202)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await indexnow.notify_urls(
            [
                "https://mokaair.com/zh-TW/life/story-a",
                "https://mokaair.com/zh-TW/life/story-a",
                "https://other.example/zh-TW/life/foreign",
                "https://mokaair.com/en/guides/howto/story-b",
            ],
            key="abcd1234efgh5678",
            site_url="https://mokaair.com",
            client=client,
        )

    assert result == indexnow.IndexNowResult(submitted=2, accepted=True, status_code=202)
    assert captured == [
        {
            "host": "mokaair.com",
            "key": "abcd1234efgh5678",
            "keyLocation": "https://mokaair.com/indexnow-key.txt",
            "urlList": [
                "https://mokaair.com/zh-TW/life/story-a",
                "https://mokaair.com/en/guides/howto/story-b",
            ],
        }
    ]

    def failing_handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(429)

    async with httpx.AsyncClient(transport=httpx.MockTransport(failing_handler)) as client:
        rejected = await indexnow.notify_urls(
            ["https://mokaair.com/zh-TW/life/story-a"],
            key="abcd1234efgh5678",
            site_url="https://mokaair.com",
            client=client,
        )
    assert rejected.accepted is False
    assert rejected.status_code == 429
    assert rejected.error == "HTTP 429"


async def test_recent_published_urls_returns_only_live_revisions_in_window(
    database,
) -> None:
    now = datetime.now(UTC)
    async with database() as session:
        fresh = GuideArticle(kind="life", slug="fresh-story", is_active=True)
        stale = GuideArticle(kind="howto", slug="stale-story", is_active=True)
        hidden = GuideArticle(kind="life", slug="hidden-story", is_active=False)
        session.add_all([fresh, stale, hidden])
        await session.flush()

        for article, locale, rev_time in [
            (fresh, "zh-TW", now - timedelta(hours=2)),
            (stale, "en", now - timedelta(hours=72)),
            (hidden, "zh-TW", now - timedelta(hours=1)),
        ]:
            loc = GuideArticleLocale(
                article_id=article.id,
                locale=locale,
                version=1,
                published_version=1,
                published_at=rev_time,
                draft_json={"title": article.slug, "description": "d", "blocks": [], "sources": []},
            )
            session.add(loc)
            await session.flush()
            session.add(
                GuideArticleRevision(
                    article_locale_id=loc.id,
                    version=1,
                    action="published",
                    document_json=loc.draft_json,
                    created_at=rev_time,
                )
            )
        await session.commit()

        urls = await indexnow.recent_published_urls(
            session, since_hours=48, site_url="https://mokaair.com"
        )
        assert urls == ["https://mokaair.com/zh-TW/life/fresh-story"]


async def test_admin_publish_triggers_indexnow_notification(
    database, actor, monkeypatch: pytest.MonkeyPatch
) -> None:
    spy = AsyncMock(
        return_value=indexnow.IndexNowResult(submitted=1, accepted=True, status_code=202)
    )
    monkeypatch.setattr(indexnow, "notify_guide_change", spy)

    async with guides.client(guides.make_app(database, actor)) as api:
        created = await guides.create_article(
            api,
            slug="indexnow-hook-test",
            kind="life",
            topics=["ai"],
            destination_id=None,
        )
        res = await guides.publish(api, created["id"], "zh-TW", created["version"])
        assert res.status_code == 200, res.text

    spy.assert_awaited_once_with("life", "indexnow-hook-test", ["zh-TW"])
