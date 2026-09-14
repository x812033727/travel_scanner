"""Run the complete web suite in a disposable native WSL source snapshot."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
runtime = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix='mokaair-web-source-')).resolve()
assert runtime.is_relative_to(Path(tempfile.gettempdir()).resolve()) and runtime.name.startswith('mokaair-web-source-')
archive = runtime / 'source.tar.gz'
receipt = {'started_at': datetime.now(timezone.utc).isoformat(), 'environment': 'WSL Ubuntu, Linux ARM64, native temporary filesystem', 'source': 'current working tree, not a different checkout', 'production_access': False}
receipt['setup_recovery'] = 'Fixed Windows UTF-8 path decoding and sent Bash input as bytes to preserve LF line endings; earlier setup attempts did not run Vitest.'
excluded = {'node_modules', '.next', 'test-results', 'playwright-report', 'coverage', '.git'}
files = [ROOT / name for name in ['package.json', 'package-lock.json', 'tools/check-i18n.mjs']]
for directory in ['apps/web', 'apps/api/app/guides/content']:
    for base, dirs, names in os.walk(ROOT / directory):
        dirs[:] = [name for name in dirs if name not in excluded]
        files.extend(Path(base) / name for name in names if not name.startswith('.env') and not name.endswith('.tsbuildinfo'))
hashes = {}
with tarfile.open(archive, 'w:gz', compresslevel=1) as package:
    for path in sorted(files):
        if path.is_symlink():
            raise RuntimeError(f'Unexpected symlink: {path}')
        relative = path.relative_to(ROOT).as_posix()
        hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        package.add(path, arcname=relative, recursive=False)
(OUT / 'web-linux-source-hashes.json').write_text(json.dumps(hashes, indent=2) + '\n', encoding='utf-8')
receipt['source_files'] = len(hashes)
receipt['package_lock_sha256'] = hashes['package-lock.json']
receipt['source_archive_sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
print(f'Source snapshot: {len(hashes)} files, {archive.stat().st_size} bytes', flush=True)

def wsl_path(path):
    return subprocess.check_output(['wsl', '-d', 'Ubuntu', '--exec', 'wslpath', '-a', str(path)], text=True, encoding='utf-8').strip()

# Paths are positional arguments, never inserted into shell source.
script = r'''set -eu
source_archive="$1"
output_dir="$2"
runtime=$(mktemp -d /tmp/mokaair-web-validation-XXXXXX)
printf '%s\n' "$runtime" > "$output_dir/web-linux-runtime.txt"
cd "$runtime"
curl --fail --location --retry 2 -o SHASUMS256.txt https://nodejs.org/dist/v24.13.0/SHASUMS256.txt
curl --fail --location --retry 2 -o node-v24.13.0-linux-arm64.tar.xz https://nodejs.org/dist/v24.13.0/node-v24.13.0-linux-arm64.tar.xz
grep ' node-v24.13.0-linux-arm64.tar.xz$' SHASUMS256.txt > node-checksum.txt
sha256sum -c node-checksum.txt
cp node-checksum.txt "$output_dir/web-linux-node-checksum.txt"
tar -xf node-v24.13.0-linux-arm64.tar.xz
export PATH="$runtime/node-v24.13.0-linux-arm64/bin:$PATH"
export npm_config_cache="$runtime/npm-cache"
mkdir source
tar -xf "$source_archive" -C source
cd source
node --version
npm --version
uname -sm
npm ci --ignore-scripts --no-audit --no-fund
cd apps/web
set +e
node ../../node_modules/vitest/vitest.mjs run --pool=threads --maxWorkers=1 --reporter=default --reporter=json --outputFile="$runtime/web-full-linux.json"
test_exit=$?
set -e
if test -f "$runtime/web-full-linux.json"; then cp "$runtime/web-full-linux.json" "$output_dir/web-full-linux.json"; fi
exit "$test_exit"
'''
try:
    with (OUT / 'web-full-linux.log').open('w', encoding='utf-8') as log:
        result = subprocess.run(['wsl', '-d', 'Ubuntu', '--exec', 'bash', '-s', '--', wsl_path(archive), wsl_path(OUT)], input=script.encode('utf-8'), stdout=log, stderr=subprocess.STDOUT, timeout=2400)
    receipt['exit'] = result.returncode
    report = json.loads((OUT / 'web-full-linux.json').read_text(encoding='utf-8'))
    receipt['passed'] = result.returncode == 0 and report['success'] and report['numFailedTests'] == 0 and report['numTotalTests'] > 0
except Exception as error:
    receipt['passed'] = False
    receipt['error'] = str(error)
finally:
    receipt['finished_at'] = datetime.now(timezone.utc).isoformat()
    (OUT / 'web-linux-validation.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt), flush=True)
raise SystemExit(0 if receipt['passed'] else 1)
