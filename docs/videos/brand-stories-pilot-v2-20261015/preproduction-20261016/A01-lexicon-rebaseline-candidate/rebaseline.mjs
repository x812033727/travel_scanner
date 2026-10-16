#!/usr/bin/env node
// Offline proposal and transition verifier. It never connects to or writes a host.
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readFileSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { HISTORICAL_PINS, inspectSnapshot } from '../A01-host-inspect-candidate/inspect.mjs';

const SLUG = 'story-rolling-suitcase-v2';
const CHAPTERS = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const SOURCE_KEYS = ['auto', 'video', 'series', 'claims', 'script', 'lexicon', 'narrative', 'pilot', 'verify', 'chapters'];
const OLD_LEXICON_SHA256 = 'ebfa590a69b4328ed9bc0141832bb73d27cba51963fca78778258d404c3bc4c9';
const NEW_LEXICON_SHA256 = '835e09df378d0c1b542b89c3fc44b2583b201217679267bce1146c638187d9c1';
const HASH = /^[a-f0-9]{64}$/u;
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

class RebaselineError extends Error {
  constructor(code) { super(code); this.code = code; }
}
const need = (condition, code) => { if (!condition) throw new RebaselineError(code); };
const compact = (value) => `${JSON.stringify(value)}\n`;

function localRoot(root) {
  need(typeof root === 'string' && path.isAbsolute(root) && !root.startsWith('\\\\') && !root.startsWith('//'), 'ABSOLUTE_LOCAL_ROOT_REQUIRED');
  const resolved = path.resolve(root);
  need(existsSync(resolved) && lstatSync(resolved).isDirectory() && !lstatSync(resolved).isSymbolicLink(), 'INVALID_LOCAL_ROOT');
  return resolved;
}

function localFile(root, rel, optional = false) {
  need(typeof rel === 'string' && rel && !/[\\:\x00-\x1f]/u.test(rel)
    && rel.split('/').every((part) => part && part !== '.' && part !== '..'), 'INVALID_RELATIVE_PATH');
  let current = localRoot(root);
  for (const [index, part] of rel.split('/').entries()) {
    current = path.join(current, part);
    if (!existsSync(current)) {
      need(optional, 'MISSING_FILE');
      return null;
    }
    const stat = lstatSync(current);
    need(!stat.isSymbolicLink(), 'SYMLINK_IN_SNAPSHOT');
    need(index === rel.split('/').length - 1 ? stat.isFile() : stat.isDirectory(), 'INVALID_FILE_TYPE');
  }
  return current;
}

function bytesAt(root, rel, optional = false) {
  const file = localFile(root, rel, optional);
  return file === null ? null : readFileSync(file);
}

function fileAtAbsolute(file) {
  need(typeof file === 'string' && path.isAbsolute(file) && !file.startsWith('\\\\') && !file.startsWith('//'), 'ABSOLUTE_LOCAL_FILE_REQUIRED');
  need(existsSync(file) && lstatSync(file).isFile() && !lstatSync(file).isSymbolicLink(), 'INVALID_LOCAL_FILE');
  return readFileSync(file);
}

function parseJson(bytes, code = 'INVALID_JSON') {
  try { return JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/u, '')); }
  catch { throw new RebaselineError(code); }
}

function listDirs(root, rel) {
  const dir = path.join(localRoot(root), ...rel.split('/'));
  need(existsSync(dir) && lstatSync(dir).isDirectory() && !lstatSync(dir).isSymbolicLink(), 'MISSING_DIRECTORY');
  const entries = readdirSync(dir, { withFileTypes: true });
  need(entries.every((entry) => entry.isDirectory() && !entry.isSymbolicLink()
    && /^[A-Za-z0-9._-]+$/u.test(entry.name)), 'UNEXPECTED_DIRECTORY_ENTRY');
  return entries.map((entry) => entry.name).sort();
}

