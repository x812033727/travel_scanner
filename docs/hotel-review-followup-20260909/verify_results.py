"""Independently verify downloaded evidence using only the Python standard library.

No API imports, database connections, network calls or source-file writes.
Run when all seven inputs are present: python -B verify_results.py
The output is exclusive-created only after every required check passes. Optional
--rows-only prints row/log results without writing a final verification report.
SQL independently verifies audit actors, other settings and prior receipt records.
"""

import argparse
import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

TAG = "hotel-review-followup-20260909"
BASELINE_HASH = "d9823e0996ad09ba14fe05b2e9a674544544d4dacb7b87d6fac288be5e51453c"
MANIFEST_HASH = "c7370067e1ab7a9bd30f4724ba91c7315dd17ac4c36a1fe032876e2af269eb2f"
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
}
CITIES = {"tokyo", "osaka", "kyoto", "seoul", "busan", "taipei"}
LOCALES = {"en", "ja", "ko", "zh-TW", "zh-CN"}
PRICE_FIELDS = {"reference_price", "currency", "price_checked_at"}
CREDIT_FIELDS = {"title", "publisher", "url", "license_name", "license_url", "changes"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path):
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def unique(rows, key, label):
    result = {}
    for row in rows:
        value = row[key]
        require(value not in result, f"Duplicate {label}: {value}")
        result[value] = row
    return result


def indexed(data):
    result = {}
    for kind, collection in (("product", "products"), ("option", "options")):
        for identifier, row in unique(data[collection], "id", collection).items():
            result[(kind, identifier)] = row
    return result


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Timestamp lacks timezone")
    return parsed


def target(entry):
    return f"{TAG}:{entry['kind']}:{entry['id']}"


def verify_rows(before, manifest, apply_log, replay_log, final):
    require(digest(before) == BASELINE_HASH, "Baseline semantic hash mismatch")
    require(digest(manifest) == MANIFEST_HASH, "Reviewed manifest semantic hash mismatch")
    require(
        manifest["tag"] == TAG and manifest["baseline_hash"] == BASELINE_HASH,
        "Manifest provenance mismatch",
    )
    initial, current = indexed(before), indexed(final)
    require(len(before["products"]) == len(final["products"]) == 60, "Product scope changed")
    require(len(before["options"]) == len(final["options"]) == 360, "Option scope changed")
    require(set(initial) == set(current), "Catalog membership changed")
    require(
        digest(sorted(before["configs"], key=lambda r: r["id"]))
        == digest(sorted(final["configs"], key=lambda r: r["id"])),
        "Configuration changed",
    )
    approved_before = {k for k, row in initial.items() if row["status"] == "approved"}
    require(len(approved_before) == 246, "Original approved-row count mismatch")
    entries = unique([{**e, "target": target(e)} for e in manifest["decisions"]], "target", "entry")
    applied = unique(apply_log, "target", "apply target")
    replayed = unique(replay_log, "target", "replay target")
    require(
        len(entries) == 67 and set(entries) == set(applied) == set(replayed),
        "Expected the exact 67 manifest/apply/replay targets",
    )
    receipt_ids = [r["receipt_id"] for r in applied.values()]
    require(len(set(receipt_ids)) == 67, "Receipt IDs are not unique")
    for receipt_id in receipt_ids:
        require(str(UUID(receipt_id)) == receipt_id, "Noncanonical receipt UUID")
    changed_fields, outcomes, guard_counts = Counter(), Counter(), Counter()
    changed_ids = []
    approved_targets = set()
    for name, entry in entries.items():
        key = (entry["kind"], entry["id"])
        old, new = initial[key], current[key]
        result, replay = applied[name], replayed[name]
        require(
            old["status"] == "pending" and key not in approved_before,
            "Selected a previously reviewed row",
        )
        require(
            entry["before_hash"] == digest(old) and entry["version"] == old["version"],
            "Entry baseline/version mismatch",
        )
        require(
            set(result) == {"target", "outcome", "receipt_id", "after_hash", "guard_code"},
            "Unexpected apply log fields",
        )
        require(
            set(replay) == {"target", "outcome", "receipt_id", "after_hash"},
            "Unexpected replay log fields",
        )
        require(
            replay["outcome"] == "replayed" and replay["receipt_id"] == result["receipt_id"],
            "Replay did not reuse its original receipt",
        )
        require(
            result["after_hash"] == replay["after_hash"] == digest(new),
            "Apply/replay/final row hash mismatch",
        )
        outcome, guard = result["outcome"], result["guard_code"]
        require(outcome in {"approved", "hold"}, "Nonterminal apply outcome")
        outcomes[f"{entry['kind']}:{outcome}"] += 1
        if outcome == "hold":
            require(old == new, "Hold changed its target row")
            if entry["decision"] == "approve":
                require(guard in KNOWN_GUARDS, "Unexpected approval fallback guard")
                guard_counts[guard] += 1
            else:
                require(entry["decision"] == "hold" and guard is None, "Invalid hold outcome")
            continue
        require(
            entry["kind"] == "option" and entry["decision"] == "approve" and guard is None,
            "Only requested independent option approvals may change rows",
        )
        require(
            entry["method"] == "iab" and entry["browser_verified"] is True,
            "Actual batch approval lacks its IAB evidence",
        )
        require(set(old) == set(new), "Option schema changed")
        fields = {field for field in old if old[field] != new[field]}
        require(fields <= ALLOWED_OPTION_FIELDS, f"Immutable option fields changed: {fields}")
        require(
            type(new["version"]) is int
            and new["version"] == old["version"] + 1
            and new["status"] == "approved",
            "Incorrect approval status/version increment",
        )
        require(
            new["identity_note"] == entry["identity_note"], "Identity note differs from evidence"
        )
        require(new["health_status"] in {"healthy", "unconfirmed"}, "Unsafe approval health result")
        for field in ("verified_at", "checked_at", "updated_at"):
            require(
                timestamp(before["captured_at"])
                <= timestamp(new[field])
                <= timestamp(final["captured_at"]),
                f"Invalid approval {field}",
            )
        changed_fields.update(fields)
        changed_ids.append(entry["id"])
        approved_targets.add(key)
    for key, old in initial.items():
        if key not in approved_targets:
            require(old == current[key], f"Non-approved-target full row changed: {key}")
    require(
        all(initial[k] == current[k] for k in initial if k[0] == "product"),
        "A hotel product changed despite this batch containing only product holds",
    )
    require(
        all(initial[k] == current[k] for k in approved_before),
        "A previously approved product or option changed",
    )
    return {
        "catalog_rows": len(initial),
        "all_60_products_unchanged": True,
        "original_246_approved_unchanged": True,
        "configs_unchanged": True,
        "untouched_rows": len(initial) - len(approved_targets),
        "manifest_entries": len(entries),
        "unique_receipts": len(receipt_ids),
        "replay_same_receipts_and_hashes": True,
        "apply_final_hashes_match": True,
        "actual_outcomes": dict(sorted(outcomes.items())),
        "guard_fallbacks": dict(sorted(guard_counts.items())),
        "approved_option_ids": sorted(changed_ids),
        "changed_field_counts": dict(sorted(changed_fields.items())),
        "final_status_counts": dict(
            sorted(Counter(f"{kind}:{r['status']}" for (kind, _), r in current.items()).items())
        ),
    }


