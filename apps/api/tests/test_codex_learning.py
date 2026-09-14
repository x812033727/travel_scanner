"""Tutorial blocks remain inert, and the series is a complete navigable content pack."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.guides.content_pack import ArticlePack
from app.guides.schemas import GuideDocument

ROOT = Path(__file__).resolve().parents[3]


def document(block):
    return GuideDocument.model_validate({"title": "Test", "description": "Test", "blocks": [block]})


def test_code_preserves_markup_whitespace_and_line_endings():
    code = "<script>alert(1)</script>\r\n\tvalue = 1\n"
    parsed = document({"type": "code", "language": "html", "label": "HTML", "code": code})
    assert parsed.blocks[0].code == code


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "data:text/html,test",
        "https://u:p@example.com",
        "//example.com",
        "https://example.com/\n",
    ],
)
def test_inline_links_reject_unsafe_destinations(url):
    with pytest.raises(ValidationError):
        document(
            {"type": "rich_paragraph", "inlines": [{"type": "link", "text": "Read", "url": url}]}
        )


def test_inline_spacing_and_legacy_paragraphs():
    block = {
        "type": "rich_paragraph",
        "inlines": [
            {"type": "text", "text": "Read "},
            {"type": "link", "text": "more", "url": "https://example.com"},
            {"type": "text", "text": " here."},
        ],
    }
    assert "".join(span.text for span in document(block).blocks[0].inlines) == "Read more here."
    assert (
        document({"type": "paragraph", "text": "[literal](url)"}).blocks[0].text == "[literal](url)"
    )


def test_ready_lessons_have_five_locales_valid_images_and_existing_links():
    catalog = json.loads(
        (ROOT / "apps/web/lib/codex-learning/catalog.json").read_text(encoding="utf-8")
    )
    assert len(catalog) == 60
    assert [row["id"] for row in catalog] == list(range(1, 61))
    assert sorted(row["order"] for row in catalog) == list(range(1, 61))
    assert all(sum(row["unit"] == unit for row in catalog) == 6 for unit in "ABCDEFGHIJ")
    # Platform alternatives must be usable without completing a different OS.
    by_id = {row["id"]: row for row in catalog}
    assert all(by_id[id_]["prerequisites"] == [5] for id_ in [35, 36, 37])
    assert all(by_id[id_]["prerequisites"] == [4] for id_ in [38, 39])
    assert 40 not in by_id[15]["prerequisites"]  # Cloud does not require mobile pairing.
    known = {row["slug"] for row in catalog} | {"codex-learning-hub"}
    for row in catalog:
        if not row["ready"]:
            assert not (ROOT / f"apps/api/app/guides/content/{row['slug']}.json").exists()
        assert all(
            any(prereq["id"] == id_ and prereq["order"] < row["order"] for prereq in catalog)
            for id_ in row["prerequisites"]
        )
    ready = {row["slug"] for row in catalog if row["ready"]} | {"codex-learning-hub"}
    locales = {"zh-TW", "zh-CN", "en", "ja", "ko"}
    for slug in ready:
        path = ROOT / f"apps/api/app/guides/content/{slug}.json"
        pack = ArticlePack.model_validate_json(path.read_text(encoding="utf-8"))
        assert set(pack.locales) == locales
        for locale, doc in pack.locales.items():
            assert doc.sources and all(source.checked_on for source in doc.sources)
            assert doc.hero and (ROOT / "apps/web/public" / doc.hero.src.lstrip("/")).is_file()
            assert len([block for block in doc.blocks if block.type == "heading"]) >= 3
            for block in doc.blocks:
                if block.type == "image":
                    assert (ROOT / "apps/web/public" / block.src.lstrip("/")).is_file()
                if block.type == "rich_paragraph":
                    assert all(
                        node.slug in known for node in block.inlines if node.type == "article"
                    )
                links = (
                    [block.url]
                    if block.type == "link"
                    else [span.url for span in block.inlines if span.type == "link"]
                    if block.type == "rich_paragraph"
                    else []
                )
                for url in links:
                    if url.startswith("https://mokaair.com/"):
                        if url.startswith("https://mokaair.com/guides/"):
                            asset = url.removeprefix("https://mokaair.com/")
                            assert asset in {
                                "guides/codex-first-project/todo-practice.zip",
                                "guides/codex-skills/todo-acceptance.zip",
                                "guides/codex-skill-resources/todo-summary-practice.zip",
                                "guides/codex-csv-workshop/contacts-practice.zip",
                            }
                            assert (ROOT / "apps/web/public" / asset).is_file()
                            continue
                        assert url.startswith(f"https://mokaair.com/{locale}/life/")
                        # References may name planned lessons; the publication-aware
                        # renderer makes those references inert until actually public.
                        assert url.rsplit("/", 1)[-1] in known


def test_deep_drafts_preserve_code_sources_and_structures_across_locales():
    catalog = json.loads(
        (ROOT / "apps/web/lib/codex-learning/catalog.json").read_text(encoding="utf-8")
    )
    for slug in [row["slug"] for row in catalog if row["deepDraft"]]:
        pack = ArticlePack.model_validate_json(
            (ROOT / f"apps/api/app/guides/content/{slug}.json").read_text(encoding="utf-8")
        )
        reference = pack.locales["zh-TW"]
        for document in pack.locales.values():
            assert [
                "prose" if block.type in {"paragraph", "rich_paragraph"} else block.type
                for block in document.blocks
            ] == [
                "prose" if block.type in {"paragraph", "rich_paragraph"} else block.type
                for block in reference.blocks
            ]
            assert [
                (block.language, block.code) for block in document.blocks if block.type == "code"
            ] == [
                (block.language, block.code) for block in reference.blocks if block.type == "code"
            ]
            assert document.sources == reference.sources
            body = [block for block in document.blocks if block.type != "image"]
            assert body[0].type == body[-1].type == "rich_paragraph"
            assert body[0].inlines[0].slug == body[-1].inlines[0].slug == "codex-learning-hub"
        if slug == "codex-skills":
            sample = (
                ROOT / "docs/codex-learning/practice/skills/todo-acceptance/SKILL.md"
            ).read_text(encoding="utf-8")
            assert (
                next(
                    block.code
                    for block in reference.blocks
                    if block.type == "code" and block.language == "markdown"
                )
                == sample
            )
