// A01-only offline r22: resolve the two P1 and six P2 findings in r21 reviews.
// Pins all r21 outputs and both independent r21 reviews; creates only new outputs here.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r21 = path.resolve(here, '../A01-editorial-candidate-20261019-r21');
const expected = {
  r21Manifest: '5131d53cef6f20184c1d5043cf63428602deb1551ffb9808ca42e940f190e900',
  r21FactReview: 'a2570970dc7a240b2e7ed25313ee2ab787214f155e11de5fdaec0e86051e0409',
  r21BlindReview: '939ee33e1656e4be78a0e48762eacad8db581b518bd6cf4196a9ec06f52dbecd',
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
const r21Manifest = verifyPinned(r21, expected.r21Manifest);
assert.equal(sha(readPinned(r21, 'independent-fact-full-plan-review-20261019.md')), expected.r21FactReview,
  'pinned r21 full fact/plan review drift');
assert.equal(sha(readPinned(r21, 'blind-story-review-20261019.md')), expected.r21BlindReview,
  'pinned r21 blind review drift');

const before = JSON.parse(readPinned(r21, 'candidate/video.json'));
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
  ['hook-anita', 'r17h01',
    '1928 年，安妮塔的兒子把舊嬰兒車輪裝上箱子。旅程結束後，她還會帶輪子箱出門嗎？',
    '1928 年那趟旅行出發前，安妮塔的兒子把舊嬰兒車輪裝上箱子。旅程結束後，她還會帶輪子箱出門嗎？'],
  ['idea-memory', 'r14i01',
    '三十多年後，Sadow 一家從阿魯巴返程；因為帶著兩個孩子，兩只二十七吋傳統箱都塞得滿滿。',
    '多年後，Sadow 一家從阿魯巴返程；因為帶著兩個孩子，兩只二十七吋傳統箱都塞得滿滿。'],
  ['turn-09b', '3zwf',
    '箱身直立，底下兩個輪子，上面接一根能收回去的伸縮拉桿。',
    '安檢時，他把推車鎖上硬殼箱。後來的 Rollaboard 才是直立雙輪，拉桿能收回。'],
];
for (const [sceneId, lineId, oldText, newText] of lineChanges) {
  const lines = scene(sceneId).lines.filter((line) => line.id === lineId);
  assert.equal(lines.length, 1, 'line drift ' + lineId);
  assert.equal(lines[0].text, oldText, 'old line drift ' + lineId);
  lines[0].text = newText;
}
const memoryPrompt = scene('idea-memory').data.prompt;
assert.ok(memoryPrompt.includes('returning from Aruba around 1970.'), 'idea-memory visual prompt drift');
scene('idea-memory').data.prompt = memoryPrompt.replace('returning from Aruba around 1970.',
  'returning from Aruba at an unspecified date before the 1970 luggage patent filing.');
const designPrompt = scene('turn-09b').data.prompt;
assert.ok(designPrompt.includes('not a photographed historical prototype or a dated garage event.'),
  'turn-09b visual prompt drift');
scene('turn-09b').data.prompt = designPrompt.replace('not a photographed historical prototype or a dated garage event.',
  'not the screw-on security trolley experiment, a photographed historical prototype or a dated garage event.');

