"""Synthetic mixed-review verification tests; no API/database/network imports."""

import copy
import hashlib
import importlib.util
import json
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("mixed_test_verifier", HERE / "verify_results.py")
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)
BASE = V.PURE.read_json(HERE / "before.json")
ORIGINAL = V.indexed(BASE)
WESTIN_EXPEDIA = "42a3558d-bb99-4312-abe8-e06e080c09a3"
TOKYO_AGODA = "e5da18b7-0b5e-4e1d-8c38-d76d8b795ac8"
ORDER = [V.WESTIN, WESTIN_EXPEDIA, TOKYO_AGODA] + sorted(
    V.ALLOWED_OPTIONS - {WESTIN_EXPEDIA, TOKYO_AGODA}
)


def time_at(minutes):
    return (V.stamp(V.BASELINE_AT) + timedelta(minutes=minutes)).isoformat()


def fixture(size=3, approved=3):
    final = copy.deepcopy(BASE)
    final["captured_at"] = time_at(3)
    current = V.indexed(final)
    decisions, dry, apply, replay = [], [], [], []
    for pos, identifier in enumerate(ORDER[:size]):
        kind = "product" if identifier == V.WESTIN else "option"
        old, new = ORIGINAL[(kind, identifier)], current[(kind, identifier)]
        entry = {
            "kind": kind,
            "id": identifier,
            "version": old["version"],
            "before_hash": V.digest(old),
            "decision": "approve",
            "reason": "Synthetic only",
            "method": "iab",
            "checked_at": time_at(1),
            "browser_verified": True,
        }
        if kind == "product":
            entry.update(
                source_urls=[V.MAP_URL, V.COORDINATE_URL],
                facts_patch=V.expected_facts(old),
                evidence={
                    "map": {
                        "url": V.MAP_URL,
                        "identity_verified": True,
                        "method": "iab",
                        "checked_at": time_at(1),
                        "place_id": V.PLACE_ID,
                    },
                    "coordinates": {
                        "url": V.COORDINATE_URL,
                        "license_url": V.LICENSE_URL,
                        "non_google": True,
                        "checked_at": time_at(1),
                        "qid": V.QID,
                        "claim_id": V.CLAIM_ID,
                        "revision": V.REVISION,
                        "reference": "P143:Q177837",
                    },
                },
            )
        else:
            url = f"https://www.{old['provider']}.com/offline-fixture-{identifier}"
            entry.update(
                source_urls=[url],
                option_patch={"url": url, "evidence_url": url},
                identity_note="Offline fixture only, never production evidence.",
            )
        success = pos < approved
        if success:
            new.update(status="approved", version=3, verified_at=time_at(2), updated_at=time_at(2))
            if kind == "product":
                new["facts"].update(entry["facts_patch"])
            else:
                new.update(entry["option_patch"])
                new.update(
                    discovery_status="found",
                    identity_note=entry["identity_note"],
                    checked_at=time_at(2),
                    health_status="unconfirmed",
                )
        target = f"{V.TAG}:{kind}:{identifier}"
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


def rehash(data, identifier):
    kind = "product" if identifier == V.WESTIN else "option"
    data[6]["products"] = copy.deepcopy(data[5]["products"])
    data[6]["options"] = copy.deepcopy(data[5]["options"])
    for stream in (data[3], data[4]):
        next(r for r in stream if r["target"].endswith(identifier))["after_hash"] = V.digest(
            V.indexed(data[5])[(kind, identifier)]
        )


@pytest.mark.parametrize("size,approved", [(1, 0), (1, 1), (3, 0), (3, 2), (3, 3), (19, 19)])
def test_variable_mixed_scope_and_actual_guard_outcomes(size, approved):
    report = V.rows_check(*fixture(size, approved))
    assert report["scope_count"] == size
    assert report["approved"] == approved
    assert report["untouched_rows"] == 420 - approved


@pytest.mark.parametrize("index", [2, 3, 4])
def test_stdout_exact_coverage(index):
    data = fixture()
    data[index].append(copy.deepcopy(data[index][0]))
    with pytest.raises(ValueError, match="Duplicate"):
        V.rows_check(*data)


