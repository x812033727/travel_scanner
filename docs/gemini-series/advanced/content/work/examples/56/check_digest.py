"""Check dates/source coverage in an authored digest. Never creates a schedule or browses."""
import argparse
import json
from datetime import datetime
from pathlib import Path


def instant(value):
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timezone_required")
    return parsed


def check(value):
    start, end = instant(value["start"]), instant(value["end"])
    if start >= end:
        raise ValueError("invalid_period")
    allowed = set(value["allowed_sources"])
    if not allowed or len(allowed) != len(value["allowed_sources"]):
        raise ValueError("source_scope_must_be_nonempty_and_unique")
    states = value["sources"]
    if len({s["url"] for s in states}) != len(states) or {s["url"] for s in states} != allowed:
        raise ValueError("all_sources_must_be_accounted_for_once")
    if any(s["status"] not in {"read", "unavailable", "needs_date"} for s in states):
        raise ValueError("unknown_source_status")
    readable = {s["url"] for s in states if s["status"] == "read"}
    for item in value["items"]:
        if item["source"] not in readable:
            raise ValueError("item_has_no_read_source")
        if not start <= instant(item["published"]) < end:
            raise ValueError("item_outside_period")
        if any(not isinstance(item.get(k), str) or not item[k].strip() for k in ("title", "summary", "quote")):
            raise ValueError("missing_item_evidence")
    return {"dateAndCoverageCheck": "passed", "authoredFixture": value.get("authored_fixture") is True,
            "missingSources": sorted(allowed - readable), "semanticSourceReviewRequired": True,
            "scheduleCreated": False, "actualScheduledRunVerified": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("digest", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(json.loads(args.digest.read_text(encoding="utf-8"))), ensure_ascii=False, indent=2))
