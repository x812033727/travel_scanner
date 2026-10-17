import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Offline editorial candidate. Do not install it into a worker or call media providers.
const here = path.dirname(fileURLToPath(import.meta.url));
const base = path.resolve(here, '../B18-now-s095-tts-segment-candidate-20261017');
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const baseManifestSha = 'ec1cc2909c7ba27798d7a6f0217e879b13d92fcd2299859a624390607a14efd3';
const sha = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (file) => fs.readFileSync(file, 'utf8');
assert.equal(sha(fs.readFileSync(path.join(base, 'sha256.json'))), baseManifestSha, 'parent manifest drift');
for (const [name, expected] of Object.entries(JSON.parse(read(path.join(base, 'sha256.json'))).files)) {
  assert.equal(sha(fs.readFileSync(path.join(base, name))), expected, `parent file drift: ${name}`);
}

const previousSeries = JSON.parse(read(path.join(base, 'series.json')));
const series = structuredClone(previousSeries);
const previous = Object.fromEntries(keys.map((key) => [key, JSON.parse(read(path.join(base, 'chapters', `${key}.json`)))]));
const chapters = structuredClone(previous);

series.logline = '大阪小壽司店為解決遞盤與人手不足，借啤酒工廠的輸送帶做出會轉彎的餐台；萬博讓更多人看見後，其他店把同一個送盤想法改成後場直線、不同形狀的餐台。';
series.plan.chapters.find((chapter) => chapter.key === 'turn').point = '萬博讓元祿被看見並透過加盟展店。法院認定特定第579776號實用新案於1972年期滿，此後已有元祿以外的經營者；不能說所有權利同時到期或新店只因到期才出現。跟著一盤壽司看新店如何在後場製作、用直線送到客人面前；設備商年表另記1980年大型店旁通裝置、1986年ㄇ字型輸送帶店，發明協會記八〇年代中期郊區大店與後期家庭用餐場景。所有演變是不同店的路線，不講成同一家公司或一台機器的連續改造。';
series.plan.chapters.find((chapter) => chapter.key === 'now').point = '收回元祿堺東店2021年仍在使用的1985年製輸送機，與元祿產業另外保存的早期魚鱗板；兩者同在機械遺產第112號但不是同一台1958年機器。由早期轉彎、其他店的直線與不同座位路線，回到客人伸手拿盤的同一個送餐問題。原企劃1991辭書及2023市場數字保留作未口播背景，不再當後半段支線。';
series.plan.takeaway = '一間缺人的小店解決了壽司盤如何轉彎、走到客人眼前；萬博後不同經營者依店面重畫送盤路線，早期板片與後來仍使用的機器留下這條路的兩個不同年代。';
series.plan.must_verify[8].claim = '2021年日本機械學會將元祿壽司堺東店1985年製造、認定時仍在使用的輸送機，以及元祿產業另外保存的早期魚鱗板，認定為機械遺產第112號；兩者不是同一台1958年首店原機。';
series.plan.sources[2].supports += '；後來新業者改由師傅或員工在後場做壽司，使用直線輸送帶送到用餐區（同頁沿革段）。';
series.plan.caveats = series.plan.caveats.replace(
  '1971自動給茶裝置另有開發／供應版本差，旁白不定年；1974整合依發明協會。',
  '給茶整合時間未解：石野官方年表寫1971年已販售附給茶裝置的壽司輸送帶，集團介紹與發明協會則寫1974年整合／開發；不能推定1974為首次，本版給茶年份與支線不口播。',
);
assert(series.plan.caveats.includes('1971年已販售附給茶裝置'), 'tea conflict caveat missing');
series.plan.sources.push(
  { url: 'https://www.ishino-group.com/history/', publisher: '石野集團／北日本カコー官方年表', kind: 'official', supports: '1970年開發給茶裝置、1971年已販售附給茶裝置的壽司輸送帶；1980年販售大型店旁通裝置、1986年記錄ㄇ字型輸送帶的店。1971與集團介紹所述1974整合／開發口徑不合，不能推定首次整合年。', checked: '2026-10-17' },
  { url: 'https://www.ishino-group.com/group/', publisher: '石野集團官方介紹', kind: 'official', supports: '集團介紹稱1974年開發／整合附給茶裝置的壽司輸送帶；與同集團年表的1971年已販售整合設備說法有未解差異。只用於 caveat，不作本版旁白主張。', checked: '2026-10-17' },
);
series.plan.must_verify.push(
  { claim: '石野集團官方年表記1980年已販售大型店旁通裝置，1986年已有ㄇ字型輸送帶的店；不得說兩者是同一家公司同一餐廳的一次改造，也不得說由旁通直接導致ㄇ字型店。', sources: [4] },
  { claim: '石野年表寫1971年已販售附給茶裝置的壽司輸送帶，集團介紹稱1974年開發／整合；兩個版本的先後與產品型號未解，旁白不說首次整合年。', sources: [4, 5] },
  { claim: '發明協會記載新業者讓師傅或員工在後場做壽司，將盤子放上直線輸送帶，從後場送至客人所在用餐區；只適用部分新業者，不當作白石元祿首店的改裝。', sources: [2] },
);
assert.equal(series.plan.sources.length, 6);
assert.equal(series.plan.must_verify.length, 13);

