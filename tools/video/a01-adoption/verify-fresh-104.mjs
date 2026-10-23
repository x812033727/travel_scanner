#!/usr/bin/env node
// Offline only: independently verify a fresh archive and its complete A01 104
// source chain. A PASS receipt proves source evidence, never installation safety.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { SLUG, PRODUCTION_104_PINS } from './transaction.mjs';
import { verifySource104 } from './source-104.mjs';

const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const exact = (file) => {
  const stat = fs.lstatSync(file);
  assert.ok(stat.isFile() && !stat.isSymbolicLink(), `regular file required: ${file}`);
  return fs.readFileSync(file);
};
const json = (object) => Buffer.from(`${JSON.stringify(object, null, 2)}\n`);

function assertCaptureRoot(captureDir) {
  assert.ok(path.isAbsolute(captureDir), 'absolute capture directory required');
  const root = path.resolve(captureDir);
  const stat = fs.lstatSync(root);
  assert.ok(stat.isDirectory() && !stat.isSymbolicLink(), 'real capture directory required');
  assert.equal(fs.realpathSync(root).toLowerCase(), root.toLowerCase(),
    'linked capture directory refused');
  return root;
}

function removeOwnedTemp(temp) {
  const base = path.resolve(os.tmpdir());
  const resolved = path.resolve(temp);
  assert.ok(resolved.startsWith(`${base}${path.sep}`)
    && path.basename(resolved).startsWith('a01-104-'),
  'temporary cleanup path escaped OS Temp');
  const stat = fs.lstatSync(resolved);
  assert.ok(stat.isDirectory() && !stat.isSymbolicLink(),
    'temporary cleanup target changed');
  fs.rmSync(resolved, { recursive: true, force: false });
}

/** Recomputes the receipt. The fixed capture-helper import is an integration
 * dependency: until that independently reviewed helper is merged, this HOLDs.
 */
export async function verifyFresh104(captureDir) {
  const root = assertCaptureRoot(captureDir);
  let verifyCapture;
  try {
    ({ verifyCapture } = await import('../a01-capture/verify-archive.mjs'));
  } catch (error) {
    if (error?.code === 'ERR_MODULE_NOT_FOUND')
      throw Error('CAPTURE_VERIFIER_NOT_IN_RELEASE_HOLD', { cause: error });
    throw error;
  }
  assert.equal(typeof verifyCapture, 'function', 'capture verifier export missing');
  const reportFile = path.join(root, 'capture-report.json');
  const reportBytes = exact(reportFile);
  const report = JSON.parse(reportBytes);
  const archive = path.join(root, 'a01-source.tar');
  const archiveExpected = report.files?.['a01-source.tar'];
  assert.equal(report.schema_version, 1);
  assert.equal(report.slug, SLUG);
  assert.equal(report.status, 'HOLD');
  assert.equal(report.production_adoption_allowed, false);
  assert.ok(archiveExpected && /^[0-9a-f]{64}$/u.test(archiveExpected.sha256));
  const archiveResult = await verifyCapture(root);
  assert.equal(archiveResult.audit_events, 104, 'capture must contain exactly 104 events');
  assert.equal(report.audit_events, 104, 'capture report event count changed');
  assert.ok(exact(reportFile).equals(reportBytes), 'capture report changed while verifying');

  // Extraction is permitted only from a private byte-for-byte copy of the
  // already verified archive. A changed copy fails before tar sees it.
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'a01-104-'));
  try {
    const privateArchive = path.join(temp, 'verified-source.tar');
    fs.copyFileSync(archive, privateArchive, fs.constants.COPYFILE_EXCL);
    const copied = exact(privateArchive);
    assert.equal(sha(copied), archiveExpected.sha256,
      'archive changed after independent membership verification');
    assert.equal(copied.length, archiveExpected.bytes,
      'archive size changed after independent membership verification');
    const extracted = path.join(temp, 'source');
    fs.mkdirSync(extracted, { mode: 0o700 });
    execFileSync('tar', ['-xf', privateArchive, '-C', extracted], {
      windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'], maxBuffer: 1024 * 1024,
    });
    const roots = { docs: path.join(extracted, 'docs', 'videos'), work: extracted };
    const source = verifySource104(roots);
    assert.equal(source.oldAudit.count, PRODUCTION_104_PINS.audit_file_count);
    assert.equal(source.source, PRODUCTION_104_PINS.source_sha256);
    assert.equal(source.oldIndexSha, PRODUCTION_104_PINS.tip_index_sha256);
    assert.equal(source.oldAudit.sha256, PRODUCTION_104_PINS.audit_inventory_sha256);
    assert.ok(exact(reportFile).equals(reportBytes),
      'capture report changed after 104 verification');
    const fileHashes = Object.fromEntries(Object.entries(report.files).sort(([a], [b]) =>
      a < b ? -1 : a > b ? 1 : 0).map(([name, item]) => [name, item.sha256]));
    return {
      schema_version: 1,
      kind: 'a01_fresh_104_capture_independent_verification',
      status: 'PASS',
      verification_scope: 'ARCHIVE_MEMBERSHIP_AND_IMMUTABLE_104_ONLY',
      production_adoption_allowed: false,
      slug: SLUG,
      capture_manifest_sha256: sha(reportBytes),
      capture_files_sha256: fileHashes,
      archive_sha256: archiveExpected.sha256,
      archive_members: archiveResult.files,
      archive_receipts: archiveResult.receipts,
      lexicon_files: archiveResult.lexicon_files,
      source_sha256: source.source,
      old_event_id: source.oldEventId,
      old_index_sha256: source.oldIndexSha,
      old_audit_inventory_sha256: source.oldAudit.sha256,
      old_audit_file_count: source.oldAudit.count,
      audit_events: 104,
      release_sha: report.release_sha,
      capture_operational_status: report.status,
      capture_consistent: report.capture_consistent,
      capture_issues: report.issues,
    };
  } finally { removeOwnedTemp(temp); }
}

export function saveNewReceipt(file, receipt) {
  assert.ok(path.isAbsolute(file), 'absolute receipt path required');
  assert.equal(receipt.kind, 'a01_fresh_104_capture_independent_verification');
  assert.equal(receipt.status, 'PASS');
  assert.equal(receipt.production_adoption_allowed, false);
  const fd = fs.openSync(file, 'wx', 0o600);
  try { fs.writeFileSync(fd, json(receipt)); fs.fsyncSync(fd); }
  finally { fs.closeSync(fd); }
  return sha(exact(file));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.length !== 6 || process.argv[2] !== '--capture'
    || process.argv[4] !== '--out') {
    process.stderr.write('Usage: node verify-fresh-104.mjs --capture ABS_DIR --out ABS_RECEIPT.json\n');
    process.exitCode = 2;
  } else {
    verifyFresh104(process.argv[3]).then((receipt) => {
      const receiptHash = saveNewReceipt(process.argv[5], receipt);
      process.stdout.write(`A01 source-only 104 PASS, receipt SHA-256 ${receiptHash}; production HOLD.\n`);
    }).catch((error) => {
      process.stderr.write(`A01 fresh 104 HOLD: ${error.message}\n`);
      process.exitCode = 2;
    });
  }
}
