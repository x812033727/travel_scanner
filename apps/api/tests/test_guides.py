"""Travel intel and guide articles: per-locale publication, versioning and audit.

PostgreSQL variants run in their own disposable schema only when the existing integration
flag is enabled. SQLite is not presented as evidence of PostgreSQL row races.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, func, select, text, update
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.auth.service import current_user
from app.config import get_settings
from app.db import Base, get_session
from app.guides.models import (
    GuideArticle,
    GuideArticleLocale,
    GuideArticleRevision,
    GuideArticleTopic,
    GuideTopic,
)
from app.guides.router import admin_router, public_router
from app.guides.taxonomy import LIFE_SEED_TOPICS, SEED_TOPICS, seed_names
from app.models import AdminAuditLog, User
from app.problems import AppError, app_error_handler, validation_error_handler

TABLES = [
    User.__table__,
    GuideTopic.__table__,
    GuideArticle.__table__,
    GuideArticleLocale.__table__,
    GuideArticleRevision.__table__,
    GuideArticleTopic.__table__,
    AdminAuditLog.__table__,
]


@pytest.fixture(params=["sqlite", "postgresql"])
async def database(request, tmp_path) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    schema = f"guides_test_{uuid4().hex}"
    if request.param == "postgresql":
        if os.getenv("RUN_INTEGRATION_TESTS") != "1":
            pytest.skip("requires isolated PostgreSQL integration services")
        url = get_settings().database_url
        assert make_url(url).host in {"localhost", "127.0.0.1", "::1", "postgres", "db"}
        engine = create_async_engine(
            url, poolclass=NullPool, execution_options={"schema_translate_map": {None: schema}}
        )
        async with engine.begin() as connection:
            await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    else:
        engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'guides.db'}")

        @event.listens_for(engine.sync_engine, "connect")
        def foreign_keys(connection, _record):
            connection.execute("PRAGMA foreign_keys=ON")

    async with engine.begin() as connection:
        await connection.run_sync(lambda conn: Base.metadata.create_all(conn, tables=TABLES))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        for order, (slug, labels) in enumerate(SEED_TOPICS):
            session.add(
                GuideTopic(
                    slug=slug,
                    names_json=seed_names(labels),
                    display_order=order * 10,
                    section="travel",
                    source="seed",
                )
            )
        # The lifestyle vocabulary is seeded here too, so a life article can attach `ai`
        # without every test first inventing a topic the migration already ships.
        for order, (slug, labels) in enumerate(LIFE_SEED_TOPICS):
            session.add(
                GuideTopic(
                    slug=slug,
                    names_json=seed_names(labels),
                    display_order=200 + order * 10,
                    section="life",
                    source="seed",
                )
            )
        await session.commit()
    try:
        yield factory
    finally:
        async with engine.begin() as connection:
            if request.param == "postgresql":
                await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
            else:
                await connection.run_sync(lambda conn: Base.metadata.drop_all(conn, tables=TABLES))
        await engine.dispose()


@pytest.fixture
async def actor(database) -> User:
    user = User(
        id=uuid4(),
        email=f"guides-{uuid4().hex}@example.com",
        password_hash="test-hash",
        is_admin=True,
        is_active=True,
    )
    async with database() as session:
        session.add(user)
        await session.commit()
    return user


def make_app(database, user=None) -> FastAPI:
    application = FastAPI()
    application.include_router(admin_router, prefix="/api/v1")
    application.include_router(public_router, prefix="/api/v1")
    application.add_exception_handler(AppError, app_error_handler)
    application.add_exception_handler(RequestValidationError, validation_error_handler)

    async def session_dependency():
        async with database() as session:
            yield session

    application.dependency_overrides[get_session] = session_dependency
    if user is not None:
        application.dependency_overrides[current_user] = lambda: user
    return application


def client(application: FastAPI) -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app=application), base_url="http://guides.test/api/v1"
    )


def document(title="成田機場到東京車站怎麼走", description="三種交通方式的時間與票價比較"):
    return {
        "title": title,
        "description": description,
        "blocks": [
            {"type": "heading", "text": "三種選擇", "level": 2},
            {"type": "paragraph", "text": "Skyliner 最快，利木津巴士最省力，JR 最便宜。"},
            {"type": "list", "items": ["Skyliner 約 41 分鐘", "巴士約 85 分鐘"], "ordered": False},
        ],
        "sources": [
            {
                "title": "Keisei Skyliner timetable",
                "url": "https://www.keisei.co.jp/keisei/tetudou/skyliner/us/",
                "checked_on": "2026-09-01",
            }
        ],
    }


async def create_article(api: AsyncClient, slug="narita-to-tokyo", kind="howto", **extra):
    payload = {
        "slug": slug,
        "kind": kind,
        "destination_id": "tokyo",
        "topics": ["transport"],
        "document": document(),
        "locale": "zh-TW",
        **extra,
    }
    response = await api.post("/admin/guides", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


async def publish(api: AsyncClient, article_id: str, locale: str, version: int):
    return await api.post(
        f"/admin/guides/{article_id}/{locale}/publish",
        json={"expected_version": version, "confirmed": True, "reason": "測試發布"},
    )


async def set_hidden(
    api: AsyncClient, article_id: str, version: int, *, hidden: bool = True, reason="內容有誤"
):
    return await api.post(
        f"/admin/guides/{article_id}/{'hide' if hidden else 'unhide'}",
        json={"expected_version": version, "confirmed": True, "reason": reason},
    )


async def batch(api: AsyncClient, items: list[tuple[str, int]], action: str, **extra):
    return await api.post(
        "/admin/guides/batch",
        json={
            "items": [
                {"id": article_id, "expected_version": version} for article_id, version in items
            ],
            "action": action,
            "confirmed": True,
            "reason": "批次處理",
            **extra,
        },
    )


async def admin_list(api: AsyncClient, **params):
    response = await api.get("/admin/guides", params={"locale": "zh-TW", **params})
    assert response.status_code == 200, response.text
    return response.json()


def facet(body, name: str) -> dict[str, int]:
    return {item["code"]: item["count"] for item in body["facets"][name]}


async def test_publishing_one_locale_leaves_the_others_unpublished(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        assert (await publish(api, created["id"], "zh-TW", created["version"])).status_code == 200

        published = await api.get("/guides/howto/narita-to-tokyo", params={"locale": "zh-TW"})
        assert published.status_code == 200
        body = published.json()
        assert body["status"] == "published"
        assert body["document"]["title"] == "成田機場到東京車站怎麼走"
        assert body["published_locales"] == ["zh-TW"]
        assert body["destination_label"] == "東京"

        other = await api.get("/guides/howto/narita-to-tokyo", params={"locale": "ja"})
        assert other.status_code == 200
        # No fallback: an unwritten translation is never served as if it were one.
        assert other.json()["status"] == "unpublished"
        assert other.json()["document"] is None
        assert other.json()["published_locales"] == ["zh-TW"]


async def test_a_draft_is_never_public_in_any_locale(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await create_article(api)
        for locale in ("zh-TW", "en", "ja", "ko", "zh-CN"):
            response = await api.get("/guides/howto/narita-to-tokyo", params={"locale": locale})
            assert response.json()["status"] == "unpublished"
            assert response.json()["document"] is None
        listing = await api.get("/guides", params={"locale": "zh-TW"})
        assert listing.json()["articles"] == []


async def test_a_dangling_published_pointer_is_unavailable_not_the_draft(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        await publish(api, created["id"], "zh-TW", created["version"])
    async with database() as session:
        row = await session.scalar(select(GuideArticleLocale))
        assert row is not None
        await session.execute(
            update(GuideArticleLocale)
            .where(GuideArticleLocale.id == row.id)
            .values(published_version=row.version + 0, version=row.version)
        )
        await session.execute(
            update(GuideArticleRevision)
            .where(GuideArticleRevision.article_locale_id == row.id)
            .values(action="draft_saved")
        )
        await session.commit()
    async with client(make_app(database, actor)) as api:
        response = await api.get("/guides/howto/narita-to-tokyo", params={"locale": "zh-TW"})
        assert response.status_code == 503
        assert response.json()["code"] == "guide_article_unavailable"


async def test_a_stale_expected_version_is_a_conflict_and_writes_nothing(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        first = await api.put(
            f"/admin/guides/{created['id']}/zh-TW/draft",
            json={"expected_version": 1, "document": document(title="第一次修改")},
        )
        assert first.status_code == 200
        second = await api.put(
            f"/admin/guides/{created['id']}/zh-TW/draft",
            json={"expected_version": 1, "document": document(title="第二次修改")},
        )
        assert second.status_code == 409
        assert second.json()["code"] == "guide_version_conflict"
        detail = await api.get(f"/admin/guides/{created['id']}", params={"locale": "zh-TW"})
        assert detail.json()["draft"]["title"] == "第一次修改"
    async with database() as session:
        revisions = int(
            await session.scalar(select(func.count()).select_from(GuideArticleRevision))
        )
        assert revisions == 2


@pytest.mark.parametrize("confirmed", [False, "true", 1, None, "yes"])
async def test_publication_requires_a_strict_confirmation(database, actor, confirmed) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        response = await api.post(
            f"/admin/guides/{created['id']}/zh-TW/publish",
            json={"expected_version": 1, "confirmed": confirmed, "reason": "測試"},
        )
        assert response.status_code == 422
        assert (await api.get("/guides/howto/narita-to-tokyo", params={"locale": "zh-TW"})).json()[
            "status"
        ] == "unpublished"


async def test_publication_requires_a_reason(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        response = await api.post(
            f"/admin/guides/{created['id']}/zh-TW/publish",
            json={"expected_version": 1, "confirmed": True, "reason": "   "},
        )
        assert response.status_code == 422


async def test_unpublishing_withdraws_the_page_and_keeps_the_history(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        published = await publish(api, created["id"], "zh-TW", created["version"])
        version = published.json()["locales"][0]["version"]
        first_published_at = published.json()["locales"][0]["published_at"]

        withdrawn = await api.post(
            f"/admin/guides/{created['id']}/zh-TW/unpublish",
            json={"expected_version": version, "confirmed": True, "reason": "票價已更新"},
        )
        assert withdrawn.status_code == 200
        assert withdrawn.json()["locales"][0]["published_version"] is None
        # published_at survives so a later republication keeps the original date.
        assert withdrawn.json()["locales"][0]["published_at"] == first_published_at

        assert (await api.get("/guides/howto/narita-to-tokyo", params={"locale": "zh-TW"})).json()[
            "status"
        ] == "unpublished"
        assert (await api.get("/guides", params={"locale": "zh-TW"})).json()["articles"] == []
        assert (await api.get("/guides/sitemap")).json()["entries"] == []

        actions = [item["action"] for item in withdrawn.json()["revisions"]]
        assert "unpublished" in actions and "published" in actions


async def test_an_expired_notice_keeps_its_page_but_leaves_the_listings(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api, slug="jr-pass-sale", kind="intel")
        await publish(api, created["id"], "zh-TW", created["version"])
        assert len((await api.get("/guides", params={"locale": "zh-TW"})).json()["articles"]) == 1

    async with database() as session:
        await session.execute(
            update(GuideArticle).values(valid_until=date.today() - timedelta(days=1))
        )
        await session.commit()

    async with client(make_app(database, actor)) as api:
        # The URL still answers, so links already published elsewhere do not break.
        article = await api.get("/guides/intel/jr-pass-sale", params={"locale": "zh-TW"})
        assert article.json()["status"] == "published"
        assert article.json()["expired"] is True
        # But "what is current" excludes it.
        assert (await api.get("/guides", params={"locale": "zh-TW"})).json()["articles"] == []
        assert (await api.get("/guides/sitemap")).json()["entries"] == []


async def test_publishing_an_already_expired_article_is_refused(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(
            api,
            slug="last-winter-sale",
            kind="intel",
            valid_until=(date.today() - timedelta(days=2)).isoformat(),
        )
        response = await publish(api, created["id"], "zh-TW", created["version"])
        assert response.status_code == 409
        assert response.json()["code"] == "guide_article_expired"


async def test_hiding_withdraws_every_locale_and_restoring_brings_them_all_back(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        await publish(api, created["id"], "zh-TW", created["version"])
        japanese = await api.post(
            f"/admin/guides/{created['id']}/ja",
            json=document(title="成田空港から東京駅まで", description="三つの行き方を比べます"),
        )
        assert japanese.status_code == 201
        await publish(api, created["id"], "ja", 1)

        hidden = await set_hidden(api, created["id"], created["version"])
        assert hidden.status_code == 200, hidden.text
        assert hidden.json()["status"] == "hidden"
        assert hidden.json()["is_active"] is False
        assert hidden.json()["version"] == created["version"] + 1
        # Only the article-wide switch moved: each translation keeps its published pointer.
        assert all(row["published_version"] for row in hidden.json()["locales"])
        for locale in ("zh-TW", "ja"):
            page = await api.get("/guides/howto/narita-to-tokyo", params={"locale": locale})
            assert page.json()["status"] == "unpublished"
        assert (await api.get("/guides", params={"locale": "zh-TW"})).json()["articles"] == []
        assert (await api.get("/guides/sitemap")).json()["entries"] == []

        restored = await set_hidden(
            api, created["id"], hidden.json()["version"], hidden=False, reason="已修正"
        )
        assert restored.status_code == 200, restored.text
        assert restored.json()["status"] == "published"
        # No second round of publishing: both languages are back at once.
        for locale in ("zh-TW", "ja"):
            page = await api.get("/guides/howto/narita-to-tokyo", params={"locale": locale})
            assert page.json()["status"] == "published"
        entries = (await api.get("/guides/sitemap")).json()["entries"]
        assert sorted(entry["locale"] for entry in entries) == ["ja", "zh-TW"]


@pytest.mark.parametrize(
    "payload",
    [
        {"expected_version": 1, "confirmed": False, "reason": "下架"},
        {"expected_version": 1, "confirmed": "true", "reason": "下架"},
        {"expected_version": 1, "confirmed": True, "reason": ""},
        {"expected_version": 1, "confirmed": True},
        {"expected_version": "1", "confirmed": True, "reason": "下架"},
    ],
)
async def test_hiding_requires_a_strict_confirmation_and_a_reason(database, actor, payload) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        response = await api.post(f"/admin/guides/{created['id']}/hide", json=payload)
        assert response.status_code == 422
        assert (await api.get(f"/admin/guides/{created['id']}")).json()["is_active"] is True


async def test_a_stale_version_cannot_hide_and_repeating_a_hide_is_a_conflict(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        stale = await set_hidden(api, created["id"], created["version"] + 5)
        assert stale.status_code == 409
        assert stale.json()["code"] == "guide_version_conflict"

        hidden = await set_hidden(api, created["id"], created["version"])
        assert hidden.status_code == 200
        again = await set_hidden(api, created["id"], hidden.json()["version"])
        assert again.status_code == 409
        assert again.json()["code"] == "guide_article_already_hidden"

        restored = await set_hidden(api, created["id"], hidden.json()["version"], hidden=False)
        assert restored.status_code == 200
        twice = await set_hidden(api, created["id"], restored.json()["version"], hidden=False)
        assert twice.status_code == 409
        assert twice.json()["code"] == "guide_article_not_hidden"

        detail = await api.get(f"/admin/guides/{created['id']}", params={"locale": "zh-TW"})
        actions = [item["action"] for item in detail.json()["audit"]]
        assert actions.count("guide_article_hidden") == 1
        assert actions.count("guide_article_unhidden") == 1
    async with database() as session:
        rows = list(
            await session.scalars(
                select(AdminAuditLog)
                .where(AdminAuditLog.action == "guide_article_hidden")
                .order_by(AdminAuditLog.created_at)
            )
        )
    assert len(rows) == 1
    assert rows[0].metadata_json["reason"] == "內容有誤"
    assert rows[0].metadata_json["operator_confirmed"] is True
    assert rows[0].metadata_json["before"] == {"is_active": True}
    assert rows[0].metadata_json["after"] == {"is_active": False}
    assert rows[0].metadata_json["batch_id"] is None


async def test_a_hidden_article_cannot_be_published_until_it_is_restored(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        hidden = await set_hidden(api, created["id"], created["version"])
        refused = await publish(api, created["id"], "zh-TW", created["locales"][0]["version"])
        assert refused.status_code == 409
        assert refused.json()["code"] == "guide_article_inactive"

        await set_hidden(api, created["id"], hidden.json()["version"], hidden=False)
        allowed = await publish(api, created["id"], "zh-TW", created["locales"][0]["version"])
        assert allowed.status_code == 200, allowed.text
        assert allowed.json()["status"] == "published"


async def test_a_classification_save_never_changes_visibility(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        hidden = await set_hidden(api, created["id"], created["version"])
        taxonomy = {
            "kind": "howto",
            "destination_id": "tokyo",
            "topics": ["transport"],
            "featured": True,
        }
        saved = await api.put(
            f"/admin/guides/{created['id']}",
            json={"expected_version": hidden.json()["version"], **taxonomy},
        )
        assert saved.status_code == 200, saved.text
        assert saved.json()["featured"] is True
        assert saved.json()["is_active"] is False
        assert saved.json()["status"] == "hidden"
        # The old shape carried the switch inside the classification payload. Refusing it
        # outright is what keeps a stale client from quietly republishing an article.
        legacy = await api.put(
            f"/admin/guides/{created['id']}",
            json={"expected_version": saved.json()["version"], **taxonomy, "is_active": True},
        )
        assert legacy.status_code == 422
        assert (await api.get(f"/admin/guides/{created['id']}")).json()["is_active"] is False


async def test_the_admin_listing_filters_by_status_and_reports_facets(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await create_article(api, slug="draft-only")
        live = await create_article(api, slug="live-guide")
        await publish(api, live["id"], "zh-TW", live["version"])
        gone = await create_article(api, slug="hidden-guide")
        await publish(api, gone["id"], "zh-TW", gone["version"])
        await set_hidden(api, gone["id"], gone["version"])
        await create_article(
            api,
            slug="old-deal",
            kind="intel",
            valid_until=(date.today() - timedelta(days=1)).isoformat(),
        )

        everything = await admin_list(api)
        assert everything["total"] == 4
        assert everything["pages"] == 1
        assert {item["slug"]: item["status"] for item in everything["articles"]} == {
            "draft-only": "draft",
            "live-guide": "published",
            "hidden-guide": "hidden",
            "old-deal": "expired",
        }
        assert facet(everything, "status") == {
            "published": 1,
            "draft": 1,
            "hidden": 1,
            "expired": 1,
        }
        assert facet(everything, "kind") == {"intel": 1, "howto": 3, "life": 0}

        hidden = await admin_list(api, status="hidden")
        assert [item["slug"] for item in hidden["articles"]] == ["hidden-guide"]
        # A facet never counts its own filter, so the other pills keep their numbers.
        assert facet(hidden, "status") == facet(everything, "status")
        assert facet(hidden, "kind") == {"intel": 0, "howto": 1, "life": 0}

        intel = await admin_list(api, kind="intel")
        assert intel["total"] == 1
        assert facet(intel, "kind") == {"intel": 1, "howto": 3, "life": 0}
        assert facet(intel, "status") == {"published": 0, "draft": 0, "hidden": 0, "expired": 1}

        nonsense = await api.get("/admin/guides", params={"locale": "zh-TW", "status": "gone"})
        assert nonsense.status_code == 422


async def test_the_admin_listing_searches_by_slug_or_title_and_pages(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        for index in range(5):
            await create_article(
                api, slug=f"guide-{index}", document=document(title=f"第 {index} 篇攻略")
            )
        first = await admin_list(api, limit=2, page=1)
        assert first["total"] == 5
        assert first["pages"] == 3
        assert len(first["articles"]) == 2
        last = await admin_list(api, limit=2, page=3)
        assert len(last["articles"]) == 1
        seen: list[str] = []
        for number in (1, 2, 3):
            chunk = await admin_list(api, limit=2, page=number)
            seen.extend(item["slug"] for item in chunk["articles"])
        assert sorted(seen) == [f"guide-{index}" for index in range(5)]
        assert len(seen) == len(set(seen))

        async def found(q: str) -> list[str]:
            return [item["slug"] for item in (await admin_list(api, q=q))["articles"]]

        assert await found("guide-3") == ["guide-3"]
        assert await found("第 4") == ["guide-4"]
        # LIKE metacharacters are matched literally, never as wildcards.
        assert (await admin_list(api, q="%"))["articles"] == []
        assert (await admin_list(api, q="_"))["total"] == 0


async def test_batch_visibility_is_all_or_nothing_and_skips_rows_already_there(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        first = await create_article(api, slug="batch-a")
        await publish(api, first["id"], "zh-TW", first["version"])
        second = await create_article(api, slug="batch-b")
        await publish(api, second["id"], "zh-TW", second["version"])
        third = await create_article(api, slug="batch-c")
        already = await set_hidden(api, third["id"], third["version"])

        stale = await batch(api, [(first["id"], 1), (second["id"], 99)], "hide")
        assert stale.status_code == 409
        assert stale.json()["code"] == "guide_version_conflict"
        assert (await admin_list(api, status="hidden"))["total"] == 1

        missing = await batch(api, [(first["id"], 1), (str(uuid4()), 1)], "hide")
        assert missing.status_code == 404

        done = await batch(
            api,
            [(first["id"], 1), (second["id"], 1), (third["id"], already.json()["version"])],
            "hide",
        )
        assert done.status_code == 200, done.text
        assert done.json()["updated"] == 2
        assert done.json()["skipped"] == 1
        assert done.json()["status"] == "hidden"
        assert [item["slug"] for item in done.json()["articles"]] == [
            "batch-a",
            "batch-b",
            "batch-c",
        ]
        assert all(item["status"] == "hidden" for item in done.json()["articles"])
        assert [item["version"] for item in done.json()["articles"]] == [2, 2, 2]
        assert (await api.get("/guides", params={"locale": "zh-TW"})).json()["articles"] == []

        restored = await batch(api, [(first["id"], 2), (second["id"], 2)], "unhide")
        assert restored.status_code == 200
        assert restored.json()["updated"] == 2
        assert restored.json()["status"] == "active"
        assert len((await api.get("/guides", params={"locale": "zh-TW"})).json()["articles"]) == 2

        for broken in (
            {"confirmed": False},
            {"items": [{"id": first["id"], "expected_version": 3}] * 2},
            {"items": []},
            {"action": "archive"},
        ):
            response = await api.post(
                "/admin/guides/batch",
                json={
                    "items": [{"id": first["id"], "expected_version": 3}],
                    "action": "hide",
                    "confirmed": True,
                    "reason": "批次處理",
                    **broken,
                },
            )
            assert response.status_code == 422, broken
    async with database() as session:
        rows = list(
            await session.scalars(
                select(AdminAuditLog)
                .where(AdminAuditLog.action == "guide_article_hidden")
                .order_by(AdminAuditLog.created_at)
            )
        )
    assert len(rows) == 3
    batch_ids = {row.metadata_json["batch_id"] for row in rows}
    assert None in batch_ids and len(batch_ids) == 2


async def test_restoring_a_revision_writes_a_draft_and_never_moves_the_public_pointer(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        published = await publish(api, created["id"], "zh-TW", created["version"])
        published_version = published.json()["locales"][0]["published_version"]
        version = published.json()["locales"][0]["version"]
        original = next(
            item for item in published.json()["revisions"] if item["action"] == "created"
        )

        edited = await api.put(
            f"/admin/guides/{created['id']}/zh-TW/draft",
            json={"expected_version": version, "document": document(title="改壞了")},
        )
        restored = await api.post(
            f"/admin/guides/{created['id']}/zh-TW/restore",
            json={
                "expected_version": edited.json()["locales"][0]["version"],
                "revision_id": original["id"],
                "reason": "回到原本的版本",
            },
        )
        assert restored.status_code == 200
        assert restored.json()["draft"]["title"] == "成田機場到東京車站怎麼走"
        # The public pointer stays where it was; a restore is not a publication.
        assert restored.json()["locales"][0]["published_version"] == published_version
        assert restored.json()["published"]["title"] == "成田機場到東京車站怎麼走"


async def test_every_write_leaves_one_audit_row_with_a_matching_hash(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        await publish(api, created["id"], "zh-TW", created["version"])
    async with database() as session:
        rows = list(await session.scalars(select(AdminAuditLog).order_by(AdminAuditLog.created_at)))
    assert [row.action for row in rows] == ["guide_article_created", "guide_article_published"]
    for row in rows:
        assert row.actor_user_id == actor.id
        assert len(row.target) <= 128
        assert row.metadata_json["document_sha256"]
    assert rows[-1].metadata_json["reason"] == "測試發布"
    assert rows[-1].metadata_json["operator_confirmed"] is True


async def test_an_unknown_destination_or_topic_is_refused(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        bad_destination = await api.post(
            "/admin/guides",
            json={
                "slug": "somewhere",
                "kind": "howto",
                "destination_id": "atlantis",
                "topics": [],
                "document": document(),
            },
        )
        assert bad_destination.status_code == 422
        assert bad_destination.json()["code"] == "guide_destination_unknown"

        bad_topic = await api.post(
            "/admin/guides",
            json={
                "slug": "somewhere",
                "kind": "howto",
                "destination_id": None,
                "topics": ["teleportation"],
                "document": document(),
            },
        )
        assert bad_topic.status_code == 422
        assert bad_topic.json()["code"] == "guide_topic_unknown"


async def test_a_duplicate_slug_is_a_conflict(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await create_article(api)
        response = await api.post(
            "/admin/guides",
            json={
                "slug": "narita-to-tokyo",
                "kind": "intel",
                "topics": [],
                "document": document(),
            },
        )
        assert response.status_code == 409
        assert response.json()["code"] == "guide_slug_taken"


@pytest.mark.parametrize("slug", ["Narita To Tokyo", "narita_to_tokyo", "成田到東京", "a--b", "-x"])
async def test_a_slug_must_be_a_url_safe_lowercase_word_list(database, actor, slug) -> None:
    async with client(make_app(database, actor)) as api:
        response = await api.post(
            "/admin/guides",
            json={"slug": slug, "kind": "howto", "topics": [], "document": document()},
        )
        assert response.status_code == 422


@pytest.mark.parametrize(
    "url", ["javascript:alert(1)", "data:text/html,x", "mailto:a@example.com", "http://u:p@x.test/"]
)
async def test_a_source_link_must_be_a_plain_http_url(database, actor, url) -> None:
    payload = document()
    payload["sources"] = [{"title": "來源", "url": url}]
    async with client(make_app(database, actor)) as api:
        response = await api.post(
            "/admin/guides",
            json={"slug": "source-test", "kind": "intel", "topics": [], "document": payload},
        )
        assert response.status_code == 422


async def test_the_body_rejects_html_rather_than_sanitizing_it(database, actor) -> None:
    payload = document()
    payload["blocks"] = [{"type": "paragraph", "text": "<script>alert(1)</script>"}]
    async with client(make_app(database, actor)) as api:
        response = await api.post(
            "/admin/guides",
            json={"slug": "html-test", "kind": "howto", "topics": [], "document": payload},
        )
        assert response.status_code == 422


async def test_the_listing_filters_by_kind_destination_and_topic(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        deal = await create_article(api, slug="tokyo-fare-deal", kind="intel")
        await publish(api, deal["id"], "zh-TW", deal["version"])
        guide = await create_article(api, slug="narita-to-tokyo", kind="howto")
        await publish(api, guide["id"], "zh-TW", guide["version"])

        async def slugs(**params):
            response = await api.get("/guides", params={"locale": "zh-TW", **params})
            return sorted(item["slug"] for item in response.json()["articles"])

        assert await slugs() == ["narita-to-tokyo", "tokyo-fare-deal"]
        assert await slugs(kind="intel") == ["tokyo-fare-deal"]
        assert await slugs(destination="tokyo") == ["narita-to-tokyo", "tokyo-fare-deal"]
        assert await slugs(destination="seoul") == []
        assert await slugs(topic="transport") == ["narita-to-tokyo", "tokyo-fare-deal"]
        assert await slugs(topic="budget") == []


async def test_the_sitemap_lists_one_entry_per_published_locale(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        await publish(api, created["id"], "zh-TW", created["version"])
        japanese = await api.post(
            f"/admin/guides/{created['id']}/ja",
            json=document(title="成田空港から東京駅まで", description="三つの行き方を比べます"),
        )
        assert japanese.status_code == 201
        await publish(api, created["id"], "ja", 1)

        entries = (await api.get("/guides/sitemap")).json()["entries"]
        assert sorted(entry["locale"] for entry in entries) == ["ja", "zh-TW"]
        assert {entry["slug"] for entry in entries} == {"narita-to-tokyo"}
        assert all(entry["published_at"] for entry in entries)


async def test_a_translation_starts_empty_and_never_copies_another_locale(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        await publish(api, created["id"], "zh-TW", created["version"])
        korean = await api.post(
            f"/admin/guides/{created['id']}/ko",
            json=document(title="나리타에서 도쿄역까지", description="세 가지 교통편 비교"),
        )
        assert korean.status_code == 201
        assert korean.json()["draft"]["title"] == "나리타에서 도쿄역까지"
        again = await api.post(
            f"/admin/guides/{created['id']}/ko",
            json=document(title="중복", description="중복"),
        )
        assert again.status_code == 409
        assert again.json()["code"] == "guide_locale_exists"


async def test_topic_labels_follow_the_reader_language(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        by_locale = {}
        for locale in ("zh-TW", "ja", "en"):
            response = await api.get("/guides/topics", params={"locale": locale})
            by_locale[locale] = {item["slug"]: item["label"] for item in response.json()["topics"]}
        assert by_locale["zh-TW"]["transport"] == "交通"
        assert by_locale["ja"]["transport"] == "交通"
        assert by_locale["en"]["transport"] == "Transport"


async def test_an_admin_without_content_capability_cannot_write(database, actor) -> None:
    actor._admin_roles_cache = {"support"}
    async with client(make_app(database, actor)) as api:
        response = await api.post(
            "/admin/guides",
            json={"slug": "blocked", "kind": "howto", "topics": [], "document": document()},
        )
        assert response.status_code == 403


async def test_public_reads_never_require_an_account(database) -> None:
    async with client(make_app(database)) as api:
        for path in ("/guides", "/guides/topics", "/guides/sitemap"):
            response = await api.get(path, params={"locale": "zh-TW"})
            assert response.status_code == 200
            assert response.headers["Cache-Control"] == "no-store"


async def test_a_hand_edited_cursor_is_rejected_rather_than_silently_restarting(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        response = await api.get("/guides", params={"locale": "zh-TW", "cursor": "not-a-cursor"})
        assert response.status_code == 422
        assert response.json()["code"] == "guide_cursor_invalid"


async def test_the_listing_pages_without_repeating_or_dropping_an_article(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        for index in range(7):
            created = await create_article(api, slug=f"deal-{index}", kind="intel")
            await publish(api, created["id"], "zh-TW", created["version"])
        seen: list[str] = []
        cursor = None
        for _ in range(10):
            params = {"locale": "zh-TW", "limit": 3}
            if cursor:
                params["cursor"] = cursor
            page = (await api.get("/guides", params=params)).json()
            seen.extend(item["slug"] for item in page["articles"])
            cursor = page["next_cursor"]
            if not cursor:
                break
        assert sorted(seen) == sorted(f"deal-{index}" for index in range(7))
        assert len(seen) == len(set(seen))


async def test_published_at_records_the_first_publication_not_the_latest(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        first = await publish(api, created["id"], "zh-TW", created["version"])
        original = first.json()["locales"][0]["published_at"]
        edited = await api.put(
            f"/admin/guides/{created['id']}/zh-TW/draft",
            json={
                "expected_version": first.json()["locales"][0]["version"],
                "document": document(title="更新後的標題"),
            },
        )
        again = await publish(api, created["id"], "zh-TW", edited.json()["locales"][0]["version"])
        assert again.json()["locales"][0]["published_at"] == original
        assert again.json()["published"]["title"] == "更新後的標題"


def test_the_seed_topics_carry_a_label_in_every_locale() -> None:
    from app.i18n import LOCALES

    for slug, labels in SEED_TOPICS:
        names = seed_names(labels)
        assert set(names) == set(LOCALES), slug
        assert all(value.strip() for value in names.values()), slug


def test_the_shared_topic_ids_match_the_discovery_vocabulary() -> None:
    """A guide tagged ``food`` and an attraction categorised ``food`` mean the same thing.

    They are two tables today, so nothing but this test stops the two label sets drifting.
    """
    from app.discovery.taxonomy import LABELS

    guide_labels = dict(SEED_TOPICS)
    shared = set(guide_labels) & set(LABELS)
    assert len(shared) >= 7
    for slug in sorted(shared):
        assert guide_labels[slug] == LABELS[slug], slug


def test_now_is_utc_not_local_time() -> None:
    assert datetime.now(UTC).tzinfo is UTC


async def test_a_lifestyle_article_lives_in_its_own_section(database, actor) -> None:
    """The section is what the public listings filter on, and `life` is its only kind."""
    async with client(make_app(database, actor)) as api:
        life = await create_article(
            api, slug="ai-notes", kind="life", destination_id=None, topics=["ai"]
        )
        await publish(api, life["id"], "zh-TW", life["version"])
        travel = await create_article(api, slug="narita-to-tokyo", kind="howto")
        await publish(api, travel["id"], "zh-TW", travel["version"])

        async def slugs(**params):
            response = await api.get("/guides", params={"locale": "zh-TW", **params})
            assert response.status_code == 200, response.text
            return sorted(item["slug"] for item in response.json()["articles"])

        assert await slugs() == ["ai-notes", "narita-to-tokyo"]
        assert await slugs(section="life") == ["ai-notes"]
        assert await slugs(section="travel") == ["narita-to-tokyo"]
        # kind and section compose as an intersection, and an empty one is an empty list --
        # not, as a careless refactor would have it, an unfiltered one.
        assert await slugs(section="life", kind="life") == ["ai-notes"]
        assert await slugs(section="life", kind="intel") == []
        assert await slugs(section="travel", kind="howto") == ["narita-to-tokyo"]
        assert (await api.get("/guides", params={"section": "hobby"})).status_code == 422

        # Its own kind path serves it; the travel path does not, whatever the slug.
        served = await api.get("/guides/life/ai-notes", params={"locale": "zh-TW"})
        assert served.status_code == 200
        assert served.json()["status"] == "published"
        assert served.json()["destination_id"] is None
        elsewhere = await api.get("/guides/howto/ai-notes", params={"locale": "zh-TW"})
        assert elsewhere.json()["status"] == "unpublished"

        entries = (await api.get("/guides/sitemap")).json()["entries"]
        assert {entry["kind"] for entry in entries} == {"life", "howto"}


async def test_topics_belong_to_one_section_and_are_refused_in_the_other(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        for section, slugs in (("life", ["ai"]), ("travel", ["transport"])):
            response = await api.get(
                "/guides/topics", params={"locale": "zh-TW", "section": section}
            )
            rows = response.json()["topics"]
            assert {row["section"] for row in rows} == {section}
            assert set(slugs) <= {row["slug"] for row in rows}
        life_rows = (await api.get("/guides/topics", params={"section": "life"})).json()["topics"]
        assert [row["slug"] for row in life_rows] == [
            "ai", "tutorial", "software", "gadgets", "productivity", "daily", "misc",
        ]
        unfiltered = (await api.get("/guides/topics", params={"locale": "zh-TW"})).json()["topics"]
        assert len(unfiltered) == len(life_rows) + 19

        # A travel topic on a lifestyle article, and the reverse, are both refused -- on
        # create and on update, because `topics` is optional and would otherwise be a way in.
        wrong_way = await api.post(
            "/admin/guides",
            json={
                "slug": "mismatched", "kind": "life", "destination_id": None,
                "topics": ["transport"], "document": document(),
            },
        )
        assert wrong_way.status_code == 422
        assert wrong_way.json()["code"] == "guide_topic_section_mismatch"

        other_way = await api.post(
            "/admin/guides",
            json={
                "slug": "mismatched", "kind": "howto", "destination_id": "tokyo",
                "topics": ["ai"], "document": document(),
            },
        )
        assert other_way.status_code == 422
        assert other_way.json()["code"] == "guide_topic_section_mismatch"

        article = await create_article(api, slug="narita-to-tokyo", kind="howto")
        update = await api.put(
            f"/admin/guides/{article['id']}",
            json={
                "expected_version": article["version"], "kind": "howto",
                "destination_id": "tokyo", "topics": ["ai"], "valid_until": None,
                "featured": False, "display_order": 100,
            },
        )
        assert update.status_code == 422
        assert update.json()["code"] == "guide_topic_section_mismatch"


async def test_a_published_article_cannot_change_section(database, actor) -> None:
    """Kind is part of the URL. Moving sections moves the URL, so it is refused while any
    translation is public; withdrawing every language first is the way through."""
    async with client(make_app(database, actor)) as api:
        article = await create_article(api, slug="narita-to-tokyo", kind="howto")
        await publish(api, article["id"], "zh-TW", article["version"])

        def taxonomy(version: int, kind: str, topics: list[str]):
            return {
                "expected_version": version, "kind": kind, "destination_id": "tokyo",
                "topics": topics, "valid_until": None, "featured": False,
                "display_order": 100,
            }

        detail = (await api.get(f"/admin/guides/{article['id']}")).json()
        locked = await api.put(
            f"/admin/guides/{article['id']}", json=taxonomy(detail["version"], "life", [])
        )
        assert locked.status_code == 409
        assert locked.json()["code"] == "guide_kind_locked"

        # Within the section the URL keeps the same shape, so this stays allowed.
        same_section = await api.put(
            f"/admin/guides/{article['id']}",
            json=taxonomy(detail["version"], "intel", ["transport"]),
        )
        assert same_section.status_code == 200
        assert same_section.json()["kind"] == "intel"

        row = next(
            entry for entry in same_section.json()["locales"] if entry["locale"] == "zh-TW"
        )
        withdrawn = await api.post(
            f"/admin/guides/{article['id']}/zh-TW/unpublish",
            json={"expected_version": row["version"], "confirmed": True, "reason": "測試撤下"},
        )
        assert withdrawn.status_code == 200
        moved = await api.put(
            f"/admin/guides/{article['id']}",
            json=taxonomy(withdrawn.json()["version"], "life", ["ai"]),
        )
        assert moved.status_code == 200
        assert moved.json()["kind"] == "life"
        assert [topic["section"] for topic in moved.json()["topics"]] == ["life"]


def test_the_two_seed_vocabularies_stay_disjoint() -> None:
    """A slug is global (uq_guide_topic_slug), so the sections cannot share one; and a
    lifestyle slug must not collide with the discovery vocabulary either."""
    from app.discovery.taxonomy import LABELS
    from app.guides.taxonomy import LIFE_SEED_TOPICS

    life = {slug for slug, _ in LIFE_SEED_TOPICS}
    travel = {slug for slug, _ in SEED_TOPICS}
    assert life & travel == set()
    assert life & set(LABELS) == set()
    assert len(life) == len(LIFE_SEED_TOPICS)
