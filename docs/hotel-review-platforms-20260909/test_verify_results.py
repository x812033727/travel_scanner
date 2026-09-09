"""Synthetic platform review verification tests; no API/database/network imports."""

import copy
import hashlib
import importlib.util
import json
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("platform_test_verifier", HERE / "verify_results.py")
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)
BASE = V.PURE.read_json(HERE / "before.json")
ORIGINAL = V.indexed(BASE)
EMPTY = sorted(
    i
    for (kind, i), row in ORIGINAL.items()
    if kind == "option"
    and row["status"] == "pending"
    and row["url"] is None
    and row["provider"] in {"expedia", "agoda"}
    and ORIGINAL[("product", row["product_id"])]["destination_id"] in {"taipei", "osaka"}
)


def time_at(minutes):
    return (V.stamp(V.BASELINE_AT) + timedelta(minutes=minutes)).isoformat()


def fixture(size=3, approved=3):
    ids = ([V.DAIWA] + EMPTY)[:size]
    final = copy.deepcopy(BASE)
    final["captured_at"] = time_at(3)
    current = V.indexed(final)
    decisions, dry, apply, replay = [], [], [], []
    for pos, identifier in enumerate(ids):
        old, new = ORIGINAL[("option", identifier)], current[("option", identifier)]
        url = (
            V.DAIWA_NEW
            if identifier == V.DAIWA
            else (f"https://www.{old['provider']}.com/offline-fixture-{identifier}")
        )
        entry = {
            "kind": "option",
            "id": identifier,
            "version": old["version"],
            "before_hash": V.digest(old),
            "decision": "approve",
            "reason": "Synthetic only",
            "method": "iab",
            "checked_at": time_at(1),
            "browser_verified": True,
            "source_urls": [url],
            "option_patch": {"url": url, "evidence_url": url},
            "identity_note": "Offline fixture name and full address; never production evidence.",
        }
        success = pos < approved
        if success:
            new.update(entry["option_patch"])
            new.update(
                status="approved",
                version=3,
                discovery_status="found",
                identity_note=entry["identity_note"],
                checked_at=time_at(2),
                verified_at=time_at(2),
                updated_at=time_at(2),
                health_status="unconfirmed",
            )
        target = f"{V.TAG}:option:{identifier}"
        result = {
            "target": target,
            "outcome": "approved" if success else "hold",
            "receipt_id": str(uuid4()),
            "after_hash": V.digest(new),
            "guard_code": None if success else "service_link_unavailable",
        }
        decisions.append(entry)
        dry.append(
            {
                "target": target,
                "decision": "approve",
                "before_hash": V.digest(old),
                "mode": "dry-run",
            }
        )
        apply.append(result)
        replay.append(
            {k: result[k] for k in ("target", "receipt_id", "after_hash")} | {"outcome": "replayed"}
        )
    manifest = {
        "schema_version": 1,
        "tag": V.TAG,
        "baseline_hash": V.BASELINE_HASH,
        "decisions": decisions,
    }
    repeated = copy.deepcopy(final)
    repeated["captured_at"] = time_at(4)
    return [copy.deepcopy(BASE), manifest, dry, apply, replay, final, repeated]


@pytest.mark.parametrize("size,approved", [(1, 0), (1, 1), (3, 0), (3, 2), (3, 3), (21, 21)])
def test_subset_size_and_actual_normal_guard_outcomes(size, approved):
    report = V.rows_check(*fixture(size, approved))
    assert report["scope_count"] == size
    assert report["approved"] == approved
    assert report["untouched_rows"] == 420 - approved


@pytest.mark.parametrize("position", [2, 3, 4])
def test_stdout_exact_unique_coverage(position):
    data = fixture()
    data[position].append(copy.deepcopy(data[position][0]))
    with pytest.raises(ValueError, match="Duplicate"):
        V.rows_check(*data)


