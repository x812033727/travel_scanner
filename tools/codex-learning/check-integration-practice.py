"""Execute the parallel-integration lesson in isolated temporary Git worktrees."""
import json
import os
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTHOR = ROOT / "docs/codex-learning/deep/modules/54.json"
module = json.loads(AUTHOR.read_text(encoding="utf-8"))
env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
checks = []

with tempfile.TemporaryDirectory(prefix="codex-integration-practice-") as temporary:
    parent = Path(temporary).resolve()
    assert parent.parent == Path(tempfile.gettempdir()).resolve()
    assert parent.name.startswith("codex-integration-practice-")
    primary = parent / "integration-lab"
    primary.mkdir()
    for name in ["heading.txt", "footer.txt", "integration.test.mjs"]:
        code = next(b["code"] for b in module["blocks"] if b["type"] == "code" and b.get("label", [None])[0] == "integration-lab/" + name)
        (primary / name).write_text(code, encoding="utf-8")

    def git(*arguments, cwd=primary, expected=0):
        result = subprocess.run(["git", *arguments], cwd=cwd, env=env, capture_output=True, encoding="utf-8", timeout=20, check=False)
        assert result.returncode == expected, result.stdout + result.stderr
        return result.stdout

    def tests(directory, passes, fails):
        # Match the lesson: call from the original directory with a path to the other test.
        result = subprocess.run(["node", "--test", "--test-reporter=tap", str(directory / "integration.test.mjs")], cwd=primary, capture_output=True, encoding="utf-8", timeout=20, check=False)
        assert result.returncode == (1 if fails else 0), result.stdout + result.stderr
        assert re.search(rf"# pass {passes}\b", result.stdout) and re.search(rf"# fail {fails}\b", result.stdout), result.stdout

    version = git("--version").strip()
    git("init", "-b", "main")
    git("config", "user.name", "Codex Learner")
    git("config", "user.email", "learner@example.test")
    tests(primary, 0, 2)
    git("add", "--", "heading.txt", "footer.txt", "integration.test.mjs")
    git("commit", "-m", "Add integration exercise and acceptance cases")
    original = {p.name: p.read_bytes() for p in primary.iterdir() if p.is_file()}
    baseline = git("rev-parse", "HEAD").strip()
    checks.append("The exact authored baseline has two intentionally unmet acceptance cases")
    paths = {name: parent / ("integration-" + name) for name in ["heading", "footer", "review", "conflict"]}
    branches = {"heading": "codex/heading", "footer": "codex/footer", "review": "codex/integration", "conflict": "codex/conflict"}
    for name in ["heading", "footer", "review"]:
        assert paths[name].parent == parent and not paths[name].exists()
        git("worktree", "add", "-b", branches[name], str(paths[name]), "main")
    changes = {"heading": ("heading.txt", "Title: Small Steps Lab\n"), "footer": ("footer.txt", "Footer: Practice only\n")}
    inputs = {}
    for name, (filename, value) in changes.items():
        (paths[name] / filename).write_text(value, encoding="utf-8")
        assert git("diff", "--name-only", cwd=paths[name]).strip() == filename
        tests(paths[name], 1, 1)
        git("add", "--", filename, cwd=paths[name])
        git("commit", "-m", "Label practice " + name, cwd=paths[name])
        inputs[name] = git("rev-parse", "HEAD", cwd=paths[name]).strip()
    checks.append("Each independent checkout changes only its assigned file and passes only its own requirement")
    for name in ["heading", "footer"]:
        git("merge", "--no-ff", branches[name], "-m", "Integrate practice " + name, cwd=paths["review"])
    tests(paths["review"], 2, 0)
    assert set(git("diff", "--name-only", "main...HEAD", cwd=paths["review"]).splitlines()) == {"heading.txt", "footer.txt"}
    combined = git("rev-parse", "HEAD", cwd=paths["review"]).strip()
    assert git("status", "--short", cwd=paths["review"]) == ""
    checks.append("Sequential integration produces both expected changes, two passing tests and a clean checkout")
    assert paths["conflict"].parent == parent and not paths["conflict"].exists()
    git("worktree", "add", "-b", branches["conflict"], str(paths["conflict"]), "main")
    (paths["conflict"] / "heading.txt").write_text("Title: Another direction\n", encoding="utf-8")
    git("add", "--", "heading.txt", cwd=paths["conflict"])
    git("commit", "-m", "Create a conflicting practice heading", cwd=paths["conflict"])
    git("merge", "--no-ff", "codex/conflict", "-m", "Attempt conflicting integration", cwd=paths["review"], expected=1)
    assert "UU heading.txt" in git("status", "--short", cwd=paths["review"])
    assert "<<<<<<<" in (paths["review"] / "heading.txt").read_text(encoding="utf-8")
    checks.append("The deliberate conflicting heading yields an actual unmerged file and conflict markers")
    git("merge", "--abort", cwd=paths["review"])
    assert git("rev-parse", "HEAD", cwd=paths["review"]).strip() == combined
    assert git("status", "--short", cwd=paths["review"]) == ""
    tests(paths["review"], 2, 0)
    checks.append("Abort restores the exact pre-conflict commit, clean state and both passing tests")
    for directory in paths.values():
        assert directory.resolve().parent == parent and git("status", "--short", cwd=directory) == ""
        git("worktree", "remove", str(directory))
    assert git("worktree", "list", "--porcelain").count("worktree ") == 1
    assert git("show", "codex/integration:heading.txt").strip() == "Title: Small Steps Lab"
    assert git("show", "codex/integration:footer.txt").strip() == "Footer: Practice only"
    assert git("rev-parse", "main").strip() == baseline and git("remote") == ""
    assert {p.name: p.read_bytes() for p in primary.iterdir() if p.is_file()} == original
    checks.append("Cleanup preserves the original main files and the integrated branch without any remote")

report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "status": "passed", "environment": "Windows; isolated temporary Git repository; explicit reference edits", "gitVersion": version, "checks": checks, "inputCommits": inputs, "integrationCommit": combined, "baselineCommit": baseline, "authorHash": sha256(AUTHOR.read_bytes()).hexdigest(), "notTested": ["Actual model delegation", "Codex Handoff", "macOS/Linux execution", "Website build, browser UI, publication or deployment"]}
(ROOT / "docs/codex-learning/evidence/integration-practice.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"{len(checks)} integration practice checks passed; no real project merge or remote action")
