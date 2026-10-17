// Isolated A01 r3 narration candidate. Reads only frozen r2 bytes; writes here only.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(here, '../../../../..');
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(JSON.stringify(value, null, 2) + '\n');
const baseRead = (name) => fs.readFileSync(path.join(here, 'base', name));
const r2ManifestBytes = baseRead('r2-manifest.json');
assert.equal(sha(r2ManifestBytes), 'd25ad9e97a94c2c6172b05df2ff046de281832fde7df163a22fab024491aa78d', 'frozen r2 manifest drift');
const r2Manifest = JSON.parse(r2ManifestBytes);
for (const name of ['video.json', 'series.json', 'lexicon.json', 'script.md', 'claims.md']) {
  assert.equal(sha(baseRead(name)), r2Manifest.outputs_sha256['candidate/' + name], 'frozen r2 ' + name + ' drift');
}
for (const name of ['source-map.json', 'validation.json']) {
  assert.equal(sha(baseRead('r2-' + name)), r2Manifest.outputs_sha256[name], 'frozen r2 ' + name + ' drift');
}
assert.equal(sha(baseRead('brief.md')), r2Manifest.base_sha256['brief.md'], 'frozen brief drift');

const video = JSON.parse(baseRead('video.json'));
const series = JSON.parse(baseRead('series.json'));
const lexicon = JSON.parse(baseRead('lexicon.json'));
assert.equal(video.slug, 'story-rolling-suitcase-v2');
const scene = (id) => {
  const found = video.scenes.filter((item) => item.id === id);
  assert.equal(found.length, 1, 'expected one scene ' + id);
  return found[0];
};
const exact = (id, lineId, expected) => {
  const found = scene(id).lines.filter((item) => item.id === lineId);
  assert.equal(found.length, 1, 'expected one line ' + lineId);
  assert.equal(found[0].text, expected, 'r2 changed line ' + lineId);
  return found[0];
};
const insertAfter = (id, ...newScenes) => {
  const index = video.scenes.findIndex((item) => item.id === id);
  assert.ok(index >= 0, 'missing scene ' + id);
  video.scenes.splice(index + 1, 0, ...newScenes);
};

// The opening asks about continued wheeled-case use, not the identity of one object.
exact('hook-anita', 'r17h01', '1928 年，兒子替箱子裝了輪子，父親卻笑他們。旅程結束後，母親還會帶著它走嗎？').text =
  '1928 年，兒子替箱子裝了輪子，父親卻笑他們。旅程結束後，母親還會帶輪子箱出門嗎？';
const lecture = scene('origin-r12-03');
exact('origin-r12-03', 'r12o03', '旅程結束後，安妮塔巡迴講旅行故事時，仍帶著輪子行李箱。').text =
  '到了 1939 年，安妮塔在德州米德蘭一場茶會上談旅行；當地報紙記下她的出場。';
lecture.data.prompt = 'Cute historical illustration of an anonymous woman speaking about travel at a modest Midland, Texas study-club guest-day tea in 1939. A small listening group is present; this scene shows the speaking engagement without revealing the wheeled luggage yet. No readable newspaper, signs, logos, quotation text or real-person likeness.';
const anitaCase = {
  id: 'origin-1939-case', template: 'shot',
  data: {
    prompt: 'Cute illustrative detail at a modest 1939 Texas study-club tea: an anonymous woman in a plain dark cape and practical travel hat stands beside one unbranded wheeled suitcase and a small extra bag. These are details recorded in a contemporary local report, not a reconstruction of the surviving museum object or proof of every lecture. No readable text, logos or real-person likeness.',
    camera: 'push in', visual: 'still',
  },
  claims: ['o34'],
  lines: [{ id: 'r3o01', text: '報導說，她披著黑色斗篷，戴著實用的帽子；身旁還有一只帶輪子的行李箱。' }],
};
insertAfter('origin-r12-03', anitaCase);

// A later reporter's actual travel test supplies a new consumer-side result.
const passenger = scene('now-passenger');
exact('now-passenger', 'r15n01', '《紐約時報》回顧，旅客在航站看見空服員拉箱快步走，新的市場才慢慢打開。').text =
  '《紐約時報》回顧，旅客在航站看見空服員拉著箱子快步走。';
