import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { applyFixture, inspectFixture, SimulatedCrash } from './fixture.mjs';

const slug = 'story-rolling-suitcase-v2';
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
function write(root, rel, bytes) {
  const file = path.join(root, ...rel.split('/'));
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, bytes);
  return file;
}
function inventory(root) {
  const rows = [];
  function visit(dir, prefix = '') {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const rel = prefix ? `${prefix}/${entry.name}` : entry.name;
      const file = path.join(dir, entry.name);
      if (entry.isDirectory()) visit(file, rel);
      else rows.push([rel, sha(fs.readFileSync(file))]);
    }
  }
  visit(root);
  rows.sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0);
  return { count: rows.length, sha256: sha(rows.map(([rel, hash]) => `${rel}\0${hash}\n`).join('')) };
}
function setup(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'a01-105-offline-test-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const source = path.join(root, 'source');
  fs.mkdirSync(source);
  const auditRel = `${slug}/story/recheck-audit`;
  for (let n = 0; n < 104; n++)
    write(source, `${auditRel}/event-${String(n).padStart(3, '0')}/index.json`,
      json({ schema_version: 1, n, after_source_sha256: `old-${n}` }));
  const changeNames = [
    `${slug}/auto.json`, `docs/videos/${slug}/series.json`,
    `docs/videos/${slug}/video.json`,
    ...['hook', 'origin', 'idea', 'engine', 'turn', 'now'].map((key) => `${slug}/story/chapters/${key}.json`),
  ];
  const changes = new Map(changeNames.map((rel, i) => {
    write(source, rel, json({ source: i }));
    return [rel, json({ candidate: i, status: 'UNCHECKED' })];
  }));
  for (let n = 0; n < 254 - 104 - changeNames.length; n++)
    write(source, `unrelated/filler-${String(n).padStart(3, '0')}.txt`, `unchanged ${n}\n`);
  const captured = inventory(source);
  assert.equal(captured.count, 254);
  const audit = inventory(path.join(source, ...auditRel.split('/')));
  const event = { id: 'r16-existing-revision-synthetic',
    result_kind: 'OFFLINE_PROPOSAL_ONLY_DO_NOT_INSTALL',
    before_source_sha256: 'a'.repeat(64), after_source_sha256: 'b'.repeat(64),
    old_audit_file_count: audit.count, old_audit_inventory_sha256: audit.sha256 };
  const gates = { production_status: 'HOLD', installation_allowed: false,
    capture_inventory_sha256: captured.sha256, editorial_manifest_sha256: 'c'.repeat(64) };
  const proposal = { changes, event, gates };
  write(root, 'A01-105-OFFLINE-FIXTURE.json', json({ schema_version: 1,
    slug, offline_fixture: true, allow_production: false }));
  write(root, 'STOP', 'synthetic A01 STOP\n');
  const evidence = { schema_version: 1, synthetic: true, slug,
    before_source_sha256: event.before_source_sha256,
    capture_inventory_sha256: captured.sha256,
    stop_sha256: sha(fs.readFileSync(path.join(root, 'STOP'))),
    lease_present: false, budget_limit_usd: '25.00', budget_reserved_usd: '0.00',
    budget_settled_usd: '0.00', budget_operations: 0,
    stage_running: 0, stage_queued: 0, media_running: 0, media_queued: 0,
    paid_calls_in_flight: 0, unresolved_run_receipts: 0,
    global_paid_running: 0, global_paid_queued: 0,
    hold: true, owner_approval: 'SYNTHETIC_ONLY', production_install_allowed: false };
  return { root, source, auditRel, proposal, evidence, captured, audit };
}

test('synthetic 105 preserves all 104 old audit bytes and remains HOLD', (t) => {
  const f = setup(t);
  assert.equal(inspectFixture(f.proposal, f.root), 'READY_SYNTHETIC_HELD');
  const receipt = applyFixture(f.proposal, f.root, f.evidence);
  assert.deepEqual(receipt, { status: 'SYNTHETIC_COMMITTED_HELD', production_status: 'HOLD', paid_calls: 0 });
  assert.equal(inspectFixture(f.proposal, f.root), 'SYNTHETIC_COMMITTED_HELD');
  assert.deepEqual(inventory(path.join(f.source, ...f.auditRel.split('/'))).count, 105);
  assert.equal(fs.readFileSync(path.join(f.root, 'STOP'), 'utf8'), 'synthetic A01 STOP\n');
  assert.throws(() => applyFixture(f.proposal, f.root, f.evidence), /STALE_CAPTURE|PENDING_TRANSACTION/);
});

