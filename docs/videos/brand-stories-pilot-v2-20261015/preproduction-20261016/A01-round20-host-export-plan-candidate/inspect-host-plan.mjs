#!/usr/bin/env node
// Read-only bridge from a separately pinned A01 80 -> 81 export to the 82nd
// round20 chapter proposal. No host connection, installer, retry or paid call.
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { inspectTransitionExport } from '../A01-host-transition-export-candidate/inspect-transition-export.mjs';
import { planOfflineRevision, prepareOfflineRevision } from '../A01-round20-existing-revision-offline-candidate/revision-fixture.mjs';

const HASH = /^[a-f0-9]{64}$/u;
const FIXED = Object.freeze({ production_status: 'HOLD', installation_allowed: false,
  paid_work_allowed: false, host_origin_verified: false, inventory_completeness_verified: false,
  freshness_verified: false, exclusive_writer_window_verified: false,
  owner_approval_verified: false });
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');

class GateError extends Error {
  constructor(code) { super(code); this.code = code; }
}
const need = (condition, code) => { if (!condition) throw new GateError(code); };

function localFile(file) {
  need(typeof file === 'string' && path.isAbsolute(file)
    && !file.startsWith('\\\\') && !file.startsWith('//'), 'ABSOLUTE_LOCAL_FILE_REQUIRED');
  const stat = fs.lstatSync(file);
  need(stat.isFile() && !stat.isSymbolicLink() && stat.size <= 1_048_576,
    'UNSAFE_LOCAL_FILE');
  return fs.readFileSync(file);
}

function localJson(file) {
  try { return JSON.parse(localFile(file).toString('utf8').replace(/^\uFEFF/u, '')); }
  catch (error) {
    if (error instanceof GateError) throw error;
    throw new GateError('INVALID_LOCAL_JSON');
  }
}

