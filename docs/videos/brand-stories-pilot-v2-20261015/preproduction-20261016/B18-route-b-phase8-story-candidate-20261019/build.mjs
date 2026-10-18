import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const base = resolve(here, '..');
const phase4 = join(base, 'B18-route-b-phase4-candidate-20261017');
const phase5 = join(base, 'B18-route-b-phase5-hook-diagnostic-20261018');
const phase6 = join(base, 'B18-route-b-phase6-story-candidate-20261019');
const phase7 = join(base, 'B18-route-b-phase7-story-candidate-20261019');
const row10c = join(base, 'B18-route-b-row10c-phase4-candidate-20261017');
const read = (path) => readFileSync(path, 'utf8');
const json = (path) => JSON.parse(read(path));
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const hashFile = (path) => sha(readFileSync(path));
const stringify = (value) => `${JSON.stringify(value, null, 2)}\n`;
const assert = (okay, reason) => { if (!okay) throw new Error(reason); };

const pins = {
  phase4_script: [join(phase4, 'B18.md'), '73236441aebc92e804436fd9371a3044a27e5decdd7438905459ef214023768f'],
  phase4_manifest: [join(phase4, 'sha256.json'), 'efdf3994152db18892d70c35f6ae10ba3f1d4a9076078922a8a988ee0bbd7422'],
  phase5_visual: [join(phase5, 'visual-patch.json'), '9dea7dbf1294215b62200e90b79d3a1f2dc4243c6fec5137a07b1e66844fbd19'],
  phase6_script: [join(phase6, 'B18.md'), 'd9fab72f15a5eb44d20437e1dd7f50caf476d7113a3d2ad6645dc2554f20e65e'],
  phase6_manifest: [join(phase6, 'manifest.json'), '1da727619472e4394eaf7e3854712c90ea5432182f3d6f9e9879b787c93a41f6'],
  phase7_script: [join(phase7, 'B18.md'), '9814170a3c03d024e34485aa63e174a864b508974f5210b427a12f172cbbd29e'],
  phase7_manifest: [join(phase7, 'manifest.json'), '3633a4ca2587ea0bc977933971a44d644120caa0e4c20e58ea187291c1529604'],
  row10c: [join(row10c, 'B18.json'), '6c2eb6172d0afc6d5c92a91736cf1ad606ea3302d904c749d42d1b74533b14bc'],
};
for (const [name, [file, expected]] of Object.entries(pins)) assert(hashFile(file) === expected, `source drift: ${name}`);

const oldCoverage = json(join(phase4, 'coverage.json'));
const oldClaims = json(join(phase4, 'claim-coverage.json')).claims;
const phase4Chapters = Object.fromEntries(['hook', 'origin', 'idea', 'engine', 'turn', 'now'].map((key) => [key, json(join(phase4, 'remapped-chapters', `${key}.json`))]));
const oldScenes = new Map(Object.values(phase4Chapters).flatMap((chapter) => chapter.scenes.map((scene) => [scene.id, scene])));
const plan = json(pins.row10c[0]);
const revisions = json(join(here, 'paragraph-overrides.json'));
const loopInput = json(join(here, 'loops.json'));
const sourceEvidence = json(join(here, 'source-evidence.json'));
const phase7Loops = json(join(phase7, 'loops.json'));
const visualInput = json(pins.phase5_visual[0]);
const keys = ['H01', 'H02', 'H03', 'O01', 'O02', 'O03', 'O04', 'I01', 'I02', 'I03', 'I04', 'E01', 'E02', 'E03', 'E04', 'E05', 'T01', 'T02', 'T03', 'T04', 'T05', 'T06', 'N01', 'N02', 'N03'];
const chapterFor = (key) => ({ H: 'hook', O: 'origin', I: 'idea', E: 'engine', T: 'turn', N: 'now' })[key[0]];
const headings = {
  hook: '瓶子往前走，盤子還靠人遞',
  origin: '便宜立食店先被客人填滿',
  idea: '直線能走，轉角卻掉盤',
  engine: '首店開門，萬博又考驗備料',
  turn: '店與設備各自重畫送餐路',
  now: '兩件不同年代的機械遺產',
};
assert(keys.length === 25 && oldCoverage.paragraph_count === 25, '25 paragraph baseline required');
assert(plan.slug === 'story-conveyor-belt-sushi-v2' && plan.must_verify.length === 10 && plan.sources.length === 6, 'reviewed Row10c shape drift');
assert(revisions.schema_version === 1 && loopInput.schema_version === 1, 'candidate schema drift');
assert(sourceEvidence.schema_version === 1 && sourceEvidence.claims.length === 2, 'source evidence shape drift');
assert(Object.keys(revisions.overrides).every((key) => keys.includes(key)), 'unknown paragraph override');
assert(Object.keys(revisions.source_additions).every((key) => keys.includes(key)), 'unknown paragraph source addition');
const omitted = new Set(revisions.omit_paragraphs);
assert(omitted.size === 3 && ['H03', 'O04', 'N02'].every((key) => omitted.has(key)), 'only reviewed duplicate paragraphs may be omitted');
const activeKeys = keys.filter((key) => !omitted.has(key));
assert(activeKeys.length === 22, 'Phase8 active paragraph count drift');

