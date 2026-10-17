import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import { inspectHostPlan, sameTransitionReadback, suppliedStateQuiet } from './inspect-host-plan.mjs';
import { inspectCaptureSummary } from './capture-gate.mjs';
import { prepareOfflineRevision, verify82Fixture } from './revision-plan.mjs';
import { hostFixture } from './synthetic-fixture.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));

function state() {
  return { filesystem: { global_stop: { present: true },
    scoped_stop: { present: true }, lease: { present: false },
    unresolved_journals: 0, run_receipts: [{ path: 'resolved.json' }], media_assets: [] },
  db: { project: { stage: 'blocked', retry_request_id: null,
    retry_acknowledged_id: null },
  stage_jobs: [{ status: 'succeeded' }], media_jobs: [],
  budget: { reserved_usd: '0.000000', total_over_limit: false,
    operations: [{ status: 'settled' }] } } };
}

test('supplied quiet projection rejects active, uncertain and changed control state', () => {
  const original = state();
  assert.equal(suppliedStateQuiet(original), true);
  for (const mutate of [
    (value) => { value.filesystem.scoped_stop.present = false; },
    (value) => { value.filesystem.lease.present = true; },
    (value) => { value.filesystem.unresolved_journals = 1; },
    (value) => { value.db.project.retry_request_id = 'pending'; },
    (value) => { value.db.stage_jobs[0].status = 'running'; },
    (value) => { value.db.stage_jobs[0].status = 'uncertain'; },
    (value) => { value.db.media_jobs.push({ status: 'submitted' }); },
    (value) => { value.db.budget.operations[0].status = 'uncertain'; },
    (value) => { value.db.budget.reserved_usd = '0.010000'; },
    (value) => { value.filesystem.media_assets.push({ path: 'old.mp4' }); },
  ]) {
    const changed = structuredClone(original);
    mutate(changed);
    assert.equal(suppliedStateQuiet(changed), false);
  }
});

test('missing export refuses and does not create a destination', (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'a01-host-plan-refusal-'));
  t.after(() => {
    const resolved = fs.realpathSync(root);
    assert.equal(path.dirname(resolved), fs.realpathSync(os.tmpdir()));
    assert.ok(path.basename(resolved).startsWith('a01-host-plan-refusal-'));
    fs.rmSync(resolved, { recursive: true, force: true });
  });
  const destination = path.join(root, 'proposed-82');
  const report = inspectHostPlan({ before80Root: path.join(root, 'missing-80'),
    before81Root: path.join(root, 'missing-81'),
    oldLexiconFile: path.join(root, 'missing-lexicon'),
    beforePinsFile: path.join(root, 'missing-before-pins'),
    afterPinsFile: path.join(root, 'missing-after-pins'),
    stateFile: path.join(root, 'missing-state'), destination });
  assert.equal(report.result, 'REJECTED');
  assert.equal(report.production_status, 'HOLD');
  assert.equal(report.installation_allowed, false);
  assert.equal(report.exclusive_writer_window_verified, false);
  assert.equal(fs.existsSync(destination), false);
});

test('CLI rejects an apply flag with no write path', () => {
  const script = path.join(here, 'inspect-host-plan.mjs');
  assert.throws(() => execFileSync(process.execPath, [script, '--apply'],
    { encoding: 'utf8', stdio: 'pipe' }), (error) => {
    assert.equal(error.status, 1);
    const report = JSON.parse(error.stdout);
    assert.equal(report.result, 'REJECTED');
    assert.equal(report.installation_allowed, false);
    return true;
  });
});

