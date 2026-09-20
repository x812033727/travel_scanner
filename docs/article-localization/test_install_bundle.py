"""Local install/restart invariants; no database sessions or model calls."""

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "test_localization_installer", Path(__file__).with_name("install_bundle.py")
)
installer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)
pipeline = installer.pipeline


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return pipeline.file_hash(path)


@pytest.fixture
def case(tmp_path, monkeypatch):
    slug = "test-guide"
    pack_path = f"apps/api/app/guides/content/{slug}.json"
    document = installer.publisher.normalized(
        {
            "title": "Original article",
            "description": "Every original condition is preserved.",
            "blocks": [
                {"type": "paragraph", "text": "Full body of the original article."}
            ],
            "sources": [
                {
                    "title": "Official source",
                    "url": "https://example.org/",
                    "checked_on": "2026-09-14",
                }
            ],
        }
    )
    metadata = {
        "slug": slug,
        "kind": "howto",
        "destination_id": None,
        "topics": [],
        "valid_until": None,
        "featured": False,
        "display_order": 100,
    }
    original_pack = {**metadata, "locales": {"zh-TW": document}}
    original_sha = write(tmp_path / pack_path, original_pack)
    source_sha = pipeline.digest(document)
    article = {
        "slug": slug,
        "pack_path": pack_path,
        "pack_sha256": original_sha,
        "metadata": metadata,
        "source_locale": "zh-TW",
        "source_document": document,
        "source_sha256": source_sha,
        "locale_documents": {"zh-TW": document},
        "missing_locales": ["en", "ja", "ko", "zh-CN"],
        "publication_locales": ["en", "ja", "ko", "zh-CN"],
        "published_locales": ["zh-TW"],
        "status": "published",
        "database": {"id": "unchanged"},
        "assets": [],
    }
    baseline_path = tmp_path / "docs/article-localization/baseline.json"
    baseline_sha = write(baseline_path, {"schema_version": 1, "articles": [article]})
    bundle = tmp_path / "docs/article-localization/releases/test"
    work = tmp_path / "docs/article-localization/work"
    pack = copy.deepcopy(original_pack)
    asset_path = "public/guides/test-guide/hero-en.jpg"
    asset = bundle / asset_path
    asset.parent.mkdir(parents=True)
    asset.write_bytes(b"<svg>reviewed</svg>")
    job = {
        "slug": slug,
        "locale": "en",
        "pack_path": pack_path,
        "pack_sha256": original_sha,
        "source_document": document,
        "source_sha256": source_sha,
        "baseline_source_sha256": source_sha,
        "assets": [],
    }
    job["job_sha256"] = pipeline.digest(job)
    job_directory = work / slug / "en"
    source_job_sha = write(job_directory / "source.json", job)
    artifact_sha = write(
        job_directory / "artifact-manifest.json",
        {"binding_version": 1, "job_sha256": job["job_sha256"]},
    )
    review_sha = write(
        job_directory / "review.json",
        {"artifact_manifest_sha256": artifact_sha},
    )
    job_binding = {
        "job_sha256": job["job_sha256"],
        "source_sha256": source_sha,
        "source_job_sha256": source_job_sha,
        "artifact_manifest_sha256": artifact_sha,
        "review_sha256": review_sha,
    }
    for locale in article["missing_locales"]:
        translated = copy.deepcopy(document)
        translated["title"] = f"Translated article ({locale})"
        translated["hero"] = {
            "src": "/guides/test-guide/hero-en.jpg",
            "alt": "Reviewed image",
            "width": 1600,
            "height": 900,
            "credit": None,
        }
        pack["locales"][locale] = translated
    pack_sha = write(bundle / f"packs/{slug}.json", pack)
    manifest = {
        "schema_version": 1,
        "baseline_sha256": baseline_sha,
        "articles": [
            {
                "slug": slug,
                "pack_path": f"packs/{slug}.json",
                "pack_sha256": pack_sha,
                "locales": article["missing_locales"],
                "publish_locales": article["missing_locales"],
                "hub": False,
            }
        ],
        "assets": [{"path": asset_path, "sha256": pipeline.file_hash(asset)}],
    }
    pin = write(bundle / "release-manifest.json", manifest)
    monkeypatch.setattr(
        installer,
        "reviewed_jobs",
        lambda *_: {slug: {"en": job_binding}},
    )
    return {
        "root": tmp_path,
        "bundle": bundle,
        "baseline": baseline_path,
        "pin": pin,
        "work": work,
        "job": job,
        "article": article,
        "manifest": manifest,
        "destination": tmp_path / pack_path,
        "asset": tmp_path / ("apps/web/" + asset_path),
        "job_directory": job_directory,
    }


