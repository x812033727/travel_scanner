"""Execute the worktree lesson in a new temporary repository, without remotes."""
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTHOR = ROOT / "docs/codex-learning/deep/modules/27.json"
module = json.loads(AUTHOR.read_text(encoding="utf-8"))
sample = next(block["code"] for block in module["blocks"] if block["type"] == "code" and block.get("label", [None])[0] == "worktree-lab/notes.md")
checks = []
env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")

with tempfile.TemporaryDirectory(prefix="codex-worktree-practice-") as temporary:
    parent = Path(temporary).resolve()
    assert parent.parent == Path(tempfile.gettempdir()).resolve()
    assert parent.name.startswith("codex-worktree-practice-")
    primary = parent / "worktree-lab"
    secondary = parent / "worktree-copy"
    primary.mkdir()

    def git(*arguments, cwd=primary, expected=0):
        result = subprocess.run(["git", *arguments], cwd=cwd, env=env, capture_output=True, encoding="utf-8", timeout=20, check=False)
        assert result.returncode == expected, result.stdout + result.stderr
        return result.stdout, result.stderr

    version = git("--version")[0].strip()
    git("init", "-b", "main")
    git("config", "user.name", "Codex Learner")
    git("config", "user.email", "learner@example.test")
    (primary / "notes.md").write_text(sample, encoding="utf-8")
    git("add", "--", "notes.md")
    git("commit", "-m", "Add worktree practice baseline")
    assert git("status", "--short")[0] == ""
    original = (primary / "notes.md").read_bytes()
    checks.append("A new repository contains only the committed fictional lesson file")
    assert not secondary.exists() and secondary.parent == parent
    git("worktree", "add", "-b", "codex/worktree-practice", "../worktree-copy")
    assert git("worktree", "list", "--porcelain")[0].count("worktree ") == 2
    assert (secondary / "notes.md").read_bytes() == original
    checks.append("The sibling worktree begins with an identical tracked file on its own branch")
    (secondary / "notes.md").write_text(sample.replace("LOCAL-A", "COPY-B"), encoding="utf-8")
    assert (primary / "notes.md").read_bytes() == original
    assert git("status", "--short")[0] == ""
    assert "notes.md" in git("status", "--short", cwd=secondary)[0]
    difference = git("diff", "--", "notes.md", cwd=secondary)[0]
    assert "-Marker: LOCAL-A" in difference and "+Marker: COPY-B" in difference
    checks.append("Editing the secondary marker leaves the primary file and index unchanged")
    _, error = git("switch", "main", cwd=secondary, expected=128)
    assert "already used by worktree" in error or "already checked out" in error
    assert git("branch", "--show-current", cwd=secondary)[0].strip() == "codex/worktree-practice"
    checks.append("Git refuses to check out the already-used main branch without moving either checkout")
    assert secondary.resolve().parent == parent
    _, error = git("worktree", "remove", "../worktree-copy", expected=128)
    assert secondary.exists() and (secondary / "notes.md").read_text(encoding="utf-8") == sample.replace("LOCAL-A", "COPY-B")
    checks.append("Ordinary removal refuses a dirty worktree and preserves the uncommitted marker")
    git("add", "--", "notes.md", cwd=secondary)
    git("commit", "-m", "Change isolated practice marker", cwd=secondary)
    assert git("status", "--short", cwd=secondary)[0] == ""
    assert "+Marker: COPY-B" in git("diff", "main...codex/worktree-practice", "--", "notes.md")[0]
    checks.append("The feature commit retains the expected diff without merging into main")
    assert secondary.resolve().parent == parent and secondary.name == "worktree-copy"
    git("worktree", "remove", "../worktree-copy")
    assert not secondary.exists() and git("worktree", "list", "--porcelain")[0].count("worktree ") == 1
    assert git("show", "codex/worktree-practice:notes.md")[0] == sample.replace("LOCAL-A", "COPY-B")
    assert (primary / "notes.md").read_bytes() == original and git("remote")[0] == ""
    checks.append("Removing the clean checkout preserves main and the committed feature branch; no remote exists")

report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "status": "passed", "environment": "Windows; temporary repository; isolated Git configuration", "gitVersion": version, "checks": checks, "authorHash": sha256(AUTHOR.read_bytes()).hexdigest(), "notTested": ["Codex-managed worktree creation or Handoff", "macOS/Linux execution", "mobile Remote", "deployment or merge into the website repository"]}
(ROOT / "docs/codex-learning/evidence/worktree-practice.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"{len(checks)} worktree practice checks passed; original website repository was not modified")
