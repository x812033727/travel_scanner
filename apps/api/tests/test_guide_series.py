"""Publication boundaries are identical for the directory, navigation and inline links."""

from datetime import timedelta

import pytest
from pydantic import ValidationError
from sqlalchemy import update

from app.guides.admin_service import _ordinary_urls
from app.guides.models import GuideArticle, GuideArticleLocale
from app.guides.schemas import GuideDocument
from app.guides.series import catalogues
from tests import test_guides as guides

database = guides.database
actor = guides.actor


def test_catalogue_is_complete_and_references_are_valid():
    catalogue = next(item for item in catalogues() if item.slug == "claude-code")
    assert len(catalogue.entries) == 96
    assert len(catalogue.groups) == 16
    assert len(catalogue.paths) == 12
    assert catalogue.hub == "claude-code-tutorials"


def test_the_registry_names_hubs_that_exist_and_series_the_api_can_serve():
    """A registry row is a promise the section page will keep: its hub is a shipped pack,
    an ``api-series`` row has a catalogue, and its topic is in the lifestyle vocabulary."""
    from app.guides.content_pack import load_packs
    from app.guides.retopic import LIFE_VOCABULARY
    from app.guides.series import registry

    entries = registry()
    assert [entry.slug for entry in entries] == [
        "claude-code",
        "codex",
        "gemini",
        "ai-terms",
        "ai-search-terms",
    ]
    shipped = {pack.slug: pack.kind for pack in load_packs()}
    catalogued = {item.slug for item in catalogues()}
    for entry in entries:
        assert shipped.get(entry.hub_slug) == entry.hub_kind, entry.slug
        assert entry.section == "life"
        assert entry.topic in LIFE_VOCABULARY, entry.slug
        if entry.source == "api-series":
            assert entry.slug in catalogued, entry.slug


async def test_the_series_index_lists_only_hubs_published_in_the_locale(database, actor):
    from app.guides.series import public_series_index

    async with guides.client(guides.make_app(database, actor)) as api:
        hub = await guides.create_article(
            api, slug="claude-code-tutorials", kind="life", destination_id=None, topics=["ai"]
        )
        await guides.publish(api, hub["id"], "zh-TW", hub["version"])
        terms = await guides.create_article(
            api, slug="ai-terms-index", kind="life", destination_id=None, topics=["ai"]
        )
        assert terms["status"] == "draft"

        response = await api.get("/guides/series", params={"locale": "zh-TW"})
        assert response.status_code == 200, response.text
        assert response.headers["cache-control"] == "no-store"
        assert response.json() == {
            "series": [
                {
                    "slug": "claude-code",
                    "section": "life",
                    "hub": {
                        "kind": "life",
                        "slug": "claude-code-tutorials",
                        "title": "成田機場到東京車站怎麼走",
                        "description": "三種交通方式的時間與票價比較",
                    },
                    "source": "api-series",
                    "topic": "claude-code",
                    "entries": 96,
                }
            ]
        }
        assert (await api.get("/guides/series", params={"locale": "ja"})).json() == {"series": []}
        # Publishing the glossary hub adds its row, in registry order, with no catalogue count.
        await guides.publish(api, terms["id"], "zh-TW", terms["version"])
        rows = (await api.get("/guides/series", params={"locale": "zh-TW"})).json()["series"]
        assert [(row["slug"], row["entries"]) for row in rows] == [
            ("claude-code", 96),
            ("ai-terms", None),
        ]

    async with database() as session:
        assert [row.slug for row in (await public_series_index(session, "zh-TW")).series] == [
            "claude-code",
            "ai-terms",
        ]


def test_codex_catalogues_select_exact_locale_and_preserve_stable_routes():
    from app.guides.series import catalogue_for_article

    codex = [item for item in catalogues() if item.slug == "codex"]
    assert {item.locale for item in codex} == {"zh-TW", "zh-CN", "en", "ja", "ko"}
    for item in codex:
        assert len(item.entries) == 60
        assert len(item.groups) == 10
        assert len(item.paths) == 5
        assert item.navigation_by_group
        assert catalogue_for_article(item.hub, item.locale) is item
        assert catalogue_for_article("codex-cli-getting-started", item.locale) is item
        assert all(
            entry.reading_minutes and entry.operation_minutes
            for entry in item.entries
            if entry.slug == "codex-skills"
        )
    assert catalogue_for_article("claude-code-tutorials", "en") is None