function same(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

/** Pure comparison used by the second read; callers cannot mutate the capture through it. */
export function sameTransitionReadback(before, after) {
  return after?.result === before?.result && same(after, before);
}

// This examines only the caller's supplied JSON. A quiet projection is not a
// lock, does not prove complete enumeration, and cannot authorize an append.
export function suppliedStateQuiet(state) {
  const f = state?.filesystem, d = state?.db;
  if (!f || !d || !d.project || !d.budget) return false;
  return f.global_stop?.present === true && f.scoped_stop?.present === true
    && f.lease?.present === false && f.unresolved_journals === 0
    && Array.isArray(f.run_receipts) && Array.isArray(f.media_assets)
    && f.media_assets.length === 0
    && d.project.stage === 'blocked'
    && d.project.retry_request_id === d.project.retry_acknowledged_id
    && Array.isArray(d.stage_jobs)
    && d.stage_jobs.every((row) => ['succeeded', 'failed'].includes(row.status))
    && Array.isArray(d.media_jobs)
    && d.media_jobs.every((row) => ['ready', 'failed', 'expired'].includes(row.status))
    && d.budget.reserved_usd !== undefined && /^0(?:\.0+)?$/u.test(d.budget.reserved_usd)
    && d.budget.total_over_limit === false
    && Array.isArray(d.budget.operations)
    && d.budget.operations.every((row) => ['settled', 'released'].includes(row.status));
}

function pinAgreement(plan, pins81, transition) {
  const keys = ['links', 'install_receipt_sha256', 'tip_index_sha256',
    'source_composite_sha256', 'archive_index_manifest_sha256'];
  need(keys.every((key) => plan.previous_81_pins[key] === pins81[key]),
    'PLAN_81_PIN_MISMATCH');
  need(plan.previous_81_pins.source_composite_sha256 === transition.source_composite_sha256
    && plan.previous_81_pins.tip_index_sha256 === transition.tip_index_sha256
    && plan.previous_81_pins.archive_index_manifest_sha256 === transition.audit_manifest_sha256,
  'TRANSITION_PLAN_MISMATCH');
}

/** Bind local export, budget/state projection, and the exact round20 plan. Never writes. */
export function inspectHostPlan(options = {}) {
  const report = { schema_version: 1, kind: 'a01_round20_read_only_host_export_plan',
    slug: 'story-rolling-suitcase-v2', result: 'REJECTED', ...FIXED,
    synthetic_fixture: options.syntheticFixture === true,
    supplied_state_quiet: false, transition_result: null,
    plan_sha256: null, previous_81_tip_sha256: null,
    proposed_82_source_sha256: null, expected_82_pins: null,
    state_file_sha256: null, review_file_sha256: null, receipt_file_sha256: null,
    errors: [] };
  try {
    const args = { beforeRoot: options.before80Root, afterRoot: options.before81Root,
      oldLexiconFile: options.oldLexiconFile, beforePinsFile: options.beforePinsFile,
      afterPinsFile: options.afterPinsFile, stateFile: options.stateFile,
      syntheticFixture: options.syntheticFixture === true,
      expectedOldSha: options.expectedOldSha, expectedNewSha: options.expectedNewSha };
    const before = inspectTransitionExport(args);
    report.transition_result = before.result;
    need(before.result === 'LOCAL_TRANSITION_EXPORT_BINDING_ONLY',
      before.errors?.[0]?.code ?? 'TRANSITION_EXPORT_REJECTED');
    const pins80 = localJson(options.beforePinsFile);
    const pins81 = localJson(options.afterPinsFile);
    const stateBytes = localFile(options.stateFile);
    const state = JSON.parse(stateBytes.toString('utf8').replace(/^\uFEFF/u, ''));
    report.state_file_sha256 = sha(stateBytes);
    need(HASH.test(pins81.state_sha256 ?? '')
      && pins81.state_sha256 === report.state_file_sha256, 'STATE_PIN_MISMATCH');
    report.supplied_state_quiet = suppliedStateQuiet(state);
    need(report.supplied_state_quiet, 'SUPPLIED_STATE_NOT_QUIET');
    const revisionOptions = { before80Root: options.before80Root,
      before81Root: options.before81Root, oldLexiconFile: options.oldLexiconFile,
      pins80, ...(options.syntheticFixture === true ? {
        expectedOldSha: options.expectedOldSha, expectedNewSha: options.expectedNewSha,
      } : {}) };
    const planned = planOfflineRevision(revisionOptions);
    pinAgreement(planned.plan, pins81, before);
    report.plan_sha256 = planned.plan_sha256;
    report.previous_81_tip_sha256 = planned.plan.previous_81_pins.tip_index_sha256;
    report.proposed_82_source_sha256 = planned.plan.after_source_composite_sha256;
    const hasReview = options.reviewFile !== undefined;
    const hasReceipt = options.receiptFile !== undefined;
    need(hasReview === hasReceipt, 'REVIEW_AND_RECEIPT_MUST_PAIR');
    if (hasReview) {
      const reviewBytes = localFile(options.reviewFile);
      const receiptBytes = localFile(options.receiptFile);
      const prepared = prepareOfflineRevision({ ...revisionOptions, reviewBytes, receiptBytes });
      need(prepared.plan_sha256 === planned.plan_sha256, 'REVIEW_PREPARATION_PLAN_DRIFT');
      report.review_file_sha256 = sha(reviewBytes);
      report.receipt_file_sha256 = sha(receiptBytes);
      report.expected_82_pins = prepared.expected_pins;
    }
    // Re-run the complete 80 -> 81 gate after building the 82 plan. This can
    // catch intervening local edits, but never substitutes for a shared lock.
    const after = inspectTransitionExport(args);
    need(sameTransitionReadback(before, after), 'EXPORT_DRIFT_DURING_PLAN');
    report.result = hasReview ? 'LOCAL_82_BYTES_PREPARED_OFFLINE'
      : 'LOCAL_82_PLAN_BOUND_TO_SUPPLIED_EXPORT';
  } catch (error) {
    report.errors.push({ code: typeof error?.code === 'string'
      ? error.code : 'LOCAL_SNAPSHOT_READ_ERROR' });
  }
  return report;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const args = process.argv.slice(2);
  const names = ['--before80', '--before81', '--old-lexicon', '--before-pins',
    '--after-pins', '--state'];
  const valid = (args.length === 12 || args.length === 16)
    && names.every((name, index) => args[index * 2] === name)
    && (args.length === 12 || (args[12] === '--review' && args[14] === '--receipt'));
  const opts = valid ? { before80Root: args[1], before81Root: args[3],
    oldLexiconFile: args[5], beforePinsFile: args[7], afterPinsFile: args[9],
    stateFile: args[11], ...(args.length === 16 ? {
      reviewFile: args[13], receiptFile: args[15],
    } : {}) } : {};
  const report = inspectHostPlan(opts);
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  process.exitCode = report.result.startsWith('LOCAL_82_') ? 0 : 1;
}
