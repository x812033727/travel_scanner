#!/usr/bin/env node
// Local-only verification of an A01 capture. Never extracts archive members.
import { createHash } from 'node:crypto';
import { createReadStream } from 'node:fs';
import { lstat, open, readFile, realpath } from 'node:fs/promises';
import { dirname, isAbsolute, join, parse, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseHostState, SLUG } from './capture.mjs';

const BLOCK = 512;
const HASH = /^[a-f0-9]{64}$/;
const decoder = new TextDecoder('utf-8', { fatal: true });
const SOURCE_KEYS = [
  'docs/videos/lexicon.json',
  ...['series.json', 'video.json', 'claims.md', 'script.md', 'verify-1.md']
    .map(name => `docs/videos/${SLUG}/${name}`),
  `${SLUG}/auto.json`, `${SLUG}/review/narrative.json`,
  ...['hook', 'origin', 'idea', 'engine', 'turn', 'now']
    .map(name => `${SLUG}/story/chapters/${name}.json`),
  `${SLUG}/story/reviews/script-review.json`,
];
const OPTIONAL_KEYS = new Set([
  `docs/videos/${SLUG}/verify-1.md`,
  `${SLUG}/story/reviews/script-review.json`,
]);
const AUDIT_ROOT = `${SLUG}/story/recheck-audit`;
const RECEIPT_ROOT = `${SLUG}/manual-revisions`;
const LEXICON_ROOT = `docs/videos/${SLUG}/story-lexicon`;
// Historical A01 installation receipt, independently pinned by the original
// 80-link inspector and repeated in each later audit index. It predates the
// per-revision `index.revision` binding; no other unbound receipt is allowed.
const LEGACY_INSTALL_RECEIPT = Object.freeze({
  path: `${RECEIPT_ROOT}/2026-10-15T14-56-20-757Z-8b8398df-3afa-4828-8db0-1a7ca0a9b047/installation-receipt.json`,
  sha256: '24110fc8cc1665e9f6830db23e57cde12640c4bd947af3a42a25602528a266fd',
});

