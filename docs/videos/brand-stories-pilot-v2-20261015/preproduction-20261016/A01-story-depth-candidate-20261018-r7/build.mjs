// Isolated A01 r7 edit: remove r6's misleading or low-value hooks; preserve r6 bytes.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const r6 = path.resolve(here, '../A01-story-depth-candidate-20261018-r6');
const r5 = path.resolve(here, '../A01-story-depth-candidate-20261018-r5');
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const baseRead = (name) => fs.readFileSync(path.join(here, 'base', name));
const expectedR6Manifest = '2022c21f9f2ef3e41a674e7e7c81568344427dc5a0ab413c6f97ca82a75fcc76';
const r6ManifestBytes = baseRead('r6-manifest.json');
assert.equal(sha(r6ManifestBytes), expectedR6Manifest, 'frozen r6 manifest snapshot drift');
assert.equal(sha(fs.readFileSync(path.join(r6, 'manifest.json'))), expectedR6Manifest, 'frozen r6 manifest drift');
const r6Manifest = JSON.parse(r6ManifestBytes);
const candidateNames = ['video.json', 'series.json', 'lexicon.json', 'script.md', 'claims.md'];
for (const name of candidateNames) {
  const bytes = baseRead(name);
  assert.equal(sha(bytes), r6Manifest.outputs_sha256['candidate/' + name], 'r6 snapshot drift ' + name);
  assert.ok(fs.readFileSync(path.join(r6, 'candidate', name)).equals(bytes), 'r6 candidate drift ' + name);
}
for (const name of ['source-map.json', 'validation.json']) {
  const bytes = baseRead('r6-' + name);
  assert.equal(sha(bytes), r6Manifest.outputs_sha256[name], 'r6 metadata snapshot drift ' + name);
  assert.ok(fs.readFileSync(path.join(r6, name)).equals(bytes), 'r6 metadata drift ' + name);
}
assert.equal(sha(baseRead('r6-README.md')), r6Manifest.readme_sha256, 'r6 README snapshot drift');
assert.ok(fs.readFileSync(path.join(r6, 'README.md')).equals(baseRead('r6-README.md')), 'r6 README drift');

const video = JSON.parse(baseRead('video.json'));
const series = JSON.parse(baseRead('series.json'));
const lexicon = JSON.parse(baseRead('lexicon.json'));
const scene = (id) => {
  const found = video.scenes.filter((item) => item.id === id);
  assert.equal(found.length, 1, 'expected one scene ' + id);
  return found[0];
};
const line = (sceneId, lineId, expected) => {
  const found = scene(sceneId).lines.filter((item) => item.id === lineId);
  assert.equal(found.length, 1, 'expected one line ' + lineId);
  assert.equal(found[0].text, expected, 'r6 line drift ' + lineId);
  return found[0];
};
const dropScene = (id) => {
  const at = video.scenes.findIndex((item) => item.id === id);
  assert.ok(at >= 0, 'missing scene ' + id);
  video.scenes.splice(at, 1);
};
const dropLine = (sceneId, lineId) => {
  const lines = scene(sceneId).lines;
  const at = lines.findIndex((item) => item.id === lineId);
  assert.ok(at >= 0, 'missing line ' + lineId);
  lines.splice(at, 1);
};
const dropLoop = (setup) => {
  const at = video.loops.findIndex((item) => item.setup === setup);
  assert.ok(at >= 0, 'missing loop ' + setup);
  video.loops.splice(at, 1);
};

// One airport scene, two factual actions: carrying cases and spotting a wheel board.
line('hook-01', '3rdw', '波多黎各機場，Sadow 兩手提著沉箱；一台重機器，卻從旁邊滑過。').text =
  '波多黎各機場，Sadow 一手一只提著沉箱；一名男子卻推著重機器，從他身旁過去。';
line('hook-02', 'e37u', '他後來回憶，那人只是推著它，走得比他輕鬆。').text =
  '機器底下是一塊有輪子的板子。Sadow 轉頭對妻子說了一句話。';
scene('hook-02').claims = ['h3'];
scene('hook-02').data.prompt = 'Cute medium-low shot of the same early-1970s Puerto Rico airport. A generic person pushes a heavy machine on a low wheeled board past a traveler holding two plain heavy cases; the traveler turns toward a companion but no dialogue or later suitcase prototype is depicted. Show the wheels clearly, without logos, readable signs, historical portrait likeness or an invented outcome.';
dropScene('hook-02b');
dropScene('hook-03');
assert.ok(!video.loops.some((item) => item.setup === 'e37u'));
video.loops.push({ setup: 'e37u', payoff: 'r14i02', what: 'Sadow 看見輪板後對妻子說要給行李裝輪子' });

