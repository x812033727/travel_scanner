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
from app.guides.taxonomy import SEED_TOPICS, seed_names
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


async def test_archiving_removes_the_article_from_every_public_surface(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(api)
        await publish(api, created["id"], "zh-TW", created["version"])
        updated = await api.put(
            f"/admin/guides/{created['id']}",
            json={
                "expected_version": created["version"],
                "kind": "howto",
                "destination_id": "tokyo",
                "topics": ["transport"],
                "is_active": False,
            },
        )
        assert updated.status_code == 200
        assert (await api.get("/guides/howto/narita-to-tokyo", params={"locale": "zh-TW"})).json()[
            "status"
        ] == "unpublished"
        assert (await api.get("/guides", params={"locale": "zh-TW"})).json()["articles"] == []
        assert (await api.get("/guides/sitemap")).json()["entries"] == []


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
