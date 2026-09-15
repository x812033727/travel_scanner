"""Build three revised lessons in an isolated output; preserve historical author files."""

import hashlib
import importlib
import io
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
ROOT = next(p for p in HERE.parents if (p / "tools/tasks.mjs").exists())
LIVE = WORK / "verification/live-20260915"
sys.path.insert(0, str(ROOT / "docs/gemini-series"))
build_advanced = importlib.import_module("build").build_advanced

NUMBERS = (52, 53, 54)
CAPTIONS = {
    52: (
        "資料變更後重跑相同題庫。本次三十六份回歸含拒答與文字問題，"
        "未通過完整品質驗收。原創概念圖，非介面截圖。"
    ),
    53: (
        "先核對公式，再檢查介面。本次模型 v4 三十五項限定觀察通過，"
        "實體手機等範圍仍未驗。原創概念圖，非介面截圖。"
    ),
    54: (
        "五封合成信保留更正與未知。Gmail／Docs／Sheets 貼入流程已測，"
        "接收者權限未驗。原創概念圖，非介面截圖。"
    ),
}
VERIFY_ARCHIVE = '''"""Verify bundled bytes; this does not rerun Google or approve model quality."""
import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parent
entries = json.loads((base / "evidence-index.json").read_text(encoding="utf-8"))
for entry in entries:
    path = (base / entry["archivePath"]).resolve()
    assert path.is_relative_to(base), entry["archivePath"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"], entry["archivePath"]
print(f"Verified {len(entries)} bundled files. Semantic approval and publication remain pending.")
'''


def digest(data):
    return hashlib.sha256(data).hexdigest()


def historical_check():
    records = json.loads((WORK / "verification/authoring-review.json").read_text(encoding="utf-8"))[
        "files"
    ]
    for record in records:
        assert digest((ROOT / record["path"]).read_bytes()) == record["sha256"], record["path"]
    return len(records)


def make_bundle(number):
    entries, index = {}, []
    for source in sorted((WORK / "examples" / str(number)).rglob("*")):
        if source.is_file() and "__pycache__" not in source.parts:
            entries[
                "original/" + source.relative_to(WORK / "examples" / str(number)).as_posix()
            ] = source
    live = LIVE / str(number)
    if number == 52:
        selected = list((live / "raw").glob("*.txt")) + list((live / "corrected/raw").glob("*.txt"))
        selected += [
            live / name
            for name in (
                "gem-instructions-corrected.md",
                "environment.json",
                "captured.json",
                "capture-audit.json",
                "v1-setup.json",
                "corrected/captured.json",
                "corrected/capture-audit.json",
            )
        ]
    else:
        selected = [
            p
            for p in live.iterdir()
            if p.is_file()
            and p.suffix in {".json", ".txt", ".html", ".csv", ".md"}
            and p.name != "README.md"
        ]
    for source in sorted(selected):
        entries["live/" + source.relative_to(live).as_posix()] = source
    payload = {}
    for name, source in entries.items():
        data = source.read_bytes()
        payload[name] = data
        index.append(
            {
                "archivePath": name,
                "source": source.relative_to(ROOT).as_posix(),
                "sha256": digest(data),
            }
        )
    readme = f"""# 第 {number} 篇：原始練習與 2026-09-15 實測增補

original/ 保留原作者練習，內有 not_run 的空白表是供重做使用，不是本轮實測狀態。
live/ 保存這輪模型產物及證據；environment.json 與 capture-audit.json 記錄環境和限制。
evidence-index.json 保存來源檔案與 SHA256。解壓後執行 python verify_archive.py 檢查保存位元組。
這個檢查不重新呼叫 Google、不驗證雲端目前狀態，也不等於人工語意核准。

第 52 篇：original/ 手冊與题庫；live/raw/ 原始 v1/v2 共 24 份，live/corrected/raw/ 修正後 12 份。
第 53 篇：original/ 作者參考工具；live/budget-v4.html 是本次模型成品，前版失敗另存。
第 54 篇：original/ 合成信與檢查器；live/ 的文件文字和試算表 TSV 是介面擷取。
candidate-normalized.csv 是 Codex 衍生資料。
只會包含本篇對應檔案。完整實測報告在 repository 的 work/verification/live-20260915/{number}/。

原作者練習授權見 original/LICENSE.txt。實測檔案標示為模型輸出或觀察，不冒稱 Google 官方文件。
本包尚未公開；文章與整套發布仍須其他驗收。沒有附帳號、金鑰或私人雲端連結。
"""
    payload["README.md"] = readme.replace("本轮", "本輪").replace("题庫", "題庫").encode()
    payload["verify_archive.py"] = VERIFY_ARCHIVE.encode()
    payload["evidence-index.json"] = (
        json.dumps(index, ensure_ascii=False, indent=2) + "\n"
    ).encode()
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    with zipfile.ZipFile(io.BytesIO(stream.getvalue())) as archive:
        assert archive.testzip() is None
        for name, data in payload.items():
            assert archive.read(name) == data, name
    return stream.getvalue(), len(index)


