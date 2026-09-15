"""Inspect real CLI startup inputs without making a model request or exposing them.

Only public exercise markers and hashes enter the report. Global instructions,
credentials, and the rest of the model-visible prompt are never saved or printed.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
module = json.loads((ROOT / "docs/codex-learning/deep/modules/42.json").read_text(encoding="utf-8"))
samples = [block["code"] for block in module["blocks"] if block["type"] == "code" and block["language"] == "markdown"]
assert len(samples) == 4
codex = shutil.which("codex")
assert codex
version = subprocess.run([codex, "--version"], capture_output=True, text=True, check=True).stdout.strip()
checks = []


def inspect(folder, expected):
    result = subprocess.run([codex, "debug", "prompt-input", "Report the current directory without editing files."],
                            cwd=folder, capture_output=True, encoding="utf-8", errors="replace", timeout=90)
    if result.returncode:
        # stderr may include paths or account details. Preserve only the status.
        raise RuntimeError(f"CLI input inspection failed with exit {result.returncode}; raw output withheld")
    payload = json.loads(result.stdout)
    rendered = json.dumps(payload, ensure_ascii=False)
    markers = {marker: marker in rendered for marker in ["ROOT-LAB", "KEEP-DATA", "UI-BASE", "UI-OVERRIDE", "OVERRIDE-ACTIVE", "DATA-NOTE"]}
    assert markers == expected, f"Unexpected public exercise markers: {markers}"
    return markers


with tempfile.TemporaryDirectory(prefix="codex-rules-") as temp:
    lab = Path(temp)
    # Validate the absolute disposable target before TemporaryDirectory cleanup.
    assert lab.resolve().parent == Path(tempfile.gettempdir()).resolve()
    assert lab.name.startswith("codex-rules-")
    (lab / "ui").mkdir()
    (lab / "data").mkdir()
    subprocess.run(["git", "init", "--quiet"], cwd=lab, check=True, capture_output=True)
    for name, body in zip(["AGENTS.md", "ui/AGENTS.md", "data/README.md"], samples[:3], strict=True):
        (lab / name).write_text(body, encoding="utf-8")
    baseline = {"ROOT-LAB": True, "KEEP-DATA": True, "UI-BASE": False, "UI-OVERRIDE": False, "OVERRIDE-ACTIVE": False, "DATA-NOTE": False}
    checks.append({"case": "root", "markers": inspect(lab, baseline)})
    nested = {**baseline, "UI-BASE": True}
    checks.append({"case": "ui", "markers": inspect(lab / "ui", nested)})
    override = lab / "ui/AGENTS.override.md"
    override.write_text(samples[3], encoding="utf-8")
    checks.append({"case": "nonempty override", "markers": inspect(lab / "ui", {**baseline, "UI-OVERRIDE": True, "OVERRIDE-ACTIVE": True})})
    override.write_text("", encoding="utf-8")
    # This installed build ignores the empty override body but still selects its
    # filename, so it does not fall back to the same-directory AGENTS.md.
    checks.append({"case": "empty override does not load ui base in this build", "markers": inspect(lab / "ui", baseline)})
    override.rename(lab / "ui/override.saved.md")
    checks.append({"case": "renamed override restores ui base", "markers": inspect(lab / "ui", nested)})
    assert all((lab / name).read_text(encoding="utf-8") == body for name, body in zip(["AGENTS.md", "ui/AGENTS.md", "data/README.md"], samples[:3], strict=True))

report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "environment": f"Windows / {version}",
          "method": "Real codex debug prompt-input; no model call or output-following claim; private prompt content discarded",
          "checks": checks, "sourceHashes": [sha256(body.encode()).hexdigest() for body in samples]}
target = ROOT / "docs/codex-learning/evidence/rule-discovery.json"
target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"Passed {len(checks)} real CLI instruction-discovery cases; only exercise markers saved")