const source = read(pins.phase4_script[0]);
const voices = [...source.matchAll(/^> (.+)$/gmu)].map((match) => match[1]);
const notes = [...source.matchAll(/^\*\*製作註 ([HOIETN]\d{2})（不朗讀）\*\*：([^\n]*)$/gmu)];
assert(voices.length === keys.length && notes.length === keys.length, 'Phase4 script paragraph/note shape drift');
const paragraphs = Object.fromEntries(keys.map((key, index) => {
  assert(notes[index][1] === key, `Phase4 note order drift ${key}`);
  const text = omitted.has(key) ? '' : revisions.overrides[key] ?? voices[index];
  assert(typeof text === 'string' && (omitted.has(key) || text.length > 5), `empty narration ${key}`);
  return [key, text];
}));
const sourcesFor = Object.fromEntries(keys.map((key, index) => [key, [...new Set([...notes[index][2].matchAll(/\[(\d+)\]/gu)].map((match) => Number(match[1])).concat(revisions.source_additions[key] ?? []))].sort((a, b) => a - b)]));
assert(Object.values(sourcesFor).every((sources) => sources.length && sources.every((number) => number >= 0 && number < plan.sources.length)), 'bad source index in inherited note');
const existingClaimsByParagraph = Object.fromEntries(keys.map((key) => [key, []]));
const unspokenClaims = [];
for (const claim of oldClaims) {
  const match = claim.note.match(/([HOIETN]\d{2})/u);
  assert(match && keys.includes(match[1]), `claim paragraph missing ${claim.id}`);
  const originalParagraph = match[1];
  assert(oldCoverage.source_to_scene[originalParagraph].scene_ids.includes(claim.scene), `old claim scene not in original paragraph ${claim.id}`);
  if (revisions.unspoken_claim_ids.includes(claim.id)) {
    assert(claim.id === 't12', `unplanned unspoken claim ${claim.id}`);
    unspokenClaims.push({ ...claim, original_paragraph: originalParagraph, status: 'UNCHECKED_NOT_IN_PHASE8_VOICE', reason: '1980 bypass device name documented but its routing mechanism is not; dropped from narration and conceptual visuals.' });
    continue;
  }
  const paragraph = revisions.claim_moves[claim.id] ?? originalParagraph;
  assert(activeKeys.includes(paragraph), `claim placed in omitted paragraph ${claim.id}`);
  const anchor = revisions.claim_revisions[claim.id] ?? claim.claim;
  assert(paragraphs[paragraph].includes(anchor), `old claim anchor removed ${claim.id} in ${paragraph}`);
  assert(sourcesFor[paragraph].includes(claim.source), `old claim source not in paragraph ${claim.id}`);
  existingClaimsByParagraph[paragraph].push(claim.id);
}
assert(oldClaims.length === 65 && oldClaims.every((claim) => claim.verdict === 'UNCHECKED'), 'old claim review state drift');
assert(unspokenClaims.length === 1 && Object.values(existingClaimsByParagraph).flat().length === 64, 'old claim disposition incomplete');

