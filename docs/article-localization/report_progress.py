"""Deterministic localization evidence report; never imports or publishes articles.

Run with the API Python environment. --baseline and --work are required;
--output writes progress.json, progress.csv (one article per row), progress.md.
Optional repeated --bundle DIR, --journal FILE and --browser-evidence FILE add
later stages. No timestamp is invented and no completion is inferred from file
existence. Database states are historical journal evidence, not a live DB check.
The inventory is always described as a pinned historical snapshot, never as the
current repository or production state.

Browser evidence schema 1: baseline_sha256, entries with slug, locale,
document_sha256, manifest_sha256, published_version, url, checks (body, images,
canonical, hreflang, links, desktop, mobile all true), and evidence (path, sha256).
Evidence paths are relative to the browser JSON; at least one hash-pinned file
is required. Browser success additionally requires matching recorded publication.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

from app.guides.schemas import GuideDocument

ROOT = Path(__file__).resolve().parents[2]
STAGES = (
    "translated",
    "rendered",
    "reviewed",
    "assembled",
    "draft_imported",
    "published",
    "browser_verified",
)


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


pipeline = module(
    "progress_localization_pipeline", ROOT / "tools/article-localization/pipeline.py"
)
publisher = module(
    "progress_localization_publisher", Path(__file__).with_name("publish_bundle.py")
)
assembler = module(
    "progress_localization_assembler", Path(__file__).with_name("assemble_bundle.py")
)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def normalized(document):
    return GuideDocument.model_validate(document).model_dump(mode="json")


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_issue(error):
    # Schema and database exceptions may contain complete content or SQL parameters.
    return (
        str(error)
        if type(error) in {ValueError, publisher.Refused}
        else type(error).__name__
    )


def staged_locale(article, locale, work, root):
    directory = work / article["slug"] / locale
    result = {
        "locale": locale,
        "required_translation": locale
        in article.get("translation_missing_locales", article["missing_locales"]),
        "required_work": locale
        in article.get("target_locales", article["missing_locales"]),
        "baseline_document_present": locale in article["locale_documents"],
        "baseline_published": locale in article["published_locales"],
        "work_status": "not_started",
        "mode": None,
        "rendering_required": True,
        **dict.fromkeys(STAGES, False),
        "artifact_manifest_sha256": None,
        "document_sha256": None,
        "publication": [],
        "issues": [],
    }
    document = None
    binding_valid = False
    if not directory.exists():
        return result, document
    try:
        source, receipt = (
            read(directory / "source.json"),
            read(directory / "receipt.json"),
        )
        result["work_status"] = receipt.get("status", "unknown")
        result["mode"] = source.get("mode")
        result["rendering_required"] = source.get("mode") != "review-only"
        require(
            source.get("slug") == article["slug"] and source.get("locale") == locale,
            "Job article/locale does not match directory",
        )
        expected_source = article["locale_documents"].get(
            locale, article["source_document"]
        )
        require(
            source.get("source_sha256") == digest(expected_source)
            and source.get("baseline_source_sha256") == article["source_sha256"],
            "Job source differs from pinned baseline",
        )
        require(
            source.get("database") == article.get("database")
            and source.get("pack_sha256") == article.get("pack_sha256")
            and source.get("pack_path") == article.get("pack_path"),
            "Job database/pack identity differs from pinned baseline",
        )
        pipeline.assert_no_drift(source, root)
        manifest = pipeline.verify_artifacts(directory, source, receipt)
        result["artifact_manifest_sha256"] = receipt["artifact_manifest_sha256"]
        stage = receipt["status"]
        if stage in {"failed", "invalid", "blocked", "running"}:
            result["issues"].append("pipeline_status:" + stage)
        if stage in {"translated", "rendered"}:
            document = normalized(read(directory / "document.json"))
            require(
                digest(document) == receipt["document_sha256"],
                "Normalized document differs from validated hash",
            )
            require(
                manifest.get("schema_validated") is True,
                "Schema validation is not recorded",
            )
            result["document_sha256"] = digest(document)
            result["translated"] = source.get("mode") == "full"
        elif source.get("mode") == "review-only" and stage == "pending_review":
            document = normalized(expected_source)
            result["document_sha256"] = digest(document)
            result["translated"] = not result["required_translation"]
        if stage == "rendered":
            render = read(directory / "render-receipt.json")
            require(
                receipt.get("automated_layout_passed") is True
                and render.get("automatedLayoutPassed") is True,
                "Automated layout has not passed",
            )
            require(
                all(not row.get("layoutIssues") for row in render["results"]),
                "Layout issues remain",
            )
            assets = read(directory / "assets.json")
            require(
                {row["source"] for row in render["results"]}
                == {row["public_svg"] for row in assets},
                "Render receipt does not cover every SVG",
            )
            for row in render["results"]:
                require(
                    sha(
                        publisher.safe_path(
                            directory / "assets", row["source"].lstrip("/")
                        )
                    )
                    == row["sha256"],
                    "Rendered SVG hash changed",
                )
                for target in row.get("rendered", []):
                    require(
                        sha(
                            publisher.safe_path(
                                directory / "assets", target["target"].lstrip("/")
                            )
                        )
                        == target["sha256"],
                        "Rendered raster hash changed",
                    )
            result["rendered"] = True
        binding_valid = True
        if not (directory / "review.json").is_file():
            return result, document
        review = read(directory / "review.json")
        require(
            review.get("artifact_manifest_sha256")
            == receipt["artifact_manifest_sha256"],
            "Independent review refers to an obsolete artifact manifest",
        )
        require(
            document is not None and review.get("document_sha256") == digest(document),
            "Independent review document hash changed",
        )
        require(
            all(
                review.get(key) is True
                for key in ("text_reviewed", "visual_reviewed", "glyph_reviewed")
            ),
            "Independent text/visual/glyph review incomplete",
        )
        require(
            result["rendered"] or source.get("mode") == "review-only",
            "Review needs current render evidence",
        )
        expected_assets = set()
        for asset in source.get("assets", []):
            expected_assets.add(asset["target_svg"])
            expected_assets.update(ref["target"] for ref in asset["references"])
        reviewed_assets = review.get("assets", {})
        require(
            expected_assets <= set(reviewed_assets),
            "Independent asset review incomplete",
        )
        for src, expected in reviewed_assets.items():
            require(
                sha(publisher.safe_path(directory / "assets", src.lstrip("/")))
                == expected,
                "Independent review asset hash changed",
            )
        for src in source.get("raster_review_required", []):
            assessment = review.get("source_rasters", {}).get(src, {})
            original = next(
                (asset for asset in article["assets"] if asset["src"] == src), None
            )
            require(
                original is not None
                and assessment.get("sha256") == original["sha256"]
                and assessment.get("editorial_overlay") is False
                and assessment.get("reusable_without_pixel_translation") is True
                and bool(assessment.get("reason"))
                and (
                    not assessment.get("caption_review_required")
                    or assessment.get("caption_reviewed") is True
                ),
                "Original raster still needs a hash-pinned reuse assessment",
            )
        # Authentic photographs may contain real-world signs. Their reuse assessment
        # must follow the assembler contract, rather than falsely declaring no text.
        # Raster bytes themselves are pinned and checked by assert_no_drift above.
        result["reviewed"] = True
    except Exception as error:  # noqa: BLE001 -- evidence errors are reported per artifact
        result["issues"].append(safe_issue(error))
        # No obsolete artifact may retain a green stage. A current render with only an
        # obsolete independent review keeps its automated stages, but never reviewed.
        if not binding_valid:
            for stage in STAGES:
                result[stage] = False
            document = None
    return result, document


def add_bundles(report, baseline_path, bundle_dirs, documents, records):
    valid = {}
    candidates = {}
    articles = {row["slug"]: row for row in report["baseline_articles"]}
    for directory in sorted(set(map(Path, bundle_dirs)), key=str):
        try:
            manifest_sha = sha(directory / "release-manifest.json")
            bundle = publisher.verify_bundle(directory, baseline_path, manifest_sha)
            valid[manifest_sha] = bundle
            for entry in bundle.entries:
                for locale in entry["locales"]:
                    key = (entry["slug"], locale)
                    record = records[key]
                    target = (
                        bundle.packs[entry["slug"]]
                        .locales[locale]
                        .model_dump(mode="json")
                    )
                    old = articles[entry["slug"]]["locale_documents"].get(locale)
                    unchanged = old is not None and normalized(old) == target
                    try:
                        if not unchanged:
                            require(
                                record["reviewed"],
                                "Bundle lacks current independent review",
                            )
                            expected = documents[key]
                            if record["required_translation"]:
                                expected, _ = assembler.localize_links(
                                    expected, locale, articles
                                )
                            require(
                                expected == target,
                                "Bundle differs from current reviewed document",
                            )
                        candidates.setdefault(key, []).append(
                            {
                                "manifest_sha256": manifest_sha,
                                "document_sha256": digest(target),
                            }
                        )
                    except Exception as error:  # noqa: BLE001 -- evidence errors are reported per artifact
                        record["issues"].append(safe_issue(error))
        except Exception as error:  # noqa: BLE001 -- evidence errors are reported per artifact
            report["errors"].append(
                {"file": str(directory), "error": safe_issue(error)}
            )
    for key, values in candidates.items():
        if len({value["document_sha256"] for value in values}) > 1:
            records[key]["issues"].append("Conflicting assembled document hashes")
            continue
        records[key]["assembled"] = True
        records[key]["bundles"] = sorted(
            values, key=lambda value: value["manifest_sha256"]
        )
    return valid


def operation_complete(journal, accepted, pending, slug, locale, phase):
    ops = [
        op
        for op in journal["operations"][phase]
        if op["slug"] == slug and op["locale"] == locale
    ]
    return bool(ops) and all(
        op["id"] in journal["done"][phase]
        and op["id"] in accepted
        and (pending is None or op["id"] != pending["id"])
        for op in ops
    )


def add_journals(report, paths, bundles, records):
    by_manifest = {}
    for path in sorted(set(map(Path, paths)), key=str):
        try:
            journal = read(path)
            manifest_sha = journal["manifest_sha256"]
            require(manifest_sha in bundles, "Journal does not match a verified bundle")
            publisher.validate_journal(bundles[manifest_sha], journal)
            by_manifest.setdefault(manifest_sha, []).append((path, journal))
        except Exception as error:  # noqa: BLE001 -- evidence errors are reported per artifact
            report["errors"].append({"file": str(path), "error": safe_issue(error)})
    for manifest_sha, entries in sorted(by_manifest.items()):
        if len({digest(journal) for _, journal in entries}) != 1:
            report["errors"].append(
                {"file": manifest_sha, "error": "Conflicting journals for one bundle"}
            )
            continue
        path, journal = entries[0]
        bundle = bundles[manifest_sha]
        try:
            require(
                journal.get("slugs") == bundle.slugs,
                "Journal article scope differs from bundle",
            )
            accepted = {
                row["id"]
                for row in journal["history"]
                if row.get("status")
                in {"committed", "committed_reconciled", "unchanged"}
                and "id" in row
            }
            for row in journal["history"]:
                if row.get("status") == "stopped":
                    report["errors"].append(
                        {
                            "file": str(path),
                            "error": "journal_stopped:" + row.get("reason", "unknown"),
                        }
                    )
            pending = journal.get("pending")
            if pending:
                report["errors"].append(
                    {"file": str(path), "error": "journal_pending:" + pending["id"]}
                )
            for entry in bundle.entries:
                state = journal["expected"].get(entry["slug"])
                if state is None:
                    continue
                for locale in entry["locales"]:
                    record = records[(entry["slug"], locale)]
                    if not record["assembled"]:
                        continue
                    target_sha = digest(
                        bundle.packs[entry["slug"]]
                        .locales[locale]
                        .model_dump(mode="json")
                    )
                    if not any(
                        item["manifest_sha256"] == manifest_sha
                        for item in record.get("bundles", [])
                    ):
                        continue
                    actual = state["locales"].get(locale)
                    if actual is None or actual["draft_sha256"] != target_sha:
                        continue

                    if operation_complete(
                        journal, accepted, pending, entry["slug"], locale, "drafts"
                    ):
                        record["draft_imported"] = True
                    phase = "publish-hubs" if entry["hub"] else "publish-articles"
                    if (
                        locale in entry["publish_locales"]
                        and operation_complete(
                            journal, accepted, pending, entry["slug"], locale, phase
                        )
                        and actual.get("published_version") == actual["version"]
                        and actual.get("published_sha256") == target_sha
                        and actual.get("latest_sha256") == target_sha
                        and actual.get("latest_action") == "published"
                        and actual.get("latest_actor") == journal["actor_id"]
                    ):
                        record["published"] = True
                        record["publication"].append(
                            {
                                "manifest_sha256": manifest_sha,
                                "document_sha256": target_sha,
                                "published_version": actual["published_version"],
                                "journal_sha256": sha(path),
                            }
                        )
        except Exception as error:  # noqa: BLE001 -- evidence errors are reported per artifact
            report["errors"].append({"file": str(path), "error": safe_issue(error)})


def add_browser(report, paths, records):
    for path in sorted(set(map(Path, paths)), key=str):
        try:
            evidence = read(path)
            require(
                evidence.get("schema_version") == 1
                and evidence.get("baseline_sha256") == report["baseline_sha256"],
                "Browser evidence baseline mismatch",
            )
            for entry in evidence["entries"]:
                key = (entry["slug"], entry["locale"])
                require(key in records, "Browser evidence outside baseline")
                record = records[key]
                expected_path = (
                    f"/life/{entry['slug']}"
                    if record["kind"] == "life"
                    else f"/guides/{record['kind']}/{entry['slug']}"
                )
                try:
                    require(
                        record["published"]
                        and any(
                            all(
                                entry.get(key) == publication[key]
                                for key in (
                                    "document_sha256",
                                    "manifest_sha256",
                                    "published_version",
                                )
                            )
                            for publication in record["publication"]
                        ),
                        "Browser evidence does not match recorded publication",
                    )
                    require(
                        entry.get("url")
                        == f"https://mokaair.com/{entry['locale']}{expected_path}",
                        "Browser evidence URL mismatch",
                    )
                    require(
                        all(
                            entry.get("checks", {}).get(check) is True
                            for check in (
                                "body",
                                "images",
                                "canonical",
                                "hreflang",
                                "links",
                                "desktop",
                                "mobile",
                            )
                        ),
                        "Browser checks incomplete",
                    )
                    require(
                        bool(entry.get("evidence")),
                        "Browser verification has no captured evidence",
                    )
                    for capture in entry["evidence"]:
                        require(
                            sha(publisher.safe_path(path.parent, capture["path"]))
                            == capture["sha256"],
                            "Browser capture hash changed",
                        )
                    record["browser_verified"] = True
                except Exception as error:  # noqa: BLE001 -- evidence errors are reported per artifact
                    record["issues"].append(safe_issue(error))
        except Exception as error:  # noqa: BLE001 -- evidence errors are reported per artifact
            report["errors"].append({"file": str(path), "error": safe_issue(error)})


def build_report(
    baseline_path, work, *, bundle_dirs=(), journals=(), browser_evidence=(), root=ROOT
):
    baseline_path, work, root = Path(baseline_path), Path(work), Path(root)
    baseline = read(baseline_path)
    require(baseline.get("schema_version") == 1, "Unsupported baseline schema")
    articles = sorted(baseline["articles"], key=lambda row: row["slug"])
    require(
        len({article["slug"] for article in articles}) == len(articles),
        "Duplicate baseline article",
    )
    report = {
        "schema_version": 1,
        "baseline_sha256": sha(baseline_path),
        "baseline_repo_commit": baseline.get("repo_commit"),
        "baseline_captured_at": baseline.get("captured_at"),
        "live_database_checked": False,
        "baseline_articles": articles,
        "articles": [],
        "batches": [],
        "errors": [],
    }
    records, documents = {}, {}
    for article in articles:
        require(
            digest(article["source_document"]) == article["source_sha256"],
            "Baseline source hash mismatch",
        )
        for locale in publisher.LOCALES:
            record, document = staged_locale(article, locale, work, root)
            record["kind"] = article["kind"]
            records[(article["slug"], locale)] = record
            documents[(article["slug"], locale)] = document
    bundles = add_bundles(report, baseline_path, bundle_dirs, documents, records)
    add_journals(report, journals, bundles, records)
    add_browser(report, browser_evidence, records)
    assigned = set()
    for batch in sorted(baseline.get("batches", []), key=lambda row: row["id"]):
        slugs = batch["slugs"]
        require(
            1 <= len(slugs) <= 20 and len(set(slugs)) == len(slugs),
            "Batch requires 1..20 distinct articles",
        )
        require(
            set(slugs) <= {article["slug"] for article in articles}
            and not assigned.intersection(slugs),
            "Batch includes unknown or repeated article",
        )
        report["batches"].append({"id": batch["id"], "slugs": sorted(slugs)})
        assigned.update(slugs)
    pending = [
        article["slug"]
        for article in articles
        if article.get("target_locales", article["missing_locales"])
        and article["slug"] not in assigned
    ]
    for start in range(0, len(pending), 20):
        report["batches"].append(
            {
                "id": f"unassigned-{start // 20 + 1:03d}",
                "slugs": pending[start : start + 20],
            }
        )
    batches = {
        slug: batch["id"] for batch in report["batches"] for slug in batch["slugs"]
    }
    for article in articles:
        locales = [records[(article["slug"], locale)] for locale in publisher.LOCALES]
        for row in locales:
            row["issues"] = sorted(set(row["issues"]))
            row["publication"] = sorted(
                row["publication"],
                key=lambda value: (
                    value["manifest_sha256"],
                    value["published_version"],
                ),
            )
        required = [row for row in locales if row["required_work"]]
        report["articles"].append(
            {
                "slug": article["slug"],
                "kind": article["kind"],
                "baseline_status": article["status"],
                "batch": batches.get(article["slug"]),
                "missing_locales": sorted(article["missing_locales"]),
                "target_locales": sorted(
                    article.get("target_locales", article["missing_locales"])
                ),
                "publication_missing_locales": sorted(
                    article.get("publication_missing_locales", [])
                ),
                "baseline_published_locales": sorted(article["published_locales"]),
                "required_language_documents": len(required),
                "completed": {
                    stage: sum(row[stage] for row in required) for stage in STAGES
                },
                "all_required": {
                    stage: bool(required) and all(row[stage] for row in required)
                    for stage in STAGES
                },
                "locales": locales,
            }
        )
    report.pop("baseline_articles")
    work_statuses = Counter(record["work_status"] for record in records.values())
    staged_work_statuses = {
        status: count
        for status, count in sorted(work_statuses.items())
        if status != "not_started"
    }
    report["summary"] = {
        "articles": len(articles),
        "baseline_statuses": dict(
            sorted(Counter(article["status"] for article in articles).items())
        ),
        "missing_language_documents": sum(
            len(article["missing_locales"]) for article in articles
        ),
        "target_language_documents": sum(
            len(article.get("target_locales", article["missing_locales"]))
            for article in articles
        ),
        "publication_missing_language_documents": sum(
            len(article.get("publication_missing_locales", [])) for article in articles
        ),
        "baseline_complete_articles": sum(
            not article["missing_locales"] for article in articles
        ),
        "batches": len(report["batches"]),
        "missing_language_progress": {
            stage: sum(
                record[stage]
                for record in records.values()
                if record["required_translation"]
            )
            for stage in STAGES
        },
        "target_language_progress": {
            stage: sum(
                record[stage] for record in records.values() if record["required_work"]
            )
            for stage in STAGES
        },
        "all_staged_language_progress": {
            stage: sum(record[stage] for record in records.values()) for stage in STAGES
        },
        "staged_jobs": sum(staged_work_statuses.values()),
        "staged_work_statuses": staged_work_statuses,
        "work_statuses": dict(sorted(work_statuses.items())),
        "article_locale_issues": sum(bool(row["issues"]) for row in records.values()),
    }
    expected = baseline.get("summary", {})
    for key in ("articles", "missing_language_documents"):
        if key in expected and expected[key] != report["summary"][key]:
            report["errors"].append(
                {
                    "file": str(baseline_path),
                    "error": f"Baseline summary mismatch: {key}",
                }
            )
    report["errors"] = sorted(
        {json.dumps(row, sort_keys=True) for row in report["errors"]}
    )
    report["errors"] = [json.loads(row) for row in report["errors"]]
    return report


def write_report(report, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "progress.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    fields = [
        "slug",
        "kind",
        "baseline_status",
        "batch",
        "missing_locales",
        "target_locales",
        *STAGES,
        "issues",
    ]
    with (output / "progress.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for article in report["articles"]:
            writer.writerow(
                {
                    "slug": article["slug"],
                    "kind": article["kind"],
                    "baseline_status": article["baseline_status"],
                    "batch": article["batch"],
                    "missing_locales": ";".join(article["missing_locales"]),
                    "target_locales": ";".join(article["target_locales"]),
                    **{
                        stage: str(article["completed"][stage])
                        + "/"
                        + str(article["required_language_documents"])
                        for stage in STAGES
                    },
                    "issues": " | ".join(
                        f"{row['locale']}:{issue}"
                        for row in article["locales"]
                        for issue in row["issues"]
                    ),
                }
            )
    summary = report["summary"]
    commit = report.get("baseline_repo_commit")
    captured = report.get("baseline_captured_at")
    lines = [
        "# 文章五語補齊進度",
        "",
        (
            "固定歷史快照基準（不代表目前儲存庫或正式站狀態）："
            f"{summary['articles']:,} 篇文章，"
            f"缺少 {summary['missing_language_documents']:,} 份語言稿。"
        ),
        "",
        "快照來源："
        + (f"儲存庫 commit `{commit}`" if commit else "基準未記錄儲存庫 commit")
        + (f"；擷取時間 `{captured}`。" if captured else "；基準未記錄擷取時間。"),
        "",
        "下列完成數只計基準缺漏語言；既有語言、圖片更新與逐篇證據另列於 JSON。",
        "",
        "| 階段 | 已有吻合證據的語言稿 |",
        "|---|---:|",
    ]
    labels = {
        "translated": "翻譯與結構檢查",
        "rendered": "圖片渲染與自動版面檢查",
        "reviewed": "獨立文字／圖片／字型審查",
        "assembled": "組包",
        "draft_imported": "草稿匯入紀錄",
        "published": "公開發布紀錄",
        "browser_verified": "正式站桌面／手機驗證",
    }
    lines.extend(
        f"| {labels[stage]} | {summary['target_language_progress'][stage]} |"
        for stage in STAGES
    )
    lines += [
        "",
        "工作目錄內有 "
        f"{summary['staged_jobs']} 個 staged 文章語言工作："
        + (
            ", ".join(
                f"{status}={count}"
                for status, count in summary["staged_work_statuses"].items()
            )
            or "無"
        )
        + "。",
        "",
        "匯入與發布依持久 journal 記錄；此報表未重新查詢正式資料庫。未附瀏覽器證據不會視為已驗證。",
        (
            f"共 {summary['batches']} 批，每批最多 20 篇；"
            f"{summary['article_locale_issues']} 個文章語言有待處理問題，"
            f"另有 {len(report['errors'])} 項整批證據錯誤。"
        ),
        "",
        "逐篇明細：`progress.csv`；完整證據、問題與批次文章清單：`progress.json`。",
        "",
    ]
    (output / "progress.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, action="append", default=[])
    parser.add_argument("--journal", type=Path, action="append", default=[])
    parser.add_argument("--browser-evidence", type=Path, action="append", default=[])
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    report = build_report(
        args.baseline,
        args.work,
        bundle_dirs=args.bundle,
        journals=args.journal,
        browser_evidence=args.browser_evidence,
        root=args.root,
    )
    write_report(report, args.output)
    print(json.dumps(report["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
