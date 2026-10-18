// A01-only offline r18: tighten the 1993 retail claim and security hook.
// Pins r17 and its corrected proposed 25-source plan; creates only new outputs here.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r17 = path.resolve(here, '../A01-editorial-candidate-20261019-r17');
const sources25 = path.resolve(here, '../A01-r16-source-plan-25-candidate-20261019');
const expected = {
  r17Manifest: 'f0603ac804089797bdd1c083ee006306618d19d67b58e621058db026eee02805',
  sources25Manifest: '61257b4687f232fa8a963332f4c8fab988a83565ce4f08615c5e0ceeac7d449a',
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const readPinned = (dir, name) => fs.readFileSync(path.join(dir, name));
const verifyPinned = (dir, expectedManifest) => {
  assert.equal(sha(readPinned(dir, 'manifest.json')), expectedManifest, 'pinned manifest drift ' + dir);
  const manifest = JSON.parse(readPinned(dir, 'manifest.json'));
  for (const [name, digest] of Object.entries(manifest.outputs_sha256)) {
    assert.equal(sha(readPinned(dir, name)), digest, 'pinned output drift ' + name);
  }
  assert.equal(sha(readPinned(dir, 'build.mjs')), manifest.build_sha256, 'pinned builder drift');
  assert.equal(sha(readPinned(dir, 'README.md')), manifest.readme_sha256, 'pinned README drift');
  return manifest;
};
const r17Manifest = verifyPinned(r17, expected.r17Manifest);
verifyPinned(sources25, expected.sources25Manifest);

const before = JSON.parse(readPinned(r17, 'candidate/video.json'));
const video = structuredClone(before);
assert.equal(video.slug, 'story-rolling-suitcase-v2');
assert.deepEqual(video.target_minutes, [7, 8]);
assert.equal(video.scenes.length, 65);
assert.equal(video.sources.length, 18);
const scene = (id) => {
  const matches = video.scenes.filter((item) => item.id === id);
  assert.equal(matches.length, 1, 'scene drift ' + id);
  return matches[0];
};
const retail = scene('now-1993-retail');
assert.deepEqual(retail.claims, ['n56']);
assert.deepEqual(retail.lines, [
  { id: 'r11n01', text: 'Travelpro 起初靠郵購賣輪箱。' },
  { id: 'r3n03', text: '1993 年，記者寫道：百貨已有四家品牌的輪子登機箱可買。' },
]);
retail.lines[1].text = '1993 年，記者寫道：主要百貨或行李專門店，已有四家品牌的輪子登機箱可選。';
const security = scene('turn-security-question');
const securityLine = security.lines.find((line) => line.id === 'r6t01');
assert.ok(securityLine, 'security hook missing');
assert.equal(securityLine.text, '如果把兩樣東西鎖在一起，安檢員會讓它過嗎？');
securityLine.text = '如果把兩樣東西鎖在一起，安檢員會怎麼回答？';
const securityPayoff = scene('turn-07c').lines.find((line) => line.id === 'r13t02');
assert.equal(securityPayoff?.text, '安檢員聽完，只回了一句：「好。」');

const oldClaims = readPinned(r17, 'candidate/claims.md').toString('utf8');
const oldClaimLines = oldClaims.replace(/\r\n/g, '\n').split('\n');
const oldRows = oldClaimLines.filter((line) => /^[a-z]\d+[a-z]?｜/.test(line));
assert.equal(oldRows.length, 73);
const oldN56 = 'n56｜Dash 在 1993 年記載 Travelpro 起初以郵購販售，當時已有多個品牌的輪子登機箱可在主要百貨或行李專門店選購；這是可買到的通路證據，不推算銷量｜https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html｜2026-10-18｜now-1993-retail｜PENDING';
const newN56 = 'n56｜Dash 在 1993 年記載 Travelpro 起初以郵購販售；她實測的四家品牌輪子登機箱型號當時可在主要百貨或行李專門店選購，未聲稱四家皆在每一家百貨同時上架，也不推算銷量｜https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html｜2026-10-18｜now-1993-retail｜PENDING';
assert.equal(oldClaimLines.filter((line) => line === oldN56).length, 1, 'n56 provenance drift');
const claims = Buffer.from(oldClaimLines.map((line) => line === oldN56 ? newN56 : line).join('\n'));
const claimRows = claims.toString('utf8').split('\n').filter((line) => /^[a-z]\d+[a-z]?｜/.test(line));
assert.equal(claimRows.length, 73);
const claimEntries = claimRows.map((row) => row.split('｜'));
const sceneByClaim = new Map(video.scenes.flatMap((item) => (item.claims ?? []).map((id) => [id, item.id])));
assert.equal(sceneByClaim.size, 73, 'claim anchors not unique');
assert.deepEqual(new Set(claimEntries.map((cells) => cells[0])), new Set(sceneByClaim.keys()), 'claim rows / anchors differ');
for (const cells of claimEntries) {
  assert.equal(cells.length, 6, 'malformed claim row ' + cells[0]);
  assert.equal(cells[4], sceneByClaim.get(cells[0]), 'claim scene drift ' + cells[0]);
  assert.equal(cells[5], 'PENDING', 'no formal verdict may be inherited');
}
const claimUrlById = new Map(claimEntries.map((cells) => [cells[0], cells[2]]));
assert.deepEqual(new Set(claimEntries.map((cells) => cells[2])), new Set(video.sources.map((source) => source.url)));
assert.equal(claimUrlById.get('n56'), 'https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html');
assert.deepEqual(video.sources, before.sources, '18 public sources changed');
assert.deepEqual(video.scenes.map((item) => item.id), before.scenes.map((item) => item.id), 'scene order changed');
assert.deepEqual(video.scenes.flatMap((item) => item.lines.map((line) => line.id)),
  before.scenes.flatMap((item) => item.lines.map((line) => line.id)), 'line IDs changed');
assert.deepEqual(video.loops, before.loops, 'setup/payoff IDs changed');
for (let i = 0; i < video.scenes.length; i++) {
  const oldScene = before.scenes[i];
  const newScene = video.scenes[i];
  if (oldScene.id === 'now-1993-retail') {
    assert.deepEqual({ ...newScene, lines: oldScene.lines }, oldScene, 'unexpected retail change');
  } else if (oldScene.id === 'turn-security-question') {
    assert.deepEqual({ ...newScene, lines: oldScene.lines }, oldScene, 'unexpected security change');
  } else {
    assert.deepEqual(newScene, oldScene, 'unexpected scene change ' + oldScene.id);
  }
}

const priorMap = JSON.parse(readPinned(r17, 'source-map.json'));
const sourceMap = {
  status: 'HOLD_UNREVIEWED_R18_SOURCE_MAP',
  derives_from_r17_manifest_sha256: expected.r17Manifest,
  r17_review_not_inherited: true,
  source_index: priorMap.source_index,
  changed_line_ids: ['r6t01', 'r3n03'],
  changed_claim_ids: ['n56'],
  host_source_guard: 'HOLD: r18 has 73 PENDING claims; fresh worker IDs, verifier/listener/two-reader review and formal receipt are required after host six-chapter adoption.',
};
assert.deepEqual(sourceMap.source_index.map((entry) => entry.url), priorMap.source_index.map((entry) => entry.url));
const mappedIds = sourceMap.source_index.flatMap((entry) => entry.claim_ids);
assert.equal(mappedIds.length, 73);
assert.deepEqual(new Set(mappedIds), new Set(claimUrlById.keys()));
for (const entry of sourceMap.source_index) {
  for (const id of entry.claim_ids) assert.equal(claimUrlById.get(id), entry.url, 'source-map URL drift ' + id);
}
const priorAlignment = JSON.parse(readPinned(r17, 'source-alignment.json'));
const sourcePlan = JSON.parse(readPinned(sources25, 'candidate/series.json'));
assert.equal(sourcePlan.plan.sources.length, 25);
const alignment = structuredClone(priorAlignment);
alignment.status = 'HOLD_UNREVIEWED_R18_73_CLAIM_ALIGNMENT';
alignment.derives_from_r17_manifest_sha256 = expected.r17Manifest;
alignment.r17_claim_alignment_not_inherited = true;
alignment.changed_claim_ids = ['n56'];
assert.equal(alignment.claim_source_rows.length, 73);
assert.deepEqual(new Set(alignment.claim_source_rows.map((row) => row.id)), new Set(claimUrlById.keys()));
for (const row of alignment.claim_source_rows) {
  assert.equal(row.url, claimUrlById.get(row.id), 'alignment URL drift ' + row.id);
  assert.equal(sourcePlan.plan.sources[row.plan_source_index].url, row.url, 'plan URL drift ' + row.id);
  assert.equal(video.sources[row.public_source_index].url, row.url, 'public URL drift ' + row.id);
}
assert.equal(alignment.direct_host_adoption_allowed, false);
assert.equal(alignment.formal_script_review_receipt_issued, false);
assert.equal(alignment.paid_media_allowed, false);

const [{ screenplay }, { estimateTimeline, spokenUnits }, { lintVideo }, { cuteStoryVisualProblems }] = await Promise.all([
  import(pathToFileURL(path.join(repo, 'tools/video/core/screenplay.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/core/timeline.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/core/lint.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/automation/story.mjs'))),
]);
assert.equal(screenplay(before), readPinned(r17, 'candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r17 script drift');
const script = Buffer.from(screenplay(video));
const series = JSON.parse(readPinned(r17, 'candidate/series.json'));
assert.equal(series.plan.sources.length, 23, 'candidate source count drift');
const lexicon = JSON.parse(readPinned(r17, 'candidate/lexicon.json'));
const lintContext = {
  lexicon,
  brief: fs.readFileSync(path.join(here, '../A01-story-depth-candidate-20261018-r4/base/brief.md'), 'utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(video, lintContext);
const lintAt300 = lintVideo(video, { ...lintContext, cpm: 300 });
const cute = cuteStoryVisualProblems(video);
assert.equal(lint.errors.length, 0, 'lint errors ' + JSON.stringify(lint.errors));
assert.equal(lintAt300.errors.length, 0, '300-CPM lint errors ' + JSON.stringify(lintAt300.errors));
assert.equal(cute.length, 0, 'cute visual errors ' + JSON.stringify(cute));
const seconds = Object.fromEntries([250, 275, 300].map((cpm) =>
  [cpm, Number((estimateTimeline(video, cpm).total_frames / 30).toFixed(1))]));
assert.ok(seconds[300] >= 420 && seconds[300] <= 480, 'paper body out of owner range');
const lines = video.scenes.flatMap((item) => item.lines);
assert.equal(lines.length, 77);
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_PENDING_R18_REVIEW',
  target_body_seconds: [420, 480],
  scenes: video.scenes.length,
  lines: lines.length,
  claims: claimEntries.length,
  loops: video.loops.length,
  spoken_units: lines.reduce((sum, line) => sum + spokenUnits(line.text), 0),
  estimated_body_seconds_not_tts: seconds,
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_errors_at_300_cpm: lintAt300.errors,
  cute_visual_errors: cute,
  public_sources: video.sources.length,
  candidate_plan_sources: series.plan.sources.length,
  proposed_plan_sources: sourcePlan.plan.sources.length,
  source_index_matches_claims: true,
  measured_tts_and_cut: 'NOT_RUN',
  independent_full_r18_review: 'NOT_RUN',
  six_chapter_host_bridge: 'NOT_INSTALLED_OR_FORMALLY_REVIEWED',
  worker_claim_id_and_source_merge: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  host_import_or_paid_media: 'NOT_RUN',
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', readPinned(r17, 'candidate/series.json')],
  ['candidate/lexicon.json', readPinned(r17, 'candidate/lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['source-alignment.json', json(alignment)],
  ['validation.json', json(validation)],
  ['plan-source-addition.json', readPinned(r17, 'plan-source-addition.json')],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE',
  slug: video.slug,
  derives_from_r17_manifest_sha256: expected.r17Manifest,
  derives_from_r16_source_plan_manifest_sha256: expected.sources25Manifest,
  r17_review_not_inherited: true,
  source_snapshot: r17Manifest.source_snapshot,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r17_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r18');
  if (action === '--write') {
    assert.ok(!fs.existsSync(file), 'r18 output exists; do not overwrite ' + name);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes, { flag: 'wx' });
  } else {
    assert.ok(fs.existsSync(file), 'missing output ' + name);
    assert.ok(fs.readFileSync(file).equals(bytes), 'stale output ' + name);
  }
}
console.log(JSON.stringify({ action, status: validation.status, scenes: validation.scenes, lines: validation.lines,
  claims: validation.claims, public_sources: validation.public_sources, spoken_units: validation.spoken_units,
  seconds_250: seconds[250], seconds_275: seconds[275], seconds_300: seconds[300],
  lint_errors: lint.errors.length, cute_errors: cute.length }));
