"""Verify the exact published skill files without installing a skill or calling a model."""
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
MODULES = ROOT / "docs/codex-learning/deep/modules"
resource = json.loads((MODULES / "48.json").read_text(encoding="utf-8"))
testing = json.loads((MODULES / "49.json").read_text(encoding="utf-8"))
templates = json.loads((MODULES / "51.json").read_text(encoding="utf-8"))


def sample(module, label):
    return next(block["code"] for block in module["blocks"] if block["type"] == "code" and block["label"][0] == label)


files = {
    "data/tasks.json": sample(resource, "data/tasks.json"),
    ".agents/skills/todo-summary/SKILL.md": sample(resource, "SKILL.md"),
    ".agents/skills/todo-summary/references/input-format.md": sample(resource, "references/input-format.md"),
    ".agents/skills/todo-summary/assets/report.md": sample(resource, "assets/report.md"),
    ".agents/skills/todo-summary/scripts/count-tasks.mjs": sample(resource, "scripts/count-tasks.mjs"),
    "skill.test.mjs": sample(testing, "skill.test.mjs"),
}
report = {"environment": "Windows / Node.js " + subprocess.check_output(["node", "--version"], text=True).strip(),
          "scope": "Exact reference files, no installed skill, no Codex model or automatic invocation",
          "moduleHashes": {str(i): hashlib.sha256((MODULES / f"{i}.json").read_bytes()).hexdigest() for i in [48, 49, 51]}, "checks": []}
with tempfile.TemporaryDirectory(prefix="codex-skill-reference-") as temporary:
    root = Path(temporary).resolve()
    assert root.parent == Path(tempfile.gettempdir()).resolve()
    assert root.name.startswith("codex-skill-reference-")
    for name, body in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8", newline="\n")
    script = root / ".agents/skills/todo-summary/scripts/count-tasks.mjs"

    def execute(args, expected):
        result = subprocess.run(["node", *args], cwd=root, capture_output=True, text=True, encoding="utf-8", timeout=60, check=False)
        assert result.returncode == expected, result.stdout + result.stderr
        return result

    initial = {name: (root / name).read_bytes() for name in files}
    result = execute([str(script), "data/tasks.json"], 0)
    assert json.loads(result.stdout) == {"total": 3, "active": 1, "completed": 2}
    report["checks"].append("Literal lesson 48 command: total 3, active 1, completed 2; exit 0")
    baseline = execute(["--test", "--test-reporter=tap", "skill.test.mjs"], 0)
    assert "# pass 8" in baseline.stdout and "# fail 0" in baseline.stdout
    report["checks"].append("Exact lesson 49 test file: eight passes, including six correctly rejected inputs")
    replacement = sample(testing, "只替換 result 內的 total 欄位").strip()
    original = script.read_text(encoding="utf-8")
    assert original.count("total: tasks.length") == 1
    script.write_text(original.replace("total: tasks.length", replacement), encoding="utf-8", newline="\n")
    faulty = execute(["--test", "--test-reporter=tap", "skill.test.mjs"], 1)
    assert "# pass 7" in faulty.stdout and "# fail 1" in faulty.stdout
    assert "not ok 1 - keeps repeated titles as three records" in faulty.stdout
    report["checks"].append("Exact title-deduplication fault: seven passes, one meaningful regression failure")
    script.write_text(original, encoding="utf-8", newline="\n")
    restored = execute(["--test", "--test-reporter=tap", "skill.test.mjs"], 0)
    assert "# pass 8" in restored.stdout
    assert all((root / name).read_bytes() == body for name, body in initial.items())
    report["checks"].append("Restored checker: eight passes; all six source files byte-for-byte preserved")
    # Links in a skill resolve relative to SKILL.md, independently from command cwd.
    skill_root = script.parent.parent
    import re
    for relative in re.findall(r"\]\(([^)]+)\)", files[".agents/skills/todo-summary/SKILL.md"]):
        assert (skill_root / relative).is_file()
    report["checks"].append("All three SKILL.md resource references resolve to the exact authored files")
    wrong_cwd = subprocess.run(
        ["node", "scripts/count-tasks.mjs", "data/tasks.json"],
        cwd=skill_root, capture_output=True, text=True, encoding="utf-8", timeout=60, check=False,
    )
    assert wrong_cwd.returncode == 1 and "ENOENT" in wrong_cwd.stderr
    assert wrong_cwd.stdout == ""
    assert (skill_root / "../../..").resolve() == root
    result = execute([str(script), "data/tasks.json"], 0)
    assert json.loads(result.stdout) == {"total": 3, "active": 1, "completed": 2}
    report["checks"].append("48: exact wrong-cwd example finds the script but rejects the input path; returning to the lab root restores 3/1/2")
    next_input = sample(resource, "data/tasks-next.json")
    next_path = root / "data/tasks-next.json"
    next_path.write_text(next_input, encoding="utf-8", newline="\n")
    result = execute([str(script), "data/tasks-next.json"], 0)
    assert json.loads(result.stdout) == {"total": 2, "active": 2, "completed": 0}
    result = execute([str(script), "data/tasks.json"], 0)
    assert json.loads(result.stdout) == {"total": 3, "active": 1, "completed": 2}
    assert next_path.read_bytes() == next_input.encode()
    assert all((root / name).read_bytes() == body for name, body in initial.items())
    report["checks"].append("48: second exact input returns 2/2/0, original still returns 3/1/2; both files and all original resources remain unchanged")

    adapted = sample(templates, "任務副本：adapted-task.md")
    for fixture, status, passes, failures in [("expected", 0, 3, 0), ("broken", 1, 2, 1)]:
        example = root / ("template-" + fixture)
        example.mkdir()
        for source in (ROOT / "docs/codex-learning/practice" / fixture).iterdir():
            if source.is_file():
                (example / source.name).write_bytes(source.read_bytes())
        before = {p.name: p.read_bytes() for p in example.iterdir()}
        assert len(before) == 5 and "package.json" not in before
        (example / "adapted-task.md").write_text(adapted, encoding="utf-8", newline="\n")
        result = subprocess.run(
            ["node", "--test-reporter=tap", "--test", "core.test.mjs"],
            cwd=example, capture_output=True, text=True, encoding="utf-8", timeout=60, check=False,
        )
        assert result.returncode == status
        assert f"# pass {passes}" in result.stdout and f"# fail {failures}" in result.stdout
        assert all((example / name).read_bytes() == body for name, body in before.items())
        report["checks"].append(f"51: exact adapted task command on {fixture} returns {passes} passes/{failures} failures with all five source files unchanged")

# A deterministic archive is a practice artifact, not an installation operation.
archive_path = ROOT / "apps/web/public/guides/codex-skill-resources/todo-summary-practice.zip"
archive_path.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
    for name, body in sorted(files.items()):
        info = ZipInfo("codex-skill-lab/" + name, date_time=(2026, 9, 14, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        archive.writestr(info, body.encode("utf-8"))
with ZipFile(archive_path) as archive:
    assert len(archive.namelist()) == len(files)
    for name, body in files.items():
        assert archive.read("codex-skill-lab/" + name) == body.encode("utf-8")
report["checks"].append("Download ZIP contains the six exact files at documented practice paths")
report["archiveHash"] = hashlib.sha256(archive_path.read_bytes()).hexdigest()
(ROOT / "docs/codex-learning/evidence/skill-practice.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f'{len(report["checks"])} skill reference checks passed; no skill was installed or invoked')
