"""Verify authored exec/JSON/CI examples without calling a model or GitHub workflow."""
import argparse
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/codex-learning/examples/run_summary.py"
spec = importlib.util.spec_from_file_location("practice_summary", SOURCE)
summary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(summary)
checks = []
parser = argparse.ArgumentParser()
parser.add_argument("--codex", help="Optional real CLI path; only help/version and an invalid flag are run")
args = parser.parse_args()
cli_probe = None
authors = {key: json.loads((ROOT / f"docs/codex-learning/deep/modules/{key}.json").read_text(encoding="utf-8")) for key in [26, 29, 30, 55, 56, 57]}
expected = {"revision": "exec-practice-1", "total": 3, "completed": 1, "pending": 2}
events = [{"type": "thread.started", "thread_id": "fictional-reference"}, {"type": "turn.started"},
          {"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps(expected)}},
          {"type": "turn.completed"}]
workflow_path = ROOT / "docs/codex-learning/examples/practice-codex.yml"
workflow = yaml.load(workflow_path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
for id_, source in [(55, SOURCE), (56, workflow_path)]:
    module = json.loads((ROOT / f"docs/codex-learning/deep/modules/{id_}.json").read_text(encoding="utf-8"))
    assert any(b.get("code") == source.read_text(encoding="utf-8") for b in module["blocks"])
checks.append("Rendered lesson programs exactly match the reference sources")

with tempfile.TemporaryDirectory(prefix="codex-exec-reference-") as temporary:
    root = Path(temporary).resolve()
    assert root.parent == Path(tempfile.gettempdir()).resolve()
    assert root.name.startswith("codex-exec-reference-")
    baseline = root / "run-01"
    baseline.mkdir()

    def write_case(path, *, result=expected, event_list=events, status=None):
        path.mkdir(exist_ok=True)
        (path / "status.json").write_text(json.dumps(status or {"state": "exited", "exit_code": 0}), encoding="utf-8")
        (path / "events.jsonl").write_text("\n".join(json.dumps(e) for e in event_list) + "\n", encoding="utf-8")
        (path / "final.json").write_text(json.dumps(result), encoding="utf-8")

    def rejected(path):
        try:
            summary.verify(path)
        except (OSError, ValueError):
            return
        raise AssertionError("Invalid case accepted: " + path.name)

    write_case(baseline)
    assert summary.verify(baseline) == expected
    checks.append("A synthetic single-turn JSONL stream and exact fixture answer are accepted")
    wrong = json.loads(next(b["code"] for b in authors[55]["blocks"] if b.get("label", [None])[0] == "run-wrong-counts/final.json：刻意錯誤的計數"))
    wrong_path = root / "run-wrong-counts"
    write_case(wrong_path, result=wrong)
    assert summary.verify(wrong_path) == wrong and wrong != expected
    verify_wrong = subprocess.run([sys.executable, str(SOURCE), wrong_path.name, "--verify-only"], cwd=root, capture_output=True, timeout=10, check=False)
    assert verify_wrong.returncode == 0 and json.loads(verify_wrong.stdout) == wrong
    assert summary.verify(baseline) == expected
    checks.append("The exact authored wrong-count answer passes structural verify-only but fails fixture truth; original evidence stays valid")
    browser_code = next(b["code"] for b in authors[26]["blocks"] if b.get("language") == "javascript")
    syntax = subprocess.run(["node", "--check", "--input-type=commonjs"], input=browser_code, text=True, capture_output=True, timeout=10, check=False)
    assert syntax.returncode == 0, syntax.stderr
    checks.append("The browser measurement parses as JavaScript only; no DOM, page, browser or preview was executed")
    if args.codex:
        version = subprocess.run([args.codex, "--version"], cwd=root, capture_output=True, text=True, timeout=20, check=False)
        help_result = subprocess.run([args.codex, "exec", "--help"], cwd=root, capture_output=True, text=True, timeout=20, check=False)
        assert version.returncode == help_result.returncode == 0
        for flag in ["--sandbox", "--ephemeral", "--json", "--output-schema", "--output-last-message"]:
            assert flag in help_result.stdout
        old_report = root / "report-01.md"
        old_report.write_text("Fictional previous answer; never a new model result.\n", encoding="utf-8")
        prior = {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()}
        invalid = subprocess.run([args.codex, "exec", "--sandbox", "invalid", "Read tasks.md"], cwd=root, capture_output=True, text=True, timeout=20, check=False)
        assert invalid.returncode == 2 and "invalid value" in invalid.stderr and "sandbox" in invalid.stderr
        assert {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()} == prior
        cli_probe = {"version": version.stdout.strip(), "helpSha256": sha256(help_result.stdout.encode()).hexdigest(), "invalidFlagExit": invalid.returncode, "oldReportPreserved": True, "modelInvoked": False}
        checks.append("Real CLI help confirms flags; an invalid sandbox exits during parsing and leaves old output unchanged without a model call")
    invalid_results = [
        {k: v for k, v in expected.items() if k != "pending"},
        {**expected, "extra": "not permitted"}, {**expected, "total": True},
        {**expected, "pending": -1}, {**expected, "completed": "1"},
        {**expected, "total": 20}, {**expected, "revision": "old"}, [],
    ]
    for number, result in enumerate(invalid_results):
        case = root / f"fields-{number}"
        write_case(case, result=result)
        rejected(case)
    checks.append("Eight invalid shapes, types, revisions and count combinations are rejected")
    for number, event_list in enumerate([[], [{"type": "turn.started"}], events + [{"type": "error"}],
                                       events + [{"type": "turn.failed"}], events + [{"type": "turn.completed"}],
                                       events + [{"type": "turn.started"}], list(reversed(events))]):
        case = root / f"events-{number}"
        write_case(case, event_list=event_list)
        rejected(case)
    malformed = root / "malformed"
    write_case(malformed)
    (malformed / "events.jsonl").write_text('{"type":"turn.started"\n', encoding="utf-8")
    rejected(malformed)
    checks.append("Truncated JSONL, missing completion, failure events and duplicate or reversed turn boundaries are rejected")
    for number, status in enumerate([{"state": "exited", "exit_code": 7}, {"state": "running"}, {"state": "timeout"}, {"state": "launch_failed"},
                                     {"state": "exited", "exit_code": False}, {"state": "exited", "exit_code": 0.0}]):
        case = root / f"status-{number}"
        write_case(case, status=status)
        rejected(case)
    checks.append("A valid-looking final answer cannot override unsuccessful or incorrectly typed process status")
    extra = root / "new-event"
    write_case(extra, event_list=events[:2] + [{"type": "future.event"}] + events[2:])
    assert summary.verify(extra) == expected
    (extra / "events.jsonl").write_text("\n" + (extra / "events.jsonl").read_text(encoding="utf-8") + "\n", encoding="utf-8-sig")
    assert summary.verify(extra) == expected
    checks.append("Unknown event kinds, blank lines and UTF-8 BOM do not break valid input")
    for name, code in [("run-01", 0), ("fields-0", 1), ("malformed", 1), ("status-0", 1)]:
        run = subprocess.run([sys.executable, str(SOURCE), name, "--verify-only"], cwd=root, capture_output=True, timeout=10, check=False)
        assert run.returncode == code, run.stderr
    assert summary.verify(baseline) == expected
    checks.append("The documented verify-only command returns correct exit codes and original output remains valid")

    (root / "tasks.md").write_text("# Fictional wrapper input\n", encoding="utf-8")
    before = (root / "tasks.md").read_bytes()
    previous = Path.cwd()
    os.chdir(root)
    try:
        def reference_launch(command, **kwargs):
            assert isinstance(command, list) and command[:2] == ["codex", "exec"]
            assert kwargs["timeout"] == 120 and kwargs.get("shell", False) is False
            output = Path(command[command.index("-o") + 1])
            assert output.parent.parent == root
            kwargs["stdout"].write(("\n".join(json.dumps(e) for e in events) + "\n").encode())
            output.write_text(json.dumps(expected), encoding="utf-8")
            return subprocess.CompletedProcess(command, 0)

        with patch.object(sys, "argv", ["run_summary.py", "wrapper-ok"]), patch.object(summary.subprocess, "run", side_effect=reference_launch) as launch, redirect_stdout(io.StringIO()):
            summary.main()
            assert launch.call_count == 1
        assert summary.verify(root / "wrapper-ok") == expected
        with patch.object(sys, "argv", ["run_summary.py", "wrapper-ok"]), patch.object(summary.subprocess, "run") as launch:
            try:
                summary.main()
            except FileExistsError:
                pass
            else:
                raise AssertionError("Previous run overwritten")
            launch.assert_not_called()
        checks.append("The wrapper uses an argument array, calls once and refuses to overwrite previous evidence")
        for name, error, state in [("timeout", subprocess.TimeoutExpired(["codex"], 120), "timeout"), ("launch-failed", FileNotFoundError("reference failure"), "launch_failed")]:
            with patch.object(sys, "argv", ["run_summary.py", name]), patch.object(summary.subprocess, "run", side_effect=error) as launch:
                try:
                    summary.main()
                except ValueError:
                    pass
                else:
                    raise AssertionError("Failure accepted")
                assert launch.call_count == 1
            assert json.loads((root / name / "status.json").read_text()) == {"state": state}
        assert (root / "tasks.md").read_bytes() == before
        checks.append("Simulated timeout and launch failure retain distinct status without retry or input edits")
    finally:
        os.chdir(previous)

    assert set(workflow["on"]) == {"workflow_dispatch"}
    assert workflow["permissions"] == {"contents": "read"}
    first = workflow["jobs"]["summarize"]
    action = first["steps"][-1]
    assert action["uses"] == "openai/codex-action@86365089eb2b84e0a8fb0717b304f8bdcb13b20e"
    assert action["with"]["permission-profile"] == ":read-only" and "sandbox" not in action["with"]
    assert action["with"]["safety-strategy"] == "drop-sudo"
    assert first["steps"][0]["with"]["persist-credentials"] == "false"
    second = workflow["jobs"]["save_report"]
    assert second["permissions"] == {} and second["needs"] == "summarize"
    script = second["steps"][0]["run"].split("\n", 1)[1].rsplit("\nPY", 1)[0]
    assert "${{" not in script
    checks.append("CI is manually triggered with pinned Actions, read-only permissions and a separate secret-free validation job")
    ci = root / "ci-validation"
    ci.mkdir()
    ci_env = {**os.environ, "PRACTICE_SHA": "fictional-sha", "PRACTICE_RUN_ID": "fixture-run", "PRACTICE_ATTEMPT": "1"}
    for number, result in enumerate([expected, wrong, {**expected, "completed": True}, {**expected, "extra": "unexpected"}]):
        target = ci / str(number)
        target.mkdir()
        run = subprocess.run([sys.executable, "-c", script], cwd=target, env={**ci_env, "PRACTICE_RESULT": json.dumps(result)}, capture_output=True, timeout=10, check=False)
        assert run.returncode == (0 if number == 0 else 1), run.stderr
        assert (target / "report.json").exists() == (number == 0)
    assert json.loads((ci / "0/run-info.json").read_text()) == {"sha": "fictional-sha", "run_id": "fixture-run", "attempt": "1"}
    checks.append("The exact CI validation script accepts the fixture, rejects changed counts and writes matching synthetic run identifiers")

report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "status": "passed", "checks": checks,
          "cliProbe": cli_probe,
          "authorHashes": {key: sha256((ROOT / f"docs/codex-learning/deep/modules/{key}.json").read_bytes()).hexdigest() for key in authors},
          "environment": "Windows; temporary fictional files; mocked Codex process; exact local Python validator",
          "sourceHashes": {p.name: sha256(p.read_bytes()).hexdigest() for p in [SOURCE, workflow_path]},
          "notTested": ["Actual model output or API authentication", "GitHub-hosted workflow execution", "macOS/Linux runtime", "Publication or deployment"]}
(ROOT / "docs/codex-learning/evidence/exec-reference.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"{len(checks)} exec/JSON/CI reference checks passed; no model or GitHub run triggered")
