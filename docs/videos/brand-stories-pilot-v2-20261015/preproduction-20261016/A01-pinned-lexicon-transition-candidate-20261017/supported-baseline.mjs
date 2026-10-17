#!/usr/bin/env node
// Offline proposal and transition verifier. It never connects to or writes a host.
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readFileSync, readdirSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { entriesUsed, termPattern, termsUsed, unknownTermsFor, validateLexicon } from '../../../../../tools/video/core/lexicon.mjs';
import { HISTORICAL_PINS, inspectSnapshot } from '../A01-host-inspect-candidate/inspect.mjs';

const SLUG = 'story-rolling-suitcase-v2';
const CANDIDATE_ID = 'a01-lexicon-rebaseline-e6403c824aac13b4-20261017';
const CHAPTERS = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const SOURCE_KEYS = ['auto', 'video', 'series', 'claims', 'script', 'lexicon', 'narrative', 'pilot', 'verify', 'chapters'];
const OLD_LEXICON_SHA256 = 'ebfa590a69b4328ed9bc0141832bb73d27cba51963fca78778258d404c3bc4c9';
const NEW_LEXICON_SHA256 = 'e6403c824aac13b4c0a1ae737e8a597a8bf60c353e9faf0cc4915c3214114a30';
// Exact additions in the 2026-10-17 host capture. The old two-term review cannot bind this plan.
const EXPECTED_ADDITIONS = Object.freeze({
  pull: null, request: null, Eiliko: null, Energize: null, Lab: null,
  CVE: 'C V E', IP: 'I P', Seiko: '精工', Quartz: '夸茲', Astron: '阿斯特朗',
  K: null, CEH: 'C E H', IEEE: 'I triple E', Beta: '貝塔', swissinfo: 'swiss info',
  Europa: '歐羅巴', Star: null, Donz: '東澤', Swatch: null, Group: null,
  SSIH: 'S S I H', ASUAG: 'A S U A G', Hayek: '海耶克',
});
const AFTERNOON_SHA='4d3e995b1abf1acd64db3eafd397f1cad8e220880e95f2c39ab108ecaea8c9f6';
const AFTERNOON_ADDITIONS=Object.freeze({...EXPECTED_ADDITIONS,Nieman:'尼曼',Daniel:null,Roberts:null,One:null});
const HASH = /^[a-f0-9]{64}$/u;
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const ADDED_PATTERN = termPattern(Object.keys(EXPECTED_ADDITIONS)
  .sort((a, b) => b.length - a.length).map((key) => [key, EXPECTED_ADDITIONS[key]]));

/** Uses the speech/glossary matcher, including its ASCII boundaries beside Chinese text. */
export function addedTermsInSpoken(text, expected=EXPECTED_ADDITIONS) {
  const pattern=expected===EXPECTED_ADDITIONS?ADDED_PATTERN:termPattern(Object.entries(expected).sort((a,b)=>b[0].length-a[0].length));
  return [...String(text).matchAll(pattern)].map((match) => match[0]);
}

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