// The patent details stay as facts; a normal handle is not an engaging unresolved stake.
dropLine('origin-06', 'r6o02');
dropLoop('r6o02');
const r5VideoBytes = fs.readFileSync(path.join(r5, 'candidate', 'video.json'));
assert.equal(sha(r5VideoBytes), '5b13694801609070313f1e5dbf26823c3bd51f5fa8fbac03d41e174d36f6941c', 'r5 visual snapshot drift');
const r5Video = JSON.parse(r5VideoBytes);
for (const id of ['idea-r12-02', 'idea-r12-06']) {
  const original = r5Video.scenes.find((item) => item.id === id);
  assert.ok(original, 'missing r5 visual ' + id);
  scene(id).data.prompt = original.data.prompt;
}

// The opening already previews the buyer's decision; do not ask it a second time.
dropScene('idea-buyer-question');
dropLoop('r6i01');

// Shiller's personal wobbling bag is separate from Plath's cart. Start the cart
// story only when Plath later recalls seeing it; avoid a second security question.
dropScene('engine-security-question');
dropLoop('r6e01');
dropScene('engine-10b');

// By the next crew shot, the viewer can see who uses the case. Let the action tell it.
dropLine('turn-09', 'r6t02');
dropLoop('r6t02');

// The 1993 reporter tested one bag's stowage. She did not test the 2010 flight
// attendant's claim that easy rolling encourages heavier packing.
dropScene('now-packing-question');
dropLoop('r6n01');
line('now-05', 'opk01', '一位受訪空服員觀察：箱子好推，旅客反而塞得更滿；一旦不能滾，可能就搬不動。').text =
  '多年後，一位受訪空服員觀察：箱子好推，旅客反而塞得更滿；一旦不能滾，可能就搬不動。';

// The 1989 and 1991 company updates belong before the specific 1993 cabin test.
const consumerAt = video.scenes.findIndex((item) => item.id === 'now-consumer-question');
assert.equal(video.scenes[consumerAt - 1].id, 'now-passenger');
assert.equal(video.scenes[consumerAt + 1].id, 'now-11');
assert.equal(video.scenes[consumerAt + 2].id, 'now-12');
const [year1989, year1991] = video.scenes.splice(consumerAt + 1, 2);
video.scenes.splice(consumerAt, 0, year1989, year1991);
assert.deepEqual(video.scenes.slice(consumerAt - 1, consumerAt + 4).map((item) => item.id), ['now-passenger', 'now-11', 'now-12', 'now-consumer-question', 'now-1993-test']);

// R6's mechanically counted micro loops were not editorially durable. Keep their
// underlying facts and questions in the script; drop only the misleading loop rows.
for (const setup of ['r14i02', 'r17e01', '3zwf']) dropLoop(setup);

const claimsLines = baseRead('claims.md').toString('utf8').replace(/\r\n/g, '\n').split('\n');
const claimIndex = (id) => {
  const matches = claimsLines.map((row, index) => row.startsWith(id + '｜') ? index : -1).filter((index) => index >= 0);
  assert.equal(matches.length, 1, 'claim row ' + id);
  return matches[0];
};
claimsLines[claimIndex('h3')] = claimsLines[claimIndex('h3')].replace('｜hook-02b｜', '｜hook-02｜');
for (const id of ['h8', 'e36']) claimsLines.splice(claimIndex(id), 1);
const claimRows = claimsLines.filter((row) => /^[a-z]\d+｜/.test(row));
const claimScene = new Map(video.scenes.flatMap((item) => (item.claims ?? []).map((id) => [id, item.id])));
assert.equal(claimScene.size, video.scenes.reduce((sum, item) => sum + (item.claims ?? []).length, 0), 'duplicate claim ID');
assert.deepEqual(new Set(claimRows.map((row) => row.split('｜', 1)[0])), new Set(claimScene.keys()), 'claim rows must match scenes');
for (const row of claimRows) {
  const cells = row.split('｜');
  assert.equal(cells.length, 6, 'malformed claim row ' + cells[0]);
  assert.equal(cells[4], claimScene.get(cells[0]), 'claim scene mismatch ' + cells[0]);
  assert.equal(cells[5], 'PENDING', 'no inherited approval');
}
const claims = Buffer.from(claimsLines.join('\n'));

