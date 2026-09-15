"""Validate retained browser evidence and unchanged fixtures, without calling Google."""

import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "tools/tasks.mjs").exists())
RESEARCH = HERE.parents[1]
LIVE = HERE / "57"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fnv(text):
    data = text.encode("utf-16le")
    value = 2166136261
    for i in range(0, len(data), 2):
        value = ((value ^ int.from_bytes(data[i : i + 2], "little")) * 16777619) & 0xFFFFFFFF
    return f"{value:08x}"


def normalize_source(text):
    text = text.replace("\\#", "#").replace("&nbsp;", "")
    return "\n".join(
        re.sub(r"^#+\s*", "", line.strip())
        for line in text.splitlines()
        if line.strip() and line.strip() != "Tab 1"
    )


def main():
    history = read(RESEARCH / "verification/authoring-review.json")["files"]
    for item in history:
        assert sha(ROOT / item["path"]) == item["sha256"], item["path"]
    manifest = read(LIVE / "evidence-manifest.json")
    for item in manifest["files"]:
        path = (LIVE / item["path"]).resolve()
        assert path.is_relative_to(LIVE)
        assert sha(path) == item["sha256"], item["path"]
        assert path.stat().st_size == item["bytes"], item["path"]
    for item in manifest["inputs"]:
        assert sha(ROOT / item["path"]) == item["sha256"], item["path"]
    answers, notes = read(LIVE / "answers.json"), read(LIVE / "notes.json")
    observations = read(LIVE / "observations.json")
    sources = observations["sources"]
    assert len(answers) == 5 and len(notes) == 4 and len(sources) == 14
    assert len(observations["citations"]) == 7
    by_answer = {(a["mode"], a["version"]): a for a in answers}
    for item in answers + notes + sources:
        assert fnv(item["text"]) == item["checksum"], item
    for answer in answers:
        assert fnv(answer["prompt"]) == answer["promptChecksum"]
        assert datetime.fromisoformat(answer["startedAt"]) <= datetime.fromisoformat(
            answer["capturedAt"]
        )
    assert len({a["prompt"] for a in answers if a["version"] != "both"}) == 1
    for note in notes:
        version = "v1" if note["version"] == "v1-after-v2" else "v2"
        answer = by_answer[note["mode"], version]
        assert note["text"] == answer["text"].removeprefix("Thoughts\nexpand_more\n")
    for source in sources:
        filename = source["source"]
        if filename.startswith("S01 Google Doc"):
            filename = "S01-" + filename.rsplit(" ", 1)[1] + ".md"
        fixture = RESEARCH / "examples/57/sources" / filename
        assert normalize_source(source["text"]) == normalize_source(fixture.read_text("utf-8"))
    for version in ("v1", "v2"):
        export = (LIVE / f"doc-{version}-export.md").read_text("utf-8")
        fixture = (RESEARCH / f"examples/57/sources/S01-{version}.md").read_text("utf-8")
        assert normalize_source(export) == normalize_source(fixture)
    for citation in observations["citations"]:
        evidence = citation.get("visibleEvidence", citation.get("sourcePanelEvidence"))
        assert evidence and any(evidence)
        assert all(text is None or any(s["text"] == text for s in sources) for text in evidence)
    old_citation = observations["citations"][-1]
    assert "參與名額為 24 人。" in old_citation["citationPopupAx"]
    assert "修訂為 30 人" in old_citation["sourcePanelEvidence"][0]
    reopened = read(LIVE / "reopen-check.json")
    for mode in ("upload", "drive"):
        assert reopened[mode]["checksums"] == [a["checksum"] for a in answers if a["mode"] == mode]
    assert "S01-v1.md」, Value: 0" in reopened["upload"]["finalSelection"]
    assert "S01-v1.md」, Value: 1" in reopened["upload"]["selectionAfterReload"]
    assert "S01-v2.md」, Value: 1" in reopened["upload"]["finalSelection"]
    environment = read(LIVE / "environment.json")
    assert environment["apiCalls"] == environment["extraSpendTwd"] == 0
    for path in LIVE.iterdir():
        if path.suffix in {".json", ".md"}:
            assert not re.search(
                r"AIza[0-9A-Za-z_-]{20,}|notebook\.google\.com/notebook/|docs\.google\.com/document/d/",
                path.read_text("utf-8"),
            ), path.name
    report = {
        "checkedAt": datetime.now(UTC).isoformat(),
        "status": "retained-evidence-integrity-pass",
        "historicalFilesUnchanged": len(history),
        "frozenEvidenceFiles": len(manifest["files"]),
        "responses": 5,
        "savedNotes": 4,
        "sourceViews": 14,
        "citationClicks": 7,
        "googleCallsByAudit": 0,
        "semanticReview": "See README.md; auto source guide has unsupported wording.",
        "publication": "not-published",
    }
    (LIVE / "capture-audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
