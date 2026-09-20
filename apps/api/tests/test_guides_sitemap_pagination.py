"""The sitemap must enumerate every published language without a 1,000-row truncation."""

from __future__ import annotations

import base64
import json
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select, update

from app.guides.models import GuideArticle, GuideArticleLocale, GuideArticleRevision
from app.guides.publication import today
from app.guides.service import SITEMAP_LIMIT
from tests import test_guides as guides

database = guides.database


async def seed_articles(database, count: int) -> list[tuple[str, str]]:
    """Real publication pointers/revisions, with timestamps deliberately unlike slug order."""
    expected = []
    async with database() as session:
        for index in reversed(range((count + 4) // 5)):
            article = GuideArticle(slug=f"article-{index:04d}", kind="howto")
            session.add(article)
            await session.flush()
            for offset, locale in enumerate(("zh-TW", "ko", "en", "zh-CN", "ja")):
                if index * 5 + offset >= count:
                    continue
                stamp = datetime(2026, 9, 1, tzinfo=UTC) + timedelta(minutes=index)
                row = GuideArticleLocale(
                    article_id=article.id,
                    locale=locale,
                    draft_json=guides.document(),
                    published_version=1,
                    published_at=stamp,
                )
                session.add(row)
                await session.flush()
                session.add(
                    GuideArticleRevision(
                        article_locale_id=row.id,
                        version=1,
                        action="published",
                        document_json=guides.document(),
                        created_at=stamp + timedelta(seconds=1),
                    )
                )
                expected.append((article.slug, locale))
        await session.commit()
    return sorted(expected)


@pytest.mark.parametrize("count", [SITEMAP_LIMIT, SITEMAP_LIMIT + 5])
async def test_every_translation_survives_the_default_page_boundary(database, count) -> None:
    expected = await seed_articles(database, count)
    async with guides.client(guides.make_app(database)) as api:
        first = await api.get("/guides/sitemap")
        assert first.status_code == 200
        assert first.headers["cache-control"] == "no-store"
        page = first.json()
        assert len(page["entries"]) == SITEMAP_LIMIT
        assert (page["next_cursor"] is not None) == (count > SITEMAP_LIMIT)
        entries = page["entries"]
        if page["next_cursor"]:
            final = await api.get("/guides/sitemap", params={"cursor": page["next_cursor"]})
            assert final.status_code == 200
            assert final.json()["next_cursor"] is None
            entries += final.json()["entries"]
        assert [(row["slug"], row["locale"]) for row in entries] == expected
        assert all(row["modified_at"] > row["published_at"] for row in entries)


async def test_cursor_splits_languages_of_one_article_without_losing_siblings(database) -> None:
    expected = await seed_articles(database, 10)
    async with guides.client(guides.make_app(database)) as api:
        cursor = None
        entries = []
        page_sizes = []
        while True:
            params = {"limit": 3, **({"cursor": cursor} if cursor else {})}
            response = await api.get("/guides/sitemap", params=params)
            assert response.status_code == 200
            page = response.json()
            page_sizes.append(len(page["entries"]))
            entries.extend((row["slug"], row["locale"]) for row in page["entries"])
            cursor = page["next_cursor"]
            if cursor is None:
                break
        assert page_sizes == [3, 3, 3, 1]
        assert entries == expected
        assert len(set(entries)) == 10


async def test_each_page_excludes_hidden_expired_draft_and_withdrawn_locales(database) -> None:
    expected = await seed_articles(database, 25)
    async with database() as session:
        await session.execute(
            update(GuideArticle).where(GuideArticle.slug == "article-0000").values(is_active=False)
        )
        await session.execute(
            update(GuideArticle)
            .where(GuideArticle.slug == "article-0001")
            .values(valid_until=today() - timedelta(days=1))
        )
        # Draft and withdrawn locales both lack a public pointer. Withdrawal retains the
        # old timestamp, so filtering only by published_at would accidentally expose it.
        await session.execute(
            update(GuideArticleLocale)
            .where(GuideArticleLocale.locale == "ja")
            .values(published_version=None, published_at=None)
        )
        await session.execute(
            update(GuideArticleLocale)
            .where(GuideArticleLocale.locale == "ko")
            .values(published_version=None)
        )
        await session.commit()
    expected = [
        pair for pair in expected if pair[0] >= "article-0002" and pair[1] not in {"ja", "ko"}
    ]
    async with guides.client(guides.make_app(database)) as api:
        entries = []
        cursor = None
        while True:
            response = await api.get(
                "/guides/sitemap", params={"limit": 2, **({"cursor": cursor} if cursor else {})}
            )
            page = response.json()
            entries.extend((row["slug"], row["locale"]) for row in page["entries"])
            cursor = page["next_cursor"]
            if cursor is None:
                break
        assert entries == expected


async def test_sitemap_skips_locales_without_their_published_revision(database) -> None:
    expected = await seed_articles(database, 10)
    missing = {("article-0000", "en"), ("article-0001", "ja")}
    async with database() as session:
        missing_revision_locale_id = await session.scalar(
            select(GuideArticleLocale.id)
            .join(GuideArticle)
            .where(GuideArticle.slug == "article-0000", GuideArticleLocale.locale == "en")
        )
        assert missing_revision_locale_id is not None
        await session.execute(
            update(GuideArticleLocale)
            .where(GuideArticleLocale.id == missing_revision_locale_id)
            .values(version=2, published_version=2)
        )
        draft_revision_locale_id = await session.scalar(
            select(GuideArticleLocale.id)
            .join(GuideArticle)
            .where(GuideArticle.slug == "article-0001", GuideArticleLocale.locale == "ja")
        )
        assert draft_revision_locale_id is not None
        await session.execute(
            update(GuideArticleRevision)
            .where(GuideArticleRevision.article_locale_id == draft_revision_locale_id)
            .values(action="draft_saved")
        )
        await session.commit()

    async with guides.client(guides.make_app(database)) as api:
        for slug, locale in missing:
            article = await api.get(f"/guides/howto/{slug}", params={"locale": locale})
            assert article.status_code == 503

        entries = []
        cursor = None
        while True:
            response = await api.get(
                "/guides/sitemap", params={"limit": 3, **({"cursor": cursor} if cursor else {})}
            )
            assert response.status_code == 200
            page = response.json()
            entries.extend((row["slug"], row["locale"]) for row in page["entries"])
            cursor = page["next_cursor"]
            if cursor is None:
                break
        assert entries == [entry for entry in expected if entry not in missing]
        counts = (await api.get("/guides/sitemap/summary")).json()["counts"]
        by_locale = {row["locale"]: row["count"] for row in counts}
        assert by_locale["en"] == 1
        assert by_locale["ja"] == 1


async def test_republication_or_removal_before_cursor_does_not_skip_next_rows(database) -> None:
    expected = await seed_articles(database, 10)
    async with guides.client(guides.make_app(database)) as api:
        page = (await api.get("/guides/sitemap", params={"limit": 3})).json()
        async with database() as session:
            # The row holding the cursor becomes unpublished, while timestamps change
            # for everyone else. Keyset pagination must still resume after its key.
            await session.execute(
                update(GuideArticleLocale).values(published_at=datetime.now(UTC))
            )
            await session.execute(
                update(GuideArticleLocale)
                .where(GuideArticleLocale.locale == "ko")
                .values(published_version=None)
            )
            await session.commit()
        remaining = await api.get("/guides/sitemap", params={"cursor": page["next_cursor"]})
        assert remaining.status_code == 200
        assert remaining.json()["next_cursor"] is None
        assert [(row["slug"], row["locale"]) for row in remaining.json()["entries"]] == [
            pair for pair in expected[3:] if pair[1] != "ko"
        ]


def encoded(value: object) -> str:
    return base64.urlsafe_b64encode(json.dumps(value).encode()).decode().rstrip("=")


@pytest.mark.parametrize(
    "cursor",
    [
        "",
        "not-a-cursor",
        "%%%",
        encoded(["article-0001", "xx"]),
        encoded(["BAD&SLUG", "en"]),
        encoded(["a" * 121, "en"]),
        encoded(["article-0001"]),
        encoded({"slug": "article-0001", "locale": "en"}),
        encoded([4, "en"]),
        encoded(["article-0001", {}]),
    ],
)
async def test_invalid_cursor_is_rejected_instead_of_restarting(database, cursor) -> None:
    async with guides.client(guides.make_app(database)) as api:
        response = await api.get("/guides/sitemap", params={"cursor": cursor})
        assert response.status_code == 422
        assert response.json()["code"] == "guide_cursor_invalid"


@pytest.mark.parametrize("limit", [0, -1, SITEMAP_LIMIT + 1])
async def test_page_limit_is_validated(database, limit) -> None:
    async with guides.client(guides.make_app(database)) as api:
        response = await api.get("/guides/sitemap", params={"limit": limit})
        assert response.status_code == 422
