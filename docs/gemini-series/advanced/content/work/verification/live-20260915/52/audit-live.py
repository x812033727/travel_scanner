"""Validate captured Gems runs against frozen authored fixtures; no semantic grading."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[7]
EXAMPLES = ROOT / "docs/gemini-series/advanced/content/work/examples/52"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_paragraphs(text: str) -> str:
    return re.sub(r"\n+", "\n", text.strip())


def validate_setup() -> None:
    instructions = (EXAMPLES / "gem-instructions.md").read_text(encoding="utf-8")
    for version in ("v1", "v2"):
        setup = json.loads((HERE / f"{version}-setup.json").read_text(encoding="utf-8"))
        events = {event["event"]: event for event in setup["events"]}
        for name in ("before-save", "reopened"):
            observed = events[f"{version}-{name}"]
            if normalize_paragraphs(observed["instructions"]) != normalize_paragraphs(instructions):
                raise ValueError("saved instructions mismatch: " + version)
            if observed["disableCitations"] or observed["file"] != f"product-handbook-{version}.md":
                raise ValueError("saved source or citation configuration mismatch")
            if version == "v2" and observed["oldFileAbsent"] is not True:
                raise ValueError("v1 reference was not removed before v2 testing")
        if "已儲存 Gem" not in events[f"{version}-save-success"]["observed"]:
            raise ValueError("save confirmation missing")
        source = (events["v1-citation-document-opened"] if version == "v1" else
                  json.loads((HERE / "v2-source-view.json").read_text(encoding="utf-8")))
        if source["text"] != (EXAMPLES / f"product-handbook-{version}.md").read_text(encoding="utf-8"):
            raise ValueError("opened source differs from uploaded fixture")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corrected", action="store_true")
    args = parser.parse_args()
    output = HERE / "corrected" if args.corrected else HERE
    environment = json.loads((HERE / "environment.json").read_text(encoding="utf-8"))
    for entry in environment["inputs"]:
        if sha((ROOT / entry["path"]).read_bytes()) != entry["sha256"]:
            raise ValueError("frozen input changed: " + entry["path"])
    validate_setup()
    with (EXAMPLES / "regression-cases.csv").open(encoding="utf-8-sig", newline="") as file:
        cases = list(csv.DictReader(file))
    rows = json.loads((output / "captured.json").read_text(encoding="utf-8"))
    versions = ("v2",) if args.corrected else ("v1", "v2")
    expected = [(version, case["id"]) for version in versions for case in cases]
    required = len(expected)
    if [(row["version"], row["id"]) for row in rows] != expected:
        raise ValueError("expected all 12 cases per version in declared order")
    if len({row["conversationSha256"] for row in rows}) != required:
        raise ValueError("each regression answer must have a different conversation")
    if args.corrected:
        setup = json.loads((HERE / "corrected-setup.json").read_text(encoding="utf-8"))
        if sha((HERE / setup["instructionFile"]).read_bytes()) != setup["sha256"]:
            raise ValueError("corrected instructions changed")
        corrected = (HERE / setup["instructionFile"]).read_text(encoding="utf-8")
        if normalize_paragraphs(setup["instructionsObserved"]) != normalize_paragraphs(corrected):
            raise ValueError("reopened corrected instructions differ")
        if setup["handbook"] != "product-handbook-v2.md" or setup["oldHandbookAbsent"] is not True:
            raise ValueError("corrected source configuration differs")
        baseline = json.loads((HERE / "captured.json").read_text(encoding="utf-8"))
        if {r["conversationSha256"] for r in baseline} & {r["conversationSha256"] for r in rows}:
            raise ValueError("corrected run reused a baseline conversation")
    raw_root = output / "raw"
    raw_root.mkdir(exist_ok=True)
    files = []
    citation_issues = []
    for row in rows:
        if args.corrected and (row.get("instructionRevision") != "capability-boundary"
                               or row.get("inputUiVerified") is not True):
            raise ValueError("corrected run metadata incomplete")
        case = next(item for item in cases if item["id"] == row["id"])
        if row["question"] != case["question"] or row["modelLabel"] != "Flash":
            raise ValueError("question or displayed model mismatch")
        if not re.fullmatch(r"[0-9a-f]{64}", row["conversationSha256"]):
            raise ValueError("invalid conversation fingerprint")
        if datetime.fromisoformat(row["capturedAt"]) < datetime.fromisoformat(row["startedAt"]):
            raise ValueError("capture precedes submission")
        if not row["raw"].strip() or "complete" not in row["footerClass"].split():
            raise ValueError("response was empty or still generating")
        file_name = "product-handbook-" + row["version"] + ".md"
        if not row["citationLabels"] or any(file_name not in label for label in row["citationLabels"]):
            citation_issues.append({"id": row["id"], "version": row["version"],
                                    "reason": "missing or mismatched citation file"})
        name = row["version"] + "-" + row["id"] + ".txt"
        (raw_root / name).write_text(row["raw"], encoding="utf-8", newline="\n")
        files.append({"path": "raw/" + name, "sha256": sha((raw_root / name).read_bytes())})
    report = {
        "status": f"{required}-real-gem-answers-captured",
        "responseCount": len(rows), "distinctConversations": required,
        "instructionRevision": "capability-boundary" if args.corrected else "original",
        "questionStringsMatch": True, "inputHashesMatch": True,
        "savedSetupAndOpenedSourcesMatch": True,
        "displayedModel": "Flash", "citationFilesMatchConfiguredVersion": not citation_issues,
        "citationIssues": citation_issues,
        "semanticQualityApproved": False, "googleApiCalls": 0, "additionalPurchases": 0,
        "captureMethod": "Rendered model-response-content innerText, including visible citation labels.",
        "files": files,
    }
    (output / "capture-audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({key: value for key, value in report.items() if key != "files"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
