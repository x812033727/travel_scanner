"""Pinned platform-only hotel evidence batch; never changes parent hotel facts.

The unchanged SHA-pinned core retains ordinary admin edit/review, actor freshness,
URL health, full-row locks, rollback, durable receipts and replay. One specifically
pinned pending Agoda slot can correct its observed same-hotel landing URL. All
other edits require empty pending identities. The final manifest is hash-bound.
"""

import hashlib
import importlib.util
from pathlib import Path

SOURCE = Path(__file__).with_name("hotel_review_remaining_20260909.py")
SOURCE_SHA256 = "28f8bdfe73a9b2fbbb954d14b8fc44373cecf0c353135de34ea995a35a4cb503"
if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
    raise RuntimeError("Immutable core source changed")
SPEC = importlib.util.spec_from_file_location("platform_review_core", SOURCE)
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)
TAG = "hotel-review-platforms-20260909"
BASELINE_HASH = "7b86b02a40dfe00946f1df45d8e201e3dc59bf49066469c30dbfcc60f5628e49"
BASELINE_CAPTURED_AT = "2026-09-08 23:37:42.330750+00:00"
# Filled only after the offline compiler has validated actual IAB observations.
# An unpinned draft cannot be used by any core review/dry-run/verify entry point.
MANIFEST_HASH = "0ac83abdcf4d61caecc235e785d4734346a2bfa596afa4f5be883c79753537fa"
EXISTING_ID = "ff023c57-7f7c-460f-9523-a55805fa42e0"
EXISTING_PARENT = "0a47515c-1b5a-4750-9790-1b7969048e30"
EXISTING_URL = (
    "https://www.agoda.com/en-us/daiwa-roynet-hotel-kyoto-terrace-hachijohigashiguchi/"
    "hotel/kyoto-jp.html"
)
CORRECTED_URL = (
    "https://www.agoda.com/zh-tw/daiwa-roynet-hotel-kyoto-terrace-hachijohigashiguchi/"
    "hotel/kyoto-jp.html"
)
EXISTING_EVIDENCE = "https://www.daiwaroynet.jp/en/kyoto-terrace/"
CORE.TAG = TAG
CORE.BASELINE_HASH = BASELINE_HASH
CORE.BASELINE_CAPTURED_AT = BASELINE_CAPTURED_AT
CORE_VALIDATE = CORE.validate_manifest
CORE_EMPTY_EDIT = CORE.option_edit_payload


def baseline_data(path):
    data = CORE.read_json(path)
    if CORE.digest(data) != BASELINE_HASH or data["captured_at"] != BASELINE_CAPTURED_AT:
        raise ValueError("Unexpected platform batch baseline")
    rows = CORE.indexed(data)
    pending = {key: row for key, row in rows.items() if row["status"] == "pending"}
    if (
        len(data["products"]) != 60 or len(data["options"]) != 360
        or len(pending) != 101
        or sum(k[0] == "product" for k in pending) != 20
        or sum(r["status"] == "approved" for r in rows.values()) != 319
    ):
        raise ValueError("Unexpected fixed hotel inventory/status")
    return data, rows, pending


def option_edit_payload(row, entry):
    if str(row["id"]) != EXISTING_ID:
        return CORE_EMPTY_EDIT(row, entry)
    if (
        entry["kind"] != "option" or entry["id"] != EXISTING_ID
        or entry["decision"] != "approve" or entry["method"] != "iab"
        or entry["browser_verified"] is not True
        or row["product_id"] != EXISTING_PARENT or row["provider"] != "agoda"
        or row["status"] != "pending" or row["version"] != 1
        or row["property_id"] is not None or row["discovery_status"] != "found"
        or row["url"] != EXISTING_URL or row["evidence_url"] != EXISTING_EVIDENCE
        or entry.get("option_patch") != {
            "url": CORRECTED_URL, "evidence_url": CORRECTED_URL,
        }
        or not {EXISTING_URL, EXISTING_EVIDENCE, CORRECTED_URL} <= set(entry["source_urls"])
    ):
        raise ValueError("Existing identity correction differs from exact pinned old/new URLs")
    payload = CORE.HotelOptionEdit(
        version=1, provider="agoda", url=CORRECTED_URL, property_id=None,
        evidence_url=CORRECTED_URL, identity_note=entry["identity_note"],
        discovery_status="found",
    )
    if payload.url != CORRECTED_URL or payload.evidence_url != CORRECTED_URL:
        raise ValueError("Normal schema changed the exact corrected URL")
    return payload


def validate_payload(manifest, pending):
    """Offline structural validation only; core write paths use the pinned wrapper."""
    CORE_VALIDATE(manifest, pending)
    entries = manifest["decisions"]
    if not 1 <= len(entries) <= 21:
        raise ValueError("A bounded explicit subset is required")
    for entry in entries:
        if (
            entry["kind"] != "option" or entry["decision"] != "approve"
            or entry["method"] != "iab" or entry["browser_verified"] is not True
            or entry.get("facts_patch") or entry.get("evidence")
            or not entry.get("option_patch")
            or pending[("option", entry["id"])]["provider"] not in {"agoda", "expedia"}
        ):
            raise ValueError("Only newly IAB-verified platform URL edits are authorized")


def validate_manifest(manifest, pending):
    if CORE.digest(manifest) != MANIFEST_HASH:
        raise ValueError("Manifest is not the exact pinned reviewed batch")
    validate_payload(manifest, pending)


CORE.baseline_data = baseline_data
CORE.option_edit_payload = option_edit_payload
CORE.validate_manifest = validate_manifest

if __name__ == "__main__":
    CORE.main()