async def test_codex_navigation_uses_live_locale_withdrawal_and_unit_boundaries(monkeypatch):
    from app.guides import series
    from app.guides.schemas import ArticleReference

    public = {
        "codex-learning-hub",
        "codex-beginner-guide",
        "codex-account-usage",
        "codex-cli-getting-started",
    }

    async def documents(_session, locale, targets):
        return {
            slug: (
                ArticleReference(kind="life", slug=slug, title=f"{locale} published {slug}"),
                GuideDocument.model_validate(guides.document(title=f"{locale} published {slug}")),
            )
            for kind, slug in targets
            if kind == "life" and slug in public
        }

    monkeypatch.setattr(series, "published_documents", documents)
    for locale in ["zh-TW", "zh-CN", "en", "ja", "ko"]:
        value = await series.article_navigation(None, "life", "codex-account-usage", locale)
        assert value.hub.title.startswith(locale)
        assert value.previous.slug == "codex-beginner-guide"
        assert value.next is None  # CLI is in the next unit, not the current route.
        assert value.current.minutes == 10
        assert value.current.operation_minutes
    public.remove("codex-account-usage")
    directory = await series.public_series(None, "codex", "ja")
    assert "codex-account-usage" not in {entry.slug for entry in directory.entries}
    assert all("codex-account-usage" not in path.slugs for path in directory.paths)
    nav = await series.article_navigation(None, "life", "codex-beginner-guide", "ja")
    assert nav.next is None
    public.remove("codex-learning-hub")
    assert await series.public_series(None, "codex", "ja") is None


def rich_document():
    document = guides.document()
    document["blocks"] += [
        {
            "type": "rich_paragraph",
            "inlines": [
                {"type": "text", "text": "Read "},
                {
                    "type": "article",
                    "kind": "life",
                    "slug": "claude-code-accounts-and-access",
                    "text": "account setup",
                },
                {"type": "code", "text": " <button> "},
                {
                    "type": "link",
                    "url": "https://code.claude.com/docs/en/memory",
                    "text": "official docs",
                },
            ],
        },
        {
            "type": "code",
            "label": "Write index.html",
            "language": "html",
            "code": '<button>\n\tSave & "test"\n</button>\n',
        },
    ]
    return document


def test_code_and_spaces_round_trip_without_html_interpretation():
    value = rich_document()
    assert GuideDocument.model_validate(value).model_dump()["blocks"] == [
        {**block, **({"ordered": False} if block["type"] == "list" else {})}
        for block in value["blocks"]
    ]
    assert list(_ordinary_urls(GuideDocument.model_validate(value))) == [
        "https://code.claude.com/docs/en/memory",
        value["sources"][0]["url"],
    ]


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "data:text/html,bad",
        "https://u:p@example.com/x",
        "https://example.com/\n",
    ],
)
def test_inline_urls_use_the_existing_safety_boundary(url):
    value = rich_document()
    value["blocks"][-2]["inlines"][-1]["url"] = url
    with pytest.raises(ValidationError):
        GuideDocument.model_validate(value)


async def create(api, slug, *, doc=None):
    created = await guides.create_article(
        api,
        slug,
        "life",
        destination_id=None,
        topics=["ai"],
        document=doc or guides.document(title=slug),
    )
    await guides.publish(api, created["id"], "zh-TW", created["version"])
    return created


async def test_series_route_precedes_kind_route_and_requires_published_hub(database, actor):
    async with guides.client(guides.make_app(database, actor)) as api:
        await create(api, "claude-code-getting-started")
        response = await api.get("/guides/series/claude-code")
        assert response.status_code == 404
        await create(api, "claude-code-tutorials")
        response = await api.get("/guides/series/claude-code")
        assert response.status_code == 200
        assert response.headers["cache-control"] == "no-store"
        assert [entry["number"] for entry in response.json()["entries"]] == [1]
        assert (await api.get("/guides/series/claude-code?locale=en")).status_code == 404


