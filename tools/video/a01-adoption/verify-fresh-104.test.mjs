import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { saveNewReceipt, verifyFresh104 } from './verify-fresh-104.mjs';

test('independent source receipt is create-only and cannot grant production adoption', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'a01-receipt-test-'));
  try {
    const file = path.join(dir, 'source-verification.json');
    const receipt = {
      kind: 'a01_fresh_104_capture_independent_verification',
      status: 'PASS', production_adoption_allowed: false,
    };
    assert.match(saveNewReceipt(file, receipt), /^[0-9a-f]{64}$/);
    assert.deepEqual(JSON.parse(fs.readFileSync(file, 'utf8')), receipt);
    assert.throws(() => saveNewReceipt(file, receipt), { code: 'EEXIST' });
    assert.throws(() => saveNewReceipt(path.join(dir, 'unsafe.json'), {
      ...receipt, production_adoption_allowed: true,
    }), /true !== false/);
  } finally {
    assert.ok(path.resolve(dir).startsWith(`${path.resolve(os.tmpdir())}${path.sep}`));
    assert.ok(fs.lstatSync(dir).isDirectory() && !fs.lstatSync(dir).isSymbolicLink());
    fs.rmSync(dir, { recursive: true });
  }
});

test('fresh verifier refuses a missing absolute capture before attempting import', async () => {
  const missing = path.join(os.tmpdir(), `a01-missing-${process.pid}-${Date.now()}`);
  await assert.rejects(verifyFresh104(missing), { code: 'ENOENT' });
});