@pytest.mark.parametrize(
    "field,value",
    [
        ("property_id", "not-authorized"),
        ("provider", "booking"),
        ("version", 2),
        ("health_status", "unsafe"),
        ("health_status", "unavailable"),
        ("url", "https://www.agoda.com/different-property"),
    ],
)
def test_approved_wrong_fields_rejected_even_if_hashes_recomputed(field, value):
    data = fixture()
    row = V.indexed(data[5])[("option", V.DAIWA)]
    row[field] = value
    data[6]["options"] = copy.deepcopy(data[5]["options"])
    for output in (data[3], data[4]):
        output[0]["after_hash"] = V.digest(row)
    with pytest.raises(ValueError):
        V.rows_check(*data)


def test_known_nonfatal_health_allowed_but_unknown_conflict_not_held():
    data = fixture()
    row = V.indexed(data[5])[("option", V.DAIWA)]
    row["health_status"] = "blocked"
    data[6]["options"] = copy.deepcopy(data[5]["options"])
    for output in (data[3], data[4]):
        output[0]["after_hash"] = V.digest(row)
    V.rows_check(*data)
    data = fixture(1, 0)
    data[3][0]["guard_code"] = "service_version_conflict"
    with pytest.raises(ValueError, match="Unknown guard"):
        V.rows_check(*data)


@pytest.mark.parametrize("collection", ["products", "options", "configs"])
def test_nonscope_rows_and_configs_unchanged(collection):
    data = fixture(1, 1)
    row = next(r for r in data[5][collection] if r["id"] != V.DAIWA)
    row["updated_at"] = time_at(2)
    data[6][collection] = copy.deepcopy(data[5][collection])
    with pytest.raises(ValueError):
        V.rows_check(*data)


def test_daiwa_path_cannot_change_and_hold_cannot_retain_edits():
    data = fixture(1, 0)
    data[1]["decisions"][0]["option_patch"]["url"] = (
        "https://www.agoda.com/other/hotel/kyoto-jp.html"
    )
    with pytest.raises(ValueError):
        V.rows_check(*data)
    data = fixture(1, 0)
    row = V.indexed(data[5])[("option", V.DAIWA)]
    row["evidence_url"] = V.DAIWA_NEW
    data[6]["options"] = copy.deepcopy(data[5]["options"])
    for output in (data[3], data[4]):
        output[0]["after_hash"] = V.digest(row)
    with pytest.raises(ValueError, match="roll back"):
        V.rows_check(*data)


def public_fixture(data):
    result = {}
    for pos, phase in enumerate(V.PHASES):
        source = data[0] if phase == "before" else data[5]
        products = {p["id"]: p for p in source["products"] if p["status"] == "approved"}
        options = {
            o["id"]: o
            for o in source["options"]
            if o["status"] == "approved" and o["product_id"] in products
        }
        responses = []
        for city in sorted(V.PURE.CITIES):
            for locale in sorted(V.PURE.LOCALES):
                items = []
                for identifier, product in sorted(products.items()):
                    if product["destination_id"] != city:
                        continue
                    shown = [
                        {
                            "id": i,
                            "provider": o["provider"],
                            "name": {"agoda": "Agoda", "expedia": "Expedia"}.get(o["provider"]),
                            "mode": "direct",
                            "quote_status": "not_configured",
                        }
                        for i, o in sorted(options.items())
                        if o["product_id"] == identifier
                    ]
                    items.append(
                        {
                            "id": identifier,
                            "kind": "hotel",
                            "destination_id": city,
                            "title": f"{product['title']} {locale}",
                            "source_url": product["source_url"],
                            "source_credits": product["facts"]["source_credits"],
                            **dict.fromkeys(V.PRICES),
                            "booking_options": shown,
                        }
                    )
                responses.append(
                    {
                        "city": city,
                        "locale": locale,
                        "http_status": 200,
                        "cache_control": "no-store",
                        "issues": [],
                        "started_at": time_at(pos * 3 + 1),
                        "completed_at": time_at(pos * 3 + 1),
                        "items": items,
                        "item_ids": sorted(p["id"] for p in items),
                        "booking_option_ids": sorted(
                            o["id"] for p in items for o in p["booking_options"]
                        ),
                        "body_hash": V.digest(items),
                    }
                )
        result[phase] = {
            "tag": V.TAG,
            "phase": phase,
            "baseline_hash": V.BASELINE_HASH,
            "method": "anonymous_public_GET_only",
            "credentials_sent": False,
            "cookies_sent": False,
            "redirects_followed": 0,
            "quote_calls": 0,
            "clickout_calls": 0,
            "mutating_api_calls": 0,
            "database_connections": 0,
            "started_at": time_at(pos * 3 + 1),
            "completed_at": time_at(pos * 3 + 1),
            "summary": {
                "all_checks_pass": True,
                "http_200": 30,
                "no_store_responses": 30,
                "unique_public_products": 40,
                "unique_public_booking_options": len(options),
            },
            "responses": responses,
        }
    return result