const allLines = video.scenes.flatMap((item) => item.lines);
const sceneByLine = new Map(video.scenes.flatMap((item) => item.lines.map((itemLine) => [itemLine.id, item.id])));
assert.equal(sceneByLine.size, allLines.length, 'duplicate line ID');
assert.equal(new Set(video.scenes.map((item) => item.id)).size, video.scenes.length, 'duplicate scene ID');
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
assert.equal(screenplay(JSON.parse(baseRead('video.json'))), baseRead('script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r6 screenplay drift');
const script = Buffer.from(screenplay(video));
const lint = lintVideo(video, { lexicon, brief: fs.readFileSync(path.join(here, '../A01-story-depth-candidate-20261018-r4/base/brief.md'), 'utf8'), translations: {}, others: [], series });
const cute = cuteStoryVisualProblems(video);
const timing = {};
for (const cpm of [250, 275, 300]) {
  const timeline = estimateTimeline(video, cpm);
  const previous = estimateTimeline(JSON.parse(baseRead('video.json')), cpm);
  const sceneIndex = new Map(video.scenes.map((item, index) => [item.id, index]));
  const lineTime = new Map(timeline.lines.map((item) => [item.id, item]));
  const bodyStart = timeline.chapters[1].start_frame / 30;
  const outroId = video.scenes.find((item) => item.template === 'outro')?.id;
  const bodyEnd = timeline.scenes.find((item) => item.id === outroId).start_frame / 30;
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
    const gaps = points.slice(1).map((item, index) => ({ from: points[index].id, to: item.id, seconds: Number((item.at - points[index].at).toFixed(1)) }));
    return { max_gap_seconds: Math.max(...gaps.map((item) => item.seconds)), gaps_over_45_seconds: gaps.filter((item) => item.seconds > 45), devices: points.map((item) => ({ at: Number(item.at.toFixed(1)), id: item.id })) };
  };
  const declaredQuestions = video.loops.map((loop) => loop.setup).filter((id) => /[？?]\s*$/.test(allLines.find((item) => item.id === id)?.text ?? ''));
  const allQuestions = allLines.filter((item) => /[？?]\s*$/.test(item.text)).map((item) => item.id);
  const sourceEvents = ['r12o01', 'r12o02', 'r3o01', '83ew', 'r14i02', 'dgbq', 'zaky', 'j9sw', 's7me', 'amrq', 'r17e02', 'r15t07', 'crcw', 'q4zn', '3zwf', 'r15n01', 'jspd', 'r3n02', 'r3n05', 'r4n01', '7asx'];
  timing[cpm] = {
    r6_seconds: Number((previous.total_frames / 30).toFixed(1)),
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
  derives_from_r6_manifest_sha256: expectedR6Manifest,
  source_snapshot: r6Manifest.source_snapshot,
  prior_review_not_inherited: true,
  changed_line_ids: ['3rdw', 'e37u', 'opk01'],
  removed_scene_ids: ['hook-02b', 'hook-03', 'idea-buyer-question', 'engine-security-question', 'engine-10b', 'now-packing-question'],
  removed_claim_ids: ['h8', 'e36'],
  removed_line_ids: ['avqs', 'wibh', 'r6o02', 'r6i01', 'r6e01', 'r16e01', 'r6t02', 'r6n01'],
  moved_scene_ids_before_cabin_question: ['now-11', 'now-12'],
  visual_changes: ['hook-02: reveal wheel board and withheld wife reply', 'idea-r12-02 and idea-r12-06: restore r5 patent illustrations', 'now-consumer-question remains an answer-hidden cabin-space image'],
  added_opening_loop: { setup: 'e37u', payoff: 'r14i02', source: 'https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469', scope: 'Sadow recounts what he told his wife after seeing the wheeled machine; withheld words, not fabricated dialogue' },
  cut_r6_loops: ['r6o02', 'r6i01', 'r6e01', 'r6t02', 'r6n01', 'r14i02', 'r17e01', '3zwf'],
  retained_new_r6_loops: ['r6o01', 'r6t01'],
  attribution_guard: 'The 1993 LA Times one-reporter packing case is not evidence that easy rolling caused heavy packing. The later flight-attendant observation is expressly introduced as her separate observation.',
  chronology_guard: 'Emmer’s undated sketch anecdote remains separate from Plath’s independently recounted security-cart incident. The 1989/1991 company chronology now precedes the 1993 cabin-stowage question.',
  caveats: [
    '1939 Midland report proves one wheeled-case appearance, not identity with the 1928 homemade case.',
    'Travelpro says 1987 while Plath’s 2024 first-person alumni entry says 1988; r7 retains the existing attributed Travelpro wording only.',
    'Sadow retail refusal is his retrospective; guard OK is Plath’s account of one encounter; neither is a universal claim.',
    'The source-event cadence is a selected text proxy, not a blind listening result or real narration timing.',
  ],
  host_migration: 'SPEC_ONLY_SIX_CHAPTER_SOURCES_AND_SERIES_PLAN_REQUIRE_SEPARATE_REVIEW',
};
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_UNREVIEWED',
  source_snapshot: r6Manifest.source_snapshot,
  derives_from_r6_manifest_sha256: expectedR6Manifest,
  scenes: video.scenes.length,
  lines: allLines.length,
  claims: claimRows.length,
  loops: video.loops.length,
  narration_spoken_units: allLines.reduce((sum, item) => sum + spokenUnits(item.text), 0),
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
  derives_from_r6_manifest_sha256: expectedR6Manifest,
  source_snapshot: r6Manifest.source_snapshot,
  base_sha256: Object.fromEntries(['r6-manifest.json', 'r6-source-map.json', 'r6-validation.json', 'r6-README.md', ...candidateNames].map((name) => [name, sha(baseRead(name))])),
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...outputs].map(([name, bytes]) => [name, sha(bytes)])),
  r6_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
outputs.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of outputs) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r7');
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