const newClaims = revisions.new_claims.map((claim) => {
  assert(keys.includes(claim.paragraph) && paragraphs[claim.paragraph].includes(claim.anchor), `new claim anchor missing ${claim.id}`);
  assert(!oldClaims.some((old) => old.id === claim.id), `new claim id collision ${claim.id}`);
  assert(sourcesFor[claim.paragraph].includes(claim.source), `new claim source missing ${claim.id}`);
  const proposedScenes = { e14: 'engine-phase7-busy-01', e15: 'engine-phase8-dotonbori-01', e16: 'engine-phase8-expo-visitors-01', t19: 'turn-phase7-datecard-01', t20: 'turn-phase8-irie-01', t21: 'turn-phase7-export-01' };
  assert(proposedScenes[claim.id], `new claim scene missing ${claim.id}`);
  return { ...claim, verdict: 'UNCHECKED', proposed_scene: proposedScenes[claim.id] };
});
assert(newClaims.length === 6 && ['e14', 'e15', 'e16', 't19', 't20', 't21'].every((id) => newClaims.some((claim) => claim.id === id)), 'six new source claims expected');
for (const evidence of [...sourceEvidence.claims, ...sourceEvidence.additional_source_pointers]) {
  const claim = newClaims.find((item) => item.id === evidence.id);
  assert(claim && claim.source === evidence.source_index && plan.sources[claim.source].url === evidence.url, `source evidence route ${evidence.id}`);
  assert(evidence.source_excerpt && evidence.location && evidence.claim_boundary, `source evidence incomplete ${evidence.id}`);
}

const units = (text) => (text.match(/[\p{Script=Han}0-9〇]/gu) ?? []).length;
const bodyUnits = activeKeys.reduce((sum, key) => sum + units(paragraphs[key]), 0);
const bodySecondsAt300 = Number((bodyUnits / 5).toFixed(1));
const targetPaperRange = bodyUnits >= 2700 && bodyUnits <= 3300;
const timeline = [];
let cursor = 0;
for (const key of activeKeys) {
  const duration = units(paragraphs[key]) / 5;
  timeline.push({ paragraph: key, chapter: chapterFor(key), source_indices: sourcesFor[key], claim_ids: existingClaimsByParagraph[key], paper_start_seconds_300cpm: Number(cursor.toFixed(1)), paper_end_seconds_300cpm: Number((cursor + duration).toFixed(1)) });
  cursor += duration;
}

const indexOf = (key) => activeKeys.indexOf(key);
const loopAudit = loopInput.loops.map((loop) => {
  const setupIndex = indexOf(loop.setup_paragraph);
  const obstacleIndex = indexOf(loop.obstacle_paragraph);
  const payoffIndex = indexOf(loop.payoff_paragraph);
  assert(setupIndex >= 0 && setupIndex < obstacleIndex && obstacleIndex <= payoffIndex, `loop chronology ${loop.id}`);
  const setupText = paragraphs[loop.setup_paragraph];
  const payoffText = paragraphs[loop.payoff_paragraph];
  assert(setupText.includes(loop.setup_phrase) && payoffText.includes(loop.payoff_phrase), `loop phrase missing ${loop.id}`);
  assert(loop.source_indices.every((number) => number >= 0 && number < plan.sources.length), `loop source out of range ${loop.id}`);
  assert(loop.source_indices.every((number) => sourcesFor[loop.setup_paragraph].includes(number) || sourcesFor[loop.payoff_paragraph].includes(number)), `loop source not routed at setup or payoff ${loop.id}`);
  assert(loop.source_indices.some((number) => sourcesFor[loop.payoff_paragraph].includes(number)), `loop payoff lacks routed source ${loop.id}`);
  const setupOffset = units(setupText.slice(0, setupText.indexOf(loop.setup_phrase))) / 5;
  const payoffOffset = units(payoffText.slice(0, payoffText.indexOf(loop.payoff_phrase))) / 5;
  const setupAt = timeline[setupIndex].paper_start_seconds_300cpm + setupOffset;
  const payoffAt = timeline[payoffIndex].paper_start_seconds_300cpm + payoffOffset;
  const span = Number((payoffAt - setupAt).toFixed(1));
  assert(span >= 40, `loop too immediate at paper speed ${loop.id}: ${span}s`);
  return { ...loop, paper_setup_seconds_300cpm: Number(setupAt.toFixed(1)), paper_payoff_seconds_300cpm: Number(payoffAt.toFixed(1)), paper_open_seconds_300cpm: span, measured_tts_seconds: null, editorial_verdict: 'PENDING_INDEPENDENT_FULL_REVIEW' };
});
assert(loopAudit.length === 8 && new Set(loopAudit.map((loop) => loop.id)).size === 8, 'eight unique delayed loops required');

