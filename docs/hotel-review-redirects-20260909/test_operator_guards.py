"""Offline restrictions added by the new three-slot wrapper."""

import copy
import importlib.util
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "redirect_guard_test", HERE.parents[1] / "ops/hotel_review_redirects_20260909.py"
)
OP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OP)
BASE, ROWS, PENDING = OP.baseline_data(HERE / "before.json")
MANIFEST = OP.CORE.read_json(HERE / "manifest.json")


def test_exact_new_scope_accepted():
    OP.validate_manifest(MANIFEST, PENDING)
    assert len(PENDING) == 104
    assert len(ROWS) == 420
    assert len([r for r in ROWS.values() if r["status"] == "approved"]) == 316


@pytest.mark.parametrize("mutation", [
    "missing", "extra", "duplicate", "wrong_tag", "old_baseline", "old_timestamp",
    "wrong_version", "wrong_hash", "hold", "non_iab", "unverified", "old_url",
    "property_id", "coordinates", "unknown_option", "product", "empty_note",
])
def test_rejects_scope_and_evidence_changes(mutation):
    manifest = copy.deepcopy(MANIFEST)
    entry = manifest["decisions"][0]
    if mutation == "missing":
        manifest["decisions"].pop()
    elif mutation == "extra":
        manifest["decisions"].append(copy.deepcopy(entry))
    elif mutation == "duplicate":
        manifest["decisions"][1] = copy.deepcopy(entry)
    elif mutation == "wrong_tag":
        manifest["tag"] = "hotel-review-remaining-20260909"
    elif mutation == "old_baseline":
        manifest["baseline_hash"] = "0" * 64
    elif mutation == "old_timestamp":
        entry["checked_at"] = OP.BASELINE_CAPTURED_AT
    elif mutation == "wrong_version":
        entry["version"] = 2
    elif mutation == "wrong_hash":
        entry["before_hash"] = "0" * 64
    elif mutation == "hold":
        entry["decision"] = "hold"
        entry.pop("option_patch")
        entry.pop("identity_note")
    elif mutation == "non_iab":
        entry["method"] = "primary_web"
    elif mutation == "unverified":
        entry["browser_verified"] = False
    elif mutation == "old_url":
        entry["option_patch"] = {k: entry["source_urls"][1] for k in entry["option_patch"]}
    elif mutation == "property_id":
        entry["option_patch"]["property_id"] = "unauthorized"
    elif mutation == "coordinates":
        entry["facts_patch"] = {"latitude": 35.0}
    elif mutation == "unknown_option":
        entry["id"] = "00000000-0000-0000-0000-000000000001"
    elif mutation == "product":
        entry["kind"] = "product"
    elif mutation == "empty_note":
        entry["identity_note"] = ""
    with pytest.raises((ValueError, KeyError)):
        OP.validate_manifest(manifest, PENDING)


@pytest.mark.parametrize("field", ["captured_at", "configs", "products", "options"])
def test_baseline_semantic_changes_rejected(field, monkeypatch):
    changed = copy.deepcopy(BASE)
    changed[field] = None
    monkeypatch.setattr(OP.CORE, "read_json", lambda _: changed)
    with pytest.raises(ValueError):
        OP.baseline_data("unused")


def test_snapshot_protects_other_rows_and_configuration():
    changed = copy.deepcopy(BASE)
    changed["products"][0]["version"] += 1
    with pytest.raises(RuntimeError, match="Full-row"):
        OP.CORE.verify_state(changed, BASE, ROWS, MANIFEST, {})
    changed = copy.deepcopy(BASE)
    changed["configs"][0]["version"] += 1
    with pytest.raises(RuntimeError, match="Configuration"):
        OP.CORE.verify_state(changed, BASE, ROWS, MANIFEST, {})
