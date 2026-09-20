"""Progress requires current hash evidence; neither files nor stale flags imply success."""

import copy
import csv
import importlib.util
import json
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "report_progress_tested", Path(__file__).with_name("report_progress.py")
)
reporter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reporter)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return reporter.sha(path)


def document():
    return reporter.normalized(
        {
            "title": "原始文章標題",
            "description": "原始文章摘要",
            "blocks": [{"type": "paragraph", "text": "這是完整的原始文章內容。"}],
            "sources": [],
        }
    )


def article(slug="example-guide"):
    doc = document()
    return {
        "slug": slug,
        "kind": "howto",
        "status": "published",
        "source_locale": "zh-TW",
        "source_document": doc,
        "source_sha256": reporter.digest(doc),
        "locale_documents": {"zh-TW": doc},
        "published_locales": ["zh-TW"],
        "publication_locales": [
            locale for locale in reporter.publisher.LOCALES if locale != "zh-TW"
        ],
        "missing_locales": [
            locale for locale in reporter.publisher.LOCALES if locale != "zh-TW"
        ],
        "pack_path": None,
        "pack_sha256": None,
        "assets": [],
        "metadata": {
            "slug": slug,
            "kind": "howto",
            "destination_id": None,
            "topics": [],
            "valid_until": None,
            "featured": False,
            "display_order": 100,
        },
        "database": {
            "id": "00000000-0000-0000-0000-000000000001",
            "version": 1,
            "locales": {
                "zh-TW": {
                    "id": "00000000-0000-0000-0000-000000000002",
                    "version": 2,
                    "published_version": 2,
                    "draft_sha256": reporter.digest(doc),
                    "published_sha256": reporter.digest(doc),
                }
            },
        },
    }


def stage(tmp_path, *, render=True, review=True):
    baseline_article = article()
    baseline_path = tmp_path / "baseline.json"
    write(baseline_path, {"schema_version": 1, "articles": [baseline_article]})
    work = tmp_path / "work"
    job_dir = reporter.pipeline.prepare(
        baseline_article, "en", work, tmp_path / "public", False
    )
    job = reporter.read(job_dir / "source.json")
    translations = {key: "Complete translated content" for key in job["fields"]}
    write(job_dir / "translated-fields.json", {"translations": translations})
    result = reporter.pipeline.materialize(job, translations, job_dir)
    receipt = reporter.read(job_dir / "receipt.json")
    receipt.update(status="translated", **result)
    write(job_dir / "receipt.json", receipt)
    if render:
        write(
            job_dir / "render-receipt.json",
            {"automatedLayoutPassed": True, "results": []},
        )
        receipt.update(
            status="rendered",
            automated_layout_passed=True,
            **reporter.pipeline.bind_artifacts(job_dir, job, "rendered", True),
        )
        write(job_dir / "receipt.json", receipt)
    if review:
        write(
            job_dir / "review.json",
            {
                "artifact_manifest_sha256": receipt["artifact_manifest_sha256"],
                "document_sha256": receipt["document_sha256"],
                "text_reviewed": True,
                "visual_reviewed": True,
                "glyph_reviewed": True,
                "assets": {},
                "text_free_rasters": [],
            },
        )
    return baseline_path, work, job_dir


def locale(report, language="en"):
    return next(
        row for row in report["articles"][0]["locales"] if row["locale"] == language
    )


