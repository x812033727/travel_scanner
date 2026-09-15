"""Explicit selection of API family; creating a cache never happens during import."""
import argparse
import sys
from pathlib import Path

import httpx
from google.genai.errors import APIError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lablib import cache_lab
from lablib.common import client_for, model_name, read_json, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["implicit", "create", "query", "delete"])
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--ledger", type=Path, default=Path("cache-ledger.json"))
    parser.add_argument("--output", type=Path, default=Path("cache-usage.json"))
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Choose a new output filename to preserve previous observations.")
    if not args.live:
        parser.error("--live required: cache creation/storage and model requests can incur charges.")
    folder = Path(__file__).parent
    family = "interactions" if args.action == "implicit" else "generateContent"
    try:
        with client_for(family) as client:
            if args.action == "implicit":
                result = cache_lab.implicit(client, folder/"document.txt", read_json(folder/"questions.json"), model_name(), args.output)
            elif args.action == "create":
                result = cache_lab.explicit_create(client, folder/"document.txt", model_name(), args.ledger)
            elif args.action == "query":
                result = cache_lab.explicit_query(client, args.ledger, "只列出前三個合成規格段落的識別碼。")
            else:
                cache_lab.explicit_delete(client, args.ledger)
                result = {"status": "deleted"}
    except (APIError, httpx.HTTPError, ValueError) as error:
        partial = read_json(args.output) if args.output.exists() else {}
        write_json(args.output, {**partial, "status": "request_failed", "action": args.action, "error_type": type(error).__name__, "code": getattr(error, "code", None), "bill": "not_measured"})
        raise SystemExit(1) from None
    write_json(args.output, result)
    print("Saved observation; compare actual billing separately.")


if __name__ == "__main__":
    main()