const consumerQuestion = {
  id: 'now-consumer-question', template: 'shot',
  data: {
    prompt: 'Cute illustration of an anonymous early-1990s traveler looking from a rolling carry-on in a shop window toward an airport corridor in the distance. The scene asks whether the bag will work for an ordinary traveler; do not show a purchase, plane-cabin fit or later packing result. No readable signs, logos or real-person likeness.',
    camera: 'push in', visual: 'still',
  },
  claims: [],
  lines: [{ id: 'r3n01', text: '他們看見了；但買得到、推上飛機、再放進置物櫃，真的都這麼順嗎？' }],
};
insertAfter('now-passenger', consumerQuestion);
assert.equal(video.scenes[video.scenes.findIndex((item) => item.id === 'now-12') + 1]?.id, 'now-overhead', '1993 insertion point drift');
const shop = {
  id: 'now-1993-test', template: 'shot',
  data: {
    prompt: 'Cute 1993 travel-gear illustration: an anonymous newspaper reporter compares four plain two-wheel carry-on bags on the ground and before a trip. Four generic shapes evoke a hands-on comparison, not a measured laboratory result. No brand marks, readable newspaper text, store labels or real-person likeness.',
    camera: 'track right', visual: 'still',
  },
  claims: ['n55'],
  lines: [{ id: 'r3n02', text: '到了 1993 年，《洛杉磯時報》一位記者，真的把四家輪子登機箱帶上路測試。' }],
};
const retail = {
  id: 'now-1993-retail', template: 'shot',
  data: {
    prompt: 'Cute illustrative 1993 luggage-shop counter with several anonymous rolling carry-on cases available for customers to inspect. A small mail-order parcel sits to one side as a visual transition, without implying a specific sale or exact inventory in one shop. No readable signage, prices, brands or real-person likeness.',
    camera: 'pull out', visual: 'still',
  },
  claims: ['n56'],
  lines: [{ id: 'r3n03', text: '她寫，Travelpro 起初靠郵購；到了這時，百貨和行李店也能選到不同品牌。' }],
};
const cabin = {
  id: 'now-1993-cabin', template: 'shot',
  data: {
    prompt: 'Cute illustrative early-1990s aircraft cabin: an anonymous traveler rolls a modestly packed two-wheel carry-on through a narrow aisle toward a seat. The bag is not shown as fitting every aircraft or every overhead bin. No airline branding, readable markings or real-person likeness.',
    camera: 'track left', visual: 'still',
  },
  claims: ['n57'],
  lines: [{ id: 'r3n04', text: '她說，這類箱子能穿過多數機艙走道；尺寸合適時，也能收進座位下或多數頭頂櫃。' }],
};
const overpacked = {
  id: 'now-1993-limit', template: 'shot',
  data: {
    prompt: 'Cute illustrative close view in a generic early-1990s airplane cabin: an anonymous traveler removes a few belongings from an overfilled outside pocket of an unbranded two-wheel carry-on before storing the case. Show a practical packing limit, not a blocked aisle, angry crew or a claim about all flights. No text, logos or real-person likeness.',
    camera: 'push in', visual: 'still',
  },
  claims: ['n58'],
  lines: [{ id: 'r3n05', text: '但她的 Travelpro 外袋一塞滿，座位下和頭頂櫃都放不進；只好先把外袋的東西拿出來。' }],
};
insertAfter('now-12', shop, retail, cabin, overpacked);

const firstLoop = video.loops.find((loop) => loop.setup === 'r17h01');
assert.equal(firstLoop.payoff, 'r12o03', 'Anita loop drift');
firstLoop.payoff = 'r3o01';
firstLoop.what = '父親嘲笑後，1939 年報紙仍記錄 Anita 帶輪箱出席講座';
video.loops.push({
  setup: 'r3n01', payoff: 'r3n05',
  what: '1993 年記者驗證店面與機艙使用，外袋過滿卻放不進',
});

