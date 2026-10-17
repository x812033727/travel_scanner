import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { cpSync, mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { prepareProposedEvent, proposeRebaseline, verifyProposedTransition } from './rebaseline.mjs';

const SLUG = 'story-rolling-suitcase-v2';
const CHAPTERS = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(`${JSON.stringify(value)}\n`);
const getCode = (call) => { try { call(); return null; } catch (error) { return error.code ?? error.message; } };

function fixture(t, { narrationText = '這是原始旁白。', narrationSay,
  videoText = '這是影片旁白。', videoSay } = {}) {
  const parent = mkdtempSync(path.join(os.tmpdir(), 'a01-lexicon-rebaseline-'));
  t.after(() => rmSync(parent, { recursive: true, force: true }));
  const beforeRoot = path.join(parent, 'before');
  const afterRoot = path.join(parent, 'after');
  mkdirSync(beforeRoot);
  const at = (root, rel) => path.join(root, ...rel.split('/'));
  const write = (root, rel, bytes) => {
    const file = at(root, rel);
    mkdirSync(path.dirname(file), { recursive: true });
    writeFileSync(file, bytes);
    return file;
  };
  const hash = (root, rel) => sha(readFileSync(at(root, rel)));
  const docs = `docs/videos/${SLUG}`;
  const oldLexicon = json({ schema_version: 1, terms: { OpenAI: 'Open A I', Plath: null } });
  const newLexicon = json({ schema_version: 1, terms: { OpenAI: 'Open A I', Plath: null, pull: null, request: null } });
  const oldLexiconFile = write(parent, 'old-lexicon.json', oldLexicon);
  for (const [rel, content] of Object.entries({
    [`${docs}/series.json`]: 'series\n',
    [`${docs}/claims.md`]: 'claims\n', [`${docs}/script.md`]: 'script\n',
    [`${SLUG}/review/narrative.json`]: 'narrative\n',
  })) write(beforeRoot, rel, content);
  write(beforeRoot, `${docs}/video.json`, json({ schema_version: 1, slug: SLUG,
    scenes: [{ id: 'video-01', lines: [{ id: 'video-line-01', text: videoText,
      ...(videoSay === undefined ? {} : { say: videoSay }) }] }] }));
  write(beforeRoot, 'docs/videos/lexicon.json', newLexicon);
  for (const key of CHAPTERS) write(beforeRoot, `${SLUG}/story/chapters/${key}.json`, json({ key,
    scenes: [{ id: `${key}-01`, lines: [{ id: 'line-01', text: narrationText,
      ...(narrationSay === undefined ? {} : { say: narrationSay }) }] }] }));
  write(beforeRoot, `${SLUG}/auto.json`, 'auto-80\n');
  const source = (n, lexiconHash = sha(oldLexicon)) => ({
    auto: sha(`auto-${n}\n`), video: hash(beforeRoot, `${docs}/video.json`),
    series: hash(beforeRoot, `${docs}/series.json`), claims: hash(beforeRoot, `${docs}/claims.md`),
    script: hash(beforeRoot, `${docs}/script.md`), lexicon: lexiconHash,
    narrative: hash(beforeRoot, `${SLUG}/review/narrative.json`), pilot: null, verify: null,
    chapters: Object.fromEntries(CHAPTERS.map((key) => [key, hash(beforeRoot, `${SLUG}/story/chapters/${key}.json`)])),
  });
  const installed = {
    'docs/video.json': source(0).video, 'docs/script.md': source(0).script,
    'docs/claims.md': source(0).claims, 'docs/series.json': source(0).series,
    ...Object.fromEntries(CHAPTERS.map((key) => [`work/story/chapters/${key}.json`, source(0).chapters[key]])),
    'work/auto.json': source(0).auto,
  };
  const receiptRel = `${SLUG}/manual-revisions/initial/installation-receipt.json`;
  write(beforeRoot, receiptRel, json({ schema_version: 1, kind: 'a01-candidate-installation', slug: SLUG,
    installed_sha256: installed }));
  const manifest = [];
  for (let n = 0; n < 80; n++) {
    const id = `event-${String(n).padStart(3, '0')}`;
    const dir = `${SLUG}/story/recheck-audit/${id}`;
    const journalBytes = json({ n, result: 'saved' });
    const journalHash = sha(journalBytes);
    write(beforeRoot, `${dir}/${journalHash}.json`, journalBytes);
    const before = source(n), after = source(n + 1);
    const index = { schema_version: 1, slug: SLUG, result_kind: 'saved',
      install_receipt_sha256: hash(beforeRoot, receiptRel),
      before_source_sha256: sha(JSON.stringify(before)), after_source_sha256: sha(JSON.stringify(after)),
      before, after, journals: [{ name: `${journalHash}.json`, sha256: journalHash }] };
    write(beforeRoot, `${dir}/index.json`, json(index));
    manifest.push({ id, index_sha256: hash(beforeRoot, `${dir}/index.json`) });
  }
  const pins = { id: 'synthetic-fixed-80', links: 80,
    install_receipt_sha256: hash(beforeRoot, receiptRel),
    tip_index_sha256: manifest.at(-1).index_sha256,
    source_composite_sha256: sha(JSON.stringify(source(80))),
    archive_index_manifest_sha256: sha(JSON.stringify(manifest)) };
  const options = { snapshotRoot: beforeRoot, oldLexiconFile, pins,
    expectedOldSha: sha(oldLexicon), expectedNewSha: sha(newLexicon) };
  const clone = () => cpSync(beforeRoot, afterRoot, { recursive: true });
  const evidence = () => {
    const { plan, plan_sha256: planSha } = proposeRebaseline(options);
    const reviewBytes = json({ schema_version: 1, kind: 'a01_lexicon_rebaseline_independent_review',
      slug: SLUG, verdict: 'PASS', independent: true, reviewer: 'independent-editor',
      plan_sha256: planSha, old_lexicon_sha256: plan.old_lexicon_sha256,
      new_lexicon_sha256: plan.new_lexicon_sha256,
      before_source_sha256: plan.old_pinset.source_composite_sha256,
      after_source_sha256: plan.after_source_composite_sha256, delta: plan.delta });
    const receiptBytes = json({ schema_version: 1, kind: 'a01_lexicon_rebaseline_record_receipt',
      slug: SLUG, plan_sha256: planSha, event_id: plan.event_id, revision: plan.revision,
      old_lexicon_sha256: plan.old_lexicon_sha256,
      new_lexicon_sha256: plan.new_lexicon_sha256,
      before_source_sha256: plan.old_pinset.source_composite_sha256,
      after_source_sha256: plan.after_source_composite_sha256,
      review_sha256: sha(reviewBytes), record_only: true, lexicon_file_writes: 0,
      operator: 'fixture-operator', owner_approval_ref: 'synthetic-owner-approval' });
    return { plan, reviewBytes, receiptBytes };
  };
  const prepare = () => {
    const { reviewBytes, receiptBytes } = evidence();
    return prepareProposedEvent({ ...options, reviewBytes, receiptBytes });
  };
  const addFiles = (files) => { for (const [rel, bytes] of Object.entries(files)) write(afterRoot, rel, bytes); };
  const verify = () => verifyProposedTransition({ ...options, beforeRoot, afterRoot });
  return { parent, beforeRoot, afterRoot, oldLexiconFile, at, write, hash, clone,
    options, evidence, prepare, addFiles, verify };
}

test('deterministic 80-to-81 proposal and local transition keep production HOLD', (t) => {
  const f = fixture(t);
  const first = proposeRebaseline(f.options), second = proposeRebaseline(f.options);
  assert.deepEqual(first, second);
  assert.equal(first.plan.delta.old_term_count, 2);
  assert.equal(first.plan.delta.new_term_count, 4);
  assert.deepEqual(first.plan.delta.additions, { pull: null, request: null });
  assert.equal(first.plan.narration_term_hits, 0);
  assert.equal(first.production_status, 'HOLD');
  const prepared = f.prepare();
  f.clone();
  f.addFiles(prepared.files);
  const verified = f.verify();
  assert.equal(verified.integrity, 'LOCAL_81_EVENT_TRANSITION_PASS');
  assert.equal(verified.new_pins.links, 81);
  assert.equal(verified.new_pins.tip_index_sha256, sha(prepared.files[`${prepared.event_path}/index.json`]));
  assert.equal(verified.installation_allowed, false);
  assert.equal(verified.paid_work_allowed, false);
  assert.equal(f.hash(f.beforeRoot, `${SLUG}/story/recheck-audit/event-079/index.json`),
    f.hash(f.afterRoot, `${SLUG}/story/recheck-audit/event-079/index.json`));
});

test('forged previous index link fails historical pins even when current source still matches', (t) => {
  const f = fixture(t);
  const rel = `${SLUG}/story/recheck-audit/event-040/index.json`;
  const index = JSON.parse(readFileSync(f.at(f.beforeRoot, rel), 'utf8'));
  index.result_kind = 'forged';
  f.write(f.beforeRoot, rel, json(index));
  assert.equal(getCode(() => proposeRebaseline(f.options)), 'BASELINE_ARCHIVE_INDEX_MANIFEST_MISMATCH');
});

test('new event with a forged previous source link cannot pass exact byte transition', (t) => {
  const f = fixture(t), prepared = f.prepare();
  f.clone(); f.addFiles(prepared.files);
  const rel = `${prepared.event_path}/index.json`;
  const index = JSON.parse(readFileSync(f.at(f.afterRoot, rel), 'utf8'));
  index.before_source_sha256 = 'f'.repeat(64);
  f.write(f.afterRoot, rel, json(index));
  assert.equal(getCode(f.verify), 'PROPOSED_EVENT_BYTES_MISMATCH');
});

test('review and receipt forgery fail before event preparation or after staging', (t) => {
  const f = fixture(t), { reviewBytes, receiptBytes } = f.evidence();
  const forgedReview = JSON.parse(reviewBytes.toString('utf8'));
  forgedReview.verdict = 'FAIL';
  assert.equal(getCode(() => prepareProposedEvent({ ...f.options,
    reviewBytes: json(forgedReview), receiptBytes })), 'REVIEW_BINDING_INVALID');
  const forgedReceipt = JSON.parse(receiptBytes.toString('utf8'));
  forgedReceipt.owner_approval_ref = '';
  assert.equal(getCode(() => prepareProposedEvent({ ...f.options,
    reviewBytes, receiptBytes: json(forgedReceipt) })), 'RECEIPT_BINDING_INVALID');
  const prepared = f.prepare(); f.clone(); f.addFiles(prepared.files);
  f.write(f.afterRoot, `${prepared.event_path}/independent-review.json`, 'forged review\n');
  assert.equal(getCode(f.verify), 'INVALID_REVIEW_JSON');
  f.addFiles(prepared.files);
  f.write(f.afterRoot, `${SLUG}/${prepared.candidate.plan.revision}/installation-receipt.json`, 'forged receipt\n');
  assert.equal(getCode(f.verify), 'INVALID_RECEIPT_JSON');
});

test('other source drift and used narration terms cannot be hidden behind the lexicon change', (t) => {
  const f = fixture(t);
  f.write(f.beforeRoot, `docs/videos/${SLUG}/script.md`, 'new script\n');
  assert.equal(getCode(() => proposeRebaseline(f.options)), 'OTHER_SOURCE_DRIFT');
  const g = fixture(t, { narrationText: 'Please pull this.' });
  assert.equal(getCode(() => proposeRebaseline(g.options)), 'NEW_LEXICON_TERM_IN_NARRATION');
});

test('chapter say-only lexicon term is refused even when text is clean', (t) => {
  const f = fixture(t, { narrationSay: 'Please pull this.' });
  assert.equal(getCode(() => proposeRebaseline(f.options)), 'NEW_LEXICON_TERM_IN_NARRATION');
});

test('video-only spoken lexicon term is refused while all chapter lines are clean', (t) => {
  const f = fixture(t, { videoText: '沒有敏感詞。', videoSay: 'Please request this.' });
  assert.equal(getCode(() => proposeRebaseline(f.options)), 'NEW_LEXICON_TERM_IN_NARRATION');
});

test('video-only text fallback is refused when say is absent', (t) => {
  const f = fixture(t, { videoText: 'Please request this.' });
  assert.equal(getCode(() => proposeRebaseline(f.options)), 'NEW_LEXICON_TERM_IN_NARRATION');
});

test('duplicate event is refused before planning or after the proposed transition', (t) => {
  const f = fixture(t), prepared = f.prepare();
  f.clone(); f.addFiles(prepared.files);
  f.write(f.afterRoot, `${SLUG}/story/recheck-audit/duplicate/index.json`, '{}\n');
  assert.equal(getCode(f.verify), 'EVENT_COUNT_OR_ID_MISMATCH');
  f.write(f.beforeRoot, `${SLUG}/story/recheck-audit/duplicate/index.json`, '{}\n');
  assert.equal(getCode(() => proposeRebaseline(f.options)), 'BASELINE_AUDIT_INDEX_INVALID');
});

test('concurrent lexicon mutation and changed historical evidence fail the post-readback', (t) => {
  const f = fixture(t), prepared = f.prepare();
  f.clone(); f.addFiles(prepared.files);
  f.write(f.afterRoot, 'docs/videos/lexicon.json', 'changed concurrently\n');
  assert.equal(getCode(f.verify), 'CONCURRENT_SOURCE_DRIFT');
  f.addFiles(prepared.files);
  f.write(f.afterRoot, 'docs/videos/lexicon.json', readFileSync(f.at(f.beforeRoot, 'docs/videos/lexicon.json')));
  f.write(f.afterRoot, `${SLUG}/story/recheck-audit/event-040/index.json`, 'tampered\n');
  assert.equal(getCode(f.verify), 'HISTORICAL_EVIDENCE_DRIFT');
});

test('partial staging leaves a HOLD and never promotes a pin transition', (t) => {
  const f = fixture(t), prepared = f.prepare();
  f.clone();
  const receiptPath = `${SLUG}/${prepared.candidate.plan.revision}/installation-receipt.json`;
  f.write(f.afterRoot, receiptPath, prepared.files[receiptPath]);
  assert.equal(getCode(f.verify), 'MISSING_FILE');
  f.write(f.afterRoot, `${prepared.event_path}/independent-review.json`,
    prepared.files[`${prepared.event_path}/independent-review.json`]);
  assert.equal(getCode(f.verify), 'UNEXPECTED_NEW_EVENT_FILE');
  assert.equal(f.hash(f.beforeRoot, 'docs/videos/lexicon.json'), f.hash(f.afterRoot, 'docs/videos/lexicon.json'));
});

test('semantic lexicon edits other than exactly two null terms are refused', (t) => {
  const f = fixture(t);
  const changed = json({ schema_version: 1, terms: { OpenAI: 'changed', Plath: null,
    pull: null, request: null } });
  f.write(f.beforeRoot, 'docs/videos/lexicon.json', changed);
  assert.equal(getCode(() => proposeRebaseline({ ...f.options, expectedNewSha: sha(changed) })),
    'LEXICON_DELTA_NOT_ALLOWED');
});
