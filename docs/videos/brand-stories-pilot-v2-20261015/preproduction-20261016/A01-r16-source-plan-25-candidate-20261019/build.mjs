// A01 source-plan metadata correction only. --check is read-only; --write writes here only.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.dirname(here);
const bridge = path.join(parent, 'A01-r12-snapshot104-six-chapter-bridge-20261018');
const r16 = path.join(parent, 'A01-editorial-candidate-20261019-r16');
const pins = {
  bridge_manifest: '17e44cdf2cdd8361d218b58b4574a7d52acf4898ba9c86fd64b58a59336982dc',
  bridge_series: 'cb93e3da3e5b25b9ed50135d07c499b0f5db2bd54169c9c5335a5613f5c276e1',
  bridge_assessment: 'c81b791bca0122be686e868a4f751a356af2d693a47c591e9a6410343dcc1998',
  r16_series: 'abeb7a283809a696c7ab8734ffa10ec83ec5494b7cf99584497e4e9cb3f2cafc',
  r16_video: '2c095cab5f92aa50e55e8035e4bdc8de4ca8b8bdba6c82f15a0ea009d5f19ff1',
  r16_claims: '3e16c3ccd57298abfd7a87fd7a1846a7cc7f422da488d91c281ffcd31e0a9e92',
  r16_source_map: 'dae0f774562967153aebf9786579c313cce9e32c8047dcf58893b63465def821',
};
const sl8 = 'https://www.sl8.com/journal/may24/journal_images/Chinook_2024_5-3-24_FINAL.pdf';
const stairs = 'https://travelpro.com/blogs/the-travelpro-blog/bring-this-not-that-duffel-bags-versus-rolling-suitcases';
const oldPublisher = 'Plath 2024 年校友刊自述（第 17 頁）';
const correctedPublisher = 'West Seattle High School Alumni Association《Chinook》';
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(`${JSON.stringify(value, null, 2)}\n`, 'utf8');
function regularFile(file) {
  const stat = fs.lstatSync(file);
  assert.ok(stat.isFile() && !stat.isSymbolicLink(), `regular file required: ${file}`);
  return fs.readFileSync(file);
}
function pinned(file, digest) {
  const bytes = regularFile(file);
  assert.equal(hash(bytes), digest, `pinned input changed: ${file}`);
  return bytes;
}
const parse = (bytes) => JSON.parse(bytes.toString('utf8'));
function uniqueByUrl(rows, label) {
  const out = new Map();
  for (const row of rows) {
    assert.ok(typeof row.url === 'string' && row.url.startsWith('https://') && !out.has(row.url), `${label}: duplicate or invalid URL`);
    out.set(row.url, row);
  }
  return out;
}
function claimRows(bytes) {
  const rows = [];
  for (const line of bytes.toString('utf8').split(/\r?\n/)) {
    if (!/^[a-z]\d+[a-z]?｜/.test(line)) continue;
    const fields = line.split('｜');
    assert.equal(fields.length, 6, 'r16 claim row shape');
    assert.equal(fields[5], 'PENDING', `claim review unexpectedly changed: ${fields[0]}`);
    rows.push({ id: fields[0], url: fields[2] });
  }
  assert.equal(rows.length, 78, 'r16 claim count');
  assert.equal(new Set(rows.map((row) => row.id)).size, 78, 'duplicate r16 claim ID');
  return rows;
}

