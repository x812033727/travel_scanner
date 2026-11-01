import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, copyFileSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { ROOT, DIRECTORY, buildCatalog, readCatalog, select, brief } from './catalog.mjs';

test('the selection preserves all original ids and excludes historical duplicate rejections', () => {
  const catalog = readCatalog();
  assert.equal(catalog.episodes.filter((entry) => entry.season !== null).length, 300);
  for (const id of ['B30', 'B32', 'B33', 'B38', 'T39', 'A26', 'A27', 'A30', 'A08', 'A09', 'A16']) {
    assert.equal(select(catalog, id).active, false);
    assert.throws(() => brief(catalog, id), /excluded/);
  }
  assert.equal(new Set(catalog.first_batch).size, 24);
  assert.ok(catalog.first_batch.every((id) => select(catalog, id).active));
  assert.throws(() => select(catalog, 'NOT-A-TOPIC'), /Unknown topic/);
});

test('a new brief carries current rules but cannot masquerade as a production approval', () => {
  const result = brief(readCatalog(), 'S76');
  assert.equal(result.status, 'EDITORIAL_BRIEF_NOT_IMPORT_READY');
  assert.equal(result.current_profile.target_minutes, 13);
  assert.equal(result.current_profile.subtitles.burn_in, true);
  assert.equal(result.current_profile.production_synced, false);
  assert.equal(result.chapter_budget_seconds.reduce((sum, seconds) => sum + seconds, 0), 780);
  assert.ok(result.source_material.record.limits.length);
  assert.ok(result.source_material.references[0].url.startsWith('https://'));
  const battery = brief(readCatalog(), 'S17');
  assert.deepEqual(battery.merged_topics.map(({ id }) => id).sort(), ['A05', 'A51']);
  assert.ok(battery.merged_topics.every((topic) => topic.record.facts_to_verify.length && topic.references.length));
});

test('changed legacy source facts fail closed instead of silently reusing an editorial decision', () => {
  const catalog = buildCatalog();
  const root = mkdtempSync(path.join(os.tmpdir(), 'stw-catalog-'));
  try {
    const files = new Set([...catalog.sources.map(({ file }) => file), `${DIRECTORY}/catalog.json`, `${DIRECTORY}/AUDIT.md`, `${DIRECTORY}/TOPICS.md`, ...catalog.episodes.flatMap((entry) => entry.source_references ?? [])]);
    for (const file of files) {
      mkdirSync(path.dirname(path.join(root, file)), { recursive: true });
      copyFileSync(path.join(ROOT, file), path.join(root, file));
    }
    readCatalog(root);
    const auditPath = path.join(root, DIRECTORY, 'AUDIT.md');
    const originalAudit = readFileSync(auditPath, 'utf8');
    writeFileSync(auditPath, `${originalAudit}edited outside the catalog\n`);
    assert.throws(() => readCatalog(root), /Audit drift/);
    writeFileSync(auditPath, originalAudit);
    const reviewedFile = path.join(root, catalog.episodes.find((entry) => entry.source_references?.length).source_references[0]);
    const reviewedBytes = readFileSync(reviewedFile);
    writeFileSync(reviewedFile, Buffer.concat([reviewedBytes, Buffer.from('\nchanged source package')]));
    assert.throws(() => readCatalog(root), /Catalog drift/);
    writeFileSync(reviewedFile, reviewedBytes);
    const file = path.join(root, 'docs/videos/so-thats-why/episodes.json');
    const source = JSON.parse(readFileSync(file, 'utf8'));
    source.episodes[0].answer = 'changed fact';
    writeFileSync(file, JSON.stringify(source));
    assert.throws(() => readCatalog(root), /Catalog drift/);
  } finally {
    assert.equal(path.dirname(path.resolve(root)), path.resolve(os.tmpdir()));
    assert.ok(path.basename(root).startsWith('stw-catalog-'));
    rmSync(root, { recursive: true, force: true });
  }
});
