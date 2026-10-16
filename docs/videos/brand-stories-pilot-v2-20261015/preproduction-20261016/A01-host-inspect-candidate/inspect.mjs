#!/usr/bin/env node
// Read-only verifier for a LOCAL A01 archive. It has no install or host mode.
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readFileSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SLUG = 'story-rolling-suitcase-v2';
const CHAPTERS = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const SOURCE_KEYS = ['auto', 'video', 'series', 'claims', 'script', 'lexicon', 'narrative', 'pilot', 'verify', 'chapters'];
const HASH = /^[a-f0-9]{64}$/;
const sha256 = (value) => createHash('sha256').update(value).digest('hex');

// Pins from the 2026-10-16 03:50:53 local archive, NOT a fresh live-host readback.
export const HISTORICAL_PINS = Object.freeze({
  id: 'a01-local-archive-20261016-035053',
  links: 80,
  install_receipt_sha256: '24110fc8cc1665e9f6830db23e57cde12640c4bd947af3a42a25602528a266fd',
  tip_index_sha256: 'c7ddb6b5796605c08b3c47c305864eddf28e5246ee6ad8426c3601637ecdc9a4',
  source_composite_sha256: 'cf39296d597d36db3cafedc1c2ca5ae730dd104a34b1d1868fb5b83fc089c56b',
  archive_index_manifest_sha256: 'ada7ff1859788310fcda7ca35da052a2c4f1009b2c9058454b0e1b4d74d3614f',
});

const REQUIRED_LIVE_EVIDENCE = Object.freeze([
  'fresh_video_worker_release_and_panel_rules_sha256',
  'fresh_host_docs_work_source_hashes_and_audit_chain',
  'a01_scoped_STOP_global_STOP_and_exclusive_lease_owner',
  'a01_db_project_retry_and_stage_media_job_state',
  'a01_db_usd25_budget_row_and_every_operation_status',
  'a01_run_receipts_and_unresolved_journals',
  'a01_visual_audio_manifests_and_paid_asset_inventory',
]);

class GateError extends Error {
  constructor(code, relativePath = null) { super(code); this.code = code; this.relativePath = relativePath; }
}
const fail = (code, relativePath = null) => { throw new GateError(code, relativePath); };
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

function safePath(root, rel, kind = 'file', optional = false) {
  if (typeof rel !== 'string' || !path.isAbsolute(root) || !rel
    || /[\\:\x00-\x1f]/u.test(rel)
    || rel.split('/').some((part) => !part || part === '.' || part === '..')) fail('INVALID_LOCAL_PATH');
  let current = root;
  const parts = rel.split('/');
  const relative = path.relative(root, path.resolve(root, ...parts));
  if (relative === '..' || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) fail('INVALID_LOCAL_PATH');
  for (let i = 0; i < parts.length; i++) {
    current = path.join(current, parts[i]);
    if (!existsSync(current)) {
      if (optional) return null;
      fail('MISSING_FILE_OR_DIRECTORY', rel);
    }
    const stat = lstatSync(current);
    if (stat.isSymbolicLink()) fail('SYMLINK_IN_SNAPSHOT', rel);
    if (i < parts.length - 1 && !stat.isDirectory()) fail('INVALID_LOCAL_PATH');
    if (i === parts.length - 1 && !(kind === 'directory' ? stat.isDirectory() : stat.isFile())) fail('INVALID_FILE_TYPE');
  }
  return current;
}

