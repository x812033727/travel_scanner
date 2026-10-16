import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, readdirSync, rmSync, unlinkSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { inspectSnapshot } from './inspect.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const SLUG = 'story-rolling-suitcase-v2';
const CHAPTERS = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (value) => createHash('sha256').update(value).digest('hex');
const relAudit = `${SLUG}/story/recheck-audit`;

function fixture(t) {
  const root = mkdtempSync(path.join(os.tmpdir(), 'a01-host-inspect-fixture-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const write = (rel, value) => {
    const file = path.join(root, ...rel.split('/'));
    mkdirSync(path.dirname(file), { recursive: true });
    writeFileSync(file, value);
    return file;
  };
  const hashFile = (rel) => sha(readFileSync(path.join(root, ...rel.split('/'))));
  const docs = `docs/videos/${SLUG}`;
  for (const [rel, value] of Object.entries({
    [`${docs}/video.json`]: 'video\n', [`${docs}/series.json`]: 'series\n',
    [`${docs}/claims.md`]: 'claims\n', [`${docs}/script.md`]: 'script\n',
    'docs/videos/lexicon.json': 'lexicon\n',
    [`${SLUG}/review/narrative.json`]: 'narrative\n',
  })) write(rel, value);
  for (const key of CHAPTERS) write(`${SLUG}/story/chapters/${key}.json`, `${key}\n`);
  write(`${SLUG}/auto.json`, 'auto-80\n');

  const map = (hop) => ({
    auto: sha(`auto-${hop}\n`), video: hashFile(`${docs}/video.json`), series: hashFile(`${docs}/series.json`),
    claims: hashFile(`${docs}/claims.md`), script: hashFile(`${docs}/script.md`), lexicon: hashFile('docs/videos/lexicon.json'),
    narrative: hashFile(`${SLUG}/review/narrative.json`), pilot: null, verify: null,
    chapters: Object.fromEntries(CHAPTERS.map((key) => [key, hashFile(`${SLUG}/story/chapters/${key}.json`)])),
  });
  const initial = map(0);
  const installed = {
    'docs/video.json': initial.video, 'docs/script.md': initial.script, 'docs/claims.md': initial.claims,
    'docs/series.json': initial.series,
    ...Object.fromEntries(CHAPTERS.map((key) => [`work/story/chapters/${key}.json`, initial.chapters[key]])),
    'work/auto.json': initial.auto,
  };
  const receiptRel = `${SLUG}/manual-revisions/initial/installation-receipt.json`;
  write(receiptRel, `${JSON.stringify({ schema_version: 1, kind: 'a01-candidate-installation', slug: SLUG, installed_sha256: installed })}\n`);
  for (let hop = 0; hop < 80; hop++) {
    const id = `event-${String(hop).padStart(3, '0')}`;
    const rel = `${relAudit}/${id}`;
    const before = map(hop), after = map(hop + 1);
    const index = {
      schema_version: 1, slug: SLUG, result_kind: 'saved',
      install_receipt_sha256: hashFile(receiptRel),
      before_source_sha256: sha(JSON.stringify(before)), after_source_sha256: sha(JSON.stringify(after)),
      before, after,
    };
    if (hop === 20) {
      const revision = 'manual-revisions/rev-020';
      const receipt = `${SLUG}/${revision}/installation-receipt.json`;
      write(receipt, 'manual revision receipt\n');
      write(`${rel}/independent-review.json`, 'independent review\n');
      write(`${rel}/author-manifest.json`, 'author manifest\n');
      Object.assign(index, { revision, revision_receipt_sha256: hashFile(receipt),
        independent_review_sha256: hashFile(`${rel}/independent-review.json`),
        author_manifest_sha256: hashFile(`${rel}/author-manifest.json`) });
    } else {
      const journalBytes = Buffer.from(`${JSON.stringify({ hop })}\n`);
      const journalHash = sha(journalBytes);
      write(`${rel}/${journalHash}.json`, journalBytes);
      index.journals = [{ name: `${journalHash}.json`, stage: 'verifier', variant: 'story', status: 'succeeded', sha256: journalHash }];
    }
    write(`${rel}/index.json`, `${JSON.stringify(index, null, 2)}\n`);
  }
  const pinset = () => {
    const names = readdirSync(path.join(root, ...relAudit.split('/'))).sort();
    const manifest = names.map((id) => ({ id, index_sha256: hashFile(`${relAudit}/${id}/index.json`) }));
    return {
      id: 'synthetic-test-fixture', links: 80,
      install_receipt_sha256: hashFile(receiptRel),
      tip_index_sha256: manifest.at(-1).index_sha256,
      source_composite_sha256: sha(JSON.stringify(map(80))),
      archive_index_manifest_sha256: sha(JSON.stringify(manifest)),
    };
  };
  return { root, write, hashFile, pinset };
}

const errorCodes = (report) => report.errors.map((error) => error.code);

test('synthetic 80-link chain passes local integrity only and still lists live gates', (t) => {
  const f = fixture(t);
  const report = inspectSnapshot({ snapshotRoot: f.root, pins: f.pinset() });
  assert.equal(report.integrity, 'LOCAL_SNAPSHOT_INTEGRITY_PASS');
  assert.equal(report.chain.observed_links, 80);
  assert.equal(report.source.composite_sha256, f.pinset().source_composite_sha256);
  assert.equal(report.chain.tip_index_sha256, f.pinset().tip_index_sha256);
  assert.equal(report.installation_allowed, false);
  assert.equal(report.paid_work_allowed, false);
  assert.ok(report.required_live_evidence.some((item) => item.includes('db_usd25_budget')));
  assert.ok(report.required_live_evidence.some((item) => item.includes('STOP')));
  assert.ok(report.required_live_evidence.some((item) => item.includes('manifests')));
  assert.deepEqual(report.errors, []);
});

test('tampered middle index metadata is rejected by the archive index manifest pin', (t) => {
  const f = fixture(t), pins = f.pinset();
  const rel = `${relAudit}/event-031/index.json`;
  const index = JSON.parse(readFileSync(path.join(f.root, ...rel.split('/')), 'utf8'));
  index.result_kind = 'changed';
  f.write(rel, `${JSON.stringify(index, null, 2)}\n`);
  assert.deepEqual(errorCodes(inspectSnapshot({ snapshotRoot: f.root, pins })), ['ARCHIVE_INDEX_MANIFEST_MISMATCH']);
});

test('tampered journal bytes are rejected even with unchanged index', (t) => {
  const f = fixture(t), pins = f.pinset();
  const rel = `${relAudit}/event-031/index.json`;
  const index = JSON.parse(readFileSync(path.join(f.root, ...rel.split('/')), 'utf8'));
  f.write(`${relAudit}/event-031/${index.journals[0].name}`, 'altered\n');
  assert.deepEqual(errorCodes(inspectSnapshot({ snapshotRoot: f.root, pins })), ['AUDIT_JOURNAL_HASH_MISMATCH']);
});

test('manual revision review and receipt hashes are also checked', (t) => {
  const f = fixture(t), pins = f.pinset();
  f.write(`${relAudit}/event-020/independent-review.json`, 'altered\n');
  assert.deepEqual(errorCodes(inspectSnapshot({ snapshotRoot: f.root, pins })), ['AUDIT_REVIEW_HASH_MISMATCH']);
  const g = fixture(t), nextPins = g.pinset();
  g.write(`${SLUG}/manual-revisions/rev-020/installation-receipt.json`, 'altered\n');
  assert.deepEqual(errorCodes(inspectSnapshot({ snapshotRoot: g.root, pins: nextPins })), ['AUDIT_REVISION_RECEIPT_MISMATCH']);
});

test('missing index and missing source are rejected with relative path evidence', (t) => {
  const f = fixture(t), pins = f.pinset();
  unlinkSync(path.join(f.root, ...`${relAudit}/event-031/index.json`.split('/')));
  const missingIndex = inspectSnapshot({ snapshotRoot: f.root, pins });
  assert.deepEqual(errorCodes(missingIndex), ['MISSING_FILE_OR_DIRECTORY']);
  assert.equal(missingIndex.errors[0].relative_path, `${relAudit}/event-031/index.json`);
  const g = fixture(t), nextPins = g.pinset();
  unlinkSync(path.join(g.root, 'docs', 'videos', 'lexicon.json'));
  const missingSource = inspectSnapshot({ snapshotRoot: g.root, pins: nextPins });
  assert.deepEqual(errorCodes(missingSource), ['MISSING_FILE_OR_DIRECTORY']);
  assert.equal(missingSource.errors[0].relative_path, 'docs/videos/lexicon.json');
});

test('missing audit directory is rejected before treating 79 links as a complete chain', (t) => {
  const f = fixture(t), pins = f.pinset();
  rmSync(path.join(f.root, ...`${relAudit}/event-031`.split('/')), { recursive: true });
  const report = inspectSnapshot({ snapshotRoot: f.root, pins });
  assert.equal(report.chain.observed_links, 79);
  assert.deepEqual(errorCodes(report), ['LINK_COUNT_MISMATCH']);
});

test('a forked 80-link chain is rejected even when the caller recomputes archive pins', (t) => {
  const f = fixture(t);
  const rel = `${relAudit}/event-002/index.json`;
  const index = JSON.parse(readFileSync(path.join(f.root, ...rel.split('/')), 'utf8'));
  const previous = JSON.parse(readFileSync(path.join(f.root, ...`${relAudit}/event-001/index.json`.split('/')), 'utf8'));
  index.before = previous.before;
  index.before_source_sha256 = previous.before_source_sha256;
  f.write(rel, `${JSON.stringify(index, null, 2)}\n`);
  assert.deepEqual(errorCodes(inspectSnapshot({ snapshotRoot: f.root, pins: f.pinset() })), ['AUDIT_FORK']);
});

test('source drift from the 80th tip is rejected', (t) => {
  const f = fixture(t), pins = f.pinset();
  f.write(`${SLUG}/auto.json`, 'changed after capture\n');
  assert.deepEqual(errorCodes(inspectSnapshot({ snapshotRoot: f.root, pins })), ['SOURCE_DRIFT_FROM_TIP']);
});

test('revision paths cannot escape the snapshot with Windows separators', (t) => {
  const f = fixture(t);
  const rel = `${relAudit}/event-020/index.json`;
  const index = JSON.parse(readFileSync(path.join(f.root, ...rel.split('/')), 'utf8'));
  index.revision = String.raw`manual-revisions/..\..\..\outside`;
  f.write(rel, `${JSON.stringify(index, null, 2)}\n`);
  assert.deepEqual(errorCodes(inspectSnapshot({ snapshotRoot: f.root, pins: f.pinset() })), ['INVALID_LOCAL_PATH']);
});

test('UNC snapshot roots are rejected before filesystem reads', () => {
  const report = inspectSnapshot({ snapshotRoot: '//server/share/archive' });
  assert.deepEqual(errorCodes(report), ['UNC_SNAPSHOT_ROOT_UNSUPPORTED']);
});

test('CLI emits one JSON report and nonzero exit for a snapshot outside historical pins', (t) => {
  const f = fixture(t);
  unlinkSync(path.join(f.root, 'docs', 'videos', 'lexicon.json'));
  const result = spawnSync(process.execPath, [path.join(here, 'inspect.mjs'), '--snapshot', f.root], { encoding: 'utf8' });
  assert.equal(result.status, 1);
  assert.equal(result.stderr, '');
  const report = JSON.parse(result.stdout);
  assert.equal(report.integrity, 'REJECTED');
  assert.deepEqual(errorCodes(report), ['INSTALL_RECEIPT_MISSING_OR_DUPLICATED']);
});
