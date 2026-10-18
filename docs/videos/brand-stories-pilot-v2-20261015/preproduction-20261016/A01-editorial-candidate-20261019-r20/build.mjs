// A01-only offline r20: narrow overstatements found by r19 independent fact audit.
// Pins r19, its audit, and the corrected proposed 25-source plan; creates only new outputs here.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r19 = path.resolve(here, '../A01-editorial-candidate-20261019-r19');
const sources25 = path.resolve(here, '../A01-r16-source-plan-25-candidate-20261019');
const expected = {
  r19Manifest: '9e2ebdd0c82f61baa8cf50041b13e47e1070bd0c7950d2e577890313d6db1f6e',
  r19FactAudit: '03a9b3bd20f45d97408e561eaf390ab0b0af253d0b679c3d13bc136a7bff0273',
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
const r19Manifest = verifyPinned(r19, expected.r19Manifest);
assert.equal(sha(readPinned(r19, 'independent-fact-audit-20261019.md')), expected.r19FactAudit,
  'pinned r19 fact audit drift');
verifyPinned(sources25, expected.sources25Manifest);

const before = JSON.parse(readPinned(r19, 'candidate/video.json'));
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
  ['hook-04', '47gq', '1970 年，Sadow 帶著樣品走進百貨公司。',
    '後來，Sadow 帶著輪子箱樣品去找百貨公司採購。'],
  ['origin-r12-01', 'r12o01', '到了 1928 年，準備第二次環遊時，安妮塔不想再像馱馬般提箱。',
    '到了 1928 年，準備第二趟長途旅行時，安妮塔不想再像馱馬般提箱。'],
  ['origin-01b', '6b28', '兒子改好箱子後，畫家 Anita Willets-Burnham 才帶著一家六口，展開第二次環遊世界。',
    '兒子改好箱子後，畫家 Anita Willets-Burnham 才帶著一家六口，展開第二趟長途旅行。'],
  ['now-outro', 'g5b8', '輪子不是唯一答案；願意拉、買得到、用得順手，才走進日常。這三人的故事沒有可證實的直接傳承。',
    '輪子能走進日常，還得有人肯拉、店肯賣，最後用起來順手。至於這三人是不是一棒接一棒發明出來的，我們查到的資料還不能證明。'],
];
for (const [sceneId, lineId, oldText, newText] of lineChanges) {
  const lines = scene(sceneId).lines.filter((line) => line.id === lineId);
  assert.equal(lines.length, 1, 'line drift ' + lineId);
  assert.equal(lines[0].text, oldText, 'old line drift ' + lineId);
  lines[0].text = newText;
}
const hookVisual = scene('hook-04').data;
const oldHookPrompt = 'Medium shot of a generic 1970s department-store buying office. A buyer studies an unbranded closed sample case with an unreadable neutral expression; only its ordinary top and carrying handle rise above a high counter. Keep the casters, rope, full silhouette, purchase order and sales floor out of frame until the story reaches the prototype and Macy demonstration. Soft warm lamp light, no signs, words or logos.';
assert.equal(hookVisual.prompt, oldHookPrompt);
hookVisual.prompt = oldHookPrompt.replace('generic 1970s', 'generic period-neutral');
const reveal = scene('turn-06');
assert.deepEqual(reveal.claims, ['t46']);
const oldRevealPrompt = 'Cute illustrative close-up at a period-neutral airport security checkpoint. One generic traveler in plain casual clothes strains to free an unbranded travel bag from a bulky separate metal luggage trolley; visible elastic bungee cords secure the bag to the trolley. The cords and unloading action are the focus, while the bag material and shell construction stay indistinct. Mild overhead lamp light. No precise year markers, words, logos or real-person likeness.';
assert.equal(reveal.data.prompt, oldRevealPrompt);
reveal.data.prompt = oldRevealPrompt.replace('The cords and unloading action', 'The cords and attempted unloading action');

