"""Exact new-evidence batch, using unchanged normal services in the pinned release."""

import hashlib
import importlib.util
from pathlib import Path

SOURCE = Path(__file__).with_name("hotel_review_remaining_20260909.py")
SOURCE_SHA256 = "28f8bdfe73a9b2fbbb954d14b8fc44373cecf0c353135de34ea995a35a4cb503"
if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
    raise RuntimeError("Immutable core source changed")
SPEC = importlib.util.spec_from_file_location("evidence_review_core", SOURCE)
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)
TAG = "hotel-review-evidence-20260909"
BASELINE_HASH = "342aee9610db65e78626d950efef368919a7d8e4cfcf55d06a32b64e26c5adee"
BASELINE_CAPTURED_AT = "2026-09-09 00:32:08.141514+00:00"
# Compiler can structurally validate, but no core entry point accepts an unpinned draft.
MANIFEST_HASH = "c39dbbacf10c193de385a2a22930d6fcf4af6c36cea6c28e2b7a5d3bc07a3887"
WESTIN = "50f2d47d-24fe-4b07-85a2-3e1c7671e452"
PLACE_ID = "ChIJN1AzAd8IAWAR2hJ9wcsW4TE"
MAP_URL = "https://www.google.com/maps/place/?q=place_id:ChIJN1AzAd8IAWAR2hJ9wcsW4TE"
RUNTIME_SHA256 = {
    "travel_services/admin.py": "1924fa196f54d252593897adf6eab4b6a7a033ea6b58cfccd8deab8ca6bd0588",
    "travel_services/network.py": (
        "942bed1bb4787b93ad62a89ac0b161c2e99dd55964f6c4da8fff4cf1ba62b67b"
    ),
    "travel_services/service.py": (
        "bdb5e969f2e8fa07b2d43d6f31ac2b3ceecd7de30bfbaec73f6a0894ec152626"
    ),
    "travel_services/schemas.py": (
        "94e5a985688bc6a665556b28bff88e2c049536b1ceb42d22546df985bfd83448"
    ),
    "travel_services/hotel_options.py": (
        "80fb02b61ad0180cb720d83875fc8768ee673f2e26a72d1dbe5f07de8e6656c4"
    ),
    "auth/service.py": "1d8c50d2651344eea2c35089a087137bc2014dc9d7c31a1806e70552cb2d47a4",
    "models.py": "e80995463f39a82b4ba306a0e02930fb52dcb984974959a6b5740fef29272f8b",
}
APP = Path(CORE.admin.__file__).parents[1]
for relative, expected in RUNTIME_SHA256.items():
    if hashlib.sha256((APP / relative).read_bytes()).hexdigest() != expected:
        raise RuntimeError(f"Current application source differs from reviewed f752ce43: {relative}")
CORE.TAG, CORE.BASELINE_HASH, CORE.BASELINE_CAPTURED_AT = TAG, BASELINE_HASH, BASELINE_CAPTURED_AT
CORE_VALIDATE = CORE.validate_manifest


def baseline_data(path):
    data = CORE.read_json(path)
    if CORE.digest(data) != BASELINE_HASH or data["captured_at"] != BASELINE_CAPTURED_AT:
        raise ValueError("Not the exact post-deployment baseline")
    rows = CORE.indexed(data)
    pending = {key: row for key, row in rows.items() if row["status"] == "pending"}
    if (
        len(data["products"]) != 60
        or len(data["options"]) != 360
        or len(pending) != 80
        or sum(k[0] == "product" for k in pending) != 20
        or sum(r["status"] == "approved" for r in rows.values()) != 340
    ):
        raise ValueError("Unexpected hotel inventory/status")
    return data, rows, pending


def validate_payload(manifest, pending):
    CORE_VALIDATE(manifest, pending)
    entries = manifest["decisions"]
    if not 1 <= len(entries) <= 19:
        raise ValueError("Only the bounded new-evidence subset is allowed")
    for entry in entries:
        row = pending[(entry["kind"], entry["id"])]
        if (
            entry["decision"] != "approve"
            or entry["method"] != "iab"
            or not entry["browser_verified"]
        ):
            raise ValueError("Only actual new IAB approval proposals are allowed")
        if entry["kind"] == "product":
            expected = {
                **CORE.coordinate_patch(row),
                "google_place_id": PLACE_ID,
                "map_verified": True,
            }
            if (
                entry["id"] != WESTIN
                or entry.get("facts_patch") != expected
                or entry["evidence"]["map"]["url"] != MAP_URL
                or entry["evidence"]["map"]["place_id"] != PLACE_ID
            ):
                raise ValueError(
                    "Only the exact Westin independent coordinate/map patch is allowed"
                )
        else:
            # Parent UUID sets are derived only from the SHA-pinned immutable baseline.
            if row["version"] != 1 or not entry.get("option_patch"):
                raise ValueError("Only exact empty version-one option identities are allowed")
            prefix = row["provider"]
            parents = {p["id"] for (kind, _), p in pending.items() if kind == "product"}
            if prefix == "expedia" and row["product_id"] in parents:
                parent = pending[("product", row["product_id"])]
                permitted = parent["destination_id"] == "kyoto"
            else:
                # These original source keys encode the imported exact city/identity,
                # and their membership is immutable under BASELINE_HASH.
                permitted = (
                    prefix == "rakuten"
                    and row["product_id"] in OSAKA_PARENTS
                    or prefix == "agoda"
                    and row["product_id"] in TOKYO_PARENTS
                )
            if not permitted:
                raise ValueError("Option is outside the researched city/provider scope")


# The baseline is only loaded from the mandatory caller argument by core.main.
# City membership is populated from that validated file, never live mutable state.
OSAKA_PARENTS = set()
TOKYO_PARENTS = set()
BASELINE_LOADER = baseline_data


def load_baseline(path):
    data, rows, pending = BASELINE_LOADER(path)
    OSAKA_PARENTS.clear()
    TOKYO_PARENTS.clear()
    OSAKA_PARENTS.update(p["id"] for p in data["products"] if p["destination_id"] == "osaka")
    TOKYO_PARENTS.update(p["id"] for p in data["products"] if p["destination_id"] == "tokyo")
    return data, rows, pending


def validate_manifest(manifest, pending):
    if not MANIFEST_HASH or CORE.digest(manifest) != MANIFEST_HASH:
        raise ValueError("Manifest is not the exact pinned reviewed batch")
    validate_payload(manifest, pending)


CORE.baseline_data = load_baseline
CORE.validate_manifest = validate_manifest

if __name__ == "__main__":
    CORE.main()
