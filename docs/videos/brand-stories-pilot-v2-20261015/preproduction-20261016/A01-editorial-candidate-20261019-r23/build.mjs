// A01-only offline r23: resolve the r22 factual and storytelling review findings.
// Pins all r22 outputs and both independent r22 reviews; creates only new outputs here.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r22 = path.resolve(here, '../A01-editorial-candidate-20261019-r22');
const expected = {
  r22Manifest: '9ab4e2bca9411951e9471e414ec4170a3ed3d793d645ed9c5921cb941e12b33d',
  r22FactReview: '8432218884329f8bd2978c0661658457c605d1d3e7eadcee209d3d0230b9b3ed',
  r22BlindReview: 'a8bad7081b7c6e44ff116f41d21a0b005a85dca58fd91c8f72a36cde2e93bdbe',
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
const r22Manifest = verifyPinned(r22, expected.r22Manifest);
assert.equal(sha(readPinned(r22, 'independent-fact-delta-review-20261019.md')), expected.r22FactReview,
  'pinned r22 fact/plan review drift');
assert.equal(sha(readPinned(r22, 'blind-story-review-20261019.md')), expected.r22BlindReview,
  'pinned r22 blind review drift');

const before = JSON.parse(readPinned(r22, 'candidate/video.json'));
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
const lineChanges = [
  ['turn-09b', '3zwf',
    '安檢時，他把推車鎖上硬殼箱。後來的 Rollaboard 才是直立雙輪，拉桿能收回。',
    '安檢故事裡，鎖在箱上的是推車；Travelpro 記的 Rollaboard，則是直立雙輪、可收拉桿。'],
  ['engine-09', 'kzmj',
    '廣告把這種走法寫成「The Luggage That Glides」，',
    '廣告主打「會滑行的行李箱」。'],
  ['now-11', 'jspd',
    '1989 年，他把生產搬進了一間倉庫。',
    '1989 年，他把營運從車庫搬到倉庫。'],
  ['now-1993-test', 'r3n02',
    '那位記者還把四家輪子登機箱帶上路，看看它們在地面和機艙裡到底怎樣。',
    '記者把四家輪子登機箱帶上路實測。'],
];
for (const [sceneId, lineId, oldText, newText] of lineChanges) {
  const lines = scene(sceneId).lines.filter((line) => line.id === lineId);
  assert.equal(lines.length, 1, 'line drift ' + lineId);
  assert.equal(lines[0].text, oldText, 'old line drift ' + lineId);
  lines[0].text = newText;
}
const adLines = scene('engine-09').lines;
assert.deepEqual(adLines.map((line) => line.id), ['kzmj', '393x'], 'ad line ID drift');
assert.equal(adLines[1].text, '也就是「會滑行的行李箱」。', 'ad translation line drift');
scene('engine-09').lines = [adLines[0]];

const oldClaims = readPinned(r22, 'candidate/claims.md').toString('utf8');
const oldClaimLines = oldClaims.replace(/\r\n/g, '\n').split('\n');
const oldRows = oldClaimLines.filter((line) => /^[a-z]\d+[a-z]?｜/.test(line));
assert.equal(oldRows.length, 74);
const claimRewrites = new Map([
  ['n42', ['Travelpro 自述需求增加，車庫已不夠用；1989 年 Plath 把生產搬進倉庫',
    'Travelpro 自述需求增加，車庫已不夠用；1989 年 Plath 將營運從車庫搬到倉庫']],
]);
const rewrittenIds = new Set();
const claims = Buffer.from(oldClaimLines.map((line) => {
  const cells = line.split('｜');
  const change = claimRewrites.get(cells[0]);
  if (!change) return line;
  assert.equal(cells.length, 6, 'malformed source claim ' + cells[0]);
  assert.equal(cells[1], change[0], 'source claim drift ' + cells[0]);
  assert.equal(cells[5], 'PENDING', 'source claim unexpectedly reviewed ' + cells[0]);
  assert.ok(!rewrittenIds.has(cells[0]), 'duplicate source claim ' + cells[0]);
  rewrittenIds.add(cells[0]);
  cells[1] = change[1];
  cells[3] = '2026-10-19';
  return cells.join('｜');
}).join('\n'));
assert.deepEqual(rewrittenIds, new Set(claimRewrites.keys()), 'not all intended claims changed');
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
assert.equal(claimUrlById.get('h6'), plathUrl);
assert.equal(sceneByClaim.get('h6'), 'hook-06');
assert.deepEqual(video.sources, before.sources, '18 public sources changed');
const expectedSceneOrder = before.scenes.map((item) => item.id);
assert.deepEqual(video.scenes.map((item) => item.id), expectedSceneOrder, 'unexpected scene order change');
const originalScenesById = new Map(before.scenes.map((item) => [item.id, item]));
assert.deepEqual(video.scenes.flatMap((item) => item.lines.map((line) => line.id)),
  expectedSceneOrder.flatMap((id) => originalScenesById.get(id).lines.map((line) => line.id))
    .filter((id) => id !== '393x'), 'unexpected line IDs or line positions changed');
assert.deepEqual(video.loops, before.loops, 'setup/payoff IDs changed');
const changedSceneIds = new Set(video.scenes
  .filter((item) => JSON.stringify(item) !== JSON.stringify(originalScenesById.get(item.id)))
  .map((item) => item.id));
assert.deepEqual(changedSceneIds,
  new Set(['turn-09b', 'engine-09', 'now-11', 'now-1993-test']));
for (const newScene of video.scenes) {
  const oldScene = originalScenesById.get(newScene.id);
  const copied = structuredClone(newScene);
  if (lineChanges.some(([id]) => id === oldScene.id)) copied.lines = oldScene.lines;
  assert.deepEqual(copied, oldScene, 'unexpected scene change ' + oldScene.id);
}

const priorMap = JSON.parse(readPinned(r22, 'source-map.json'));
const plathSource = priorMap.source_index.filter((entry) => entry.url === plathUrl);
assert.equal(plathSource.length, 1, 'Plath map URL missing or duplicated');
assert.deepEqual(plathSource[0].claim_ids, ['h6', 't5', 't46', 't6', 't17', 't29']);
const sourceMap = {
  status: 'HOLD_UNREVIEWED_R23_SOURCE_MAP',
  derives_from_r22_manifest_sha256: expected.r22Manifest,
  derives_from_r22_fact_review_sha256: expected.r22FactReview,
  derives_from_r22_blind_review_sha256: expected.r22BlindReview,
  r22_reviews_not_inherited_as_approval: true,
  source_index: structuredClone(priorMap.source_index),
  changed_line_ids: lineChanges.map(([, id]) => id),
  removed_line_ids: ['393x'],
  changed_claim_ids: [...claimRewrites.keys()],
  changed_visual_prompt_scene_ids: [],
  changed_plan_fields: ['chapters.turn.point', 'must_verify[4].claim'],
  reordered_scene_ids: [],
  host_source_guard: 'HOLD: r23 has 74 PENDING claims; fresh worker IDs, verifier/listener/two-reader review and formal receipt are required after host six-chapter adoption.',
};
assert.deepEqual(sourceMap.source_index.map((entry) => entry.url), priorMap.source_index.map((entry) => entry.url));
const mappedIds = sourceMap.source_index.flatMap((entry) => entry.claim_ids);
assert.equal(mappedIds.length, 74);
assert.deepEqual(new Set(mappedIds), new Set(claimUrlById.keys()));
for (const entry of sourceMap.source_index) {
  for (const id of entry.claim_ids) assert.equal(claimUrlById.get(id), entry.url, 'source-map URL drift ' + id);
}
const priorAlignment = JSON.parse(readPinned(r22, 'source-alignment.json'));
const sourcePlan = JSON.parse(readPinned(r22, 'proposed-25-source-series.json'));
const sourcePlanBefore = structuredClone(sourcePlan);
assert.equal(sourcePlan.plan.sources.length, 25);
const replaceOnce = (value, beforeText, afterText, label) => {
  assert.equal(value.split(beforeText).length, 2, 'plan text drift ' + label);
  return value.replace(beforeText, afterText);
};
const fixPlanFindings = (series, expectedSourceCount) => {
  assert.equal(series.plan.sources.length, expectedSourceCount);
  assert.equal(series.plan.chapters[4].key, 'turn');
  series.plan.chapters[4].point = replaceOnce(series.plan.chapters[4].point,
    '1989 年生產搬離車庫', '1989 年將營運從車庫搬到倉庫', 'turn chapter');
  series.plan.must_verify[4].claim = replaceOnce(series.plan.must_verify[4].claim,
    '1989 年生產搬離車庫', '1989 年將營運從車庫搬到倉庫', 'must_verify 4');
  assert.ok(!JSON.stringify(series).includes('1989 年生產搬離車庫'),
    'stale 1989 production-line assertion');
  return series;
};
fixPlanFindings(sourcePlan, 25);
assert.deepEqual(sourcePlan.plan.sources.map((entry) => entry.url),
  sourcePlanBefore.plan.sources.map((entry) => entry.url), 'proposed plan source URL/order drift');
const alignment = structuredClone(priorAlignment);
alignment.status = 'HOLD_UNREVIEWED_R23_74_CLAIM_ALIGNMENT';
delete alignment.derives_from_r21_manifest_sha256;
delete alignment.derives_from_r21_full_fact_plan_review_sha256;
delete alignment.derives_from_r21_blind_review_sha256;
delete alignment.r21_reviews_not_inherited_as_approval;
alignment.derives_from_r22_manifest_sha256 = expected.r22Manifest;
alignment.derives_from_r22_fact_review_sha256 = expected.r22FactReview;
alignment.derives_from_r22_blind_review_sha256 = expected.r22BlindReview;
alignment.r22_reviews_not_inherited_as_approval = true;
alignment.changed_claim_ids = [...claimRewrites.keys()];
alignment.changed_plan_fields = sourceMap.changed_plan_fields;
assert.equal(alignment.counts.cited_claims, 74);
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
assert.equal(screenplay(before), readPinned(r22, 'candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r22 script drift');
const script = Buffer.from(screenplay(video));
assert.ok(!script.equals(readPinned(r22, 'candidate/script.md')), 'r23 narration must reflect precision edits');
const priorSeries = JSON.parse(readPinned(r22, 'candidate/series.json'));
const series = fixPlanFindings(structuredClone(priorSeries), 23);
assert.deepEqual(series.plan.sources.map((entry) => entry.url),
  priorSeries.plan.sources.map((entry) => entry.url), 'candidate source URL/order drift');
assert.deepEqual(sourcePlan.plan.sources.slice(0, 23).map((entry) => entry.url),
  series.plan.sources.map((entry) => entry.url), 'proposed plan source URL/order drift');
const lexicon = JSON.parse(readPinned(r22, 'candidate/lexicon.json'));
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
assert.ok(seconds[275] <= 480, '275-cpm paper body exceeds 8 minutes');
const lines = video.scenes.flatMap((item) => item.lines);
assert.equal(lines.length, 76);
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_PENDING_R23_REVIEW',
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
  r22_manifest_sha256: expected.r22Manifest,
  r22_fact_review_sha256: expected.r22FactReview,
  r22_blind_review_sha256: expected.r22BlindReview,
  r22_findings_addressed_in_draft: [
    'garage-action-misplaced-at-security', '1989-operations-not-production',
    'ad-narration-shortened', '1993-test-narration-shortened',
  ],
  changed_line_ids: sourceMap.changed_line_ids,
  removed_line_ids: sourceMap.removed_line_ids,
  changed_claim_ids: sourceMap.changed_claim_ids,
  changed_visual_prompt_scene_ids: sourceMap.changed_visual_prompt_scene_ids,
  changed_plan_fields: sourceMap.changed_plan_fields,
  measured_tts_and_cut: 'NOT_RUN',
  independent_r23_fact_review: 'NOT_RUN',
  independent_r23_blind_review: 'NOT_RUN',
  six_chapter_host_bridge: 'NOT_INSTALLED_OR_FORMALLY_REVIEWED',
  worker_claim_id_and_source_merge: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  host_import_or_paid_media: 'NOT_RUN',
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', json(series)],
  ['candidate/lexicon.json', readPinned(r22, 'candidate/lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['source-alignment.json', json(alignment)],
  ['validation.json', json(validation)],
  ['plan-source-addition.json', readPinned(r22, 'plan-source-addition.json')],
  ['proposed-25-source-series.json', json(sourcePlan)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE',
  slug: video.slug,
  derives_from_r22_manifest_sha256: expected.r22Manifest,
  derives_from_r22_independent_fact_review_sha256: expected.r22FactReview,
  derives_from_r22_blind_story_review_sha256: expected.r22BlindReview,
  r22_reviews_not_inherited_as_approval: true,
  source_snapshot: r22Manifest.source_snapshot,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r22_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(['--preview', '--write', '--check'].includes(action), 'use --preview, --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r23');
  if (action === '--preview') {
    assert.ok(!fs.existsSync(file), 'preview requires a fresh r23 output slot ' + name);
  } else if (action === '--write') {
    assert.ok(!fs.existsSync(file), 'r23 output exists; do not overwrite ' + name);
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
  lint_errors: lint.errors.length, cute_errors: cute.length, manifest_sha256: sha(json(manifest)) }));