const midlandUrl = 'https://newspapers.swco.ttu.edu/bitstreams/b9cd84b8-2ba7-4506-9eff-7cca3e5c6376/download';
const latUrl = 'https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html';
series.plan.sources.push(
  { url: midlandUrl, publisher: 'The Midland (Texas) Reporter-Telegram, 1939-02-09, PDF p. 4', kind: 'contemporary_newspaper_report', supports: 'Modern Study Club guest-day tea, 1939-02-08; Burnham arrives with cape, hat, wheeled suitcase and extra bag. One documented appearance only.', checked: '2026-10-18' },
  { url: latUrl, publisher: 'Los Angeles Times, Judi Dash, 1993-08-01', kind: 'contemporary_first_person_test', supports: 'Reporter compares four rolling carry-on lines on ground and in air; mail-order to retail availability; most aisles/storage; her overfilled Travelpro exterior pockets prevent stowage until emptied.', checked: '2026-10-18' },
);
series.plan.must_verify.push(
  { claim: '1939-02-09 Midland local report documents one tea/lecture the previous afternoon with wheeled suitcase; no proof it is the exact 1928 case or that every lecture included one', sources: [series.plan.sources.length - 2], core: true, attributed: true },
  { claim: 'Judi Dash 1993 first-person report tested four brands and recorded a partial retail/cabin success plus an overpacking limit; no universal aircraft fit or sales total', sources: [series.plan.sources.length - 1], core: true, attributed: true },
);
const originPlan = series.plan.chapters.find((chapter) => chapter.key === 'origin');
const nowPlan = series.plan.chapters.find((chapter) => chapter.key === 'now');
assert.ok(originPlan && nowPlan);
originPlan.point += ' 1939 年 Midland 當時報紙提供一場具體巡講和輪箱到場的後續證據，不識別為同一只館藏箱。';
nowPlan.point += ' 1993 年 LA Times 記者四品牌旅途實測提供店面、客艙與外袋塞滿反例，放在 1991 年轉全職後；不推及所有飛機。';
series.plan.takeaway += ' 1993 年旅客實測仍有機艙收納與裝填界線。';
series.plan.caveats += ' 1939 報導只證一場出席的輪箱；1993 記者實測不能當全市場銷量或所有客艙尺寸證據。';

const claimLines = baseRead('claims.md').toString('utf8').replace(/\r\n/g, '\n').split('\n');
const replaceClaim = (id, row) => {
  const matches = claimLines.map((line, index) => line.startsWith(id + '｜') ? index : -1).filter((index) => index >= 0);
  assert.equal(matches.length, 1, 'claim row ' + id);
  claimLines[matches[0]] = row;
};
const insertAfterClaim = (id, rows) => {
  const index = claimLines.findIndex((line) => line.startsWith(id + '｜'));
  assert.ok(index >= 0, 'insert claim after ' + id);
  claimLines.splice(index + 1, 0, ...rows);
};
replaceClaim('o27', `o27｜1939 年 2 月 9 日 Midland 當地報紙報導，安妮塔在前一日 Modern Study Club 茶會談旅行；此鏡尚不展示輪箱｜${midlandUrl}｜2026-10-18｜origin-r12-03｜PENDING`);
insertAfterClaim('o27', [`o34｜同篇 1939 年當地報導寫安妮塔出席時有黑色披肩、實用帽子、一只帶輪子的行李箱和另一只放遺漏物品的袋子；只證該場，不能識別箱子實物｜${midlandUrl}｜2026-10-18｜origin-1939-case｜PENDING`]);
replaceClaim('n44', 'n44｜Joe Sharkey 2010 年《紐約時報》文章回顧，旅客在航站見空服員拉著 Rollaboard 快步走；此文重印於 RNPA 2016 Contrails p.48，與 Emmer p.46–47 回憶是不同作者｜https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf｜2026-10-18｜now-passenger｜PENDING');
insertAfterClaim('n43', [
  `n55｜Judi Dash 在 1993 年《洛杉磯時報》記錄自己在地面與飛機上測試 Travelpro、American Tourister、Lark、Samsonite 四家輪子登機箱；不是全市場調查｜${latUrl}｜2026-10-18｜now-1993-test｜PENDING`,
  `n56｜Dash 指 Travelpro 起初以郵購販售；到 1993 年，多個品牌的輪子登機箱可在主要百貨或行李專門店選購；不推算銷量｜${latUrl}｜2026-10-18｜now-1993-retail｜PENDING`,
  `n57｜Dash 指該類內建輪子行李箱可通過多數機艙走道，合適的裝填與尺寸可放在座位下或多數頭頂櫃；不是每架飛機保證適用｜${latUrl}｜2026-10-18｜now-1993-cabin｜PENDING`,
  `n58｜Dash 自述 Travelpro 可擴充外袋裝入額外物品後，箱子放不進座位下或頭頂櫃，需先清空外袋；僅是她的實測反例｜${latUrl}｜2026-10-18｜now-1993-limit｜PENDING`,
]);
const finalClaimScene = new Map(video.scenes.flatMap((item) => (item.claims ?? []).map((id) => [id, item.id])));
assert.equal(finalClaimScene.size, video.scenes.reduce((sum, item) => sum + (item.claims ?? []).length, 0), 'duplicate claim IDs');
const claimRows = claimLines.filter((line) => /^[a-z]\d+｜/.test(line));
assert.deepEqual(new Set(claimRows.map((row) => row.split('｜', 1)[0])), new Set(finalClaimScene.keys()), 'claim rows match video');
for (const row of claimRows) {
  const cells = row.split('｜');
  assert.equal(cells.length, 6, 'malformed claim row ' + cells[0]);
  assert.equal(cells[4], finalClaimScene.get(cells[0]), 'claim scene mismatch ' + cells[0]);
  assert.equal(cells[5], 'PENDING', 'no inherited approval ' + cells[0]);
}
const claimsMarkdown = Buffer.from(claimLines.join('\n'));

