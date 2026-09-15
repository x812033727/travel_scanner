"""Rebuild in dependency order and stop at the first failure; never publish."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
for script in ["render-authors.py", "build-depth.py", "expand-catalog.py"]:
    subprocess.run([sys.executable, "-X", "utf8", str(Path(__file__).with_name(script))], cwd=ROOT, check=True)
subprocess.run(["node", "tools/codex-learning/render.mjs"], cwd=ROOT, check=True)
api_python = ROOT / "apps/api/.venv/Scripts/python.exe"
if not api_python.exists():
    api_python = ROOT / "apps/api/.venv/bin/python"
subprocess.run([str(api_python), "-X", "utf8", "tools/codex-learning/build-series.py"], cwd=ROOT, check=True)
