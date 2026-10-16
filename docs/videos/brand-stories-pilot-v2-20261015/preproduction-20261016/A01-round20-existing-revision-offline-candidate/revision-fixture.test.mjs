import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { inspectSnapshot } from '../A01-host-inspect-candidate/inspect.mjs';
import { prepareProposedEvent, proposeRebaseline, verifyProposedTransition } from '../A01-lexicon-rebaseline-candidate/rebaseline.mjs';
import { applyOfflineFixture, OFFLINE_PINS, planOfflineRevision,
  prepareOfflineRevision, SimulatedFixtureCrash, verify82Fixture } from './revision-fixture.mjs';

const SLUG = 'story-rolling-suitcase-v2';
const CHAPTERS = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(`${JSON.stringify(value)}\n`);
const at = (root, rel) => path.join(root, ...rel.split('/'));
const write = (root, rel, value) => {
  const file = at(root, rel);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, value);
  return file;
};
const hash = (root, rel) => sha(fs.readFileSync(at(root, rel)));
const codeOf = (run) => { try { run(); return null; }
  catch (error) { return error.code ?? error.message; } };

// Execute the repository's actual checkChapter body with deterministic, unpaid stubs.
// Its max-round branch is the regression: an old round-2 counter would skip recheck.
async function actualWorkerCheck(entry) {
  const here = path.dirname(fileURLToPath(import.meta.url));
  const workerFile = path.resolve(here, '../../../../../tools/video/automation/story.mjs');
  const source = fs.readFileSync(workerFile, 'utf8');
  const start = source.indexOf('async function checkChapter(');
  const end = source.indexOf('/** A line the listener', start);
  assert.ok(start >= 0 && end > start);
  const chapter = { key: 'hook', title: 'Hook', scenes: [{ id: 'hook-01',
    lines: [{ id: 'line-01', text: 'Example.' }] }], claims: [] };
  const state = { slug: SLUG, story: { chapters: Object.fromEntries(CHAPTERS.map(
    (key) => [key, key === 'hook' ? entry : { checked: false }])) } };
  let askedRound = null;
  const context = {
    seriesInfo: () => ({ plan: { sources: [], chapters: [{ point: 'point' }],
      must_verify: [], names: [] }, title: 'Title' }),
    entryOf: (_state, key) => _state.story.chapters[key],
    CHAPTER_OF: new Map([['hook', { index: 0 }]]),
    readChapter: () => chapter,
    factChapters: () => [], chapterNarration: () => [], anchorsFor: () => [],
    factsPayload: () => [], sourcesPayload: async () => [],
    checkerSourceOrder: () => [], CHECKER_TOKENS: 1, STORY_VARIANT: 'story',
    isObject: (value) => value !== null && typeof value === 'object',
    applyPatch: () => ({ chapter, changed: [], dropped: [], refused: [] }),
    checkedRows: () => Array.from({ length: 4 }, (_, index) => ({
      id: `c${index}`, verdict: 'CHANGED' })),
    COUNTED: new Set(['CHANGED', 'ATTRIBUTED', 'NOT FOUND']),
    saveChapter: () => {}, relint: async () => ({ other: [] }),
    CHANGED_FACTS_RECHECK: 3,
    CHAPTER_KEYS: CHAPTERS,
    VERDICTS: ['CONFIRMED', 'PLAN', 'CHANGED', 'ATTRIBUTED', 'NOT FOUND',
      'OUT OF SCOPE'],
    isText: (value) => typeof value === 'string' && value.length > 0,
  };
  const checkChapter = vm.runInNewContext(`${source.slice(start, end)}\ncheckChapter`,
    context, { filename: workerFile });
  const automation = { ctx: { now: () => new Date('2026-10-17T00:00:00Z') },
    settings: { max_verify_rounds: 3 },
    stage: async (_kind, _slug, payload) => {
      askedRound = payload.round;
      return { claims: [], patch: {}, drop: [], report: 'Four changed facts.' };
    },
    cleared: () => {}, persist: () => {},
    retryLater: () => { throw Error('unexpected retry'); },
  };
  await checkChapter(automation, state, 'hook');
  return { askedRound, checked: entry.checked, changed: entry.changed };
}

