#!/usr/bin/env node
// OFFLINE ONLY: validates one exact A01 80 -> 81 audit transition and supplied readbacks.
// The readback checks mirror the older 80-link export gate without changing its contract.
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { HISTORICAL_PINS } from '../A01-host-inspect-candidate/inspect.mjs';
import { verifyProposedTransition } from '../A01-lexicon-rebaseline-candidate/rebaseline.mjs';

const SLUG = 'story-rolling-suitcase-v2';
const AUTHORED_SERIES_SHA256 = 'b2cdb40dd5c6b9e7723ae76fd5fb9992ca66fc0baebabc4ae0f5caabdb38502b';
// These are the importer COMPARED fields in apps/api/app/video_automation/stories.py.
const PLAN_FIELDS = ['title', 'premise', 'note', 'target_minutes', 'planned_episodes',
  'episodes_per_day', 'image_model', 'look', 'style_preset', 'hands_off', 'visual_tier', 'compilation'];
const HASH = /^[a-f0-9]{64}$/;
const GIT_SHA = /^[a-f0-9]{40}$/;
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const object = (value) => value && typeof value === 'object' && !Array.isArray(value);
const ownKeys = (value, keys) => object(value) && Object.keys(value).sort().join('|') === [...keys].sort().join('|');

class SnapshotError extends Error {
  constructor(code) { super(code); this.code = code; }
}
const need = (condition, code) => { if (!condition) throw new SnapshotError(code); };
const uuidish = (value) => typeof value === 'string' && /^[a-f0-9-]{36}$/i.test(value);
const decimal = (value, signed = false) => {
  need(typeof value === 'string' && (signed ? /^-?(?:0|[1-9]\d*)(?:\.\d{1,6})?$/ : /^(?:0|[1-9]\d*)(?:\.\d{1,6})?$/).test(value), 'INVALID_BUDGET_AMOUNT');
  const [whole, fractional = ''] = value.split('.');
  const fraction = fractional.padEnd(6, '0');
  return BigInt(whole) * 1_000_000n + BigInt(whole.startsWith('-') ? `-${fraction}` : fraction);
};

function localJson(file) {
  need(typeof file === 'string' && path.isAbsolute(file), 'ABSOLUTE_INPUT_REQUIRED');
  need(!file.startsWith('\\\\') && !file.startsWith('//'), 'UNC_INPUT_UNSUPPORTED');
  const stat = lstatSync(file);
  need(stat.isFile() && !stat.isSymbolicLink() && stat.size <= 1_048_576, 'INVALID_INPUT_FILE');
  const bytes = readFileSync(file);
  return { value: JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/, '')), sha256: sha(bytes) };
}

function checkStop(record) {
  need(ownKeys(record, ['present', 'sha256']), 'INVALID_STOP_RECORD');
  need(typeof record.present === 'boolean', 'INVALID_STOP_RECORD');
  need(record.present ? HASH.test(record.sha256 ?? '') : record.sha256 === null, 'INVALID_STOP_RECORD');
}

function checkInventory(rows, code) {
  need(Array.isArray(rows), code);
  const paths = new Set();
  for (const row of rows) {
    need(ownKeys(row, ['path', 'sha256', 'bytes']), code);
    need(typeof row.path === 'string' && row.path.length > 0 && !/[\\:\x00-\x1f]/u.test(row.path)
      && row.path.split('/').every((part) => part && part !== '.' && part !== '..')
      && HASH.test(row.sha256 ?? '') && Number.isSafeInteger(row.bytes) && row.bytes >= 0
      && !paths.has(row.path), code);
    paths.add(row.path);
  }
}