function sourceHashes(root) {
  const docs = `docs/videos/${SLUG}`;
  const hash = (rel, optional = false) => {
    const bytes = bytesAt(root, rel, optional);
    return bytes === null ? null : sha(bytes);
  };
  return {
    auto: hash(`${SLUG}/auto.json`), video: hash(`${docs}/video.json`),
    series: hash(`${docs}/series.json`), claims: hash(`${docs}/claims.md`),
    script: hash(`${docs}/script.md`), lexicon: hash('docs/videos/lexicon.json'),
    narrative: hash(`${SLUG}/review/narrative.json`),
    pilot: hash(`${SLUG}/story/reviews/script-review.json`, true),
    verify: hash(`${docs}/verify-1.md`, true),
    chapters: Object.fromEntries(CHAPTERS.map((key) => [key, hash(`${SLUG}/story/chapters/${key}.json`)])),
  };
}

function historicalFiles(root, eventIds, excludedRevision = null) {
  const rows = [];
  for (const id of eventIds) {
    const dir = `${SLUG}/story/recheck-audit/${id}`;
    const full = path.join(localRoot(root), ...dir.split('/'));
    const entries = readdirSync(full, { withFileTypes: true });
    need(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()), 'UNEXPECTED_AUDIT_ENTRY');
    for (const entry of entries.sort((a, b) => a.name.localeCompare(b.name))) {
      const rel = `${dir}/${entry.name}`;
      rows.push({ path: rel, sha256: sha(bytesAt(root, rel)) });
    }
  }
  const base = `${SLUG}/manual-revisions`;
  const revisionIds = listDirs(root, base).filter((id) => id !== excludedRevision);
  for (const id of revisionIds) {
    const revisionDir = path.join(localRoot(root), ...`${base}/${id}`.split('/'));
    const entries = readdirSync(revisionDir, { withFileTypes: true });
    need(entries.length === 1 && entries[0].name === 'installation-receipt.json'
      && entries[0].isFile() && !entries[0].isSymbolicLink(), 'UNEXPECTED_HISTORICAL_REVISION_FILE');
    const rel = `${base}/${id}/installation-receipt.json`;
    rows.push({ path: rel, sha256: sha(bytesAt(root, rel)) });
  }
  return { rows, revisionIds, sha256: sha(JSON.stringify(rows)) };
}

function indexManifest(root, eventIds) {
  return eventIds.map((id) => ({ id,
    index_sha256: sha(bytesAt(root, `${SLUG}/story/recheck-audit/${id}/index.json`)) }));
}

function lexiconDelta(oldBytes, newBytes) {
  const oldLexicon = parseJson(oldBytes, 'INVALID_OLD_LEXICON');
  const newLexicon = parseJson(newBytes, 'INVALID_NEW_LEXICON');
  need(oldLexicon?.schema_version === 1 && newLexicon?.schema_version === 1
    && oldLexicon.terms && newLexicon.terms && typeof oldLexicon.terms === 'object'
    && typeof newLexicon.terms === 'object' && !Array.isArray(oldLexicon.terms)
    && !Array.isArray(newLexicon.terms), 'INVALID_LEXICON_SHAPE');
  need(same(Object.keys(oldLexicon).sort(), ['schema_version', 'terms'].sort())
    && same(Object.keys(oldLexicon).sort(), Object.keys(newLexicon).sort()), 'LEXICON_TOP_LEVEL_DRIFT');
  const oldTerms = oldLexicon.terms, newTerms = newLexicon.terms;
  need(!Object.hasOwn(oldTerms, 'pull') && !Object.hasOwn(oldTerms, 'request')
    && Object.hasOwn(newTerms, 'pull') && Object.hasOwn(newTerms, 'request')
    && newTerms.pull === null && newTerms.request === null, 'LEXICON_DELTA_NOT_ALLOWED');
  need(Object.keys(newTerms).length === Object.keys(oldTerms).length + 2
    && Object.entries(oldTerms).every(([key, value]) => Object.hasOwn(newTerms, key) && same(value, newTerms[key])), 'LEXICON_DELTA_NOT_ALLOWED');
  return { old_term_count: Object.keys(oldTerms).length, new_term_count: Object.keys(newTerms).length,
    additions: { pull: null, request: null } };
}