function assertFrozenInputs(root, pins, expectedOldSha, expectedNewSha) {
  const fields = ['links', 'install_receipt_sha256', 'tip_index_sha256',
    'source_composite_sha256', 'archive_index_manifest_sha256'];
  const frozen = fields.every((key) => pins?.[key] === HISTORICAL_PINS[key])
    && expectedOldSha === OLD_LEXICON_SHA256 && (expectedNewSha === NEW_LEXICON_SHA256 || expectedNewSha === AFTERNOON_SHA);
  if (frozen) return;
  const relative = path.relative(os.tmpdir(), localRoot(root));
  need(relative && relative !== '..' && !relative.startsWith(`..${path.sep}`)
    && !path.isAbsolute(relative), 'SYNTHETIC_OVERRIDE_FORBIDDEN');
  const markerBytes = bytesAt(root, 'A01-LEXICON-E640-OFFLINE-FIXTURE.json', true);
  need(markerBytes !== null, 'SYNTHETIC_OVERRIDE_FORBIDDEN');
  const marker = parseJson(markerBytes,
    'SYNTHETIC_MARKER_INVALID');
  need(marker?.schema_version === 1 && marker.slug === SLUG
    && marker.synthetic_fixture === true
    && same(Object.keys(marker).sort(), ['schema_version', 'slug', 'synthetic_fixture'].sort()),
  'SYNTHETIC_MARKER_INVALID');
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

function lexiconDelta(oldBytes, newBytes, expected=EXPECTED_ADDITIONS) {
  const oldLexicon = parseJson(oldBytes, 'INVALID_OLD_LEXICON');
  const newLexicon = parseJson(newBytes, 'INVALID_NEW_LEXICON');
  need(oldLexicon?.schema_version === 1 && newLexicon?.schema_version === 1
    && oldLexicon.terms && newLexicon.terms && typeof oldLexicon.terms === 'object'
    && typeof newLexicon.terms === 'object' && !Array.isArray(oldLexicon.terms)
    && !Array.isArray(newLexicon.terms), 'INVALID_LEXICON_SHAPE');
  need(same(Object.keys(oldLexicon).sort(), ['schema_version', 'terms'].sort())
    && same(Object.keys(oldLexicon).sort(), Object.keys(newLexicon).sort()), 'LEXICON_TOP_LEVEL_DRIFT');
  need(validateLexicon(oldLexicon).length === 0 && validateLexicon(newLexicon).length === 0,
    'INVALID_LEXICON_CONTENT');
  const oldTerms = oldLexicon.terms, newTerms = newLexicon.terms;
  const additions = Object.fromEntries(Object.entries(newTerms)
    .filter(([key]) => !Object.hasOwn(oldTerms, key)));
  need(Object.keys(newTerms).length === Object.keys(oldTerms).length + Object.keys(expected).length
    && Object.entries(oldTerms).every(([key, value]) => Object.hasOwn(newTerms, key) && same(value, newTerms[key])), 'LEXICON_DELTA_NOT_ALLOWED');
  need(same(Object.keys(additions).sort(), Object.keys(expected).sort())
    && Object.entries(expected).every(([key, value]) => same(additions[key], value)),
  'LEXICON_DELTA_NOT_ALLOWED');
  return { old_term_count: Object.keys(oldTerms).length, new_term_count: Object.keys(newTerms).length,
    additions };
}

function assertNoNarrationUsage(root, oldLexicon, newLexicon, expected=EXPECTED_ADDITIONS) {
  const hits = [];
  const addedKeys = Object.keys(expected);
  const spokenLines = [];
  let sceneCount = 0;
  const sources = [
    ...CHAPTERS.map((key) => ({ label: `chapter/${key}`,
      rel: `${SLUG}/story/chapters/${key}.json` })),
    { label: 'video', rel: `docs/videos/${SLUG}/video.json` },
  ];
  for (const { label, rel } of sources) {
    const doc = parseJson(bytesAt(root, rel), 'INVALID_NARRATION_JSON');
    need(Array.isArray(doc?.scenes), 'INVALID_NARRATION_SCENES');
    for (const scene of doc.scenes) {
      sceneCount++;
      need(Array.isArray(scene.lines), 'INVALID_NARRATION_LINES');
      for (const line of scene.lines) {
        // Match the TTS path in tools/video/core/schema.mjs: spokenText(line).
        need(typeof line.text === 'string' && (line.say == null || typeof line.say === 'string'),
          'INVALID_NARRATION_LINES');
        const spoken = line.say ?? line.text;
        spokenLines.push(spoken);
        if (addedTermsInSpoken(spoken, expected).length > 0) hits.push(`${label}/${scene.id}/${line.id}`);
      }
    }
  }
  need(hits.length === 0, 'NEW_LEXICON_TERM_IN_NARRATION');
  const unknown = (lexicon) => spokenLines.flatMap((line) => unknownTermsFor(line, lexicon, 'zh-TW'));
  need(same(termsUsed(spokenLines, oldLexicon), termsUsed(spokenLines, newLexicon))
    && same(entriesUsed(spokenLines, oldLexicon), entriesUsed(spokenLines, newLexicon))
    && same(unknown(oldLexicon), unknown(newLexicon)), 'NARRATION_LEXICON_SEMANTIC_DRIFT');
  return { scenes: sceneCount, lines: spokenLines.length, added_terms_checked: addedKeys.length };
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
  const oldBytes = fileAtAbsolute(oldLexiconFile);
  const newBytes = bytesAt(snapshotRoot, 'docs/videos/lexicon.json');
  const expected=expectedNewSha===AFTERNOON_SHA?AFTERNOON_ADDITIONS:EXPECTED_ADDITIONS;
  const delta = lexiconDelta(oldBytes, newBytes, expected);
  const narration = assertNoNarrationUsage(snapshotRoot,
    parseJson(oldBytes, 'INVALID_OLD_LEXICON'), parseJson(newBytes, 'INVALID_NEW_LEXICON'),expected);
  const eventIds = listDirs(snapshotRoot, `${SLUG}/story/recheck-audit`);
  need(eventIds.length === 80, 'BASELINE_LINK_COUNT_MISMATCH');
  const manifest = indexManifest(snapshotRoot, eventIds);
  need(sha(JSON.stringify(manifest)) === pins.archive_index_manifest_sha256, 'HISTORICAL_MANIFEST_MISMATCH');
  return { before, after, delta, narration, eventIds, manifest,
    historicalFiles: historicalFiles(snapshotRoot, eventIds) };
}

/** Read-only plan. CLI uses immutable historical pins and exact 2026-10-17 lexicon hashes. */
export function proposeRebaseline({ snapshotRoot, oldLexiconFile,
  pins = HISTORICAL_PINS, expectedOldSha = OLD_LEXICON_SHA256,
  expectedNewSha = sha(bytesAt(snapshotRoot, 'docs/videos/lexicon.json')) } = {}) {
  assertFrozenInputs(snapshotRoot, pins, expectedOldSha, expectedNewSha);
  const baseline = validatedBaseline({ snapshotRoot, oldLexiconFile, pins, expectedOldSha, expectedNewSha });
  const eventId = `lexicon-rebaseline-${expectedNewSha.slice(0, 16)}`;
  const revisionId = eventId;
  need(!baseline.eventIds.includes(eventId)
    && !baseline.historicalFiles.revisionIds.includes(revisionId), 'DUPLICATE_REBASELINE_EVENT');
  const plan = {
    schema_version: 1, kind: 'a01_lexicon_rebaseline_plan', candidate_id: expectedNewSha===AFTERNOON_SHA?'a01-lexicon-baseline-4d3e995b1abf1acd-20261017':CANDIDATE_ID, slug: SLUG,
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
    delta: baseline.delta, narration: baseline.narration, narration_term_hits: 0,
  };
  return { plan, plan_sha256: sha(JSON.stringify(plan)), production_status: 'HOLD',
    installation_allowed: false, paid_work_allowed: false };
}
