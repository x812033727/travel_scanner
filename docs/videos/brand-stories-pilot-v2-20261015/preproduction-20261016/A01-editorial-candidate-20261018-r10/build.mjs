// A01-only offline editorial corrections over frozen r9. Never touches production.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r9 = path.resolve(here, '../A01-duration-decision-20261018-r9');
const review = path.resolve(here, '../A01-r8-independent-full-editorial-review-20261018.md');
const expected = {
  r9_manifest: 'e414858f7ec6ebd0b07711e0a025cd96c04a80434c9cfff5ccbc6ebf7e498ee4',
  r8_review: '71ef4677c20262ad1df336c626a1662d3c010f1938c3225d6dc9cbcc5ad88cf5',
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const readR9 = (name) => fs.readFileSync(path.join(r9, name));
const candidateNames = ['video.json', 'series.json', 'lexicon.json', 'script.md', 'claims.md'];

assert.equal(sha(readR9('manifest.json')), expected.r9_manifest, 'r9 manifest drift');
assert.equal(sha(fs.readFileSync(review)), expected.r8_review, 'full editorial review drift');
const r9Manifest = JSON.parse(readR9('manifest.json'));
for (const name of candidateNames) {
  assert.equal(sha(readR9('candidate/' + name)), r9Manifest.outputs_sha256['candidate/' + name], 'r9 candidate drift ' + name);
}
assert.equal(sha(readR9('validation.json')), r9Manifest.outputs_sha256['validation.json'], 'r9 validation drift');
assert.equal(sha(readR9('README.md')), r9Manifest.readme_sha256, 'r9 README drift');

const before = JSON.parse(readR9('candidate/video.json'));
const video = structuredClone(before);
assert.equal(video.slug, 'story-rolling-suitcase-v2');
assert.deepEqual(video.target_minutes, [7, 8], 'A01 duration drift');
const series = JSON.parse(readR9('candidate/series.json'));
const lexicon = JSON.parse(readR9('candidate/lexicon.json'));
assert.equal(series.target_minutes, 10, 'shared pilot target must stay ten minutes');
const scene = (id) => {
  const matches = video.scenes.filter((item) => item.id === id);
  assert.equal(matches.length, 1, 'expected scene ' + id);
  return matches[0];
};
const line = (sceneId, lineId, oldText) => {
  const matches = scene(sceneId).lines.filter((item) => item.id === lineId);
  assert.equal(matches.length, 1, 'expected line ' + lineId);
  assert.equal(matches[0].text, oldText, 'r9 line drift ' + lineId);
  return matches[0];
};
const removeScene = (id) => {
  const index = video.scenes.findIndex((item) => item.id === id);
  assert.ok(index >= 0 && video.scenes.filter((item) => item.id === id).length === 1, 'scene to remove drift ' + id);
  video.scenes.splice(index, 1);
};

// The society describes waiting with the children and luggage after train
// arrival. It does not place that waiting at a specific station.
line('origin-budget', 'r14o01', '館方寫她第一次窮遊：每到新地方，丈夫去找便宜住處，安妮塔就帶著四個孩子，在車站守著還沒地方放的行李。').text =
  '館方寫她第一次窮遊：每到一個新地方，丈夫去找便宜住處，安妮塔就帶著四個孩子，守著還沒地方放的行李。';
scene('origin-budget').data.prompt =
  'Cute illustration of a family pausing with ordinary unwheeled luggage after arriving in a new place during their earlier 1921 journey. An anonymous mother waits with four children and several cases while another adult goes to seek low-cost lodging. The waiting place is deliberately unspecified: no station platform, station building or sign. This represents a repeated arrangement, not one documented location or a 1928 wheeled-case event. No readable text, logos or real-person likeness.';

// The previous transition repeated the already-established burden. Let the
// new chapter introduce the separate Aruba trip, dimensions and children.
removeScene('origin-06');
line('idea-memory', 'r14i01', '從阿魯巴返程，兩只二十七吋箱子裡，塞滿了孩子們的行李。').text =
  '三十多年後，Sadow 一家從阿魯巴返程；兩只二十七吋傳統箱裡，裝滿了孩子們的行李。';
scene('idea-memory').data.prompt =
  'Cute medium-wide illustration of a separate family returning from Aruba around 1970. An anonymous couple and two children pause with two large, tightly packed, unwheeled suitcases; the adult holding both handles visibly strains. This is a different journey and family from the 1939 Anita scene, not a direct inventor handoff. Keep the earlier wheeled platform and any later prototype out of frame. No printed dimensions, labels, airline marks or real-person likeness.';

// The patent-bottom construction would require a technical drawing the cute
// image route cannot safely reconstruct; the relevant strap and handle follow.
removeScene('idea-r12-02');

// Return to the opening garage with a deliberately matching composition. The
// reveal still waits for turn-09b and no generated image is claimed approved.
const garageAnchor = 'Recurring illustrative garage composition: plain wood workbench centered, small metal tool tray at left, warm task lamp at right, unmarked storage shelf behind. Use the same camera angle, bench arrangement and warm palette in hook-06 and turn-09; once a hook-06 still is approved, reuse it as the turn-09 composition reference.';
scene('hook-06').data.prompt =
  `Cute medium close-up in a generic late-1980s home garage. ${garageAnchor} An anonymous middle-aged man in a plain work shirt leans over a closed unbranded suitcase before beginning work. The bench edge conceals loose hardware, the lower case and any finished wheel layout; no telescoping handle is visible. This is a story illustration, not a documented historical garage or prototype. No words, logos or real-person likeness.`;
scene('turn-09').data.prompt =
  `Cute medium close-up returning to the very same generic late-1980s garage view from hook-06. ${garageAnchor} Anonymous hands begin work on the closed unbranded suitcase at the same bench. Keep the base, two-wheel layout and telescoping handle hidden until turn-09b. This is an illustrative visual callback, not a documented historical garage or prototype. No words, logos or real-person likeness.`;

// The opening's big question is adoption, not merely the shape reveal. The
// first loop remains a shorter garage-design callback; the second is paid off
// by the later retail/adoption evidence, explicitly in the spoken line.
const garageLoop = video.loops.find((item) => item.setup === 'jtmg' && item.payoff === '3zwf');
assert.ok(garageLoop, 'r9 garage loop drift');
garageLoop.what = '開場未露車庫完成品；後段用同一構圖回到車庫，再揭示直立雙輪伸縮拉桿';
assert.ok(!video.loops.some((item) => item.setup === 'x7r4'), 'opening adoption loop already exists');
video.loops.push({
  setup: 'x7r4',
  payoff: 'r3n03',
  what: '機組採用、旅客看見，1993 年商店有多品牌可買',
});

// Put market context before the reporter's individual carry-on test. Once
// she loads the outer pocket, the question leads directly to the result.
const retail = scene('now-1993-retail');
const retailIndex = video.scenes.indexOf(retail);
assert.equal(video.scenes[retailIndex - 1]?.id, 'now-1993-test', 'r9 retail order drift');
video.scenes.splice(retailIndex, 1);
const testIndex = video.scenes.findIndex((item) => item.id === 'now-1993-test');
video.scenes.splice(testIndex, 0, retail);
line('now-1993-retail', 'r3n03', '她寫，Travelpro 起初靠郵購；到了這時，百貨和行李店也能選到不同品牌。').text =
  '回到開頭：機組有人用，旅客也看見；到 1993 年，記者寫百貨和行李店已有多種輪箱可買。';
line('now-1993-test', 'r3n02', '到了 1993 年，《洛杉磯時報》一位記者，真的把四家輪子登機箱帶上路測試。').text =
  '那位記者還把四家輪子登機箱帶上路，看看它們在地面和機艙裡到底怎樣。';
const question = scene('now-consumer-question');
assert.equal(video.scenes[video.scenes.indexOf(question) + 1]?.id, 'now-1993-retail', 'r9 question order drift after retail move');
video.scenes.splice(video.scenes.indexOf(question), 1);
const stowIndex = video.scenes.findIndex((item) => item.id === 'now-1993-stow');
assert.equal(video.scenes[stowIndex - 1]?.id, 'now-1993-limit', 'r9 limit/stow order drift');
video.scenes.splice(stowIndex, 0, question);
line('now-consumer-question', 'r3n01', '如果外袋多裝了衣物和平裝書，登機後還放得進座位下或頭頂櫃嗎？').text =
  '外袋多放了衣物和書，這只箱子還塞得進座位下或頭頂櫃嗎？';
question.data.prompt =
  'Cute early-1990s aircraft-cabin illustration immediately after the reporter has placed some extra clothes and paperback books in the expandable outside pocket of a plain two-wheel carry-on. The pocket is modestly expanded but not stuffed or bulging. An anonymous traveler pauses before trying the still-closed overhead bin and under-seat space; do not show whether this one bag fits, a shop display, readable text, logos or real-person likeness.';

// Answer the title's three barriers explicitly. This is a synthesis of
// separately sourced histories, not a claim of direct inventor lineage.
line('now-outro', 'g5b8', '輪子早有人裝上箱子；自製、進貨、改直立，一次次解開旅途卡關，它才走進日常。').text =
  '輪子早有，卻卡在三關：拉箱被笑、百貨拒賣、外置推車安檢得拆。示範與上架，加上直立拉桿，才讓機組和旅客漸漸用起來；三人的故事沒有可證實的直接傳承。';
line('now-outro', 'xjmb', '你最記得哪次箱子卡關：安檢、登機，還是樓梯？').text =
  '你的箱子最常卡在哪：安檢、登機，還是樓梯？';
line('now-outro', 'ek2s', '想聽日用品背後這些有轉折的故事，歡迎訂閱。').text =
  '更多日用品故事，歡迎訂閱。';

const claimRows = readR9('candidate/claims.md').toString('utf8').replace(/\r\n/g, '\n').split('\n');
const replaceClaim = (id, oldText, newText) => {
  const positions = claimRows.map((row, index) => row.startsWith(id + '｜') ? index : -1).filter((index) => index >= 0);
  assert.equal(positions.length, 1, 'expected claim ' + id);
  assert.equal(claimRows[positions[0]], oldText, 'r9 claim drift ' + id);
  claimRows[positions[0]] = newText;
};
const removeClaim = (id) => {
  const positions = claimRows.map((row, index) => row.startsWith(id + '｜') ? index : -1).filter((index) => index >= 0);
  assert.equal(positions.length, 1, 'expected claim to remove ' + id);
  claimRows.splice(positions[0], 1);
};
replaceClaim('o30',
  'o30｜溫尼特卡歷史學會另文記載 1921 年首次經濟旅行時，每到新地方父親去找廉價住宿，Anita 和四個孩子留在車站守著行李；這不是 1928 年輪箱旅程的一次特定車站事件｜https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/｜2026-10-18｜origin-budget｜PENDING',
  'o30｜溫尼特卡歷史學會另文記載 1921 年首次經濟旅行時，乘火車抵達新地方後父親去找廉價住宿，Anita 和四個孩子守著行李；等候地點未指明，不能拍成特定車站事件｜https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/｜2026-10-18｜origin-budget｜PENDING');
removeClaim('o33');
replaceClaim('i35',
  'i35｜Sadow 回憶，他與妻子和兩個孩子從阿魯巴回程，兩只 27 吋行李箱因孩子的行李而裝得滿滿｜https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469｜2026-10-18｜idea-memory｜PENDING',
  'i35｜Sadow 回憶約 1970 年與妻子和兩個孩子從阿魯巴回程，兩只 27 吋傳統行李箱因孩子的行李而裝得滿滿；與 Anita 的故事沒有可證實的直接交接｜https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469｜2026-10-18｜idea-memory｜PENDING');
removeClaim('i29');
replaceClaim('n56',
  'n56｜Dash 指 Travelpro 起初以郵購販售；到 1993 年，多個品牌的輪子登機箱可在主要百貨或行李專門店選購；不推算銷量｜https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html｜2026-10-18｜now-1993-retail｜PENDING',
  'n56｜Dash 在 1993 年記載 Travelpro 起初以郵購販售，當時已有多個品牌的輪子登機箱可在主要百貨或行李專門店選購；這是可買到的通路證據，不推算銷量｜https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html｜2026-10-18｜now-1993-retail｜PENDING');
replaceClaim('n16',
  'n16｜輪子箱從家庭自製、百貨展示到一體式機組行李，有不同人物各自解決的使用與採用障礙；三條證據不構成直接發明傳承｜https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469｜2026-10-16｜now-outro｜PENDING',
  'n16｜Sadow 回憶採購起初拒絕、Macy 副總裁示範後進貨及當時替女性提箱的習慣；此為社會和零售阻礙的兩種證據，不證明與 Anita 或 Plath 有直接發明傳承｜https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469｜2026-10-18｜now-outro｜PENDING');
const insertAfterClaim = (id, newRows) => {
  const index = claimRows.findIndex((row) => row.startsWith(id + '｜'));
  assert.ok(index >= 0, 'insert anchor missing ' + id);
  claimRows.splice(index + 1, 0, ...newRows);
};
insertAfterClaim('n56', [
  'n60｜Travelpro 公司沿革稱 Rollaboard 先在機組員間流行；此處僅回扣先前已講的採用階段，不推算銷量｜https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage｜2026-10-18｜now-1993-retail｜PENDING',
  'n64｜2010 年紐約時報回顧記旅客在航站看見空服員拉著 Rollaboard 快步走；此文重印在 RNPA Contrails 第 48 頁｜https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf｜2026-10-18｜now-1993-retail｜PENDING',
]);
insertAfterClaim('n16', [
  'n61｜Winnetka 歷史學會記載 Anita 一家自製輪箱與丈夫嘲笑的反應；沒有史料把該家族案例直接接到 Sadow 或 Plath｜https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/｜2026-10-18｜now-outro｜PENDING',
  'n62｜Plath 專利記載外置推車於安檢和登機時反覆卸裝的限制；不可說他用過 Shiller 的那只箱子｜https://patents.google.com/patent/US4995487A/en｜2026-10-18｜now-outro｜PENDING',
  'n63｜Travelpro 公司稱 Plath 直立雙輪拉桿設計先在機組員間流行；與 Anita、Sadow 的直接發明傳承無獨立證據｜https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage｜2026-10-18｜now-outro｜PENDING',
]);
scene('now-1993-retail').claims.push('n60', 'n64');
scene('now-outro').claims.push('n61', 'n62', 'n63');
const claims = Buffer.from(claimRows.join('\n'));

const claimEntries = claimRows.filter((row) => /^[a-z]\d+｜/.test(row)).map((row) => row.split('｜'));
const claimScene = new Map(video.scenes.flatMap((item) => (item.claims ?? []).map((id) => [id, item.id])));
assert.equal(claimScene.size, video.scenes.reduce((sum, item) => sum + (item.claims ?? []).length, 0), 'duplicate claim ID');
assert.deepEqual(new Set(claimEntries.map((cells) => cells[0])), new Set(claimScene.keys()), 'claim rows must match scene claim IDs');
for (const cells of claimEntries) {
  assert.equal(cells.length, 6, 'malformed claim row ' + cells[0]);
  assert.equal(cells[4], claimScene.get(cells[0]), 'claim/scene mismatch ' + cells[0]);
  assert.equal(cells[5], 'PENDING', 'no approval inherited');
}

// Public description sources are exactly the distinct URLs cited by the
// current scene claims. A source that appears only in a historical note is
// deliberately excluded from the upload description.
const titleByUrl = new Map([
  ['https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469', 'ABC News：Bernard Sadow 當事人訪談（2010）'],
  ['https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/', 'Winnetka Historical Society：Anita 的輪箱收藏資料'],
  ['https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage', 'Travelpro：輪子行李箱與 Rollaboard 公司沿革'],
  ['https://www.winnetkahistory.org/gazette/hope-amidst-hardship-the-indomitable-character-of-anita-willets-burnham/', 'Winnetka Historical Society：Anita 第一次旅行'],
  ['https://www.winnetkahistory.org/who-were-the-burnhams/', 'Winnetka Historical Society：Burnham 家族資料'],
  ['https://newspapers.swco.ttu.edu/bitstreams/b9cd84b8-2ba7-4506-9eff-7cca3e5c6376/download', 'Midland 當地報紙：1939 年 Anita 茶會報導'],
  ['https://patents.google.com/patent/US3653474A/en', '美國專利 US3653474A：Bernard Sadow 輪箱'],
  ['https://oyc.yale.edu/economics/econ-252-08/lecture-3', 'Yale Open Courses：Robert Shiller 2008 年講稿'],
  ['https://oyc.yale.edu/economics/econ-252-11/lecture-3', 'Yale Open Courses：Robert Shiller 2011 年講稿'],
  ['https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf', 'RNPA Contrails 2016：Bill Emmer 回憶及紐約時報重印'],
  ['https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603', 'ABC News：Robert Plath 當事人訪談（2012）'],
  ['https://patents.google.com/patent/US4995487A/en', '美國專利 US4995487A：Robert Plath 輪箱'],
  ['https://www.globaltravelerusa.com/reinventing-the-wheel/', 'Global Traveler：Travelpro 時任執行長訪談'],
  ['https://travelpro.com/pages/our-history', 'Travelpro：公司歷史'],
  ['https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html', 'Los Angeles Times：Judi Dash 1993 年登機箱實測'],
  ['https://corporate.samsonite.com/on/demandware.static/-/Sites-InvestorRelations-Library/default/dwa68533ea/PDF/announcements/2011/20110602100852_Samsonite_Final_Prospectus_en.pdf', 'Samsonite 2011 年招股書：產品年表'],
]);
const datesByUrl = new Map();
const claimIdsByUrl = new Map();
for (const cells of claimEntries) {
  if (!cells[2]) continue;
  assert.ok(titleByUrl.has(cells[2]), 'untitled source ' + cells[2]);
  assert.ok(/^2026-\d\d-\d\d$/.test(cells[3]), 'missing checked_on ' + cells[0]);
  if (!datesByUrl.has(cells[2]) || cells[3] > datesByUrl.get(cells[2])) datesByUrl.set(cells[2], cells[3]);
  if (!claimIdsByUrl.has(cells[2])) claimIdsByUrl.set(cells[2], []);
  claimIdsByUrl.get(cells[2]).push(cells[0]);
}
assert.equal(datesByUrl.size, 16, 'expected exactly sixteen cited URLs');
assert.deepEqual(new Set(datesByUrl.keys()), new Set(titleByUrl.keys()), 'public source index must exactly match cited URLs');
video.sources = [...datesByUrl].map(([url, checked_on]) => ({ title: titleByUrl.get(url), url, checked_on }));

const allLines = video.scenes.flatMap((item) => item.lines);
const sceneByLine = new Map(video.scenes.flatMap((item) => item.lines.map((part) => [part.id, item.id])));
assert.equal(sceneByLine.size, allLines.length, 'duplicate line ID');
assert.equal(new Set(video.scenes.map((item) => item.id)).size, video.scenes.length, 'duplicate scene ID');
const sceneIndex = new Map(video.scenes.map((item, index) => [item.id, index]));
for (const loop of video.loops) {
  assert.ok(sceneByLine.has(loop.setup) && sceneByLine.has(loop.payoff), 'missing loop line ' + loop.setup);
  assert.ok(sceneIndex.get(sceneByLine.get(loop.setup)) < sceneIndex.get(sceneByLine.get(loop.payoff)), 'reversed loop ' + loop.setup);
}
const module = (relative) => import(pathToFileURL(path.join(repo, relative)));
const [{ screenplay }, { estimateTimeline, spokenUnits }, { lintVideo }, { cuteStoryVisualProblems }] = await Promise.all([
  module('tools/video/core/screenplay.mjs'),
  module('tools/video/core/timeline.mjs'),
  module('tools/video/core/lint.mjs'),
  module('tools/video/automation/story.mjs'),
]);
assert.equal(screenplay(before), readR9('candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r9 screenplay drift');
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
assert.equal(cute.length, 0, 'cute illustration errors: ' + JSON.stringify(cute));
const timing = Object.fromEntries([250, 275, 300].map((cpm) => {
  const seconds = estimateTimeline(video, cpm).total_frames / 30;
  return [cpm, Number(seconds.toFixed(1))];
}));
const timeline300 = estimateTimeline(video, 300);
const line300 = new Map(timeline300.lines.map((item) => [item.id, item]));
const longLoopTiming300 = {
  setup: 'x7r4',
  payoff: 'r3n03',
  payoff_scene_id: 'now-1993-retail',
  payoff_scene_ordinal: sceneIndex.get('now-1993-retail') + 1,
  scene_total: video.scenes.length,
  setup_end_seconds: Number((line300.get('x7r4').end_frame / 30).toFixed(1)),
  payoff_start_seconds: Number((line300.get('r3n03').start_frame / 30).toFixed(1)),
  intervening_seconds: Number(((line300.get('r3n03').start_frame - line300.get('x7r4').end_frame) / 30).toFixed(1)),
};
const sourceMap = {
  status: 'PENDING_INDEPENDENT_FULL_R10_REVIEW',
  derives_from_r9_manifest_sha256: expected.r9_manifest,
  resolves_report_sha256: expected.r8_review,
  prior_reviews_not_inherited: true,
  source_index: [...claimIdsByUrl].map(([url, ids]) => ({ url, claim_ids: ids })),
  removed_scene_ids: ['origin-06', 'idea-r12-02'],
  removed_claim_ids: ['o33', 'i29'],
  modified_line_ids: ['r14o01', 'r14i01', 'r3n03', 'r3n02', 'r3n01', 'g5b8', 'xjmb', 'ek2s'],
  modified_visual_scene_ids: ['origin-budget', 'idea-memory', 'hook-06', 'turn-09', 'now-consumer-question'],
  moved_scene_ids: ['now-1993-retail', 'now-consumer-question'],
  long_loop: { setup: 'x7r4', payoff: 'r3n03', payoff_scene_id: 'now-1993-retail', reason: '1993 retail availability after crew use and passenger visibility; explicitly called back in spoken line' },
  evidence_guard: 'The 1939 suitcase is one reported appearance, not established as the 1928 physical case or continuous use. Anita, Sadow and Plath are distinct histories without proven direct invention lineage. Emmer and Plath undated recollections are not ordered.',
  patent_guard: 'Technical two-half underside line removed rather than asking MiniMax to reconstruct a patent diagram; remaining strap/handle claims stay attributed to US3653474A.',
  host_adoption_guard: 'PENDING: current worker merges sources from its plan during re-draft. Host six-chapter source list and exact version must be inspected, compared to this 16-URL set, and reconciled without overwriting provenance before adoption.',
};
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_UNREVIEWED',
  target_body_seconds: [420, 480],
  scenes: video.scenes.length,
  lines: allLines.length,
  claims: claimEntries.length,
  loops: video.loops.length,
  narration_spoken_units: allLines.reduce((sum, item) => sum + spokenUnits(item.text), 0),
  estimated_body_seconds_not_tts: timing,
  long_loop_300_cpm_not_tts: longLoopTiming300,
  estimated_300_cpm_in_owner_range: timing[300] >= 420 && timing[300] <= 480,
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_errors_at_300_cpm: lintAt300.errors,
  cute_visual_errors: cute,
  public_sources: video.sources.length,
  claim_source_urls: datesByUrl.size,
  source_index_matches_claims: true,
  actual_tts_body_and_cut: 'NOT_RUN',
  independent_full_fact_visual_listener_review: 'NOT_RUN_FOR_R10',
  host_worker_source_merge_and_duration_gate: 'NOT_CHECKED_OR_INSTALLED',
  script_review_receipt: 'NOT_ISSUED',
  host_import_or_paid_media: 'NOT_RUN',
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', readR9('candidate/series.json')],
  ['candidate/lexicon.json', readR9('candidate/lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['validation.json', json(validation)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE',
  slug: video.slug,
  derives_from_r9_manifest_sha256: expected.r9_manifest,
  resolves_report_sha256: expected.r8_review,
  source_snapshot: r9Manifest.source_snapshot,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r9_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r10');
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), 'missing output ' + name);
    assert.ok(fs.readFileSync(file).equals(bytes), 'stale output ' + name);
  }
}
console.log(JSON.stringify({ action, status: validation.status, scenes: validation.scenes, lines: validation.lines, claims: validation.claims, loops: validation.loops, sources: validation.public_sources, spoken_units: validation.narration_spoken_units, seconds_250: timing[250], seconds_275: timing[275], seconds_300: timing[300], in_range_at_300: validation.estimated_300_cpm_in_owner_range, lint_errors: lint.errors.length, cute_errors: cute.length }));
