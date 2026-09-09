"""Carry forward unchanged pending rows without renewing old review evidence."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build():
    old = read(HERE.parent / "hotel-review-redirects-20260909/remaining-items.json")
    before = read(HERE / "before.json")
    final = read(HERE / "post-replay-snapshot.json")
    accepted = read(HERE / "verification-report.json")
    if accepted["status"] != "passed" or accepted["final_acceptance"] is not True:
        raise ValueError("Full acceptance is required before carrying forward evidence")
    rows = {
        (kind, row["id"]): row
        for kind, collection in (("product", "products"), ("option", "options"))
        for row in final[collection]
    }
    originals = {
        (kind, row["id"]): row
        for kind, collection in (("product", "products"), ("option", "options"))
        for row in before[collection]
    }
    pending = {key for key, row in rows.items() if row["status"] == "pending"}
    prior = {(item["kind"], item["id"]): item for item in old["items"]}
    if len(prior) != len(old["items"]) or not pending <= set(prior):
        raise ValueError("Missing/duplicate prior evidence; do not invent reasons")
    if any(rows[key] != originals[key] for key in pending):
        raise ValueError("Pending row changed since the pinned baseline")
    items = [{**prior[key], "evidence_age_note": (
        "Unchanged prior review carried forward with its original timestamp; "
        "not freshly re-reviewed or re-audited in the platform-source batch."
    )} for key in sorted(pending)]
    options = [rows[key] for key in pending if key[0] == "option"]
    return {
        "as_of": final["captured_at"],
        "description": (
            "Only the 21 browser-evidenced platform identities were reviewed in this batch. "
            "Remaining pending rows retain prior evidence; not a claim of full approval."
        ),
        "pending_products": sum(key[0] == "product" for key in pending),
        "pending_options": len(options),
        "pending_options_without_stored_url": sum(not r["url"] for r in options),
        "pending_options_with_stored_url": sum(bool(r["url"]) for r in options),
        "items": items,
    }


if __name__ == "__main__":
    result = build()
    with (HERE / "remaining-items.json").open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({k: v for k, v in result.items() if k != "items"}))
