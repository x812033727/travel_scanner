// A01-only offline r14 pacing correction over frozen r13. Never writes outside this directory.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r13 = path.resolve(here, '../A01-editorial-candidate-20261018-r13');
const expected = {
  manifest: '9a2d05a012da83b569181c0a6e69847b4d72858be23861a4210c7b69f115886c',
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const readR13 = (name) => fs.readFileSync(path.join(r13, name));
assert.equal(sha(readR13('manifest.json')), expected.manifest, 'r13 manifest drift');
const r13Manifest = JSON.parse(readR13('manifest.json'));
for (const [name, digest] of Object.entries(r13Manifest.outputs_sha256)) {
  assert.equal(sha(readR13(name)), digest, 'r13 output drift ' + name);
}
assert.equal(sha(readR13('build.mjs')), r13Manifest.build_sha256, 'r13 builder drift');
assert.equal(sha(readR13('README.md')), r13Manifest.readme_sha256, 'r13 README drift');

const before = JSON.parse(readR13('candidate/video.json'));
const video = structuredClone(before);
assert.equal(video.slug, 'story-rolling-suitcase-v2');
assert.deepEqual(video.target_minutes, [7, 8]);
assert.equal(video.scenes.length, 65);
assert.equal(video.sources.length, 18);
const editLine = (sceneId, lineId, oldText, newText, claimIds) => {
  const scenes = video.scenes.filter((scene) => scene.id === sceneId);
  assert.equal(scenes.length, 1, 'scene drift ' + sceneId);
  assert.deepEqual(scenes[0].claims, claimIds, 'claim anchor drift ' + sceneId);
  assert.deepEqual(scenes[0].lines, [{ id: lineId, text: oldText }], 'narration drift ' + sceneId);
  scenes[0].lines[0].text = newText;
};
editLine('turn-05', 'crcw',
  '在另一段時間未明的回憶裡，Plath 排在安檢隊伍中，看見前面的旅客費力拆開箱子和金屬推車。',
  '另一次日期未明的回憶裡，Plath 在安檢隊伍中，看見前方旅客正費力處理箱子和金屬推車。',
  ['t5']);
assert.deepEqual(video.sources, before.sources, 'source list must be unchanged');
assert.deepEqual(video.scenes.map((scene) => scene.id), before.scenes.map((scene) => scene.id), 'scene order drift');
assert.deepEqual(video.scenes.flatMap((scene) => scene.lines.map((line) => line.id)),
  before.scenes.flatMap((scene) => scene.lines.map((line) => line.id)), 'line IDs drift');
const changed = [];
for (let i = 0; i < before.scenes.length; i++) {
  const oldScene = before.scenes[i];
  const newScene = video.scenes[i];
  if (JSON.stringify(oldScene) !== JSON.stringify(newScene)) changed.push(oldScene.id);
  assert.deepEqual(newScene.data, oldScene.data, 'visual drift ' + oldScene.id);
  assert.deepEqual(newScene.claims, oldScene.claims, 'claims drift ' + oldScene.id);
}
assert.deepEqual(changed, ['turn-05'], 'unreviewed scene change');

const claims = readR13('candidate/claims.md');
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
], 'r13 source-precise t5 claim drift');
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
assert.equal(screenplay(before), readR13('candidate/script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r13 script drift');
const script = Buffer.from(screenplay(video));
const series = JSON.parse(readR13('candidate/series.json'));
const lexicon = JSON.parse(readR13('candidate/lexicon.json'));
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

const priorSourceMap = JSON.parse(readR13('source-map.json'));
const sourceMap = {
  status: 'HOLD_PENDING_INDEPENDENT_R14_REVIEW',
  derives_from_r13_manifest_sha256: expected.manifest,
  r13_review_not_inherited: true,
  r13_source_map_status_historical: priorSourceMap.status,
  source_index: priorSourceMap.source_index,
  changed_line_ids: ['crcw'],
  changed_scene_ids: changed,
  claim_ids_rechecked_without_changing_rows: ['t5'],
  fact_guard: 'ABC/USA TODAY 2012 describes people struggling with bags attached to separate metal trolleys at security; r14 sets up the difficulty without claiming a trolley was stuck or preempting the cord-removal detail in turn-06.',
  pacing_guard: 'turn-05 narration names the two objects; turn-security-question asks about joining them; turn-06 narration explains the elastic cords and unloading action. The unchanged turn-05 illustration prompt already shows cords.',
  worker_claim_id_guard: 't7b is an offline claim ID, not a worker numberClaims output; expect a fresh ID and receipt binding after the six host chapters are reconciled.',
  host_source_guard: 'HOLD: reconcile 23 current plan sources with 18 cited r14 sources and the worker 25-source merge before any host adoption; do not inherit r13 review or fabricate a script-review receipt.',
};
assert.deepEqual(sourceMap.source_index, priorSourceMap.source_index, 'source map index drift');
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_PENDING_R14_REVIEW',
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
  independent_full_r14_review: 'NOT_RUN',
  six_chapter_host_bridge: 'NOT_INSTALLED_OR_FORMALLY_REVIEWED',
  worker_claim_id_and_source_merge: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  host_import_or_paid_media: 'NOT_RUN',
};
assert.equal(validation.estimated_300_cpm_in_owner_range, true, 'paper duration outside owner range');
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', readR13('candidate/series.json')],
  ['candidate/lexicon.json', readR13('candidate/lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['validation.json', json(validation)],
  ['plan-source-addition.json', readR13('plan-source-addition.json')],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_EDITORIAL_CANDIDATE',
  slug: video.slug,
  derives_from_r13_manifest_sha256: expected.manifest,
  r13_review_not_inherited: true,
  source_snapshot: r13Manifest.source_snapshot,
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r13_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r14');
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