const module = (relative) => import(pathToFileURL(path.join(repo, relative)));
const [{ screenplay }, { estimateTimeline, spokenUnits }, { lintVideo }, { hookCadenceProblems }, { cuteStoryVisualProblems }] = await Promise.all([
  module('tools/video/core/screenplay.mjs'),
  module('tools/video/core/timeline.mjs'),
  module('tools/video/core/lint.mjs'),
  module('tools/video/core/narrative.mjs'),
  module('tools/video/automation/story.mjs'),
]);
assert.equal(screenplay(JSON.parse(baseRead('video.json'))), baseRead('script.md').toString('utf8').replace(/\r\n/g, '\n'), 'r2 screenplay mismatch');
const script = Buffer.from(screenplay(video));
const lint = lintVideo(video, { lexicon, brief: baseRead('brief.md').toString('utf8'), translations: {}, others: [], series });
const cute = cuteStoryVisualProblems(video);
const allLines = video.scenes.flatMap((item) => item.lines);
const lineScene = new Map(video.scenes.flatMap((item) => item.lines.map((line) => [line.id, item.id])));
assert.equal(lineScene.size, allLines.length, 'duplicate line IDs');
assert.equal(new Set(video.scenes.map((item) => item.id)).size, video.scenes.length, 'duplicate scene IDs');
for (const loop of video.loops) {
  assert.ok(lineScene.has(loop.setup) && lineScene.has(loop.payoff), 'loop line missing ' + loop.setup);
  assert.notEqual(lineScene.get(loop.setup), lineScene.get(loop.payoff), 'same-scene loop ' + loop.setup);
}

