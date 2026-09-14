"""Evaluate a running loopback service; --live permits at most the fixed twenty cases."""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lablib.common import read_json, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8765")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("service-evaluation.json"))
    args = parser.parse_args()
    url = urlsplit(args.url)
    if url.scheme != "http" or url.hostname != "127.0.0.1" or url.username or url.password or url.path not in {"", "/"} or url.query or url.fragment:
        parser.error("Use a loopback service URL.")
    rows = []
    with httpx.Client(base_url=args.url, timeout=20) as client:
        health = client.get("/health")
        health.raise_for_status()
        mode = health.json()["mode"]
        if mode != "author_fixture" and not args.live:
            parser.error("Service is live: --live explicitly allows the fixed evaluation requests.")
        for case in read_json(Path(__file__).parent.parent/"golden-cases.json"):
            reply = client.post("/ask", json={"question": case["question"]})
            result = reply.json()
            if case["expected_status"] == "invalid_input":
                passed = reply.status_code == 422
            else:
                passed = reply.status_code == 200 and result.get("status") == case["expected_status"]
                if case["expected_text"]:
                    passed = passed and case["expected_text"] in result.get("answer", "") and any(c.get("document_id") == case["expected_document"] for c in result.get("citations", []))
            rows.append({"key": case["key"], "http_status": reply.status_code, "passed": passed, "response": result})
            write_json(args.output, {"mode": mode, "checks": rows, "limitation": "matching values and source IDs are screening checks, not semantic proof"})
    print(json.dumps({"mode": mode, "passed": sum(r["passed"] for r in rows), "total": len(rows)}))


if __name__ == "__main__":
    main()
