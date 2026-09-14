"""Publication boundaries are identical for the directory, navigation and inline links."""

from datetime import date, timedelta

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
    (catalogue,) = catalogues()
    assert len(catalogue.entries) == 60
    assert len(catalogue.groups) == 10
    assert len(catalogue.paths) == 5
    assert catalogue.hub == "claude-code-tutorials"


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
async def test_unavailable_targets_leave_no_public_navigation_or_inline_link(
    database, actor, state
):
    async with guides.client(guides.make_app(database, actor)) as api:
        await create(api, "claude-code-tutorials")
        await create(api, "claude-code-getting-started", doc=rich_document())
        target = await create(api, "claude-code-accounts-and-access")
        before = (await api.get("/guides/life/claude-code-getting-started")).json()
        assert before["article_links"][0]["slug"] == "claude-code-accounts-and-access"
        assert before["series"]["next"]["slug"] == "claude-code-accounts-and-access"
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
                    .values(valid_until=date.today() - timedelta(days=1))
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
        after = (await api.get("/guides/life/claude-code-getting-started")).json()
        assert after["article_links"] == []
        assert after["series"]["next"] is None
        directory = (await api.get("/guides/series/claude-code")).json()
        assert [entry["number"] for entry in directory["entries"]] == [1]
        assert all(
            "claude-code-accounts-and-access" not in path["slugs"] for path in directory["paths"]
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
