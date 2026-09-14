"""Record observed command exits and parse current post-main test receipts."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'docs/claude-code-series/advanced/evidence'
LIVE = E / 'live'

def read(name):
    return json.loads((LIVE / name).read_text(encoding='utf-8'))

first = read('web-focused-main-retry.json')
retry = read('web-server-main-retry.json')
assert first['numPassedTests'] == 50 and first['numFailedTests'] == 0
assert retry['success'] and retry['numPassedTests'] == 23 and retry['numFailedTests'] == 0
assert 'Timeout waiting for worker to respond' in (LIVE / 'web-focused-main-retry.log').read_text(encoding='utf-8')
assert '23 passed' in (LIVE / 'web-server-main-retry.log').read_text(encoding='utf-8')
browser = json.loads((E / 'browser-main-retry.json').read_text(encoding='utf-8'))
assert browser['stats']['expected'] == 9 and browser['stats']['unexpected'] == 0
suite = ET.parse(LIVE / 'api-main-tests.xml').getroot().find('testsuite')
assert suite is not None and suite.attrib['failures'] == '0' and suite.attrib['errors'] == '0'
commands = []
for command, log in [
    ('npm ci --ignore-scripts', 'npm-ci-main-retry.log'),
    ('npm run build:web', 'build-main.log'),
    ('npm run lint:web', 'lint-main.log'),
    ('npm run check:i18n', 'i18n-main.log'),
    ('npm run typecheck:web', 'typecheck-main.log'),
    ('npm run test:tools', 'tools-main.log'),
    ('npm run check:tasks', 'tasks-main.log'),
    ('cd apps/api; uv run ruff check .', 'ruff-main.log'),
    ('cd apps/api; uv run mypy app', 'mypy-main.log'),
    ('cd apps/api; uv run pytest tests/test_guide_series.py', 'api-main-tests.log'),
]:
    path = LIVE / log
    assert path.is_file()
    commands.append({'command': command, 'observed_exit': 0, 'log': log, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})

result = {
    'checked_at': datetime.now(timezone.utc).isoformat(),
    'scope': 'After merging origin/main 8c83e90a; current local checks, not CI or release approval',
    'local_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
    'node': '24.15.0 win-arm64',
    'commands': commands,
    'affected_web_tests': {
        'numTotalTests': 73, 'numPassedTests': 73, 'numFailedTests': 0, 'numPendingTests': 0,
        'scope': 'Union of four completed suites and the isolated missing server suite; not a successful single invocation',
        'attempts': [
            {'source': 'web-focused-main.json', 'exit': 1, 'reason': 'worker startup timeout; JSON success alone is insufficient'},
            {'source': 'web-focused-main-retry.json', 'exit': 1, 'passed_tests': 50, 'reason': 'guides.server worker startup timeout'},
            {'source': 'web-server-main.log', 'exit': 1, 'reason': 'incorrect path to hoisted Vitest; no test executed'},
            {'source': 'web-server-main-retry.json', 'exit': 0, 'passed_tests': 23, 'pool': 'forks'},
        ],
    },
    'api': {'passed': int(suite.attrib['tests'])-int(suite.attrib['skipped']), 'skipped': int(suite.attrib['skipped']), 'source': 'api-main-tests.xml', 'note': 'PostgreSQL was not running in this local invocation. Historical 164-test run is separate; current CI supplies integration services.'},
    'browser': {'passed': 9, 'source': '../browser-main-retry.json', 'previous_attempt': '../browser-main.json', 'note': 'First attempt lacked the matching Chromium revision after main updated Playwright; installed it before retry. Viewport emulation is not a physical phone.'},
}
(LIVE / 'post-main-checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'web_assertions_passed': 73, 'browser_passed': 9, 'api': result['api']}))