const oldClaims = readPinned(r19, 'candidate/claims.md').toString('utf8');
const oldClaimLines = oldClaims.replace(/\r\n/g, '\n').split('\n');
const oldRows = oldClaimLines.filter((line) => /^[a-z]\d+[a-z]?｜/.test(line));
assert.equal(oldRows.length, 74);
const claimRewrites = new Map([
  ['h4', ['1970 年，Sadow 帶著樣品走進百貨公司',
    'Sadow 受訪回憶，他把輪子箱樣品帶到紐約大型百貨推銷；報導未標出逐店拜訪的確切年份']],
  ['o1', ['溫尼特卡歷史學會記載，畫家 Anita Willets-Burnham 在兒子改裝輪子箱後，與一家六口展開第二次環遊世界',
    '溫尼特卡歷史學會記載，畫家 Anita Willets-Burnham 在兒子改裝輪子箱後，與一家六口展開 1928 至 1930 年的第二趟長途旅行']],
  ['o32', ['溫尼特卡歷史學會記載，1928 至 1930 年第二次環遊期間安妮塔與兩名女兒沿途以畫作換餐食或住宿；行李仍伴隨旅程，不能推論為某站特定交易',
    '溫尼特卡歷史學會記載，1928 至 1930 年第二趟長途旅行期間安妮塔與兩名女兒沿途以畫作換餐食或住宿；行李仍伴隨旅程，不能推論為某站特定交易']],
  ['t5', ['Plath 受訪回憶在安檢排隊，看見前方旅客解彈力繩、將箱子從外置金屬推車卸下；與 Emmer 未標年份的草圖記憶無法排定先後',
    '2012 年 USA TODAY 對 Plath 的受訪報導記述，他在安檢排隊時看見前方旅客正費力想把以彈力繩固定的箱子從笨重金屬推車解下；未證實已完成卸箱，也無法排定與 Emmer 未標年份草圖回憶的先後']],
  ['t46', ['2012 年 USA TODAY 對 Plath 的受訪報導敘述，他在安檢隊伍看到前方旅客費力解開把箱子綁在笨重金屬推車上的彈力繩，將箱子從推車取下；此為受訪報導的回憶，非專利獨立證實該旅客的動作',
    '2012 年 USA TODAY 對 Plath 的受訪報導敘述，安檢隊伍前方旅客正費力想把以彈力繩綁在笨重金屬推車上的箱子卸下；報導未說是否成功，這也不是 Plath 的逐字引言']],
  ['n16', ['Sadow 回憶採購先拒絕、Macy 副總裁示範後進貨與當時替女性提箱的習慣；這些支持觀念與通路曾成為障礙，但不證明多位人物有直接發明傳承，也不推算銷量',
    'Sadow 回憶採購先拒絕、Macy 副總裁示範後進貨與當時替女性提箱的習慣；這些支持觀念與通路曾成為障礙，不能據此推算銷量或推定其他人直接承接他的設計']],
  ['n61', ['Winnetka 歷史學會記載 Anita 一家自製輪箱與丈夫嘲笑的反應；沒有史料把該家族案例直接接到 Sadow 或 Plath',
    'Winnetka 歷史學會記載 Anita 一家自製輪箱與丈夫嘲笑的反應；本集核對的該篇館方文章沒有說 Anita 家族設計直接影響 Sadow 或 Plath']],
  ['n63', ['Travelpro 公司稱 Plath 直立雙輪拉桿設計先在機組員間流行；與 Anita、Sadow 的直接發明傳承無獨立證據',
    'Travelpro 公司史稱 Plath 的直立雙輪拉桿箱先在機組員間流行，並把它寫作對 Sadow 輪箱的改良；該篇文章未記 Plath 親眼見過 Sadow 原型，也未提 Anita 家族的影響']],
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
assert.deepEqual(video.sources, before.sources, '18 public sources changed');
assert.deepEqual(video.scenes.map((item) => item.id), before.scenes.map((item) => item.id), 'scene order changed');
assert.deepEqual(video.scenes.flatMap((item) => item.lines.map((line) => line.id)),
  before.scenes.flatMap((item) => item.lines.map((line) => line.id)), 'line IDs changed');
assert.deepEqual(video.loops, before.loops, 'setup/payoff IDs changed');
const changedSceneIds = new Set(video.scenes
  .filter((item, index) => JSON.stringify(item) !== JSON.stringify(before.scenes[index]))
  .map((item) => item.id));
assert.deepEqual(changedSceneIds,
  new Set(['hook-04', 'origin-r12-01', 'origin-01b', 'turn-06', 'now-outro']));
for (let i = 0; i < video.scenes.length; i++) {
  const oldScene = before.scenes[i];
  const newScene = video.scenes[i];
  const copied = structuredClone(newScene);
  if (lineChanges.some(([id]) => id === oldScene.id)) copied.lines = oldScene.lines;
  if (oldScene.id === 'hook-04' || oldScene.id === 'turn-06') copied.data.prompt = oldScene.data.prompt;
  assert.deepEqual(copied, oldScene, 'unexpected scene change ' + oldScene.id);
}

const priorMap = JSON.parse(readPinned(r19, 'source-map.json'));
const plathSource = priorMap.source_index.filter((entry) => entry.url === plathUrl);
assert.equal(plathSource.length, 1, 'Plath map URL missing or duplicated');
assert.deepEqual(plathSource[0].claim_ids, ['h6', 't5', 't46', 't6', 't17', 't29']);
const sourceMap = {
  status: 'HOLD_UNREVIEWED_R20_SOURCE_MAP',
  derives_from_r19_manifest_sha256: expected.r19Manifest,
  derives_from_r19_fact_audit_sha256: expected.r19FactAudit,
  r19_review_not_inherited: true,
  source_index: structuredClone(priorMap.source_index),
  changed_line_ids: lineChanges.map(([, id]) => id),
  changed_claim_ids: [...claimRewrites.keys()],
  host_source_guard: 'HOLD: r20 has 74 PENDING claims; fresh worker IDs, verifier/listener/two-reader review and formal receipt are required after host six-chapter adoption.',
};
assert.deepEqual(sourceMap.source_index.map((entry) => entry.url), priorMap.source_index.map((entry) => entry.url));
const mappedIds = sourceMap.source_index.flatMap((entry) => entry.claim_ids);
assert.equal(mappedIds.length, 74);
assert.deepEqual(new Set(mappedIds), new Set(claimUrlById.keys()));
for (const entry of sourceMap.source_index) {
  for (const id of entry.claim_ids) assert.equal(claimUrlById.get(id), entry.url, 'source-map URL drift ' + id);
}
const priorAlignment = JSON.parse(readPinned(r19, 'source-alignment.json'));
const sourcePlan = JSON.parse(readPinned(sources25, 'candidate/series.json'));
assert.equal(sourcePlan.plan.sources.length, 25);
const replaceOnce = (value, beforeText, afterText, label) => {
  assert.equal(value.split(beforeText).length, 2, 'plan text drift ' + label);
  return value.replace(beforeText, afterText);
};
const tightenTravelPlan = (series, expectedSourceCount) => {
  assert.equal(series.plan.sources.length, expectedSourceCount);
  const plan = series.plan;
  assert.deepEqual(plan.must_verify[8].sources, [19]);
  plan.must_verify[8].claim = replaceOnce(plan.must_verify[8].claim,
    '1928 年第二次環遊', '1928 年第二趟長途旅行', 'must_verify 8');
  assert.equal(plan.sources[7].url, 'https://msmagazine.com/2021/08/18/gender-bias-covid-vaccine-katalin-kariko/');
  plan.sources[7].supports = replaceOnce(plan.sources[7].supports,
    '1928 年第二次環遊世界前', '1928 年第二趟長途旅行前', 'source 7');
  assert.equal(plan.sources[8].url,
    'https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/');
  plan.sources[8].supports = replaceOnce(plan.sources[8].supports,
    '1928–1930 年第二次環遊世界', '1928–1930 年第二趟長途旅行', 'source 8');
  assert.equal(plan.sources[16].url, 'https://www.winnetkahistory.org/who-were-the-burnhams/');
  plan.sources[16].supports = replaceOnce(plan.sources[16].supports,
    '第二次環遊期間', '1928–1930 年第二趟長途旅行期間', 'source 16');
  return series;
};
tightenTravelPlan(sourcePlan, 25);
const alignment = structuredClone(priorAlignment);
alignment.status = 'HOLD_UNREVIEWED_R20_74_CLAIM_ALIGNMENT';
delete alignment.derives_from_r18_manifest_sha256;
delete alignment.r18_claim_alignment_not_inherited;
alignment.derives_from_r19_manifest_sha256 = expected.r19Manifest;
alignment.derives_from_r19_fact_audit_sha256 = expected.r19FactAudit;
alignment.r19_claim_alignment_not_inherited = true;
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
assert.equal(screenplay(before), readPinned(r19, 'candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r19 script drift');
const script = Buffer.from(screenplay(video));
assert.ok(!script.equals(readPinned(r19, 'candidate/script.md')), 'r20 narration must reflect precision edits');
const priorSeries = JSON.parse(readPinned(r19, 'candidate/series.json'));
const series = tightenTravelPlan(structuredClone(priorSeries), 23);
assert.deepEqual(series.plan.sources.map((entry) => entry.url),
  priorSeries.plan.sources.map((entry) => entry.url), 'candidate source URL/order drift');
assert.deepEqual(sourcePlan.plan.sources.slice(0, 23).map((entry) => entry.url),
  series.plan.sources.map((entry) => entry.url), 'proposed plan source URL/order drift');
const lexicon = JSON.parse(readPinned(r19, 'candidate/lexicon.json'));
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
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_PENDING_R20_REVIEW',
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
  r19_fact_audit_sha256: expected.r19FactAudit,
  r19_claim_audit_findings_addressed_in_draft: ['t5', 't46', 'h4', 'o1', 'n61'],
  measured_tts_and_cut: 'NOT_RUN',
  independent_full_r20_review: 'NOT_RUN',
  six_chapter_host_bridge: 'NOT_INSTALLED_OR_FORMALLY_REVIEWED',
  worker_claim_id_and_source_merge: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  host_import_or_paid_media: 'NOT_RUN',
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', json(series)],
  ['candidate/lexicon.json', readPinned(r19, 'candidate/lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['source-alignment.json', json(alignment)],
  ['validation.json', json(validation)],
  ['plan-source-addition.json', readPinned(r19, 'plan-source-addition.json')],
  ['proposed-25-source-series.json', json(sourcePlan)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE',
  slug: video.slug,
  derives_from_r19_manifest_sha256: expected.r19Manifest,
  derives_from_r19_independent_fact_audit_sha256: expected.r19FactAudit,
  derives_from_r16_source_plan_manifest_sha256: expected.sources25Manifest,
  r19_review_not_inherited: true,
  source_snapshot: r19Manifest.source_snapshot,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r19_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(['--preview', '--write', '--check'].includes(action), 'use --preview, --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r20');
  if (action === '--preview') {
    assert.ok(!fs.existsSync(file), 'preview requires a fresh r20 output slot ' + name);
  } else if (action === '--write') {
    assert.ok(!fs.existsSync(file), 'r20 output exists; do not overwrite ' + name);
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