const visualProposal = visualInput.scenes.map((scene) => {
  const prior = oldScenes.get(scene.id);
  assert(prior && prior.data.prompt === scene.original_prompt, `Phase4 prompt drift ${scene.id}`);
  const sourceIndices = scene.source_indices.map((index) => {
    const url = visualInput.source_urls[index];
    const mapped = plan.sources.findIndex((item) => item.url === url);
    assert(mapped >= 0, `visual source URL missing ${scene.id}`);
    return mapped;
  });
  const updatedWhy = scene.id === 'turn-s081'
    ? 'T03 shows the space between the back room and seats; the straight-lane answer remains withheld until T04.'
    : scene.id === 'turn-s070'
      ? 'T04 has named a later back-room problem; this establishing view precedes the sourced straight-lane reveal at turn-s072.'
      : scene.narrative_reason;
  return { id: scene.id, chapter: scene.chapter, prompt: `Cute storybook editorial illustration, ${scene.proposed_prompt}`, source_indices: sourceIndices, why: updatedWhy, status: 'TEXT_ONLY_NOT_GENERATED' };
});
visualProposal.push({
  id: 'engine-s046', chapter: 'engine',
  prompt: 'Wide editorial view of a late-1950s Osaka sushi restaurant exterior, the circular serving conveyor visible through a broad plain window, an unbranded storefront and ordinary street; no passerby stopping, pointing or reacting.',
  source_indices: [0], why: 'The source supports visibility from the street, not an individual passerby stopping to watch.', status: 'TEXT_ONLY_NOT_GENERATED',
});
visualProposal.push({
  id: 'engine-phase7-busy-01', chapter: 'engine',
  prompt: 'Wide cute editorial illustration of an anonymous busy 1958 Osaka conveyor sushi shop with occupied stools and plain plates moving on a circular counter, no identifiable founder, readable signs, sales chart or invented individual customer reaction.',
  source_indices: [0], why: 'New e14 scene candidate for the reported busy first shop; replaces the mismatched Phase6 engine-s046b pointer.', status: 'NEW_SCENE_PROPOSAL_NOT_GENERATED',
});
visualProposal.push({
  id: 'engine-phase8-dotonbori-01', chapter: 'engine',
  prompt: 'Cute storybook editorial illustration of a generic 1960 Osaka Dotonbori shopping-street sushi storefront as a location transition, anonymous passersby with no directed action, no reconstructed actual facade, sign, interior or founder portrait.',
  source_indices: [0], why: 'J-Net21 documents the second Dotonbori shop opening in 1960; the image is a conceptual location transition, not an archive reconstruction.', status: 'NEW_SCENE_PROPOSAL_NOT_GENERATED',
});
visualProposal.push({
  id: 'engine-phase8-expo-visitors-01', chapter: 'engine',
  prompt: 'Cute storybook editorial wide view of an anonymous group of Japanese and foreign visitors inside a generic 1970 Osaka Expo sushi kiosk, plain clothing and decor, no identifiable person, pavilion, brand sign, queue length, country flag or invented reaction.',
  source_indices: [0], why: 'J-Net21 reports foreign as well as Japanese visitors; avoid any invented individual visitor or measurable crowd outcome.', status: 'NEW_SCENE_PROPOSAL_NOT_GENERATED',
});
visualProposal.push({
  id: 'turn-phase8-irie-01', chapter: 'turn', method: 'source_card',
  prompt: 'Cute storybook source card only: 1978 April, the Ishino Group company history names Dai Masu Shoji as Kurukuru Sushi chain headquarters and Irie as its first directly managed restaurant. Separate, blank cards for 1975 Kanazawa operator unknown and Genroku; no imagined Irie facade or corporate relationship beyond the named source entry.',
  source_indices: [5], why: 'The named 1978 entity and direct-store scope answer L01 without attributing the 1975 Kanazawa store to the equipment company.', status: 'NEW_SOURCE_CARD_PROPOSAL_NOT_GENERATED',
});
visualProposal.push({
  id: 'turn-phase7-datecard-01', chapter: 'turn', method: 'source_card',
  prompt: 'Editorial source card only: Ishino Group market timeline lists sales of an automatic sushi-forming machine in 1978. Do not depict a demonstration, exact machine model, showroom or Genroku Expo operation.',
  source_indices: [4], why: 'Retires the unsupported Phase6 robot demonstration illustration and preserves the precise limited claim.', status: 'NEW_SOURCE_CARD_PROPOSAL_NOT_GENERATED',
});
visualProposal.push({
  id: 'turn-phase7-export-01', chapter: 'turn', method: 'source_card',
  prompt: 'Editorial source card only: Ishino Group corporate history records its first exported sushi conveyor delivered to Honolulu in September 1980. Do not depict a Genroku branch or unspecified recipient.',
  source_indices: [5], why: 'New t21 source-bound export event is an equipment shipment, not a restaurant opening.', status: 'NEW_SOURCE_CARD_PROPOSAL_NOT_GENERATED',
});
assert(visualProposal.length === 15 && visualProposal.some((scene) => scene.id === 'hook-s006' && !/straight lane|straight conveyor|直線/u.test(scene.prompt)), 'opening image reveals straight-lane payoff');
assert(visualProposal.some((scene) => scene.id === 'turn-s072' && /straight serving conveyor/u.test(scene.prompt)), 'straight-lane reveal not at T04');
assert(visualProposal.some((scene) => scene.id === 'turn-phase7-datecard-01' && scene.method === 'source_card'), '1978 equipment must remain a source card');
assert(!visualProposal.some((scene) => /1975 Kanazawa.*(operator|vendor)/iu.test(scene.prompt) && scene.id !== 'turn-phase8-irie-01'), '1975 shop identity cannot be illustrated as vendor operation');
assert(newClaims.every((claim) => visualProposal.some((scene) => scene.id === claim.proposed_scene && scene.source_indices.includes(claim.source))), 'new claim lacks source-aligned scene proposal');

