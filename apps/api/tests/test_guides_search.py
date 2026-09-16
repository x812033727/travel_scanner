"""The reader's article search: what is indexed, when, and how a query is answered.

Reuses the guides fixtures (SQLite plus the optional PostgreSQL leg), so the index is
proven through the publish and withdraw endpoints that maintain it and the public endpoint
that reads it, never by poking rows in.
"""

from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from sqlalchemy import func, select, update

from app.guides import aliases, search
from app.guides import router as guides_router
from app.guides.models import GuideArticle, GuideArticleAlias, GuideSearchEntry
from app.guides.publication import today
from app.guides.schemas import GuideDocument
from app.guides.search_cli import reindex_guide_search, seed_guide_aliases
from app.problems import AppError
from tests import test_guides as guides

# The guides fixtures, registered here under their own names (see test_guide_partner_links).
database = guides.database
actor = guides.actor
client = guides.client
make_app = guides.make_app
document = guides.document
create_article = guides.create_article
publish = guides.publish
set_hidden = guides.set_hidden


@pytest.fixture(autouse=True)
def limiter(monkeypatch):
    """The search limiter fails open; here it never trips unless a test flips it."""
    over = AsyncMock(return_value=False)
    hit = AsyncMock()
    monkeypatch.setattr(guides_router, "over_named_rate_limit", over)
    monkeypatch.setattr(guides_router, "record_rate_limit_hit", hit)
    return over, hit


def prose(title: str, description: str, *body: str, heading: str | None = None) -> dict:
    """A document whose body is the given paragraphs, so a test controls where a term sits."""
    doc = document(title=title, description=description)
    # The shared fixture's source names Skyliner; a neutral one keeps the body the test's.
    doc["sources"][0]["title"] = "官方來源"
    doc["blocks"] = [
        *([{"type": "heading", "text": heading, "level": 2}] if heading else []),
        *({"type": "paragraph", "text": text} for text in body),
    ]
    return doc


async def published(api, slug: str, doc: dict, **extra) -> dict:
    """An article created and published in one go; returns the create response."""
    created = await create_article(api, slug=slug, document=doc, **extra)
    response = await publish(api, created["id"], extra.get("locale", "zh-TW"), created["version"])
    assert response.status_code == 200, response.text
    return created


async def find(api, q: str, **params) -> dict:
    response = await api.get("/guides/search", params={"locale": "zh-TW", "q": q, **params})
    assert response.status_code == 200, response.text
    return response.json()


async def slugs(api, q: str, **params) -> list[str]:
    return [hit["slug"] for hit in (await find(api, q, **params))["results"]]


async def entries(database) -> list[GuideSearchEntry]:
    async with database() as session:
        return list(await session.scalars(select(GuideSearchEntry)))


# --- keeping the index ---------------------------------------------------------


