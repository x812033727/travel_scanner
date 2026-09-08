"""Capture only anonymous hotel catalog GETs; never quote, click, or mutate.

Run from any directory with the canonical Python runtime:
  python -B capture_public.py --phase before
  python -B capture_public.py --phase after --manifest manifest.json
  python -B capture_public.py --phase after-replay --manifest manifest.json

Outputs are exclusive-create JSON files beside this script. Six workers execute
the fixed 30-request matrix. No retries, auth, cookies, redirects, API imports,
database connections, booking URLs, or provider calls are used.
"""

import argparse
import hashlib
import json
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

CITIES = ("tokyo", "osaka", "kyoto", "seoul", "busan", "taipei")
LOCALES = ("en", "ja", "ko", "zh-TW", "zh-CN")
ORIGIN = "https://mokaair.com"
TAG = "hotel-review-remaining-20260909"
BASELINE_HASH = "c938d83913645ac6a7651eca0e705621b33b40bb235905392c54917492bdb03d"
BASELINE_FILE_SHA256 = "bb71358eb2c9bc797b55d808939d0374aacd2b04a263a92609b8cc4f98dc6c60"
MAX_RESPONSE_BYTES = 2_000_000
PRICES = ("reference_price", "currency", "price_checked_at")
CREDIT_FIELDS = {"title", "publisher", "url", "license_name", "license_url", "changes"}