@pytest.mark.parametrize(
    "field,value",
    [
        ("latitude", 35.1),
        ("longitude", 135.1),
        ("source_credits", []),
        ("coordinate_source_url", "https://example.com/"),
        ("map_verified", False),
        ("google_place_id", "ChIJWrongPlaceID"),
        ("reference_price", 99),
    ],
)
def test_product_tampered_facts_even_with_matching_receipt_hash(field, value):
    data = fixture()
    V.indexed(data[5])[("product", V.WESTIN)]["facts"][field] = value
    rehash(data, V.WESTIN)
    with pytest.raises(ValueError, match="facts changed"):
        V.rows_check(*data)


@pytest.mark.parametrize(
    "field,value",
    [
        ("latitude", 35.1),
        ("source_credits", []),
        ("google_place_id", "ChIJWrong"),
    ],
)
def test_manifest_patch_cannot_expand_coordinate_authority(field, value):
    data = fixture()
    data[1]["decisions"][0]["facts_patch"][field] = value
    with pytest.raises(ValueError, match="fact patch"):
        V.rows_check(*data)


@pytest.mark.parametrize(
    "where,field,value",
    [
        ("map", "place_id", "ChIJWrong"),
        ("map", "url", "https://www.google.com/maps/"),
        ("map", "checked_at", V.BASELINE_AT),
        ("coordinates", "revision", 1),
        ("coordinates", "claim_id", "Q11288502$wrong"),
        ("coordinates", "license_url", "https://example.com/"),
        ("coordinates", "checked_at", V.BASELINE_AT),
    ],
)
def test_product_manifest_provenance_tamper(where, field, value):
    data = fixture()
    data[1]["decisions"][0]["evidence"][where][field] = value
    with pytest.raises(ValueError):
        V.rows_check(*data)


@pytest.mark.parametrize(
    "field,value",
    [
        ("property_id", "not-authorized"),
        ("provider", "booking"),
        ("version", 2),
        ("health_status", "unsafe"),
        ("health_status", "unavailable"),
        ("url", "https://example.com/different-property"),
    ],
)
def test_option_tampered_fields(field, value):
    data = fixture()
    V.indexed(data[5])[("option", WESTIN_EXPEDIA)][field] = value
    rehash(data, WESTIN_EXPEDIA)
    with pytest.raises(ValueError):
        V.rows_check(*data)


def test_stale_manifest_version_and_unknown_guard_rejected():
    data = fixture()
    data[1]["decisions"][0]["version"] = 2
    with pytest.raises(ValueError, match="version"):
        V.rows_check(*data)
    data = fixture(1, 0)
    data[3][0]["guard_code"] = "service_version_conflict"
    with pytest.raises(ValueError, match="Unknown guard"):
        V.rows_check(*data)


def test_hold_full_rollback_and_replay_unchanged():
    data = fixture(1, 0)
    V.indexed(data[5])[("product", V.WESTIN)]["facts"]["map_verified"] = True
    rehash(data, V.WESTIN)
    with pytest.raises(ValueError, match="roll back"):
        V.rows_check(*data)
    data = fixture()
    data[4][0]["receipt_id"] = str(uuid4())
    with pytest.raises(ValueError, match="Replay"):
        V.rows_check(*data)


@pytest.mark.parametrize("collection", ["products", "options", "configs"])
def test_protected_fullrows_and_configuration(collection):
    data = fixture(1, 1)
    next(r for r in data[5][collection] if r["id"] != V.WESTIN)["updated_at"] = time_at(2)
    data[6][collection] = copy.deepcopy(data[5][collection])
    with pytest.raises(ValueError):
        V.rows_check(*data)


