// A01 r44: create-only offline alternate. Never writes r43, approved plans or production.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { URL, beats, chapters, visual } from './story-data.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r43 = path.join(here, 'reference/r43');
const r43Sha = 'be7fc07bba7dd6f1d4851399a9d46e36afab8fbf438d3a7bba7a2e9473201ced';
const r43StoryReviewSha = 'c5858c317176f3a1b66cc200fecb51c3f1e32092463ffd9adc13c7edf7775958';
const r43SourceReviewSha = '0cb1cf80c5360144e63badac92958a00a876420defb68d693ce62592777320e5';
const r43VisualReviewSha = 'c2cd8ef92f064b695be48aa96729b144b3a22a415c0e46c54ba2c2c4eea02e14';
const baseline104 = {
  id: 'A01-20261017-afternoon-fe35369c/snapshot-104',
  source_sha256: 'e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7',
  index_manifest_sha256: 'eb22c3ef4bb0254618d7a3f06c1840ec2c6564a0baec02930e1b46b25f7d4ccd',
  tip_index_sha256: 'f2628d894d6907f64733325581e0116c1d7b297b45fec0d9d63c4aff82d09288',
  meaning: 'Historical 104-event baseline only; not a fresh host readback or approval.',
};
const baselineReadbackSha = '425107765c8a2371aad3a3ac6e31496a82e204bf5a8048782c025f9dc955124b';
// Raw review/readback hashes above remain historical provenance. Only local paths
// were redacted in the packaged copies; these hashes bind the portable file bytes.
// See ../portability-20261019/receipt.json for the exact old-to-new mapping.
const portableReferenceSha = {
  "reference/r43/independent-blind-story-review.md": "9dd31303d9ab5073213e61d810058ab60cfc66a8a9b51d1169d1166847ac91d5",
  "reference/r43/independent-source-review.md": "db36d89162f678d5fb6ecc18b956ee5bc141ac127a45daf32ede46b36b0dd4b7",
  "reference/r43/independent-visual-fact-audit.md": "8f40d47b3771d6646134edcf348a34c10bda42d7d01d0c9bd26fd43c2a390c52",
  "reference/snapshot104-host-readback.md": "712621b7fbc7e4f3c59bcc0026722915b942e76020673e9adad717ff41806acd"
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const read = (dir, name) => fs.readFileSync(path.join(dir, name));
assert.equal(sha(read(r43, 'manifest.json')), r43Sha, 'r43 manifest drift');
const oldManifest = JSON.parse(read(r43, 'manifest.json'));
assert.equal(oldManifest.source_snapshot104.id, baseline104.id, '104 snapshot id drift');
assert.equal(oldManifest.status, 'ALTERNATE_PROPOSAL_HOLD_OFFLINE_ONLY');
for (const name of ['candidate/video.json', 'candidate/series.json', 'candidate/lexicon.json'])
  assert.equal(sha(read(r43, name)), oldManifest.outputs_sha256[name], 'r43 packaged input drift ' + name);
assert.equal(sha(read(r43, 'research-plan-25-series.json')),
  oldManifest.outputs_sha256['research-plan-25-series.json'], 'r43 packaged research plan drift');
assert.equal(sha(read(r43, 'independent-blind-story-review.md')), portableReferenceSha['reference/r43/independent-blind-story-review.md'], 'r43 blind review drift');
assert.equal(sha(read(r43, 'independent-source-review.md')), portableReferenceSha['reference/r43/independent-source-review.md'], 'r43 source review drift');
assert.equal(sha(read(r43, 'independent-visual-fact-audit.md')), portableReferenceSha['reference/r43/independent-visual-fact-audit.md'], 'r43 visual review drift');
const oldStoryReview = read(r43, 'independent-blind-story-review.md').toString('utf8');
const oldSourceReview = read(r43, 'independent-source-review.md').toString('utf8');
const oldVisualReview = read(r43, 'independent-visual-fact-audit.md').toString('utf8');
assert.match(oldStoryReview, /PASS/);
assert.match(oldSourceReview, /P1 0、P2 5/);
assert.match(oldVisualReview, /50 條圖片提示詞/);
const oldReadback = read(here, 'reference/snapshot104-host-readback.md');
assert.equal(sha(oldReadback), portableReferenceSha['reference/snapshot104-host-readback.md'], 'historical snapshot104 readback drift');
for (const digest of [baseline104.source_sha256, baseline104.index_manifest_sha256, baseline104.tip_index_sha256])
  assert.ok(oldReadback.toString('utf8').includes(digest), 'historical snapshot104 digest missing');

assert.equal(chapters.length, 6);
const chapterTitle = new Map(chapters);
assert.equal(new Set(chapterTitle.keys()).size, 6);
const chapterOrder = new Map(chapters.map(([key], index) => [key, index]));
assert.equal(beats.length, 50, 'story beat drift');
const seenScene = new Set();
let priorChapter = 0;
const video = structuredClone(JSON.parse(read(r43, 'candidate/video.json')));
const oldSeries = JSON.parse(read(r43, 'candidate/series.json'));
const oldResearch = JSON.parse(read(r43, 'research-plan-25-series.json'));
const activeKeys = ['security', 'company', 'chief', 'patent', 'witness', 'dash'];
const activeUrls = activeKeys.map((key) => URL[key]);
assert.equal(new Set(activeUrls).size, activeUrls.length);
const oldPublic = new Map(video.sources.map((row) => [row.url, row]));
const oldPlan = new Map(oldResearch.plan.sources.map((row) => [row.url, row]));
for (const url of activeUrls) {
  assert.ok(oldPublic.has(url), 'missing r43 public source ' + url);
  assert.ok(oldPlan.has(url), 'missing r43 research source ' + url);
}

const claims = [];
const lineIds = new Map();
video.scenes = beats.map(([chapter, id, text, keys, statement, picture], index) => {
  assert.ok(chapterOrder.has(chapter) && !seenScene.has(id), 'invalid or duplicate scene ' + id);
  assert.ok(chapterOrder.get(chapter) >= priorChapter, 'chapter order drift ' + id);
  priorChapter = chapterOrder.get(chapter);
  seenScene.add(id);
  const sourceKeys = Array.isArray(keys) ? keys : [keys];
  for (const key of sourceKeys) assert.ok(activeKeys.includes(key), 'inactive claim source ' + id + ':' + key);
  const lineId = `r44l${String(index + 1).padStart(3, '0')}`;
  lineIds.set(id, lineId);
  const sceneClaims = sourceKeys.map((key) => {
    const claimId = `q${String(claims.length + 1).padStart(3, '0')}`;
    const claimStatement = statementForSource(id, key, statement);
    claims.push({ id: claimId, statement: claimStatement, url: URL[key], checked: '2026-10-19', scene_id: id, status: 'PENDING' });
    return claimId;
  });
  const row = { id, template: 'shot',
    data: { prompt: visual.people + picture, camera: index % 3 === 0 ? 'push in' : index % 3 === 1 ? 'track right' : 'static', visual: 'still' },
    claims: sceneClaims, lines: [{ id: lineId, text }] };
  if (index === 0 || beats[index - 1][0] !== chapter) row.chapter = chapterTitle.get(chapter);
  return row;
});
function statementForSource(id, key, defaultText) {
  if (id === 'hook-security') return key === 'company'
    ? 'Travelpro 公司史記 Plath 做出 Rollaboard 成品；不提供安檢樣品到成品的物理橋接。'
    : 'Plath 未標年的安檢回憶記他將外置行李推車用螺絲固定在自己的硬殼箱上，帶回機場安檢；推車材質未載，未證這只樣品變為後來成品。';
  if (id === 'hook-pilot-burden') return key === 'chief'
    ? 'Ballis 2007 受訪稱 Plath 日復一日提著沉重行李穿過航站。'
    : key === 'security'
      ? 'Plath 安檢回憶未標事件年份，不能指認與日常搬行李或 1993 商用箱測試為同一天。'
      : 'Dash 1993 原文測的是已上市的 Travelpro Rollaboard，不是早期安檢螺絲樣品。';
  if (id === 'idea-one-unit') return key === 'company'
    ? 'Travelpro 公司史記成品直立雙輪、頂部可收拉桿的一體箱。'
    : 'Plath 專利方案含箱身雙輪與可收拉桿，避免另帶推車。';
  if (id === 'origin-two-pieces') return key === 'security'
    ? '2012 安檢回憶記前方旅客費力想把箱子從外置輪架卸下。'
    : 'Plath 專利先前技術段指出外置輪架安檢須卸箱。';
  return defaultText;
}
assert.equal(seenScene.size, beats.length);
const pictureScenes = video.scenes.filter((scene) => scene.data.prompt);
assert.equal(pictureScenes.length, 50, 'visual audit must cover all 50 prompts');
const revealSceneIndex = pictureScenes.findIndex((scene) => scene.id === 'now-pocket');
assert.ok(revealSceneIndex > 0);
for (const [index, scene] of pictureScenes.entries()) {
  const prompt = scene.data.prompt;
  assert.ok(!/\b(?:the closed|the compact) the\b|The unbranded an unbranded|prototype's retractable handle|several expandable exterior|main-case zipper|bulky luggage trolley|nearby generic stairs|generic shop floor|passing a generic baggage carousel/i.test(prompt),
    'known prompt wording regression ' + scene.id);
  if (index < revealSceneIndex && prompt.includes('navy soft-sided two-wheel carry-on')) {
    assert.ok(prompt.includes('exterior storage out of view'), 'pre-reveal storage visible ' + scene.id);
    assert.ok(!prompt.includes('expandable exterior zippered compartments'), 'pre-reveal pocket detail ' + scene.id);
  }
}
const outro = structuredClone(JSON.parse(read(r43, 'candidate/video.json')).scenes.find((scene) => scene.id === 'now-outro'));
assert.ok(outro);
outro.chapter = undefined;
outro.data = { title: '能走，也要收得進去', cta: '資料來源在說明欄' };
outro.lines = [
  { id: 'r44out1', text: '你有沒有遇過，箱子明明拉得順，登機時卻放不下？' },
  { id: 'r44out2', text: '喜歡這種有來源的日用品故事，歡迎訂閱。' },
];
video.scenes.push(outro);
assert.equal(video.scenes.filter((row) => row.chapter).length, 6);
const loop = (setupScene, payoffScene, what) => ({ setup: lineIds.get(setupScene), payoff: lineIds.get(payoffScene), what });
video.loops = [
  loop('hook-security', 'origin-ok', '安檢回憶中的螺絲樣品，後續安檢員只答 OK'),
  loop('hook-crew', 'engine-first-eyes', '其他機師看見另有記錄的直立成品後請 Plath 製作'),
  loop('hook-curb', 'turn-curb', '1993 年記者對四家箱的地面路緣與階梯測試'),
  loop('hook-pocket', 'now-empty', 'Travelpro 取出外袋加放的衣書後才能收進機艙'),
  loop('origin-next', 'now-stow-fail', '安檢員回答 OK 不代表後來的市售箱能裝進機艙收納空間'),
  loop('idea-next', 'engine-crew', '直立成品先獲機組員使用'),
  loop('engine-competition', 'turn-choose', '四家比較中追一只 Travelpro Rollaboard'),
  loop('now-cabin-edge', 'now-empty', '收納空間成為下一道障礙，清出衣書才解決'),
];
for (const item of video.loops) assert.ok(item.setup && item.payoff);

const title = 'Rollaboard：機師做出會滾的登機箱，為何最後仍得拆包？';
video.characters = [
  { id: 'anonymous-pilot', name: 'anonymous pilot', appearance: 'anonymous adult pilot in a plain brown jacket, no uniform insignia, no identifiable historical likeness', voice: structuredClone(video.voice) },
  { id: 'anonymous-reporter', name: 'anonymous reporter', appearance: 'anonymous short-haired adult reporter in a muted rust jacket, no identifiable historical likeness', voice: structuredClone(video.voice) },
];
video.youtube.title = title;
video.youtube.description = '機師 Plath 把硬殼箱與外置輪架用螺絲鎖在一起，帶回安檢。到一九九三年，記者 Judi Dash 試一只市售 Travelpro Rollaboard：地面拉得動，座位下與頭頂櫃卻放不進。她最後得先取出什麼？\n\n未標年的車庫螺絲樣品，與後來 Rollaboard 的成品記錄，中間缺少可核的實物演變；1993 年的市售箱也不是同一實物。所有歷史人物與箱子為匿名可愛插畫示意。公司回顧與校友刊搜尋索引對成品年份不一致，原頁未完成查核，旁白不選定年份；1989 年是後來專利的申請年。1993 年測試只代表 Dash 當次經驗，地面測試、最後加物及取物的確切位置未見於原文；機艙走道說法是當時輪箱類型的概述。';
video.youtube.tags = ['品牌故事', 'Rollaboard', 'Travelpro', '輪子行李箱', '登機箱', 'Robert Plath', 'Judi Dash', '行李箱故事'];
video.thumbnail = { template: 'thumb', data: { headline: '會滾卻放不下？', tag: '品牌故事', shot: 'now-stow-fail' } };
video.sources = activeUrls.map((url) => structuredClone(oldPublic.get(url)));
assert.equal(video.sources.length, 6);
assert.deepEqual(new Set(claims.map((row) => row.url)), new Set(video.sources.map((row) => row.url)), 'public list must be exactly active claims');
const lexicon = structuredClone(JSON.parse(read(r43, 'candidate/lexicon.json')));
for (const term of ['Sadow', "Macy's", 'Anita', 'Willets', 'Burnham', 'Shiller']) delete lexicon.terms[term];
lexicon.terms.Judi = null;
lexicon.terms.Dash = null;

const series = structuredClone(oldSeries);
series.title = title;
series.series.note = 'A01 r44 Rollaboard 單線離線替代提案；r43 三份獨立報告為改稿依據，不構成 r44 審查。原 A01 核准企劃未改；新標題、縮圖、brief 待站主另審，無匯入、付費或排程授權。';
series.logline = '一位機師因安檢口的分離輪架而在車庫實驗；後來另有記錄的 Rollaboard 先給機組員用，再由 1993 年記者的一只市售 Travelpro 箱撞上機艙收納邊界。';
series.names = ['Robert Plath', 'Plath', 'Travelpro', 'Rollaboard', 'Judi Dash'];
series.characters = structuredClone(video.characters);
series.plan.question = 'Rollaboard 把輪子與拉桿整合成一件登機行李，為什麼 1993 年那只箱要收進機艙時仍得取出東西？';
series.plan.subject = 'Travelpro Rollaboard 產品線';
series.plan.chapters = [
  { key: 'hook', point: '第一句在 20 秒內提出 1993 Travelpro Rollaboard 放不進座位下與頭頂櫃、為何要取物的具體問題，先不說外袋原因；隨即點名 Plath 的負重、安檢螺絲樣品，再閃看機組反應與記者地面關卡。' },
  { key: 'origin', point: '倒回安檢樣品之前：前方旅客費力解彈力繩卸外置輪架；Plath 車庫把自己的硬殼箱與材質未載的外置行李推車以螺絲固定，回安檢聽見 OK 後說出反應；不證放行或登機。' },
  { key: 'idea', point: '明說螺絲樣品到成品缺可核橋接。另一份 Travelpro 公司記錄的 Rollaboard 為直立雙輪與可收拉桿的一體箱，免另帶輪架；接機組員是否採用。' },
  { key: 'engine', point: '其他機師請 Plath 做，同事先用；他仍在航空公司飛行時車庫製箱，需求使車庫轉倉庫。1989 專利只作後見文件，僅帶出嵌入輪子與機艙收納設計目的；旅客在航站看見空服員，Dash 1993 回顧早期 Travelpro 郵購與後來四牌並存。' },
  { key: 'turn', point: 'Dash 為避轉盤與錯送常帶手提行李，舊輪具上機需拆且可能另算件；這些是不同過往經驗。本次四牌實測只追一只 Travelpro，路緣與樓梯不定先後、轉彎大致順利；旅途中尼龍箱扛住碰撞推擠。大主艙的容量只講一次，接著記她把箱子塞得很滿；不把主艙冒充外袋所致收納失敗的直接原因，也不重建未載的開箱動作。' },
  { key: 'now', point: '先用「多數窄走道可過」作當時輪箱類型概述，隨即轉入這只 1993 市售 Travelpro 的座位下／頭頂櫃收納考驗；先呈兩處放不進，之後才揭最後加衣書令可擴外袋撐大箱身，取出外袋加物後收好。不臆造外袋確切個數或各袋裝載分布、先試哪處、加放或取出地點，也不重建這只箱的走道通行。' },
];
series.plan.takeaway = '這條產品線把輪架整合進箱身，1993 年一次實測卻顯示外袋加物仍可能讓登機箱放不進機艙收納空間；只有該記者那只箱的結果，不推廣成普遍性能。';
series.plan.must_verify = [
  { claim: 'Plath 未標年安檢回憶的前方旅客仍在費力卸箱；螺絲固定、警衛 OK 只證報導轉述，與成品無可核實物橋接', sources: [0], core: true, attributed: true },
  { claim: 'Travelpro 公司史敘述直立雙輪可收拉桿成品、機組先用、車庫轉倉庫及 Plath 後來全職經營；其 1987 年份為公司回顧，不在口播選定', sources: [1], core: true, attributed: true },
  { claim: 'Ballis 2007 受訪回憶其他機師見 Plath 使用輪箱後請他製作，不能以訪談的相對年份反推某一天', sources: [2], core: true, attributed: true },
  { claim: 'Plath 1989 申請專利的先前技術比較外置輪架及四輪拖帶箱，所提方案為一體雙輪可收拉桿；不是產品首發年或樣品演變實錄', sources: [3], core: true, attributed: true },
  { claim: 'Sharkey 在 RNPA 2016 p.48 重印之 2010 文章回顧旅客見空服員快步拉 Rollaboard；與鄰頁 Emmer 作者不能混同', sources: [4], core: false, attributed: true },
  { claim: 'Dash 1993 原文說早期 Travelpro 郵購、四牌地面與機上測試、先前舊輪具經驗；其單只 Travelpro 外袋加衣書後放不進兩種機艙收納處，清空才好', sources: [5], core: true, attributed: true },
];
series.plan.sources = activeUrls.map((url) => {
  const row = structuredClone(oldPlan.get(url));
  row.supports = series.plan.must_verify.find((entry) => entry.sources.includes(activeUrls.indexOf(url)))?.claim ?? row.supports;
  return row;
});
series.plan.names = structuredClone(series.names);
series.plan.cast = video.characters.map(({ id, appearance }) => ({ id, appearance, role: id === 'anonymous-pilot'
  ? '匿名機師插畫，不呈現 Plath 可辨面容或制服標誌'
  : '1993 年匿名記者插畫，不呈現 Judi Dash 可辨面容' }));
series.plan.image_notes = 'MiniMax image-01 可愛插畫；安檢隊伍前方是人數不指定的旅客群，彈力繩綁住的行李材質未載，不能畫硬殼；硬殼只屬 Plath 後來螺絲固定的樣品。前方旅客的外置輪架可畫笨重金屬，Plath 自己樣品的外置行李推車重量與材質未載，不指定笨重或金屬。車庫鎖螺絲鏡先畫未接合兩件物品，安檢對話不畫指螺絲手勢或放行。螺絲樣品與後來一體雙輪 Rollaboard 分成不同物件，不畫變形箭頭。1993 年記者固定短髮與暗紅外套，測試的是另一只後期市售深藍尼龍箱；箱內主艙剖面僅為結構示意，不畫記者於特定時間開箱。now-pocket 揭曉前僅畫深藍箱素面側，不顯外袋結構或鼓起；揭曉後才畫複數外側可擴拉鍊收納處，但不指定總數與各袋裝物分布。拉鍊局部不指定箱上部位。機艙走道只用匿名類型示意，不用同一只深藍實測箱；收納示意不畫箱子原先在地上。四牌比較不用同一商店場景，轉盤只作分隔的抽象對照，不能畫記者走過或連續選箱；陡路緣與樓梯不畫成同地點或先後。最後加放及取出衣書不標地點，不畫座位旁拆包或放下重量。所有姓名、商標、年份僅後製文字，不送圖像模型。';
series.plan.thumbnail = { headline: '會滾卻放不下？', idea: '匿名記者與一只深藍、無商標的直立雙輪箱，座位下和頭頂櫃顯得太窄；外袋結構完全遮蔽，以保留原因懸念。後製才加入主字；不畫歷史真人或真實商標。' };
series.plan.caveats = 'ALTERNATE_PROPOSAL: 這是改動已核准 A01 主題的離線替代方向，站主須另審標題、縮圖與 brief；原 A01 企劃未改。Plath 安檢回憶未標年，前方旅客的箱子材質未載、其輪架可據報導畫笨重金屬；Plath 自己螺絲樣品的外置推車材質及笨重程度未載。螺絲樣品→Rollaboard 成品無逐步實物橋接；1993 Travelpro 是後期市售個體。Travelpro 公司史記 1987，Chinook 2024 校友刊索引文字記 1988，原 PDF p.17 未目視，不口播任一年；1989 專利只是後見申請文件。Dash 的先前輪具與本次四牌測試不是一班機；走道說法是類型概述，地面路緣及最後加物、取物位置未載，收納段不補造從地上提箱。1993 Travelpro 外袋只知複數，不定總數或各袋裝物分布；四牌比較與轉盤也非來源已證同場動作。TTS、圖片、正式六章和收據未完成。';
series.target_minutes = 10; // series default; A01 video-only 7–8 minute owner exception.
assert.equal(series.title, video.youtube.title);
assert.deepEqual(series.plan.sources.map((row) => row.url), activeUrls);

const research = structuredClone(series);
const researchExtras = oldResearch.plan.sources.filter((row) => !activeUrls.includes(row.url));
assert.equal(researchExtras.length, 19);
research.plan.sources.push(...structuredClone(researchExtras));
assert.equal(research.plan.sources.length, 25);
research.plan.caveats += ' 後列 19 筆是舊 A01 廣題研究保留，無 r44 現行 claim；不可視為本片公開播出來源或已驗史實。';
const claimsText = ['# A01 r44 現行逐景主張（全部 PENDING）', '', 'ID｜主張｜公開 URL｜查閱日｜scene_id｜狀態',
  ...claims.map((row) => [row.id, row.statement, row.url, row.checked, row.scene_id, row.status].join('｜')), ''].join('\n');
assert.equal(new Set(claims.map((row) => row.id)).size, claims.length);
const sceneClaimIds = video.scenes.flatMap((scene) => scene.claims.map((id) => ({ id, scene_id: scene.id })));
assert.equal(sceneClaimIds.length, claims.length);
for (const row of claims) assert.equal(sceneClaimIds.filter((seen) => seen.id === row.id && seen.scene_id === row.scene_id).length, 1);
const publicIndex = new Map(video.sources.map((row, index) => [row.url, index]));
const candidateIndex = new Map(series.plan.sources.map((row, index) => [row.url, index]));
const researchIndex = new Map(research.plan.sources.map((row, index) => [row.url, index]));
const claimSourceRows = claims.map((row) => ({ id: row.id, url: row.url,
  public_source_index: publicIndex.get(row.url), plan_source_index: candidateIndex.get(row.url),
  research_source_index: researchIndex.get(row.url) }));
for (const row of claimSourceRows) {
  for (const [list, index] of [[video.sources, row.public_source_index], [series.plan.sources, row.plan_source_index],
    [research.plan.sources, row.research_source_index]]) {
    assert.ok(Number.isInteger(index) && index >= 0 && index < list.length, 'source index range ' + row.id);
    assert.equal(list[index].url, row.url, 'source URL mismatch ' + row.id);
  }
}
assert.deepEqual(new Set(claims.map((row) => row.url)), new Set(video.sources.map((row) => row.url)));

const [{ screenplay }, { estimateTimeline }, { lintVideo }, { cuteStoryVisualProblems }] = await Promise.all([
  import(pathToFileURL(path.join(repo, 'tools/video/core/screenplay.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/core/timeline.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/core/lint.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/automation/story.mjs'))),
]);
const script = Buffer.from(screenplay(video));
const lintContext = { lexicon,
  brief: read(here, 'brief.md').toString('utf8'),
  translations: {}, others: [], series };
const lint = lintVideo(video, lintContext);
const lint300 = lintVideo(video, { ...lintContext, cpm: 300 });
const cute = cuteStoryVisualProblems(video);
assert.equal(lint.errors.length, 0, 'lint errors ' + JSON.stringify(lint.errors));
assert.equal(lint300.errors.length, 0, '300-cpm lint errors ' + JSON.stringify(lint300.errors));
assert.equal(cute.length, 0, 'cute errors ' + JSON.stringify(cute));
const bodySeconds = {};
const totalSeconds = {};
const chapterSeconds = {};
for (const cpm of [250, 275, 300]) {
  const timeline = estimateTimeline(video, cpm);
  const final = timeline.scenes.find((entry) => entry.id === 'now-outro');
  assert.ok(final);
  bodySeconds[cpm] = Number((final.start_frame / 30).toFixed(1));
  totalSeconds[cpm] = Number((timeline.total_frames / 30).toFixed(1));
  if (cpm === 275) for (const [key, name] of chapters) {
    const startScene = video.scenes.find((scene) => scene.chapter === name);
    const start = timeline.scenes.find((entry) => entry.id === startScene.id).start_frame;
    const next = chapters[chapterOrder.get(key) + 1];
    const nextScene = next ? video.scenes.find((scene) => scene.chapter === next[1]) : video.scenes.find((scene) => scene.id === 'now-outro');
    const end = timeline.scenes.find((entry) => entry.id === nextScene.id).start_frame;
    chapterSeconds[key] = Number(((end - start) / 30).toFixed(1));
  }
}
const hookTimeline = estimateTimeline(video, 275);
const firstQuestionEndSeconds = Number((hookTimeline.lines[0].end_frame / 30).toFixed(1));
const plathStartSeconds = Number((hookTimeline.lines[1].start_frame / 30).toFixed(1));
assert.equal(video.scenes[0].id, 'hook-pocket');
assert.equal(video.scenes[1].id, 'hook-pilot-burden');
assert.ok(video.scenes[0].lines[0].text.includes('Rollaboard') && video.scenes[0].lines[0].text.includes('取出東西'));
assert.ok(video.scenes[1].lines[0].text.includes('Plath') && video.scenes[1].lines[0].text.includes('沒標年份'));
assert.ok(firstQuestionEndSeconds <= 20 && plathStartSeconds < 20, 'specific hook question and Plath must appear in first 20 seconds');
assert.ok(['now-stow-fail', 'now-pocket', 'now-space', 'now-empty'].every((id, index, list) =>
  index === 0 || video.scenes.findIndex((scene) => scene.id === list[index - 1]) < video.scenes.findIndex((scene) => scene.id === id)), 'failure must precede cause reveal and single remedy');

const sourceIndex = video.sources.map((source, index) => ({ index, url: source.url,
  claim_ids: claims.filter((row) => row.url === source.url).map((row) => row.id) }));
assert.ok(sourceIndex.every((row) => row.claim_ids.length > 0));
const sourceMap = {
  schema_version: 1, status: 'ALTERNATE_PROPOSAL_HOLD_R44_SOURCE_MAP',
  derives_from_r43_manifest_sha256: r43Sha,
  r43_blind_story_review_sha256: r43StoryReviewSha,
  r43_source_review_sha256: r43SourceReviewSha,
  r43_visual_review_sha256: r43VisualReviewSha,
  source_snapshot104: baseline104,
  source_snapshot104_readback_sha256: baselineReadbackSha,
  active_claims: claims.length,
  host_source_guard: `HOLD: ${claims.length} claims remain PENDING. Source indices bind to exact URLs; no old review becomes a formal receipt or paid authorization.`,
  source_index: sourceIndex,
  chapter_threads: chapters.map(([key, name]) => ({ key, name,
    first_scene: video.scenes.find((scene) => scene.chapter === name)?.id,
    last_scene: beats.filter((beat) => beat[0] === key).at(-1)?.[1] })),
  fixes_from_r43_review: ['Plath prototype trolley bulk and material remain unspecified; security answer quotes only the inability to remove the case',
    'curb and stair tests, four-brand comparison, and carousel preference do not invent a shared place or action order',
    'prototype and product visual nouns are separate; the garage fastening scene starts with unjoined objects',
    'before now-pocket the exterior storage is fully hidden; after reveal the outside compartments are plural without an asserted total count or filling pattern',
    'zipper crop has no asserted bag location and witnessed crew are flight attendants',
    'current source map and exact alignment status identify r44; prior r43 report hashes remain fixed inputs'],
  retained_research_only: 'r43 and earlier research artifacts remain frozen; r44 research-plan-25-series retains unplayed links.',
  prototype_product_caveat: 'Undated screw-fastened hard case and trolley is not asserted to evolve physically into the later integrated Rollaboard; the 1993 tested Travelpro is another commercial unit in the product line.',
  exact_year_caveat: '1987 company history vs index-only 1988 Chinook report remains unresolved and unspoken; 1989 is later patent filing, not product birth.',
};
const alignment = {
  schema_version: 1, status: 'ALTERNATE_PROPOSAL_HOLD_R44_EXACT_SOURCE_ALIGNMENT',
  counts: { source_snapshot104_events_historical: 104, scenes: video.scenes.length,
    lines: video.scenes.flatMap((scene) => scene.lines).length, claims: claims.length,
    public_sources: video.sources.length, candidate_plan_sources: series.plan.sources.length,
    research_plan_sources: research.plan.sources.length, research_only_sources: researchExtras.length },
  public_list_equals_claim_urls: true,
  all_three_indices_in_range_and_url_exact: true,
  claim_source_rows: claimSourceRows,
  host_adoption_allowed: false, paid_media_allowed: false,
};
assert.match(sourceMap.host_source_guard, new RegExp(`\\b${claims.length} claims remain PENDING\\b`));
const validation = {
  status: 'ALTERNATE_PROPOSAL_HOLD_OFFLINE_MECHANICAL_ONLY',
  derives_from_r43_manifest_sha256: r43Sha,
  r43_reviews_not_inherited_as_approval: true,
  owner_approval_of_new_title_and_brief: 'NOT_REQUESTED_NOT_GRANTED',
  target_body_seconds: [420, 480],
  estimated_body_seconds_not_tts: bodySeconds,
  first_question_end_seconds_275: firstQuestionEndSeconds,
  plath_start_seconds_275: plathStartSeconds,
  estimated_total_seconds_not_tts: totalSeconds,
  chapter_seconds_at_275_cpm: chapterSeconds,
  in_7_to_8_minute_band_at_275_cpm: bodySeconds[275] >= 420 && bodySeconds[275] <= 480,
  scenes: video.scenes.length, lines: video.scenes.flatMap((scene) => scene.lines).length,
  claims: claims.length, loops: video.loops.length,
  illustration_prompts_scanned: pictureScenes.length,
  pre_reveal_storage_hidden_by_prompt: true,
  known_prompt_wording_regressions: 0,
  public_sources: video.sources.length, candidate_plan_sources: series.plan.sources.length,
  research_plan_sources: research.plan.sources.length,
  lint_errors: lint.errors, lint_warning_count: lint.warnings.length,
  lint_300_errors: lint300.errors, cute_visual_errors: cute,
  independent_r44_first_time_story_review: 'NOT_RUN', independent_r44_source_review: 'NOT_RUN',
  independent_r44_visual_fact_review: 'NOT_RUN',
  official_six_chapter_host_review: 'NOT_RUN', actual_tts_and_cut: 'NOT_RUN',
  formal_script_review_receipt: 'NOT_ISSUED', host_import_or_paid_media: 'NOT_RUN',
};
const researchYear = {
  status: 'RESEARCH_ONLY_UNRESOLVED_NOT_NARRATED',
  derives_from_r43_manifest_sha256: r43Sha,
  company_url: URL.company,
  company_year: 1987,
  index_only_year: 1988,
  index_only_url: 'https://www.sl8.com/journal/may24/journal_images/Chinook_2024_5-3-24_FINAL.pdf',
  original_page17_visually_verified: false,
  patent_filed: '1989-08-08',
  interpretation: 'Do not pick a unique finished-product year, date the airport anecdote, or infer a documented prototype-to-product path.',
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', json(series)],
  ['candidate/lexicon.json', json(lexicon)],
  ['candidate/script.md', script],
  ['candidate/claims.md', Buffer.from(claimsText)],
  ['research-plan-25-series.json', json(research)],
  ['research-year-discrepancy.json', json(researchYear)],
  ['source-map.json', json(sourceMap)],
  ['source-alignment.json', json(alignment)],
  ['validation.json', json(validation)],
]);
const manifest = {
  status: 'ALTERNATE_PROPOSAL_HOLD_OFFLINE_ONLY',
  slug: video.slug,
  derives_from_r43_manifest_sha256: r43Sha,
  r43_story_review_sha256: r43StoryReviewSha,
  r43_source_review_sha256: r43SourceReviewSha,
  r43_visual_review_sha256: r43VisualReviewSha,
  prior_reviews_not_inherited_as_approval: true,
  source_snapshot104: baseline104,
  source_snapshot104_readback_sha256: baselineReadbackSha,
  owner_approved_A01_plan_unchanged: true,
  new_title_brief_thumbnail_need_owner_editorial_approval: true,
  build_sha256: sha(read(here, 'build.mjs')),
  story_data_sha256: sha(read(here, 'story-data.mjs')),
  brief_sha256: sha(read(here, 'brief.md')),
  readme_sha256: sha(read(here, 'README.md')),
  packaged_reference_sha256: Object.fromEntries([
    'reference/r43/manifest.json',
    'reference/r43/candidate/video.json',
    'reference/r43/candidate/series.json',
    'reference/r43/candidate/lexicon.json',
    'reference/r43/research-plan-25-series.json',
    'reference/r43/independent-blind-story-review.md',
    'reference/r43/independent-source-review.md',
    'reference/r43/independent-visual-fact-audit.md',
    'reference/snapshot104-host-readback.md',
  ].map((name) => [name, sha(read(here, name))])),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  old_candidates_or_production_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(['--preview', '--write', '--check'].includes(action), 'use --preview, --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output escaped r44');
  if (action === '--preview') assert.ok(!fs.existsSync(file), 'preview requires fresh output slot: ' + name);
  else if (action === '--write') {
    assert.ok(!fs.existsSync(file), 'r44 output exists; never overwrite: ' + name);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes, { flag: 'wx' });
  } else {
    assert.ok(fs.existsSync(file), 'missing output: ' + name);
    assert.ok(fs.readFileSync(file).equals(bytes), 'stale output: ' + name);
  }
}
console.log(JSON.stringify({ action, status: validation.status, scenes: validation.scenes,
  lines: validation.lines, claims: validation.claims,
  first_question_end_seconds_275: firstQuestionEndSeconds, plath_start_seconds_275: plathStartSeconds,
  chapter_seconds_275: chapterSeconds, body_seconds_250: bodySeconds[250],
  body_seconds_275: bodySeconds[275], body_seconds_300: bodySeconds[300],
  lint_errors: lint.errors.length, cute_errors: cute.length,
  manifest_sha256: sha(json(manifest)) }));
