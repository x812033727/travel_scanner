// A01-only offline r19: bind the security-unloading reveal to its own cited claim.
// Pins r18 and its corrected proposed 25-source plan; creates only new outputs here.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r18 = path.resolve(here, '../A01-editorial-candidate-20261019-r18');
const sources25 = path.resolve(here, '../A01-r16-source-plan-25-candidate-20261019');
const expected = {
  r18Manifest: '6228fa78cbb686e01e10a5b1053204a53b71f248fcda93ae364c501cce518b4c',
  r18BlindReview: '5ff24d81de5d02d712a1cac810fccdfbd2de466e12eb76433ead6e55d4743222',
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
const r18Manifest = verifyPinned(r18, expected.r18Manifest);
assert.equal(sha(readPinned(r18, 'blind-story-review-20261019.md')), expected.r18BlindReview,
  'pinned r18 blind review drift');
verifyPinned(sources25, expected.sources25Manifest);

const before = JSON.parse(readPinned(r18, 'candidate/video.json'));
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
const reveal = scene('turn-06');
assert.deepEqual(reveal.claims, [], 'r18 reveal unexpectedly has a claim');
assert.deepEqual(reveal.lines, [{
  id: 'iu9y',
  text: '原來，箱子用彈力繩綁在笨重的金屬推車上；旅客得解開繩子，再把箱子卸下來。',
}]);
reveal.claims = ['t46'];

const oldClaims = readPinned(r18, 'candidate/claims.md').toString('utf8');
const oldClaimLines = oldClaims.replace(/\r\n/g, '\n').split('\n');
const oldRows = oldClaimLines.filter((line) => /^[a-z]\d+[a-z]?｜/.test(line));
assert.equal(oldRows.length, 73);
const oldT5 = 't5｜Plath 受訪回憶在安檢排隊，看見前方旅客解彈力繩、將箱子從外置金屬推車卸下；與 Emmer 未標年份的草圖記憶無法排定先後｜https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603｜2026-09-28｜turn-05｜PENDING';
const newT46 = 't46｜2012 年 USA TODAY 對 Plath 的受訪報導敘述，他在安檢隊伍看到前方旅客費力解開把箱子綁在笨重金屬推車上的彈力繩，將箱子從推車取下；此為受訪報導的回憶，非專利獨立證實該旅客的動作｜https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603｜2026-10-19｜turn-06｜PENDING';
assert.equal(oldClaimLines.filter((line) => line === oldT5).length, 1, 't5 provenance drift');
assert.equal(oldRows.some((line) => line.startsWith('t46｜')), false, 't46 ID already in use');
const claims = Buffer.from(oldClaimLines.flatMap((line) => line === oldT5 ? [line, newT46] : [line]).join('\n'));
const claimRows = claims.toString('utf8').split('\n').filter((line) => /^[a-z]\d+[a-z]?｜/.test(line));
assert.equal(claimRows.length, 74);
const claimEntries = claimRows.map((row) => row.split('｜'));
const sceneByClaim = new Map(video.scenes.flatMap((item) => (item.claims ?? []).map((id) => [id, item.id])));
assert.equal(sceneByClaim.size, 74, 'claim anchors not unique');
assert.deepEqual(new Set(claimEntries.map((cells) => cells[0])), new Set(sceneByClaim.keys()), 'claim rows / anchors differ');
for (const cells of claimEntries) {
  assert.equal(cells.length, 6, 'malformed claim row ' + cells[0]);
  assert.equal(cells[4], sceneByClaim.get(cells[0]), 'claim scene drift ' + cells[0]);
  assert.equal(cells[5], 'PENDING', 'no formal verdict may be inherited');
}
const claimUrlById = new Map(claimEntries.map((cells) => [cells[0], cells[2]]));
assert.deepEqual(new Set(claimEntries.map((cells) => cells[2])), new Set(video.sources.map((source) => source.url)));
const plathUrl = 'https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603';
assert.equal(claimUrlById.get('t46'), plathUrl);
assert.equal(sceneByClaim.get('t46'), 'turn-06');
assert.deepEqual(video.sources, before.sources, '18 public sources changed');
assert.deepEqual(video.scenes.map((item) => item.id), before.scenes.map((item) => item.id), 'scene order changed');
assert.deepEqual(video.scenes.flatMap((item) => item.lines.map((line) => line.id)),
  before.scenes.flatMap((item) => item.lines.map((line) => line.id)), 'line IDs changed');
assert.deepEqual(video.loops, before.loops, 'setup/payoff IDs changed');
for (let i = 0; i < video.scenes.length; i++) {
  const oldScene = before.scenes[i];
  const newScene = video.scenes[i];
  if (oldScene.id === 'turn-06') {
    assert.deepEqual({ ...newScene, claims: oldScene.claims }, oldScene, 'unexpected reveal change');
  } else {
    assert.deepEqual(newScene, oldScene, 'unexpected scene change ' + oldScene.id);
  }
}

const priorMap = JSON.parse(readPinned(r18, 'source-map.json'));
const plathSource = priorMap.source_index.filter((entry) => entry.url === plathUrl);
assert.equal(plathSource.length, 1, 'Plath map URL missing or duplicated');
assert.deepEqual(plathSource[0].claim_ids, ['h6', 't5', 't6', 't17', 't29']);
const mappedSources = structuredClone(priorMap.source_index);
mappedSources.find((entry) => entry.url === plathUrl).claim_ids.splice(2, 0, 't46');
const sourceMap = {
  status: 'HOLD_UNREVIEWED_R19_SOURCE_MAP',
  derives_from_r18_manifest_sha256: expected.r18Manifest,
  r18_review_not_inherited: true,
  source_index: mappedSources,
  changed_line_ids: [],
  changed_claim_ids: ['t46'],
  host_source_guard: 'HOLD: r19 has 74 PENDING claims; fresh worker IDs, verifier/listener/two-reader review and formal receipt are required after host six-chapter adoption.',
};
assert.deepEqual(sourceMap.source_index.map((entry) => entry.url), priorMap.source_index.map((entry) => entry.url));
const mappedIds = sourceMap.source_index.flatMap((entry) => entry.claim_ids);
assert.equal(mappedIds.length, 74);
assert.deepEqual(new Set(mappedIds), new Set(claimUrlById.keys()));
for (const entry of sourceMap.source_index) {
  for (const id of entry.claim_ids) assert.equal(claimUrlById.get(id), entry.url, 'source-map URL drift ' + id);
}
const priorAlignment = JSON.parse(readPinned(r18, 'source-alignment.json'));
const sourcePlan = JSON.parse(readPinned(sources25, 'candidate/series.json'));
assert.equal(sourcePlan.plan.sources.length, 25);
const alignment = structuredClone(priorAlignment);
alignment.status = 'HOLD_UNREVIEWED_R19_74_CLAIM_ALIGNMENT';
delete alignment.derives_from_r17_manifest_sha256;
delete alignment.r17_claim_alignment_not_inherited;
alignment.derives_from_r18_manifest_sha256 = expected.r18Manifest;
alignment.r18_claim_alignment_not_inherited = true;
alignment.changed_claim_ids = ['t46'];
assert.equal(alignment.claim_source_rows.length, 73);
const t5Rows = alignment.claim_source_rows.filter((row) => row.id === 't5');
assert.deepEqual(t5Rows, [{ id: 't5', plan_source_index: 5, public_source_index: 10, url: plathUrl }]);
const t5Index = alignment.claim_source_rows.findIndex((row) => row.id === 't5');
alignment.claim_source_rows.splice(t5Index + 1, 0,
  { id: 't46', plan_source_index: 5, public_source_index: 10, url: plathUrl });
alignment.counts.cited_claims = 74;
assert.equal(alignment.claim_source_rows.length, 74);
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
assert.equal(screenplay(before), readPinned(r18, 'candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r18 script drift');
const script = Buffer.from(screenplay(video));
assert.ok(script.equals(readPinned(r18, 'candidate/script.md')), 'r19 must not change r18 narration');
const series = JSON.parse(readPinned(r18, 'candidate/series.json'));
assert.equal(series.plan.sources.length, 23, 'candidate source count drift');
const lexicon = JSON.parse(readPinned(r18, 'candidate/lexicon.json'));
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
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_PENDING_R19_REVIEW',
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
  security_reveal_claim_bound_to_2012_interview: sceneByClaim.get('t46') === 'turn-06'
    && claimUrlById.get('t46') === plathUrl,
  measured_tts_and_cut: 'NOT_RUN',
  independent_full_r19_review: 'NOT_RUN',
  six_chapter_host_bridge: 'NOT_INSTALLED_OR_FORMALLY_REVIEWED',
  worker_claim_id_and_source_merge: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  host_import_or_paid_media: 'NOT_RUN',
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', readPinned(r18, 'candidate/series.json')],
  ['candidate/lexicon.json', readPinned(r18, 'candidate/lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['source-alignment.json', json(alignment)],
  ['validation.json', json(validation)],
  ['plan-source-addition.json', readPinned(r18, 'plan-source-addition.json')],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE',
  slug: video.slug,
  derives_from_r18_manifest_sha256: expected.r18Manifest,
  derives_from_r18_blind_review_sha256: expected.r18BlindReview,
  derives_from_r16_source_plan_manifest_sha256: expected.sources25Manifest,
  r18_review_not_inherited: true,
  source_snapshot: r18Manifest.source_snapshot,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r18_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r19');
  if (action === '--write') {
    assert.ok(!fs.existsSync(file), 'r19 output exists; do not overwrite ' + name);
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
