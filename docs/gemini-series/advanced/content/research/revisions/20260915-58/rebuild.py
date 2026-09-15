"""Build lesson 58's isolated live-evidence revision; leave historical author files intact."""

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
LIVE = RESEARCH / "verification/live-20260915/58"
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
    lesson = (HERE / "lessons/58.md").read_text("utf-8")
    original = (RESEARCH / "58/lesson.md").read_text("utf-8")
    assert re.findall(r"^## .+$", lesson, re.MULTILINE) == re.findall(
        r"^## .+$", original, re.MULTILINE
    )
    with tempfile.TemporaryDirectory(prefix="gemini58-revision-") as directory:
        temporary = Path(directory)
        track = temporary / "content/research"
        target = track / "58"
        target.mkdir(parents=True)
        examples = track / "examples"
        examples.mkdir()
        shutil.copytree(RESEARCH / "examples/58", examples / "58")
        for name in ("hero.svg", "diagram-1.svg", "hero.jpg"):
            shutil.copyfile(RESEARCH / "58" / name, target / name)
        diagram = target / "diagram-1.svg"
        art = diagram.read_text("utf-8")
        assert art.count("五列矩陣已查；模型引用待驗") == 1
        diagram.write_text(
            art.replace("五列矩陣已查；模型引用待驗", "五列引用已核；未知仍留空白"),
            encoding="utf-8", newline="\n",
        )
        (target / "lesson.md").write_text(lesson, encoding="utf-8", newline="\n")
        meta = json.loads((RESEARCH / "58/meta.json").read_text("utf-8"))
        meta["diagram_caption"] = (
            "名額修訂為 30 人，日期提案待確認，餐點資料未知。"
            "五列矩陣與引用已實測；假引文及錯誤主張另做離線檢查。原創概念圖，非介面截圖。"
        )
        for source in meta["sources"]:
            source["checked_on"] = "2026-09-15"
        archive_name = "lesson-58-live-20260915.zip"
        entries = {}
        for path in sorted((RESEARCH / "examples/58").rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                entries["original/58/" + path.relative_to(RESEARCH / "examples/58").as_posix()] = (
                    path
                )
        entries["original/research_checks.py"] = RESEARCH / "examples/research_checks.py"
        for path in sorted(LIVE.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                entries["live/" + path.relative_to(LIVE).as_posix()] = path
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
            "# 第 58 篇練習與實測\n\n"
            "original/58 是作者參考教材，live/ 是三次真實回答、三份筆記、引用與修正。"
            "CSV 由保存的模型文字整理，不是產品直接匯出。假引用與錯誤主張是離線故障。\n\n"
            "解壓後在本目錄執行 python verify_archive.py 檢查保存位元組；"
            "執行 python original/research_checks.py evidence original/58 核對原教材。\n\n"
            "故障練習：python original/research_checks.py evidence live/fault-lab/reviewed；"
            "把尾端 reviewed 換成 fake-quote，預期拒絕 fabricated_quote；"
            "換 bad-claim 時字串檢查仍通過，人工必須拒絕 54 人；repaired 還原後通過。"
            "上述指令均不呼叫 Google。live 內重建腳本與 README 的相對連結需於 repository 使用。\n\n"
            "原始回答仍有章節層級及表格換行問題，詳見 live/README.md。"
            "沒有私人雲端連結或金鑰。未公開；授權見 original/58/LICENSE.txt。\n"
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
                [sys.executable, "-X", "utf8", "research_checks.py", "evidence", "58"],
                extracted / "original",
            ),
        ):
            # Both commands run local, hash-verified repository fixtures without a shell.
            subprocess.run(command, cwd=cwd, check=True, timeout=30)  # noqa: S603
        meta["downloads"][0] = {
            "source": "examples/" + archive_name,
            "filename": archive_name,
            "text": "下載第 58 篇練習與真實實測增補",
        }
        shutil.copyfile(
            RESEARCH / "examples/research-verification.zip", examples / "research-verification.zip"
        )
        (target / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        report = build_advanced("research", [58], temporary / "content", HERE / "output", False)
    output = HERE / "output"
    findings = lint_all(
        output / "apps/api/app/guides/content",
        output / "apps/web/public",
        slugs={"notebooklm-conflicting-sources"},
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
    files.append({"path": "lessons/58.md", "sha256": sha((HERE / "lessons/58.md").read_bytes())})
    review = {
        "date": "2026-09-15",
        "lessons": report,
        "publishable": False,
        "historicalFilesUnchanged": len(history),
        "archiveSourceFiles": len(index),
        "archiveChecks": "CRC, member bytes, extracted hash checker and evidence fixture passed",
        "packLint": "passed",
        "preservedSectionAnchors": True,
        "artwork": "Original hero reused; "
        "diagram footer and caption updated in this revision only.",
        "remaining": [
            "Series integration and publication",
            "Other research lessons 59-62 live tests",
        ],
        "files": files,
    }
    (HERE / "review.json").write_text(
        json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({k: v for k, v in review.items() if k != "files"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
