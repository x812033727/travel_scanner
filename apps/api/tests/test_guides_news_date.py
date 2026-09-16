"""The day a news article's news happened: stored once per article, written by the editor
and the content packs, and what ``sort=news`` orders a news list by.

The reason it exists is the batch import. A week of stories is published within the same
minute, so publication time says nothing about which story is newer, and ``updated_at``
moves with every correction.
"""

from __future__ import annotations

import base64
import importlib.util
import json
import re
from datetime import UTC, date, datetime
from pathlib import Path
from uuid import UUID, uuid4

import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import select, update

from app.guides.content_pack import apply_import, load_packs, plan_import
from app.guides.models import GuideArticle, GuideArticleLocale
from app.models import AdminAuditLog
from tests import test_guides as guides
from tests.test_guides_content_pack import write_pack

# Fixtures and helpers shared with the guides suite (SQLite plus the optional PostgreSQL leg).
database = guides.database
actor = guides.actor
client = guides.client
make_app = guides.make_app
create_article = guides.create_article
publish = guides.publish

NEWS_SLUG = re.compile(r"-(20\d{2})(\d{2})(\d{2})$")


async def news_article(api, database, slug: str, *, news_date: str | None, day: int) -> dict:
    """A published ``ai-news`` article with a news day, published on a fixed day of
    September 2026 so the order does not depend on the clock."""
    created = await create_article(
        api, slug=slug, kind="life", destination_id=None, topics=["ai-news"], news_date=news_date
    )
    response = await publish(api, created["id"], "zh-TW", created["version"])
    assert response.status_code == 200, response.text
    async with database() as session:
        await session.execute(
            update(GuideArticleLocale)
            .where(GuideArticleLocale.article_id == UUID(created["id"]))
            .values(published_at=datetime(2026, 9, day, tzinfo=UTC))
        )
        await session.commit()
    return created


async def slugs(api, **params) -> list[str]:
    response = await api.get("/guides", params={"locale": "zh-TW", **params})
    assert response.status_code == 200, response.text
    return [item["slug"] for item in response.json()["articles"]]


# --- the order -----------------------------------------------------------------------