@pytest.mark.parametrize("approved", [0, 1, 2, 3])
def test_public_actual_additions_parent_gate_and_old_fields(approved):
    data = fixture(3, approved)
    report = V.public_check(public_fixture(data), data[0], data[5])
    assert report["option_counts"]["after"] == 192 + max(0, approved - 1)


@pytest.mark.parametrize(
    "field,value",
    [
        ("reference_price", 1),
        ("currency", "TWD"),
        ("title", "wrong title"),
        ("source_credits", []),
        ("source_url", "https://example.com/"),
    ],
)
def test_public_drift_rejected_with_consistent_hash(field, value):
    data = fixture()
    public = public_fixture(data)
    response = next(r for r in public["after"]["responses"] if r["items"])
    response["items"][0][field] = value
    response["body_hash"] = V.digest(response["items"])
    with pytest.raises(ValueError):
        V.public_check(public, data[0], data[5])


def test_public_new_quote_and_pending_kyoto_leak_rejected():
    data = fixture()
    public = public_fixture(data)
    row = next(
        r
        for r in public["after"]["responses"]
        if any(o["id"] == EMPTY[0] for p in r["items"] for o in p["booking_options"])
    )
    option = next(o for p in row["items"] for o in p["booking_options"] if o["id"] == EMPTY[0])
    option["quote_status"] = "ready"
    row["body_hash"] = V.digest(row["items"])
    with pytest.raises(ValueError, match="quote"):
        V.public_check(public, data[0], data[5])
    public = public_fixture(data)
    public["after"]["responses"][0]["booking_option_ids"].append(V.DAIWA)
    with pytest.raises(ValueError):
        V.public_check(public, data[0], data[5])


