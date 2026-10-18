// Deliberately synthetic two-store crash exercise. No production entry point.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const slug = 'story-rolling-suitcase-v2';
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const need = (yes, code) => { if (!yes) throw Error(code); };
export class SimulatedCrash extends Error { constructor(phase) { super(`SIMULATED_CRASH_${phase}`); this.phase = phase; } }

function safeFixture(root) {
  need(path.isAbsolute(root), 'FIXTURE_ABSOLUTE_ROOT_REQUIRED');
  const resolved = path.resolve(root), temp = path.resolve(os.tmpdir());
  need(resolved.startsWith(temp + path.sep), 'FIXTURE_MUST_BE_UNDER_OS_TEMP');
  need(fs.lstatSync(resolved).isDirectory() && !fs.lstatSync(resolved).isSymbolicLink(), 'FIXTURE_ROOT_UNSAFE');
  // A lexical child of Temp can still escape through a junction in an ancestor.
  const realTemp = fs.realpathSync.native(temp);
  const realRoot = fs.realpathSync.native(resolved);
  const relative = path.relative(realTemp, realRoot);
  need(relative && relative !== '..' && !relative.startsWith(`..${path.sep}`)
    && !path.isAbsolute(relative), 'FIXTURE_REALPATH_ESCAPE');
  const marker = path.join(resolved, 'A01-105-OFFLINE-FIXTURE.json');
  need(fs.existsSync(marker), 'FIXTURE_MARKER_REQUIRED');
  const raw = fs.readFileSync(marker);
  const parsed = JSON.parse(raw);
  need(parsed.schema_version === 1 && parsed.slug === slug && parsed.offline_fixture === true
    && parsed.allow_production === false, 'FIXTURE_MARKER_INVALID');
  return resolved;
}
function at(root, rel) {
  need(typeof rel === 'string' && rel && !/[\\:\x00-\x1f]/u.test(rel)
    && rel.split('/').every((part) => part && part !== '.' && part !== '..'), 'UNSAFE_RELATIVE_PATH');
  let file = root;
  for (const part of rel.split('/')) {
    file = path.join(file, part);
    if (fs.existsSync(file)) need(!fs.lstatSync(file).isSymbolicLink(), 'SYMLINK_IN_FIXTURE');
  }
  return file;
}
function inventory(root, omit = new Set()) {
  const rows = [];
  function visit(dir, rel = '') {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      need(!entry.isSymbolicLink(), 'FIXTURE_SYMLINK_REFUSED');
      const name = rel ? `${rel}/${entry.name}` : entry.name;
      if (omit.has(name)) continue;
      const file = path.join(dir, entry.name);
      if (entry.isDirectory()) visit(file, name);
      else { need(entry.isFile(), 'FIXTURE_SPECIAL_FILE_REFUSED'); rows.push([name, sha(fs.readFileSync(file))]); }
    }
  }
  visit(root);
  rows.sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0);
  return { count: rows.length, sha256: sha(rows.map(([rel, hash]) => `${rel}\0${hash}\n`).join('')) };
}
function oldAudit(proposal, source) {
  const base = path.join(source, slug, 'story', 'recheck-audit');
  const omit = new Set([proposal.event.id]);
  const result = inventory(base, omit);
  need(result.count === proposal.event.old_audit_file_count
    && result.sha256 === proposal.event.old_audit_inventory_sha256, '104_AUDIT_BYTES_DRIFT');
}
function safety(proposal, fixture, evidence) {
  need(evidence && evidence.schema_version === 1 && evidence.synthetic === true, 'SYNTHETIC_SAFETY_ONLY');
  need(evidence.slug === slug && evidence.before_source_sha256 === proposal.event.before_source_sha256,
    'SAFETY_SOURCE_DRIFT');
  need(evidence.capture_inventory_sha256 === proposal.gates.capture_inventory_sha256,
    'SAFETY_CAPTURE_DRIFT');
  const stop = at(fixture, 'STOP');
  need(fs.existsSync(stop) && fs.lstatSync(stop).isFile() && !fs.lstatSync(stop).isSymbolicLink(), 'STOP_REQUIRED');
  need(sha(fs.readFileSync(stop)) === evidence.stop_sha256, 'STOP_DRIFT');
  need(!fs.existsSync(at(fixture, 'LEASE')) && evidence.lease_present === false, 'LEASE_COLLISION');
  need(evidence.budget_limit_usd === '25.00' && evidence.budget_reserved_usd === '0.00'
    && evidence.budget_settled_usd === '0.00' && evidence.budget_operations === 0,
  'BUDGET_DRIFT');
  for (const field of ['stage_running', 'stage_queued', 'media_running', 'media_queued',
    'paid_calls_in_flight', 'unresolved_run_receipts', 'global_paid_running',
    'global_paid_queued'])
    need(evidence[field] === 0, `JOB_DRIFT_${field}`);
  need(evidence.hold === true && evidence.owner_approval === 'SYNTHETIC_ONLY'
    && evidence.production_install_allowed === false, 'FIXTURE_NOT_HELD');
  return sha(fs.readFileSync(stop));
}
function assertBefore(proposal, source) {
  const inv = inventory(source);
  need(inv.count === 254 && inv.sha256 === proposal.gates.capture_inventory_sha256, 'STALE_CAPTURE');
  oldAudit(proposal, source);
  for (const [rel, replacement] of proposal.changes) {
    const file = at(source, rel);
    need(fs.existsSync(file) && fs.lstatSync(file).isFile(), 'MISSING_SOURCE_FILE');
    need(sha(fs.readFileSync(file)) !== sha(replacement), 'CHANGE_ALREADY_PRESENT');
  }
  const events = fs.readdirSync(at(source, `${slug}/story/recheck-audit`));
  need(events.length === 104 && !events.includes(proposal.event.id), 'EVENT_COUNT_OR_ID_DRIFT');
}
function checkpoint(phase, crashAt) { if (phase === crashAt) throw new SimulatedCrash(phase); }

