#!/usr/bin/env node
// Deliberately fixture-only. This module cannot write a production checkout.
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {
  prepareProposedEvent, proposeRebaseline, verifyProposedTransition,
} from '../A01-lexicon-rebaseline-candidate/rebaseline.mjs';

const SLUG = 'story-rolling-suitcase-v2';
const MARKER = 'A01-LEXICON-APPLY-OFFLINE-FIXTURE.json';
const HASH = /^[a-f0-9]{64}$/u;
const GIT_SHA = /^[a-f0-9]{40}$/u;
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const jsonBytes = (value) => Buffer.from(`${JSON.stringify(value)}\n`);
const same = (left, right) => JSON.stringify(left) === JSON.stringify(right);

export class ApplyGateError extends Error {
  constructor(code) { super(code); this.code = code; }
}
/** Test-only way to model a process killed between two durable renames. */
export class SimulatedFixtureCrash extends Error {}
const need = (condition, code) => { if (!condition) throw new ApplyGateError(code); };

function inside(child, parent) {
  const relative = path.relative(parent, child);
  return relative === '' || (relative !== '..' && !relative.startsWith(`..${path.sep}`)
    && !path.isAbsolute(relative));
}

function safeRoot(root, requireMarker = false) {
  need(typeof root === 'string' && path.isAbsolute(root) && !root.startsWith('\\\\')
    && !root.startsWith('//'), 'ABSOLUTE_LOCAL_ROOT_REQUIRED');
  const resolved = path.resolve(root);
  const temporary = fs.realpathSync(os.tmpdir());
  need(fs.existsSync(resolved) && fs.lstatSync(resolved).isDirectory()
    && !fs.lstatSync(resolved).isSymbolicLink(), 'INVALID_LOCAL_ROOT');
  need(fs.realpathSync(resolved) === resolved && inside(resolved, temporary)
    && resolved !== temporary, 'FIXTURE_TEMP_ROOT_REQUIRED');
  if (requireMarker) {
    const marker = readRegular(resolved, MARKER);
    let parsed;
    try { parsed = JSON.parse(marker.toString('utf8')); } catch { throw new ApplyGateError('INVALID_FIXTURE_MARKER'); }
    need(same(parsed, { schema_version: 1, slug: SLUG, offline_fixture: true }), 'INVALID_FIXTURE_MARKER');
  }
  return resolved;
}

function at(root, relative) {
  need(typeof relative === 'string' && relative.length > 0
    && !/[\\:\x00-\x1f]/u.test(relative)
    && relative.split('/').every((part) => part && part !== '.' && part !== '..'), 'INVALID_RELATIVE_PATH');
  const resolved = path.resolve(root, ...relative.split('/'));
  need(inside(resolved, root) && resolved !== root, 'PATH_OUTSIDE_FIXTURE');
  let parent = root;
  for (const component of relative.split('/').slice(0, -1)) {
    parent = path.join(parent, component);
    if (present(parent)) need(fs.lstatSync(parent).isDirectory()
      && !fs.lstatSync(parent).isSymbolicLink(), 'UNSAFE_PARENT_DIRECTORY');
  }
  return resolved;
}

function present(file) {
  try { fs.lstatSync(file); return true; }
  catch (error) { if (error.code === 'ENOENT') return false; throw error; }
}

function readRegular(root, relative) {
  const file = at(root, relative);
  need(present(file), 'MISSING_REQUIRED_FILE');
  const stat = fs.lstatSync(file);
  need(stat.isFile() && !stat.isSymbolicLink(), 'UNSAFE_FILE_TYPE');
  return fs.readFileSync(file);
}

function checkStopsAndLease(liveRoot) {
  readRegular(liveRoot, 'STOP');
  readRegular(liveRoot, `${SLUG}/STOP`);
  need(!present(at(liveRoot, `${SLUG}/LEASE`)), 'A01_LEASE_PRESENT');
}

