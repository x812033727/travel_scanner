"""Explicit, one-action-at-a-time File Search lifecycle commands."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lablib import file_store
from lablib.common import client_for, model_name, serialized, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["create", "import", "poll", "query", "delete-document", "cleanup"])
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--ledger", type=Path, default=Path("resource-ledger.json"))
    parser.add_argument("--file", type=Path)
    parser.add_argument("--id", default="S001")
    parser.add_argument("--version", default="v1")
    parser.add_argument("--question", default="請說明 S001 的規格；只用目前來源，沒有證據時明說。")
    parser.add_argument("--output", type=Path, default=Path("file-search-response.json"))
    args = parser.parse_args()
    if not args.live:
        parser.error("--live can create or remove only resources recorded in this exercise ledger; check project and cost first.")
    family = "interactions" if args.action == "query" else "generateContent"
    with client_for(family) as client:
        if args.action == "create":
            result = file_store.create_store(client, args.ledger)
        elif args.action == "import":
            if not args.file:
                parser.error("--file required")
            result = file_store.import_document(client, args.ledger, args.file, args.id, args.version)
        elif args.action == "poll":
            result = file_store.poll_document(client, args.ledger, args.id, args.version)
        elif args.action == "delete-document":
            result = file_store.delete_document(client, args.ledger, args.id, args.version)
        elif args.action == "cleanup":
            file_store.cleanup(client, args.ledger)
            result = {"status": "cleaned"}
        else:
            result = serialized(file_store.query_store(client, args.ledger, args.question, model_name()))
            write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
