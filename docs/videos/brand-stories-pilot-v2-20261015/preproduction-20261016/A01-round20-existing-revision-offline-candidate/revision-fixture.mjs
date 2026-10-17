// A01 81 -> 82 existing-chapter revision model. This module has no CLI, host,
// provider, database, retry or production installer. Writes require an OS-Temp
// fixture marker; all successful results still hold production and paid work.
import assert from 'node:assert/strict';
import { createHash, randomUUID } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { HISTORICAL_PINS } from '../A01-host-inspect-candidate/inspect.mjs';
import { verifyProposedTransition } from '../A01-lexicon-rebaseline-candidate/rebaseline.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PACKAGE = path.resolve(HERE, '../A01-round20-i17-fact-index-candidate');
const PACKAGE_MANIFEST_SHA256 = '4d701779891e1076c3729788cc82165901d71140bfbd77c07fa9b1c060b32549';
const SLUG = 'story-rolling-suitcase-v2';
const CHAPTERS = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const HASH = /^[a-f0-9]{64}$/u;
const DOCS = `docs/videos/${SLUG}`;
const WORK = SLUG;
const EVENT_ID = `round20-existing-revision-${PACKAGE_MANIFEST_SHA256.slice(0, 16)}`;
const EVENT_DIR = `${WORK}/story/recheck-audit/${EVENT_ID}`;
const RECEIPT_DIR = `${WORK}/manual-revisions/${EVENT_ID}`;
const SOURCE_KEYS = ['auto', 'video', 'series', 'claims', 'script', 'lexicon', 'narrative', 'pilot', 'verify', 'chapters'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(`${JSON.stringify(value)}\n`, 'utf8');
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const fixed = Object.freeze({ production_status: 'HOLD',
  installation_allowed: false, paid_work_allowed: false });

export class RevisionError extends Error {
  constructor(code) { super(code); this.code = code; }
}
export class SimulatedFixtureCrash extends Error {}
const need = (yes, code) => { if (!yes) throw new RevisionError(code); };

function rootPath(root) {
  need(typeof root === 'string' && path.isAbsolute(root) && !root.startsWith('\\\\')
    && !root.startsWith('//'), 'ABSOLUTE_LOCAL_ROOT_REQUIRED');
  const resolved = path.resolve(root);
  need(fs.existsSync(resolved) && fs.lstatSync(resolved).isDirectory()
    && !fs.lstatSync(resolved).isSymbolicLink(), 'UNSAFE_LOCAL_ROOT');
  return resolved;
}

function at(root, rel) {
  need(typeof rel === 'string' && rel && !/[\\:\x00-\x1f]/u.test(rel)
    && rel.split('/').every((part) => part && part !== '.' && part !== '..'), 'UNSAFE_RELATIVE_PATH');
  let current = rootPath(root);
  for (const part of rel.split('/')) {
    current = path.join(current, part);
    if (fs.existsSync(current)) need(!fs.lstatSync(current).isSymbolicLink(), 'SYMLINK_IN_SNAPSHOT');
  }
  return current;
}
function bytes(root, rel, optional = false) {
  const file = at(root, rel);
  if (!fs.existsSync(file)) { need(optional, 'MISSING_FILE'); return null; }
  need(fs.lstatSync(file).isFile(), 'NOT_REGULAR_FILE');
  return fs.readFileSync(file);
}
function parsed(root, rel) {
  try { return JSON.parse(bytes(root, rel).toString('utf8')); }
  catch { throw new RevisionError('INVALID_JSON'); }
}
function directories(root, rel) {
  const directory = at(root, rel);
  need(fs.existsSync(directory) && fs.lstatSync(directory).isDirectory(), 'MISSING_DIRECTORY');
  const entries = fs.readdirSync(directory, { withFileTypes: true });
  need(entries.every((entry) => entry.isDirectory() && !entry.isSymbolicLink()
    && /^[A-Za-z0-9._-]+$/u.test(entry.name)), 'UNEXPECTED_DIRECTORY_ENTRY');
  return entries.map((entry) => entry.name).sort();
}
function sourceHashes(root) {
  const hash = (rel, optional = false) => {
    const value = bytes(root, rel, optional);
    return value === null ? null : sha(value);
  };
  const result = {
    auto: hash(`${WORK}/auto.json`), video: hash(`${DOCS}/video.json`),
    series: hash(`${DOCS}/series.json`), claims: hash(`${DOCS}/claims.md`),
    script: hash(`${DOCS}/script.md`), lexicon: hash('docs/videos/lexicon.json'),
    narrative: hash(`${WORK}/review/narrative.json`),
    pilot: hash(`${WORK}/story/reviews/script-review.json`, true),
    verify: hash(`${DOCS}/verify-1.md`, true),
    chapters: Object.fromEntries(CHAPTERS.map((key) => [key,
      hash(`${WORK}/story/chapters/${key}.json`)])),
  };
  need(same(Object.keys(result), SOURCE_KEYS), 'SOURCE_KEY_ORDER_DRIFT');
  return result;
}
function sourceComposite(value) { return sha(JSON.stringify(value)); }

function packageData() {
  const manifestBytes = bytes(PACKAGE, 'manifest.json');
  need(sha(manifestBytes) === PACKAGE_MANIFEST_SHA256, 'ROUND20_MANIFEST_DRIFT');
  const manifest = JSON.parse(manifestBytes);
  need(manifest.status === 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE'
    && manifest.slug === SLUG && manifest.inherited_round9_narrative_passed === false
    && manifest.authorizes_host_install_or_paid_media === false,
  'ROUND20_STATUS_DRIFT');
  const chapterBytes = Object.fromEntries(CHAPTERS.map((key) => [key,
    bytes(PACKAGE, `candidate/chapters/${key}.json`)]));
  const chapters = Object.fromEntries(CHAPTERS.map((key) => [key,
    JSON.parse(chapterBytes[key])]));
  for (const key of CHAPTERS) {
    need(sha(chapterBytes[key]) === manifest.candidate_chapter_sha256[key]
      && chapters[key].key === key && Array.isArray(chapters[key].scenes)
      && Array.isArray(chapters[key].claims), 'ROUND20_CHAPTER_DRIFT');
  }
  const seriesBytes = bytes(PACKAGE, 'candidate/series.json');
  const series = JSON.parse(seriesBytes);
  need(sha(seriesBytes) === manifest.candidate_series_sha256
    && series.plan?.id === 'A01' && series.target_minutes === 10
    && series.image_model === 'image-01' && same(series.look, { preset: 'cute-mystery' }),
  'ROUND20_SERIES_DRIFT');
  const mapBytes = bytes(PACKAGE, 'source-map.json');
  const map = JSON.parse(mapBytes);
  need(sha(mapBytes) === manifest.source_map_sha256 && map.lines?.length === 27,
    'ROUND20_SOURCE_MAP_DRIFT');
  const lineRefs = new Set();
  for (const row of map.lines) {
    const chapter = chapters[row.chapter];
    const scene = chapter?.scenes.find((item) => item.id === row.scene_id);
    const line = scene?.lines.find((item) => item.id === row.line_id);
    const ref = `${row.chapter}/${row.scene_id}/${row.line_id}`;
    need(line && !lineRefs.has(ref) && line.text === row.text
      && row.verdict === 'PENDING_INDEPENDENT_REVIEW', 'ROUND20_SOURCE_LINE_MISMATCH');
    lineRefs.add(ref);
    if (row.claim_id !== null) {
      const claim = chapter.claims.find((item) => item.id === row.claim_id);
      need(claim && claim.scene === row.scene_id && claim.claim.includes(row.text)
        && claim.source === row.source_index
        && claim.fact === (row.fact_index ?? null)
        && claim.verdict === 'PENDING', 'ROUND20_CLAIM_BINDING_MISMATCH');
    }
    if (row.source_index !== null) {
      need(series.plan.sources[row.source_index]?.url === row.source_url
        && (row.fact_index === null || row.fact_index === undefined
          || series.plan.must_verify[row.fact_index]?.sources.includes(row.source_index)),
      'ROUND20_SOURCE_BINDING_MISMATCH');
    }
  }
  const validationBytes = bytes(PACKAGE, 'validation.json');
  need(sha(validationBytes) === manifest.validation_sha256, 'ROUND20_VALIDATION_DRIFT');
  const validation = JSON.parse(validationBytes);
  const scenes = CHAPTERS.flatMap((key) => chapters[key].scenes);
  const lines = scenes.flatMap((scene) => scene.lines);
  need(scenes.length === validation.scene_count && lines.length === validation.line_count
    && scenes.length === 79 && lines.length === 108
    && validation.narration_sha256 === manifest.narration_sha256
    && validation.lint_errors.length === 0 && validation.cute_errors.length === 0,
  'ROUND20_COUNTS_OR_LINT_DRIFT');
  return { manifest, manifestBytes, chapterBytes, seriesBytes, mapBytes };
}

function revisedState(beforeBytes) {
  let before;
  try { before = JSON.parse(beforeBytes); }
  catch { throw new RevisionError('INVALID_AUTO_JSON'); }
  need(before.slug === SLUG && before.status === 'blocked'
    && before.blocked_kind === 'prompt_fixes:narrative'
    && before.verified === true && before.listener_done === true
    && before.story?.narrative?.passed === false
    && before.story?.narrative?.rounds === 9
    && same(before.story?.narrative?.failed,
      ['chapters_link', 'payoffs', 'one_thread'])
    && before.story?.narrative_fixes === 2
    && (before.story?.owner_note === null || before.story?.owner_note === undefined),
  'A01_STATE_NOT_ROUND9_HOLD');
  for (const key of CHAPTERS) need(before.story.chapters[key]?.written === true
    && before.story.chapters[key]?.checked === true
    && before.story.chapters[key]?.listened === true
    && Number.isInteger(before.story.chapters[key]?.check_rounds)
    && before.story.chapters[key].check_rounds >= 0
    && Number.isInteger(before.story.chapters[key]?.lint_fixes ?? 0)
    && (before.story.chapters[key].lint_fixes ?? 0) >= 0
    && (!before.story.chapters[key]?.lint || before.story.chapters[key].lint.length === 0),
  'A01_CHAPTER_STATE_DRIFT');
  const previousChapterCounters = Object.fromEntries(CHAPTERS.map((key) => [key, {
    check_rounds: before.story.chapters[key].check_rounds,
    lint_fixes: before.story.chapters[key].lint_fixes ?? 0,
    changed: before.story.chapters[key].changed ?? null,
  }]));
  const after = structuredClone(before);
  for (const key of CHAPTERS) {
    after.story.chapters[key].checked = false;
    after.story.chapters[key].listened = false;
    after.story.chapters[key].lint = null;
    after.story.chapters[key].check_rounds = 0;
    after.story.chapters[key].lint_fixes = 0;
    delete after.story.chapters[key].changed;
  }
  after.verified = false;
  after.listener_done = false;
  // Keep the historical counters only in the 81 snapshot, staged backup and audit plan.
  // The revised source starts a new checker/lint cycle without carrying a stale tally.
  return { before, previousChapterCounters,
    afterBytes: Buffer.from(`${JSON.stringify(after, null, 2)}\n`) };
}

function historyDigest(root, eventIds, revisionIds) {
  const rows = [];
  for (const id of eventIds) {
    const rel = `${WORK}/story/recheck-audit/${id}`;
    const names = fs.readdirSync(at(root, rel), { withFileTypes: true });
    need(names.every((entry) => entry.isFile() && !entry.isSymbolicLink()), 'UNEXPECTED_HISTORY_FILE');
    for (const entry of names.sort((a, b) => a.name.localeCompare(b.name))) {
      const file = `${rel}/${entry.name}`;
      rows.push({ path: file, sha256: sha(bytes(root, file)) });
    }
  }
  for (const id of revisionIds) {
    const rel = `${WORK}/manual-revisions/${id}`;
    const names = fs.readdirSync(at(root, rel));
    need(same(names, ['installation-receipt.json']), 'UNEXPECTED_HISTORY_REVISION');
    const file = `${rel}/installation-receipt.json`;
    rows.push({ path: file, sha256: sha(bytes(root, file)) });
  }
  return sha(JSON.stringify(rows));
}

function baseline(options) {
  const { before80Root, before81Root, oldLexiconFile,
    pins80 = HISTORICAL_PINS, expectedOldSha, expectedNewSha } = options;
  need(path.resolve(rootPath(before80Root)) !== path.resolve(rootPath(before81Root)),
    'BEFORE_SNAPSHOTS_MUST_BE_DISTINCT');
  const result = verifyProposedTransition({ beforeRoot: before80Root,
    afterRoot: before81Root, oldLexiconFile, pins: pins80,
    expectedOldSha, expectedNewSha });
  need(result.integrity === 'LOCAL_81_EVENT_TRANSITION_PASS'
    && result.new_pins.links === 81, 'UNVERIFIED_81_BASELINE');
  const current = sourceHashes(before81Root);
  need(sourceComposite(current) === result.new_pins.source_composite_sha256
    && current.pilot === null, 'BASELINE_SOURCE_OR_REVIEW_DRIFT');
  const eventIds = directories(before81Root, `${WORK}/story/recheck-audit`);
  const revisionIds = directories(before81Root, `${WORK}/manual-revisions`);
  need(eventIds.length === 81, 'BASELINE_EVENT_COUNT_DRIFT');
  const historySha = historyDigest(before81Root, eventIds, revisionIds);
  return { pins81: result.new_pins, current, eventIds, revisionIds, historySha };
}

/** Offline read-only proposal: 81st lexicon event stays intact; chapter adoption is a separate 82nd source revision. */
export function planOfflineRevision(options) {
  const base = baseline(options);
  const pkg = packageData();
  need(!base.eventIds.includes(EVENT_ID) && !base.revisionIds.includes(EVENT_ID),
    'ROUND20_REVISION_ALREADY_EXISTS');
  const state = revisedState(bytes(options.before81Root, `${WORK}/auto.json`));
  const replacements = {
    [`${WORK}/auto.json`]: state.afterBytes,
    [`${DOCS}/series.json`]: pkg.seriesBytes,
    ...Object.fromEntries(CHAPTERS.map((key) =>
      [`${WORK}/story/chapters/${key}.json`, pkg.chapterBytes[key]])),
  };
  const fileDiff = Object.fromEntries(Object.entries(replacements).map(([rel, value]) => [rel,
    { before_sha256: sha(bytes(options.before81Root, rel)), after_sha256: sha(value) }]));
  need(fileDiff[`${WORK}/auto.json`].before_sha256 !== fileDiff[`${WORK}/auto.json`].after_sha256,
    'NO_STATE_INVALIDATION');
  const after = structuredClone(base.current);
  after.auto = fileDiff[`${WORK}/auto.json`].after_sha256;
  after.series = fileDiff[`${DOCS}/series.json`].after_sha256;
  for (const key of CHAPTERS) after.chapters[key] = fileDiff[`${WORK}/story/chapters/${key}.json`].after_sha256;
  const plan = {
    schema_version: 1, kind: 'a01_round20_existing_story_revision_plan', slug: SLUG,
    event_id: EVENT_ID, revision: `manual-revisions/${EVENT_ID}`,
    round20_manifest_sha256: PACKAGE_MANIFEST_SHA256,
    round20_source_map_sha256: pkg.manifest.source_map_sha256,
    previous_81_pins: base.pins81,
    history_sha256: base.historySha,
    historical_event_ids: base.eventIds,
    historical_revision_ids: base.revisionIds,
    previous_chapter_counters: state.previousChapterCounters,
    before_source_hashes: base.current,
    after_source_hashes: after,
    after_source_composite_sha256: sourceComposite(after),
    file_diff: fileDiff,
    invalidated_checks: ['hook', 'origin', 'idea', 'engine', 'turn', 'now',
      'chapter_check_rounds', 'chapter_lint_fixes', 'chapter_changed_tallies',
      'aggregate_verified', 'aggregate_listener_done'],
    stale_generated_docs_retained_until_real_worker_relint: [
      'video.json', 'script.md', 'claims.md', 'verify-1.md'],
    prior_narrative_fail_preserved: true,
  };
  return { status: 'OFFLINE_PLAN_ONLY', plan,
    plan_sha256: sha(JSON.stringify(plan)), replacements, ...fixed };
}

function externalEvidence(plan, planSha, reviewBytes, receiptBytes) {
  need(Buffer.isBuffer(reviewBytes) && Buffer.isBuffer(receiptBytes),
    'REVIEW_AND_RECEIPT_REQUIRED');
  let review, receipt;
  try { review = JSON.parse(reviewBytes); receipt = JSON.parse(receiptBytes); }
  catch { throw new RevisionError('INVALID_EXTERNAL_EVIDENCE_JSON'); }
  need(review.schema_version === 1 && review.kind === 'a01_round20_existing_story_independent_review'
    && review.slug === SLUG && review.verdict === 'PASS' && review.independent === true
    && typeof review.reviewer === 'string' && review.reviewer.trim()
    && review.plan_sha256 === planSha
    && review.round20_manifest_sha256 === PACKAGE_MANIFEST_SHA256
    && review.before_source_sha256 === plan.previous_81_pins.source_composite_sha256
    && review.after_source_sha256 === plan.after_source_composite_sha256,
  'REVIEW_BINDING_INVALID');
  need(receipt.schema_version === 1 && receipt.kind === 'a01_round20_existing_story_revision_receipt'
    && receipt.slug === SLUG && receipt.event_id === EVENT_ID
    && receipt.plan_sha256 === planSha
    && receipt.review_sha256 === sha(reviewBytes)
    && receipt.round20_manifest_sha256 === PACKAGE_MANIFEST_SHA256
    && receipt.before_source_sha256 === plan.previous_81_pins.source_composite_sha256
    && receipt.after_source_sha256 === plan.after_source_composite_sha256
    && receipt.paid_calls === 0 && receipt.auto_retry === false
    && typeof receipt.operator === 'string' && receipt.operator.trim()
    && receipt.operator !== review.reviewer
    && typeof receipt.owner_approval_ref === 'string' && receipt.owner_approval_ref.trim(),
  'RECEIPT_BINDING_INVALID');
}

/** Exact proposed bytes. External strings do not authenticate human approval. */
export function prepareOfflineRevision(options) {
  const proposal = planOfflineRevision(options);
  const { plan, plan_sha256: planSha } = proposal;
  externalEvidence(plan, planSha, options.reviewBytes, options.receiptBytes);
  const authorBytes = json({ schema_version: 1, kind: 'a01_round20_existing_story_author_manifest',
    slug: SLUG, event_id: EVENT_ID, plan_sha256: planSha,
    previous_tip_index_sha256: plan.previous_81_pins.tip_index_sha256,
    round20_manifest_sha256: PACKAGE_MANIFEST_SHA256,
    round20_source_map_sha256: plan.round20_source_map_sha256,
    previous_chapter_counters: plan.previous_chapter_counters,
    file_diff: plan.file_diff, independent_review_sha256: sha(options.reviewBytes),
    revision_receipt_sha256: sha(options.receiptBytes) });
  const indexBytes = json({ schema_version: 1, slug: SLUG,
    result_kind: 'manual_existing_story_source_revision',
    install_receipt_sha256: plan.previous_81_pins.install_receipt_sha256,
    before_source_sha256: plan.previous_81_pins.source_composite_sha256,
    after_source_sha256: plan.after_source_composite_sha256,
    before: plan.before_source_hashes, after: plan.after_source_hashes,
    revision: plan.revision, revision_receipt_sha256: sha(options.receiptBytes),
    independent_review_sha256: sha(options.reviewBytes),
    author_manifest_sha256: sha(authorBytes) });
  const files = {
    [`${RECEIPT_DIR}/installation-receipt.json`]: options.receiptBytes,
    [`${EVENT_DIR}/independent-review.json`]: options.reviewBytes,
    [`${EVENT_DIR}/author-manifest.json`]: authorBytes,
    [`${EVENT_DIR}/index.json`]: indexBytes,
  };
  const manifest = [...plan.historical_event_ids.map((id) => ({ id,
    index_sha256: sha(bytes(options.before81Root,
      `${WORK}/story/recheck-audit/${id}/index.json`)) })),
  { id: EVENT_ID, index_sha256: sha(indexBytes) }].sort((a, b) => a.id.localeCompare(b.id));
  need(sha(JSON.stringify(manifest.filter((row) => row.id !== EVENT_ID)))
    === plan.previous_81_pins.archive_index_manifest_sha256,
  'HISTORICAL_INDEX_MANIFEST_DRIFT');
  const expectedPins = { id: `a01-${EVENT_ID}`, links: 82,
    install_receipt_sha256: plan.previous_81_pins.install_receipt_sha256,
    tip_index_sha256: sha(indexBytes),
    source_composite_sha256: plan.after_source_composite_sha256,
    archive_index_manifest_sha256: sha(JSON.stringify(manifest)) };
  return { ...proposal, files, expected_pins: expectedPins };
}

/** Compare immutable 81 and separate 82 snapshots, preserving all original audit bytes. */
export function verify82Fixture(options) {
  need(path.resolve(rootPath(options.before81Root)) !== path.resolve(rootPath(options.after82Root)),
    'BEFORE_AND_AFTER_MUST_BE_DISTINCT');
  const prepared = prepareOfflineRevision(options);
  const { plan } = prepared;
  const afterRoot = options.after82Root;
  need(same(directories(afterRoot, `${WORK}/story/recheck-audit`),
    [...plan.historical_event_ids, EVENT_ID].sort()), 'EVENT_82_COUNT_OR_ID_MISMATCH');
  need(same(directories(afterRoot, `${WORK}/manual-revisions`),
    [...plan.historical_revision_ids, EVENT_ID].sort()), 'REVISION_COUNT_OR_ID_MISMATCH');
  need(historyDigest(afterRoot, plan.historical_event_ids, plan.historical_revision_ids)
    === plan.history_sha256, 'HISTORICAL_81_BYTES_DRIFT');
  const eventNames = fs.readdirSync(at(afterRoot, EVENT_DIR)).sort();
  const receiptNames = fs.readdirSync(at(afterRoot, RECEIPT_DIR)).sort();
  need(same(eventNames, ['author-manifest.json', 'independent-review.json', 'index.json'])
    && same(receiptNames, ['installation-receipt.json']), 'UNEXPECTED_82_EVENT_FILE');
  for (const [rel, value] of Object.entries(prepared.files))
    need(bytes(afterRoot, rel).equals(value), 'PROPOSED_82_EVENT_BYTES_MISMATCH');
  for (const [rel, value] of Object.entries(prepared.replacements))
    need(bytes(afterRoot, rel).equals(value), 'ROUND20_REPLACEMENT_BYTES_MISMATCH');
  const source = sourceHashes(afterRoot);
  need(same(source, plan.after_source_hashes)
    && sourceComposite(source) === plan.after_source_composite_sha256,
  'POST_REVISION_SOURCE_DRIFT');
  const old = plan.before_source_hashes;
  for (const key of ['video', 'claims', 'script', 'lexicon', 'narrative', 'pilot', 'verify'])
    need(source[key] === old[key], 'UNEXPECTED_GENERATED_DOC_OR_REVIEW_CHANGE');
  const manifest = directories(afterRoot, `${WORK}/story/recheck-audit`).map((id) => ({ id,
    index_sha256: sha(bytes(afterRoot, `${WORK}/story/recheck-audit/${id}/index.json`)) }));
  need(sha(JSON.stringify(manifest)) === prepared.expected_pins.archive_index_manifest_sha256,
    'NEW_82_PIN_MISMATCH');
  return { schema_version: 1, integrity: 'LOCAL_82_EVENT_TRANSITION_PASS',
    slug: SLUG, new_pins: prepared.expected_pins, plan_sha256: prepared.plan_sha256,
    ...fixed };
}

function fixtureRoot(root) {
  const resolved = rootPath(root);
  const temp = fs.realpathSync(os.tmpdir());
  need(resolved.startsWith(`${temp}${path.sep}`)
    && fs.realpathSync(resolved).startsWith(`${temp}${path.sep}`),
  'OS_TEMP_FIXTURE_ONLY');
  need(same(parsed(resolved, 'A01-ROUND20-82-OFFLINE-FIXTURE.json'),
    { schema_version: 1, slug: SLUG, offline_fixture: true }),
  'FIXTURE_MARKER_REQUIRED');
  return resolved;
}
function syncDir(directory) {
  if (process.platform === 'win32') return;
  const fd = fs.openSync(directory, 'r');
  try { fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
}
function putNew(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const fd = fs.openSync(file, 'wx', 0o600);
  try { fs.writeFileSync(fd, value); fs.fsyncSync(fd); }
  finally { fs.closeSync(fd); }
  need(fs.readFileSync(file).equals(value), 'STAGED_BYTE_MISMATCH');
  syncDir(path.dirname(file));
}
function replaceExact(file, value) {
  const temp = `${file}.${process.pid}.${randomUUID()}.tmp`;
  putNew(temp, value);
  fs.renameSync(temp, file);
  syncDir(path.dirname(file));
  need(fs.readFileSync(file).equals(value), 'REPLACEMENT_READBACK_MISMATCH');
}
function safety(options, plan, live) {
  const s = options.safety;
  need(s?.schema_version === 1 && s.slug === SLUG && s.plan_sha256 === options.expectedPlanSha
    && s.worker_commit === options.expectedWorkerCommit
    && s.panel_rules_sha256 === options.expectedPanelRulesSha
    && s.checkout_clean === true && s.project_status === 'blocked'
    && s.retry_id === null && s.stage_running === 0 && s.stage_queued === 0
    && s.media_running === 0 && s.media_queued === 0 && s.paid_calls_in_flight === 0
    && s.unarchived_run_journals === 0 && s.unresolved_run_receipts === 0
    && s.media_asset_files === 0 && s.budget_limit_usd === '25.00'
    && s.budget_reserved_usd === '0.00' && s.budget_settled_usd === '0.00'
    && s.budget_operations === 0 && s.global_stop_present === true
    && s.a01_stop_present === true && s.a01_lease_present === false
    && Number.isInteger(s.observed_at_ms)
    && options.now - s.observed_at_ms >= 0 && options.now - s.observed_at_ms <= 60_000,
  'UNSAFE_FIXTURE_STATE');
  need(options.expectedPlanSha === sha(JSON.stringify(plan))
    && /^[a-f0-9]{40}$/u.test(options.expectedWorkerCommit ?? '')
    && HASH.test(options.expectedPanelRulesSha ?? ''), 'UNPINNED_FIXTURE_STATE');
  const globalStop = bytes(live, 'STOP');
  const scopedStop = bytes(live, `${WORK}/STOP`);
  need(globalStop.length > 0 && scopedStop.length > 0
    && !fs.existsSync(at(live, `${WORK}/LEASE`)), 'STOP_OR_LEASE_DRIFT');
  for (const rel of [`${WORK}/story/reviews/script-review.json`,
    `${WORK}/timeline.json`, `${WORK}/final.mp4`])
    need(!fs.existsSync(at(live, rel)), 'PAID_OR_APPROVED_ARTIFACT_ALREADY_EXISTS');
  return { global_stop_sha256: sha(globalStop), scoped_stop_sha256: sha(scopedStop),
    safety_sha256: sha(json(s)) };
}
function exactDir(root, rel, files) {
  const directory = at(root, rel);
  need(fs.existsSync(directory) && fs.lstatSync(directory).isDirectory()
    && same(fs.readdirSync(directory).sort(), Object.keys(files).sort()),
  'PUBLISHED_DIRECTORY_DRIFT');
  for (const [name, value] of Object.entries(files))
    need(bytes(root, `${rel}/${name}`).equals(value), 'PUBLISHED_FILE_DRIFT');
}
function removeExactDir(root, rel, files) {
  exactDir(root, rel, files);
  for (const name of Object.keys(files)) fs.unlinkSync(at(root, `${rel}/${name}`));
  fs.rmdirSync(at(root, rel));
  syncDir(path.dirname(at(root, rel)));
}

/** Synthetic Temp transaction. It cannot be pointed at a host or production workdir. */
export function applyOfflineFixture(options) {
  const live = fixtureRoot(options.liveRoot);
  const before81 = rootPath(options.before81Root);
  need(path.resolve(live) !== path.resolve(before81), 'BEFORE_AND_LIVE_MUST_BE_DISTINCT');
  const receiptExists = fs.existsSync(at(live, RECEIPT_DIR));
  const auditExists = fs.existsSync(at(live, EVENT_DIR));
  if (receiptExists && auditExists) {
    const checked = verify82Fixture({ ...options, after82Root: live });
    return { status: 'ALREADY_APPLIED_LOCAL_FIXTURE', inspection: checked, ...fixed };
  }
  need(!receiptExists && !auditExists, 'PARTIAL_82_EVENT_REQUIRES_MANUAL_RECOVERY');
  const prepared = prepareOfflineRevision(options);
  need(same(prepared.expected_pins, options.approvedPins82), 'APPROVED_82_PINS_MISMATCH');
  const initial = safety(options, prepared.plan, live);
  const source = sourceHashes(live);
  need(same(source, prepared.plan.before_source_hashes)
    && sourceComposite(source) === prepared.plan.previous_81_pins.source_composite_sha256,
  'LIVE_81_SOURCE_DRIFT');
  need(historyDigest(live, prepared.plan.historical_event_ids,
    prepared.plan.historical_revision_ids) === prepared.plan.history_sha256,
  'LIVE_81_HISTORY_DRIFT');
  need(same(directories(live, `${WORK}/story/recheck-audit`),
    prepared.plan.historical_event_ids), 'LIVE_81_EVENT_LIST_DRIFT');
  const txnParent = at(live, `${WORK}/story/round20-offline-transactions`);
  if (!fs.existsSync(txnParent)) { fs.mkdirSync(txnParent); syncDir(path.dirname(txnParent)); }
  need(fs.lstatSync(txnParent).isDirectory() && !fs.lstatSync(txnParent).isSymbolicLink(),
    'UNSAFE_TRANSACTION_PARENT');
  const txn = path.join(txnParent, EVENT_ID);
  need(!fs.existsSync(txn), 'PENDING_TRANSACTION_REQUIRES_MANUAL_RECOVERY');
  fs.mkdirSync(txn); syncDir(txnParent);
  putNew(path.join(txn, 'intent.json'), json({ schema_version: 1,
    kind: 'a01_round20_existing_revision_offline_intent', event_id: EVENT_ID,
    plan_sha256: prepared.plan_sha256, approved_pins: prepared.expected_pins,
    safety_sha256: initial.safety_sha256, file_diff: prepared.plan.file_diff }));
  const receiptFiles = { 'installation-receipt.json': prepared.files[
    `${RECEIPT_DIR}/installation-receipt.json`] };
  const eventFiles = Object.fromEntries(Object.entries(prepared.files)
    .filter(([rel]) => rel.startsWith(`${EVENT_DIR}/`))
    .map(([rel, value]) => [rel.slice(EVENT_DIR.length + 1), value]));
  for (const [group, files] of [['receipt', receiptFiles], ['audit', eventFiles]]) {
    const dir = path.join(txn, group);
    fs.mkdirSync(dir); syncDir(txn);
    for (const [name, value] of Object.entries(files)) putNew(path.join(dir, name), value);
  }
  // Crash recovery needs the exact original bytes, not a reconstructed version
  // of a file whose write may have been interrupted. This is still fixture-only.
  for (const [rel, hashes] of Object.entries(prepared.plan.file_diff)) {
    const original = bytes(before81, rel);
    need(sha(original) === hashes.before_sha256, 'BACKUP_SOURCE_DRIFT');
    putNew(path.join(txn, 'before', ...rel.split('/')), original);
  }
  const touched = [];
  let publishedReceipt = false, publishedAudit = false;
  const fault = options.fault ?? (() => {});
  try {
    fault('after-stage');
    const fresh = prepareOfflineRevision(options);
    need(fresh.plan_sha256 === prepared.plan_sha256
      && same(fresh.expected_pins, prepared.expected_pins), 'PRECOMMIT_PLAN_DRIFT');
    need(same(safety(options, fresh.plan, live), initial), 'PRECOMMIT_SAFETY_DRIFT');
    need(same(sourceHashes(live), prepared.plan.before_source_hashes)
      && historyDigest(live, prepared.plan.historical_event_ids,
        prepared.plan.historical_revision_ids) === prepared.plan.history_sha256,
    'PRECOMMIT_SOURCE_OR_HISTORY_DRIFT');
    for (const [rel, value] of Object.entries(prepared.replacements)) {
      if (sha(bytes(live, rel)) === sha(value)) continue;
      replaceExact(at(live, rel), value);
      touched.push(rel);
      fault(`after-source:${rel}`);
    }
    fault('after-source');
    fs.renameSync(path.join(txn, 'receipt'), at(live, RECEIPT_DIR));
    publishedReceipt = true; syncDir(path.dirname(at(live, RECEIPT_DIR)));
    fault('after-receipt-publish');
    fs.renameSync(path.join(txn, 'audit'), at(live, EVENT_DIR));
    publishedAudit = true; syncDir(path.dirname(at(live, EVENT_DIR)));
    fault('after-audit-publish');
    const inspection = verify82Fixture({ ...options, after82Root: live });
    exactDir(live, RECEIPT_DIR, receiptFiles);
    exactDir(live, EVENT_DIR, eventFiles);
    need(same(safety(options, prepared.plan, live), initial), 'POSTCOMMIT_SAFETY_DRIFT');
    putNew(path.join(txn, 'readback.json'), json({ status: 'LOCAL_FIXTURE_APPENDED',
      new_pins: inspection.new_pins, installation_allowed: false,
      paid_work_allowed: false }));
    return { status: 'LOCAL_FIXTURE_APPENDED', inspection, ...fixed };
  } catch (error) {
    if (error instanceof SimulatedFixtureCrash) throw error;
    let rollbackError = null;
    try {
      if (publishedAudit) removeExactDir(live, EVENT_DIR, eventFiles);
      if (publishedReceipt) removeExactDir(live, RECEIPT_DIR, receiptFiles);
      for (const rel of touched.reverse()) {
        const currentSha = sha(bytes(live, rel));
        const expected = prepared.plan.file_diff[rel];
        need(currentSha === expected.after_sha256 || currentSha === expected.before_sha256,
          'CONCURRENT_SOURCE_EDIT_PREVENTS_ROLLBACK');
        replaceExact(at(live, rel), bytes(before81, rel));
      }
      need(same(sourceHashes(live), prepared.plan.before_source_hashes)
        && historyDigest(live, prepared.plan.historical_event_ids,
          prepared.plan.historical_revision_ids) === prepared.plan.history_sha256,
      'ROLLBACK_INCOMPLETE');
      putNew(path.join(txn, 'rollback.json'), json({ status: 'ROLLED_BACK_LOCAL_FIXTURE',
        reason: error.code ?? error.message, installation_allowed: false,
        paid_work_allowed: false }));
    } catch (failure) { rollbackError = failure; }
    if (rollbackError) throw new AggregateError([error, rollbackError],
      'MANUAL_RECOVERY_REQUIRED: fixture transaction retained');
    throw error;
  }
}

export const OFFLINE_PINS = Object.freeze({ slug: SLUG, round20_manifest_sha256: PACKAGE_MANIFEST_SHA256,
  event_id: EVENT_ID, event_dir: EVENT_DIR, receipt_dir: RECEIPT_DIR });
