// A01-only offline r21: factual and editorial delta after two independent r20 reviews.
// Pins all r20 outputs and both r20 review receipts; creates only new outputs here.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r20 = path.resolve(here, '../A01-editorial-candidate-20261019-r20');
const expected = {
  r20Manifest: '78826bcfc6356335855756fc7f81a7c846087df340c4a7753c270c186d1077eb',
  r20FactReview: '116a048ab552f19850f58aaccc22b8e7324591e992a7a828737cad2dbab5ae85',
  r20BlindReview: '903ce88b8e43526a3862760dc198ba789b27278f891520dd84490b9a67f4701e',
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
const r20Manifest = verifyPinned(r20, expected.r20Manifest);
assert.equal(sha(readPinned(r20, 'independent-fact-delta-review-20261019.md')), expected.r20FactReview,
  'pinned r20 fact review drift');
assert.equal(sha(readPinned(r20, 'blind-story-review-20261019.md')), expected.r20BlindReview,
  'pinned r20 blind review drift');

const before = JSON.parse(readPinned(r20, 'candidate/video.json'));
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
  ['origin-01b', '6b28',
    '兒子改好箱子後，畫家 Anita Willets-Burnham 才帶著一家六口，展開第二趟長途旅行。',
    '兒子改好箱子後，畫家 Anita Willets-Burnham 才帶著一家六口出發，輪子箱也跟著上路。'],
  ['engine-porter', 'r17e01',
    'Shiller 說，助理打電話問過 Sadow。據 Sadow 轉述，採購還問：車站不是有搬運工嗎？',
    '耶魯教授 Shiller 說，助理打電話問過 Sadow。據 Sadow 轉述，採購還問：車站不是有搬運工嗎？'],
];
for (const [sceneId, lineId, oldText, newText] of lineChanges) {
  const lines = scene(sceneId).lines.filter((line) => line.id === lineId);
  assert.equal(lines.length, 1, 'line drift ' + lineId);
  assert.equal(lines[0].text, oldText, 'old line drift ' + lineId);
  lines[0].text = newText;
}
// Let the audience see the design after the security payoff; compare the conflicting years
// in the following beat. Claim IDs and source anchors stay on their own scene IDs.
const designIndex = video.scenes.findIndex((item) => item.id === 'turn-09b');
const dateIndex = video.scenes.findIndex((item) => item.id === 'turn-09');
assert.ok(dateIndex > 0 && designIndex === dateIndex + 1, 'year/design scene adjacency drift');
[video.scenes[dateIndex], video.scenes[designIndex]] = [video.scenes[designIndex], video.scenes[dateIndex]];
const dateScene = scene('turn-09');
const oldDatePrompt = 'Cute medium product-study view at a neutral plain worktable, outside the garage visual callback. An anonymous hand rests near a closed unbranded suitcase while the lower case and top stay cropped to withhold its wheel layout and handle until turn-09b. The narration attributes two different years to two sources; the illustration represents neither as a dated historical photograph. No calendar, date text, patent number, logo or real-person likeness.';
assert.equal(dateScene.data.prompt, oldDatePrompt);
dateScene.data.prompt = 'Cute medium source-checking view at a neutral worktable after the upright suitcase design has been revealed. A closed unbranded two-wheel case stands beside two plain unmarked folders, one from a company account and one from a biographical account. The narration attributes their different years; the illustration is not a dated historical photograph. No calendar, readable text, patent number, logo or real-person likeness.';
const designScene = scene('turn-09b');
const oldDesignPrompt = 'Cute medium side view of an illustrative upright rolling suitcase on a neutral plain background, outside the garage visual callback. An anonymous hand extends a retractable handle from a compact case with exactly two small base wheels. This clarifies the design described in the separately attributed 1987/1988 accounts, not a photographed historical prototype or a dated garage event. No calendar, date text, logo or real-person likeness.';
assert.equal(designScene.data.prompt, oldDesignPrompt);
designScene.data.prompt = oldDesignPrompt.replace('This clarifies the design described in the separately attributed 1987/1988 accounts',
  'This reveals the design before the following beat compares the 1987/1988 accounts');