function hold(code) { throw new Error(code); }
function requireTrue(value, code) { if (!value) hold(code); }
function decode(buffer) {
  const nul = buffer.indexOf(0);
  return decoder.decode(nul < 0 ? buffer : buffer.subarray(0, nul));
}
function safePath(path) {
  requireTrue(typeof path === 'string' && path.length > 0
    && !path.startsWith('/') && !path.includes('\\') && !/[\x00-\x1f\x7f]/.test(path)
    && !/^[A-Za-z]:/.test(path), 'UNSAFE_TAR_PATH');
  const parts = path.split('/');
  requireTrue(parts.every(part => part && part !== '.' && part !== '..'), 'UNSAFE_TAR_PATH');
  return path;
}
function bound(item, code) {
  requireTrue(item && item.present === true && HASH.test(item.sha256)
    && Number.isSafeInteger(item.bytes) && item.bytes >= 0, code);
  return { sha256: item.sha256, bytes: item.bytes };
}
function validateRuntime(state) {
  const worker = state.worker;
  requireTrue(worker.release_sha === state.git_sha
    && /^[a-f0-9]{40,64}$/.test(worker.tools_video_tree_sha ?? '')
    && /^sha256:[a-f0-9]{64}$/.test(worker.worker_image_id ?? '')
    && HASH.test(worker.tools_video_runtime_inventory_sha256 ?? '')
    && Number.isSafeInteger(worker.tools_video_runtime_file_count)
    && worker.tools_video_runtime_file_count > 0
    && Array.isArray(worker.tools_video_runtime_files)
    && worker.tools_video_runtime_files.length === worker.tools_video_runtime_file_count,
  'RUNTIME_PIN_INCOMPLETE');
  const digest = createHash('sha256');
  let previous = null;
  let story = null;
  for (const item of worker.tools_video_runtime_files) {
    const path = safePath(item.path);
    const bytes = Buffer.from(path, 'utf8');
    if (previous !== null) {
      requireTrue(Buffer.compare(previous, bytes) < 0, 'RUNTIME_INVENTORY_UNSORTED');
    }
    previous = bytes;
    requireTrue(HASH.test(item.sha256) && Number.isSafeInteger(item.bytes)
      && item.bytes >= 0, 'RUNTIME_FILE_PIN_INVALID');
    digest.update(bytes);
    digest.update(Buffer.from([0]));
    digest.update(item.sha256, 'ascii');
    digest.update('\n');
    if (path === 'automation/story.mjs') story = item.sha256;
  }
  requireTrue(digest.digest('hex') === worker.tools_video_runtime_inventory_sha256,
    'RUNTIME_INVENTORY_HASH_MISMATCH');
  requireTrue(story && worker.story_mjs_sha256 === story
    && worker.public_filter_sha256 === story
    && worker.worker?.story_mjs?.sha256 === story,
  'RUNTIME_STORY_PIN_MISMATCH');
}
function octal(bytes, code) {
  requireTrue((bytes[0] & 0x80) === 0, code); // Reject GNU base-256 sizes.
  const value = bytes.toString('ascii').replace(/\0.*$/s, '').trim();
  requireTrue(!value || /^[0-7]+$/.test(value), code);
  const parsed = value ? parseInt(value, 8) : 0;
  requireTrue(Number.isSafeInteger(parsed), code);
  return parsed;
}
async function exact(handle, bytes, position) {
  const buffer = Buffer.alloc(bytes);
  for (let offset = 0; offset < bytes;) {
    const result = await handle.read(buffer, offset, bytes - offset, position + offset);
    requireTrue(result.bytesRead > 0, 'TRUNCATED_TAR');
    offset += result.bytesRead;
  }
  return buffer;
}
function headerAt(block) {
  const stored = octal(block.subarray(148, 156), 'TAR_CHECKSUM_FIELD');
  let sum = 0;
  for (let i = 0; i < BLOCK; i += 1) sum += i >= 148 && i < 156 ? 32 : block[i];
  requireTrue(sum === stored, 'TAR_CHECKSUM_MISMATCH');
  requireTrue(block.subarray(257, 262).toString('ascii') === 'ustar', 'TAR_FORMAT_UNSUPPORTED');
  const name = decode(block.subarray(0, 100));
  const prefix = decode(block.subarray(345, 500));
  return {
    name: prefix ? `${prefix}/${name}` : name,
    type: block[156] === 0 ? '0' : String.fromCharCode(block[156]),
    size: octal(block.subarray(124, 136), 'TAR_SIZE_FIELD'),
    linkname: decode(block.subarray(157, 257)),
  };
}
async function sha256File(path) {
  const hash = createHash('sha256');
  let bytes = 0;
  for await (const chunk of createReadStream(path)) { hash.update(chunk); bytes += chunk.length; }
  return { sha256: hash.digest('hex'), bytes };
}
async function inputFile(root, name) {
  const path = join(root, name);
  const info = await lstat(path);
  requireTrue(info.isFile() && !info.isSymbolicLink(), 'CAPTURE_INPUT_NOT_REGULAR');
  return path;
}

async function existing(path) {
  try { await lstat(path); return true; }
  catch (error) { if (error.code === 'ENOENT') return false; throw error; }
}

async function checkCaptureRoot(directory) {
  requireTrue(isAbsolute(directory), 'CAPTURE_PATH_NOT_ABSOLUTE');
  const root = resolve(directory);
  requireTrue((await realpath(root)).toLowerCase() === root.toLowerCase(),
    'CAPTURE_PATH_NOT_CANONICAL');
  for (let current = root; ; current = dirname(current)) {
    const info = await lstat(current);
    requireTrue(info.isDirectory() && !info.isSymbolicLink(), 'CAPTURE_PARENT_LINKED');
    requireTrue(!(await existing(join(current, '.git'))), 'CAPTURE_INSIDE_REPOSITORY');
    if (current === parse(current).root) break;
  }
  return root;
}

