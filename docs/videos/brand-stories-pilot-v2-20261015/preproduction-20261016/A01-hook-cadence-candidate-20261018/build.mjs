// Offline, source-bound A01 narration candidate. No host, media or review writes.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const sourceTip = 'e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7';
const baseSha = {
  'video.json': '66fa192bc314a787a0ab66ec2a93976b4110138f4184747de7d3bfda2c5a6812',
  'series.json': '68df2792fa98971eb805c8af773c8b3726801832cca03ed753a950bb56311cbc',
  'claims.md': '98da3fec10b4b393516d09c9bf3ba30bbd74b40b16fedd01703aff9abac3307b',
  'script.md': '65e7fbe9fa980b4687c835a4a117bb2ce2f36be8009ce85139ee00e4fb42b3c4',
  'verify-1.md': 'cad5e5d5bca357b4a427306edc092973809418804f9fcb75c98cc7691fa24314',
  'lexicon.json': 'e24382a54e9d8fe4570ddc176fa39081a7e3a4a728b481caae5f12cc81ad2903',
  'brief.md': 'c177663ea0b04234f5ed74f3f9646ff4e37b0803ba8a8beb861603fcbdb5e02f',
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const source = {};
for (const [name, expected] of Object.entries(baseSha)) {
  const bytes = fs.readFileSync(path.join(here, 'base', name));
  assert.equal(sha(bytes), expected, 'snapshot-104 ' + name + ' drift');
  source[name] = bytes;
}
const video = JSON.parse(source['video.json'].toString('utf8'));
const series = JSON.parse(source['series.json'].toString('utf8'));
const candidateLexicon = JSON.parse(source['lexicon.json'].toString('utf8'));
candidateLexicon.terms.Bill = '比爾';
candidateLexicon.terms.Emmer = '艾默';
assert.equal(video.slug, 'story-rolling-suitcase-v2');
assert.equal(series.slug, 'brand-stories-curio-pilot-v2');
const storytellerStyle = 'Warm, curious Taiwan Mandarin storyteller with a natural Taiwanese accent. Begin with the concrete action, vary pace with the people and their choices, and give a brief natural pause before a consequential reveal. Speak clearly and conversationally; do not sound like a technical lecture, read a list, or slow down artificially to meet a duration target.';
video.voice.style = storytellerStyle;
for (const character of video.characters ?? []) character.voice.style = storytellerStyle;
for (const character of series.characters ?? []) character.voice.style = storytellerStyle;
series.logline = '一只自製輪子箱、一位帶樣品跑百貨的主管，和在安檢口停下的機師：三條沒有證據顯示直接承襲的人物線，各自把旅途中卡住的一步往前推。';
series.plan.question = '有了輪子，行李箱為何還要經過使用、進貨與機組員的改造，才成為熟悉的旅行用品？';
series.plan.chapters = [
  { key: 'hook', point: '先看 Sadow 雙手提沉箱與旁邊輪板推重機器的反差；只預告百貨採購的決定與機師車庫的未解結果，不提前畫出樣品或 Rollaboard 成品。' },
  { key: 'origin', point: '館方引述 Anita 旅前不想再提箱；交代家計與兒子先用嬰兒車零件改箱，然後一家六口出發。丈夫嘲笑後她仍使用，旅後巡講與館藏收束；不把後來的 Sadow 說成受她影響。' },
  { key: 'idea', point: '回到 Sadow 的阿魯巴返程重箱與波多黎各輪板；他在工廠裝四腳輪與拖繩。專利需求和可提可拖只作簡短、明確歸屬的設計背景；結尾是帶樣品去找買家。' },
  { key: 'engine', point: 'Sadow 回憶百貨採購拒絕，Macy 副總裁親自試拉後叫回採購、安排進貨與展示；顧客反應屬其回憶。以另一種外置推車在安檢口遇阻，轉入獨立的機師故事。' },
  { key: 'turn', point: 'Plath 見旅客在安檢卸下外置推車；本人回憶把車鎖在箱上後與安檢員對話。另一條未標年份的同機師 Emmer 回憶談既有機組袋、改良草圖與製作者婉拒，不能排成確切先後或與安檢車混為一物。Travelpro 記述 1987 車庫 Rollaboard；後來專利只作對比，不反推原型規格。' },
  { key: 'now', point: '同事請 Plath 製作、機組使用、旅客看見。以 Samsonite 研究主管的不同產品線作緊湊平行試驗，明確倒回 1986–1990 且不稱有技術繼承；回到 Travelpro 1989 搬倉與 1991 全職經營，最後簡述四輪改變及樓梯前仍需提箱。' },
];
series.plan.takeaway = '輪子箱的故事由多個互不證實直接承襲的人物與產品線構成：搬得動、有人進貨、機組願意用，才讓更多旅客看見它。';
series.plan.must_verify = [
  { claim: 'Winnetka 館方記述 Anita 旅前問題、兒子改箱、一次出發、母女沿路作畫、丈夫反應、後續巡講與館藏；無證據顯示她影響 Sadow', sources: [8, 16], core: true, attributed: true },
  { claim: 'Sadow 本人談阿魯巴回程兩只 27 吋箱、波多黎各輪板、工廠四腳輪與繩、百貨拒絕、Macy 副總裁試拉和後續顧客反應', sources: [6], core: true, attributed: true },
  { claim: 'US3653474A 只支持申請人描述的大型航站自提需求及普通箱可提可拖設計，不證明每只售出品的構造', sources: [0], core: true, attributed: true },
  { claim: 'Plath 的安檢經歷是其受訪回憶；1989 年專利描述外置推車反覆拆綁，不能倒推 1987 年所有細節', sources: [5, 12], core: true, attributed: true },
  { claim: 'Travelpro 回顧 1987 年車庫 Rollaboard、機組採用、1989 年搬倉及 1991 年 Plath 全職經營；年份有其他晚年回憶差異', sources: [1, 2], core: true, attributed: true },
  { claim: 'Emmer 多年後回憶既有機組輪子袋、Plath 草圖遭婉拒及較低掛帶；原文未給事件年份或與安檢的先後', sources: [13], core: true, attributed: true },
  { claim: 'Travelpro 當時執行長說其他機師見 Plath 使用後請他製作；不按訪談的相對年份推算事件年', sources: [15], core: true, attributed: true },
  { claim: 'Samsonite 研究主管 1992 年一手回顧 Piggyback 另一產品線；1997 四輪資料是獨立公司年表，不推定與 Plath 有因果', sources: [14, 11], core: false, attributed: true },
];
series.plan.sources.push(
  { url: 'https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf', publisher: 'RNPA Contrails（Bill Emmer 2016 回憶，印刷頁 46–47；Joe Sharkey 2010 文章重印頁 48）', kind: 'archive', supports: '已存在的機組輪子袋、草圖與製作者答覆、後來掛帶；旅客見空服員使用的回顧屬另一作者，兩者不可混作同一證詞', checked: '2026-10-18' },
  { url: 'https://www.quirks.com/articles/research-with-travelers-helps-samsonite-develop-a-convenient-new-line-of-luggage/', publisher: 'Bob Bengen，Samsonite 研究主管（1992）', kind: 'industry_first_person', supports: '另一條 Piggyback 產品線的 1986–1990 樣品、停車場試拉、空服員研究與上架，非獨立市場成效證明', checked: '2026-10-18' },
  { url: 'https://www.globaltravelerusa.com/reinventing-the-wheel/', publisher: 'Global Traveler，Travelpro 執行長訪談（2007）', kind: 'interview', supports: '同事見 Plath 使用輪子箱後請他製作，不據此固定發明年份', checked: '2026-10-18' },
  { url: 'https://www.winnetkahistory.org/who-were-the-burnhams/', publisher: 'Winnetka Historical Society，Burnham 家族簡史', kind: 'archive', supports: '第二次環遊期間 Anita 和兩名女兒沿路以畫作換餐食或住宿；不指認特定交易發生的站點', checked: '2026-10-18' },
);
series.plan.names = [...new Set([...series.plan.names, 'Bill Emmer', 'Jet Eze', 'Piggyback'])];
series.plan.image_notes = 'MiniMax image-01 可愛插畫，人物只以匿名示意。開場與每段未解動作不得在旁白前畫出結果；安檢外置金屬推車、Emmer 所述舊機組輪子袋、後來 Rollaboard、Samsonite Piggyback 為不同物件。專利圖以提案示意，不充作當年實物照片。';
series.plan.caveats = '此為離線候選規劃，base/series.json 為正式來源快照，需另外審查六章主機 JSON 與 series plan 的遷移。所有新增史實仍待逐句獨立審稿；Emmer 未給確定年份，Samsonite 為另一公司產品線，實際 TTS 與畫面尚未驗收。';
assert.deepEqual(video.scenes.filter((scene) => scene.id === 'turn-08').map((scene) => scene.lines.map((line) => line.id)), [['6i8x']]);
assert.deepEqual(video.scenes.find((scene) => scene.id === 'turn-08').claims, ['t19']);
video.scenes = video.scenes.filter((scene) => scene.id !== 'turn-08');
const removedScenes = [
  { id: 'hook-07', lines: ['p5hs', 'y9b6'], claims: ['h7'], reason: '1928 family thread starts in the body instead of a cold-open table of contents' },
  { id: 'hook-05', lines: ['emju'], claims: ['h5'], reason: 'buyer demonstration is more effective at the later reversal; the cold open stays with the obstacle' },
  { id: 'origin-02', lines: ['4prs'], claims: ['o17'], reason: 'general travel-logistics restatement delays the family disagreement; remove it so the first body beat can be an obstacle without a false immediate-answer question' },
  { id: 'origin-01', lines: ['zc7k'], claims: ['o22'], reason: 'a second Anita departure after the first is chronologically false; keep one departure after the son builds the wheeled case' },
  { id: 'origin-10', lines: ['nzyh', 'dkkz'], claims: [], reason: 'Anita and Kelly evidence does not establish retail availability; remove the false store question before Sadow has approached buyers' },
  { id: 'origin-15', lines: ['vfi9', '3s8v'], claims: ['o14'], reason: 'patent reference-list detour interrupts Sadow action and invents an early buyer objection before the office scene' },
  { id: 'origin-07', lines: ['heut'], claims: ['o5'], reason: 'Kelly patent aside interrupts Anita to Sadow character transition; retain the independent patent only in source notes' },
  { id: 'origin-08', lines: ['8wb3'], claims: ['o6'], reason: 'Kelly drawing is archival context rather than a consequential action in this story' },
  { id: 'origin-11', lines: ['kzku'], claims: ['o24'], reason: 'Sadow returns through his own family baggage experience, not a recall after a patent aside' },
  { id: 'engine-r12-03', lines: ['r12e03'], claims: ['e22'], reason: 'patent bottom-seam step is too much mechanism before the retail decision' },
  { id: 'engine-r12-04', lines: ['r12e04'], claims: ['e23'], reason: 'second patent-parts shot repeats the ordinary-case design without a new person decision' },
  { id: 'engine-r12-01', lines: ['r12e01'], claims: ['e20'], reason: 'the long-terminal self-carry obstacle is already established in the preceding scene' },
  { id: 'engine-r12-07', lines: ['r12e07'], claims: ['e25'], reason: 'ordinary carry handle does not warrant a separate suspense scene' },
  { id: 'engine-02', lines: ['ij3c', 'bgdh'], claims: ['e1'], reason: 'porter-to-self-carry explanation repeats the terminal obstacle already stated in the neighboring patent beats' },
  { id: 'idea-04', lines: ['pupq'], claims: [], reason: 'sample-not-on-shelf is already implied by all-store rejection and repeats the same retail obstruction' },
  { id: 'idea-11', lines: ['89gj'], claims: ['i11'], reason: 'grant-status date detour after customer reaction interrupts the human retail outcome' },
  { id: 'idea-11b', lines: ['eb45'], claims: ['i18'], reason: 'exact 1972 grant date is archival context, not a new dramatic decision' },
  { id: 'idea-12', lines: ['srsf', '5382'], claims: ['i12', 'i13'], reason: 'assignee and elapsed-time recap interrupts the story after Macy customer response' },
  { id: 'idea-13', lines: ['5vh3', 'rpvf'], claims: ['i15'], reason: 'patent terminal question is a location quiz whose answer is immediately supplied; move the actual self-carry obstacle into Sadow design chapter' },
  { id: 'turn-01', lines: ['5wnh', 'hixq'], claims: ['t1'], reason: 'after the retail chapter states the concrete tipping and ankle problem, this scene would immediately restate it before Plath acts' },
  { id: 'turn-02', lines: ['edtc'], claims: ['t3'], reason: 'the crew burden is already bridged in engine-14 and turn-03 moves to a specific pilot' },
  { id: 'turn-08b', lines: ['b7mz'], claims: [], reason: 'the claimed remaining weight of Plath’s screwed-together prototype is inference; move directly from reported guard response to the later upright design' },
  { id: 'engine-13', lines: ['w9bj', 'tquw'], claims: ['e9'], reason: 'horizontal case tipping is a different problem from Plath’s security-cart observation and breaks the buyer-to-pilot transition' },
  { id: 'engine-14', lines: ['rs29'], claims: ['e19'], reason: 'explicit bridge repeats the separate-cart obstruction shown in the next chapter' },
  { id: 'turn-r12-04', lines: ['r12t04'], claims: ['t22'], reason: 'mechanical question before the crew outcome turns the chapter into a patent appendix' },
  { id: 'turn-r12-08', lines: ['r12t08'], claims: ['t26'], reason: 'friction-lock detail belongs in evidence notes, not this character-led script' },
  { id: 'turn-r12-05', lines: ['r12t05'], claims: ['t23'], reason: 'recessed-wheels feature repeats the preceding Rollaboard reveal; keep patent detail in claims notes' },
  { id: 'turn-r12-07', lines: ['r12t07'], claims: ['t25'], reason: 'standing and tilting mechanism repeats the preceding shot and stalls crew adoption' },
  { id: 'turn-r12-06', lines: ['r12t06'], claims: ['t24'], reason: 'support-foot mechanics after the integrated-case reveal slow the transition to colleagues using the case' },
  { id: 'turn-03', lines: ['9dkc'], claims: ['t20'], reason: 'new chapter begins with the named pilot rather than a generic tease' },
  { id: 'turn-10b', lines: ['ewj7'], claims: ['t18'], reason: 'Emmer’s witnessed passenger questions replace the company-history recap' },
  { id: 'turn-15', lines: ['arxr', '4e5m'], claims: [], reason: 'two-versus-four-wheel quiz is immediately answered by the next scene and repeats the design question' },
  { id: 'now-04', lines: ['kkjv'], claims: [], reason: 'stairs/weight is an obvious fact, not suspense; finish with a direct observation' },
  { id: 'now-02b', lines: ['5tik'], claims: ['n3'], reason: '2000 date adds a product chronology after the character story without a new human obstacle' },
  { id: 'now-03', lines: ['fmd7'], claims: ['n4'], reason: 'directions of four-wheel movement are a feature catalogue; replace with the separate Samsonite researcher’s test and carry-on decision' },
  { id: 'turn-r12-11', lines: ['r12t11'], claims: ['t27'], reason: '1991 patent-grant date after mechanism adds a chronology list without a human choice or new consequence' },
];
for (const item of removedScenes) {
  const matches = video.scenes.filter((scene) => scene.id === item.id);
  assert.equal(matches.length, 1, 'removed scene ' + item.id);
  assert.deepEqual(matches[0].lines.map((line) => line.id), item.lines);
  assert.deepEqual(matches[0].claims ?? [], item.claims);
}
video.scenes = video.scenes.filter((scene) => !removedScenes.some((item) => item.id === scene.id));
const terminalScene = video.scenes.find((scene) => scene.id === 'engine-01');
assert.deepEqual(terminalScene.lines.map((line) => line.id), ['3d52', 'gtab']);
terminalScene.lines = terminalScene.lines.filter((line) => line.id !== 'gtab');
const patentStrapScene = video.scenes.find((scene) => scene.id === 'engine-r12-06');
assert.deepEqual(patentStrapScene.claims, ['e24']);
patentStrapScene.claims.push('e25');
const hook02Scene = video.scenes.find((scene) => scene.id === 'hook-02');
const sadowFactoryScene = video.scenes.find((scene) => scene.id === 'origin-12');
assert.deepEqual(hook02Scene.claims, ['h2']);
assert.deepEqual(sadowFactoryScene.claims, ['o10']);
hook02Scene.claims = [];
sadowFactoryScene.claims.push('h2');
const hook03 = video.scenes.find((scene) => scene.id === 'hook-03');
assert.deepEqual(hook03.lines.map((line) => line.id), ['wibh', '6h2q']);
hook03.lines = hook03.lines.filter((line) => line.id !== '6h2q');
const idea01 = video.scenes.find((scene) => scene.id === 'idea-01');
assert.equal(idea01.chapter, '樣品被退回後拿到訂單');
idea01.chapter = '輪子箱在百貨店碰壁';
assert.deepEqual(idea01.lines.map((line) => line.id), ['j9sw', 'ugak']);
assert.deepEqual(idea01.claims, ['i1', 'i19']);
idea01.lines = idea01.lines.filter((line) => line.id !== 'ugak');
idea01.claims = ['i1'];
const idea10 = video.scenes.find((scene) => scene.id === 'idea-10');
assert.deepEqual(idea10.lines.map((line) => line.id), ['eghq', 'ys5y', 'quhs']);
idea10.lines = idea10.lines.filter((line) => !['eghq', 'quhs'].includes(line.id));
const idea06 = video.scenes.find((scene) => scene.id === 'idea-06');
assert.deepEqual(idea06.lines.map((line) => line.id), ['8n2r', '4qtf']);
assert.deepEqual(idea06.claims, ['i14', 'i6']);
idea06.lines = idea06.lines.filter((line) => line.id !== '4qtf');
idea06.claims = ['i14'];
const origin14 = video.scenes.find((scene) => scene.id === 'origin-14');
assert.deepEqual(origin14.claims, ['o12', 'o13', 'o21']);
origin14.claims = ['o12', 'o13'];
const now01 = video.scenes.find((scene) => scene.id === 'now-01');
assert.deepEqual(now01.lines.map((line) => line.id), ['7asx', 'kfiw']);
now01.lines = now01.lines.filter((line) => line.id !== 'kfiw');
now01.claims = ['n1'];
const turn12 = video.scenes.find((scene) => scene.id === 'turn-12');
assert.deepEqual(turn12.lines.map((line) => line.id), ['3tsp', '6jx3']);
assert.deepEqual(turn12.claims, ['t12', 't13']);
turn12.lines = turn12.lines.filter((line) => line.id !== '3tsp');
turn12.claims = ['t13'];

// The contemporary cabin-crew observation adds a consequence of easier rolling
// near the close. Keep it attributed, separate from the earlier historical
// inventions, and do not turn the obvious need to lift a bag into a quiz.
const now06Index = video.scenes.findIndex((scene) => scene.id === 'now-06');
assert.ok(now06Index >= 0 && video.scenes[now06Index - 1]?.id === 'now-01');
const addedScene = {
  id: 'now-05', template: 'shot',
  data: {
    prompt: 'Medium shot of an anonymous adult traveler packing an unbranded wheeled suitcase very full in a plain room around 2010. The traveler presses down the closed lid with both hands; the small wheels are visible but not moving. Do not depict a named flight attendant, an interview, stairs or an airport security event. Soft daylight, no signs, text or logos.',
    camera: 'push in', visual: 'still',
  },
  claims: ['n17'],
  lines: [{ id: 'opk01', text: '一位受訪空服員觀察：箱子好推，旅客反而塞得更滿；一旦不能滾，可能就搬不動。' }],
};
video.scenes.splice(now06Index, 0, addedScene);

// Expected old text is part of the patch identity. Stop rather than transplanting
// these edits onto a later or otherwise different host revision.
const revisions = [
  {
    scene: 'hook-01', line: '3rdw', claims: ['h1'],
    before: '據 Sadow 回憶，那天在波多黎各機場，他手上提著兩個沉重的箱子。',
    after: '波多黎各機場，Sadow 兩手提著沉箱；一台重機器，卻從旁邊滑過。',
    claim_text: { h1: 'Sadow 回憶在波多黎各機場一手一只提著兩個沉重行李箱時，看見旁邊有人輕鬆推行重機器' },
    sources: [{ index: 6, location: 'ABC News 2010, Sadow recalls lugging two heavy suitcases through Puerto Rico airport', role: 'first-person reported action; attribution follows in next line' }],
    payoff: 'avqs', reason: '第一句先讓沉箱的具體動作入耳，下一句立即交代這是 Sadow 的回憶。',
  },
  {
    scene: 'hook-02', line: 'e37u', claims: [],
    before: '他是一家行李箱公司的主管。就在這時候，一個工人從他身邊走過。',
    after: '他後來回憶，那人只是推著它，走得比他輕鬆。',
    claim_text: {},
    sources: [{ index: 5, location: 'ABC/USA TODAY 2012, Sadow identified as a luggage executive', role: 'reported occupation, no invented job title' }, { index: 6, location: 'ABC News 2010, Sadow later runs the luggage factory', role: 'interview context' }],
    payoff: 'avqs', reason: '推輪板的人先入鏡、輪板再揭示；在此句補回 Sadow 回憶的歸屬，來源未指明此人職務。',
  },
  {
    scene: 'hook-02b', line: 'avqs', claims: ['h3'],
    before: '工人推著一塊裝了輪子的板子，上面載的竟然是重機器。',
    after: '那人推著一塊裝輪子的板子，上面載的竟是重機器。',
    claim_text: { h3: '據 Sadow 回憶，一名男子從身旁推過裝輪子的板子，載著重機器' },
    sources: [{ index: 6, location: 'ABC News 2010, a man passed with heavy machinery on wheeled skids', role: 'the source does not identify the person as an airport worker' }],
    payoff: 'wibh', reason: '來源只稱 a man，不替他添加機場工人職務。',
  },
  {
    scene: 'hook-06', line: 'jtmg', claims: ['h6'],
    before: '1987 年，一位機師又把箱子帶進車庫。',
    after: '依 Travelpro 的回顧，1987 年有位機師把箱子帶進車庫。',
    claim_text: { h6: 'Travelpro 公司沿革稱，1987 年一位機師把箱子帶進車庫製作新輪子箱' },
    sources: [{ index: 1, location: 'Travelpro company history dates Plath garage Rollaboard to 1987', role: 'company-attributed chronology, not independently resolved date' }],
    payoff: 'jm3w', reason: '片頭年份即歸屬公司記述，避免把有其他年分回憶的時間點說成無爭議。',
  },
  {
    scene: 'turn-09', line: 'jm3w', claims: ['t7'],
    before: '1987 年，Plath 就在開場那間車庫裡，做出了 Rollaboard。',
    after: '另一份 Travelpro 公司回顧說，1987 年 Plath 在車庫做出了 Rollaboard。',
    claim_text: { t7: 'Travelpro 公司沿革稱，Plath 於 1987 年在車庫製作 Rollaboard；外形在下一鏡示意' },
    sources: [{ index: 1, location: 'Travelpro history, 1987 garage Rollaboard chronology', role: 'company-attributed year; not independently resolved against later Plath recollection' }],
    payoff: '3zwf', reason: '公司回顧日期在口播就地歸屬；這一鏡只講製作，下一鏡才露設計。',
  },
  {
    scene: 'origin-r12-01', line: 'r12o01', claims: ['o25'],
    before: '溫尼特卡歷史學會引述她的遊記：1928 年出發前，安妮塔問，人為什麼得像馱馬一樣搬行李？',
    after: '溫尼特卡館方引述安妮塔：1928 年出發前，她不想再像馱馬般提箱。',
    claim_text: { o25: '溫尼特卡歷史學會引述安妮塔遊記：1928 年出發前，她已不想再像馱馬般提行李' },
    sources: [{ index: 8, location: 'Before Her Time, Anita asks why travelers must carry luggage like pack horses; her son adapts old baby-carriage wheels to a suitcase', role: 'attributed travelogue question and later family action' }],
    payoff: null, reason: '章首先交代館方歸屬，後續家人的動作不必每句重複「館方說」；沒有宣稱她是第一人。',
  },
  {
    scene: 'origin-01b', line: '6b28', claims: ['o1'],
    before: '館方說，那是畫家 Anita Willets-Burnham 帶著一家六口，展開的第二次環遊世界。',
    after: '兒子改好箱子後，畫家 Anita Willets-Burnham 才帶著一家六口，展開第二次環遊世界。',
    claim_text: { o1: '溫尼特卡歷史學會記載，畫家 Anita Willets-Burnham 在兒子改裝輪子箱後，與一家六口展開第二次環遊世界' },
    sources: [{ index: 8, location: 'Before Her Time, family of six and 1928 second world tour', role: 'museum account under the already introduced attribution' }],
    payoff: 'r13o02', reason: '安妮塔只出發一次，且在兒子改箱之後；下一鏡才展示旅程中的輪子箱。',
  },
  {
    scene: 'origin-03', line: 'csdd', claims: ['o2'],
    before: '館方說，兒子把舊嬰兒車的兩輪裝在箱子一端。',
    after: '兒子把舊嬰兒車的兩輪裝在箱子一端。',
    claim_text: { o2: '溫尼特卡歷史學會記載，安妮塔的兒子用舊嬰兒車兩輪和伸縮木把手改裝行李箱' },
    sources: [{ index: 8, location: 'Before Her Time, son Bud fits two old baby-carriage wheels at one end and telescoping wooden handle at the other', role: 'museum account of construction' }],
    payoff: '9ij6', reason: '來源沿用章首歸屬，讓兒子改裝的動作直接入耳。',
  },
  {
    scene: 'origin-01', line: 'zc7k', claims: ['o22'],
    before: '據館方記載，安妮塔就拉著兒子做的這只箱子出發；它還只是一家人的自製品。',
    after: '安妮塔拉著兒子做的箱子出發；這時它還只是一家人的自製品。',
    claim_text: { o22: '溫尼特卡歷史學會記載，安妮塔拉著兒子做的輪子箱出發，當時仍是一家人的自製品' },
    sources: [{ index: 8, location: 'Before Her Time, family-made rolling suitcases used on 1928 trip', role: 'museum account, no claim of commercial availability' }],
    payoff: 'r12o02', reason: '承接輪子與木把手的動作，不再連續插入來源提示。',
  },
  {
    scene: 'origin-06', line: '83ew', claims: ['o20'],
    before: '還記得開場那只自製的輪子箱嗎？溫尼特卡歷史學會的館藏裡，就保存著安妮塔的一只。',
    after: '溫尼特卡歷史學會的館藏裡，至今保存著安妮塔的一只輪子箱。',
    claim_text: { o20: '溫尼特卡歷史學會館藏保存安妮塔的一只輪子行李箱' },
    sources: [{ index: 8, location: 'Before Her Time, museum collection retains one of Anita’s wheeled cases', role: 'museum-held object, no cold-open callback' }],
    payoff: null, reason: '開場不再提前講 1928 年輪子箱，故移除錯誤的「還記得開場」回指。',
  },
  {
    scene: 'origin-r12-02', line: 'r12o02', claims: ['o26'],
    before: '館方還轉述，她的丈夫寧可提重箱，還拿妻兒的輪子箱開玩笑。',
    after: '丈夫寧可自己提重箱，還笑妻兒的輪子箱。',
    claim_text: { o26: '館方轉述，安妮塔的丈夫寧可提重箱，還拿妻兒的輪子箱開玩笑' },
    sources: [{ index: 8, location: 'Before Her Time, paragraph on her husband continuing to carry his own heavy bag and teasing Anita and the children about their rolling case', role: 'reported family reaction' }],
    payoff: 'r12o03', reason: '章首館方歸屬仍有效；丈夫的反對本身是事件，旅後仍使用是結果。',
  },
  {
    scene: 'origin-r12-03', line: 'r12o03', claims: ['o27'],
    before: '館方記載，旅程結束後，安妮塔巡迴講旅行故事時，仍帶著輪子行李箱。',
    after: '旅程結束後，安妮塔巡迴講旅行故事時，仍帶著輪子行李箱。',
    claim_text: { o27: '溫尼特卡歷史學會記載，旅程結束後安妮塔巡迴講旅行故事，仍帶著輪子行李箱' },
    sources: [{ index: 8, location: 'Before Her Time, Anita later toured lectures with rolling luggage in tow', role: 'museum account of continued use' }],
    payoff: null, reason: '用她持續使用的結果收束家庭衝突，避免再次說「館方記載」。',
  },
  {
    scene: 'idea-02', line: '9ijb', claims: ['i2'],
    before: '他回憶，採購覺得拖著行李走很荒唐，甚至認為他瘋了。',
    after: '採購覺得拖著行李走很荒唐，甚至認為他瘋了。',
    claim_text: { i2: '據 Sadow 回憶，採購認為拖著行李行走很荒唐，甚至覺得他瘋了' },
    sources: [{ index: 6, location: 'ABC News 2010, Sadow recounts department-store buyers calling his pulled luggage crazy', role: 'his account, introduced at engine-01' }],
    payoff: '8n2r', reason: '上一鏡已說「據 Sadow 回憶」，這句直接交代採購阻力。',
  },
  {
    scene: 'idea-03b', line: 'dibw', claims: ['i16'],
    before: '他說當時有大男人的風氣，男人替太太提行李，是理所當然的事。',
    after: '當時的大男人風氣，把替太太提行李看作理所當然。',
    claim_text: { i16: 'Sadow 指出當時有大男人風氣，男人替太太提行李被看作理所當然' },
    sources: [{ index: 6, location: 'ABC News 2010, Sadow describes the macho feeling around men carrying bags for their wives', role: 'attributed social context, not independent market survey' }],
    payoff: 's7me', reason: '採購反應已由 Sadow 回憶引入，讓社會阻力用一句具體情境承接。',
  },
  {
    scene: 'idea-05', line: 's7me', claims: ['i5'],
    before: '幾週後，樣品到了 Macy\'s 另一個人的手裡，這次會不同嗎？',
    after: '幾週後，Macy\'s 副總裁看到了那只曾被採購拒絕的箱子。',
    claim_text: { i5: '據 Sadow 回憶，原採購拒絕數週後，Macy\'s 副總裁看到了輪子箱樣品' },
    sources: [{ index: 6, location: 'ABC News 2010, Macy’s vice president Jerry Levy sees bag after earlier Macy’s buyer rejection', role: 'attributed chronology; names retained in evidence, not spoken' }],
    payoff: '8n2r', reason: '以新的決策者拿到被退樣品這件事銜接親自試拉，不再重問商店會否進貨。',
  },
  {
    scene: 'idea-06', line: '8n2r', claims: ['i14'],
    before: '還記得開頭那個要親手試的人嗎？據 Sadow 回憶，這個人拉著箱子走了走。',
    after: '據 Sadow 回憶，這位副總裁拿起拖帶，在辦公室拉著樣品走了一圈。',
    claim_text: { i14: '據 Sadow 回憶，Macy\'s 副總裁在辦公室親手拉著輪子箱樣品試走' },
    sources: [{ index: 6, location: 'ABC News 2010, Macy’s vice president walked around his office with the sample', role: 'attributed office demonstration; no removed cold-open callback' }],
    payoff: 'mryd', reason: '先在上一鏡確認副總裁身分，再讓親自試拉引出他叫回採購的行動；不重複身分句。',
  },
  {
    scene: 'idea-07', line: 'mryd', claims: ['i7'],
    before: '他把幾週前拒絕過箱子的採購叫進來，推翻了原本的決定。',
    after: '副總裁把幾週前拒絕箱子的採購叫回來。',
    claim_text: { i7: '據 Sadow 回憶，Macy’s 副總裁叫回幾週前拒絕樣品的採購' },
    sources: [{ index: 6, location: 'ABC News 2010, Macy’s vice president tests the suitcase, summons the buyer who had refused it, then orders it', role: 'chronology; order withheld until next line' }],
    payoff: '76ur', reason: '下一鏡交代進貨指示；這裡以行動自然承接，不再多塞一句明知答案的提問。',
  },
  {
    scene: 'idea-08', line: 'apb3', claims: ['i8'],
    before: '這個陌生的用法，路過的人一眼就看得到。',
    after: '這種走法，路過的人一眼可見；顧客會買帳嗎？',
    claim_text: { i8: '1970 年 10 月，店內的人偶展示了拉著輪子箱行走的方式' },
    sources: [{ index: 6, location: 'ABC News 2010, October 1970 Macy’s mannequin display and Sadow’s later customer-adoption account', role: 'store demonstration followed by attributed response' }],
    payoff: 'ys5y', reason: '展示樣品之後問顧客反應，隔過廣告鏡才由 Sadow 多年後的回憶回答。',
  },
  {
    scene: 'engine-r12-02', line: 'r12e02', claims: ['e21'],
    before: '他要的箱子，形狀、大小和樣式都跟普通的一樣，卻能讓旅客拖著走。',
    after: '普通箱仍要開合；Sadow 的專利把箱蓋與箱身，當成同一底面的兩半。',
    claim_text: { e21: 'Sadow 專利以帶鉸鏈的普通箱蓋與箱身為例，關閉時兩半構成底面，分別有腳輪配置' },
    sources: [{ index: 0, location: 'US3653474A, summary and description: hinged cover and body form two parts of bottom wall and rollers preferably attach to both', role: 'patent design question, not an observed production failure' }],
    payoff: 'r12e04', reason: '用普通箱的開合需求帶出分裝腳輪的設計選擇；本句不是懸念鉤子。',
  },
  {
    scene: 'turn-07', line: 'q4zn', claims: ['t6'],
    before: '他回到車庫，用螺絲把推車鎖在一個硬殼箱上，再帶進機場。',
    after: '他在車庫用螺絲鎖住推車和硬殼箱，再把這個組合帶回機場。',
    claim_text: { t6: '據 Plath 敘述，他在車庫用螺絲把推車固定到硬殼箱上' },
    sources: [{ index: 5, location: 'ABC/USA TODAY 2012, Plath sees travelers unstrap bags at security, screws a luggage trolley to a hard-sided suitcase in his garage, then returns to the airport', role: 'attributed sequence; garage image previews security' }],
    payoff: 'bxv2', reason: '先講他實際試的固定方式，再讓下一鏡的安檢對話自然發生；不猜答案，也不暗示是否通過安檢。',
  },
  {
    scene: 'turn-07b', line: 'bxv2', claims: ['t17'],
    before: '照他自己的說法，安檢員要他把箱子卸下來，他說拆不了，箱子是鎖在推車上的。',
    after: '照他自己的說法，安檢員要他卸下箱子；他說拆不了，箱子鎖在推車上。',
    claim_text: { t17: '照 Plath 自己的說法，安檢員要他卸下箱子，他回答無法拆下，因為箱子鎖在推車上' },
    sources: [{ index: 5, location: 'ABC/USA TODAY 2012, Plath’s returned-airport security-guard exchange immediately after the garage modification', role: 'attributed personal account, not independent security record' }],
    payoff: 'r13t02', reason: '先聽到 Plath 說無法卸箱，下一鏡補上他回憶中的安檢員回話；不推論正式放行。',
  },
  {
    scene: 'turn-10', line: 'hiwy', claims: ['t9', 't10'],
    before: 'Travelpro 說，這款箱子原本是為機組員設計的，也最先在他們之間流行。',
    after: 'Travelpro 說，這款箱子原本為機組員設計，也先在他們之間流行。',
    claim_text: {
      t9: 'Travelpro 自述，Rollaboard 先在機組員間流行',
      t10: 'Travelpro 自述，Rollaboard 原先為機組員設計',
    },
    sources: [
      { index: 2, location: 'Travelpro Our History, 1987 entry: designed for flight crews, popularity first among crew and later passengers', role: 'company account, not independent market data' },
      { index: 1, location: 'Travelpro The History of Rolling Luggage, 1987 Rollaboard and early crew use', role: 'company chronology' },
    ],
    payoff: 'r15n01', reason: '先講機組員採用，同事請他也做，再由另位記者的回顧說明旅客在航站看見。',
  },
  {
    scene: 'turn-10b', line: 'ewj7', claims: ['t18', 't12'],
    before: '握著拉桿就能帶箱子走，旅客不必另外帶推車了。',
    after: '不用另帶推車就能拉箱子；一般乘客也很快注意到了。',
    claim_text: {
      t18: 'Rollaboard 的一體式拉桿使旅客不用另帶推車也能拉箱子',
      t12: 'Travelpro 自述，一般乘客很快注意到 Rollaboard',
    },
    sources: [{ index: 2, location: 'Travelpro Our History, first crew adoption followed by passenger attention', role: 'company adoption claim' }, { index: 1, location: 'Travelpro The History of Rolling Luggage, integrated upright rolling form', role: 'company product account' }],
    payoff: null, reason: '上鏡已交代 Travelpro 歸屬，直接說從機組員到乘客的結果。',
  },
  {
    scene: 'turn-11', line: 'fd4h', claims: ['t11'],
    before: '照公司的說法，需求越來越多，車庫已經不夠用了。',
    after: '回到 Plath：依 Travelpro 回顧，需求越來越多，車庫已經不夠用了。',
    claim_text: { t11: 'Travelpro 自述需求增加，車庫已不夠用；1989 年 Plath 把生產搬進倉庫' },
    sources: [{ index: 1, location: 'Travelpro history, rising demand, 1989 garage to warehouse', role: 'company account, introduced by name in turn-10' }],
    payoff: 'jspd', reason: '沿用前兩鏡 Travelpro 歸屬，讓車庫不夠用直接成為搬倉庫的動因。',
  },
  {
    scene: 'origin-07', line: 'heut', claims: ['o5'],
    before: '到了 1943 年，另一位發明人申請了行李箱腳輪的專利，1946 年獲准。',
    after: '1943 年，發明人凱利也申請一份手提箱腳輪附件專利，三年後獲准。',
    claim_text: { o5: 'Daniel Allcott Kelly 於 1943 年申請手提箱腳輪附件專利，1946 年獲准' },
    sources: [{ index: 9, location: 'US2392926A, inventor Daniel Allcott Kelly, filing 1943-07-26, grant 1946-01-15, title Hand luggage attachment', role: 'patent chronology; no causal link to Anita or Sadow' }],
    payoff: '8wb3', reason: '把獨立的凱利專利當作下一件有證據的事，不暗示他承襲安妮塔的自製箱。',
  },
  {
    scene: 'origin-11', line: 'kzku', claims: ['o24'],
    before: '後來，開場在機場裡的那位 Sadow，也動手把點子做成樣品。',
    after: '再回到開場的 Sadow：他想把機場看到的輪板，變成能拉的行李箱。',
    claim_text: { o24: '據 Sadow 回憶，他受機場一名男子推動輪板的啟發，著手做輪子行李箱樣品' },
    sources: [{ index: 6, location: 'ABC News 2010, Sadow describes the airport wheeled-platform observation and prototype work', role: 'attributed inspiration and action; no lineage from Anita or Kelly asserted' }],
    payoff: '3zkh', reason: '1928 家庭物件和 1943 獨立專利後明示回到另一條 1970 年人物線，不暗示 Sadow 借用兩者的設計。',
  },
  {
    scene: 'origin-13', line: '3zkh', claims: ['o11'],
    before: '他把四個腳輪裝在箱底。開場那塊輪板，靠的也是讓輪子承重。',
    after: '最早的樣品，他把四個鋼製舊箱腳輪裝到箱底。',
    claim_text: { o11: '據 Sadow 回憶，他的首件樣品把四個鋼製舊箱腳輪裝到箱底' },
    sources: [{ index: 6, location: 'ABC News 2010, first prototype had four steel trunk coasters fitted under a suitcase and a rope', role: 'interview account of prototype action' }],
    payoff: 'idiy', reason: '把工廠裡的改裝說成可見的動作；樣品構件來自受訪回憶，不拿專利圖當上市產品照片。',
  },
  {
    scene: 'origin-14', line: 'dgbq', claims: ['o13'],
    before: '1970 年 2 月，人類登月約七個月後，他提出了專利申請。',
    after: '1970 年 2 月，他提出了輪子行李箱的專利申請。',
    claim_text: { o13: 'Sadow 的輪子行李箱專利於 1970 年 2 月申請' },
    sources: [{ index: 0, location: 'US3653474A filing date 1970-02-16', role: 'patent chronology; Apollo comparison removed' }],
    payoff: null, reason: '日期只作事件定位，剪掉與箱子抉擇無關的登月對照。',
  },
  {
    scene: 'engine-01', line: '3d52', claims: ['e17'],
    before: '那段長路，就在大型航站裡。',
    after: '他後來在專利裡寫明：航站越蓋越大，旅客得自己提箱走長路。',
    claim_text: { e17: 'Sadow 的專利申請書指出，旅行增長與大型航站使乘客自行搬運行李更困難' },
    sources: [{ index: 0, location: 'US3653474A, BACKGROUND: travel growth, large terminals, passengers handling own luggage over long distances', role: 'inventor written account of use problem' }],
    payoff: 'r12e01', reason: '專利提出航站自提長路，下一鏡接其他交通站點後回到工廠試裝。',
  },
  {
    scene: 'engine-01', line: 'gtab', claims: ['e17'],
    before: 'Sadow 寫道，旅行大幅增加，搬行李的方式也跟著變了。',
    after: '旅行多了，航站變大，搬行李的方式也跟著變了。',
    claim_text: { e17: 'Sadow 的申請書指出，旅行增長與大型航站使乘客自行搬運行李更困難' },
    sources: [{ index: 0, location: 'US3653474A background, travel increase and growth of passenger terminals', role: 'same scene as 3d52; one shared claim row' }],
    payoff: 'ij3c', reason: '上一句已把訊息歸給申請書，下一句直接說難題。',
  },
  {
    scene: 'engine-r12-01', line: 'r12e01', claims: ['e20'],
    before: 'Sadow 的申請書還點名火車站和巴士站：沒人幫忙時，旅客得自己搬箱子走完長路。',
    after: '火車站和巴士站也一樣：沒人幫忙，旅客得自己搬箱子走長路。',
    claim_text: { e20: 'Sadow 專利申請書點名大型火車站和巴士站，旅客沒人幫忙時得自行搬行李走長路' },
    sources: [{ index: 0, location: 'US3653474A background, railroad and bus terminals plus self-carry long distances', role: 'same patent attribution carried from earlier scene' }],
    payoff: '3zkh', reason: '此段已交代專利來源，改用旅客真正要走的路承接樣品動作。',
  },
  {
    scene: 'engine-13', line: 'tquw', claims: ['e9'],
    before: '可是這種拖法，還有地方可以再改。',
    after: 'Travelpro 後來說，它會翻倒，還可能撞腳踝。',
    claim_text: { e9: 'Sadow 型箱子橫放拖行；Travelpro 回顧，這類橫拖箱會翻倒且可能碰撞拉箱人的腳踝' },
    sources: [{ index: 5, location: 'ABC/USA TODAY 2012, contrast between horizontal Sadow case and later upright bag', role: 'horizontal form' }, { index: 1, location: 'Travelpro history, flat cases tipping and hitting ankles', role: 'company-retrospective failure mode, not a universal measurement' }],
    payoff: '9dkc', reason: '直接指出橫拖箱的可見故障，下一章以機師決定動手與安檢難題接續，不用空泛預告。',
  },
  {
    scene: 'engine-14', line: 'rs29', claims: ['e19'],
    before: '箱子已經不必一路提著了，天天跑機場的人，為什麼還想換一種拉法？',
    after: '那是橫拖箱的問題。另一種外置推車，卻在安檢口卡住。',
    claim_text: { e19: 'Travelpro 回顧橫拖箱容易翻倒；ABC／USA TODAY 記述 Plath 看見旅客把箱子綁在外置推車上，到安檢又得拆卸，這是另一種問題' },
    sources: [{ index: 1, location: 'Travelpro history, horizontal cases tipped and hit ankles', role: 'company retrospective of horizontal cases' }, { index: 5, location: 'ABC/USA TODAY 2012, Plath saw luggage tied to separate bulky trolley at security', role: 'separate external-cart obstacle, not a consequence of horizontal cases' }],
    payoff: 'iu9y', reason: '橫拖箱翻倒與外置推車安檢拆箱是兩件事；章尾指出下一障礙但不提前介紹 Plath。',
  },
  {
    scene: 'origin-08', line: '8wb3', claims: ['o6'],
    before: '專利圖裡，箱底裝著腳輪，人拉著把手或帶子，行李就跟在身邊走。',
    after: '凱利的專利圖畫出箱底腳輪，以及能拖著走的把手與帶子。',
    claim_text: { o6: '凱利的手提箱腳輪附件專利圖文提出箱底腳輪與把手或帶子拖行的設計；此證據不證明當時已販售或採用' },
    sources: [{ index: 9, location: 'US2392926A drawings and description of hand-luggage attachment', role: 'patent proposal, not adoption evidence' }],
    payoff: 'kzku', reason: '1943 年專利只作另一條設計證據，接 Sadow 時不暗示它已普及。',
  },
  {
    scene: 'turn-r12-01', line: 'r12t01', claims: ['t21'],
    before: '同在 1989 年，Plath 申請了一份專利，不過專利裡寫的設計，不一定就是車庫原型的樣子。',
    after: 'Plath 後來的專利說：外置推車在安檢卸箱、登機再拆，下機又得綁回去。',
    claim_text: { t21: 'Plath 於 1989 年申請專利；文件將外置推車在安檢、登機和下機反覆拆裝列為先前設計限制' },
    sources: [{ index: 12, location: 'US4995487A filing 1989 and described preferred embodiment, distinct evidence type from garage recollection', role: 'patent design, no unsupported identity with garage prototype' }],
    payoff: 'jm3w', reason: '把 1989 專利描述的反覆拆裝濃縮為一個人的重複動作，不倒推為 1987 車庫實物規格。',
  },
  {
    scene: 'turn-r12-04', line: 'r12t04', claims: ['t22'],
    before: '專利要解決的是箱子本身：停下來怎麼站穩，走起來又怎麼讓輪子承重？',
    after: '這份設計還有機械難題：停下怎麼站穩，走起來怎麼讓輪子承重？',
    claim_text: { t22: 'Plath 專利設計要讓箱子停下時站穩，移動時由輪子承重' },
    sources: [{ index: 12, location: 'US4995487A summary and description of recessed rollers, support feet and tilted travel', role: 'patent design problem, not sold-unit test' }],
    payoff: 'r12t07', reason: '已交代文件與方案，改以站立／承重的具體機械衝突接下三鏡示意。',
  },
  {
    scene: 'turn-r12-05', line: 'r12t05', claims: ['t23'],
    before: '專利把兩個輪子凹進箱身底端。',
    after: '兩個輪子凹進箱身底端。',
    claim_text: { t23: 'Plath 專利提出雙輪凹入箱身底端的設計' },
    sources: [{ index: 12, location: 'US4995487A summary, two recessed roller wheels at the lower part of the suitcase', role: 'same patent context as previous scene' }],
    payoff: 'r12t07', reason: '省去連續「專利」口頭標籤，細節仍由主張表逐句指向文件。',
  },
  {
    scene: 'turn-r12-08', line: 'r12t08', claims: ['t26'],
    before: '專利裡的伸縮拉桿能抽出、收回，靠摩擦固定。',
    after: '伸縮拉桿能抽出、收回，靠摩擦固定。',
    claim_text: { t26: 'Plath 專利的伸縮拉桿可抽出或收回，透過摩擦保持位置' },
    sources: [{ index: 12, location: 'US4995487A handle guide and friction locking in description and claim 1', role: 'patent mechanism' }],
    payoff: null, reason: '沿用本章專利設計語境，集中講動作，避免重複名詞。',
  },
  {
    scene: 'now-01', line: '7asx', claims: ['n1'],
    before: '還有位置。1997 年，Samsonite 發表了平衡四輪直立箱，箱子能站著推。',
    after: '到了 1997 年，Samsonite 發表平衡四輪直立箱，讓箱子站著也能往前推。',
    claim_text: { n1: 'Samsonite 於 1997 年發表平衡四輪直立箱，可站立推行' },
    sources: [{ index: 11, location: 'Samsonite prospectus, 1997 introduction of upright four-wheeled case', role: 'company filing chronology and product capability' }],
    payoff: null, reason: '不承接已刪的兩輪或四輪猜題，直接接在 1991 年後的產品演進。',
  },
  {
    scene: 'now-06', line: 'tszs', claims: ['n14'],
    before: '輪子能幫你推著走，箱子的重量卻一點也沒少。',
    after: '到了樓梯前，旅客仍得提起箱子；輪子省得了拖行，省不了重量。',
    claim_text: { n14: '樓梯前仍須提起行李箱；輪子不消除箱子和內容物的重量' },
    sources: [],
    payoff: null, reason: '用具體行動收束日常限制；不把顯而易見的樓梯重量當懸念。',
  },
];
revisions.push({
  scene: 'engine-r12-03', line: 'r12e03', claims: ['e22'],
  before: '這份獲准的專利裡，輪組還分成兩部分。',
  after: '箱子還得照常打開。專利圖先沿著底面接縫，把箱蓋和箱身分開看。',
  claim_text: { e22: 'Sadow 專利以帶鉸鏈的箱蓋與箱身為例，關閉時兩半構成底面' },
  sources: [{ index: 0, location: 'US3653474A summary and description, hinged cover and body each form part of the closed bottom wall', role: 'patent design, not retail proof' }],
  payoff: 'r12e04', reason: '先讓觀眾看清底面接縫，再揭示兩半各自裝輪；圖像仍不提前顯示輪件。',
});
revisions.push({
  scene: 'turn-12', line: '6jx3', claims: ['t13'],
  before: '同在 1991 年，Plath 離開航空公司，全職經營 Travelpro。',
  after: 'Travelpro 說，Plath 一直飛到 1991 年；那年他離開航空公司，全職做箱子。',
  claim_text: { t13: 'Travelpro 自述 Plath 持續擔任機師至 1991 年，當年離開航空公司，全職經營公司' },
  sources: [{ index: 1, location: 'Travelpro history, Plath continued flying until 1991 and then left to run company full time', role: 'company account of career decision; no causal claim about patent grant' }],
  payoff: null, reason: '把 1989 車庫搬倉庫接到 1991 人物選擇；不與專利核准日期並排造成虛假因果。',
});
revisions.push({
  scene: 'origin-12', line: 'vdxp', claims: ['o10', 'h2'],
  before: '從阿魯巴度假回來，他走進麻州的行李箱工廠，開始試裝輪子。',
  after: 'Sadow 本來就是行李箱公司的主管；回到麻州工廠，他馬上試裝輪子。',
  claim_text: { o10: 'Sadow 回憶從阿魯巴回程轉機看見輪板，回到麻州工廠後開始試裝輪子', h2: 'Sadow 是行李箱公司的主管' },
  sources: [{ index: 6, location: 'ABC News 2010, Sadow’s luggage business and factory experiment after the airport observation', role: 'interview account of occupation and workshop action' }],
  payoff: '3zkh', reason: '接在具體家庭行李回憶後，不重複阿魯巴；把回家後的決定帶往樣品動作。',
});
revisions.push({
  scene: 'engine-r12-06', line: 'r12e06', claims: ['e24', 'e25'],
  before: '至於怎麼拖：一條可拆的拖帶，扣在箱子上端的環上，旅客拉著它往前走。',
    after: '專利提出，長路扣上拖帶來拉；要提箱時，普通箱原本的提把還在。',
  claim_text: {
    e24: 'Sadow 專利提出可拆拖帶扣在箱子上端的環上供旅客拉行',
    e25: 'Sadow 專利保留普通箱原有提把，可在需要提起時手提',
  },
  sources: [{ index: 0, location: 'US3653474A, detachable flexible strap fastens to ring while ordinary suitcase handle is retained', role: 'patent design choice, not evidence of every sold suitcase' }],
  payoff: 'zaky', reason: '以「專利提出」清楚區分設計主張與實際售出商品，接著回到推銷行動。',
});
revisions.push({
  scene: 'turn-04', line: '8wiw', claims: ['t4'],
  before: '他叫 Robert Plath，是西北航空的 747 機師。',
  after: '另一位決定動手的人，是西北航空的 747 機師 Robert Plath。',
  claim_text: { t4: 'Robert Plath 是西北航空 747 機師，後來自行設計輪子行李箱' },
  sources: [{ index: 5, location: 'ABC/USA TODAY 2012, Plath identified as a Northwest Airlines 747 pilot who developed Rollaboard', role: 'independent character introduction after Sadow retail arc' }],
  payoff: 'iu9y', reason: '百貨顧客接受後直接切到另一位人物與安檢阻力，不重講橫拖箱問題。',
});
revisions.push({
  scene: 'now-outro', line: 'g5b8', claims: ['n16'],
  before: '還記得開場的問題嗎？會滾的箱子缺的，是有人把它放上貨架，也讓人帶得順手。',
  after: '輪子早有人裝上箱子；自製、進貨、改直立，一次次解開旅途卡關，它才走進日常。',
  claim_text: { n16: '輪子箱從家庭自製、百貨展示到一體式機組行李，有不同人物各自解決的使用與採用障礙；三條證據不構成直接發明傳承' },
  sources: [{ index: 8, location: 'Winnetka account of Anita family-made case', role: 'independent early family action' }, { index: 6, location: 'ABC News 2010 account of Sadow and Macy demonstration', role: 'separate retail arc' }, { index: 1, location: 'Travelpro history of Plath crew design', role: 'later company account without claimed lineage' }],
  payoff: 'tszs', reason: '直接回答開場對比，保留三條獨立人物線，不用模板式「還記得」提問。',
});
revisions.push({
  scene: 'now-outro', line: 'xjmb', claims: [],
  before: '你拖過的箱子裡，哪一次輪子或拉桿的改變，最讓你省力？',
  after: '你最記得哪次箱子卡關：安檢、登機，還是樓梯？',
  claim_text: {}, sources: [], payoff: null,
  reason: '留言題連到片中實際阻力與最後仍須提箱的限制。',
});

// Retire explanation beats whose originating scene is no longer narrated.
const removedSceneIds = new Set(removedScenes.map((item) => item.id));
for (let index = revisions.length - 1; index >= 0; index--) {
  if (removedSceneIds.has(revisions[index].scene) || revisions[index].line === 'gtab') revisions.splice(index, 1);
}

const changedClaimIds = new Set();
for (const change of revisions) {
  const matches = video.scenes.filter((scene) => scene.id === change.scene);
  assert.equal(matches.length, 1, 'scene ' + change.scene);
  const scene = matches[0];
  const lines = scene.lines.filter((line) => line.id === change.line);
  assert.equal(lines.length, 1, 'line ' + change.line);
  assert.equal(lines[0].text, change.before, 'text ' + change.line);
  for (const id of change.claims) {
    assert.ok(scene.claims.includes(id), 'claim ' + id);
    changedClaimIds.add(id);
  }
  lines[0].text = change.after;
}
assert.ok(revisions.length >= 25, 'substantive narration revisions retained');
assert.ok(!video.scenes.some((scene) => scene.lines.some((line) => line.id === '6i8x')));

// Storyboard candidates are source-bound and stay unreviewed until image QA.
// Stop if the host snapshot's visual text has drifted; never rewrite media.
const visualRevisions = [
  {
    scene: 'hook-04',
    before: 'Medium shot of a 1970s city department store luggage counter with plain wooden display shelves. One generic store buyer in a 1970s suit leans over a flat suitcase lying on the counter that has small casters underneath and a rope tied to one end, frowning in doubt. No signs. Soft warm lamp light from overhead.',
    after: 'Medium shot of a generic 1970s department-store buying office. A buyer studies an unbranded closed sample case with an unreadable neutral expression; only its ordinary top and carrying handle rise above a high counter. Keep the casters, rope, full silhouette, purchase order and sales floor out of frame until the story reaches the prototype and Macy demonstration. Soft warm lamp light, no signs, words or logos.',
    reason: '冷開場只提出採購決定，表情不提前洩漏拒絕；樣品構造和結果留到後文。',
  },
  {
    scene: 'origin-01b',
    before: 'Wide shot of a quiet railway platform in the late 1920s. One anonymous mother in a plain travel coat leads five anonymous family members, an adult and four children, toward a waiting train while pulling one old leather suitcase with two small wheels and a wooden handle. The rolling case and family group occupy the middle third in diffuse daylight. No readable signs, text, logos or likeness to real people.',
    after: 'Wide shot of a quiet late-1920s railway platform. An anonymous mother, father and four children depart together after the son’s modification. One homemade suitcase with two small old stroller wheels and a wooden pulling handle is visible beside several plain cases; do not imply it is a retail product or a documented portrait of the family. Diffuse daylight; no readable signs, text, logos or real-person likeness.',
    reason: '造箱後才出發，畫面同步展示已有的家庭輪子箱；不再有出發前後顛倒。',
  },
  {
    scene: 'origin-08',
    before: 'Wide shot, a 1940s railway station platform with a plain steam train, one generic traveler in a 1940s hat and coat walks while pulling a suitcase rolling on small casters by its handle, relieved expression, the rolling suitcase as the focal object, mild grey overcast light.',
    after: 'Close-up of a period-neutral patent drafting table. A generic hand points to a proposed small caster attachment beneath an outlined suitcase on an unlabelled technical drawing. The diagram is clearly a plan, with no traveler, train platform, manufactured product, patent number or readable text. Soft desk light.',
    reason: '1943 年凱利專利圖只證明設計主張，不代表它當時已成為實際使用的市售箱。',
  },
  {
    scene: 'turn-r12-01',
    before: 'Close-up of a plain late-1980s desk, one anonymous hand places a blank line drawing of a small suitcase and separate trolley beside a blank drawing of an integrated wheeled case. The contrast is the focal object, soft lamp light, no legible words, patent number or logos.',
    after: 'Close-up of a plain late-1980s desk. An anonymous hand lays down a closed, unlabelled patent folder beside a loose strap and a separate luggage-trolley handle; the technical drawing inside stays hidden. Do not show the integrated case, recessed wheels or telescoping-handle layout before the patent explanation. Soft lamp light, no legible text, patent number or logos.',
    reason: '1989 年申請文件先入場，不用圖像提早交代接下來要講的機構。',
  },
  {
    scene: 'turn-09',
    before: 'Close-up in a 1980s garage workshop. Generic hands extend a telescoping metal handle from a plain upright suitcase with two wheels at its base. A simple hand tool rests nearby. The new integrated structure is the focus, warm lamp light, no words or logos.',
    after: 'Medium close-up in a generic 1980s home garage. Anonymous hands work on a closed plain suitcase at a bench with a simple hand tool nearby; crop the base and top so the two-wheel layout and telescoping handle are still hidden. This is the moment before the new design is described in the next shot. Warm lamp light, no words, labels or logos.',
    reason: '「做出 Rollaboard」先呈現車庫動作，兩輪、直立箱和伸縮拉桿要等下一句旁白才揭示。',
  },
  {
    scene: 'hook-01',
    before: 'Medium-wide shot of a 1970s airport concourse with a long tiled floor. On the right, one generic adult traveler strains forward, carrying two heavy, overstuffed plain suitcases by their handles, face tense with effort and visible to the viewer. On the left, a tall window shows a pale moon in a soft grey dusk sky, with open empty space for a headline. Mild overcast window light mixed with soft lamp light inside. The mood is tired and quietly comic.',
    after: 'Medium-close shot of a 1970s island airport concourse. One generic adult traveler strains to carry two heavy plain suitcases by their handles; the bags and his tired posture dominate the frame. A heavy machine glides through the far edge of frame, but crop out the board and all wheels underneath it. No moon, headline space, readable sign or brand. Mild overcast window light and a quietly comic contrast.',
    reason: '第一句即有沉箱與重機器滑行的反差，畫面暫不揭示輪板，留給第三句的真實觀察。',
  },
  {
    scene: 'hook-02',
    before: 'Wide shot of a 1970s island airport hallway with plain walls and a soft grey sky beyond the glass. One generic airport worker in plain work overalls pushes a heavy grey machine that rests on a low wooden skid with small wheels underneath. His expression is calm and easy. The focal point is the wheeled skid gliding across the floor. Mild overcast light from the side.',
    after: 'Medium shot of a 1970s island airport hallway. One anonymous man in plain period clothes pushes a heavy machine across the frame with apparent ease; keep its hidden support board and all wheels below the crop. The contrast with the nearby traveler carrying cases is visible. Mild side light, no occupational uniform, signs, words or logos.',
    reason: '第二鏡保留 Sadow 回憶中的推行動作，輪板結構到 hook-02b 才揭示。',
  },
  {
    scene: 'hook-02b',
    before: 'Close-up near the floor in the same airport hallway. One generic airport worker in plain work overalls pushes a heavy grey machine resting on a low wooden skid with small wheels underneath. His hands and calm face remain visible above the machine. The wheels and loaded board fill the foreground. Mild overcast light from the side.',
    after: 'Close-up near the floor in the same airport hallway. The anonymous man in plain period clothes pushes a heavy grey machine resting on a low wooden skid with small wheels underneath. His hands and face are partly visible above the machine. The wheels and loaded board fill the foreground. Mild overcast light from the side; no occupational uniform, text or logos.',
    reason: '揭示重機器與輪板，不給來源未指明的機場工作身分。',
  },
  {
    scene: 'origin-r12-02',
    before: 'Medium shot beside a quiet late-1920s station platform. One anonymous adult man in plain travel clothes lifts a heavy unwheeled suitcase by its handle while a separate small wheeled trunk rests nearby. The two different ways of moving a case are visually clear, gentle daylight, no signs, words or real-person likeness.',
    after: 'Medium shot beside a quiet late-1920s station platform. An anonymous adult man chooses to lift a heavy unwheeled suitcase and glances skeptically toward a small wheeled trunk near an anonymous adult woman. The two ways of moving luggage and the disagreement are clear; she has not set the wheeled trunk aside. Gentle daylight, no signs, words or real-person likeness.',
    reason: '只呈現館方所述的家庭反應，後續是否繼續使用留給 origin-r12-03。',
  },
  {
    scene: 'idea-07',
    before: 'Medium close-up of a generic 1970s executive seated at a wooden desk, pressing the button of a plain desk intercom with a decisive, confident look. The flat caster-wheeled suitcase stands parked beside his chair. Warm desk lamp light falls from the left.',
    after: 'Medium shot in a generic 1970s executive office. A suited executive gestures for a buyer at the doorway to come into the room while a flat caster-wheeled suitcase stands parked beside the desk. Do not show an intercom, signed order or stockroom. Warm desk lamp light from the left, no words or logos.',
    reason: 'Sadow 回憶副總裁叫回採購，沒有證據支持使用對講機；也不提前畫出進貨結論。',
  },
  {
    scene: 'turn-07b',
    before: 'Close-up at a 1980s airport security checkpoint. An unbranded hard-shell suitcase and a compact metal luggage trolley remain joined by a visible mounting screw. A generic adult traveler\'s hand rests beside the fixed joint. The fixed joint sits in the middle third with generous space around it. Soft grey overhead light, no insignia, text or logos',
    after: 'Medium shot at a generic 1980s airport security checkpoint. An anonymous security worker gestures toward an unbranded hard-shell suitcase mounted to a compact metal luggage trolley; an anonymous traveler points to the visible fixed joint. The two are in conversation, with no cleared-gate gesture or passage beyond the checkpoint. Soft grey overhead light, no insignia, text or logos.',
    reason: '對應 Plath 自述的要求和回答；畫面不宣稱獨立證實安檢放行。',
  },
];
for (let index = visualRevisions.length - 1; index >= 0; index--) {
  if (removedSceneIds.has(visualRevisions[index].scene)) visualRevisions.splice(index, 1);
}
for (const change of visualRevisions) {
  const scene = video.scenes.find((item) => item.id === change.scene);
  assert.ok(scene, 'visual scene ' + change.scene);
  assert.equal(scene.data.prompt, change.before, 'visual source drift ' + change.scene);
  scene.data.prompt = change.after;
}
const prototypeScene = video.scenes.find((scene) => scene.id === 'origin-13');
assert.deepEqual(prototypeScene.lines.map((line) => line.id), ['3zkh', 'idiy']);
prototypeScene.lines = prototypeScene.lines.filter((line) => line.id !== 'idiy');
const splitPrototypeScene = {
  id: 'idea-13b', template: 'shot',
  data: {
    prompt: 'Medium-close side view in a plain 1970 luggage workshop. An anonymous worker pulls a short rope tied to a suitcase whose four small steel trunk casters now bear its weight as the case rolls across the floor. Show the rope and motion clearly; no sign, words, brand or real-person likeness.',
    camera: 'track right', visual: 'still',
  },
  claims: ['i34'],
  lines: [{ id: 'idiy', text: '再綁一條繩子，箱子就跟著人往前滾。' }],
};
const familyStreetScene = {
  id: 'origin-street', template: 'shot',
  data: {
    prompt: 'Medium shot on an anonymous late-1920s city street. An adult woman and several children are just beginning to pull small homemade wheeled trunks. Do not depict a recorded passerby reaction: the historical society only judges the sight unusual for its time. Keep the father and later lecture journey out of frame; show this first public use, not evidence that the family kept using the cases after anyone objected. No captions, period brand signs, words or real-person likeness.',
    camera: 'track left', visual: 'still',
  },
  claims: ['o29'],
  lines: [{ id: 'r13o02', text: '到了街上，母子拉著自製輪子箱；在 1928 年，這幅景象少見得很。' }],
};

// Compose the six story chapters in event order. Scene/claim prefixes are a
// host allocation contract, so a cross-chapter move gets a destination prefix
// here and in the bridge map; the unchanged narration line ID identifies the
// same utterance. This is still an offline proposal, not host chapter source.
const patentScenes = [
  {
    id: 'turn-patent-answer', template: 'shot',
    data: {
      prompt: 'Clean close-up view of a proposed integrated late-1980s carry-on suitcase design: a retractable handle nested in the body and two small wheels recessed at the lower edge. A separate empty trolley stands blurred far behind to show what the design aims to avoid. This is an explanatory patent-design illustration, not a photo of a sold model. No words, numerals, logos or real-person likeness.',
      camera: 'push in', visual: 'still',
    },
    claims: ['t38'],
    lines: [{ id: 'r13p02', text: '他後來的專利把這個想法寫成登機箱設計：輪子和拉桿屬於箱子本身，不用另帶一台推車去反覆拆綁。' }],
  },
];
const guardResponseScene = {
  id: 'turn-07c', template: 'shot',
  data: {
    prompt: 'Medium close-up at a generic late-1980s airport security desk. An anonymous traveler who has just pointed at the fixed joint listens to an anonymous guard across the counter; both remain by the joined case and trolley. Show a neutral spoken response with no nod of clearance, gate crossing, official badge detail, words, signs or logos.',
    camera: 'static', visual: 'still',
  },
  claims: ['t29'],
  lines: [{ id: 'r13t02', text: '安檢員聽完，只回了一句：「好。」' }],
};
const turn09Scene = video.scenes.find((scene) => scene.id === 'turn-09');
assert.deepEqual(turn09Scene.lines.map((line) => line.id), ['jm3w', '3zwf']);
const designRevealLine = turn09Scene.lines.pop();
const turnRevealScene = {
  id: 'turn-09b', template: 'shot',
  data: {
    prompt: 'Clear medium side view of a late-1980s upright rolling suitcase form in a generic garage, revealed as an anonymous hand extends the telescoping pull handle from a compact case with exactly two small base wheels. Keep the case unbranded and illustrative; do not show a documented historical prototype or later patent internals. Warm workshop light, no signs, words or logos.',
    camera: 'pull out', visual: 'still',
  },
  claims: ['t31'], lines: [designRevealLine],
};
const cabinObstacleScene = {
  id: 'turn-cabin-obstacle', template: 'shot',
  data: {
    prompt: 'Medium shot of a late-1980s airplane boarding aisle. One anonymous traveler struggles to turn a single oversized horizontal four-caster suitcase toward a visibly smaller overhead space. This is the patent-described size limitation of a large four-wheel case; do not depict an external trolley or tie it to the separate security-cart problem. Keep the case outside the bin. No boarding staff, readable signs, brand, baggage policy text or historical product likeness.',
    camera: 'static', visual: 'still',
  },
  claims: ['t35'],
  lines: [{ id: 'r13t01', text: '另一種四輪大箱太大，進不了客艙；他想做一只可帶上機的箱子。' }],
};
const overheadScene = {
  id: 'now-overhead', template: 'shot',
  data: {
    prompt: 'Medium-wide view of an anonymous 1990s airline cabin. A compact unbranded wheeled carry-on rests inside a generous overhead compartment while an anonymous traveler seated below looks up. Illustrate a later cabin accommodation, not a specific carrier or dated aircraft refit. No text, logo, visible airline uniform or real-person likeness.',
    camera: 'tilt up', visual: 'still',
  },
  claims: ['n28'],
  lines: [{ id: 'r13n01', text: '報導回顧，航空公司後來也調整頭頂置物空間，讓輪子登機箱放得進去。' }],
};
const addedStoryScenes = [
  {
    id: 'origin-budget', template: 'shot',
    data: { prompt: 'Illustrative late-1920s home packing scene before departure: an anonymous mother considers several ordinary heavy suitcases and a modest travel budget while a small inset silhouette shows distant travelers hiring a porter. This is a visual comparison, not a recorded port transaction. No wheeled luggage or completed invention yet; no signs, text, logos or real-person likeness.', camera: 'pan left', visual: 'still' },
    claims: ['o30'], lines: [{ id: 'r14o01', text: '那時，有錢的旅客能付小費，把重箱交給搬運工或旅館服務生；安妮塔的旅費卻掐得很緊。' }],
  },
  {
    id: 'origin-transfer', template: 'shot',
    data: { prompt: 'Two-stage late-1920s travel illustration: the same anonymous family carries closed ordinary suitcases from a ship landing toward a train platform, with a different lodging doorway in the far distance. Keep wheels, pull handles and a completed modified case out of frame; focus on having to lift the same weight at each transfer. No signs, text, logos or real-person likeness.', camera: 'track right', visual: 'still' },
    claims: ['o31'], lines: [{ id: 'r14o02', text: '港口、月台、下一處住處，箱子一次次又得提起來；輪子若要有用，得經得起整趟路。' }],
  },
  {
    id: 'idea-memory', template: 'shot',
    data: { prompt: 'Medium-wide return-trip illustration at a plain airport around 1970. An anonymous couple and two children pause beside two large unbranded, unwheeled suitcases that look tightly packed; the adult holding both handles visibly strains. Keep the earlier wheeled platform and any later prototype out of frame. No numbers, labels, airline marks or real-person likeness.', camera: 'push in', visual: 'still' },
    claims: ['i35'], lines: [{ id: 'r14i01', text: '多年後，開場的 Sadow 一家從阿魯巴回來；兩只二十七吋箱子都塞滿了。' }],
  },
  {
    id: 'idea-wife', template: 'shot',
    data: { prompt: 'Medium close-up in a generic 1970 airport concourse. An anonymous adult carrying two heavy plain suitcases turns toward an anonymous adult companion as if sharing an idea; a wheeled machinery skid passes blurred far behind them. Do not show a completed rolling suitcase, workshop or patent drawing yet. No readable signs, airline logos or real-person likeness.', camera: 'pan left', visual: 'still' },
    claims: ['i36'], lines: [{ id: 'r14i02', text: '他轉頭對妻子說：我們的行李也該裝輪子。' }],
  },
  {
    id: 'turn-cart-distinction', template: 'shot',
    data: { prompt: 'Close-up at a generic late-1980s airport security queue. An anonymous traveler has loosened the elastic cords holding an ordinary hard-shell case to a separate wheeled metal trolley; the two objects are visibly distinct. No horizontal strap-pulled caster suitcase, clearance gesture, readable sign, logo or named-person likeness.', camera: 'tilt down', visual: 'still' },
    claims: ['t30'], lines: [{ id: 'r14t01', text: '前一只橫拖箱的缺點在地板上；這裡的難題在連接處：輪子屬於推車，箱子必須離開它。' }],
  },
  {
    id: 'turn-cart-board', template: 'shot',
    data: { prompt: 'Explanatory view at a generic late-1980s airplane boarding doorway. An anonymous traveler must again separate ordinary bags from a separate metal luggage trolley before stowing them. Keep the trolley outside the cabin, and do not show a modern integrated wheeled case, a clearance gesture, readable signs, text or logos.', camera: 'static', visual: 'still' },
    claims: ['t33'], lines: [{ id: 'r14n02', text: '用一般外置推車，好不容易在安檢綁回去，登機前又得拆一次；推車和箱子不能原樣收進機艙。' }],
  },
  {
    id: 'turn-cart-exit', template: 'shot',
    data: { prompt: 'Explanatory view just after leaving an airplane. An anonymous traveler bends to retie ordinary bags onto a separate small metal luggage trolley with elastic cord. No integrated wheeled suitcase, readable gate sign, official insignia, logo or real-person likeness.', camera: 'pull out', visual: 'still' },
    claims: ['t34'], lines: [{ id: 'r14n03', text: '下機後還要把行李重新固定。專利說，少提箱子的代價，反而是多帶一台要照顧的車。' }],
  },
  {
    id: 'turn-cabin-risk', template: 'shot',
    data: { prompt: 'Illustrative comparison at a generic late-1980s airline check-in area. A large horizontal four-caster case stands beside a smaller overhead-bin-size outline; the large case remains outside the cabin and is offered for check-in. Do not depict the case as actually lost or damaged. No external trolley, airline policy placard, readable text, logos or real-person likeness.', camera: 'static', visual: 'still' },
    claims: ['t36'], lines: [{ id: 'r14n04', text: '專利也指出，大型四輪箱得託運；行李若沒跟人同時抵達，或在運送中受損，就是另一層風險。' }],
  },
  {
    id: 'now-handle-risk', template: 'shot',
    data: { prompt: 'Close-up explanatory illustration of a proposed upright wheeled suitcase handle at full extension. An anonymous hand grips the raised handle while the hidden lower guide and its locking detail remain out of frame. Show the practical question of whether the handle stays extended under a pulling hand; do not reveal the internal offset guide or an actual product test. No text or logo.', camera: 'push in', visual: 'still' },
    claims: ['n34'], lines: [{ id: 'r14n05', text: '還有拉桿：拉高後若一受力就縮回去，輪子再順也不好用；專利怎麼讓它停在伸出的位子？' }],
  },
  {
    id: 'now-handle-release', template: 'shot',
    data: { prompt: 'Simple two-panel patent-design illustration of a telescoping suitcase-handle rod inside a guide sleeve. In the first panel a slightly offset lower guide presses the rod against the sleeve when raised; in the second an anonymous hand applies downward pressure to slide it back. Keep this clearly an illustrative proposed mechanism, not a photograph of every retail handle. No labels, words, numerals or logos.', camera: 'tilt down', visual: 'still' },
    claims: ['n35'], lines: [{ id: 'r14n06', text: '拉高時，偏心導件把桿身擠向套筒，摩擦力卡住位置；要收回，就得往下施力推開。' }],
  },
  {
    id: 'now-piggyback', template: 'shot',
    data: { prompt: 'Clean explanatory patent-design illustration of a compact upright two-wheel carry-on with a small second travel bag secured on top by an optional detachable hook and strap. The suitcase is stationary, the second bag visibly separate. Show a proposed accessory rather than a documented retail sale or named user. No words, numbers, logos or real-person likeness.', camera: 'pull out', visual: 'still' },
    claims: ['n36'], lines: [{ id: 'r14n07', text: '直立箱不只自己會走。這份專利還畫了可拆的掛件，讓另一件小袋能跟著箱子一起帶。' }],
  },
  {
    id: 'now-piggyback-limit', template: 'shot',
    data: { prompt: 'Simple patent-proposal diagram of one upright two-wheel suitcase used as the base for several separate small travel items, shown as four distinct unbranded luggage silhouettes held by optional removable attachments. Keep the stack balanced in an explanatory side view, not as a photographed or tested retail product. No words, numerals, logos or people.', camera: 'static', visual: 'still' },
    claims: ['n38'], lines: [{ id: 'r14n09', text: '專利甚至主張，加上附件最多能帶四件行李；這時，箱子自己像一台小推車。' }],
  },
  {
    id: 'now-era-bridge', template: 'shot',
    data: { prompt: 'Medium shot of an anonymous traveler in a plain late-1990s airport corridor, gently tipping a compact unbranded two-wheel upright case so its wheels touch the floor. Leave the later four-wheel standing case out of frame. This is an explanatory movement shot, not a historical reconstruction. No signs, logos, words or real-person likeness.', camera: 'track left', visual: 'still' },
    claims: ['n37', 'n39'], lines: [{ id: 'r14n08', text: '兩輪直立箱走路時，仍要把箱身傾斜。再看後來另一款箱子，怎麼讓輪子站著走。' }],
  },
];
// The documentary cut keeps the security-cart account and crew-bag memoir as
// separate attributed threads. It drops the patent feature catalogue.
const retiredAddedSceneIds = new Set([
  'turn-cart-distinction', 'turn-cabin-risk', 'now-handle-risk',
  'now-handle-release', 'now-piggyback', 'now-piggyback-limit',
  'origin-transfer', 'turn-cart-board', 'turn-cart-exit', 'now-era-bridge',
]);
for (let index = addedStoryScenes.length - 1; index >= 0; index--) {
  if (retiredAddedSceneIds.has(addedStoryScenes[index].id)) addedStoryScenes.splice(index, 1);
}
const emmerUrl = 'https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf';
const crewInterviewUrl = 'https://www.globaltravelerusa.com/reinventing-the-wheel/';
const anitaBackgroundUrl = 'https://www.winnetkahistory.org/who-were-the-burnhams/';
const samsoniteResearchUrl = 'https://www.quirks.com/articles/research-with-travelers-helps-samsonite-develop-a-convenient-new-line-of-luggage/';
const anitaSketchScene = {
  id: 'origin-sketches', template: 'shot',
  data: { prompt: 'An anonymous mother and two daughters sketch in a modest late-1920s lodging dining room, with one already-made unbranded family wheeled trunk standing quietly near the doorway. Suggest drawings exchanged for food or lodging through a simple handover, without depicting a specific named transaction. No readable words, brand, money figure or real-person likeness.', camera: 'pan right', visual: 'still' },
  claims: ['o32'], lines: [{ id: 'r15o01', text: '在路上，母女沿途畫素描，拿作品換餐食或住宿；自製輪子箱也陪著一家人走。' }],
};
const emmerScenes = [
  {
    id: 'turn-emmer-01', template: 'shot',
    data: { prompt: 'Anonymous late-1980s airline crew corridor, with a plain closed notebook and several unbranded bags in the foreground. A pilot colleague appears in profile but no named-person likeness is depicted. Introduce a separate memoir thread; no security trolley or completed later integrated case reveal. No words or logos.', camera: 'push in', visual: 'still' },
    claims: ['t39'], lines: [{ id: 'r15t01', text: '還有一條沒標年份的線索，來自 Plath 同機組一位機師的回憶。' }],
  },
  {
    id: 'turn-emmer-02', template: 'shot',
    data: { prompt: 'Illustration of anonymous period airline crew with an earlier upright wheeled crew bag, a fabric bag supported by a simple frame and a small upper zip compartment. Keep it clearly distinct from the separate metal trolley tied to a hard case at security and from the later integrated two-wheel case. No brand lettering or real-person likeness.', camera: 'track right', visual: 'still' },
    claims: ['t40'], lines: [{ id: 'r15t02', text: '他說，機組早有人用另一款直立輪子袋，空服員也在用。' }],
  },
  {
    id: 'turn-emmer-03', template: 'shot',
    data: { prompt: 'Two anonymous male pilots in a plain crew corridor, one still carrying a heavy traditional flight bag by hand while a wheeled crew bag is nearby with another crew member. Their reserve is understated, not ridicule or universal behavior. No later integrated case, words, logos or real-person likeness.', camera: 'static', visual: 'still' },
    claims: ['t41'], lines: [{ id: 'r15t03', text: '有些男機師卻仍寧可手提，怕拉著箱子被看輕。' }],
  },
  {
    id: 'turn-emmer-04', template: 'shot',
    data: { prompt: 'Close-up of an older wheeled crew bag upper zip pocket, with anonymous hands taking keys and glasses from it while a wallet stays safely inside. Do not show the later integrated case, separate security trolley or branded product. Warm cabin prep light, no text or logos.', camera: 'tilt down', visual: 'still' },
    claims: ['t42'], lines: [{ id: 'r15t04', text: 'Plath 喜歡上層拉鍊格：鑰匙、眼鏡、錢包，不必翻整箱就拿得到。' }],
  },
  {
    id: 'turn-emmer-05', template: 'shot',
    data: { prompt: 'Anonymous pilot hands compare the rough seams of an earlier fabric wheeled crew bag with a private sketch of an improved bag. The sketch remains partly folded; no finished design, security trolley or later patent diagram. No legible words, logo or real-person likeness.', camera: 'push in', visual: 'still' },
    claims: ['t43'], lines: [{ id: 'r15t05', text: '可他嫌袋子做得粗糙，自己畫了改良草圖。' }],
  },
  {
    id: 'turn-emmer-06', template: 'shot',
    data: { prompt: 'Generic Seattle airport satellite terminal meeting: one anonymous pilot offers a folded design sketch to an anonymous maker of an earlier wheeled crew bag. Show the handover before any decision, with no agreement, product launch, security trolley or named likeness. No readable signs or logos.', camera: 'pan left', visual: 'still' },
    claims: ['t44'], lines: [{ id: 'r15t06', text: '在西雅圖航站，他把草圖遞給這款袋子的製作者。' }],
  },
  {
    id: 'turn-emmer-07', template: 'shot',
    data: { prompt: 'Small three-panel illustration of two anonymous men meeting in the same generic terminal on separate weeks: first a pending hand gesture, then a reserved decline over a still folded sketch. Do not depict a formal company procurement board, signed rejection or fixed calendar year. No words, logos or real-person likeness.', camera: 'static', visual: 'still' },
    claims: ['t45'], lines: [{ id: 'r15t07', text: '隔一週再碰面，對方還沒跟合夥人談；又過一週，答覆是不做。' }],
  },
  {
    id: 'turn-emmer-08', template: 'shot',
    data: { prompt: 'An anonymous pilot leaves a generic terminal holding his own folded luggage-design sketch, with the earlier crew bag maker walking away in soft background. The drawing stays hidden and the finished integrated case is not visible. Do not imply a dated sequence with the security event. No words, logos or real-person likeness.', camera: 'pull out', visual: 'still' },
    claims: ['t46'], lines: [{ id: 'r15t08', text: '草圖沒人接。那位機師回憶，Plath 繼續自己摸索。' }],
  },
  {
    id: 'turn-balance-01', template: 'shot',
    data: { prompt: 'Anonymous crew member gently pulls an early upright wheeled bag with a separate flight bag resting too high on top; the upper bag leans forward. Show a practical balance problem without a fall, injury, security trolley, four-bag stack or branded commercial model. No words or logos.', camera: 'track left', visual: 'still' },
    claims: ['t47'], lines: [{ id: 'r15t09', text: '他還記得，另一件飛行袋擺在頂上，拉起來容易前傾。' }],
  },
  {
    id: 'turn-balance-02', template: 'shot',
    data: { prompt: 'Close-up illustrative later improvement to a generic upright wheeled crew bag: an adjustable strap and small hook hold one separate flight bag lower against the bag body. Show the lower center of mass, without claiming a universal retail feature or exact historical prototype. No words, logos or named likeness.', camera: 'tilt down', visual: 'still' },
    claims: ['t48'], lines: [{ id: 'r15t10', text: '依他的回憶，Plath 後來用可調掛帶和掛鉤，把第二件包掛得更低、更穩。' }],
  },
];
const emmerOpening = emmerScenes.find((scene) => scene.id === 'turn-emmer-01');
emmerOpening.claims.push('t40');
emmerOpening.lines[0].text = '同機組機師 Bill Emmer 回憶，當時機組已用另一款輪子袋；這段往事，他沒標年份。';
emmerOpening.data.prompt = 'Anonymous airline crew corridor with a distinct early fabric wheeled crew bag and its metal support frame, while an anonymous colleague observes. This is an undated memoir thread, distinct from the separate security trolley and the later integrated upright case. No words, logos or named-person likeness.';
const emmerSketch = emmerScenes.find((scene) => scene.id === 'turn-emmer-05');
emmerSketch.claims.unshift('t42');
emmerSketch.lines[0].text = 'Plath 喜歡舊袋上層能放鑰匙、眼鏡，卻嫌做工粗糙，於是畫了改良草圖。';
const emmerMaker = emmerScenes.find((scene) => scene.id === 'turn-emmer-07');
emmerMaker.claims.unshift('t44');
emmerMaker.lines[0].text = 'Emmer 說，Plath 在西雅圖把草圖交給製作者；隔了兩週，得到的答覆是不做。';
emmerMaker.data.prompt = 'Two small chronological panels in a generic Seattle terminal: first an anonymous pilot offers a folded design sketch to a wheeled crew-bag maker, then the maker declines at a later meeting. Show no exact calendar year, formal company procurement vote, security trolley, finished case, words or logos.';
emmerScenes.find((scene) => scene.id === 'turn-balance-01').lines[0].text = 'Emmer 還記得，另一件飛行袋若放在頂上，拉著走容易前傾。';
emmerScenes.find((scene) => scene.id === 'turn-balance-02').lines[0].text = '依 Emmer 的回憶，Plath 後來用可調掛帶，把第二件包掛得更低、更穩。';
for (let index = emmerScenes.length - 1; index >= 0; index--) {
  if (new Set(['turn-emmer-02', 'turn-emmer-04', 'turn-emmer-06', 'turn-emmer-08']).has(emmerScenes[index].id)) emmerScenes.splice(index, 1);
}
const emmerPassengerScene = {
  id: 'now-passenger', template: 'shot',
  data: { prompt: 'Anonymous late-1980s airport concourse: flight attendants stride through the terminal wheeling unbranded upright two-wheel cases, while some travelers look over with curiosity. Show observation without invented dialogue, sale transaction, exact airline uniforms, readable text, logos or real-person likeness.', camera: 'track right', visual: 'still' },
  claims: ['n44'], lines: [{ id: 'r15n01', text: '《紐約時報》回顧，旅客在航站看見空服員拉箱快步走，新的市場才慢慢打開。' }],
};
const crewRequestScene = {
  id: 'now-crew-request', template: 'shot',
  data: { prompt: 'Anonymous airline pilots in a late-1980s crew room, one pulling a plain integrated upright wheeled suitcase while two colleagues ask to inspect it and gesture toward their own heavy bags. Show a request, not a signed purchase or exact historical prototype. No readable words, brand logo or named-person likeness.', camera: 'push in', visual: 'still' },
  claims: ['n45'], lines: [{ id: 'r15n02', text: 'Travelpro 當時執行長回憶，其他機師看他拉著箱子，就請他也做一只。' }],
};
const retailToSecurityScene = {
  id: 'engine-10b', template: 'shot',
  data: { prompt: 'Visual handoff from a 1970s luggage-store doorway to a different late-1980s airport security queue. In the airport half, show only an unbranded hard case secured to a separate metal luggage trolley approaching the checkpoint; do not show the disassembly, guard answer or an integrated suitcase yet. Anonymous people, illustrative transition, no words or logos.', camera: 'track right', visual: 'still' },
  claims: ['e36'], lines: [{ id: 'r16e01', text: '百貨店這關過了；在機場，另一種帶箱子的推車，卻卡在安檢口。' }],
};
// A separate manufacturer runs its own experiment in the same era. Bob Bengen
// describes Samsonite's Piggyback work as its research director in 1992. This
// sequence neither makes Piggyback a Rollaboard nor links it causally to Spinner.
const samsoniteScenes = [
  {
    id: 'now-sam-01', template: 'shot',
    data: { prompt: 'Anonymous mid-1980s luggage design office. A closed conventional hard-shell suitcase sits beside a soft travel bag while two company staff compare them. Introduce a separate company thread, without the completed wheeled prototype or later four-wheel case. No brand sign, writing or real-person likeness.', camera: 'push in', visual: 'still' },
    claims: ['n46'], lines: [{ id: 'r16n01', text: '把時間倒回 1986 年。另一家行李公司的研究主管回憶：Samsonite 當時正擔心硬殼箱不再受歡迎。' }],
  },
  {
    id: 'now-sam-02', template: 'shot',
    data: { prompt: 'Close view of hands placing a separate small bag atop a plain large hard-shell wheeled prototype and testing an unbranded hidden pull handle, in a mid-1980s workshop. This belongs to a separate luggage-company research line developing a stacked-bag design from earlier concept research. Do not reveal the later parking-lot result. No readable words, logos or real-person likeness.', camera: 'tilt down', visual: 'still' },
    claims: ['n47'], lines: [{ id: 'r16n02', text: '他們把早就研究過的「小袋疊大箱」想法做成樣品。畫在紙上很方便，推到不平的地上還穩嗎？' }],
  },
  {
    id: 'now-sam-03', template: 'shot',
    data: { prompt: '1987 outdoor company parking lot, first frame of a test: anonymous staff member starts to pull one hard-shell two-wheel stacked-bag prototype toward a low curb, a short gravel strip and a shallow ditch beyond. Do not depict a successful finish yet. No readable signs, logos or named-person likeness.', camera: 'track right', visual: 'still' },
    claims: ['n48'], lines: [{ id: 'r16n03', text: '1987 年，員工連總裁都下停車場，把樣品推過路緣、碎石和淺溝，專測真實旅途會卡住的地方。' }],
  },
  {
    id: 'now-sam-04', template: 'shot',
    data: { prompt: 'End of the same internal 1987 outdoor trial: an anonymous staff member steadies the hard-shell Piggyback prototype after the low curb and gravel strip, with a separate small bag still secured on top. Show the research director\'s reported positive internal result, not independent market proof or an exact historical photo. No logos, readable words or real-person likeness.', camera: 'pull out', visual: 'still' },
    claims: ['n49'], lines: [{ id: 'r16n04', text: '按這位主管的說法，公司內部試拉後覺得它穩，頂上的小袋也跟著走；但路障還只在停車場。' }],
  },
  {
    id: 'now-sam-05', template: 'shot',
    data: { prompt: 'Generic late-1980s luggage trade show obstacle course. Anonymous visitors take turns testing a plain hard-shell two-wheel Piggyback style case on a low curb and gravel patch, with company staff nearby. This represents the reported 1988 demonstration and reactions, not measured population-wide demand. No readable exhibition signs, logos or real-person likeness.', camera: 'track left', visual: 'still' },
    claims: ['n50'], lines: [{ id: 'r16n05', text: '隔年，他們把同樣路線搬進展場，讓參觀者親手推。主管回憶，現場反應好；但原有一道門檻還沒解。' }],
  },
  {
    id: 'now-sam-06', template: 'shot',
    data: { prompt: 'Illustrative late-1980s luggage research room, not a real airplane: a full-size hard-shell two-wheel stacked-bag case stands beside a smaller generic carry-on-size silhouette and overhead-bin outline. Show the full-size case outside the outline to convey the separate product-size obstacle, without portraying an actual denied boarding event or universal airline rule. No insignia, readable signs, words or logos.', camera: 'static', visual: 'still' },
    claims: ['n51'], lines: [{ id: 'r16n06', text: '這款大箱好推，卻不能當手提箱上機。要進狹窄走道、塞進尺寸各異的置物櫃，得另外改。' }],
  },
  {
    id: 'now-sam-07', template: 'shot',
    data: { prompt: '1988 anonymous flight-attendant research discussion around a table with an unbranded carry-on prototype; participants gesture toward a narrow airplane aisle model, varied overhead-bin outlines and a separate cart parked aside. This generic cart discussion is distinct from the earlier named pilot\'s security encounter. No text, logos, exact airline uniform or named-person likeness.', camera: 'push in', visual: 'still' },
    claims: ['n52'], lines: [{ id: 'r16n07', text: '1988 年，公司找空服員試談。他們說外加推車不好用，機上走道窄、頭頂空間又不一樣。' }],
  },
  {
    id: 'now-sam-08', template: 'shot',
    data: { prompt: 'Illustrative late-1980s luggage research room, not a real aircraft: anonymous screened participants take turns wheeling, lifting and opening a smaller hard-shell stacked-bag carry-on sample, with a plain narrow-aisle mockup and overhead-size outline in the background as design criteria only. Do not depict actual in-flight testing or imply all aircraft accepted it. No logos, readable words, exact historical product photo or real-person likeness.', camera: 'track right', visual: 'still' },
    claims: ['n53'], lines: [{ id: 'r16n08', text: '當時，手提款原型已在。他們再找篩選過的旅客推、提、打開看，收了意見再改。' }],
  },
  {
    id: 'now-sam-09', template: 'shot',
    data: { prompt: 'Plain early-1990s luggage department with a compact two-wheel hard-shell stacked-bag carry-on displayed beside its distinct larger sibling; an anonymous traveler examines the smaller case. Show a separate product family arriving in stores, not a sale count or causal link to other designs. No readable signs, prices, logos or real-person likeness.', camera: 'pull out', visual: 'still' },
    claims: ['n54'], lines: [{ id: 'r16n09', text: '研究主管寫道：改過樣子、開始量產後，這款疊袋式手提箱在 1990 年進了美國店面。這是另一條解法。' }],
  },
];
const samsoniteOpening = samsoniteScenes.find((scene) => scene.id === 'now-sam-01');
samsoniteOpening.claims.push('n47');
samsoniteOpening.lines[0].text = '把時間撥回 1986 年。Samsonite 研究主管回憶，硬殼箱不再討喜，他們把先前「小袋疊大箱」的想法做成輪子樣品。';
samsoniteScenes.find((scene) => scene.id === 'now-sam-06').lines[0].text = '還有一道原本沒解的門檻：這款大箱好推，卻不適合當手提行李進客艙。';
samsoniteScenes.find((scene) => scene.id === 'now-sam-07').lines[0].text = '1988 年，他們請空服員談已做出的手提款：外加推車不好用，機上走道窄，頭頂空間也不一樣。';
for (let index = samsoniteScenes.length - 1; index >= 0; index--) {
  if (new Set(['now-sam-02', 'now-sam-05', 'now-sam-08']).has(samsoniteScenes[index].id)) samsoniteScenes.splice(index, 1);
}
const chapterLayout = [
  { prefix: 'hook', title: '兩只沉箱旁的意外', ids: ['hook-01', 'hook-02', 'hook-02b', 'hook-03', 'hook-04', 'hook-06'] },
  { prefix: 'origin', title: '安妮塔出發前的難題', ids: ['origin-r12-01', 'origin-budget', 'origin-03', 'origin-01b', 'origin-street', 'origin-sketches', 'origin-r12-02', 'origin-r12-03', 'origin-06'] },
  { prefix: 'idea', title: '機場裡的兩只沉箱', ids: ['idea-memory', 'idea-wife', 'engine-01', 'origin-12', 'origin-13', 'idea-13b', 'origin-14', 'engine-r12-02', 'engine-r12-06', 'origin-16'] },
  { prefix: 'engine', title: '樣品走進百貨辦公室', ids: ['idea-01', 'idea-02', 'idea-03b', 'idea-05', 'idea-06', 'idea-07', 'idea-07b', 'idea-08', 'idea-09', 'idea-10', 'engine-10b'] },
  { prefix: 'turn', title: '安檢口的另一道關', ids: ['turn-04', 'turn-05', 'turn-06', 'turn-r12-01', 'turn-07', 'turn-07b', 'turn-07c', ...emmerScenes.filter((scene) => scene.id.startsWith('turn-emmer')).map((scene) => scene.id), 'turn-09', 'turn-09b', ...emmerScenes.filter((scene) => scene.id.startsWith('turn-balance')).map((scene) => scene.id)] },
  { prefix: 'now', title: '箱子走出車庫之後', ids: ['now-crew-request', 'turn-10', 'now-passenger', ...samsoniteScenes.map((scene) => scene.id), 'turn-11', 'turn-12', 'now-overhead', 'now-01', 'now-05', 'now-06', 'now-outro'] },
];
const extraScenes = [splitPrototypeScene, familyStreetScene, guardResponseScene, turnRevealScene, overheadScene, ...addedStoryScenes, anitaSketchScene, ...emmerScenes, emmerPassengerScene, crewRequestScene, retailToSecurityScene, ...samsoniteScenes];
const oldSceneById = new Map([...video.scenes, ...extraScenes].map((scene) => [scene.id, scene]));
assert.equal(oldSceneById.size, video.scenes.length + extraScenes.length, 'old scene IDs unique');
const layoutIds = chapterLayout.flatMap((chapter) => chapter.ids);
assert.equal(new Set(layoutIds).size, layoutIds.length, 'layout IDs unique');
assert.deepEqual([...layoutIds].sort(), [...oldSceneById.keys()].sort(), 'layout must cover every remaining scene');
const claimIdRemap = {
  o10: 'i21', o11: 'i22', o12: 'i23', o13: 'i24', o15: 'i25', h2: 'i37',
  e17: 'i26', e20: 'i28', e21: 'i29', e23: 'i31', e24: 'i32', e25: 'i33',
  i1: 'e26', i2: 'e27', i16: 'e28', i5: 'e29', i14: 'e30', i7: 'e31', i17: 'e32', i8: 'e33', i9: 'e34', i10: 'e35',
  t9: 'n40', t10: 'n41', t11: 'n42', t13: 'n43',
};
assert.equal(new Set(Object.values(claimIdRemap)).size, Object.keys(claimIdRemap).length, 'claim ID remap unique');
const sceneIdRemap = {};
video.scenes = chapterLayout.flatMap((chapter) => chapter.ids.map((oldId, index) => {
  const scene = oldSceneById.get(oldId);
  assert.ok(scene, 'layout scene ' + oldId);
  const oldPrefix = oldId.split('-')[0];
  const newId = oldPrefix === chapter.prefix ? oldId : chapter.prefix + oldId.slice(oldPrefix.length);
  if (newId !== oldId) sceneIdRemap[oldId] = newId;
  scene.id = newId;
  scene.claims = (scene.claims ?? []).map((id) => claimIdRemap[id] ?? id);
  if (index === 0) scene.chapter = chapter.title;
  else delete scene.chapter;
  return scene;
}));
assert.equal(new Set(video.scenes.map((scene) => scene.id)).size, video.scenes.length, 'new scene IDs unique');
for (const chapter of chapterLayout) {
  for (const oldId of chapter.ids) {
    const newId = sceneIdRemap[oldId] ?? oldId;
    assert.ok(newId.startsWith(chapter.prefix + '-'), 'destination prefix ' + newId);
  }
}
video.thumbnail.data.shot = sceneIdRemap[video.thumbnail.data.shot] ?? video.thumbnail.data.shot;
const finalSceneByLine = new Map(video.scenes.flatMap((scene) => scene.lines.map((line) => [line.id, scene.id])));
assert.equal(finalSceneByLine.size, video.scenes.reduce((n, scene) => n + scene.lines.length, 0), 'line IDs unique');

// These are proposed source-bound obstacle/action/result arcs, not a numeric
// editorial PASS. A few are voiced as questions; most are carried by action.
// Reviewers must reject any loop whose payoff is already visible or stated.
const loops = [
  { setup: '3rdw', payoff: 'idiy', what: '冷開場沉箱與滑行重機器相撞；Sadow 後來把看見的輪板方法試在行李箱上' },
  { setup: 'b6mn', payoff: 'j9sw', what: '冷開場採購能否接受樣品；Sadow 後來回憶首輪百貨全部拒絕' },
  { setup: 'jtmg', payoff: '3zwf', what: '冷開場機師把箱子帶進車庫，沒有露完成品；後段揭示直立雙輪拉桿的公司記述' },
  { setup: 'r12o01', payoff: 'csdd', what: '安妮塔不願再手提重箱；兒子在出發前拿舊嬰兒車輪改裝' },
  { setup: 'r12o02', payoff: 'r12o03', what: '丈夫取笑家人的輪子箱；安妮塔旅後仍帶它巡講' },
  { setup: 'r14i02', payoff: 'vdxp', what: 'Sadow 對妻子說行李該有輪子；回麻州工廠親手試裝' },
  { setup: 'j9sw', payoff: '76ur', what: '百貨採購拒絕；Macy 副總裁試拉後叫回採購並決定進貨' },
  { setup: 'apb3', payoff: 'ys5y', what: '店內展示人偶示範拉行；Sadow 回憶顧客看懂後接受' },
  { setup: 'iu9y', payoff: 'q4zn', what: 'Plath 看見旅客在安檢卸外置推車；回車庫把推車鎖上硬箱試' },
  { setup: 'q4zn', payoff: 'r13t02', what: 'Plath 把箱與車鎖在一起再到安檢；他回憶安檢員聽到不能卸箱後說好' },
  { setup: 'r15t05', payoff: 'r15t07', what: 'Plath 因舊機組袋做工粗糙而畫改良草圖；後來交給製作者卻被婉拒' },
  { setup: '3zwf', payoff: 'r15n02', what: 'Plath 的一體直立箱成形；同機師看見後請他幫忙製作' },
  { setup: 'r16n01', payoff: 'r16n04', what: 'Samsonite 把疊袋硬箱做成樣品；研究主管回憶停車場障礙試拉結果' },
  { setup: 'r16n06', payoff: 'r16n09', what: '原 Piggyback 大箱不適合客艙；手提款經空服員意見後進店面' },
];
const linePositions = new Map(video.scenes.flatMap((scene, sceneIndex) => scene.lines.map((line) => [line.id, sceneIndex])));
for (const loop of loops) {
  assert.ok(linePositions.has(loop.setup) && linePositions.has(loop.payoff));
  assert.ok(linePositions.get(loop.setup) < linePositions.get(loop.payoff), 'loop ordering ' + loop.setup);
  assert.ok(loop.what.length >= 12, 'loop needs a concrete event description ' + loop.setup);
}
const formerSameShot = video.loops.filter((loop) => loop.setup === 'eghq');
assert.deepEqual(formerSameShot, [{ setup: 'eghq', payoff: 'ys5y', what: '顧客是否接受這種新用法' }]);
const removedOriginalLoops = video.loops.filter((loop) => !loops.some((candidate) => candidate.setup === loop.setup));
video.loops = loops;
assert.equal(video.loops.length, 14);
for (const loop of video.loops) {
  assert.ok(finalSceneByLine.has(loop.setup) && finalSceneByLine.has(loop.payoff), 'loop line exists ' + loop.setup);
  assert.ok(finalSceneByLine.get(loop.setup) !== finalSceneByLine.get(loop.payoff), 'loop payoff not same scene ' + loop.setup);
}
const openingPreviews = video.loops.filter((loop) => finalSceneByLine.get(loop.setup).startsWith('hook-'));
assert.deepEqual(openingPreviews.map((loop) => loop.setup), ['3rdw', 'b6mn', 'jtmg'], 'three distinct unresolved opening actions');
const chapterBoundaryHandoffs = [
  { from: 'hook', to: 'origin', setup: 'x7r4', next_opening: 'r12o01', relation: 'broad everyday-use question begins with the early family obstacle; this is the first case, not the final answer', direct_answer: false },
  { from: 'origin', to: 'idea', setup: '83ew', next_opening: 'r14i01', relation: 'museum-held early case contrasts with Sadow still carrying full cases decades later; independent people, no lineage asserted', direct_answer: false },
  { from: 'idea', to: 'engine', setup: 'zaky', next_opening: 'j9sw', relation: 'Sadow takes his working sample to buyers; their rejection is heard at the next chapter opening', direct_answer: true },
  { from: 'engine', to: 'turn', setup: 'r16e01', next_opening: '8wiw', relation: 'airport security obstruction introduces a different pilot and equipment; the actual cart removal follows two scenes later', direct_answer: false },
  { from: 'turn', to: 'now', setup: 'r15t10', next_opening: 'r15n02', relation: 'Emmer’s later second-bag balance memory hands off to fellow pilots requesting Plath’s case; no causal claim about the strap causing adoption', direct_answer: false },
];
for (const handoff of chapterBoundaryHandoffs) {
  assert.ok(finalSceneByLine.get(handoff.setup)?.startsWith(handoff.from + '-'), 'boundary setup chapter ' + handoff.from);
  assert.ok(finalSceneByLine.get(handoff.next_opening)?.startsWith(handoff.to + '-'), 'boundary next chapter ' + handoff.to);
  assert.ok(linePositions.get(handoff.setup) < linePositions.get(handoff.next_opening), 'boundary order ' + handoff.from);
}

const rawClaimLines = source['claims.md'].toString('utf8').replace(/\r\n/g, '\n').split('\n');
const sourceClaims = new Map(rawClaimLines.filter((row) => /^[a-z]\d+｜/.test(row)).map((row) => {
  const cells = row.split('｜');
  assert.equal(cells.length, 6, 'claims.md row ' + cells[0]);
  return [cells[0], cells];
}));
const claimText = Object.assign({}, ...revisions.map((change) => change.claim_text));
claimText.t7 = 'Travelpro 公司沿革稱，Plath 於 1987 年在車庫製作 Rollaboard；外形在下一鏡示意';
changedClaimIds.add('t7');
const addedClaims = {
  e36: ['e36', 'ABC／USA TODAY 記述 Plath 在安檢看見旅客把行李從外置金屬推車卸下；此事與 Sadow 百貨銷售是獨立事件，不推定因果或技術承襲', 'https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603', '2026-10-18', 'engine-10b', 'PENDING'],
  i34: ['i34', '據 Sadow 回憶，他在四個鋼製舊箱腳輪樣品上綁一條拖繩，箱子便能跟著人滾動', 'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469', '2026-10-18', 'idea-13b', 'PENDING'],
  o29: ['o29', '溫尼特卡歷史學會稱，1928 年女子與孩子拉著輪子箱上街在當時頗奇特；此鏡只展示當時街頭使用，不提前敘述旅後是否繼續', 'https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/', '2026-10-18', 'origin-street', 'PENDING'],
  o30: ['o30', '溫尼特卡歷史學會記載，當時較富裕旅客可付小費讓搬運工與飯店服務生協助行李，而安妮塔一家六口以緊預算長途旅行', 'https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/', '2026-10-18', 'origin-budget', 'PENDING'],
  o31: ['o31', '溫尼特卡歷史學會記載，安妮塔家族為減輕港口、車站和住處之間反覆搬運行李的負擔而改裝輪子箱', 'https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/', '2026-10-18', 'origin-transfer', 'PENDING'],
  i35: ['i35', 'Sadow 回憶，他與妻子和兩個孩子從阿魯巴回程，兩只 27 吋行李箱因孩子的行李而裝得滿滿', 'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469', '2026-10-18', 'idea-memory', 'PENDING'],
  i36: ['i36', 'Sadow 回憶在波多黎各轉機時看見輪板承載重機器，當場對妻子說行李應該有輪子，回程後到工廠實驗', 'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469', '2026-10-18', 'idea-wife', 'PENDING'],
  t30: ['t30', 'ABC／USA TODAY 記述 Plath 在安檢看到行李被綁在外置金屬推車上而須拆開；這與橫拖箱翻倒是不同障礙', 'https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603', '2026-10-18', 'turn-cart-distinction', 'PENDING'],
  t29: ['t29', 'Plath 回憶，安檢員要求他把箱子從推車卸下；他回答無法拆，安檢員只回了一句 OK', 'https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603', '2026-10-18', 'turn-07c', 'PENDING'],
  t31: ['t31', 'Travelpro 公司記述 Plath 於 1987 年設計直立雙輪、可收回拉桿的 Rollaboard；此畫面只作示意，不冒充車庫原型實物', 'https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage', '2026-10-18', 'turn-09b', 'PENDING'],
  n17: ['n17', '2010 年受訪空服員 Heather Poole 觀察，旅客因箱子能滾而塞得更滿，不能滾時可能搬不動', 'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469', '2026-10-18', 'now-05', 'PENDING'],
  t38: ['t38', 'Plath 的 1989 年專利提出一體化登機箱設計，包含可收回把手與箱底凹入的兩個輪子，目的是免去外置推車與反覆拆裝；不主張其與 1987 年車庫原型逐件相同', 'https://patents.google.com/patent/US4995487A/en', '2026-10-18', 'turn-patent-answer', 'PENDING'],
  t35: ['t35', 'Plath 專利把較大型四輪行李箱不適合作客艙手提行李列為既有設計限制，提出可登機的一體箱方案', 'https://patents.google.com/patent/US4995487A/en', '2026-10-18', 'turn-cabin-obstacle', 'PENDING'],
  n28: ['n28', 'ABC／USA TODAY 回顧，航空公司後來調整頭頂置物空間，以容納 22 吋輪子登機箱', 'https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603', '2026-10-18', 'now-overhead', 'PENDING'],
  t33: ['t33', 'Plath 專利背景指出，旅客登機前又須把外置推車上的行李拆下，以便機上收納', 'https://patents.google.com/patent/US4995487A/en', '2026-10-18', 'turn-cart-board', 'PENDING'],
  t34: ['t34', 'Plath 專利背景指出，下機後須再次把行李固定到外置推車，且額外推車本身也成為旅客須管理的物品', 'https://patents.google.com/patent/US4995487A/en', '2026-10-18', 'turn-cart-exit', 'PENDING'],
  t36: ['t36', 'Plath 專利背景稱大型四輪箱太大而須託運，並將晚到、受損或遺失列為託運風險；非證明每件箱子均發生此事', 'https://patents.google.com/patent/US4995487A/en', '2026-10-18', 'turn-cabin-risk', 'PENDING'],
  n34: ['n34', 'Plath 專利描述伸縮拉桿在拉高後以摩擦方式保持伸出位置，並可再受力收回；此鏡提出該設計需求', 'https://patents.google.com/patent/US4995487A/en', '2026-10-18', 'now-handle-risk', 'PENDING'],
  n35: ['n35', 'Plath 專利描述偏心導件使伸縮桿在伸出時壓向套筒，以摩擦保持位置；向下施力可解除並收回', 'https://patents.google.com/patent/US4995487A/en', '2026-10-18', 'now-handle-release', 'PENDING'],
  n36: ['n36', 'Plath 專利提出可拆掛件以讓另一件行李隨一體式登機箱攜帶；此為設計主張而非市售功能證據', 'https://patents.google.com/patent/US4995487A/en', '2026-10-18', 'now-piggyback', 'PENDING'],
  n37: ['n37', 'Plath 專利的雙輪箱須傾斜，才會以輪子承重', 'https://patents.google.com/patent/US4995487A/en', '2026-10-18', 'now-era-bridge', 'PENDING'],
  n38: ['n38', 'Plath 專利的可拆附件方案主張可讓箱子以平衡方式攜帶最多四件行李；這是專利設計主張，不代表市售實測容量', 'https://patents.google.com/patent/US4995487A/en', '2026-10-18', 'now-piggyback-limit', 'PENDING'],
  n39: ['n39', 'Samsonite 公司招股文件稱 1997 年推出可站立推動的四輪直立箱；此句用作下一鏡的設計問題橋接', 'https://corporate.samsonite.com/on/demandware.static/-/Sites-InvestorRelations-Library/default/dwa68533ea/PDF/announcements/2011/20110602100852_Samsonite_Final_Prospectus_en.pdf', '2026-10-18', 'now-era-bridge', 'PENDING'],
  t39: ['t39', '同機組機師 Bill Emmer 於 2016 年第一人稱回憶 Plath 的另一段輪子袋設計經過；本文未標出該段事件年份或與安檢經歷的先後', emmerUrl, '2026-10-18', 'turn-emmer-01', 'PENDING'],
  t40: ['t40', 'Emmer 回憶機組在 Plath 改良前已使用 Jet Eze 直立輪子袋，空服員也在使用；不是 Plath 首創機組輪子袋', emmerUrl, '2026-10-18', 'turn-emmer-02', 'PENDING'],
  t41: ['t41', 'Emmer 回憶一些男機師因擔心被看輕而仍選擇手提行李，此為他的觀察而非所有機師的行為', emmerUrl, '2026-10-18', 'turn-emmer-03', 'PENDING'],
  t42: ['t42', 'Emmer 回憶 Plath 喜歡 Jet Eze 上層拉鍊格，能方便取用鑰匙、眼鏡與錢包', emmerUrl, '2026-10-18', 'turn-emmer-04', 'PENDING'],
  t43: ['t43', 'Emmer 回憶 Plath 認為 Jet Eze 做工粗糙，曾畫出改良輪子袋的草圖', emmerUrl, '2026-10-18', 'turn-emmer-05', 'PENDING'],
  t44: ['t44', 'Emmer 回憶 Plath 在西雅圖航站遇到 Jet Eze 製作者 Moon Mullins，向他展示改良草圖', emmerUrl, '2026-10-18', 'turn-emmer-06', 'PENDING'],
  t45: ['t45', 'Emmer 回憶隔週 Moon 尚未與合夥人商議，再隔一週回覆不感興趣；不是正式百貨採購拒絕', emmerUrl, '2026-10-18', 'turn-emmer-07', 'PENDING'],
  t46: ['t46', 'Emmer 回憶草圖未被 Moon 接受後 Plath 繼續自行發展設計；其時間與安檢經歷的先後未明', emmerUrl, '2026-10-18', 'turn-emmer-08', 'PENDING'],
  t47: ['t47', 'Emmer 回憶較早輪子袋頂部承載第二件飛行袋時容易前傾，為機組攜物時的具體平衡障礙', emmerUrl, '2026-10-18', 'turn-balance-01', 'PENDING'],
  t48: ['t48', 'Emmer 回憶 Plath 後來以可調掛帶與掛鉤讓第二件飛行袋掛得更低且較穩；不主張所有市售箱型均具備', emmerUrl, '2026-10-18', 'turn-balance-02', 'PENDING'],
  n44: ['n44', 'Joe Sharkey 2010 年《紐約時報》文章回顧，旅客在航站見空服員拉著 Rollaboard 快步走，產生一般旅客市場；此文重印於 RNPA 2016 Contrails p.48，與 Emmer p.46–47 回憶是不同作者', emmerUrl, '2026-10-18', 'now-passenger', 'PENDING'],
  o32: ['o32', '溫尼特卡歷史學會記載，1928 至 1930 年第二次環遊期間安妮塔與兩名女兒沿途以畫作換餐食或住宿；行李仍伴隨旅程，不能推論為某站特定交易', anitaBackgroundUrl, '2026-10-18', 'origin-sketches', 'PENDING'],
  n45: ['n45', 'Travelpro 當時執行長 Kim Ballis 於 2007 年受訪回憶，其他機師看到 Plath 使用輪子箱後請他替自己製作；訪談年份表述與公司史 1987 原型時間不同，不據此推算確切事件年份', crewInterviewUrl, '2026-10-18', 'now-crew-request', 'PENDING'],
  n46: ['n46', 'Samsonite 研究主管 Bob Bengen 於 1992 年回顧，公司在 1986 年擔心硬殼行李箱偏好下降；敘事從 Plath 1991 年主線明確倒回另一家公司 1986 年，不稱該年首創 Piggyback', samsoniteResearchUrl, '2026-10-18', 'now-sam-01', 'PENDING'],
  n47: ['n47', 'Bengen 回顧 Piggyback 疊放行李概念的探索早於 1986 年，後來做成可承載另一袋的硬殼輪子箱樣品；不宣稱源於 Plath', samsoniteResearchUrl, '2026-10-18', 'now-sam-02', 'PENDING'],
  n48: ['n48', 'Bengen 回顧 1987 年公司人員含總裁在停車場以路緣、淺溝、碎石路測試 Piggyback 正式樣品', samsoniteResearchUrl, '2026-10-18', 'now-sam-03', 'PENDING'],
  n49: ['n49', 'Bengen 自述 Samsonite 內部人員試拉 Piggyback 後認為移動穩定且能在箱頂攜帶另一袋；這是公司內部正面回顧，非獨立實測結果', samsoniteResearchUrl, '2026-10-18', 'now-sam-04', 'PENDING'],
  n50: ['n50', 'Bengen 記述 Samsonite 於 1988 年行李展以停車場式障礙路線讓參觀者試拉 Piggyback，並自述反應正面；非量化市場資料', samsoniteResearchUrl, '2026-10-18', 'now-sam-05', 'PENDING'],
  n51: ['n51', 'Bengen 指原先全尺寸 Piggyback 不適合作客艙手提，較小型需能進狹窄走道與多數不同頭頂置物櫃；非所有航班或所有箱型規範', samsoniteResearchUrl, '2026-10-18', 'now-sam-06', 'PENDING'],
  n52: ['n52', 'Bengen 記述 1988 年公司請空服員小組談手提行李；他們表示外加推車不受歡迎、客艙空間受限、置物櫃尺寸不一', samsoniteResearchUrl, '2026-10-18', 'now-sam-07', 'PENDING'],
  n53: ['n53', 'Bengen 記述 1988 年空服員小組討論時手提款原型已存在；公司其後讓篩選受訪者實際推、提與檢視樣品，並據意見修訂；不是小組後才縮小原箱或全體旅客實測', samsoniteResearchUrl, '2026-10-18', 'now-sam-08', 'PENDING'],
  n54: ['n54', 'Bengen 記述 Piggyback 手提箱修訂後量產，於 1990 年進入美國行李店面；與 Rollaboard 或 1997 年 Spinner 無因果聲稱', samsoniteResearchUrl, '2026-10-18', 'now-sam-09', 'PENDING'],
};
const finalClaimScene = new Map(video.scenes.flatMap((scene) => (scene.claims ?? []).map((id) => [id, scene.id])));
assert.equal(finalClaimScene.size, video.scenes.reduce((n, scene) => n + (scene.claims ?? []).length, 0), 'final claim IDs unique');
const inverseClaimIdRemap = Object.fromEntries(Object.entries(claimIdRemap).map(([oldId, newId]) => [newId, oldId]));
const claims = ['# 主張表：輪子行李箱：有了輪子，為什麼還等了這麼久？', '', '這是離線候選稿的逐句來源表；搬章與改寫的主張均待獨立審稿。', ''];
for (const chapter of chapterLayout) {
  claims.push('## ' + chapter.title + '（' + chapter.prefix + '）', '');
  const scenes = video.scenes.filter((scene) => scene.id.startsWith(chapter.prefix + '-'));
  for (const scene of scenes) {
    for (const id of scene.claims ?? []) {
      const oldId = inverseClaimIdRemap[id] ?? id;
      const sourceCells = addedClaims[id] ?? sourceClaims.get(oldId);
      assert.ok(sourceCells, 'missing claim source row ' + id);
      const cells = [...sourceCells];
      if (claimText[oldId]) cells[1] = claimText[oldId];
      if (id === 'h2') cells[2] = series.plan.sources[5].url;
      if (id === 'e9') cells[2] = series.plan.sources[1].url;
      cells[0] = id;
      cells[4] = scene.id;
      // The whole reordered candidate needs a fresh independent verdict;
      // snapshot-104 CONFIRMED labels are historical, not portable receipts.
      cells[5] = 'PENDING';
      claims.push(cells.join('｜'));
    }
  }
  claims.push('');
}
assert.deepEqual(new Set(claims.filter((row) => /^[a-z]\d+｜/.test(row)).map((row) => row.split('｜', 1)[0])), new Set(finalClaimScene.keys()), 'claims rows exactly cover final scenes');
const claimsMarkdown = Buffer.from(claims.join('\n'));

const module = (relative) => import(pathToFileURL(path.join(repo, relative)));
const [{ screenplay }, { estimateTimeline, spokenUnits }, { lintVideo }, { hookCadenceProblems }, { cuteStoryVisualProblems }] = await Promise.all([
  module('tools/video/core/screenplay.mjs'),
  module('tools/video/core/timeline.mjs'),
  module('tools/video/core/lint.mjs'),
  module('tools/video/core/narrative.mjs'),
  module('tools/video/automation/story.mjs'),
]);
assert.equal(screenplay(JSON.parse(source['video.json'].toString('utf8'))), source['script.md'].toString('utf8').replace(/\r\n/g, '\n'), 'baseline screenplay mismatch');
const script = Buffer.from(screenplay(video));
const lint = lintVideo(video, {
  lexicon: candidateLexicon,
  brief: source['brief.md'].toString('utf8'),
  translations: {}, others: [], series,
});
const cute = cuteStoryVisualProblems(video);
const cadence45 = (timeline, includeActionLed) => {
  const from = timeline.chapters[1].start_frame / 30;
  const outro = video.scenes.find((scene) => scene.template === 'outro');
  const to = timeline.scenes.find((scene) => scene.id === outro.id).start_frame / 30;
  const bodyFirstIndex = video.scenes.findIndex((scene) => scene.id === timeline.chapters[1].scene);
  const outroIndex = video.scenes.findIndex((scene) => scene.id === outro.id);
  assert.ok(bodyFirstIndex > 0 && outroIndex > bodyFirstIndex, 'body scene bounds');
  const bodySceneIds = new Set(video.scenes.slice(bodyFirstIndex, outroIndex).map((scene) => scene.id));
  const sceneByLine = new Map(video.scenes.flatMap((scene) => scene.lines.map((line) => [line.id, scene.id])));
  const timelineByLine = new Map(timeline.lines.map((line) => [line.id, line]));
  // The first report counts only explicit voiced questions. The second is an
  // *unreviewed event proxy* across declared obstacle/action/result arcs.
  // Neither report proves that a visual or prior line has not spoiled a loop.
  const events = video.loops.flatMap((loop) => {
    const setup = timelineByLine.get(loop.setup);
    const payoff = timelineByLine.get(loop.payoff);
    assert.ok(setup && payoff, 'missing cadence loop ' + loop.setup);
    if (!bodySceneIds.has(sceneByLine.get(loop.setup))) return [];
    if (sceneByLine.get(loop.setup) === sceneByLine.get(loop.payoff)) return [];
    assert.ok(setup.end_frame <= payoff.start_frame, 'non-later cadence payoff ' + loop.setup);
    const spoken = video.scenes.flatMap((scene) => scene.lines).find((line) => line.id === loop.setup).text;
    if (!includeActionLed && !/[？?]\s*$/.test(spoken)) return [];
    const at = setup.end_frame / 30;
    return at >= from && at < to ? [{ at, id: loop.setup, payoff: loop.payoff }] : [];
  });
  const points = [{ at: from, id: 'body:start' }, ...events.sort((a, b) => a.at - b.at), { at: to, id: 'body:end' }];
  const gaps = points.slice(1).map((point, index) => ({
    from: points[index].id,
    to: point.id,
    seconds: Number((point.at - points[index].at).toFixed(1)),
  }));
  return {
    counted_rule: includeActionLed
      ? 'UNREVIEWED PROXY: declared source-bound action or explicit question with later payoff in a different scene; requires independent anti-spoiler narrative and visual review'
      : 'declared explicit question with later payoff in a different scene; point is spoken line end; no chapter boundaries or arbitrary questions',
    max_gap_seconds: Math.max(...gaps.map((gap) => gap.seconds)),
    gaps_over_45_seconds: gaps.filter((gap) => gap.seconds > 45),
    devices: points,
  };
};
const timing = {};
for (const cpm of [250, 275, 300]) {
  const timeline = estimateTimeline(video, cpm);
  const original = estimateTimeline(JSON.parse(source['video.json'].toString('utf8')), cpm);
  const starts = new Map(timeline.lines.map((line) => [line.id, line.start_frame / 30]));
  const shots = new Map(timeline.scenes.map((scene) => [scene.id, (scene.end_frame - scene.start_frame) / 30]));
  const outroScene = video.scenes.find((scene) => scene.template === 'outro');
  const outroStart = timeline.scenes.find((scene) => scene.id === outroScene.id).start_frame / 30;
  const bodyStart = timeline.chapters[1].start_frame / 30;
  timing[cpm] = {
    baseline_seconds: Number((original.total_frames / 30).toFixed(1)),
    candidate_seconds: Number((timeline.total_frames / 30).toFixed(1)),
    opening_seconds: Number((timeline.chapters[1].start_frame / 30).toFixed(1)),
    middle_between_opening_and_outro_seconds: Number((outroStart - bodyStart).toFixed(1)),
    outro_narration_seconds: Number((timeline.total_frames / 30 - outroStart).toFixed(1)),
    six_chapter_narration_seconds: timeline.chapters.map((chapter, index) => ({
      scene_id: chapter.scene,
      seconds: Number((((timeline.chapters[index + 1]?.start_frame ?? timeline.total_frames) - chapter.start_frame) / 30).toFixed(1)),
    })),
    opening_first_30_scene_ids: timeline.scenes.filter((scene) => scene.start_frame < 30 * 30).map((scene) => scene.id),
    opening_board_reveal_line_start_seconds: Number(starts.get('avqs').toFixed(1)),
    opening_first_contrast_line_start_seconds: Number(starts.get('3rdw').toFixed(1)),
    scene_estimated_seconds: timeline.scenes.map((scene) => ({ scene_id: scene.id, seconds: Number(((scene.end_frame - scene.start_frame) / 30).toFixed(1)) })),
    opening_preview_payoff_gaps_seconds: openingPreviews.map((loop) => ({ setup: loop.setup, payoff: loop.payoff, seconds: Number((starts.get(loop.payoff) - (timeline.lines.find((line) => line.id === loop.setup).end_frame / 30)).toFixed(1)) })),
    declared_loop_payoff_gaps_seconds: video.loops.map((loop) => ({ setup: loop.setup, payoff: loop.payoff, seconds: Number((starts.get(loop.payoff) - (timeline.lines.find((line) => line.id === loop.setup).end_frame / 30)).toFixed(1)) })),
    chapter_boundary_line_gaps_seconds: chapterBoundaryHandoffs.map((handoff) => ({ from: handoff.from, to: handoff.to, seconds: Number((starts.get(handoff.next_opening) - (timeline.lines.find((line) => line.id === handoff.setup).end_frame / 30)).toFixed(1)), direct_answer: handoff.direct_answer })),
    hook_line_starts_seconds: Object.fromEntries(revisions.map((item) => [item.line, Number(starts.get(item.line).toFixed(1))])),
    changed_line_seconds: Object.fromEntries(revisions.map((item) => {
      const line = timeline.lines.find((entry) => entry.id === item.line);
      return [item.line, Number(((line.end_frame - line.start_frame) / 30).toFixed(1))];
    })),
    target_shot_seconds: Object.fromEntries(revisions.map((item) => {
      const sceneId = sceneIdRemap[item.scene] ?? item.scene;
      return [sceneId, Number(shots.get(sceneId).toFixed(1))];
    })),
    shot_over_8_seconds: timeline.scenes.filter((scene) => (scene.end_frame - scene.start_frame) / 30 > 8).map((scene) => scene.id),
    cadence_45_seconds: cadence45(timeline, false),
    proposed_action_event_cadence_not_a_pass: cadence45(timeline, true),
    legacy_lint_hook_cadence_90_second_warnings: hookCadenceProblems(video, timeline),
  };
}
const sourceMap = {
  status: 'PENDING_INDEPENDENT_REVIEW',
  supersedes_manifest_sha256: 'A391F721CBA58896E8E9C9ED2F20C2794C587AE61C8E07C379DBD85518585F42',
  prior_review_snapshot: 'review-baseline-A391F721/review-notes.md',
  source_snapshot: 'snapshot-104',
  source_tip_sha256: sourceTip,
  sources: series.plan.sources.map((item, index) => ({ index, url: item.url, checked_on: item.checked })),
  supplemental_sources: [
    { url: emmerUrl, location: 'Bill Emmer, Manly Men Didn’t Use Wheelies!, Contrails August 2016, printed pp. 46–47', checked_on: '2026-10-18', role: 'first-person later memoir; no fixed year or sequence relative to Plath security recollection' },
    { url: emmerUrl, location: 'Joe Sharkey, Reinventing the Suitcase by Adding the Wheel, New York Times 2010 article reprinted in Contrails August 2016 p. 48', checked_on: '2026-10-18', role: 'separate reporter retrospect on travelers seeing flight attendants in terminals; no passenger dialogue in this source' },
    { url: anitaBackgroundUrl, location: 'Winnetka Historical Society, Who Were the Burnhams?, second world trip', checked_on: '2026-10-18', role: 'museum account of sketches exchanged for food or lodging, no invented specific transaction' },
    { url: crewInterviewUrl, location: 'Global Traveler, Kim Ballis interview, September 2007, question one', checked_on: '2026-10-18', role: 'then-CEO recollection of fellow pilots requesting a case; interview date math conflicts with Travelpro 1987 and is not used to date the event' },
    { url: samsoniteResearchUrl, location: 'Bob Bengen, Samsonite marketing research director, Quirks 1992, Development/Model Tested/Distinct Criteria/Well Received', checked_on: '2026-10-18', role: 'first-party company account of a separate Piggyback line; parking-lot trial, carry-on research and 1990 retail, not independent sales proof or a Rollaboard/Spinner causal chain' },
  ],
  changed_lines: revisions.map((change) => ({
    source_scene_id: change.scene, scene_id: sceneIdRemap[change.scene] ?? change.scene,
    line_id: change.line, previous_text: change.before, candidate_text: change.after,
    source_claim_ids: change.claims, claim_ids: change.claims.map((id) => claimIdRemap[id] ?? id),
    source_pins: change.sources.map((pin) => ({ ...pin, url: series.plan.sources[pin.index].url })),
    payoff_line_id: change.payoff, editorial_payoff: change.reason, verdict: 'PENDING_INDEPENDENT_REVIEW',
  })),
  changed_visuals: visualRevisions.map((change) => ({ source_scene_id: change.scene, scene_id: sceneIdRemap[change.scene] ?? change.scene, previous_prompt: change.before, candidate_prompt: change.after, editorial_reason: change.reason, verdict: 'PENDING_IMAGE_AND_SOURCE_REVIEW' })),
  added_scenes: [
    { scene_id: familyStreetScene.id, line_id: familyStreetScene.lines[0].id, claim_id: familyStreetScene.claims[0], candidate_text: familyStreetScene.lines[0].text, candidate_prompt: familyStreetScene.data.prompt, source_pin: { url: series.plan.sources[8].url, location: 'Winnetka Historical Society, Before Her Time, wheeled suitcase would have been an unusual sight', role: 'museum interpretation only; do not depict observed bystander response or later-use outcome' }, verdict: 'PENDING_INDEPENDENT_SOURCE_AND_IMAGE_REVIEW' },
    { scene_id: splitPrototypeScene.id, line_id: 'idiy', claim_id: 'i34', candidate_text: splitPrototypeScene.lines[0].text, candidate_prompt: splitPrototypeScene.data.prompt, source_pin: { url: series.plan.sources[6].url, location: 'ABC News 2010, four steel trunk casters and a pulling rope on Sadow’s first prototype', role: 'attributed prototype action' }, verdict: 'PENDING_INDEPENDENT_SOURCE_AND_IMAGE_REVIEW' },
    { scene_id: addedScene.id, line_id: 'opk01', claim_id: 'n17', candidate_text: addedScene.lines[0].text, candidate_prompt: addedScene.data.prompt, source_pin: { url: series.plan.sources[6].url, location: 'ABC News 2010, flight attendant Heather Poole on overpacked rolling bags', role: 'attributed observation, not measured prevalence' }, verdict: 'PENDING_INDEPENDENT_SOURCE_AND_IMAGE_REVIEW' },
    { scene_id: guardResponseScene.id, line_id: 'r13t02', claim_id: 't29', candidate_text: guardResponseScene.lines[0].text, candidate_prompt: guardResponseScene.data.prompt, source_pin: { url: series.plan.sources[5].url, location: 'ABC/USA TODAY 2012, Plath recalls the guard replying OK after he said the screwed-on case could not be removed', role: 'reported recollection, not an independently verified clearance record' }, verdict: 'PENDING_INDEPENDENT_SOURCE_AND_IMAGE_REVIEW' },
    { scene_id: turnRevealScene.id, line_id: '3zwf', claim_id: 't31', candidate_text: turnRevealScene.lines[0].text, candidate_prompt: turnRevealScene.data.prompt, source_pin: { url: series.plan.sources[1].url, location: 'Travelpro company history of the 1987 upright two-wheel retractable-handle Rollaboard form', role: 'company account, shown as illustrative design not a garage-prototype photograph' }, verdict: 'PENDING_INDEPENDENT_SOURCE_AND_IMAGE_REVIEW' },
    { scene_id: overheadScene.id, line_id: 'r13n01', claim_id: 'n28', candidate_text: overheadScene.lines[0].text, candidate_prompt: overheadScene.data.prompt, source_pin: { url: series.plan.sources[5].url, location: 'ABC/USA TODAY 2012 retrospective on airlines reconfiguring overhead bins for 22-inch wheeled carry-ons', role: 'retrospective consequence without precise date or adoption rate' }, verdict: 'PENDING_INDEPENDENT_SOURCE_AND_IMAGE_REVIEW' },
    ...addedStoryScenes.map((scene) => ({
      scene_id: scene.id, line_id: scene.lines[0].id, claim_ids: scene.claims,
      candidate_text: scene.lines[0].text, candidate_prompt: scene.data.prompt,
      source_pins: scene.claims.map((id) => ({ url: addedClaims[id][2], location: addedClaims[id][1], role: 'claim-specific source; narration and picture remain pending independent review' })),
      verdict: 'PENDING_INDEPENDENT_SOURCE_AND_IMAGE_REVIEW',
    })),
    ...[anitaSketchScene, ...emmerScenes, emmerPassengerScene, crewRequestScene, retailToSecurityScene, ...samsoniteScenes].map((scene) => ({
      scene_id: scene.id, line_id: scene.lines[0].id, claim_ids: scene.claims,
      candidate_text: scene.lines[0].text, candidate_prompt: scene.data.prompt,
      source_pins: scene.claims.map((id) => ({ url: addedClaims[id][2], location: addedClaims[id][1], role: 'claim-specific source; narrated identity may be omitted for untested TTS pronunciation but attribution remains in the beat and evidence' })),
      verdict: 'PENDING_INDEPENDENT_SOURCE_AND_IMAGE_REVIEW',
    })),
  ],
  chapter_migration: {
    status: 'SPEC_ONLY_FORMAL_HOST_CHAPTER_SOURCE_MIGRATION_REQUIRED',
    order: chapterLayout.map((chapter) => ({ prefix: chapter.prefix, first_source_scene: chapter.ids[0], first_candidate_scene: sceneIdRemap[chapter.ids[0]] ?? chapter.ids[0], title: chapter.title })),
    scene_id_old_to_new: sceneIdRemap,
    claim_id_old_to_new: claimIdRemap,
    stable_line_ids: true,
    thumbnail_candidate_shot: video.thumbnail.data.shot,
    loop_line_ids: video.loops,
    reason: 'host composes six chapter JSON containers in fixed order and assigns seconds/claim numbering by destination prefix; a merged video.json is not an installable host source',
  },
  series_plan_migration: {
    status: 'SPEC_ONLY_REVIEW_HOST_PLAN_AND_SIX_CHAPTER_SOURCES_BEFORE_INSTALL',
    base_series_sha256: baseSha['series.json'],
    candidate_series_sha256: sha(json(series)),
    candidate_lexicon_sha256: sha(json(candidateLexicon)),
    chapter_keys: series.plan.chapters.map((chapter) => chapter.key),
    changed_fields: ['logline', 'plan.question', 'plan.chapters', 'plan.takeaway', 'plan.must_verify', 'plan.names', 'plan.image_notes', 'plan.caveats', 'characters.voice.style'],
    reason: 'the frozen base series plan contradicts the reordered candidate and cannot be reused as host source',
  },
  retired_candidate_scenes: ['origin-transfer', 'turn-cart-board', 'turn-cart-exit', 'turn-cabin-obstacle', 'turn-patent-answer', 'now-era-bridge', 'turn-emmer-02', 'turn-emmer-04', 'turn-emmer-06', 'turn-emmer-08', 'now-sam-02', 'now-sam-05', 'now-sam-08'],
  removed: { scene_id: 'turn-08', line_id: '6i8x', claim_id: 't19', basis: 'frozen round12 one-scene cut only' },
  removed_story_scenes: removedScenes,
  other_removed_lines: [
    { scene_id: 'idea-01', line_id: 'ugak', claim_id: 'i19', basis: 'specific Macy’s rejection repeats the already spoken all-buyers refusal; the later turnaround names the store' },
    { scene_id: 'hook-03', line_id: '6h2q', claim_id: null, basis: 'the title and visible wheel board already make the adaptation answer obvious; keep the concrete contrast and later retail obstacle' },
    { scene_id: 'idea-10', line_id: 'eghq', claim_id: null, basis: 'same-shot question or filler immediately before Sadow’s answer' },
    { scene_id: 'turn-12', line_id: '3tsp', claim_id: null, basis: 'passenger adoption is now spoken in turn-10b/ewj7 before the patent detour; t12 claim moved there' },
    { scene_id: 'idea-06', line_id: '4qtf', claim_id: 'i6', basis: 'buyer action follows the VP demonstration naturally without an immediate-answer question' },
    { scene_id: 'engine-01', line_id: 'gtab', claim_id: null, basis: 'terminal growth is already established in the preceding line' },
    { scene_id: 'idea-10', line_id: 'quhs', claim_id: null, basis: 'precise sales count caveat interrupted the bridge; claims still do not assert a sales number' },
    { scene_id: 'now-01', line_id: 'kfiw', claim_id: 'n2', basis: 'second four-wheel feature line is redundant after the four-wheel introduction' },
  ],
  chapter_titles: chapterLayout.map((chapter) => ({ first_scene_id: sceneIdRemap[chapter.ids[0]] ?? chapter.ids[0], title: chapter.title, basis: 'chapter marks only the first scene, without spoiling the outcome' })),
  removed_same_shot_loop: formerSameShot[0],
  removed_original_loops: removedOriginalLoops,
  opening_three_unresolved_actions: openingPreviews.map((loop) => ({ setup_line_id: loop.setup, payoff_line_id: loop.payoff, source_bound_event: loop.what, visual_anti_spoiler_review: 'PENDING' })),
  chapter_boundary_handoffs: chapterBoundaryHandoffs,
  action_obstacle_payoffs_for_human_review: loops.map((loop) => {
    const spoken = video.scenes.flatMap((scene) => scene.lines).find((line) => line.id === loop.setup).text;
    return { obstacle: loop.setup, action_or_result: loop.payoff, story_event: loop.what, counted_by_explicit_question_cadence: /[？?]\s*$/.test(spoken), verdict: 'PENDING_INDEPENDENT_NARRATIVE_AND_VISUAL_ANTI_SPOILER_REVIEW' };
  }),
  caveats: [
    'Winnetka official page was accessible in the 2026-10-18 web search and directly supports the family-budget, transfer-route, unusual-street-sight and retained-object details; the 1933 travelogue pages remain unread directly.',
    'Anita 1933 travelogue pages have not been read directly; husband and lecture details remain attributed to Winnetka Historical Society.',
    'Travelpro crew-to-passenger sequence is the company account, not independent adoption data.',
    'Patent US3653474A describes a proposed design; its parts must not be represented as an observed retail specimen.',
    'Plath security exchange is his reported recollection, not an independently verified airport record.',
    'The new Plath patent beats describe the inventor’s stated design and background, not production specifications of every sold Rollaboard.',
    'The security-cart disassembly and oversize four-caster carry-on problem are different prior-art obstacles in US4995487A; neither should be visually collapsed into the other.',
    'Emmer’s Jet Eze crew bag was already in crew use and is not Plath’s separate security trolley or proof Plath invented crew wheeled bags; the memoir gives no year or ordering relative to the security anecdote.',
    'Emmer’s old-bag top-pocket, maker conversation, pilot stigma and lower bag-support account are one colleague’s retrospective testimony, not independently measured adoption or a specification for every sold unit.',
    'The 2007 Travelpro CEO interview supplies a specific peer-request action but implies a different invention year than Travelpro’s later 1987 history; this candidate deliberately does not use it to date the event.',
    'The 1992 Samsonite research-director case study is a first-party retrospective on the separate Piggyback line; favorable internal and exhibition reactions are attributed, not independently measured adoption, and it has no asserted influence on Rollaboard or Spinner.',
    'The 1986 screening already included external respondents and use-based evaluation before the 1987 internal parking-lot course; the 1988 trade show was not the first outside test. A carry-on prototype already existed before the 1988 flight-attendant focus groups; the groups did not cause the first downsizing.',
    'Winnetka calls the 1928 street sight unusual but does not record passersby turning to look; the candidate depicts no witnessed bystander reaction.',
    'The declared loops are candidate action arcs, not independently judged retention beats. Any setup revealed early by a still or obvious prior line must be excluded by the next reviewer.',
    'The 1989 patent is explicitly a later filing used to explain Plath’s prior obstacles; it is not claimed to be a photo or exact bill of materials for the 1987 garage Rollaboard.',
    'The airline overhead-bin consequence is a retrospective report without a precise installation chronology; its placement is thematic after passenger adoption.',
    `The six-chapter static estimate at 300 Chinese units per minute is ${timing[300].candidate_seconds} seconds, below the formal 540-second lower bound; no real TTS has been measured and no slow playback or unsupported filler is allowed to close the deficit.`,
    'Only the idea-to-engine boundary has an immediate direct answer. Other chapter boundaries are obstacle continuations or independent-person handoffs, not falsely labeled as closed questions.',
    'A six-chapter host source migration with scene and claim remap needs separate review; this merged offline candidate does not authorize installation.',
  ],
};
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_UNREVIEWED',
  source_snapshot: 'snapshot-104',
  source_tip_sha256: sourceTip,
  removed_scene_line_claim: ['turn-08', '6i8x', 't19'],
  removed_story_scenes: removedScenes,
  other_removed_line_ids: ['6h2q', 'ugak', 'eghq', '3tsp', '4qtf', 'gtab', 'quhs', 'kfiw'],
  moved_claim_ids: [
    { id: 'h2', from_scene: 'hook-02', to_scene: 'idea-12', candidate_id: 'i37', line_id: 'vdxp' },
    { id: 'e25', from_scene: 'engine-r12-07', to_scene: 'idea-r12-06', candidate_id: 'i33', line_id: 'r12e06' },
  ],
  retired_claim_ids: ['t12'],
  chapter_migration: sourceMap.chapter_migration,
  series_plan_migration: sourceMap.series_plan_migration,
  supersedes_manifest_sha256: sourceMap.supersedes_manifest_sha256,
  changed_line_ids: revisions.map((item) => item.line),
  changed_visual_scene_ids: visualRevisions.map((item) => sceneIdRemap[item.scene] ?? item.scene),
  added_scene_ids: [familyStreetScene.id, splitPrototypeScene.id, addedScene.id, guardResponseScene.id, turnRevealScene.id, overheadScene.id, ...addedStoryScenes.map((scene) => scene.id), anitaSketchScene.id, ...emmerScenes.map((scene) => scene.id), emmerPassengerScene.id, crewRequestScene.id, retailToSecurityScene.id, ...samsoniteScenes.map((scene) => scene.id)],
  added_claim_ids: ['o29', 'i34', 't29', 't31', 'n17', 'n28', ...addedStoryScenes.flatMap((scene) => scene.claims), 'o32', ...emmerScenes.flatMap((scene) => scene.claims), 'n44', 'n45', 'e36', ...samsoniteScenes.flatMap((scene) => scene.claims)],
  changed_claim_ids: [...changedClaimIds].map((id) => claimIdRemap[id] ?? id),
  added_loops: loops,
  removed_same_shot_loop: formerSameShot[0],
  removed_original_loops: removedOriginalLoops,
  total_loops: video.loops.length,
  opening_three_unresolved_actions: sourceMap.opening_three_unresolved_actions,
  chapter_boundary_handoffs: chapterBoundaryHandoffs,
  scenes: video.scenes.length,
  lines: video.scenes.reduce((sum, scene) => sum + scene.lines.length, 0),
  narration_spoken_units: video.scenes.flatMap((scene) => scene.lines).reduce((sum, line) => sum + spokenUnits(line.text), 0),
  narration_characters_including_punctuation: [...video.scenes.flatMap((scene) => scene.lines).map((line) => line.text).join('')].length,
  max_changed_line_spoken_units: Math.max(...revisions.map((item) => spokenUnits(item.after))),
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_warnings: lint.warnings,
  cute_visual_errors: cute,
  estimated_timing_not_tts: timing,
  independent_fact_review: 'NOT_RUN',
  independent_listener_review: 'NOT_RUN',
  independent_narrative_panel: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  actual_tts_or_media: 'NOT_RUN',
};
const output = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', json(series)],
  ['candidate/lexicon.json', json(candidateLexicon)],
  ['candidate/script.md', script],
  ['candidate/claims.md', claimsMarkdown],
  ['source-map.json', json(sourceMap)],
  ['validation.json', json(validation)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  supersedes_manifest_sha256: sourceMap.supersedes_manifest_sha256,
  prior_review_snapshot: sourceMap.prior_review_snapshot,
  slug: video.slug,
  source_snapshot: 'A01-20261017-afternoon-fe35369c/snapshot-104',
  source_tip_sha256: sourceTip,
  base_sha256: baseSha,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...output].map(([name, bytes]) => [name, sha(bytes)])),
  frozen_round12_driver_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
output.set('manifest.json', json(manifest));

const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of output) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep));
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), 'missing generated ' + name);
    assert.ok(fs.readFileSync(file).equals(bytes), 'stale generated ' + name);
  }
}
assert.equal(lint.errors.length, 0, 'video lint errors');
assert.equal(cute.length, 0, 'cute visual errors');
// A cadence gap remains a review finding. Rewriting chronology to satisfy a
// numeric threshold with fact-free quiz lines would misrepresent the story.
for (const item of Object.values(timing)) {
  for (const seconds of Object.values(item.changed_line_seconds)) assert.ok(seconds <= 8, 'changed line above eight-second target');
}
console.log(JSON.stringify({
  action, status: validation.status, scenes: validation.scenes, lines: validation.lines,
  seconds_250: timing[250].candidate_seconds, seconds_275: timing[275].candidate_seconds,
  seconds_300: timing[300].candidate_seconds, lint_errors: lint.errors.length,
  lint_warnings: lint.warnings.length, cute_errors: cute.length,
}));
