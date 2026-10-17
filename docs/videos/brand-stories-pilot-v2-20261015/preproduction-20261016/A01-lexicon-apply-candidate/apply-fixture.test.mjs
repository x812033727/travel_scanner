import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { inspectSnapshot } from '../A01-host-inspect-candidate/inspect.mjs';
import { prepareProposedEvent, proposeRebaseline } from '../A01-lexicon-rebaseline-candidate/rebaseline.mjs';
import { applyOfflineFixture, inspect81Fixture, SimulatedFixtureCrash } from './apply-fixture.mjs';

const SLUG = 'story-rolling-suitcase-v2';
const CHAPTERS = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(`${JSON.stringify(value)}\n`);
const codeOf = (run) => {
  try { run(); return null; }
  catch (error) { return error.code ?? error.message; }
};

function fixture(t) {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), 'a01-lexicon-apply-'));
  t.after(() => fs.rmSync(parent, { recursive: true, force: true }));
  const beforeRoot = path.join(parent, 'before');
  const liveRoot = path.join(parent, 'live');
  fs.mkdirSync(beforeRoot);
  const at = (root, rel) => path.join(root, ...rel.split('/'));
  const write = (root, rel, bytes) => {
    const file = at(root, rel);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
    return file;
  };
  const hash = (root, rel) => sha(fs.readFileSync(at(root, rel)));
  const docs = `docs/videos/${SLUG}`;
  const oldLexicon = json({ schema_version: 1, terms: { OpenAI: 'Open A I', Plath: null } });
  const newLexicon = json({ schema_version: 1, terms: {
    OpenAI: 'Open A I', Plath: null, pull: null, request: null,
  } });
  const oldLexiconFile = write(parent, 'old-lexicon.json', oldLexicon);
  for (const [rel, bytes] of Object.entries({
    [`${docs}/series.json`]: 'series\n', [`${docs}/claims.md`]: 'claims\n',
    [`${docs}/script.md`]: 'script\n', [`${SLUG}/review/narrative.json`]: 'narrative\n',
  })) write(beforeRoot, rel, bytes);
  write(beforeRoot, `${docs}/video.json`, json({ scenes: [{ id: 'v1', lines: [{
    id: 'l1', text: '一段中文旁白。',
  }] }] }));
  write(beforeRoot, 'docs/videos/lexicon.json', newLexicon);
  for (const chapter of CHAPTERS) write(beforeRoot,
    `${SLUG}/story/chapters/${chapter}.json`, json({ scenes: [{
      id: `${chapter}-01`, lines: [{ id: 'l1', text: '一段中文旁白。' }],
    }] }));
  write(beforeRoot, `${SLUG}/auto.json`, 'auto-80\n');
  const source = (n, lexiconHash = sha(oldLexicon)) => ({
    auto: sha(`auto-${n}\n`), video: hash(beforeRoot, `${docs}/video.json`),
    series: hash(beforeRoot, `${docs}/series.json`),
    claims: hash(beforeRoot, `${docs}/claims.md`),
    script: hash(beforeRoot, `${docs}/script.md`), lexicon: lexiconHash,
    narrative: hash(beforeRoot, `${SLUG}/review/narrative.json`), pilot: null, verify: null,
    chapters: Object.fromEntries(CHAPTERS.map((chapter) => [chapter,
      hash(beforeRoot, `${SLUG}/story/chapters/${chapter}.json`)])),
  });
  const installed = {
    'docs/video.json': source(0).video, 'docs/script.md': source(0).script,
    'docs/claims.md': source(0).claims, 'docs/series.json': source(0).series,
    ...Object.fromEntries(CHAPTERS.map((chapter) => [`work/story/chapters/${chapter}.json`,
      source(0).chapters[chapter]])),
    'work/auto.json': source(0).auto,
  };
  const installRel = `${SLUG}/manual-revisions/initial/installation-receipt.json`;
  write(beforeRoot, installRel, json({ schema_version: 1, kind: 'a01-candidate-installation',
    slug: SLUG, installed_sha256: installed }));
  const manifest = [];
  for (let n = 0; n < 80; n++) {
    const id = `event-${String(n).padStart(3, '0')}`;
    const dir = `${SLUG}/story/recheck-audit/${id}`;
    const journal = json({ n, result: 'saved' });
    const journalHash = sha(journal);
    write(beforeRoot, `${dir}/${journalHash}.json`, journal);
    const before = source(n), after = source(n + 1);
    const index = { schema_version: 1, slug: SLUG, result_kind: 'saved',
      install_receipt_sha256: hash(beforeRoot, installRel),
      before_source_sha256: sha(JSON.stringify(before)),
      after_source_sha256: sha(JSON.stringify(after)), before, after,
      journals: [{ name: `${journalHash}.json`, sha256: journalHash }] };
    write(beforeRoot, `${dir}/index.json`, json(index));
    manifest.push({ id, index_sha256: hash(beforeRoot, `${dir}/index.json`) });
  }
  const pins = { id: 'fixture-80', links: 80,
    install_receipt_sha256: hash(beforeRoot, installRel),
    tip_index_sha256: manifest.at(-1).index_sha256,
    source_composite_sha256: sha(JSON.stringify(source(80))),
    archive_index_manifest_sha256: sha(JSON.stringify(manifest)) };
  fs.cpSync(beforeRoot, liveRoot, { recursive: true });
  write(liveRoot, 'A01-LEXICON-APPLY-OFFLINE-FIXTURE.json', json({ schema_version: 1,
    slug: SLUG, offline_fixture: true }));
  write(liveRoot, 'STOP', 'fixture global STOP\n');
  write(liveRoot, `${SLUG}/STOP`, 'fixture A01 STOP\n');
  const base = { snapshotRoot: beforeRoot, oldLexiconFile, pins,
    expectedOldSha: sha(oldLexicon), expectedNewSha: sha(newLexicon) };
  const { plan, plan_sha256: planSha } = proposeRebaseline(base);
  const reviewBytes = json({ schema_version: 1,
    kind: 'a01_lexicon_rebaseline_independent_review', slug: SLUG,
    verdict: 'PASS', independent: true, reviewer: 'synthetic-independent-editor',
    plan_sha256: planSha, old_lexicon_sha256: plan.old_lexicon_sha256,
    new_lexicon_sha256: plan.new_lexicon_sha256,
    before_source_sha256: plan.old_pinset.source_composite_sha256,
    after_source_sha256: plan.after_source_composite_sha256, delta: plan.delta });
  const receiptBytes = json({ schema_version: 1,
    kind: 'a01_lexicon_rebaseline_record_receipt', slug: SLUG,
    plan_sha256: planSha, event_id: plan.event_id, revision: plan.revision,
    old_lexicon_sha256: plan.old_lexicon_sha256,
    new_lexicon_sha256: plan.new_lexicon_sha256,
    before_source_sha256: plan.old_pinset.source_composite_sha256,
    after_source_sha256: plan.after_source_composite_sha256,
    review_sha256: sha(reviewBytes), record_only: true, lexicon_file_writes: 0,
    operator: 'synthetic-operator', owner_approval_ref: 'synthetic-only' });
  const prepared = prepareProposedEvent({ ...base, reviewBytes, receiptBytes });
  const now = Date.now();
  const expectedWorkerCommit = 'a'.repeat(40);
  const expectedPanelRulesSha = 'b'.repeat(64);
  const safety = { schema_version: 1, kind: 'a01_lexicon_apply_fixture_safety',
    slug: SLUG, observed_at_ms: now, plan_sha256: planSha,
    worker_commit: expectedWorkerCommit, panel_rules_sha256: expectedPanelRulesSha,
    checkout_clean: true, worker_alive: true,
    project_status: 'blocked', retry_id: null,
    stage_running: 0, stage_queued: 0, media_running: 0, media_queued: 0,
    paid_calls_in_flight: 0, unarchived_run_journals: 0,
    unresolved_run_receipts: 0, media_asset_files: 0,
    budget_limit_usd: '25.00', budget_reserved_usd: '0.00',
    budget_settled_usd: '0.00', budget_operations: 0,
    global_stop_present: true, a01_stop_present: true, a01_lease_present: false };
  const options = { beforeRoot, liveRoot, oldLexiconFile, pins,
    expectedOldSha: base.expectedOldSha, expectedNewSha: base.expectedNewSha,
    reviewBytes, receiptBytes, approvedPins: prepared.expected_pins,
    expectedPlanSha: planSha, expectedReviewSha: sha(reviewBytes),
    expectedReceiptSha: sha(receiptBytes), expectedWorkerCommit,
    expectedPanelRulesSha, safety, now };
  const receiptRel = `${SLUG}/manual-revisions/${plan.event_id}`;
  const auditRel = `${SLUG}/story/recheck-audit/${plan.event_id}`;
  return { parent, beforeRoot, liveRoot, oldLexiconFile, pins, options,
    plan, prepared, at, write, hash, receiptRel, auditRel };
}

