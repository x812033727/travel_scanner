"""Pinned, local-only acceptance of the variable platform-source review manifest."""

import argparse
import hashlib
import importlib.util
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

HERE = Path(__file__).resolve().parent
HELPER = HERE.parent / "hotel-review-redirects-20260909/verify_results.py"
HELPER_SHA = "21f56cde81065c3c85ac6582dd6aeeae54bb590383915e55b6db2aaf37ddcc27"
if hashlib.sha256(HELPER.read_bytes()).hexdigest() != HELPER_SHA:
    raise ValueError("Immutable pure helper changed")
SPEC = importlib.util.spec_from_file_location("platform_local_helpers", HELPER)
PURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PURE)
# Only pure primitives/constants are reused, never the previous count-specific checks.
digest, require, unique, indexed, stamp = (
    PURE.digest,
    PURE.require,
    PURE.unique,
    PURE.indexed,
    PURE.stamp,
)
TAG = "hotel-review-platforms-20260909"
BASELINE_HASH = "7b86b02a40dfe00946f1df45d8e201e3dc59bf49066469c30dbfcc60f5628e49"
BASELINE_AT = "2026-09-08 23:37:42.330750+00:00"
DAIWA = "ff023c57-7f7c-460f-9523-a55805fa42e0"
DAIWA_OLD = (
    "https://www.agoda.com/en-us/"
    "daiwa-roynet-hotel-kyoto-terrace-hachijohigashiguchi/hotel/kyoto-jp.html"
)
DAIWA_NEW = (
    "https://www.agoda.com/zh-tw/"
    "daiwa-roynet-hotel-kyoto-terrace-hachijohigashiguchi/hotel/kyoto-jp.html"
)
PHASES = ("before", "after", "after-replay")
PRICES = ("reference_price", "currency", "price_checked_at")
ACTIONS = ("travel_services.hotel_option_edit", "travel_services.hotel_option_review")
PRODUCT_FIELDS = {"id", "kind", "destination_id", "title", "source_url", "source_credits", *PRICES}
OPTION_FIELDS = {"id", "provider", "name", "mode", "quote_status"}
CORE_FILES = (
    "before.json",
    "manifest.json",
    "dry-run.ndjson",
    "apply.ndjson",
    "replay.ndjson",
    "final-snapshot.json",
    "post-replay-snapshot.json",
)


def equal(actual, expected, label):
    require(actual == expected, label)


def fingerprint(value, size=32):
    require(
        isinstance(value, str) and re.fullmatch(f"[0-9a-f]{{{size}}}", value),
        "Malformed evidence fingerprint",
    )


def interval(value, start, end):
    require(stamp(start) <= stamp(value) <= stamp(end), "Evidence timestamp out of order")