def bundle_and_journal(tmp_path, baseline_path, job_dir):
    baseline = reporter.read(baseline_path)["articles"][0]
    translated = reporter.normalized(reporter.read(job_dir / "document.json"))
    pack = {
        **baseline["metadata"],
        "locales": {
            language: copy.deepcopy(translated)
            for language in reporter.publisher.LOCALES
        },
    }
    pack["locales"]["zh-TW"] = baseline["source_document"]
    directory = tmp_path / "bundle"
    pack_path = "packs/example-guide.json"
    pack_sha = write(directory / pack_path, pack)
    manifest = {
        "schema_version": 1,
        "baseline_sha256": reporter.sha(baseline_path),
        "articles": [
            {
                "slug": "example-guide",
                "pack_path": pack_path,
                "pack_sha256": pack_sha,
                "locales": ["en"],
                "publish_locales": ["en"],
                "hub": False,
            }
        ],
        "assets": [],
    }
    manifest_sha = write(directory / "release-manifest.json", manifest)
    bundle = reporter.publisher.verify_bundle(directory, baseline_path, manifest_sha)
    actor_id = "00000000-0000-0000-0000-000000000099"
    source_sha = reporter.digest(baseline["source_document"])
    source_locale = {
        "id": baseline["database"]["locales"]["zh-TW"]["id"],
        "version": 2,
        "published_version": 2,
        "published_at": "2026-09-20T00:00:00+00:00",
        "updated_at": "2026-09-20T00:00:00+00:00",
        "draft_sha256": source_sha,
        "published_sha256": source_sha,
        "latest_sha256": source_sha,
        "latest_action": "published",
        "latest_actor": actor_id,
    }
    initial_article = {
        "id": baseline["database"]["id"],
        "version": baseline["database"]["version"],
        "kind": "howto",
        "destination_id": None,
        "valid_until": None,
        "featured": False,
        "display_order": 100,
        "is_active": True,
        "updated_at": "2026-09-20T00:00:00+00:00",
        "topics": [],
        "metadata_audit": None,
        "locales": {"zh-TW": source_locale},
    }
    initial = {"example-guide": initial_article}
    operations = reporter.publisher.planned_operations(bundle, initial)
    draft = operations["drafts"][0]
    publish = operations["publish-articles"][0]
    doc_sha = reporter.digest(translated)
    final_article = copy.deepcopy(initial_article)
    final_article["locales"]["en"] = {
        "id": "00000000-0000-0000-0000-000000000003",
        "version": 2,
        "published_version": 2,
        "published_at": "2026-09-20T00:02:00+00:00",
        "updated_at": "2026-09-20T00:02:00+00:00",
        "draft_sha256": doc_sha,
        "published_sha256": doc_sha,
        "latest_sha256": doc_sha,
        "latest_action": "published",
        "latest_actor": actor_id,
    }
    journal = {
        "schema_version": 2,
        "manifest_sha256": manifest_sha,
        "baseline_sha256": reporter.sha(baseline_path),
        "slugs": ["example-guide"],
        "actor_id": actor_id,
        "created_at": "2026-09-20T00:00:00+00:00",
        "initial": initial,
        "authorization_sha256": reporter.publisher.journal_authorization(
            bundle, initial, operations
        ),
        "seal_sha256": "",
        "dry_run": True,
        "pending": None,
        "expected": {"example-guide": final_article},
        "operations": operations,
        "done": {
            "drafts": [draft["id"]],
            "publish-articles": [publish["id"]],
            "publish-hubs": [],
        },
        "history": [
            {
                "phase": "dry-run",
                "status": "read_only",
                "at": "2026-09-20T00:00:00+00:00",
            },
            {
                "id": draft["id"],
                "status": "committed",
                "at": "2026-09-20T00:01:00+00:00",
            },
            {
                "id": publish["id"],
                "status": "committed_reconciled",
                "at": "2026-09-20T00:02:00+00:00",
            },
        ],
    }
    reporter.publisher.seal_journal(journal)
    journal_path = tmp_path / "journal.json"
    write(journal_path, journal)
    return directory, journal_path


def test_all_626_articles_and_2404_missing_languages_are_reported_deterministically(
    tmp_path,
):
    articles = []
    for index in range(626):
        item = article(f"article-{index:04d}")
        item["status"] = "published" if index < 287 else "draft"
        if index < 10:
            item["missing_locales"] = []
        elif index < 70:
            item["missing_locales"] = item["missing_locales"][:3]
        articles.append(item)
    baseline = tmp_path / "baseline.json"
    write(
        baseline,
        {
            "schema_version": 1,
            "repo_commit": "8c83e90ab401f05044f614e5843c00d26aaed3dd",
            "captured_at": "2026-09-14T13:58:13.225571+00:00",
            "articles": list(reversed(articles)),
            "summary": {"articles": 626, "missing_language_documents": 2404},
        },
    )
    first = reporter.build_report(baseline, tmp_path / "work", root=tmp_path)
    second = reporter.build_report(baseline, tmp_path / "work", root=tmp_path)
    assert first == second
    assert first["summary"]["articles"] == 626
    assert first["summary"]["missing_language_documents"] == 2404
    assert first["summary"]["baseline_statuses"] == {"draft": 339, "published": 287}
    assert first["baseline_repo_commit"] == "8c83e90ab401f05044f614e5843c00d26aaed3dd"
    assert first["summary"]["staged_jobs"] == 0
    assert first["summary"]["staged_work_statuses"] == {}
    assert first["summary"]["missing_language_progress"] == dict.fromkeys(
        reporter.STAGES, 0
    )
    assert all(len(batch["slugs"]) <= 20 for batch in first["batches"])
    assert sum(len(batch["slugs"]) for batch in first["batches"]) == 616
    reporter.write_report(first, tmp_path / "out-one")
    reporter.write_report(second, tmp_path / "out-two")
    for name in ("progress.json", "progress.csv", "progress.md"):
        assert (tmp_path / "out-one" / name).read_bytes() == (
            tmp_path / "out-two" / name
        ).read_bytes()
    with (tmp_path / "out-one/progress.csv").open(
        encoding="utf-8-sig", newline=""
    ) as stream:
        assert len(list(csv.DictReader(stream))) == 626
    markdown = (tmp_path / "out-one/progress.md").read_text(encoding="utf-8")
    assert (
        "固定歷史快照基準（不代表目前儲存庫或正式站狀態）：626 篇文章，缺少 2,404 份語言稿"
    ) in markdown
    assert "儲存庫 commit `8c83e90ab401f05044f614e5843c00d26aaed3dd`" in markdown


