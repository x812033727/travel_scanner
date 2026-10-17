// Isolated A01 r8: three incremental corrections to frozen r7; no production work.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r7 = path.resolve(here, '../A01-story-depth-candidate-20261018-r7');
const expectedR7Manifest = '37b1fd3fb4e7c67a1dde34d00a854d02a3e09b1dd2995d418b4ebce1767a2a8b';
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const baseRead = (name) => fs.readFileSync(path.join(here, 'base', name));
const candidateNames = ['video.json', 'series.json', 'lexicon.json', 'script.md', 'claims.md'];

const manifestBytes = baseRead('r7-manifest.json');
assert.equal(sha(manifestBytes), expectedR7Manifest, 'r7 manifest snapshot drift');
assert.equal(sha(fs.readFileSync(path.join(r7, 'manifest.json'))), expectedR7Manifest, 'live r7 manifest drift');
const r7Manifest = JSON.parse(manifestBytes);
for (const name of candidateNames) {
  const bytes = baseRead(name);
  assert.equal(sha(bytes), r7Manifest.outputs_sha256['candidate/' + name], 'r7 snapshot drift ' + name);
  assert.ok(fs.readFileSync(path.join(r7, 'candidate', name)).equals(bytes), 'live r7 candidate drift ' + name);
}
for (const name of ['source-map.json', 'validation.json']) {
  const bytes = baseRead('r7-' + name);
  assert.equal(sha(bytes), r7Manifest.outputs_sha256[name], 'r7 metadata snapshot drift ' + name);
  assert.ok(fs.readFileSync(path.join(r7, name)).equals(bytes), 'live r7 metadata drift ' + name);
}
assert.equal(sha(baseRead('r7-README.md')), r7Manifest.readme_sha256, 'r7 README snapshot drift');
assert.ok(fs.readFileSync(path.join(r7, 'README.md')).equals(baseRead('r7-README.md')), 'live r7 README drift');

const video = JSON.parse(baseRead('video.json'));
const series = JSON.parse(baseRead('series.json'));
const lexicon = JSON.parse(baseRead('lexicon.json'));
const scene = (id) => {
  const rows = video.scenes.filter((entry) => entry.id === id);
  assert.equal(rows.length, 1, 'expected one scene ' + id);
  return rows[0];
};
const line = (sceneId, id, before) => {
  const rows = scene(sceneId).lines.filter((entry) => entry.id === id);
  assert.equal(rows.length, 1, 'expected one line ' + id);
  assert.equal(rows[0].text, before, 'r7 line drift ' + id);
  return rows[0];
};

// Shiller's personally used four-caster strap case and Plath's later problem
// are separate stories. Neither source says the latter used the former's bag.
line('turn-04', '8wiw', '另一位決定動手的人，是西北航空的 747 機師 Robert Plath。').text =
  'Shiller 說的是他自己的拖帶箱。接下來，西北航空的 747 機師 Robert Plath，碰上另一種行李難題。';

// The prior image showed only the pilot. The source says people ahead of him
// struggled to remove suitcases from external carts at airport security.
const oldTurn05Prompt = 'Wide shot at a 1980s airport security checkpoint queue. One generic middle-aged pilot in a plain dark jacket with no insignia stands waiting in line, his face showing a clear curious expression as he looks ahead. Plain rope barriers frame the long queue. Soft overcast light.';
assert.equal(scene('turn-05').data.prompt, oldTurn05Prompt, 'r7 turn-05 visual drift');
scene('turn-05').data.prompt = 'Cute wide shot at a generic 1980s airport security queue. A plain-clothed traveler ahead of an anonymous middle-aged pilot pauses at the checkpoint, beginning to unhook elastic cords from an unbranded suitcase strapped to a separate bulky metal luggage trolley. Show the pilot behind observing this specific difficulty; rope barriers and soft overhead light. Keep suitcase and trolley visibly separate. Do not show screws, a joined prototype, a guard, a cleared gate, a future design, words, logos or real-person likeness.';