const displaySources = plan.sources.map((item, index) => `- [${index}] [${item.publisher}](${item.url})`).join('\n');
let manuscript = '# B18｜迴轉壽司如何從小店的一盤走出去？\n\n';
manuscript += '**隔離的 Phase 8 全文候選，正式製作 HOLD。** 僅 `>` 區塊朗讀；段號、來源與製作註不朗讀。64 個舊口播主張、1 個退成非口播的舊主張，以及新增六項仍 `UNCHECKED`；此稿未進正式 worker。\n\n';
manuscript += `正文紙上計數 ${bodyUnits} 個漢字／數字／〇，以每分鐘 300 字估 ${bodySecondsAt300} 秒。真實 TTS、畫面節奏與 9–11 分鐘驗收尚未測量；5 秒片頭及 21 秒片尾不得充當正文。\n\n`;
let currentChapter = null;
for (const key of activeKeys) {
  const chapter = chapterFor(key);
  if (chapter !== currentChapter) {
    manuscript += `## ${headings[chapter]}\n\n`;
    currentChapter = chapter;
  }
  manuscript += `### ${key}\n\n> ${paragraphs[key]}\n\n`;
  manuscript += `非口播：來源 ${sourcesFor[key].map((index) => `[${index}]`).join('')}；Phase 4 留存 claim ${existingClaimsByParagraph[key].join('、') || '無'}${newClaims.filter((claim) => claim.paragraph === key).map((claim) => `；新增待查 ${claim.id}`).join('')}。\n\n`;
  if (key === 'H02') manuscript += '**接既有 5 秒片頭動畫；下一章才恢復旁白。**\n\n';
}
manuscript += '**旁白後接既有 21 秒片尾動畫及 YouTube 結束畫面位置；尚未生成或驗證連結。**\n\n## 來源（非口播）\n\n';
manuscript += `${displaySources}\n\n`;
manuscript += '本稿保留來源歧異：撲克牌／名片不可合成同一幕；法院僅認特定第 579776 號餐台實用新案於 1972 年屆滿，不採其他資料的 1978 年為同一權利到期日；1967 仙台／東京展店屬獲授權的另一家公司；1985 年機器與另存早期板片不可畫成一台。\n';
manuscript += '石野集團市場年表的 1975 年金澤「一號店」經營者未明；公司沿革明確命名 1978 年大増商事的入江「直營一號店」，兩者不能混為同一店或同一主體。1978 年市場年表的機器販售與公司沿革 1980 年自家製造販售也不能合成同一款。大増商事的店、石野／北日本カコー的機器和出口紀錄均不等於元祿分店或白石萬博店的設備使用證據。\n';

