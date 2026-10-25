import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import test from 'node:test';

const here = dirname(fileURLToPath(import.meta.url));

for (const filename of [
  'host-cutover-driver.test.py',
  'host-cutover-driver.deploy-guard.test.py',
]) {
  test(`Linux A01 host cutover safety: ${filename}`, { skip: process.platform !== 'linux' }, () => {
    const result = spawnSync('python3', [join(here, filename)], {
      cwd: here,
      encoding: 'utf8',
      timeout: 60_000,
      maxBuffer: 1024 * 1024,
    });
    assert.equal(result.error, undefined, result.error?.message);
    assert.equal(result.status, 0, `${filename}\n${result.stdout}\n${result.stderr}`);
  });
}
