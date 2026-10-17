import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const base = path.resolve(here, '../A01-round17-source-bound-candidate');
const chapterKeys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const read = (file) => fs.readFileSync(file);
const parse = (file) => JSON.parse(read(file).toString('utf8'));
const json = (value) => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const output = new Map();
const baseManifestBytes = read(path.join(base, 'manifest.json'));
const baseManifest = JSON.parse(baseManifestBytes.toString('utf8'));
const delta = parse(path.join(here, 'delta.json'));
assert.equal(delta.status, 'OFFLINE_METADATA_DELTA_PENDING_INDEPENDENT_REVIEW');
assert.equal(delta.base, 'A01-round17-source-bound-candidate');
assert.equal(delta.reconciliation_id, 'n14');
assert.equal(sha(baseManifestBytes), delta.base_manifest_sha256, 'frozen round17 manifest drift');
assert.equal(baseManifest.status, 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE');

for (const key of chapterKeys) {
  const name = `candidate/chapters/${key}.json`;
  const bytes = read(path.join(base, name));
  assert.equal(sha(bytes), baseManifest.candidate_chapter_sha256[key], `round17 ${name} drift`);
  output.set(name, bytes);
}
for (const [name, expected] of [
  ['candidate/series.json', baseManifest.candidate_series_sha256],
  ['validation.json', baseManifest.validation_sha256],
]) {
  const bytes = read(path.join(base, name));
  assert.equal(sha(bytes), expected, `round17 ${name} drift`);
  output.set(name, bytes);
}
const now = JSON.parse(output.get('candidate/chapters/now.json').toString('utf8'));
const activeClaim = now.claims.find(({ id }) => id === 'n14');
assert.ok(activeClaim && activeClaim.source === null && activeClaim.fact === null && activeClaim.verdict === 'PENDING');
assert.equal(now.scenes.find(({ id }) => id === 'now-06').lines.find(({ id }) => id === 'tszs').text,
  '輪子能幫忙移動，卻不會減掉重量。');
const baseValidation = JSON.parse(output.get('validation.json').toString('utf8'));
assert.equal(baseValidation.scene_count, 79);
assert.equal(baseValidation.line_count, 108);
assert.equal(baseValidation.lint_errors.length, 0);
assert.equal(baseValidation.cute_errors.length, 0);
assert.equal(baseValidation.narration_sha256, baseManifest.narration_sha256);

const baseMapBytes = read(path.join(base, 'source-map.json'));
assert.equal(sha(baseMapBytes), baseManifest.source_map_sha256, 'round17 source map drift');
const baseMap = JSON.parse(baseMapBytes.toString('utf8'));
assert.equal(baseMap.lines.length, 27);
const activeRow = baseMap.lines.find(({ line_id }) => line_id === 'tszs');
assert.ok(activeRow && activeRow.claim_id === 'n14' && activeRow.source_index === null);
assert.equal(activeRow.verdict, 'PENDING_INDEPENDENT_REVIEW');
const sourceMap = structuredClone(baseMap);
const rows = sourceMap.inherited_claim_reconciliation.filter(({ id }) => id === delta.reconciliation_id);
assert.equal(rows.length, 1);
const row = rows[0];
assert.equal(row.active, true);
assert.equal(row.oldScene, 'now-06');
assert.equal(row.source, delta.prior_source.source);
assert.equal(row.source_url, delta.prior_source.source_url);
assert.equal(row.current.claim, activeRow.text);
assert.equal(row.current.verdict, 'PENDING');
assert.equal(row.historical.verdict, 'NOT FOUND');
const oldHistorical = structuredClone(row.historical);
const oldCurrent = structuredClone(row.current);
const priorPin = row.pin;
assert.match(priorPin, /ABC News 2010/);
row.prior_source = { ...delta.prior_source, pin: priorPin };
row.source = null;
row.source_url = null;
row.pin = delta.current_pin;
row.note = delta.current_note;
row.current = { ...oldCurrent, source: null, source_url: null, note: delta.current_claim_note };
assert.deepEqual(row.historical, oldHistorical, 'Round11 historical verdict drift');
assert.deepEqual(sourceMap.lines, baseMap.lines, 'active source matrix drift');
assert.ok(json(sourceMap.lines).equals(json(baseMap.lines)), 'active source rows byte drift');
assert.deepEqual(sourceMap.inherited_claim_reconciliation.filter(({ id }) => id !== 'n14'),
  baseMap.inherited_claim_reconciliation.filter(({ id }) => id !== 'n14'), 'other provenance drift');
assert.equal(row.prior_source.source, 6);
assert.equal(row.current.source, activeClaim.source);
assert.equal(row.current.source_url, null);
assert.equal(row.source, activeRow.source_index);
output.set('source-map.json', json(sourceMap));

const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  slug: baseManifest.slug,
  base_round17_manifest_sha256: delta.base_manifest_sha256,
  delta_sha256: sha(read(path.join(here, 'delta.json'))),
  candidate_chapter_sha256: Object.fromEntries(chapterKeys.map((key) => [key, sha(output.get(`candidate/chapters/${key}.json`))])),
  candidate_series_sha256: sha(output.get('candidate/series.json')),
  source_map_sha256: sha(output.get('source-map.json')),
  validation_sha256: sha(output.get('validation.json')),
  narration_sha256: baseManifest.narration_sha256,
  active_source_rows_identical_to_round17: true,
  n14_current_source: null,
  n14_historical_source: 6,
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
console.log(JSON.stringify({ action, status: manifest.status, scenes: baseValidation.scene_count,
  lines: baseValidation.line_count, changed_spoken_lines: 0,
  changed_active_source_rows: 0, n14_current_source: row.current.source,
  n14_historical_source: row.prior_source.source }));