function fileBytes(root, rel, optional = false) {
  const resolved = safePath(root, rel, 'file', optional);
  return resolved ? readFileSync(resolved) : null;
}
function fileHash(root, rel, optional = false) {
  const bytes = fileBytes(root, rel, optional);
  return bytes === null ? null : sha256(bytes);
}
function jsonFile(root, rel) {
  const bytes = fileBytes(root, rel);
  try { return JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/, '')); }
  catch { fail('INVALID_JSON'); }
}
function dirs(root, rel) {
  const directory = safePath(root, rel, 'directory');
  const entries = readdirSync(directory, { withFileTypes: true });
  if (entries.some((entry) => entry.isSymbolicLink() || !entry.isDirectory())) fail('UNEXPECTED_AUDIT_ENTRY');
  return entries.map((entry) => entry.name).sort();
}
function validSourceMap(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value) || !same(Object.keys(value), SOURCE_KEYS)) return false;
  if (!value.chapters || !same(Object.keys(value.chapters), CHAPTERS)) return false;
  for (const key of SOURCE_KEYS.filter((key) => !['chapters', 'pilot', 'verify'].includes(key))) if (!HASH.test(value[key] ?? '')) return false;
  for (const key of ['pilot', 'verify']) if (value[key] !== null && !HASH.test(value[key] ?? '')) return false;
  return CHAPTERS.every((key) => HASH.test(value.chapters[key] ?? ''));
}
function sourceSnapshot(root) {
  const work = SLUG;
  const docs = `docs/videos/${SLUG}`;
  const hashes = {
    auto: fileHash(root, `${work}/auto.json`),
    video: fileHash(root, `${docs}/video.json`),
    series: fileHash(root, `${docs}/series.json`),
    claims: fileHash(root, `${docs}/claims.md`),
    script: fileHash(root, `${docs}/script.md`),
    lexicon: fileHash(root, 'docs/videos/lexicon.json'),
    narrative: fileHash(root, `${work}/review/narrative.json`),
    pilot: fileHash(root, `${work}/story/reviews/script-review.json`, true),
    verify: fileHash(root, `${docs}/verify-1.md`, true),
    chapters: Object.fromEntries(CHAPTERS.map((key) => [key, fileHash(root, `${work}/story/chapters/${key}.json`)])),
  };
  return { hashes, composite: sha256(JSON.stringify(hashes)) };
}
function installReceipt(root, expectedHash) {
  const revisions = dirs(root, `${SLUG}/manual-revisions`);
  const matches = [];
  for (const name of revisions) {
    const rel = `${SLUG}/manual-revisions/${name}/installation-receipt.json`;
    if (fileHash(root, rel, true) === expectedHash) matches.push(jsonFile(root, rel));
  }
  if (matches.length !== 1) fail('INSTALL_RECEIPT_MISSING_OR_DUPLICATED');
  const receipt = matches[0];
  if (receipt.schema_version !== 1 || receipt.kind !== 'a01-candidate-installation' || receipt.slug !== SLUG) fail('INSTALL_RECEIPT_INVALID');
  const installed = receipt.installed_sha256;
  const required = ['docs/video.json', 'docs/script.md', 'docs/claims.md', 'docs/series.json',
    ...CHAPTERS.map((key) => `work/story/chapters/${key}.json`), 'work/auto.json'];
  if (!installed || !same(Object.keys(installed).sort(), [...required].sort()) || !required.every((key) => HASH.test(installed[key] ?? ''))) fail('INSTALL_RECEIPT_INVALID');
  return installed;
}
function installedMatches(installed, hashes) {
  return installed['docs/video.json'] === hashes.video && installed['docs/script.md'] === hashes.script
    && installed['docs/claims.md'] === hashes.claims && installed['docs/series.json'] === hashes.series
    && installed['work/auto.json'] === hashes.auto
    && CHAPTERS.every((key) => installed[`work/story/chapters/${key}.json`] === hashes.chapters[key]);
}
function auditEntries(root, receiptHash) {
  const base = `${SLUG}/story/recheck-audit`;
  const names = dirs(root, base);
  const entries = names.map((name) => {
    if (!/^[A-Za-z0-9._-]+$/.test(name)) fail('INVALID_AUDIT_DIRECTORY');
    const rel = `${base}/${name}`;
    const bytes = fileBytes(root, `${rel}/index.json`);
    const index = jsonFile(root, `${rel}/index.json`);
    if (index.schema_version !== 1 || index.slug !== SLUG || index.install_receipt_sha256 !== receiptHash
      || !validSourceMap(index.before) || !validSourceMap(index.after)
      || index.before_source_sha256 !== sha256(JSON.stringify(index.before))
      || index.after_source_sha256 !== sha256(JSON.stringify(index.after))) fail('AUDIT_INDEX_INVALID');
    if (index.journals !== undefined && !Array.isArray(index.journals)) fail('AUDIT_EVIDENCE_INVALID');
    const journals = index.journals ?? [];
    if (journals.length === 0 && !index.revision) fail('AUDIT_EVIDENCE_INVALID');
    const journalNames = new Set();
    for (const journal of journals) {
      if (!/^[a-f0-9]{64}\.json$/.test(journal?.name ?? '') || !HASH.test(journal.sha256 ?? '')
        || journalNames.has(journal.name)) fail('AUDIT_JOURNALS_INVALID');
      journalNames.add(journal.name);
      if (fileHash(root, `${rel}/${journal.name}`) !== journal.sha256) fail('AUDIT_JOURNAL_HASH_MISMATCH');
    }
    const boundFiles = new Set(['index.json', ...journalNames]);
    for (const [field, name] of [['independent_review_sha256', 'independent-review.json'],
      ['author_manifest_sha256', 'author-manifest.json']]) {
      if (index[field] !== undefined) {
        if (!HASH.test(index[field] ?? '') || fileHash(root, `${rel}/${name}`) !== index[field]) fail('AUDIT_REVIEW_HASH_MISMATCH');
        boundFiles.add(name);
      }
    }
    if (index.revision !== undefined) {
      if (typeof index.revision !== 'string' || !index.revision.startsWith('manual-revisions/')
        || !HASH.test(index.independent_review_sha256 ?? '')
        || !HASH.test(index.revision_receipt_sha256 ?? '')
        || fileHash(root, `${SLUG}/${index.revision}/installation-receipt.json`) !== index.revision_receipt_sha256)
        fail('AUDIT_REVISION_RECEIPT_MISMATCH');
    }
    const actualFiles = readdirSync(safePath(root, rel, 'directory'), { withFileTypes: true });
    if (actualFiles.some((file) => !file.isFile() || !boundFiles.has(file.name))
      || actualFiles.length !== boundFiles.size) fail('UNEXPECTED_AUDIT_FILE');
    return { id: name, index, index_sha256: sha256(bytes) };
  });
  return entries;
}
function assertPins(pins) {
  if (pins?.links !== 80 || !['install_receipt_sha256', 'tip_index_sha256', 'source_composite_sha256',
    'archive_index_manifest_sha256'].every((key) => HASH.test(pins[key] ?? ''))) fail('PINSET_INVALID');
}

