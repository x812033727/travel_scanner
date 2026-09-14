"""Run one bounded synthetic-order conversation only with --live."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lablib.common import client_for, model_name, read_json, write_json
from lablib.function_loop import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("order-run.json"))
    args = parser.parse_args()
    if not args.live:
        parser.error("Use local tests first; --live sends up to three paid model requests.")
    with client_for("interactions") as client:
        result = run(client.interactions.create, args.question, read_json(Path(__file__).parent.parent/"orders.json"), model_name())
    write_json(args.output, result)
    print(json.dumps({"status": result["status"], "requests": len(result["trace"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