function fixture(t) {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), 'a01-round20-82-'));
  t.after(() => fs.rmSync(parent, { recursive: true, force: true }));
  const before80Root = path.join(parent, 'immutable-80');
  const before81Root = path.join(parent, 'immutable-81');
  const liveRoot = path.join(parent, 'fixture-live');
  fs.mkdirSync(before80Root);
  const oldLexicon = json({ schema_version: 1, terms: { OpenAI: 'Open A I', Plath: null } });
  const newLexicon = json({ schema_version: 1, terms: {
    OpenAI: 'Open A I', Plath: null, pull: null, request: null } });
  const oldLexiconFile = write(parent, 'old-lexicon.json', oldLexicon);
  const docs = `docs/videos/${SLUG}`;
  for (const [rel, value] of Object.entries({
    [`${docs}/series.json`]: 'old series\n', [`${docs}/claims.md`]: 'old claims\n',
    [`${docs}/script.md`]: 'old script\n', [`${SLUG}/review/narrative.json`]: json({
      round: 9, passed: false, failed: ['chapters_link', 'payoffs', 'one_thread'] }),
  })) write(before80Root, rel, value);
  write(before80Root, `${docs}/video.json`, json({ scenes: [{ id: 'v1',
    lines: [{ id: 'l1', text: '一段中文旁白。' }] }] }));
  write(before80Root, 'docs/videos/lexicon.json', newLexicon);
  for (const key of CHAPTERS) write(before80Root,
    `${SLUG}/story/chapters/${key}.json`, json({ key, scenes: [{ id: `${key}-01`,
      lines: [{ id: 'l1', text: '一段中文旁白。' }] }], claims: [] }));
  const state = (n) => ({ slug: SLUG, status: 'blocked',
    blocked_kind: 'prompt_fixes:narrative', verified: true, listener_done: true,
    sequence: n, story: { narrative_fixes: 2, owner_note: null,
      narrative: { passed: false, rounds: 9, failed: ['chapters_link', 'payoffs', 'one_thread'] },
      chapters: Object.fromEntries(CHAPTERS.map((key) => [key,
        { written: true, checked: true, listened: true, check_rounds: 2,
          lint_fixes: 2, changed: 4, lint: null }])) } });
  write(before80Root, `${SLUG}/auto.json`, json(state(80)));
  const source = (n, lexiconHash = sha(oldLexicon)) => ({
    auto: sha(json(state(n))), video: hash(before80Root, `${docs}/video.json`),
    series: hash(before80Root, `${docs}/series.json`),
    claims: hash(before80Root, `${docs}/claims.md`),
    script: hash(before80Root, `${docs}/script.md`), lexicon: lexiconHash,
    narrative: hash(before80Root, `${SLUG}/review/narrative.json`),
    pilot: null, verify: null,
    chapters: Object.fromEntries(CHAPTERS.map((key) => [key,
      hash(before80Root, `${SLUG}/story/chapters/${key}.json`)])),
  });
  const installed = { 'docs/video.json': source(0).video,
    'docs/script.md': source(0).script, 'docs/claims.md': source(0).claims,
    'docs/series.json': source(0).series, 'work/auto.json': source(0).auto,
    ...Object.fromEntries(CHAPTERS.map((key) => [`work/story/chapters/${key}.json`,
      source(0).chapters[key]])) };
  const installRel = `${SLUG}/manual-revisions/initial/installation-receipt.json`;
  write(before80Root, installRel, json({ schema_version: 1,
    kind: 'a01-candidate-installation', slug: SLUG, installed_sha256: installed }));
  const manifest80 = [];
  for (let n = 0; n < 80; n++) {
    const id = `event-${String(n).padStart(3, '0')}`;
    const dir = `${SLUG}/story/recheck-audit/${id}`;
    const journal = json({ n, result: 'saved' });
    write(before80Root, `${dir}/${sha(journal)}.json`, journal);
    const before = source(n), after = source(n + 1);
    write(before80Root, `${dir}/index.json`, json({ schema_version: 1,
      slug: SLUG, result_kind: 'saved',
      install_receipt_sha256: hash(before80Root, installRel),
      before_source_sha256: sha(JSON.stringify(before)),
      after_source_sha256: sha(JSON.stringify(after)), before, after,
      journals: [{ name: `${sha(journal)}.json`, sha256: sha(journal) }] }));
    manifest80.push({ id, index_sha256: hash(before80Root, `${dir}/index.json`) });
  }
  const pins80 = { id: 'synthetic-80', links: 80,
    install_receipt_sha256: hash(before80Root, installRel),
    tip_index_sha256: manifest80.at(-1).index_sha256,
    source_composite_sha256: sha(JSON.stringify(source(80))),
    archive_index_manifest_sha256: sha(JSON.stringify(manifest80)) };
  fs.cpSync(before80Root, before81Root, { recursive: true });
  const rebaselineOptions = { snapshotRoot: before80Root, oldLexiconFile,
    pins: pins80, expectedOldSha: sha(oldLexicon), expectedNewSha: sha(newLexicon) };
  const proposed81 = proposeRebaseline(rebaselineOptions);
  const p = proposed81.plan;
  const review81 = json({ schema_version: 1,
    kind: 'a01_lexicon_rebaseline_independent_review', slug: SLUG,
    verdict: 'PASS', independent: true, reviewer: 'synthetic-independent-editor',
    plan_sha256: proposed81.plan_sha256, old_lexicon_sha256: p.old_lexicon_sha256,
    new_lexicon_sha256: p.new_lexicon_sha256,
    before_source_sha256: p.old_pinset.source_composite_sha256,
    after_source_sha256: p.after_source_composite_sha256, delta: p.delta });
  const receipt81 = json({ schema_version: 1,
    kind: 'a01_lexicon_rebaseline_record_receipt', slug: SLUG,
    plan_sha256: proposed81.plan_sha256, event_id: p.event_id, revision: p.revision,
    old_lexicon_sha256: p.old_lexicon_sha256,
    new_lexicon_sha256: p.new_lexicon_sha256,
    before_source_sha256: p.old_pinset.source_composite_sha256,
    after_source_sha256: p.after_source_composite_sha256,
    review_sha256: sha(review81), record_only: true, lexicon_file_writes: 0,
    operator: 'synthetic-operator', owner_approval_ref: 'synthetic-only' });
  const prepared81 = prepareProposedEvent({ ...rebaselineOptions,
    reviewBytes: review81, receiptBytes: receipt81 });
  for (const [rel, value] of Object.entries(prepared81.files)) write(before81Root, rel, value);
  assert.equal(verifyProposedTransition({ ...rebaselineOptions, beforeRoot: before80Root,
    afterRoot: before81Root }).integrity, 'LOCAL_81_EVENT_TRANSITION_PASS');
  fs.cpSync(before81Root, liveRoot, { recursive: true });
  write(liveRoot, 'A01-ROUND20-82-OFFLINE-FIXTURE.json', json({ schema_version: 1,
    slug: SLUG, offline_fixture: true }));
  write(liveRoot, 'STOP', 'synthetic global STOP\n');
  write(liveRoot, `${SLUG}/STOP`, 'synthetic A01 STOP\n');
  const base = { before80Root, before81Root, oldLexiconFile, pins80,
    expectedOldSha: rebaselineOptions.expectedOldSha,
    expectedNewSha: rebaselineOptions.expectedNewSha };
  const proposal82 = planOfflineRevision(base);
  const reviewBytes = json({ schema_version: 1,
    kind: 'a01_round20_existing_story_independent_review', slug: SLUG,
    verdict: 'PASS', independent: true, reviewer: 'synthetic-second-editor',
    plan_sha256: proposal82.plan_sha256,
    round20_manifest_sha256: OFFLINE_PINS.round20_manifest_sha256,
    before_source_sha256: proposal82.plan.previous_81_pins.source_composite_sha256,
    after_source_sha256: proposal82.plan.after_source_composite_sha256 });
  const receiptBytes = json({ schema_version: 1,
    kind: 'a01_round20_existing_story_revision_receipt', slug: SLUG,
    event_id: OFFLINE_PINS.event_id, plan_sha256: proposal82.plan_sha256,
    review_sha256: sha(reviewBytes),
    round20_manifest_sha256: OFFLINE_PINS.round20_manifest_sha256,
    before_source_sha256: proposal82.plan.previous_81_pins.source_composite_sha256,
    after_source_sha256: proposal82.plan.after_source_composite_sha256,
    paid_calls: 0, auto_retry: false, operator: 'synthetic-fixture-operator',
    owner_approval_ref: 'synthetic-only' });
  const options = { ...base, liveRoot, reviewBytes, receiptBytes,
    expectedWorkerCommit: 'a'.repeat(40), expectedPanelRulesSha: 'b'.repeat(64),
    expectedPlanSha: proposal82.plan_sha256, now: Date.now() };
  options.approvedPins82 = prepareOfflineRevision(options).expected_pins;
  options.safety = { schema_version: 1, slug: SLUG,
    plan_sha256: options.expectedPlanSha,
    worker_commit: options.expectedWorkerCommit,
    panel_rules_sha256: options.expectedPanelRulesSha,
    checkout_clean: true, project_status: 'blocked', retry_id: null,
    stage_running: 0, stage_queued: 0, media_running: 0, media_queued: 0,
    paid_calls_in_flight: 0, unarchived_run_journals: 0,
    unresolved_run_receipts: 0, media_asset_files: 0,
    budget_limit_usd: '25.00', budget_reserved_usd: '0.00',
    budget_settled_usd: '0.00', budget_operations: 0,
    global_stop_present: true, a01_stop_present: true,
    a01_lease_present: false, observed_at_ms: options.now };
  return { parent, before80Root, before81Root, liveRoot, options,
    pins80, prepared81, proposal82, at, write, hash };
}