test('stale source, altered STOP, LEASE, job and budget drift all refuse before intent', (t) => {
  const f = setup(t);
  const bads = [
    [{ stage_running: 1 }, /JOB_DRIFT_stage_running/],
    [{ global_paid_running: 1 }, /JOB_DRIFT_global_paid_running/],
    [{ global_paid_queued: 1 }, /JOB_DRIFT_global_paid_queued/],
    [{ budget_reserved_usd: '0.01' }, /BUDGET_DRIFT/],
    [{ budget_limit_usd: '24.00' }, /BUDGET_DRIFT/],
    [{ capture_inventory_sha256: 'd'.repeat(64) }, /SAFETY_CAPTURE_DRIFT/],
  ];
  for (const [change, pattern] of bads) {
    assert.throws(() => applyFixture(f.proposal, f.root, { ...f.evidence, ...change }), pattern);
    assert.equal(fs.existsSync(path.join(f.root, 'transaction')), false);
  }
  write(f.root, 'LEASE', 'foreign owner\n');
  assert.throws(() => applyFixture(f.proposal, f.root, f.evidence), /LEASE_COLLISION/);
  fs.unlinkSync(path.join(f.root, 'LEASE'));
  fs.writeFileSync(path.join(f.root, 'STOP'), 'different STOP\n');
  assert.throws(() => applyFixture(f.proposal, f.root, f.evidence), /STOP_DRIFT/);
  fs.writeFileSync(path.join(f.root, 'STOP'), 'synthetic A01 STOP\n');
  fs.writeFileSync(path.join(f.source, `${slug}/auto.json`), 'stale source\n');
  assert.throws(() => applyFixture(f.proposal, f.root, f.evidence), /STALE_CAPTURE/);
  assert.equal(inspectFixture(f.proposal, f.root), 'DRIFT_HOLD');
});

test('a queued global paid job appearing before synthetic source write retains HOLD', (t) => {
  const f = setup(t);
  const before = inventory(f.source);
  assert.throws(() => applyFixture(f.proposal, f.root, f.evidence, {
    prewriteEvidence: { ...f.evidence, global_paid_queued: 1 },
  }), /JOB_DRIFT_global_paid_queued/);
  assert.deepEqual(inventory(f.source), before, 'no source file may change');
  assert.equal(inspectFixture(f.proposal, f.root), 'PARTIAL_HOLD_MANUAL_RECOVERY_REQUIRED');
  assert.ok(fs.existsSync(path.join(f.root, 'STOP')));
});

for (const phase of ['intent', 'backup', 'sources', 'event']) {
  test(`synthetic crash at ${phase} never permits blind retry`, (t) => {
    const f = setup(t);
    assert.throws(() => applyFixture(f.proposal, f.root, f.evidence, { crashAt: phase }),
      (error) => error instanceof SimulatedCrash && error.phase === phase);
    assert.equal(inspectFixture(f.proposal, f.root), phase === 'event'
      ? 'SYNTHETIC_COMMITTED_HELD' : 'PARTIAL_HOLD_MANUAL_RECOVERY_REQUIRED');
    assert.throws(() => applyFixture(f.proposal, f.root, f.evidence));
    assert.ok(fs.existsSync(path.join(f.root, 'STOP')));
  });
}

test('fixture refuses unmarked and non-temp roots', (t) => {
  const f = setup(t);
  fs.unlinkSync(path.join(f.root, 'A01-105-OFFLINE-FIXTURE.json'));
  assert.throws(() => applyFixture(f.proposal, f.root, f.evidence), /FIXTURE_MARKER_REQUIRED/);
  assert.throws(() => applyFixture(f.proposal, path.resolve('.'), f.evidence), /FIXTURE_MUST_BE_UNDER_OS_TEMP/);
});

test('fixture refuses a Temp ancestor junction that resolves outside Temp', (t) => {
  const f = setup(t);
  const junction = path.join(f.root, 'escape-junction');
  try { fs.symlinkSync(path.dirname(os.homedir()), junction, 'junction'); }
  catch (error) {
    if (['EPERM', 'EACCES', 'ENOSYS'].includes(error.code)) {
      t.diagnostic(`junction creation unavailable: ${error.code}`);
      return;
    }
    throw error;
  }
  try {
    const escaped = path.join(junction, path.basename(os.homedir()));
    assert.ok(fs.lstatSync(escaped).isDirectory() && !fs.lstatSync(escaped).isSymbolicLink());
    assert.throws(() => applyFixture(f.proposal, escaped, f.evidence), /FIXTURE_REALPATH_ESCAPE/);
  } finally { fs.unlinkSync(junction); }
});
