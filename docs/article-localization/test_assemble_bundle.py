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
    result, changes = module.localize_links(before, "ja", {"lesson-one": {"kind": "life"}})
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
    binding = module.pipeline.bind_artifacts(tmp_path, data["source.json"], "rendered", True)
    for filename in ["receipt.json", "review.json"]:
        data[filename].update(binding)
        (tmp_path / filename).write_text(json.dumps(data[filename]), encoding="utf-8")
    assert module.reviewed_document(tmp_path, article, "en")[0] == doc
    data["document.json"]["title"] = "Edited after review"
    (tmp_path / "document.json").write_text(json.dumps(data["document.json"]), encoding="utf-8")
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
            module.assemble(tmp_path / "missing.json", tmp_path, slugs, tmp_path / "output")
    assert not (tmp_path / "output").exists()


def test_hub_requires_public_catalogue_lessons_even_without_body_links(tmp_path, monkeypatch):
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
        "gemini-guide": [{"slug": "public-lesson", "locale": "en", "document_sha256": "a" * 64}],
    }


def test_unchanged_reviewed_database_draft_is_selected_and_published(tmp_path, monkeypatch):
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
                    locale: ("database-draft" if locale == "en" else "database-published")
                    for locale in module.LOCALES
                },
                "published_locales": [locale for locale in module.LOCALES if locale != "en"],
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

    original = copy.deepcopy(locale_documents["zh-TW"])
    corrected = copy.deepcopy(original)
    corrected["title"] = "Reviewed source correction"
    corrected["sources"].append(
        {
            "title": "Correction evidence",
            "url": "https://example.org/correction",
            "checked_on": "2026-09-22",
        }
    )
    article = baseline["articles"][0]
    article["source_document"] = corrected
    article["source_sha256"] = module.digest(corrected)
    article["locale_documents"]["zh-TW"] = corrected
    old_hash = module.digest(original)
    article["database"]["locales"]["zh-TW"] = {
        "id": "locale-id",
        "version": 6,
        "published_version": 6,
        "published_sha256": old_hash,
        "draft_sha256": old_hash,
    }
    pack["locales"]["zh-TW"] = corrected
    pack_path.write_text(json.dumps(pack), encoding="utf-8")
    article["pack_sha256"] = module.sha(pack_path)
    baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
    review = {
        "schema_version": 1,
        "approved": True,
        "reviewer": "independent-editor",
        "reason": "Verified source correction",
        "evidence_sha256": "e" * 64,
        "slug": "public-article",
        "article_id": "article-id",
        "article_version": 7,
        "locale": "zh-TW",
        "locale_version": 6,
        "published_version": 6,
        "published_sha256": old_hash,
        "draft_sha256": old_hash,
        "corrected_sha256": module.digest(corrected),
        "old_document": original,
        "changes": [
            {"pointer": "/title", "before": original["title"], "after": corrected["title"]},
            {"pointer": "/sources", "before": original["sources"], "after": corrected["sources"]},
        ],
        "assets": [],
    }
    review_path = tmp_path / "independent-source-review.json"
    review_path.write_text(json.dumps(review), encoding="utf-8")
    with pytest.raises(ValueError, match="without correction review"):
        module.assemble(baseline_path, work, ["public-article"], tmp_path / "unreviewed-bundle")
    assert not (tmp_path / "unreviewed-bundle").exists()
    correction_manifest = module.assemble(
        baseline_path,
        work,
        ["public-article"],
        tmp_path / "corrected-bundle",
        source_correction_reviews=[review_path],
    )
    entry = correction_manifest["articles"][0]
    assert entry["locales"] == ["zh-TW", "en"]
    assert entry["publish_locales"] == ["zh-TW", "en"]
    assert entry["source_corrections"][0]["review_sha256"] == module.sha(review_path)
    assert (
        tmp_path / "corrected-bundle" / entry["source_corrections"][0]["review_path"]
    ).read_bytes() == review_path.read_bytes()
    overlapping = copy.deepcopy(review)
    overlapping["changes"].append(
        {"pointer": "/sources/0/title", "before": "Official source", "after": "Edited"}
    )
    with pytest.raises(ValueError, match="Overlapping"):
        module.source_correction.verify_review(
            overlapping, article, "zh-TW", corrected, {}
        )


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