def verify_public(report, snapshot, phase):
    require(
        report["phase"] == phase and report["method"] == "anonymous_public_GET_only",
        "Public capture phase/method mismatch",
    )
    for field in ("credentials_sent", "cookies_sent"):
        require(report[field] is False, "Public capture used credentials/cookies")
    for field in (
        "redirects_followed",
        "quote_calls",
        "clickout_calls",
        "mutating_api_calls",
        "database_connections",
    ):
        require(report[field] == 0, "Public capture exceeded read-only scope")
    require(
        report["matrix_requests_retained"] == report["total_http_gets_in_this_check"] == 30,
        "Public matrix request count mismatch",
    )
    require(
        report["summary"]["all_checks_pass"] is True and not report["summary"]["issues"],
        "Public capture reported problems",
    )
    source_products = unique(snapshot["products"], "id", "snapshot product")
    source_options = unique(snapshot["options"], "id", "snapshot option")
    expected_products = {i for i, r in source_products.items() if r["status"] == "approved"}
    expected_options = {
        i
        for i, r in source_options.items()
        if r["status"] == "approved" and r["product_id"] in expected_products
    }
    products = unique(report["public_products"], "id", "public product")
    options = unique(report["public_booking_options"], "id", "public option")
    require(set(products) == expected_products, "Public approved-product membership mismatch")
    require(set(options) == expected_options, "Public approved-option/parent membership mismatch")
    require(
        report["summary"]["unique_public_products"] == len(products)
        and report["summary"]["unique_public_booking_options"] == len(options),
        "Public summary count mismatch",
    )
    credits = report["source_credit_sets"]
    used_credits = set()
    for identifier, row in products.items():
        original = source_products[identifier]
        require(
            row["kind"] == "hotel"
            and row["destination_id"] == original["destination_id"]
            and row["source_url"] == original["source_url"],
            "Public product identity changed",
        )
        require(
            PRICE_FIELDS <= set(row) and all(row[field] is None for field in PRICE_FIELDS),
            "Price keys must be present and explicitly unknown, not free",
        )
        require(set(row["titles_by_locale"]) == LOCALES, "Missing localized public title")
        require(
            all(
                row["titles_by_locale"][loc]
                == (original["names_json"].get(loc) or original["title"])
                for loc in LOCALES
            ),
            "Public title/original fallback mismatch",
        )
        credit_hash = row["source_credit_set_sha256"]
        used_credits.add(credit_hash)
        require(
            credit_hash in credits
            and digest(credits[credit_hash]) == credit_hash
            and credits[credit_hash] == original["facts"]["source_credits"],
            "Public source credit or attribution hash changed",
        )
        for credit in credits[credit_hash]:
            require(
                set(credit) == CREDIT_FIELDS
                and all(isinstance(v, str) and v.strip() for v in credit.values()),
                "Invalid public credit shape",
            )
            require(
                all(credit[k].startswith("https://") for k in ("url", "license_url")),
                "Non-HTTPS public source attribution",
            )
        expected = {i for i in expected_options if source_options[i]["product_id"] == identifier}
        require(
            len(row["booking_option_ids"]) == len(set(row["booking_option_ids"]))
            and set(row["booking_option_ids"]) == expected,
            "Product option membership mismatch",
        )
    require(used_credits == set(credits), "Unused or missing public attribution set")
    for identifier, row in options.items():
        original = source_options[identifier]
        require(
            row["product_id"] == original["product_id"] and row["provider"] == original["provider"],
            "Public option identity/provider mismatch",
        )
        require(
            row["mode"] == "direct" and row["quote_status"] == "not_configured",
            "Unexpected affiliate or quote activation",
        )
    pairs = set()
    for check in report["checks"]:
        pair = (check["destination_id"], check["locale"])
        require(
            pair not in pairs and pair[0] in CITIES and pair[1] in LOCALES,
            "Duplicate or unexpected public city/locale",
        )
        pairs.add(pair)
        require(
            check["http_status"] == 200
            and check["enabled"] is True
            and "no-store" in (check["cache_control"] or "").lower()
            and not check["issues"]
            and check["all_checks_pass"] is True,
            "Public response HTTP/cache/enabled/issue check failed",
        )
        city_products = {i for i in products if products[i]["destination_id"] == pair[0]}
        city_options = {i for i in options if options[i]["product_id"] in city_products}
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
        require(check["reported_total"] == len(city_products), "Public result was truncated")
    require(
        pairs == {(city, loc) for city in CITIES for loc in LOCALES}, "Incomplete public matrix"
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
        "held_parents_and_options_hidden": True,
        "source_credits_unchanged": True,
        "prices_explicitly_unknown": True,
    }