test('synthetic e640 80→81→82 binds round20 and preserves every older audit link', (t) => {
  const f = hostFixture(t);
  assert.equal(f.prepared81.candidate.plan.candidate_id,
    'a01-lexicon-rebaseline-e6403c824aac13b4-20261017');
  assert.equal(Object.keys(f.prepared81.candidate.plan.delta.additions).length, 23);
  assert.equal(f.prepared81.candidate.plan.delta.old_term_count, 2);
  assert.equal(f.prepared81.candidate.plan.delta.new_term_count, 25);
  assert.equal(f.prepared81.production_status, 'HOLD');
  const planned = inspectHostPlan(f.inspectionOptions);
  assert.equal(planned.result, 'LOCAL_82_PLAN_BOUND_TO_SUPPLIED_EXPORT',
    JSON.stringify(planned.errors));
  assert.equal(planned.synthetic_fixture, true);
  assert.equal(planned.transition_result, 'LOCAL_TRANSITION_EXPORT_BINDING_ONLY');
  assert.equal(planned.supplied_state_quiet, true);
  assert.equal(planned.plan_sha256, f.proposal82.plan_sha256);
  assert.equal(planned.previous_81_tip_sha256, f.prepared81.expected_pins.tip_index_sha256);
  assert.equal(planned.proposed_82_source_sha256,
    f.proposal82.plan.after_source_composite_sha256);
  assert.equal(planned.expected_82_pins, null);
  assert.equal(planned.installation_allowed, false);
  const prepared = inspectHostPlan({ ...f.inspectionOptions,
    reviewFile: f.reviewFile, receiptFile: f.receiptFile });
  assert.equal(prepared.result, 'LOCAL_82_BYTES_PREPARED_OFFLINE',
    JSON.stringify(prepared.errors));
  assert.equal(prepared.synthetic_fixture, true);
  assert.deepEqual(prepared.expected_82_pins, f.options.approvedPins82);
  assert.equal(prepared.production_status, 'HOLD');
  assert.equal(prepared.exclusive_writer_window_verified, false);
  assert.equal(f.prepared81.expected_pins.links, 81);
  assert.equal(f.proposal82.plan.previous_81_pins.tip_index_sha256,
    f.prepared81.expected_pins.tip_index_sha256);
  const prepared82 = prepareOfflineRevision(f.options);
  const after82Root = path.join(f.parent, 'immutable-82');
  fs.cpSync(f.before81Root, after82Root, { recursive: true });
  for (const [rel, value] of Object.entries({ ...prepared82.replacements,
    ...prepared82.files })) f.write(after82Root, rel, value);
  const verified = verify82Fixture({ ...f.options, after82Root });
  assert.equal(verified.integrity, 'LOCAL_82_EVENT_TRANSITION_PASS');
  assert.equal(verified.new_pins.links, 82);
  assert.equal(verified.production_status, 'HOLD');
  assert.equal(verified.installation_allowed, false);
  assert.equal(verified.paid_work_allowed, false);
  for (const id of f.proposal82.plan.historical_event_ids) {
    const rel = `story-rolling-suitcase-v2/story/recheck-audit/${id}/index.json`;
    assert.equal(f.hash(f.before81Root, rel), f.hash(after82Root, rel));
  }
  assert.equal(f.hash(f.before80Root,
    'story-rolling-suitcase-v2/story/recheck-audit/event-079/index.json'),
  f.hash(after82Root,
    'story-rolling-suitcase-v2/story/recheck-audit/event-079/index.json'));
  f.write(after82Root, 'story-rolling-suitcase-v2/story/recheck-audit/event-040/index.json',
    '{"forged":true}\n');
  assert.throws(() => verify82Fixture({ ...f.options, after82Root }),
    (error) => error.code === 'HISTORICAL_81_BYTES_DRIFT');
  fs.writeFileSync(f.stateFile,
    JSON.stringify({ ...f.state, observed_at: '2026-10-17T00:00:01Z' }) + '\n');
  const stale = inspectHostPlan(f.inspectionOptions);
  assert.equal(stale.result, 'REJECTED');
  assert.equal(stale.synthetic_fixture, true);
  assert.equal(stale.errors[0]?.code, 'STATE_PIN_MISMATCH');
  assert.equal(stale.installation_allowed, false);
});

test('captured 80-link state with absent controls and an uncertain job remains HOLD', () => {
  const report = inspectCaptureSummary({ schema_version: 1,
    kind: 'a01_read_only_capture_summary', production_status: 'HOLD',
    archive: { tar_sha256: 'a'.repeat(64) },
    chain: { links: 80, captured_lexicon_sha256:
      'e6403c824aac13b4c0a1ae737e8a597a8bf60c353e9faf0cc4915c3214114a30',
    result: 'REJECTED' },
    host: { controls_absent_count: 3 },
    readback: { stage_job_status_counts: { uncertain: 1 } } });
  assert.equal(report.result, 'REJECTED');
  assert.equal(report.production_status, 'HOLD');
  assert.deepEqual(report.reasons, [
    'NO_VERIFIED_81_EVENT', 'CAPTURED_CONTROLS_ABSENT',
    'UNCERTAIN_STAGE_JOB', 'AUDIT_SOURCE_NOT_REBASELINED',
  ]);
  assert.equal(report.installation_allowed, false);
});

test('second-pass export comparison rejects any changed field', () => {
  const before = { result: 'LOCAL_TRANSITION_EXPORT_BINDING_ONLY',
    state_file_sha256: 'a'.repeat(64), tip_index_sha256: 'b'.repeat(64), errors: [] };
  assert.equal(sameTransitionReadback(before, structuredClone(before)), true);
  assert.equal(sameTransitionReadback(before, { ...before,
    state_file_sha256: 'c'.repeat(64) }), false);
  assert.equal(sameTransitionReadback(before, { ...before,
    tip_index_sha256: 'd'.repeat(64) }), false);
  assert.equal(sameTransitionReadback(before, { ...before,
    result: 'REJECTED' }), false);
});