def run(case):
    return installer.install(
        case["bundle"], case["baseline"], case["pin"], case["work"], root=case["root"]
    )


def test_installs_exact_bytes_and_resumes_without_invalidating_baseline(case):
    original = case["destination"].read_bytes()
    pipeline.assert_no_drift(case["job"], case["root"])
    result = run(case)
    assert result["status"] == "installed"
    expected = case["bundle"] / "packs/test-guide.json"
    assert case["destination"].read_bytes() == expected.read_bytes()
    backup = (
        case["root"]
        / installer.STATE
        / "bundles"
        / case["pin"][:16]
        / "backups"
        / (case["article"]["pack_sha256"][:24] + ".bin")
    )
    assert backup.read_bytes() == original
    pipeline.assert_no_drift(case["job"], case["root"])
    receipt = case["root"] / installer.STATE / "test-guide.json"
    receipt_bytes = receipt.read_bytes()
    assert run(case) == result
    assert receipt.read_bytes() == receipt_bytes
    assert case["job"]["pack_sha256"] == case["article"]["pack_sha256"]


@pytest.mark.parametrize("target", ["asset", "destination"])
def test_preflight_refuses_unrelated_bytes_before_any_install(case, target):
    path = case[target]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"another editor's changes")
    original_pack = case["destination"].read_bytes()
    with pytest.raises(installer.publisher.Refused):
        run(case)
    assert case["destination"].read_bytes() == original_pack
    assert not (case["root"] / installer.STATE / "test-guide.json").exists()


def test_interrupted_install_resumes_own_exact_partial_write(case, monkeypatch):
    original_write = installer.write_bytes
    count = 0

    def crash_after_asset(path, data):
        nonlocal count
        original_write(path, data)
        if path == case["asset"]:
            count += 1
            raise OSError("simulated interruption after atomic asset replacement")

    monkeypatch.setattr(installer, "write_bytes", crash_after_asset)
    with pytest.raises(OSError, match="simulated interruption"):
        run(case)
    assert count == 1
    assert pipeline.file_hash(case["destination"]) == case["article"]["pack_sha256"]
    monkeypatch.setattr(installer, "write_bytes", original_write)
    run(case)
    pipeline.assert_no_drift(case["job"], case["root"])


def test_resume_refuses_concurrent_edit_and_corrupt_original_backup(case):
    run(case)
    case["destination"].write_bytes(b"new editor body")
    with pytest.raises(installer.publisher.Refused, match="Destination drift"):
        run(case)
    with pytest.raises(ValueError, match="source pack changed"):
        pipeline.assert_no_drift(case["job"], case["root"])
    case["destination"].write_bytes(
        (case["bundle"] / "packs/test-guide.json").read_bytes()
    )
    backup = (
        case["root"]
        / installer.STATE
        / "bundles"
        / case["pin"][:16]
        / "backups"
        / (case["article"]["pack_sha256"][:24] + ".bin")
    )
    backup.write_bytes(b"corrupted backup")
    with pytest.raises(installer.publisher.Refused, match="backup"):
        run(case)
    with pytest.raises(ValueError, match="source pack changed"):
        pipeline.assert_no_drift(case["job"], case["root"])


