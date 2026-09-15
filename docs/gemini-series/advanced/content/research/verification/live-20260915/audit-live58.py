"""Verify retained lesson 58 evidence; local checks cannot reproduce cloud state."""

import csv
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "tools/tasks.mjs").exists())
RESEARCH = HERE.parents[1]
LIVE = HERE / "58"


def read(path):
    return json.loads(path.read_text("utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fnv(text):
    data = text.encode("utf-16le")
    value = 2166136261
    for i in range(0, len(data), 2):
        value = ((value ^ int.from_bytes(data[i : i + 2], "little")) * 16777619) & 0xFFFFFFFF
    return f"{value:08x}"


def source_text(text):
    return "\n".join(re.sub(r"^#+\s*", "", s.strip()) for s in text.splitlines() if s.strip())


def main():
    history = read(RESEARCH / "verification/authoring-review.json")["files"]
    for item in history:
        assert sha(ROOT / item["path"]) == item["sha256"], item["path"]
    # Prior lesson revision must remain independently reviewable.
    revision57 = RESEARCH / "revisions/20260915"
    for item in read(revision57 / "review.json")["files"]:
        assert sha(revision57 / item["path"]) == item["sha256"], item["path"]
    manifest = read(LIVE / "evidence-manifest.json")
    for item in manifest["files"]:
        path = (LIVE / item["path"]).resolve()
        assert path.is_relative_to(LIVE)
        assert sha(path) == item["sha256"] and path.stat().st_size == item["bytes"], item["path"]
    for item in manifest["inputs"]:
        assert sha(ROOT / item["path"]) == item["sha256"], item["path"]
    answers = [read(LIVE / f"{name}.json") for name in ("initial", "unknown", "corrected")]
    notes, sources = read(LIVE / "notes.json"), read(LIVE / "sources.json")
    citations = read(LIVE / "citations.json")
    assert len(notes) == len(sources) == 3 and len(citations) == 17
    for item in answers + notes + sources:
        assert fnv(item["text"]) == item["checksum"]
    for answer, note in zip(answers, notes, strict=True):
        assert answer["id"] == note["id"]
        assert fnv(answer["prompt"]) == answer["promptChecksum"]
        assert datetime.fromisoformat(answer["startedAt"]) <= datetime.fromisoformat(
            answer["capturedAt"]
        )
        assert note["text"] == answer["text"].removeprefix("Thoughts\nexpand_more\n")
    prompt = (RESEARCH / "examples/58/prompt.txt").read_text("utf-8").rstrip("\n")
    assert answers[0]["prompt"] == prompt
    by_source = {s["source"]: s for s in sources}
    fixtures = {}
    for sid, source in by_source.items():
        fixtures[sid] = (RESEARCH / f"examples/58/sources/{sid}.md").read_text("utf-8")
        assert source_text(source["text"]) == source_text(fixtures[sid])
    reopened = read(LIVE / "reopen-check.json")
    for citation in citations + [reopened["savedNoteCitation"]]:
        sid = citation["source"].removesuffix(".md")
        assert citation["texts"] and len(citation["texts"]) == len(citation["checksums"])
        for text, checksum in zip(citation["texts"], citation["checksums"], strict=True):
            assert text == by_source[sid]["text"] and fnv(text) == checksum
    with (LIVE / "evidence-matrix.csv").open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    assert [r["id"] for r in rows] == [f"C{i}" for i in range(1, 6)]
    assert [r["status"] for r in rows] == [
        "supported",
        "conflict",
        "unknown",
        "supported",
        "unknown",
    ]
    raw_rows = answers[2]["text"].split("未知項目查核與補件需求", 1)[0].rstrip().split("\n\n\n")[1:]
    for row, raw in zip(rows, raw_rows, strict=True):
        fields = raw.split("\n\t\n")
        for key, index in (("claim", 1), ("judgment", 6)):
            expected = "\n".join(s for s in fields[index].splitlines() if s not in {"1", "2", "3"})
            assert row[key] == expected
        for sid, quote in json.loads(row["quotes"]).items():
            chapter = json.loads(row["chapters"])[sid]
            assert f"## {chapter}\n" in fixtures[sid]
            section = fixtures[sid].split(f"## {chapter}\n", 1)[1].split("\n## ", 1)[0]
            assert quote in section
    for unknown in read(LIVE / "unknown-register.json"):
        assert unknown["status"] == "unknown" and unknown["supportQuotes"] == {}
        assert unknown["checkedSources"] == ["E1", "E2", "E3"]
        assert unknown["neededInformation"] in answers[2]["text"]
    normalization = read(LIVE / "normalization.json")
    assert normalization["inputSha256"] == sha(LIVE / "corrected.json")
    assert reopened["responseChecksums"] == [a["checksum"] for a in answers]
    assert reopened["correctedNoteChecksum"] == notes[2]["checksum"]
    assert reopened["correctedNoteMatchesAnswer"]
    for sid in by_source:
        assert any(f"{sid}.md」, Value: 1" in line for line in reopened["sourceAndNoteState"])
    fault = read(LIVE / "fault-lab-results.json")
    assert [(c["case"], c["checkerOutcome"]) for c in fault["cases"]] == [
        ("reviewed", "accepted"),
        ("fake-quote", "rejected"),
        ("bad-claim", "accepted"),
        ("repaired", "accepted"),
    ]
    assert fault["cases"][1]["detail"] == "fabricated_quote"
    environment = read(LIVE / "environment.json")
    assert environment["apiCalls"] == environment["extraSpendTwd"] == fault["modelCalls"] == 0
    assert environment["manualPrompts"] == 3
    for path in LIVE.rglob("*"):
        if path.suffix in {".json", ".md", ".csv"}:
            assert not re.search(
                r"AIza[0-9A-Za-z_-]{20,}|notebook\.google\.com/notebook/|docs\.google\.com/document/d/",
                path.read_text("utf-8"),
            ), path.name
    report = {
        "checkedAt": datetime.now(UTC).isoformat(),
        "status": "retained-evidence-integrity-pass",
        "historicalFilesUnchanged": len(history),
        "priorLesson57RevisionUnchanged": True,
        "frozenEvidenceFiles": len(manifest["files"]),
        "responses": 3,
        "savedNotes": 3,
        "sourceViews": 3,
        "retainedAnswerCitationObservations": 17,
        "reopenedNoteCitationObservations": 1,
        "reviewedClaims": 5,
        "unknownItems": 2,
        "offlineFaultCases": 4,
        "googleCallsByAudit": 0,
        "semanticReview": "Initial wording repaired; core corrected claims reviewed; "
        "format defects retained.",
        "publication": "not-published",
    }
    (LIVE / "capture-audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
