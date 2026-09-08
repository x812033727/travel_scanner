"""Synthetic offline verifier acceptance/rejection; no API, SQL or HTTP calls."""

import copy
import hashlib
import importlib.util
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

import pytest

DIRECTORY = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "redirect_verifier", DIRECTORY / "verify_results.py"
)
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)
BASELINE = verify.read_json(DIRECTORY / "before.json")


def fixture(approved=3):
    before = copy.deepcopy(BASELINE)
    final = copy.deepcopy(before)
    baseline_time = verify.stamp(before["captured_at"])
    now = (baseline_time + timedelta(minutes=2)).isoformat()
    final["captured_at"] = (baseline_time + timedelta(minutes=3)).isoformat()
    options = {row["id"]: row for row in final["options"]}
    original = {row["id"]: row for row in before["options"]}
    manifest = {
        "schema_version": 1,
        "tag": verify.TAG,
        "baseline_hash": verify.BASELINE_HASH,
        "decisions": [],
    }
    dry_run, apply, replay = [], [], []
    for index, identifier in enumerate(sorted(verify.SCOPE)):
        old, new = original[identifier], options[identifier]
        url = verify.TARGET_URLS[identifier]
        entry = {
            "kind": "option",
            "id": identifier,
            "version": old["version"],
            "before_hash": verify.digest(old),
            "decision": "approve",
            "reason": "Synthetic offline same-hotel identity fixture; not production evidence.",
            "new_evidence": "Synthetic fixture only, never authorizes actual review.",
            "source_urls": [url],
            "method": "iab",
            "checked_at": now,
            "browser_verified": True,
            "identity_note": "Offline same-hotel name and address fixture.",
            "option_patch": {"url": url, "evidence_url": url},
        }
        manifest["decisions"].append(entry)
        success = index < approved
        if success:
            new.update(entry["option_patch"])
            new.update(
                status="approved",
                discovery_status="found",
                version=old["version"] + 2,
                identity_note=entry["identity_note"],
                health_status="unconfirmed",
                checked_at=now,
                verified_at=now,
                updated_at=now,
            )
        result = {
            "target": verify.target(entry),
            "outcome": "approved" if success else "hold",
            "receipt_id": str(uuid4()),
            "after_hash": verify.digest(new),
            "guard_code": None if success else "service_link_unavailable",
        }
        apply.append(result)
        replay.append(
            {k: result[k] for k in ("target", "receipt_id", "after_hash")}
            | {"outcome": "replayed"}
        )
        dry_run.append(
            {
                "target": verify.target(entry),
                "decision": "approve",
                "before_hash": entry["before_hash"],
                "mode": "dry-run",
            }
        )
    repeated = copy.deepcopy(final)
    repeated["captured_at"] = (baseline_time + timedelta(minutes=4)).isoformat()
    return [before, manifest, dry_run, apply, replay, final, repeated]


@pytest.mark.parametrize("approved", range(4))
def test_actual_success_and_known_guard_rollback_counts(approved):
    report = verify.verify_rows(*fixture(approved))
    assert len(report["approved_option_ids"]) == approved
    assert report["untouched_rows"] == 420 - approved
    assert (
        report["expected_normal_audit_additions"]["travel_services.hotel_option_edit"]
        == approved
    )
    assert (
        report["expected_normal_audit_additions"]["travel_services.hotel_option_review"]
        == approved
    )
    assert report["original_316_approved_unchanged"]


@pytest.mark.parametrize("position", (2, 3, 4))
def test_missing_or_duplicate_stdout_rows_rejected(position):
    data = fixture()
    data[position].append(copy.deepcopy(data[position][0]))
    with pytest.raises(ValueError, match="Duplicate"):
        verify.verify_rows(*data)
    data = fixture()
    data[position].pop()
    with pytest.raises(ValueError, match="coverage"):
        verify.verify_rows(*data)


@pytest.mark.parametrize("collection", ("products", "options", "configs"))
def test_unrelated_and_original_approved_full_rows_immutable(collection):
    data = fixture()
    row = next(r for r in data[5][collection] if r["id"] not in verify.SCOPE)
    row["updated_at"] = "2026-09-08T23:11:00+00:00"
    data[6][collection] = copy.deepcopy(data[5][collection])
    with pytest.raises(ValueError):
        verify.verify_rows(*data)


