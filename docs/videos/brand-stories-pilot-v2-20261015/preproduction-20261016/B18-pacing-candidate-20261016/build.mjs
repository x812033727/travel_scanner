import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// A strictly offline, pinned edit of the source-bound candidate. It never touches that input.
const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.dirname(here);
const source = path.join(parent, 'B18-source-bound-revision-candidate-20261016');
const authored = path.join(parent, 'B18-authored-chapters-candidate');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const pins = {
  'series.json': '54152ce70772ffb1890ef83fdc0dec8dfd8071afe75db976b7b08975cfea5c97',
  'chapters/hook.json': '370baea920b35bd5c774bfc4e199d920a9c406f0f470d32c4e2430a300955388',
  'chapters/origin.json': '131819138e82506c095df4a9379d4f11e6d108e5d4b48b01495d2eddb8dd16dd',
  'chapters/idea.json': '159a25dc1a13ac1247467507064625f3599db535500c67a88c490cebaff763b1',
  'chapters/engine.json': '0776cc88fdaf456f8907775af23b53be9560ed53b56557a300e0fe2291fff33b',
  'chapters/turn.json': 'db5f9b19343a1e1814a769cd121cef891ccda1faaba09a526295b019092e5d73',
  'chapters/now.json': 'db1736a1989efe6662373856b65ed191bbe55206c1517cf376dbc535e619511a',
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
const fileOf = (name) => name.includes('chapters/idea') || name.includes('chapters/now')
  ? path.join(authored, name) : path.join(source, name);
for (const [name, expected] of Object.entries(pins)) {
  assert.equal(sha(fs.readFileSync(fileOf(name))), expected, `input drift: ${name}`);
}
const read = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const series = read(fileOf('series.json'));
const chapters = Object.fromEntries(keys.map((key) => [key, read(fileOf(`chapters/${key}.json`))]));
const oldChapters = structuredClone(chapters);
const changes = [];
const find = (chapter, id) => {
  const value = chapters[chapter].scenes.find((item) => item.id === id);
  assert(value, `${chapter}/${id} missing`);
  return value;
};
const edit = (chapter, scene, line, before, after) => {
  const found = find(chapter, scene).lines.find((item) => item.id === line);
  assert(found, `${chapter}/${scene}/${line} missing`);
  assert.equal(found.text, before, `spoken input drift: ${chapter}/${scene}/${line}`);
  assert(after.trim(), `empty line: ${chapter}/${scene}/${line}`);
  found.text = after;
  changes.push({ kind: 'spoken', chapter, scene, line, before, after });
};
const data = (chapter, scene, field, before, after) => {
  const found = find(chapter, scene);
  assert.equal(found.data[field], before, `visual input drift: ${chapter}/${scene}/${field}`);
  found.data[field] = after;
  changes.push({ kind: 'visual', chapter, scene, field, before, after });
};
const drop = (chapter, id) => {
  const old = find(chapter, id);
  assert(!chapters[chapter].claims.some((item) => item.scene === id), `claimed scene: ${id}`);
  const lineIds = new Set(old.lines.map((item) => item.id));
  assert(!keys.some((key) => chapters[key].loops?.some((item) => lineIds.has(item.setup) || lineIds.has(item.payoff))), `loop scene: ${id}`);
  assert.notEqual(chapters[chapter].scenes[0].id, id, `chapter opener: ${id}`);
  chapters[chapter].scenes = chapters[chapter].scenes.filter((item) => item.id !== id);
  changes.push({ kind: 'drop_repeated_scene', chapter, scene: id, lines: old.lines.map((item) => ({ id: item.id, text: item.text })) });
};
const addLoop = (chapter, setup, payoff, what) => {
  assert(keys.some((key) => chapters[key].scenes.some((scene) => scene.lines.some((line) => line.id === setup))), `loop setup: ${setup}`);
  assert(keys.some((key) => chapters[key].scenes.some((scene) => scene.lines.some((line) => line.id === payoff))), `loop payoff: ${payoff}`);
  assert(!chapters[chapter].loops.some((item) => item.setup === setup), `duplicate loop: ${setup}`);
  chapters[chapter].loops.push({ setup, payoff, what });
  changes.push({ kind: 'open_loop', chapter, setup, payoff, what });
};

// The staffing and handoff bottleneck has already been demonstrated; move to his answer.
drop('origin', 'origin-s018');
edit('origin', 'origin-s019', '9acdd125',
  '即使多找人握壽司，盤子仍要有人送。白石至少得先改掉送盤的方法。',
  '師傅留不住，白石得先改掉送盤的方法。');

// Keep both attributed fan-leaf origin versions, and pay off the uncertainty honestly.
edit('idea', 'idea-s023', 'b14f7257',
  '開場那個會卡住的轉角，難題才真正露出來。直線上，盤子能跟著輸送帶走；',
  '直線走得通，轉角卻會出事。');
edit('idea', 'idea-s026', 'f93257dd',
  '這裡有個流傳很廣的畫面：一疊薄片打開，像扇子一樣排開。但那疊薄片究竟是什麼，',
  '像扇子攤開的薄片，究竟是什麼？');
edit('idea', 'idea-s030', '8761bf5b',
  '我們無法用這兩份記載，替白石挑出唯一的那一刻。可以確定的是，',
  '兩種記載，現在無法判定哪個才是現場；能確定的是，');
drop('idea', 'idea-s039');
addLoop('idea', 'f93257dd', '8761bf5b', '扇形靈感版本能否確定');

// Hold on the first real handoff as the payoff for the opening staffing problem;
// trim the repeated order-taking detail before moving into protection and expo.
edit('engine', 'engine-s044', 'd428ad00',
  '這時主要賣的是一盤四貫、五十日圓。比起早年的立食壽司，店變了，',
  '這時主要賣一盤四貫、五十日圓，和早年立食壽司不同。');
drop('engine', 'engine-s045');
edit('engine', 'engine-s046', '128aabfa',
  '就能拿哪盤。從店外還看得見輸送帶在轉，連經過的人也會停下來看。',
  '從店外還看得見輸送帶在轉，路人也會停下來看。');
edit('engine', 'engine-s047', 'b7cfe92f',
  '第一家店熱鬧之後，問題換了。這個做法別人看得見，也可能照著做。',
  '別的店若照著做，白石怎麼回應？');
drop('engine', 'engine-s051');
edit('engine', 'engine-s054', '14b284ee',
  '不過，法律能守住一種裝置，還不能讓全國的人都看過這種店。',
  '法律能守住裝置，怎麼讓更多人看見這種店？');
edit('engine', 'engine-s055', '7b46f60c',
  '開場的萬博會場，真的迎來元祿壽司。',
  '下一站，是開場的萬博會場。');
addLoop('engine', 'b7cfe92f', 'b4d30dda', '白石如何回應相似店');

// Expo already paid off; the rights, tea, route and price changes carry this chapter.
drop('turn', 'turn-s066');
edit('turn', 'turn-s085', '7151b051',
  '同一條送餐路，連客人伸手拿盤時要付多少錢，也開始有新答案。',
  '路線能改，成本和盤子的價錢呢？');
edit('turn', 'turn-s091', '3f9afeb4',
  '走到店與店比採購、比價格、比誰能讓一家人坐得下，這條路已經換了好多種走法。',
  '送盤、採購、定價、家庭座位，這條路走出許多岔。');
addLoop('turn', '7151b051', '9c345945', '獨立店如何調整成本與盤價');

// Keep dates and the fact that 2023 figures were historical projections, but avoid a
// third spoken 2023 and a second explanation of the dictionary entry.
drop('now', 'now-s094');
edit('now', 'now-s097', 'ecbc8805',
  '二〇二三年的報導引用富士經濟調查：',
  '一份報導引用富士經濟調查：');
edit('now', 'now-s099', '25b47e1e',
  '不是今天的實績。這些數字，已經離布施那家二十坪小店很遠。',
  '不是今天的實績；數字已遠離那間二十坪小店。');
const repeatedEnding = 'Medium shot at an unbranded Japanese sushi counter in a present-day illustrative setting, one generic diner reaching toward one plate on the circulating belt, another plate remains farther along the route, the choice at the diner’s fingertips is the focal object, neutral soft light.';
data('now', 'now-s101', 'prompt', repeatedEnding,
  'Cute illustration, wide overhead shot of a compact circular sushi counter branching visually into several distinct unbranded modern counter layouts, anonymous diners choosing plates, no store names or text, warm light.');
data('now', 'now-s101', 'camera', 'Medium shot, push in', 'Wide shot, overhead drift');
data('now', 'now-s101b', 'prompt', repeatedEnding,
  'Cute illustration, wide shot of many distinct unbranded sushi storefronts across a stylized Japanese town grid, small conveyor motifs visible inside a few windows, no numerals or labels, warm light.');
data('now', 'now-s101b', 'camera', 'Medium shot, drift', 'Wide shot, drift');
data('now', 'now-s102', 'prompt', repeatedEnding,
  'Cute illustration, medium shot over an anonymous diner’s shoulder, one hand weighing a nearby sushi plate against a different plate still approaching on the belt, warm light.');
data('now', 'now-s103', 'prompt', repeatedEnding,
  'Cute illustration, wide shot of an unbranded sushi counter with a few diners sharing a meal and the belt continuing around the corner, clear empty space at upper right for an end-screen overlay, warm light, no text.');
data('now', 'now-s103', 'camera', 'Medium shot, pull out', 'Wide shot, pull out');

for (const key of keys) {
  assert.deepEqual(chapters[key].claims, oldChapters[key].claims, `claim/source/scene mapping drift: ${key}`);
  for (const claim of chapters[key].claims) {
    const target = find(key, claim.scene);
    assert(target.lines.map((line) => line.text).join('').includes(claim.claim), `claim unbound: ${key}/${claim.id}`);
    assert.equal(claim.verdict, 'UNCHECKED', `review verdict drift: ${key}/${claim.id}`);
    assert(Number.isInteger(claim.source) && series.plan.sources[claim.source], `source index: ${key}/${claim.id}`);
  }
}
assert.equal(keys.flatMap((key) => chapters[key].claims).length, 65);
const beforeIds = keys.flatMap((key) => oldChapters[key].scenes.flatMap((scene) => scene.lines.map((line) => line.id)));
const afterIds = keys.flatMap((key) => chapters[key].scenes.flatMap((scene) => scene.lines.map((line) => line.id)));
assert.equal(new Set(afterIds).size, afterIds.length, 'duplicate line IDs');
assert(afterIds.every((id) => beforeIds.includes(id)), 'new line ID');
const removedIds = beforeIds.filter((id) => !afterIds.includes(id));
assert.deepEqual(removedIds.sort(), changes.filter((item) => item.kind === 'drop_repeated_scene').flatMap((item) => item.lines.map((line) => line.id)).sort());

const story = ['# B18 節奏修訂候選（離線、未審）', '',
  '逐鏡旁白；65 筆主張仍全部 UNCHECKED。此檔不是正式 checker、聽眾審稿或配音稿。', '',
  ...keys.flatMap((key) => [`## ${key}｜${chapters[key].title}`, '',
    ...chapters[key].scenes.map((scene) => `- ${scene.id} [${scene.template}] ${scene.lines.map((line) => line.text).join('')}`), ''])].join('\n');

const root = path.resolve(here, '../../../../..');
const { composeStory, cuteStoryVisualProblems } = await import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs')).href);
const { loadProject, lintProject } = await import(pathToFileURL(path.join(root, 'tools/video/core/state.mjs')).href);
const { estimateTimeline } = await import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs')).href);
let externalCalls = 0;
globalThis.fetch = () => { externalCalls++; throw new Error('offline build must not fetch'); };
const slug = 'story-conveyor-belt-sushi-v2';
const voice = read(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'video.json')).voice;
const baseDoc = composeStory({ slug, info: series, chapters: oldChapters, voice, drama: { music_enabled: false }, root });
const doc = composeStory({ slug, info: series, chapters, voice, drama: { music_enabled: false }, root });
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'b18-pacing-'));
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
assert.deepEqual(lint.errors, [], `official lint errors: ${JSON.stringify(lint.errors)}`);
assert.deepEqual(cuteStoryVisualProblems(doc), [], 'cute visual lint errors');
assert.equal(sha(canonical(series)), pins['series.json'], 'proposed source/plan drift');
assert.equal(doc.subtitles.burn_in, false);
assert.deepEqual(doc.look, { preset: 'cute-mystery' });
const shots = doc.scenes.filter((item) => item.template === 'shot').length;
const cards = doc.scenes.filter((item) => item.template === 'title').length;
assert(shots / doc.scenes.length >= .7);
assert.equal(externalCalls, 0);
const timeline = estimateTimeline(doc);
const estimatedBodySeconds = timeline.total_frames / 30;
const baselineBodySeconds = estimateTimeline(baseDoc).total_frames / 30;
assert.equal(baselineBodySeconds, 644.7, 'baseline estimator drift');
const chapterSeconds = Object.fromEntries(keys.map((key, index) => [key, Number(((
  (timeline.chapters[index + 1]?.start_frame ?? timeline.total_frames) - timeline.chapters[index].start_frame
) / 30).toFixed(1))]));
const result = {
  schema_version: 1, status: 'OFFLINE_PACING_CANDIDATE_NOT_REVIEWED',
  base_pins: pins, scenes: doc.scenes.length, lines: afterIds.length,
  removed_scene_ids: changes.filter((item) => item.kind === 'drop_repeated_scene').map((item) => item.scene),
  removed_line_ids: removedIds, claims_unchecked: 65,
  illustrations: shots, cards, illustration_ratio: Number((shots / doc.scenes.length).toFixed(4)),
  open_loops: doc.loops.length, lint_errors: lint.errors, cute_errors: [],
  lint_warnings: lint.warnings.length,
  narrative_warnings: lint.warnings.filter((item) => item.kind === 'narrative'),
  baseline_estimated_body_seconds: baselineBodySeconds,
  estimated_body_seconds: estimatedBodySeconds, assumed_animations_seconds: 26,
  estimated_total_seconds: Number((estimatedBodySeconds + 26).toFixed(1)),
  estimated_body_seconds_saved: Number((baselineBodySeconds - estimatedBodySeconds).toFixed(1)),
  chapter_estimated_seconds: chapterSeconds,
  measured_body_seconds: null, external_calls: externalCalls, worker_pass: false,
};
const output = new Map([
  ['series.json', canonical(series)],
  ['delta.json', canonical({ schema_version: 1, status: result.status, base_pins: pins, changes })],
  ['READABLE-SCRIPT.md', `${story.trimEnd()}\n`],
  ['lint-warnings.json', canonical(lint.warnings)],
  ['verification.json', canonical(result)],
]);
for (const key of keys) output.set(`chapters/${key}.json`, canonical(chapters[key]));
const hashes = Object.fromEntries([
  ['build.mjs', sha(fs.readFileSync(path.join(here, 'build.mjs')))],
  ['README.md', sha(fs.readFileSync(path.join(here, 'README.md')))],
  ...[...output].map(([name, content]) => [name, sha(content)]),
]);
output.set('sha256.json', canonical({ schema_version: 1, files: hashes }));
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
for (const [name, content] of output) {
  const file = path.join(here, name);
  if (mode === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, content);
  } else assert.equal(fs.readFileSync(file, 'utf8'), content, `generated output drift: ${name}`);
}
console.log(JSON.stringify({ scenes: result.scenes, claims_unchecked: 65, estimated_body_seconds: estimatedBodySeconds, estimated_total_seconds: result.estimated_total_seconds, narrative_warnings: result.narrative_warnings, lint_warnings: result.lint_warnings }, null, 2));
