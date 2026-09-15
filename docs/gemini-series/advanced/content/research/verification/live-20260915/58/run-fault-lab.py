"""Reproduce quote and claim faults against the existing evidence checker, offline."""

import copy
import csv
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[2]


def write_rows(path, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    spec = importlib.util.spec_from_file_location(
        "research_checks", RESEARCH / "examples/research_checks.py"
    )
    checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)
    with (HERE / "evidence-matrix.csv").open(encoding="utf-8", newline="") as file:
        baseline = list(csv.DictReader(file))
    variants = {
        "reviewed": baseline,
        "fake-quote": copy.deepcopy(baseline),
        "bad-claim": copy.deepcopy(baseline),
    }
    fake = variants["fake-quote"][0]
    quotes = json.loads(fake["quotes"])
    quotes["E2"] = "總共有 54 人"
    fake["quotes"] = json.dumps(quotes, ensure_ascii=False)
    variants["bad-claim"][0]["claim"] = "有效名額54人"
    variants["repaired"] = copy.deepcopy(baseline)
    results = []
    for name, rows in variants.items():
        folder = HERE / "fault-lab" / name
        folder.mkdir(parents=True, exist_ok=True)
        sources = folder / "sources"
        sources.mkdir(exist_ok=True)
        for source in (RESEARCH / "examples/58/sources").glob("*.md"):
            (sources / source.name).write_bytes(source.read_bytes())
        write_rows(folder / "evidence-matrix.csv", rows)
        try:
            result = checks.evidence(folder)
            outcome = "accepted"
        except ValueError as error:
            outcome, result = "rejected", str(error)
        expected = "rejected" if name == "fake-quote" else "accepted"
        assert outcome == expected, (name, outcome, result)
        if name == "fake-quote":
            assert result == "fabricated_quote"
        results.append({"case": name, "checkerOutcome": outcome, "detail": result})
    report = {
        "cases": results,
        "humanReview": {
            "bad-claim": "Rejected: E2 replaces 24 with 30; "
            "54 is not supported even with exact quotes.",
            "repaired": "Accepted within the five-claim exercise; "
            "date proposal still needs confirmation.",
        },
        "provenance": "Controlled local mutations of the reviewed model-derived matrix, "
        "not model mistakes.",
        "modelCalls": 0,
    }
    (HERE / "fault-lab-results.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