@pytest.mark.parametrize(
    "field,value",
    [
        ("property_id", "would-enable-quotes"),
        ("provider", "booking"),
        ("product_id", "4938181e-0007-4143-aa0c-4b5ed44f4f8b"),
        ("version", 2),
        ("url", "https://www.agoda.com/other/hotel/busan-kr.html"),
        ("health_status", "unsafe"),
        ("health_status", "unavailable"),
    ],
)
def test_approved_mutations_fail_even_when_receipt_hash_is_recomputed(field, value):
    data = fixture()
    identifier = min(verify.SCOPE)
    row = next(r for r in data[5]["options"] if r["id"] == identifier)
    row[field] = value
    data[6]["options"] = copy.deepcopy(data[5]["options"])
    for output in (data[3], data[4]):
        next(r for r in output if r["target"].endswith(identifier))["after_hash"] = (
            verify.digest(row)
        )
    with pytest.raises(ValueError):
        verify.verify_rows(*data)


def test_browser_override_matches_normal_nonfatal_guard():
    data = fixture()
    identifier = min(verify.SCOPE)
    row = next(r for r in data[5]["options"] if r["id"] == identifier)
    row["health_status"] = "blocked"
    data[6]["options"] = copy.deepcopy(data[5]["options"])
    for output in (data[3], data[4]):
        next(r for r in output if r["target"].endswith(identifier))["after_hash"] = (
            verify.digest(row)
        )
    verify.verify_rows(*data)


def test_failed_review_cannot_leave_new_url_or_convert_conflict_to_hold():
    data = fixture(0)
    data[3][0]["guard_code"] = "service_version_conflict"
    with pytest.raises(ValueError, match="Unknown failure"):
        verify.verify_rows(*data)
    data = fixture(0)
    identifier = min(verify.SCOPE)
    row = next(r for r in data[5]["options"] if r["id"] == identifier)
    row["url"] = data[1]["decisions"][0]["option_patch"]["url"]
    data[6]["options"] = copy.deepcopy(data[5]["options"])
    for output in (data[3], data[4]):
        output[0]["after_hash"] = verify.digest(row)
    with pytest.raises(ValueError, match="rolled back"):
        verify.verify_rows(*data)


def test_exact_scope_and_fresh_baseline_guard():
    data = fixture()
    data[1]["decisions"][0]["id"] = str(uuid4())
    with pytest.raises(ValueError, match="exactly"):
        verify.verify_rows(*data)
    data = fixture()
    data[1]["decisions"][0]["checked_at"] = data[0]["captured_at"]
    with pytest.raises(ValueError, match="predates"):
        verify.verify_rows(*data)


def test_replay_receipt_and_final_snapshot_must_be_identical():
    data = fixture()
    data[4][0]["receipt_id"] = str(uuid4())
    with pytest.raises(ValueError, match="Replay"):
        verify.verify_rows(*data)
    data = fixture()
    data[6]["options"][0]["version"] += 1
    with pytest.raises(ValueError, match="Post-replay"):
        verify.verify_rows(*data)


def public_fixture():
    products = {r["id"]: r for r in BASELINE["products"] if r["status"] == "approved"}
    options = {
        r["id"]: r
        for r in BASELINE["options"]
        if r["status"] == "approved" and r["product_id"] in products
    }
    result = {}
    for phase_index, phase in enumerate(("before", "after", "after-replay")):
        now = (
            verify.stamp(verify.BASELINE_CAPTURED_AT)
            + timedelta(minutes=phase_index + 1)
        ).isoformat()
        responses = []
        for city in sorted(verify.CITIES):
            item_ids = sorted(
                i for i, r in products.items() if r["destination_id"] == city
            )
            option_ids = sorted(
                i for i, r in options.items() if r["product_id"] in item_ids
            )
            for locale in sorted(verify.LOCALES):
                responses.append(
                    {
                        "city": city,
                        "locale": locale,
                        "http_status": 200,
                        "started_at": now,
                        "completed_at": now,
                        "cache_control": "no-store",
                        "issues": [],
                        "item_ids": item_ids,
                        "booking_option_ids": option_ids,
                        "body_hash": verify.digest(
                            [city, locale, item_ids, option_ids]
                        ),
                    }
                )
        result[phase] = {
            "tag": verify.TAG,
            "phase": phase,
            "baseline_hash": verify.BASELINE_HASH,
            "started_at": now,
            "completed_at": now,
            "method": "anonymous_public_GET_only",
            "credentials_sent": False,
            "cookies_sent": False,
            "redirects_followed": 0,
            "quote_calls": 0,
            "clickout_calls": 0,
            "mutating_api_calls": 0,
            "database_connections": 0,
            "responses": responses,
            "summary": {
                "all_checks_pass": True,
                "http_200": 30,
                "no_store_responses": 30,
                "unique_public_products": 40,
                "unique_public_booking_options": 192,
            },
        }
    return result