def test_staged_job_statuses_exclude_unstarted_baseline_locales(tmp_path):
    baseline, work, _ = stage(tmp_path, render=False, review=False)
    report = reporter.build_report(baseline, work, root=tmp_path)
    assert report["summary"]["staged_jobs"] == 1
    assert report["summary"]["staged_work_statuses"] == {"translated": 1}
    assert report["summary"]["work_statuses"] == {"not_started": 4, "translated": 1}


def test_schema_render_and_independent_review_are_separate_stages(tmp_path):
    baseline, work, job = stage(tmp_path, render=False, review=False)
    row = locale(reporter.build_report(baseline, work, root=tmp_path))
    assert row["translated"] is True
    assert all(row[key] is False for key in reporter.STAGES if key != "translated")
    # File presence alone does not prove a completed render or review.
    write(
        job / "review.json",
        {"text_reviewed": True, "visual_reviewed": True, "glyph_reviewed": True},
    )
    row = locale(reporter.build_report(baseline, work, root=tmp_path))
    assert row["translated"] is True and row["reviewed"] is False


@pytest.mark.parametrize(
    "change",
    ["document", "fields", "extra_attempt", "missing_manifest", "legacy_receipt"],
)
def test_obsolete_artifact_hashes_cannot_keep_green_stages(tmp_path, change):
    baseline, work, job = stage(tmp_path)
    assert (
        locale(reporter.build_report(baseline, work, root=tmp_path))["reviewed"] is True
    )
    if change == "document":
        value = reporter.read(job / "document.json")
        value["title"] = "Changed without rerunning materialization"
        write(job / "document.json", value)
    elif change == "fields":
        write(job / "fields.json", {})
    elif change == "extra_attempt":
        write(job / "attempt-99.output.json", {"unexpected": True})
    elif change == "missing_manifest":
        (job / "artifact-manifest.json").unlink()
    else:
        receipt = reporter.read(job / "receipt.json")
        receipt.pop("artifact_manifest_sha256")
        write(job / "receipt.json", receipt)
    row = locale(reporter.build_report(baseline, work, root=tmp_path))
    assert not any(row[key] for key in reporter.STAGES)
    assert row["issues"]


def test_obsolete_review_retains_current_automated_results_but_not_approval(tmp_path):
    baseline, work, job = stage(tmp_path)
    review = reporter.read(job / "review.json")
    review["artifact_manifest_sha256"] = "0" * 64
    write(job / "review.json", review)
    row = locale(reporter.build_report(baseline, work, root=tmp_path))
    assert row["translated"] and row["rendered"]
    assert row["reviewed"] is False
    assert any("obsolete artifact" in issue for issue in row["issues"])


