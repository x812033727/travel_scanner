"""Offline compiler for exactly three recorded IAB landing observations."""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "apps/api"))
SPEC = importlib.util.spec_from_file_location(
    "redirect_operator", REPO / "ops/hotel_review_redirects_20260909.py"
)
OP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OP)


def compile_manifest():
    baseline, rows, pending = OP.baseline_data(HERE / "before.json")
    previous = OP.CORE.read_json(
        HERE.parent / "hotel-review-remaining-20260909/final-snapshot.json"
    )
    if {k: v for k, v in previous.items() if k != "captured_at"} != {
        k: v for k, v in baseline.items() if k != "captured_at"
    }:
        raise ValueError("Baseline drift since the previous completed batch")
    evidence = OP.CORE.read_json(HERE / "iab-observations.json")
    if (
        evidence["tag"] != OP.TAG
        or evidence["method"] != "iab"
        or evidence["baseline_captured_at"] != OP.BASELINE_CAPTURED_AT
        or len(evidence["entries"]) != 3
    ):
        raise ValueError("Unexpected observation provenance/scope")
    decisions = []
    for item in evidence["entries"]:
        row = pending[("option", item["option_id"])]
        parent_id, url = OP.TARGETS[row["id"]]
        if (
            item["product_id"] != parent_id
            or item["final_url"] != url
            or item["same_final_url_after_reload"] is not True
            or not item["name"]
            or not item["address"]
        ):
            raise ValueError("Actual IAB destination/name/address evidence required")
        official = [
            r for r in baseline["options"]
            if r["product_id"] == parent_id and r["provider"] == "official"
        ]
        if len(official) != 1 or official[0]["status"] != "approved":
            raise ValueError("Missing previously approved official identity support")
        prior = official[0]
        if not prior["verified_at"] or not prior["identity_note"] or not prior["url"]:
            raise ValueError("Prior official evidence is incomplete")
        note = (
            f"IAB direct final-page reload {evidence['checked_at']}: {item['name']}; "
            f"{item['address']}. Matches prior approved official identity "
            f"{prior['id']} ({prior['verified_at']}); official page not re-read today. "
            "Independent booking identity only; parent map review remains pending. "
            "No property_id, quote, price or affiliate authority is established."
        )
        decisions.append({
            "kind": "option",
            "id": row["id"],
            "version": row["version"],
            "before_hash": OP.CORE.digest(row),
            "decision": "approve",
            "reason": (
                f"New IAB observation and direct reload of the actual landing URL for "
                f"{rows[('product', parent_id)]['title']}: exact name and street address "
                "match the prior official identity. Retain all normal URL safety checks; "
                "rollback and hold if the normal review rejects this destination."
            ),
            "source_urls": [url, item["requested_url"], prior["url"]],
            "method": "iab",
            "checked_at": evidence["checked_at"],
            "browser_verified": True,
            "new_evidence": (
                f"The prior attempted URL {item['requested_url']} visibly landed on {url}. "
                "A fresh direct reload preserved this exact destination and showed the "
                "matching name/address. This is new observed URL evidence, not a "
                "replay or reclassification of the previous guard-failure receipt."
            ),
            "identity_note": note,
            "option_patch": {"url": url, "evidence_url": url},
        })
    manifest = {
        "schema_version": 1, "tag": OP.TAG, "baseline_hash": OP.BASELINE_HASH,
        "decisions": decisions,
    }
    OP.validate_manifest(manifest, pending)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sql-projection", action="store_true")
    args = parser.parse_args()
    result = compile_manifest()
    if args.sql_projection:
        if result != OP.CORE.read_json(HERE / "manifest.json"):
            raise ValueError("Stored manifest changed")
        projection = [{
            **{k: e[k] for k in ("id", "kind", "version", "before_hash", "option_patch")},
            "entry_hash": OP.CORE.digest(e),
        } for e in result["decisions"]]
        OP.CORE.save_new(HERE / "sql-entries.json", projection)
    else:
        OP.CORE.save_new(HERE / "manifest.json", result)
    OP.CORE.emit({"decisions": len(result["decisions"]), "hash": OP.CORE.digest(result)})