def now():
    return datetime.now(UTC).isoformat()


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def capture(pair):
    city, locale = pair
    url = f"{ORIGIN}/api/travel/travel-services?destination_id={city}&type=hotel"
    result = {
        "destination_id": city,
        "locale": locale,
        "started_at": now(),
        "url": url,
        "http_status": None,
        "cache_control": None,
        "content_type": None,
        "enabled": None,
        "items": [],
        "issues": [],
    }
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "X-Travel-Locale": locale,
            "Accept-Language": locale,
            "Cache-Control": "no-cache",
            "User-Agent": "MokaairReadOnlyPublicHotelReview/20260909",
        },
        method="GET",
    )
    # A new opener per request has no cookie jar or auth handler. Disable proxy
    # environment discovery so no ambient proxy credentials can be forwarded.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(request, timeout=25) as response:
            result["http_status"] = response.status
            result["cache_control"] = response.headers.get("Cache-Control")
            result["content_type"] = response.headers.get("Content-Type")
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                raise ValueError("Response exceeds the bounded capture size")
            payload = json.loads(body)
        if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
            raise ValueError("Invalid public response structure")
        if not isinstance(payload.get("enabled"), bool):
            raise ValueError("Invalid enabled status")
        result["enabled"] = payload["enabled"]
        result["enabled_kinds"] = payload.get("enabled_kinds")
        result["reported_total"] = payload.get("total")
        if payload.get("destination_id") != city:
            result["issues"].append("destination_mismatch")
        for item in payload["items"]:
            if not isinstance(item, dict) or not isinstance(item.get("facts"), dict):
                raise ValueError("Invalid public item structure")
            facts = item["facts"]
            if not isinstance(facts.get("source_credits"), list) or not isinstance(
                item.get("booking_options"), list
            ):
                raise ValueError("Invalid public credit or booking option structure")
            # Do not retain unexpected source-credit fields in local evidence.
            # This is an allowlist check, not a dump of malformed public content.
            for credit in facts["source_credits"]:
                if not isinstance(credit, dict) or set(credit) != CREDIT_FIELDS:
                    raise ValueError("Invalid source credit fields")
                if not all(isinstance(v, str) for v in credit.values()):
                    raise ValueError("Invalid source credit value types")
            for option in item["booking_options"]:
                if not isinstance(option, dict):
                    raise ValueError("Invalid booking option structure")
            # Required keys are indexed, not defaulted to null: a missing price
            # field must not be misrepresented as an explicitly unknown price.
            compact = {
                "id": item["id"],
                "kind": item["kind"],
                "destination_id": item["destination_id"],
                "title": item["title"],
                "source_url": item["source_url"],
                "source_credits": facts["source_credits"],
                **{field: facts[field] for field in PRICES},
                "booking_options": [
                    {
                        "id": option["id"],
                        "provider": option["provider"],
                        "name": option.get("name"),
                        "mode": option.get("mode"),
                        "quote_status": option.get("quote_status"),
                    }
                    for option in item["booking_options"]
                ],
            }
            result["items"].append(compact)
            if compact["kind"] != "hotel" or compact["destination_id"] != city:
                result["issues"].append(f"non_hotel_or_wrong_city:{item['id']}")
            if any(compact[field] is not None for field in PRICES):
                result["issues"].append(f"non_null_price:{item['id']}")
            if not compact["title"] or not compact["source_credits"]:
                result["issues"].append(f"missing_title_or_credit:{item['id']}")
            for credit in compact["source_credits"]:
                if set(credit) != CREDIT_FIELDS or not all(
                    isinstance(value, str) and value.strip()
                    for value in credit.values()
                ):
                    result["issues"].append(f"invalid_source_credit:{item['id']}")
                if not all(
                    str(credit.get(key, "")).startswith("https://")
                    for key in ("url", "license_url")
                ):
                    result["issues"].append(f"non_https_credit:{item['id']}")
        if "application/json" not in (result["content_type"] or "").lower():
            result["issues"].append("non_json_content_type")
        if result["reported_total"] != len(result["items"]):
            result["issues"].append("reported_total_mismatch_or_truncation")
        if result["http_status"] != 200:
            result["issues"].append("non_200_response")
        if "no-store" not in (result["cache_control"] or "").lower():
            result["issues"].append("no_store_missing")
        if result["enabled"] is not True:
            result["issues"].append("city_disabled")
    except urllib.error.HTTPError as exc:
        result["http_status"] = exc.code
        result["cache_control"] = exc.headers.get("Cache-Control")
        result["content_type"] = exc.headers.get("Content-Type")
        result["issues"].append(f"http_error:{exc.code}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result["issues"].append(f"capture_error:{type(exc).__name__}")
    result["completed_at"] = now()
    return result


def summarize(phase, results, started_at, contract=None):
    products, options, credits, checks = {}, {}, {}, []
    issues = []
    by_city = {}
    for response in results:
        city, locale = response["destination_id"], response["locale"]
        item_ids, option_ids = [], []
        for item in response["items"]:
            item_ids.append(item["id"])
            credit_hash = digest(item["source_credits"])
            credits[credit_hash] = item["source_credits"]
            row = {
                key: item[key]
                for key in ("id", "kind", "destination_id", "source_url", *PRICES)
            }
            row["source_credit_set_sha256"] = credit_hash
            row["booking_option_ids"] = [
                option["id"] for option in item["booking_options"]
            ]
            previous = products.get(item["id"])
            if (
                previous is not None
                and {k: v for k, v in previous.items() if k != "titles_by_locale"}
                != row
            ):
                issues.append(f"cross_locale_product_change:{item['id']}:{locale}")
            if previous is None:
                products[item["id"]] = {**row, "titles_by_locale": {}}
            products[item["id"]]["titles_by_locale"][locale] = item["title"]
            for option in item["booking_options"]:
                option_ids.append(option["id"])
                option_row = {"product_id": item["id"], **option}
                if option["id"] in options and options[option["id"]] != option_row:
                    issues.append(f"cross_locale_option_change:{option['id']}:{locale}")
                options[option["id"]] = option_row
        check = {key: value for key, value in response.items() if key != "items"}
        check.update(
            {
                "item_count": len(item_ids),
                "booking_option_count": len(option_ids),
                "item_ids": item_ids,
                "booking_option_ids": option_ids,
                "item_ids_sha256": digest(sorted(item_ids)),
                "booking_option_ids_sha256": digest(sorted(option_ids)),
            }
        )
        if len(set(item_ids)) != len(item_ids) or len(set(option_ids)) != len(
            option_ids
        ):
            check["issues"].append("duplicate_public_ids")
        check["all_checks_pass"] = not check["issues"]
        checks.append(check)
        entry = by_city.setdefault(
            city,
            {
                "enabled_by_locale": {},
                "counts_by_locale": {},
                "option_counts_by_locale": {},
            },
        )
        entry["enabled_by_locale"][locale] = response["enabled"]
        entry["counts_by_locale"][locale] = len(item_ids)
        entry["option_counts_by_locale"][locale] = len(option_ids)
    for product in products.values():
        if set(product["titles_by_locale"]) != set(LOCALES):
            issues.append(f"missing_locale:{product['id']}")
    if phase == "before" and (len(products), len(options)) != (40, 183):
        issues.append("before_expected_40_products_183_options_mismatch")
    if contract is not None:
        issues.extend(check_local_contract(phase, products, options, contract))
    return {
        "schema_version": 2,
        "tag": TAG,
        "phase": phase,
        "local_contract": None if contract is None else {
            "baseline_sha256": BASELINE_FILE_SHA256,
            "manifest_sha256": contract["manifest_sha256"],
            "pending_option_visibility_check": (
                "baseline" if phase == "before" else
                "manifest_allowlist" if contract["manifest_sha256"] else
                "not_assessed_capture_only_without_manifest"
            ),
            "after_count_assumption": None,
        },
        "started_at": started_at,
        "completed_at": now(),
        "method": "anonymous_public_GET_only",
        "matrix_requests_retained": len(results),
        "total_http_gets_in_this_check": len(results),
        "credentials_sent": False,
        "cookies_sent": False,
        "redirects_followed": 0,
        "quote_calls": 0,
        "clickout_calls": 0,
        "mutating_api_calls": 0,
        "database_connections": 0,
        "locale_headers": "X-Travel-Locale and Accept-Language match the five requested locales.",
        "summary": {
            "http_200": sum(r["http_status"] == 200 for r in results),
            "no_store_responses": sum(
                "no-store" in (r["cache_control"] or "").lower() for r in results
            ),
            "all_checks_pass": not issues and all(c["all_checks_pass"] for c in checks),
            "unique_public_products": len(products),
            "unique_public_booking_options": len(options),
            "issues": issues,
            "by_city": by_city,
        },
        "checks": checks,
        "public_products": sorted(
            products.values(), key=lambda r: (r["destination_id"], r["id"])
        ),
        "public_booking_options": sorted(options.values(), key=lambda r: r["id"]),
        "source_credit_sets": credits,
        "interpretation": (
            "Null price fields mean unknown/not quoted, not free. Locale titles may use "
            "existing original-name fallback. This matrix is not an atomic database "
            "snapshot; cross-locale differences are reported."
        ),
    }


def load_local_contract(manifest_path=None):
    """Only read local pinned evidence; never import an API/database module."""
    baseline_path = Path(__file__).resolve().parent / "before.json"
    raw = baseline_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != BASELINE_FILE_SHA256:
        raise ValueError("Pinned local baseline file changed")
    baseline = json.loads(raw)
    if digest(baseline) != BASELINE_HASH:
        raise ValueError("Pinned local baseline semantic hash changed")
    products = {row["id"]: row for row in baseline["products"]}
    options = {row["id"]: row for row in baseline["options"]}
    if len(products) != 60 or len(options) != 360:
        raise ValueError("Unexpected local baseline inventory")
    if sum(p["status"] == "approved" for p in products.values()) != 40:
        raise ValueError("Unexpected baseline approved products")
    if sum(o["status"] == "approved" for o in options.values()) != 255:
        raise ValueError("Unexpected baseline approved options")
    contract = {
        "products": products,
        "options": options,
        "manifest_sha256": None,
        "manifest_approved_option_ids": set(),
    }
    if manifest_path is None:
        return contract
    manifest_raw = Path(manifest_path).read_bytes()
    manifest = json.loads(manifest_raw)
    if manifest.get("tag") != TAG or manifest.get("baseline_hash") != BASELINE_HASH:
        raise ValueError("Manifest does not match the pinned review scope")
    decisions = manifest.get("decisions")
    if not isinstance(decisions, list) or not 1 <= len(decisions) <= 125:
        raise ValueError("Invalid manifest decision count")
    seen = set()
    for entry in decisions:
        kind, ident = entry["kind"], entry["id"]
        if (kind, ident) in seen or kind not in ("product", "option"):
            raise ValueError("Unknown or repeated manifest target")
        seen.add((kind, ident))
        row = (products if kind == "product" else options).get(ident)
        if row is None or row["status"] != "pending" or row["version"] != entry["version"]:
            raise ValueError("Manifest target is not a version-matched pending baseline row")
        if entry["decision"] not in ("approve", "hold"):
            raise ValueError("Unknown manifest decision")
        if kind == "product" and entry["decision"] != "hold":
            raise ValueError("This capture contract permits no product changes")
        if kind == "option" and entry["decision"] == "approve":
            contract["manifest_approved_option_ids"].add(ident)
    contract["manifest_sha256"] = hashlib.sha256(manifest_raw).hexdigest()
    return contract


def check_local_contract(phase, products, options, contract):
    """Do not assume that every approved decision passed a normal route guard."""
    issues = []
    baseline_products, baseline_options = contract["products"], contract["options"]
    expected_products = {
        ident for ident, row in baseline_products.items() if row["status"] == "approved"
    }
    if set(products) != expected_products:
        issues.append("public_products_differ_from_unchanged_40_approved_baseline")
    for ident, product in products.items():
        original = baseline_products.get(ident)
        if original is None or original["status"] != "approved":
            issues.append(f"unknown_or_pending_parent_public:{ident}")
            continue
        if product["source_url"] != original["source_url"]:
            issues.append(f"changed_public_source_url:{ident}")
        if product["source_credit_set_sha256"] != digest(original["facts"]["source_credits"]):
            issues.append(f"changed_public_source_credits:{ident}")
    allowed_options = {
        ident for ident, row in baseline_options.items() if row["status"] == "approved"
    }
    if phase != "before":
        allowed_options |= contract["manifest_approved_option_ids"]
    for ident, option in options.items():
        original = baseline_options.get(ident)
        if original is None:
            issues.append(f"unknown_public_option:{ident}")
            continue
        if (
            original["product_id"] != option["product_id"]
            or original["provider"] != option["provider"]
        ):
            issues.append(f"public_option_identity_changed:{ident}")
        if option["product_id"] not in expected_products:
            issues.append(f"pending_parent_option_public:{ident}")
        if (phase == "before" or contract["manifest_sha256"]) and ident not in allowed_options:
            issues.append(f"pending_hold_or_out_of_manifest_option_public:{ident}")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phase", required=True, choices=("before", "after", "after-replay")
    )
    parser.add_argument(
        "--manifest", type=Path,
        help="Optional local manifest; exclude held and out-of-scope pending options.",
    )
    args = parser.parse_args()
    try:
        contract = load_local_contract(args.manifest)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(
            f"Local evidence validation failed: {type(exc).__name__}; no HTTP requests made"
        )
    output = Path(__file__).resolve().parent / f"public-{args.phase}.json"
    if output.exists():
        parser.error(f"Refusing to overwrite {output.name}; no HTTP requests made")
    started_at = now()
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(
            pool.map(capture, ((city, locale) for city in CITIES for locale in LOCALES))
        )
    report = summarize(args.phase, results, started_at, contract)
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"file": str(output), **report["summary"]}))
    return 0 if report["summary"]["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
