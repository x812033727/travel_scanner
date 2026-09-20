"""Content-bundle safety checks; these tests do not write to an application database."""

import copy
import importlib.util
import json
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "assemble_bundle", Path(__file__).with_name("assemble_bundle.py")
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def document():
    return {
        "title": "A complete translated article",
        "description": "An explanatory description",
        "hero": None,
        "blocks": [
            {
                "type": "paragraph",
                "text": "Retain the original audience and every condition.",
            },
            {
                "type": "code",
                "language": "markdown",
                "label": "notes.md",
                "code": "# 原文\nhttps://mokaair.com/zh-TW/life/lesson-one",
            },
        ],
        "sources": [
            {
                "title": "Official source",
                "url": "https://example.org/docs",
                "checked_on": "2026-09-14",
            }
        ],
    }


def test_links_follow_publication_without_rewriting_code_or_sources():
    before = document()
    before["blocks"] += [
        {
            "type": "link",
            "text": "Private lesson",
            "url": "https://mokaair.com/zh-TW/guides/howto/lesson-one",
        },
        {
            "type": "rich_paragraph",
            "inlines": [
                {"type": "text", "text": "Read "},
                {
                    "type": "link",
                    "text": "Lesson",
                    "url": "https://mokaair.com/zh-TW/life/lesson-one",
                },
            ],
        },
        {
            "type": "link",
            "text": "Trips",
            "url": "https://mokaair.com/zh-TW/trips?view=all",
        },
        {"type": "link", "text": "External", "url": "https://example.org/zh-TW/docs"},
    ]
    immutable = copy.deepcopy(before)
    result, changes = module.localize_links(
        before, "ja", {"lesson-one": {"kind": "life"}}
    )
    assert before == immutable
    assert result["blocks"][1] == before["blocks"][1]
    assert result["sources"] == before["sources"]
    reference = result["blocks"][2]["inlines"][0]
    assert reference == {
        "type": "article",
        "text": "Private lesson",
        "kind": "life",
        "slug": "lesson-one",
    }
    assert "url" not in result["blocks"][3]["inlines"][1]
    assert result["blocks"][4]["url"] == "https://mokaair.com/ja/trips?view=all"
    assert result["blocks"][5]["url"] == "https://example.org/zh-TW/docs"
    assert len(changes) == 3


def test_unknown_and_fragment_links_require_review_instead_of_silent_damage():
    value = document()
    value["blocks"].append(
        {"type": "link", "text": "Lesson", "url": "https://mokaair.com/en/life/missing"}
    )
    with pytest.raises(ValueError, match="Unknown internal article"):
        module.localize_links(value, "ko", {})
    value["blocks"][-1]["url"] += "#details"
    with pytest.raises(ValueError, match="query/fragment"):
        module.localize_links(value, "ko", {})


def test_existing_locale_can_change_image_paths_but_not_reader_text():
    before = document()
    before["hero"] = {"src": "/guides/a/hero.jpg", "alt": "Existing translated alt"}
    after = copy.deepcopy(before)
    after["hero"]["src"] = "/guides/a/hero-en.jpg"
    assert module.only_image_paths_changed(before, after)
    after["blocks"][0]["text"] = "Accidentally overwrite the existing editor's work"
    assert not module.only_image_paths_changed(before, after)


def test_review_is_bound_to_document_and_asset_bytes(tmp_path):
    doc = module.GuideDocument.model_validate(document()).model_dump(mode="json")
    source_document = copy.deepcopy(doc)
    source_document["title"] = "A different source-language article"
    article = {
        "slug": "a-lesson",
        "locale_documents": {"en": doc},
        "source_document": source_document,
    }
    data = {
        "source.json": {
            "source_sha256": module.digest(doc),
            "job_sha256": "a" * 64,
            "fields": {},
        },
        "fields.json": {},
        "translated-fields.json": {},
        "render-receipt.json": {},
        "document.json": copy.deepcopy(doc),
        "receipt.json": {
            "status": "rendered",
            "job_sha256": "a" * 64,
            "automated_layout_passed": True,
            "document_sha256": module.digest(doc),
            "raster_review_required": [],
        },
        "review.json": {
            "text_reviewed": True,
            "visual_reviewed": True,
            "glyph_reviewed": True,
            "document_sha256": module.digest(doc),
            "assets": {},
        },
        "assets.json": [],
    }
    for filename, content in data.items():
        (tmp_path / filename).write_text(json.dumps(content), encoding="utf-8")
    binding = module.pipeline.bind_artifacts(
        tmp_path, data["source.json"], "rendered", True
    )
    for filename in ["receipt.json", "review.json"]:
        data[filename].update(binding)
        (tmp_path / filename).write_text(json.dumps(data[filename]), encoding="utf-8")
    assert module.reviewed_document(tmp_path, article, "en")[0] == doc
    data["document.json"]["title"] = "Edited after review"
    (tmp_path / "document.json").write_text(
        json.dumps(data["document.json"]), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="staged artifact changed"):
        module.reviewed_document(tmp_path, article, "en")


def test_parallel_asset_edit_cannot_inherit_reviewed_hash(tmp_path, monkeypatch):
    source = tmp_path / "hero.svg"
    target = tmp_path / "copy.svg"
    source.write_text("reviewed SVG", encoding="utf-8")
    expected = module.sha(source)
    copyfile = module.shutil.copyfile

    def changed_copy(original, destination):
        original.write_text("unreviewed concurrent edit", encoding="utf-8")
        return copyfile(original, destination)

    monkeypatch.setattr(module.shutil, "copyfile", changed_copy)
    with pytest.raises(ValueError, match="Asset changed while copying"):
        module.copy_pinned_asset(source, target, expected)


