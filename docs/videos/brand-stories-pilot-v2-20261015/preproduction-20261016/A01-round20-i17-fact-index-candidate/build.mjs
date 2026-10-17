import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const base = path.resolve(here, '../A01-round19-origin-year-repeat-candidate');
const chapterKeys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const read = (file) => fs.readFileSync(file);
const parse = (file) => JSON.parse(read(file).toString('utf8'));
const json = (value) => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const output = new Map();

const baseManifestBytes = read(path.join(base, 'manifest.json'));
const baseManifest = JSON.parse(baseManifestBytes.toString('utf8'));
const deltaBytes = read(path.join(here, 'delta.json'));
const delta = JSON.parse(deltaBytes.toString('utf8'));
assert.equal(delta.status, 'OFFLINE_METADATA_DELTA_PENDING_INDEPENDENT_REVIEW');
assert.equal(delta.base, 'A01-round19-origin-year-repeat-candidate');
assert.equal(sha(baseManifestBytes), delta.base_manifest_sha256, 'frozen round19 manifest drift');
assert.equal(baseManifest.status, 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE');
assert.deepEqual([delta.chapter, delta.scene_id, delta.line_id, delta.claim_id,
  delta.source_index, delta.fact_index], ['idea', 'idea-07b', '76ur', 'i17', 6, 4]);

for (const key of chapterKeys) {
  const name = `candidate/chapters/${key}.json`;
  const bytes = read(path.join(base, name));
  assert.equal(sha(bytes), baseManifest.candidate_chapter_sha256[key], `round19 ${name} drift`);
  output.set(name, bytes);
}
const idea = parse(path.join(base, 'candidate/chapters/idea.json'));
const claim = idea.claims.find(({ id }) => id === delta.claim_id);
const line = idea.scenes.find(({ id }) => id === delta.scene_id)?.lines.find(({ id }) => id === delta.line_id);
assert.ok(claim && line);
assert.equal(claim.scene, delta.scene_id);
assert.equal(claim.claim, line.text);
assert.equal(claim.source, delta.source_index);
assert.equal(claim.fact, delta.fact_index);
assert.equal(claim.verdict, 'PENDING');

const seriesBytes = read(path.join(base, 'candidate/series.json'));
assert.equal(sha(seriesBytes), baseManifest.candidate_series_sha256, 'round19 series drift');
const series = JSON.parse(seriesBytes.toString('utf8'));
assert.ok(series.plan.must_verify[delta.fact_index].sources.includes(delta.source_index));
const sourceUrl = series.plan.sources[delta.source_index].url;
assert.equal(sourceUrl, 'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469');
output.set('candidate/series.json', seriesBytes);

const validationBytes = read(path.join(base, 'validation.json'));
assert.equal(sha(validationBytes), baseManifest.validation_sha256, 'round19 validation drift');
const validation = JSON.parse(validationBytes.toString('utf8'));
assert.equal(validation.scene_count, 79);
assert.equal(validation.line_count, 108);
assert.equal(validation.narration_sha256, baseManifest.narration_sha256);
assert.equal(validation.lint_errors.length, 0);
assert.equal(validation.cute_errors.length, 0);
assert.equal(validation.independent_full_script_review, 'NOT_RUN_FOR_ROUND19');
output.set('validation.json', validationBytes);

const baseMapBytes = read(path.join(base, 'source-map.json'));
assert.equal(sha(baseMapBytes), baseManifest.source_map_sha256, 'round19 source map drift');
const sourceMap = JSON.parse(baseMapBytes.toString('utf8'));
assert.equal(sourceMap.lines.length, 27);
const oldMap = structuredClone(sourceMap);
const matches = sourceMap.lines.filter(({ line_id }) => line_id === delta.line_id);
assert.equal(matches.length, 1);
const row = matches[0];
assert.deepEqual([row.chapter, row.scene_id, row.claim_id, row.source_index],
  [delta.chapter, delta.scene_id, delta.claim_id, delta.source_index]);
assert.equal(row.text, line.text);
assert.equal(row.source_url, sourceUrl);
assert.equal(row.verdict, 'PENDING_INDEPENDENT_REVIEW');
assert.equal(Object.hasOwn(row, 'fact_index'), false, 'fact_index already present');
row.fact_index = delta.fact_index;
const mapWithOldValue = structuredClone(sourceMap);
delete mapWithOldValue.lines.find(({ line_id }) => line_id === delta.line_id).fact_index;
assert.deepEqual(mapWithOldValue, oldMap, 'unrelated source map fields drift');
assert.deepEqual(sourceMap.inherited_claim_reconciliation,
  oldMap.inherited_claim_reconciliation, 'historical verdict or n14 provenance drift');
assert.equal(new Set(sourceMap.lines.map(({ line_id }) => line_id)).size, 27);
output.set('source-map.json', json(sourceMap));

const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  slug: baseManifest.slug,
  base_round19_manifest_sha256: delta.base_manifest_sha256,
  delta_sha256: sha(deltaBytes),
  candidate_chapter_sha256: Object.fromEntries(chapterKeys.map((key) => [key, sha(output.get(`candidate/chapters/${key}.json`))])),
  candidate_series_sha256: sha(output.get('candidate/series.json')),
  source_map_sha256: sha(output.get('source-map.json')),
  validation_sha256: sha(output.get('validation.json')),
  narration_sha256: baseManifest.narration_sha256,
  changed_spoken_lines: 0,
  changed_active_source_rows: 1,
  active_source_rows: 27,
  i17_fact_index: delta.fact_index,
  inherited_round9_narrative_passed: false,
  authorizes_host_install_or_paid_media: false,
};
output.set('manifest.json', json(manifest));

const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of output) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(`${here}${path.sep}`), `unsafe output path ${name}`);
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), `missing generated ${name}`);
    assert.ok(read(file).equals(bytes), `stale generated ${name}`);
  }
}
console.log(JSON.stringify({ action, status: manifest.status,
  scenes: validation.scene_count, lines: validation.line_count,
  changed_spoken_lines: 0, changed_active_source_rows: 1,
  active_source_rows: 27, i17_fact_index: row.fact_index,
  narration_sha256: manifest.narration_sha256 }));