test('81 -> 82 fixture preserves the exact 81 history, pins round20 and restarts real checker', async (t) => {
  const f = fixture(t);
  const oldStateBytes = fs.readFileSync(f.at(f.before81Root, `${SLUG}/auto.json`));
  const oldState = JSON.parse(oldStateBytes);
  for (const key of CHAPTERS) assert.deepEqual(f.proposal82.plan.previous_chapter_counters[key],
    { check_rounds: 2, lint_fixes: 2, changed: 4 });
  const prior40 = f.hash(f.liveRoot, `${SLUG}/story/recheck-audit/event-040/index.json`);
  const prior81 = f.hash(f.liveRoot,
    `${SLUG}/story/recheck-audit/lexicon-rebaseline-${f.options.expectedNewSha.slice(0, 16)}/index.json`);
  const first = applyOfflineFixture(f.options);
  assert.equal(first.status, 'LOCAL_FIXTURE_APPENDED');
  assert.equal(first.inspection.new_pins.links, 82);
  assert.equal(first.installation_allowed, false);
  assert.equal(first.paid_work_allowed, false);
  assert.equal(f.hash(f.liveRoot, `${SLUG}/story/recheck-audit/event-040/index.json`), prior40);
  assert.equal(f.hash(f.liveRoot,
    `${SLUG}/story/recheck-audit/lexicon-rebaseline-${f.options.expectedNewSha.slice(0, 16)}/index.json`), prior81);
  assert.equal(inspectSnapshot({ snapshotRoot: f.liveRoot, pins: f.pins80 }).errors[0].code,
    'LINK_COUNT_MISMATCH');
  const state = JSON.parse(fs.readFileSync(f.at(f.liveRoot, `${SLUG}/auto.json`)));
  assert.equal(state.story.narrative.passed, false);
  assert.equal(state.story.narrative_fixes, 2);
  assert.equal(state.verified, false);
  assert.equal(state.listener_done, false);
  for (const key of CHAPTERS) {
    assert.equal(state.story.chapters[key].checked, false);
    assert.equal(state.story.chapters[key].listened, false);
    assert.equal(state.story.chapters[key].check_rounds, 0);
    assert.equal(state.story.chapters[key].lint_fixes, 0);
    assert.equal(Object.hasOwn(state.story.chapters[key], 'changed'), false);
  }
  const backup = f.at(f.liveRoot, `${SLUG}/story/round20-offline-transactions/`
    + `${OFFLINE_PINS.event_id}/before/${SLUG}/auto.json`);
  assert.deepEqual(fs.readFileSync(backup), oldStateBytes);
  const author = JSON.parse(fs.readFileSync(f.at(f.liveRoot,
    `${OFFLINE_PINS.event_dir}/author-manifest.json`)));
  assert.deepEqual(author.previous_chapter_counters,
    f.proposal82.plan.previous_chapter_counters);
  assert.deepEqual(await actualWorkerCheck(structuredClone(state.story.chapters.hook)),
    { askedRound: 1, checked: false, changed: 4 });
  const stale = structuredClone(oldState.story.chapters.hook);
  stale.checked = false;
  stale.listened = false;
  assert.deepEqual(await actualWorkerCheck(stale),
    { askedRound: 3, checked: true, changed: 4 });
  assert.equal(applyOfflineFixture(f.options).status, 'ALREADY_APPLIED_LOCAL_FIXTURE');
  assert.equal(fs.readdirSync(f.at(f.liveRoot, `${SLUG}/story/recheck-audit`)).length, 82);
  f.write(f.liveRoot, `${SLUG}/story/recheck-audit/event-040/index.json`, '{}\n');
  assert.notEqual(codeOf(() => verify82Fixture({ ...f.options, after82Root: f.liveRoot })), null);
});