const cadence45 = (timeline, explicitOnly) => {
  const bodyStart = timeline.chapters[1].start_frame / 30;
  const outroId = video.scenes.find((item) => item.template === 'outro')?.id;
  assert.ok(outroId, 'missing outro');
  const bodyEnd = timeline.scenes.find((item) => item.id === outroId).start_frame / 30;
  const sceneIndex = new Map(video.scenes.map((item, index) => [item.id, index]));
  const bodyFirst = sceneIndex.get(timeline.chapters[1].scene);
  const bodyLast = sceneIndex.get(outroId);
  const lineTime = new Map(timeline.lines.map((item) => [item.id, item]));
  const points = [{ at: bodyStart, id: 'body:start' }];
  for (const loop of video.loops) {
    const si = sceneIndex.get(lineScene.get(loop.setup));
    if (si < bodyFirst || si >= bodyLast) continue;
    const setup = lineTime.get(loop.setup);
    const payoff = lineTime.get(loop.payoff);
    assert.ok(setup.end_frame <= payoff.start_frame, 'loop payoff before setup ' + loop.setup);
    const spoken = allLines.find((item) => item.id === loop.setup).text;
    if (explicitOnly && !/[？?]\s*$/.test(spoken)) continue;
    points.push({ at: setup.end_frame / 30, id: loop.setup });
  }
  points.sort((a, b) => a.at - b.at);
  points.push({ at: bodyEnd, id: 'body:end' });
  const gaps = points.slice(1).map((item, index) => ({ from: points[index].id, to: item.id, seconds: Number((item.at - points[index].at).toFixed(1)) }));
  return { rule: explicitOnly ? 'declared later-payoff voiced questions only' : 'unreviewed declared action/question arcs; visual anti-spoiler review required', max_gap_seconds: Math.max(...gaps.map((item) => item.seconds)), gaps_over_45_seconds: gaps.filter((item) => item.seconds > 45), devices: points };
};
const timing = {};
for (const cpm of [250, 275, 300]) {
  const t = estimateTimeline(video, cpm);
  const old = estimateTimeline(JSON.parse(baseRead('video.json')), cpm);
  const lineTime = new Map(t.lines.map((item) => [item.id, item]));
  const addedLineIds = ['r3o01', 'r3n01', 'r3n02', 'r3n03', 'r3n04', 'r3n05'];
  timing[cpm] = {
    r2_seconds: Number((old.total_frames / 30).toFixed(1)),
    candidate_seconds: Number((t.total_frames / 30).toFixed(1)),
    added_seconds: Number(((t.total_frames - old.total_frames) / 30).toFixed(1)),
    shortfall_to_540_seconds: Number((540 - t.total_frames / 30).toFixed(1)),
    six_chapter_seconds: t.chapters.map((chapter, index) => ({ scene_id: chapter.scene, seconds: Number((((t.chapters[index + 1]?.start_frame ?? t.total_frames) - chapter.start_frame) / 30).toFixed(1)) })),
    added_line_seconds: Object.fromEntries(addedLineIds.map((id) => [id, Number(((lineTime.get(id).end_frame - lineTime.get(id).start_frame) / 30).toFixed(1))])),
    loops: video.loops.map((loop) => ({ setup: loop.setup, payoff: loop.payoff, gap_seconds: Number(((lineTime.get(loop.payoff).start_frame - lineTime.get(loop.setup).end_frame) / 30).toFixed(1)) })),
    explicit_question_cadence_45: cadence45(t, true),
    action_proxy_cadence_45_not_pass: cadence45(t, false),
    legacy_hook_cadence_warnings: hookCadenceProblems(video, t),
  };
}