function expectedFromState(state) {
  const worker = state?.worker;
  requireTrue(worker?.slug === SLUG && worker.files && worker.audit_files
    && worker.lexicon_files
    && Array.isArray(worker.audit_events) && worker.audit_events.length >= 104,
  'HOST_INVENTORY_INCOMPLETE');
  requireTrue(JSON.stringify(Object.keys(worker.files).sort()) === JSON.stringify([...SOURCE_KEYS].sort()),
    'SOURCE_KEYS_UNEXPECTED');
  const expected = new Map();
  for (const name of SOURCE_KEYS) {
    const item = worker.files[name];
    if (item?.present === false && OPTIONAL_KEYS.has(name)) continue;
    expected.set(name, bound(item, 'SOURCE_HASH_MISSING'));
  }
  const lexiconNames = Object.keys(worker.lexicon_files);
  requireTrue(lexiconNames.includes(`${LEXICON_ROOT}/current.json`)
    && lexiconNames.some(name => name.startsWith(`${LEXICON_ROOT}/events/`))
    && lexiconNames.some(name => name.startsWith(`${LEXICON_ROOT}/versions/`)),
  'LEXICON_INVENTORY_INCOMPLETE');
  for (const name of lexiconNames) {
    safePath(name);
    const relative = name.startsWith(`${LEXICON_ROOT}/`)
      ? name.slice(LEXICON_ROOT.length + 1) : '';
    requireTrue(relative === 'current.json'
      || /^(events|versions)\/[a-f0-9]{64}\.json$/.test(relative),
    'LEXICON_FILE_PATH_UNEXPECTED');
    expected.set(name, bound(worker.lexicon_files[name], 'LEXICON_FILE_HASH_MISSING'));
  }
  const eventNames = new Set();
  for (const event of worker.audit_events) {
    const name = safePath(event.name);
    requireTrue(!name.includes('/') && !eventNames.has(name), 'AUDIT_EVENT_NAME_INVALID');
    eventNames.add(name);
    const index = worker.audit_files[`${name}/index.json`];
    const pinned = bound(event.index, 'AUDIT_INDEX_MISSING');
    requireTrue(index && index.sha256 === pinned.sha256 && index.bytes === pinned.bytes,
      'AUDIT_INDEX_PIN_MISMATCH');
  }
  for (const [relative, item] of Object.entries(worker.audit_files)) {
    safePath(relative);
    requireTrue(relative.endsWith('.json') && eventNames.has(relative.split('/')[0])
      && relative.split('/').length === 2, 'AUDIT_FILE_PATH_UNEXPECTED');
    expected.set(`${AUDIT_ROOT}/${relative}`, bound(item, 'AUDIT_FILE_HASH_MISSING'));
  }
  return { expected, eventNames, lexiconCount: lexiconNames.length };
}