def sql_fixture(data):
    outcomes = V.rows_check(*data)
    results = outcomes["outcomes"]
    specs = {
        "all_hotel_products": 60,
        "non_scope_hotel_options": 360 - len(results),
        "baseline_approved": 319,
        "travel_service_config": None,
        "provider_configs_full": None,
        "provider_configs_stable": None,
        "brands_all": None,
        "hotel_offers": 0,
        "destination_hotel_offers": 0,
        "hotel_booking_clicks_all": 0,
        "affiliate_clicks_hotel": 0,
        "all_historical_audits": None,
        "old_hotel_receipts_387": 387,
    }
    captures = {}
    for pos, phase in enumerate(V.PHASES):
        active = set() if phase == "before" else set(outcomes["approved_ids"])
        scope, receipts, audits, checks = [], [], [], []
        for index, result in enumerate(results):
            identifier, success = result["id"], result["id"] in active
            scope.append(
                {
                    "id": identifier,
                    "parent_id": result["product_id"],
                    "parent_match": True,
                    "provider_match": True,
                    "provider": result["provider"],
                    "baseline_provider": result["provider"],
                    "parent_status": result["parent_status"],
                    "parent_destination_id": result["destination_id"],
                    "before_version": 1,
                    "version": 3 if success else 1,
                    "status": "approved" if success else "pending",
                    "property_id_null": True,
                    "before_url_null": result["before_url"] is None,
                    "before_evidence_url_null": result["before_evidence_url"] is None,
                    "url_null": not success and result["before_url"] is None,
                    "evidence_url_null": not success and result["before_evidence_url"] is None,
                    "before_url_matches_baseline": not success,
                    "before_evidence_url_matches_baseline": not success,
                    "url_matches_manifest": success,
                    "evidence_url_matches_manifest": success,
                    "row_md5": V.digest([identifier, success])[:32],
                }
            )
            if phase != "before":
                fields = (
                    "receipt_id",
                    "target",
                    "requested_decision",
                    "outcome",
                    "guard_code",
                    "entry_hash",
                    "before_hash",
                    "after_hash",
                    "before_version",
                    "after_version",
                )
                receipts.append(
                    {
                        **{k: result[k] for k in fields},
                        "kind": "option",
                        "browser_verified": "true",
                        "actor_root_match": True,
                        "actor_null": False,
                        **dict.fromkeys(
                            (
                                "provenance_match",
                                "scope_match",
                                "entry_hash_match",
                                "before_hash_match",
                                "option_patch_match",
                                "after_hash_valid",
                            ),
                            True,
                        ),
                        "target_id": identifier,
                        "created_at": time_at(2),
                        "row_md5": V.digest(identifier)[:32],
                    }
                )
            if success:
                for action_index, action in enumerate(V.ACTIONS):
                    audits.append(
                        {
                            "audit_id": f"11111111-1111-4111-8111-{index * 2 + action_index:012d}",
                            "action": action,
                            "target": identifier,
                            "created_at": time_at(2),
                            "row_md5": V.digest([identifier, action])[:32],
                            "in_scope": True,
                            "actor_root_match": True,
                            "actor_null": False,
                        }
                    )
            checks.append(
                {
                    "id": identifier,
                    "receipt_count": int(phase != "before"),
                    "edit_audit_count": int(success),
                    "review_audit_count": int(success),
                    "outcome": None if phase == "before" else result["outcome"],
                    "row_transition_valid": True,
                }
            )
        md5 = hashlib.md5(
            "".join(r["row_md5"] for r in sorted(receipts, key=lambda r: r["receipt_id"])).encode(),
            usedforsecurity=False,
        ).hexdigest()
        captures[phase] = {
            "schema_version": 1,
            "tag": V.TAG,
            "phase": phase,
            "baseline_hash": V.BASELINE_HASH,
            "baseline_at": V.BASELINE_AT,
            "completed_with": "ROLLBACK",
            "snapshot": {
                "captured_at": time_at(pos * 2 + 1),
                "isolation_level": "repeatable read",
                "read_only": "on",
                "matching_roots": 1,
                "review_pending_roots": 1,
                "active_actors": 1,
                "authenticated_request_audits": 1,
            },
            "expected": {
                "scope_count": len(results),
                "receipts": len(receipts),
                "approved": len(active),
                "edits": len(active),
                "holds": 0 if phase == "before" else len(results) - len(active),
            },
            "inventory": {
                "hotel_products": 60,
                "hotel_options": 360,
                "approved_products": 40,
                "approved_options": 279 + len(active),
            },
            "protected_groups": [
                {
                    "name": name,
                    "count": value if value is not None else 1,
                    "expected_count": value,
                    "count_matches": None if value is None else True,
                    "rows_md5": V.digest(name)[:32],
                }
                for name, value in specs.items()
            ],
            "scope_rows": scope,
            "receipts": receipts,
            "normal_audits": audits,
            "entry_checks": checks,
            "receipt_totals": {
                "count": len(receipts),
                "distinct_targets": len(receipts),
                "approved": len(active),
                "holds": 0 if phase == "before" else len(results) - len(active),
                "rows_md5": md5,
            },
        }
    return captures, outcomes