def test_coordinate_fresh_artifact_and_literal_tamper():
    evidence = V.PURE.read_json(HERE / "westin-coordinate-evidence.json")
    V.coordinate_check(evidence)
    for section, field, value in [
        ("current", "lastrevid", 1),
        ("pinned", "url", "https://example.com"),
        ("current", "checked_at", V.BASELINE_AT),
        ("pinned", "http_status", 503),
    ]:
        bad = copy.deepcopy(evidence)
        bad[section][field] = value
        with pytest.raises(ValueError):
            V.coordinate_check(bad)
    bad = copy.deepcopy(evidence)
    bad["current"]["selected_claim"]["mainsnak"]["datavalue"]["value"]["latitude"] = 35.1
    with pytest.raises(ValueError):
        V.coordinate_check(bad)


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
                            "name": V.NAMES[o["provider"]],
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
                            "title": product["names_json"].get(locale) or product["title"],
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
                "unique_public_products": len(products),
                "unique_public_booking_options": len(options),
            },
            "responses": responses,
        }
    return result


@pytest.mark.parametrize("approved", [0, 1, 2, 3, 19])
def test_public_new_parent_options_derived_from_actual_final(approved):
    data = fixture(19, approved)
    report = V.public_check(public_fixture(data), data[0], data[5])
    final = V.indexed(data[5])
    expected = sum(
        k == "option"
        and row["status"] == "approved"
        and final[("product", row["product_id"])]["status"] == "approved"
        for (k, _), row in final.items()
    )
    assert report["option_counts"]["before"] == 212
    assert report["option_counts"]["after"] == expected
    assert report["products"] == 40 + int(approved > 0)


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
def test_public_new_westin_and_original_fields_checked(field, value):
    data = fixture()
    captures = public_fixture(data)
    response = next(
        r for r in captures["after"]["responses"] if r["city"] == "kyoto" and r["locale"] == "en"
    )
    response["items"][0][field] = value
    response["body_hash"] = V.digest(response["items"])
    with pytest.raises(ValueError):
        V.public_check(captures, data[0], data[5])


def test_pending_parent_option_leak_and_replay_tamper():
    data = fixture(19, 0)
    captures = public_fixture(data)
    response = next(r for r in captures["after"]["responses"] if r["city"] == "kyoto")
    response["booking_option_ids"].append(WESTIN_EXPEDIA)
    with pytest.raises(ValueError):
        V.public_check(captures, data[0], data[5])
    data = fixture()
    captures = public_fixture(data)
    captures["after-replay"]["responses"][0]["body_hash"] = "0" * 64
    with pytest.raises(ValueError):
        V.public_check(captures, data[0], data[5])


def test_new_visible_old_westin_options_cannot_enable_prices():
    data = fixture(1, 1)
    captures = public_fixture(data)
    response = next(r for r in captures["after"]["responses"] if r["city"] == "kyoto")
    response["items"][0]["booking_options"][0]["quote_status"] = "ready"
    response["body_hash"] = V.digest(response["items"])
    with pytest.raises(ValueError, match="quote"):
        V.public_check(captures, data[0], data[5])


def test_manifest_file_pin_and_missing_evidence_fail_closed(tmp_path, monkeypatch):
    with pytest.raises(OSError):
        V.verify(tmp_path, "0" * 64)
    monkeypatch.setattr(Path, "read_bytes", lambda path: b"{}")
    with pytest.raises(ValueError, match="Pinned manifest"):
        V.verify(HERE, "0" * 64)