function assertNoNarrationUsage(root) {
  const hits = [];
  const term = /(?<![\p{L}\p{N}])(?:pull|request)(?![\p{L}\p{N}])/iu;
  const sources = [
    ...CHAPTERS.map((key) => ({ label: `chapter/${key}`,
      rel: `${SLUG}/story/chapters/${key}.json` })),
    { label: 'video', rel: `docs/videos/${SLUG}/video.json` },
  ];
  for (const { label, rel } of sources) {
    const doc = parseJson(bytesAt(root, rel), 'INVALID_NARRATION_JSON');
    need(Array.isArray(doc?.scenes), 'INVALID_NARRATION_SCENES');
    for (const scene of doc.scenes) {
      need(Array.isArray(scene.lines), 'INVALID_NARRATION_LINES');
      for (const line of scene.lines) {
        // Match the TTS path in tools/video/core/schema.mjs: spokenText(line).
        need(typeof line.text === 'string' && (line.say == null || typeof line.say === 'string'),
          'INVALID_NARRATION_LINES');
        if (term.test(line.say ?? line.text)) hits.push(`${label}/${scene.id}/${line.id}`);
      }
    }
  }
  need(hits.length === 0, 'NEW_LEXICON_TERM_IN_NARRATION');
}

function validatedBaseline({ snapshotRoot, oldLexiconFile, pins, expectedOldSha, expectedNewSha }) {
  const inspected = inspectSnapshot({ snapshotRoot, pins });
  need(same(inspected.errors.map((error) => error.code), ['SOURCE_DRIFT_FROM_TIP']),
    `BASELINE_${inspected.errors[0]?.code ?? 'UNEXPECTED_RESULT'}`);
  need(inspected.chain.observed_links === 80 && inspected.chain.expected_links === 80
    && inspected.chain.archive_index_manifest_sha256 === pins.archive_index_manifest_sha256
    && inspected.chain.tip_index_sha256 === pins.tip_index_sha256
    && inspected.chain.tip_source_composite_sha256 === pins.source_composite_sha256,
  'HISTORICAL_PIN_MISMATCH');
  const before = inspected.chain.tip_after_hashes;
  const after = inspected.source.hashes;
  need(same(Object.keys(before), SOURCE_KEYS) && same(Object.keys(after), SOURCE_KEYS)
    && Object.keys(before).every((key) => key === 'lexicon' || same(before[key], after[key])),
  'OTHER_SOURCE_DRIFT');
  need(before.lexicon === expectedOldSha && after.lexicon === expectedNewSha
    && sha(fileAtAbsolute(oldLexiconFile)) === expectedOldSha, 'LEXICON_HASH_MISMATCH');
  const delta = lexiconDelta(fileAtAbsolute(oldLexiconFile), bytesAt(snapshotRoot, 'docs/videos/lexicon.json'));
  assertNoNarrationUsage(snapshotRoot);
  const eventIds = listDirs(snapshotRoot, `${SLUG}/story/recheck-audit`);
  need(eventIds.length === 80, 'BASELINE_LINK_COUNT_MISMATCH');
  const manifest = indexManifest(snapshotRoot, eventIds);
  need(sha(JSON.stringify(manifest)) === pins.archive_index_manifest_sha256, 'HISTORICAL_MANIFEST_MISMATCH');
  return { before, after, delta, eventIds, manifest,
    historicalFiles: historicalFiles(snapshotRoot, eventIds) };
}

