"""Compile only the root's 24 new IAB option identities and three unresolved maps.

Offline only: import schema/hash helpers without opening a database or provider.
All URLs remain byte-for-byte observations; this is not a discovery tool.
"""

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "apps/api"))
SPEC = importlib.util.spec_from_file_location(
    "remaining_hotel_operator", REPO / "ops/hotel_review_remaining_20260909.py"
)
OP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OP)


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def official_support(product, baseline, old_official, tokyo, kyoto):
    """Keep the provenance/age of official evidence separate from today's IAB read."""
    product_id = product["id"]
    if product["source_key"].startswith("editorial:tokyo:"):
        fresh = [
            item
            for item in tokyo["options"]
            if item["product_id"] == product_id
            and item["official_identity"]["freshly_read_this_task"] is True
        ]
        if fresh:
            item = fresh[0]
            proof = item["official_identity"]
            if any(other["official_identity"] != proof for other in fresh):
                raise ValueError("Conflicting Tokyo official identity evidence")
            return proof["source_url"], (
                f"Official primary-web identity read {item['checked_at']} in "
                f"tokyo-platform-leads.json: {proof['name']}; {proof['address']}. "
                "This official read was not an IAB inspection."
            )
        prior = [item for item in old_official["hotels"] if item["product_id"] == product_id]
        if len(prior) != 1 or prior[0]["full_address_verified"] is not True:
            raise ValueError("Missing previously verified Tokyo official identity")
        proof = prior[0]
        return proof["source_url"], (
            f"Prior official primary-web evidence ({old_official['review_date']}; "
            f"hotel-review-all-20260908/root-cities-official.json): "
            f"{proof['official_name']}; {proof['address']}. "
            "Not re-read as fresh official evidence in this batch."
        )
    if not product["source_key"].startswith("editorial:busan:"):
        raise ValueError("Unexpected city outside the root's IAB subset")
    official = [
        row
        for row in baseline["options"]
        if row["product_id"] == product_id and row["provider"] == "official"
    ]
    if len(official) != 1:
        raise ValueError("Expected exactly one existing official identity slot")
    row = official[0]
    if row["status"] == "approved":
        if not all(row[key] for key in ("url", "identity_note", "verified_at")):
            raise ValueError("Approved official identity lacks its evidence record")
        return row["url"], (
            f"Prior official option {row['id']} approved {row['verified_at']}, "
            f"retained in before.json: {row['identity_note']} "
            "This is prior evidence, not a fresh official-page/IAB read."
        )
    if product["source_key"] != "editorial:busan:park-hyatt-busan":
        raise ValueError("Unapproved official identity requires explicit supplementary evidence")
    alternate = [
        item for item in kyoto["hyatt_identity_alternates"] if item["product_id"] == product_id
    ]
    if len(alternate) != 1:
        raise ValueError("Missing Park Hyatt Busan supplementary official evidence")
    proof = alternate[0]
    if proof["same_hotel_name_and_full_address_readable"] is not True:
        raise ValueError("Supplementary official identity was not readable")
    return proof["alternate_official_url"], (
        f"Supplementary official primary-web read {proof['checked_at']} in "
        f"kyoto-map-leads.json: {proof['hotel_name']}; {proof['observed_address']}. "
        "Not a fresh IAB read or approval of the separate official URL slot."
    )


