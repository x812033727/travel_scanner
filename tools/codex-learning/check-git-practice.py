"""Run the authored Git lesson only in a fresh, isolated temporary repository."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/codex-learning/deep/modules/19.json"
module = json.loads(SOURCE.read_text(encoding="utf-8"))
groups = [b["code"] for b in module["blocks"] if b["type"] == "code" and b["language"] == "sh"]
comment = next(b["code"] for b in module["blocks"] if b["type"] == "code" and b["language"] == "css")
assert len(groups) == 7
checks = []
executed = []

with tempfile.TemporaryDirectory(prefix="codex-git-lesson-") as directory:
    lab = Path(directory).resolve()
    assert lab.parent == Path(tempfile.gettempdir()).resolve()
    assert lab.name.startswith("codex-git-lesson-")
    # Ignore inherited repository pointers and Git configuration in this child
    # process only. Never edit the user's config, hooks, credentials or checkout.
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0")

    def command(line):
        args = shlex.split(line)
        assert args[0] == "git"
        result = subprocess.run(args, cwd=lab, env=env, capture_output=True, encoding="utf-8")
        assert result.returncode == 0, (line, result.stderr)
        executed.append(line)
        return result.stdout

    def group(number):
        for line in groups[number].strip().splitlines():
            command(line)

    for source in (ROOT / "docs/codex-learning/practice/expected").iterdir():
        if source.is_file():
            (lab / source.name).write_bytes(source.read_bytes())
    original = {p.name: p.read_bytes() for p in lab.iterdir()}
    group(0)
    assert not command("git status --short").strip()
    assert set(command("git ls-files").splitlines()) == set(original)
    checks.append("Exact baseline commands commit five files and leave a clean worktree")
    group(1)
    assert command("git branch --show-current").strip() == "codex/title-lab"
    index = lab / "index.html"
    css = lab / "style.css"
    old = b"Make room for one small task."
    new = b"Plan one useful step."
    assert original["index.html"].count(old) == 1
    index.write_bytes(original["index.html"].replace(old, new))
    css.write_bytes(original["style.css"] + comment.encode())
    group(2)
    assert set(command("git diff --name-only").splitlines()) == {"index.html", "style.css"}
    group(3)
    assert command("git diff --cached --name-only").strip() == "index.html"
    assert command("git diff --name-only").strip() == "style.css"
    checks.append("Staging only index.html excludes and preserves the independent CSS note")
    restore_lines = groups[4].strip().splitlines()
    command(restore_lines[0])
    assert not command("git diff --cached --name-only").strip()
    assert new in index.read_bytes()
    checks.append("Unstage changes only the index and preserves the new title on disk")
    for line in restore_lines[1:]:
        command(line)
    # Git may normalize line endings; require exact text and untouched CSS bytes.
    assert index.read_text(encoding="utf-8") == original["index.html"].decode().replace("\r\n", "\n")
    assert css.read_bytes() == original["style.css"] + comment.encode()
    assert command("git diff --name-only").strip() == "style.css"
    checks.append("Path-specific worktree restore discards only the title while preserving CSS bytes")
    current_bytes = index.read_bytes()
    index.write_bytes(current_bytes.replace(old, new))
    group(5)
    assert command("git show --format= --name-only HEAD").strip() == "index.html"
    assert command("git diff --name-only").strip() == "style.css"
    assert b"KEEP-MY-NOTE" in css.read_bytes()
    title_commit = command("git rev-parse HEAD").strip()
    checks.append("Title commit contains only index.html and leaves the CSS note uncommitted")
    group(6)
    assert not command("git status --short").strip()
    assert command("git rev-list --count HEAD").strip() == "3"
    assert command("git rev-parse HEAD^").strip() == title_commit
    assert index.read_text(encoding="utf-8") == original["index.html"].decode().replace("\r\n", "\n")
    assert css.read_text(encoding="utf-8") == original["style.css"].decode().replace("\r\n", "\n")
    assert not command("git remote").strip()
    checks.append("Explicit note cleanup and revert leave original content, three commits and no remote")

review_source = ROOT / "docs/codex-learning/deep/modules/21.json"
review_module = json.loads(review_source.read_text(encoding="utf-8"))
review_test = next(b["code"] for b in review_module["blocks"] if b["type"] == "code" and b["language"] == "javascript")
with tempfile.TemporaryDirectory(prefix="codex-review-lesson-") as directory:
    lab = Path(directory).resolve()
    assert lab.parent == Path(tempfile.gettempdir()).resolve()
    assert lab.name.startswith("codex-review-lesson-")
    for source in (ROOT / "docs/codex-learning/practice/expected").iterdir():
        if source.is_file():
            (lab / source.name).write_bytes(source.read_bytes())
    group(0)
    command("git switch -c codex/review-lab")
    core = lab / "core.mjs"
    original_core = core.read_bytes()
    target = b"  return tasks;"
    assert original_core.count(target) == 1
    core.write_bytes(original_core.replace(target, b"  return tasks.reverse();"))

    def node_tests(files, status, passed, failed):
        result = subprocess.run(["node", "--test-reporter=tap", "--test", *files],
                                cwd=lab, capture_output=True, encoding="utf-8")
        assert result.returncode == status, result.stdout + result.stderr
        assert f"# pass {passed}" in result.stdout and f"# fail {failed}" in result.stdout

    node_tests(["core.test.mjs"], 0, 3, 0)
    checks.append("21: intentionally mutating All change still passes all three original tests")
    (lab / "review.test.mjs").write_bytes(review_test.encode())
    node_tests(["core.test.mjs", "review.test.mjs"], 1, 3, 2)
    checks.append("21: exact new tests detect both reversed order and attempted input mutation")
    core.write_bytes(original_core)
    node_tests(["core.test.mjs", "review.test.mjs"], 0, 5, 0)
    assert not command("git diff --name-only").strip()
    assert command("git status --short").strip() == "?? review.test.mjs"
    commit_group = next(b["code"] for b in review_module["blocks"]
                        if b["type"] == "code" and b["code"].startswith("git add review.test.mjs"))
    for line in commit_group.strip().splitlines():
        command(line)
    assert command("git diff --name-only main...HEAD").strip() == "review.test.mjs"
    assert not command("git status --short").strip()
    assert not command("git remote").strip()
    checks.append("21: final five tests pass and branch diff contains only new regression coverage")

report = {
    "checkedAt": datetime.now(timezone.utc).isoformat(),
    "environment": "Windows / " + subprocess.check_output(["git", "--version"], text=True).strip(),
    "method": "Exact authored commands in a newly created temporary Git repository with per-process isolated Git config.",
    "limitations": "No model session, GitHub, push, production repository change, user-global config or other-platform execution.",
    "sourceHash": sha256(SOURCE.read_bytes()).hexdigest(),
    "reviewSourceHash": sha256(review_source.read_bytes()).hexdigest(),
    "checks": checks,
    "commands": executed,
}
(ROOT / "docs/codex-learning/evidence/git-practice.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"Passed {len(checks)} Git workflow and preservation checks")
