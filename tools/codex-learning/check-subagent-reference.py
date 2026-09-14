"""Check the reference evidence, not a subagent run or custom-role activation."""
import json
import re
import shlex
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
MODULES = ROOT / "docs/codex-learning/deep/modules"
reference = ROOT / "docs/codex-learning/practice/expected"
roles = json.loads((MODULES / "28.json").read_text(encoding="utf-8"))
quality = json.loads((MODULES / "53.json").read_text(encoding="utf-8"))
role = tomllib.loads(next(b["code"] for b in roles["blocks"] if b["type"] == "code" and b["language"] == "toml"))
assert role["name"] == "data_reader" and role["sandbox_mode"] == "read-only" and role["developer_instructions"]
checks = ["Custom role is valid TOML with required fields; activation and runtime permissions are not tested"]

with tempfile.TemporaryDirectory(prefix="codex-subagent-reference-") as folder:
    lab = Path(folder).resolve()
    assert lab.parent == Path(tempfile.gettempdir()).resolve()
    assert lab.name.startswith("codex-subagent-reference-")
    for source in reference.iterdir():
        if source.is_file():
            shutil.copy2(source, lab / source.name)
    before = {p.name: p.read_bytes() for p in lab.iterdir()}

    def run(args, passes=None, fails=0):
        result = subprocess.run(args, cwd=lab, capture_output=True, encoding="utf-8", timeout=20, check=False)
        assert result.returncode == (1 if fails else 0), result.stdout + result.stderr
        if passes is not None:
            assert re.search(rf"# pass {passes}\b", result.stdout), result.stdout
            assert re.search(rf"# fail {fails}\b", result.stdout), result.stdout
        return result.stdout

    version = run(["node", "--version"]).strip()
    run(["node", "--test", "--test-reporter=tap", "core.test.mjs"], passes=3)
    checks.append("The original complete reference has three passing tests")
    command = next(b["code"] for b in quality["blocks"] if b["type"] == "code" and b["code"].startswith("node --input-type=module"))
    assert run(shlex.split(command)).strip() == "Duplicate ID rejected: task-id"
    checks.append("The exact one-line reproduction disproves the fictional duplicate-ID claim")
    sample = next(b["code"] for b in quality["blocks"] if b["type"] == "code" and b["language"] == "javascript")
    extra = lab / "review-evidence.test.mjs"
    assert not extra.exists()
    extra.write_text(sample, encoding="utf-8")
    args = ["node", "--test", "--test-reporter=tap", "core.test.mjs", "review-evidence.test.mjs"]
    run(args, passes=6)
    checks.append("All six original and added evidence tests pass without editing the application")
    core = lab / "core.mjs"
    guard = next(b["code"] for b in quality["blocks"] if b["type"] == "code" and b["code"].startswith(" || tasks.some")).rstrip("\n")
    assert core.read_text(encoding="utf-8").count(guard) == 1
    core.write_text(core.read_text(encoding="utf-8").replace(guard, ""), encoding="utf-8")
    run(args, passes=4, fails=2)
    checks.append("Removing duplicate-ID validation is detected by two failures, with four other tests passing")
    core.write_bytes(before["core.mjs"])
    run(args, passes=6)
    assert extra.resolve().parent == lab and extra.name == "review-evidence.test.mjs"
    extra.unlink()
    run(["node", "--test", "--test-reporter=tap", "core.test.mjs"], passes=3)
    assert {p.name: p.read_bytes() for p in lab.iterdir()} == before
    checks.append("Restoration passes six tests, then returns to the original three with all five files identical")

report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "status": "passed", "environment": "Windows; temporary Small Steps reference copy", "nodeVersion": version, "checks": checks, "notTested": ["Actual subagent spawning, steering, stopping or inspection", "Custom role activation or runtime permission enforcement", "macOS/Linux execution", "Codex desktop/CLI/IDE UI"], "authorHashes": {key: sha256((MODULES / f"{key}.json").read_bytes()).hexdigest() for key in ["28", "53"]}}
(ROOT / "docs/codex-learning/evidence/subagent-reference.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"{len(checks)} subagent reference checks passed; no subagent was spawned")
