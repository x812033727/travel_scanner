import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fixture } from './synthetic-fixture.mjs';
import { planPinnedTransition, preparePinnedEvent, verifyPinnedTransition } from './transition.mjs';
import { readStoryLexicon } from './snapshot-format.mjs';

const SLUG = 'story-rolling-suitcase-v2';
const KIND = 'a01_pinned_historical_lexicon_20261017';
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const json = value => Buffer.from(`${JSON.stringify(value)}\n`);
function evidence(f) {
  const { plan, plan_sha256 } = planPinnedTransition(f.options);
  const common = { schema_version: 1, slug: SLUG, plan_sha256,
    pinned_lexicon_sha256: plan.pinned_lexicon_sha256, pinned_head_event_sha256: plan.pinned_head_event_sha256,
    before_source_sha256: plan.before_source_sha256, after_source_sha256: plan.after_source_sha256 };
  const reviewBytes = json({ ...common, kind: `${KIND}_review`, verdict: 'PASS', independent: true, reviewer: 'synthetic-independent-reviewer' });
  const receiptBytes = json({ ...common, kind: `${KIND}_receipt`, operator: 'synthetic-operator',
    owner_approval_ref: 'SYNTHETIC_NOT_PRODUCTION', review_sha256: sha(reviewBytes), paid_calls: 0, shared_lexicon_writes: 0 });
  return { reviewBytes, receiptBytes };
}
function installFixture(f, prepared) {
  f.clone();
  for (const [rel, bytes] of Object.entries(prepared.files)) f.write(f.afterRoot, rel, bytes);
}
const verify = f => verifyPinnedTransition({ ...f.options, beforeRoot: f.beforeRoot, afterRoot: f.afterRoot });

test('an isolated 80-to-81 pin preserves the old dictionary, all old files and counters', t => {
  const f = fixture(t);
  const first = planPinnedTransition(f.options);
  assert.deepEqual(first, planPinnedTransition(f.options));
  assert.notEqual(first.plan.before_source_sha256, first.plan.after_source_sha256);
  assert.equal(first.plan.before_source_hashes.lexicon, first.plan.after_source_hashes.lexicon);
  assert.notEqual(first.plan.pinned_lexicon_sha256, first.plan.observed_shared_lexicon_sha256);
  assert.equal(first.plan.historical_event_ids.length, 80);
  assert.throws(() => preparePinnedEvent(f.options), /INDEPENDENT_REVIEW_AND_OWNER_RECEIPT_REQUIRED/);
  const prepared = preparePinnedEvent({ ...f.options, ...evidence(f) });
  installFixture(f, prepared);
  const checked = verify(f);
  assert.equal(checked.integrity, 'LOCAL_PINNED_81_EVENT_TRANSITION_PASS');
  assert.equal(checked.production_status, 'HOLD');
  assert.equal(checked.installation_allowed, false);
  const before = JSON.parse(readFileSync(f.at(f.beforeRoot, `${SLUG}/auto.json`)));
  const after = JSON.parse(readFileSync(f.at(f.afterRoot, `${SLUG}/auto.json`)));
  delete after.story.lexicon_sha256;
  delete after.story.lexicon_head_event_sha256;
  assert.deepEqual(after, before);
  const selected = readStoryLexicon({ slug: SLUG, storyDir: f.at(f.afterRoot, `docs/videos/${SLUG}`), sharedFile: f.at(f.afterRoot, 'docs/videos/lexicon.json') });
  assert.deepEqual(selected.bytes, readFileSync(f.oldLexiconFile));
});

test('changing or adding an old audit file is rejected', t => {
  for (const extra of [false, true]) {
    const f = fixture(t);
    installFixture(f, preparePinnedEvent({ ...f.options, ...evidence(f) }));
    const event = planPinnedTransition(f.options).plan.historical_event_ids[0];
    f.write(f.afterRoot, `${SLUG}/story/recheck-audit/${event}/${extra ? 'extra.json' : 'index.json'}`, json({ changed: true }));
    assert.throws(() => verify(f), /HISTORICAL_(BYTES|FILE_SET)_CHANGED/);
  }
});

test('partial publication, a new optional approval and changed shared bytes cannot pass readback', t => {
  for (const mode of ['snapshot-only', 'extra-pilot', 'shared-drift']) {
    const f = fixture(t);
    const prepared = preparePinnedEvent({ ...f.options, ...evidence(f) });
    if (mode === 'snapshot-only') {
      f.clone();
      for (const [rel, bytes] of Object.entries(prepared.files).filter(([rel]) => rel.includes('/story-lexicon/'))) f.write(f.afterRoot, rel, bytes);
    } else {
      installFixture(f, prepared);
      if (mode === 'extra-pilot') f.write(f.afterRoot, `${SLUG}/story/reviews/script-review.json`, json({ pass: true }));
      else f.write(f.afterRoot, 'docs/videos/lexicon.json', json({ schema_version: 1, terms: { changed: null } }));
    }
    assert.throws(() => verify(f));
  }
});

test('a changed review, reused reviewer identity or old state mutation is rejected', t => {
  const f = fixture(t);
  const input = evidence(f);
  const receipt = JSON.parse(input.receiptBytes);
  receipt.operator = 'synthetic-independent-reviewer';
  assert.throws(() => preparePinnedEvent({ ...f.options, ...input, receiptBytes: json(receipt) }), /OWNER_RECORD_RECEIPT_INVALID/);
  installFixture(f, preparePinnedEvent({ ...f.options, ...input }));
  const current = JSON.parse(readFileSync(f.at(f.afterRoot, `${SLUG}/auto.json`)));
  current.story.narrative_fixes = 0;
  f.write(f.afterRoot, `${SLUG}/auto.json`, json(current));
  assert.throws(() => verify(f), /TRANSITION_FILE_MISMATCH/);
});
