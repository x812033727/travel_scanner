import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { prepareProposedEvent, proposeRebaseline, verifyProposedTransition } from '../A01-lexicon-rebaseline-candidate/rebaseline.mjs';
import { OFFLINE_PINS, planOfflineRevision, prepareOfflineRevision } from '../A01-round20-existing-revision-offline-candidate/revision-fixture.mjs';

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

// Adapted from the independently tested 81→82 synthetic fixture. Test data only.
function fixture(t) {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), 'a01-round20-82-'));
  t.after(() => {
    const resolved = fs.realpathSync(parent);
    assert.equal(path.dirname(resolved), fs.realpathSync(os.tmpdir()));
    assert.ok(path.basename(resolved).startsWith('a01-round20-82-'));
    fs.rmSync(resolved, { recursive: true, force: true });
  });
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

const id = (digit) => `${digit}`.repeat(8) + '-0000-4000-8000-' + `${digit}`.repeat(12);

export function hostFixture(t) {
  const f = fixture(t);
  const marker = json({ schema_version: 1, slug: SLUG, synthetic_fixture: true });
  write(f.before80Root, 'A01-HOST-TRANSITION-OFFLINE-FIXTURE.json', marker);
  write(f.before81Root, 'A01-HOST-TRANSITION-OFFLINE-FIXTURE.json', marker);
  const authored = JSON.parse(fs.readFileSync(new URL('../../series.json', import.meta.url), 'utf8'));
  const state = {
    schema_version: 1, slug: SLUG, observed_at: '2026-10-17T00:00:00Z',
    release: { git_sha: 'a'.repeat(40), worker_sha256: 'b'.repeat(64),
      panel_rules_sha256: 'c'.repeat(64) },
    archive: { source_composite_sha256: f.prepared81.expected_pins.source_composite_sha256,
      audit_manifest_sha256: f.prepared81.expected_pins.archive_index_manifest_sha256,
      tip_index_sha256: f.prepared81.expected_pins.tip_index_sha256 },
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
  const beforePinsFile = write(f.parent, 'before-pins.json', json(f.pins80));
  const stateFile = write(f.parent, 'state.json', json(state));
  const afterPinsFile = write(f.parent, 'after-pins.json',
    json({ ...f.prepared81.expected_pins, state_sha256: hash(f.parent, 'state.json') }));
  const reviewFile = write(f.parent, 'review.json', f.options.reviewBytes);
  const receiptFile = write(f.parent, 'receipt.json', f.options.receiptBytes);
  const inspectionOptions = { before80Root: f.before80Root, before81Root: f.before81Root,
    oldLexiconFile: f.options.oldLexiconFile, beforePinsFile, afterPinsFile, stateFile,
    expectedOldSha: f.options.expectedOldSha, expectedNewSha: f.options.expectedNewSha,
    syntheticFixture: true };
  return { ...f, state, beforePinsFile, afterPinsFile, stateFile,
    reviewFile, receiptFile, inspectionOptions };
}
