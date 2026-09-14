"""Run the existing lesson 94 SDK example twice in an isolated working directory."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
SDK = ROOT / 'tools/claude-code-series/advanced/lab/automation/sdk'
directory = Path(tempfile.mkdtemp(prefix='mokaair-sdk-live-')).resolve()
env = {**os.environ, 'CLAUDE_BIN': shutil.which('claude')}
report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'scope': 'Lesson 94 query and resume in a disposable directory using only a synthetic marker', 'sdk_version': json.loads((SDK/'package.json').read_text(encoding='utf-8'))['dependencies']['@anthropic-ai/claude-agent-sdk'], 'source_sha256': hashlib.sha256((SDK/'run.mjs').read_bytes()).hexdigest(), 'runs': []}
for name, args in [('query', []), ('resume', ['--resume'])]:
    try:
        run = subprocess.run([shutil.which('node'), str(SDK/'run.mjs'), *args], cwd=directory, env=env, capture_output=True, text=True, encoding='utf-8', timeout=100)
        state_path = directory/'run-data/session.json'
        state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
        passed = run.returncode == 0 and state.get('status') == 'completed' and 'MOKAAIR-SDK-94' in state.get('result', '')
        report['runs'].append({'case': name, 'exit': run.returncode, 'passed': passed, 'state': state, 'stderr': run.stderr[-2000:]})
    except subprocess.TimeoutExpired:
        report['runs'].append({'case': name, 'passed': False, 'error': '100-second timeout'})
    (OUT/'sdk-query-resume.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'case': name, 'passed': report['runs'][-1]['passed']}), flush=True)
    if not report['runs'][-1]['passed']:
        break
report['passed'] = len(report['runs']) == 2 and all(r['passed'] for r in report['runs']) and report['runs'][0]['state']['sessionId'] == report['runs'][1]['state']['sessionId']
report['finished_at'] = datetime.now(timezone.utc).isoformat()
report['temporary_directory'] = str(directory)
(OUT/'sdk-query-resume.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
raise SystemExit(0 if report['passed'] else 1)