// Each surviving spoken line has one source-bound action or a connective question.
const turnLines = {
  'turn-s081': '別家店接手後，盤子要怎麼走，還能重畫。',
  'turn-s070': '新店想讓更多客人拿到壽司，師傅還非得站在客人面前嗎？',
  'turn-s071': '發明協會記錄，有新業者讓師傅或員工改在後場做壽司。',
  'turn-s072': '他們先在後場完成一盤壽司，再把盤子放上輸送帶。',
  'turn-s073': '餐台不再只繞著吧台，而是拉成一條直線。',
  'turn-s075': '盤子從後場走進用餐區，在客人面前經過；人仍能伸手拿到它。',
  'turn-s084': '白石花多年解決的轉角，不是每一家後來的店都必須保留。',
  'turn-s085': '等店面再變大，一條送盤的路，又要怎麼安排？',
  'turn-s086': '石野集團年表記下，一九八〇年已有賣給大型店的旁通裝置。',
  'turn-s088': '可是座位再排開，盤子最後要繞到哪裡？',
  'turn-s089': '到了八〇年代中期，郊區開始有面積更大的迴轉壽司店。',
  'turn-s090': '石野集團記下一九八六年已出現ㄇ字型輸送帶的店；盤子沿座位折回來。',
  'turn-s091': '八〇年代後期，郊區大店也成了家人一起吃飯的地方。',
  'turn-s092': '再往後，元祿自己的店裡竟還有一台舊輸送機在使用。它是哪一年造的？',
};
const nowLines = {
  'now-s093': ['那部還在店裡工作的輸送機，是最早的那一台嗎？'],
  'now-s097': ['被保存的早期板片，和那台一九八五年的輸送機，是兩件分開的東西。'],
  'now-s098': ['早期的扇形板片，回答了當年那個彎怎麼過。', '後來仍在店裡運轉的機器，則讓人看到這個辦法沒有只停在第一次試作。'],
  'now-s101': ['送餐的走法變了，客人伸手拿盤這個動作卻留下來。'],
  'now-s101b': ['當初白石把輸送帶帶回小店；別的店又把那條送餐路，改成自己的形狀。'],
};
for (const [id, text] of Object.entries(turnLines)) {
  const scene = chapters.turn.scenes.find((row) => row.id === id);
  assert.equal(scene?.lines.length, 1, `turn scene shape: ${id}`);
  scene.lines[0].text = text;
}
for (const [id, texts] of Object.entries(nowLines)) {
  const scene = chapters.now.scenes.find((row) => row.id === id);
  assert.equal(scene?.lines.length, texts.length, `now scene shape: ${id}`);
  scene.lines.forEach((line, index) => { line.text = texts[index]; });
}
const turnCards = {
  'turn-s071': { title: '後場製作', subtitle: '師傅或員工先做好壽司', tag: '發明協會' },
  'turn-s073': { title: '直線送盤', subtitle: '後場 → 用餐區', tag: '發明協會' },
};
const nowCards = {
  'now-s093': { title: '2021 · 元祿壽司堺東店', subtitle: '仍在使用的輸送機', tag: '日本機械學會' },
  'now-s098': { title: '兩個年代 · 兩件實物', subtitle: '早期板片／1985 年製輸送機', tag: '日本機械學會' },
};
for (const [id, data] of Object.entries(turnCards)) Object.assign(chapters.turn.scenes.find((row) => row.id === id).data, data);
for (const [id, data] of Object.entries(nowCards)) Object.assign(chapters.now.scenes.find((row) => row.id === id).data, data);

