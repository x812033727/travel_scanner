import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { additions } from './additions.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const previous = path.resolve(here, '../A01-round11-candidate');
const round10 = path.resolve(here, '../A01-round10-candidate');
const chaptersInOrder = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (file) => fs.readFileSync(file);
const parse = (file) => JSON.parse(read(file).toString('utf8'));
const output = new Map();
const addOutput = (name, value) => output.set(name, Buffer.from(json(value)));

const previousManifest = parse(path.join(previous, 'manifest.json'));
const sourceDelta = parse(path.join(here, 'source-delta.json'));
assert.equal(previousManifest.status, 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE');
assert.equal(sourceDelta.status, 'OFFLINE_UNREVIEWED_SOURCE_DELTA');
assert.equal(sourceDelta.source_additions.length, 1);
assert.equal(sourceDelta.fact_additions.length, 4);

const series = parse(path.join(round10, 'evidence/round9-series.json'));
assert.equal(series.plan.sources.length, 12);
assert.equal(series.plan.must_verify.length, 10);
for (const update of sourceDelta.source_updates) {
  const prior = series.plan.sources[update.index];
  assert.ok(prior?.url?.startsWith('https://'), `source ${update.index}`);
  prior.supports = `${prior.supports}；${update.supports_append}`;
  prior.checked = sourceDelta.checked_on;
}
series.plan.sources.push(...sourceDelta.source_additions);
series.plan.must_verify.push(...sourceDelta.fact_additions);
assert.equal(series.plan.sources.length, 13);
assert.equal(series.plan.must_verify.length, 14);
for (const [key, extra] of Object.entries(sourceDelta.chapter_point_append)) {
  const chapter = series.plan.chapters[chaptersInOrder.indexOf(key)];
  assert.ok(chapter && chaptersInOrder.indexOf(key) >= 0);
  chapter.point = `${chapter.point}\n\n${extra}`;
}
series.plan.caveats = `${series.plan.caveats}\n\n${sourceDelta.caveat_append}`;

const chapters = {};
const baseHashes = {};
const ids = new Set();
const lineIds = new Set();
const claimIds = new Set();
for (const key of chaptersInOrder) {
  const file = path.join(previous, 'candidate/chapters', `${key}.json`);
  const bytes = read(file);
  baseHashes[key] = sha(bytes);
  assert.equal(baseHashes[key], previousManifest.candidate_chapters_sha256[key], `round11 ${key} hash`);
  const chapter = JSON.parse(bytes.toString('utf8'));
  assert.equal(chapter.key, key);
  for (const scene of chapter.scenes) {
    assert.ok(!ids.has(scene.id), `duplicate base scene ${scene.id}`);
    ids.add(scene.id);
    for (const line of scene.lines) {
      assert.ok(!lineIds.has(line.id), `duplicate base line ${line.id}`);
      lineIds.add(line.id);
    }
  }
  for (const claim of chapter.claims) {
    assert.ok(!claimIds.has(claim.id), `duplicate base claim ${claim.id}`);
    claimIds.add(claim.id);
  }
  chapters[key] = chapter;
}

const sourceMap = [];
for (const addition of additions) {
  const chapter = chapters[addition.chapter];
  assert.ok(chapter, `unknown chapter ${addition.chapter}`);
  const after = chapter.scenes.findIndex((scene) => scene.id === addition.after);
  assert.ok(after >= 0, `missing ${addition.chapter}/${addition.after}`);
  assert.ok(!ids.has(addition.id), `duplicate scene ${addition.id}`);
  assert.ok(!lineIds.has(addition.lineId), `duplicate line ${addition.lineId}`);
  const claimId = `claim-${addition.lineId}`;
  assert.ok(!claimIds.has(claimId), `duplicate claim ${claimId}`);
  assert.ok(addition.prompt && !/\b(?:Sadow|Plath|Anita|Macy's|Travelpro|Rollaboard|Samsonite|Silhouette)\b/i.test(addition.prompt), `named image ${addition.id}`);
  assert.ok(Number.isInteger(addition.source) && series.plan.sources[addition.source], `bad source ${addition.id}`);
  assert.ok(Number.isInteger(addition.fact) && series.plan.must_verify[addition.fact], `bad fact ${addition.id}`);
  assert.ok(addition.pin && addition.support, `missing source pin ${addition.id}`);
  if (addition.secondary) {
    assert.ok(Number.isInteger(addition.secondary.source) && series.plan.sources[addition.secondary.source], `bad secondary source ${addition.id}`);
    assert.ok(addition.secondary.pin, `missing secondary pin ${addition.id}`);
  }
  const scene = {
    id: addition.id,
    template: 'shot',
    data: { prompt: addition.prompt, camera: addition.camera, visual: 'still' },
    lines: [{ id: addition.lineId, text: addition.text }],
  };
  chapter.scenes.splice(after + 1, 0, scene);
  chapter.claims.push({
    id: claimId,
    claim: addition.text,
    scene: addition.id,
    source: addition.source,
    fact: addition.fact,
    verdict: 'PENDING',
    note: `Round12 authored offline; ${addition.support}; ${addition.pin}.${addition.secondary ? ` Second source: ${addition.secondary.pin}.` : ''} The independent verifier has not ruled on this line.`,
  });
  chapter.report = 'Round12 offline source-bound authoring candidate. Inherited round11 reports are historical. Every new line and every inherited line require a fresh independent fact/listener/narrative panel on the exact candidate; no media or host adoption is authorized.';
  ids.add(addition.id);
  lineIds.add(addition.lineId);
  claimIds.add(claimId);
  sourceMap.push({
    chapter: addition.chapter,
    scene_id: addition.id,
    line_id: addition.lineId,
    text: addition.text,
    claim_id: claimId,
    source_index: addition.source,
    source_url: series.plan.sources[addition.source].url,
    secondary_source_index: addition.secondary?.source,
    secondary_source_url: addition.secondary ? series.plan.sources[addition.secondary.source].url : undefined,
    secondary_source_location: addition.secondary?.pin,
    source_location: addition.pin,
    support_type: addition.support,
    fact_index: addition.fact,
    verdict: 'PENDING_INDEPENDENT_REVIEW',
  });
}
assert.equal(additions.length, sourceMap.length);
assert.equal(additions.length, 16);

// The collection account needs a legible chronology. Reorder only the first
// eight origin scenes; all later scenes keep their inherited order.
const originPrefix = ['origin-r12-01', 'origin-03', 'origin-01', 'origin-01b', 'origin-02', 'origin-r12-02', 'origin-r12-03', 'origin-06'];
const originScenesById = new Map(chapters.origin.scenes.map((item) => [item.id, item]));
assert.deepEqual(chapters.origin.scenes.slice(0, originPrefix.length).map((item) => item.id).sort(), [...originPrefix].sort());
chapters.origin.scenes = [...originPrefix.map((id) => originScenesById.get(id)), ...chapters.origin.scenes.filter((item) => !originPrefix.includes(item.id))];

const [{ composeStory, cuteStoryVisualProblems }, { lintVideo }, { estimateTimeline, spokenUnits }] = await Promise.all([
  import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/lint.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs'))),
]);

const revisions = [
  { chapter: 'origin', scene: 'origin-03', line: 'csdd', claim: 'o2', expected: '兒子拆下舊嬰兒車的兩個輪子，裝到箱子的一頭。', text: '館方說，兒子把舊嬰兒車的兩輪裝在箱子一端。', source: 8, fact: 5, pin: 'Before Her Time, paragraph beginning “Why be a human truck horse?”, son Bud fashions the case with two baby-carriage wheels and a telescoping wooden handle' },
  { chapter: 'origin', scene: 'origin-01', line: 'zc7k', claim: 'o22', expected: '1928 年，母親拉著兒子做的箱子出發；輪子有了，這卻還是一家人的自製品。', text: '據館方記載，1928 年安妮塔拉著兒子做的輪子箱出發；它仍是一家人的自製品。', source: 8, fact: 5, pin: 'Before Her Time, opening on her homemade rolling trunk and paragraph on the 1928–1930 second world tour' },
  { chapter: 'origin', scene: 'origin-01b', line: '6b28', claim: 'o1', expected: '畫家 Anita Willets-Burnham 一家六口，正展開第二次環遊世界。', text: '館方說，畫家 Anita Willets-Burnham 帶著一家六口，展開第二次環遊世界。', source: 8, fact: 5, pin: 'Before Her Time, opening on artist Anita leading her family of six on two world tours; 1928–1930 second trip' },
  { chapter: 'origin', scene: 'origin-02', line: '4prs', claim: 'o17', expected: '沿途要換船、搭火車、換住處，每到一站，行李都得跟著搬。', text: '館方記述，沿途要換船、搭火車、換住處；每到一站，行李都得跟著搬。', source: 8, fact: null, pin: 'Before Her Time, paragraph on transporting luggage between shipping ports, train stations and housing' },
  { chapter: 'origin', scene: 'origin-06', line: '83ew', claim: 'o20', expected: '開頭那只自製箱沒有消失，歷史學會的館藏裡留著它。', text: '溫尼特卡歷史學會的館藏裡，如今還留著那只自製輪子箱。', source: 8, fact: null, pin: 'Before Her Time, object caption “Anita Willets-Burnham’s suitcase, WHS Object ID 2005.26.576”' },
  { chapter: 'turn', scene: 'turn-12', line: '6jx3', claim: 't13', expected: '到了 1991 年，Plath 離開航空公司，改為全職經營 Travelpro。', text: '同在 1991 年，照 Travelpro 的說法，Plath 離開航空公司，全職經營這個品牌。', source: 1, fact: 7, pin: 'Travelpro, “The History of Rolling Luggage,” A Summation of Wheeled Suitcase History, 1991 bullet' },
];
let revisedUnitsDelta = 0;
for (const revision of revisions) {
  const chapter = chapters[revision.chapter];
  const scene = chapter.scenes.find((item) => item.id === revision.scene);
  const line = scene?.lines.find((item) => item.id === revision.line);
  const claim = chapter.claims.find((item) => item.id === revision.claim);
  assert.equal(line?.text, revision.expected, `inherited line ${revision.line}`);
  assert.ok(claim && claim.scene === revision.scene, `inherited claim ${revision.claim}`);
  line.text = revision.text;
  revisedUnitsDelta += spokenUnits(revision.text) - spokenUnits(revision.expected);
  if (revision.line === '6jx3') {
    assert.deepEqual(scene.lines.map((item) => item.id), ['3tsp', '6jx3']);
    const passengerClaim = chapter.claims.find((item) => item.id === 't12');
    assert.ok(passengerClaim && passengerClaim.scene === revision.scene && passengerClaim.source === 2 && passengerClaim.verdict === 'CONFIRMED');
    assert.equal(passengerClaim.claim, scene.lines[0].text.replace(/[。.!！]$/, ''));
    claim.claim = revision.text;
  } else {
    claim.claim = scene.lines.map((item) => item.text).join(' ');
  }
  claim.source = revision.source;
  claim.fact = revision.fact;
  claim.verdict = 'PENDING';
  claim.note = `Round12 revised and reordered inherited narration; ${revision.pin}. Fresh independent review required; prior verdict is historical.`;
  sourceMap.push({
    chapter: revision.chapter,
    scene_id: revision.scene,
    line_id: revision.line,
    previous_text: revision.expected,
    text: revision.text,
    claim_id: revision.claim,
    origin: 'modified_inherited_line',
    source_index: revision.source,
    source_url: series.plan.sources[revision.source].url,
    source_location: revision.pin,
    support_type: 'direct',
    claim_scope: revision.line === '6jx3' ? 'line_only; 3tsp remains under t12/source 2' : undefined,
    fact_index: revision.fact,
    verdict: 'PENDING_INDEPENDENT_REVIEW',
  });
}
assert.equal(revisions.length, 6);
assert.equal(sourceMap.length, 22);
const familyScene = chapters.origin.scenes.find((item) => item.id === 'origin-01b');
assert.ok(familyScene?.data.prompt.startsWith('Wide shot of a quiet railway platform in the late 1920s. One generic woman'));
familyScene.data.prompt = 'Wide shot of a quiet railway platform in the late 1920s. One anonymous mother in a plain travel coat leads five anonymous family members, an adult and four children, toward a waiting train while pulling one old leather suitcase with two small wheels and a wooden handle. The rolling case and family group occupy the middle third in diffuse daylight. No readable signs, text, logos or likeness to real people.';
sourceMap.find((item) => item.line_id === '6b28').visual_prompt_changed = true;
const originAssembly = chapters.origin.scenes.find((item) => item.id === 'origin-03');
assert.ok(originAssembly?.data.prompt.includes('with a screwdriver'));
originAssembly.data.prompt = 'Close-up of a late-1920s home table. A pair of old baby-carriage wheels is visibly fitted to one end of a plain worn suitcase; an anonymous family member’s hands steady the case and a sliding wooden handle is at its other end. Show the documented parts without inventing a fastening method. Warm lamp light, no tools, screws, readable words, logos or likeness to a real person.';
sourceMap.find((item) => item.line_id === 'csdd').visual_prompt_changed = true;
const earlyNineties = chapters.turn.scenes.find((item) => item.id === 'turn-12');
assert.ok(earlyNineties?.data.prompt.includes('modern airport departure hall'));
earlyNineties.data.prompt = 'Medium shot of an early-1990s terminal, not a reconstruction of a specific day. In the foreground an anonymous civilian rolls a plain upright two-wheel suitcase; beside the route, an unmarked airline pilot cap rests on a modest desk next to several unbranded cases, suggesting a move from flying to full-time luggage work. Period clothing and terminal furnishings, no identified person, readable signs, text or logos.';
sourceMap.find((item) => item.line_id === '6jx3').visual_prompt_changed = true;

// Round11's five NOT FOUND rows are retained as historical verdicts in its
// immutable base. Four scenes are retired; n14 points at a live physical line
// after its flight-attendant attribution was removed. Reconcile current rows
// without treating the newly located sources as fresh verifier approval.
const inheritedClaimReconciliation = [
  { chapter: 'origin', id: 'o7', oldScene: 'origin-09', source: 9,
    pin: 'US2392926A, DESCRIPTION, opening paragraph on scarce railroad-terminal porters and hardship for women and men',
    note: 'Round11 NOT FOUND provenance retained: original source-absence rationale is contradicted by Kelly US2392926A DESCRIPTION. origin-09 is retired; do not restore its narration without a new review.',
    active: false },
  { chapter: 'engine', id: 'e11', oldScene: 'engine-04', source: 0,
    pin: 'US3653474A, BACKGROUND OF THE INVENTION, air, rail and bus terminals',
    note: 'Round11 NOT FOUND provenance retained: original source-absence rationale is contradicted by Sadow US3653474A BACKGROUND. engine-04 is retired; round12 r12e01 independently rewords the terminal point and remains PENDING.',
    active: false },
  { chapter: 'engine', id: 'e3', oldScene: 'engine-05', source: 0,
    pin: 'US3653474A, BACKGROUND OF THE INVENTION, perhaps biggest single difficulty for an air passenger',
    note: 'Round11 NOT FOUND provenance retained: original source-absence rationale is contradicted by Sadow US3653474A BACKGROUND. engine-05 is retired; the superlative is not restored to round12 narration.',
    active: false },
  { chapter: 'now', id: 'n13', oldScene: 'now-05', source: 6,
    pin: 'ABC News 2010, “The Suitcase With Wheels Turns 40,” Heather Poole interview on overstuffed rolling luggage',
    note: 'Round11 NOT FOUND provenance retained: original source-absence rationale is contradicted by the ABC News 2010 first-hand Heather Poole interview. now-05 is retired; the quotation is not restored.',
    active: false },
  { chapter: 'now', id: 'n14', oldScene: 'now-06', source: 6,
    pin: 'ABC News 2010, “The Suitcase With Wheels Turns 40,” Heather Poole interview; retained tszs is an unattributed physical observation',
    note: 'Round11 NOT FOUND rejected a removed flight-attendant attribution, but its source-absence rationale is contradicted by the ABC News 2010 Heather Poole interview. now-06/tszs remains active as a separate general physical sentence; this rebound claim is PENDING independent review, not approved.',
    active: true },
];
for (const item of inheritedClaimReconciliation) {
  const chapter = chapters[item.chapter];
  const claim = chapter.claims.find((row) => row.id === item.id);
  const scene = chapter.scenes.find((row) => row.id === item.oldScene);
  assert.ok(claim && claim.scene === item.oldScene && claim.source === item.source && claim.verdict === 'NOT FOUND', `inherited claim ${item.id}`);
  assert.equal(Boolean(scene), item.active, `scene presence ${item.id}`);
  const prior = { claim: claim.claim, verdict: claim.verdict, note: claim.note };
  claim.note = item.note;
  if (item.id === 'n14') {
    assert.deepEqual(scene.lines.map((line) => line.id), ['tszs']);
    claim.claim = scene.lines[0].text;
    claim.verdict = 'PENDING';
  }
  item.historical = prior;
  item.current = { claim: claim.claim, verdict: claim.verdict, note: claim.note };
  item.source_url = series.plan.sources[item.source].url;
}
const turnIds = chapters.turn.scenes.map((item) => item.id);
assert.ok(turnIds.indexOf('turn-09') < turnIds.indexOf('turn-11'));
assert.ok(turnIds.indexOf('turn-11') < turnIds.indexOf('turn-r12-01'));
assert.ok(turnIds.indexOf('turn-r12-01') < turnIds.indexOf('turn-r12-11'));
assert.ok(turnIds.indexOf('turn-r12-11') < turnIds.indexOf('turn-12'));
assert.ok(!turnIds.includes('turn-r12-02') && !turnIds.includes('turn-r12-03'));
assert.ok(!chapters.engine.scenes.flatMap((item) => item.lines).some((line) => line.text.includes('1974')));

for (const key of chaptersInOrder) addOutput(`candidate/chapters/${key}.json`, chapters[key]);
addOutput('candidate/series.json', series);
addOutput('source-map.json', {
  status: 'PENDING_INDEPENDENT_REVIEW',
  base: 'A01-round11-candidate',
  date: sourceDelta.checked_on,
  notes: [
    '16 lines are new in round12. Six inherited lines are reworded and the first eight origin scenes are rearranged to follow question, construction, departure, response, lecture and collection. All other inherited narration stays unchanged. The current claim bound to active now-06/tszs is separately rebound as PENDING.',
    'The 1974 Samsonite source stays in the unspoken source notes. engine-13/w9bj remains byte-identical to round11.',
    'Sadow 1970 filing and Plath 1989 filing describe proposed structures, not independently observed sales or exact 1987 prototype parts.',
    'The authoring pass read the Winnetka official-domain indexed copy after direct browser fetch timed out. A separate independent reader fetched the official page on 2026-10-16 05:23:44–48 UTC: HTTP 200, raw body 123873 bytes, SHA-256 0219df34bcd52f93ff9346883ad865af9e9a0c65e2efba87079d62dcaefb1fb4. The 1933 travelogue pages were not directly checked, and review of this exact revised candidate is still pending.',
    'PENDING is an offline marker. This file is neither an independent verifier result nor a script-review receipt.',
  ],
  lines: sourceMap,
  inherited_claim_reconciliation: inheritedClaimReconciliation,
});

const archivedVideo = parse(path.join(round10, 'evidence/round9-composed-video.json'));
const makePreview = (info, allChapters) => composeStory({
  slug: previousManifest.slug,
  info,
  chapters: allChapters,
  voice: archivedVideo.voice,
  drama: { music_enabled: Boolean(archivedVideo.music) },
  root,
  videoId: archivedVideo.youtube.video_id ?? null,
});
const preview = makePreview(series, chapters);
const baseSeries = parse(path.join(round10, 'evidence/round9-series.json'));
const baseChapters = Object.fromEntries(chaptersInOrder.map((key) => [key, parse(path.join(previous, 'candidate/chapters', `${key}.json`))]));
const basePreview = makePreview(baseSeries, baseChapters);
const context = {
  lexicon: parse(path.join(round10, 'evidence/round9-lexicon.json')),
  brief: read(path.join(round10, 'evidence/round9-brief.md')).toString('utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(preview, context);
const cute = cuteStoryVisualProblems(preview);
const timing = {};
for (const cpm of [250, 300, 320, 340]) {
  const baseline = estimateTimeline(basePreview, cpm);
  const current = estimateTimeline(preview, cpm);
  const starts = current.chapters.map((item) => item.start_frame);
  timing[String(cpm)] = {
    base_seconds: baseline.total_frames / 30,
    candidate_seconds: current.total_frames / 30,
    added_seconds: (current.total_frames - baseline.total_frames) / 30,
    chapter_seconds: Object.fromEntries(current.chapters.map((item, index) => [chaptersInOrder[index], ((starts[index + 1] ?? current.total_frames) - item.start_frame) / 30])),
  };
}
const newUnits = additions.reduce((sum, addition) => sum + spokenUnits(addition.text), 0);
const scenes = preview.scenes.length;
const lines = preview.scenes.reduce((sum, scene) => sum + scene.lines.length, 0);
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_UNREVIEWED',
  base_round11_estimate_seconds_250_cpm: timing['250'].base_seconds,
  six_chapters: chaptersInOrder,
  new_scenes: additions.length,
  new_lines: additions.length,
  revised_inherited_lines: revisions.map((item) => item.line),
  reordered_origin_prefix: originPrefix,
  new_spoken_units: newUnits,
  revised_inherited_units_delta: revisedUnitsDelta,
  scenes,
  lines,
  illustrated_body_shots: preview.scenes.filter((scene) => scene.template === 'shot').length,
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_warnings: lint.warnings,
  cute_errors: cute,
  estimated_timing_not_tts: timing,
  source_pins_for_new_and_revised_lines: sourceMap.length,
  inherited_claim_reconciliation: inheritedClaimReconciliation.map((item) => ({ id: item.id, scene_active: item.active, current_verdict: item.current.verdict })),
  independent_fact_review: 'NOT_RUN',
  independent_listener_review: 'NOT_RUN',
  narrative_panel: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  generated_images_or_audio: 0,
};
addOutput('validation.json', validation);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  slug: previousManifest.slug,
  base_round11_manifest_sha256: sha(read(path.join(previous, 'manifest.json'))),
  base_chapter_sha256: baseHashes,
  additions_sha256: sha(read(path.join(here, 'additions.mjs'))),
  source_delta_sha256: sha(read(path.join(here, 'source-delta.json'))),
  candidate_chapter_sha256: Object.fromEntries(chaptersInOrder.map((key) => [key, sha(output.get(`candidate/chapters/${key}.json`))])),
  candidate_series_sha256: sha(output.get('candidate/series.json')),
  source_map_sha256: sha(output.get('source-map.json')),
  validation_sha256: sha(output.get('validation.json')),
  inherited_round9_narrative_passed: false,
  authorizes_host_install_or_paid_media: false,
};
addOutput('manifest.json', manifest);

const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of output) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(`${here}${path.sep}`), `unsafe output path ${name}`);
  if (action === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, bytes);
  } else {
    assert.ok(fs.existsSync(file), `missing generated ${name}`);
    assert.ok(read(file).equals(bytes), `stale generated ${name}`);
  }
}
assert.equal(lint.errors.length, 0, `lint errors: ${JSON.stringify(lint.errors)}`);
assert.equal(cute.length, 0, `cute visual errors: ${JSON.stringify(cute)}`);
console.log(JSON.stringify({ action, status: validation.status, scenes, lines, new_scenes: additions.length, new_spoken_units: newUnits, seconds_250: timing['250'].candidate_seconds, seconds_300: timing['300'].candidate_seconds, seconds_320: timing['320'].candidate_seconds, seconds_340: timing['340'].candidate_seconds, lint_errors: 0, lint_warnings: lint.warnings.length, cute_errors: 0 }));
