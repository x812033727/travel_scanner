import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { inspectSnapshot } from '../A01-host-inspect-candidate/inspect.mjs';
import { prepareProposedEvent, proposeRebaseline } from '../A01-lexicon-rebaseline-candidate/rebaseline.mjs';
import { inspectTransitionExport } from './inspect-transition-export.mjs';

const SLUG = 'story-rolling-suitcase-v2';
const CHAPTERS = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(`${JSON.stringify(value)}\n`, 'utf8');
const id = (digit) => `${digit}`.repeat(8) + '-0000-4000-8000-' + `${digit}`.repeat(12);
const authored = JSON.parse(fs.readFileSync(new URL('../../series.json', import.meta.url), 'utf8'));

function fixture(t) {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), 'a01-transition-export-'));
  t.after(() => fs.rmSync(parent, { recursive: true, force: true }));
  const beforeRoot = path.join(parent, 'before');
  const afterRoot = path.join(parent, 'after');
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
  write(beforeRoot, `${docs}/video.json`, json({ scenes: [{ id: 'v1', lines: [
    { id: 'l1', text: '一段中文旁白。' },
  ] }] }));
  write(beforeRoot, 'docs/videos/lexicon.json', newLexicon);
  for (const chapter of CHAPTERS) write(beforeRoot,
    `${SLUG}/story/chapters/${chapter}.json`, json({ scenes: [{
      id: `${chapter}-01`, lines: [{ id: 'l1', text: '一段中文旁白。' }],
    }] }));
  write(beforeRoot, `${SLUG}/auto.json`, 'auto-80\n');
  const source = (n, lexiconHash = sha(oldLexicon)) => ({
    auto: sha(`auto-${n}\n`), video: hash(beforeRoot, `${docs}/video.json`),
    series: hash(beforeRoot, `${docs}/series.json`), claims: hash(beforeRoot, `${docs}/claims.md`),
    script: hash(beforeRoot, `${docs}/script.md`), lexicon: lexiconHash,
    narrative: hash(beforeRoot, `${SLUG}/review/narrative.json`), pilot: null, verify: null,
    chapters: Object.fromEntries(CHAPTERS.map((chapter) => [chapter,
      hash(beforeRoot, `${SLUG}/story/chapters/${chapter}.json`)])),
  });
  const first = source(0);
  const installed = { 'docs/video.json': first.video, 'docs/script.md': first.script,
    'docs/claims.md': first.claims, 'docs/series.json': first.series,
    ...Object.fromEntries(CHAPTERS.map((chapter) => [`work/story/chapters/${chapter}.json`,
      first.chapters[chapter]])), 'work/auto.json': first.auto };
  const receiptRel = `${SLUG}/manual-revisions/initial/installation-receipt.json`;
  write(beforeRoot, receiptRel, json({ schema_version: 1, kind: 'a01-candidate-installation',
    slug: SLUG, installed_sha256: installed }));
  const manifest = [];
  for (let n = 0; n < 80; n++) {
    const event = `event-${String(n).padStart(3, '0')}`;
    const dir = `${SLUG}/story/recheck-audit/${event}`;
    const journal = json({ n, result: 'saved' });
    const journalHash = sha(journal);
    write(beforeRoot, `${dir}/${journalHash}.json`, journal);
    const before = source(n), after = source(n + 1);
    write(beforeRoot, `${dir}/index.json`, json({ schema_version: 1, slug: SLUG,
      result_kind: 'saved', install_receipt_sha256: hash(beforeRoot, receiptRel),
      before_source_sha256: sha(JSON.stringify(before)),
      after_source_sha256: sha(JSON.stringify(after)), before, after,
      journals: [{ name: `${journalHash}.json`, sha256: journalHash }] }));
    manifest.push({ id: event, index_sha256: hash(beforeRoot, `${dir}/index.json`) });
  }
  const pins = { id: 'fixture-80', links: 80,
    install_receipt_sha256: hash(beforeRoot, receiptRel),
    tip_index_sha256: manifest.at(-1).index_sha256,
    source_composite_sha256: sha(JSON.stringify(source(80))),
    archive_index_manifest_sha256: sha(JSON.stringify(manifest)) };
  const base = { snapshotRoot: beforeRoot, oldLexiconFile, pins,
    expectedOldSha: sha(oldLexicon), expectedNewSha: sha(newLexicon) };
  const { plan, plan_sha256: planSha } = proposeRebaseline(base);
  const reviewBytes = json({ schema_version: 1,
    kind: 'a01_lexicon_rebaseline_independent_review', slug: SLUG,
    verdict: 'PASS', independent: true, reviewer: 'synthetic-only',
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
  fs.cpSync(beforeRoot, afterRoot, { recursive: true });
  for (const [rel, bytes] of Object.entries(prepared.files)) write(afterRoot, rel, bytes);
  const marker = json({ schema_version: 1, slug: SLUG, synthetic_fixture: true });
  write(beforeRoot, 'A01-HOST-TRANSITION-OFFLINE-FIXTURE.json', marker);
  write(afterRoot, 'A01-HOST-TRANSITION-OFFLINE-FIXTURE.json', marker);
  const state = {
    schema_version: 1, slug: SLUG, observed_at: '2026-10-16T06:00:00Z',
    release: { git_sha: 'a'.repeat(40), worker_sha256: 'b'.repeat(64),
      panel_rules_sha256: 'c'.repeat(64) },
    archive: { source_composite_sha256: prepared.expected_pins.source_composite_sha256,
      audit_manifest_sha256: prepared.expected_pins.archive_index_manifest_sha256,
      tip_index_sha256: prepared.expected_pins.tip_index_sha256 },
    filesystem: { global_stop: { present: true, sha256: 'd'.repeat(64) },
      scoped_stop: { present: true, sha256: 'e'.repeat(64) },
      lease: { present: false, sha256: null }, unresolved_journals: 0,
      run_receipts: [], media_assets: [] },
    db: {
      series: { id: id('1'), slug: authored.slug, kind: authored.kind, status: 'active',
        title: authored.title, premise: authored.premise, note: authored.note,
        target_minutes: authored.target_minutes, planned_episodes: authored.planned_episodes,
        episodes_per_day: authored.episodes_per_day, image_model: authored.image_model,
        look: authored.look, style_preset: authored.style_preset, hands_off: authored.hands_off,
        visual_tier: authored.visual_tier, compilation: authored.compilation },
      episode: { id: id('2'), series_id: id('1'), number: 1, slug: SLUG, status: 'started' },
      project: { slug: SLUG, format: 'drama', series_slug: authored.slug, episode_number: 1,
        stage: 'blocked', retry_request_id: null, retry_acknowledged_id: null },
      budget: { slug: SLUG, limit_usd: '25.000000', reserved_usd: '0', settled_usd: '0',
        remaining_usd: '25.000000', total_over_limit: false, over_limit_usd: '0.000000',
        uncertain_operations: 0, overrun_operations: 0, operations: [] },
      stage_jobs: [], media_jobs: [],
    },
  };
  const beforePinsFile = write(parent, 'before-pins.json', json(pins));
  const stateFile = at(parent, 'state.json');
  const afterPinsFile = at(parent, 'after-pins.json');
  const saveState = () => {
    const bytes = json(state);
    fs.writeFileSync(stateFile, bytes);
    fs.writeFileSync(afterPinsFile, json({ ...prepared.expected_pins, state_sha256: sha(bytes) }));
  };
  saveState();
  const run = () => inspectTransitionExport({ beforeRoot, afterRoot, oldLexiconFile,
    beforePinsFile, afterPinsFile, stateFile, expectedOldSha: base.expectedOldSha,
    expectedNewSha: base.expectedNewSha, syntheticFixture: true });
  return { parent, beforeRoot, afterRoot, oldLexiconFile, pins, prepared,
    state, stateFile, beforePinsFile, afterPinsFile, saveState, run, at, write };
}

test('A01 offline transition and export gate', async (t) => {
  const f = fixture(t);
  await t.test('exact 80 to 81 transition binds independently pinned export state; old gate stays strict', () => {
  const result = f.run();
  assert.equal(result.result, 'LOCAL_TRANSITION_EXPORT_BINDING_ONLY', JSON.stringify(result.errors));
  assert.equal(result.source_integrity, 'LOCAL_81_EVENT_TRANSITION_PASS');
  assert.equal(result.before_history_links, 80);
  assert.equal(result.after_history_links, 81);
  assert.equal(result.production_status, 'HOLD');
  assert.equal(result.installation_allowed, false);
  assert.equal(result.paid_work_allowed, false);
  assert.equal(result.owner_approval_verified, false);
  assert.equal(result.exclusive_writer_window_verified, false);
  assert.equal(inspectSnapshot({ snapshotRoot: f.afterRoot, pins: f.pins }).errors[0].code,
    'LINK_COUNT_MISMATCH');
  });

  await t.test('old evidence, exact new event, source and external pins reject tampering', () => {
  const rel = `${SLUG}/story/recheck-audit/event-040/index.json`;
  const old = fs.readFileSync(f.at(f.beforeRoot, rel));
  f.write(f.beforeRoot, rel, '{}\n');
  assert.equal(f.run().result, 'REJECTED');
  f.write(f.beforeRoot, rel, old);
  const afterOld = fs.readFileSync(f.at(f.afterRoot, rel));
  f.write(f.afterRoot, rel, '{}\n');
  assert.equal(f.run().result, 'REJECTED');
  f.write(f.afterRoot, rel, afterOld);
  const journal = fs.readdirSync(f.at(f.afterRoot, `${SLUG}/story/recheck-audit/event-040`))
    .find((name) => name !== 'index.json');
  const journalRel = `${SLUG}/story/recheck-audit/event-040/${journal}`;
  const journalBytes = fs.readFileSync(f.at(f.afterRoot, journalRel));
  f.write(f.afterRoot, journalRel, 'changed\n');
  assert.equal(f.run().result, 'REJECTED');
  f.write(f.afterRoot, journalRel, journalBytes);
  const newIndexRel = `${SLUG}/story/recheck-audit/${f.prepared.candidate.plan.event_id}/index.json`;
  const newIndex = fs.readFileSync(f.at(f.afterRoot, newIndexRel));
  f.write(f.afterRoot, newIndexRel, '{}\n');
  assert.equal(f.run().result, 'REJECTED');
  f.write(f.afterRoot, newIndexRel, newIndex);
  const lexiconRel = 'docs/videos/lexicon.json';
  const lexicon = fs.readFileSync(f.at(f.afterRoot, lexiconRel));
  f.write(f.afterRoot, lexiconRel, json({ schema_version: 1, terms: { extra: null } }));
  assert.equal(f.run().result, 'REJECTED');
  f.write(f.afterRoot, lexiconRel, lexicon);
  const afterPins = fs.readFileSync(f.afterPinsFile);
  fs.writeFileSync(f.afterPinsFile, json({ ...JSON.parse(afterPins), links: 82 }));
  assert.equal(f.run().errors[0].code, 'AFTER_PINSET_INVALID');
  fs.writeFileSync(f.afterPinsFile, afterPins);
  const beforePins = fs.readFileSync(f.beforePinsFile);
  fs.writeFileSync(f.beforePinsFile, json({ ...JSON.parse(beforePins),
    tip_index_sha256: 'f'.repeat(64) }));
  assert.equal(f.run().result, 'REJECTED');
  fs.writeFileSync(f.beforePinsFile, beforePins);
  assert.equal(f.run().result, 'LOCAL_TRANSITION_EXPORT_BINDING_ONLY');
  });

  await t.test('missing or extra event and changed review or receipt refuse the transition', () => {
  const event = f.prepared.candidate.plan.event_id;
  const eventDir = f.at(f.afterRoot, `${SLUG}/story/recheck-audit/${event}`);
  const missingDir = `${eventDir}-missing`;
  fs.renameSync(eventDir, missingDir);
  assert.equal(f.run().result, 'REJECTED');
  fs.renameSync(missingDir, eventDir);
  f.write(f.afterRoot, `${SLUG}/story/recheck-audit/extra/index.json`, '{}\n');
  assert.equal(f.run().result, 'REJECTED');
  fs.rmSync(f.at(f.afterRoot, `${SLUG}/story/recheck-audit/extra`), { recursive: true });
  const reviewRel = `${SLUG}/story/recheck-audit/${event}/independent-review.json`;
  const review = fs.readFileSync(f.at(f.afterRoot, reviewRel));
  f.write(f.afterRoot, reviewRel, json({ verdict: 'fake' }));
  assert.equal(f.run().result, 'REJECTED');
  f.write(f.afterRoot, reviewRel, review);
  const receiptRel = `${SLUG}/manual-revisions/${event}/installation-receipt.json`;
  const receipt = fs.readFileSync(f.at(f.afterRoot, receiptRel));
  f.write(f.afterRoot, receiptRel, json({ receipt: 'fake' }));
  assert.equal(f.run().result, 'REJECTED');
  f.write(f.afterRoot, receiptRel, receipt);
  assert.equal(f.run().result, 'LOCAL_TRANSITION_EXPORT_BINDING_ONLY');
  });

  await t.test('state, budget, jobs, inventory and release bind to the 81st pinset', () => {
  f.state.archive.tip_index_sha256 = 'f'.repeat(64); f.saveState();
  assert.equal(f.run().errors[0].code, 'ARCHIVE_STATE_BINDING_MISMATCH');
  f.state.archive.tip_index_sha256 = f.prepared.expected_pins.tip_index_sha256;
  f.state.db.budget.remaining_usd = '24.000000'; f.saveState();
  assert.equal(f.run().errors[0].code, 'BUDGET_TOTAL_MISMATCH');
  f.state.db.budget.remaining_usd = '25.000000';
  f.state.db.media_jobs = [{ id: id('3'), status: 'queued', kind: 'image', operation_id: null }];
  f.saveState();
  assert.equal(f.run().errors[0].code, 'MEDIA_BUDGET_LINK_MISSING');
  f.state.db.media_jobs = [];
  f.state.filesystem.global_stop.sha256 = null; f.saveState();
  assert.equal(f.run().errors[0].code, 'INVALID_STOP_RECORD');
  f.state.filesystem.global_stop.sha256 = 'd'.repeat(64);
  f.state.filesystem.run_receipts = [{ path: '../escape', sha256: 'f'.repeat(64), bytes: 1 }];
  f.saveState();
  assert.equal(f.run().errors[0].code, 'INVALID_RUN_RECEIPTS');
  f.state.filesystem.run_receipts = [];
  f.state.release.worker_sha256 = 'invalid'; f.saveState();
  assert.equal(f.run().errors[0].code, 'INVALID_RELEASE_READBACK');
  f.state.release.worker_sha256 = 'b'.repeat(64); f.saveState();
  assert.equal(f.run().result, 'LOCAL_TRANSITION_EXPORT_BINDING_ONLY');
  const state = fs.readFileSync(f.stateFile);
  fs.writeFileSync(f.stateFile, json({ ...JSON.parse(state), observed_at: '2026-10-17T00:00:00Z' }));
  assert.equal(f.run().errors[0].code, 'STATE_PIN_MISMATCH');
  f.saveState();
  });

  await t.test('synthetic overrides cannot be used through the production-shaped interface', () => {
  const result = inspectTransitionExport({ beforeRoot: f.beforeRoot, afterRoot: f.afterRoot,
    oldLexiconFile: f.oldLexiconFile, beforePinsFile: f.beforePinsFile,
    afterPinsFile: f.afterPinsFile, stateFile: f.stateFile });
  assert.equal(result.errors[0].code, 'HISTORICAL_PINS_MISMATCH');
  const missingMarker = f.at(f.afterRoot, 'A01-HOST-TRANSITION-OFFLINE-FIXTURE.json');
  fs.rmSync(missingMarker);
  assert.equal(f.run().errors[0].code, 'SYNTHETIC_MARKER_MISSING');
  });
});