@pytest.mark.parametrize("state", ["hidden", "withdrawn", "expired", "other-locale"])
@pytest.mark.parametrize("numbers", [(1, 2), (60, 61)])
async def test_unavailable_targets_leave_no_public_navigation_or_inline_link(
    database, actor, state, numbers
):
    catalogue = catalogues()[0]
    source_slug = catalogue.entries[numbers[0] - 1].slug
    target_slug = catalogue.entries[numbers[1] - 1].slug
    document = rich_document()
    document["blocks"][-2]["inlines"][1]["slug"] = target_slug
    async with guides.client(guides.make_app(database, actor)) as api:
        await create(api, "claude-code-tutorials")
        await create(api, source_slug, doc=document)
        target = await create(api, target_slug)
        before = (await api.get(f"/guides/life/{source_slug}")).json()
        assert before["article_links"][0]["slug"] == target_slug
        assert before["series"]["next"]["slug"] == target_slug
        async with database() as session:
            from uuid import UUID

            identifier = UUID(target["id"])
            if state == "hidden":
                await session.execute(
                    update(GuideArticle)
                    .where(GuideArticle.id == identifier)
                    .values(is_active=False)
                )
            elif state == "expired":
                await session.execute(
                    update(GuideArticle)
                    .where(GuideArticle.id == identifier)
                    .values(valid_until=guides.today() - timedelta(days=1))
                )
            elif state == "withdrawn":
                await session.execute(
                    update(GuideArticleLocale)
                    .where(GuideArticleLocale.article_id == identifier)
                    .values(published_version=None)
                )
            else:
                await session.execute(
                    update(GuideArticleLocale)
                    .where(GuideArticleLocale.article_id == identifier)
                    .values(locale="en")
                )
            await session.commit()
        after = (await api.get(f"/guides/life/{source_slug}")).json()
        assert after["article_links"] == []
        assert after["series"]["next"] is None
        directory = (await api.get("/guides/series/claude-code")).json()
        assert [entry["number"] for entry in directory["entries"]] == [numbers[0]]
        assert all(
            target_slug not in path["slugs"] for path in directory["paths"]
        )


async def test_draft_title_never_replaces_the_published_revision(database, actor):
    async with guides.client(guides.make_app(database, actor)) as api:
        await create(api, "claude-code-tutorials")
        article = await create(api, "claude-code-getting-started")
        detail = (await api.get(f"/admin/guides/{article['id']}?locale=zh-TW")).json()
        response = await api.put(
            f"/admin/guides/{article['id']}/zh-TW/draft",
            json={
                "expected_version": detail["locales"][0]["version"],
                "document": guides.document(title="PRIVATE DRAFT"),
            },
        )
        assert response.status_code == 200, response.text
        assert "PRIVATE DRAFT" not in (await api.get("/guides/series/claude-code")).text