def test_bundle_journal_and_browser_success_are_distinct_exact_evidence(tmp_path):
    baseline, work, job = stage(tmp_path)
    bundle, journal = bundle_and_journal(tmp_path, baseline, job)
    assembled = locale(
        reporter.build_report(baseline, work, bundle_dirs=[bundle], root=tmp_path)
    )
    assert (
        assembled["assembled"]
        and not assembled["draft_imported"]
        and not assembled["published"]
    )
    published = locale(
        reporter.build_report(
            baseline, work, bundle_dirs=[bundle], journals=[journal], root=tmp_path
        )
    )
    assert (
        published["draft_imported"]
        and published["published"]
        and not published["browser_verified"]
    )
    capture = tmp_path / "desktop-mobile.png"
    capture.write_bytes(b"Recorded browser evidence fixture")
    evidence = {
        "schema_version": 1,
        "baseline_sha256": reporter.sha(baseline),
        "entries": [
            {
                "slug": "example-guide",
                "locale": "en",
                **{
                    key: published["publication"][0][key]
                    for key in (
                        "document_sha256",
                        "manifest_sha256",
                        "published_version",
                    )
                },
                "url": "https://mokaair.com/en/guides/howto/example-guide",
                "checks": dict.fromkeys(
                    (
                        "body",
                        "images",
                        "canonical",
                        "hreflang",
                        "links",
                        "desktop",
                        "mobile",
                    ),
                    True,
                ),
                "evidence": [{"path": capture.name, "sha256": reporter.sha(capture)}],
            }
        ],
    }
    browser = tmp_path / "browser.json"
    write(browser, evidence)
    options = {
        "bundle_dirs": [bundle],
        "journals": [journal],
        "browser_evidence": [browser],
        "root": tmp_path,
    }
    assert locale(reporter.build_report(baseline, work, **options))["browser_verified"]
    capture.write_bytes(b"Changed after verification")
    assert (
        locale(reporter.build_report(baseline, work, **options))["browser_verified"]
        is False
    )


@pytest.mark.parametrize(
    "change", ["pending", "wrong_hash", "missing_commit_history", "wrong_actor"]
)
def test_journal_pending_or_mismatched_publication_never_counts_as_published(
    tmp_path, change
):
    baseline, work, job = stage(tmp_path)
    bundle, path = bundle_and_journal(tmp_path, baseline, job)
    journal = reporter.read(path)
    if change == "pending":
        journal["pending"] = journal["operations"]["publish-articles"][0]
    elif change == "wrong_hash":
        journal["expected"]["example-guide"]["locales"]["en"]["published_sha256"] = (
            "0" * 64
        )
    elif change == "missing_commit_history":
        journal["history"] = journal["history"][:1]
    else:
        journal["expected"]["example-guide"]["locales"]["en"]["latest_actor"] = (
            "other-owner"
        )
    write(path, journal)
    report = reporter.build_report(
        baseline, work, bundle_dirs=[bundle], journals=[path], root=tmp_path
    )
    assert locale(report)["published"] is False


def test_stale_review_invalidates_assembled_and_later_stages_even_with_old_journal(
    tmp_path,
):
    baseline, work, job = stage(tmp_path)
    bundle, journal = bundle_and_journal(tmp_path, baseline, job)
    review = reporter.read(job / "review.json")
    review["artifact_manifest_sha256"] = "0" * 64
    write(job / "review.json", review)
    row = locale(
        reporter.build_report(
            baseline, work, bundle_dirs=[bundle], journals=[journal], root=tmp_path
        )
    )
    assert not any(
        row[key]
        for key in (
            "reviewed",
            "assembled",
            "draft_imported",
            "published",
            "browser_verified",
        )
    )


def test_duplicate_conflicting_journals_are_reported_without_picking_a_winner(tmp_path):
    baseline, work, job = stage(tmp_path)
    bundle, first = bundle_and_journal(tmp_path, baseline, job)
    other = reporter.read(first)
    other["history"].append(
        {
            "phase": "publish-articles",
            "status": "complete",
            "at": "2026-09-20T00:03:00+00:00",
        }
    )
    reporter.publisher.seal_journal(other)
    second = tmp_path / "other-journal.json"
    write(second, other)
    report = reporter.build_report(
        baseline, work, bundle_dirs=[bundle], journals=[first, second], root=tmp_path
    )
    assert locale(report)["published"] is False
    assert any("Conflicting journals" in row["error"] for row in report["errors"])


def photo_stage(tmp_path, *, missing=False):
    item = article()
    japanese = copy.deepcopy(item["source_document"])
    source_path = "/guides/example-guide/photo.jpg"
    japanese["hero"] = {
        "src": source_path,
        "alt": "Existing photograph description",
        "width": 1600,
        "height": 900,
        "credit": None,
    }
    if missing:
        item["source_document"] = japanese
        item["source_sha256"] = reporter.digest(japanese)
        item["locale_documents"]["zh-TW"] = japanese
    else:
        item["locale_documents"]["ja"] = japanese
        item["missing_locales"].remove("ja")
    raster = tmp_path / "apps/web/public/guides/example-guide/photo.jpg"
    raster.parent.mkdir(parents=True)
    raster.write_bytes(b"Original image requiring inspection")
    item["assets"] = [{"src": source_path, "sha256": reporter.sha(raster)}]
    baseline = tmp_path / "baseline.json"
    write(baseline, {"schema_version": 1, "articles": [item]})
    work = tmp_path / "work"
    job = reporter.pipeline.prepare(
        item, "ja", work, tmp_path / "apps/web/public", True
    )
    return baseline, work, job, raster, source_path, japanese


