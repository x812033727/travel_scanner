"""Build only the paths owned by the second phase; no database or deployment access."""
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[3]
numbers=[0,20,38,41,43,47,51,*range(61,97)]
def run(args):subprocess.run(args,cwd=ROOT,check=True)
run([sys.executable,'tools/claude-code-series/advanced/normalize.py'])
run(['uv','run','--project','apps/api','python','tools/claude-code-series/generate.py','--only',*map(str,numbers)])
run([sys.executable,'tools/claude-code-series/advanced/package-labs.py'])
run(['node','tools/claude-code-series/render-art.mjs','--only',','.join(map(str,numbers)),'--evidence','docs/claude-code-series/advanced/evidence'])
run(['uv','run','--project','apps/api','python','tools/claude-code-series/validate.py','--output','docs/claude-code-series/advanced/evidence/content-validation.json'])
