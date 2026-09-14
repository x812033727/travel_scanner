"""Execute authored reference examples; never call a model or alter user settings."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
AUTHORS = ROOT / "docs/codex-learning/deep/modules"
PRACTICE = ROOT / "docs/codex-learning/practice"
checks = []


def samples(number, language):
    module = json.loads((AUTHORS / f"{number:02d}.json").read_text(encoding="utf-8"))
    return [b["code"] for b in module["blocks"] if b["type"] == "code" and b["language"] == language]


def run(directory, args, expected_exit=0):
    if args[0] == "--test":
        args = ["--test-reporter=tap", *args]
    result = subprocess.run(["node", *args], cwd=directory, capture_output=True, encoding="utf-8")
    assert result.returncode == expected_exit, result.stdout + result.stderr
    return result.stdout


def fixture(target, name):
    target.mkdir(parents=True)
    for source in (PRACTICE / name).iterdir():
        if source.is_file():
            (target / source.name).write_bytes(source.read_bytes())


def hashes(directory):
    return {p.name: sha256(p.read_bytes()).hexdigest() for p in directory.iterdir() if p.is_file()}


# Only temporary files created here are recursively cleaned up.
with tempfile.TemporaryDirectory(prefix="codex-session-plan-") as temp:
    lab = Path(temp).resolve()
    assert lab.parent == Path(tempfile.gettempdir()).resolve()
    assert lab.name.startswith("codex-session-plan-")

    plan = lab / "plan"
    fixture(plan, "start")
    baseline = hashes(plan)
    assert "# pass 2" in run(plan, ["--test", "core.test.mjs"], 1)
    checks.append("08: exact start fixture fails its filter test as expected")
    original_bytes = (plan / "core.mjs").read_bytes()
    original = original_bytes.decode("utf-8").replace("\r\n", "\n")
    updated, count = re.subn(
        r"export function visibleTasks\(tasks, filter\) \{.*?\n\}",
        lambda _: samples(8, "javascript")[0].rstrip("\n"),
        original,
        count=1,
        flags=re.S,
    )
    assert count == 1
    (plan / "core.mjs").write_bytes(updated.encode("utf-8"))
    assert "# pass 3" in run(plan, ["--test", "core.test.mjs"])
    assert [name for name, digest in hashes(plan).items() if baseline[name] != digest] == ["core.mjs"]
    checks.append("08: literal reference function passes all three tests; only core.mjs changes")
    matrix = """