const additions = [
  { scene_id: 'origin-1939-case', line_id: 'r3o01', claim_id: 'o34', source_url: midlandUrl, source_location: 'The Midland Reporter-Telegram, 1939-02-09, PDF p. 4, Modern Study Club guest-day tea report', evidence_type: 'contemporary local report; one observed appearance', caution: 'not the identified 1928 object or every lecture' },
  { scene_id: 'now-1993-test', line_id: 'r3n02', claim_id: 'n55', source_url: latUrl, source_location: 'Judi Dash, LA Times, 1993-08-01, first-person four-brand comparison', evidence_type: 'contemporary reporter test', caution: 'not a market-wide controlled study' },
  { scene_id: 'now-1993-retail', line_id: 'r3n03', claim_id: 'n56', source_url: latUrl, source_location: 'Judi Dash, 1993, mail-order origin and current department/specialty retail paragraph', evidence_type: 'contemporary distribution report', caution: 'no sales total or exact retail launch date' },
  { scene_id: 'now-1993-cabin', line_id: 'r3n04', claim_id: 'n57', source_url: latUrl, source_location: 'Judi Dash, 1993, most aisles and most under-seat/overhead storage with suitable bag size', evidence_type: 'first-person and contemporary product report', caution: 'not every plane or every loading configuration' },
  { scene_id: 'now-1993-limit', line_id: 'r3n05', claim_id: 'n58', source_url: latUrl, source_location: 'Judi Dash, 1993, her Travelpro expanded outside pocket prevented under-seat/overhead stowage until emptied', evidence_type: 'first-person practical counterexample', caution: 'her case, not all bags' },
];
const sourceMap = {
  status: 'PENDING_INDEPENDENT_REVIEW',
  derives_from_r2_manifest_sha256: sha(r2ManifestBytes),
  derives_from_r2_source_map_sha256: sha(baseRead('r2-source-map.json')),
  source_snapshot: r2Manifest.source_snapshot,
  prior_review_not_inherited: true,
  sources: [
    { url: midlandUrl, date: '1939-02-09', page: 'PDF p. 4', checked_on: '2026-10-18', kind: 'contemporary newspaper', scope: 'one 1939-02-08 lecture appearance only' },
    { url: latUrl, date: '1993-08-01', checked_on: '2026-10-18', kind: 'contemporary first-person travel test', scope: 'four product lines plus reporter’s own Travelpro packing counterexample' },
  ],
  changed_lines: [
    { scene_id: 'hook-anita', line_id: 'r17h01', prior: '旅程結束後，母親還會帶著它走嗎？', now: '旅程結束後，母親還會帶輪子箱出門嗎？', reason: 'do not assert 1939 case is the same physical object', verdict: 'PENDING' },
    { scene_id: 'origin-r12-03', line_id: 'r12o03', source_url: midlandUrl, source_location: '1939-02-09 PDF p. 4', reason: 'contemporary scene replaces generic retrospective lecture statement', verdict: 'PENDING' },
    { scene_id: 'now-passenger', line_id: 'r15n01', reason: 'withhold the market outcome until the 1993 contemporary retail report; retains attributed passenger sighting', verdict: 'PENDING' },
  ],
  added_question_line: { scene_id: 'now-consumer-question', line_id: 'r3n01', candidate_text: consumerQuestion.lines[0].text, candidate_prompt: consumerQuestion.data.prompt, source_context: latUrl, partial_answers: ['r3n03', 'r3n04'], limitation_payoff: 'r3n05', verdict: 'PENDING_ANTI_SPOILER_REVIEW' },
  added_scenes: additions.map((item) => ({ ...item, candidate_text: scene(item.scene_id).lines[0].text, candidate_prompt: scene(item.scene_id).data.prompt, verdict: 'PENDING_INDEPENDENT_SOURCE_AND_IMAGE_REVIEW' })),
  revised_scene: { scene_id: 'origin-r12-03', line_id: 'r12o03', claim_id: 'o27', candidate_text: lecture.lines[0].text, candidate_prompt: lecture.data.prompt, source_url: midlandUrl, source_location: '1939-02-09 PDF p. 4', verdict: 'PENDING_INDEPENDENT_SOURCE_AND_IMAGE_REVIEW' },
  loops: video.loops.map((loop) => ({ ...loop, setup_scene: lineScene.get(loop.setup), payoff_scene: lineScene.get(loop.payoff), explicit_question: /[？?]\s*$/.test(allLines.find((item) => item.id === loop.setup).text), timing_300_gap_seconds: timing[300].loops.find((item) => item.setup === loop.setup).gap_seconds, verdict: 'PENDING_NARRATIVE_AND_VISUAL_ANTI_SPOILER_REVIEW' })),
  host_migration: 'SPEC_ONLY_SIX_CHAPTER_SOURCES_AND_SERIES_PLAN_REQUIRE_SEPARATE_REVIEW',
  caveats: [
    '1939 report records a wheeled suitcase at one study-club appearance; it does not identify the same 1928 homemade case or prove wheeled luggage at every lecture.',
    'The 1993 report is a contemporary reporter’s own comparison; mail-order-to-retail wording does not establish exact launch dates, overall sales or universal cabin compatibility.',
    'The 1993 overpacking outcome is an observed limit on the reporter’s Travelpro case; the voiceover does not assert all wheeled bags fail to stow.',
    'The new question receives partial answers before its final practical packing counterexample. The declared loop is not a cadence PASS without blind listening and picture anti-spoiler review.',
    'All prior r2 source, chronology and visual caveats remain binding; see the frozen r2 source-map and validation under base/.',
  ],
};
const validation = {
  status: 'OFFLINE_MECHANICAL_ONLY_HOLD_UNREVIEWED',
  source_snapshot: r2Manifest.source_snapshot,
  r2_manifest_sha256: sha(r2ManifestBytes),
  scenes: video.scenes.length,
  lines: allLines.length,
  claims: finalClaimScene.size,
  narration_spoken_units: allLines.reduce((sum, item) => sum + spokenUnits(item.text), 0),
  narration_characters_including_punctuation: [...allLines.map((item) => item.text).join('')].length,
  added_scene_ids: [consumerQuestion.id, ...additions.map((item) => item.scene_id)],
  changed_line_ids: ['r17h01', 'r12o03', 'r15n01'],
  added_line_ids: ['r3o01', 'r3n01', 'r3n02', 'r3n03', 'r3n04', 'r3n05'],
  loops: video.loops.length,
  lint_errors: lint.errors,
  lint_warning_count: lint.warnings.length,
  lint_warnings: lint.warnings,
  cute_visual_errors: cute,
  estimated_timing_not_tts: timing,
  duration_540_gate: timing[300].candidate_seconds >= 540 && timing[250].candidate_seconds >= 540 ? 'ESTIMATE_ONLY_PENDING_TTS' : 'HOLD',
  explicit_45_second_gate: timing[300].explicit_question_cadence_45.max_gap_seconds <= 45 ? 'ESTIMATE_ONLY_PENDING_LISTENING' : 'HOLD',
  independent_fact_review: 'NOT_RUN',
  independent_listener_review: 'NOT_RUN',
  independent_visual_review: 'NOT_RUN',
  script_review_receipt: 'NOT_ISSUED',
  actual_tts_or_media: 'NOT_RUN',
  production_or_paid_work: 'NOT_RUN',
};