const prompts = {
  'turn-s081': 'Medium shot at a 1970s Japanese sushi shop planning table, one operator drawing a new plain conveyor route around empty seat shapes on a blank sheet, his fingertip resting beside one serving plate, soft desk light.',
  'turn-s070': 'Medium shot inside a 1970s Japanese sushi dining room, one chef facing a row of waiting diners across a small circular counter, his worried eyes on a single unserved plate, gentle overhead light.',
  'turn-s072': 'Medium shot in a 1970s Japanese restaurant back room, one chef setting a prepared sushi plate onto the entrance of a straight conveyor, the kitchen opening visible beyond, soft indoor light.',
  'turn-s075': 'Medium shot in a 1970s sushi dining room, one diner reaching toward a plate arriving along a straight conveyor from the distant kitchen opening, the plate and hand in clear focus, mild window light.',
  'turn-s085': 'Medium shot inside a larger 1980s Japanese sushi restaurant, one operator studying a blank floor plan beside a single serving plate, rows of empty seats beyond, mild afternoon light.',
  'turn-s086': 'Medium shot at a 1980 Japanese restaurant equipment workbench, one technician fitting a simplified conveyor bypass section beside a plain plate, no readable markings, soft workshop light.',
  'turn-s088': 'Wide shot in a growing 1980s Japanese sushi dining room, one operator looking from the end of a serving conveyor across several empty seats, the unfinished route stopping before the last seat, gentle ceiling light.',
  'turn-s090': 'Wide shot inside a 1986 Japanese conveyor sushi restaurant, one diner reaching toward a plate on a simple U-shaped conveyor between seats, the broad bend visible, soft indoor light.',
  'turn-s091': 'Medium shot inside a late-1980s suburban Japanese sushi restaurant, one parent drawing a serving plate toward a family table beside the conveyor, child seat and spacious aisle in the background, mellow ceiling light.',
  'turn-s092': 'Close-up at a 2021 Japanese sushi restaurant, one equipment attendant checking a visibly used but unbranded conveyor machine beside a dining counter, no date or logo on the machine, gentle overhead light.',
  'now-s097': 'Medium shot at a 2021 illustrative archive worktable, one attendant setting a detached early fan-shaped conveyor plate apart from a model of a later whole machine, clear gap between the two objects, soft overhead light.',
  'now-s101b': 'Wide street-level shot of a present-day unbranded Japanese sushi restaurant, one passerby looking through the window at a conveyor and a diner taking one plate inside, soft overcast daylight.',
};
for (const [id, prompt] of Object.entries(prompts)) {
  const scene = [...chapters.turn.scenes, ...chapters.now.scenes].find((row) => row.id === id);
  assert.equal(scene?.template, 'shot', `prompt edit needs shot: ${id}`);
  scene.data.prompt = prompt;
}
const removedScenes = ['turn-s083', 'turn-s087', 'now-s099', 'now-s100'];
chapters.turn.scenes = chapters.turn.scenes.filter((scene) => !removedScenes.includes(scene.id));
chapters.now.scenes = chapters.now.scenes.filter((scene) => !removedScenes.includes(scene.id));

