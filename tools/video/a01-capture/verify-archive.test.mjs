import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdtemp, mkdir, readFile, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve, sep } from 'node:path';
import { test } from 'node:test';
import { verifyCapture } from './verify-archive.mjs';
import { SLUG } from './capture.mjs';

const hash = value => createHash('sha256').update(value).digest('hex');
const tarProgram = process.platform === 'win32'
  ? 'C:/Program Files/Git/usr/bin/tar.exe' : 'tar';
const sources = [
  'docs/videos/lexicon.json',
  ...['series.json', 'video.json', 'claims.md', 'script.md', 'verify-1.md']
    .map(name => `docs/videos/${SLUG}/${name}`),
  `${SLUG}/auto.json`, `${SLUG}/review/narrative.json`,
  ...['hook', 'origin', 'idea', 'engine', 'turn', 'now']
    .map(name => `${SLUG}/story/chapters/${name}.json`),
  `${SLUG}/story/reviews/script-review.json`,
];
const firstEvent = 'event-' + 'x'.repeat(100); // GNU LongLink, not PAX.
const receiptRel = `${SLUG}/manual-revisions/rev-1/installation-receipt.json`;
const lexiconRoot = `docs/videos/${SLUG}/story-lexicon`;
const lexiconNames = [
  `${lexiconRoot}/current.json`,
  `${lexiconRoot}/events/${'a'.repeat(64)}.json`,
  `${lexiconRoot}/versions/${'b'.repeat(64)}.json`,
];

async function createFixture(t) {
  const root = await mkdtemp(join(tmpdir(), 'a01-archive-verify-'));
  const tempRoot = resolve(tmpdir()) + sep;
  assert.ok(resolve(root).startsWith(tempRoot));
  t.after(async () => rm(root, { recursive: true, force: true }));
  const docs = join(root, 'docs');
  const work = join(root, 'work');
  const capture = join(root, 'capture');
  await mkdir(capture);
  const receipt = Buffer.from('{"receipt":true}\n');
  const inventory = {};
  const lexiconFiles = {};
  for (const path of sources) {
    const base = path.startsWith('docs/') ? docs : work;
    const data = Buffer.from(`source:${path}\n`);
    const target = join(base, path);
    await mkdir(dirname(target), { recursive: true });
    await writeFile(target, data);
    inventory[path] = { present: true, sha256: hash(data), bytes: data.length };
  }
  for (const path of lexiconNames) {
    const data = Buffer.from(`lexicon:${path}\n`);
    const target = join(docs, path);
    await mkdir(dirname(target), { recursive: true });
    await writeFile(target, data);
    lexiconFiles[path] = { present: true, sha256: hash(data), bytes: data.length };
  }
  const receiptPath = join(work, receiptRel);
  await mkdir(dirname(receiptPath), { recursive: true });
  await writeFile(receiptPath, receipt);
  const auditFiles = {};
  const auditEvents = [];
  for (let index = 0; index < 104; index += 1) {
    const event = index === 0 ? firstEvent : `event-${String(index).padStart(3, '0')}`;
    const data = Buffer.from(JSON.stringify({ event_id: event,
      ...(index === 0 ? { revision: 'manual-revisions/rev-1',
        revision_receipt_sha256: hash(receipt) } : {}) }) + '\n');
    const relative = `${event}/index.json`;
    const target = join(work, SLUG, 'story/recheck-audit', relative);
    await mkdir(dirname(target), { recursive: true });
    await writeFile(target, data);
    const pin = { present: true, sha256: hash(data), bytes: data.length };
    auditFiles[relative] = pin;
    auditEvents.push({ name: event, index: pin });
  }
  const state = `GIT ${'a'.repeat(40)}\nDEPLOY_HOLD absent\n${JSON.stringify({
    schema_version: 1, slug: SLUG, files: inventory, audit_files: auditFiles,
    lexicon_files: lexiconFiles,
    audit_events: auditEvents,
    release_sha: 'a'.repeat(40),
    tools_video_tree_sha: 'b'.repeat(40),
    worker_image_id: `sha256:${'d'.repeat(64)}`,
    worker: { story_mjs: { sha256: 'c'.repeat(64) } },
    story_mjs_sha256: 'c'.repeat(64),
    public_filter_sha256: 'c'.repeat(64),
    tools_video_runtime_files: [{ path: 'automation/story.mjs',
      sha256: 'c'.repeat(64), bytes: 42 }],
    tools_video_runtime_file_count: 1,
    tools_video_runtime_inventory_sha256: hash(
      `automation/story.mjs\0${'c'.repeat(64)}\n`),
  })}\n`;
  await writeFile(join(capture, 'host-state-before.txt'), state);
  await writeFile(join(capture, 'host-state-after.txt'), state);
  for (const name of ['db-before.json', 'db-after.json',
    'budget-before.json', 'budget-after.json']) {
    await writeFile(join(capture, name), '{}\n');
  }
  const tarPath = join(capture, 'a01-source.tar');
  execFileSync(tarProgram, ['--force-local', '-cf', tarPath,
    '-C', docs, ...sources.filter(path => path.startsWith('docs/')), lexiconRoot,
    '-C', work, ...sources.filter(path => !path.startsWith('docs/')),
    `${SLUG}/story/recheck-audit`, receiptRel]);
  const report = { slug: SLUG, status: 'HOLD', production_adoption_allowed: false,
    capture_complete: true, files_captured: 7, operational_gate: 'HOLD',
    issues: ['GLOBAL_JOB_ACTIVE'], files: {} };
  async function updateReport() {
    for (const name of ['a01-source.tar', 'host-state-before.txt', 'host-state-after.txt',
      'db-before.json', 'db-after.json', 'budget-before.json', 'budget-after.json']) {
      const bytes = await readFile(join(capture, name));
      report.files[name] = { sha256: hash(bytes), bytes: bytes.length };
    }
    await writeFile(join(capture, 'capture-report.json'), JSON.stringify(report));
  }
  await updateReport();
  return { root, capture, tarPath, updateReport };
}