def rows_check(before, manifest, dry, applied, replay, final, repeated):
    equal(digest(before), BASELINE_HASH, "Wrong pinned baseline")
    equal(before["captured_at"], BASELINE_AT, "Wrong baseline clock")
    equal(
        {k: v for k, v in manifest.items() if k != "decisions"},
        {"schema_version": 1, "tag": TAG, "baseline_hash": BASELINE_HASH},
        "Manifest provenance mismatch",
    )
    initial, after, again = map(indexed, (before, final, repeated))
    require(
        len(before["products"]) == 60 and len(before["options"]) == 360,
        "Baseline membership differs",
    )
    equal(set(initial), set(after), "Final membership changed")
    equal(after, again, "Replay full rows changed")
    for snap in (final, repeated):
        equal(
            sorted(snap["configs"], key=lambda r: r["id"]),
            sorted(before["configs"], key=lambda r: r["id"]),
            "Configuration changed",
        )
    interval(final["captured_at"], BASELINE_AT, repeated["captured_at"])
    old_approved = {k for k, r in initial.items() if r["status"] == "approved"}
    require(
        len(old_approved) == 319 and sum(k[0] == "product" for k in old_approved) == 40,
        "Original approved inventory differs",
    )
    entries = unique(manifest["decisions"], "id", "manifest")
    require(
        1 <= len(entries) <= 21 and all(e["kind"] == "option" for e in entries.values()),
        "Unauthorized scope size/kind",
    )
    outputs = [
        unique(stream, "target", name)
        for stream, name in ((dry, "dry-run"), (applied, "apply"), (replay, "replay"))
    ]
    targets = {f"{TAG}:option:{i}" for i in entries}
    require(all(set(output) == targets for output in outputs), "Exact stdout coverage differs")
    require(len({r["receipt_id"] for r in applied}) == len(entries), "Duplicate receipt UUID")
    results, approved = [], set()
    for identifier, entry in entries.items():
        old, new = initial[("option", identifier)], after[("option", identifier)]
        parent = initial[("product", old["product_id"])]
        require(
            old["status"] == "pending"
            and old["version"] == 1
            and old["property_id"] is None
            and old["provider"] in {"agoda", "expedia"},
            "Not an authorized pending null-quote option",
        )
        patch = entry.get("option_patch")
        require(
            isinstance(patch, dict)
            and set(patch) == {"url", "evidence_url"}
            and all(
                isinstance(u, str) and u.startswith("https://") and u in entry["source_urls"]
                for u in patch.values()
            ),
            "Unobserved URL patch",
        )
        if identifier == DAIWA:
            require(
                parent["destination_id"] == "kyoto"
                and parent["status"] == "pending"
                and old["provider"] == "agoda"
                and old["url"] == DAIWA_OLD
                and old["evidence_url"] == "https://www.daiwaroynet.jp/en/kyoto-terrace/"
                and patch == {"url": DAIWA_NEW, "evidence_url": DAIWA_NEW},
                "Daiwa correction is not the exact observed locale-only identity",
            )
        else:
            require(
                parent["destination_id"] in {"osaka", "taipei"}
                and parent["status"] == "approved"
                and old["url"] is None
                and old["evidence_url"] is None,
                "Unauthorized existing URL or parent",
            )
        require(
            entry["decision"] == "approve"
            and entry["method"] == "iab"
            and entry["browser_verified"] is True
            and not entry.get("facts_patch")
            and not entry.get("evidence")
            and entry["before_hash"] == digest(old)
            and entry["version"] == old["version"],
            "Manifest authority/hash/version mismatch",
        )
        require(stamp(entry["checked_at"]) > stamp(BASELINE_AT), "Stale IAB evidence")
        name = f"{TAG}:option:{identifier}"
        plan, result, retry = (output[name] for output in outputs)
        equal(
            plan,
            {"target": name, "decision": "approve", "before_hash": digest(old), "mode": "dry-run"},
            "Dry-run contains mutation or differs",
        )
        equal(
            set(result),
            {"target", "outcome", "receipt_id", "after_hash", "guard_code"},
            "Unexpected apply outcome schema",
        )
        equal(str(UUID(result["receipt_id"])), result["receipt_id"], "Invalid receipt UUID")
        equal(result["after_hash"], digest(new), "After-row hash mismatch")
        equal(
            retry,
            {
                "target": name,
                "outcome": "replayed",
                "receipt_id": result["receipt_id"],
                "after_hash": digest(new),
            },
            "Replay receipt/hash differs",
        )
        require(result["outcome"] in {"approved", "hold"}, "Nonterminal result")
        if result["outcome"] == "hold":
            equal(old, new, "Guard hold did not fully roll back")
            require(result["guard_code"] in PURE.KNOWN_GUARDS, "Unknown guard silently held")
        else:
            require(
                result["guard_code"] is None
                and new["status"] == "approved"
                and new["version"] == old["version"] + 2
                and new["property_id"] is None
                and new["discovery_status"] == "found"
                and new["identity_note"] == entry["identity_note"],
                "Normal +2 approval differs",
            )
            equal(set(new), set(old), "Option schema changed")
            require(
                {k for k in old if old[k] != new[k]} <= PURE.NORMAL_FIELDS,
                "Immutable identity/price field changed",
            )
            require(all(new[k] == v for k, v in patch.items()), "Stored URL differs from evidence")
            require(
                isinstance(new["health_status"], str)
                and bool(new["health_status"])
                and new["health_status"] not in {"unsafe", "unavailable"},
                "Fatal link approved",
            )
            for field in ("checked_at", "verified_at", "updated_at"):
                interval(new[field], BASELINE_AT, final["captured_at"])
            approved.add(identifier)
        results.append(
            {
                **result,
                "id": identifier,
                "product_id": old["product_id"],
                "parent_status": parent["status"],
                "destination_id": parent["destination_id"],
                "checked_at": entry["checked_at"],
                "provider": old["provider"],
                "before_url": old["url"],
                "before_evidence_url": old["evidence_url"],
                "before_version": old["version"],
                "after_version": new["version"],
                "entry_hash": digest(entry),
                "before_hash": digest(old),
                "requested_decision": "approve",
            }
        )
    for key, row in initial.items():
        if key[0] != "option" or key[1] not in approved:
            equal(row, after[key], f"Untouched or original approved row changed: {key}")
    return {
        "scope_count": len(entries),
        "approved": len(approved),
        "holds": len(entries) - len(approved),
        "original_319_approved_unchanged": True,
        "all_60_products_unchanged": True,
        "untouched_rows": 420 - len(approved),
        "full_replay_420_rows_unchanged": True,
        "approved_ids": sorted(approved),
        "outcomes": sorted(results, key=lambda r: r["id"]),
    }


