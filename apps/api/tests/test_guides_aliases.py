"""An article's other names: the editor's field on a pack and in the admin panel, the
keyword table as a seed source, and what the public read shows.
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID

import pytest
from sqlalchemy import select

from app.guides import aliases
from app.guides.content_pack import apply_import, load_packs, plan_import
from app.guides.models import GuideArticleAlias
from app.guides.search_cli import seed_guide_aliases
from tests import test_guides as guides
from tests.test_guides_content_pack import write_pack

database = guides.database
actor = guides.actor
client = guides.client
make_app = guides.make_app
document = guides.document
create_article = guides.create_article
publish = guides.publish


def taxonomy(article: dict, **overrides) -> dict:
    return {
        "expected_version": article["version"],
        "kind": "life",
        "destination_id": None,
        "topics": ["ai"],
        "valid_until": None,
        "featured": False,
        "display_order": 100,
        **overrides,
    }


async def stored(database, article_id: str) -> list[tuple[str, str, str]]:
    async with database() as session:
        rows = await session.scalars(
            select(GuideArticleAlias)
            .where(GuideArticleAlias.article_id == UUID(article_id))
            .order_by(GuideArticleAlias.locale, GuideArticleAlias.source, GuideArticleAlias.alias)
        )
        return [(row.locale, row.source, row.alias) for row in rows]


# --- the keyword table -------------------------------------------------------------


def test_the_keyword_table_names_the_primary_landing_or_its_fallback(tmp_path: Path) -> None:
    packs = tmp_path / "packs"
    packs.mkdir()
    for slug, locales in (("written", ["zh-TW", "en"]), ("fallback", ["zh-TW"]), ("cn", ["zh-CN"])):
        (packs / f"{slug}.json").write_text(
            json.dumps({"slug": slug, "locales": {locale: {} for locale in locales}}),
            encoding="utf-8",
        )
    table = tmp_path / "keywords.md"
    table.write_text(
        "\n".join(
            [
                "### 文字與工作",
                "",
                "| 關鍵字 | 變體 | 讀者要做的事 | 對應 slug | 狀態 | 動作 | 實際查詢 | 曝光 |",
                "| --- | --- | --- | --- | --- | --- | --- | --- |",
                "| 翻譯 AI | 日文翻譯 AI、英文翻譯 AI | 翻譯 | `written` | 已寫 | 補描述 |  |  |",
                "| 文案 AI | 貼文 AI | 文案 | `missing`；備 `fallback` | 待批次 09 | 帶入 |  |  |",
                "| 簡報 AI |  | 簡報 | `nothing` | 待批次 12 | 批次 12 |  |  |",
                "| 簡體 AI |  | 簡體 | `cn` | 已寫 |  |  |  |",
                "| 沒有 slug |  | x |  |  |  |  |  |",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    rows = aliases.keyword_aliases(table, packs)
    assert [(row.slug, row.locale, row.alias, row.source) for row in rows] == [
        ("written", "zh-TW", "翻譯 AI", "keyword"),
        ("written", "zh-TW", "日文翻譯 AI", "keyword"),
        ("written", "zh-TW", "英文翻譯 AI", "keyword"),
        ("fallback", "zh-TW", "文案 AI", "keyword"),
        ("fallback", "zh-TW", "貼文 AI", "keyword"),
        ("cn", "zh-CN", "簡體 AI", "keyword"),
    ]
    # Absent by default is fine; a named path that is missing is not.
    monkey = tmp_path / "missing.md"
    with pytest.raises(FileNotFoundError):
        aliases.keyword_aliases(monkey, packs)
    # And the glossary comes first in the merged seed, keeping its source on a shared name.
    terms = tmp_path / "aliases.json"
    terms.write_text(json.dumps({"written": ["翻譯 AI", "MT"]}), encoding="utf-8")
    merged = aliases.seed_rows(terms, packs, keywords_file=table)
    by_alias = {(row.slug, row.locale, row.alias): row.source for row in merged}
    assert by_alias[("written", "zh-TW", "翻譯 AI")] == "term"
    assert by_alias[("fallback", "zh-TW", "貼文 AI")] == "keyword"


def test_the_shipped_keyword_table_parses_to_names_of_shipped_packs() -> None:
    if not aliases.default_keywords_file().is_file():
        pytest.skip("the repository's docs are not on disk")
    rows = aliases.keyword_aliases()
    assert rows and all(row.locale in aliases.KEYWORD_LOCALES for row in rows)
    assert all(row.alias and len(row.alias) <= aliases.MAX_ALIAS_LENGTH for row in rows)


# --- the editor's field ---------------------------------------------------------------


async def test_the_editor_field_replaces_its_own_names_and_leaves_the_seeded_ones(
    database, actor, tmp_path: Path, monkeypatch
) -> None:
    async with client(make_app(database, actor)) as api:
        created = await create_article(
            api,
            slug="ai-term-machine-learning",
            kind="life",
            destination_id=None,
            topics=["ai-terms"],
            document=document(title="機器學習是什麼"),
        )
        await publish(api, created["id"], "zh-TW", created["version"])

    # Seed a glossary name first.
    packs = tmp_path / "packs"
    packs.mkdir()
    (packs / "ai-term-machine-learning.json").write_text(
        json.dumps({"slug": "ai-term-machine-learning", "locales": {"zh-TW": {}}}), encoding="utf-8"
    )
    terms = tmp_path / "aliases.json"
    terms.write_text(json.dumps({"machine-learning": ["ML"]}), encoding="utf-8")
    monkeypatch.setattr(aliases, "default_directory", lambda: packs)
    monkeypatch.setattr(aliases, "series_aliases", lambda: [])
    monkeypatch.setattr(aliases, "default_keywords_file", lambda: tmp_path / "absent.md")
    assert (await seed_guide_aliases(terms_file=terms, factory=database))["inserted"] == 1

    async with client(make_app(database, actor)) as api:
        detail = (await api.get(f"/admin/guides/{created['id']}")).json()
        assert detail["aliases"] == {}  # the seed's names are not the editor's to edit
        response = await api.put(
            f"/admin/guides/{created['id']}",
            json=taxonomy(
                detail,
                topics=["ai-terms"],
                aliases={"zh-TW": ["機器學習", " ml ", "Machine  Learning"]},
            ),
        )
        assert response.status_code == 200, response.text
        # ``ml`` folds to the seeded ``ML`` and is not written twice; spacing is tidied.
        assert response.json()["aliases"] == {"zh-TW": ["機器學習", "Machine Learning"]}
        assert await stored(database, created["id"]) == [
            ("zh-TW", "editor", "Machine Learning"),
            ("zh-TW", "editor", "機器學習"),
            ("zh-TW", "term", "ML"),
        ]
        # The index saw it: an exact name is now the best match.
        found = (
            await api.get("/guides/search", params={"locale": "zh-TW", "q": "機器學習"})
        ).json()
        assert found["best_match"]["slug"] == "ai-term-machine-learning"
        public = await api.get("/guides/life/ai-term-machine-learning", params={"locale": "zh-TW"})
        assert public.json()["aliases"] == ["ML", "機器學習", "Machine Learning"]

        # A payload without the field leaves the names alone; a listed locale replaces them,
        # and ``[]`` clears the editor's names while the seed's stay.
        version = response.json()["version"]
        untouched = await api.put(
            f"/admin/guides/{created['id']}",
            json=taxonomy({"version": version}, topics=["ai-terms"]),
        )
        assert untouched.json()["aliases"] == {"zh-TW": ["機器學習", "Machine Learning"]}
        cleared = await api.put(
            f"/admin/guides/{created['id']}",
            json=taxonomy({"version": version + 1}, topics=["ai-terms"], aliases={"zh-TW": []}),
        )
        assert cleared.json()["aliases"] == {}
        assert await stored(database, created["id"]) == [("zh-TW", "term", "ML")]
        # Too many names for one locale is refused by the schema.
        refused = await api.put(
            f"/admin/guides/{created['id']}",
            json=taxonomy(
                {"version": version + 2},
                topics=["ai-terms"],
                aliases={"zh-TW": [f"n{i}" for i in range(13)]},
            ),
        )
        assert refused.status_code == 422


# --- the pack field -------------------------------------------------------------------


async def test_pack_aliases_and_related_import_through_the_taxonomy_path(
    database, actor, tmp_path: Path
) -> None:
    write_pack(tmp_path, "narita-to-tokyo", aliases={"zh-TW": ["成田到東京", "Skyliner 攻略"]})
    write_pack(tmp_path, "tokyo-pass", related=["narita-to-tokyo"])
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        report = await apply_import(session, actor, plan, publish=True)
    assert report.failed is None
    # The names ride the create path (as ``featured`` does); the picks are the second pass.
    assert sorted(report.created) == [
        "narita-to-tokyo:en",
        "narita-to-tokyo:zh-TW",
        "tokyo-pass:en",
        "tokyo-pass:zh-TW",
    ]
    assert report.taxonomy_updated == ["tokyo-pass"]

    async with client(make_app(database, actor)) as api:
        rows = (await api.get("/admin/guides", params={"locale": "zh-TW"})).json()["articles"]
        by_slug = {row["slug"]: row for row in rows}
        narita = (await api.get(f"/admin/guides/{by_slug['narita-to-tokyo']['id']}")).json()
        assert narita["aliases"] == {"zh-TW": ["成田到東京", "Skyliner 攻略"]}
        tokyo = (await api.get(f"/admin/guides/{by_slug['tokyo-pass']['id']}")).json()
        assert tokyo["related"] == ["narita-to-tokyo"]
        public = (await api.get("/guides/howto/tokyo-pass", params={"locale": "zh-TW"})).json()
        assert [item["slug"] for item in public["related"]][:1] == ["narita-to-tokyo"]

    # Idempotent: the same packs plan as unchanged and write nothing.
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        assert [entry.taxonomy for entry in plan.articles] == ["unchanged", "unchanged"]
        report = await apply_import(session, actor, plan, publish=False)
    assert report.taxonomy_updated == []

    # Dropping the names from the pack clears them; a pick that names no pack fails the run.
    write_pack(tmp_path, "narita-to-tokyo")
    write_pack(tmp_path, "tokyo-pass", related=["nowhere"])
    async with database() as session:
        plan = await plan_import(session, load_packs(tmp_path))
        assert [entry.taxonomy for entry in plan.articles] == ["update", "update"]
        report = await apply_import(session, actor, plan, publish=False)
    assert report.failed == "related: guide_related_unknown: 延伸閱讀指定的文章不存在"
    async with client(make_app(database, actor)) as api:
        narita = (await api.get(f"/admin/guides/{by_slug['narita-to-tokyo']['id']}")).json()
        assert narita["aliases"] == {}