def preservation_case(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    slug = "preserved-source"
    pack_path = root / f"apps/api/app/guides/content/{slug}.json"
    pack_path.parent.mkdir(parents=True)
    live = module.GuideDocument.model_validate(document()).model_dump(mode="json")
    repository = copy.deepcopy(live)
    repository["description"] = "Reviewed repository-only answer-first description"
    locales = {"zh-TW": repository}
    for locale in module.LOCALES[1:]:
        translated = copy.deepcopy(live)
        translated["title"] = f"Reviewed {locale} title"
        translated["description"] = f"Reviewed {locale} description"
        locales[locale] = translated
    pack = module.ArticlePack.model_validate(
        {
            "slug": slug,
            "kind": "life",
            "destination_id": None,
            "topics": ["packing", "connectivity"],
            "valid_until": None,
            "featured": False,
            "display_order": 100,
            "locales": locales,
        }
    ).model_dump(mode="json")
    pack_path.write_text(
        json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    repo_commit = "1" * 40
    targets = list(module.LOCALES[1:])
    article = {
        "slug": slug,
        "kind": "life",
        "status": "published",
        "pack_path": pack_path.relative_to(root).as_posix(),
        "pack_sha256": module.sha(pack_path),
        "metadata": {key: pack[key] for key in (
            "slug", "kind", "destination_id", "topics", "valid_until", "featured",
            "display_order",
        )},
        "source_locale": "zh-TW",
        "source_document": live,
        "source_sha256": module.digest(live),
        "locale_documents": {**locales, "zh-TW": live},
        "existing_locales": list(module.LOCALES),
        "missing_locales": [],
        "translation_missing_locales": [],
        "publication_missing_locales": targets,
        "publication_locales": targets,
        "target_locales": targets,
        "batch_locales": targets,
        "locale_provenance": {
            locale: "database-published" if locale == "zh-TW" else "repository-only"
            for locale in module.LOCALES
        },
        "published_locales": ["zh-TW"],
        "database": {
            "id": "article-id",
            "version": 2,
            "locales": {
                "zh-TW": {
                    "id": "locale-id",
                    "version": 8,
                    "published_version": 8,
                    "published_sha256": module.digest(live),
                    "draft_sha256": module.digest(live),
                }
            },
        },
        "assets": [],
    }
    baseline = {"schema_version": 1, "repo_commit": repo_commit, "articles": [article]}
    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
    work = tmp_path / "work"
    for locale in targets:
        directory = work / slug / locale
        directory.mkdir(parents=True)
        (directory / "document.json").write_text("{}", encoding="utf-8")

    def reviewed(_directory, _article, locale):
        return copy.deepcopy(_article["locale_documents"][locale]), []

    monkeypatch.setattr(module, "ROOT", root)
    monkeypatch.setattr(module, "reviewed_document", reviewed)

    def pinned_git_blob(revision, path):
        assert revision == repo_commit
        assert path == article["pack_path"]
        return module.repository_preservation.git_blob_sha1(pack_path.read_bytes())

    monkeypatch.setattr(
        module,
        "git_blob",
        pinned_git_blob,
    )
    raw = pack_path.read_bytes()
    review = {
        "schema_version": 1,
        "status": "PASS",
        "reviewer": "independent-reviewer",
        "reviewed_at": "2026-09-22T04:45:00+00:00",
        "reason": "Preserve the independently reviewed repository description",
        "evidence_sha256": "e" * 64,
        "slug": slug,
        "article_id": "article-id",
        "article_version": 2,
        "locale": "zh-TW",
        "locale_id": "locale-id",
        "locale_version": 8,
        "published_version": 8,
        "live_published_sha256": module.digest(live),
        "live_draft_sha256": module.digest(live),
        "baseline_source_sha256": module.digest(live),
        "baseline_locale_sha256": module.digest(live),
        "repo_commit": repo_commit,
        "repo_pack_path": article["pack_path"],
        "repo_pack_git_blob_sha1": module.repository_preservation.git_blob_sha1(raw),
        "repo_pack_sha256": module.sha(pack_path),
        "repo_document_sha256": module.digest(repository),
        "changes": [
            {
                "pointer": "/description",
                "before": live["description"],
                "after": repository["description"],
            }
        ],
    }
    review_path = tmp_path / "preservation-review.json"
    review_path.write_text(json.dumps(review), encoding="utf-8")
    return {
        "root": root,
        "slug": slug,
        "pack_path": pack_path,
        "pack": pack,
        "article": article,
        "baseline": baseline,
        "baseline_path": baseline_path,
        "work": work,
        "review": review,
        "review_path": review_path,
        "live": live,
        "repository": repository,
        "targets": targets,
    }


def write_preservation_case(case):
    case["pack_path"].write_text(
        json.dumps(case["pack"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    raw = case["pack_path"].read_bytes()
    case["article"]["pack_sha256"] = module.sha(case["pack_path"])
    case["review"]["repo_pack_sha256"] = module.sha(case["pack_path"])
    case["review"]["repo_pack_git_blob_sha1"] = (
        module.repository_preservation.git_blob_sha1(raw)
    )
    case["baseline_path"].write_text(json.dumps(case["baseline"]), encoding="utf-8")
    case["review_path"].write_text(json.dumps(case["review"]), encoding="utf-8")


def test_reviewed_unselected_repository_description_is_preserved_from_final_git_pack(
    tmp_path, monkeypatch
):
    case = preservation_case(tmp_path, monkeypatch)
    output = tmp_path / "bundle"
    manifest = module.assemble(
        case["baseline_path"],
        case["work"],
        [case["slug"]],
        output,
        repository_preservation_reviews=[case["review_path"]],
    )
    entry = manifest["articles"][0]
    assert entry["locales"] == case["targets"]
    assert entry["publish_locales"] == case["targets"]
    assert entry["repository_preservations"][0]["locale"] == "zh-TW"
    assert (output / entry["pack_path"]).read_bytes() == case["pack_path"].read_bytes()
    assembled = json.loads((output / entry["pack_path"]).read_text(encoding="utf-8"))
    assert assembled["locales"]["zh-TW"] == case["repository"]
    assert case["article"]["source_document"] == case["live"]
    assert "zh-TW" not in entry["locales"] and "zh-TW" not in entry["publish_locales"]


@pytest.mark.parametrize(
    "tamper",
    [
        "status",
        "reviewed_at",
        "blob",
        "git_commit_tree",
        "pointer",
        "baseline_source",
        "extra_source",
        "target",
        "target_translation",
        "metadata",
    ],
)
def test_repository_preservation_rejects_tamper_or_other_scope(tmp_path, monkeypatch, tamper):
    case = preservation_case(tmp_path, monkeypatch)
    if tamper == "status":
        case["review"]["status"] = "DESIGN_ALIGNED_NOT_IMPLEMENTATION_APPROVAL"
    elif tamper == "reviewed_at":
        case["review"]["reviewed_at"] = "not-a-time"
    elif tamper == "blob":
        case["review"]["repo_pack_git_blob_sha1"] = "f" * 40
    elif tamper == "git_commit_tree":
        monkeypatch.setattr(module, "git_blob", lambda _revision, _path: "f" * 40)
    elif tamper == "pointer":
        case["review"]["changes"][0]["pointer"] = "/title"
    elif tamper == "baseline_source":
        changed = copy.deepcopy(case["article"]["source_document"])
        changed["title"] = "Tampered baseline source title"
        case["article"]["source_document"] = changed
        case["article"]["source_sha256"] = module.digest(changed)
        case["review"]["baseline_source_sha256"] = module.digest(changed)
    elif tamper == "extra_source":
        case["pack"]["locales"]["zh-TW"]["title"] = "Unreviewed repository title"
        case["review"]["repo_document_sha256"] = module.digest(
            case["pack"]["locales"]["zh-TW"]
        )
        write_preservation_case(case)
    elif tamper == "target":
        case["article"]["published_locales"] = []
        case["article"]["publication_missing_locales"] = list(module.LOCALES)
        case["article"]["publication_locales"] = list(module.LOCALES)
        case["article"]["target_locales"] = list(module.LOCALES)
        case["article"]["batch_locales"] = list(module.LOCALES)
    elif tamper == "target_translation":
        case["pack"]["locales"]["en"]["title"] = "Unreviewed final-Git target title"
        write_preservation_case(case)
    elif tamper == "metadata":
        case["pack"]["display_order"] = 101
        write_preservation_case(case)
    case["baseline_path"].write_text(json.dumps(case["baseline"]), encoding="utf-8")
    case["review_path"].write_text(json.dumps(case["review"]), encoding="utf-8")
    with pytest.raises(ValueError):
        module.assemble(
            case["baseline_path"],
            case["work"],
            [case["slug"]],
            tmp_path / "rejected-bundle",
            repository_preservation_reviews=[case["review_path"]],
        )
    assert not (tmp_path / "rejected-bundle").exists()


def test_repository_preservation_cannot_overlap_source_correction(tmp_path, monkeypatch):
    case = preservation_case(tmp_path, monkeypatch)
    correction = tmp_path / "source-correction.json"
    correction.write_text(
        json.dumps({"slug": case["slug"], "locale": "zh-TW"}), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="overlaps selected/source-correction"):
        module.assemble(
            case["baseline_path"],
            case["work"],
            [case["slug"]],
            tmp_path / "rejected-overlap",
            source_correction_reviews=[correction],
            repository_preservation_reviews=[case["review_path"]],
        )
    assert not (tmp_path / "rejected-overlap").exists()