def test_public_three_phase_body_fingerprints_and_memberships():
    report = verify.verify_public(public_fixture(), BASELINE)
    assert report["public_options"] == 192


@pytest.mark.parametrize(
    "mutation",
    [
        lambda d: d["after"]["responses"].pop(),
        lambda d: d["after"]["responses"][0].update(cache_control="public, max-age=60"),
        lambda d: d["after"]["responses"][0]["booking_option_ids"].append(
            min(verify.SCOPE)
        ),
        lambda d: d["after-replay"]["responses"][0].update(body_hash="0" * 64),
        lambda d: d["after"].update(quote_calls=1),
    ],
)
def test_public_leak_or_body_drift_rejected(mutation):
    data = public_fixture()
    mutation(data)
    with pytest.raises(ValueError):
        verify.verify_public(data, BASELINE)


def sql_fixture(approved=3):
    row_report = verify.verify_rows(*fixture(approved))
    results = row_report["outcomes"]
    approvals = set(row_report["approved_option_ids"])
    result = {}
    baseline_time = verify.stamp(verify.BASELINE_CAPTURED_AT)
    event_at = (baseline_time + timedelta(minutes=2)).isoformat()
    for phase_index, phase in enumerate(("before", "after", "after-replay")):
        actual = 0 if phase == "before" else approved
        count = 0 if phase == "before" else 3
        holds = 0 if phase == "before" else 3 - actual
        scope, receipts, audits, checks = [], [], [], []
        for index, outcome in enumerate(results):
            identifier = outcome["id"]
            success = phase != "before" and identifier in approvals
            scope.append(
                {
                    "id": identifier,
                    "parent_id": outcome["product_id"],
                    "provider": "agoda",
                    "status": "approved" if success else "pending",
                    "version": 3 if success else 1,
                    "row_md5": verify.digest([identifier, success])[:32],
                    "property_id_null": True,
                    "url_null": not success,
                    "evidence_url_null": not success,
                    "parent_match": True,
                    "parent_status": "pending",
                    "parent_destination_id": "busan",
                    "url_matches_manifest": success,
                    "evidence_url_matches_manifest": success,
                }
            )
            if phase != "before":
                receipts.append(
                    {
                        **{
                            k: outcome[k]
                            for k in (
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
                        },
                        "target_id": identifier,
                        "kind": "option",
                        "created_at": event_at,
                        "row_md5": verify.digest([identifier, "receipt"])[:32],
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
                    }
                )
            if success:
                for action_index, action in enumerate(("edit", "review")):
                    audits.append(
                        {
                            "audit_id": f"11111111-1111-4111-8111-{index * 2 + action_index:012d}",
                            "action": f"travel_services.hotel_option_{action}",
                            "target": identifier,
                            "created_at": event_at,
                            "row_md5": verify.digest([identifier, action])[:32],
                            "in_scope": True,
                            "actor_root_match": True,
                            "actor_null": False,
                        }
                    )
            checks.append(
                {
                    "id": identifier,
                    "receipt_count": 0 if phase == "before" else 1,
                    "edit_audit_count": int(success),
                    "review_audit_count": int(success),
                    "outcome": None if phase == "before" else outcome["outcome"],
                    "row_transition_valid": True,
                }
            )
        fingerprint = hashlib.md5(
            "".join(
                r["row_md5"] for r in sorted(receipts, key=lambda r: r["receipt_id"])
            ).encode(),
            usedforsecurity=False,
        ).hexdigest()
        result[phase] = {
            "schema_version": 1,
            "tag": verify.TAG,
            "phase": phase,
            "baseline_hash": verify.BASELINE_HASH,
            "baseline_at": verify.BASELINE_CAPTURED_AT,
            "completed_with": "ROLLBACK",
            "expected": {
                "scope_count": 3,
                "receipts": count,
                "approved": actual,
                "edits": actual,
                "holds": holds,
            },
            "snapshot": {
                "captured_at": (
                    baseline_time + timedelta(minutes=phase_index * 2 + 1)
                ).isoformat(),
                "isolation_level": "repeatable read",
                "read_only": "on",
                "matching_roots": 1,
                "review_pending_roots": 1,
                "active_actors": 1,
                "authenticated_request_audits": 1,
            },
            "inventory": {
                "hotel_products": 60,
                "hotel_options": 360,
                "approved_products": 40,
                "approved_options": 276 + actual,
            },
            "protected_groups": [
                {
                    "name": name,
                    "count": expected if expected is not None else 1,
                    "expected_count": expected,
                    "count_matches": None if expected is None else True,
                    "rows_md5": verify.digest(name)[:32],
                }
                for name, expected in verify.PROTECTED_GROUPS.items()
            ],
            "scope_rows": scope,
            "receipts": receipts,
            "normal_audits": audits,
            "entry_checks": checks,
            "receipt_totals": {
                "count": count,
                "distinct_targets": count,
                "approved": actual,
                "holds": holds,
                "rows_md5": fingerprint,
            },
        }
    return result, row_report


@pytest.mark.parametrize("approved", range(4))
def test_sql_dynamic_outcomes_and_zero_replay_additions(approved):
    report = verify.verify_independent(*sql_fixture(approved))
    assert report["normal_reviews"] == approved
    assert report["receipt_count"] == 3
    assert report["replay_same_receipts_and_zero_added_audits"]


@pytest.mark.parametrize(
    "mutation",
    [
        lambda d: d["before"].update(completed_with="COMMIT"),
        lambda d: d["after"].update(baseline_hash="0" * 64),
        lambda d: d["after"]["snapshot"].update(read_only="off"),
        lambda d: d["after"]["snapshot"].update(active_actors=0),
        lambda d: d["before"]["expected"].update(approved=3),
        lambda d: d["after"]["inventory"].update(approved_products=41),
        lambda d: d["after"]["protected_groups"].pop(),
        lambda d: d["after"]["protected_groups"][0].update(rows_md5="0" * 32),
        lambda d: d["after"]["scope_rows"][0].update(parent_status="approved"),
        lambda d: d["after"]["scope_rows"][0].update(property_id_null=False),
        lambda d: d["after"]["scope_rows"][0].update(version=2),
        lambda d: d["after"]["receipts"][0].update(actor_root_match=False),
        lambda d: d["after"]["receipts"][0].update(actor_null=True),
        lambda d: d["after"]["receipts"][0].update(entry_hash="0" * 64),
        lambda d: d["after"]["receipts"][0].update(option_patch_match=False),
        lambda d: d["after"]["receipt_totals"].update(rows_md5="0" * 32),
        lambda d: d["after"]["receipts"].append(
            copy.deepcopy(d["after"]["receipts"][0])
        ),
        lambda d: d["after"]["normal_audits"].pop(),
        lambda d: d["after"]["normal_audits"][0].update(in_scope=False),
        lambda d: d["after"]["normal_audits"][0].update(actor_root_match=False),
        lambda d: d["after"]["normal_audits"][0].update(
            action="travel_services.product_review"
        ),
        lambda d: d["after"]["entry_checks"][0].update(edit_audit_count=0),
        lambda d: d["after-replay"]["normal_audits"][0].update(audit_id=str(uuid4())),
        lambda d: d["after-replay"]["scope_rows"][0].update(row_md5="0" * 32),
    ],
)
def test_sql_actor_scope_hash_transition_and_replay_drift_rejected(mutation):
    data, row_report = sql_fixture()
    mutation(data)
    with pytest.raises(ValueError):
        verify.verify_independent(data, row_report)


def test_sql_hold_full_row_md5_catches_unlisted_metadata_drift():
    data, row_report = sql_fixture(0)
    for phase in ("after", "after-replay"):
        data[phase]["scope_rows"][0]["row_md5"] = "0" * 32
    with pytest.raises(ValueError, match="hold row changed"):
        verify.verify_independent(data, row_report)


def test_sql_receipt_full_row_replay_drift_rejected_even_when_total_recomputed():
    data, row_report = sql_fixture()
    data["after-replay"]["receipts"][0]["row_md5"] = "0" * 32
    data["after-replay"]["receipt_totals"]["rows_md5"] = hashlib.md5(
        "".join(
            r["row_md5"]
            for r in sorted(
                data["after-replay"]["receipts"], key=lambda r: r["receipt_id"]
            )
        ).encode(),
        usedforsecurity=False,
    ).hexdigest()
    with pytest.raises(ValueError, match="Replay changed"):
        verify.verify_independent(data, row_report)