/** Read-only plan. CLI uses immutable historical pins and exact 2026-10-16 lexicon hashes. */
export function proposeRebaseline({ snapshotRoot, oldLexiconFile,
  pins = HISTORICAL_PINS, expectedOldSha = OLD_LEXICON_SHA256,
  expectedNewSha = NEW_LEXICON_SHA256 } = {}) {
  const baseline = validatedBaseline({ snapshotRoot, oldLexiconFile, pins, expectedOldSha, expectedNewSha });
  const eventId = `lexicon-rebaseline-${expectedNewSha.slice(0, 16)}`;
  const revisionId = eventId;
  need(!baseline.eventIds.includes(eventId)
    && !baseline.historicalFiles.revisionIds.includes(revisionId), 'DUPLICATE_REBASELINE_EVENT');
  const plan = {
    schema_version: 1, kind: 'a01_lexicon_rebaseline_plan', slug: SLUG,
    event_id: eventId, revision: `manual-revisions/${revisionId}`,
    old_pinset: { links: pins.links, install_receipt_sha256: pins.install_receipt_sha256,
      tip_index_sha256: pins.tip_index_sha256,
      source_composite_sha256: pins.source_composite_sha256,
      archive_index_manifest_sha256: pins.archive_index_manifest_sha256 },
    old_lexicon_sha256: expectedOldSha, new_lexicon_sha256: expectedNewSha,
    before_source_hashes: baseline.before, after_source_hashes: baseline.after,
    after_source_composite_sha256: sha(JSON.stringify(baseline.after)),
    historical_files_sha256: baseline.historicalFiles.sha256,
    historical_revision_ids: baseline.historicalFiles.revisionIds,
    historical_event_ids: baseline.eventIds,
    delta: baseline.delta, narration_term_hits: 0,
  };
  return { plan, plan_sha256: sha(JSON.stringify(plan)), production_status: 'HOLD',
    installation_allowed: false, paid_work_allowed: false };
}

function reviewedEvidence(plan, planSha, reviewBytes, receiptBytes) {
  need(Buffer.isBuffer(reviewBytes) && Buffer.isBuffer(receiptBytes), 'REVIEW_AND_RECEIPT_BYTES_REQUIRED');
  const review = parseJson(reviewBytes, 'INVALID_REVIEW_JSON');
  const receipt = parseJson(receiptBytes, 'INVALID_RECEIPT_JSON');
  need(review?.schema_version === 1 && review.kind === 'a01_lexicon_rebaseline_independent_review'
    && review.slug === SLUG && review.verdict === 'PASS' && review.independent === true
    && typeof review.reviewer === 'string' && review.reviewer.trim().length > 0
    && review.plan_sha256 === planSha && review.old_lexicon_sha256 === plan.old_lexicon_sha256
    && review.new_lexicon_sha256 === plan.new_lexicon_sha256
    && review.before_source_sha256 === plan.old_pinset.source_composite_sha256
    && review.after_source_sha256 === plan.after_source_composite_sha256
    && same(review.delta, plan.delta), 'REVIEW_BINDING_INVALID');
  need(receipt?.schema_version === 1 && receipt.kind === 'a01_lexicon_rebaseline_record_receipt'
    && receipt.slug === SLUG && receipt.plan_sha256 === planSha
    && receipt.event_id === plan.event_id && receipt.revision === plan.revision
    && receipt.old_lexicon_sha256 === plan.old_lexicon_sha256
    && receipt.new_lexicon_sha256 === plan.new_lexicon_sha256
    && receipt.before_source_sha256 === plan.old_pinset.source_composite_sha256
    && receipt.after_source_sha256 === plan.after_source_composite_sha256
    && receipt.review_sha256 === sha(reviewBytes) && receipt.record_only === true
    && receipt.lexicon_file_writes === 0 && typeof receipt.operator === 'string'
    && receipt.operator.trim().length > 0 && receipt.operator !== review.reviewer
    && typeof receipt.owner_approval_ref === 'string' && receipt.owner_approval_ref.trim().length > 0,
  'RECEIPT_BINDING_INVALID');
  return { review, receipt };
}