async function readTar(tarPath, initialExpected) {
  const handle = await open(tarPath, 'r');
  try {
    const info = await handle.stat();
    requireTrue(info.size > 0 && info.size % BLOCK === 0, 'TAR_LENGTH_INVALID');
    const members = new Map();
    const directories = new Set();
    let position = 0;
    let pendingLongName = null;
    let zeroBlocks = 0;
    while (position < info.size) {
      const block = await exact(handle, BLOCK, position);
      position += BLOCK;
      if (block.every(byte => byte === 0)) {
        zeroBlocks += 1;
        if (zeroBlocks >= 2) {
          requireTrue(pendingLongName === null, 'ORPHAN_LONG_NAME');
          while (position < info.size) {
            const tail = await exact(handle, Math.min(64 * 1024, info.size - position), position);
            requireTrue(tail.every(byte => byte === 0), 'TAR_TRAILING_DATA');
            position += tail.length;
          }
          return { members, directories };
        }
        continue;
      }
      requireTrue(zeroBlocks === 0, 'TAR_SINGLE_ZERO_BLOCK');
      const header = headerAt(block);
      requireTrue(position + Math.ceil(header.size / BLOCK) * BLOCK <= info.size,
        'TAR_MEMBER_TRUNCATED');
      if (header.type === 'L') {
        requireTrue(pendingLongName === null && header.name === '././@LongLink'
          && header.size > 1 && header.size <= 8192 && !header.linkname,
        'TAR_LONG_NAME_INVALID');
        const data = await exact(handle, header.size, position);
        requireTrue(data.at(-1) === 0 && data.subarray(0, -1).indexOf(0) < 0,
          'TAR_LONG_NAME_INVALID');
        pendingLongName = decoder.decode(data.subarray(0, -1));
      } else {
        requireTrue(header.type === '0' || header.type === '5', 'TAR_MEMBER_TYPE_UNSUPPORTED');
        requireTrue(!header.linkname, 'TAR_LINK_REJECTED');
        const rawName = pendingLongName ?? header.name;
        pendingLongName = null;
        const name = safePath(header.type === '5' && rawName.endsWith('/')
          ? rawName.slice(0, -1) : rawName);
        requireTrue(!members.has(name) && !directories.has(name), 'TAR_DUPLICATE_MEMBER');
        if (header.type === '5') {
          requireTrue(header.size === 0 && rawName.endsWith('/'), 'TAR_DIRECTORY_INVALID');
          directories.add(name);
        } else {
          requireTrue(initialExpected.has(name)
            || name.startsWith(`${RECEIPT_ROOT}/`) && name.endsWith('/installation-receipt.json')
              && name.split('/').length === 4,
          'TAR_UNEXPECTED_FILE');
          const hash = createHash('sha256');
          const indexChunks = name.startsWith(`${AUDIT_ROOT}/`) && name.endsWith('/index.json')
            ? [] : null;
          requireTrue(indexChunks === null || header.size <= 2 * 1024 * 1024,
            'AUDIT_INDEX_TOO_LARGE');
          for (let offset = 0; offset < header.size;) {
            const chunk = await exact(handle, Math.min(64 * 1024, header.size - offset), position + offset);
            hash.update(chunk);
            if (indexChunks) indexChunks.push(chunk);
            offset += chunk.length;
          }
          members.set(name, { sha256: hash.digest('hex'), bytes: header.size,
            index: indexChunks ? Buffer.concat(indexChunks) : null });
        }
      }
      const padded = Math.ceil(header.size / BLOCK) * BLOCK;
      if (padded > header.size) {
        const padding = await exact(handle, padded - header.size, position + header.size);
        requireTrue(padding.every(byte => byte === 0), 'TAR_PADDING_NONZERO');
      }
      position += padded;
    }
    hold('TAR_END_MARKER_MISSING');
  } finally { await handle.close(); }
}

