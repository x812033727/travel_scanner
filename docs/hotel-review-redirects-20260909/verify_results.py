"""Local-only acceptance of three redirected Agoda identity reviews.

Reads retained JSON/NDJSON evidence, never imports the API or contacts a service.
Default output is JSON on stdout. --output exclusively creates a new report.
Missing independent/public evidence is partial; --require-complete fails closed.
"""

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

TAG = "hotel-review-redirects-20260909"
BASELINE_HASH = "14978ec20e1b05f7f5991194c9568f56bb6da93486c91105ebc5391dc4fad56d"
BASELINE_CAPTURED_AT = "2026-09-08 23:08:17.381350+00:00"
SCOPE = {
    "00307d02-975e-4b2f-8843-df7000cd7c50",
    "2c41cd84-0813-42cf-8a54-003bc6f0cff4",
    "d55df51d-b401-468a-8149-bec50508b4c2",
}
TARGET_URLS = {
    "00307d02-975e-4b2f-8843-df7000cd7c50": "https://www.agoda.com/zh-tw/shilla-stay-haeundae/hotel/busan-kr.html",
    "2c41cd84-0813-42cf-8a54-003bc6f0cff4": "https://www.agoda.com/zh-tw/paradise-hotel-busan/hotel/busan-kr.html",
    "d55df51d-b401-468a-8149-bec50508b4c2": "https://www.agoda.com/zh-tw/toyoko-inn-busan-seomyeon_4/hotel/busan-kr.html",
}
PROTECTED_GROUPS = {
    "all_hotel_products": 60,
    "non_scope_hotel_options": 357,
    "baseline_approved": 316,
    "travel_service_config": None,
    "provider_configs_full": None,
    "provider_configs_stable": None,
    "brands_all": None,
    "hotel_offers": 0,
    "destination_hotel_offers": 0,
    "hotel_booking_clicks_all": 0,
    "affiliate_clicks_hotel": 0,
    "all_historical_audits": None,
    "old_hotel_receipts_384": 384,
}
NORMAL_FIELDS = {
    "url",
    "evidence_url",
    "discovery_status",
    "identity_note",
    "status",
    "version",
    "verified_at",
    "checked_at",
    "health_status",
    "updated_at",
}
KNOWN_GUARDS = {
    "service_identity_required",
    "service_source_required",
    "service_destination_mismatch",
    "service_area_required",
    "service_link_unavailable",
    "service_offer_mismatch",
}
CITIES = {"tokyo", "osaka", "kyoto", "seoul", "busan", "taipei"}
LOCALES = {"en", "ja", "ko", "zh-TW", "zh-CN"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_ndjson(path):
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def unique(rows, key, label):
    result = {}
    for row in rows:
        require(isinstance(row, dict), f"Invalid {label} row")
        value = row[key]
        require(value not in result, f"Duplicate {label}: {value}")
        result[value] = row
    return result


def indexed(snapshot):
    return {
        (kind, key): row
        for kind, collection in (("product", "products"), ("option", "options"))
        for key, row in unique(snapshot[collection], "id", collection).items()
    }


def stamp(value):
    require(isinstance(value, str), "Evidence timestamp is not text")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Evidence timestamp lacks timezone")
    return parsed


def target(entry):
    return f"{TAG}:{entry['kind']}:{entry['id']}"


def verify_rows(before, manifest, dry_run, apply, replay, final, post_replay):
    require(
        digest(before) == BASELINE_HASH
        and before["captured_at"] == BASELINE_CAPTURED_AT,
        "Wrong pinned baseline",
    )
    require(
        set(manifest) == {"schema_version", "tag", "baseline_hash", "decisions"}
        and manifest["schema_version"] == 1
        and manifest["tag"] == TAG
        and manifest["baseline_hash"] == BASELINE_HASH,
        "Manifest provenance/schema mismatch",
    )
    initial, after, repeated = map(indexed, (before, final, post_replay))
    require(
        len(before["products"]) == 60 and len(before["options"]) == 360,
        "Wrong baseline catalog size",
    )
    require(
        set(initial) == set(after) == set(repeated) and len(initial) == 420,
        "Catalog membership changed",
    )
    require(after == repeated, "Post-replay full rows changed")
    for snapshot in (final, post_replay):
        require(
            digest(sorted(snapshot["configs"], key=lambda r: r["id"]))
            == digest(sorted(before["configs"], key=lambda r: r["id"])),
            "Configuration full rows changed",
        )
    require(
        stamp(before["captured_at"])
        <= stamp(final["captured_at"])
        <= stamp(post_replay["captured_at"]),
        "Snapshot timestamps are unordered",
    )
    approved_before = {
        key for key, row in initial.items() if row["status"] == "approved"
    }
    require(
        len(approved_before) == 316
        and sum(k[0] == "product" for k in approved_before) == 40,
        "Wrong original 40-product/276-option approved set",
    )
    entries = unique(
        [{**e, "target": target(e)} for e in manifest["decisions"]],
        "target",
        "manifest target",
    )
    require(
        {(e["kind"], e["id"]) for e in entries.values()}
        == {("option", identifier) for identifier in SCOPE}
        and len(entries) == 3,
        "Manifest must cover exactly the three authorized pending Agoda slots",
    )
    planned, applied, replayed = [
        unique(rows, "target", label)
        for rows, label in ((dry_run, "dry-run"), (apply, "apply"), (replay, "replay"))
    ]
    require(
        set(entries) == set(planned) == set(applied) == set(replayed),
        "Manifest/dry-run/apply/replay exact coverage differs",
    )
    ids = [r["receipt_id"] for r in applied.values()]
    require(len(set(ids)) == 3, "Receipt IDs are not unique")
    for identifier in ids:
        require(str(UUID(identifier)) == identifier, "Noncanonical receipt UUID")
    approvals, guards, counts, changed_fields, outcome_rows = (
        set(),
        Counter(),
        Counter(),
        Counter(),
        [],
    )
    for name, entry in entries.items():
        key = ("option", entry["id"])
        old, new, result = initial[key], after[key], applied[name]
        parent = initial[("product", old["product_id"])]
        require(
            old["status"] == "pending"
            and old["provider"] == "agoda"
            and old["discovery_status"] == "unconfirmed"
            and all(old[k] is None for k in ("url", "evidence_url", "property_id")),
            "A target is not the original empty pending Agoda slot",
        )
        require(
            parent["status"] == "pending" and parent["destination_id"] == "busan",
            "A target no longer belongs to its pending Busan parent",
        )
        require(
            entry["before_hash"] == digest(old)
            and type(entry["version"]) is int
            and entry["version"] == old["version"],
            "Entry baseline hash/version differs",
        )
        require(
            stamp(entry["checked_at"]) > stamp(before["captured_at"]),
            "Redirect evidence predates the fresh baseline",
        )
        require(
            entry["decision"] == "approve"
            and entry["method"] == "iab"
            and entry["browser_verified"] is True
            and entry.get("option_patch")
            == {
                "url": TARGET_URLS[entry["id"]],
                "evidence_url": TARGET_URLS[entry["id"]],
            }
            and not entry.get("facts_patch")
            and not entry.get("evidence"),
            "Unauthorized redirect URL patch or decision",
        )
        require(
            planned[name]
            == {
                "target": name,
                "decision": entry["decision"],
                "before_hash": entry["before_hash"],
                "mode": "dry-run",
            },
            "Dry-run differs or contains a write receipt",
        )
        require(
            set(result)
            == {"target", "outcome", "receipt_id", "after_hash", "guard_code"}
            and result["after_hash"] == digest(new),
            "Apply shape/full-row hash mismatch",
        )
        require(
            replayed[name]
            == {
                "target": name,
                "outcome": "replayed",
                "receipt_id": result["receipt_id"],
                "after_hash": result["after_hash"],
            },
            "Replay did not preserve its exact receipt and full-row hash",
        )
        outcome, guard = result["outcome"], result["guard_code"]
        require(outcome in {"approved", "hold"}, "Nonterminal outcome")
        counts[outcome] += 1
        if outcome == "hold":
            require(old == new, "Hold/failed edit was not completely rolled back")
            if entry["decision"] == "approve":
                require(
                    guard in KNOWN_GUARDS,
                    "Unknown failure was silently converted to hold",
                )
                guards[guard] += 1
            else:
                require(
                    guard is None and "option_patch" not in entry,
                    "Explicit hold contains a mutation or fallback",
                )
        else:
            require(
                entry["decision"] == "approve"
                and guard is None
                and entry["method"] == "iab"
                and entry["browser_verified"] is True,
                "Approval lacks actual IAB authorization",
            )
            patch = entry.get("option_patch")
            require(
                isinstance(patch, dict)
                and set(patch) == {"url", "evidence_url"}
                and all(
                    isinstance(u, str)
                    and u.startswith("https://")
                    and u in entry["source_urls"]
                    for u in patch.values()
                ),
                "A new slot lacks its exact reviewed URLs",
            )
            require(
                all(new[k] == value for k, value in patch.items())
                and new["property_id"] is None
                and new["discovery_status"] == "found",
                "Stored URLs/quote guard differ from the authorized patch",
            )
            require(set(old) == set(new), "Option schema changed")
            changed = {k for k in old if old[k] != new[k]}
            require(
                changed <= NORMAL_FIELDS,
                f"Immutable option fields changed: {changed - NORMAL_FIELDS}",
            )
            require(
                type(new["version"]) is int
                and new["version"] == old["version"] + 2
                and new["status"] == "approved"
                and new["identity_note"] == entry["identity_note"],
                "Normal edit/review did not produce the exact +2 approval",
            )
            require(
                isinstance(new["health_status"], str)
                and bool(new["health_status"])
                and new["health_status"] not in {"unsafe", "unavailable"},
                "Fatal link state was approved",
            )
            for field in ("checked_at", "verified_at", "updated_at"):
                require(
                    stamp(before["captured_at"])
                    <= stamp(new[field])
                    <= stamp(final["captured_at"]),
                    f"Invalid approval timestamp: {field}",
                )
            changed_fields.update(changed)
            approvals.add(entry["id"])
        outcome_rows.append(
            {
                "id": entry["id"],
                "product_id": old["product_id"],
                "target": name,
                "requested_decision": entry["decision"],
                "outcome": outcome,
                "guard_code": guard,
                "receipt_id": result["receipt_id"],
                "entry_hash": digest({k: v for k, v in entry.items() if k != "target"}),
                "before_hash": digest(old),
                "after_hash": digest(new),
                "before_version": old["version"],
                "after_version": new["version"],
            }
        )
    for key, old in initial.items():
        if key[0] != "option" or key[1] not in approvals:
            require(old == after[key], f"Non-approved-result row changed: {key}")
    require(
        all(initial[key] == after[key] for key in approved_before),
        "An original approved row changed",
    )
    return {
        "catalog_rows": 420,
        "exact_scope_rows": 3,
        "original_316_approved_unchanged": True,
        "all_60_products_unchanged": True,
        "configs_full_rows_unchanged": True,
        "untouched_rows": 420 - len(approvals),
        "post_replay_420_full_rows_unchanged": True,
        "property_identity_and_prices_unchanged": True,
        "quote_property_ids_remain_null": True,
        "dry_run_exact_no_write_receipts": True,
        "replay_same_receipt_ids_and_hashes": True,
        "actual_outcomes": dict(sorted(counts.items())),
        "guard_fallbacks": dict(sorted(guards.items())),
        "approved_option_ids": sorted(approvals),
        "changed_field_counts": dict(sorted(changed_fields.items())),
        "outcomes": sorted(outcome_rows, key=lambda r: r["id"]),
        "expected_normal_audit_additions": {
            "travel_services.hotel_option_edit": len(approvals),
            "travel_services.hotel_option_review": len(approvals),
            "travel_services.product_edit": 0,
            "travel_services.product_review": 0,
        },
    }


def verify_public(captures, before):
    products = unique(before["products"], "id", "baseline product")
    options = unique(before["options"], "id", "baseline option")
    public_products = {i for i, row in products.items() if row["status"] == "approved"}
    public_options = {
        i
        for i, row in options.items()
        if row["status"] == "approved" and row["product_id"] in public_products
    }
    require(
        len(public_products) == 40 and len(public_options) == 192,
        "Pinned public baseline membership is not 40/192",
    )
    phase_rows = {}
    for phase in ("before", "after", "after-replay"):
        report = captures[phase]
        require(
            report["tag"] == TAG
            and report["phase"] == phase
            and report["baseline_hash"] == BASELINE_HASH
            and report["method"] == "anonymous_public_GET_only",
            "Public provenance mismatch",
        )
        require(
            stamp(BASELINE_CAPTURED_AT)
            <= stamp(report["started_at"])
            <= stamp(report["completed_at"]),
            "Public capture is stale or unordered",
        )
        for field in ("credentials_sent", "cookies_sent"):
            require(report[field] is False, f"Public capture sent {field}")
        for field in (
            "redirects_followed",
            "quote_calls",
            "clickout_calls",
            "mutating_api_calls",
            "database_connections",
        ):
            require(
                report[field] == 0, f"Public capture exceeded read-only scope: {field}"
            )
        summary = report["summary"]
        require(
            summary["all_checks_pass"] is True
            and summary["http_200"] == 30
            and summary["no_store_responses"] == 30
            and summary["unique_public_products"] == 40
            and summary["unique_public_booking_options"] == 192,
            "Public summary mismatch",
        )
        responses = {}
        for row in report["responses"]:
            pair = (row["city"], row["locale"])
            require(
                pair not in responses and pair[0] in CITIES and pair[1] in LOCALES,
                "Duplicate/unknown public city-locale pair",
            )
            require(
                row["http_status"] == 200
                and "no-store" in (row["cache_control"] or "").lower()
                and not row["issues"],
                "Public response HTTP/cache/issue check failed",
            )
            require(
                stamp(report["started_at"])
                <= stamp(row["started_at"])
                <= stamp(row["completed_at"])
                <= stamp(report["completed_at"]),
                "Public response timestamp is outside its capture",
            )
            expected_products = {
                i for i in public_products if products[i]["destination_id"] == pair[0]
            }
            expected_options = {
                i
                for i in public_options
                if options[i]["product_id"] in expected_products
            }
            for field, expected in (
                ("item_ids", expected_products),
                ("booking_option_ids", expected_options),
            ):
                require(
                    len(row[field]) == len(set(row[field]))
                    and set(row[field]) == expected,
                    f"Public membership differs: {phase}/{pair}/{field}",
                )
            require(
                isinstance(row["body_hash"], str)
                and re.fullmatch(r"[0-9a-f]{64}", row["body_hash"]),
                "Invalid public allowlisted-body fingerprint",
            )
            responses[pair] = row
        require(
            set(responses) == {(city, loc) for city in CITIES for loc in LOCALES},
            "Incomplete public 30-request matrix",
        )
        phase_rows[phase] = responses
    require(
        stamp(captures["before"]["completed_at"])
        <= stamp(captures["after"]["started_at"])
        and stamp(captures["after"]["completed_at"])
        <= stamp(captures["after-replay"]["started_at"]),
        "Public phases are unordered",
    )
    for pair, original in phase_rows["before"].items():
        for phase in ("after", "after-replay"):
            row = phase_rows[phase][pair]
            require(
                row["body_hash"] == original["body_hash"]
                and set(row["item_ids"]) == set(original["item_ids"])
                and set(row["booking_option_ids"])
                == set(original["booking_option_ids"]),
                f"Public allowlisted body or IDs changed: {phase}/{pair}",
            )
    return {
        "phases": 3,
        "requests_per_phase": 30,
        "public_products": 40,
        "public_options": 192,
        "all_pair_memberships_and_body_fingerprints_unchanged": True,
        "all_three_pending_busan_parents_and_their_options_hidden": True,
        "scope_note": (
            "Body fingerprints attest unchanged captured titles/credits/prices/options; "
            "raw bodies are not retained here."
        ),
    }


def verify_independent(captures, row_report):
    outcomes = unique(row_report["outcomes"], "id", "verified outcome")
    require(set(outcomes) == SCOPE, "Independent expected outcome scope differs")
    approved = set(row_report["approved_option_ids"])
    phases = ("before", "after", "after-replay")
    by_phase = {}
    for phase in phases:
        report = captures[phase]
        require(
            report["schema_version"] == 1
            and report["tag"] == TAG
            and report["phase"] == phase
            and report["baseline_hash"] == BASELINE_HASH
            and stamp(report["baseline_at"]) == stamp(BASELINE_CAPTURED_AT)
            and report["completed_with"] == "ROLLBACK",
            "Independent SQL provenance or completion mismatch",
        )
        snapshot = report["snapshot"]
        require(
            snapshot["isolation_level"] == "repeatable read"
            and snapshot["read_only"] == "on"
            and snapshot["matching_roots"] == 1
            and snapshot["review_pending_roots"] == 1
            and snapshot["active_actors"] == 1
            and snapshot["authenticated_request_audits"] >= 1
            and stamp(snapshot["captured_at"]) >= stamp(BASELINE_CAPTURED_AT),
            "SQL snapshot is not fresh, authorized and read-only",
        )
        actual = 0 if phase == "before" else len(approved)
        receipt_count = 0 if phase == "before" else 3
        hold_count = 0 if phase == "before" else 3 - actual
        require(
            report["expected"]
            == {
                "scope_count": 3,
                "receipts": receipt_count,
                "approved": actual,
                "edits": actual,
                "holds": hold_count,
            },
            "SQL expected counts do not match actual operator outcomes",
        )
        require(
            report["inventory"]
            == {
                "hotel_products": 60,
                "hotel_options": 360,
                "approved_products": 40,
                "approved_options": 276 + actual,
            },
            "SQL inventory differs from independently verified full snapshots",
        )
        groups = unique(report["protected_groups"], "name", "protected group")
        require(set(groups) == set(PROTECTED_GROUPS), "SQL protected groups incomplete")
        for name, expected in PROTECTED_GROUPS.items():
            group = groups[name]
            require(
                type(group["count"]) is int
                and group["count"] >= 0
                and group["expected_count"] == expected
                and group["count_matches"] is (None if expected is None else True)
                and (expected is None or group["count"] == expected)
                and bool(re.fullmatch(r"[0-9a-f]{32}", group["rows_md5"])),
                f"Invalid protected SQL group: {name}",
            )
        scope_rows = unique(report["scope_rows"], "id", "SQL scope row")
        require(set(scope_rows) == SCOPE, "SQL scope membership differs")
        for identifier, scope in scope_rows.items():
            success = phase != "before" and identifier in approved
            require(
                scope["parent_id"] == outcomes[identifier]["product_id"]
                and scope["provider"] == "agoda"
                and scope["parent_match"] is True
                and scope["parent_status"] == "pending"
                and scope["parent_destination_id"] == "busan"
                and scope["property_id_null"] is True
                and scope["status"] == ("approved" if success else "pending")
                and scope["version"] == (3 if success else 1)
                and scope["url_null"] is (not success)
                and scope["evidence_url_null"] is (not success)
                and scope["url_matches_manifest"] is success
                and scope["evidence_url_matches_manifest"] is success
                and bool(re.fullmatch(r"[0-9a-f]{32}", scope["row_md5"])),
                f"SQL scope parent, quote guard or normal transition differs: {identifier}",
            )
        receipts = unique(report["receipts"], "target_id", "SQL receipt")
        require(
            set(receipts) == (set() if phase == "before" else SCOPE),
            "SQL receipt coverage differs",
        )
        receipt_ids = set()
        for identifier, receipt in receipts.items():
            expected = outcomes[identifier]
            require(
                all(
                    receipt[field] == expected[field]
                    for field in (
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
                )
                and receipt["kind"] == "option"
                and receipt["browser_verified"] == "true"
                and receipt["actor_root_match"] is True
                and receipt["actor_null"] is False
                and all(
                    receipt[field] is True
                    for field in (
                        "provenance_match",
                        "scope_match",
                        "entry_hash_match",
                        "before_hash_match",
                        "option_patch_match",
                        "after_hash_valid",
                    )
                )
                and stamp(BASELINE_CAPTURED_AT)
                <= stamp(receipt["created_at"])
                <= stamp(snapshot["captured_at"])
                and bool(re.fullmatch(r"[0-9a-f]{32}", receipt["row_md5"])),
                f"SQL receipt actor, provenance, patch or stdout binding differs: {identifier}",
            )
            require(
                receipt["receipt_id"] not in receipt_ids, "Duplicate SQL receipt UUID"
            )
            receipt_ids.add(receipt["receipt_id"])
        totals = report["receipt_totals"]
        receipt_fingerprint = hashlib.md5(
            "".join(
                r["row_md5"]
                for r in sorted(receipts.values(), key=lambda r: r["receipt_id"])
            ).encode(),
            usedforsecurity=False,
        ).hexdigest()
        require(
            totals
            == {
                "count": receipt_count,
                "distinct_targets": receipt_count,
                "approved": actual,
                "holds": hold_count,
                "rows_md5": receipt_fingerprint,
            },
            "SQL receipt totals or full-row fingerprint differs",
        )
        audits = unique(report["normal_audits"], "audit_id", "normal audit")
        expected_pairs = {
            (identifier, action)
            for identifier in (set() if phase == "before" else approved)
            for action in (
                "travel_services.hotel_option_edit",
                "travel_services.hotel_option_review",
            )
        }
        require(
            len(audits) == actual * 2
            and {(a["target"], a["action"]) for a in audits.values()} == expected_pairs,
            "SQL normal audit count, target or action differs",
        )
        for identifier, audit in audits.items():
            require(
                str(UUID(identifier)) == identifier
                and identifier not in receipt_ids
                and audit["in_scope"] is True
                and audit["actor_root_match"] is True
                and audit["actor_null"] is False
                and stamp(BASELINE_CAPTURED_AT)
                <= stamp(audit["created_at"])
                <= stamp(snapshot["captured_at"])
                and bool(re.fullmatch(r"[0-9a-f]{32}", audit["row_md5"])),
                "SQL normal audit actor, scope, timestamp or hash differs",
            )
        entry_checks = unique(report["entry_checks"], "id", "SQL entry check")
        require(set(entry_checks) == SCOPE, "SQL entry-check coverage differs")
        for identifier, check in entry_checks.items():
            success = phase != "before" and identifier in approved
            require(
                check
                == {
                    "id": identifier,
                    "receipt_count": 0 if phase == "before" else 1,
                    "edit_audit_count": int(success),
                    "review_audit_count": int(success),
                    "outcome": None
                    if phase == "before"
                    else outcomes[identifier]["outcome"],
                    "row_transition_valid": True,
                },
                f"SQL entry transition/audit checks differ: {identifier}",
            )
        by_phase[phase] = {
            "groups": groups,
            "scope": scope_rows,
            "receipts": receipts,
            "audits": audits,
            "totals": totals,
            "entry_checks": entry_checks,
        }
    require(
        stamp(captures["before"]["snapshot"]["captured_at"])
        <= stamp(captures["after"]["snapshot"]["captured_at"])
        <= stamp(captures["after-replay"]["snapshot"]["captured_at"]),
        "SQL phase timestamps are unordered",
    )
    for phase in phases[1:]:
        require(
            by_phase[phase]["groups"] == by_phase["before"]["groups"],
            f"Protected SQL full-row fingerprints changed: {phase}",
        )
        require(
            {k: v for k, v in captures[phase]["snapshot"].items() if k != "captured_at"}
            == {
                k: v
                for k, v in captures["before"]["snapshot"].items()
                if k != "captured_at"
            },
            "SQL authorization/read-only context changed",
        )
        for identifier in SCOPE - approved:
            require(
                by_phase[phase]["scope"][identifier]
                == by_phase["before"]["scope"][identifier],
                f"SQL hold row changed instead of fully rolling back: {identifier}",
            )
    require(
        by_phase["after"] == by_phase["after-replay"],
        "Replay changed SQL full rows, receipt IDs/hashes or added normal audits",
    )
    return {
        "status": "passed",
        "phases": 3,
        "read_only_repeatable_read": True,
        "receipt_count": 3,
        "normal_edits": len(approved),
        "normal_reviews": len(approved),
        "all_316_original_approved_and_417_nonscope_rows_protected": True,
        "all_384_previous_receipts_and_historical_audits_unchanged": True,
        "configs_brands_prices_offers_and_clicks_unchanged": True,
        "hold_rows_fully_unchanged": True,
        "all_normal_audits_bound_to_authenticated_root": True,
        "replay_same_receipts_and_zero_added_audits": True,
    }


def verify(directory, require_complete=False):
    required = (
        "before.json",
        "manifest.json",
        "dry-run.ndjson",
        "apply.ndjson",
        "replay.ndjson",
        "final-snapshot.json",
        "post-replay-snapshot.json",
    )
    optional = tuple(
        f"{prefix}-{phase}.json"
        for prefix in ("independent", "public")
        for phase in ("before", "after", "after-replay")
    )
    data, missing = {}, []
    for name in (*required, *optional):
        path = directory / name
        if not path.exists():
            require(name not in required, f"Required local artifact missing: {name}")
            missing.append(name)
        else:
            data[name] = (
                read_ndjson(path) if name.endswith(".ndjson") else read_json(path)
            )
    rows = verify_rows(*(data[name] for name in required))
    sections = {}
    for prefix, checker in (
        ("public", verify_public),
        ("independent", verify_independent),
    ):
        names = [
            f"{prefix}-{phase}.json" for phase in ("before", "after", "after-replay")
        ]
        if all(name in data for name in names):
            captures = {
                phase: data[f"{prefix}-{phase}.json"]
                for phase in ("before", "after", "after-replay")
            }
            sections[prefix] = checker(
                captures, data["before.json"] if prefix == "public" else rows
            )
        else:
            sections[prefix] = {"status": "not_fully_available"}
    if require_complete:
        require(not missing, f"Final acceptance evidence missing: {missing}")
    return {
        "schema_version": 1,
        "tag": TAG,
        "verified_at": datetime.now(UTC).isoformat(),
        "status": "partial" if missing else "passed",
        "final_acceptance": not missing,
        "production_access_by_verifier": False,
        "network_calls": 0,
        "database_connections": 0,
        "baseline_semantic_sha256": BASELINE_HASH,
        "manifest_semantic_sha256": digest(data["manifest.json"]),
        "rows": rows,
        **sections,
        "missing_final_acceptance_evidence": missing,
        "input_file_sha256": {
            name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
            for name in sorted(data)
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directory", type=Path, default=Path(__file__).resolve().parent
    )
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument(
        "--output", type=Path, help="Optional exclusive-create report path"
    )
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error("Refusing to overwrite an existing verification report")
    try:
        report = verify(args.directory, args.require_complete)
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                json.dump(report, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
        print(json.dumps(report, ensure_ascii=True))
    except (OSError, ValueError, KeyError, TypeError) as exc:
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
