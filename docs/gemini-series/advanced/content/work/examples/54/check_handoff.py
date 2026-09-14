"""Check evidence and uncertainty fields; humans still review the meaning of each claim."""
import argparse
import csv
import json
from pathlib import Path


def check(mails, items):
    sources = {m["id"]: m["text"] for m in mails}
    errors, seen = [], set()
    for row in items:
        try:
            if not row.get("id") or row["id"] in seen:
                raise ValueError("missing_or_duplicate_id")
            seen.add(row["id"])
            ids = row.get("source_ids", "").split("|")
            quotes = json.loads(row.get("source_quotes", "{}"))
            if not isinstance(quotes, dict) or set(quotes) != set(ids):
                raise ValueError("quote_keys_do_not_match_sources")
            for source in ids:
                quote = quotes[source]
                if source not in sources or not isinstance(quote, str) or not quote or quote not in sources[source]:
                    raise ValueError("missing_or_fabricated_evidence")
            status = row.get("status")
            if status not in {"confirmed", "conflict", "needs_owner"}:
                raise ValueError("unknown_status")
            if status == "confirmed" and (not row.get("owner") or not row.get("due") or "|" in row.get("due", "")):
                raise ValueError("confirmed_row_is_unresolved")
            if status == "needs_owner" and row.get("owner"):
                raise ValueError("unassigned_owner_must_stay_empty")
            if status == "conflict" and len(row.get("due", "").split("|")) < 2:
                raise ValueError("retain_both_candidate_dates")
        except (ValueError, TypeError) as error:
            errors.append({"id": row.get("id"), "reason": str(error)})
    return {"evidenceFieldsValid": bool(items) and not errors, "semanticReviewRequired": True,
            "rows": len(items), "errors": errors, "sentEmails": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mails", type=Path)
    parser.add_argument("items", type=Path)
    args = parser.parse_args()
    with args.items.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    result = check(json.loads(args.mails.read_text(encoding="utf-8")), rows)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["evidenceFieldsValid"] else 1)