def test_receipt_must_pin_exact_manifest_source_job_and_final_pack(case):
    run(case)
    receipt_path = case["root"] / installer.STATE / "test-guide.json"
    receipt = pipeline.read_json(receipt_path)
    for field in (
        "original_pack_sha256",
        "installed_pack_sha256",
        "source_sha256",
        "baseline_sha256",
        "manifest_sha256",
        "journal_sha256",
    ):
        damaged = {**receipt, field: "a" * 64}
        write(receipt_path, damaged)
        with pytest.raises(ValueError, match="source pack changed"):
            pipeline.assert_no_drift(case["job"], case["root"])
    write(receipt_path, receipt)
    for field in (
        "job_sha256",
        "source_sha256",
        "source_job_sha256",
        "artifact_manifest_sha256",
        "review_sha256",
    ):
        damaged = copy.deepcopy(receipt)
        damaged["jobs"]["en"][field] = "a" * 64
        write(receipt_path, damaged)
        with pytest.raises(ValueError, match="source pack changed"):
            pipeline.assert_no_drift(case["job"], case["root"])
    write(receipt_path, receipt)
    manifest_path = case["bundle"] / "release-manifest.json"
    manifest_path.write_bytes(manifest_path.read_bytes() + b" ")
    with pytest.raises(ValueError, match="source pack changed"):
        pipeline.assert_no_drift(case["job"], case["root"])


@pytest.mark.parametrize(
    "target",
    ["source.json", "artifact-manifest.json", "review.json", "baseline", "journal"],
)
def test_admission_rechecks_exact_source_review_baseline_and_journal_files(
    case, target
):
    run(case)
    receipt = pipeline.read_json(case["root"] / installer.STATE / "test-guide.json")
    paths = {
        "source.json": case["job_directory"] / "source.json",
        "artifact-manifest.json": case["job_directory"] / "artifact-manifest.json",
        "review.json": case["job_directory"] / "review.json",
        "baseline": case["baseline"],
        "journal": case["root"] / receipt["journal_path"],
    }
    paths[target].write_bytes(paths[target].read_bytes() + b" ")
    with pytest.raises(ValueError, match="source pack changed"):
        pipeline.assert_no_drift(case["job"], case["root"])


def test_only_a_completed_install_journal_can_admit_pack_drift(case):
    run(case)
    receipt_path = case["root"] / installer.STATE / "test-guide.json"
    receipt = pipeline.read_json(receipt_path)
    journal_path = case["root"] / receipt["journal_path"]
    journal = pipeline.read_json(journal_path)
    journal["status"] = "installing"
    receipt["journal_sha256"] = write(journal_path, journal)
    write(receipt_path, receipt)
    with pytest.raises(ValueError, match="source pack changed"):
        pipeline.assert_no_drift(case["job"], case["root"])


def test_crash_after_completed_journal_resumes_and_creates_receipt(case, monkeypatch):
    original_persist = installer.publisher.persist
    receipt_path = case["root"] / installer.STATE / "test-guide.json"
    interrupted = False

    def crash_before_receipt(path, value):
        nonlocal interrupted
        if path == receipt_path and not interrupted:
            interrupted = True
            raise OSError("simulated interruption before receipt")
        original_persist(path, value)

    monkeypatch.setattr(installer.publisher, "persist", crash_before_receipt)
    with pytest.raises(OSError, match="simulated interruption"):
        run(case)
    assert interrupted
    journal = pipeline.read_json(
        case["root"] / installer.STATE / "bundles" / case["pin"][:16] / "journal.json"
    )
    assert journal["status"] == "installed"
    assert not receipt_path.exists()

    monkeypatch.setattr(installer.publisher, "persist", original_persist)
    assert run(case)["status"] == "installed"
    pipeline.assert_no_drift(case["job"], case["root"])


def test_unadmitted_bundle_is_not_automatically_trusted(case):
    case["destination"].write_bytes(
        (case["bundle"] / "packs/test-guide.json").read_bytes()
    )
    with pytest.raises(ValueError, match="source pack changed"):
        pipeline.assert_no_drift(case["job"], case["root"])
    with pytest.raises(installer.publisher.Refused, match="Destination drift"):
        run(case)


def test_invalid_manifest_or_missing_review_never_changes_pack(case, monkeypatch):
    original = case["destination"].read_bytes()
    case["pin"] = "a" * 64
    with pytest.raises(installer.publisher.Refused, match="Manifest SHA256 mismatch"):
        run(case)
    assert case["destination"].read_bytes() == original
    case["pin"] = pipeline.file_hash(case["bundle"] / "release-manifest.json")
    monkeypatch.setattr(
        installer,
        "reviewed_jobs",
        lambda *_: (_ for _ in ()).throw(ValueError("review missing")),
    )
    with pytest.raises(ValueError, match="review missing"):
        run(case)
    assert case["destination"].read_bytes() == original