def photo_review(job, raster, source_path, doc):
    receipt = reporter.read(job / "receipt.json")
    return {
        "artifact_manifest_sha256": receipt["artifact_manifest_sha256"],
        "document_sha256": reporter.digest(doc),
        "text_reviewed": True,
        "visual_reviewed": True,
        "glyph_reviewed": True,
        "assets": {},
        "source_rasters": {
            source_path: {
                "sha256": reporter.sha(raster),
                "editorial_overlay": False,
                "reusable_without_pixel_translation": True,
                "reason": "Authentic street photograph; shop signs belong to the scene.",
                "caption_review_required": True,
                "caption_reviewed": True,
            }
        },
    }


def test_existing_raster_review_requires_current_bytes_and_explicit_reuse_evidence(
    tmp_path,
):
    baseline, work, job, raster, source_path, japanese = photo_stage(tmp_path)
    row = locale(reporter.build_report(baseline, work, root=tmp_path), "ja")
    assert row["work_status"] == "pending_review"
    assert row["rendering_required"] is False and row["reviewed"] is False
    review = photo_review(job, raster, source_path, japanese)
    write(job / "review.json", review)
    assert locale(reporter.build_report(baseline, work, root=tmp_path), "ja")[
        "reviewed"
    ]
    raster.write_bytes(b"Changed original photograph")
    assert (
        locale(reporter.build_report(baseline, work, root=tmp_path), "ja")["reviewed"]
        is False
    )


@pytest.mark.parametrize(
    "change", ["absent", "legacy", "hash", "overlay", "reuse", "reason", "caption"]
)
def test_source_photo_assessment_must_match_assembler_contract(tmp_path, change):
    baseline, work, job, raster, source_path, japanese = photo_stage(tmp_path)
    review = photo_review(job, raster, source_path, japanese)
    assessment = review["source_rasters"][source_path]
    if change in {"absent", "legacy"}:
        review.pop("source_rasters")
        if change == "legacy":
            review["text_free_rasters"] = [source_path]
    elif change == "hash":
        assessment["sha256"] = "0" * 64
    elif change == "overlay":
        assessment["editorial_overlay"] = True
    elif change == "reuse":
        assessment["reusable_without_pixel_translation"] = False
    elif change == "reason":
        assessment["reason"] = ""
    else:
        assessment["caption_reviewed"] = False
    write(job / "review.json", review)
    row = locale(reporter.build_report(baseline, work, root=tmp_path), "ja")
    assert row["reviewed"] is False
    assert "Original raster still needs a hash-pinned reuse assessment" in row["issues"]


def test_full_translation_with_authentic_photo_is_counted_only_after_reuse_review(
    tmp_path,
):
    baseline, work, job, raster, source_path, _ = photo_stage(tmp_path, missing=True)
    source = reporter.read(job / "source.json")
    translations = {key: "完整な翻訳の文章です。" for key in source["fields"]}
    write(job / "translated-fields.json", {"translations": translations})
    result = reporter.pipeline.materialize(source, translations, job)
    receipt = reporter.read(job / "receipt.json")
    receipt.update(status="translated", **result)
    write(job / "receipt.json", receipt)
    write(job / "render-receipt.json", {"automatedLayoutPassed": True, "results": []})
    receipt.update(
        status="rendered",
        automated_layout_passed=True,
        **reporter.pipeline.bind_artifacts(job, source, "rendered", True),
    )
    write(job / "receipt.json", receipt)
    row = locale(reporter.build_report(baseline, work, root=tmp_path), "ja")
    assert row["translated"] and row["rendered"] and not row["reviewed"]
    review = photo_review(
        job, raster, source_path, reporter.read(job / "document.json")
    )
    write(job / "review.json", review)
    assert locale(reporter.build_report(baseline, work, root=tmp_path), "ja")[
        "reviewed"
    ]
