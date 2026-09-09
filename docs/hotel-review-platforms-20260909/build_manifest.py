"""Offline compilation of actual IAB observations, not automated hotel research."""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "apps/api"))
SPEC = importlib.util.spec_from_file_location(
    "platform_operator", REPO / "ops/hotel_review_platforms_20260909.py"
)
OP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OP)


def compile_manifest():
    baseline, rows, pending = OP.baseline_data(HERE / "before.json")
    prior = OP.CORE.read_json(
        HERE.parent / "hotel-review-redirects-20260909/post-replay-snapshot.json"
    )
    if {k: v for k, v in baseline.items() if k != "captured_at"} != {
        k: v for k, v in prior.items() if k != "captured_at"
    }:
        raise ValueError("Catalog drift since the last completed review")
    observations = OP.CORE.read_json(HERE / "iab-observations.json")
    if (
        observations["tag"] != OP.TAG or observations["method"] != "iab"
        or observations["baseline_captured_at"] != OP.BASELINE_CAPTURED_AT
    ):
        raise ValueError("Wrong IAB observation provenance")
    osaka = OP.CORE.read_json(HERE / "osaka-expedia-leads.json")["leads"]
    taipei = OP.CORE.read_json(HERE / "taipei-expedia-leads.json")["entries"]
    sources = {e["observed_url"]: e["option_id"] for e in osaka}
    sources.update({e["candidate_url"]: e["option_id"] for e in taipei if e["candidate_url"]})
    sources[OP.EXISTING_URL] = OP.EXISTING_ID
    # This href was read from the actual IAB review-page link, not guessed.
    westgate = "https://www.agoda.com/zh-tw/westgate-hotel/hotel/taipei-tw.html"
    sources[westgate] = "f4f26da8-cfa0-42c0-b2a3-01bf6d34bc4d"
    decisions = []
    for item in observations["entries"]:
        identifier = sources[item["requested_url"]]
        row = pending[("option", identifier)]
        parent = rows[("product", row["product_id"])]
        if (
            item["method"] != "iab" or not item["name"] or not item["address"]
            or item["provider"] != row["provider"] or row["version"] != 1
            or (
                identifier != OP.EXISTING_ID
                and parent["destination_id"] not in {"osaka", "taipei"}
            )
        ):
            raise ValueError("IAB identity/provider/source membership mismatch")
        if identifier == sources[westgate] and item.get("source_navigation") != {
            "page": "https://www.agoda.com/zh-tw/westgate-hotel/reviews/taipei-tw.html",
            "label": "立即預訂永安棧", "href": "/zh-tw/westgate-hotel/hotel/taipei-tw.html",
        }:
            raise ValueError("Missing actual WESTGATE navigation provenance")
        officials = [
            r for r in baseline["options"]
            if r["product_id"] == row["product_id"] and r["provider"] == "official"
        ]
        if len(officials) != 1 or officials[0]["status"] != "approved":
            raise ValueError("No previously approved official identity support")
        official = officials[0]
        if not official["url"] or not official["verified_at"] or not official["identity_note"]:
            raise ValueError("Official prior record is incomplete")
        note = (
            f"IAB {item['checked_at']}: {item['name']}; {item['address']}. "
            f"Matches prior official identity {official['id']} "
            f"({official['verified_at']}); official page not re-read this batch. "
            "Platform identity only; parent review separate. "
            "No quotes, prices or affiliate authority."
        )
        if item.get("url_city_note"):
            note += " Provider URL says kobe-jp; rendered full address is the matching Osaka hotel."
        urls = [item["landing_url"], item["requested_url"], official["url"]]
        if official["evidence_url"]:
            urls.append(official["evidence_url"])
        if identifier == OP.EXISTING_ID:
            urls.extend([OP.EXISTING_EVIDENCE, OP.EXISTING_URL])
        if item.get("source_navigation"):
            urls.append(item["source_navigation"]["page"])
        new_evidence = (
            f"Fresh rendered name and complete street at the observed destination "
            f"{item['landing_url']}. Source discovery text alone was not used as browser proof."
        )
        if identifier == OP.EXISTING_ID:
            new_evidence += (
                " The pinned pending en-us URL landed on this exact same-property zh-tw URL; "
                "direct reload preserved the hotel identity. Preserve the old URL in this receipt."
            )
        if item.get("url_city_note"):
            new_evidence += " " + item["url_city_note"]
        decisions.append({
            "kind": "option", "id": identifier, "version": row["version"],
            "before_hash": OP.CORE.digest(row), "decision": "approve",
            "reason": (
                f"{parent['title']} / {row['provider']}: new IAB name/full-street match to "
                "the recorded official identity. Apply only through normal versioned edit/review; "
                "retain a full rollback hold if any normal safety guard rejects the observed URL."
            ),
            "source_urls": list(dict.fromkeys(urls)), "method": "iab",
            "checked_at": item["checked_at"], "browser_verified": True,
            "new_evidence": new_evidence, "identity_note": note,
            "option_patch": {"url": item["landing_url"], "evidence_url": item["landing_url"]},
        })
    manifest = {
        "schema_version": 1, "tag": OP.TAG, "baseline_hash": OP.BASELINE_HASH,
        "decisions": decisions,
    }
    OP.validate_payload(manifest, pending)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sql-projection", action="store_true")
    args = parser.parse_args()
    result = compile_manifest()
    if args.sql_projection:
        if result != OP.CORE.read_json(HERE / "manifest.json"):
            raise ValueError("Stored manifest differs from observed evidence")
        OP.validate_manifest(result, OP.baseline_data(HERE / "before.json")[2])
        projection = [{
            **{k: e[k] for k in ("id", "kind", "version", "before_hash", "option_patch")},
            "entry_hash": OP.CORE.digest(e),
        } for e in result["decisions"]]
        OP.CORE.save_new(HERE / "sql-entries.json", projection)
    else:
        OP.CORE.save_new(HERE / "manifest.json", result)
    OP.CORE.emit({"decisions": len(result["decisions"]), "semantic_sha256": OP.CORE.digest(result)})