const oldClaims = readPinned(r21, 'candidate/claims.md').toString('utf8');
const oldClaimLines = oldClaims.replace(/\r\n/g, '\n').split('\n');
const oldRows = oldClaimLines.filter((line) => /^[a-z]\d+[a-z]?｜/.test(line));
assert.equal(oldRows.length, 74);
const claimRewrites = new Map([
  ['i35', ['Sadow 回憶與妻子和兩個孩子從阿魯巴返程，因孩子同行，兩只 27 吋傳統箱塞得滿滿；訪談未列箱內物品的所有權，與 Anita 的故事也無可證實的直接交接',
    'Sadow 回憶與妻子和兩個孩子從阿魯巴返程，因孩子同行，兩只 27 吋傳統箱塞得滿滿；訪談未列箱內物品的所有權。本集核對的這篇 ABC 訪談未提 Anita，也未記兩者直接交接']],
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
  expectedSceneOrder.flatMap((id) => originalScenesById.get(id).lines.map((line) => line.id)),
  'line IDs or line positions changed');
assert.deepEqual(video.loops, before.loops, 'setup/payoff IDs changed');
const changedSceneIds = new Set(video.scenes
  .filter((item) => JSON.stringify(item) !== JSON.stringify(originalScenesById.get(item.id)))
  .map((item) => item.id));
assert.deepEqual(changedSceneIds,
  new Set(['hook-anita', 'idea-memory', 'turn-09b']));
for (const newScene of video.scenes) {
  const oldScene = originalScenesById.get(newScene.id);
  const copied = structuredClone(newScene);
  if (lineChanges.some(([id]) => id === oldScene.id)) copied.lines = oldScene.lines;
  if (oldScene.id === 'idea-memory' || oldScene.id === 'turn-09b') copied.data.prompt = oldScene.data.prompt;
  assert.deepEqual(copied, oldScene, 'unexpected scene change ' + oldScene.id);
}

const priorMap = JSON.parse(readPinned(r21, 'source-map.json'));
const plathSource = priorMap.source_index.filter((entry) => entry.url === plathUrl);
assert.equal(plathSource.length, 1, 'Plath map URL missing or duplicated');
assert.deepEqual(plathSource[0].claim_ids, ['h6', 't5', 't46', 't6', 't17', 't29']);
const sourceMap = {
  status: 'HOLD_UNREVIEWED_R22_SOURCE_MAP',
  derives_from_r21_manifest_sha256: expected.r21Manifest,
  derives_from_r21_full_fact_plan_review_sha256: expected.r21FactReview,
  derives_from_r21_blind_review_sha256: expected.r21BlindReview,
  r21_reviews_not_inherited_as_approval: true,
  source_index: structuredClone(priorMap.source_index),
  changed_line_ids: lineChanges.map(([, id]) => id),
  changed_claim_ids: [...claimRewrites.keys()],
  changed_visual_prompt_scene_ids: ['idea-memory', 'turn-09b'],
  changed_plan_fields: ['chapters.turn.point', 'must_verify[3].claim', 'must_verify[4].claim',
    'must_verify[8].claim', 'sources[4].supports', 'sources[6].supports'],
  reordered_scene_ids: [],
  host_source_guard: 'HOLD: r22 has 74 PENDING claims; fresh worker IDs, verifier/listener/two-reader review and formal receipt are required after host six-chapter adoption.',
};
assert.deepEqual(sourceMap.source_index.map((entry) => entry.url), priorMap.source_index.map((entry) => entry.url));
const mappedIds = sourceMap.source_index.flatMap((entry) => entry.claim_ids);
assert.equal(mappedIds.length, 74);
assert.deepEqual(new Set(mappedIds), new Set(claimUrlById.keys()));
for (const entry of sourceMap.source_index) {
  for (const id of entry.claim_ids) assert.equal(claimUrlById.get(id), entry.url, 'source-map URL drift ' + id);
}
const priorAlignment = JSON.parse(readPinned(r21, 'source-alignment.json'));
const sourcePlan = JSON.parse(readPinned(r21, 'proposed-25-source-series.json'));
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
    '與 Plath 自述安檢推車故事分列，不排定兩者先後。Plath 試著把推車鎖在箱上，安檢員回應只依本人回憶；Travelpro 記述 1987 車庫 Rollaboard，1989 專利只支持後來寫出的設計目標。',
    '與 2012 年 USA TODAY／ABC 記者敘述的安檢推車故事分列，不排定兩者先後。報導記旅客正費力想卸下彈力繩綁箱，未說是否成功；另記 Plath 回車庫將推車用螺絲固定在硬殼箱上，確切年份未標。安檢員的答話由 Plath 直接引述。這只螺絲推車箱不得與後來直立雙輪、可收拉桿的 Rollaboard 原型直接視為同一物；Travelpro 把該設計記於 1987 年，另記 1989 年生產搬離車庫。1989 年專利只支持後來寫出的結構目標。',
    'turn chapter');
  series.plan.must_verify[3].claim = replaceOnce(series.plan.must_verify[3].claim,
    'Plath 的安檢經歷是其受訪回憶；1989 年專利描述外置推車反覆拆綁，不能倒推 1987 年所有細節',
    '2012 年 USA TODAY／ABC 記者敘述安檢旅客正費力想卸下彈力繩綁箱，未說是否成功；Plath 的直接引語只涉及他與安檢員的對話。1989 年專利描述外置推車反覆拆綁，不能倒推安檢故事的年份或車庫箱細節',
    'must_verify 3');
  series.plan.must_verify[4].claim = replaceOnce(series.plan.must_verify[4].claim,
    'Travelpro 回顧 1987 年車庫 Rollaboard、機組採用、1989 年搬倉及 1991 年 Plath 全職經營；年份有其他晚年回憶差異',
    'Travelpro 回顧 1987 年直立雙輪伸縮把手設計與機組採用、1989 年生產搬離車庫及 1991 年 Plath 全職經營',
    'must_verify 4');
  series.plan.must_verify[8].claim = replaceOnce(series.plan.must_verify[8].claim,
    'Winnetka 館方區分 Anita 的 1921 年首旅車站候宿經驗與 1928 年第二趟長途旅行；不能把早期經歷移到輪子箱旅程',
    'Winnetka 館方區分 Anita 的 1921 年首旅搭火車抵達新地方後由丈夫尋找廉價住處、她與四個孩子守著行李，與 1928 年第二趟長途旅行；館方未指明守行李的地點，不能把早期經歷移到輪子箱旅程',
    'must_verify 8');
  assert.equal(series.plan.sources[4].url, 'https://en.wikipedia.org/wiki/Suitcase');
  series.plan.sources[4].supports = replaceOnce(series.plan.sources[4].supports,
    "Sadow 在波多黎各機場得到靈感、Macy's 1970 年 10 月開賣與廣告詞；其 Samsonite 2004 年說法與官方年表衝突，不作依據",
    "Sadow 輪箱早期史的背景索引；Macy's 1970 年 10 月店內展示人偶另以 ABC 2010 訪談回核，不用本條確定首次開賣日期；其 Samsonite 2004 年說法與官方年表衝突，不作依據",
    'plan source 4');
  assert.equal(series.plan.sources[6].url,
    'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469');
  series.plan.sources[6].supports = replaceOnce(series.plan.sources[6].supports,
    "Macy's 採購先拒後由副總裁下單、1970 年 10 月開賣",
    "Macy's 採購先拒後由副總裁下單、1970 年 10 月店內人偶展示；未指明首次開賣日期",
    'plan source 6');
  const rendered = JSON.stringify(series);
  for (const stale of ['1987 車庫 Rollaboard', '1987 年車庫 Rollaboard',
    '1921 年首旅車站候宿', 'Plath 自述安檢推車故事', "1970 年 10 月開賣"]) {
    assert.ok(!rendered.includes(stale), 'stale plan overclaim ' + stale);
  }
  return series;
};
fixPlanFindings(sourcePlan, 25);
assert.deepEqual(sourcePlan.plan.sources.map((entry) => entry.url),
  sourcePlanBefore.plan.sources.map((entry) => entry.url), 'proposed plan source URL/order drift');
