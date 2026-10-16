import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const preproduction = path.dirname(here);
const original = path.join(preproduction, 'B18-authored-chapters-candidate');
const audit = path.join(preproduction, 'B18-fact-audit-candidate-20261016', 'claim-audit.json');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const pins = {
  'series.json': '6e3e09680dc39b3bcb1db6dc7d4e027feaa37174f4f751a0f4f088aa45d11346',
  'chapters/hook.json': 'e98bdefb26bab591ad27c66b2748d213809544e872697f4e7261174ee7caed1f',
  'chapters/origin.json': '87a9d62a099da7ed3f5cef8d7dfd8ddac4f61c545c580387415207a31f940551',
  'chapters/idea.json': '159a25dc1a13ac1247467507064625f3599db535500c67a88c490cebaff763b1',
  'chapters/engine.json': '2917a212792e79094e7e10fe46d170375e04c0bff0e27d9f36fbac6a1b30e01a',
  'chapters/turn.json': 'eb70c7b3332d8285ecd87fff072e39cf0921362cf28259d694d55bd679e9e536',
  'chapters/now.json': 'db1736a1989efe6662373856b65ed191bbe55206c1517cf376dbc535e619511a',
  'fact-audit/claim-audit.json': 'c9c743dc91edaa9961d7fc91b64c4eadcef30446e8fc2f54d655130c167eb07a',
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
for (const [name, expected] of Object.entries(pins)) {
  const file = name.startsWith('fact-audit/') ? audit : path.join(original, name);
  assert.equal(sha(fs.readFileSync(file)), expected, `input drift: ${name}`);
}
const read = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const previousAudit = read(audit);
for (const id of ['B18-PC-H02-4', 'B18-PC-E03-1', 'B18-PC-T02-1', 'B18-PC-T02-2', 'B18-PC-T02-3']) {
  assert(previousAudit.rows.some((row) => row.planning_id === id && row.audit_verdict.startsWith('HOLD_')), `missing audit hold: ${id}`);
}
const chapters = Object.fromEntries(keys.map((key) => [key, read(path.join(original, 'chapters', `${key}.json`))]));
const series = read(path.join(original, 'series.json'));
const changes = [];
const scene = (key, id) => {
  const found = chapters[key].scenes.find((item) => item.id === id);
  assert(found, `${key}/${id} missing`);
  return found;
};
const line = (key, id, lineId, before, after) => {
  const found = scene(key, id).lines.find((item) => item.id === lineId);
  assert(found, `${key}/${id}/${lineId} missing`);
  assert.equal(found.text, before, `spoken source drift: ${key}/${lineId}`);
  found.text = after;
  changes.push({ kind: 'spoken', chapter: key, scene: id, line: lineId, before, after });
};
const data = (key, id, field, before, after) => {
  const found = scene(key, id);
  assert.equal(found.data[field], before, `visual source drift: ${key}/${id}/${field}`);
  found.data[field] = after;
  changes.push({ kind: 'visual', chapter: key, scene: id, field, before, after });
};
const claim = (key, id, before, after, source, fact = undefined, targetScene = undefined) => {
  const found = chapters[key].claims.find((item) => item.id === id);
  assert(found, `${key}/${id} claim missing`);
  assert.equal(found.claim, before, `claim source drift: ${key}/${id}`);
  const old = { text: found.claim, source: found.source, fact: found.fact, scene: found.scene };
  found.claim = after;
  found.source = source;
  if (fact !== undefined) found.fact = fact;
  if (targetScene !== undefined) found.scene = targetScene;
  changes.push({ kind: 'claim', chapter: key, id, before: old, after: { text: found.claim, source: found.source, fact: found.fact, scene: found.scene } });
};

// Hook: retain the third question, but remove the disputed 1978 date and sole-switch premise.
line('hook', 'hook-s006', 'a1485302',
  '一九七八年，一項權利走到期限，接下來又會有誰走進這門生意？',
  '一項保護餐台的權利後來到期，其他店會怎麼用這條送餐路？');
const rightsImage = 'Medium shot at a Japanese office desk in the early 1970s, one generic restaurant operator closing an unmarked document folder beside an empty sushi plate, the final blank divider sheet is the focal object, neutral soft light.';
const oldRightsImage = 'Medium shot at a Japanese office desk in 1978, one generic restaurant operator closing an unmarked document folder beside an empty sushi plate, the final blank divider sheet is the focal object, neutral soft light.';
data('hook', 'hook-s006', 'prompt', oldRightsImage, rightsImage);
claim('hook', 'h7', '一九七八年，一項權利走到期限', '一項保護餐台的權利後來到期', 3, 4);
const hookLoop = chapters.hook.loops.find((item) => item.setup === 'a1485302');
assert.equal(hookLoop.what, '權利期滿後誰加入經營');
hookLoop.what = '餐台權利期滿後其他店怎麼經營';

// The J-Net21 article supports a circulating counter; the old worker source pointer did not.
claim('origin', 'o11', '一盤盤壽司沿著吧台繞一圈', '一盤盤壽司沿著吧台繞一圈', 0, null);

// The two reported Dotonbori dates disagree; the opening itself does not.
line('engine', 'engine-s048', '8d903637',
  '一九六〇年，第二家店開到大阪道頓堀；白石自己的版圖在長大。',
  '元祿壽司後來也開進大阪道頓堀，白石自己的版圖在長大。');
data('engine', 'engine-s048', 'prompt',
  'Wide shot along a busy-looking but unoccupied Osaka commercial lane in 1960, one generic shop worker raising a plain storefront shutter, the second modest sushi counter visible inside is the focal object, neutral soft light.',
  'Wide shot along a busy-looking but unoccupied Osaka commercial lane in the early 1960s, one generic shop worker raising a plain storefront shutter, another modest unbranded sushi counter visible inside is the focal object, neutral soft light.');
claim('engine', 'e5', '一九六〇年，第二家店開到大阪道頓堀', '元祿壽司後來也開進大阪道頓堀', 0, null);
line('engine', 'engine-s050', '9af5eda1',
  '名字叫「附輸送帶的料理台」。它保護的是這套裝置的做法，不是壽司本身。',
  '登記的日文名稱，直譯是「附輸送帶的料理台」。它保護的是這套裝置的做法，不是壽司本身。');
claim('engine', 'e7', '名字叫「附輸送帶的料理台」', '登記的日文名稱，直譯是「附輸送帶的料理台」', 3, 4);
line('engine', 'engine-s061', 'f7104e65',
  '兒子博志回憶，自己暑假去幫忙，剝蝦、剪海苔都忙個不停。',
  '報導記下博志對萬博店的回憶：蝦要剝，海苔要剪，備料全靠人手。');
data('engine', 'engine-s061', 'subtitle', '博志回憶的暑假幫忙', '萬博店的備料');
claim('engine', 'e13', '兒子博志回憶，自己暑假去幫忙，剝蝦、剪海苔都忙個不停', '博志對萬博店的回憶：蝦要剝，海苔要剪', 0, null);

// The official judgment identifies registration 579776 and a 1972 expiry. The retrospective
// 1978 accounts may describe another right; the unresolved chain is explicitly kept open.
chapters.turn.title = '萬博之後，這條輸送帶分出新路';
line('turn', 'turn-s068', '2317894a',
  '元祿壽司後來靠加盟擴到約兩百四十家，但主要仍在同一品牌與權利之下。',
  '發明協會記載，元祿壽司後來靠加盟擴到約兩百四十家。它把小店的做法帶往各地。');
line('turn', 'turn-s076', '7c2ba19d',
  '可白石保護裝置的那項權利，會走到哪一步？',
  '可白石保護餐台的那項權利，又能守到什麼時候？');
line('turn', 'turn-s077', '529a2c13',
  '開場那項走到期限的權利，就是白石登記的實用新案。',
  '開場那項權利，是白石一九六二年登記的實用新案。');
data('turn', 'turn-s077', 'prompt', oldRightsImage, rightsImage);
line('turn', 'turn-s078', '5d0a1084',
  '一九七八年，它期滿了。這時候，原先由元祿壽司幾乎獨占的市場，出現了更多經營者。',
  '法院判決理由記載，這項實用新案在一九七二年期滿。');
data('turn', 'turn-s078', 'title', '1978 · 期滿', '1972 · 實用新案期滿');
data('turn', 'turn-s078', 'subtitle', '輸送帶料理台的實用新案', '第 579776 號餐台實用新案');
data('turn', 'turn-s078', 'tag', 'J-Net21／發明協會', '日本法院判決理由');
line('turn', 'turn-s079', '230c59db',
  '大批新業者進入迴轉壽司市場；原本的加盟店，也有人獨立，換上自己的招牌。',
  '此後，已有許多公司在元祿之外，開起自己的輸送帶壽司店。');
data('turn', 'turn-s079', 'prompt',
  'Wide shot outside a Japanese sushi restaurant in the late 1970s, one generic shop worker fitting a new blank signboard above the doorway, the fresh sign and existing counter inside are the focal objects, neutral soft light.',
  'Wide shot across two separate unbranded Japanese sushi storefronts in the 1970s, generic diners at the distinct conveyor counters, the separate independent shops are the focal objects, neutral soft light.');
line('turn', 'turn-s080', '09d46243',
  '權利期滿不是全國才開始吃迴轉壽司：',
  '另有報導記下，元祿的加盟店後來也有人獨立，換上自己的招牌。');
data('turn', 'turn-s080', 'prompt',
  'Medium shot inside an established Japanese sushi shop in the late 1970s, one generic diner lifting a plate from an older counter conveyor, the worn but functioning counter is the focal object, neutral soft light.',
  'Medium shot outside an unbranded Japanese sushi restaurant in a later expansion period, one generic shop worker fitting a new blank signboard above the doorway, the fresh sign and existing counter inside are the focal objects, neutral soft light.');
line('turn', 'turn-s081', 'd8ecd870',
  '萬博已讓許多人認識，元祿壽司也早在展店。',
  '萬博先讓更多人看見這種吃法，元祿也早在展店。');
claim('turn', 't7', '一九七八年，它期滿了', '這項實用新案在一九七二年期滿', 3, 4);
claim('turn', 't8', '大批新業者進入迴轉壽司市場', '已有許多公司在元祿之外，開起自己的輸送帶壽司店', 3, 5);
claim('turn', 't9', '原本的加盟店，也有人獨立，換上自己的招牌', '元祿的加盟店後來也有人獨立，換上自己的招牌', 0, 5, 'turn-s080');
claim('turn', 't10', '萬博已讓許多人認識，元祿壽司也早在展店', '萬博先讓更多人看見這種吃法，元祿也早在展店', 2, 7);
const rightsLoop = chapters.turn.loops.find((item) => item.setup === 'a1485302');
assert.equal(rightsLoop.payoff, '230c59db');
rightsLoop.what = '餐台權利期滿後其他店怎麼經營';
line('turn', 'turn-s071', 'bb08c911',
  '一九七一年，石野製作所供應元祿壽司自動給茶裝置，',
  '石野製作所也做出自動給茶裝置，');
data('turn', 'turn-s071', 'title', '1971', '自動給茶裝置');
data('turn', 'turn-s071', 'subtitle', '石野製作所 · 自動給茶裝置', '石野製作所');
claim('turn', 't5', '一九七一年，石野製作所供應元祿壽司自動給茶裝置', '石野製作所也做出自動給茶裝置', 2, null);
line('turn', 'turn-s083', 'ba2ba154',
  '新業者進來後，有些店把繞吧台的輸送帶改成直線，從後場送到用餐區。',
  '後來有些店把繞吧台的輸送帶改成直線，從後場送到用餐區。');
claim('turn', 't11', '有些店把繞吧台的輸送帶改成直線，從後場送到用餐區', '有些店把繞吧台的輸送帶改成直線，從後場送到用餐區', 2, null);
line('turn', 'turn-s086', 'ed0c5c6c',
  '新進的店在競爭裡試著把魚料從漁民或漁協直接買來；',
  '也有業者試著把魚料從漁民或漁協直接買來；');
claim('turn', 't12', '把魚料從漁民或漁協直接買來', '把魚料從漁民或漁協直接買來', 2, null);
const beforeOrder = chapters.turn.scenes.map((item) => item.id);
const prefix = ['turn-s063', 'turn-s065', 'turn-s066', 'turn-s068', 'turn-s076', 'turn-s077', 'turn-s078', 'turn-s079', 'turn-s080', 'turn-s081', 'turn-s070', 'turn-s071', 'turn-s072', 'turn-s073', 'turn-s075'];
assert.deepEqual(beforeOrder.slice(0, 15), ['turn-s063', 'turn-s065', 'turn-s066', 'turn-s068', 'turn-s070', 'turn-s071', 'turn-s072', 'turn-s073', 'turn-s075', 'turn-s076', 'turn-s077', 'turn-s078', 'turn-s079', 'turn-s080', 'turn-s081']);
chapters.turn.scenes = [...prefix.map((id) => scene('turn', id)), ...chapters.turn.scenes.slice(15)];
changes.push({ kind: 'scene_order', chapter: 'turn', before: beforeOrder, after: chapters.turn.scenes.map((item) => item.id) });

// Keep the whole-story proposition aligned with the revised narration. This is a proposal,
// not a mutation of the imported B18 plan or any production series row.
const plan = series.plan;
series.logline = '大阪壽司店為解決遞盤與人手不足，從啤酒工廠輸送帶想到迴轉餐台；經過轉角試作、1958 年開店與 1970 年萬博，後來有不同業者把做法走成各自的店。';
const points = Object.fromEntries(plan.chapters.map((item) => [item.key, item]));
points.hook.point = '1948 年吹田啤酒工廠開場：白石想到用輸送帶送壽司。預告三問：轉角如何通過；1970 年萬博會場有什麼反應；保護餐台的權利期滿後，別的店又會怎麼用這條路。不要在鉤子先揭露板片或權利日期。';
points.engine.point = '1958 年 4 月布施首店開門，約 20 坪、一盤四貫 50 日圓；後來亦在大阪道頓堀展店，但 J-Net21 的 1960 年與法院判決記載的 1962 年 4 月不合，旁白不給確定開店年或第幾店。1962 年白石登記餐台實用新案，之後萬博出店，讓更多人看見。萬博暑假幫忙的家屬回憶有來源版本差，僅轉述備料忙碌，不確定其在場時間。';
points.turn.point = '萬博之後元祿透過加盟展店；法院判決理由認定第 579776 號實用新案於 1972 年期滿，此後已有其他獨立業者經營。J-Net21 另記加盟店有人獨立，但不能把它繫成 1972 或 1978 單一權利的直接效果。給茶、直線輸送、採購與盤色價格是後續不同業者及設備商的改進；1974 年設備整合有來源。';
points.now.point = '1991 年回転寿司進入《廣辭苑》第四版；2021 年機械學會認定 1985 年製造、認定時使用中的機器與另存早期板片。2023 年 J-Net21 引述的市場與店數只能作帶年份的當時資料。收束人手瓶頸、扇形轉角、萬博曝光與後來多種經營路徑；不把 1978 寫成確定的原始實用新案到期日。';
plan.takeaway = '一間小店為解決遞盤人手不足，做出會轉彎的餐台；萬博讓更多人看見，之後加盟店與獨立業者各自把這條送餐路發展成不同店型。';
plan.must_verify[4] = {
  claim: '日本法院判決理由認定「コンベヤ附調理食台」實用新案第 579776 號於 1960-02-20 申請、1962-12-06 登錄，並於 1972 年期滿；J-Net21 與發明協會所述 1978 年尚未釐清是否指其他權利，旁白不能混為同一項。',
  sources: [0, 2, 3], core: true,
};
plan.must_verify[5] = {
  claim: 'J-Net21 記載元祿曾在東京和大阪請律師對相似店警告，也記載加盟店後來有人獨立；法院判決理由另認定基本實用新案在 1972 年期滿後已有與元祿無關的公司經營。來源不足以把所有入場與加盟獨立歸因於 1978 年單一權利期滿。',
  sources: [0, 3], core: true,
};
assert.equal(plan.sources.length, 4);
assert.equal(plan.sources[3].publisher, 'Wikipedia');
plan.sources[0].supports = plan.sources[0].supports.replace('1962年取得權利與1978年期滿', '報導寫1962年取得「特許」與1978年期滿（權利種類及期滿年與法院判決衝突，僅作版本紀錄）');
plan.sources[2].supports = plan.sources[2].supports.replace('1978年期滿後新業者大量進入', '沿革寫1978年期滿後新業者大量進入（與法院判決衝突，僅作版本紀錄）');
assert(plan.sources[0].supports.includes('僅作版本紀錄') && plan.sources[2].supports.includes('僅作版本紀錄'));
plan.sources[3] = {
  url: 'https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf',
  publisher: '日本法院官方判決（昭和59年(ワ)5473號等）',
  kind: 'official',
  supports: '判決理由 PDF P8 L466–474：實用新案579776號申請與登錄、原告道頓堀店1962年4月開設；P10 L574–578：該權利1972年期滿，之後已有與原告無關的多家公司經營。被告答辯 P5 L306–315 所述另一權利851953的期滿日並非法院獨立認定。',
  checked: '2026-10-16',
};
plan.caveats = '法院判決理由認定第579776號餐台實用新案1972年期滿；J-Net21、發明協會及家屬回憶的1978年可能混及其他權利，未取得完整權利鏈，不能寫成原案到期日或唯一入場開關。道頓堀開店年份：J-Net21與家屬訪談1960，法院對原告道頓堀店認定1962年4月；尚未證實是否不同店／法人，旁白只說後來展店。萬博暑假幫忙的J-Net21轉述與家屬另一段海外回憶時間未排清；只引其備料記憶，不定他何時在場。1971自動給茶裝置另有開發／供應版本差，旁白不定年；1974整合依發明協會。撲克牌／名片兩版本保留各自歸屬。魚鱗板為「ウロコ」中文解說名，1985機器與另存早期板片分清。J-Net21 2023年的市場與店數不可當今日實績。原正式企劃與其核准未被本離線提案修改；重入工人前須獨立查核並重新審稿。';

for (const key of keys) for (const row of chapters[key].claims) {
  const bound = scene(key, row.scene).lines.map((item) => item.text).join('');
  assert(bound.includes(row.claim), `claim no longer in scene: ${key}/${row.id}`);
  assert.equal(row.verdict, 'UNCHECKED', `unexpected review verdict: ${key}/${row.id}`);
  assert(Number.isInteger(row.source) && plan.sources[row.source], `invalid source: ${key}/${row.id}`);
}
assert.equal(keys.flatMap((key) => chapters[key].claims).length, 65);
const oldOrder = keys.flatMap((key) => read(path.join(original, 'chapters', `${key}.json`)).scenes.flatMap((item) => item.lines.map((lineItem) => lineItem.id)));
const newOrder = keys.flatMap((key) => chapters[key].scenes.flatMap((item) => item.lines.map((lineItem) => lineItem.id)));
assert.equal(oldOrder.length, newOrder.length);
assert.deepEqual([...oldOrder].sort(), [...newOrder].sort());
assert(!keys.flatMap((key) => chapters[key].scenes).some((item) => item.lines.some((lineItem) => /一九七八年|1978年|一九六〇年，第二家店/.test(lineItem.text))));
const story = ['# B18 修訂口播候選（離線、未審）', '', '章節順序與逐鏡旁白如下。主張仍全部 UNCHECKED；此檔不是正式逐章審核或配音稿。', '', ...keys.flatMap((key) => [`## ${key}｜${chapters[key].title}`, '', ...chapters[key].scenes.map((item) => `- ${item.id} [${item.template}] ${item.lines.map((lineItem) => lineItem.text).join('')}`), ''])].join('\n');

const edited = ['hook', 'origin', 'engine', 'turn'];
const output = new Map([['series.json', canonical(series)], ['delta.json', canonical({ schema_version: 1, status: 'OFFLINE_SOURCE_BOUND_REVISION_NOT_REVIEWED', base_pins: pins, changes })], ['READABLE-SCRIPT.md', `${story.trimEnd()}\n`]]);
for (const key of edited) output.set(`chapters/${key}.json`, canonical(chapters[key]));

const repo = path.resolve(here, '../../../../..');
const { composeStory, cuteStoryVisualProblems } = await import(pathToFileURL(path.join(repo, 'tools/video/automation/story.mjs')).href);
const { loadProject, lintProject } = await import(pathToFileURL(path.join(repo, 'tools/video/core/state.mjs')).href);
const { estimateTimeline } = await import(pathToFileURL(path.join(repo, 'tools/video/core/timeline.mjs')).href);
let externalCalls = 0;
globalThis.fetch = () => { externalCalls++; throw new Error('offline build must not fetch'); };
const slug = 'story-conveyor-belt-sushi-v2';
const doc = composeStory({ slug, info: series, chapters, voice: read(path.join(original, 'synthetic/docroot/docs/videos', slug, 'video.json')).voice, drama: { music_enabled: false }, root: repo });
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'b18-source-bound-'));
let lint;
try {
  const shelf = path.join(tmp, 'docs', 'videos');
  const dir = path.join(shelf, slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'video.json'), canonical(doc));
  fs.writeFileSync(path.join(dir, 'series.json'), canonical(series));
  fs.copyFileSync(path.join(original, 'synthetic/docroot/docs/videos', slug, 'brief.md'), path.join(dir, 'brief.md'));
  fs.copyFileSync(path.join(original, 'fixtures/lexicon.json'), path.join(shelf, 'lexicon.json'));
  lint = lintProject(loadProject({ slug, root: tmp }));
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
assert.deepEqual(lint.errors, [], `official lint errors: ${JSON.stringify(lint.errors)}`);
assert.deepEqual(cuteStoryVisualProblems(doc), [], 'cute visual lint errors');
assert.equal(doc.sources[3].url, plan.sources[3].url);
assert.equal(doc.subtitles.burn_in, false);
assert.deepEqual(doc.look, { preset: 'cute-mystery' });
const shots = doc.scenes.filter((item) => item.template === 'shot').length;
const cards = doc.scenes.filter((item) => item.template === 'title').length;
assert(shots / doc.scenes.length >= .7);
const result = {
  schema_version: 1, status: 'OFFLINE_SOURCE_BOUND_REVISION_NOT_REVIEWED',
  original_files_pinned: Object.keys(pins).length, edited_chapters: edited,
  scenes: doc.scenes.length, lines: newOrder.length, claims_unchecked: 65,
  illustrations: shots, cards, illustration_ratio: Number((shots / doc.scenes.length).toFixed(4)),
  lint_errors: lint.errors, cute_errors: [], lint_warnings: lint.warnings.length,
  estimated_body_seconds: estimateTimeline(doc).total_frames / 30,
  measured_body_seconds: null, external_calls: externalCalls, worker_pass: false,
  proposed_series_sha256: sha(output.get('series.json')),
  edited_chapter_sha256: Object.fromEntries(edited.map((key) => [key, sha(output.get(`chapters/${key}.json`))])),
};
assert.equal(externalCalls, 0);
output.set('lint-warnings.json', canonical(lint.warnings));
output.set('verification.json', canonical(result));
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
for (const [name, content] of output) {
  const file = path.join(here, name);
  if (mode === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, content);
  } else assert.equal(fs.readFileSync(file, 'utf8'), content, `generated output drift: ${name}`);
}
console.log(JSON.stringify(result, null, 2));