const openingLoop = video.loops.filter((entry) => entry.setup === 'r17h01' && entry.payoff === 'r3o01');
assert.equal(openingLoop.length, 1, 'r7 Anita loop drift');
assert.equal(openingLoop[0].what, '父親嘲笑後，1939 年報紙仍記錄 Anita 帶輪箱出席講座', 'r7 Anita what drift');
openingLoop[0].what = '旅後是否仍帶輪箱；1939 年一場茶會報導記她身旁有輪箱';

const claimsLines = baseRead('claims.md').toString('utf8').replace(/\r\n/g, '\n').split('\n');
const replaceClaim = (id, before, after) => {
  const matches = claimsLines.map((row, index) => row.startsWith(id + '｜') ? index : -1).filter((index) => index >= 0);
  assert.equal(matches.length, 1, 'claim row ' + id);
  assert.equal(claimsLines[matches[0]], before, 'r7 claim drift ' + id);
  claimsLines[matches[0]] = after;
};
replaceClaim('t4',
  't4｜Robert Plath 是西北航空 747 機師，後來自行設計輪子行李箱｜https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage｜2026-09-28｜turn-04｜PENDING',
  't4｜Robert Plath 是西北航空 747 機師，後來自行設計輪子行李箱；此段另起其經歷，沒有證據把他與 Shiller 的個人箱子接成同一實物或影響鏈｜https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage｜2026-09-28｜turn-04｜PENDING');
replaceClaim('t5',
  't5｜Plath 受訪回憶自己在安檢排隊看見前方旅客被外置金屬推車困住；與 Emmer 未標年份的草圖記憶無法排定先後｜https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603｜2026-09-28｜turn-05｜PENDING',
  't5｜Plath 受訪回憶在安檢排隊，看見前方旅客解彈力繩、將箱子從外置金屬推車卸下；與 Emmer 未標年份的草圖記憶無法排定先後｜https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603｜2026-09-28｜turn-05｜PENDING');
const claimRows = claimsLines.filter((row) => /^[a-z]\d+｜/.test(row));
const claimScene = new Map(video.scenes.flatMap((entry) => (entry.claims ?? []).map((id) => [id, entry.id])));
assert.equal(claimScene.size, video.scenes.reduce((sum, entry) => sum + (entry.claims ?? []).length, 0), 'duplicate claim ID');
assert.deepEqual(new Set(claimRows.map((row) => row.split('｜', 1)[0])), new Set(claimScene.keys()), 'claim rows must match scenes');
for (const row of claimRows) {
  const cells = row.split('｜');
  assert.equal(cells.length, 6, 'malformed claim row ' + cells[0]);
  assert.equal(cells[4], claimScene.get(cells[0]), 'claim scene mismatch ' + cells[0]);
  assert.equal(cells[5], 'PENDING', 'no inherited approval');
}
const claims = Buffer.from(claimsLines.join('\n'));

