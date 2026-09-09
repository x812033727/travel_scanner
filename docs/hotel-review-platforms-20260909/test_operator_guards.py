"""Offline guards for the exact platform batch; no database or network access."""

import copy
import importlib.util
import socket
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "platform_operator_guard_tests", HERE.parents[1] / "ops/hotel_review_platforms_20260909.py"
)
OP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OP)
BASE, ROWS, PENDING = OP.baseline_data(HERE / "before.json")
MANIFEST = OP.CORE.read_json(HERE / "manifest.json")
EXISTING_ENTRY = next(e for e in MANIFEST["decisions"] if e["id"] == OP.EXISTING_ID)
EMPTY_ENTRY = next(e for e in MANIFEST["decisions"] if e["id"] != OP.EXISTING_ID)
EXISTING_ROW = ROWS[("option", OP.EXISTING_ID)]


@pytest.fixture(autouse=True)
def deny_external_access(monkeypatch):
    def denied(*args, **kwargs):
        raise AssertionError("Offline guard tests must not access database or network")

    monkeypatch.setattr(OP.CORE, "SessionFactory", denied)
    monkeypatch.setattr(socket.socket, "connect", denied)
    monkeypatch.setattr(socket, "getaddrinfo", denied)


def test_exact_manifest_accepted_by_real_core_entry_point():
    assert OP.CORE.validate_manifest is OP.validate_manifest
    assert OP.CORE.option_edit_payload is OP.option_edit_payload
    assert OP.MANIFEST_HASH == "0ac83abdcf4d61caecc235e785d4734346a2bfa596afa4f5be883c79753537fa"
    assert OP.CORE.digest(MANIFEST) == OP.MANIFEST_HASH
    OP.CORE.validate_manifest(MANIFEST, PENDING)
    assert len(MANIFEST["decisions"]) == 21
    assert len(ROWS) == 420 and len(PENDING) == 101
    assert sum(r["status"] == "approved" for r in ROWS.values()) == 319
    empty_rows = [
        ROWS[("option", e["id"])] for e in MANIFEST["decisions"] if e["id"] != OP.EXISTING_ID
    ]
    assert len(empty_rows) == 20
    assert all(r["url"] is r["evidence_url"] is r["property_id"] is None for r in empty_rows)
    for entry in MANIFEST["decisions"]:
        payload = OP.option_edit_payload(ROWS[("option", entry["id"])], entry)
        assert payload.version == 1 and payload.property_id is None
        assert payload.url == entry["option_patch"]["url"]
        assert payload.evidence_url == entry["option_patch"]["evidence_url"]


def test_daiwa_correction_retains_exact_old_and_new_identity():
    assert EXISTING_ROW["url"] == OP.EXISTING_URL
    assert EXISTING_ROW["evidence_url"] == OP.EXISTING_EVIDENCE
    assert EXISTING_ROW["property_id"] is None
    payload = OP.option_edit_payload(EXISTING_ROW, EXISTING_ENTRY)
    assert payload.model_dump() == {
        "version": 1,
        "provider": "agoda",
        "url": OP.CORRECTED_URL,
        "property_id": None,
        "evidence_url": OP.CORRECTED_URL,
        "identity_note": EXISTING_ENTRY["identity_note"],
        "discovery_status": "found",
    }
    assert {OP.EXISTING_URL, OP.EXISTING_EVIDENCE, OP.CORRECTED_URL} <= set(
        EXISTING_ENTRY["source_urls"]
    )


@pytest.mark.parametrize("mutation", ["reason", "order", "missing", "extra", "url"])
def test_real_write_entry_point_rejects_any_manifest_drift(mutation):
    manifest = copy.deepcopy(MANIFEST)
    if mutation == "reason":
        manifest["decisions"][0]["reason"] += " Changed after review."
    elif mutation == "order":
        manifest["decisions"].reverse()
    elif mutation == "missing":
        manifest["decisions"].pop()
    elif mutation == "extra":
        manifest["decisions"].append(copy.deepcopy(EMPTY_ENTRY))
    elif mutation == "url":
        manifest["decisions"][0]["option_patch"]["url"] = OP.EXISTING_URL
    with pytest.raises(ValueError, match="exact pinned"):
        OP.CORE.validate_manifest(manifest, PENDING)


@pytest.mark.parametrize(
    "mutation",
    ["non_iab", "unverified", "hold", "facts", "evidence", "no_patch", "unknown", "old_time"],
)
def test_structural_checks_are_not_hidden_by_manifest_hash(mutation):
    manifest = copy.deepcopy(MANIFEST)
    entry = next(e for e in manifest["decisions"] if e["id"] == EMPTY_ENTRY["id"])
    if mutation == "non_iab":
        entry["method"] = "primary_web"
    elif mutation == "unverified":
        entry["browser_verified"] = False
    elif mutation == "hold":
        entry["decision"] = "hold"
        entry.pop("option_patch")
        entry.pop("identity_note")
    elif mutation == "facts":
        entry["facts_patch"] = {"latitude": 0}
    elif mutation == "evidence":
        entry["evidence"] = {"unreviewed": True}
    elif mutation == "no_patch":
        entry.pop("option_patch")
    elif mutation == "unknown":
        entry["unreviewed_field"] = True
    elif mutation == "old_time":
        entry["checked_at"] = OP.BASELINE_CAPTURED_AT
    with pytest.raises(ValueError):
        OP.validate_payload(manifest, PENDING)


