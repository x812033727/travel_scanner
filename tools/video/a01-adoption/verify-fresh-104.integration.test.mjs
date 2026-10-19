// Optional offline integration against an independently reviewed capture
// helper checkout and a real capture. CI has neither input, so it skips.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import test from 'node:test';
import { PRODUCTION_104_PINS } from './transaction.mjs';

const captureDir = process.env.A01_VERIFIED_CAPTURE_DIR;
const helperDir = process.env.A01_CAPTURE_HELPER_DIR;

test('fresh capture archive and full immutable 104 chain issue a source-only receipt',
  { skip: !captureDir || !helperDir }, async (t) => {
    assert.ok(path.isAbsolute(captureDir) && path.isAbsolute(helperDir));
    const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'a01-verifier-integration-'));
    try {
      const video = path.join(temp, 'tools', 'video');
      fs.mkdirSync(video, { recursive: true });
      const copy = (source, destination) => {
        fs.mkdirSync(path.dirname(destination), { recursive: true });
        fs.copyFileSync(source, destination, fs.constants.COPYFILE_EXCL);
      };
      const copyModules = (relative) => {
        const sourceRoot = path.join(process.cwd(), 'tools', 'video', relative);
        const walk = (dir) => {
          for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
            assert.ok(!entry.isSymbolicLink(), 'linked module in test checkout');
            const source = path.join(dir, entry.name);
            if (entry.isDirectory()) walk(source);
            else if (entry.isFile() && entry.name.endsWith('.mjs')) {
              const rel = path.relative(sourceRoot, source);
              copy(source, path.join(video, relative, rel));
            }
          }
        };
        walk(sourceRoot);
      };
      for (const name of ['verify-fresh-104.mjs', 'source-104.mjs', 'transaction.mjs'])
        copy(path.join(process.cwd(), 'tools', 'video', 'a01-adoption', name),
          path.join(video, 'a01-adoption', name));
      for (const directory of ['core', 'screencast', 'production'])
        copyModules(directory);
      for (const name of ['verify-archive.mjs', 'capture.mjs'])
        copy(path.join(helperDir, name), path.join(video, 'a01-capture', name));
      const { verifyFresh104, saveNewReceipt } = await import(pathToFileURL(
        path.join(video, 'a01-adoption', 'verify-fresh-104.mjs')).href);
      const receipt = await verifyFresh104(captureDir);
      assert.equal(receipt.kind, 'a01_fresh_104_capture_independent_verification');
      assert.equal(receipt.status, 'PASS');
      assert.equal(receipt.verification_scope,
        'ARCHIVE_MEMBERSHIP_AND_IMMUTABLE_104_ONLY');
      assert.equal(receipt.production_adoption_allowed, false);
      assert.equal(receipt.audit_events, 104);
      assert.equal(receipt.source_sha256, PRODUCTION_104_PINS.source_sha256);
      assert.equal(receipt.old_index_sha256, PRODUCTION_104_PINS.tip_index_sha256);
      assert.equal(receipt.old_audit_inventory_sha256,
        PRODUCTION_104_PINS.audit_inventory_sha256);
      assert.equal(receipt.old_audit_file_count, 222);
      const receiptFile = path.join(temp, 'verified-source-only.json');
      assert.match(saveNewReceipt(receiptFile, receipt), /^[0-9a-f]{64}$/);
      assert.deepEqual(JSON.parse(fs.readFileSync(receiptFile, 'utf8')), receipt);
      t.diagnostic(`source-only PASS; ${receipt.audit_events} events, `
        + `${receipt.old_audit_file_count} audit files; operational `
        + `${receipt.capture_consistent ? 'REVIEW_REQUIRED' : 'HOLD'}`);
    } finally {
      const base = path.resolve(os.tmpdir());
      const resolved = path.resolve(temp);
      assert.ok(resolved.startsWith(`${base}${path.sep}`)
        && path.basename(resolved).startsWith('a01-verifier-integration-'));
      const stat = fs.lstatSync(resolved);
      assert.ok(stat.isDirectory() && !stat.isSymbolicLink());
      fs.rmSync(resolved, { recursive: true });
    }
  });
