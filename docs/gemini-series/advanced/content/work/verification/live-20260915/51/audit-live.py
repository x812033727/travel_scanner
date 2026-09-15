"""Check captured browser outputs against the frozen lesson inputs; does not grade answers."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[7]
EXAMPLES = ROOT / "docs/gemini-series/advanced/content/work/examples/51"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    environment = json.loads((HERE / "environment.json").read_text(encoding="utf-8"))
    for entry in environment["inputs"]:
        if sha((ROOT / entry["path"]).read_bytes()) != entry["sha256"]:
            raise ValueError("lesson input changed: " + entry["path"])
    with (EXAMPLES / "cases.csv").open(encoding="utf-8-sig", newline="") as file:
        cases = list(csv.DictReader(file))
    source = (EXAMPLES / "prompts-v1-v2.md").read_text(encoding="utf-8")
    base = source.split("## A：基準版本\n", 1)[1].split("\n[", 1)[0]
    revised = source.split("## B：只增加一項規則\n", 1)[1].split("\n[", 1)[0]
    rows = json.loads((HERE / "captured.json").read_text(encoding="utf-8"))
    expected = [(case["id"], variant) for index, case in enumerate(cases)
                for variant in (("A", "B") if index % 2 == 0 else ("B", "A"))]
    if [(row["id"], row["variant"]) for row in rows] != expected:
        raise ValueError("expected all 20 cases in the declared alternating order")
    if len({row["conversationSha256"] for row in rows}) != 20:
        raise ValueError("each answer must have its own conversation")
    raw_root = HERE / "raw"
    raw_root.mkdir(exist_ok=True)
    files = []
    for row in rows:
        case = next(item for item in cases if item["id"] == row["id"])
        prompt = (base if row["variant"] == "A" else revised) + "\n\n" + case["input"]
        if row["prompt"] != prompt or row["modelLabel"] != "Flash":
            raise ValueError("input or displayed model mismatch")
        if not row["raw"].strip():
            raise ValueError("empty response")
        if not re.fullmatch(r"[0-9a-f]{64}", row["conversationSha256"]):
            raise ValueError("invalid conversation fingerprint")
        if datetime.fromisoformat(row["finishedAt"]) < datetime.fromisoformat(row["startedAt"]):
            raise ValueError("capture timestamp precedes submission")
        name = row["id"] + "-" + row["variant"] + ".txt"
        (raw_root / name).write_text(row["raw"], encoding="utf-8", newline="\n")
        files.append({"path": "raw/" + name, "sha256": sha((raw_root / name).read_bytes())})
    report = {
        "status": "20-real-web-outputs-captured-human-ratings-pending",
        "responseCount": len(rows), "newConversations": 20, "sameDisplayedModel": "Flash",
        "alternatingOrder": True, "inputHashesMatch": True,
        "humanRatingsComplete": False, "semanticQualityApproved": False,
        "googleApiCalls": 0, "additionalPurchases": 0,
        "rawCapture": "Rendered answer body text from the connected browser; not HTTP response JSON.",
        "files": files,
    }
    (HERE / "capture-audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({key: value for key, value in report.items() if key != "files"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
