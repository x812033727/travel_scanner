"""``relink`` and ``autolink``: pure rewrites of a pack's blocks, proven on packs in a
temporary directory so the rules are the subject, not the corpus.

The corpus itself is covered by ``test_guides_content_links`` (which imports ``SITE_LINK``
from here) and by ``pack_cli lint``'s ``raw_internal_url`` warning.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.guides import autolink
from app.guides.autolink import AliasIndex, autolink_document, parse_site_link, relink_document
from app.guides.pack_cli import main
from app.guides.schemas import GuideDocument, Kind


def pack(slug: str, blocks: list[dict], *, kind: str = "life", aliases: dict | None = None) -> dict:
    return {
        "slug": slug,
        "kind": kind,
        "destination_id": None if kind == "life" else "tokyo",
        "topics": ["ai"] if kind == "life" else ["transport"],
        "valid_until": None,
        "featured": False,
        "display_order": 100,
        **({"aliases": aliases} if aliases else {}),
        "locales": {
            "zh-TW": {
                "title": f"{slug} 標題",
                "description": "一句描述。",
                "blocks": blocks,
                "sources": [
                    {"title": "來源", "url": "https://example.com/", "checked_on": "2026-09-01"}
                ],
            }
        },
    }


def write(directory: Path, *packs: dict) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    for item in packs:
        (directory / f"{item['slug']}.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return directory


KINDS: dict[str, Kind] = {"ai-term-fine-tuning": "life", "narita-to-tokyo": "howto", "me": "life"}


def test_site_links_name_an_article_only_under_a_locale_and_an_article_route() -> None:
    assert parse_site_link("https://mokaair.com/zh-TW/life/ai-term-fine-tuning") == (
        autolink.SiteLink("life", "ai-term-fine-tuning", "")
    )
    assert parse_site_link("https://mokaair.com/en/guides/howto/narita-to-tokyo?utm=x") == (
        autolink.SiteLink("howto", "narita-to-tokyo", "?utm=x")
    )
    for url in (
        "https://mokaair.com/zh-TW/destinations/tokyo",
        "https://mokaair.com/guides/codex-learning-hub",  # web-only series route, no locale
        "https://mokaair.com/zh-TW/guides",
        "https://example.com/zh-TW/life/x",
    ):
        assert parse_site_link(url) is None, url


def test_relink_turns_article_links_into_inlines_and_keeps_the_rest() -> None:
    document = {
        "blocks": [
            {
                "type": "link",
                "text": "微調是什麼",
                "url": "https://mokaair.com/zh-TW/life/ai-term-fine-tuning",
            },
            {
                "type": "link",
                "text": "帶著 query",
                "url": "https://mokaair.com/zh-TW/guides/howto/narita-to-tokyo?ref=a",
            },
            {"type": "link", "text": "自己", "url": "https://mokaair.com/zh-TW/life/me"},
            {
                "type": "link",
                "text": "錯的 kind",
                "url": "https://mokaair.com/zh-TW/life/narita-to-tokyo",
            },
            {"type": "link", "text": "沒有包", "url": "https://mokaair.com/zh-TW/life/nowhere"},
            {
                "type": "link",
                "text": "目的地",
                "url": "https://mokaair.com/zh-TW/destinations/tokyo",
            },
            {"type": "link", "text": "外站", "url": "https://example.com/"},
            {
                "type": "rich_paragraph",
                "inlines": [
                    {"type": "text", "text": "先讀 "},
                    {
                        "type": "link",
                        "text": "微調",
                        "url": "https://mokaair.com/zh-TW/life/ai-term-fine-tuning",
                    },
                    {"type": "link", "text": "文件", "url": "https://example.com/docs"},
                ],
            },
        ]
    }
    rewritten, report = relink_document(document, self_slug="me", kinds=KINDS, locale="zh-TW")
    assert report.converted == 3
    assert [reason for _, _, reason in report.kept] == [
        "self_link",
        "wrong_kind",
        "no_pack",
        "not_an_article",
    ]
    blocks = rewritten["blocks"]
    assert blocks[0] == {
        "type": "rich_paragraph",
        "inlines": [
            {"type": "article", "text": "微調是什麼", "kind": "life", "slug": "ai-term-fine-tuning"}
        ],
    }
    # The query string is dropped: an article has one address.
    assert blocks[1]["inlines"] == [
        {"type": "article", "text": "帶著 query", "kind": "howto", "slug": "narita-to-tokyo"}
    ]
    assert blocks[2:7] == document["blocks"][2:7]
    assert blocks[7]["inlines"][1] == {
        "type": "article",
        "text": "微調",
        "kind": "life",
        "slug": "ai-term-fine-tuning",
    }
    assert blocks[7]["inlines"][2] == document["blocks"][7]["inlines"][2]
    # The rewritten document still validates as a guide document.
    GuideDocument.model_validate(
        {"title": "t", "description": "d", "blocks": blocks, "sources": []}
    )
    # Idempotent: nothing left to convert.
    again, report = relink_document(rewritten, self_slug="me", kinds=KINDS, locale="zh-TW")
    assert report.converted == 0 and again == rewritten


@pytest.fixture
def index(tmp_path: Path) -> AliasIndex:
    """A glossary of two terms plus one pack-written name, with a shared name left out."""
    packs = write(
        tmp_path / "packs",
        pack(
            "ai-term-fine-tuning",
            [{"type": "paragraph", "text": "內文"}],
            aliases={"zh-TW": ["Fine-tuning"]},
        ),
        pack("ai-term-machine-learning", [{"type": "paragraph", "text": "內文"}]),
        pack("shared-a", [{"type": "paragraph", "text": "x"}], aliases={"zh-TW": ["共用"]}),
        pack("shared-b", [{"type": "paragraph", "text": "x"}], aliases={"zh-TW": ["共用", "b"]}),
        pack("me", [{"type": "paragraph", "text": "x"}], aliases={"zh-TW": ["我自己"]}),
    )
    terms = tmp_path / "aliases.json"
    terms.write_text(
        json.dumps(
            {
                "fine-tuning": ["微調", "FT"],
                "machine-learning": ["機器學習", "ML", "machine learning"],
            }
        ),
        encoding="utf-8",
    )
    keywords = tmp_path / "keywords.md"
    keywords.write_text(
        "| 關鍵字 | 變體 | 讀者要做的事 | 對應 slug | 狀態 |\n| --- | --- | --- | --- | --- |\n"
    )
    return AliasIndex.build(packs, terms_file=terms, keywords_file=keywords)


def test_the_index_keeps_only_names_that_point_at_one_article(index: AliasIndex) -> None:
    aliases = [term.alias for term in index.terms["zh-TW"]]
    assert "共用" not in aliases  # two owners: a ranking hint, not a link target
    assert "b" not in aliases  # too short
    assert "Fine-tuning" in aliases and "微調" in aliases and "machine learning" in aliases
    # Longest first, so ``machine learning`` is tried before ``ML``.
    assert aliases.index("machine learning") < aliases.index("ML")


def test_autolink_links_the_first_mention_once_with_word_boundaries(index: AliasIndex) -> None:
    document = {
        "blocks": [
            {"type": "heading", "text": "微調不在標題連", "level": 2},
            {
                "type": "paragraph",
                "text": (
                    "OpenAI 與 EMAIL 都不是 ML。真正的 ML 才連，machine learning 已經連過就不再連。"
                ),
            },
            {
                "type": "paragraph",
                "text": "第二段再提微調與 ML 都不會再連；fine-TUNING 也不會，因為目標已經連過。",
            },
            {"type": "list", "items": ["清單裡的微調不連"], "ordered": False},
            {
                "type": "rich_paragraph",
                "inlines": [
                    {"type": "text", "text": "文字 inline 的機器學習會連，"},
                    {"type": "code", "text": "ML"},
                    {"type": "text", "text": " 程式碼不連。"},
                ],
            },
        ]
    }
    rewritten, linked = autolink_document(document, locale="zh-TW", self_slug="other", index=index)
    assert [(item.alias, item.slug) for item in linked] == [
        ("ML", "ai-term-machine-learning"),
        ("微調", "ai-term-fine-tuning"),
    ]
    first = rewritten["blocks"][1]
    assert first["type"] == "rich_paragraph"
    # The first mention is the one linked: inside ``OpenAI`` and ``EMAIL`` is no mention.
    assert first["inlines"] == [
        {"type": "text", "text": "OpenAI 與 EMAIL 都不是 "},
        {"type": "article", "text": "ML", "kind": "life", "slug": "ai-term-machine-learning"},
        {"type": "text", "text": "。真正的 ML 才連，machine learning 已經連過就不再連。"},
    ]
    second = rewritten["blocks"][2]
    assert second["inlines"][:2] == [
        {"type": "text", "text": "第二段再提"},
        {"type": "article", "text": "微調", "kind": "life", "slug": "ai-term-fine-tuning"},
    ]
    assert rewritten["blocks"][0] == document["blocks"][0]
    assert rewritten["blocks"][3] == document["blocks"][3]
    # Machine learning was linked (as ``ML``) already, so the inline text is left alone.
    assert rewritten["blocks"][4] == document["blocks"][4]
    GuideDocument.model_validate(
        {"title": "t", "description": "d", "blocks": rewritten["blocks"], "sources": []}
    )
    # Deterministic and idempotent.
    again, more = autolink_document(rewritten, locale="zh-TW", self_slug="other", index=index)
    assert more == [] and again == rewritten


def test_autolink_never_links_an_article_to_itself_and_respects_existing_links_and_the_cap(
    index: AliasIndex,
) -> None:
    document = {
        "blocks": [
            {
                "type": "rich_paragraph",
                "inlines": [
                    {"type": "text", "text": "已經手動連了"},
                    {
                        "type": "article",
                        "text": "微調",
                        "kind": "life",
                        "slug": "ai-term-fine-tuning",
                    },
                ],
            },
            {"type": "paragraph", "text": "我自己 這個名字指向這篇，微調已經連過，ML 可以連。"},
        ]
    }
    rewritten, linked = autolink_document(document, locale="zh-TW", self_slug="me", index=index)
    assert [item.slug for item in linked] == ["ai-term-machine-learning"]
    _, capped = autolink_document(document, locale="zh-TW", self_slug="me", index=index, limit=0)
    assert capped == []


def test_the_command_reports_and_applies_only_the_changed_packs(tmp_path: Path, capsys) -> None:
    content = write(
        tmp_path / "content",
        pack("ai-term-fine-tuning", [{"type": "paragraph", "text": "內文"}]),
        pack(
            "reader",
            [
                {
                    "type": "link",
                    "text": "微調",
                    "url": "https://mokaair.com/zh-TW/life/ai-term-fine-tuning",
                },
                {"type": "paragraph", "text": "這裡提到微調。"},
            ],
        ),
        pack("untouched", [{"type": "paragraph", "text": "沒有連結。"}]),
    )
    assert main(["--content-dir", str(content), "relink", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "| `reader` | 1 | - |" in out and "1 of 3 packs would change" in out
    assert "dry run: nothing written" in out
    assert (
        "link"
        == json.loads((content / "reader.json").read_text())["locales"]["zh-TW"]["blocks"][0][
            "type"
        ]
    )

    assert main(["--content-dir", str(content), "relink", "--apply"]) == 0
    written = json.loads((content / "reader.json").read_text(encoding="utf-8"))
    assert written["locales"]["zh-TW"]["blocks"][0]["type"] == "rich_paragraph"
    # Only the blocks moved: every other key and the file's shape are as they were.
    assert (content / "reader.json").read_text(encoding="utf-8") == json.dumps(
        written, ensure_ascii=False, indent=2
    ) + "\n"
    assert json.loads((content / "untouched.json").read_text())["locales"]["zh-TW"]["blocks"] == [
        {"type": "paragraph", "text": "沒有連結。"}
    ]

    # Autolink over the same packs uses the packs' own names; with no glossary here the
    # target has no alias, so nothing links -- the command still runs and says so.
    assert main(["--content-dir", str(content), "autolink", "--prefix", "read"]) == 0
    assert "0 of 1 packs would change" in capsys.readouterr().out
