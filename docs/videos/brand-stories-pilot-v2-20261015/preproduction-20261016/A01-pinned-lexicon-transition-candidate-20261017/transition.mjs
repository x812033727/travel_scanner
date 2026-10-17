#!/usr/bin/env node
// LOCAL planning/readback only. No installer, host, model, database or retry command.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readFileSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { proposeRebaseline } from './supported-baseline.mjs';
import { planInitialStoryLexicon, readStoryLexicon } from './snapshot-format.mjs';

const SLUG = 'story-rolling-suitcase-v2';
const KIND = 'a01_pinned_historical_lexicon_20261017';
const CHAPTERS = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = value => createHash('sha256').update(value).digest('hex');
const json = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const digestObject = value => sha(JSON.stringify(value));
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const need = (ok, code) => { if (!ok) { const error = new Error(code); error.code = code; throw error; } };

function at(root, rel) {
  need(path.isAbsolute(root) && !root.startsWith('\\\\') && !root.startsWith('//'), 'LOCAL_ROOT_REQUIRED');
  need(rel && !/[\\:\x00-\x1f]/u.test(rel) && rel.split('/').every(p => p && p !== '.' && p !== '..'), 'LOCAL_PATH_INVALID');
  let current = path.resolve(root);
  need(lstatSync(current).isDirectory() && !lstatSync(current).isSymbolicLink(), 'LOCAL_ROOT_UNSAFE');
  for (const part of rel.split('/')) {
    current = path.join(current, part);
    need(!lstatSync(current).isSymbolicLink(), 'LOCAL_SYMLINK_REFUSED');
  }
  return current;
}
const bytesAt = (root, rel) => readFileSync(at(root, rel));
const hashAt = (root, rel) => sha(bytesAt(root, rel));
const parse = bytes => JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/, ''));
const dirs = (root, rel) => {
  const entries = readdirSync(at(root, rel), { withFileTypes: true });
  need(entries.every(e => e.isDirectory() && !e.isSymbolicLink()), 'UNEXPECTED_DIRECTORY_ENTRY');
  return entries.map(e => e.name).sort();
};

