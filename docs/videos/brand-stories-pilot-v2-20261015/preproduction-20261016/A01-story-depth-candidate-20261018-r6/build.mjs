// Isolated A01 r6 hook edit. r5 and every production capture remain immutable.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r5 = path.resolve(here, '../A01-story-depth-candidate-20261018-r5');
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const baseRead = (name) => fs.readFileSync(path.join(here, 'base', name));
const r5ManifestBytes = baseRead('r5-manifest.json');
const expectedR5Manifest = '8acaa2c01f210dea99dc44e703be1caa90e30ecfe502e55ef247c5584e2abf3e';
assert.equal(sha(r5ManifestBytes), expectedR5Manifest, 'frozen r5 manifest snapshot drift');
assert.equal(sha(fs.readFileSync(path.join(r5, 'manifest.json'))), expectedR5Manifest, 'frozen r5 manifest drift');
const r5Manifest = JSON.parse(r5ManifestBytes);
const candidateNames = ['video.json', 'series.json', 'lexicon.json', 'script.md', 'claims.md'];
for (const name of candidateNames) {
  const bytes = baseRead(name);
  assert.equal(sha(bytes), r5Manifest.outputs_sha256['candidate/' + name], 'r5 snapshot drift: ' + name);
  assert.ok(fs.readFileSync(path.join(r5, 'candidate', name)).equals(bytes), 'r5 candidate drift: ' + name);
}
for (const name of ['source-map.json', 'validation.json']) {
  const bytes = baseRead('r5-' + name);
  assert.equal(sha(bytes), r5Manifest.outputs_sha256[name], 'r5 snapshot drift: ' + name);
  assert.ok(fs.readFileSync(path.join(r5, name)).equals(bytes), 'r5 metadata drift: ' + name);
}
assert.equal(sha(baseRead('r5-README.md')), r5Manifest.readme_sha256, 'r5 README snapshot drift');
assert.ok(fs.readFileSync(path.join(r5, 'README.md')).equals(baseRead('r5-README.md')), 'r5 README drift');

const video = JSON.parse(baseRead('video.json'));
const series = JSON.parse(baseRead('series.json'));
const lexicon = JSON.parse(baseRead('lexicon.json'));
const scene = (id) => {
  const found = video.scenes.filter((item) => item.id === id);
  assert.equal(found.length, 1, 'expected one scene ' + id);
  return found[0];
};
const exact = (sceneId, lineId, expected) => {
  const found = scene(sceneId).lines.filter((item) => item.id === lineId);
  assert.equal(found.length, 1, 'expected one line ' + lineId);
  assert.equal(found[0].text, expected, 'r5 line drift ' + lineId);
  return found[0];
};
const addAfter = (sceneId, afterId, id, text) => {
  const lines = scene(sceneId).lines;
  const at = lines.findIndex((item) => item.id === afterId);
  assert.ok(at >= 0 && !lines.some((item) => item.id === id), 'bad insertion ' + id);
  lines.splice(at + 1, 0, { id, text });
};
const insertSceneAfter = (afterId, newScene) => {
  const at = video.scenes.findIndex((item) => item.id === afterId);
  assert.ok(at >= 0 && !video.scenes.some((item) => item.id === newScene.id), 'bad scene insertion ' + newScene.id);
  video.scenes.splice(at + 1, 0, newScene);
};
const addLoop = (setup, payoff, what) => {
  assert.ok(!video.loops.some((item) => item.setup === setup), 'duplicate setup ' + setup);
  video.loops.push({ setup, payoff, what });
};

// Keep the father's documented objection as a later, genuinely new 1928 beat.
exact('hook-anita', 'r17h01', '1928 年，兒子替箱子裝了輪子，父親卻笑他們。旅程結束後，母親還會帶輪子箱出門嗎？').text =
  '1928 年，安妮塔的兒子把舊嬰兒車輪裝上箱子。旅程結束後，她還會帶輪子箱出門嗎？';
scene('hook-anita').data.prompt = 'Cute illustrative late-1920s railway platform. An anonymous mother and four children stand beside a small homemade suitcase with two old stroller wheels and a wooden pull handle, about to begin a journey. Keep the father and his later reaction out of frame. This is an illustration, not an identified surviving suitcase or real-person portrait. No completed voyage, 1939 lecture, readable text, logos or spoiler.';
addAfter('origin-r12-01', 'r12o01', 'r6o01', '輪子裝上去後，同行的丈夫會跟著拉嗎？');
addLoop('r6o01', 'r12o02', '丈夫是否接受妻兒的輪子箱；後來仍寧願手提並嘲笑');

