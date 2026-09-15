"""Separate plan, submit, one status check, and explicit retry planning."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lablib import batch
from lablib.common import client_for, model_name, read_json, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["submit", "fetch", "reconcile", "merge", "cleanup"])
    parser.add_argument("--cases", type=Path, default=Path(__file__).parent.parent/"cases.jsonl")
    parser.add_argument("--results", type=Path, default=Path("results.jsonl"))
    parser.add_argument("--ledger", type=Path, default=Path("job-ledger.json"))
    parser.add_argument("--parent-ledger", type=Path, help="Required when submitting a retry; validates prior results and total attempts.")
    parser.add_argument("--summary", type=Path, default=Path("reconciliation.json"))
    parser.add_argument("--summaries", type=Path, nargs="+")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    if args.action == "merge":
        if not args.summaries:
            parser.error("--summaries required")
        result = batch.merge_accepted(batch.jsonl(args.cases), [read_json(p) for p in args.summaries])
        write_json(args.summary, result)
    elif args.action == "reconcile":
        cases = batch.jsonl(args.cases)
        result = batch.reconcile(cases, batch.jsonl(args.results))
        write_json(args.summary, result)
        retry = batch.retry_cases(cases, result)
        Path("retry-cases.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False)+"\n" for c in retry), encoding="utf-8")
    else:
        if not args.live:
            parser.error("--live required; submit creates one non-idempotent billable batch")
        with client_for("generateContent") as client:
            if args.action == "submit":
                result = batch.submit(client, args.cases, args.ledger, model_name(), parent_ledger=args.parent_ledger)
            elif args.action == "cleanup":
                result = batch.cleanup(client, args.ledger)
            else:
                result = batch.fetch(client, args.ledger, args.results)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
