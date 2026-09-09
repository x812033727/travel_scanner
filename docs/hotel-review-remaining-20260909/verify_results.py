"""Verify this subset review using local JSON/NDJSON/psql evidence only.

No API imports, database connections, network calls or production actions. The
default command only prints JSON. --output exclusively creates a report after
verification; --require-complete rejects absent replay, public or SQL evidence.
Missing optional evidence is explicitly partial, never a completed acceptance.
"""

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

TAG = "hotel-review-remaining-20260909"
BASELINE_HASH = "c938d83913645ac6a7651eca0e705621b33b40bb235905392c54917492bdb03d"
ALLOWED_OPTION_FIELDS = {
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
PRICE_FIELDS = {"reference_price", "currency", "price_checked_at"}
CREDIT_FIELDS = {"title", "publisher", "url", "license_name", "license_url", "changes"}
NORMAL_ACTIONS = {
    "travel_services.hotel_option_edit",
    "travel_services.hotel_option_review",
    "travel_services.product_edit",
    "travel_services.product_review",
}
UNCHANGED_SQL_SECTIONS = {
    "hotel_products",
    "travel_service_config",
    "provider_configs",
    "affiliate_clicks_hotel",
    "destination_affiliate_offers_hotel",
    "hotel_booking_clicks_all",
    "travel_service_brands_all",
    "travel_service_offers_hotel",
    "protected_groups",
    "all_historical_audits",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_jsonl(path):
    # No silent skipping of non-JSON stdout, warnings, duplicate rows or summaries.
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def unique(rows, key, label):
    result = {}
    for row in rows:
        value = row[key]
        require(value not in result, f"Duplicate {label}: {value}")
        result[value] = row
    return result


def indexed(data):
    return {
        (kind, identifier): row
        for kind, collection in (("product", "products"), ("option", "options"))
        for identifier, row in unique(data[collection], "id", collection).items()
    }


def timestamp(value):
    require(isinstance(value, str), "Timestamp is not a string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Timestamp lacks timezone")
    return parsed


def target(entry):
    return f"{TAG}:{entry['kind']}:{entry['id']}"


def verify_rows(before, manifest, apply_log, final, replay_log=None, dry_run=None):
    require(digest(before) == BASELINE_HASH, "Pinned baseline semantic hash mismatch")
    require(
        set(manifest) == {"schema_version", "tag", "baseline_hash", "decisions"},
        "Unexpected manifest schema",
    )
    require(
        manifest["schema_version"] == 1
        and manifest["tag"] == TAG
        and manifest["baseline_hash"] == BASELINE_HASH,
        "Manifest provenance mismatch",
    )
    initial, current = indexed(before), indexed(final)
    require(
        len(before["products"]) == len(final["products"]) == 60, "Product scope changed"
    )
    require(
        len(before["options"]) == len(final["options"]) == 360, "Option scope changed"
    )
    require(set(initial) == set(current), "420-row membership changed")
    require(
        digest(sorted(before["configs"], key=lambda r: r["id"]))
        == digest(sorted(final["configs"], key=lambda r: r["id"])),
        "Configuration full rows changed",
    )
    approved_before = {k for k, r in initial.items() if r["status"] == "approved"}
    require(
        len(approved_before) == 295,
        "Pinned original approved-row count differs from 295",
    )
    entries = unique(
        [{**e, "target": target(e)} for e in manifest["decisions"]],
        "target",
        "manifest target",
    )
    require(1 <= len(entries) <= 125, "Expected a nonempty subset of pending rows")
    applied = unique(apply_log, "target", "apply target")
    require(set(entries) == set(applied), "Manifest/apply target coverage mismatch")
    replayed = (
        None if replay_log is None else unique(replay_log, "target", "replay target")
    )
    if replayed is not None:
        require(
            set(entries) == set(replayed), "Manifest/replay target coverage mismatch"
        )
    if dry_run is not None:
        planned = unique(dry_run, "target", "dry-run target")
        require(set(entries) == set(planned), "Dry-run target coverage mismatch")
        for name, entry in entries.items():
            require(
                planned[name]
                == {
                    "target": name,
                    "decision": entry["decision"],
                    "before_hash": entry["before_hash"],
                    "mode": "dry-run",
                },
                "Dry-run contains a write receipt or differs from the manifest",
            )
    receipts = [r["receipt_id"] for r in applied.values()]
    require(len(set(receipts)) == len(entries), "Duplicate apply receipt IDs")
    for identifier in receipts:
        require(str(UUID(identifier)) == identifier, "Noncanonical receipt UUID")
    start, end = timestamp(before["captured_at"]), timestamp(final["captured_at"])
    require(start <= end, "Final snapshot predates baseline")
    approvals, patches, outcomes, guards, changed_fields = (
        set(),
        set(),
        Counter(),
        Counter(),
        Counter(),
    )
    outcome_groups = Counter()
    for name, entry in entries.items():
        require(entry["kind"] in {"option", "product"}, "Unexpected entry kind")
        require(
            entry["kind"] == "option" or entry["decision"] == "hold",
            "Products may only receive unchanged hold receipts in this scope",
        )
        key = (entry["kind"], entry["id"])
        require(
            key in initial and key not in approved_before,
            "Unknown or already approved target",
        )
        old, new, result = initial[key], current[key], applied[name]
        require(
            old["status"] == "pending"
            and type(entry["version"]) is int
            and entry["version"] == old["version"]
            and entry["before_hash"] == digest(old),
            "Entry is not the exact version-matched pending baseline row",
        )
        require(
            entry["decision"] in {"approve", "hold"}, "Unauthorized requested decision"
        )
        require(
            timestamp(entry["checked_at"]) > start, "Entry evidence predates baseline"
        )
        require(
            set(result)
            == {"target", "outcome", "receipt_id", "after_hash", "guard_code"},
            "Unexpected apply stdout record shape",
        )
        require(
            result["after_hash"] == digest(new), "Apply/final full-row hash mismatch"
        )
        if replayed is not None:
            require(
                replayed[name]
                == {
                    "target": name,
                    "outcome": "replayed",
                    "receipt_id": result["receipt_id"],
                    "after_hash": result["after_hash"],
                },
                "Replay is not the exact unchanged original receipt/hash",
            )
        outcome, guard = result["outcome"], result["guard_code"]
        require(outcome in {"approved", "hold"}, "Nonterminal apply outcome")
        outcomes[outcome] += 1
        outcome_groups[
            (entry["kind"], entry["decision"], outcome, guard or "(none)")
        ] += 1
        if outcome == "hold":
            require(old == new, "Held or failed-review row was modified")
            if entry["decision"] == "approve":
                require(
                    guard in KNOWN_GUARDS,
                    "Unknown failure was silently converted to hold",
                )
                guards[guard] += 1
            else:
                require(
                    guard is None and "option_patch" not in entry,
                    "An explicit hold carries a mutation or unexpected fallback",
                )
            continue
        require(
            entry["decision"] == "approve" and guard is None,
            "Approval was not requested or carries a guard failure",
        )
        require(
            type(entry["browser_verified"]) is bool
            and entry["method"] in {"iab", "primary_web"},
            "Invalid evidence method",
        )
        require(
            not entry["browser_verified"] or entry["method"] == "iab",
            "Browser override lacks IAB provenance",
        )
        allowed = set(ALLOWED_OPTION_FIELDS)
        patch = entry.get("option_patch")
        if "option_patch" in entry:
            require(
                isinstance(patch, dict) and set(patch) == {"url", "evidence_url"},
                "Null-slot patch contains unscoped fields",
            )
            require(
                entry["method"] == "iab" and entry["browser_verified"] is True,
                "A new URL slot requires actual IAB evidence",
            )
            require(
                old["discovery_status"] in {"unconfirmed", "not_found"}
                and all(old[k] is None for k in ("url", "property_id", "evidence_url")),
                "Attempted replacement of an existing identity",
            )
            require(
                all(
                    isinstance(v, str)
                    and v.startswith("https://")
                    and v in entry["source_urls"]
                    for v in patch.values()
                ),
                "New exact URL/evidence absent from the source list",
            )
            require(
                all(new[k] == v for k, v in patch.items())
                and new["property_id"] is None
                and new["discovery_status"] == "found",
                "New slot differs from reviewed URLs or enables provider quotes",
            )
            allowed |= {"url", "evidence_url", "discovery_status"}
            patches.add(entry["id"])
        else:
            require(
                old["discovery_status"] == "found"
                and old["url"]
                and old["evidence_url"]
                and old["url"] in entry["source_urls"],
                "Existing identity evidence missing",
            )
        require(set(old) == set(new), "Option schema changed")
        fields = {field for field in old if old[field] != new[field]}
        require(
            fields <= allowed,
            f"Immutable option fields changed: {key}: {fields - allowed}",
        )
        require(
            type(new["version"]) is int
            and new["version"] == old["version"] + (2 if patch else 1)
            and new["status"] == "approved",
            "Unexpected approval status/version delta",
        )
        require(
            new["identity_note"] == entry["identity_note"],
            "Identity note differs from review",
        )
        # Mirror normal review and operator guards; nonfatal read failures may
        # use actual browser evidence, but unsafe/unavailable may never pass.
        require(
            isinstance(new["health_status"], str)
            and bool(new["health_status"])
            and new["health_status"] not in {"unsafe", "unavailable"}
            and (
                new["health_status"] == "healthy" or entry["browser_verified"] is True
            ),
            "Unsafe or unverified unhealthy approval",
        )
        for field in ("verified_at", "checked_at", "updated_at"):
            require(start <= timestamp(new[field]) <= end, f"Invalid approval {field}")
        changed_fields.update(fields)
        approvals.add(entry["id"])
    for key, old in initial.items():
        if key[0] != "option" or key[1] not in approvals:
            require(old == current[key], f"Non-approved-result full row changed: {key}")
    return {
        "catalog_rows": 420,
        "all_60_products_unchanged": True,
        "original_295_approved_unchanged": True,
        "configs_full_rows_unchanged": True,
        "immutable_identity_and_prices_unchanged": True,
        "untouched_rows": 420 - len(approvals),
        "manifest_entries": len(entries),
        "unique_receipts": len(receipts),
        "apply_final_hashes_match": True,
        "replay_same_receipts_and_hashes": None if replayed is None else True,
        "dry_run_exact_and_no_write_receipts": None if dry_run is None else True,
        "actual_outcomes": dict(sorted(outcomes.items())),
        "guard_fallbacks": dict(sorted(guards.items())),
        "approved_option_ids": sorted(approvals),
        "filled_null_slot_ids": sorted(patches),
        "expected_scope_rows": [
            {
                "kind": e["kind"],
                "id": e["id"],
                "before_status": initial[(e["kind"], e["id"])]["status"],
                "before_version": initial[(e["kind"], e["id"])]["version"],
                "after_status": current[(e["kind"], e["id"])]["status"],
                "after_version": current[(e["kind"], e["id"])]["version"],
                "outcome": applied[name]["outcome"],
            }
            for name, e in sorted(entries.items())
        ],
        "expected_normal_audit_additions": {
            "travel_services.hotel_option_edit": len(patches),
            "travel_services.hotel_option_review": len(approvals),
            "travel_services.product_edit": 0,
            "travel_services.product_review": 0,
        },
        "expected_sql_receipt_outcomes": [
            {
                "kind": k[0],
                "requested_decision": k[1],
                "outcome": k[2],
                "guard_code": k[3],
                "rows": count,
            }
            for k, count in sorted(outcome_groups.items())
        ],
        "changed_field_counts": dict(sorted(changed_fields.items())),
        "final_status_counts": dict(
            sorted(
                Counter(
                    f"{kind}:{r['status']}" for (kind, _), r in current.items()
                ).items()
            )
        ),
    }


def verify_public(report, snapshot, phase):
    require(
        report["tag"] == TAG
        and report["phase"] == phase
        and report["method"] == "anonymous_public_GET_only",
        "Public capture provenance mismatch",
    )
    require(
        report["credentials_sent"] is False and report["cookies_sent"] is False,
        "Public capture used credentials/cookies",
    )
    for field in (
        "redirects_followed",
        "quote_calls",
        "clickout_calls",
        "mutating_api_calls",
        "database_connections",
    ):
        require(report[field] == 0, f"Public capture exceeded read-only scope: {field}")
    require(
        report["matrix_requests_retained"]
        == report["total_http_gets_in_this_check"]
        == 30,
        "Incomplete public request matrix",
    )
    require(
        report["summary"]["all_checks_pass"] is True
        and not report["summary"]["issues"],
        "Public capture reported errors",
    )
    source_products = unique(snapshot["products"], "id", "snapshot product")
    source_options = unique(snapshot["options"], "id", "snapshot option")
    expected_products = {
        i for i, r in source_products.items() if r["status"] == "approved"
    }
    expected_options = {
        i
        for i, r in source_options.items()
        if r["status"] == "approved" and r["product_id"] in expected_products
    }
    products = unique(report["public_products"], "id", "public product")
    options = unique(report["public_booking_options"], "id", "public option")
    require(
        len(products) == 40 and set(products) == expected_products,
        "Public catalog lost original hotels or exposed pending parents",
    )
    require(
        set(options) == expected_options,
        "Public options differ from actual approved results",
    )
    require(
        report["summary"]["unique_public_products"] == len(products)
        and report["summary"]["unique_public_booking_options"] == len(options),
        "Public aggregate count mismatch",
    )
    credits, used = report["source_credit_sets"], set()
    for identifier, row in products.items():
        original = source_products[identifier]
        require(
            row["kind"] == "hotel"
            and row["destination_id"] == original["destination_id"]
            and row["source_url"] == original["source_url"],
            "Public product identity changed",
        )
        require(
            PRICE_FIELDS <= set(row) and all(row[f] is None for f in PRICE_FIELDS),
            "Prices must be explicitly unknown, not zero or missing",
        )
        require(
            set(row["titles_by_locale"]) == LOCALES
            and all(
                row["titles_by_locale"][loc]
                == (original["names_json"].get(loc) or original["title"])
                for loc in LOCALES
            ),
            "Public localized title/fallback changed",
        )
        credit_hash = row["source_credit_set_sha256"]
        used.add(credit_hash)
        require(
            credit_hash in credits
            and digest(credits[credit_hash]) == credit_hash
            and credits[credit_hash] == original["facts"]["source_credits"],
            "Public source attribution changed",
        )
        for credit in credits[credit_hash]:
            require(
                set(credit) == CREDIT_FIELDS
                and all(isinstance(v, str) and v.strip() for v in credit.values()),
                "Invalid source credit",
            )
            require(
                all(credit[k].startswith("https://") for k in ("url", "license_url")),
                "Non-HTTPS source attribution",
            )
        expected = {
            i for i in expected_options if source_options[i]["product_id"] == identifier
        }
        require(
            len(row["booking_option_ids"]) == len(set(row["booking_option_ids"]))
            and set(row["booking_option_ids"]) == expected,
            "Public product option set differs",
        )
    require(used == set(credits), "Unused/missing public credit set")
    for identifier, row in options.items():
        original = source_options[identifier]
        require(
            row["product_id"] == original["product_id"]
            and row["provider"] == original["provider"],
            "Public option ownership/provider changed",
        )
        require(
            row["mode"] == "direct" and row["quote_status"] == "not_configured",
            "Affiliate or quote behavior changed",
        )
    pairs = set()
    for check in report["checks"]:
        pair = (check["destination_id"], check["locale"])
        require(
            pair not in pairs and pair[0] in CITIES and pair[1] in LOCALES,
            "Duplicate/unknown public city-locale pair",
        )
        pairs.add(pair)
        require(
            check["http_status"] == 200
            and check["enabled"] is True
            and "no-store" in (check["cache_control"] or "").lower()
            and "application/json" in (check["content_type"] or "").lower()
            and check["all_checks_pass"] is True
            and not check["issues"],
            "Public response HTTP/cache/content/enabled checks failed",
        )
        city_products = {
            i for i, r in products.items() if r["destination_id"] == pair[0]
        }
        city_options = {
            i for i, r in options.items() if r["product_id"] in city_products
        }
        for ids_key, count_key, expected in (
            ("item_ids", "item_count", city_products),
            ("booking_option_ids", "booking_option_count", city_options),
        ):
            ids = check[ids_key]
            require(
                len(ids) == len(set(ids)) == check[count_key]
                and set(ids) == expected
                and digest(sorted(ids)) == check[f"{ids_key}_sha256"],
                "Public per-locale IDs/count/hash mismatch",
            )
        require(
            check["reported_total"] == len(city_products),
            "Public results are truncated",
        )
    require(
        pairs == {(c, loc) for c in CITIES for loc in LOCALES},
        "Public matrix incomplete",
    )
    require(
        report["summary"]["http_200"] == report["summary"]["no_store_responses"] == 30,
        "Public HTTP/cache summary mismatch",
    )
    return {
        "matrix_requests": 30,
        "products": len(products),
        "options": len(options),
        "all_locales_exact": True,
        "held_options_and_parents_hidden": True,
        "source_credits_preserved": True,
        "prices_unknown_and_quotes_disabled": True,
    }


def verify_public_delta(before, after, row_report, snapshot):
    old_products = unique(before["public_products"], "id", "before public product")
    new_products = unique(after["public_products"], "id", "after public product")
    old_options = unique(before["public_booking_options"], "id", "before public option")
    new_options = unique(after["public_booking_options"], "id", "after public option")
    require(set(old_products) == set(new_products), "Original 40 public hotels changed")
    require(
        set(old_options) <= set(new_options), "An original public option disappeared"
    )
    for identifier, old in old_products.items():
        require(
            {k: v for k, v in old.items() if k != "booking_option_ids"}
            == {
                k: v
                for k, v in new_products[identifier].items()
                if k != "booking_option_ids"
            },
            "An immutable public hotel field changed",
        )
    require(
        all(new_options[i] == row for i, row in old_options.items()),
        "An original public option field changed",
    )
    source_options = unique(snapshot["options"], "id", "final option")
    expected = {
        i
        for i in row_report["approved_option_ids"]
        if source_options[i]["product_id"] in new_products
    }
    require(
        set(new_options) - set(old_options) == expected,
        "Public additions differ from successful approvals under approved parents",
    )
    return {
        "original_hotels_retained": 40,
        "original_options_retained": len(old_options),
        "new_public_option_ids": sorted(expected),
        "new_public_options": len(expected),
        "new_approved_options_hidden_by_pending_parent": sorted(
            set(row_report["approved_option_ids"]) - expected
        ),
    }


def read_psql(path):
    """Parse aligned psql tables; do not accept errors or partially printed tables."""
    raw = path.read_text(encoding="utf-8-sig")
    require(
        not re.search(r"(?:^|\n).*\b(?:ERROR|FATAL|ROLLBACK)\b", raw),
        f"SQL evidence contains an error: {path.name}",
    )
    require(
        raw.strip().startswith("BEGIN") and raw.strip().endswith("COMMIT"),
        f"SQL evidence lacks a completed read-only transaction: {path.name}",
    )
    lines, tables, idx = raw.splitlines(), {}, 0
    while idx + 1 < len(lines):
        header = [part.strip() for part in lines[idx].split("|")]
        if "section" not in header or not re.fullmatch(r"[-+\s]+", lines[idx + 1]):
            idx += 1
            continue
        idx += 2
        count = 0
        while idx < len(lines) and not re.fullmatch(
            r"\(\d+ rows?\)", lines[idx].strip()
        ):
            if lines[idx].strip():
                values = [part.strip() for part in lines[idx].split("|")]
                require(len(values) == len(header), f"Malformed SQL row in {path.name}")
                row = dict(zip(header, values, strict=True))
                tables.setdefault(row["section"], []).append(row)
                count += 1
            idx += 1
        require(idx < len(lines), f"Truncated SQL table in {path.name}")
        require(
            int(re.search(r"\d+", lines[idx])[0]) == count,
            "SQL table row count mismatch",
        )
        idx += 1
    require(tables, "No SQL result tables found")
    return tables


def only(tables, section):
    rows = tables.get(section, [])
    require(len(rows) == 1, f"Expected exactly one SQL {section} row")
    return rows[0]


def sql_int(row, key):
    require(key in row and re.fullmatch(r"\d+", row[key]), f"Invalid SQL integer {key}")
    return int(row[key])


def canonical_rows(rows):
    return sorted(rows, key=lambda r: json.dumps(r, sort_keys=True))


def verify_sql(before, after, replay, row_report):
    count = row_report["manifest_entries"]
    approved = len(row_report["approved_option_ids"])
    edited = len(row_report["filled_null_slot_ids"])
    expected_scope = {
        (r["kind"], r["id"]): r for r in row_report["expected_scope_rows"]
    }
    scope_maps = []
    for phase, data in (("before", before), ("after", after), ("after-replay", replay)):
        snap = only(data, "snapshot")
        require(
            snap["phase"] == phase
            and snap["baseline_hash"] == BASELINE_HASH
            and snap["isolation_level"] == "repeatable read"
            and snap["read_only"] == "on",
            f"SQL {phase} snapshot provenance/read-only isolation failed",
        )
        timestamp(snap["captured_at"])
        root = only(data, "root_actor_provenance")
        require(
            all(
                sql_int(root, k) == 1
                for k in (
                    "matching_roots",
                    "review_pending_roots",
                    "active_actors",
                    "authenticated_request_audits",
                )
            ),
            "SQL root authorization provenance failed",
        )
        inventory = only(data, "inventory_totals")
        for actual, expected in (
            ("hotel_products", 60),
            ("hotel_options", 360),
            ("approved_products", 40),
            ("approved_options", 255 + (0 if phase == "before" else approved)),
        ):
            require(
                sql_int(inventory, actual)
                == sql_int(inventory, f"expected_{actual}")
                == expected,
                f"SQL inventory differs from actual outcomes: {phase}/{actual}",
            )
        for section, expected in (
            ("hotel_products", {"approved": 40, "pending": 20}),
            (
                "hotel_options",
                {
                    "approved": 255 + (0 if phase == "before" else approved),
                    "pending": 105 - (0 if phase == "before" else approved),
                },
            ),
        ):
            status_counts = Counter()
            for row in data.get(section, []):
                status_counts[row["status"]] += sql_int(row, "rows")
            require(
                status_counts == expected,
                f"SQL grouped status counts differ: {section}",
            )
        guards = only(data, "receipt_version_audit_guards")
        require(
            all(
                sql_int(guards, k) == 0
                for k in (
                    "invalid_baseline_version",
                    "unknown_outcomes",
                    "forbidden_product_mutations",
                    "option_version_or_audit_errors",
                )
            ),
            "SQL per-receipt version/audit/rollback guard failed",
        )
        scope = {}
        for row in data.get("scope_row_fingerprints", []):
            key = (row["kind"], row["id"])
            require(
                key not in scope and key in expected_scope,
                "SQL scope duplicate/unknown target",
            )
            expected = expected_scope[key]
            prefix = "before" if phase == "before" else "after"
            require(
                row["status"] == expected[f"{prefix}_status"]
                and sql_int(row, "version") == expected[f"{prefix}_version"],
                "SQL scope status/version differs from full snapshot",
            )
            require(
                row["receipt_outcome"]
                == ("" if phase == "before" else expected["outcome"]),
                "SQL scope receipt outcome differs from operator stdout",
            )
            require(
                re.fullmatch(r"[0-9a-f]{32}", row["row_md5"]), "Invalid SQL scope hash"
            )
            scope[key] = row
        require(
            set(scope) == set(expected_scope),
            "SQL scope does not cover the exact manifest subset",
        )
        scope_maps.append(scope)
        protected = unique(
            data.get("protected_groups", []), "bucket", "SQL protected bucket"
        )
        counts = {
            "all_hotel_products_unchanged": 60,
            "initial_approved_products_40": 40,
            "initial_approved_options_255": 255,
            "all_non_scope_hotel_options": 360
            - sum(k[0] == "option" for k in expected_scope),
        }
        require(
            set(protected)
            == set(counts) | {"all_non_hotel_products", "all_non_hotel_options"},
            "SQL protected-group coverage is incomplete",
        )
        for bucket, expected in counts.items():
            row = protected[bucket]
            require(
                sql_int(row, "rows") == sql_int(row, "expected_rows") == expected
                and row["count_matches"] == "t",
                f"SQL protected membership differs: {bucket}",
            )
    for key, expected in expected_scope.items():
        if expected["outcome"] == "hold":
            require(
                scope_maps[0][key]["row_md5"]
                == scope_maps[1][key]["row_md5"]
                == scope_maps[2][key]["row_md5"],
                "SQL hold target hash changed",
            )
    require(
        timestamp(only(before, "snapshot")["captured_at"])
        <= timestamp(only(after, "snapshot")["captured_at"])
        <= timestamp(only(replay, "snapshot")["captured_at"]),
        "SQL phase timestamps are unordered",
    )
    for section in UNCHANGED_SQL_SECTIONS:
        require(
            section in before and section in after and section in replay,
            f"Required SQL protected-table evidence missing: {section}",
        )
        require(
            canonical_rows(before[section])
            == canonical_rows(after[section])
            == canonical_rows(replay[section]),
            f"Protected SQL section changed: {section}",
        )
    previous_sections = {
        k for k in before if k.startswith("previous_") and "receipt" in k
    }
    require(previous_sections, "Previous review receipt preservation evidence missing")
    for section in previous_sections:
        require(
            canonical_rows(before[section])
            == canonical_rows(after.get(section, []))
            == canonical_rows(replay.get(section, [])),
            "Prior batch receipt rows changed",
        )
        require(
            all(r.get("unchanged") == "t" for r in before[section]),
            "Prior receipts differ from their pinned fingerprints",
        )
    require(
        sql_int(only(before, "receipt_totals"), "rows") == 0,
        "This batch already had receipts before apply",
    )
    for phase, data in (("before", before), ("after", after), ("after-replay", replay)):
        total = only(data, "receipt_totals")
        expected_count = 0 if phase == "before" else count
        require(
            sql_int(total, "expected_final_rows") == count
            and sql_int(total, "expected_now_rows") == expected_count
            and sql_int(total, "rows")
            == sql_int(total, "distinct_targets")
            == sql_int(total, "root_actor_rows")
            == expected_count,
            "SQL receipt count/actor mismatch",
        )
        require(
            sql_int(total, "distinct_actors") == (1 if expected_count else 0)
            and all(
                sql_int(total, k) == 0
                for k in (
                    "duplicate_targets",
                    "null_actor_rows",
                    "invalid_provenance_rows",
                    "non_scope_receipt_rows",
                )
            ),
            "SQL duplicate receipt or provenance mismatch",
        )
        require(
            sql_int(total, "approved_rows") == (0 if phase == "before" else approved)
            and sql_int(total, "approved_edit_rows")
            == (0 if phase == "before" else edited),
            "SQL successful review/edit receipt counts differ",
        )
        groups = Counter()
        for row in data.get("receipt_outcomes", []):
            require(sql_int(row, "changed_hold_rows") == 0, "SQL found a changed hold")
            groups[
                (
                    row["kind"],
                    row["requested_decision"],
                    row["outcome"],
                    row["guard_code"],
                )
            ] += sql_int(row, "rows")
        expected = (
            Counter()
            if phase == "before"
            else Counter(
                {
                    (
                        r["kind"],
                        r["requested_decision"],
                        r["outcome"],
                        r["guard_code"],
                    ): r["rows"]
                    for r in row_report["expected_sql_receipt_outcomes"]
                }
            )
        )
        require(
            groups == expected,
            "SQL receipt outcomes differ from actual operator stdout",
        )
        audits = unique(
            data.get("normal_service_audits_since_baseline", []),
            "action",
            "SQL normal action",
        )
        require(
            set(audits) == NORMAL_ACTIONS, "SQL normal audit action coverage incomplete"
        )
        for action, addition in row_report["expected_normal_audit_additions"].items():
            row, expected = audits[action], 0 if phase == "before" else addition
            require(
                sql_int(row, "rows")
                == sql_int(row, "expected_rows")
                == sql_int(row, "root_actor_rows")
                == expected
                and row["count_matches"] == "t"
                and sql_int(row, "invalid_actor_rows") == 0
                and sql_int(row, "non_scope_rows") == 0,
                f"Normal audit count/actor/target differs: {phase}/{action}",
            )
    require(set(after) == set(replay), "SQL after/replay section coverage differs")
    for section in set(after) - {"snapshot"}:
        require(
            canonical_rows(after[section]) == canonical_rows(replay[section]),
            f"Replay changed SQL rows, settings, receipts or audit hashes: {section}",
        )
    return {
        "receipt_count": count,
        "receipt_outcomes_match_stdout": True,
        "normal_audit_additions": row_report["expected_normal_audit_additions"],
        "normal_audit_actor_and_target_provenance": True,
        "per_target_versions_and_hold_hashes_match": True,
        "prior_receipts_and_all_historical_audits_unchanged": True,
        "settings_brands_offers_clicks_unchanged": True,
        "replay_zero_additions_and_all_nonclock_hashes_unchanged": True,
    }


def verify(directory, require_complete=False):
    required = ("before.json", "manifest.json", "apply.ndjson", "final-snapshot.json")
    optional = (
        "replay.ndjson",
        "dry-run.ndjson",
        "verify.json",
        "public-before.json",
        "public-after.json",
        "public-after-replay.json",
        "independent-before.txt",
        "independent-after.txt",
        "independent-after-replay.txt",
    )
    data, used, missing = {}, [], []
    for name in (*required, *optional):
        path = directory / name
        if not path.exists():
            require(name not in required, f"Required local artifact missing: {name}")
            missing.append(name)
            continue
        data[name] = (
            read_psql(path)
            if name.endswith(".txt")
            else read_jsonl(path)
            if name.endswith(".ndjson")
            else read_json(path)
        )
        used.append(name)
    rows = verify_rows(
        data["before.json"],
        data["manifest.json"],
        data["apply.ndjson"],
        data["final-snapshot.json"],
        data.get("replay.ndjson"),
        data.get("dry-run.ndjson"),
    )
    if "verify.json" in data:
        require(
            data["verify.json"]
            == {
                "verified": rows["manifest_entries"],
                "untouched_rows": 420 - rows["manifest_entries"],
                "catalog_rows": 420,
                "configs_unchanged": True,
                "approved": rows["actual_outcomes"].get("approved", 0),
                "hold": rows["actual_outcomes"].get("hold", 0),
            },
            "Operator verify summary differs from independently checked actual outcomes",
        )
    public = {}
    for phase, snapshot in (
        ("before", data["before.json"]),
        ("after", data["final-snapshot.json"]),
        ("after-replay", data["final-snapshot.json"]),
    ):
        name = f"public-{phase}.json"
        if name in data:
            public[phase] = verify_public(data[name], snapshot, phase)
    if "public-before.json" in data and "public-after.json" in data:
        public["delta"] = verify_public_delta(
            data["public-before.json"],
            data["public-after.json"],
            rows,
            data["final-snapshot.json"],
        )
    if "public-after.json" in data and "public-after-replay.json" in data:
        for field in (
            "public_products",
            "public_booking_options",
            "source_credit_sets",
        ):
            require(
                data["public-after.json"][field]
                == data["public-after-replay.json"][field],
                f"Public replay changed {field}",
            )
        public["replay_unchanged"] = True
    sql_names = (
        "independent-before.txt",
        "independent-after.txt",
        "independent-after-replay.txt",
    )
    sql = (
        verify_sql(*(data[name] for name in sql_names), rows)
        if all(name in data for name in sql_names)
        else None
    )
    # Public replay and dry-run are extra checks, not required for final acceptance.
    completion_required = {
        "replay.ndjson",
        "public-before.json",
        "public-after.json",
        *sql_names,
    }
    missing_required = sorted(completion_required - set(data))
    if require_complete:
        require(
            not missing_required,
            f"Final acceptance evidence missing: {missing_required}",
        )
    return {
        "schema_version": 1,
        "tag": TAG,
        "verified_at": datetime.now(UTC).isoformat(),
        "status": "partial" if missing_required else "passed",
        "final_acceptance": not missing_required,
        "verification_mode": "independent_local_stdlib_full_rows_actual_outcomes_public_and_sql",
        "production_access_by_verifier": False,
        "network_calls": 0,
        "database_connections": 0,
        "baseline_semantic_sha256": BASELINE_HASH,
        "manifest_semantic_sha256": digest(data["manifest.json"]),
        "rows": rows,
        "public": public,
        "independent_sql": sql,
        "missing_final_acceptance_evidence": missing_required,
        "missing_optional_artifacts": missing,
        "input_file_sha256": {
            name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
            for name in sorted(used)
        },
        "limitations": (
            "Verifies retained evidence, not unrecorded production activity; no live DB test."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directory", type=Path, default=Path(__file__).resolve().parent
    )
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument(
        "--output", type=Path, help="Optional exclusive-create JSON report path"
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