async def test_publishing_writes_the_row_and_withdrawing_deletes_it(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        doc = prose("東京地鐵一日券", "怎麼買最划算", "在自動售票機買。")
        created = await create_article(api, document=doc)
        assert await entries(database) == []

        await publish(api, created["id"], "zh-TW", created["version"])
        [entry] = await entries(database)
        assert entry.locale == "zh-TW"
        assert entry.revision_version == created["version"] + 1
        assert entry.title == "東京地鐵一日券"
        assert entry.title_norm == "東京地鐵一日券"
        assert "自動售票機" in entry.body_text
        assert (await find(api, "一日券"))["total"] == 1

        # A republished revision replaces the row rather than adding a second one.
        detail = await api.get(f"/admin/guides/{created['id']}", params={"locale": "zh-TW"})
        version = detail.json()["locales"][0]["version"]
        edited = await api.put(
            f"/admin/guides/{created['id']}/zh-TW/draft",
            json={
                "expected_version": version,
                "document": prose("東京地鐵二日券", "怎麼買最划算", "在自動售票機買。"),
            },
        )
        assert edited.status_code == 200, edited.text
        # A saved draft is not public: the index still says what readers see.
        [entry] = await entries(database)
        assert entry.title == "東京地鐵一日券"
        await publish(api, created["id"], "zh-TW", version + 1)
        [entry] = await entries(database)
        assert entry.title == "東京地鐵二日券"
        assert entry.revision_version == version + 2
        assert await slugs(api, "二日券") == ["narita-to-tokyo"]
        assert await slugs(api, "一日券") == []

        withdrawn = await api.post(
            f"/admin/guides/{created['id']}/zh-TW/unpublish",
            json={"expected_version": version + 2, "confirmed": True, "reason": "下架"},
        )
        assert withdrawn.status_code == 200, withdrawn.text
        assert await entries(database) == []
        assert (await find(api, "二日券"))["total"] == 0


async def test_hidden_and_expired_articles_leave_the_results_without_a_republication(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        hidden = await published(api, "hidden-one", prose("隱藏測試", "描述", "內文"))
        expired = await published(
            api, "expired-one", prose("過期測試", "描述", "內文"), kind="intel"
        )
        assert sorted(await slugs(api, "測試")) == ["expired-one", "hidden-one"]

        assert (await set_hidden(api, hidden["id"], hidden["version"])).status_code == 200
        assert await slugs(api, "測試") == ["expired-one"]
        # The row is kept: unhiding must not wait for the next publish.
        assert len(await entries(database)) == 2
        assert (
            await set_hidden(api, hidden["id"], hidden["version"] + 1, hidden=False)
        ).status_code == 200
        assert sorted(await slugs(api, "測試")) == ["expired-one", "hidden-one"]

    async with database() as session:
        await session.execute(
            update(GuideArticle)
            .where(GuideArticle.slug == "expired-one")
            .values(valid_until=today() - timedelta(days=1))
        )
        await session.commit()
    async with client(make_app(database, actor)) as api:
        assert await slugs(api, "測試") == ["hidden-one"]
        del expired


async def test_a_stale_row_is_invisible_rather_than_wrong(database, actor) -> None:
    """The row names the version it was built from; if the pointer moved without it (a
    write path that skipped the hook), the reader sees nothing rather than old text."""
    async with client(make_app(database, actor)) as api:
        await published(api, "stale", prose("版本測試", "描述", "內文"))
        assert await slugs(api, "版本") == ["stale"]
    async with database() as session:
        await session.execute(update(GuideSearchEntry).values(revision_version=99))
        await session.commit()
    async with client(make_app(database, actor)) as api:
        assert await slugs(api, "版本") == []


async def test_reindex_rebuilds_what_is_missing_and_drops_what_is_not_published(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        kept = await published(api, "kept", prose("保留的文章", "描述", "內文"))
        await published(api, "gone", prose("撤下的文章", "描述", "內文"), kind="intel")
        draft = await create_article(api, slug="draft-only", document=prose("草稿", "描述", "內文"))
        del draft, kept
    async with database() as session:
        # Simulate an index that never saw ``kept`` and still carries a withdrawn one.
        await session.execute(
            GuideSearchEntry.__table__.delete().where(
                GuideSearchEntry.article_id.in_(
                    select(GuideArticle.id).where(GuideArticle.slug == "kept")
                )
            )
        )
        gone = await session.scalar(select(GuideArticle).where(GuideArticle.slug == "gone"))
        assert gone is not None
        await session.execute(
            update(guides.GuideArticleLocale)
            .where(guides.GuideArticleLocale.article_id == gone.id)
            .values(published_version=None)
        )
        await session.commit()

    assert await reindex_guide_search(dry_run=True, factory=database) == {
        "dry_run": True, "indexed": 1, "unchanged": 0, "dropped": 1, "unavailable": 0,
    }
    # A dry run wrote nothing.
    assert [entry.title for entry in await entries(database)] == ["撤下的文章"]

    assert await reindex_guide_search(factory=database) == {
        "dry_run": False, "indexed": 1, "unchanged": 0, "dropped": 1, "unavailable": 0,
    }
    assert [entry.title for entry in await entries(database)] == ["保留的文章"]
    # Idempotent: a second run has nothing to do.
    assert await reindex_guide_search(factory=database) == {
        "dry_run": False, "indexed": 0, "unchanged": 1, "dropped": 0, "unavailable": 0,
    }


# --- the query ----------------------------------------------------------------


async def test_terms_are_folded_so_width_and_case_do_not_matter(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await published(
            api,
            "ml-course",
            prose("機器學習教學", "從零開始的 Machine LEARNING 課程", "第一課介紹 AI 與資料集。"),
            kind="life", destination_id=None, topics=["ai"],
        )
        assert await slugs(api, "機器學習") == ["ml-course"]
        assert await slugs(api, "ＡＩ") == ["ml-course"]  # full-width folds to ASCII
        assert await slugs(api, "machine learning") == ["ml-course"]
        assert await slugs(api, "MACHINE  Learning") == ["ml-course"]
        assert await slugs(api, "深度學習") == []


async def test_every_term_must_match(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await published(api, "narita", prose("成田機場交通", "描述", "Skyliner 最快。"))
        await published(
            api, "haneda", prose("羽田機場交通", "描述", "單軌電車最快。"), kind="intel"
        )
        assert sorted(await slugs(api, "機場")) == ["haneda", "narita"]
        assert await slugs(api, "機場 Skyliner") == ["narita"]
        assert await slugs(api, "機場 單軌") == ["haneda"]
        assert await slugs(api, "機場 新幹線") == []
        body = await find(api, "機場 Skyliner")
        assert body["results"][0]["matched"] == ["機場", "skyliner"]


async def test_like_metacharacters_match_literally(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await published(api, "percent", prose("折扣 50%% 起", "描述", "用 a_b 代碼。"))
        await published(api, "plain", prose("折扣 50 元起", "描述", "用 ab 代碼。"), kind="intel")
        assert await slugs(api, "50%%") == ["percent"]
        assert await slugs(api, "a_b") == ["percent"]
        assert sorted(await slugs(api, "折扣")) == ["percent", "plain"]
        assert await slugs(api, "%%%%") == []


@pytest.mark.parametrize("q", ["", "   ", "a", "a b c", "、，。", "%"])
async def test_a_query_with_nothing_to_search_for_is_422(database, q) -> None:
    async with client(make_app(database)) as api:
        response = await api.get("/guides/search", params={"locale": "zh-TW", "q": q})
        assert response.status_code == 422
        if q.strip():
            assert response.json()["code"] == "guide_search_query_invalid"


async def test_a_query_over_the_length_limit_is_422_not_truncated(database) -> None:
    async with client(make_app(database)) as api:
        response = await api.get("/guides/search", params={"locale": "zh-TW", "q": "東" * 101})
        assert response.status_code == 422


def test_parse_query_keeps_a_lone_cjk_character_and_at_most_six_terms() -> None:
    assert search.parse_query("雪") == ["雪"]
    assert search.parse_query("Next.js GPT-4 C++ C#") == ["next.js", "gpt-4", "c++", "c#"]
    assert search.parse_query("一 二 三 四 五 六 七 八") == ["一", "二", "三", "四", "五", "六"]
    assert search.parse_query("東京 東京 tokyo TOKYO") == ["東京", "tokyo"]
    with pytest.raises(AppError) as error:
        search.parse_query("x, y; z")
    assert error.value.code == "guide_search_query_invalid"


async def test_the_title_outranks_the_body_and_the_alias_names_the_best_match(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        in_body = await published(
            api, "in-body", prose("東京住宿區域比較", "描述", "從新宿到淺草，順便提到 JR Pass。")
        )
        in_title = await published(api, "in-title", prose("JR Pass 值得買嗎", "描述", "算給你看。"))
        in_heading = await published(
            api, "in-heading", prose("關西交通", "描述", "內文", heading="JR Pass 的替代方案"),
            kind="intel",
        )
        assert await slugs(api, "jr pass") == ["in-title", "in-heading", "in-body"]
        del in_body, in_heading

    async with database() as session:
        session.add(
            GuideArticleAlias(
                article_id=UUID(in_title["id"]), locale="zh-TW", alias="JR PASS",
                alias_norm="jr pass", source="editor",
            )
        )
        await session.commit()
    assert await reindex_guide_search(factory=database) == {
        "dry_run": False, "indexed": 0, "unchanged": 3, "dropped": 0, "unavailable": 0,
    }
    async with client(make_app(database, actor)) as api:
        # The alias is not in the row until it is refreshed: the seed does that itself,
        # and the reindex does not, since the published version did not move.
        body = await find(api, "JR Pass")
        assert body["best_match"]["slug"] == "in-title"
        # ...and the best match is not repeated in the ranked list below it.
        assert [hit["slug"] for hit in body["results"]] == ["in-heading", "in-body"]
        assert body["total"] == 2
        # A title that is the whole query is a best match too, without an alias.
        body = await find(api, "關西交通")
        assert body["best_match"]["slug"] == "in-heading"
        assert body["results"] == []
        # An alias only in the best-match table does not widen the substring match.
        assert (await find(api, "jr pass 東京"))["best_match"] is None


async def test_an_alias_several_articles_share_ranks_but_names_no_best_match(
    database, actor
) -> None:
    async with client(make_app(database, actor)) as api:
        one = await published(api, "cli-one", prose("安裝命令列", "描述", "第一課"))
        two = await published(
            api, "cli-two", prose("命令列常用指令", "描述", "第二課"), kind="intel"
        )
    async with database() as session:
        for article in (one, two):
            session.add(
                GuideArticleAlias(
                    article_id=UUID(article["id"]), locale="zh-TW", alias="CLI",
                    alias_norm="cli", source="series",
                )
            )
        await session.commit()
        for article in (one, two):
            assert await search.refresh_aliases(session, UUID(article["id"]), "zh-TW")
        await session.commit()
    async with client(make_app(database, actor)) as api:
        body = await find(api, "CLI")
        assert body["best_match"] is None
        assert sorted(hit["slug"] for hit in body["results"]) == ["cli-one", "cli-two"]


async def test_filters_narrow_the_results_the_same_way_the_listing_does(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        await published(api, "tokyo-howto", prose("東京交通攻略", "描述", "內文"))
        await published(
            api, "seoul-intel", prose("首爾交通優惠", "描述", "內文"), kind="intel",
            destination_id="seoul",
        )
        await published(
            api, "ai-life", prose("AI 交通預測工具", "描述", "內文"), kind="life",
            destination_id=None, topics=["ai-terms"],
        )
        assert sorted(await slugs(api, "交通")) == ["ai-life", "seoul-intel", "tokyo-howto"]
        assert sorted(await slugs(api, "交通", section="travel")) == ["seoul-intel", "tokyo-howto"]
        assert await slugs(api, "交通", section="life") == ["ai-life"]
        assert await slugs(api, "交通", kind="intel") == ["seoul-intel"]
        assert await slugs(api, "交通", destination="tokyo") == ["tokyo-howto"]
        assert await slugs(api, "交通", country="south-korea") == ["seoul-intel"]
        assert await slugs(api, "交通", country="atlantis") == []
        # A parent topic finds an article filed under its child.
        assert await slugs(api, "交通", topic="ai") == ["ai-life"]
        assert await slugs(api, "交通", topic="ai-terms") == ["ai-life"]
        assert await slugs(api, "交通", topic="nope") == []
        assert await slugs(api, "交通", section="life", kind="intel") == []


async def test_pages_never_overlap_and_say_when_there_is_more(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        for index in range(5):
            await published(
                api, f"page-{index}", prose(f"分頁測試 {index}", "描述", "內文"),
                kind="howto" if index % 2 else "intel",
            )
        first = await find(api, "分頁", limit=2)
        assert first["total"] == 5 and first["offset"] == 0 and first["limit"] == 2
        assert first["next_offset"] == 2
        second = await find(api, "分頁", limit=2, offset=2)
        assert second["next_offset"] == 4
        third = await find(api, "分頁", limit=2, offset=4)
        assert third["next_offset"] is None
        seen = [hit["slug"] for page in (first, second, third) for hit in page["results"]]
        assert len(seen) == 5 and len(set(seen)) == 5
        beyond = await find(api, "分頁", limit=2, offset=10)
        assert beyond["results"] == [] and beyond["total"] == 5
        for params in ({"limit": 21}, {"offset": 201}, {"limit": 0}):
            response = await api.get("/guides/search", params={"q": "x y", **params})
            assert response.status_code == 422, params


async def test_a_hit_carries_the_card_fields_a_passage_and_the_hero(database, actor) -> None:
    async with client(make_app(database, actor)) as api:
        doc = guides.rich_document(heading="先買車票")
        await published(api, "rich", doc)
        body = await find(api, "計程車")
        [hit] = body["results"]
        assert hit["kind"] == "howto" and hit["destination_label"] == "東京"
        assert [topic["slug"] for topic in hit["topics"]] == ["transport"]
        assert hit["hero"]["src"] == "/guides/narita-to-tokyo/hero.jpg"
        assert hit["title"] == doc["title"] and hit["published_at"]
        # The passage comes from the callout's text and is marked as cut on the left.
        assert "計程車" in hit["snippet"] and hit["snippet"].startswith("…")
        # A title-only match falls back to the description.
        [hit] = (await find(api, "怎麼走"))["results"]
        assert hit["snippet"] == doc["description"]


def test_document_text_takes_prose_from_every_block_and_nothing_else() -> None:
    doc = GuideDocument.model_validate(
        {
            **guides.rich_document(heading="先買車票"),
            "blocks": [
                *guides.rich_document(heading="先買車票")["blocks"],
                {"type": "list", "items": ["第一項", "第二項"], "ordered": True},
                {"type": "link", "text": "官方網站", "url": "https://example.com/secret-path"},
                {
                    "type": "rich_paragraph",
                    "inlines": [
                        {"type": "text", "text": "先讀 "},
                        {"type": "code", "text": "npm install"},
                        {"type": "link", "text": " 官方文件", "url": "https://example.com/docs"},
                        {
                            "type": "article", "text": "，再看名詞解釋", "kind": "life",
                            "slug": "ai-term-x",
                        },
                    ],
                },
                {
                    "type": "code", "language": "bash", "label": "安裝指令",
                    "code": "rm -rf ./node_modules",
                },
                {
                    "type": "partner_link", "partner": "example_partner",
                    "url": "https://partner.example/deal", "label": "合作方案", "note": "限時",
                },
            ],
        }
    )
    text = search.document_text(doc)
    assert text.title == doc.title and text.description == doc.description
    assert text.headings == ["三種選擇"]
    joined = " ".join(text.body)
    for expected in (
        "Skyliner 停在成田機場月台",  # hero alt
        "成田到東京的三條路線", "路線示意圖",  # image alt and caption
        "方式", "2,580 日圓", "2026 年 9 月查證",  # table header, cell, caption
        "注意", "末班車後只剩計程車。",  # callout
        "先買車票",  # offer heading
        # Inline nodes join without a separator (a link's text is stripped on validation).
        "第一項", "官方網站", "先讀 npm install官方文件，再看名詞解釋",
        "安裝指令", "合作方案", "限時", "Keisei Skyliner timetable",  # code label, partner, source
    ):
        assert expected in joined, expected
    for excluded in ("secret-path", "rm -rf", "partner.example", "route-map.svg", "ai-term-x"):
        assert excluded not in joined, excluded


def test_snippet_centres_on_the_first_term_and_falls_back_to_the_description() -> None:
    body = "前言。" + "甲" * 100 + "關鍵字在這裡" + "乙" * 100 + "結尾。"
    passage = search.snippet(body, "描述", ["關鍵字"])
    assert passage.startswith("…") and passage.endswith("…")
    assert "關鍵字在這裡" in passage and len(passage) <= 2 * search.SNIPPET_RADIUS + 2
    assert search.snippet("短內文 Keyword 在這", "描述", ["keyword"]) == "短內文 Keyword 在這"
    assert search.snippet("沒有這個詞", "描述", ["關鍵字"]) == "描述"
    long = "很長的描述" * 40
    assert search.snippet("", long, ["x"]) == long[: search.DESCRIPTION_SNIPPET] + "…"
    # ``ß`` casefolds to two letters but lowers to one, so the lower-cased pass still slices.
    assert search.snippet("Straße keyword", "描述", ["keyword"]) == "Straße keyword"
    # A body neither fold keeps the length of cannot be sliced safely: the description wins.
    assert search.snippet("İstanbul keyword", "描述", ["keyword"]) == "描述"


async def test_the_limiter_fails_open_and_answers_429_when_it_trips(
    database, actor, limiter
) -> None:
    over, hit = limiter
    async with client(make_app(database, actor)) as api:
        await published(api, "limited", prose("限流測試", "描述", "內文"))
        assert (await find(api, "限流"))["total"] == 1
        over.assert_awaited()
        assert over.await_args.args[0] == "guide-search"
        assert over.await_args.kwargs == {"limit": 120, "window_seconds": 60}
        hit.assert_not_awaited()

        over.return_value = True
        response = await api.get("/guides/search", params={"locale": "zh-TW", "q": "限流"})
        assert response.status_code == 429
        assert response.json()["code"] == "rate_limit_exceeded"
        hit.assert_awaited_once()


# --- the alias seed ------------------------------------------------------------


def write_pack(directory: Path, slug: str, locales: list[str]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{slug}.json").write_text(
        json.dumps({"slug": slug, "locales": {locale: {} for locale in locales}}),
        encoding="utf-8",
    )


def test_seed_rows_map_glossary_keys_to_packs_and_fold_duplicates(tmp_path, monkeypatch) -> None:
    packs = tmp_path / "packs"
    write_pack(packs, "ai-term-machine-learning", ["zh-TW", "en"])
    write_pack(packs, "plain-slug", ["zh-TW"])
    terms = tmp_path / "aliases.json"
    terms.write_text(
        json.dumps(
            {
                "machine-learning": ["ML", "機器學習", "ml", " "],
                "plain-slug": ["Plain"],
                "no-such-pack": ["Nothing"],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(aliases, "series_aliases", lambda: [])
    rows = aliases.seed_rows(terms, packs)
    assert [(row.slug, row.locale, row.alias, row.source) for row in rows] == [
        ("ai-term-machine-learning", "zh-TW", "ML", "term"),
        ("ai-term-machine-learning", "zh-TW", "機器學習", "term"),
        ("ai-term-machine-learning", "en", "ML", "term"),
        ("ai-term-machine-learning", "en", "機器學習", "term"),
        ("plain-slug", "zh-TW", "Plain", "term"),
    ]
    assert aliases.shared_aliases(rows) == {}
    # A missing default glossary (a container without docs/) seeds nothing from it; a path
    # the operator named and got wrong is an error.
    monkeypatch.setattr(aliases, "default_terms_file", lambda: tmp_path / "missing.json")
    assert aliases.seed_rows(None, packs) == []
    with pytest.raises(FileNotFoundError):
        aliases.seed_rows(tmp_path / "missing.json", packs)


def test_the_shipped_seed_is_well_formed() -> None:
    rows = aliases.seed_rows()
    assert rows, "the series catalogues alone should contribute aliases"
    assert all(row.alias_norm and len(row.alias) <= aliases.MAX_ALIAS_LENGTH for row in rows)
    assert {row.source for row in rows} <= {"term", "keyword", "series"}
    if aliases.default_terms_file().is_file():
        term_slugs = {row.slug for row in rows if row.source == "term"}
        assert term_slugs, "the glossary keys must map to shipped packs"
        assert all(slug.startswith("ai-term-") or "-" in slug for slug in term_slugs)


async def test_the_seed_inserts_once_refreshes_the_index_and_reports_the_rest(
    database, actor, tmp_path, monkeypatch
) -> None:
    packs = tmp_path / "packs"
    write_pack(packs, "ai-term-machine-learning", ["zh-TW"])
    write_pack(packs, "not-in-db", ["zh-TW"])
    terms = tmp_path / "aliases.json"
    terms.write_text(
        json.dumps({"machine-learning": ["ML", "機器學習"], "not-in-db": ["Nope"]}),
        encoding="utf-8",
    )
    monkeypatch.setattr(aliases, "default_directory", lambda: packs)
    monkeypatch.setattr(
        aliases,
        "series_aliases",
        lambda: [aliases.SeedAlias("ai-term-machine-learning", "zh-TW", "ml", "series")],
    )
    async with client(make_app(database, actor)) as api:
        await published(
            api, "ai-term-machine-learning",
            prose("機器學習是什麼", "一句話解釋", "讓電腦從資料中學規則。"),
            kind="life", destination_id=None, topics=["ai-terms"],
        )
        assert (await find(api, "ML"))["best_match"] is None

    dry = await seed_guide_aliases(terms_file=terms, dry_run=True, factory=database)
    assert dry == {
        "rows": 3, "dry_run": True, "inserted": 2, "unchanged": 0,
        "unknown_slugs": ["not-in-db"], "shared": {}, "reindexed": 0,
    }
    async with database() as session:
        assert await session.scalar(select(func.count()).select_from(GuideArticleAlias)) == 0

    wet = await seed_guide_aliases(terms_file=terms, factory=database)
    assert wet == {
        "rows": 3, "dry_run": False, "inserted": 2, "unchanged": 0,
        "unknown_slugs": ["not-in-db"], "shared": {}, "reindexed": 1,
    }
    async with client(make_app(database, actor)) as api:
        body = await find(api, "ML")
        assert body["best_match"]["slug"] == "ai-term-machine-learning"
        # The alias also ranks: the substring match sees it now.
        assert (await find(api, "ml 規則"))["total"] == 1
    # A second run changes nothing and says so.
    again = await seed_guide_aliases(terms_file=terms, factory=database)
    assert again["inserted"] == 0 and again["unchanged"] == 2 and again["reindexed"] == 0
    async with database() as session:
        sources = sorted(await session.scalars(select(GuideArticleAlias.source)))
        # ``ML`` and ``ml`` fold to one row; the glossary's came first and kept its source.
        assert sources == ["term", "term"]

    with pytest.raises(SystemExit):
        await seed_guide_aliases(terms_file=tmp_path / "missing.json", factory=database)