def test_release_text_and_reviewed_svg_require_portable_lf_bytes(tmp_path):
    text = tmp_path / "portable.json"
    module.write_text_lf(text, '{\r\n  "ok": true\r\n}\r\n')
    assert text.read_bytes() == b'{\n  "ok": true\n}\n'

    svg = tmp_path / "reviewed.svg"
    copied = tmp_path / "copied.svg"
    svg.write_bytes(b"<svg>\r\n</svg>\r\n")
    with pytest.raises(ValueError, match="must use LF"):
        module.copy_pinned_asset(svg, copied, module.sha(svg))

    svg.write_bytes(b"<svg> \n</svg>\n")
    with pytest.raises(ValueError, match="trailing whitespace"):
        module.copy_pinned_asset(svg, copied, module.sha(svg))


def test_large_or_duplicate_batch_is_refused_before_any_io(tmp_path):
    for slugs in (["same", "same"], [f"article-{i}" for i in range(21)], []):
        with pytest.raises(ValueError, match="one to twenty"):
            module.assemble(
                tmp_path / "missing.json", tmp_path, slugs, tmp_path / "output"
            )
    assert not (tmp_path / "output").exists()


def test_hub_requires_public_catalogue_lessons_even_without_body_links(
    tmp_path, monkeypatch
):
    root = tmp_path / "apps/api/app/guides/series_data"
    root.mkdir(parents=True)
    (root / "gemini.json").write_text(
        json.dumps(
            {
                "hub": "gemini-guide",
                "entries": [{"slug": "public-lesson"}, {"slug": "private-lesson"}],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(module, "ROOT", tmp_path)
    doc = module.GuideDocument.model_validate(document())
    pack = module.ArticlePack.model_validate(
        {
            "slug": "gemini-guide",
            "kind": "life",
            "locales": {"en": doc},
        }
    )
    articles = {
        "gemini-guide": {"slug": "gemini-guide", "status": "published"},
        "public-lesson": {
            "status": "published",
            "published_locales": [],
            "database": {"locales": {}},
        },
        "private-lesson": {
            "status": "draft",
            "published_locales": [],
            "database": None,
        },
    }
    packs = [(articles["gemini-guide"], pack, ["en"])]
    with pytest.raises(ValueError, match="public-lesson:en"):
        module.hub_requirements(packs, articles)
    articles["public-lesson"].update(
        {
            "published_locales": ["en"],
            "database": {"locales": {"en": {"published_sha256": "a" * 64}}},
        }
    )
    assert module.hub_requirements(packs, articles) == {
        "gemini-guide": [
            {"slug": "public-lesson", "locale": "en", "document_sha256": "a" * 64}
        ],
    }


def test_unchanged_reviewed_database_draft_is_selected_and_published(
    tmp_path, monkeypatch
):
    root = tmp_path / "repo"
    pack_path = root / "apps/api/app/guides/content/public-article.json"
    pack_path.parent.mkdir(parents=True)
    locale_documents = {
        locale: module.GuideDocument.model_validate(document()).model_dump(mode="json")
        for locale in module.LOCALES
    }
    pack = {
        "slug": "public-article",
        "kind": "life",
        "locales": locale_documents,
    }
    pack_path.write_text(json.dumps(pack), encoding="utf-8")
    baseline = {
        "schema_version": 1,
        "articles": [
            {
                "slug": "public-article",
                "status": "published",
                "pack_path": pack_path.relative_to(root).as_posix(),
                "pack_sha256": module.sha(pack_path),
                "metadata": {
                    "slug": "public-article",
                    "kind": "life",
                    "destination_id": None,
                    "topics": [],
                    "valid_until": None,
                    "featured": False,
                    "display_order": 100,
                },
                "source_document": locale_documents["zh-TW"],
                "source_sha256": module.digest(locale_documents["zh-TW"]),
                "locale_documents": locale_documents,
                "existing_locales": list(module.LOCALES),
                "missing_locales": [],
                "translation_missing_locales": [],
                "publication_missing_locales": ["en"],
                "publication_locales": ["en"],
                "target_locales": ["en"],
                "batch_locales": ["en"],
                "locale_provenance": {
                    locale: (
                        "database-draft" if locale == "en" else "database-published"
                    )
                    for locale in module.LOCALES
                },
                "published_locales": [
                    locale for locale in module.LOCALES if locale != "en"
                ],
                "database": {"id": "article-id", "version": 7, "locales": {}},
                "assets": [],
            }
        ],
    }
    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
    work = tmp_path / "work"
    review_job = work / "public-article/en"
    review_job.mkdir(parents=True)
    (review_job / "document.json").write_text("{}", encoding="utf-8")

    def reviewed(directory, article, locale):
        assert directory == review_job
        assert locale == "en"
        return copy.deepcopy(article["locale_documents"][locale]), []

    monkeypatch.setattr(module, "ROOT", root)
    monkeypatch.setattr(module, "reviewed_document", reviewed)
    manifest = module.assemble(
        baseline_path,
        work,
        ["public-article"],
        tmp_path / "bundle",
    )
    assert manifest["articles"][0]["locales"] == ["en"]
    assert manifest["articles"][0]["publish_locales"] == ["en"]
    assembled = json.loads(
        (tmp_path / "bundle/packs/public-article.json").read_text(encoding="utf-8")
    )
    assert assembled["locales"]["en"] == locale_documents["en"]


def test_stale_baseline_without_split_targets_is_refused():
    article = {
        "slug": "old-baseline",
        "locale_documents": {"zh-TW": document()},
        "published_locales": ["zh-TW"],
        "missing_locales": ["en", "ja", "ko", "zh-CN"],
        "status": "published",
    }
    with pytest.raises(ValueError, match="rebuild"):
        module.baseline_targets(article)