const phase7Voices = [...read(pins.phase7_script[0]).matchAll(/^> (.+)$/gmu)].map((match) => match[1]);
assert(phase7Voices.length === keys.length && phase7Loops.loops.length === loopInput.loops.length, 'Phase7 delta input shape drift');
const phase7LoopById = new Map(phase7Loops.loops.map((loop) => [loop.id, loop]));
const phase7VisualById = new Map(json(join(phase7, 'visual-proposal.json')).scenes.map((scene) => [scene.id, scene]));
const phase7Revisions = json(join(phase7, 'paragraph-overrides.json'));
const phase7NewClaims = phase7Revisions.new_claims;
const phase7SourceEvidence = json(join(phase7, 'source-evidence.json'));
const phase7Delta = {
  schema_version: 1, phase7_sha256: pins.phase7_script[1],
  changed_paragraphs: keys.flatMap((key, index) => phase7Voices[index] === paragraphs[key] ? [] : [{ paragraph: key, before: phase7Voices[index], after: omitted.has(key) ? null : paragraphs[key] }]),
  omitted_paragraphs: [...omitted],
  moved_claim_anchors: revisions.claim_moves,
  revised_claim_anchors: Object.fromEntries(Object.entries(revisions.claim_revisions).map(([id, after]) => [id, { before: oldClaims.find((claim) => claim.id === id).claim, after }])),
  unspoken_old_claim_ids: revisions.unspoken_claim_ids,
  changed_loops: loopInput.loops.flatMap((loop) => {
    const oldLoop = phase7LoopById.get(loop.id);
    assert(oldLoop, `Phase7 loop missing ${loop.id}`);
    return JSON.stringify(oldLoop) === JSON.stringify(loop) ? [] : [{ id: loop.id, before: oldLoop, after: loop }];
  }),
  added_claim_ids: newClaims.filter((claim) => !phase7NewClaims.some((prior) => prior.id === claim.id)).map((claim) => claim.id),
  revised_new_claims: newClaims.flatMap((claim) => {
    const prior = phase7NewClaims.find((item) => item.id === claim.id);
    const { verdict, proposed_scene, ...bare } = claim;
    return prior && JSON.stringify(prior) !== JSON.stringify(bare) ? [{ id: claim.id, before: prior, after: bare }] : [];
  }),
  source_additions: { before: phase7Revisions.source_additions, after: revisions.source_additions },
  source_evidence: { before: phase7SourceEvidence, after: sourceEvidence },
  changed_visual_proposals: visualProposal.flatMap((scene) => {
    const previous = phase7VisualById.get(scene.id);
    return previous && JSON.stringify(previous) === JSON.stringify(scene) ? [] : [{ id: scene.id, before: previous ?? null, after: scene }];
  }),
  retired_visual_proposals: [...phase7VisualById.keys()].filter((id) => !visualProposal.some((scene) => scene.id === id)),
  status: 'EXACT_TEXT_DELTA_NOT_FORMAL_REVIEW',
};