function checkSafety(safety, plan, expectedWorkerCommit, expectedPanelRulesSha, now) {
  need(safety && safety.schema_version === 1 && safety.kind === 'a01_lexicon_apply_fixture_safety'
    && safety.slug === SLUG && safety.plan_sha256 === sha(Buffer.from(JSON.stringify(plan)))
    && Number.isSafeInteger(safety.observed_at_ms)
    && safety.observed_at_ms <= now + 5000 && now - safety.observed_at_ms <= 60000,
  'SAFETY_EVIDENCE_MISSING_OR_STALE');
  need(GIT_SHA.test(expectedWorkerCommit ?? '') && HASH.test(expectedPanelRulesSha ?? '')
    && safety.worker_commit === expectedWorkerCommit
    && safety.panel_rules_sha256 === expectedPanelRulesSha
    && safety.checkout_clean === true && safety.worker_alive === true,
  'WORKER_OR_RULES_NOT_PINNED');
  need(safety.project_status === 'blocked' && safety.retry_id === null
    && safety.stage_running === 0 && safety.stage_queued === 0
    && safety.media_running === 0 && safety.media_queued === 0
    && safety.paid_calls_in_flight === 0 && safety.unarchived_run_journals === 0
    && safety.unresolved_run_receipts === 0 && safety.media_asset_files === 0,
  'PROJECT_OR_JOB_NOT_QUIESCENT');
  need(safety.budget_limit_usd === '25.00' && safety.budget_reserved_usd === '0.00'
    && safety.budget_settled_usd === '0.00' && safety.budget_operations === 0,
  'BUDGET_NOT_EMPTY_AND_PINNED');
  need(safety.global_stop_present === true && safety.a01_stop_present === true
    && safety.a01_lease_present === false, 'STOP_OR_LEASE_EVIDENCE_INVALID');
}

function checkedProposal(options) {
  const { beforeRoot, liveRoot, oldLexiconFile, reviewBytes, receiptBytes,
    approvedPins, expectedPlanSha, expectedReviewSha, expectedReceiptSha,
    safety, expectedWorkerCommit, expectedPanelRulesSha, now = Date.now(),
    pins, expectedOldSha, expectedNewSha } = options;
  const before = safeRoot(beforeRoot), live = safeRoot(liveRoot, true);
  need(before !== live && !inside(before, live) && !inside(live, before), 'SNAPSHOTS_MUST_BE_SEPARATE');
  checkStopsAndLease(live);
  need(Buffer.isBuffer(reviewBytes) && Buffer.isBuffer(receiptBytes)
    && HASH.test(expectedPlanSha ?? '') && HASH.test(expectedReviewSha ?? '')
    && HASH.test(expectedReceiptSha ?? '')
    && sha(reviewBytes) === expectedReviewSha && sha(receiptBytes) === expectedReceiptSha,
  'EXTERNAL_EVIDENCE_HASH_MISMATCH');
  const base = { oldLexiconFile, pins, expectedOldSha, expectedNewSha };
  const proposal = proposeRebaseline({ ...base, snapshotRoot: before });
  need(proposal.plan_sha256 === expectedPlanSha, 'REVIEWED_PLAN_SHA_MISMATCH');
  const prepared = prepareProposedEvent({ ...base, snapshotRoot: before, reviewBytes, receiptBytes });
  need(same(prepared.expected_pins, approvedPins), 'APPROVED_81_PINS_MISMATCH');
  const liveProposal = proposeRebaseline({ ...base, snapshotRoot: live });
  need(same(liveProposal.plan, proposal.plan) && liveProposal.plan_sha256 === expectedPlanSha,
    'LIVE_SOURCE_OR_HISTORY_DRIFT');
  checkSafety(safety, proposal.plan, expectedWorkerCommit, expectedPanelRulesSha, now);
  return { before, live, prepared, base, planSha: proposal.plan_sha256,
    safetySha: sha(jsonBytes(safety)),
    globalStopSha: sha(readRegular(live, 'STOP')),
    a01StopSha: sha(readRegular(live, `${SLUG}/STOP`)) };
}

/** A separate 80→81 gate. The original 80-link inspector is never edited. */
export function inspect81Fixture({ beforeRoot, afterRoot, oldLexiconFile, approvedPins,
  pins, expectedOldSha, expectedNewSha } = {}) {
  const before = safeRoot(beforeRoot), after = safeRoot(afterRoot, true);
  const report = verifyProposedTransition({ beforeRoot: before, afterRoot: after,
    oldLexiconFile, pins, expectedOldSha, expectedNewSha });
  need(report.new_pins.links === 81 && same(report.new_pins, approvedPins),
    'APPROVED_81_PINS_MISMATCH');
  return { ...report, integrity: 'LOCAL_81_EVENT_INSPECTION_PASS',
    production_status: 'HOLD', installation_allowed: false, paid_work_allowed: false };
}