async def test_news_order_is_the_news_day_then_publication_with_undated_rows_last(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        # Imported in the order a batch would bring them, which is not the news order.
        await news_article(api, database, "news-a", news_date="2026-09-10", day=1)
        await news_article(api, database, "news-b", news_date="2026-09-14", day=1)
        await news_article(api, database, "news-c", news_date="2026-09-10", day=5)
        await news_article(api, database, "sources-to-follow", news_date=None, day=20)
        await news_article(api, database, "news-d", news_date="2026-07-01", day=30)

        by_news = ["news-b", "news-c", "news-a", "news-d", "sources-to-follow"]
        assert await slugs(api, sort="news") == by_news
        assert await slugs(api, sort="news", topic="ai-news") == by_news
        # Publication time says something else entirely, which is the bug this fixes.
        assert await slugs(api) == ["news-d", "sources-to-follow", "news-c", "news-a", "news-b"]

        listed = (await api.get("/guides", params={"locale": "zh-TW", "sort": "news"})).json()
        days = {item["slug"]: item["news_date"] for item in listed["articles"]}
        assert days["news-b"] == "2026-09-14"
        assert days["sources-to-follow"] is None

        article = (await api.get("/guides/life/news-b", params={"locale": "zh-TW"})).json()
        assert article["news_date"] == "2026-09-14"


async def test_the_news_order_pages_without_repeating_or_dropping_an_article(
    database, actor
) -> None:
    """Ties on the day and on the second are what a batch leaves; the keyset carries every
    sort key, including the null day the undated tail starts with."""
    async with client(make_app(database, actor)) as api:
        plan = [
            ("n-0", "2026-09-10", 1),
            ("n-1", "2026-09-10", 1),
            ("n-2", "2026-09-12", 1),
            ("n-3", None, 1),
            ("n-4", "2026-09-10", 3),
            ("n-5", None, 2),
            ("n-6", "2026-08-01", 1),
            ("n-7", None, 1),
        ]
        for slug, day, published in plan:
            await news_article(api, database, slug, news_date=day, day=published)
        whole = await slugs(api, sort="news", limit=50)
        assert whole == ["n-2", "n-4", "n-0", "n-1", "n-6", "n-5", "n-3", "n-7"]

        seen: list[str] = []
        cursor = None
        while True:
            params = {"locale": "zh-TW", "limit": 2, "sort": "news"}
            if cursor:
                params["cursor"] = cursor
            page = (await api.get("/guides", params=params)).json()
            seen.extend(item["slug"] for item in page["articles"])
            cursor = page["next_cursor"]
            if not cursor:
                break
        assert seen == whole


async def test_a_news_cursor_is_refused_under_another_order_and_the_other_way_round(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        for index in range(3):
            day = f"2026-09-0{index + 1}"
            await news_article(api, database, f"n-{index}", news_date=day, day=1)
        first = {"locale": "zh-TW", "limit": 1}
        news = (await api.get("/guides", params={**first, "sort": "news"})).json()["next_cursor"]
        latest = (await api.get("/guides", params=first)).json()["next_cursor"]
        curated = (await api.get("/guides", params={**first, "sort": "curated"})).json()[
            "next_cursor"
        ]
        padded = news + "=" * (-len(news) % 4)
        assert json.loads(base64.urlsafe_b64decode(padded))[0] == "news"

        crossings = (("latest", news), ("curated", news), ("news", latest), ("news", curated))
        for sort, cursor in crossings:
            response = await api.get("/guides", params={**first, "sort": sort, "cursor": cursor})
            assert response.status_code == 422, (sort, response.text)
            assert response.json()["code"] == "guide_cursor_invalid"


# --- the editor ----------------------------------------------------------------------


async def test_the_editor_sets_keeps_and_clears_the_news_day(database, actor) -> None:
    """A save that does not mention ``news_date`` keeps it: the classification form predates
    the field, and a save from it must not wipe every news article's day. ``null`` clears."""
    async with client(make_app(database, actor)) as api:
        created = await create_article(
            api, slug="news-x", kind="life", destination_id=None, topics=["ai-news"]
        )
        assert created["news_date"] is None

        async def save(**extra) -> dict:
            detail = (await api.get(f"/admin/guides/{created['id']}")).json()
            body = {
                "expected_version": detail["version"],
                "kind": "life",
                "destination_id": None,
                "topics": ["ai-news"],
                **extra,
            }
            response = await api.put(f"/admin/guides/{created['id']}", json=body)
            assert response.status_code == 200, response.text
            return response.json()

        assert (await save(news_date="2026-09-14"))["news_date"] == "2026-09-14"
        assert (await save())["news_date"] == "2026-09-14"
        assert (await save(featured=True, display_order=5))["news_date"] == "2026-09-14"
        assert (await save(news_date=None))["news_date"] is None

    async with database() as session:
        rows = list(
            await session.scalars(
                select(AdminAuditLog)
                .where(AdminAuditLog.action == "guide_article_updated")
                .order_by(AdminAuditLog.created_at)
            )
        )
    assert [row.metadata_json["after"]["news_date"] for row in rows] == [
        "2026-09-14",
        "2026-09-14",
        "2026-09-14",
        None,
    ]
    assert rows[0].metadata_json["before"]["news_date"] is None
    assert rows[-1].metadata_json["before"]["news_date"] == "2026-09-14"


async def test_a_pack_writes_the_news_day_and_a_changed_day_is_a_taxonomy_update(
    database, actor, tmp_path
) -> None:
    life = {"kind": "life", "destination_id": None, "topics": ["ai-news"], "featured": False}
    write_pack(tmp_path, "ai-news-thing-20260914", news_date="2026-09-14", **life)
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        await apply_import(session, actor, plan, publish=True)
    async with database() as session:
        stored = await session.scalar(
            select(GuideArticle.news_date).where(GuideArticle.slug == "ai-news-thing-20260914")
        )
        assert stored == date(2026, 9, 14)
        plan = await plan_import(session, load_packs(tmp_path))
        assert plan.articles[0].taxonomy == "unchanged"

    write_pack(tmp_path, "ai-news-thing-20260914", news_date="2026-09-15", **life)
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        assert plan.articles[0].taxonomy == "update"
        report = await apply_import(session, actor, plan, publish=True)
    assert report.taxonomy_updated == ["ai-news-thing-20260914"]
    async with database() as session:
        stored = await session.scalar(
            select(GuideArticle.news_date).where(GuideArticle.slug == "ai-news-thing-20260914")
        )
    assert stored == date(2026, 9, 15)


def test_every_shipped_dated_news_pack_carries_its_news_day() -> None:
    """A news pack's slug ends in the day of its news (``ai-news-...-20260914``). Without
    ``news_date`` the story drops to the undated tail of every news list, so a pack that
    follows the naming and forgets the field is refused here rather than on the site."""
    checked = 0
    for pack in load_packs():
        match = NEWS_SLUG.search(pack.slug)
        if "ai-news" not in pack.topics or match is None:
            continue
        checked += 1
        assert pack.news_date == date(*map(int, match.groups())), pack.slug
    assert checked >= 38


# --- the migration -------------------------------------------------------------------


def migration():
    path = Path(__file__).parents[1] / "migrations/versions/0079_guide_news_date.py"
    spec = importlib.util.spec_from_file_location("guide_news_date_migration", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_0079_adds_the_column_once_and_its_rollback_drops_only_it(monkeypatch) -> None:
    """On a database 0078 upgraded (no column) and on a fresh one built from the model
    (column already there): afterwards the column and its index exist, a re-run is a
    no-op, and the rollback drops exactly them while the rows stay."""
    module = migration()
    assert module.down_revision == "0078_guide_article_links"
    monkeypatch.setattr(module.context, "is_offline_mode", lambda: False)

    engine = sa.create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(
            sa.text(
                "CREATE TABLE guide_articles (id CHAR(32) PRIMARY KEY, slug VARCHAR(120),"
                " kind VARCHAR(16))"
            )
        )
        connection.execute(
            sa.text("INSERT INTO guide_articles (id, slug, kind) VALUES (:id, 'x', 'life')"),
            {"id": uuid4().hex},
        )
        with Operations.context(MigrationContext.configure(connection)):
            module.upgrade()
            inspector = sa.inspect(connection)
            assert "news_date" in {c["name"] for c in inspector.get_columns("guide_articles")}
            assert "ix_guide_articles_news_date" in {
                i["name"] for i in inspector.get_indexes("guide_articles")
            }
            module.upgrade()  # a re-run finds the column and does nothing

            module.downgrade()
            inspector = sa.inspect(connection)
            assert "news_date" not in {c["name"] for c in inspector.get_columns("guide_articles")}
            assert connection.scalar(sa.text("SELECT count(*) FROM guide_articles")) == 1
            module.downgrade()  # and a second rollback is a no-op too
    engine.dispose()

    fresh = sa.create_engine("sqlite://")
    with fresh.begin() as connection:
        GuideArticle.__table__.create(connection)
        with Operations.context(MigrationContext.configure(connection)):
            module.upgrade()
            assert "news_date" in {
                c["name"] for c in sa.inspect(connection).get_columns("guide_articles")
            }
    fresh.dispose()
