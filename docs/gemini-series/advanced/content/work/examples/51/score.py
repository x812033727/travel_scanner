"""Audit human ratings and raw-output evidence. This program does not grade a model."""
import argparse
import csv
import json
from pathlib import Path

CRITERIA = ("accuracy", "coverage", "format", "uncertainty")


def audit(cases, ratings, raw_root):
    root = Path(raw_root).resolve()
    expected = {(row["id"], variant) for row in cases for variant in ("A", "B")}
    seen, complete, errors = set(), [], []
    for row in ratings:
        key = (row.get("case_id"), row.get("variant"))
        if key not in expected or key in seen:
            errors.append({"row": key, "reason": "unexpected_or_duplicate"})
            continue
        seen.add(key)
        if row.get("status") == "not_run":
            continue
        try:
            if row.get("status") != "complete":
                raise ValueError("unknown_status")
            name = row.get("raw_file", "")
            file = root / name
            if not name or Path(name).is_absolute() or file.is_symlink() or not file.resolve().is_relative_to(root):
                raise ValueError("raw_output_outside_scope")
            if not file.is_file() or not file.read_text(encoding="utf-8").strip():
                raise ValueError("raw_output_missing_or_empty")
            if any(row.get(c) not in {"0", "1", "2"} for c in CRITERIA):
                raise ValueError("scores_must_be_0_to_2")
            if not row.get("evidence", "").strip():
                raise ValueError("rating_reason_required")
            complete.append({"case_id": key[0], "variant": key[1], "total": sum(int(row[c]) for c in CRITERIA)})
        except (ValueError, OSError) as error:
            errors.append({"row": key, "reason": str(error)})
    missing = sorted(expected - seen)
    ready = not errors and not missing and len(complete) == len(expected) and bool(expected)
    return {"modelTestingComplete": ready, "semanticQualityApproved": False, "completed": len(complete),
            "required": len(expected), "missingRows": missing, "errors": errors,
            "totals": {v: sum(r["total"] for r in complete if r["variant"] == v) for v in ("A", "B")} if ready else None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", type=Path)
    parser.add_argument("ratings", type=Path)
    parser.add_argument("raw_root", type=Path)
    args = parser.parse_args()
    with args.cases.open(encoding="utf-8-sig", newline="") as file:
        cases = list(csv.DictReader(file))
    with args.ratings.open(encoding="utf-8-sig", newline="") as file:
        ratings = list(csv.DictReader(file))
    result = audit(cases, ratings, args.raw_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["modelTestingComplete"] else 1)
