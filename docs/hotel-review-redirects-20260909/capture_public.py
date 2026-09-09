"""Anonymous no-quote public checks for an unchanged, parent-gated catalog."""

import argparse
import hashlib
import importlib.util
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hotel-review-remaining-20260909/capture_public.py"
SOURCE_HASH = "ab6a1a60da665469e0108006461820f05bd366e7d40f6f8070157c230889b4de"
if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_HASH:
    raise RuntimeError("Read-only capture helper changed")
SPEC = importlib.util.spec_from_file_location("redirect_public_helper", SOURCE)
CAPTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CAPTURE)
TAG = "hotel-review-redirects-20260909"
BASELINE_HASH = "14978ec20e1b05f7f5991194c9568f56bb6da93486c91105ebc5391dc4fad56d"


def run(phase):
    baseline = json.loads((HERE / "before.json").read_text(encoding="utf-8"))
    if CAPTURE.digest(baseline) != BASELINE_HASH:
        raise ValueError("Wrong local baseline; no requests made")
    output = HERE / f"public-{phase}.json"
    if output.exists():
        raise ValueError("Exclusive evidence output already exists; no requests made")
    products = {p["id"]: p for p in baseline["products"] if p["status"] == "approved"}
    options = {
        o["id"]: o for o in baseline["options"]
        if o["status"] == "approved" and o["product_id"] in products
    }
    if len(products) != 40 or len(options) != 192:
        raise ValueError("Unexpected baseline public membership")
    started = CAPTURE.now()
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(
            CAPTURE.capture, ((c, loc) for c in CAPTURE.CITIES for loc in CAPTURE.LOCALES)
        ))
    responses = []
    for result in results:
        city = result["destination_id"]
        pids = [p["id"] for p in result["items"]]
        oids = [o["id"] for p in result["items"] for o in p["booking_options"]]
        expected_pids = {i for i, p in products.items() if p["destination_id"] == city}
        expected_oids = {i for i, o in options.items() if o["product_id"] in expected_pids}
        issues = list(result["issues"])
        if len(pids) != len(set(pids)) or set(pids) != expected_pids:
            issues.append("public_product_membership_changed")
        if len(oids) != len(set(oids)) or set(oids) != expected_oids:
            issues.append("public_option_membership_changed")
        responses.append({
            "city": city, "locale": result["locale"],
            "http_status": result["http_status"], "cache_control": result["cache_control"],
            "started_at": result["started_at"], "completed_at": result["completed_at"],
            "issues": issues, "item_ids": sorted(pids), "booking_option_ids": sorted(oids),
            "body_hash": CAPTURE.digest(result["items"]),
        })
    summary = {
        "all_checks_pass": all(not r["issues"] for r in responses),
        "http_200": sum(r["http_status"] == 200 for r in responses),
        "no_store_responses": sum(
            "no-store" in (r["cache_control"] or "").lower() for r in responses
        ),
        "unique_public_products": len({i for r in responses for i in r["item_ids"]}),
        "unique_public_booking_options": len({
            i for r in responses for i in r["booking_option_ids"]
        }),
    }
    report = {
        "tag": TAG, "phase": phase, "method": "anonymous_public_GET_only",
        "baseline_hash": BASELINE_HASH, "started_at": started, "completed_at": CAPTURE.now(),
        "credentials_sent": False, "cookies_sent": False, "redirects_followed": 0,
        "quote_calls": 0, "clickout_calls": 0, "mutating_api_calls": 0,
        "database_connections": 0, "responses": responses, "summary": summary,
    }
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(summary))
    return 0 if summary["all_checks_pass"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, choices=["before", "after", "after-replay"])
    raise SystemExit(run(parser.parse_args().phase))