test('source, history, review, STOP, lease and budget drift refuse before revision', (t) => {
  for (const mutate of [
    (f) => f.write(f.liveRoot, `${SLUG}/story/chapters/hook.json`, 'changed\n'),
    (f) => f.write(f.liveRoot, `${SLUG}/story/recheck-audit/event-040/index.json`, '{}\n'),
    (f) => { f.options.reviewBytes = json({ fake: true }); },
    (f) => fs.unlinkSync(f.at(f.liveRoot, `${SLUG}/STOP`)),
    (f) => f.write(f.liveRoot, `${SLUG}/LEASE`, 'active\n'),
    (f) => f.write(f.liveRoot, `${SLUG}/timeline.json`, '{}\n'),
    (f) => { f.options.safety.budget_operations = 1; },
  ]) {
    const f = fixture(t);
    mutate(f);
    assert.notEqual(codeOf(() => applyOfflineFixture(f.options)), null);
    assert.equal(fs.existsSync(f.at(f.liveRoot, OFFLINE_PINS.event_dir)), false);
    assert.equal(fs.existsSync(f.at(f.liveRoot, OFFLINE_PINS.receipt_dir)), false);
  }
});

test('ordinary source-stage error rolls back exact bytes; retained intent blocks blind retry', (t) => {
  const f = fixture(t);
  const before = f.hash(f.liveRoot, `${SLUG}/auto.json`);
  assert.equal(codeOf(() => applyOfflineFixture({ ...f.options,
    fault: (step) => { if (step === 'after-source') throw new Error('injected'); },
  })), 'injected');
  assert.equal(f.hash(f.liveRoot, `${SLUG}/auto.json`), before);
  assert.equal(fs.existsSync(f.at(f.liveRoot, OFFLINE_PINS.event_dir)), false);
  assert.equal(codeOf(() => applyOfflineFixture(f.options)),
    'PENDING_TRANSACTION_REQUIRES_MANUAL_RECOVERY');
});

