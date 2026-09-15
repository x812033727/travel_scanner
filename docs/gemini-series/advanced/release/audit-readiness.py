"""Verify historical evidence bytes and report outstanding acceptance without upgrading it."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TRACKS = ("work", "research", "creative", "md", "automation", "api")


def digest(file: Path) -> str:
    return hashlib.sha256(file.read_bytes()).hexdigest()


def read(file: Path) -> dict:
    return json.loads(file.read_text(encoding="utf-8"))


def safe_file(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("expected portable relative path")
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError("unsafe evidence path: " + relative)
    file = (root / candidate).resolve()
    if not file.is_relative_to(root.resolve()) or not file.is_file():
        raise ValueError("missing or escaped evidence: " + relative)
    return file


def references(value):
    if isinstance(value, dict):
        if "sha256" in value and ("path" in value or "file" in value):
            yield value.get("path", value.get("file")), value["sha256"]
        if "sourceSha256" in value and "source" in value:
            yield value["source"], value["sourceSha256"]
        for child in value.values():
            yield from references(child)
    elif isinstance(value, list):
        for child in value:
            yield from references(child)


def verify_references(root: Path, rows, *, prefix="") -> list[dict]:
    verified = {}
    for relative, expected in rows:
        if prefix and not relative.startswith(("apps/", "docs/", "tools/")):
            relative = prefix + "/" + relative
        file = safe_file(root, relative)
        actual = digest(file)
        if actual != expected:
            raise ValueError("evidence hash mismatch: " + relative)
        verified[relative] = {"path": relative, "sha256": actual}
    if not verified:
        raise ValueError("evidence receipt contains no hashed files")
    return sorted(verified.values(), key=lambda row: row["path"])


def audit(root: Path = ROOT, here: Path = HERE) -> dict:
    plan = read(here / "acceptance-plan.json")
    candidate = read(here / "candidate/review.json")
    series = read(here / "candidate/guide-series.json")
    if candidate.get("schemaVersion") != "gemini-review-candidate-v1" or candidate.get("publishable") is not False:
        raise ValueError("expected a non-publishable review candidate")
    if [row["number"] for row in series["articles"]] != list(range(1, 87)):
        raise ValueError("candidate must have exact articles 1–86")
    if candidate["candidateCatalogueSha256"] != digest(here / "candidate/guide-series.json"):
        raise ValueError("candidate catalogue changed")
    if candidate["runtimeCatalogueSha256"] != digest(root / "apps/web/lib/guide-series.json"):
        raise ValueError("production catalogue changed during candidate preparation")
    candidate_files = verify_references(root, references(candidate["inputs"]))
    # Reuse the API's real persisted-content schema for every candidate page.
    sys.path.insert(0, str(root / "apps/api"))
    from app.guides.content_pack import ArticlePack
    from app.guides.pack_ingest import _body_length

    schema_rows = []
    expected_slugs = {series["hubSlug"], *(row["slug"] for row in series["articles"])}
    pack_rows = [row for row in candidate_files if "/content/" in row["path"] and row["path"].endswith(".json")]
    for row in pack_rows:
        pack = ArticlePack.model_validate_json(safe_file(root, row["path"]).read_text(encoding="utf-8"))
        schema_rows.append({"slug": pack.slug, "schema": "passed", "characters": _body_length(pack.locales["zh-TW"])})
    if len(schema_rows) != 87 or {row["slug"] for row in schema_rows} != expected_slugs:
        raise ValueError("candidate evidence does not contain exactly 87 content packs")
    (here / "candidate/schema-validation.json").write_text(
        json.dumps({"status": "passed", "pages": 87, "schema": "Existing FastAPI ArticlePack", "records": sorted(schema_rows, key=lambda row: row["slug"])}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    if [row["number"] for row in plan["lessons"]] != list(range(51, 87)):
        raise ValueError("acceptance plan must contain each of 51–86 exactly once")
    tracks, lesson_rows, blockers = [], [], []
    unique = {row["path"]: row["sha256"] for row in candidate_files}
    for track in TRACKS:
        directory = root / "docs/gemini-series/advanced/content" / track
        review_file = directory / "verification/authoring-review.json"
        visual_file = directory / "verification/visual-review.json"
        review, visual = read(review_file), read(visual_file)
        author_files = verify_references(root, references(review))
        visual_files = verify_references(root, references(visual), prefix=directory.relative_to(root).as_posix())
        for row in [*author_files, *visual_files]:
            unique[row["path"]] = row["sha256"]
        artwork = []
        for article in [row for row in series["articles"] if row.get("track") == track]:
            number, slug = article["number"], article["slug"]
            for name in ("hero", "diagram-1"):
                source = directory / str(number) / (name + ".svg")
                public = root / "apps/web/public/guides" / slug / (name + ".svg")
                if digest(source) != digest(public):
                    raise ValueError(f"{number}: public artwork differs from reviewed source")
                artwork.append(source.relative_to(root).as_posix())
                for suffix in (".png", "-mobile.png"):
                    preview = (directory / "verification/renders" / slug / (name + suffix)).relative_to(root).as_posix()
                    if preview not in {row["path"] for row in visual_files}:
                        raise ValueError(f"{number}: missing historical visual review for {preview}")
            step = next(row for row in plan["lessons"] if row["number"] == number)
            if step["track"] != track:
                raise ValueError(f"{number}: wrong acceptance track")
            lesson_rows.append({**step, "slug": slug, "title": article["title"], "authorReceipt": review_file.relative_to(root).as_posix()})
        tracks.append({"track": track, "authorReceipt": review_file.relative_to(root).as_posix(), "authorReceiptSha256": digest(review_file),
                       "authorPublishable": review.get("publishable"), "authorFilesVerified": len(author_files),
                       "visualReceipt": visual_file.relative_to(root).as_posix(), "visualReceiptSha256": digest(visual_file),
                       "visualFilesVerified": len(visual_files), "originalArtworks": len(artwork)})
        if review.get("publishable") is not True:
            blockers.append(track + ": author receipt is not publishable")
    pending = [row["number"] for row in lesson_rows if row["externalAcceptance"] == "pending"]
    blockers.extend([f"{len(pending)} lessons still require actual model/account/device evidence", "fresh Taiwan price amounts unavailable", "candidate requires review/merge, database dry-run and controlled publication", "public pages and sitemap not verified for this candidate"])
    combined = "\n".join(f"{key}\t{value}" for key, value in sorted(unique.items()))
    report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "status": "structural-checks-passed-release-not-ready", "releaseReady": False,
              "evidenceHashEncoding": "SHA-256 of raw file bytes; no fallback normalization", "candidateFilesVerified": len(candidate_files),
              "uniqueEvidenceFilesVerified": len(unique), "schemasValidated": len(schema_rows), "evidenceSetSha256": hashlib.sha256(combined.encode()).hexdigest(),
              "tracks": tracks, "newArtworks": sum(row["originalArtworks"] for row in tracks), "articlePreviewsVerified": 144,
              "pendingExternalLessonNumbers": sorted(pending), "blockingItems": blockers, "lessons": sorted(lesson_rows, key=lambda row: row["number"]),
              "limits": ["Hash verification rechecks preserved evidence, not model behavior or fresh visual inspection.", "69–71 have real Windows CLI module evidence; no macOS/Linux or second-version pass is implied.", "This report cannot authorize or trigger publication."]}
    return report


def markdown(report: dict) -> str:
    lines = ["# Gemini 深入教學逐篇驗收", "", "本機 36 篇原稿、配圖、練習包與作者證據已核對；仍有 33 篇需要真實帳號、模型或裝置操作。本表列出需要取得的成果，並非已完成實測。", "",
             "69–71 已有 Windows CLI 0.59.0 實際模組證據；73 另有 Node 22 原生 CLI 安裝、更新與回退紀錄，但模型啟用 Skill 仍待驗。跨系統及另一 CLI 版本未宣稱通過。", "",
             "| 篇號 | 本機可追查證據 | 待取得的實測成果 | 所需環境 |", "| --- | --- | --- | --- |"]
    for row in report["lessons"]:
        lines.append(f'| {row["number"]} | [{row["title"]}](../content/{row["track"]}/{row["number"]}/lesson.md)；[作者紀錄](../content/{row["track"]}/verification/authoring-review.json) | {row["requiredEvidence"]} | {row["environment"]} |')
    lines.extend(["", "發布前還要完成：當日台灣價格、候選稿審查與合併、資料庫 dry-run、限定篇章逐篇發布、新舊 86 篇核對後開放目錄，以及公開頁面／sitemap 驗收。", "", "完整機器可讀紀錄：[readiness.json](readiness.json)。"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    try:
        result = audit()
        (HERE / "readiness.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        (HERE / "ACCEPTANCE.md").write_text(markdown(result), encoding="utf-8", newline="\n")
        print(json.dumps({key: result[key] for key in ["status", "releaseReady", "uniqueEvidenceFilesVerified", "newArtworks", "pendingExternalLessonNumbers"]}, ensure_ascii=False))
        if "--require-ready" in sys.argv:
            sys.exit(1)
    except (ValueError, KeyError, OSError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