/** Returns exact proposed bytes, never writes them. The review/receipt are external inputs. */
export function prepareProposedEvent({ snapshotRoot, oldLexiconFile, reviewBytes, receiptBytes,
  pins = HISTORICAL_PINS, expectedOldSha = OLD_LEXICON_SHA256,
  expectedNewSha = NEW_LEXICON_SHA256 } = {}) {
  const candidate = proposeRebaseline({ snapshotRoot, oldLexiconFile, pins, expectedOldSha, expectedNewSha });
  const { plan, plan_sha256: planSha } = candidate;
  reviewedEvidence(plan, planSha, reviewBytes, receiptBytes);
  const authorManifest = {
    schema_version: 1, kind: 'a01_lexicon_rebaseline_author_manifest', slug: SLUG,
    plan_sha256: planSha, event_id: plan.event_id, revision: plan.revision,
    previous_tip_index_sha256: pins.tip_index_sha256,
    independent_review_sha256: sha(reviewBytes), revision_receipt_sha256: sha(receiptBytes),
  };
  const authorBytes = Buffer.from(compact(authorManifest), 'utf8');
  const index = {
    schema_version: 1, slug: SLUG, result_kind: 'manual_lexicon_rebaseline',
    install_receipt_sha256: pins.install_receipt_sha256,
    before_source_sha256: pins.source_composite_sha256,
    after_source_sha256: plan.after_source_composite_sha256,
    before: plan.before_source_hashes, after: plan.after_source_hashes,
    revision: plan.revision, revision_receipt_sha256: sha(receiptBytes),
    independent_review_sha256: sha(reviewBytes), author_manifest_sha256: sha(authorBytes),
  };
  const indexBytes = Buffer.from(compact(index), 'utf8');
  const eventPath = `${SLUG}/story/recheck-audit/${plan.event_id}`;
  const historicalManifest = indexManifest(snapshotRoot, plan.historical_event_ids);
  need(sha(JSON.stringify(historicalManifest)) === pins.archive_index_manifest_sha256
    && same(sourceHashes(snapshotRoot), plan.after_source_hashes)
    && historicalFiles(snapshotRoot, plan.historical_event_ids).sha256 === plan.historical_files_sha256,
  'CONCURRENT_BASELINE_DRIFT');
  const manifest = [...historicalManifest,
    { id: plan.event_id, index_sha256: sha(indexBytes) }].sort((a, b) => a.id.localeCompare(b.id));
  const expectedPins = {
    id: `a01-${plan.event_id}`, links: 81,
    install_receipt_sha256: pins.install_receipt_sha256,
    tip_index_sha256: sha(indexBytes),
    source_composite_sha256: plan.after_source_composite_sha256,
    archive_index_manifest_sha256: sha(JSON.stringify(manifest)),
  };
  return { candidate, event_path: eventPath,
    files: { [`${SLUG}/${plan.revision}/installation-receipt.json`]: receiptBytes,
      [`${eventPath}/independent-review.json`]: reviewBytes,
      [`${eventPath}/author-manifest.json`]: authorBytes,
      [`${eventPath}/index.json`]: indexBytes },
    expected_pins: expectedPins, production_status: 'HOLD',
    installation_allowed: false, paid_work_allowed: false };
}