import assert from 'node:assert/strict';
import {visibleTasks} from './core.mjs';
const input = Object.freeze([
 Object.freeze({title:'Read', completed:true}),
 Object.freeze({title:'Build', completed:false}),
]);
for (const [filter, titles] of Object.entries({all:['Read','Build'], active:['Build'], completed:['Read']})) {
 assert.deepEqual(visibleTasks(input,filter).map(x=>x.title),titles);
 assert.deepEqual(visibleTasks(Object.freeze([]),filter),[]);
}
assert.deepEqual(input.map(x=>x.title),['Read','Build']);
"""
    run(plan, ["--input-type=module", "-e", matrix])
    checks.append("08: six published filter cases pass with frozen inputs and preserved ordering")
    (plan / "core.mjs").write_bytes(original_bytes)
    assert hashes(plan) == baseline
    assert "# pass 2" in run(plan, ["--test", "core.test.mjs"], 1)
    checks.append("08: scoped restoration recovers the known failing baseline exactly")

    handoff = lab / "handoff"
    fixture(handoff, "broken")
    state = samples(22, "text")[0]
    note = samples(22, "markdown")[0]
    (handoff / "LAB_STATE.txt").write_bytes(state.encode())
    (handoff / "handoff.md").write_bytes(note.encode())
    assert "# pass 2" in run(handoff, ["--test", "core.test.mjs"], 1)
    assert "BROKEN-1" in state and "BROKEN-1" in note
    before = hashes(handoff)
    (handoff / "core.mjs").write_bytes((PRACTICE / "expected/core.mjs").read_bytes())
    (handoff / "LAB_STATE.txt").write_bytes(state.replace("BROKEN-1", "FIXED-2").encode())
    assert "# pass 3" in run(handoff, ["--test", "core.test.mjs"])
    assert sorted(k for k, v in hashes(handoff).items() if before[k] != v) == ["LAB_STATE.txt", "core.mjs"]
    assert (handoff / "handoff.md").read_text() == note
    checks.append("22: stale BROKEN-1 handoff coexists with FIXED-2 and three passing tests")
    (handoff / "core.mjs").write_bytes((PRACTICE / "broken/core.mjs").read_bytes())
    (handoff / "LAB_STATE.txt").write_bytes(state.encode())
    assert hashes(handoff) == before
    checks.append("22: restoration recovers all original files without changing tests or handoff")

    models = lab / "models"
    models.mkdir()
    sample = samples(17, "javascript")[0]
    (models / "sample.mjs").write_bytes(sample.encode())
    run(models, ["--input-type=module", "-e",
        "import assert from 'node:assert/strict';import {completedTitles,sample} from './sample.mjs';"
        "const before=JSON.stringify(sample);assert.deepEqual(completedTitles(sample),['Build']);"
        "assert.deepEqual(completedTitles([]),[]);assert.equal(JSON.stringify(sample),before);"])
    checks.append("17: exact faulty sample returns Build; empty input and nonmutation verified")
    (models / "sample.mjs").write_bytes(sample.replace("!task.completed", "task.completed").encode())
    run(models, ["--input-type=module", "-e",
        "import assert from 'node:assert/strict';import {completedTitles,sample} from './sample.mjs';"
        "const before=JSON.stringify(sample);assert.deepEqual(completedTitles(sample),['Read']);"
        "assert.deepEqual(completedTitles([]),[]);assert.equal(JSON.stringify(sample),before);"])
    checks.append("17: stated one-character repair returns Read and preserves empty/input behavior")

    sessions = lab / "sessions"
    sessions.mkdir()
    a, b = samples(45, "text")[:2]
    assert a == "SESSION-A\nRevision: 1\n" and b == "SESSION-B\nRevision: 100\n"
    for folder, data in [("a", a), ("b", b)]:
        (sessions / folder).mkdir()
        (sessions / folder / "note.txt").write_bytes(data.encode())
    (sessions / "a/note.txt").write_bytes(a.replace("Revision: 1", "Revision: 2").encode())
    assert (sessions / "a/note.txt").read_text() != a
    assert (sessions / "b/note.txt").read_text() == b
    checks.append("45: same-name A/B fixtures and stale-memory scenario verified without resuming a model")

    readonly, writable = samples(18, "sh")
    assert "--sandbox read-only --ask-for-approval on-request" in readonly
    assert "--sandbox workspace-write --ask-for-approval on-request" in writable
    first, second = samples(18, "text")[:2]
    assert "PERMISSION-LAB\nRevision: 1\n" == first
    assert "Only note.txt" in second and "Target revision: 2" in second
    checks.append("18: literal scope markers and command modes checked; no OS sandbox execution claim")

    feature = lab / "feature"
    fixture(feature, "start")
    feature_test, feature_fix = samples(47, "javascript")
    (feature / "filter.test.mjs").write_bytes(feature_test.encode())
    initial = hashes(feature)
    result = run(feature, ["--test", "core.test.mjs", "filter.test.mjs"], 1)
    assert "# pass 4" in result and "# fail 2" in result
    checks.append("47: exact added tests detect the start defect, four passes and two expected failures")
    source_bytes = (feature / "core.mjs").read_bytes()
    source_text = source_bytes.decode().replace("\r\n", "\n")
    fixed, count = re.subn(
        r"export function visibleTasks\(tasks, filter\) \{.*?\n\}",
        lambda _: feature_fix.rstrip("\n"), source_text, count=1, flags=re.S,
    )
    assert count == 1
    (feature / "core.mjs").write_bytes(fixed.encode())
    result = run(feature, ["--test", "core.test.mjs", "filter.test.mjs"])
    assert "# pass 6" in result and "# fail 0" in result
    assert [k for k, v in hashes(feature).items() if initial[k] != v] == ["core.mjs"]
    checks.append("47: literal repair passes all six tests including duplicate-title identity and frozen inputs")
    (feature / "core.mjs").write_bytes(source_bytes)
    assert hashes(feature) == initial
    assert "# fail 2" in run(feature, ["--test", "core.test.mjs", "filter.test.mjs"], 1)
    checks.append("47: restoring only core.mjs preserves added tests and reproduces two failures")

    codebase = lab / "codebase"
    fixture(codebase, "expected")
    original_hashes = hashes(codebase)
    (codebase / "project-map.md").write_bytes(samples(46, "markdown")[0].encode())
    assert "# pass 3" in run(codebase, ["--test", "core.test.mjs"])
    assert all(hashes(codebase)[name] == digest for name, digest in original_hashes.items())
    checks.append("46: exact map is an added document; expected reference still passes three tests unchanged")

    debugging = lab / "debugging"
    fixture(debugging, "broken")
    repro, repaired_line = samples(20, "javascript")
    (debugging / "repro.mjs").write_bytes(repro.encode())
    assert 'Completed IDs: ["b"]' in run(debugging, ["repro.mjs"], 1)
    assert "# pass 2" in run(debugging, ["--test", "core.test.mjs"], 1)
    before = hashes(debugging)
    source_bytes = (debugging / "core.mjs").read_bytes()
    source_text = source_bytes.decode().replace("\r\n", "\n")
    wrong = 'if (filter === "completed") return tasks.filter((task) => !task.completed);'
    assert source_text.count(wrong) == 1
    source_text = source_text.replace(wrong, repaired_line.strip()).replace(
        "  // EXERCISE: this predicate is deliberately wrong.\n", "")
    (debugging / "core.mjs").write_bytes(source_text.encode())
    output = run(debugging, ["repro.mjs"])
    assert 'Completed IDs: ["a"]' in output and "Reproduction passed." in output
    assert "# pass 3" in run(debugging, ["--test", "core.test.mjs"])
    assert [k for k, v in hashes(debugging).items() if before[k] != v] == ["core.mjs"]
    checks.append("20: authored minimal repro fails with b and passes with a after only the stated repair")
    (debugging / "core.mjs").write_bytes(source_bytes)
    assert hashes(debugging) == before
    assert 'Completed IDs: ["b"]' in run(debugging, ["repro.mjs"], 1)
    checks.append("20: scoped restoration reproduces the original bug with unchanged reproduction and tests")

report = {
    "checkedAt": datetime.now(timezone.utc).isoformat(),
    "environment": "Windows / Node " + subprocess.check_output(["node", "--version"], text=True).strip(),
    "method": "Execute exact authored fixtures and targeted reference changes in an isolated temporary directory.",
    "limitations": [
        "No model calls, interactive Plan/resume/compact, model comparison or permission approvals executed.",
        "Permission commands checked structurally only; OS sandbox behavior requires separate evidence.",
        "Filter matrix is a function-level check; UI testing is separately recorded.",
    ],
    "moduleHashes": {f"{i:02d}": sha256((AUTHORS / f"{i:02d}.json").read_bytes()).hexdigest() for i in [8, 17, 18, 20, 22, 45, 46, 47]},
    "checks": checks,
}
(ROOT / "docs/codex-learning/evidence/session-plan-practice.json").write_text(
    json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"Passed {len(checks)} session, plan, model and handoff reference checks")