export function inspectSnapshot({ snapshotRoot, pins = HISTORICAL_PINS } = {}) {
  const report = {
    schema_version: 1, kind: 'a01_local_snapshot_chain_gate', slug: SLUG,
    input_scope: 'local_snapshot_only', pinset_id: pins?.id ?? 'caller_supplied_fixture',
    integrity: 'REJECTED', installation_allowed: false, paid_work_allowed: false,
    chain: { expected_links: 80, observed_links: null, tip_index_sha256: null,
      tip_source_composite_sha256: null, tip_after_hashes: null, archive_index_manifest_sha256: null },
    source: { composite_sha256: null, hashes: null },
    required_live_evidence: [...REQUIRED_LIVE_EVIDENCE], errors: [],
  };
  try {
    assertPins(pins);
    if (!snapshotRoot || !path.isAbsolute(snapshotRoot)) fail('ABSOLUTE_LOCAL_SNAPSHOT_REQUIRED');
    if (snapshotRoot.startsWith('\\\\') || snapshotRoot.startsWith('//')) fail('UNC_SNAPSHOT_ROOT_UNSUPPORTED');
    const root = path.resolve(snapshotRoot);
    if (!existsSync(root) || !lstatSync(root).isDirectory() || lstatSync(root).isSymbolicLink()) fail('INVALID_LOCAL_SNAPSHOT_ROOT');
    const installed = installReceipt(root, pins.install_receipt_sha256);
    const events = auditEntries(root, pins.install_receipt_sha256);
    report.chain.observed_links = events.length;
    if (events.length !== pins.links) fail('LINK_COUNT_MISMATCH');
    const manifest = events.map(({ id, index_sha256 }) => ({ id, index_sha256 }));
    report.chain.archive_index_manifest_sha256 = sha256(JSON.stringify(manifest));
    if (report.chain.archive_index_manifest_sha256 !== pins.archive_index_manifest_sha256) fail('ARCHIVE_INDEX_MANIFEST_MISMATCH');
    const anchors = events.filter(({ index }) => installedMatches(installed, index.before));
    if (anchors.length !== 1) fail('AUDIT_ANCHOR_MISSING_OR_FORKED');
    let current = anchors[0];
    const visited = new Set();
    while (current) {
      if (visited.has(current.id)) fail('AUDIT_CYCLE');
      visited.add(current.id);
      const next = events.filter(({ index }) => index.before_source_sha256 === current.index.after_source_sha256
        && same(index.before, current.index.after));
      if (next.length > 1) fail('AUDIT_FORK');
      current = next[0] ?? null;
      if (!current && visited.size !== events.length) fail('AUDIT_CHAIN_DISCONNECTED');
    }
    const tip = events.find(({ id }) => id === [...visited].at(-1));
    report.chain.tip_index_sha256 = tip.index_sha256;
    report.chain.tip_source_composite_sha256 = tip.index.after_source_sha256;
    report.chain.tip_after_hashes = tip.index.after;
    report.chain.tip_directory = tip.id;
    const source = sourceSnapshot(root);
    report.source.composite_sha256 = source.composite;
    report.source.hashes = source.hashes;
    if (!same(tip.index.after, source.hashes) || tip.index.after_source_sha256 !== source.composite) fail('SOURCE_DRIFT_FROM_TIP');
    if (tip.index_sha256 !== pins.tip_index_sha256) fail('TIP_PIN_MISMATCH');
    if (source.composite !== pins.source_composite_sha256) fail('SOURCE_PIN_MISMATCH');
    report.integrity = 'LOCAL_SNAPSHOT_INTEGRITY_PASS';
  } catch (error) {
    report.errors.push(error instanceof GateError
      ? { code: error.code, ...(error.relativePath ? { relative_path: error.relativePath } : {}) }
      : { code: 'SNAPSHOT_READ_ERROR' });
  }
  return report;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const args = process.argv.slice(2);
  const valid = args.length === 2 && args[0] === '--snapshot';
  const report = inspectSnapshot({ snapshotRoot: valid ? args[1] : undefined });
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  process.exitCode = report.integrity === 'LOCAL_SNAPSHOT_INTEGRITY_PASS' ? 0 : 1;
}
