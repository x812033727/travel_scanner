// Ordinary Node/real-filesystem checks. Does not import the Mod adapter,
// start Claude, simulate its host, or establish native Mod compatibility.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import {
  copyFileSync, existsSync, mkdirSync, mkdtempSync, readFileSync,
  renameSync, statSync, writeFileSync,
} from 'node:fs';
import { dirname, isAbsolute, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  TARGETS, parseDirectoryArg, targetPath, classifyStat, classifyStatError, formatCheckedAt,
} from './delivery-check/hooks/delivery-logic.mjs';

const reportPath = process.argv[2];
if (!reportPath || !isAbsolute(reportPath)) {
  throw new Error('Provide a new absolute JSON report path. Evidence files are preserved.');
}
if (existsSync(reportPath)) throw new Error('Report already exists; choose a new report path.');
mkdirSync(dirname(reportPath), { recursive: true });
const evidenceDirectory = mkdtempSync(join(dirname(reportPath), 'delivery-logic-'));
const sourceDirectory = fileURLToPath(new URL('./delivery-fixtures/', import.meta.url));
const sourceHashes = Object.fromEntries(TARGETS.map(({ name }) => [name, hash(join(sourceDirectory, name))]));
const checks = [];
const snapshots = {};

function hash(path) {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}
function check(name, fn) {
  try {
    fn();
    checks.push({ name, passed: true });
  } catch (error) {
    checks.push({ name, passed: false, error: error.message });
  }
}
function fixture(name, files = ['article.md', 'sources.md']) {
  const directory = join(evidenceDirectory, name);
  mkdirSync(directory);
  for (const file of files) copyFileSync(join(sourceDirectory, file), join(directory, file));
  return directory;
}
function inspect(directory) {
  return TARGETS.map((target) => {
    const path = targetPath(directory, target.name);
    try {
      const stat = statSync(path);
      const kind = stat.isFile() ? 'file' : stat.isDirectory() ? 'dir' : 'other';
      return { name: target.name, path, ...classifyStat({ kind, size: stat.size }) };
    } catch (error) {
      return { name: target.name, path, ...classifyStatError(error) };
    }
  });
}
function statuses(rows) { return rows.map(({ status }) => status); }

check('Quoted absolute paths preserve Unicode, spaces, and literal backslashes', () => {
  for (const directory of ['C:\\練習 資料夾\\交稿', '/workspace/練習 資料夾', '/workspace/literal\\name']) {
    assert.deepEqual(parseDirectoryArg('"' + directory + '"'), { ok: true, directory });
  }
  assert.deepEqual(parseDirectoryArg(''), { ok: true, directory: null });
  assert.equal(targetPath('C:\\', 'article.md'), 'C:\\article.md');
  assert.equal(targetPath('/', 'article.md'), '/article.md');
  assert.equal(targetPath('/workspace/literal\\name/', 'article.md'), '/workspace/literal\\name/article.md');
});

check('Incomplete, relative, network, device, placeholder, and control-character inputs are rejected', () => {
  for (const raw of ['relative/path', '~', 'C:relative', '\\\\server\\share', '\\\\?\\C:\\data',
    '//server/share', '"C:\\unclosed', '""', '/workspace/<replace-me>', '/workspace/a\nb',
    '"C:\\one" "C:\\two"']) {
    assert.equal(parseDirectoryArg(raw).ok, false, JSON.stringify(raw));
  }
  for (const name of ['../secret', '..', '.', 'sub/file', 'sub\\file', 'a\nb']) {
    assert.throws(() => targetPath('/workspace/practice', name));
  }
});

check('Real missing file becomes present after adding the supplied material', () => {
  const directory = fixture('有空格的 練習資料夾');
  const preserved = ['article.md', 'sources.md'].map((name) => hash(join(directory, name)));
  snapshots.before = inspect(directory);
  assert.deepEqual(statuses(snapshots.before), ['exists', 'exists', 'missing']);
  copyFileSync(join(sourceDirectory, 'cover-brief.md'), join(directory, 'cover-brief.md'));
  snapshots.after = inspect(directory);
  assert.deepEqual(statuses(snapshots.after), ['exists', 'exists', 'exists']);
  assert.deepEqual(['article.md', 'sources.md'].map((name) => hash(join(directory, name))), preserved);
  assert.equal(hash(join(directory, 'cover-brief.md')), sourceHashes['cover-brief.md']);
});