@pytest.mark.parametrize("size,approved", [(1, 0), (1, 1), (3, 0), (3, 2), (21, 21)])
def test_sql_dynamic_counts_and_existing_url_hold(size, approved):
    report = V.independent_check(*sql_fixture(fixture(size, approved)))
    assert report["receipts"] == size
    assert report["normal_edits"] == approved


@pytest.mark.parametrize(
    "mutation",
    [
        lambda d: d["after"]["snapshot"].update(read_only="off"),
        lambda d: d["after"]["expected"].update(approved=0),
        lambda d: d["after"]["protected_groups"][0].update(rows_md5="0" * 32),
        lambda d: d["after"]["scope_rows"][0].update(property_id_null=False),
        lambda d: d["after"]["scope_rows"][0].update(before_url_matches_baseline=True),
        lambda d: d["after"]["receipts"][0].update(actor_root_match=False),
        lambda d: d["after"]["receipts"][0].update(entry_hash="0" * 64),
        lambda d: d["after"]["receipts"][0].update(option_patch_match=False),
        lambda d: d["after"]["normal_audits"].pop(),
        lambda d: d["after"]["normal_audits"][0].update(actor_null=True),
        lambda d: d["after"]["entry_checks"][0].update(review_audit_count=0),
        lambda d: d["after-replay"]["normal_audits"][0].update(audit_id=str(uuid4())),
        lambda d: d["after-replay"]["scope_rows"][0].update(row_md5="0" * 32),
    ],
)
def test_sql_scope_actor_hash_and_replay_errors_rejected(mutation):
    captures, outcomes = sql_fixture(fixture())
    mutation(captures)
    with pytest.raises(ValueError):
        V.independent_check(captures, outcomes)


def test_daiwa_sql_hold_full_row_unchanged_not_just_url():
    captures, outcomes = sql_fixture(fixture(1, 0))
    for phase in ("after", "after-replay"):
        captures[phase]["scope_rows"][0]["row_md5"] = "0" * 32
    with pytest.raises(ValueError, match="hold full row"):
        V.independent_check(captures, outcomes)


def test_manifest_file_pin_and_missing_final_evidence_fail_closed(tmp_path, monkeypatch):
    # Reading an unpinned or missing manifest must fail before accepting anything.
    with pytest.raises(OSError):
        V.verify(tmp_path, "0" * 64)
    monkeypatch.setattr(Path, "read_bytes", lambda path: b"{}")
    with pytest.raises(ValueError, match="Pinned manifest"):
        V.verify(HERE, "0" * 64)


def test_complete_acceptance_binds_every_retained_file_without_io(monkeypatch):
    data = fixture(3, 2)
    captures, _ = sql_fixture(data)
    public = public_fixture(data)
    files = dict(zip(V.CORE_FILES, data, strict=True))
    files.update({f"independent-{phase}.json": captures[phase] for phase in V.PHASES})
    files.update({f"public-{phase}.json": public[phase] for phase in V.PHASES})

    def contents(path):
        return json.dumps(files[path.name], sort_keys=True).encode()

    monkeypatch.setattr(Path, "read_bytes", contents)
    monkeypatch.setattr(V.PURE, "read_json", lambda path: copy.deepcopy(files[path.name]))
    monkeypatch.setattr(V.PURE, "read_ndjson", lambda path: copy.deepcopy(files[path.name]))
    pinned = hashlib.sha256(contents(HERE / "manifest.json")).hexdigest()
    report = V.verify(HERE, pinned)
    assert report["final_acceptance"]
    assert report["rows"]["approved"] == 2
    assert report["rows"]["holds"] == 1
    assert report["public"]["option_counts"]["after"] == 193
    assert len(report["input_file_sha256"]) == 13
    assert report["network_calls"] == report["database_connections"] == 0
    files.pop("independent-after-replay.json")
    with pytest.raises(KeyError):
        V.verify(HERE, pinned)