def public_check(captures, before, final):
    baseline, current = map(indexed, (before, final))
    phase_items, phase_hashes, public_counts = {}, {}, {}
    for phase in PHASES:
        report, snapshot = captures[phase], baseline if phase == "before" else current
        require(
            report["tag"] == TAG
            and report["phase"] == phase
            and report["baseline_hash"] == BASELINE_HASH
            and report["method"] == "anonymous_public_GET_only",
            "Public provenance differs",
        )
        require(
            report["credentials_sent"] is False and report["cookies_sent"] is False,
            "Public authentication unexpectedly used",
        )
        require(
            all(
                report[k] == 0
                for k in (
                    "redirects_followed",
                    "quote_calls",
                    "clickout_calls",
                    "mutating_api_calls",
                    "database_connections",
                )
            ),
            "Public scope exceeded",
        )
        interval(report["started_at"], BASELINE_AT, report["completed_at"])
        products = {
            i: p
            for (kind, i), p in snapshot.items()
            if kind == "product" and p["status"] == "approved"
        }
        options = {
            i: o
            for (kind, i), o in snapshot.items()
            if kind == "option" and o["status"] == "approved" and o["product_id"] in products
        }
        require(
            len(products) == 40 and (phase != "before" or len(options) == 192),
            "Public baseline inventory differs",
        )
        expected_summary = {
            "all_checks_pass": True,
            "http_200": 30,
            "no_store_responses": 30,
            "unique_public_products": 40,
            "unique_public_booking_options": len(options),
        }
        equal(report["summary"], expected_summary, "Public summary differs")
        pairs = {}
        for response in report["responses"]:
            pair = (response["city"], response["locale"])
            require(
                pair not in pairs and pair[0] in PURE.CITIES and pair[1] in PURE.LOCALES,
                "Public matrix duplicated/unknown",
            )
            require(
                response["http_status"] == 200
                and not response["issues"]
                and "no-store" in (response["cache_control"] or "").lower(),
                "Public HTTP/cache",
            )
            interval(response["started_at"], report["started_at"], response["completed_at"])
            interval(response["completed_at"], response["started_at"], report["completed_at"])
            items = unique(response["items"], "id", "public item")
            expected_products = {i for i, p in products.items() if p["destination_id"] == pair[0]}
            equal(set(items), expected_products, "Public products missing or leaked")
            equal(response["item_ids"], sorted(items), "Public product IDs differ from body")
            equal(
                response["body_hash"], digest(response["items"]), "Public body fingerprint differs"
            )
            seen_options = set()
            for identifier, item in items.items():
                product = products[identifier]
                equal(
                    set(item), PRODUCT_FIELDS | {"booking_options"}, "Public item allowlist differs"
                )
                require(
                    item["kind"] == "hotel"
                    and item["destination_id"] == pair[0]
                    and isinstance(item["title"], str)
                    and bool(item["title"])
                    and item["source_url"] == product["source_url"]
                    and item["source_credits"] == product["facts"]["source_credits"]
                    and all(item[k] is None for k in PRICES),
                    "Public title/credit/price differs",
                )
                shown = unique(item["booking_options"], "id", "public option")
                equal(
                    set(shown),
                    {i for i, o in options.items() if o["product_id"] == identifier},
                    "Public booking option membership/parent differs",
                )
                for oid, option in shown.items():
                    equal(set(option), OPTION_FIELDS, "Public option allowlist differs")
                    equal(option["provider"], options[oid]["provider"], "Public provider differs")
                    if baseline[("option", oid)]["status"] != "approved":
                        equal(
                            option,
                            {
                                "id": oid,
                                "provider": options[oid]["provider"],
                                "name": {"agoda": "Agoda", "expedia": "Expedia"}[
                                    options[oid]["provider"]
                                ],
                                "mode": "direct",
                                "quote_status": "not_configured",
                            },
                            "New null-property option unexpectedly enables quote/affiliate",
                        )
                seen_options.update(shown)
            equal(response["booking_option_ids"], sorted(seen_options), "Public option IDs differ")
            pairs[pair] = items
        equal(
            set(pairs),
            {(c, loc) for c in PURE.CITIES for loc in PURE.LOCALES},
            "Public 30-request matrix incomplete",
        )
        phase_items[phase], public_counts[phase] = pairs, len(options)
        phase_hashes[phase] = {
            (r["city"], r["locale"]): r["body_hash"] for r in report["responses"]
        }
    for phase in PHASES[1:]:
        for pair, originals in phase_items["before"].items():
            for identifier, old in originals.items():
                new = phase_items[phase][pair][identifier]
                equal(
                    {k: v for k, v in old.items() if k != "booking_options"},
                    {k: v for k, v in new.items() if k != "booking_options"},
                    "Old public fields drifted",
                )
                old_options = unique(old["booking_options"], "id", "old public option")
                new_options = unique(new["booking_options"], "id", "new public option")
                require(
                    all(new_options.get(i) == o for i, o in old_options.items()),
                    "Existing public option changed",
                )
    equal(phase_items["after"], phase_items["after-replay"], "Public replay body changed")
    equal(phase_hashes["after"], phase_hashes["after-replay"], "Public replay fingerprint changed")
    for previous, later in zip(PHASES, PHASES[1:], strict=False):
        require(
            stamp(captures[previous]["completed_at"]) <= stamp(captures[later]["started_at"]),
            "Public phases unordered",
        )
    return {
        "requests": 90,
        "products": 40,
        "option_counts": public_counts,
        "existing_192_options_and_all_public_fields_unchanged": True,
        "new_options_exactly_successful_with_approved_parent": True,
        "replay_body_unchanged": True,
    }