test('exact fixture append preserves 80 links, verifies the 81st, and retries idempotently', (t) => {
  const f = fixture(t);
  const prior = f.hash(f.liveRoot, `${SLUG}/story/recheck-audit/event-040/index.json`);
  const first = applyOfflineFixture(f.options);
  assert.equal(first.status, 'LOCAL_FIXTURE_APPENDED');
  assert.equal(first.inspection.new_pins.links, 81);
  assert.equal(first.installation_allowed, false);
  assert.equal(f.hash(f.liveRoot, `${SLUG}/story/recheck-audit/event-040/index.json`), prior);
  assert.deepEqual(fs.readdirSync(f.at(f.liveRoot, `${SLUG}/story/recheck-audit`)).length, 81);
  assert.equal(inspectSnapshot({ snapshotRoot: f.liveRoot, pins: f.pins }).errors[0].code,
    'LINK_COUNT_MISMATCH');
  const second = applyOfflineFixture(f.options);
  assert.equal(second.status, 'ALREADY_APPLIED_LOCAL_FIXTURE');
  assert.equal(fs.readdirSync(f.at(f.liveRoot, `${SLUG}/story/recheck-audit`)).length, 81);
});

test('missing STOP, present LEASE, stale or busy safety, and budget activity all hold before write', (t) => {
  for (const mutate of [
    (f) => fs.unlinkSync(f.at(f.liveRoot, `${SLUG}/STOP`)),
    (f) => f.write(f.liveRoot, `${SLUG}/LEASE`, 'active\n'),
    (f) => { f.options.safety.observed_at_ms -= 61000; },
    (f) => { f.options.safety.stage_running = 1; },
    (f) => { f.options.safety.budget_operations = 1; },
  ]) {
    const f = fixture(t);
    mutate(f);
    assert.notEqual(codeOf(() => applyOfflineFixture(f.options)), null);
    assert.equal(fs.existsSync(f.at(f.liveRoot, f.auditRel)), false);
    assert.equal(fs.existsSync(f.at(f.liveRoot, f.receiptRel)), false);
  }
});

