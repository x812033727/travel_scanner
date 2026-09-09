"""Compile only the recorded IAB identities and fresh, pinned independent coordinates."""

import argparse
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "evidence_operator", HERE.parents[1] / "ops/hotel_review_evidence_20260909.py"
)
OP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OP)


def compile_manifest():
    baseline, rows, pending = OP.load_baseline(HERE / "before.json")
    prior = OP.CORE.read_json(
        HERE.parent / "hotel-review-platforms-20260909/post-replay-snapshot.json"
    )
    if {k: v for k, v in baseline.items() if k != "captured_at"} != {
        k: v for k, v in prior.items() if k != "captured_at"
    }:
        raise ValueError("Catalog drift since previous completed batch")
    observations = OP.CORE.read_json(HERE / "iab-observations.json")
    if (
        observations["tag"] != OP.TAG
        or observations["method"] != "iab"
        or observations["baseline_captured_at"] != OP.BASELINE_CAPTURED_AT
    ):
        raise ValueError("Wrong actual browser observation provenance")
    sources = {}
    for filename, sha, key, identifier in (
        (
            "global-rakuten-leads.json",
            "6bd7b7cf30afd60ae59ef09f75797221f42c4551a72cd27a80e2d16de5d77551",
            "entries",
            "id",
        ),
        (
            "osaka-rakuten-leads.json",
            "19e7c13145379d91f65df8c840829033a4ad07d6fd51f2d5b68e6e2a3df6a2d0",
            "items",
            "option_id",
        ),
        (
            "kyoto-expedia-leads.json",
            "21c4c59cb0cb89cd7a5121372d45b162904aa2634f47df6fb3987da0cafc38ef",
            "entries",
            "id",
        ),
    ):
        if hashlib.sha256((HERE / filename).read_bytes()).hexdigest() != sha:
            raise ValueError("Source-discovery artifact changed")
        for lead in OP.CORE.read_json(HERE / filename)[key]:
            sources[lead["candidate_url"]] = lead[identifier]
    decisions = []
    for item in observations["entries"]:
        row = pending[("option", sources[item["requested_url"]])]
        parent = rows[("product", row["product_id"])]
        if (
            item["method"] != "iab"
            or not item["name"]
            or not item["address"]
            or item["provider"] != row["provider"]
            or row["version"] != 1
        ):
            raise ValueError("Wrong observed platform identity")
        officials = [
            o
            for o in baseline["options"]
            if o["product_id"] == parent["id"] and o["provider"] == "official"
        ]
        if len(officials) != 1 or officials[0]["status"] != "approved":
            raise ValueError("Missing previously approved official identity")
        official = officials[0]
        if not all(official[k] for k in ("url", "verified_at", "identity_note")):
            raise ValueError("Incomplete official identity provenance")
        urls = [item["landing_url"], item["requested_url"], official["url"]]
        if official["evidence_url"]:
            urls.append(official["evidence_url"])
        decisions.append(
            {
                "kind": "option",
                "id": row["id"],
                "version": row["version"],
                "before_hash": OP.CORE.digest(row),
                "decision": "approve",
                "reason": (
                    f"{parent['title']} / {row['provider']}: actual IAB hotel name and "
                    "complete street address agree with the recorded official identity. "
                    "Normal versioned edit/review only; fully roll back if a safety guard fails."
                ),
                "source_urls": list(dict.fromkeys(urls)),
                "method": "iab",
                "checked_at": item["checked_at"],
                "browser_verified": True,
                "new_evidence": (
                    "Fresh rendered property name and full address at actual URL "
                    f"{item['landing_url']}; discovery/index results are not browser proof."
                ),
                "identity_note": (
                    f"IAB {item['checked_at']}: {item['name']}; {item['address']}. "
                    f"Matches prior official identity {official['id']} "
                    f"({official['verified_at']}); "
                    "official page not re-read in this IAB batch. Platform identity only; "
                    "parent review separate. No quotes, prices or affiliate authority."
                ),
                "option_patch": {"url": item["landing_url"], "evidence_url": item["landing_url"]},
            }
        )
    if len(decisions) != 18 or len(observations["products"]) != 1:
        raise ValueError("Unexpected recorded evidence count")
    item = observations["products"][0]
    row = pending[("product", OP.WESTIN)]
    coords = OP.CORE.read_json(HERE / "westin-coordinate-evidence.json")
    pinned = coords["pinned"]
    allowed = OP.CORE.COORDINATE_ROWS[OP.WESTIN]
    claim = pinned["selected_claim"]
    point = claim["mainsnak"]["datavalue"]["value"]
    if (
        item["id"] != OP.WESTIN
        or item["map_url"] != OP.MAP_URL
        or item["place_id"] != OP.PLACE_ID
        or item["identity_verified"] is not True
        or pinned["http_status"] != 200
        or coords["current"]["http_status"] != 200
        or pinned["selected_claim"] != coords["current"]["selected_claim"]
        or pinned["qid"] != allowed["qid"]
        or pinned["lastrevid"] != allowed["revision"]
        or claim["id"] != allowed["claim_id"]
        or point["latitude"] != allowed["latitude"]
        or point["longitude"] != allowed["longitude"]
    ):
        raise ValueError("Independent coordinate or actual map evidence mismatch")
    ce = OP.CORE.coordinate_evidence(row, pinned["checked_at"])
    decisions.insert(
        0,
        {
            "kind": "product",
            "id": row["id"],
            "version": row["version"],
            "before_hash": OP.CORE.digest(row),
            "decision": "approve",
            "reason": (
                "Westin Miyako Kyoto: actual IAB Google Place ID resolves to matching name, "
                "street and official Marriott website. Fresh independent CC0 Wikidata P625 "
                "Japanese-Wikipedia claim supplies a representative hotel point. "
                "Normal area, source and map gates remain mandatory."
            ),
            "source_urls": [
                OP.MAP_URL,
                ce["url"],
                row["source_url"],
                coords["licensing_policy_url"],
                ce["license_url"],
            ],
            "method": "iab",
            "checked_at": pinned["checked_at"],
            "browser_verified": True,
            "new_evidence": (
                f"IAB {item['checked_at']}: {item['name']}; {item['address']}; "
                "official marriott.com link. Refreshed current and pinned Wikidata JSON "
                "agree on the selected independent CC0 claim. No Google/OTA coordinates; "
                "not a surveyed entrance or positional accuracy guarantee."
            ),
            "facts_patch": {
                **OP.CORE.coordinate_patch(row),
                "google_place_id": OP.PLACE_ID,
                "map_verified": True,
            },
            "evidence": {
                "map": {
                    "url": OP.MAP_URL,
                    "identity_verified": True,
                    "method": "iab",
                    "checked_at": item["checked_at"],
                    "place_id": OP.PLACE_ID,
                },
                "coordinates": ce,
            },
        },
    )
    manifest = {
        "schema_version": 1,
        "tag": OP.TAG,
        "baseline_hash": OP.BASELINE_HASH,
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
            raise ValueError("Stored manifest is not the observed evidence")
        OP.validate_manifest(result, OP.load_baseline(HERE / "before.json")[2])
        projection = [
            {
                **{k: e[k] for k in ("kind", "id", "version", "before_hash")},
                **{k: e[k] for k in ("option_patch", "facts_patch") if k in e},
                "entry_hash": OP.CORE.digest(e),
            }
            for e in result["decisions"]
        ]
        OP.CORE.save_new(HERE / "sql-entries.json", projection)
    else:
        OP.CORE.save_new(HERE / "manifest.json", result)
    OP.CORE.emit({"decisions": len(result["decisions"]), "semantic_sha256": OP.CORE.digest(result)})
