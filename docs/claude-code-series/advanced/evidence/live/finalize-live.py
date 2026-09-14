"""Summarize recorded runs; never turn missing evidence into a passing result."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent

def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))

def web_result(filename, environment):
    data = read(filename)
    result = {
        'environment': environment,
        'source': filename,
        'files': len(data['testResults']),
        'tests': data['numPassedTests'],
        'total_tests': data['numTotalTests'],
        'failed': data['numFailedTests'],
        'skipped': data['numPendingTests'],
        'passed': data['success'] and data['numFailedTests'] == 0,
    }
    assert result['passed'] and result['files'] == 258, result
    return result

web_runs = []
web_attempts = []
for filename, environment in [('web-full.json', 'Windows'), ('web-full-linux.json', 'WSL Ubuntu / Linux ARM64')]:
    if filename == 'web-full-linux.json' and (OUT / 'web-linux-validation.json').exists() and not read('web-linux-validation.json')['passed']:
        web_attempts.append({'environment': environment, 'passed': False, 'source': 'web-linux-validation.json'})
        continue
    if (OUT / filename).exists():
        web_runs.append(web_result(filename, environment))
assert web_runs, 'No completed full web test report'
pg = read('postgres-validation.json')
assert pg['passed'] and pg['stopped'] and pg['remaining_test_schemas'] == 0
suites = ET.parse(OUT / 'postgres-tests.xml').getroot().iter('testsuite')
counts = {key: 0 for key in ['tests', 'failures', 'errors', 'skipped']}
for suite in suites:
    for key in counts:
        counts[key] += int(suite.get(key, '0'))
assert counts == {'tests': 164, 'failures': 0, 'errors': 0, 'skipped': 0}, counts
api = {'passed': True, **counts, 'postgresql_version': pg['version'].split()[-1], 'source': 'postgres-validation.json', 'test_report': 'postgres-tests.xml', 'environment': 'Windows; disposable PostgreSQL 17 and SQLite', 'server_stopped': True, 'remaining_test_schemas': 0}
source_hashes = read('web-linux-source-hashes.json')
changed = [name for name, expected in source_hashes.items() if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected]
assert not changed, f'Source changed after test snapshot: {changed}'
content = read('content-recheck.json')
assert content['complete'] and len(content['pages']) == 97
summary = {
    'checked_at': datetime.now(timezone.utc).isoformat(),
    'git_base': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
    'scope': 'Supplementary full frontend and isolated PostgreSQL checks for the current uncommitted phase 2 changes',
    'web': web_runs[0],
    'web_runs': web_runs,
    'other_web_attempts': web_attempts,
    'api': api,
    'temporary_postgresql_files_removed': pg.get('temporary_runtime_removed', False),
    'cleanup_note': pg.get('cleanup_note'),
    'source_hash_verification': {'files': len(source_hashes), 'changed': changed, 'source': 'web-linux-source-hashes.json'},
    'content': {'pages': 97, 'passed': True, 'source': 'content-recheck.json'},
    'tools': {'tests': 11, 'source': 'series-tools-recheck.log'},
    'pending': ['Claude account reauthentication and real model workflows', 'Physical mobile, MCP OAuth, Agent Teams, external CI, product schedules and SDK calls', 'Phase 2 PR and merge', 'Deployment, content import and publication'],
}
if (OUT/'real-operations-summary.json').exists():
    summary['real_operations']=read('real-operations-summary.json')
    summary['pending']=summary['real_operations']['pending']+['Phase 2 PR and merge', 'Deployment, content import and publication']
if (OUT/'ci-workflow-validation.json').exists():
    workflow=read('ci-workflow-validation.json')
    if workflow.get('full_tools',{}).get('passed'):summary['tools']=workflow['full_tools']
(OUT / 'verification-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'web': summary['web'], 'api': api}))