const oldClaims = readPinned(r20, 'candidate/claims.md').toString('utf8');
const oldClaimLines = oldClaims.replace(/\r\n/g, '\n').split('\n');
const oldRows = oldClaimLines.filter((line) => /^[a-z]\d+[a-z]?｜/.test(line));
assert.equal(oldRows.length, 74);
const claimRewrites = new Map([
  ['h6', ['Plath 的受訪回憶記他看見旅客在安檢拆外置推車後，回車庫把硬殼箱與推車鎖在一起；該段未指明精確年份，不與 Travelpro 的 1987 設計年份併為同一事',
    '2012 年 USA TODAY／ABC 報導記述 Plath 在安檢看見旅客正費力想把以彈力繩固定的箱子從笨重金屬推車解下；報導未說是否成功。他之後回車庫，把一台行李推車用螺絲固定在硬殼箱上，再帶回機場。報導未指明該段確切年份，不能與 Travelpro 所稱 1987 年設計直接併為同一事']],
  ['e37', ['Robert Shiller 2008 年耶魯課堂說其學生助理致電 Sadow，Sadow 轉述百貨商以車站已有搬運工反對輪箱；屬轉述，不當作原始採購文件',
    '耶魯教授 Robert Shiller 在 2008 年課堂說其學生助理致電 Sadow；據 Shiller 轉述，Sadow 回述百貨商以車站已有搬運工反對輪箱。這是課堂上的轉述，不是原始採購文件或 Sadow 的錄音逐字稿']],
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
[expectedSceneOrder[dateIndex], expectedSceneOrder[designIndex]] =
  [expectedSceneOrder[designIndex], expectedSceneOrder[dateIndex]];
assert.deepEqual(video.scenes.map((item) => item.id), expectedSceneOrder, 'unexpected scene order change');
const originalScenesById = new Map(before.scenes.map((item) => [item.id, item]));
assert.deepEqual(video.scenes.flatMap((item) => item.lines.map((line) => line.id)),
  expectedSceneOrder.flatMap((id) => originalScenesById.get(id).lines.map((line) => line.id)),
  'line IDs or line positions changed beyond the two-scene reorder');
assert.deepEqual(video.loops, before.loops, 'setup/payoff IDs changed');
const changedSceneIds = new Set(video.scenes
  .filter((item) => JSON.stringify(item) !== JSON.stringify(originalScenesById.get(item.id)))
  .map((item) => item.id));
assert.deepEqual(changedSceneIds,
  new Set(['origin-01b', 'engine-porter', 'turn-09', 'turn-09b']));
for (const newScene of video.scenes) {
  const oldScene = originalScenesById.get(newScene.id);
  const copied = structuredClone(newScene);
  if (lineChanges.some(([id]) => id === oldScene.id)) copied.lines = oldScene.lines;
  if (oldScene.id === 'turn-09' || oldScene.id === 'turn-09b') copied.data.prompt = oldScene.data.prompt;
  assert.deepEqual(copied, oldScene, 'unexpected scene change ' + oldScene.id);
}

const priorMap = JSON.parse(readPinned(r20, 'source-map.json'));
const plathSource = priorMap.source_index.filter((entry) => entry.url === plathUrl);
assert.equal(plathSource.length, 1, 'Plath map URL missing or duplicated');
assert.deepEqual(plathSource[0].claim_ids, ['h6', 't5', 't46', 't6', 't17', 't29']);
const sourceMap = {
  status: 'HOLD_UNREVIEWED_R21_SOURCE_MAP',
  derives_from_r20_manifest_sha256: expected.r20Manifest,
  derives_from_r20_fact_review_sha256: expected.r20FactReview,
  derives_from_r20_blind_review_sha256: expected.r20BlindReview,
  r20_reviews_not_inherited_as_approval: true,
  source_index: structuredClone(priorMap.source_index),
  changed_line_ids: lineChanges.map(([, id]) => id),
  changed_claim_ids: [...claimRewrites.keys()],
  reordered_scene_ids: ['turn-09b', 'turn-09'],
  host_source_guard: 'HOLD: r21 has 74 PENDING claims; fresh worker IDs, verifier/listener/two-reader review and formal receipt are required after host six-chapter adoption.',
};
assert.deepEqual(sourceMap.source_index.map((entry) => entry.url), priorMap.source_index.map((entry) => entry.url));
const mappedIds = sourceMap.source_index.flatMap((entry) => entry.claim_ids);
assert.equal(mappedIds.length, 74);
assert.deepEqual(new Set(mappedIds), new Set(claimUrlById.keys()));
for (const entry of sourceMap.source_index) {
  for (const id of entry.claim_ids) assert.equal(claimUrlById.get(id), entry.url, 'source-map URL drift ' + id);
}
const priorAlignment = JSON.parse(readPinned(r20, 'source-alignment.json'));
const sourcePlan = JSON.parse(readPinned(r20, 'proposed-25-source-series.json'));
assert.equal(sourcePlan.plan.sources.length, 25);
const replaceOnce = (value, beforeText, afterText, label) => {
  assert.equal(value.split(beforeText).length, 2, 'plan text drift ' + label);
  return value.replace(beforeText, afterText);
};
const scopePlanEvidence = (series, expectedSourceCount) => {
  assert.equal(series.plan.sources.length, expectedSourceCount);
  series.logline = replaceOnce(series.logline,
    '三條沒有證據顯示直接承襲的人物線，各自把旅途中卡住的一步往前推。',
    '三人各自跨過一道阻礙；本集所查來源未證實他們一棒接一棒地直接傳承。', 'logline');
  assert.equal(series.plan.chapters[1].key, 'origin');
  series.plan.chapters[1].point = replaceOnce(series.plan.chapters[1].point,
    '無證據顯示她影響 Sadow。 1939 年',
    '本集所查來源未證實她直接影響 Sadow。1939 年', 'origin chapter');
  series.plan.must_verify[0].claim = replaceOnce(series.plan.must_verify[0].claim,
    '無證據顯示她影響 Sadow',
    '本集所查來源未證實她直接影響 Sadow', 'must_verify 0');
  series.plan.takeaway = replaceOnce(series.plan.takeaway,
    '由多個互不證實直接承襲的人物與產品線構成',
    '由多位人物與產品線構成，本集所查來源未證實三人直接承襲', 'takeaway');
  const rendered = JSON.stringify(series);
  assert.ok(!rendered.includes('無證據顯示她影響 Sadow'));
  assert.ok(!rendered.includes('沒有證據顯示直接承襲'));
  return series;
};
scopePlanEvidence(sourcePlan, 25);
const alignment = structuredClone(priorAlignment);
alignment.status = 'HOLD_UNREVIEWED_R21_74_CLAIM_ALIGNMENT';
alignment.derives_from_r20_manifest_sha256 = expected.r20Manifest;
alignment.derives_from_r20_fact_review_sha256 = expected.r20FactReview;
alignment.derives_from_r20_blind_review_sha256 = expected.r20BlindReview;
alignment.r20_reviews_not_inherited_as_approval = true;
alignment.changed_claim_ids = [...claimRewrites.keys()];
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
assert.equal(screenplay(before), readPinned(r20, 'candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r20 script drift');
const script = Buffer.from(screenplay(video));
assert.ok(!script.equals(readPinned(r20, 'candidate/script.md')), 'r21 narration must reflect editorial changes');
const priorSeries = JSON.parse(readPinned(r20, 'candidate/series.json'));
const series = scopePlanEvidence(structuredClone(priorSeries), 23);
assert.deepEqual(series.plan.sources.map((entry) => entry.url),
  priorSeries.plan.sources.map((entry) => entry.url), 'candidate source URL/order drift');
assert.deepEqual(sourcePlan.plan.sources.slice(0, 23).map((entry) => entry.url),
  series.plan.sources.map((entry) => entry.url), 'proposed plan source URL/order drift');
const lexicon = JSON.parse(readPinned(r20, 'candidate/lexicon.json'));
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
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_PENDING_R21_REVIEW',
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
  r20_manifest_sha256: expected.r20Manifest,
  r20_fact_review_sha256: expected.r20FactReview,
  r20_blind_review_sha256: expected.r20BlindReview,
  r20_findings_addressed_in_draft: ['h6', 'plan-evidence-scope', 'journey-repetition', 'shiller-identity', 'date-beat-order'],
  measured_tts_and_cut: 'NOT_RUN',
  independent_full_r21_review: 'NOT_RUN',
  six_chapter_host_bridge: 'NOT_INSTALLED_OR_FORMALLY_REVIEWED',
  worker_claim_id_and_source_merge: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  host_import_or_paid_media: 'NOT_RUN',
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', json(series)],
  ['candidate/lexicon.json', readPinned(r20, 'candidate/lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['source-alignment.json', json(alignment)],
  ['validation.json', json(validation)],
  ['plan-source-addition.json', readPinned(r20, 'plan-source-addition.json')],
  ['proposed-25-source-series.json', json(sourcePlan)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE',
  slug: video.slug,
  derives_from_r20_manifest_sha256: expected.r20Manifest,
  derives_from_r20_independent_fact_review_sha256: expected.r20FactReview,
  derives_from_r20_blind_story_review_sha256: expected.r20BlindReview,
  r20_reviews_not_inherited_as_approval: true,
  source_snapshot: r20Manifest.source_snapshot,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r20_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(['--preview', '--write', '--check'].includes(action), 'use --preview, --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r21');
  if (action === '--preview') {
    assert.ok(!fs.existsSync(file), 'preview requires a fresh r21 output slot ' + name);
  } else if (action === '--write') {
    assert.ok(!fs.existsSync(file), 'r21 output exists; do not overwrite ' + name);
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