/** Validates an 80 -> 81 local snapshot transition against the exact proposal. */
export function verifyProposedTransition({ beforeRoot, afterRoot, oldLexiconFile,
  pins = HISTORICAL_PINS, expectedOldSha = OLD_LEXICON_SHA256,
  expectedNewSha = NEW_LEXICON_SHA256 } = {}) {
  const eventId = `lexicon-rebaseline-${expectedNewSha.slice(0, 16)}`;
  const eventPath = `${SLUG}/story/recheck-audit/${eventId}`;
  const reviewBytes = bytesAt(afterRoot, `${eventPath}/independent-review.json`);
  const receiptBytes = bytesAt(afterRoot, `${SLUG}/manual-revisions/${eventId}/installation-receipt.json`);
  const prepared = prepareProposedEvent({ snapshotRoot: beforeRoot, oldLexiconFile,
    reviewBytes, receiptBytes, pins, expectedOldSha, expectedNewSha });
  const { plan } = prepared.candidate;
  need(!same(path.resolve(beforeRoot), path.resolve(afterRoot)), 'BEFORE_AND_AFTER_MUST_BE_SEPARATE');
  const afterSource = sourceHashes(afterRoot);
  need(same(afterSource, plan.after_source_hashes)
    && sha(JSON.stringify(afterSource)) === plan.after_source_composite_sha256, 'CONCURRENT_SOURCE_DRIFT');
  const afterEventIds = listDirs(afterRoot, `${SLUG}/story/recheck-audit`);
  need(afterEventIds.length === 81 && same(afterEventIds,
    [...plan.historical_event_ids, eventId].sort()), 'EVENT_COUNT_OR_ID_MISMATCH');
  const history = historicalFiles(afterRoot, plan.historical_event_ids, eventId);
  need(history.sha256 === plan.historical_files_sha256
    && same(history.revisionIds, plan.historical_revision_ids), 'HISTORICAL_EVIDENCE_DRIFT');
  const revisionDir = path.join(localRoot(afterRoot), SLUG, 'manual-revisions', eventId);
  need(same(readdirSync(revisionDir).sort(), ['installation-receipt.json']), 'UNEXPECTED_REVISION_FILE');
  const auditDir = path.join(localRoot(afterRoot), ...eventPath.split('/'));
  need(same(readdirSync(auditDir).sort(), ['author-manifest.json', 'independent-review.json', 'index.json']),
    'UNEXPECTED_NEW_EVENT_FILE');
  for (const [rel, expected] of Object.entries(prepared.files)) {
    need(bytesAt(afterRoot, rel).equals(expected), 'PROPOSED_EVENT_BYTES_MISMATCH');
  }
  const fullManifest = indexManifest(afterRoot, afterEventIds);
  need(sha(JSON.stringify(fullManifest)) === prepared.expected_pins.archive_index_manifest_sha256
    && fullManifest.find((item) => item.id === eventId)?.index_sha256 === prepared.expected_pins.tip_index_sha256,
  'NEW_PIN_TRANSITION_MISMATCH');
  return { schema_version: 1, kind: 'a01_lexicon_rebaseline_transition_check', slug: SLUG,
    integrity: 'LOCAL_81_EVENT_TRANSITION_PASS', production_status: 'HOLD',
    plan_sha256: prepared.candidate.plan_sha256, previous_tip_index_sha256: pins.tip_index_sha256,
    new_pins: prepared.expected_pins, installation_allowed: false, paid_work_allowed: false };
}

function cli() {
  const args = process.argv.slice(2);
  try {
    if (args.length === 4 && args[0] === '--snapshot' && args[2] === '--old-lexicon') {
      process.stdout.write(compact(proposeRebaseline({ snapshotRoot: args[1], oldLexiconFile: args[3] })));
    } else if (args.length === 8 && args[0] === '--prepare' && args[2] === '--old-lexicon'
      && args[4] === '--review' && args[6] === '--receipt') {
      const proposed = prepareProposedEvent({ snapshotRoot: args[1], oldLexiconFile: args[3],
        reviewBytes: fileAtAbsolute(args[5]), receiptBytes: fileAtAbsolute(args[7]) });
      process.stdout.write(compact({ schema_version: 1, kind: 'a01_lexicon_rebaseline_event_preview',
        slug: SLUG, plan_sha256: proposed.candidate.plan_sha256,
        event_path: proposed.event_path,
        files_sha256: Object.fromEntries(Object.entries(proposed.files).map(([rel, bytes]) => [rel, sha(bytes)])),
        expected_pins: proposed.expected_pins, production_status: 'HOLD',
        installation_allowed: false, paid_work_allowed: false }));
    } else if (args.length === 6 && args[0] === '--before' && args[2] === '--after' && args[4] === '--old-lexicon') {
      process.stdout.write(compact(verifyProposedTransition({ beforeRoot: args[1], afterRoot: args[3], oldLexiconFile: args[5] })));
    } else {
      throw new RebaselineError('USAGE');
    }
  } catch (error) {
    process.stdout.write(compact({ schema_version: 1, kind: 'a01_lexicon_rebaseline_gate',
      integrity: 'REJECTED', production_status: 'HOLD', installation_allowed: false,
      paid_work_allowed: false, error: error instanceof RebaselineError ? error.code : 'LOCAL_READ_ERROR' }));
    process.exitCode = 1;
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) cli();
