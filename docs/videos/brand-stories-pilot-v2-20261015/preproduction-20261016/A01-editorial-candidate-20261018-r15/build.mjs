// A01-only offline r15 visual-reveal correction over frozen r14. Never writes outside this directory.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r14 = path.resolve(here, '../A01-editorial-candidate-20261018-r14');
const expected = {
  manifest: 'b0f44ac19ff6a449113570a9fe0ccc20667d9093eef383219c95a8ce2dae9231',
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const readR14 = (name) => fs.readFileSync(path.join(r14, name));
assert.equal(sha(readR14('manifest.json')), expected.manifest, 'r14 manifest drift');
const r14Manifest = JSON.parse(readR14('manifest.json'));
for (const [name, digest] of Object.entries(r14Manifest.outputs_sha256)) {
  assert.equal(sha(readR14(name)), digest, 'r14 output drift ' + name);
}
assert.equal(sha(readR14('build.mjs')), r14Manifest.build_sha256, 'r14 builder drift');
assert.equal(sha(readR14('README.md')), r14Manifest.readme_sha256, 'r14 README drift');

const before = JSON.parse(readR14('candidate/video.json'));
const video = structuredClone(before);
assert.equal(video.slug, 'story-rolling-suitcase-v2');
assert.deepEqual(video.target_minutes, [7, 8]);
assert.equal(video.scenes.length, 65);
assert.equal(video.sources.length, 18);
const editPrompt = (sceneId, oldPrompt, newPrompt, claimIds, lineId, lineText) => {
  const scenes = video.scenes.filter((scene) => scene.id === sceneId);
  assert.equal(scenes.length, 1, 'scene drift ' + sceneId);
  assert.deepEqual(scenes[0].claims, claimIds, 'claim anchor drift ' + sceneId);
  assert.deepEqual(scenes[0].lines, [{ id: lineId, text: lineText }], 'narration drift ' + sceneId);
  assert.equal(scenes[0].data.visual, 'still', 'not a still ' + sceneId);
  assert.equal(scenes[0].data.prompt, oldPrompt, 'visual prompt drift ' + sceneId);
  scenes[0].data.prompt = newPrompt;
};
editPrompt('turn-05',
  'Cute wide shot at a generic 1980s airport security queue. A plain-clothed traveler ahead of an anonymous middle-aged pilot pauses at the checkpoint, beginning to unhook elastic cords from an unbranded suitcase strapped to a separate bulky metal luggage trolley. Show the pilot behind observing this specific difficulty; rope barriers and soft overhead light. Keep suitcase and trolley visibly separate. Do not show screws, a joined prototype, a guard, a cleared gate, a future design, words, logos or real-person likeness.',
  'Cute wide establishing still at a period-neutral airport security queue, clearly an illustration rather than archival evidence. An anonymous traveler pauses with an unbranded hard suitcase resting on a separate bulky metal luggage trolley; an anonymous pilot observes from behind. A waist-height wide frame shows the suitcase body and the trolley wheels and handle as two distinct objects, while the traveler and a foreground queue barrier naturally hide every strap, cord, knot, fastening point and any unloading action. Keep hands away from the hidden connection. No joined prototype, security-worker response, cleared gate, specific year markers, words, logos or real-person likeness.',
  ['t5'], 'crcw', '另一次日期未明的回憶裡，Plath 在安檢隊伍中，看見前方旅客正費力處理箱子和金屬推車。');
editPrompt('turn-security-question',
  'Cute close-up at a generic 1980s airport checkpoint: an anonymous traveler pauses beside a hard suitcase still tied to a separate metal trolley. Focus on the joint and the inspection line; do not show anyone untying it, an integrated prototype, a cleared gate or a guard reply. No logos, words or real-person likeness.',
  'Cute medium over-the-shoulder still in the same period-neutral airport security queue, looking past an anonymous pilot toward a traveler with an unbranded hard suitcase on a separate bulky metal luggage trolley. Keep both object silhouettes clear, but frame the contact area behind a foreground queue rail and the traveler\'s coat so no straps, bungee cords, knots, screws or joined prototype can be seen. Show a pause before any answer, not an unloading action. No security-worker reply, gate clearance, passage through the checkpoint, precise year markers, words, logos or real-person likeness.',
  [], 'r6t01', '如果把兩樣東西鎖在一起，安檢員會讓它過嗎？');
assert.deepEqual(video.sources, before.sources, 'source list must be unchanged');
assert.deepEqual(video.scenes.map((scene) => scene.id), before.scenes.map((scene) => scene.id), 'scene order drift');
assert.deepEqual(video.scenes.flatMap((scene) => scene.lines.map((line) => line.id)),
  before.scenes.flatMap((scene) => scene.lines.map((line) => line.id)), 'line IDs drift');
const changed = [];
for (let i = 0; i < before.scenes.length; i++) {
  const oldScene = before.scenes[i];
  const newScene = video.scenes[i];
  if (JSON.stringify(oldScene) !== JSON.stringify(newScene)) changed.push(oldScene.id);
  assert.deepEqual(newScene.lines, oldScene.lines, 'narration drift ' + oldScene.id);
  assert.equal(newScene.data.visual, oldScene.data.visual, 'visual route drift ' + oldScene.id);
  assert.equal(newScene.data.camera, oldScene.data.camera, 'camera drift ' + oldScene.id);
  if (newScene.data.prompt !== oldScene.data.prompt) {
    assert.ok(['turn-05', 'turn-security-question'].includes(oldScene.id), 'unexpected prompt change ' + oldScene.id);
  } else {
    assert.deepEqual(newScene.data, oldScene.data, 'visual drift ' + oldScene.id);
  }
  assert.deepEqual(newScene.claims, oldScene.claims, 'claims drift ' + oldScene.id);
}
assert.deepEqual(changed, ['turn-05', 'turn-security-question'], 'unreviewed scene change');

const claims = readR14('candidate/claims.md');
const claimRows = claims.toString('utf8').replace(/\r\n/g, '\n').split('\n')
  .filter((row) => /^[a-z]\d+[a-z]?｜/.test(row));
const claimEntries = claimRows.map((row) => row.split('｜'));
assert.equal(claimEntries.length, 78);
const t5 = claimEntries.find((cells) => cells[0] === 't5');
assert.deepEqual(t5, [
  't5',
  'Plath 受訪回憶在安檢排隊，看見前方旅客解彈力繩、將箱子從外置金屬推車卸下；與 Emmer 未標年份的草圖記憶無法排定先後',
  'https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603',
  '2026-09-28', 'turn-05', 'PENDING',
], 'r14 source-precise t5 claim drift');
const sceneByClaim = new Map(video.scenes.flatMap((scene) => (scene.claims ?? []).map((id) => [id, scene.id])));
assert.equal(sceneByClaim.size, 78, 'claim IDs must be unique');
assert.deepEqual(new Set(claimEntries.map((cells) => cells[0])), new Set(sceneByClaim.keys()), 'claim rows / scene IDs mismatch');
for (const cells of claimEntries) {
  assert.equal(cells.length, 6, 'malformed claim ' + cells[0]);
  assert.equal(cells[4], sceneByClaim.get(cells[0]), 'claim scene mismatch ' + cells[0]);
  assert.equal(cells[5], 'PENDING', 'no formal verdict can be inherited');
}
const citedUrls = new Set(claimEntries.map((cells) => cells[2]).filter(Boolean));
assert.deepEqual(citedUrls, new Set(video.sources.map((source) => source.url)));
assert.equal(citedUrls.size, 18);

const [{ screenplay }, { estimateTimeline, spokenUnits }, { lintVideo }, { cuteStoryVisualProblems }] = await Promise.all([
  import(pathToFileURL(path.join(repo, 'tools/video/core/screenplay.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/core/timeline.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/core/lint.mjs'))),
  import(pathToFileURL(path.join(repo, 'tools/video/automation/story.mjs'))),
]);
assert.equal(screenplay(before), readR14('candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r14 script drift');
const script = Buffer.from(screenplay(video));
const series = JSON.parse(readR14('candidate/series.json'));
const lexicon = JSON.parse(readR14('candidate/lexicon.json'));
const lintContext = {
  lexicon,
  brief: fs.readFileSync(path.join(here, '../A01-story-depth-candidate-20261018-r4/base/brief.md'), 'utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(video, lintContext);
const lintAt300 = lintVideo(video, { ...lintContext, cpm: 300 });
const cute = cuteStoryVisualProblems(video);
assert.equal(lint.errors.length, 0, 'video lint errors ' + JSON.stringify(lint.errors));
assert.equal(lintAt300.errors.length, 0, '300-CPM lint errors ' + JSON.stringify(lintAt300.errors));
assert.equal(cute.length, 0, 'cute visual errors ' + JSON.stringify(cute));
const seconds = Object.fromEntries([250, 275, 300].map((cpm) => [cpm, Number((estimateTimeline(video, cpm).total_frames / 30).toFixed(1))]));
const lines = video.scenes.flatMap((scene) => scene.lines);
assert.equal(lines.length, 77);

const priorSourceMap = JSON.parse(readR14('source-map.json'));
const sourceMap = {
  status: 'HOLD_PENDING_INDEPENDENT_R15_REVIEW',
  derives_from_r14_manifest_sha256: expected.manifest,
  r14_review_not_inherited: true,
  r14_source_map_status_historical: priorSourceMap.status,
  source_index: priorSourceMap.source_index,
  changed_line_ids: [],
  changed_scene_ids: changed,
  changed_visual_scene_ids: changed,
  claim_ids_rechecked_without_changing_rows: ['t5'],
  fact_guard: 'ABC/USA TODAY 2012 describes people struggling with bags attached to separate metal trolleys at security. The prompts are editorial illustrations, not archival reconstruction or proof of an exact date.',
  visual_reveal_guard: 'turn-05 and turn-security-question show two distinct objects while blocking straps, joints and unloading; turn-06 keeps the first cord-and-unloading close-up. Neither earlier still depicts a guard response or cleared checkpoint.',
  worker_claim_id_guard: 't7b is an offline claim ID, not a worker numberClaims output; expect a fresh ID and receipt binding after the six host chapters are reconciled.',
  host_source_guard: 'HOLD: reconcile 23 current plan sources with 18 cited r15 sources and the worker 25-source merge before any host adoption; do not inherit r14 review or fabricate a script-review receipt.',
};
assert.deepEqual(sourceMap.source_index, priorSourceMap.source_index, 'source map index drift');
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_PENDING_R15_REVIEW',
  target_body_seconds: [420, 480],
  scenes: video.scenes.length,
  lines: lines.length,
  claims: claimEntries.length,
  loops: video.loops.length,
  spoken_units: lines.reduce((sum, line) => sum + spokenUnits(line.text), 0),
  estimated_body_seconds_not_tts: seconds,
  estimated_300_cpm_in_owner_range: seconds[300] >= 420 && seconds[300] <= 480,
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_errors_at_300_cpm: lintAt300.errors,
  cute_visual_errors: cute,
  public_sources: video.sources.length,
  claim_source_urls: citedUrls.size,
  source_index_matches_claims: true,
  measured_tts_and_cut: 'NOT_RUN',
  independent_full_r15_review: 'NOT_RUN',
  six_chapter_host_bridge: 'NOT_INSTALLED_OR_FORMALLY_REVIEWED',
  worker_claim_id_and_source_merge: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  host_import_or_paid_media: 'NOT_RUN',
};
assert.equal(validation.estimated_300_cpm_in_owner_range, true, 'paper duration outside owner range');
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', readR14('candidate/series.json')],
  ['candidate/lexicon.json', readR14('candidate/lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['validation.json', json(validation)],
  ['plan-source-addition.json', readR14('plan-source-addition.json')],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE',
  slug: video.slug,
  derives_from_r14_manifest_sha256: expected.manifest,
  r14_review_not_inherited: true,
  source_snapshot: r14Manifest.source_snapshot,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r14_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r15');
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), 'missing output ' + name);
    assert.ok(fs.readFileSync(file).equals(bytes), 'stale output ' + name);
  }
}
console.log(JSON.stringify({ action, status: validation.status, scenes: validation.scenes, lines: validation.lines,
  claims: validation.claims, sources: validation.public_sources, spoken_units: validation.spoken_units,
  seconds_250: seconds[250], seconds_275: seconds[275], seconds_300: seconds[300],
  lint_errors: lint.errors.length, cute_errors: cute.length }));
