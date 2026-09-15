"""Observe a real claude -p max-turn failure against a disposable synthetic file."""
from datetime import datetime, timezone
from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import time

out = Path(__file__).resolve().parent
project = Path(tempfile.mkdtemp(prefix='mokaair-headless-limit-'))
(project/'probe.txt').write_text('MOKAAIR-HEADLESS-BOUNDARY-91\n', encoding='utf-8')
(project/'empty-mcp.json').write_text('{"mcpServers":{}}\n', encoding='utf-8')
cli = shutil.which('claude')
assert cli
version = subprocess.check_output([cli, '--version'], text=True).strip()
args = [cli, '-p', 'Use Read to read probe.txt before returning its exact text in marker. Do not guess the file contents.', '--model', 'haiku', '--tools', 'Read', '--allowedTools', 'Read', '--setting-sources', '', '--strict-mcp-config', '--mcp-config', str(project/'empty-mcp.json'), '--max-turns', '1', '--output-format', 'json', '--json-schema', '{"type":"object","properties":{"marker":{"type":"string"}},"required":["marker"],"additionalProperties":false}']
start = time.monotonic()
run = subprocess.run(args, cwd=project, text=True, encoding='utf-8', errors='replace', capture_output=True, timeout=90)
payload = json.loads(run.stdout)
(out/'headless-turn-limit-events.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
result = payload[-1] if isinstance(payload, list) else payload
passed = result.get('type') == 'result' and result.get('is_error') is True and result.get('subtype') == 'error_max_turns'
receipt = {'checked_at': datetime.now(timezone.utc).isoformat(), 'cli_version': version, 'seconds': round(time.monotonic()-start, 3), 'exit_code': run.returncode, 'passed': passed, 'result_type': result.get('type'), 'result_subtype': result.get('subtype'), 'is_error': result.get('is_error'), 'source': 'headless-turn-limit-events.json', 'scope': 'Real one-turn CLI failure with Read-only synthetic input. The caller must reject the error result; it is not an empty successful review.', 'stderr': run.stderr}
(out/'headless-turn-limit.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(receipt))
raise SystemExit(0 if passed else 1)
