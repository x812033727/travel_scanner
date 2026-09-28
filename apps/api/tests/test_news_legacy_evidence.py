from __future__ import annotations

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.news_automation.feeds import extract_article
from app.news_automation.models import NewsEvidence, NewsSource
from app.news_automation.policy import content_fingerprint
from app.news_automation.schemas import FetchResult
from app.news_automation.validation import revalidate_evidence


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        b'<main><nav>Newsroom navigation</nav><img src="seal.png"/>'
        b"<p>Old story.</p></main>",
        b'<main><p>Retained lead.</p><img src="cover.png"/>'
        b"<p>Old story.</p></main>",
        b'<main><nav>Old story. Extra navigation</nav><img src="seal.png"/>'
        b"<p>Old story.</p></main>",
    ],
)
async def test_legacy_hash_cannot_authorize_story_text_it_never_covered(body: bytes) -> None:
    source = NewsSource(
        name="Official",
        url="https://example.com/feed",
        format="rss",
        role="evidence",
        vertical="ai",
        is_first_party=True,
        enabled=True,
    )
    url = "https://example.com/release"
    _, legacy_text, _ = extract_article(body, url, legacy=True)
    evidence = NewsEvidence(
        candidate_id=uuid4(),
        role="evidence",
        is_first_party=True,
        url=url,
        title="Official story",
        content_hash=content_fingerprint(legacy_text),
        excerpt=legacy_text,
    )
    session = AsyncMock()
    session.scalars.return_value = [source]
    fetcher = AsyncMock()
    # Both the actual edit and the previously unrecorded story require fresh evidence.
    # Navigation or a retained lead matching the old hash cannot authenticate the rest.
    changed = body.replace(b"<p>Old story.</p>", b"<p>New story.</p>")
    for current in (changed, body):
        _, current_legacy, _ = extract_article(current, url, legacy=True)
        assert content_fingerprint(current_legacy) == evidence.content_hash
        fetcher.fetch.return_value = FetchResult(
            url=url, status_code=200, content_type="text/html", body=current
        )
        assert await revalidate_evidence(session, [evidence], fetcher=fetcher) == (
            False,
            [f"source_content_changed:{url}"],
        )
        assert evidence.retrieved_at is None
