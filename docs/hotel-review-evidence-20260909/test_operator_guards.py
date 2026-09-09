"""Offline wrapper guards. Synthetic fixtures are not additional browser evidence."""

import copy
import hashlib
import importlib.util
import socket
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
WRAPPER = HERE.parents[1] / "ops/hotel_review_evidence_20260909.py"


def load_operator():
    spec = importlib.util.spec_from_file_location("evidence_operator_guard_tests", WRAPPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


OP = load_operator()
BASE, ROWS, PENDING = OP.load_baseline(HERE / "before.json")
CHECKED_AT = "2026-09-09T00:40:00Z"
WESTIN_ROW = ROWS[("product", OP.WESTIN)]
LEADS = OP.CORE.read_json(HERE / "kyoto-expedia-leads.json")["entries"]
TOKYO = [
    item for item in OP.CORE.read_json(HERE / "osaka-rakuten-leads.json")["items"]
    if item["provider"] == "agoda"
]


def common_entry(kind, row):
    return {
        "kind": kind, "id": row["id"], "version": row["version"],
        "before_hash": OP.CORE.digest(row), "decision": "approve",
        "reason": "Offline structural fixture only; this test does not approve a hotel.",
        "method": "iab", "checked_at": CHECKED_AT, "browser_verified": True,
        "new_evidence": "Offline synthetic evidence for guard validation, not a live observation.",
    }


def option_entry(identifier, url):
    entry = common_entry("option", ROWS[("option", identifier)])
    entry.update(
        source_urls=[url],
        identity_note="Offline exact-slot structural fixture; not an additional identity review.",
        option_patch={"url": url, "evidence_url": url},
    )
    return entry


def product_entry(row=WESTIN_ROW):
    entry = common_entry("product", row)
    coords = OP.CORE.coordinate_evidence(row, CHECKED_AT)
    entry.update(
        source_urls=[OP.MAP_URL, coords["url"], row["source_url"], coords["license_url"]],
        facts_patch={
            **OP.CORE.coordinate_patch(row), "google_place_id": OP.PLACE_ID, "map_verified": True,
        },
        evidence={
            "map": {
                "url": OP.MAP_URL, "identity_verified": True, "method": "iab",
                "checked_at": CHECKED_AT, "place_id": OP.PLACE_ID,
            },
            "coordinates": coords,
        },
    )
    return entry


def manifest_for(*entries):
    return {
        "schema_version": 1, "tag": OP.TAG, "baseline_hash": OP.BASELINE_HASH,
        "decisions": copy.deepcopy(list(entries)),
    }


OPTION = option_entry(LEADS[0]["id"], LEADS[0]["candidate_url"])
SYNTHETIC = manifest_for(
    product_entry(),
    *(option_entry(item["id"], item["candidate_url"]) for item in LEADS),
    *(option_entry(item["option_id"], item["candidate_url"]) for item in TOKYO),
)


@pytest.fixture(autouse=True)
def deny_external_access(monkeypatch):
    def denied(*args, **kwargs):
        raise AssertionError("Offline guard tests must not access database or network")

    monkeypatch.setattr(OP.CORE, "SessionFactory", denied)
    monkeypatch.setattr(socket.socket, "connect", denied)
    monkeypatch.setattr(socket.socket, "connect_ex", denied)
    monkeypatch.setattr(socket, "getaddrinfo", denied)


def test_exact_baseline_and_entry_point_wiring():
    assert OP.BASELINE_HASH == "342aee9610db65e78626d950efef368919a7d8e4cfcf55d06a32b64e26c5adee"
    assert OP.BASELINE_CAPTURED_AT == "2026-09-09 00:32:08.141514+00:00"
    assert OP.CORE.digest(BASE) == OP.BASELINE_HASH
    assert OP.CORE.baseline_data is OP.load_baseline
    assert OP.CORE.validate_manifest is OP.validate_manifest
    assert OP.CORE.BASELINE_HASH == OP.BASELINE_HASH and OP.CORE.TAG == OP.TAG
    assert len(ROWS) == 420 and len(PENDING) == 80
    assert sum(r["status"] == "approved" for r in ROWS.values()) == 340
    assert len(OP.OSAKA_PARENTS) == len(OP.TOKYO_PARENTS) == 10


def test_final_manifest_accepted_by_real_pinned_entry_point():
    path = HERE / "manifest.json"
    manifest = OP.CORE.read_json(path)
    assert OP.MANIFEST_HASH == "c39dbbacf10c193de385a2a22930d6fcf4af6c36cea6c28e2b7a5d3bc07a3887"
    assert OP.CORE.digest(manifest) == OP.MANIFEST_HASH
    assert 1 <= len(manifest["decisions"]) <= 19
    OP.CORE.validate_manifest(manifest, PENDING)
    for entry in manifest["decisions"]:
        row = ROWS[(entry["kind"], entry["id"])]
        if entry["kind"] == "option":
            payload = OP.CORE.option_edit_payload(row, entry)
            assert payload.property_id is None and payload.version == 1
            assert payload.url == entry["option_patch"]["url"]
            assert payload.evidence_url == entry["option_patch"]["evidence_url"]
        else:
            payload = OP.CORE.product_payload(row, entry)
            assert "hotel_links" not in payload.facts.model_fields_set


def test_structural_subsets_accept_without_mutating_inputs():
    before = copy.deepcopy((BASE, PENDING, SYNTHETIC))
    sources = [OP.SOURCE, WRAPPER, HERE / "before.json"]
    sources.extend(OP.APP / relative for relative in OP.RUNTIME_SHA256)
    hashes = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    for entries in ([SYNTHETIC["decisions"][0]], [OPTION], SYNTHETIC["decisions"]):
        OP.validate_payload(manifest_for(*entries), PENDING)
    assert (BASE, PENDING, SYNTHETIC) == before
    assert hashes == {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}


@pytest.mark.parametrize("mutation", ["reason", "order", "missing", "extra", "url", "baseline"])
def test_write_entry_point_rejects_manifest_hash_drift(mutation):
    manifest = OP.CORE.read_json(HERE / "manifest.json")
    OP.CORE.validate_manifest(manifest, PENDING)
    changed = copy.deepcopy(manifest)
    if mutation == "reason":
        changed["decisions"][0]["reason"] += " Changed after review."
    elif mutation == "order":
        changed["decisions"].reverse()
    elif mutation == "missing":
        changed["decisions"].pop()
    elif mutation == "extra":
        changed["decisions"].append(copy.deepcopy(OPTION))
    elif mutation == "url":
        entry = next(e for e in changed["decisions"] if e["kind"] == "option")
        entry["option_patch"]["url"] = OP.MAP_URL
    else:
        changed["baseline_hash"] = "0" * 64
    with pytest.raises(ValueError, match="exact pinned"):
        OP.CORE.validate_manifest(changed, PENDING)


@pytest.mark.parametrize("pin", [None, "", "0" * 64])
def test_missing_or_wrong_pin_never_accepts_structurally_valid_input(monkeypatch, pin):
    monkeypatch.setattr(OP, "MANIFEST_HASH", pin)
    with pytest.raises(ValueError, match="exact pinned"):
        OP.CORE.validate_manifest(SYNTHETIC, PENDING)


@pytest.mark.parametrize(
    "mutation",
    ["non_iab", "unverified", "string_bool", "hold", "reject", "unknown", "old_time",
     "version", "before_hash", "facts", "property_id", "missing_source", "no_patch"],
)
def test_real_structural_guards_reject_invalid_option_evidence(mutation):
    entry = copy.deepcopy(OPTION)
    if mutation == "non_iab":
        entry["method"] = "primary_web"
    elif mutation == "unverified":
        entry["browser_verified"] = False
    elif mutation == "string_bool":
        entry["browser_verified"] = "true"
    elif mutation == "hold":
        entry["decision"] = "hold"
        entry.pop("option_patch")
        entry.pop("identity_note")
    elif mutation == "reject":
        entry["decision"] = "reject"
    elif mutation == "unknown":
        entry["unreviewed"] = True
    elif mutation == "old_time":
        entry["checked_at"] = OP.BASELINE_CAPTURED_AT
    elif mutation == "version":
        entry["version"] += 1
    elif mutation == "before_hash":
        entry["before_hash"] = "0" * 64
    elif mutation == "facts":
        entry["facts_patch"] = {"latitude": 0}
    elif mutation == "property_id":
        entry["option_patch"]["property_id"] = "not-authorized"
    elif mutation == "missing_source":
        entry["source_urls"] = [OP.MAP_URL]
    else:
        entry.pop("option_patch")
    with pytest.raises(ValueError):
        OP.validate_payload(manifest_for(entry), PENDING)


def test_real_core_rejects_duplicates_and_non_pending_rows():
    with pytest.raises(ValueError, match="duplicate"):
        OP.validate_payload(manifest_for(OPTION, OPTION), PENDING)
    entry = copy.deepcopy(OPTION)
    entry["id"] = next(r["id"] for r in BASE["options"] if r["status"] == "approved")
    with pytest.raises(ValueError, match="approved"):
        OP.validate_payload(manifest_for(entry), PENDING)


@pytest.mark.parametrize("count", [0, 20])
def test_wrapper_own_subset_bound_independent_of_core(monkeypatch, count):
    # Isolate this wrapper bound; real duplicate/empty rejection is tested separately.
    monkeypatch.setattr(OP, "CORE_VALIDATE", lambda *args: None)
    with pytest.raises(ValueError, match="bounded new-evidence subset"):
        OP.validate_payload(manifest_for(*([OPTION] * count)), PENDING)
    OP.validate_payload(manifest_for(*([OPTION] * 19)), PENDING)


def test_city_provider_scope_is_checked_after_normal_schema(monkeypatch):
    # No invented platform URLs: isolate membership using only the existing pinned rows.
    monkeypatch.setattr(OP, "CORE_VALIDATE", lambda *args: None)
    approved_candidates = rejected = 0
    for (kind, identifier), row in PENDING.items():
        if kind != "option":
            continue
        parent = ROWS[("product", row["product_id"])]
        permitted = (parent["destination_id"], row["provider"]) in {
            ("osaka", "rakuten"), ("tokyo", "agoda"), ("kyoto", "expedia"),
        }
        entry = copy.deepcopy(OPTION)
        entry["id"] = identifier
        if permitted:
            OP.validate_payload(manifest_for(entry), PENDING)
            approved_candidates += 1
        else:
            with pytest.raises(ValueError):
                OP.validate_payload(manifest_for(entry), PENDING)
            rejected += 1
    assert approved_candidates == 19  # Includes Hyatt, separately rejected by the real core.
    assert rejected == 41


def test_operating_date_guard_and_rakuten_host_guard_remain_mandatory():
    row = next(r for r in PENDING.values() if r.get("product_id") in OP.CORE.OPERATING_DATE_HOLDS
               and r.get("provider") == "expedia")
    entry = copy.deepcopy(OPTION)
    entry.update(id=row["id"], version=row["version"], before_hash=OP.CORE.digest(row))
    with pytest.raises(ValueError, match="operating-date"):
        OP.validate_payload(manifest_for(entry), PENDING)
    lead = next(item for item in OP.CORE.read_json(HERE / "osaka-rakuten-leads.json")["items"]
                if item["provider"] == "rakuten")
    entry = option_entry(lead["option_id"], lead["candidate_url"])
    with pytest.raises(ValueError):
        OP.validate_payload(manifest_for(entry), PENDING)


@pytest.mark.parametrize("field", ["url", "evidence_url", "property_id", "version"])
def test_empty_slot_and_original_version_required(field):
    pending = copy.deepcopy(PENDING)
    row = pending[("option", OPTION["id"])]
    row[field] = 2 if field == "version" else OPTION["option_patch"]["url"]
    entry = copy.deepcopy(OPTION)
    entry.update(version=row["version"], before_hash=OP.CORE.digest(row))
    with pytest.raises(ValueError):
        OP.validate_payload(manifest_for(entry), pending)


def test_exact_westin_patch_retains_credit_and_omits_legacy_option_replacement():
    entry = product_entry()
    OP.validate_payload(manifest_for(entry), PENDING)
    payload = OP.CORE.product_payload(WESTIN_ROW, entry)
    patch = entry["facts_patch"]
    assert OP.WESTIN == "50f2d47d-24fe-4b07-85a2-3e1c7671e452"
    assert patch["latitude"] == 35.00886111 and patch["longitude"] == 135.78794444
    assert patch["google_place_id"] == "ChIJN1AzAd8IAWAR2hJ9wcsW4TE"
    assert patch["map_verified"] is True
    assert patch["source_credits"][:-1] == WESTIN_ROW["facts"]["source_credits"]
    assert patch["source_credits"][-1]["license_name"] == "CC0-1.0"
    assert entry["evidence"]["coordinates"]["reference"] == "P143:Q177837"
    assert "hotel_links" not in payload.facts.model_fields_set
    assert payload.source_key == WESTIN_ROW["source_key"]
    assert payload.source_url == WESTIN_ROW["source_url"]


@pytest.mark.parametrize(
    "mutation", ["latitude", "longitude", "credit", "license", "reference", "revision",
                 "non_google", "map_verified", "place_id", "map_url", "identity", "extra"],
)
def test_westin_cannot_relax_coordinate_or_map_provenance(mutation):
    entry = product_entry()
    patch, evidence = entry["facts_patch"], entry["evidence"]
    if mutation in {"latitude", "longitude"}:
        patch[mutation] += 0.001
    elif mutation == "credit":
        patch["source_credits"].pop(0)
    elif mutation == "license":
        evidence["coordinates"]["license_url"] = WESTIN_ROW["source_url"]
    elif mutation == "reference":
        evidence["coordinates"]["reference"] = "P248:Q1319169"
    elif mutation == "revision":
        evidence["coordinates"]["revision"] += 1
    elif mutation == "non_google":
        evidence["coordinates"]["non_google"] = False
    elif mutation == "map_verified":
        patch["map_verified"] = False
    elif mutation == "place_id":
        patch["google_place_id"] = "ChIJ00000000000000000000000"
        evidence["map"]["place_id"] = patch["google_place_id"]
    elif mutation == "map_url":
        evidence["map"]["url"] = WESTIN_ROW["source_url"]
    elif mutation == "identity":
        evidence["map"]["identity_verified"] = False
    else:
        patch["hotel_links"] = []
    # Missing map verification is rejected by the unchanged application service first.
    expected_error = OP.CORE.AppError if mutation == "map_verified" else ValueError
    with pytest.raises(expected_error):
        OP.validate_payload(manifest_for(entry), PENDING)


def test_other_core_allowlisted_product_is_not_westin_exception():
    other = ROWS[("product", "a124dc1e-7f75-44ff-b12d-080da031b3b9")]
    entry = product_entry(other)
    OP.CORE_VALIDATE(manifest_for(entry), PENDING)
    with pytest.raises(ValueError, match="exact Westin"):
        OP.validate_payload(manifest_for(entry), PENDING)


@pytest.mark.parametrize("source", ["immutable_core", *OP.RUNTIME_SHA256])
def test_import_rejects_each_changed_source_without_writing_files(monkeypatch, source):
    target = OP.SOURCE if source == "immutable_core" else OP.APP / source
    original = Path.read_bytes

    def changed_bytes(path):
        value = original(path)
        return value + b"\n# offline mutation" if path.resolve() == target.resolve() else value

    monkeypatch.setattr(Path, "read_bytes", changed_bytes)
    with pytest.raises(RuntimeError, match="Immutable core|Current application source"):
        load_operator()


def test_all_baseline_collections_are_semantically_pinned(monkeypatch):
    for field in ("captured_at", "products", "options", "configs"):
        changed = copy.deepcopy(BASE)
        changed[field] = None
        monkeypatch.setattr(OP.CORE, "read_json", lambda _, value=changed: value)
        with pytest.raises(ValueError, match="exact post-deployment baseline"):
            OP.load_baseline("offline-unused")


def test_full_420_rows_340_approved_and_configs_cannot_drift():
    changed = copy.deepcopy(BASE)
    assert OP.CORE.verify_state(changed, BASE, ROWS, SYNTHETIC, {}) == ROWS
    total = approved = 0
    for collection in ("products", "options"):
        for row in changed[collection]:
            original = row["version"]
            row["version"] += 1
            with pytest.raises(RuntimeError, match="Full-row snapshot changed"):
                OP.CORE.verify_state(changed, BASE, ROWS, SYNTHETIC, {})
            row["version"] = original
            total += 1
            approved += row["status"] == "approved"
    assert total == 420 and approved == 340
    changed["configs"][0]["version"] += 1
    with pytest.raises(RuntimeError, match="Configuration changed"):
        OP.CORE.verify_state(changed, BASE, ROWS, SYNTHETIC, {})


@pytest.mark.parametrize("mutation", ["remove", "add"])
def test_catalog_membership_changes_are_rejected(mutation):
    changed = copy.deepcopy(BASE)
    if mutation == "remove":
        changed["options"].pop()
    else:
        row = copy.deepcopy(changed["options"][0])
        row["id"] = "00000000-0000-0000-0000-000000000001"
        changed["options"].append(row)
    with pytest.raises(RuntimeError, match="membership changed"):
        OP.CORE.verify_state(changed, BASE, ROWS, SYNTHETIC, {})