function tarHeaders(buffer) {
  const entries = [];
  for (let at = 0; at + 512 <= buffer.length;) {
    const header = buffer.subarray(at, at + 512);
    if (header.every(byte => byte === 0)) break;
    const nul = header.subarray(0, 100).indexOf(0);
    const name = header.subarray(0, nul < 0 ? 100 : nul).toString();
    const size = parseInt(header.subarray(124, 136).toString().replace(/\0.*$/s, '').trim(), 8) || 0;
    entries.push({ at, name, type: String.fromCharCode(header[156]), size });
    at += 512 + Math.ceil(size / 512) * 512;
  }
  return entries;
}
function mutateHeader(buffer, at, callback) {
  const edited = Buffer.from(buffer);
  const block = edited.subarray(at, at + 512);
  callback(block);
  block.fill(32, 148, 156);
  let sum = 0;
  for (const byte of block) sum += byte;
  block.write(sum.toString(8).padStart(6, '0') + '\0 ', 148, 8, 'ascii');
  return edited;
}
function rename(block, name) {
  block.fill(0, 0, 100);
  block.write(name, 0, 'ascii');
}

test('GNU tar default uses LongLink, and exact 104-event archive verifies without extraction', async t => {
  const fixture = await createFixture(t);
  const tar = await readFile(fixture.tarPath);
  const headers = tarHeaders(tar);
  assert.ok(headers.some(item => item.type === 'L' && item.name === '././@LongLink'));
  assert.ok(!headers.some(item => item.type === 'x' || item.type === 'g'));
  assert.deepEqual(await verifyCapture(fixture.capture),
    { audit_events: 104, files: sources.length + lexiconNames.length + 104 + 1,
      receipts: 1, lexicon_files: lexiconNames.length });
});

