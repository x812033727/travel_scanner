"""Build lesson 57's isolated live-evidence revision; leave historical author files intact."""

import hashlib
import importlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
ROOT = next(p for p in HERE.parents if (p / "tools/tasks.mjs").exists())
LIVE = RESEARCH / "verification/live-20260915/57"
sys.path.insert(0, str(ROOT / "docs/gemini-series"))
build_advanced = importlib.import_module("build").build_advanced
lint_all = importlib.import_module("app.guides.pack_ingest").lint_all

ARCHIVE_CHECK = '''"""Verify bundled bytes without making Google calls."""
import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parent
entries = json.loads((base / "evidence-index.json").read_text("utf-8"))
for entry in entries:
    path = (base / entry["archivePath"]).resolve()
    assert path.is_relative_to(base)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"], path
print(f"Verified {len(entries)} bundled files. No cloud calls or publication.")
'''


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    history = json.loads((RESEARCH / "verification/authoring-review.json").read_text("utf-8"))[
        "files"
    ]
    for item in history:
        assert sha((ROOT / item["path"]).read_bytes()) == item["sha256"], item["path"]
    lesson = (HERE / "lessons/57.md").read_text("utf-8")
    original = (RESEARCH / "57/lesson.md").read_text("utf-8")
    assert re.findall(r"^## .+$", lesson, re.MULTILINE) == re.findall(
        r"^## .+$", original, re.MULTILINE
    )
    with tempfile.TemporaryDirectory(prefix="gemini57-revision-") as directory:
        temporary = Path(directory)
        track = temporary / "content/research"
        target = track / "57"
        target.mkdir(parents=True)
        examples = track / "examples"
        examples.mkdir()
        for name in ("hero.svg", "diagram-1.svg", "hero.jpg"):
            shutil.copyfile(RESEARCH / "57" / name, target / name)
        (target / "lesson.md").write_text(lesson, encoding="utf-8", newline="\n")
        meta = json.loads((RESEARCH / "57/meta.json").read_text("utf-8"))
        meta["diagram_caption"] = (
            "六個來源 ID 保留更新紀錄，名額由 24 人改為 30 人。"
            "兩種方式的來源、回答與舊筆記已實測；自動摘要仍需逐句查核。原創概念圖，非介面截圖。"
        )
        for source in meta["sources"]:
            source["checked_on"] = "2026-09-15"
        archive_name = "lesson-57-live-20260915.zip"
        entries = {}
        for path in sorted((RESEARCH / "examples/57").rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                entries["original/57/" + path.relative_to(RESEARCH / "examples/57").as_posix()] = (
                    path
                )
        entries["original/research_checks.py"] = RESEARCH / "examples/research_checks.py"
        for path in sorted(LIVE.iterdir()):
            if path.is_file():
                entries["live/" + path.name] = path
        index = [
            {
                "archivePath": name,
                "source": path.relative_to(ROOT).as_posix(),
                "sha256": sha(path.read_bytes()),
            }
            for name, path in entries.items()
        ]
        payload = {name: path.read_bytes() for name, path in entries.items()}
        payload["verify_archive.py"] = ARCHIVE_CHECK.encode()
        payload["evidence-index.json"] = (
            json.dumps(index, ensure_ascii=False, indent=2) + "\n"
        ).encode()
        payload["README.md"] = (
            "# 第 57 篇練習與實測\n\n"
            "original/57 是可重做的原始教材，not_run 空白表不代表本輪實測狀態。"
            "live/ 保存五筆實際回答、四份筆記與來源、引用、同步及限制。\n\n"
            "解壓後執行 python verify_archive.py 檢查保存位元組；"
            "進入 original 後執行 python research_checks.py versions 57 核對教材。"
            "兩項檢查都不呼叫 Google。"
            "實測報告 live/README.md 的站內相對連結需於 repository 閱讀。\n\n"
            "Drive 手動同步已驗；定期自動同步延遲、手機與分享權限未驗。"
            "自動來源指南曾加入未受來源支持的描述，保留失敗案例。"
            "沒有私人雲端連結或金鑰。本包尚未公開；授權見 original/57/LICENSE.txt。\n"
        ).encode()
        with zipfile.ZipFile(examples / archive_name, "w") as archive:
            for name, data in sorted(payload.items()):
                info = zipfile.ZipInfo(name, date_time=(2026, 9, 15, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, data)
        extracted = temporary / "extracted"
        with zipfile.ZipFile(examples / archive_name) as archive:
            assert archive.testzip() is None
            assert len(archive.namelist()) == len(payload)
            for name, data in payload.items():
                assert archive.read(name) == data, name
            archive.extractall(extracted)
        for command, cwd in (
            ([sys.executable, "-X", "utf8", "verify_archive.py"], extracted),
            (
                [sys.executable, "-X", "utf8", "research_checks.py", "versions", "57"],
                extracted / "original",
            ),
        ):
            # Both commands run local, hash-verified repository fixtures without a shell.
            subprocess.run(command, cwd=cwd, check=True, timeout=30)  # noqa: S603
        meta["downloads"][0] = {
            "source": "examples/" + archive_name,
            "filename": archive_name,
            "text": "下載第 57 篇練習與真實實測增補",
        }
        shutil.copyfile(
            RESEARCH / "examples/research-verification.zip", examples / "research-verification.zip"
        )
        (target / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        report = build_advanced("research", [57], temporary / "content", HERE / "output", False)
    output = HERE / "output"
    findings = lint_all(
        output / "apps/api/app/guides/content",
        output / "apps/web/public",
        slugs={"notebooklm-source-versioning"},
    )
    problems = [p for values in findings.values() for p in values if p.level == "error"]
    assert not problems, problems
    for item in history:
        assert sha((ROOT / item["path"]).read_bytes()) == item["sha256"]
    files = [
        {"path": p.relative_to(HERE).as_posix(), "sha256": sha(p.read_bytes())}
        for p in sorted(output.rglob("*"))
        if p.is_file()
    ]
    files.append({"path": "lessons/57.md", "sha256": sha((HERE / "lessons/57.md").read_bytes())})
    review = {
        "date": "2026-09-15",
        "lessons": report,
        "publishable": False,
        "historicalFilesUnchanged": len(history),
        "archiveSourceFiles": len(index),
        "archiveChecks": "CRC, member bytes, extracted hash checker and versions fixture passed",
        "packLint": "passed",
        "preservedSectionAnchors": True,
        "artwork": "Previously reviewed art reused; scoped caption updated.",
        "remaining": [
            "Series integration and publication",
            "Other research lessons 58-62 live tests",
        ],
        "files": files,
    }
    (HERE / "review.json").write_text(
        json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({k: v for k, v in review.items() if k != "files"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
