"""Derive review files from captured answer text; never replace the raw capture."""

import csv
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def write_json(name, value):
    (HERE / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


def without_citation_labels(text):
    return "\n".join(line for line in text.splitlines() if not re.fullmatch(r"[1-3]", line))


def main():
    captured = json.loads((HERE / "corrected.json").read_text("utf-8"))
    table, remaining = captured["text"].split("未知項目查核與補件需求 (U1 & U2)\n", 1)
    raw_rows = table.rstrip().split("\n\n\n")[1:]
    assert len(raw_rows) == 5
    rows = []
    for number, raw in enumerate(raw_rows, 1):
        fields = raw.split("\n\t\n")
        assert len(fields) == 7, fields
        claim_id, claim, status, source_ids, chapters, quote_cell, judgment = fields
        assert claim_id == f"C{number}"
        ids = source_ids.split(", ")
        quotes = re.findall("「([^」]+)」", quote_cell)
        assert len(ids) == len(quotes)
        chapter_map = dict(re.findall(r"(E[1-3]) #### ([A-Z]+)", chapters))
        assert set(chapter_map) == set(ids)
        rows.append(
            {
                "id": claim_id,
                "claim": without_citation_labels(claim),
                "status": status,
                "source_ids": "|".join(ids),
                "chapters": json.dumps(chapter_map, ensure_ascii=False),
                "quotes": json.dumps(dict(zip(ids, quotes, strict=True)), ensure_ascii=False),
                "judgment": without_citation_labels(judgment),
            }
        )
    with (HERE / "evidence-matrix.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    unknown = []
    for number, label in ((1, "餐點"), (2, "停車")):
        section = remaining.split(f"U{number} {label}\n", 1)[1].split("\n", 5)[:5]
        assert section[:3] == [
            "狀態：unknown",
            "支持原文：（無）",
            "查閱範圍：已查閱來源 E1、E2、E3",
        ]
        unknown.append(
            {
                "id": f"U{number}",
                "question": label,
                "status": "unknown",
                "checkedSources": ["E1", "E2", "E3"],
                "supportQuotes": {},
                "neededInformation": section[3].removeprefix("需要補件的資訊："),
            }
        )
    write_json("unknown-register.json", unknown)
    write_json(
        "normalization.json",
        {
            "provenance": "Codex derivation from captured model text, not a NotebookLM CSV export.",
            "input": "corrected.json",
            "inputSha256": hashlib.sha256((HERE / "corrected.json").read_bytes()).hexdigest(),
            "answerChecksum": captured["checksum"],
            "outputs": ["evidence-matrix.csv", "unknown-register.json"],
            "changes": [
                "Removed native citation-number display labels from claim and judgment cells.",
                "Mapped comma-separated source IDs to the local checker's pipe-separated format.",
                "Extracted verbatim quotes into per-source JSON; "
                "all quotes checked against sources.",
                "Extracted chapter names, removing erroneous #### levels "
                "and literal <br> separators.",
                "Represented U1/U2 no supporting quote as an empty object; "
                "kept checked sources separate.",
            ],
            "claimOrJudgmentRewritten": False,
            "rawCaptureUnchanged": True,
        },
    )
    print("Derived five claims and two unknown records from the preserved corrected answer.")


if __name__ == "__main__":
    main()