def verify(directory, rows_only=False):
    names = ["before.json", "manifest.json", "apply.jsonl", "replay.jsonl", "final-snapshot.json"]
    data = {
        name: read_jsonl(directory / name)
        if name.endswith(".jsonl")
        else read_json(directory / name)
        for name in names
    }
    row_report = verify_rows(*(data[name] for name in names))
    if rows_only:
        return {"status": "rows_and_logs_only", "final_acceptance": False, "rows": row_report}
    public = {}
    for phase, snapshot in (
        ("before", data["before.json"]),
        ("after", data["final-snapshot.json"]),
    ):
        name = f"public-{phase}.json"
        data[name] = read_json(directory / name)
        public[phase] = verify_public(data[name], snapshot, phase)
    return {
        "schema_version": 1,
        "tag": TAG,
        "verified_at": datetime.now(UTC).isoformat(),
        "status": "passed",
        "verification_mode": "independent_offline_full_row_and_public_comparison",
        "production_access_by_verifier": False,
        "network_calls": 0,
        "database_connections": 0,
        "baseline_semantic_sha256": BASELINE_HASH,
        "manifest_semantic_sha256": MANIFEST_HASH,
        "rows": row_report,
        "public": public,
        "input_file_sha256": {
            name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
            for name in sorted(data)
        },
        "separate_sql_checks": (
            "Normal audit actors/counts, provider settings, prior receipts and related tables "
            "must be compared independently; this report does not claim those checks."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--rows-only", action="store_true")
    args = parser.parse_args()
    output = args.directory / "verification-report.json"
    if not args.rows_only and output.exists():
        parser.error("Refusing to overwrite an existing verification-report.json")
    report = verify(args.directory, args.rows_only)
    if not args.rows_only:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    print(json.dumps(report, ensure_ascii=True))


if __name__ == "__main__":
    main()