const alignment = structuredClone(priorAlignment);
alignment.status = 'HOLD_UNREVIEWED_R22_74_CLAIM_ALIGNMENT';
alignment.derives_from_r21_manifest_sha256 = expected.r21Manifest;
alignment.derives_from_r21_full_fact_plan_review_sha256 = expected.r21FactReview;
alignment.derives_from_r21_blind_review_sha256 = expected.r21BlindReview;
alignment.r21_reviews_not_inherited_as_approval = true;
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
assert.equal(screenplay(before), readPinned(r21, 'candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r21 script drift');
const script = Buffer.from(screenplay(video));
assert.ok(!script.equals(readPinned(r21, 'candidate/script.md')), 'r22 narration must reflect precision edits');
const priorSeries = JSON.parse(readPinned(r21, 'candidate/series.json'));
const series = fixPlanFindings(structuredClone(priorSeries), 23);
assert.deepEqual(series.plan.sources.map((entry) => entry.url),
  priorSeries.plan.sources.map((entry) => entry.url), 'candidate source URL/order drift');
assert.deepEqual(sourcePlan.plan.sources.slice(0, 23).map((entry) => entry.url),
  series.plan.sources.map((entry) => entry.url), 'proposed plan source URL/order drift');
const lexicon = JSON.parse(readPinned(r21, 'candidate/lexicon.json'));
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
assert.equal(lines.length, 77);
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_PENDING_R22_REVIEW',
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
  r21_manifest_sha256: expected.r21Manifest,
  r21_full_fact_plan_review_sha256: expected.r21FactReview,
  r21_blind_review_sha256: expected.r21BlindReview,
  r21_findings_addressed_in_draft: [
    'plan-1987-garage-conflation', 'turn-09b-audible-design-bridge',
    '1921-arrival-location', 'pre-1928-wheel-modification', '1939-to-Sadow-interval',
    'i35-limited-negative-evidence', '2012-reporter-versus-direct-quote',
    '1970-October-mannequin-versus-sale-date',
  ],
  changed_line_ids: sourceMap.changed_line_ids,
  changed_claim_ids: sourceMap.changed_claim_ids,
  changed_visual_prompt_scene_ids: sourceMap.changed_visual_prompt_scene_ids,
  changed_plan_fields: sourceMap.changed_plan_fields,
  measured_tts_and_cut: 'NOT_RUN',
  independent_full_r22_review: 'NOT_RUN',
  six_chapter_host_bridge: 'NOT_INSTALLED_OR_FORMALLY_REVIEWED',
  worker_claim_id_and_source_merge: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  host_import_or_paid_media: 'NOT_RUN',
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', json(series)],
  ['candidate/lexicon.json', readPinned(r21, 'candidate/lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['source-alignment.json', json(alignment)],
  ['validation.json', json(validation)],
  ['plan-source-addition.json', readPinned(r21, 'plan-source-addition.json')],
  ['proposed-25-source-series.json', json(sourcePlan)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE',
  slug: video.slug,
  derives_from_r21_manifest_sha256: expected.r21Manifest,
  derives_from_r21_independent_full_fact_plan_review_sha256: expected.r21FactReview,
  derives_from_r21_blind_story_review_sha256: expected.r21BlindReview,
  r21_reviews_not_inherited_as_approval: true,
  source_snapshot: r21Manifest.source_snapshot,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r21_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(['--preview', '--write', '--check'].includes(action), 'use --preview, --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r22');
  if (action === '--preview') {
    assert.ok(!fs.existsSync(file), 'preview requires a fresh r22 output slot ' + name);
  } else if (action === '--write') {
    assert.ok(!fs.existsSync(file), 'r22 output exists; do not overwrite ' + name);
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