check('An empty deliverable remains content-unreviewed', () => {
  const directory = fixture('empty-file');
  writeFileSync(join(directory, 'cover-brief.md'), '');
  snapshots.emptyFile = inspect(directory);
  assert.equal(statSync(join(directory, 'cover-brief.md')).size, 0);
  assert.equal(snapshots.emptyFile[2].status, 'exists');
  assert.equal(snapshots.emptyFile[2].label, '路徑存在，內容待審閱');
});

check('A wrong file name stays missing until the actual file is renamed', () => {
  const directory = fixture('wrong-name');
  copyFileSync(join(sourceDirectory, 'cover-brief.md'), join(directory, 'cover_brief.md'));
  snapshots.wrongName = inspect(directory);
  assert.equal(snapshots.wrongName[2].status, 'missing');
  renameSync(join(directory, 'cover_brief.md'), join(directory, 'cover-brief.md'));
  snapshots.correctedName = inspect(directory);
  assert.equal(snapshots.correctedName[2].status, 'exists');
});

check('A directory with the deliverable name is not called a valid document', () => {
  const directory = fixture('directory-instead-of-file');
  mkdirSync(join(directory, 'cover-brief.md'));
  snapshots.directoryInsteadOfFile = inspect(directory);
  assert.equal(snapshots.directoryInsteadOfFile[2].status, 'exists');
  assert.equal(snapshots.directoryInsteadOfFile[2].label, '路徑存在，內容待審閱');
});

check('Injected permission and unknown errors cannot be mistaken for missing files', () => {
  const injected = [
    { code: 'EACCES', message: 'Cannot access ENOENT.md' }, { code: 'EPERM' },
    { code: 'ENOTDIR' }, { message: 'ENOENT: no such file' }, new Error('ENOENT'), null,
  ];
  snapshots.injectedErrors = injected.map((error) => ({
    input: error instanceof Error ? { message: error.message } : error,
    ...classifyStatError(error),
  }));
  assert.ok(snapshots.injectedErrors.every(({ status }) => status === 'unknown'));
  assert.equal(classifyStatError({ code: 'ENOENT' }).status, 'missing');
  assert.equal(classifyStat(null).status, 'unknown');
  assert.equal(classifyStat({ kind: 'unrecognized' }).status, 'unknown');
});

check('Timestamps use actual supplied clock values and reject unusable values', () => {
  assert.equal(formatCheckedAt(0), '1970-01-01T00:00:00.000Z');
  for (const invalid of [null, '0', NaN, Infinity, 1e30]) assert.equal(formatCheckedAt(invalid), null);
});

check('All published starting materials remain byte-identical', () => {
  assert.deepEqual(Object.fromEntries(TARGETS.map(({ name }) => [name, hash(join(sourceDirectory, name))])), sourceHashes);
});

const report = {
  generatedAt: new Date().toISOString(),
  scope: 'ordinary Node pure-data helpers and real local fixture files only',
  claudeRuntimeInvoked: false,
  adapterImported: false,
  nativeModValidated: false,
  permissionErrors: 'injected values, not actual OS permission experiments',
  node: process.version, platform: process.platform, architecture: process.arch,
  evidenceDirectory,
  logicSha256: hash(fileURLToPath(new URL('./delivery-check/hooks/delivery-logic.mjs', import.meta.url))),
  harnessSha256: hash(fileURLToPath(import.meta.url)),
  fixtureSha256: sourceHashes,
  passed: checks.every(({ passed }) => passed), checks, snapshots,
};
writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n', { flag: 'wx' });
console.log(`${checks.filter(({ passed }) => passed).length}/${checks.length} checks passed; native Mod remains unverified.`);
console.log(reportPath);
process.exitCode = report.passed ? 0 : 1;
