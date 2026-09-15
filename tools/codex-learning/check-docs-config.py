"""Verify the literal documentation and TOML teaching samples, without model calls."""
import json
import subprocess
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
deep = ROOT / "docs/codex-learning/deep/modules"
practice = ROOT / "docs/codex-learning/practice"
checks = []


def samples(id_, language):
    module = json.loads((deep / f"{id_:02d}.json").read_text(encoding="utf-8"))
    return [block["code"] for block in module["blocks"] if block["type"] == "code" and block["language"] == language]


def save(path, text):
    if path.exists() and path.read_text(encoding="utf-8") != text:
        raise ValueError(f"Existing practice sample differs; review before replacing: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


doclab = practice / "documentation"
for source in (practice / "expected").iterdir():
    if source.is_file():
        save(doclab / source.name, source.read_text(encoding="utf-8"))
names = ["AGENTS.md", "README.md", "docs/filters.md", "docs/handoff.md"]
for name, content in zip(names, samples(43, "markdown"), strict=True):
    save(doclab / name, content)
assert (doclab / "docs/filters.md").is_file()
assert (doclab / "docs/handoff.md").is_file()
assert (doclab / "docs/../README.md").is_file()
assert not (doclab / "docs/missing.md").exists()
checks.append("Lesson 43: four exact documents, forward/return paths and a missing-file boundary")
before = {source.name: sha256(source.read_bytes()).hexdigest() for source in (practice / "expected").iterdir() if source.is_file()}
test = subprocess.run(["node", "--test", "core.test.mjs"], cwd=doclab, capture_output=True, encoding="utf-8", check=True)
assert {name: sha256((doclab / name).read_bytes()).hexdigest() for name in before} == before
checks.append("Lesson 43: copied reference tests pass, all five source files remain byte-identical")

configlab = practice / "configuration"
save(configlab / "check_config.py", samples(44, "python")[0])
filenames = ["good.toml", "broken-quote.toml", "broken-duplicate.toml", "broken-scope.toml", "broken-value.toml"]
cases = samples(44, "toml")
assert len(cases) == 6, "Review new or reordered TOML teaching samples"
for index, (name, content) in enumerate(zip(filenames, cases[:5], strict=True)):
    save(configlab / name, content)
    result = subprocess.run([sys.executable, "check_config.py", name], cwd=configlab, capture_output=True, encoding="utf-8", check=False)
    assert result.returncode == (0 if index == 0 else 1), (name, result.returncode)
    checks.append(f"Lesson 44: {name} {'passes' if index == 0 else 'fails as expected'}")
repairs = [
    cases[1].replace('"disabled\n', '"disabled"\n'),
    cases[2].replace('web_search = "live"\n', ""),
    cases[3].replace("[features]\n", ""),
    cases[4].replace('"off"', '"disabled"'),
]
for name, content in zip(filenames[1:], repairs, strict=True):
    repaired = name.replace("broken-", "fixed-")
    save(configlab / repaired, content)
    result = subprocess.run([sys.executable, "check_config.py", repaired], cwd=configlab, capture_output=True, encoding="utf-8", check=False)
    assert result.returncode == 0, repaired
    checks.append(f"Lesson 44: {repaired} passes after its targeted correction")
save(configlab / "limits.toml", cases[5])
result = subprocess.run([sys.executable, "check_config.py", "limits.toml"], cwd=configlab, capture_output=True, encoding="utf-8", check=False)
assert result.returncode == 0 and "Codex loading is not verified" in result.stdout
checks.append("Lesson 44: extra unchecked key still passes; narrow parser does not establish full schema or client loading")
save(configlab / "lesson-16.toml", samples(16, "toml")[0])
result = subprocess.run([sys.executable, "check_config.py", "lesson-16.toml"], cwd=configlab, capture_output=True, encoding="utf-8", check=False)
assert result.returncode == 0
checks.append("Lesson 16: exact authored setting passes the narrow offline checker")
report = {
    "checkedAt": datetime.now(timezone.utc).isoformat(),
    "environment": f"Windows / Python {sys.version.split()[0]} / local reference files",
    "method": "Exact authored examples; no real user config, Codex model request, or effective-client-setting claim",
    "checks": checks,
    "sourceHashes": {name: digest for name, digest in before.items()},
}
(ROOT / "docs/codex-learning/evidence/docs-config-practice.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"Passed {len(checks)} documentation and configuration practice checks")
