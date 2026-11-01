import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, copyFileSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { ROOT, DIRECTORY, buildCatalog, readCatalog, select } from './catalog.mjs';
import { buildProgram, readProgram, episodeBrief } from './program.mjs';

test('the selection preserves all original ids and excludes historical duplicate rejections', () => {
  const { catalog, program } = readProgram();
  assert.equal(catalog.episodes.filter((entry) => entry.season !== null).length, 300);
  for (const id of ['B30', 'B32', 'B33', 'B38', 'T39', 'A26', 'A27', 'A30', 'A08', 'A09', 'A16']) {
    assert.equal(select(catalog, id).active, false);
    assert.throws(() => episodeBrief(catalog, program, id), /excluded/);
  }
  assert.equal(new Set(catalog.historical_first_pass_order).size, 24);
  for (const id of ['S26', 'S54', 'B26', 'A35', 'T54']) assert.throws(() => episodeBrief(catalog, program, id), /excluded by duration review/);
  assert.throws(() => select(catalog, 'NOT-A-TOPIC'), /Unknown topic/);
});

test('a new brief carries current rules but cannot masquerade as a production approval', () => {
  const { catalog, program } = readProgram();
  const result = episodeBrief(catalog, program, 'A68');
  assert.equal(result.status, 'EDITORIAL_BRIEF_NOT_IMPORT_READY');
  assert.equal(result.id, 'P01');
  assert.deepEqual(result.source_materials.map(({ id }) => id), ['A68', 'A45', 'S78']);
  assert.equal(result.current_profile.target_minutes, 15);
  assert.equal(result.current_profile.subtitles.burn_in, true);
  assert.equal(result.current_profile.production_synced, false);
  assert.equal(result.plan.chapters.reduce((sum, chapter) => sum + chapter.seconds, 0), 900);
  const added = result.source_materials.find(({ id }) => id === 'S78');
  assert.ok(added.source_material.record.limits.length);
  assert.ok(added.source_material.references[0].url.startsWith('https://'));
  const battery = episodeBrief(catalog, program, 'S17').source_materials[0];
  assert.deepEqual(battery.supplemental_candidates.map(({ id }) => id).sort(), ['A05', 'A51']);
  assert.ok(battery.supplemental_candidates.every((topic) => topic.record.facts_to_verify.length && topic.references.length));
  assert.equal(episodeBrief(catalog, program, 'P06').current_profile.target_minutes, 11);
  assert.equal(episodeBrief(catalog, program, 'P22').plan.tier, 'conditional');
});

test('changed legacy source facts fail closed instead of silently reusing an editorial decision', () => {
  const catalog = buildCatalog();
  const root = mkdtempSync(path.join(os.tmpdir(), 'stw-catalog-'));
  try {
    const files = new Set([...catalog.sources.map(({ file }) => file), ...['catalog.json', 'AUDIT.md', 'TOPICS.md', 'episodes.json', 'EPISODES.md', 'DURATION-AUDIT.md'].map((name) => `${DIRECTORY}/${name}`), 'tools/video/so-thats-why/episode-plan.mjs', ...catalog.episodes.flatMap((entry) => entry.source_references ?? [])]);
    for (const file of files) {
      mkdirSync(path.dirname(path.join(root, file)), { recursive: true });
      copyFileSync(path.join(ROOT, file), path.join(root, file));
    }
    readProgram(root);
    const episodePath = path.join(root, DIRECTORY, 'EPISODES.md');
    const originalEpisode = readFileSync(episodePath, 'utf8');
    writeFileSync(episodePath, `${originalEpisode}unreviewed duration change\n`);
    assert.throws(() => readProgram(root), /Episode document drift/);
    writeFileSync(episodePath, originalEpisode);
    const planPath = path.join(root, 'tools/video/so-thats-why/episode-plan.mjs');
    const originalPlan = readFileSync(planPath);
    writeFileSync(planPath, Buffer.concat([originalPlan, Buffer.from('\n// unreviewed plan change')]));
    assert.throws(() => readProgram(root), /Episode plan drift/);
    writeFileSync(planPath, originalPlan);
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

test('episode assembly fails closed on reused, omitted, excluded or over-budget material', () => {
  const { catalog, program } = readProgram();
  const draft = () => ({ plans: structuredClone(program.plans), outside: structuredClone(program.dispositions.filter((entry) => entry.disposition !== 'episode')) });
  let input = draft();
  input.plans[1].topics.push(input.plans[0].topics[0]);
  assert.throws(() => buildProgram(catalog, ROOT, input), /duplicate or excluded/);
  input = draft();
  input.outside.pop();
  assert.throws(() => buildProgram(catalog, ROOT, input), /exactly one duration decision/);
  input = draft();
  input.plans[0].topics.push('A08');
  assert.throws(() => buildProgram(catalog, ROOT, input), /duplicate or excluded/);
  input = draft();
  input.plans[0].chapters[1].seconds += 60;
  assert.throws(() => buildProgram(catalog, ROOT, input), /duration budget mismatch/);
});