function syncDir(directory) {
  if (process.platform === 'win32') return; // Windows fixture; Linux host adaptation must fsync directories.
  const fd = fs.openSync(directory, 'r');
  try { fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
}

function mkdirExact(directory) {
  fs.mkdirSync(directory);
  syncDir(path.dirname(directory));
}

function durableFile(file, bytes) {
  const fd = fs.openSync(file, 'wx', 0o600);
  try {
    let offset = 0;
    while (offset < bytes.length) offset += fs.writeSync(fd, bytes, offset, bytes.length - offset);
    fs.fsyncSync(fd);
  } finally { fs.closeSync(fd); }
  need(sha(fs.readFileSync(file)) === sha(bytes), 'STAGED_BYTES_MISMATCH');
  syncDir(path.dirname(file));
}

function stageFiles(dir, files) {
  mkdirExact(dir);
  for (const [name, bytes] of Object.entries(files)) {
    need(/^[A-Za-z0-9._-]+$/u.test(name) && Buffer.isBuffer(bytes), 'INVALID_STAGED_FILE');
    durableFile(path.join(dir, name), bytes);
  }
}

function exactDir(root, relative, files) {
  const dir = at(root, relative);
  need(present(dir) && fs.lstatSync(dir).isDirectory() && !fs.lstatSync(dir).isSymbolicLink(),
    'PUBLISHED_DIRECTORY_MISSING_OR_UNSAFE');
  need(same(fs.readdirSync(dir).sort(), Object.keys(files).sort()), 'PUBLISHED_DIRECTORY_DRIFT');
  for (const [name, bytes] of Object.entries(files)) {
    need(readRegular(root, `${relative}/${name}`).equals(bytes), 'PUBLISHED_FILE_DRIFT');
  }
  return dir;
}

function removeExactDir(root, relative, files) {
  const dir = exactDir(root, relative, files);
  for (const name of Object.keys(files)) fs.unlinkSync(path.join(dir, name));
  fs.rmdirSync(dir);
  syncDir(path.dirname(dir));
}

function parts(prepared) {
  const receiptRel = `${SLUG}/${prepared.candidate.plan.revision}`;
  const auditRel = prepared.event_path;
  return {
    receiptRel, auditRel,
    receiptFiles: { 'installation-receipt.json': prepared.files[`${receiptRel}/installation-receipt.json`] },
    auditFiles: Object.fromEntries(Object.entries(prepared.files)
      .filter(([rel]) => rel.startsWith(`${auditRel}/`))
      .map(([rel, bytes]) => [rel.slice(auditRel.length + 1), bytes])),
  };
}

/** Only writes a marked OS-temp fixture. Production remains HOLD even after success. */
export function applyOfflineFixture(options) {
  const { liveRoot, beforeRoot, oldLexiconFile, approvedPins,
    pins, expectedOldSha, expectedNewSha, fault = () => {} } = options;
  const live = safeRoot(liveRoot, true), before = safeRoot(beforeRoot);
  const eventId = `lexicon-rebaseline-${(expectedNewSha ?? '835e09df378d0c1b').slice(0, 16)}`;
  const receiptRel = `${SLUG}/manual-revisions/${eventId}`;
  const auditRel = `${SLUG}/story/recheck-audit/${eventId}`;
  const receiptExists = present(at(live, receiptRel));
  const auditExists = present(at(live, auditRel));
  if (receiptExists && auditExists) {
    const checked = inspect81Fixture({ beforeRoot: before, afterRoot: live,
      oldLexiconFile, approvedPins, pins, expectedOldSha, expectedNewSha });
    need(sha(readRegular(live, `${auditRel}/independent-review.json`)) === options.expectedReviewSha
      && sha(readRegular(live, `${receiptRel}/installation-receipt.json`)) === options.expectedReceiptSha,
    'EXTERNAL_EVIDENCE_HASH_MISMATCH');
    return { status: 'ALREADY_APPLIED_LOCAL_FIXTURE', inspection: checked,
      installation_allowed: false, paid_work_allowed: false };
  }
  need(!receiptExists && !auditExists, 'PARTIAL_EVENT_REQUIRES_MANUAL_RECOVERY');
  const context = checkedProposal(options);
  const { receiptFiles, auditFiles } = parts(context.prepared);
  const txnBaseRel = `${SLUG}/story/lexicon-rebaseline-transactions`;
  const txnBase = at(live, txnBaseRel);
  if (!present(txnBase)) mkdirExact(txnBase);
  need(fs.lstatSync(txnBase).isDirectory() && !fs.lstatSync(txnBase).isSymbolicLink(),
    'UNSAFE_TRANSACTION_DIRECTORY');
  const transaction = path.join(txnBase, context.prepared.candidate.plan.event_id);
  need(!present(transaction), 'PENDING_TRANSACTION_REQUIRES_MANUAL_RECOVERY');
  mkdirExact(transaction); // O_EXCL directory creation is the fixture transaction lock.
  const intent = {
    schema_version: 1, kind: 'a01_lexicon_apply_offline_fixture_intent', slug: SLUG,
    event_id: context.prepared.candidate.plan.event_id,
    plan_sha256: context.planSha, approved_pins: approvedPins,
    review_sha256: options.expectedReviewSha, receipt_sha256: options.expectedReceiptSha,
    safety_sha256: sha(jsonBytes(options.safety)),
    files_sha256: Object.fromEntries(Object.entries(context.prepared.files)
      .map(([rel, bytes]) => [rel, sha(bytes)])),
  };
  durableFile(path.join(transaction, 'intent.json'), jsonBytes(intent));
  stageFiles(path.join(transaction, 'receipt'), receiptFiles);
  stageFiles(path.join(transaction, 'audit'), auditFiles);
  let publishedReceipt = false, publishedAudit = false;
  try {
    fault('after-stage');
    const fresh = checkedProposal(options);
    need(same(fresh.prepared.expected_pins, approvedPins), 'PRECOMMIT_PIN_DRIFT');
    need(fresh.safetySha === context.safetySha, 'SAFETY_EVIDENCE_DRIFT');
    need(fresh.globalStopSha === context.globalStopSha
      && fresh.a01StopSha === context.a01StopSha, 'STOP_DRIFT');
    fs.renameSync(path.join(transaction, 'receipt'), at(live, receiptRel));
    publishedReceipt = true;
    syncDir(path.dirname(at(live, receiptRel)));
    fault('after-receipt-publish');
    fs.renameSync(path.join(transaction, 'audit'), at(live, auditRel));
    publishedAudit = true;
    syncDir(path.dirname(at(live, auditRel)));
    fault('after-audit-publish');
    const inspection = inspect81Fixture({ beforeRoot: before, afterRoot: live,
      oldLexiconFile, approvedPins, pins, expectedOldSha, expectedNewSha });
    exactDir(live, receiptRel, receiptFiles);
    exactDir(live, auditRel, auditFiles);
    durableFile(path.join(transaction, 'readback.json'), jsonBytes({ status: 'LOCAL_FIXTURE_APPENDED',
      plan_sha256: context.planSha, new_pins: inspection.new_pins,
      installation_allowed: false, paid_work_allowed: false }));
    return { status: 'LOCAL_FIXTURE_APPENDED', inspection,
      installation_allowed: false, paid_work_allowed: false };
  } catch (error) {
    if (error instanceof SimulatedFixtureCrash) throw error;
    let rollbackError = null;
    try {
      if (publishedAudit) removeExactDir(live, auditRel, auditFiles);
      if (publishedReceipt) removeExactDir(live, receiptRel, receiptFiles);
      need(!present(at(live, auditRel)) && !present(at(live, receiptRel)),
        'ROLLBACK_INCOMPLETE');
      const proposal = proposeRebaseline({ ...context.base, snapshotRoot: live });
      need(proposal.plan_sha256 === context.planSha, 'ROLLBACK_SOURCE_OR_HISTORY_DRIFT');
      durableFile(path.join(transaction, 'rollback.json'), jsonBytes({
        status: 'ROLLED_BACK_LOCAL_FIXTURE', reason: error.code ?? error.message,
        installation_allowed: false, paid_work_allowed: false,
      }));
    } catch (failure) { rollbackError = failure; }
    if (rollbackError) throw new AggregateError([error, rollbackError],
      'MANUAL_RECOVERY_REQUIRED: fixture transaction retained');
    throw error;
  }
}