const allLines = video.scenes.flatMap((entry) => entry.lines);
const sceneByLine = new Map(video.scenes.flatMap((entry) => entry.lines.map((item) => [item.id, entry.id])));
assert.equal(sceneByLine.size, allLines.length, 'duplicate line ID');
assert.equal(new Set(video.scenes.map((entry) => entry.id)).size, video.scenes.length, 'duplicate scene ID');
for (const loop of video.loops) {
  assert.ok(sceneByLine.has(loop.setup) && sceneByLine.has(loop.payoff), 'missing loop line ' + loop.setup);
  assert.notEqual(sceneByLine.get(loop.setup), sceneByLine.get(loop.payoff), 'same-scene loop ' + loop.setup);
}
const module = (relative) => import(pathToFileURL(path.join(repo, relative)));
const [{ screenplay }, { estimateTimeline, spokenUnits }, { lintVideo }, { cuteStoryVisualProblems }] = await Promise.all([
  module('tools/video/core/screenplay.mjs'),
  module('tools/video/core/timeline.mjs'),
  module('tools/video/core/lint.mjs'),
  module('tools/video/automation/story.mjs'),
]);
assert.equal(screenplay(JSON.parse(baseRead('video.json'))), baseRead('script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r7 screenplay drift');
const script = Buffer.from(screenplay(video));
const lint = lintVideo(video, { lexicon, brief: fs.readFileSync(path.join(here, '../A01-story-depth-candidate-20261018-r4/base/brief.md'), 'utf8'), translations: {}, others: [], series });
const cute = cuteStoryVisualProblems(video);
const timing = {};
for (const cpm of [250, 275, 300]) {
  const timeline = estimateTimeline(video, cpm);
  const previous = estimateTimeline(JSON.parse(baseRead('video.json')), cpm);
  const sceneIndex = new Map(video.scenes.map((entry, index) => [entry.id, index]));
  const lineTime = new Map(timeline.lines.map((entry) => [entry.id, entry]));
  const bodyStart = timeline.chapters[1].start_frame / 30;
  const outroId = video.scenes.find((entry) => entry.template === 'outro')?.id;
  const bodyEnd = timeline.scenes.find((entry) => entry.id === outroId).start_frame / 30;
  const first = sceneIndex.get(timeline.chapters[1].scene);
  const last = sceneIndex.get(outroId);
  const cadence = (ids) => {
    const points = [{ at: bodyStart, id: 'body:start' }];
    for (const id of ids) {
      const entry = lineTime.get(id);
      const index = sceneIndex.get(sceneByLine.get(id));
      if (entry && index >= first && index < last) points.push({ at: entry.end_frame / 30, id });
    }
    points.sort((a, b) => a.at - b.at);
    points.push({ at: bodyEnd, id: 'body:end' });
    const gaps = points.slice(1).map((entry, index) => ({ from: points[index].id, to: entry.id, seconds: Number((entry.at - points[index].at).toFixed(1)) }));
    return { max_gap_seconds: Math.max(...gaps.map((entry) => entry.seconds)), gaps_over_45_seconds: gaps.filter((entry) => entry.seconds > 45), devices: points.map((entry) => ({ at: Number(entry.at.toFixed(1)), id: entry.id })) };
  };
  const declaredQuestions = video.loops.map((loop) => loop.setup).filter((id) => /[？?]\s*$/.test(allLines.find((entry) => entry.id === id)?.text ?? ''));
  const allQuestions = allLines.filter((entry) => /[？?]\s*$/.test(entry.text)).map((entry) => entry.id);
  const sourceEvents = ['r12o01', 'r12o02', 'r3o01', '83ew', 'r14i02', 'dgbq', 'zaky', 'j9sw', 's7me', 'amrq', 'r17e02', 'r15t07', 'crcw', 'q4zn', '3zwf', 'r15n01', 'jspd', 'r3n02', 'r3n05', 'r4n01', '7asx'];
  timing[cpm] = {
    r7_seconds: Number((previous.total_frames / 30).toFixed(1)),
    candidate_seconds: Number((timeline.total_frames / 30).toFixed(1)),
    shortfall_to_540_seconds: Number((540 - timeline.total_frames / 30).toFixed(1)),
    six_chapter_seconds: timeline.chapters.map((chapter, index) => ({ scene_id: chapter.scene, seconds: Number((((timeline.chapters[index + 1]?.start_frame ?? timeline.total_frames) - chapter.start_frame) / 30).toFixed(1)) })),
    loops: video.loops.map((loop) => ({ setup: loop.setup, payoff: loop.payoff, gap_seconds: Number(((lineTime.get(loop.payoff).start_frame - lineTime.get(loop.setup).end_frame) / 30).toFixed(1)) })),
    declared_loop_question_cadence_45: cadence(declaredQuestions),
    all_voiced_question_cadence_45: cadence(allQuestions),
    source_event_proxy_cadence_45_unreviewed: cadence(sourceEvents),
  };
}
const sourceMap = {
  status: 'PENDING_INDEPENDENT_REVIEW',
  derives_from_r7_manifest_sha256: expectedR7Manifest,
  source_snapshot: r7Manifest.source_snapshot,
  prior_review_not_inherited: true,
  changed_line_ids: ['8wiw'],
  changed_visual_scene_ids: ['turn-05'],
  changed_loop_setup_ids: ['r17h01'],
  changed_claim_ids: ['t4', 't5'],
  source_links: [
    { id: 'e38', url: 'https://oyc.yale.edu/economics/econ-252-08/lecture-3', scope: 'Shiller personally used a four-caster strap case; no Plath use or influence established.' },
    { id: 'e39', url: 'https://oyc.yale.edu/economics/econ-252-11/lecture-3', scope: 'General older-case turning limitation; not Plath’s security-cart story.' },
    { id: 't4', url: 'https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage', scope: 'Plath was a Northwest Airlines 747 pilot; narrative transitions to a separate person.' },
    { id: 't5', url: 'https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603', scope: 'Plath recalls travelers in front taking cases off separate trolleys and elastic cords at security; turn-05 shows the beginning of that action, not his later prototype or guard reply.' },
    { id: 'o34', url: 'https://newspapers.swco.ttu.edu/bitstreams/b9cd84b8-2ba7-4506-9eff-7cca3e5c6376/download', scope: '1939 report describes one wheeled-case appearance beside Anita at one event; it cannot identify the 1928 physical case or prove continuous use.' },
  ],
  chronology_guard: 'The Emmer undated crew-bag anecdote and Plath undated security-cart anecdote remain separate recollections; neither is ordered or caused by the other.',
  image_guard: 'turn-05 shows the travelers ahead beginning to undo elastic cords and unload a case from an external trolley; no screws, joined prototype, guard, or clearance.',
  loop_guard: 'r17h01 asks only whether Anita later carried a wheeled case; r3o01 pays off only the single 1939 appearance, without using the father response absent from the opening or asserting same-case identity.',
  host_migration: 'SPEC_ONLY_SIX_CHAPTER_SOURCES_AND_SERIES_PLAN_REQUIRE_SEPARATE_REVIEW',
};
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_UNREVIEWED',
  source_snapshot: r7Manifest.source_snapshot,
  derives_from_r7_manifest_sha256: expectedR7Manifest,
  scenes: video.scenes.length,
  lines: allLines.length,
  claims: claimRows.length,
  loops: video.loops.length,
  narration_spoken_units: allLines.reduce((sum, entry) => sum + spokenUnits(entry.text), 0),
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_warnings: lint.warnings,
  cute_visual_errors: cute,
  estimated_timing_not_tts: timing,
  duration_540_gate: 'HOLD',
  strict_45_second_gate: 'HOLD',
  source_event_45_second_gate: timing[300].source_event_proxy_cadence_45_unreviewed.max_gap_seconds <= 45 ? 'UNREVIEWED_PROXY_ONLY' : 'HOLD',
  independent_fact_review: 'NOT_RUN',
  independent_listener_review: 'NOT_RUN',
  independent_visual_review: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  actual_tts_or_media: 'NOT_RUN',
  production_or_paid_work: 'NOT_RUN',
};
const outputs = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', baseRead('series.json')],
  ['candidate/lexicon.json', baseRead('lexicon.json')],
  ['candidate/script.md', script],
  ['candidate/claims.md', claims],
  ['source-map.json', json(sourceMap)],
  ['validation.json', json(validation)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  slug: video.slug,
  derives_from_r7_manifest_sha256: expectedR7Manifest,
  source_snapshot: r7Manifest.source_snapshot,
  base_sha256: Object.fromEntries(['r7-manifest.json', 'r7-source-map.json', 'r7-validation.json', 'r7-README.md', ...candidateNames].map((name) => [name, sha(baseRead(name))])),
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r7_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r8');
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), 'missing output ' + name);
    assert.ok(fs.readFileSync(file).equals(bytes), 'stale output ' + name);
  }
}
assert.equal(lint.errors.length, 0, 'video lint errors');
assert.equal(cute.length, 0, 'cute visual errors');
console.log(JSON.stringify({ action, status: validation.status, scenes: validation.scenes, lines: validation.lines, claims: validation.claims, loops: validation.loops, spoken_units: validation.narration_spoken_units, seconds_250: timing[250].candidate_seconds, seconds_275: timing[275].candidate_seconds, seconds_300: timing[300].candidate_seconds, all_question_gap_300: timing[300].all_voiced_question_cadence_45.max_gap_seconds, declared_question_gap_300: timing[300].declared_loop_question_cadence_45.max_gap_seconds, source_event_proxy_gap_300: timing[300].source_event_proxy_cadence_45_unreviewed.max_gap_seconds, duration_540_gate: validation.duration_540_gate, strict_45_second_gate: validation.strict_45_second_gate, lint_errors: lint.errors.length, cute_errors: cute.length }));
