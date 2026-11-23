"""The link graph: rows written at publish, the editor's picks, what to read next and
who cites this article. Proven through the endpoints the editor and the reader use.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import cast

import pytest
from sqlalchemy import Table, func, select, update

from app.guides import links
from app.guides.links_cli import check_guide_links, rebuild_guide_links
from app.guides.models import (
    GuideArticle,
    GuideArticleLink,
    GuideArticleLocale,
    GuideArticleRevision,
)
from app.guides.publication import today
from app.models import AdminAuditLog
from tests import test_guides as guides

database = guides.database
actor = guides.actor
client = guides.client
make_app = guides.make_app
document = guides.document
create_article = guides.create_article
publish = guides.publish
set_hidden = guides.set_hidden


def linking(title: str, *targets: tuple[str, str], description: str = "描述") -> dict:
    """A document whose text links each ``(kind, slug)`` target once, in order."""
    doc = document(title=title, description=description)
    doc["blocks"] = [
        {"type": "heading", "text": "一節", "level": 2},
        {
            "type": "rich_paragraph",
            "inlines": [
                {"type": "text", "text": "先讀 "},
                *(
                    {"type": "article", "text": f"目標 {slug}", "kind": kind, "slug": slug}
                    for kind, slug in targets
                ),
                {"type": "text", "text": " 再回來。"},
            ],
        },
    ]
    return doc


async def published(api, slug: str, doc: dict | None = None, **extra) -> dict:
    created = await create_article(api, slug=slug, document=doc or linking(slug), **extra)
    response = await publish(api, created["id"], extra.get("locale", "zh-TW"), created["version"])
    assert response.status_code == 200, response.text
    return created


async def public(api, kind: str, slug: str, locale: str = "zh-TW") -> dict:
    response = await api.get(f"/guides/{kind}/{slug}", params={"locale": locale})
    assert response.status_code == 200, response.text
    return response.json()


async def link_rows(database) -> list[tuple[str, str | None, int]]:
    async with database() as session:
        rows = await session.execute(
            select(
                GuideArticleLink.relation, GuideArticleLink.locale, GuideArticleLink.position
            ).order_by(GuideArticleLink.relation, GuideArticleLink.position)
        )
        return [tuple(row) for row in rows]


# --- the inline rows -----------------------------------------------------------


async def test_publishing_materializes_the_text_links_and_withdrawing_removes_them(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        target = await published(api, "target")
        # A link to itself and a link to nothing: neither becomes a row, the second is audited.
        source = await published(
            api,
            "source",
            linking("來源", ("howto", "target"), ("howto", "source"), ("life", "nowhere")),
        )
        assert await link_rows(database) == [("inline", "zh-TW", 0)]
        cited = (await public(api, "howto", "target"))["backlinks"]
        assert [item["slug"] for item in cited] == ["source"]

        async with database() as session:
            audit = await session.scalar(
                select(AdminAuditLog)
                .where(AdminAuditLog.action == "guide_article_published")
                .order_by(AdminAuditLog.created_at.desc())
            )
            assert audit is not None and audit.metadata_json["unresolved_links"] == ["life/nowhere"]

        # A republication with the link removed rewrites the rows.
        detail = (await api.get(f"/admin/guides/{source['id']}", params={"locale": "zh-TW"})).json()
        version = detail["locales"][0]["version"]
        edited = await api.put(
            f"/admin/guides/{source['id']}/zh-TW/draft",
            json={"expected_version": version, "document": linking("來源改")},
        )
        assert edited.status_code == 200, edited.text
        # The draft is not public: the row and the backlink stay until the republication.
        assert await link_rows(database) == [("inline", "zh-TW", 0)]
        await publish(api, source["id"], "zh-TW", version + 1)
        assert await link_rows(database) == []
        assert (await public(api, "howto", "target"))["backlinks"] == []

        # Withdrawing deletes the rows outright.
        again = await api.put(
            f"/admin/guides/{source['id']}/zh-TW/draft",
            json={
                "expected_version": version + 2,
                "document": linking("來源", ("howto", "target")),
            },
        )
        assert again.status_code == 200
        await publish(api, source["id"], "zh-TW", version + 3)
        assert await link_rows(database) == [("inline", "zh-TW", 0)]
        withdrawn = await api.post(
            f"/admin/guides/{source['id']}/zh-TW/unpublish",
            json={"expected_version": version + 4, "confirmed": True, "reason": "下架"},
        )
        assert withdrawn.status_code == 200, withdrawn.text
        assert await link_rows(database) == []
        del target


async def test_backlinks_and_related_show_only_what_the_reader_can_open(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await published(api, "target", kind="intel")
        hidden = await published(api, "hidden-source", linking("隱藏", ("intel", "target")))
        expired = await published(api, "expired-source", linking("過期", ("intel", "target")))
        other = await published(api, "ja-source", linking("日文", ("intel", "target")), locale="ja")
        fine = await published(api, "fine-source", linking("正常", ("intel", "target")))
        cited = (await public(api, "intel", "target"))["backlinks"]
        assert sorted(item["slug"] for item in cited) == [
            "expired-source",
            "fine-source",
            "hidden-source",
        ]
        assert (await public(api, "intel", "target", "ja"))["status"] == "unpublished"

        assert (await set_hidden(api, hidden["id"], hidden["version"])).status_code == 200
    async with database() as session:
        await session.execute(
            update(GuideArticle)
            .where(GuideArticle.slug == "expired-source")
            .values(valid_until=today() - timedelta(days=1))
        )
        await session.commit()
    async with client(make_app(database, actor)) as api:
        body = await public(api, "intel", "target")
        assert [item["slug"] for item in body["backlinks"]] == ["fine-source"]
        # And a reference carries the published description, for the definition card.
        assert body["backlinks"][0]["description"] == "描述"
        assert body["article_links"] == []
        del expired, other, fine


# --- the editor's picks and the reading list -----------------------------------


async def test_related_is_the_editors_picks_then_the_nearest_neighbours(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        me = await published(api, "me", kind="life", destination_id=None, topics=["ai", "ai-terms"])
        # Same sub-topic, same parent only, same parent through a sibling sub-topic,
        # unrelated, and a curated pick from a different section.
        sibling = await published(
            api, "same-subtopic", kind="life", destination_id=None, topics=["ai-terms"]
        )
        parent = await published(
            api, "same-parent", kind="life", destination_id=None, topics=["ai"]
        )
        cousin = await published(
            api, "cousin", kind="life", destination_id=None, topics=["ai-news"]
        )
        await published(api, "unrelated", kind="life", destination_id=None, topics=["tutorial"])
        pick = await published(api, "picked", kind="howto")
        del sibling, parent, cousin

        body = await public(api, "life", "me")
        # The sub-topic first; the parent's family (its own articles and its other
        # sub-topics') next, newest first.
        assert [item["slug"] for item in body["related"]] == [
            "same-subtopic",
            "cousin",
            "same-parent",
        ]

        # The editor's pick goes first; the rest fill up to four. Self and unknown are refused.
        for bad, code in ((["me"], "guide_related_self"), (["nope"], "guide_related_unknown")):
            response = await api.put(
                f"/admin/guides/{me['id']}",
                json={
                    "expected_version": me["version"],
                    "kind": "life",
                    "destination_id": None,
                    "topics": ["ai", "ai-terms"],
                    "valid_until": None,
                    "featured": False,
                    "display_order": 100,
                    "related": bad,
                },
            )
            assert response.status_code == 422 and response.json()["code"] == code
        response = await api.put(
            f"/admin/guides/{me['id']}",
            json={
                "expected_version": me["version"],
                "kind": "life",
                "destination_id": None,
                "topics": ["ai", "ai-terms"],
                "valid_until": None,
                "featured": False,
                "display_order": 100,
                "related": ["picked", "cousin"],
            },
        )
        assert response.status_code == 200, response.text
        assert response.json()["related"] == ["picked", "cousin"]
        body = await public(api, "life", "me")
        assert [item["slug"] for item in body["related"]] == [
            "picked",
            "cousin",
            "same-subtopic",
            "same-parent",
        ]
        assert body["related"][0]["kind"] == "howto"

        # A withdrawn pick makes room rather than leaving a gap.
        assert (await set_hidden(api, pick["id"], pick["version"])).status_code == 200
        body = await public(api, "life", "me")
        assert [item["slug"] for item in body["related"]] == [
            "cousin",
            "same-subtopic",
            "same-parent",
        ]

        # A payload without ``related`` leaves the picks alone; ``[]`` clears them.
        detail = (await api.get(f"/admin/guides/{me['id']}")).json()
        response = await api.put(
            f"/admin/guides/{me['id']}",
            json={
                "expected_version": detail["version"],
                "kind": "life",
                "destination_id": None,
                "topics": ["ai", "ai-terms"],
                "valid_until": None,
                "featured": False,
                "display_order": 100,
            },
        )
        assert response.json()["related"] == ["picked", "cousin"]
        response = await api.put(
            f"/admin/guides/{me['id']}",
            json={
                "expected_version": detail["version"] + 1,
                "kind": "life",
                "destination_id": None,
                "topics": ["ai", "ai-terms"],
                "valid_until": None,
                "featured": False,
                "display_order": 100,
                "related": [],
            },
        )
        assert response.json()["related"] == []


async def test_travel_articles_relate_by_destination(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await published(api, "tokyo-a", kind="howto", topics=["transport"])
        await published(api, "tokyo-b", kind="intel", topics=["budget"])
        await published(api, "seoul", kind="howto", destination_id="seoul", topics=["budget"])
        body = await public(api, "howto", "tokyo-a")
        # Nothing shares the topic; the city decides, and the other city stays out.
        assert [item["slug"] for item in body["related"]] == ["tokyo-b"]


async def test_related_pairs_the_release_with_its_system_card_in_the_published_language(
    database, actor
) -> None:
    release = "ai-news-openai-gpt-62-astra-sol-20261117"
    system_card = "ai-news-gpt-62-astra-sol-system-card-20261117"
    fifth_day = "ai-news-gpt-62-astra-sol-availability-20261112"
    wrong_locale = "ai-news-gpt-62-astra-sol-preview-20261117"
    newest = "ai-news-openai-voice-update-20261118"
    async with client(make_app(database, actor)) as api:
        for slug, locale, topic in [
            (release, "zh-TW", "ai-news"),
            (system_card, "zh-TW", "ai-news"),
            (fifth_day, "zh-TW", "ai-news"),
            ("ai-news-gpt-62-astra-sol-pricing-20261111", "zh-TW", "ai-news"),
            ("ai-news-gpt-62-astra-sol-glossary-20261117", "zh-TW", "ai-terms"),
            (wrong_locale, "ja", "ai-news"),
            ("ai-news-nvidia-stock-price-20261117", "zh-TW", "ai-news"),
            (newest, "zh-TW", "ai-news"),
        ]:
            await published(
                api,
                slug,
                kind="life",
                destination_id=None,
                topics=[topic],
                locale=locale,
                news_date=date.fromisoformat(slug[-8:]).isoformat(),
            )
        await published(api, "editors-pick")
        async with database() as session:
            source = (
                await session.scalars(select(GuideArticle).where(GuideArticle.slug == release))
            ).one()
            await links.set_related(
                session, source, await links.resolve_related(session, source, ["editors-pick"])
            )
            await session.commit()
        assert [item["slug"] for item in (await public(api, "life", release))["related"]] == [
            "editors-pick",
            system_card,
            fifth_day,
            newest,
        ]
        assert (await public(api, "life", system_card))["related"][0]["slug"] == release


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ("nvidia-board-ceo-search", "nvidia-stock-price"),
        ("amd-q3-2026-results", "intel-q3-2026-results"),
        ("united-blocks-ai-agents", "ebay-blocks-ai-agents"),
        ("claude-code-2-1-82-release", "claude-code-2-1-83-release"),
    ],
)
def test_news_subject_requires_more_than_a_vendor_or_generic_phrase(left, right) -> None:
    assert links._subject_overlap(left.split("-"), right.split("-")) == 0
    assert links._subject_overlap(right.split("-"), left.split("-")) == 0


async def test_related_reads_only_available_card_slots_and_replaces_damaged_pointers(
    database, actor, monkeypatch
) -> None:
    async with client(make_app(database, actor)) as api:
        slugs = [
            "topic-index",
            *(f"article-{index}" for index in range(8)),
            "bad-title",
            "missing-revision",
        ]
        for slug in slugs:
            await published(api, slug, kind="life", destination_id=None, topics=["tech-news"])
    async with database() as session:
        await session.execute(
            update(GuideArticleLocale)
            .where(
                GuideArticleLocale.article_id
                == select(GuideArticle.id)
                .where(GuideArticle.slug == "missing-revision")
                .scalar_subquery()
            )
            .values(version=9, published_version=9)
        )
        for slug, malformed in (
            ("bad-title", {"title": 42}),
            ("article-0", {"title": ["list"]}),
            ("article-1", {"title": {"wrong": "shape"}}),
            ("article-2", {"title": False}),
            ("article-3", {"description": "missing title"}),
            ("article-4", {"title": "42", "description": ["bad description"]}),
        ):
            await session.execute(
                update(GuideArticleRevision)
                .where(
                    GuideArticleRevision.article_locale_id
                    == select(GuideArticleLocale.id)
                    .join(GuideArticle, GuideArticle.id == GuideArticleLocale.article_id)
                    .where(GuideArticle.slug == slug)
                    .scalar_subquery(),
                    GuideArticleRevision.action == "published",
                )
                .values(document_json=malformed)
            )
        await session.commit()
        ids = (await session.scalars(select(GuideArticle.id))).all()
        references = await links.references_for(session, "zh-TW", list(ids))
        by_slug = {card.slug: card for card in references.values()}
        assert set(by_slug) == {"topic-index", *(f"article-{index}" for index in range(4, 8))}
        assert by_slug["article-4"].title == "42"
        assert by_slug["article-4"].description is None
        source = (
            await session.scalars(select(GuideArticle).where(GuideArticle.slug == "topic-index"))
        ).one()
        reads = []
        read = links._read_references

        def count_page(rows):
            page = list(rows)
            reads.append(len(page))
            return read(page)

        monkeypatch.setattr(links, "_read_references", count_page)
        cards = await links.related_articles(session, source, "zh-TW", limit=2)
        assert [card.slug for card in cards] == ["article-7", "article-6"]
        assert reads == [2, 1]


# --- the operator commands -------------------------------------------------------


async def test_rebuild_restores_missing_rows_and_drops_stale_ones(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await published(api, "target")
        await published(api, "source", linking("來源", ("howto", "target")))
        await published(api, "gone", linking("撤下", ("howto", "target")), kind="intel")
    async with database() as session:
        await session.execute(cast(Table, GuideArticleLink.__table__).delete())
        gone = await session.scalar(select(GuideArticle).where(GuideArticle.slug == "gone"))
        assert gone is not None
        # A withdrawal that bypassed the write path leaves the pointer clear and (after the
        # delete above) no row; the row must not come back.
        await session.execute(
            update(GuideArticleLocale)
            .where(GuideArticleLocale.article_id == gone.id)
            .values(published_version=None)
        )
        session.add(
            GuideArticleLink(
                source_article_id=gone.id,
                target_article_id=gone.id,
                locale="zh-TW",
                relation="inline",
                position=0,
            )
        )
        await session.commit()
    assert await rebuild_guide_links(dry_run=True, factory=database) == {
        "dry_run": True,
        "materialized": 2,
        "dropped": 1,
        "unavailable": 0,
        "unresolved": [],
    }
    async with database() as session:
        assert await session.scalar(select(func.count()).select_from(GuideArticleLink)) == 1
    assert (await rebuild_guide_links(factory=database))["materialized"] == 2
    assert await link_rows(database) == [("inline", "zh-TW", 0)]
    assert (await rebuild_guide_links(factory=database))["dropped"] == 0


async def test_the_check_lists_every_link_a_reader_cannot_follow(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await published(api, "target")
        hidden = await published(api, "hidden", kind="intel")
        draft = await create_article(api, slug="draft-only", document=document(title="草稿"))
        doc = linking(
            "來源",
            ("howto", "target"),
            ("life", "target"),
            ("intel", "hidden"),
            ("howto", "draft-only"),
            ("life", "nowhere"),
        )
        doc["blocks"].append(
            {"type": "link", "text": "raw", "url": "https://mokaair.com/zh-TW/life/target"}
        )
        await published(api, "source", doc)
        assert (await set_hidden(api, hidden["id"], hidden["version"])).status_code == 200
        del draft
    report = await check_guide_links(locale="zh-TW", factory=database)
    findings = {
        (item["target"], item["problem"])
        for item in report["findings"]
        if item["source"] == "source"
    }
    assert findings == {
        ("life/target", "wrong_kind"),
        ("intel/hidden", "hidden"),
        ("howto/draft-only", "unpublished"),
        ("life/nowhere", "missing"),
        ("https://mokaair.com/zh-TW/life/target", "raw_url"),
    }
    assert (await check_guide_links(locale="ja", factory=database))["findings"] == []