// The Sadow patent gives this practical question a later, document-backed answer.
addAfter('origin-06', '83ew', 'r6o02', '如果給箱子裝輪子，原來提箱的手把，還能留下嗎？');
addLoop('r6o02', 'r12e06', 'Sadow 專利把拉箱拖帶與原有手提把分開保留');
scene('idea-r12-02').data.prompt = 'Medium side view of a plain closed mid-century suitcase on a neutral workbench. Show the lid/body seam and opening direction as the object of this beat; crop the top carrying handle, which is revealed with the pull-strap answer in the next shot. The underside stays hidden. Gentle side lamp light, no hands, text, logos or real-person likeness.';
scene('idea-r12-06').data.prompt = 'Close-up of a plain old suitcase end and top: an anonymous hand fastens a soft pull strap to the metal loop near the end wall, while the original top carrying handle remains visible and separate. Show both ways of moving the same case without turning it into a modern telescoping case. No text, logo or real-person likeness.';

// Ask about the response to the actual dog-leash-looking sample, not a made-up sales result.
exact('idea-14', '768x', '報導形容，那條繩子就像牽狗的繩子。').text =
  '報導形容，那條繩子就像牽狗的繩子。';
insertSceneAfter('idea-14', {
  id: 'idea-buyer-question', template: 'shot',
  data: { prompt: 'Cute close view of a plain 1970s wheeled suitcase and its rope resting on a luggage-factory floor, as if ready to be shown to a buyer. No store, buyer reaction, rejection, sale, readable text, logo or real-person likeness.', camera: 'push in', visual: 'still' },
  claims: [], lines: [{ id: 'r6i01', text: '百貨採購會怎麼看這種拉法？' }],
});
addLoop('r6i01', '9ijb', '採購看見繩拖箱的拉法後，認為荒唐並拒絕');

// Distinguish the Shiller and Plath examples; then let the guard answer later.
insertSceneAfter('engine-10b', {
  id: 'engine-security-question', template: 'shot',
  data: { prompt: 'Cute illustrative late-1980s airport security approach: a plain hard suitcase is still strapped to a separate metal trolley just before inspection. Keep the joint removable and show neither a new integrated design nor the guard answer. No words, logos, real-person likeness or false historic prototype.', camera: 'track right', visual: 'still' },
  claims: [], lines: [{ id: 'r6e01', text: '到了安檢得拆開，能讓箱子和推車一路不分家嗎？' }],
});
addLoop('r6e01', 'q4zn', 'Plath 回憶將外置推車與硬箱鎖成一體');
insertSceneAfter('turn-05', {
  id: 'turn-security-question', template: 'shot',
  data: { prompt: 'Cute close-up at a generic 1980s airport checkpoint: an anonymous traveler pauses beside a hard suitcase still tied to a separate metal trolley. Focus on the joint and the inspection line; do not show anyone untying it, an integrated prototype, a cleared gate or a guard reply. No logos, words or real-person likeness.', camera: 'push in', visual: 'still' },
  claims: [], lines: [{ id: 'r6t01', text: '如果把兩樣東西鎖在一起，安檢員會讓它過嗎？' }],
});
addLoop('r6t01', 'r13t02', '安檢員要求拆卸後聽到無法拆，最後只答 OK');
addAfter('turn-09', 'jm3w', 'r6t02', '誰會先把它拉到旅客眼前？');
addLoop('r6t02', 'r15n01', '先在機組間使用，再被航站旅客看見');

// The early picture poses a cabin-space question. Packing happens only at the later test.
scene('now-consumer-question').data.prompt = 'Cute early-1990s preflight illustration: an anonymous traveler with a plain, moderately packed two-wheel carry-on looks from a narrow aircraft aisle toward the closed overhead bin and the space beneath a seat. A small folded jacket and two generic paperback books are nearby, not yet placed in the expandable exterior pocket. Keep that pocket flat and do not show whether the bag fits, any bin outcome, a shop display, readable text, logos or real-person likeness.';
insertSceneAfter('now-1993-test', {
  id: 'now-packing-question', template: 'shot',
  data: { prompt: 'Cute close side view of a plain two-wheel carry-on rolling smoothly through a generic early-1990s airport concourse. Emphasize easy motion while hiding its contents and exterior pocket; do not show packing, an overfilled bag, a cabin-stowage result, readable text, logos or real-person likeness.', camera: 'track right', visual: 'still' },
  claims: [], lines: [{ id: 'r6n01', text: '箱子越好推，旅客會不會反而裝得更滿？' }],
});
addLoop('r6n01', 'opk01', '受訪空服員觀察旅客因能滾而多裝，不能滾時反而搬不動');