/** Never retry an incomplete fixture transaction; inspect and reconcile exact bytes first. */
export function inspectFixture(proposal, fixtureRoot) {
  const fixture = safeFixture(fixtureRoot);
  const source = at(fixture, 'source');
  const tx = at(fixture, 'transaction');
  if (!fs.existsSync(tx)) {
    try { assertBefore(proposal, source); return 'READY_SYNTHETIC_HELD'; }
    catch { return 'DRIFT_HOLD'; }
  }
  const eventFile = at(source, `${slug}/story/recheck-audit/${proposal.event.id}/index.json`);
  if (!fs.existsSync(eventFile)) return 'PARTIAL_HOLD_MANUAL_RECOVERY_REQUIRED';
  if (!fs.readFileSync(eventFile).equals(json(proposal.event))) return 'EVENT_DRIFT_HOLD';
  try {
    oldAudit(proposal, source);
    for (const [rel, replacement] of proposal.changes)
      need(fs.readFileSync(at(source, rel)).equals(replacement), 'AFTER_SOURCE_DRIFT');
    need(fs.readdirSync(at(source, `${slug}/story/recheck-audit`)).length === 105,
      'EVENT_COUNT_DRIFT');
    return 'SYNTHETIC_COMMITTED_HELD';
  } catch { return 'AFTER_READBACK_DRIFT_HOLD'; }
}

/** A temporary-file rehearsal only; it cannot create a production receipt. */
export function applyFixture(proposal, fixtureRoot, evidence, { crashAt = null, prewriteEvidence = evidence } = {}) {
  const fixture = safeFixture(fixtureRoot);
  need(proposal.gates.installation_allowed === false && proposal.gates.production_status === 'HOLD'
    && proposal.event.result_kind === 'OFFLINE_PROPOSAL_ONLY_DO_NOT_INSTALL', 'PROPOSAL_STATUS_DRIFT');
  const source = at(fixture, 'source');
  need(fs.lstatSync(source).isDirectory() && !fs.lstatSync(source).isSymbolicLink(), 'SOURCE_DIR_UNSAFE');
  assertBefore(proposal, source);
  const stopSha = safety(proposal, fixture, evidence);
  const tx = at(fixture, 'transaction');
  need(!fs.existsSync(tx), 'PENDING_TRANSACTION_REQUIRES_RECOVERY');
  fs.mkdirSync(tx);
  fs.writeFileSync(at(tx, 'intent.json'), json({ schema_version: 1, slug,
    before_source_sha256: proposal.event.before_source_sha256,
    after_source_sha256: proposal.event.after_source_sha256,
    r16_manifest_sha256: proposal.gates.editorial_manifest_sha256,
    stop_sha256: stopSha, status: 'SYNTHETIC_HOLD' }), { flag: 'wx' });
  checkpoint('intent', crashAt);
  for (const [rel] of proposal.changes) {
    const backup = at(tx, `before/${rel}`);
    fs.mkdirSync(path.dirname(backup), { recursive: true });
    fs.writeFileSync(backup, fs.readFileSync(at(source, rel)), { flag: 'wx' });
  }
  checkpoint('backup', crashAt);
  need(safety(proposal, fixture, prewriteEvidence) === stopSha,
    'FENCE_DRIFT_BEFORE_WRITE');
  assertBefore(proposal, source);
  for (const [rel, bytes] of proposal.changes) {
    const file = at(source, rel), staging = `${file}.offline-105-tmp`;
    fs.writeFileSync(staging, bytes, { flag: 'wx' });
    fs.renameSync(staging, file);
  }
  checkpoint('sources', crashAt);
  oldAudit(proposal, source);
  const event = at(source, `${slug}/story/recheck-audit/${proposal.event.id}/index.json`);
  fs.mkdirSync(path.dirname(event), { recursive: false });
  fs.writeFileSync(event, json(proposal.event), { flag: 'wx' });
  checkpoint('event', crashAt);
  need(sha(fs.readFileSync(at(fixture, 'STOP'))) === stopSha, 'STOP_CHANGED_AFTER_WRITE');
  need(inspectFixture(proposal, fixture) === 'SYNTHETIC_COMMITTED_HELD', 'SYNTHETIC_READBACK_FAILED');
  return { status: 'SYNTHETIC_COMMITTED_HELD', production_status: 'HOLD', paid_calls: 0 };
}