function history(root, baseline) {
  const rows = [];
  for (const id of baseline.historical_event_ids) {
    const base = `${SLUG}/story/recheck-audit/${id}`;
    const files = readdirSync(at(root, base), { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
    need(files.every(file => file.isFile() && !file.isSymbolicLink()), 'AUDIT_FILE_UNSAFE');
    for (const file of files) rows.push({ path: `${base}/${file.name}`, sha256: hashAt(root, `${base}/${file.name}`) });
  }
  for (const id of baseline.historical_revision_ids) {
    const rel = `${SLUG}/manual-revisions/${id}/installation-receipt.json`;
    rows.push({ path: rel, sha256: hashAt(root, rel) });
  }
  need(digestObject(rows) === baseline.historical_files_sha256, 'HISTORICAL_FILES_MISMATCH');
  return rows;
}

/** Preserve the old reviewed pronunciation bytes, rather than adopt unrelated shared additions. */
export function planPinnedTransition(options) {
  const { plan: baseline, plan_sha256: baselineSha } = proposeRebaseline(options);
  const root = options.snapshotRoot;
  const autoRel = `${SLUG}/auto.json`;
  const originalAuto = parse(bytesAt(root, autoRel));
  need(originalAuto?.story && typeof originalAuto.story === 'object' && !Array.isArray(originalAuto.story), 'STORY_STATE_REQUIRED');
  need(!Object.hasOwn(originalAuto.story, 'lexicon_sha256') && !Object.hasOwn(originalAuto.story, 'lexicon_head_event_sha256'), 'STATE_ALREADY_PINNED');
  need(!existsSync(path.join(root, 'docs', 'videos', SLUG, 'story-lexicon')), 'SNAPSHOT_ALREADY_PRESENT');
  const snapshot = planInitialStoryLexicon({ slug: SLUG, sharedBytes: readFileSync(options.oldLexiconFile) });
  need(snapshot.lexicon_sha256 === baseline.old_lexicon_sha256, 'HISTORICAL_LEXICON_PIN_MISMATCH');
  const nextAuto = structuredClone(originalAuto);
  nextAuto.story.lexicon_sha256 = snapshot.lexicon_sha256;
  nextAuto.story.lexicon_head_event_sha256 = snapshot.head_event_sha256;
  const restored = structuredClone(nextAuto);
  delete restored.story.lexicon_sha256;
  delete restored.story.lexicon_head_event_sha256;
  need(same(restored, originalAuto), 'STATE_CHANGED_BEYOND_BINDING');
  const files = Object.fromEntries(snapshot.files.map(file => [`docs/videos/${SLUG}/story-lexicon/${file.relative.split(path.sep).join('/')}`, file.bytes]));
  files[autoRel] = json(nextAuto);
  const after = { ...baseline.before_source_hashes, auto: sha(files[autoRel]), lexicon: snapshot.lexicon_sha256 };
  const afterSha = digestObject(after);
  // Source equality is the old audit's edge relation. A metadata change must make a new edge.
  for (const id of baseline.historical_event_ids) {
    const index = parse(bytesAt(root, `${SLUG}/story/recheck-audit/${id}/index.json`));
    need(afterSha !== index.before_source_sha256 && afterSha !== index.after_source_sha256, 'TRANSITION_SOURCE_COLLISION');
  }
  const eventId = `lexicon-pin-${snapshot.lexicon_sha256.slice(0, 16)}`;
  need(!baseline.historical_event_ids.includes(eventId) && !baseline.historical_revision_ids.includes(eventId), 'DUPLICATE_TRANSITION');
  const plan = {
    schema_version: 1, kind: KIND, slug: SLUG, baseline_plan_sha256: baselineSha,
    baseline_pins: baseline.old_pinset, event_id: eventId, revision: `manual-revisions/${eventId}`,
    before_source_hashes: baseline.before_source_hashes, after_source_hashes: after,
    before_source_sha256: baseline.old_pinset.source_composite_sha256, after_source_sha256: afterSha,
    historical_files: history(root, baseline), historical_event_ids: baseline.historical_event_ids,
    historical_revision_ids: baseline.historical_revision_ids,
    observed_shared_lexicon_sha256: baseline.new_lexicon_sha256,
    pinned_lexicon_sha256: snapshot.lexicon_sha256, pinned_head_event_sha256: snapshot.head_event_sha256,
    snapshot_sequence: snapshot.sequence, unchanged_spoken_lexicon: true,
    state_changed_fields: ['story.lexicon_sha256', 'story.lexicon_head_event_sha256'],
    output_sha256: Object.fromEntries(Object.entries(files).map(([file, bytes]) => [file, sha(bytes)])),
    independent_delta: baseline.delta, narration: baseline.narration,
  };
  return { plan, plan_sha256: digestObject(plan), files,
    production_status: 'HOLD', installation_allowed: false, paid_work_allowed: false };
}

/** External evidence is data, not authentication. A caller must separately verify real authority. */
export function preparePinnedEvent({ reviewBytes, receiptBytes, ...options }) {
  const proposed = planPinnedTransition(options);
  const { plan, plan_sha256: planSha } = proposed;
  need(Buffer.isBuffer(reviewBytes) && Buffer.isBuffer(receiptBytes), 'INDEPENDENT_REVIEW_AND_OWNER_RECEIPT_REQUIRED');
  const review = parse(reviewBytes), receipt = parse(receiptBytes);
  const common = value => value.schema_version === 1 && value.slug === SLUG && value.plan_sha256 === planSha
    && value.pinned_lexicon_sha256 === plan.pinned_lexicon_sha256
    && value.pinned_head_event_sha256 === plan.pinned_head_event_sha256
    && value.before_source_sha256 === plan.before_source_sha256 && value.after_source_sha256 === plan.after_source_sha256;
  need(common(review) && review.kind === `${KIND}_review` && review.verdict === 'PASS' && review.independent === true
    && typeof review.reviewer === 'string' && review.reviewer.trim(), 'INDEPENDENT_REVIEW_INVALID');
  need(common(receipt) && receipt.kind === `${KIND}_receipt` && receipt.review_sha256 === sha(reviewBytes)
    && typeof receipt.operator === 'string' && receipt.operator.trim() && receipt.operator !== review.reviewer
    && typeof receipt.owner_approval_ref === 'string' && receipt.owner_approval_ref.trim()
    && receipt.paid_calls === 0 && receipt.shared_lexicon_writes === 0, 'OWNER_RECORD_RECEIPT_INVALID');
  const eventPath = `${SLUG}/story/recheck-audit/${plan.event_id}`;
  const manifestBytes = json(plan);
  const index = {
    schema_version: 1, slug: SLUG, result_kind: 'pinned_historical_lexicon',
    install_receipt_sha256: plan.baseline_pins.install_receipt_sha256,
    before: plan.before_source_hashes, after: plan.after_source_hashes,
    before_source_sha256: plan.before_source_sha256, after_source_sha256: plan.after_source_sha256,
    journals: [], revision: plan.revision, revision_receipt_sha256: sha(receiptBytes),
    independent_review_sha256: sha(reviewBytes), author_manifest_sha256: sha(manifestBytes),
    lexicon_binding: { lexicon_sha256: plan.pinned_lexicon_sha256, head_event_sha256: plan.pinned_head_event_sha256, sequence: 1 },
  };
  return { ...proposed, event_path: eventPath, files: { ...proposed.files,
    [`${eventPath}/index.json`]: json(index), [`${eventPath}/independent-review.json`]: reviewBytes,
    [`${eventPath}/author-manifest.json`]: manifestBytes,
    [`${SLUG}/${plan.revision}/installation-receipt.json`]: receiptBytes } };
}

function fileTree(root, rel) {
  const rows = [];
  for (const item of readdirSync(at(root, rel), { withFileTypes: true })) {
    need(!item.isSymbolicLink(), 'LOCAL_SYMLINK_REFUSED');
    if (item.isDirectory()) rows.push(...fileTree(root, `${rel}/${item.name}`));
    else { need(item.isFile(), 'UNSAFE_FILE_TYPE'); rows.push(`${rel}/${item.name}`); }
  }
  return rows.sort();
}

export function verifyPinnedTransition({ beforeRoot, afterRoot, ...options }) {
  const baseOptions = { ...options, snapshotRoot: beforeRoot };
  const proposed = planPinnedTransition(baseOptions);
  const eventPath = `${SLUG}/story/recheck-audit/${proposed.plan.event_id}`;
  const prepared = preparePinnedEvent({ ...baseOptions,
    reviewBytes: bytesAt(afterRoot, `${eventPath}/independent-review.json`),
    receiptBytes: bytesAt(afterRoot, `${SLUG}/${proposed.plan.revision}/installation-receipt.json`) });
  for (const [rel, bytes] of Object.entries(prepared.files)) need(bytesAt(afterRoot, rel).equals(bytes), `TRANSITION_FILE_MISMATCH:${rel}`);
  for (const file of proposed.plan.historical_files) need(hashAt(afterRoot, file.path) === file.sha256, 'HISTORICAL_BYTES_CHANGED');
  need(same(dirs(afterRoot, `${SLUG}/story/recheck-audit`), [...proposed.plan.historical_event_ids, proposed.plan.event_id].sort()), 'AUDIT_ENTRY_SET_CHANGED');
  need(same(dirs(afterRoot, `${SLUG}/manual-revisions`), [...proposed.plan.historical_revision_ids, proposed.plan.event_id].sort()), 'REVISION_ENTRY_SET_CHANGED');
  const evidenceBases = [`${SLUG}/story/recheck-audit/`, `${SLUG}/manual-revisions/`];
  const expectedEvidence = [...proposed.plan.historical_files.map(file => file.path),
    ...Object.keys(prepared.files).filter(file => evidenceBases.some(base => file.startsWith(base)))].sort();
  const actualEvidence = evidenceBases.flatMap(base => fileTree(afterRoot, base.slice(0, -1))).sort();
  need(same(actualEvidence, expectedEvidence), 'HISTORICAL_FILE_SET_CHANGED');
  const snapshotBase = `docs/videos/${SLUG}/story-lexicon`;
  need(same(fileTree(afterRoot, snapshotBase), Object.keys(proposed.files).filter(file => file.startsWith(`${snapshotBase}/`)).sort()), 'SNAPSHOT_FILE_SET_CHANGED');
  need(hashAt(afterRoot, 'docs/videos/lexicon.json') === proposed.plan.observed_shared_lexicon_sha256, 'SHARED_LEXICON_CHANGED_DURING_TRANSITION');
  const snapshot = readStoryLexicon({ slug: SLUG, storyDir: at(afterRoot, `docs/videos/${SLUG}`), sharedFile: at(afterRoot, 'docs/videos/lexicon.json') });
  need(snapshot.mode === 'snapshot' && snapshot.lexicon_sha256 === proposed.plan.pinned_lexicon_sha256
    && snapshot.head_event_sha256 === proposed.plan.pinned_head_event_sha256, 'PINNED_RUNTIME_READBACK_FAILED');
  // Every ordinary source byte remains the 80th tip's; only auto metadata and source selection change.
  const docs = `docs/videos/${SLUG}`;
  const optionalHash = rel => existsSync(path.join(afterRoot, ...rel.split('/'))) ? hashAt(afterRoot, rel) : null;
  const map = { auto: hashAt(afterRoot, `${SLUG}/auto.json`), video: hashAt(afterRoot, `${docs}/video.json`),
    series: hashAt(afterRoot, `${docs}/series.json`), claims: hashAt(afterRoot, `${docs}/claims.md`),
    script: hashAt(afterRoot, `${docs}/script.md`), lexicon: snapshot.lexicon_sha256,
    narrative: hashAt(afterRoot, `${SLUG}/review/narrative.json`),
    pilot: optionalHash(`${SLUG}/story/reviews/script-review.json`),
    verify: optionalHash(`${docs}/verify-1.md`),
    chapters: Object.fromEntries(CHAPTERS.map(key => [key, hashAt(afterRoot, `${SLUG}/story/chapters/${key}.json`)])) };
  need(same(map, proposed.plan.after_source_hashes) && digestObject(map) === proposed.plan.after_source_sha256, 'PINNED_SOURCE_READBACK_FAILED');
  return { integrity: 'LOCAL_PINNED_81_EVENT_TRANSITION_PASS', links: 81,
    historical_files_unchanged: proposed.plan.historical_files.length,
    lexicon_sha256: snapshot.lexicon_sha256, head_event_sha256: snapshot.head_event_sha256,
    source_sha256: digestObject(map), installation_allowed: false, paid_work_allowed: false, production_status: 'HOLD' };
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const args = process.argv.slice(2);
  assert(args.length === 4 && args[0] === '--snapshot' && args[2] === '--old-lexicon', 'only --snapshot <local> --old-lexicon <local>');
  const { files, ...report } = planPinnedTransition({ snapshotRoot: path.resolve(args[1]), oldLexiconFile: path.resolve(args[3]) });
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
}