export async function verifyCapture(directory) {
  const root = await checkCaptureRoot(directory);
  const report = JSON.parse(await readFile(await inputFile(root, 'capture-report.json'), 'utf8'));
  requireTrue(report.slug === SLUG && report.status === 'HOLD'
    && report.production_adoption_allowed === false
    && report.capture_complete === true && report.files_captured === 7
    && ['HOLD', 'REVIEW_REQUIRED'].includes(report.operational_gate),
  'CAPTURE_REPORT_INVALID');
  const names = ['a01-source.tar', 'host-state-before.txt', 'host-state-after.txt',
    'db-before.json', 'db-after.json', 'budget-before.json', 'budget-after.json'];
  for (const name of names) {
    const actual = await sha256File(await inputFile(root, name));
    const recorded = report.files?.[name];
    requireTrue(recorded && actual.sha256 === recorded.sha256 && actual.bytes === recorded.bytes,
      'CAPTURE_FILE_HASH_MISMATCH');
  }
  const before = parseHostState(await readFile(join(root, 'host-state-before.txt'), 'utf8'));
  const after = parseHostState(await readFile(join(root, 'host-state-after.txt'), 'utf8'));
  requireTrue(JSON.stringify(before) === JSON.stringify(after), 'HOST_STATE_DRIFT');
  validateRuntime(before);
  const { expected, eventNames, lexiconCount } = expectedFromState(before);
  const { members, directories } = await readTar(join(root, 'a01-source.tar'), expected);
  const receipts = new Map();
  let installPins = 0;
  for (const name of eventNames) {
    const rel = `${AUDIT_ROOT}/${name}/index.json`;
    const member = members.get(rel);
    requireTrue(member?.index, 'AUDIT_INDEX_NOT_ARCHIVED');
    let index;
    try { index = JSON.parse(decoder.decode(member.index)); }
    catch { hold('AUDIT_INDEX_NOT_JSON'); }
    if (index.install_receipt_sha256 !== undefined) {
      requireTrue(index.install_receipt_sha256 === LEGACY_INSTALL_RECEIPT.sha256,
        'LEGACY_INSTALL_PIN_MISMATCH');
      installPins += 1;
    }
    if (index.revision !== undefined) {
      const revision = safePath(index.revision);
      const parts = revision.split('/');
      requireTrue(parts.length === 2 && parts[0] === 'manual-revisions'
        && HASH.test(index.revision_receipt_sha256 ?? ''), 'REVISION_BINDING_INVALID');
      const receiptPath = `${SLUG}/${revision}/installation-receipt.json`;
      requireTrue(!receipts.has(receiptPath)
        || receipts.get(receiptPath).sha256 === index.revision_receipt_sha256,
      'REVISION_RECEIPT_CONFLICTING_BINDING');
      receipts.set(receiptPath, { sha256: index.revision_receipt_sha256 });
    }
  }
  if (installPins > 0) {
    requireTrue(installPins === eventNames.size, 'LEGACY_INSTALL_PIN_INCOMPLETE');
    const legacy = members.get(LEGACY_INSTALL_RECEIPT.path);
    requireTrue(legacy && legacy.sha256 === LEGACY_INSTALL_RECEIPT.sha256,
      'LEGACY_INSTALL_RECEIPT_MISMATCH');
    requireTrue(!receipts.has(LEGACY_INSTALL_RECEIPT.path), 'LEGACY_INSTALL_RECEIPT_OVERLAP');
    receipts.set(LEGACY_INSTALL_RECEIPT.path,
      { sha256: LEGACY_INSTALL_RECEIPT.sha256 });
    expected.set(LEGACY_INSTALL_RECEIPT.path,
      { sha256: LEGACY_INSTALL_RECEIPT.sha256, bytes: legacy.bytes });
  }
  for (const [path, expectedReceipt] of receipts) {
    const actual = members.get(path);
    requireTrue(actual && actual.sha256 === expectedReceipt.sha256, 'REVISION_RECEIPT_MISMATCH');
    expected.set(path, { sha256: expectedReceipt.sha256, bytes: actual.bytes });
  }
  requireTrue(members.size === expected.size, 'TAR_MEMBER_SET_MISMATCH');
  for (const [name, pinned] of expected) {
    const actual = members.get(name);
    requireTrue(actual && actual.sha256 === pinned.sha256 && actual.bytes === pinned.bytes,
      'TAR_MEMBER_HASH_MISMATCH');
  }
  for (const dir of directories) {
    requireTrue([...expected.keys()].some(path => path.startsWith(`${dir}/`)),
      'TAR_UNEXPECTED_DIRECTORY');
  }
  return { audit_events: eventNames.size, files: members.size,
    receipts: receipts.size, lexicon_files: lexiconCount };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.length !== 4 || process.argv[2] !== '--capture') {
    process.stderr.write('Usage: node verify-archive.mjs --capture C:\\absolute\\capture-directory\n');
    process.exitCode = 2;
  } else {
    verifyCapture(process.argv[3]).then(result => {
      process.stdout.write(`A01 local archive verified: ${result.audit_events} audit events, `
        + `${result.files} files, ${result.receipts} revision receipts, `
        + `${result.lexicon_files} lexicon files. Adoption remains HOLD.\n`);
    }).catch(error => {
      process.stderr.write(`A01 local archive HOLD: ${error.message}\n`);
      process.exitCode = 2;
    });
  }
}