const output = new Map([
  ['candidate/video.json', json(video)],
  ['candidate/series.json', json(series)],
  ['candidate/lexicon.json', json(lexicon)],
  ['candidate/script.md', script],
  ['candidate/claims.md', claimsMarkdown],
  ['source-map.json', json(sourceMap)],
  ['validation.json', json(validation)],
]);
const manifest = {
  status: 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE',
  slug: video.slug,
  derives_from_r2_manifest_sha256: sha(r2ManifestBytes),
  source_snapshot: r2Manifest.source_snapshot,
  base_sha256: Object.fromEntries(['video.json', 'series.json', 'lexicon.json', 'script.md', 'claims.md', 'brief.md', 'r2-manifest.json', 'r2-source-map.json', 'r2-validation.json'].map((name) => [name, sha(baseRead(name))])),
  build_sha256: sha(fs.readFileSync(path.join(here, 'build.mjs'))),
  readme_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  outputs_sha256: Object.fromEntries([...output].map(([name, bytes]) => [name, sha(bytes)])),
  r2_or_earlier_modified: false,
  production_capture_modified: false,
  authorizes_host_install_or_paid_media: false,
};
output.set('manifest.json', json(manifest));
const action = process.argv[2];
assert.ok(action === '--write' || action === '--check', 'use --write or --check');
for (const [name, bytes] of output) {
  const file = path.join(here, name);
  assert.ok(file.startsWith(here + path.sep), 'output must stay inside r3');
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
console.log(JSON.stringify({ action, status: validation.status, scenes: validation.scenes, lines: validation.lines, spoken_units: validation.narration_spoken_units, seconds_250: timing[250].candidate_seconds, seconds_275: timing[275].candidate_seconds, seconds_300: timing[300].candidate_seconds, strict_45_gap_300: timing[300].explicit_question_cadence_45.max_gap_seconds, action_proxy_gap_300: timing[300].action_proxy_cadence_45_not_pass.max_gap_seconds, lint_errors: lint.errors.length, lint_warnings: lint.warnings.length, cute_errors: cute.length }));