test('review, receipt, 81 pins, current source and old history require exact bytes', (t) => {
  for (const mutate of [
    (f) => { f.options.reviewBytes = json({ fake: true }); },
    (f) => { f.options.receiptBytes = json({ fake: true }); },
    (f) => { f.options.approvedPins = { ...f.options.approvedPins, links: 82 }; },
    (f) => f.write(f.liveRoot, `docs/videos/${SLUG}/script.md`, 'drift\n'),
    (f) => f.write(f.liveRoot, `${SLUG}/story/recheck-audit/event-040/index.json`, '{}\n'),
  ]) {
    const f = fixture(t);
    mutate(f);
    assert.notEqual(codeOf(() => applyOfflineFixture(f.options)), null);
    assert.equal(fs.existsSync(f.at(f.liveRoot, f.auditRel)), false);
  }
});

test('fault after receipt publication rolls back exact new paths and holds retry', (t) => {
  const f = fixture(t);
  const result = codeOf(() => applyOfflineFixture({ ...f.options,
    fault: (step) => { if (step === 'after-receipt-publish') throw new Error('injected'); },
  }));
  assert.equal(result, 'injected');
  assert.equal(fs.existsSync(f.at(f.liveRoot, f.receiptRel)), false);
  assert.equal(fs.existsSync(f.at(f.liveRoot, f.auditRel)), false);
  assert.equal(fs.readdirSync(f.at(f.liveRoot, `${SLUG}/story/recheck-audit`)).length, 80);
  assert.equal(codeOf(() => applyOfflineFixture(f.options)),
    'PENDING_TRANSACTION_REQUIRES_MANUAL_RECOVERY');
});