const allLines = video.scenes.flatMap((item) => item.lines);
const sceneByLine = new Map(video.scenes.flatMap((item) => item.lines.map((line) => [line.id, item.id])));
assert.equal(sceneByLine.size, allLines.length, 'duplicate line ID');
assert.equal(new Set(video.scenes.map((item) => item.id)).size, video.scenes.length, 'duplicate scene ID');
const changedLineIds = ['r17h01'];
const addedLineIds = ['r6o01', 'r6o02', 'r6i01', 'r6e01', 'r6t01', 'r6t02', 'r6n01'];
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
assert.equal(screenplay(JSON.parse(baseRead('video.json'))), baseRead('script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r5 screenplay drift');
const script = Buffer.from(screenplay(video));
const lint = lintVideo(video, { lexicon, brief: fs.readFileSync(path.join(here, '../A01-story-depth-candidate-20261018-r4/base/brief.md'), 'utf8'), translations: {}, others: [], series });
const cute = cuteStoryVisualProblems(video);
const timing = {};
for (const cpm of [250, 275, 300]) {
  const timeline = estimateTimeline(video, cpm);
  const previous = estimateTimeline(JSON.parse(baseRead('video.json')), cpm);
  const lineTime = new Map(timeline.lines.map((item) => [item.id, item]));
  const bodyStart = timeline.chapters[1].start_frame / 30;
  const outroId = video.scenes.find((item) => item.template === 'outro')?.id;
  const bodyEnd = timeline.scenes.find((item) => item.id === outroId).start_frame / 30;
  const sceneIndex = new Map(video.scenes.map((item, index) => [item.id, index]));
  const bodyFirstIndex = sceneIndex.get(timeline.chapters[1].scene);
  const bodyEndIndex = sceneIndex.get(outroId);
  const cadence = (ids) => {
    const points = [{ at: bodyStart, id: 'body:start' }];
    for (const id of ids) {
      const entry = lineTime.get(id);
      const index = sceneIndex.get(sceneByLine.get(id));
      if (entry && index >= bodyFirstIndex && index < bodyEndIndex) points.push({ at: entry.end_frame / 30, id });
    }
    points.sort((a, b) => a.at - b.at);
    points.push({ at: bodyEnd, id: 'body:end' });
    const gaps = points.slice(1).map((item, index) => ({ from: points[index].id, to: item.id, seconds: Number((item.at - points[index].at).toFixed(1)) }));
    return { max_gap_seconds: Math.max(...gaps.map((item) => item.seconds)), gaps_over_45_seconds: gaps.filter((item) => item.seconds > 45), devices: points.map((item) => ({ at: Number(item.at.toFixed(1)), id: item.id })) };
  };
  const questionIds = video.loops.map((loop) => loop.setup).filter((id) => /[？?]\s*$/.test(allLines.find((line) => line.id === id)?.text ?? ''));
  const actionIds = ['r12o01', 'r12o02', 'r3o01', '83ew', 'r14i02', 'dgbq', 'zaky', 'j9sw', 's7me', 'amrq', 'r17e02', 'r16e01', 'r15t07', 'crcw', 'q4zn', '3zwf', 'r15n01', 'r3n02', 'r3n05', 'r4n01', '7asx'];
  timing[cpm] = {
    r5_seconds: Number((previous.total_frames / 30).toFixed(1)),
    candidate_seconds: Number((timeline.total_frames / 30).toFixed(1)),
    shortfall_to_540_seconds: Number((540 - timeline.total_frames / 30).toFixed(1)),
    six_chapter_seconds: timeline.chapters.map((chapter, index) => ({ scene_id: chapter.scene, seconds: Number((((timeline.chapters[index + 1]?.start_frame ?? timeline.total_frames) - chapter.start_frame) / 30).toFixed(1)) })),
    loops: video.loops.map((loop) => ({ setup: loop.setup, payoff: loop.payoff, gap_seconds: Number(((lineTime.get(loop.payoff).start_frame - lineTime.get(loop.setup).end_frame) / 30).toFixed(1)) })),
    declared_loop_question_cadence_45: cadence(questionIds),
    all_voiced_question_cadence_45: cadence(allLines.filter((line) => /[？?]\s*$/.test(line.text)).map((line) => line.id)),
    sourced_event_proxy_cadence_45_unreviewed: cadence(actionIds),
  };
}
const loopSummary = video.loops.map((loop) => ({ ...loop, setup_scene: sceneByLine.get(loop.setup), payoff_scene: sceneByLine.get(loop.payoff), explicit_question: /[？?]\s*$/.test(allLines.find((line) => line.id === loop.setup).text), timing_300_gap_seconds: timing[300].loops.find((item) => item.setup === loop.setup).gap_seconds, verdict: 'PENDING_BLIND_LISTENING_AND_VISUAL_REVIEW' }));
const sourceMap = {
  status: 'PENDING_INDEPENDENT_REVIEW',
  derives_from_r5_manifest_sha256: expectedR5Manifest,
  source_snapshot: r5Manifest.source_snapshot,
  prior_review_not_inherited: true,
  changed_line_ids: changedLineIds,
  added_line_ids: addedLineIds,
  changed_visual_scene_ids: ['hook-anita', 'idea-r12-02', 'idea-r12-06', 'now-consumer-question'],
  added_scene_ids: ['idea-buyer-question', 'engine-security-question', 'turn-security-question', 'now-packing-question'],
  hooks: [
    { setup: 'r6o01', payoff: 'r12o02', source: 'https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/', limit: 'father reaction moved out of opening; not a new historical fact' },
    { setup: 'r6o02', payoff: 'r12e06', source: 'https://patents.google.com/patent/US3653474A/en', limit: 'patent retains the ordinary carrying handle; picture must not reveal it before narration' },
    { setup: 'r6i01', payoff: '9ijb', source: 'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469', limit: 'buyer rejection is Sadow retrospective, not an independently recovered purchase record' },
    { setup: 'r6e01', payoff: 'q4zn', source: 'https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603', limit: 'Shiller four-caster bag and Plath trolley are separate objects; no claimed influence' },
    { setup: 'r6t01', payoff: 'r13t02', source: 'https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603', limit: 'specific Plath recollection, no claim that all security desks accepted it' },
    { setup: 'r6t02', payoff: 'r15n01', source: 'https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf', limit: '2010 NYT retrospective reprinted on p.48, not a contemporary passenger study' },
    { setup: 'r6n01', payoff: 'opk01', source: 'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469', limit: 'one flight attendant observation, not universal travel behavior' },
  ],
  loops: loopSummary,
  review_warnings: [
    'The 1939 Midland case cannot be identified as the 1928 homemade case; r6 changes no line to claim that identity.',
    'Travelpro says 1987; Plath 2024 first-person alumni entry says 1988. Existing attributed line stays attributed; independent conflict review remains open.',
    'The security-cart anecdote and Emmer sketch anecdote have no verified relative chronology and must not be narrated as cause and effect.',
    'Some new loops are short local turns. Counting them mechanically does not establish that blind listeners experience them as suspense.',
    'The event cadence is an explicitly selected, unreviewed proxy; a blind listener and actual TTS timestamps are still required.',
  ],
  host_migration: 'SPEC_ONLY_SIX_CHAPTER_SOURCES_AND_SERIES_PLAN_REQUIRE_SEPARATE_REVIEW',
};
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_UNREVIEWED',
  source_snapshot: r5Manifest.source_snapshot,
  derives_from_r5_manifest_sha256: expectedR5Manifest,
  scenes: video.scenes.length,
  lines: allLines.length,
  claims: video.scenes.reduce((sum, item) => sum + (item.claims ?? []).length, 0),
  loops: video.loops.length,
  added_loops: addedLineIds.length,
  narration_spoken_units: allLines.reduce((sum, line) => sum + spokenUnits(line.text), 0),
  changed_line_ids: changedLineIds,
  added_line_ids: addedLineIds,
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_warnings: lint.warnings,
  cute_visual_errors: cute,
  estimated_timing_not_tts: timing,
  duration_540_gate: 'HOLD',
  strict_45_second_gate: timing[300].declared_loop_question_cadence_45.max_gap_seconds <= 45 ? 'ESTIMATE_ONLY_PENDING_LISTENING' : 'HOLD',
  source_event_45_second_gate: timing[300].sourced_event_proxy_cadence_45_unreviewed.max_gap_seconds <= 45 ? 'UNREVIEWED_PROXY_ONLY' : 'HOLD',
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
  ['candidate/claims.md', baseRead('claims.md')],
  ['source-map.json', json(sourceMap)],
  ['validation.json', json(validation)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  slug: video.slug,
  derives_from_r5_manifest_sha256: expectedR5Manifest,
  source_snapshot: r5Manifest.source_snapshot,
  base_sha256: Object.fromEntries(['r5-manifest.json', 'r5-source-map.json', 'r5-validation.json', 'r5-README.md', ...candidateNames].map((name) => [name, sha(baseRead(name))])),
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r5_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r6');
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
console.log(JSON.stringify({ action, status: validation.status, scenes: validation.scenes, lines: validation.lines, spoken_units: validation.narration_spoken_units, seconds_250: timing[250].candidate_seconds, seconds_275: timing[275].candidate_seconds, seconds_300: timing[300].candidate_seconds, declared_loop_question_gap_300: timing[300].declared_loop_question_cadence_45.max_gap_seconds, all_voiced_question_gap_300: timing[300].all_voiced_question_cadence_45.max_gap_seconds, source_event_proxy_gap_300: timing[300].sourced_event_proxy_cadence_45_unreviewed.max_gap_seconds, duration_540_gate: validation.duration_540_gate, strict_45_second_gate: validation.strict_45_second_gate, lint_errors: lint.errors.length, lint_warnings: lint.warnings.length, cute_errors: cute.length }));
