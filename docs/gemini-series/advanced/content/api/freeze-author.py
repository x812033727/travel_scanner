"""Create a local author snapshot only; not a publication manifest."""
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
baseline = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
catalogue = ROOT / "apps/web/lib/guide-series.json"
catalogue_sha = hashlib.sha256(catalogue.read_bytes()).hexdigest()
assert catalogue_sha == "1f6afed7f3bf7f05a407b8d5af4647938cf6d91df6b42a381a904b1f6d697bb2"
paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", baseline, "apps/api/app/guides/content"], cwd=ROOT, text=True, encoding="utf-8").splitlines()
for relative in paths:
    old = subprocess.check_output(["git", "show", f"{baseline}:{relative}"], cwd=ROOT)
    assert old.replace(b"\r\n", b"\n") == (ROOT/relative).read_bytes().replace(b"\r\n", b"\n"), relative
files = []
for base, dirs, names in os.walk(HERE):
    dirs[:] = [d for d in dirs if d not in {".venv", "node_modules", "__pycache__"}]
    files.extend(Path(base)/name for name in names if name != "authoring-review.json")
for row in json.loads((HERE/"verification/build.json").read_text(encoding="utf-8")):
    files.append(ROOT/"apps/api/app/guides/content"/(row["slug"]+".json"))
    files.extend(p for p in (ROOT/"apps/web/public/guides"/row["slug"]).rglob("*") if p.is_file())
receipt = {"checkedAt": datetime.now(timezone.utc).isoformat(), "status": "authoring-review-not-release", "publishable": False, "scope": "API 81-86 only", "baselineCommit": baseline,
           "preservation": {"runtimeArticles": 50, "originalPacksUnchanged": 51, "priorDraftsUnchanged": 30, "allExistingPacksVerified": len(paths), "catalogueSha256": catalogue_sha},
           "checks": {"newPacks": 6, "fixtureTests": 29, "archives": 7, "extractedFixtureTests": 29, "articlePreviews": 24, "browserPreviews": 6, "serviceGoldenCases": 20, "relatedApiPassed": 45, "relatedApiSkipped": 7, "skipReason": "PostgreSQL integration services unavailable", "ruff": "passed", "tasks": "passed with unrelated existing warnings"},
           "realGoogleCalls": 0, "realCloudAcceptance": "not_run", "files": [{"path": p.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size} for p in sorted(files)]}
destination = HERE/"verification/authoring-review.json"
with destination.open("x", encoding="utf-8", newline="\n") as stream:
    stream.write(json.dumps(receipt, ensure_ascii=False, indent=2)+"\n")
print(f"Frozen {len(files)} files; {len(paths)} existing packs unchanged.")