def main():
    historical = historical_check()
    with tempfile.TemporaryDirectory(prefix="gemini-live-revision-") as temp:
        content_root = Path(temp) / "content"
        track = content_root / "work"
        track.mkdir(parents=True)
        shutil.copytree(
            WORK / "examples", track / "examples", ignore=shutil.ignore_patterns("__pycache__")
        )
        bundle_counts = {}
        for number in NUMBERS:
            target = track / str(number)
            target.mkdir()
            for name in ("hero.svg", "diagram-1.svg", "hero.jpg"):
                shutil.copyfile(WORK / str(number) / name, target / name)
            lesson = (HERE / "lessons" / f"{number}.md").read_text(encoding="utf-8")
            original = (WORK / str(number) / "lesson.md").read_text(encoding="utf-8")
            assert re.findall(r"^## .+$", lesson, re.MULTILINE) == re.findall(
                r"^## .+$", original, re.MULTILINE
            ), number
            (target / "lesson.md").write_text(lesson, encoding="utf-8", newline="\n")
            meta = json.loads((WORK / str(number) / "meta.json").read_text(encoding="utf-8"))
            meta["diagram_caption"] = CAPTIONS[number]
            if number == 54:
                meta["sources"].append(
                    {
                        "title": "Gmail 中建立文件與試算表",
                        "url": "https://support.google.com/mail/answer/14355636?hl=en",
                        "checked_on": "2026-09-15",
                    }
                )
                meta["sources"][1]["checked_on"] = "2026-09-15"
            name = f"lesson-{number}-live-20260915.zip"
            data, count = make_bundle(number)
            (track / "examples" / name).write_bytes(data)
            bundle_counts[str(number)] = {"filesChecked": count, "sha256": digest(data)}
            meta["downloads"][0] = {
                "source": "examples/" + name,
                "filename": name,
                "text": f"下載第 {number} 篇練習與真實實測增補",
            }
            (target / "meta.json").write_text(
                json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        report = build_advanced("work", list(NUMBERS), content_root, HERE / "output", False)
    assert historical_check() == historical == 154
    records = [
        {"path": p.relative_to(HERE).as_posix(), "sha256": digest(p.read_bytes())}
        for p in sorted((HERE / "output").rglob("*"))
        if p.is_file()
    ]
    for p in (HERE / "lessons").glob("*.md"):
        records.append({"path": p.relative_to(HERE).as_posix(), "sha256": digest(p.read_bytes())})
    review = {
        "revisionDate": "2026-09-15",
        "status": "revised-authoring-with-live-evidence",
        "publishable": False,
        "runtimePacksChanged": False,
        "historicalFilesUnchanged": historical,
        "lessons": report,
        "archives": bundle_counts,
        "preservedSectionAnchors": True,
        "artwork": "Reviewed artwork reused unchanged; captions updated to scoped live results.",
        "remaining": [
            "52 human semantic and response-quality approval",
            "53 untested physical-device and accessibility scopes",
            "54 recipient access and real-inbox retrieval",
            "Series release integration and public verification",
        ],
        "files": records,
    }
    (HERE / "review.json").write_text(
        json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(
        json.dumps(
            {"historicalFilesUnchanged": historical, "lessons": report, "archives": bundle_counts},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
