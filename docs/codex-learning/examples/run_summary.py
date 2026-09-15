"""Run once, retain evidence, and accept only a validated practice summary."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

SCHEMA = {
    "type": "object",
    "properties": {
        "revision": {"type": "string"},
        "total": {"type": "integer", "minimum": 0},
        "completed": {"type": "integer", "minimum": 0},
        "pending": {"type": "integer", "minimum": 0},
    },
    "required": ["revision", "total", "completed", "pending"],
    "additionalProperties": False,
}
PROMPT = (
    "Read only tasks.md. Return its Revision marker and checkbox counts "
    "as revision, total, completed and pending. Do not edit input files "
    "or use external services."
)


def verify(run):
    status = json.loads((run / "status.json").read_text(encoding="utf-8"))
    if (not isinstance(status, dict)
            or status != {"state": "exited", "exit_code": 0}
            or type(status.get("exit_code")) is not int):
        raise ValueError("Process did not exit successfully")
    events = []
    for number, line in enumerate((run / "events.jsonl").read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        event = json.loads(line)
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            raise ValueError(f"Invalid event on line {number}")
        events.append(event["type"])
    if (events.count("turn.completed") != 1 or events.count("turn.started") != 1
            or events.index("turn.started") > events.index("turn.completed")):
        raise ValueError("Missing or ambiguous completed turn")
    if "turn.failed" in events or "error" in events:
        raise ValueError("Failure event requires investigation")
    result = json.loads((run / "final.json").read_text(encoding="utf-8-sig"))
    if not isinstance(result, dict) or set(result) != set(SCHEMA["required"]):
        raise ValueError("Unexpected or missing final fields")
    if result["revision"] != "exec-practice-1":
        raise ValueError("Unexpected input revision")
    if any(type(result[key]) is not int or result[key] < 0 for key in ("total", "completed", "pending")):
        raise ValueError("Counts must be nonnegative integers, not booleans")
    if result["total"] != result["completed"] + result["pending"]:
        raise ValueError("Inconsistent count arithmetic")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_name")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    if Path(args.run_name).name != args.run_name or args.run_name in {".", ".."}:
        parser.error("Use a folder name, not a path")
    run = root / args.run_name
    if not args.verify_only:
        if not (root / "tasks.md").is_file():
            parser.error("Missing tasks.md in the current folder")
        run.mkdir()  # Refuse to overwrite an earlier run.
        schema_path = run / "schema.json"
        schema_path.write_text(json.dumps(SCHEMA, indent=2) + "\n", encoding="utf-8")
        status_path = run / "status.json"
        status_path.write_text(json.dumps({"state": "running"}) + "\n", encoding="utf-8")
        command = ["codex", "exec", "--sandbox", "read-only", "--ephemeral", "--json",
                   "--output-schema", str(schema_path), "-o", str(run / "final.json"), PROMPT]
        try:
            with (run / "events.jsonl").open("xb") as stdout, (run / "stderr.log").open("xb") as stderr:
                process = subprocess.run(command, cwd=root, stdout=stdout, stderr=stderr, timeout=120, check=False)
            status = {"state": "exited", "exit_code": process.returncode}
        except subprocess.TimeoutExpired:
            status = {"state": "timeout"}
        except OSError:
            status = {"state": "launch_failed"}
        status_path.write_text(json.dumps(status) + "\n", encoding="utf-8")
    result = verify(run)
    # Output data only: never execute text returned by the model.
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"Not accepted: {error}", file=sys.stderr)
        sys.exit(1)