const outputs = {
  'B18.md': manuscript,
  'paragraph-evidence.json': stringify({ schema_version: 1, status: 'PAPER_EDITION_HOLD', body_units_han_digits: bodyUnits, paper_body_seconds_300cpm: bodySecondsAt300, paper_target_9_to_11_minutes: targetPaperRange, actual_tts_seconds: null, timeline }),
  'claim-scene-alignment.json': stringify({ schema_version: 1, status: 'PROVISIONAL_SCENE_REFLOW_REQUIRED', existing_claims: oldClaims.filter((claim) => !revisions.unspoken_claim_ids.includes(claim.id)).map((claim) => { const originalParagraph = claim.note.match(/([HOIETN]\d{2})/u)[1]; const paragraph = revisions.claim_moves[claim.id] ?? originalParagraph; return { id: claim.id, paragraph, original_paragraph: originalParagraph, anchor: revisions.claim_revisions[claim.id] ?? claim.claim, original_anchor: claim.claim, phase4_scene: claim.scene, source: claim.source, fact: claim.fact, verdict: 'UNCHECKED', note: 'Phase4 scene is a provenance pointer only; Phase8 shot/claim alignment awaits independent review.' }; }), unspoken_old_claims: unspokenClaims, new_claims: newClaims }),
  'loop-audit.json': stringify({ schema_version: 1, status: 'PAPER_LOOPS_PENDING_BLIND_LISTEN', body_seconds_300cpm: bodySecondsAt300, loops: loopAudit }),
  'visual-proposal.json': stringify({ schema_version: 1, status: 'TEXT_PROMPTS_ONLY_NOT_ADOPTED', scenes: visualProposal }),
  'phase7-delta.json': stringify(phase7Delta),
};
const manifest = {
  schema_version: 1, status: 'ISOLATED_PHASE8_EDITORIAL_HOLD',
  pinned_sources: Object.fromEntries(Object.entries(pins).map(([name, [, expected]]) => [name, expected])),
  input_sha256: Object.fromEntries(['build.mjs', 'paragraph-overrides.json', 'loops.json', 'source-evidence.json'].map((name) => [name, hashFile(join(here, name))])),
  output_sha256: Object.fromEntries(Object.entries(outputs).map(([name, text]) => [name, sha(text)])),
  body_units_han_digits: bodyUnits, paper_body_seconds_300cpm: bodySecondsAt300, paper_target_9_to_11_minutes: targetPaperRange,
  actual_tts_seconds: null, formal_fact_review: false, formal_script_review: false, worker_adopted: false, media_generated: false,
};
const write = process.argv.includes('--write');
const check = process.argv.includes('--check');
assert(write !== check, 'choose exactly one of --write or --check');
if (write) {
  for (const [name, contents] of Object.entries(outputs)) writeFileSync(join(here, name), contents);
  writeFileSync(join(here, 'manifest.json'), stringify(manifest));
} else {
  for (const [name, contents] of Object.entries(outputs)) assert(read(join(here, name)) === contents, `output drift ${name}`);
  assert(read(join(here, 'manifest.json')) === stringify(manifest), 'manifest drift');
}
console.log(`B18_PHASE8_OFFLINE_HOLD voiced_paragraphs=${activeKeys.length} old_claim_anchors=${oldClaims.length} unspoken_old_claims=${unspokenClaims.length} new_claims=${newClaims.length} loops=${loopAudit.length} paper_seconds_300cpm=${bodySecondsAt300} paper_target=${targetPaperRange}`);
