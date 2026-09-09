"""Carry forward unchanged pending rows without renewing old review evidence."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build():
    old = read(HERE.parent / "hotel-review-platforms-20260909/remaining-items.json")
    before = read(HERE / "before.json")
    final = read(HERE / "post-replay-snapshot.json")
    accepted = read(HERE / "concurrent-change-assessment.json")
    if (
        accepted["status"] != "qualified"
        or accepted["final_acceptance"] is not False
        or accepted["hotel_checks_passed"] is not True
        or accepted["strict_verification"]["status"] != "failed"
    ):
        raise ValueError("Expected qualified hotel-only assessment, not full acceptance")
    for filename, expected in accepted["input_file_sha256"].items():
        if hashlib.sha256((HERE / filename).read_bytes()).hexdigest() != expected:
            raise ValueError("Assessment input changed; do not carry forward stale evidence")
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
    items = [
        {
            **prior[key],
            "evidence_age_note": (
                "Unchanged prior review carried forward with its original timestamp; "
                "not freshly re-reviewed or re-audited in the mixed-evidence batch."
            ),
        }
        for key in sorted(pending)
    ]
    manifest = read(HERE / "manifest.json")
    entries = {(e["kind"], e["id"]): e for e in manifest["decisions"]}
    results = [json.loads(line) for line in (HERE / "apply.ndjson").read_text().splitlines()]
    holds = {tuple(r["target"].rsplit(":", 2)[1:]): r for r in results if r["outcome"] == "hold"}
    for item in items:
        key = (item["kind"], item["id"])
        if key in holds:
            entry, receipt = entries[key], holds[key]
            item["prior_assessment"] = {
                k: item[k]
                for k in ("last_review_batch", "last_evidence_checked_at", "reason", "source_urls")
            }
            item.update(
                last_review_batch=manifest["tag"],
                last_evidence_checked_at=entry["checked_at"],
                reason=f"Normal safety guard {receipt['guard_code']} retained the unchanged row. "
                + entry["reason"],
                source_urls=entry["source_urls"],
                evidence_age_note=(
                    "New browser evidence was reviewed; normal guard hold, not approval."
                ),
            )
    options = [rows[key] for key in pending if key[0] == "option"]
    return {
        "as_of": final["captured_at"],
        "verification_status": "qualified",
        "full_acceptance": False,
        "verification_note": (
            "Hotel rows/public/replay checks passed; strict all-settings-unchanged check failed "
            "on a concurrent layout settings update. Preserve that failure and the changed setting."
        ),
        "description": (
            "Only the 19 browser-evidenced hotel/product identities were proposed in this batch. "
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