def test_structural_subset_bounds_do_not_bypass_exact_write_pin(monkeypatch):
    subset = copy.deepcopy(MANIFEST)
    subset["decisions"] = [copy.deepcopy(EMPTY_ENTRY)]
    OP.validate_payload(subset, PENDING)
    with pytest.raises(ValueError, match="exact pinned"):
        OP.CORE.validate_manifest(subset, PENDING)
    # Isolate the wrapper's own bound from the core's separate duplicate checks.
    monkeypatch.setattr(OP, "CORE_VALIDATE", lambda *args: None)
    for count in (0, 22):
        oversized = copy.deepcopy(MANIFEST)
        oversized["decisions"] = [copy.deepcopy(EMPTY_ENTRY) for _ in range(count)]
        with pytest.raises(ValueError, match="bounded explicit subset"):
            OP.validate_payload(oversized, PENDING)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("product_id", EMPTY_ENTRY["id"]),
        ("provider", "expedia"),
        ("status", "approved"),
        ("version", 2),
        ("property_id", "not-authorized"),
        ("url", OP.CORRECTED_URL),
        ("evidence_url", OP.EXISTING_URL),
        ("discovery_status", "unconfirmed"),
    ],
)
def test_daiwa_requires_each_exact_existing_row_field(field, value):
    row = copy.deepcopy(EXISTING_ROW)
    row[field] = value
    with pytest.raises(ValueError, match="exact pinned old/new URLs"):
        OP.option_edit_payload(row, EXISTING_ENTRY)


@pytest.mark.parametrize(
    "mutation", ["entry_id", "url", "evidence_url", "property_id", "sources", "version"]
)
def test_daiwa_requires_exact_new_payload_and_source_binding(mutation):
    entry = copy.deepcopy(EXISTING_ENTRY)
    if mutation == "entry_id":
        entry["id"] = EMPTY_ENTRY["id"]
    elif mutation == "url":
        entry["option_patch"]["url"] = OP.EXISTING_URL
    elif mutation == "evidence_url":
        entry["option_patch"]["evidence_url"] = OP.EXISTING_EVIDENCE
    elif mutation == "property_id":
        entry["option_patch"]["property_id"] = "not-authorized"
    elif mutation == "sources":
        entry["source_urls"].remove(OP.EXISTING_EVIDENCE)
    elif mutation == "version":
        entry["version"] = 2
    if mutation == "version":
        manifest = copy.deepcopy(MANIFEST)
        manifest["decisions"] = [entry]
        with pytest.raises(ValueError, match="version"):
            OP.validate_payload(manifest, PENDING)
    else:
        with pytest.raises(ValueError, match="exact pinned old/new URLs"):
            OP.option_edit_payload(EXISTING_ROW, entry)


def test_other_existing_identity_does_not_receive_daiwa_exception():
    row = copy.deepcopy(ROWS[("option", EMPTY_ENTRY["id"])])
    row.update(
        url=OP.EXISTING_URL,
        evidence_url=OP.EXISTING_EVIDENCE,
        discovery_status="found",
    )
    with pytest.raises(ValueError):
        OP.option_edit_payload(row, EMPTY_ENTRY)


def test_full_snapshot_protects_every_catalog_row_and_configuration():
    changed = copy.deepcopy(BASE)
    assert OP.CORE.verify_state(changed, BASE, ROWS, MANIFEST, {}) == ROWS
    tested = protected_approved = 0
    for collection in ("products", "options"):
        for row in changed[collection]:
            version = row["version"]
            row["version"] = version + 1
            with pytest.raises(RuntimeError, match="Full-row snapshot changed"):
                OP.CORE.verify_state(changed, BASE, ROWS, MANIFEST, {})
            row["version"] = version
            tested += 1
            protected_approved += row["status"] == "approved"
    assert tested == 420 and protected_approved == 319
    changed["configs"][0]["version"] += 1
    with pytest.raises(RuntimeError, match="Configuration changed"):
        OP.CORE.verify_state(changed, BASE, ROWS, MANIFEST, {})


@pytest.mark.parametrize("mutation", ["removed", "added"])
def test_full_catalog_membership_cannot_change(mutation):
    changed = copy.deepcopy(BASE)
    if mutation == "removed":
        changed["options"].pop()
    else:
        new_row = copy.deepcopy(changed["options"][0])
        new_row["id"] = "00000000-0000-0000-0000-000000000001"
        changed["options"].append(new_row)
    with pytest.raises(RuntimeError, match="membership changed"):
        OP.CORE.verify_state(changed, BASE, ROWS, MANIFEST, {})


def test_baseline_timestamp_and_all_collections_are_hash_pinned(monkeypatch):
    for field in ("captured_at", "products", "options", "configs"):
        changed = copy.deepcopy(BASE)
        changed[field] = None
        monkeypatch.setattr(OP.CORE, "read_json", lambda _, value=changed: value)
        with pytest.raises(ValueError, match="Unexpected platform batch baseline"):
            OP.baseline_data("offline-unused")
