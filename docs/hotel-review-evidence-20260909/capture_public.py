"""Capture anonymous catalog GETs only, retaining allowlisted public fields."""

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
    raise RuntimeError("Immutable public GET helper changed")
SPEC = importlib.util.spec_from_file_location("platform_public_helper", SOURCE)
CAPTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CAPTURE)
TAG = "hotel-review-evidence-20260909"
BASELINE_HASH = "342aee9610db65e78626d950efef368919a7d8e4cfcf55d06a32b64e26c5adee"
MANIFEST_FILE_SHA = "2a0b4c880d948c237822aba74194138d963977296f9fdd9abc0b1f41e1794d9e"


def run(phase):
    baseline = json.loads((HERE / "before.json").read_text(encoding="utf-8"))
    if CAPTURE.digest(baseline) != BASELINE_HASH:
        raise ValueError("Wrong local baseline; no requests made")
    raw = (HERE / "manifest.json").read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_FILE_SHA:
        raise ValueError("Wrong exact manifest; no requests made")
    manifest = json.loads(raw)
    output = HERE / f"public-{phase}.json"
    if output.exists():
        raise ValueError("Refusing to overwrite evidence; no requests made")
    products = {p["id"]: p for p in baseline["products"] if p["status"] == "approved"}
    options = {o["id"]: o for o in baseline["options"]}
    approved = {i for i, o in options.items() if o["status"] == "approved"}
    if len(products) != 40 or len(approved) != 300:
        raise ValueError("Unexpected baseline inventory")
    if phase != "before":
        results = [
            json.loads(line)
            for line in (HERE / "apply.ndjson").read_text().splitlines()
            if line.strip()
        ]
        expected = {f"{TAG}:{e['kind']}:{e['id']}" for e in manifest["decisions"]}
        if len(results) != len(expected) or {r["target"] for r in results} != expected:
            raise ValueError("Incomplete apply receipt coverage; no requests made")
        for result in results:
            if result["outcome"] not in {"approved", "hold"}:
                raise ValueError("Unexpected apply outcome")
            if result["outcome"] == "approved":
                kind, identifier = result["target"].rsplit(":", 2)[1:]
                if kind == "option":
                    approved.add(identifier)
                else:
                    snapshot = json.loads(
                        (HERE / "final-snapshot.json").read_text(encoding="utf-8")
                    )
                    found = [p for p in snapshot["products"] if p["id"] == identifier]
                    if len(found) != 1 or found[0]["status"] != "approved":
                        raise ValueError("Missing approved product result")
                    products[identifier] = found[0]
    expected_options = {i: options[i] for i in approved if options[i]["product_id"] in products}
    started = CAPTURE.now()
    with ThreadPoolExecutor(max_workers=6) as pool:
        captures = list(
            pool.map(CAPTURE.capture, ((c, loc) for c in CAPTURE.CITIES for loc in CAPTURE.LOCALES))
        )
    responses = []
    for result in captures:
        city = result["destination_id"]
        pids = [p["id"] for p in result["items"]]
        oids = [o["id"] for p in result["items"] for o in p["booking_options"]]
        expected_pids = {i for i, p in products.items() if p["destination_id"] == city}
        expected_oids = {i for i, o in expected_options.items() if o["product_id"] in expected_pids}
        issues = list(result["issues"])
        if len(pids) != len(set(pids)) or set(pids) != expected_pids:
            issues.append("public_product_membership_changed")
        if len(oids) != len(set(oids)) or set(oids) != expected_oids:
            issues.append("unexpected_public_option_membership")
        responses.append(
            {
                "city": city,
                "locale": result["locale"],
                "http_status": result["http_status"],
                "cache_control": result["cache_control"],
                "started_at": result["started_at"],
                "completed_at": result["completed_at"],
                "issues": issues,
                "item_ids": sorted(pids),
                "booking_option_ids": sorted(oids),
                "items": result["items"],
                "body_hash": CAPTURE.digest(result["items"]),
            }
        )
    summary = {
        "all_checks_pass": all(not r["issues"] for r in responses),
        "http_200": sum(r["http_status"] == 200 for r in responses),
        "no_store_responses": sum(
            "no-store" in (r["cache_control"] or "").lower() for r in responses
        ),
        "unique_public_products": len({i for r in responses for i in r["item_ids"]}),
        "unique_public_booking_options": len(
            {i for r in responses for i in r["booking_option_ids"]}
        ),
    }
    report = {
        "tag": TAG,
        "phase": phase,
        "method": "anonymous_public_GET_only",
        "baseline_hash": BASELINE_HASH,
        "manifest_file_sha256": MANIFEST_FILE_SHA,
        "started_at": started,
        "completed_at": CAPTURE.now(),
        "credentials_sent": False,
        "cookies_sent": False,
        "redirects_followed": 0,
        "quote_calls": 0,
        "clickout_calls": 0,
        "mutating_api_calls": 0,
        "database_connections": 0,
        "responses": responses,
        "summary": summary,
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