test('archive verifier rejects traversal, links, duplicates, PAX and changed bytes', async t => {
  const fixture = await createFixture(t);
  const pristine = await readFile(fixture.tarPath);
  const headers = tarHeaders(pristine);
  const first = headers.find(item => item.name === 'docs/videos/lexicon.json');
  const second = headers.find(item => item.name === `docs/videos/${SLUG}/series.json`);
  const long = headers.find(item => item.type === 'L');
  const receipt = headers.find(item => item.name === receiptRel);
  const lexicon = headers.find(item => item.name === `${lexiconRoot}/current.json`);
  for (const [label, edited, pattern] of [
    ['traversal', mutateHeader(pristine, first.at, block => rename(block, '../escape')),
      /UNSAFE_TAR_PATH/],
    ['link', mutateHeader(pristine, first.at, block => { block[156] = '2'.charCodeAt(0); }),
      /TAR_MEMBER_TYPE_UNSUPPORTED/],
    ['duplicate', mutateHeader(pristine, second.at, block => rename(block, first.name)),
      /TAR_DUPLICATE_MEMBER/],
    ['PAX', mutateHeader(pristine, long.at, block => { block[156] = 'x'.charCodeAt(0); }),
      /TAR_MEMBER_TYPE_UNSUPPORTED/],
    ['changed bytes', (() => { const b = Buffer.from(pristine); b[first.at + 512] ^= 1; return b; })(),
      /TAR_MEMBER_HASH_MISMATCH/],
    ['changed receipt', (() => { const b = Buffer.from(pristine); b[receipt.at + 512] ^= 1; return b; })(),
      /REVISION_RECEIPT_MISMATCH/],
    ['changed story lexicon', (() => { const b = Buffer.from(pristine); b[lexicon.at + 512] ^= 1; return b; })(),
      /TAR_MEMBER_HASH_MISMATCH/],
  ]) {
    await writeFile(fixture.tarPath, edited);
    await fixture.updateReport();
    await assert.rejects(verifyCapture(fixture.capture), pattern, label);
  }
});

test('bundle hashes and canonical local path are required', async t => {
  const fixture = await createFixture(t);
  const linked = join(fixture.root, 'linked');
  await symlink(fixture.root, linked, 'junction');
  await assert.rejects(verifyCapture(join(linked, 'capture')),
    /CAPTURE_PATH_NOT_CANONICAL|CAPTURE_PARENT_LINKED/);
  await writeFile(join(fixture.capture, 'budget-after.json'), '{"changed":true}\n');
  await assert.rejects(verifyCapture(fixture.capture), /CAPTURE_FILE_HASH_MISMATCH/);
});

test('a complete capture can remain on operational HOLD, but an incomplete report fails', async t => {
  const fixture = await createFixture(t);
  assert.equal((await verifyCapture(fixture.capture)).audit_events, 104);
  const reportPath = join(fixture.capture, 'capture-report.json');
  const report = JSON.parse(await readFile(reportPath, 'utf8'));
  report.capture_complete = false;
  await writeFile(reportPath, JSON.stringify(report));
  await assert.rejects(verifyCapture(fixture.capture), /CAPTURE_REPORT_INVALID/);
});

test('worker image and runtime tree pins are required', async t => {
  const fixture = await createFixture(t);
  const beforePath = join(fixture.capture, 'host-state-before.txt');
  const afterPath = join(fixture.capture, 'host-state-after.txt');
  const original = await readFile(beforePath, 'utf8');
  const lines = original.trimEnd().split('\n');
  const worker = JSON.parse(lines[2]);
  worker.worker_image_id = null;
  const changed = `${lines[0]}\n${lines[1]}\n${JSON.stringify(worker)}\n`;
  await writeFile(beforePath, changed);
  await writeFile(afterPath, changed);
  await fixture.updateReport();
  await assert.rejects(verifyCapture(fixture.capture), /RUNTIME_PIN_INCOMPLETE/);
  worker.worker_image_id = `sha256:${'d'.repeat(64)}`;
  worker.tools_video_runtime_inventory_sha256 = 'e'.repeat(64);
  const badDigest = `${lines[0]}\n${lines[1]}\n${JSON.stringify(worker)}\n`;
  await writeFile(beforePath, badDigest);
  await writeFile(afterPath, badDigest);
  await fixture.updateReport();
  await assert.rejects(verifyCapture(fixture.capture), /RUNTIME_INVENTORY_HASH_MISMATCH/);
});