function checkBudget(budget, mediaJobs) {
  const keys = ['slug', 'limit_usd', 'reserved_usd', 'settled_usd', 'remaining_usd',
    'total_over_limit', 'over_limit_usd', 'uncertain_operations', 'overrun_operations', 'operations'];
  need(ownKeys(budget, keys) && budget.slug === SLUG && Array.isArray(budget.operations), 'INVALID_BUDGET_READBACK');
  need(decimal(budget.limit_usd) === 25_000_000n, 'BUDGET_LIMIT_MISMATCH');
  const ids = new Set();
  const linkedByBudget = new Map();
  let reserved = 0n, settled = 0n, uncertain = 0, overrun = 0;
  for (const row of budget.operations) {
    need(ownKeys(row, ['operation_id', 'status', 'category', 'provider', 'model', 'max_usd', 'actual_usd',
      'attempts', 'receipt_ref', 'release_reason', 'created_at', 'updated_at', 'media_jobs']), 'INVALID_OPERATION');
    need(typeof row.operation_id === 'string' && row.operation_id.length > 0 && !ids.has(row.operation_id)
      && ['reserved', 'uncertain', 'settled', 'released'].includes(row.status)
      && typeof row.category === 'string' && typeof row.provider === 'string' && typeof row.model === 'string'
      && Number.isInteger(row.attempts) && row.attempts >= 1 && Array.isArray(row.media_jobs), 'INVALID_OPERATION');
    ids.add(row.operation_id);
    const maximum = decimal(row.max_usd);
    need(maximum > 0n, 'INVALID_OPERATION');
    const actual = row.actual_usd === null ? null : decimal(row.actual_usd);
    if (row.status === 'reserved' || row.status === 'uncertain') reserved += maximum;
    if (row.status === 'settled') {
      need(actual !== null, 'INVALID_OPERATION');
      settled += actual;
      if (actual > maximum) overrun++;
    }
    if (row.status === 'uncertain') uncertain++;
    const linkedIds = new Set();
    for (const job of row.media_jobs) {
      need(object(job) && uuidish(job.id) && typeof job.status === 'string' && !linkedIds.has(job.id), 'INVALID_LINKED_MEDIA_JOB');
      linkedIds.add(job.id);
      const matching = mediaJobs.find((candidate) => candidate.id === job.id);
      need(matching && matching.operation_id === row.operation_id && matching.status === job.status,
        'MEDIA_OPERATION_LINK_MISMATCH');
      need(!linkedByBudget.has(job.id), 'MEDIA_OPERATION_LINK_MISMATCH');
      linkedByBudget.set(job.id, { operation_id: row.operation_id, status: job.status });
    }
  }
  for (const job of mediaJobs) {
    need(job.operation_id !== null, 'MEDIA_BUDGET_LINK_MISSING');
    const linked = linkedByBudget.get(job.id);
    need(ids.has(job.operation_id) && linked?.operation_id === job.operation_id
      && linked.status === job.status, 'MEDIA_OPERATION_LINK_MISMATCH');
  }
  const remaining = 25_000_000n - reserved - settled;
  need(decimal(budget.reserved_usd) === reserved && decimal(budget.settled_usd) === settled
    && decimal(budget.remaining_usd, true) === remaining
    && decimal(budget.over_limit_usd) === (remaining < 0n ? -remaining : 0n)
    && budget.total_over_limit === (remaining < 0n)
    && budget.uncertain_operations === uncertain && budget.overrun_operations === overrun,
  'BUDGET_TOTAL_MISMATCH');
  return { operation_count: ids.size, uncertain, reserved_usd: budget.reserved_usd,
    settled_usd: budget.settled_usd, remaining_usd: budget.remaining_usd };
}

function checkJobs(rows, type) {
  need(Array.isArray(rows), `INVALID_${type}_JOBS`);
  const ids = new Set();
  for (const row of rows) {
    const fields = type === 'STAGE' ? ['id', 'status', 'request_hash', 'input_hash']
      : ['id', 'status', 'kind', 'operation_id'];
    need(ownKeys(row, fields) && uuidish(row.id) && !ids.has(row.id), `INVALID_${type}_JOBS`);
    ids.add(row.id);
    if (type === 'STAGE') need(['queued', 'running', 'succeeded', 'failed', 'uncertain'].includes(row.status)
      && HASH.test(row.request_hash ?? '') && HASH.test(row.input_hash ?? ''), 'INVALID_STAGE_JOBS');
    else need(['queued', 'submitted', 'ready', 'failed', 'expired'].includes(row.status)
      && ['image', 'clip', 'music'].includes(row.kind)
      && (row.operation_id === null || typeof row.operation_id === 'string'), 'INVALID_MEDIA_JOBS');
  }
}

