"""Check saved Workspace observations; never call Google or change cloud files."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "tools/tasks.mjs").exists())


def read(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fnv(text):
    data = text.encode("utf-16le")
    value = 2166136261
    for i in range(0, len(data), 2):
        value = ((value ^ int.from_bytes(data[i:i + 2], "little")) * 16777619) & 0xFFFFFFFF
    return f"{value:08x}"


def normalize_document(text):
    lines = []
    for line in text.replace("**", "").replace("\\.", ".").splitlines():
        line = re.sub(r"^\s*(?:#+\s+|\*\s+)", "", line).strip()
        line = re.sub(r"^\d+\. (?=關於)", "", line)
        if line and line != "&nbsp;":
            lines.append(line)
    return lines


def main():
    env = read("environment.json")
    for entry in env["inputs"]:
        assert sha(ROOT / entry["path"]) == entry["sha256"], entry["path"]
    historical = json.loads(
        (HERE.parents[1] / "authoring-review.json").read_text(encoding="utf-8")
    )["files"]
    assert len(historical) == 154
    for entry in historical:
        assert sha(ROOT / entry["path"]) == entry["sha256"], entry["path"]
    manifest = read("evidence-manifest.json")
    for entry in manifest["files"]:
        assert sha(HERE / entry["path"]) == entry["sha256"], entry["path"]

    initial = read("gmail-v1.json")
    checks = initial["browserChecksums"]
    assert fnv(initial["prompt"]) == checks["prompt"]
    assert fnv(initial["text"]) == checks["text"]
    table_json = json.dumps(initial["table"], ensure_ascii=False, separators=(",", ":"))
    assert fnv(table_json) == checks["table"]
    assert initial["inputMatches"]
    assert initial["prompt"] == (HERE / "prompt-gmail-v1.txt").read_text(encoding="utf-8").rstrip("\n")
    for name, prompt_file in (
        ("gmail-create-doc.json", "prompt-gmail-doc.txt"),
        ("gmail-create-sheet.json", "prompt-gmail-sheet.txt"),
        ("docs-owner-fix.json", "prompt-docs-fix.txt"),
    ):
        record = read(name)
        assert fnv(record["prompt"]) == record["promptChecksum"]
        assert fnv(record["text"]) == record["textChecksum"]
        assert record["prompt"] == (HERE / prompt_file).read_text(encoding="utf-8").rstrip("\n")
    fix = read("docs-owner-fix.json")
    assert fix["reviewedPreview"] and fix["acceptClicked"] and fix["acceptButtonAbsentAfterClick"]

    source_path = ROOT / "docs/gemini-series/advanced/content/work/examples/54/mail-samples.json"
    mails = json.loads(source_path.read_text(encoding="utf-8"))
    sources = {m["id"]: m["text"] for m in mails}
    document = read("docs-final-text.json")
    assert fnv(document["text"]) == document["checksum"]
    assert document["reopenedAfterAccept"]
    original = (HERE / "docs-v1-export.md").read_text(encoding="utf-8")
    assert "Person" in original and "Person" not in document["text"]
    assert normalize_document(original.replace("Person", "尚未指派")) == normalize_document(document["text"])
    for mail in mails:
        assert mail["sent"] in document["text"] and mail["text"] in document["text"]
    assert "負責人： 尚未指派" in document["text"]
    assert "關於海風交流會的日期" in document["text"]
    assert "關於報名表的負責人" in document["text"]

    sheet = read("sheet-data.json")
    assert fnv(sheet["text"]) == sheet["checksum"]
    grid = [line.split("\t") for line in sheet["text"].split("\r\n")]
    assert len(grid) == 7 and all(len(row) == 6 for row in grid)
    assert grid[0] == ["工作", "負責人", "期限", "狀態", "來源編號", "支持判斷的原文"]
    rows = grid[1:5]
    assert [row[1] for row in rows] == ["阿晴", "阿晴", "小安", ""]
    assert [row[2] for row in rows] == [
        "2026-09-20 / 2026-09-21", "2026-09-18 17:00 Asia/Taipei",
        "2026-09-19", "2026-09-19 前",
    ]
    assert [row[3] for row in rows] == ["日期衝突", "已確認", "已確認", "負責人待定"]
    assert "12 組" in rows[2][0] and "10 組更正為 12 組" in rows[2][5]
    quotes_checked = 0
    for row in rows:
        quotes = dict(re.findall(r"(M\d)：(.*?)(?= M\d：|$)", row[5]))
        assert set(quotes) == set(row[4].split(", "))
        for source_id, quote in quotes.items():
            assert quote and quote in sources[source_id], (source_id, quote)
            quotes_checked += 1
    assert grid[5] == [""] * 6
    assert "合成資料" in grid[6][0] and "Asia/Taipei" in grid[6][0]

    cloud = read("cloud-checks.json")
    assert cloud["sheetReloadedAfterFilterReset"] and cloud["sheetDataUnchanged"]
    assert cloud["sheetChecksum"] == sheet["checksum"]
    assert cloud["docsFinalTextChecksum"] == document["checksum"]
    assert cloud["blankB5ValueAndFormulaObserved"]
    assert (cloud["filterPendingVisible"], cloud["filterTotalRows"]) == (2, 4)
    faults = read("fault-checks.json")["checks"]
    assert len(faults) == 4 and all(case["pass"] for case in faults[:3])
    assert faults[3]["expectedLimitationObserved"]
    assert env["googleApiCalls"] == env["additionalPurchases"] == env["additionalSpendTWD"] == 0
    for path in HERE.iterdir():
        if path.suffix in {".json", ".md", ".txt", ".csv"}:
            text = path.read_text(encoding="utf-8")
            assert not re.search(r"https://docs\.google\.com/(?:document|spreadsheets)/d/", text), path.name
            assert not re.search(r"[\w.+-]+@(?:gmail|googlemail)\.com", text), path.name
            assert not re.search(r"AIza[\w-]{30,}", text), path.name
    report = {
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "status": "saved-workspace-evidence-audit-passed",
        "publishable": False,
        "historicalFilesUnchanged": len(historical),
        "sealedEvidenceFiles": len(manifest["files"]),
        "webGeminiGenerations": 4,
        "browserChecksumsMatched": 12,
        "cloudArtifactsCreated": 2,
        "actualSheetRows": len(rows),
        "sheetSourceQuotationsChecked": quotes_checked,
        "completeDocumentSources": len(mails),
        "onlyOwnerTextChangedAfterMarkupNormalization": True,
        "injectedFaultsRejected": 3,
        "semanticCheckerLimitationDemonstrated": True,
        "limitations": env["limitations"],
        "notes": [
            "Audits saved observations; does not rerun browser operations or prove independent authenticity.",
            "The Gmail side panel received synthetic pasted text, not retrieved real inbox messages.",
            "The source CSV was an independent reference; it was not uploaded as a model answer.",
        ],
    }
    (HERE / "capture-audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