def sql_fixture(data):
    outcomes = V.rows_check(*data)
    results = outcomes["outcomes"]
    product_n = sum(r["kind"] == "product" for r in results)
    option_n = len(results) - product_n
    specs = {
        "non_scope_hotel_products": 60 - product_n,
        "non_scope_hotel_options": 360 - option_n,
        "baseline_approved": 340,
        "travel_service_config": None,
        "provider_configs_full": None,
        "provider_configs_stable": None,
        "brands_all": None,
        "hotel_offers": 0,
        "destination_hotel_offers": 0,
        "hotel_booking_clicks_all": 0,
        "affiliate_clicks_hotel": 0,
        "all_historical_audits": None,
        "old_hotel_receipts_408": 408,
    }
    captures = {}
    for pos, phase in enumerate(V.PHASES):
        active = set() if phase == "before" else set(outcomes["approved_ids"])
        scope, receipts, audits, checks = [], [], [], []
        for index, result in enumerate(results):
            identifier, success = result["id"], result["id"] in active
            option = result["kind"] == "option"
            scope.append(
                {
                    "id": identifier,
                    "kind": result["kind"],
                    "parent_id": result["product_id"] if option else None,
                    "baseline_source_key": result["source_key"],
                    "baseline_destination_id": result["destination_id"],
                    "baseline_parent_status": result["parent_status"] if option else None,
                    "before_hash": result["before_hash"],
                    "parent_match": True if option else None,
                    "provider_match": True if option else None,
                    "provider": result["provider"],
                    "baseline_provider": result["provider"],
                    "parent_status": (
                        (
                            result["parent_status"]
                            if phase == "before"
                            else result["final_parent_status"]
                        )
                        if option
                        else None
                    ),
                    "parent_destination_id": result["destination_id"] if option else None,
                    "parent_in_scope": option
                    and result["product_id"] in {r["id"] for r in results},
                    "before_version": 1,
                    "version": 3 if success else 1,
                    "status": "approved" if success else "pending",
                    "property_id_null": True if option else None,
                    "before_url_null": True if option else None,
                    "before_evidence_url_null": True if option else None,
                    "url_null": not success if option else None,
                    "evidence_url_null": not success if option else None,
                    "before_url_matches_baseline": not success if option else None,
                    "before_evidence_url_matches_baseline": not success if option else None,
                    "before_discovery_matches_baseline": not success if option else None,
                    "url_matches_manifest": success if option else None,
                    "evidence_url_matches_manifest": success if option else None,
                    "discovery_found": success if option else None,
                    "health_status": result["after_health"] if success else result["before_health"],
                    "product_identity_matches_baseline": None if option else True,
                    "before_facts_matches_baseline": None if option else not success,
                    "facts_patch_matches_manifest": None if option else success,
                    "non_patch_facts_match": None if option else True,
                    "row_md5": V.digest([identifier, success])[:32],
                    "immutable_fields_md5": V.digest([identifier, "immutable"])[:32],
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
                        "kind": result["kind"],
                        "browser_verified": "true" if success else "false",
                        "actor_root_match": True,
                        "actor_null": False,
                        **dict.fromkeys(
                            (
                                "provenance_match",
                                "scope_match",
                                "entry_hash_match",
                                "before_hash_match",
                                "option_patch_match",
                                "evidence_binding_match",
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
                for action_index, action in enumerate(V.ACTIONS[result["kind"]]):
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
                    "kind": result["kind"],
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
                "product_scope_count": product_n,
                "option_scope_count": option_n,
                "receipts": len(receipts),
                "approved": len(active),
                "edits": len(active),
                "holds": 0 if phase == "before" else len(results) - len(active),
            },
            "inventory": {
                "hotel_products": 60,
                "hotel_options": 360,
                "approved_products": 40 + int(V.WESTIN in active),
                "approved_options": 300 + len(active) - int(V.WESTIN in active),
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
                "approved_products": int(V.WESTIN in active),
                "approved_options": len(active) - int(V.WESTIN in active),
                "holds": 0 if phase == "before" else len(results) - len(active),
                "rows_md5": md5,
            },
        }
    return captures, outcomes


@pytest.mark.parametrize("size,approved", [(1, 0), (1, 1), (3, 0), (3, 1), (3, 2), (19, 19)])
def test_mixed_sql_counts_parent_transition_and_rollback(size, approved):
    report = V.independent_check(*sql_fixture(fixture(size, approved)))
    assert report["receipts"] == size
    assert report["normal_edits"] == approved


@pytest.mark.parametrize(
    "mutation",
    [
        lambda d: d["after"]["snapshot"].update(read_only="off"),
        lambda d: d["after"]["expected"].update(approved=0),
        lambda d: d["after"]["protected_groups"][0].update(rows_md5="0" * 32),
        lambda d: d["after"]["scope_rows"][0].update(facts_patch_matches_manifest=False),
        lambda d: d["after"]["scope_rows"][0].update(non_patch_facts_match=False),
        lambda d: d["after"]["scope_rows"][1].update(property_id_null=False),
        lambda d: d["after"]["scope_rows"][0].update(immutable_fields_md5="0" * 32),
        lambda d: d["after"]["receipts"][0].update(actor_root_match=False),
        lambda d: d["after"]["receipts"][0].update(entry_hash="0" * 64),
        lambda d: d["after"]["receipts"][0].update(evidence_binding_match=False),
        lambda d: d["after"]["normal_audits"].pop(),
        lambda d: d["after"]["normal_audits"][0].update(actor_null=True),
        lambda d: d["after"]["entry_checks"][0].update(review_audit_count=0),
        lambda d: d["after-replay"]["normal_audits"][0].update(audit_id=str(uuid4())),
        lambda d: d["after-replay"]["scope_rows"][0].update(row_md5="0" * 32),
    ],
)
def test_sql_scope_actor_coordinate_hash_and_replay_tamper(mutation):
    captures, outcomes = sql_fixture(fixture())
    mutation(captures)
    with pytest.raises(ValueError):
        V.independent_check(captures, outcomes)


def test_sql_product_hold_full_row_and_browser_false():
    captures, outcomes = sql_fixture(fixture(1, 0))
    assert captures["after"]["receipts"][0]["browser_verified"] == "false"
    for phase in ("after", "after-replay"):
        captures[phase]["scope_rows"][0]["row_md5"] = "0" * 32
    with pytest.raises(ValueError, match="hold full row"):
        V.independent_check(captures, outcomes)


def test_complete_acceptance_binds_files_without_io(monkeypatch):
    data = fixture(3, 2)
    captures, _ = sql_fixture(data)
    public = public_fixture(data)
    files = dict(zip(V.CORE_FILES, data, strict=True))
    files.update({f"independent-{phase}.json": captures[phase] for phase in V.PHASES})
    files.update({f"public-{phase}.json": public[phase] for phase in V.PHASES})
    files["westin-coordinate-evidence.json"] = V.PURE.read_json(
        HERE / "westin-coordinate-evidence.json"
    )

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
    assert report["public"]["option_counts"]["after"] == 218
    assert len(report["input_file_sha256"]) == 14
    assert report["network_calls"] == report["database_connections"] == 0
    files.pop("independent-after-replay.json")
    with pytest.raises(KeyError):
        V.verify(HERE, pinned)


def test_options_only_subset_does_not_publish_any_pending_parent():
    data = fixture(19, 19)
    data[1]["decisions"] = [e for e in data[1]["decisions"] if e["kind"] == "option"]
    for stream in data[2:5]:
        stream[:] = [e for e in stream if not e["target"].endswith(V.WESTIN)]
    for snapshot in data[5:7]:
        row = V.indexed(snapshot)[("product", V.WESTIN)]
        row.clear()
        row.update(copy.deepcopy(ORIGINAL[("product", V.WESTIN)]))
    report = V.rows_check(*data)
    assert report["scope_count"] == report["approved_options"] == 18
    assert report["approved_products"] == 0
    V.independent_check(*sql_fixture(data))
    public = V.public_check(public_fixture(data), data[0], data[5])
    assert public["products"] == 40
    assert public["option_counts"]["after"] == 221


def test_product_guard_hold_with_successful_child_stays_private():
    data = fixture(3, 3)
    row = V.indexed(data[5])[("product", V.WESTIN)]
    row.clear()
    row.update(copy.deepcopy(ORIGINAL[("product", V.WESTIN)]))
    data[3][0].update(outcome="hold", guard_code="service_identity_required")
    rehash(data, V.WESTIN)
    report = V.rows_check(*data)
    assert report["approved"] == 2 and report["approved_products"] == 0
    V.independent_check(*sql_fixture(data))
    public = V.public_check(public_fixture(data), data[0], data[5])
    assert public["products"] == 40
    assert public["option_counts"]["after"] == 213


def test_normal_nonfatal_browser_override_health_is_not_rejected():
    data = fixture()
    V.indexed(data[5])[("option", WESTIN_EXPEDIA)]["health_status"] = "blocked"
    rehash(data, WESTIN_EXPEDIA)
    V.rows_check(*data)
    V.independent_check(*sql_fixture(data))