def compile_manifest(compiled_at):
    baseline, rows, pending = OP.baseline_data(HERE / "before.json")
    options = read(HERE / "iab-option-observations.json")
    maps = read(HERE / "iab-map-observations.json")
    tokyo = read(HERE / "tokyo-platform-leads.json")
    kyoto = read(HERE / "kyoto-map-leads.json")
    old_official = read(HERE.parent / "hotel-review-all-20260908/root-cities-official.json")
    observed = options["entries"]
    if (
        options["baseline_captured_at"] != OP.BASELINE_CAPTURED_AT
        or len(observed) != 24
        or len({item["option_id"] for item in observed}) != 24
        or Counter(item["provider"] for item in observed)
        != {"expedia": 15, "agoda": 8, "rakuten": 1}
    ):
        raise ValueError("Root IAB option scope changed; manually re-scope before compiling")
    decisions = []
    for item in observed:
        row = pending[("option", item["option_id"])]
        product = rows[("product", row["product_id"])]
        if (
            item["product_id"] != row["product_id"]
            or item["provider"] != row["provider"]
            or item["baseline_version"] != row["version"]
            or item["source_key"] != product["source_key"]
            or item["method"] != "iab"
            or item["browser_verified"] is not True
            or item["outcome"] != "identity_match_pending_normal_guard"
            or not item["name"].strip()
            or not item["address"].strip()
        ):
            raise ValueError("Root IAB observation disagrees with the exact baseline identity")
        url = item["url"]
        official_url, provenance = official_support(product, baseline, old_official, tokyo, kyoto)
        note = (
            f"New IAB read {item['checked_at']}: {item['name']}; "
            f"displayed address: {item['address']}. {provenance} "
            "Same hotel name/street identity; postal forms retained as displayed, "
            "not asserted equal."
        )
        if len(note) > 1000:
            raise ValueError("Identity note exceeds the normal route limit; do not truncate proof")
        decisions.append(
            {
                "kind": "option",
                "id": row["id"],
                "version": row["version"],
                "before_hash": OP.digest(row),
                "decision": "approve",
                "reason": (
                    f"Root inspected the exact {row['provider']} hotel page in the built-in "
                    f"browser: {item['name']}; {item['address']}. Name and street match "
                    "the separately documented official identity. Fill only this original "
                    "null URL/evidence slot through normal edit then review; keep property_id "
                    "null and do not activate quotes or approve the parent hotel. "
                    "Normal unsafe/unavailable/duplicate guards still apply."
                ),
                "new_evidence": (
                    f"Actual new root IAB observation {item['checked_at']} recorded in "
                    f"iab-option-observations.json for {row['id']}: {item['name']}; "
                    f"{item['address']}. This exact page was readable at its recorded URL. "
                    "Prior official proof is explicitly dated in identity_note; no claim of "
                    "fresh official IAB, matching postal codes, prices or booking availability."
                ),
                "source_urls": list(dict.fromkeys([url, official_url])),
                "method": "iab",
                "checked_at": item["checked_at"],
                "browser_verified": True,
                "identity_note": note,
                "option_patch": {"url": url, "evidence_url": url},
            }
        )
    if (
        len(maps["entries"]) != 3
        or {item["product_id"] for item in maps["entries"]} != set(OP.COORDINATE_ROWS)
        or maps["finder"]["place_id_found"] is not False
    ):
        raise ValueError("Root map findings changed; manually re-scope before compiling")
    if OP.evidence_timestamp(compiled_at) < OP.evidence_timestamp(maps["recorded_at"]):
        raise ValueError("Compilation cannot precede the recorded map observations")
    for item in maps["entries"]:
        row = pending[("product", item["product_id"])]
        if (
            item["method"] != "iab"
            or item["map_identity_readable"] is not True
            or item["place_id"] is not None
            or item["decision"] != "hold"
        ):
            raise ValueError("Unexpected map status; no inferred Place ID is permitted")
        decisions.append(
            {
                "kind": "product",
                "id": row["id"],
                "version": row["version"],
                "before_hash": OP.digest(row),
                "decision": "hold",
                "reason": (
                    f"This batch's actual IAB observation ({item['observation_window_utc']}) "
                    f"opened the official short map link and read {item['name']}; "
                    f"{item['address']}. Still no directly observed Google Place ID; the "
                    "official finder had no input/result. Record compiled at "
                    f"{compiled_at}, not a new browser read at that time. Prior independent "
                    "CC0 coordinate evidence cannot replace exact map identity. Leave every "
                    "product field unchanged; no facts, coordinates or inferred ID are applied."
                ),
                "new_evidence": (
                    f"New root IAB official short-link inspection this batch: "
                    f"{item['observation_window_utc']}; {item['name']}; {item['address']}. "
                    f"Evidence record compiled {compiled_at}. Map was readable but literal "
                    "Place ID remained absent, so publication remains held. No CID conversion "
                    "or Google coordinates retained."
                ),
                "source_urls": [
                    item["official_url"],
                    item["map_url"],
                    maps["finder"]["url"],
                    OP.coordinate_source(OP.COORDINATE_ROWS[row["id"]]),
                ],
                "method": "iab",
                "checked_at": compiled_at,
                "browser_verified": False,
            }
        )
    manifest = {
        "schema_version": 1,
        "tag": OP.TAG,
        "baseline_hash": OP.BASELINE_HASH,
        "decisions": sorted(decisions, key=lambda item: (item["kind"], item["id"])),
    }
    OP.validate_manifest(manifest, pending)
    if len(manifest["decisions"]) != 27:
        raise ValueError("Expected exactly 24 option approvals and three unchanged product holds")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiled-at", required=True, help="Actual UTC evidence compilation time")
    parser.add_argument("--output", type=Path, default=HERE / "manifest.json")
    args = parser.parse_args()
    compiled = OP.evidence_timestamp(args.compiled_at)
    if compiled > datetime.now(UTC):
        parser.error("Compilation timestamp may not be in the future")
    manifest = compile_manifest(args.compiled_at)
    OP.save_new(args.output, manifest)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "decisions": len(manifest["decisions"]),
                "option_approve": 24,
                "product_hold": 3,
                "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
                "semantic_sha256": OP.digest(manifest),
                "offline_schema_validation": "passed",
                "database_calls": 0,
            }
        )
    )


if __name__ == "__main__":
    main()