const PIN_FIELDS = ['id', 'links', 'install_receipt_sha256', 'tip_index_sha256',
  'source_composite_sha256', 'archive_index_manifest_sha256'];
const OLD_PIN_FIELDS = PIN_FIELDS.filter((key) => key !== 'id');
function requireSyntheticFixtureRoots(roots) {
  for (const root of roots) {
    need(typeof root === 'string' && path.isAbsolute(root), 'SYNTHETIC_ROOT_INVALID');
    const relative = path.relative(os.tmpdir(), path.resolve(root));
    need(relative && relative !== '..' && !relative.startsWith(`..${path.sep}`)
      && !path.isAbsolute(relative), 'SYNTHETIC_ROOT_OUTSIDE_TEMP');
    const markerPath = path.join(root, 'A01-HOST-TRANSITION-OFFLINE-FIXTURE.json');
    need(existsSync(markerPath), 'SYNTHETIC_MARKER_MISSING');
    const marker = localJson(markerPath);
    need(ownKeys(marker.value, ['schema_version', 'slug', 'synthetic_fixture'])
      && marker.value.schema_version === 1 && marker.value.slug === SLUG
      && marker.value.synthetic_fixture === true, 'SYNTHETIC_MARKER_INVALID');
  }
}

export function inspectTransitionExport({ beforeRoot, afterRoot, oldLexiconFile,
  beforePinsFile, afterPinsFile, stateFile, expectedOldSha, expectedNewSha,
  syntheticFixture = false } = {}) {
  const report = {
    schema_version: 1, kind: 'a01_offline_80_to_81_export_binding', slug: SLUG,
    result: 'REJECTED', production_status: 'HOLD', installation_allowed: false, paid_work_allowed: false,
    inventory_completeness_verified: false, recency_verified: false, owner_approval_verified: false,
    exclusive_writer_window_verified: false, synthetic_fixture: syntheticFixture,
    source_integrity: 'REJECTED', binding: 'REJECTED', before_pins_file_sha256: null,
    after_pins_file_sha256: null, state_file_sha256: null,
    source_composite_sha256: null, audit_manifest_sha256: null, tip_index_sha256: null,
    old_tip_index_sha256: null, before_history_links: null, after_history_links: null,
    authored_series_sha256: null, state_summary: null, errors: [],
  };
  try {
    if (syntheticFixture) requireSyntheticFixtureRoots([beforeRoot, afterRoot]);
    const beforePins = localJson(beforePinsFile), afterPins = localJson(afterPinsFile);
    const state = localJson(stateFile);
    report.before_pins_file_sha256 = beforePins.sha256;
    report.after_pins_file_sha256 = afterPins.sha256;
    report.state_file_sha256 = state.sha256;
    need(ownKeys(beforePins.value, PIN_FIELDS) && beforePins.value.links === 80
      && OLD_PIN_FIELDS.every((key) => key === 'links' || HASH.test(beforePins.value[key] ?? '')),
    'BEFORE_PINSET_INVALID');
    need(syntheticFixture || OLD_PIN_FIELDS.every((key) => beforePins.value[key] === HISTORICAL_PINS[key]),
      'HISTORICAL_PINS_MISMATCH');
    need(ownKeys(afterPins.value, [...PIN_FIELDS, 'state_sha256']) && afterPins.value.links === 81
      && PIN_FIELDS.filter((key) => key !== 'id' && key !== 'links')
        .every((key) => HASH.test(afterPins.value[key] ?? '')), 'AFTER_PINSET_INVALID');
    need(HASH.test(afterPins.value.state_sha256 ?? '') && afterPins.value.state_sha256 === state.sha256,
      'STATE_PIN_MISMATCH');
    // Overrides exist solely for synthetic tests; the CLI has no such arguments.
    need(syntheticFixture || (expectedOldSha === undefined && expectedNewSha === undefined),
      'LEXICON_HASH_OVERRIDE_FORBIDDEN');
    const transition = verifyProposedTransition({ beforeRoot, afterRoot, oldLexiconFile,
      pins: beforePins.value, ...(expectedOldSha ? { expectedOldSha } : {}),
      ...(expectedNewSha ? { expectedNewSha } : {}) });
    report.source_integrity = transition.integrity;
    need(transition.integrity === 'LOCAL_81_EVENT_TRANSITION_PASS', 'TRANSITION_REJECTED');
    need(PIN_FIELDS.every((key) => afterPins.value[key] === transition.new_pins[key]),
      'AFTER_PINSET_MISMATCH');
    report.old_tip_index_sha256 = beforePins.value.tip_index_sha256;
    report.before_history_links = beforePins.value.links;
    report.after_history_links = transition.new_pins.links;
    const inspected = {
      source: { composite_sha256: transition.new_pins.source_composite_sha256 },
      chain: { archive_index_manifest_sha256: transition.new_pins.archive_index_manifest_sha256,
        tip_index_sha256: transition.new_pins.tip_index_sha256 },
    };
    const s = state.value;
    need(ownKeys(s, ['schema_version', 'slug', 'observed_at', 'release', 'archive', 'filesystem', 'db'])
      && s.schema_version === 1 && s.slug === SLUG
      && typeof s.observed_at === 'string' && /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z$/.test(s.observed_at)
      && Number.isFinite(Date.parse(s.observed_at)), 'INVALID_STATE_SNAPSHOT');
    need(ownKeys(s.release, ['git_sha', 'worker_sha256', 'panel_rules_sha256'])
      && GIT_SHA.test(s.release.git_sha ?? '') && HASH.test(s.release.worker_sha256 ?? '')
      && HASH.test(s.release.panel_rules_sha256 ?? ''), 'INVALID_RELEASE_READBACK');
    need(ownKeys(s.archive, ['source_composite_sha256', 'audit_manifest_sha256', 'tip_index_sha256'])
      && s.archive.source_composite_sha256 === inspected.source.composite_sha256
      && s.archive.audit_manifest_sha256 === inspected.chain.archive_index_manifest_sha256
      && s.archive.tip_index_sha256 === inspected.chain.tip_index_sha256, 'ARCHIVE_STATE_BINDING_MISMATCH');
    const f = s.filesystem;
    need(ownKeys(f, ['global_stop', 'scoped_stop', 'lease', 'unresolved_journals', 'run_receipts', 'media_assets']),
      'INVALID_FILESYSTEM_READBACK');
    checkStop(f.global_stop); checkStop(f.scoped_stop); checkStop(f.lease);
    need(Number.isSafeInteger(f.unresolved_journals) && f.unresolved_journals >= 0,
      'INVALID_FILESYSTEM_READBACK');
    checkInventory(f.run_receipts, 'INVALID_RUN_RECEIPTS');
    checkInventory(f.media_assets, 'INVALID_MEDIA_INVENTORY');
    const d = s.db;
    need(ownKeys(d, ['series', 'episode', 'project', 'budget', 'stage_jobs', 'media_jobs']), 'INVALID_DB_READBACK');
    const authoredBytes = readFileSync(fileURLToPath(new URL('../../series.json', import.meta.url)));
    need(sha(authoredBytes) === AUTHORED_SERIES_SHA256, 'AUTHORED_SERIES_DRIFT');
    const authored = JSON.parse(authoredBytes.toString('utf8'));
    need(authored.slug === 'brand-stories-curio-pilot-v2' && authored.target_minutes === 10
      && authored.hands_off === true && authored.image_model === 'image-01', 'AUTHORED_SERIES_INVALID');
    report.authored_series_sha256 = AUTHORED_SERIES_SHA256;
    need(ownKeys(d.series, ['id', 'slug', 'kind', 'status', ...PLAN_FIELDS])
      && uuidish(d.series.id) && d.series.slug === authored.slug && d.series.kind === authored.kind
      && d.series.status === 'active'
      && PLAN_FIELDS.every((key) => JSON.stringify(d.series[key]) === JSON.stringify(authored[key]))
      && d.series.look?.preset === 'cute-mystery', 'SERIES_PLAN_DRIFT');
    need(ownKeys(d.episode, ['id', 'series_id', 'number', 'slug', 'status'])
      && uuidish(d.episode.id) && d.episode.series_id === d.series.id && d.episode.slug === SLUG
      && d.episode.number === 1 && d.episode.status === 'started', 'INVALID_EPISODE_PLAN');
    need(ownKeys(d.project, ['slug', 'format', 'series_slug', 'episode_number', 'stage',
      'retry_request_id', 'retry_acknowledged_id']) && d.project.slug === SLUG
      && d.project.format === 'drama' && d.project.series_slug === d.series.slug
      && d.project.episode_number === d.episode.number && d.project.stage === 'blocked'
      && (d.project.retry_request_id === null || uuidish(d.project.retry_request_id))
      && (d.project.retry_acknowledged_id === null || uuidish(d.project.retry_acknowledged_id)), 'INVALID_PROJECT_READBACK');
    checkJobs(d.stage_jobs, 'STAGE'); checkJobs(d.media_jobs, 'MEDIA');
    const budget = checkBudget(d.budget, d.media_jobs);
    report.source_composite_sha256 = inspected.source.composite_sha256;
    report.audit_manifest_sha256 = inspected.chain.archive_index_manifest_sha256;
    report.tip_index_sha256 = inspected.chain.tip_index_sha256;
    report.state_summary = {
      observed_at: s.observed_at, release_sha: s.release.git_sha, series_slug: d.series.slug,
      episode_number: d.episode.number, project_stage: d.project.stage,
      retry_pending: d.project.retry_request_id !== d.project.retry_acknowledged_id,
      global_stop_present: f.global_stop.present, scoped_stop_present: f.scoped_stop.present,
      lease_present: f.lease.present, unresolved_journals: f.unresolved_journals,
      run_receipt_count: f.run_receipts.length, media_asset_count: f.media_assets.length,
      stage_job_statuses: d.stage_jobs.reduce((a, row) => ({ ...a, [row.status]: (a[row.status] ?? 0) + 1 }), {}),
      media_job_statuses: d.media_jobs.reduce((a, row) => ({ ...a, [row.status]: (a[row.status] ?? 0) + 1 }), {}),
      budget,
    };
    report.binding = 'LOCAL_READBACK_BINDING_PASS';
    report.result = 'LOCAL_TRANSITION_EXPORT_BINDING_ONLY';
  } catch (error) {
    report.errors.push({ code: typeof error?.code === 'string' ? error.code : 'SNAPSHOT_READ_ERROR' });
  }
  return report;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const args = process.argv.slice(2);
  const valid = args.length === 12 && args[0] === '--before' && args[2] === '--after'
    && args[4] === '--old-lexicon' && args[6] === '--before-pins'
    && args[8] === '--after-pins' && args[10] === '--state';
  const report = inspectTransitionExport({ beforeRoot: valid ? args[1] : undefined,
    afterRoot: valid ? args[3] : undefined, oldLexiconFile: valid ? args[5] : undefined,
    beforePinsFile: valid ? args[7] : undefined, afterPinsFile: valid ? args[9] : undefined,
    stateFile: valid ? args[11] : undefined });
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  process.exitCode = report.result === 'LOCAL_TRANSITION_EXPORT_BINDING_ONLY' ? 0 : 1;
}
