import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import { inspectHostPlan, sameTransitionReadback, suppliedStateQuiet } from './inspect-host-plan.mjs';
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

test('complete synthetic 80→81 export binds round20 plan and reviewed 82nd pins', (t) => {
  const f = hostFixture(t);
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
});

test('a changed local export refuses before planning; second-pass comparison is strict', (t) => {
  const f = hostFixture(t);
  fs.writeFileSync(f.stateFile,
    JSON.stringify({ ...f.state, observed_at: '2026-10-17T00:00:01Z' }) + '\n');
  const result = inspectHostPlan(f.inspectionOptions);
  assert.equal(result.result, 'REJECTED');
  assert.equal(result.synthetic_fixture, true);
  assert.equal(result.errors[0]?.code, 'STATE_PIN_MISMATCH');
  assert.equal(result.installation_allowed, false);
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
