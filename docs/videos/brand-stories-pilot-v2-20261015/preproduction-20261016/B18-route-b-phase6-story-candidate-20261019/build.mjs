import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const base = resolve(here, '..');
const phase4 = join(base, 'B18-route-b-phase4-candidate-20261017');
const phase5 = join(base, 'B18-route-b-phase5-hook-diagnostic-20261018');
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
assert(Object.keys(revisions.overrides).every((key) => keys.includes(key)), 'unknown paragraph override');

const source = read(pins.phase4_script[0]);
const voices = [...source.matchAll(/^> (.+)$/gmu)].map((match) => match[1]);
const notes = [...source.matchAll(/^\*\*製作註 ([HOIETN]\d{2})（不朗讀）\*\*：([^\n]*)$/gmu)];
assert(voices.length === keys.length && notes.length === keys.length, 'Phase4 script paragraph/note shape drift');
const paragraphs = Object.fromEntries(keys.map((key, index) => {
  assert(notes[index][1] === key, `Phase4 note order drift ${key}`);
  const text = revisions.overrides[key] ?? voices[index];
  assert(typeof text === 'string' && text.length > 5, `empty narration ${key}`);
  return [key, text];
}));
const sourcesFor = Object.fromEntries(keys.map((key, index) => [key, [...new Set([...notes[index][2].matchAll(/\[(\d+)\]/gu)].map((match) => Number(match[1])))].sort((a, b) => a - b)]));
assert(Object.values(sourcesFor).every((sources) => sources.length && sources.every((number) => number >= 0 && number < plan.sources.length)), 'bad source index in inherited note');
const existingClaimsByParagraph = Object.fromEntries(keys.map((key) => [key, []]));
for (const claim of oldClaims) {
  const match = claim.note.match(/([HOIETN]\d{2})/u);
  assert(match && keys.includes(match[1]), `claim paragraph missing ${claim.id}`);
  const paragraph = match[1];
  assert(paragraphs[paragraph].includes(claim.claim), `old claim anchor removed ${claim.id} in ${paragraph}`);
  assert(oldCoverage.source_to_scene[paragraph].scene_ids.includes(claim.scene), `old claim scene not in paragraph ${claim.id}`);
  assert(sourcesFor[paragraph].includes(claim.source), `old claim source not in paragraph ${claim.id}`);
  existingClaimsByParagraph[paragraph].push(claim.id);
}
assert(oldClaims.length === 65 && oldClaims.every((claim) => claim.verdict === 'UNCHECKED'), 'old claim review state drift');

const newClaims = revisions.new_claims.map((claim) => {
  assert(keys.includes(claim.paragraph) && paragraphs[claim.paragraph].includes(claim.anchor), `new claim anchor missing ${claim.id}`);
  assert(!oldClaims.some((old) => old.id === claim.id), `new claim id collision ${claim.id}`);
  assert(sourcesFor[claim.paragraph].includes(claim.source), `new claim source missing ${claim.id}`);
  return { ...claim, verdict: 'UNCHECKED', proposed_scene: claim.id === 'e14' ? 'engine-s046b' : 'turn-phase6-robot-01' };
});
assert(newClaims.length === 2 && newClaims.some((claim) => claim.id === 't19'), 'two new source claims expected');

const units = (text) => (text.match(/[\p{Script=Han}0-9〇]/gu) ?? []).length;
const bodyUnits = keys.reduce((sum, key) => sum + units(paragraphs[key]), 0);
const bodySecondsAt300 = Number((bodyUnits / 5).toFixed(1));
const targetPaperRange = bodyUnits >= 2700 && bodyUnits <= 3300;
const timeline = [];
let cursor = 0;
for (const key of keys) {
  const duration = units(paragraphs[key]) / 5;
  timeline.push({ paragraph: key, chapter: chapterFor(key), source_indices: sourcesFor[key], claim_ids: existingClaimsByParagraph[key], paper_start_seconds_300cpm: Number(cursor.toFixed(1)), paper_end_seconds_300cpm: Number((cursor + duration).toFixed(1)) });
  cursor += duration;
}

const indexOf = (key) => keys.indexOf(key);
const loopAudit = loopInput.loops.map((loop) => {
  const setupIndex = indexOf(loop.setup_paragraph);
  const obstacleIndex = indexOf(loop.obstacle_paragraph);
  const payoffIndex = indexOf(loop.payoff_paragraph);
  assert(setupIndex >= 0 && setupIndex < obstacleIndex && obstacleIndex <= payoffIndex, `loop chronology ${loop.id}`);
  const setupText = paragraphs[loop.setup_paragraph];
  const payoffText = paragraphs[loop.payoff_paragraph];
  assert(setupText.includes(loop.setup_phrase) && payoffText.includes(loop.payoff_phrase), `loop phrase missing ${loop.id}`);
  assert(loop.source_indices.every((number) => number >= 0 && number < plan.sources.length), `loop source out of range ${loop.id}`);
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
  return { id: scene.id, chapter: scene.chapter, prompt: scene.proposed_prompt, source_indices: sourceIndices, why: scene.narrative_reason, status: 'TEXT_ONLY_NOT_GENERATED' };
});
visualProposal.push({
  id: 'turn-phase6-robot-01', chapter: 'turn',
  prompt: 'Medium editorial illustration in an undated late-1970s Japanese equipment showroom, one anonymous technician demonstrating a generic automatic sushi-forming machine on a plain workbench, an empty separate serving conveyor in the background, no logos or readable text, no Expo imagery.',
  source_indices: [4], why: 'The 1978 vendor equipment answers the later preparation question while remaining separate from Genroku and Expo operations.', status: 'NEW_SCENE_PROPOSAL_NOT_GENERATED',
});
assert(visualProposal.length === 9 && visualProposal.some((scene) => scene.id === 'hook-s006' && !/straight lane|straight conveyor|直線/u.test(scene.prompt)), 'opening image reveals straight-lane payoff');
assert(visualProposal.some((scene) => scene.id === 'turn-s072' && /straight serving conveyor/u.test(scene.prompt)), 'straight-lane reveal not at T04');