@pytest.mark.parametrize("locale", ["zh-TW", "zh-CN", "en", "ja", "ko"])
async def test_codex_locale_publication_controls_directory_and_inline_links(
    database, actor, locale
):
    async with guides.client(guides.make_app(database, actor)) as api:
        identifiers = {}
        for slug in ["codex-learning-hub", "codex-beginner-guide", "codex-account-usage"]:
            doc = guides.document(title=f"{locale} published {slug}")
            doc["blocks"].append(
                {
                    "type": "rich_paragraph",
                    "inlines": [
                        {
                            "type": "article",
                            "kind": "life",
                            "slug": "codex-account-usage",
                            "text": "Account",
                        }
                    ],
                }
            )
            created = await guides.create_article(
                api, slug, "life", destination_id=None, topics=["ai"], document=doc
            )
            identifiers[slug] = created["id"]
            if locale == "zh-TW":
                version = created["version"]
            else:
                added = await api.post(f"/admin/guides/{created['id']}/{locale}", json=doc)
                assert added.status_code == 201, added.text
                version = next(
                    item["version"] for item in added.json()["locales"] if item["locale"] == locale
                )
            response = await guides.publish(api, created["id"], locale, version)
            assert response.status_code == 200, response.text
        directory = (await api.get(f"/guides/series/codex?locale={locale}")).json()
        assert directory["locale"] == locale
        assert len(directory["entries"]) == 2
        assert all(row["title"].startswith(locale) for row in directory["entries"])
        page = (await api.get(f"/guides/life/codex-beginner-guide?locale={locale}")).json()
        assert page["series"]["next"]["slug"] == "codex-account-usage"
        assert page["article_links"][0]["slug"] == "codex-account-usage"
        from uuid import UUID

        async with database() as session:
            await session.execute(
                update(GuideArticleLocale)
                .where(
                    GuideArticleLocale.article_id == UUID(identifiers["codex-account-usage"]),
                    GuideArticleLocale.locale == locale,
                )
                .values(published_version=None)
            )
            await session.commit()
        after = (await api.get(f"/guides/life/codex-beginner-guide?locale={locale}")).json()
        assert after["series"]["next"] is None
        assert after["article_links"] == []
        directory = (await api.get(f"/guides/series/codex?locale={locale}")).json()
        assert [row["slug"] for row in directory["entries"]] == ["codex-beginner-guide"]


async def test_corrupt_public_pointer_never_falls_back_to_draft(database, actor):
    async with guides.client(guides.make_app(database, actor)) as api:
        await create(api, "claude-code-tutorials")
        await create(api, "claude-code-getting-started")
        async with database() as session:
            await session.execute(
                update(GuideArticleLocale).values(version=999999, published_version=999999)
            )
            await session.commit()
        assert (await api.get("/guides/series/claude-code")).status_code == 503


async def test_inline_affiliate_link_cannot_bypass_partner_disclosure(database, actor):
    value = rich_document()
    value["blocks"][-2]["inlines"][-1]["url"] = "https://example.com/product?affiliate_id=42"
    async with guides.client(guides.make_app(database, actor)) as api:
        response = await api.post(
            "/admin/guides",
            json={"slug": "blocked-link", "kind": "life", "topics": ["ai"], "document": value},
        )
        assert response.status_code == 422
        assert response.json()["code"] == "content_link_affiliate"


async def test_a_glossary_entry_names_its_set_and_the_hub_and_others_do_not(database, actor):
    """An article filed under a catalogue-type series' topic is an entry of that glossary
    (the web marks it up as a DefinedTerm); the hub itself and an article under another
    topic are not, and the set is named only while the hub is published here."""
    async with guides.client(guides.make_app(database, actor)) as api:
        hub = await guides.create_article(
            api, "ai-terms-index", "life", destination_id=None, topics=["ai", "ai-terms"],
            document=guides.document(title="AI 名詞總索引", description="所有名詞"),
        )
        entry = await guides.create_article(
            api, "ai-term-machine-learning", "life", destination_id=None, topics=["ai-terms"],
            document=guides.document(title="機器學習"),
        )
        other = await guides.create_article(
            api, "ai-news-today", "life", destination_id=None, topics=["ai-news"],
        )
        for created in (hub, entry, other):
            await guides.publish(api, created["id"], "zh-TW", created["version"])

        read = lambda slug: api.get(f"/guides/life/{slug}", params={"locale": "zh-TW"})  # noqa: E731
        assert (await read("ai-term-machine-learning")).json()["term_set"] == {
            "kind": "life",
            "slug": "ai-terms-index",
            "title": "AI 名詞總索引",
            "description": "所有名詞",
        }
        assert (await read("ai-terms-index")).json()["term_set"] is None
        assert (await read("ai-news-today")).json()["term_set"] is None

        detail = (await api.get(f"/admin/guides/{hub['id']}")).json()
        withdrawn = await api.post(
            f"/admin/guides/{hub['id']}/zh-TW/unpublish",
            json={
                "expected_version": detail["locales"][0]["version"],
                "confirmed": True,
                "reason": "下架",
            },
        )
        assert withdrawn.status_code == 200, withdrawn.text
        assert (await read("ai-term-machine-learning")).json()["term_set"] is None
