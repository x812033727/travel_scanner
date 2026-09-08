"""Exact three-slot follow-up using newly observed Agoda landing URLs.

Reuse the SHA-pinned previous operator's normal edit/review, transaction rollback,
actor, URL-health, full-catalog, receipt and replay guards without weakening them.
Only the new snapshot, tag and an even narrower identity allowlist differ.
No product edits, map overrides, property IDs, quote calls or configuration edits.
"""

import hashlib
import importlib.util
from pathlib import Path

SOURCE_SHA256 = "28f8bdfe73a9b2fbbb954d14b8fc44373cecf0c353135de34ea995a35a4cb503"
SOURCE = Path(__file__).with_name("hotel_review_remaining_20260909.py")
if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
    raise RuntimeError("Previous operator bytes changed; stop without importing it")
SPEC = importlib.util.spec_from_file_location("redirect_review_core", SOURCE)
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)

TAG = "hotel-review-redirects-20260909"
BASELINE_HASH = "14978ec20e1b05f7f5991194c9568f56bb6da93486c91105ebc5391dc4fad56d"
BASELINE_CAPTURED_AT = "2026-09-08 23:08:17.381350+00:00"
# These URLs were observed as actual IAB destinations and reloaded directly.
# Do not derive other URLs by replacing locale segments.
TARGETS = {
    "00307d02-975e-4b2f-8843-df7000cd7c50": (
        "71374dce-0786-413b-aafd-b63c7d9a3786",
        "https://www.agoda.com/zh-tw/shilla-stay-haeundae/hotel/busan-kr.html",
    ),
    "2c41cd84-0813-42cf-8a54-003bc6f0cff4": (
        "6e824f93-a049-4a32-9df4-fe17dc4d3974",
        "https://www.agoda.com/zh-tw/paradise-hotel-busan/hotel/busan-kr.html",
    ),
    "d55df51d-b401-468a-8149-bec50508b4c2": (
        "4938181e-0007-4143-aa0c-4b5ed44f4f8b",
        "https://www.agoda.com/zh-tw/toyoko-inn-busan-seomyeon_4/hotel/busan-kr.html",
    ),
}
CORE.TAG = TAG
CORE.BASELINE_HASH = BASELINE_HASH
CORE.BASELINE_CAPTURED_AT = BASELINE_CAPTURED_AT
CORE_VALIDATE = CORE.validate_manifest


def baseline_data(path):
    data = CORE.read_json(path)
    if CORE.digest(data) != BASELINE_HASH or data["captured_at"] != BASELINE_CAPTURED_AT:
        raise ValueError("Not the exact new redirected-identity baseline")
    rows = CORE.indexed(data)
    pending = {k: r for k, r in rows.items() if r["status"] == "pending"}
    if (
        len(data["products"]) != 60
        or len(data["options"]) != 360
        or sum(k[0] == "product" for k in pending) != 20
        or len(pending) != 104
        or sum(r["status"] == "approved" for r in rows.values()) != 316
    ):
        raise ValueError("Unexpected fresh baseline membership/status")
    for identifier, (parent_id, _) in TARGETS.items():
        row = pending[("option", identifier)]
        parent = pending[("product", parent_id)]
        if (
            row["product_id"] != parent_id
            or row["provider"] != "agoda"
            or row["version"] != 1
            or any(row[k] is not None for k in ("url", "evidence_url", "property_id"))
            or parent["destination_id"] != "busan"
        ):
            raise ValueError("Pinned empty Agoda slot or pending parent changed")
    return data, rows, pending


def validate_manifest(manifest, pending):
    CORE_VALIDATE(manifest, pending)
    entries = manifest["decisions"]
    if len(entries) != 3 or {e["id"] for e in entries} != set(TARGETS):
        raise ValueError("This follow-up requires exactly the three observed landing identities")
    for entry in entries:
        parent, url = TARGETS[entry["id"]]
        row = pending[("option", entry["id"])]
        if (
            entry["kind"] != "option"
            or entry["decision"] != "approve"
            or entry["method"] != "iab"
            or entry["browser_verified"] is not True
            or entry["version"] != 1
            or row["product_id"] != parent
            or row["provider"] != "agoda"
            or entry.get("option_patch") != {"url": url, "evidence_url": url}
            or entry.get("facts_patch")
            or entry.get("evidence")
        ):
            raise ValueError("Only the exact three IAB URL patches are authorized")


CORE.baseline_data = baseline_data
CORE.validate_manifest = validate_manifest

if __name__ == "__main__":
    CORE.main()