test('fault after both renames rolls back both exact paths and retains transaction evidence', (t) => {
  const f = fixture(t);
  assert.equal(codeOf(() => applyOfflineFixture({ ...f.options,
    fault: (step) => { if (step === 'after-audit-publish') throw new Error('injected'); },
  })), 'injected');
  assert.equal(fs.existsSync(f.at(f.liveRoot, f.receiptRel)), false);
  assert.equal(fs.existsSync(f.at(f.liveRoot, f.auditRel)), false);
  assert.equal(fs.readdirSync(f.at(f.liveRoot, `${SLUG}/story/recheck-audit`)).length, 80);
});

test('precommit STOP or safety drift never publishes either final directory', (t) => {
  for (const drift of [
    (f) => f.write(f.liveRoot, `${SLUG}/STOP`, 'changed by another actor\n'),
    (f) => { f.options.safety.observed_at_ms += 1; },
  ]) {
    const f = fixture(t);
    assert.notEqual(codeOf(() => applyOfflineFixture({ ...f.options,
      fault: (step) => { if (step === 'after-stage') drift(f); },
    })), null);
    assert.equal(fs.existsSync(f.at(f.liveRoot, f.receiptRel)), false);
    assert.equal(fs.existsSync(f.at(f.liveRoot, f.auditRel)), false);
  }
});

test('simulated crash after receipt leaves partial HOLD and cannot double append', (t) => {
  const f = fixture(t);
  assert.equal(codeOf(() => applyOfflineFixture({ ...f.options,
    fault: (step) => { if (step === 'after-receipt-publish') throw new SimulatedFixtureCrash('crash'); },
  })), 'crash');
  assert.equal(fs.existsSync(f.at(f.liveRoot, f.receiptRel)), true);
  assert.equal(fs.existsSync(f.at(f.liveRoot, f.auditRel)), false);
  assert.equal(codeOf(() => applyOfflineFixture(f.options)),
    'PARTIAL_EVENT_REQUIRES_MANUAL_RECOVERY');
  assert.equal(fs.readdirSync(f.at(f.liveRoot, `${SLUG}/story/recheck-audit`)).length, 80);
});

test('simulated crash after audit may only be read back as the exact same 81st event', (t) => {
  const f = fixture(t);
  assert.equal(codeOf(() => applyOfflineFixture({ ...f.options,
    fault: (step) => { if (step === 'after-audit-publish') throw new SimulatedFixtureCrash('crash'); },
  })), 'crash');
  assert.equal(applyOfflineFixture(f.options).status, 'ALREADY_APPLIED_LOCAL_FIXTURE');
  assert.equal(fs.readdirSync(f.at(f.liveRoot, `${SLUG}/story/recheck-audit`)).length, 81);
  f.write(f.liveRoot, `${f.auditRel}/index.json`, '{}\n');
  assert.notEqual(codeOf(() => inspect81Fixture({ beforeRoot: f.beforeRoot, afterRoot: f.liveRoot,
    oldLexiconFile: f.oldLexiconFile, approvedPins: f.prepared.expected_pins,
    pins: f.pins, expectedOldSha: f.options.expectedOldSha,
    expectedNewSha: f.options.expectedNewSha })), null);
});

test('concurrent alteration of published receipt prevents destructive rollback', (t) => {
  const f = fixture(t);
  const result = codeOf(() => applyOfflineFixture({ ...f.options,
    fault: (step) => {
      if (step === 'after-receipt-publish') {
        f.write(f.liveRoot, `${f.receiptRel}/installation-receipt.json`, 'external edit\n');
        throw new Error('injected');
      }
    },
  }));
  assert.match(result, /MANUAL_RECOVERY_REQUIRED/u);
  assert.equal(fs.readFileSync(f.at(f.liveRoot,
    `${f.receiptRel}/installation-receipt.json`), 'utf8'), 'external edit\n');
});