test('crash after source or receipt holds partial state; full 82 readback is idempotent', (t) => {
  for (const stage of ['after-source', 'after-receipt-publish', 'after-audit-publish']) {
    const f = fixture(t);
    assert.equal(codeOf(() => applyOfflineFixture({ ...f.options,
      fault: (step) => { if (step === stage) throw new SimulatedFixtureCrash('crash'); },
    })), 'crash');
    if (stage === 'after-audit-publish') {
      assert.equal(applyOfflineFixture(f.options).status, 'ALREADY_APPLIED_LOCAL_FIXTURE');
      assert.equal(verify82Fixture({ ...f.options, after82Root: f.liveRoot }).new_pins.links, 82);
    } else {
      assert.notEqual(codeOf(() => applyOfflineFixture(f.options)), null);
      assert.equal(fs.existsSync(f.at(f.liveRoot, OFFLINE_PINS.event_dir)), false);
    }
  }
});

test('a concurrent source edit prevents destructive rollback and remains visible', (t) => {
  const f = fixture(t);
  const altered = 'external edit\n';
  const result = codeOf(() => applyOfflineFixture({ ...f.options,
    fault: (step) => { if (step === 'after-source') {
      f.write(f.liveRoot, `${SLUG}/auto.json`, altered);
      throw new Error('injected');
    } },
  }));
  assert.match(result, /MANUAL_RECOVERY_REQUIRED/u);
  assert.equal(fs.readFileSync(f.at(f.liveRoot, `${SLUG}/auto.json`), 'utf8'), altered);
});

test('a STOP change before final readback rolls back the new event and source', (t) => {
  const f = fixture(t);
  const priorAuto = f.hash(f.liveRoot, `${SLUG}/auto.json`);
  assert.equal(codeOf(() => applyOfflineFixture({ ...f.options,
    fault: (step) => { if (step === 'after-audit-publish')
      f.write(f.liveRoot, 'STOP', 'changed by another actor\n'); },
  })), 'POSTCOMMIT_SAFETY_DRIFT');
  assert.equal(f.hash(f.liveRoot, `${SLUG}/auto.json`), priorAuto);
  assert.equal(fs.existsSync(f.at(f.liveRoot, OFFLINE_PINS.event_dir)), false);
  assert.equal(fs.existsSync(f.at(f.liveRoot, OFFLINE_PINS.receipt_dir)), false);
});

test('the fixture writer refuses a repository root even with otherwise valid options', (t) => {
  const f = fixture(t);
  const repository = process.cwd();
  // The rejection occurs before any package or source mutation; no marker is ever added.
  assert.equal(codeOf(() => applyOfflineFixture({ ...f.options, liveRoot: repository })),
    'OS_TEMP_FIXTURE_ONLY');
});