const turnClaimEdits = {
  t5: { claim: '有新業者讓師傅或員工在後場做壽司', scene: 'turn-s071', source: 2, fact: 12, note: '發明協會後場製作；不是白石首店。' },
  t6: { claim: '做好的盤子從後場放上直線輸送帶', scene: 'turn-s072', source: 2, fact: 12, note: '發明協會後場到用餐區的直線輸送；無給茶年份。' },
  t10: { claim: '萬博與加盟先把元祿的做法帶到更多地方', scene: 'turn-s081', source: 2, fact: 7, note: '曝光和展店並行，不以權利到期作單因。' },
  t11: { claim: '有新店把繞吧台的餐台改成後場到用餐區的直線輸送帶', scene: 'turn-s073', source: 2, fact: 12, note: '只指部分新店，不指全部或同一台原機。' },
  t12: { claim: '一九八〇年已有賣給大型店的旁通裝置', scene: 'turn-s086', source: 4, fact: 10, note: '石野集團官方年表；不推為白石或同一間店。' },
  t13: { claim: '一九八六年已有ㄇ字型輸送帶的店', scene: 'turn-s090', source: 4, fact: 10, note: '石野集團官方年表；不推為1980旁通的直接結果。' },
  t14: { claim: '八〇年代中期，郊區出現面積更大的迴轉壽司店', scene: 'turn-s089', source: 2, fact: null, note: '發明協會記的產業變化，不指同一家元祿店。' },
  t15: { claim: '八〇年代後期，郊區大店也成了家人一起吃飯的地方', scene: 'turn-s091', source: 2, fact: null, note: '發明協會記的家客場景，不把1986ㄇ字型店指成同店。' },
};
for (const claim of chapters.turn.claims) if (turnClaimEdits[claim.id]) Object.assign(claim, turnClaimEdits[claim.id]);
chapters.turn.claims.push(
  { id: 't16', claim: '直線輸送帶把後場做好的盤子送到用餐區客人面前', scene: 'turn-s075', source: 2, fact: 12, verdict: 'UNCHECKED', note: '發明協會後場到前場的具體路徑；部分新業者，非元祿原店。' },
  { id: 't17', claim: '一些直線輸送帶店不必保留白石的繞吧台轉角', scene: 'turn-s084', source: 2, fact: 12, verdict: 'UNCHECKED', note: '由發明協會所述直線路線作有限幾何推論，不能推成全體店。' },
  { id: 't18', claim: '二〇二一年元祿堺東店仍在使用一台一九八五年製輸送機', scene: 'turn-s092', source: 1, fact: 8, verdict: 'UNCHECKED', note: '日本機械學會認定當時使用中；不暗示無間斷運轉或現今仍在用。' },
);
chapters.now.claims = chapters.now.claims.filter((claim) => !['n1', 'n7', 'n8'].includes(claim.id));
Object.assign(chapters.now.claims.find((claim) => claim.id === 'n6'), {
  claim: '早期板片與一九八五年製輸送機是分別保存或使用的兩件實物', scene: 'now-s097', source: 1, fact: 8,
  note: '日本機械學會分列元祿堺東店使用中的整機與元祿產業另存的早期板片；非1958原機一路運轉。',
});
chapters.now.claims.push(
  { id: 'n7', claim: '早期扇形魚鱗板片解決盤子過轉角的難題', scene: 'now-s098', source: 0, fact: 3, verdict: 'UNCHECKED', note: '重提首段解法作結尾回收；J-Net21 的撲克牌版本與發明協會名片版本分開。' },
  { id: 'n8', claim: '一九八五年製的後來輸送機在二〇二一年認定時仍於元祿店使用', scene: 'now-s098', source: 1, fact: 8, verdict: 'UNCHECKED', note: '日本機械學會實物資料；「沒有只停在第一次試作」是故事推論，非同一原機。' },
);
const turnLoops = chapters.turn.loops;
const bySetup = (setup) => { const loop = turnLoops.find((row) => row.setup === setup); assert(loop, `missing loop: ${setup}`); return loop; };
Object.assign(bySetup('a4b8321a'), { payoff: '86198f0e', what: '新店在後場做的盤子如何走到客人面前' });
Object.assign(bySetup('7151b051'), { payoff: 'eed19791', what: '大店如何把送盤路線排到更多座位' });
Object.assign(bySetup('f996e543'), { payoff: '8b88e002', what: '2021年仍使用的元祿輸送機是哪一年製' });
chapters.now.loops = chapters.now.loops.filter((row) => row.setup !== 'f996e543');