const displaySources = plan.sources.map((item, index) => `- [${index}] [${item.publisher}](${item.url})`).join('\n');
let manuscript = '# B18｜迴轉壽司如何從小店的一盤走出去？\n\n';
manuscript += '**隔離的 Phase 6 全文候選，正式製作 HOLD。** 僅 `>` 區塊朗讀；段號、來源與製作註不朗讀。全部舊主張與新增兩項仍 `UNCHECKED`；此稿未進正式 worker。\n\n';
manuscript += `正文紙上計數 ${bodyUnits} 個漢字／數字／〇，以每分鐘 300 字估 ${bodySecondsAt300} 秒。真實 TTS、畫面節奏與 9–11 分鐘驗收尚未測量；5 秒片頭及 21 秒片尾不得充當正文。\n\n`;
let currentChapter = null;
for (const key of keys) {
  const chapter = chapterFor(key);
  if (chapter !== currentChapter) {
    manuscript += `## ${headings[chapter]}\n\n`;
    currentChapter = chapter;
  }
  manuscript += `### ${key}\n\n> ${paragraphs[key]}\n\n`;
  manuscript += `非口播：來源 ${sourcesFor[key].map((index) => `[${index}]`).join('')}；Phase 4 留存 claim ${existingClaimsByParagraph[key].join('、') || '無'}${newClaims.filter((claim) => claim.paragraph === key).map((claim) => `；新增待查 ${claim.id}`).join('')}。\n\n`;
  if (key === 'H03') manuscript += '**接既有 5 秒片頭動畫；下一章才恢復旁白。**\n\n';
}
manuscript += '**旁白後接既有 21 秒片尾動畫及 YouTube 結束畫面位置；尚未生成或驗證連結。**\n\n## 來源（非口播）\n\n';
manuscript += `${displaySources}\n\n`;
manuscript += '本稿保留來源歧異：撲克牌／名片不可合成同一幕；法院僅認特定第 579776 號餐台實用新案於 1972 年屆滿，不採其他資料的 1978 年為同一權利到期日；1967 仙台／東京展店屬獲授權的另一家公司；1985 年機器與另存早期板片不可畫成一台。\n';

const outputs = {
  'B18.md': manuscript,
  'paragraph-evidence.json': stringify({ schema_version: 1, status: 'PAPER_EDITION_HOLD', body_units_han_digits: bodyUnits, paper_body_seconds_300cpm: bodySecondsAt300, paper_target_9_to_11_minutes: targetPaperRange, actual_tts_seconds: null, timeline }),
  'claim-scene-alignment.json': stringify({ schema_version: 1, status: 'PROVISIONAL_SCENE_REFLOW_REQUIRED', existing_claims: oldClaims.map((claim) => ({ id: claim.id, paragraph: claim.note.match(/([HOIETN]\d{2})/u)[1], anchor: claim.claim, phase4_scene: claim.scene, source: claim.source, fact: claim.fact, verdict: 'UNCHECKED', note: 'Anchor remains in the same paragraph; Phase6 scene line has not been rebuilt or formally checked.' })), new_claims: newClaims }),
  'loop-audit.json': stringify({ schema_version: 1, status: 'PAPER_LOOPS_PENDING_BLIND_LISTEN', body_seconds_300cpm: bodySecondsAt300, loops: loopAudit }),
  'visual-proposal.json': stringify({ schema_version: 1, status: 'TEXT_PROMPTS_ONLY_NOT_ADOPTED', scenes: visualProposal }),
};
const manifest = {
  schema_version: 1, status: 'ISOLATED_PHASE6_EDITORIAL_HOLD',
  pinned_sources: Object.fromEntries(Object.entries(pins).map(([name, [, expected]]) => [name, expected])),
  input_sha256: Object.fromEntries(['build.mjs', 'paragraph-overrides.json', 'loops.json'].map((name) => [name, hashFile(join(here, name))])),
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
console.log(`B18_PHASE6_OFFLINE_HOLD paragraphs=25 old_claim_anchors=65 new_claims=2 loops=${loopAudit.length} paper_seconds_300cpm=${bodySecondsAt300} paper_target=${targetPaperRange}`);
