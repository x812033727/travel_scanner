// A01-only offline r11 correction over frozen r10; no host/media actions.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r10 = path.resolve(here, '../A01-editorial-candidate-20261018-r10');
const expected = {
  r10_manifest: '6f60a5eca2e907ab494bc0fcea44d70b323e7968ac8ae435678c08f7449d5701',
  r10_review: 'dc279ebc66884d16c4c0bf4c4cd11a9cf23fdb130c3a3ede2a7551da07885e29',
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const readR10 = (name) => fs.readFileSync(path.join(r10, name));
const candidateNames = ['video.json', 'series.json', 'lexicon.json', 'script.md', 'claims.md'];
assert.equal(sha(readR10('manifest.json')), expected.r10_manifest, 'r10 manifest drift');
assert.equal(sha(readR10('independent-full-review-20261018.md')), expected.r10_review, 'r10 review drift');
const r10Manifest = JSON.parse(readR10('manifest.json'));
for (const name of candidateNames) {
  assert.equal(sha(readR10('candidate/' + name)), r10Manifest.outputs_sha256['candidate/' + name], 'r10 candidate drift ' + name);
}
for (const name of ['source-map.json', 'validation.json']) {
  assert.equal(sha(readR10(name)), r10Manifest.outputs_sha256[name], 'r10 metadata drift ' + name);
}
assert.equal(sha(readR10('README.md')), r10Manifest.readme_sha256, 'r10 README drift');

const previous = JSON.parse(readR10('candidate/video.json'));
const video = structuredClone(previous);
const series = JSON.parse(readR10('candidate/series.json'));
const lexicon = JSON.parse(readR10('candidate/lexicon.json'));
assert.equal(video.slug, 'story-rolling-suitcase-v2');
assert.deepEqual(video.target_minutes, [7, 8]);
assert.equal(series.target_minutes, 10, 'pilot series duration drift');
const scene = (id) => {
  const matches = video.scenes.filter((entry) => entry.id === id);
  assert.equal(matches.length, 1, 'expected scene ' + id);
  return matches[0];
};
const line = (sceneId, id, oldText) => {
  const matches = scene(sceneId).lines.filter((entry) => entry.id === id);
  assert.equal(matches.length, 1, 'expected line ' + id);
  assert.equal(matches[0].text, oldText, 'r10 line drift ' + id);
  return matches[0];
};

// Plath's undated garage/trolley recollection is separate from Travelpro's
// 1987 design year. The latter also differs from his 1988 alumni note.
line('hook-06', 'jtmg', '依 Travelpro 的回顧，1987 年有位機師把箱子帶進車庫。').text =
  '安檢口的一幕，讓一位機師回車庫動手。';
line('turn-09', 'jm3w', '另一份 Travelpro 公司回顧說，1987 年 Plath 在車庫做出了 Rollaboard。').text =
  'Travelpro 把直立雙輪拉桿設計記在 1987 年；Plath 自己的簡歷卻寫 1988 年。';
const garageAnchor = 'Recurring illustrative garage composition: plain wood workbench centered, small metal tool tray at left, warm task lamp at right, unmarked storage shelf behind. Use the same camera angle, bench arrangement and warm palette in hook-06 and turn-07; after a hook-06 still is approved, use it as the turn-07 composition reference.';
scene('hook-06').data.prompt =
  `Cute medium close-up in a generic home garage with no visible calendar or precise decade markers. ${garageAnchor} An anonymous pilot in a plain work shirt leans over a closed unbranded suitcase before beginning an experiment. Keep the trolley joint, fasteners, finished wheel layout and any telescoping handle hidden until their separate story moments. This illustrates an undated garage recollection, not the date of the later upright design. No words, logos or real-person likeness.`;
scene('turn-07').data.prompt =
  `Cute medium close-up returning to the same generic home garage view from hook-06, with no visible calendar or precise decade markers. ${garageAnchor} Anonymous hands fasten a separate compact metal luggage trolley to an upright hard-shell unbranded suitcase with a screw; make the two joined objects legible. This illustrates the undated garage-and-trolley episode, not proof of the later upright design's date. No telescoping-handle reveal, text, logos or real-person likeness.`;
scene('turn-09').data.prompt =
  'Cute medium product-study view at a neutral plain worktable, outside the garage visual callback. An anonymous hand rests near a closed unbranded suitcase while the lower case and top stay cropped to withhold its wheel layout and handle until turn-09b. The narration attributes two different years to two sources; the illustration represents neither as a dated historical photograph. No calendar, date text, patent number, logo or real-person likeness.';
scene('turn-09b').data.prompt =
  'Cute medium side view of an illustrative upright rolling suitcase on a neutral plain background, outside the garage visual callback. An anonymous hand extends a retractable handle from a compact case with exactly two small base wheels. This clarifies the design described in the separately attributed 1987/1988 accounts, not a photographed historical prototype or a dated garage event. No calendar, date text, logo or real-person likeness.';
const garageLoop = video.loops.find((entry) => entry.setup === 'jtmg' && entry.payoff === '3zwf');
assert.ok(garageLoop, 'r10 garage loop drift');
garageLoop.payoff = 'q4zn';
garageLoop.what = '未標年份的車庫實驗；箱子與外置推車鎖在一起';

assert.equal(video.youtube.description,
  '1928 年出發的一家人已帶著自製輪子箱；到了 1970 年，Sadow 把四輪箱送上百貨貨架。往後，機師的直立拉桿箱與 1997／2000 年的四輪設計，繼續改變旅客帶著行李移動的方式。\n\n箱子早就能滾著走，還缺什麼，才能走進旅客的日常？',
  'r10 public description drift');
video.youtube.description =
  '1928 年，一家人帶著自製輪子箱出發；1970 年，Sadow 的四輪箱終於走進百貨。往後，機師的直立拉桿箱與 1997 年的平衡四輪直立箱，讓旅客有不同的移動方式。\n\n箱子早就能滾著走，還缺什麼，才能走進旅客的日常？';

line('idea-memory', 'r14i01', '三十多年後，Sadow 一家從阿魯巴返程；兩只二十七吋傳統箱裡，裝滿了孩子們的行李。').text =
  '三十多年後，Sadow 一家從阿魯巴返程；因為帶著兩個孩子，兩只二十七吋傳統箱都塞得滿滿。';
scene('idea-memory').data.prompt =
  'Cute medium-wide illustration of a separate family returning from Aruba around 1970. An anonymous couple and two children pause with two large, tightly packed, unwheeled suitcases; the adult holding both handles visibly strains. Do not suggest that every item inside belongs to the children; the exact contents are unknown. This is a different journey and family from the 1939 Anita scene, not a direct inventor handoff. Keep the earlier wheeled platform and any later prototype out of frame. No printed dimensions, labels, airline marks or real-person likeness.';

// Two dense narrated lines were flagged for oral comprehension. Keep the
// Shiller → assistant → Sadow → buyers attribution chain intact.
line('origin-budget', 'r14o01', '館方寫她第一次窮遊：每到一個新地方，丈夫去找便宜住處，安妮塔就帶著四個孩子，守著還沒地方放的行李。').text =
  '1921 年一家人窮遊。到了新地方，丈夫去找便宜住處；安妮塔陪四個孩子看著行李。';
line('engine-porter', 'r17e01', '耶魯教授 Shiller 說，他的助理後來打電話問 Sadow，聽到百貨採購當時的另一個理由：車站不是有搬運工嗎？').text =
  'Shiller 說，助理打電話問過 Sadow。據 Sadow 轉述，採購還問：車站不是有搬運工嗎？';

// The substantial three-barrier answer moves to the evidence-backed retail
// payoff. The outro repeats only the conclusion, comment prompt and subscribe.
const retail = scene('now-1993-retail');
assert.deepEqual(retail.lines.map((item) => item.id), ['r3n03'], 'r10 retail line drift');
retail.lines.unshift({ id: 'r11n01', text: '三關：拉箱被笑、百貨拒賣、安檢拆推車。' });
line('now-1993-retail', 'r3n03', '回到開頭：機組有人用，旅客也看見；到 1993 年，記者寫百貨和行李店已有多種輪箱可買。').text =
  '直立拉桿先被機組採用，旅客看見；1993 年記者寫，百貨已有多品牌可買。';
line('now-outro', 'g5b8', '輪子早有，卻卡在三關：拉箱被笑、百貨拒賣、外置推車安檢得拆。示範與上架，加上直立拉桿，才讓機組和旅客漸漸用起來；三人的故事沒有可證實的直接傳承。').text =
  '輪子不是唯一答案；願意拉、買得到、用得順手，才走進日常。這三人的故事沒有可證實的直接傳承。';

const claimRows = readR10('candidate/claims.md').toString('utf8').replace(/\r\n/g, '\n').split('\n');
const replaceClaim = (id, before, after) => {
  const positions = claimRows.map((row, index) => row.startsWith(id + '｜') ? index : -1).filter((index) => index >= 0);
  assert.equal(positions.length, 1, 'expected claim ' + id);
  assert.equal(claimRows[positions[0]], before, 'r10 claim drift ' + id);
  claimRows[positions[0]] = after;
};
const insertAfterClaim = (id, rows) => {
  const index = claimRows.findIndex((row) => row.startsWith(id + '｜'));
  assert.ok(index >= 0, 'claim insert anchor ' + id);
  claimRows.splice(index + 1, 0, ...rows);
};
replaceClaim('h6',
  'h6｜Travelpro 公司沿革稱，1987 年一位機師把箱子帶進車庫製作新輪子箱｜https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage｜2026-09-28｜hook-06｜PENDING',
  'h6｜Plath 的受訪回憶記他看見旅客在安檢拆外置推車後，回車庫把硬殼箱與推車鎖在一起；該段未指明精確年份，不與 Travelpro 的 1987 設計年份併為同一事｜https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603｜2026-10-18｜hook-06｜PENDING');
replaceClaim('t7',
  't7｜Travelpro 公司沿革稱，Plath 於 1987 年在車庫製作 Rollaboard；外形在下一鏡示意｜https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage｜2026-09-28｜turn-09｜PENDING',
  't7｜Travelpro 公司沿革將 Plath 的直立雙輪伸縮拉桿設計記於 1987 年；它另記 1989 年從車庫搬倉，未直接記 1987 年在車庫初作｜https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage｜2026-10-18｜turn-09｜PENDING');
insertAfterClaim('t7', [
  't7b｜Plath 本人在 2024 年校友刊第 17 頁簡歷寫 1988 年發明直立 Travelpro Rollaboard；與 Travelpro 1987 年公司說法尚有一年差異，不定讞精確年份｜https://www.sl8.com/journal/may24/journal_images/Chinook_2024_5-3-24_FINAL.pdf｜2026-10-18｜turn-09｜PENDING',
]);
scene('turn-09').claims.push('t7b');
replaceClaim('i35',
  'i35｜Sadow 回憶約 1970 年與妻子和兩個孩子從阿魯巴回程，兩只 27 吋傳統行李箱因孩子的行李而裝得滿滿；與 Anita 的故事沒有可證實的直接交接｜https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469｜2026-10-18｜idea-memory｜PENDING',
  'i35｜Sadow 回憶與妻子和兩個孩子從阿魯巴返程，因孩子同行，兩只 27 吋傳統箱塞得滿滿；訪談未列箱內物品的所有權，與 Anita 的故事也無可證實的直接交接｜https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469｜2026-10-18｜idea-memory｜PENDING');
insertAfterClaim('n64', [
  'n65｜Winnetka 歷史學會記 Anita 的丈夫嘲笑妻兒輪箱；此處回扣當時拉箱曾受嘲笑的一例，不推成所有人的看法｜https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/｜2026-10-18｜now-1993-retail｜PENDING',
  'n66｜Plath 專利記外置推車於安檢等場景須反覆卸裝；此處回扣使用設計的阻力，不說 Plath 用過 Shiller 的箱子｜https://patents.google.com/patent/US4995487A/en｜2026-10-18｜now-1993-retail｜PENDING',
  'n67｜Sadow 自述多家百貨採購起初拒絕其輪箱樣品；此處回扣零售採納阻力，不推算後來實際銷量｜https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469｜2026-10-18｜now-1993-retail｜PENDING',
]);
retail.claims.push('n65', 'n66', 'n67');
replaceClaim('n16',
  'n16｜Sadow 回憶採購起初拒絕、Macy 副總裁示範後進貨及當時替女性提箱的習慣；此為社會和零售阻礙的兩種證據，不證明與 Anita 或 Plath 有直接發明傳承｜https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469｜2026-10-18｜now-outro｜PENDING',
  'n16｜Sadow 回憶採購先拒絕、Macy 副總裁示範後進貨與當時替女性提箱的習慣；這些支持觀念與通路曾成為障礙，但不證明多位人物有直接發明傳承，也不推算銷量｜https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469｜2026-10-18｜now-outro｜PENDING');
const claims = Buffer.from(claimRows.join('\n'));

const claimEntries = claimRows.filter((row) => /^[a-z]\d+[a-z]?｜/.test(row)).map((row) => row.split('｜'));
const claimScene = new Map(video.scenes.flatMap((item) => (item.claims ?? []).map((id) => [id, item.id])));
assert.equal(claimScene.size, video.scenes.reduce((sum, item) => sum + (item.claims ?? []).length, 0), 'duplicate claim ID');
assert.deepEqual(new Set(claimEntries.map((cells) => cells[0])), new Set(claimScene.keys()), 'claim rows and scene IDs must match');
for (const cells of claimEntries) {
  assert.equal(cells.length, 6, 'malformed claim row ' + cells[0]);
  assert.equal(cells[4], claimScene.get(cells[0]), 'claim scene mismatch ' + cells[0]);
  assert.equal(cells[5], 'PENDING', 'no approval inherited');
}

// Add only the newly spoken 1988 primary note. All other public source URLs
// are inherited from r10, then reconciled exactly against every claim row.
const newSource = {
  title: 'Plath 2024 年校友刊自述（第 17 頁）',
  url: 'https://www.sl8.com/journal/may24/journal_images/Chinook_2024_5-3-24_FINAL.pdf',
  checked_on: '2026-10-18',
};
assert.ok(!previous.sources.some((item) => item.url === newSource.url), '1988 note already in r10 sources');
video.sources = [...previous.sources, newSource];
const datesByUrl = new Map();
const claimIdsByUrl = new Map();
for (const cells of claimEntries) {
  if (!cells[2]) continue;
  assert.ok(/^2026-\d\d-\d\d$/.test(cells[3]), 'missing checked_on ' + cells[0]);
  if (!datesByUrl.has(cells[2]) || cells[3] > datesByUrl.get(cells[2])) datesByUrl.set(cells[2], cells[3]);
  if (!claimIdsByUrl.has(cells[2])) claimIdsByUrl.set(cells[2], []);
  claimIdsByUrl.get(cells[2]).push(cells[0]);
}
assert.equal(video.sources.length, 17, 'new spoken 1988 source should make seventeen distinct sources');
assert.equal(new Set(video.sources.map((item) => item.url)).size, 17, 'duplicate public source URL');
assert.deepEqual(new Set(video.sources.map((item) => item.url)), new Set(datesByUrl.keys()), 'public sources must exactly match claim URL set');
for (const source of video.sources) {
  assert.ok(source.title && /^https:\/\//.test(source.url), 'invalid public source');
  assert.equal(source.checked_on, datesByUrl.get(source.url), 'checked_on mismatch ' + source.url);
}

const allLines = video.scenes.flatMap((item) => item.lines);
const sceneByLine = new Map(video.scenes.flatMap((item) => item.lines.map((part) => [part.id, item.id])));
assert.equal(sceneByLine.size, allLines.length, 'duplicate line ID');
assert.equal(new Set(video.scenes.map((item) => item.id)).size, video.scenes.length, 'duplicate scene ID');
const sceneIndex = new Map(video.scenes.map((item, index) => [item.id, index]));
for (const loop of video.loops) {
  assert.ok(sceneByLine.has(loop.setup) && sceneByLine.has(loop.payoff), 'missing loop line ' + loop.setup);
  assert.ok(sceneIndex.get(sceneByLine.get(loop.setup)) < sceneIndex.get(sceneByLine.get(loop.payoff)), 'reversed loop ' + loop.setup);
}
assert.deepEqual(video.loops.find((item) => item.setup === 'jtmg')?.payoff, 'q4zn', 'undated garage payoff moved');
assert.deepEqual(video.loops.find((item) => item.setup === 'x7r4')?.payoff, 'r3n03', 'adoption payoff drift');
const module = (relative) => import(pathToFileURL(path.join(repo, relative)));
const [{ screenplay }, { estimateTimeline, spokenUnits }, { lintVideo }, { cuteStoryVisualProblems }] = await Promise.all([
  module('tools/video/core/screenplay.mjs'),
  module('tools/video/core/timeline.mjs'),
  module('tools/video/core/lint.mjs'),
  module('tools/video/automation/story.mjs'),
]);
assert.equal(screenplay(previous), readR10('candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r10 screenplay drift');
const script = Buffer.from(screenplay(video));
const lintContext = {
  lexicon,
  brief: fs.readFileSync(path.join(here, '../A01-story-depth-candidate-20261018-r4/base/brief.md'), 'utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(video, lintContext);
const lintAt300 = lintVideo(video, { ...lintContext, cpm: 300 });
const cute = cuteStoryVisualProblems(video);
assert.equal(lint.errors.length, 0, 'video lint errors: ' + JSON.stringify(lint.errors));
assert.equal(lintAt300.errors.length, 0, '300-CPM video lint errors: ' + JSON.stringify(lintAt300.errors));
assert.equal(cute.length, 0, 'cute visual errors: ' + JSON.stringify(cute));
const timing = Object.fromEntries([250, 275, 300].map((cpm) => [cpm, Number((estimateTimeline(video, cpm).total_frames / 30).toFixed(1))]));
const timeline300 = estimateTimeline(video, 300);
const line300 = new Map(timeline300.lines.map((item) => [item.id, item]));
const lineTiming = (setup, payoff) => ({
  setup,
  payoff,
  setup_scene_id: sceneByLine.get(setup),
  payoff_scene_id: sceneByLine.get(payoff),
  payoff_scene_ordinal: sceneIndex.get(sceneByLine.get(payoff)) + 1,
  setup_end_seconds: Number((line300.get(setup).end_frame / 30).toFixed(1)),
  payoff_start_seconds: Number((line300.get(payoff).start_frame / 30).toFixed(1)),
  intervening_seconds: Number(((line300.get(payoff).start_frame - line300.get(setup).end_frame) / 30).toFixed(1)),
});
const outroLines = scene('now-outro').lines;
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_UNREVIEWED',
  target_body_seconds: [420, 480],
  scenes: video.scenes.length,
  lines: allLines.length,
  claims: claimEntries.length,
  loops: video.loops.length,
  spoken_units: allLines.reduce((sum, item) => sum + spokenUnits(item.text), 0),
  estimated_body_seconds_not_tts: timing,
  estimated_300_cpm_in_owner_range: timing[300] >= 420 && timing[300] <= 480,
  loop_300_cpm_not_tts: [lineTiming('jtmg', 'q4zn'), lineTiming('x7r4', 'r3n03')],
  outro_speech_units_not_tts: outroLines.reduce((sum, item) => sum + spokenUnits(item.text), 0),
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_errors_at_300_cpm: lintAt300.errors,
  cute_visual_errors: cute,
  public_sources: video.sources.length,
  claim_source_urls: datesByUrl.size,
  source_index_matches_claims: true,
  measured_tts_and_cut: 'NOT_RUN',
  independent_full_r11_review: 'NOT_RUN',
  host_worker_source_merge_and_duration_gate: 'NOT_CHECKED_OR_INSTALLED',
  script_review_receipt: 'NOT_ISSUED',
  host_import_or_paid_media: 'NOT_RUN',
};
const sourceMap = {
  status: 'PENDING_INDEPENDENT_FULL_R11_REVIEW',
  derives_from_r10_manifest_sha256: expected.r10_manifest,
  resolves_report_sha256: expected.r10_review,
  prior_review_not_inherited: true,
  source_index: [...claimIdsByUrl].map(([url, ids]) => ({ url, claim_ids: ids })),
  changed_line_ids: ['jtmg', 'jm3w', 'r14i01', 'r14o01', 'r17e01', 'r3n03', 'g5b8'],
  added_line_ids: ['r11n01'],
  changed_visual_scene_ids: ['hook-06', 'turn-07', 'turn-09', 'turn-09b', 'idea-memory'],
  changed_claim_ids: ['h6', 't7', 'i35', 'n16'],
  added_claim_ids: ['t7b', 'n65', 'n66', 'n67'],
  garage_loop: { setup: 'jtmg', payoff: 'q4zn', note: 'Plath undated garage/trolley recollection only; no asserted ordering relative to Travelpro 1987 design' },
  adoption_loop: { setup: 'x7r4', payoff: 'r3n03', first_answer_line: 'r11n01', note: 'social, retail and usability barriers stated immediately before 1993 availability evidence; availability is not sales volume' },
  year_guard: 'Travelpro says 1987 for upright two-wheel retractable-handle design. Plath himself writes 1988 in 2024 alumni note. Neither source fixes the year of his separate garage/trolley recollection.',
  host_adoption_guard: 'PENDING: worker remerges plan sources. Inspect and reconcile live six-chapter source list and output description without overwriting provenance.',
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', readR10('candidate/series.json')],
  ['candidate/lexicon.json', readR10('candidate/lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['validation.json', json(validation)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE',
  slug: video.slug,
  derives_from_r10_manifest_sha256: expected.r10_manifest,
  resolves_report_sha256: expected.r10_review,
  source_snapshot: r10Manifest.source_snapshot,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r10_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r11');
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), 'missing output ' + name);
    assert.ok(fs.readFileSync(file).equals(bytes), 'stale output ' + name);
  }
}
console.log(JSON.stringify({ action, status: validation.status, scenes: validation.scenes, lines: validation.lines, claims: validation.claims, loops: validation.loops, sources: validation.public_sources, spoken_units: validation.spoken_units, seconds_250: timing[250], seconds_275: timing[275], seconds_300: timing[300], in_range_at_300: validation.estimated_300_cpm_in_owner_range, outro_units: validation.outro_speech_units_not_tts, lint_errors: lint.errors.length, cute_errors: cute.length }));