// Validate every binding and then run the same offline composition and lint gates.
const allScenes = keys.flatMap((key) => chapters[key].scenes);
const sceneMap = new Map(allScenes.map((scene) => [scene.id, scene]));
assert.equal(sceneMap.size, allScenes.length);
assert.equal(allScenes.length, 86);
const allClaims = keys.flatMap((key) => chapters[key].claims);
assert.equal(new Set(allClaims.map((claim) => claim.id)).size, allClaims.length, 'duplicate claim id');
for (const claim of allClaims) {
  assert(sceneMap.has(claim.scene), `claim scene missing: ${claim.id}`);
  assert(series.plan.sources[claim.source], `claim source missing: ${claim.id}`);
  if (claim.fact !== null && claim.fact !== undefined) {
    const fact = series.plan.must_verify[claim.fact];
    assert(fact?.sources.includes(claim.source), `claim fact/source mismatch: ${claim.id}`);
  }
  assert.equal(claim.verdict, 'UNCHECKED', `unreviewed claim promoted: ${claim.id}`);
}
const allLineIds = new Set(allScenes.flatMap((scene) => scene.lines.map((line) => line.id)));
assert.equal(allLineIds.size, allScenes.flatMap((scene) => scene.lines).length, 'duplicate narration line id');
assert.deepEqual(chapters.now.scenes.find((scene) => scene.id === 'now-s095').lines, previous.now.scenes.find((scene) => scene.id === 'now-s095').lines, 'punctuation successor changed');
const lateNarration = [...chapters.turn.scenes, ...chapters.now.scenes].flatMap((scene) => scene.lines.map((line) => line.text)).join('\n');
assert(!/(?:1974|一九七四|給茶|採購|盤價|廣辭苑|市場規模)/u.test(lateNarration), 'retired branch remains in narration');
assert(![...chapters.turn.scenes, ...chapters.now.scenes].some((scene) => /1974/u.test(scene.data?.title ?? '')), 'disputed tea-year card remains');
for (const loop of keys.flatMap((key) => chapters[key].loops)) {
  assert(allLineIds.has(loop.setup), `loop setup missing: ${loop.setup}`);
  if (loop.payoff) assert(allLineIds.has(loop.payoff), `loop payoff missing: ${loop.payoff}`);
}
for (const key of ['hook', 'origin', 'idea', 'engine']) assert.deepEqual(chapters[key], previous[key], `early chapter changed: ${key}`);
const { composeStory, cuteStoryVisualProblems } = await import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs')).href);
const { loadProject, lintProject } = await import(pathToFileURL(path.join(root, 'tools/video/core/state.mjs')).href);
const { estimateTimeline } = await import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs')).href);
const slug = 'story-conveyor-belt-sushi-v2';
const authored = path.resolve(base, '../B18-authored-chapters-candidate');
const voice = JSON.parse(read(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'video.json'))).voice;
const beforeDoc = composeStory({ slug, info: previousSeries, chapters: previous, voice, drama: { music_enabled: false }, root });
const doc = composeStory({ slug, info: series, chapters, voice, drama: { music_enabled: false }, root });
assert.equal(doc.scenes.length, 86);
assert.equal(doc.scenes.flatMap((scene) => scene.lines).length, 89);
assert.deepEqual(doc.look, { preset: 'cute-mystery' });
assert.equal(doc.subtitles.burn_in, false);
const cuteErrors = cuteStoryVisualProblems(doc);
assert.deepEqual(cuteErrors, []);
const punctuationOnly = doc.scenes.flatMap((scene) => scene.lines).filter((line) => /^[\p{P}\p{S}\s]+$/u.test(line.text));
assert.deepEqual(punctuationOnly, []);
assert.equal(allClaims.length, 67);
let externalCalls = 0;
globalThis.fetch = () => { externalCalls++; throw new Error('offline narrative candidate must not fetch'); };
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'b18-one-thread-'));
const relativeTmp = path.relative(path.resolve(os.tmpdir()), path.resolve(tmp));
assert(/^b18-one-thread-[^\\/]+$/.test(relativeTmp), 'unsafe temporary cleanup path');
let lint;
try {
  const shelf = path.join(tmp, 'docs', 'videos');
  const dir = path.join(shelf, slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'video.json'), canonical(doc));
  fs.writeFileSync(path.join(dir, 'series.json'), canonical(series));
  fs.copyFileSync(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'brief.md'), path.join(dir, 'brief.md'));
  fs.copyFileSync(path.join(authored, 'fixtures/lexicon.json'), path.join(shelf, 'lexicon.json'));
  lint = lintProject(loadProject({ slug, root: tmp }));
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
assert.deepEqual(lint.errors, []);
assert.equal(externalCalls, 0);
const estimatedBeforeSeconds = estimateTimeline(beforeDoc).total_frames / 30;
const estimatedBodySeconds = estimateTimeline(doc).total_frames / 30;
assert(estimatedBodySeconds >= 540 && estimatedBodySeconds <= 600, 'static body estimate escaped near-ten-minute plan');
const sceneChanges = [...Object.keys(turnLines), ...Object.keys(nowLines)];
const sceneBeforeById = new Map(keys.flatMap((key) => previous[key].scenes.map((scene) => [scene.id, scene])));
const sceneAfterById = new Map(keys.flatMap((key) => chapters[key].scenes.map((scene) => [scene.id, scene])));
const claimBeforeById = new Map(keys.flatMap((key) => previous[key].claims.map((claim) => [claim.id, claim])));
const claimAfterById = new Map(allClaims.map((claim) => [claim.id, claim]));
const allPreviousLoops = keys.flatMap((key) => previous[key].loops.map((loop) => ({ chapter: key, ...loop })));
const allNewLoops = keys.flatMap((key) => chapters[key].loops.map((loop) => ({ chapter: key, ...loop })));
const delta = {
  schema_version: 1,
  status: 'OFFLINE_ONE_THREAD_NARRATIVE_DELTA',
  base_manifest_sha256: baseManifestSha,
  changed_scene_ids: [...new Set([...sceneChanges, ...Object.keys(prompts)])],
  removed_scene_ids: removedScenes,
  changed_scene_rows: [...new Set([...sceneChanges, ...Object.keys(prompts)])].map((id) => ({ id, before: sceneBeforeById.get(id), after: sceneAfterById.get(id) })),
  removed_scene_rows: removedScenes.map((id) => ({ id, before: sceneBeforeById.get(id), after: null })),
  changed_claim_ids: [...Object.keys(turnClaimEdits), 'n6', 'n7', 'n8'],
  new_claim_ids: ['t16', 't17', 't18'],
  removed_claim_ids: ['n1'],
  claim_rows: [...Object.keys(turnClaimEdits), 'n6', 'n7', 'n8', 't16', 't17', 't18', 'n1'].map((id) => ({ id, before: claimBeforeById.get(id) ?? null, after: claimAfterById.get(id) ?? null })),
  changed_loop_setups: ['a4b8321a', '7151b051', 'f996e543'],
  removed_duplicate_loop_setup: 'now:f996e543',
  loop_rows: { before: allPreviousLoops, after: allNewLoops },
  plan_rows: {
    logline: { before: previousSeries.logline, after: series.logline },
    turn: { before: previousSeries.plan.chapters.find((row) => row.key === 'turn'), after: series.plan.chapters.find((row) => row.key === 'turn') },
    now: { before: previousSeries.plan.chapters.find((row) => row.key === 'now'), after: series.plan.chapters.find((row) => row.key === 'now') },
    takeaway: { before: previousSeries.plan.takeaway, after: series.plan.takeaway },
    caveats: { before: previousSeries.plan.caveats, after: series.plan.caveats },
    source_2: { before: previousSeries.plan.sources[2], after: series.plan.sources[2] },
    fact_8: { before: previousSeries.plan.must_verify[8], after: series.plan.must_verify[8] },
    source_appends: series.plan.sources.slice(4),
    fact_appends: series.plan.must_verify.slice(10),
  },
  source_additions: [4, 5], fact_additions: [10, 11, 12],
  new_artifact_claims_still_unchecked: true,
  old_intro_and_four_early_chapters_unchanged: true,
  parent_2021_punctuation_fix_preserved: true,
  estimated_body_seconds_before: estimatedBeforeSeconds,
  estimated_body_seconds_after: estimatedBodySeconds,
  actual_tts_seconds: null,
  paid_calls: 0,
};
const verification = {
  schema_version: 1,
  status: 'VERIFIED_OFFLINE_STRUCTURE_ONLY_FULL_STORY_HOLD',
  scenes: doc.scenes.length,
  lines: doc.scenes.flatMap((scene) => scene.lines).length,
  illustrations: doc.scenes.filter((scene) => scene.template === 'shot').length,
  cards: doc.scenes.filter((scene) => scene.template !== 'shot').length,
  claims_unchecked: allClaims.length,
  punctuation_only_lines: punctuationOnly.length,
  estimated_body_seconds: estimatedBodySeconds,
  measured_body_seconds: null,
  lint_errors: lint.errors,
  lint_warnings: lint.warnings.length,
  lint_warning_kinds: [...new Set(lint.warnings.map((warning) => warning.message.split(':', 1)[0]))],
  cute_errors: cuteErrors,
  external_calls: externalCalls,
  worker_pass: false, full_story_pass: false, full_source_pass: false, tts_generated: false,
};
const output = new Map([
  ['series.json', canonical(series)],
  ['reuse-intent.json', read(path.join(base, 'reuse-intent.json'))],
  ['delta.json', canonical(delta)],
  ['verification.json', canonical(verification)],
]);
for (const key of keys) output.set(`chapters/${key}.json`, ['turn', 'now'].includes(key) ? canonical(chapters[key]) : read(path.join(base, 'chapters', `${key}.json`)));
const hashes = Object.fromEntries([
  ['build.mjs', sha(fs.readFileSync(path.join(here, 'build.mjs')))],
  ['README.md', sha(fs.readFileSync(path.join(here, 'README.md')))],
  ...[...output].map(([name, content]) => [name, sha(content)]),
]);
output.set('sha256.json', canonical({ schema_version: 1, base_manifest_sha256: baseManifestSha, files: hashes }));
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
for (const [name, content] of output) {
  const file = path.join(here, name);
  if (mode === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, content);
  } else assert.equal(read(file), content, `generated output drift: ${name}`);
}
console.log(JSON.stringify(verification, null, 2));