def independent_check(captures, outcomes):
    results = unique(outcomes["outcomes"], "id", "expected SQL outcome")
    scope, approved = set(results), set(outcomes["approved_ids"])
    count = len(scope)
    specs = {
        "all_hotel_products": 60,
        "non_scope_hotel_options": 360 - count,
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
    phases = {}
    for phase in PHASES:
        report = captures[phase]
        require(
            report["schema_version"] == 1
            and report["tag"] == TAG
            and report["phase"] == phase
            and report["baseline_hash"] == BASELINE_HASH
            and stamp(report["baseline_at"]) == stamp(BASELINE_AT)
            and report["completed_with"] == "ROLLBACK",
            "SQL provenance/completion differs",
        )
        snapshot = report["snapshot"]
        require(
            snapshot["isolation_level"] == "repeatable read"
            and snapshot["read_only"] == "on"
            and snapshot["matching_roots"] == snapshot["review_pending_roots"] == 1
            and snapshot["active_actors"] == 1
            and snapshot["authenticated_request_audits"] >= 1
            and stamp(snapshot["captured_at"]) >= stamp(BASELINE_AT),
            "SQL authority/isolation",
        )
        active = set() if phase == "before" else approved
        receipts_expected = 0 if phase == "before" else count
        hold_count = 0 if phase == "before" else count - len(active)
        equal(
            report["expected"],
            {
                "scope_count": count,
                "receipts": receipts_expected,
                "approved": len(active),
                "edits": len(active),
                "holds": hold_count,
            },
            "SQL expected counts",
        )
        equal(
            report["inventory"],
            {
                "hotel_products": 60,
                "hotel_options": 360,
                "approved_products": 40,
                "approved_options": 279 + len(active),
            },
            "SQL inventory",
        )
        groups = unique(report["protected_groups"], "name", "SQL protected group")
        equal(set(groups), set(specs), "SQL protected groups incomplete")
        for name, expected_count in specs.items():
            group = groups[name]
            require(
                group["expected_count"] == expected_count
                and group["count_matches"] is (None if expected_count is None else True)
                and type(group["count"]) is int
                and group["count"] >= 0
                and (expected_count is None or group["count"] == expected_count),
                "SQL group count",
            )
            fingerprint(group["rows_md5"])
        scope_rows = unique(report["scope_rows"], "id", "SQL scope row")
        equal(set(scope_rows), scope, "SQL scope differs")
        for identifier, row in scope_rows.items():
            original, success = results[identifier], identifier in active
            expected_fields = {
                "parent_id": original["product_id"],
                "parent_match": True,
                "provider_match": True,
                "provider": original["provider"],
                "baseline_provider": original["provider"],
                "parent_status": original["parent_status"],
                "parent_destination_id": original["destination_id"],
                "before_version": 1,
                "version": 3 if success else 1,
                "status": "approved" if success else "pending",
                "property_id_null": True,
                "before_url_null": original["before_url"] is None,
                "before_evidence_url_null": original["before_evidence_url"] is None,
                "url_null": not success and original["before_url"] is None,
                "evidence_url_null": not success and original["before_evidence_url"] is None,
                "before_url_matches_baseline": not success,
                "before_evidence_url_matches_baseline": not success,
                "url_matches_manifest": success,
                "evidence_url_matches_manifest": success,
            }
            equal({k: row[k] for k in expected_fields}, expected_fields, "SQL exact row transition")
            fingerprint(row["row_md5"])
        receipts = unique(report["receipts"], "target_id", "SQL receipt")
        equal(set(receipts), set() if phase == "before" else scope, "SQL receipt scope")
        receipt_ids = set()
        for identifier, receipt in receipts.items():
            result = results[identifier]
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
            equal(
                {k: receipt[k] for k in fields},
                {k: result[k] for k in fields},
                "SQL receipt binding",
            )
            require(
                receipt["kind"] == "option"
                and receipt["browser_verified"] == "true"
                and receipt["actor_root_match"] is True
                and receipt["actor_null"] is False
                and all(
                    receipt[k] is True
                    for k in (
                        "provenance_match",
                        "scope_match",
                        "entry_hash_match",
                        "before_hash_match",
                        "option_patch_match",
                        "after_hash_valid",
                    )
                ),
                "SQL receipt actor/hash/patch",
            )
            interval(receipt["created_at"], result["checked_at"], snapshot["captured_at"])
            fingerprint(receipt["row_md5"])
            require(receipt["receipt_id"] not in receipt_ids, "Duplicate SQL receipt ID")
            receipt_ids.add(receipt["receipt_id"])
        receipts_md5 = hashlib.md5(
            "".join(
                r["row_md5"] for r in sorted(receipts.values(), key=lambda r: r["receipt_id"])
            ).encode(),
            usedforsecurity=False,
        ).hexdigest()
        equal(
            report["receipt_totals"],
            {
                "count": receipts_expected,
                "distinct_targets": receipts_expected,
                "approved": len(active),
                "holds": hold_count,
                "rows_md5": receipts_md5,
            },
            "SQL receipt totals/full fingerprint",
        )
        audits = unique(report["normal_audits"], "audit_id", "normal SQL audit")
        expected_pairs = Counter((i, action) for i in active for action in ACTIONS)
        equal(
            Counter((a["target"], a["action"]) for a in audits.values()),
            expected_pairs,
            "SQL unexpected/missing normal edit or review",
        )
        for identifier, audit in audits.items():
            require(
                str(UUID(identifier)) == identifier
                and identifier not in receipt_ids
                and audit["in_scope"] is True
                and audit["actor_root_match"] is True
                and audit["actor_null"] is False,
                "SQL normal audit actor/target",
            )
            interval(
                audit["created_at"],
                captures["before"]["snapshot"]["captured_at"],
                snapshot["captured_at"],
            )
            fingerprint(audit["row_md5"])
        for identifier in active:
            events = {a["action"]: a for a in audits.values() if a["target"] == identifier}
            interval(
                events[ACTIONS[1]]["created_at"],
                events[ACTIONS[0]]["created_at"],
                receipts[identifier]["created_at"],
            )
        checks = unique(report["entry_checks"], "id", "SQL entry check")
        equal(set(checks), scope, "SQL entry check scope")
        for identifier, check in checks.items():
            equal(
                check,
                {
                    "id": identifier,
                    "receipt_count": int(phase != "before"),
                    "edit_audit_count": int(identifier in active),
                    "review_audit_count": int(identifier in active),
                    "outcome": None if phase == "before" else results[identifier]["outcome"],
                    "row_transition_valid": True,
                },
                "SQL entry service guard check",
            )
        phases[phase] = {
            "groups": groups,
            "scope": scope_rows,
            "receipts": receipts,
            "audits": audits,
            "checks": checks,
            "totals": report["receipt_totals"],
        }
    for phase in PHASES[1:]:
        equal(
            phases[phase]["groups"], phases["before"]["groups"], "Protected SQL full rows changed"
        )
        equal(
            {k: v for k, v in captures[phase]["snapshot"].items() if k != "captured_at"},
            {k: v for k, v in captures["before"]["snapshot"].items() if k != "captured_at"},
            "SQL authorization snapshot changed",
        )
        for identifier in scope - approved:
            equal(
                phases[phase]["scope"][identifier],
                phases["before"]["scope"][identifier],
                "SQL hold full row changed",
            )
    equal(phases["after"], phases["after-replay"], "Replay changed SQL receipts/audits/full rows")
    interval(
        captures["after"]["snapshot"]["captured_at"],
        captures["before"]["snapshot"]["captured_at"],
        captures["after-replay"]["snapshot"]["captured_at"],
    )
    return {
        "receipts": count,
        "normal_edits": len(approved),
        "normal_reviews": len(approved),
        "protected_groups_unchanged": len(specs),
        "original_387_receipts_unchanged": True,
        "all_normal_audits_authenticated_root": True,
        "hold_rows_fully_rolled_back": True,
        "replay_zero_extra_receipts_or_audits": True,
    }


def verify(directory, expected_manifest_sha256):
    fingerprint(expected_manifest_sha256, 64)
    manifest_path = directory / "manifest.json"
    equal(
        hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        expected_manifest_sha256,
        "Pinned manifest file SHA256 differs",
    )
    filenames = (
        *CORE_FILES,
        *(f"{p}-{phase}.json" for p in ("independent", "public") for phase in PHASES),
    )
    data = {
        name: (PURE.read_ndjson if name.endswith(".ndjson") else PURE.read_json)(directory / name)
        for name in filenames
    }
    rows = rows_check(*(data[name] for name in CORE_FILES))
    sql = independent_check({p: data[f"independent-{p}.json"] for p in PHASES}, rows)
    public = public_check(
        {p: data[f"public-{p}.json"] for p in PHASES},
        data["before.json"],
        data["final-snapshot.json"],
    )
    return {
        "schema_version": 1,
        "tag": TAG,
        "status": "passed",
        "final_acceptance": True,
        "verified_at": datetime.now(UTC).isoformat(),
        "network_calls": 0,
        "database_connections": 0,
        "baseline_hash": BASELINE_HASH,
        "manifest_file_sha256": expected_manifest_sha256,
        "rows": rows,
        "independent": sql,
        "public": public,
        "input_file_sha256": {
            name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in filenames
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=HERE)
    parser.add_argument("--manifest-sha256", required=True, help="Independently pinned FILE SHA256")
    parser.add_argument(
        "--require-complete", action="store_true", help="Always required; compatibility"
    )
    parser.add_argument("--output", type=Path, help="Exclusive-create report after all checks pass")
    args = parser.parse_args()
    try:
        require(not args.output or not args.output.exists(), "Report output already exists")
        report = verify(args.directory, args.manifest_sha256)
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                json.dump(report, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
        print(json.dumps(report, ensure_ascii=True))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(
            json.dumps(
                {
                    "status": "failed",
                    "final_acceptance": False,
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                }
            )
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