function expectedOutputs() {
  const bridgeManifest = parse(pinned(path.join(bridge, 'manifest.json'), pins.bridge_manifest));
  assert.equal(bridgeManifest.status, 'OFFLINE_BRIDGE_HOLD_NO_HOST_OR_PAID_ACTION');
  assert.equal(bridgeManifest.outputs_sha256['candidate/series.json'], pins.bridge_series);
  const bridgeBytes = pinned(path.join(bridge, 'candidate', 'series.json'), pins.bridge_series);
  const assessment = parse(pinned(path.join(bridge, 'source-plan-assessment.json'), pins.bridge_assessment));
  const r16Series = parse(pinned(path.join(r16, 'candidate', 'series.json'), pins.r16_series));
  const video = parse(pinned(path.join(r16, 'candidate', 'video.json'), pins.r16_video));
  const claims = claimRows(pinned(path.join(r16, 'candidate', 'claims.md'), pins.r16_claims));
  const sourceMap = parse(pinned(path.join(r16, 'source-map.json'), pins.r16_source_map));

  const text = bridgeBytes.toString('utf8');
  const before = `"publisher": "${oldPublisher}"`;
  const after = `"publisher": "${correctedPublisher}"`;
  assert.equal(text.split(before).length, 2, 'index 23 publisher must occur exactly once');
  const seriesBytes = Buffer.from(text.replace(before, after), 'utf8');
  const sourcePlan = parse(seriesBytes);
  const original = parse(bridgeBytes);
  assert.equal(original.plan.sources[23].publisher, oldPublisher);
  assert.equal(sourcePlan.plan.sources[23].publisher, correctedPublisher);
  assert.equal(sourcePlan.plan.sources.length, 25);
  assert.equal(r16Series.plan.sources.length, 23);
  assert.equal(video.sources.length, 18);
  assert.equal(sourcePlan.plan.sources[23].url, sl8);
  assert.equal(sourcePlan.plan.sources[24].url, stairs);
  for (let index = 0; index < 23; index++) {
    assert.equal(sourcePlan.plan.sources[index].url, r16Series.plan.sources[index].url, `source order drift: ${index}`);
  }
  const reverted = structuredClone(sourcePlan);
  reverted.plan.sources[23].publisher = oldPublisher;
  assert.deepEqual(reverted, original, 'correction must change only source 23 publisher');
  assert.deepEqual(sourcePlan.plan.must_verify, r16Series.plan.must_verify, 'must_verify drift');
  assert.equal(assessment.old_plan_sources, 23);
  assert.equal(assessment.proposed_plan_sources, 25);
  assert.equal(assessment.r12_cited_public_sources, 18);

  const planByUrl = uniqueByUrl(sourcePlan.plan.sources, '25-source plan');
  const publicByUrl = uniqueByUrl(video.sources, '18 public sources');
  const mapByUrl = uniqueByUrl(sourceMap.source_index, 'r16 source map');
  assert.equal(mapByUrl.size, 18);
  assert.deepEqual([...mapByUrl.keys()].sort(), [...publicByUrl.keys()].sort(), 'r16 public/source-map URL set drift');
  assert.deepEqual([...publicByUrl.keys()].filter((url) => !r16Series.plan.sources.some((source) => source.url === url)).sort(), [sl8, stairs].sort(), '23-source gap drift');
  assert.ok([...publicByUrl.keys()].every((url) => planByUrl.has(url)), '25-source proposal still lacks a public citation');

  const claimById = new Map(claims.map((row) => [row.id, row]));
  const mappedClaims = new Map();
  for (const entry of sourceMap.source_index) for (const id of entry.claim_ids) {
    assert.ok(!mappedClaims.has(id), `duplicate source-map claim: ${id}`);
    mappedClaims.set(id, entry.url);
  }
  assert.equal(mappedClaims.size, 78);
  for (const row of claims) assert.equal(mappedClaims.get(row.id), row.url, `r16 claim/source-map drift: ${row.id}`);
  assert.equal(assessment.claim_source_rows.length, 78);
  const alignment = assessment.claim_source_rows.map((row) => {
    assert.equal(claimById.get(row.id)?.url, row.url, `r16/bridge claim URL drift: ${row.id}`);
    assert.equal(sourcePlan.plan.sources[row.proposed_plan_index]?.url, row.url, `plan index drift: ${row.id}`);
    assert.equal(video.sources[row.r12_public_index]?.url, row.url, `public index drift: ${row.id}`);
    return { id: row.id, plan_source_index: row.proposed_plan_index, public_source_index: row.r12_public_index, url: row.url };
  });
  assert.equal(new Set(alignment.map((row) => row.id)).size, 78);
  assert.deepEqual(alignment.filter((row) => row.id === 't7b').map((row) => [row.plan_source_index, row.public_source_index]), [[23, 16]]);
  assert.deepEqual(alignment.filter((row) => row.id === 'n14').map((row) => [row.plan_source_index, row.public_source_index]), [[24, 17]]);
  const uncited = sourcePlan.plan.sources.flatMap((source, index) => publicByUrl.has(source.url) ? [] : [index]);
  assert.deepEqual(uncited, [3, 4, 7, 9, 10, 14, 20], 'research-only plan source set drift');

  const evidence = {
    schema_version: 1,
    status: 'HOLD_OFFLINE_SOURCE_PLAN_METADATA_ONLY',
    counts: {
      live_snapshot104_plan_sources_reported: 13,
      editorial_plan_sources: 23,
      proposed_plan_sources: 25,
      cited_public_sources: 18,
      cited_claims: 78,
    },
    live_snapshot104_series_sha256_reported_not_recomputed_by_this_check: '68df2792fa98971eb805c8af773c8b3726801832cca03ed753a950bb56311cbc',
    appended_plan_sources: [23, 24].map((index) => ({
      index,
      public_index: index === 23 ? 16 : 17,
      url: sourcePlan.plan.sources[index].url,
      publisher: sourcePlan.plan.sources[index].publisher,
      kind: sourcePlan.plan.sources[index].kind,
      claim_ids: index === 23 ? ['t7b'] : ['n14'],
    })),
    research_only_plan_indices: uncited,
    claim_source_rows: alignment,
    direct_host_adoption_allowed: false,
    formal_script_review_receipt_issued: false,
    paid_media_allowed: false,
  };
  return {
    'candidate/series.json': seriesBytes,
    'source-alignment.json': json(evidence),
  };
}

function expectedManifest(outputs) {
  return {
    schema_version: 1,
    status: 'HOLD_OFFLINE_SOURCE_PLAN_METADATA_ONLY',
    input_sha256: pins,
    build_sha256: hash(regularFile(path.join(here, 'build.mjs'))),
    readme_sha256: hash(regularFile(path.join(here, 'README.md'))),
    outputs_sha256: Object.fromEntries(Object.entries(outputs).map(([name, bytes]) => [name, hash(bytes)])),
    correction_only: 'plan.sources[23].publisher',
    source_counts: { live_snapshot104_reported: 13, r16_editorial: 23, proposed: 25, cited_public: 18, claim_rows: 78 },
    direct_host_adoption_allowed: false,
    formal_script_review_receipt_issued: false,
    paid_media_allowed: false,
  };
}

const mode = process.argv[2] ?? '--check';
assert.ok(['--check', '--write'].includes(mode) && process.argv.length <= 3, 'usage: node build.mjs [--check|--write]');
const outputs = expectedOutputs();
const manifest = json(expectedManifest(outputs));
if (mode === '--write') {
  for (const [name, bytes] of Object.entries({ ...outputs, 'manifest.json': manifest })) {
    const target = path.join(here, name);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, bytes);
  }
} else {
  for (const [name, bytes] of Object.entries({ ...outputs, 'manifest.json': manifest })) {
    assert.deepEqual(regularFile(path.join(here, name)), bytes, `generated output drift: ${name}`);
  }
}
console.log(`A01 r16 25-source metadata ${mode}: PASS; 13 captured / 23 editorial / 25 proposed / 18 public; 78 claim mappings; HOLD`);
