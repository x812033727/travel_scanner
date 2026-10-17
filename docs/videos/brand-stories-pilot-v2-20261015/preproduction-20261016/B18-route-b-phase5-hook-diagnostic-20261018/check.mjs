import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const parent = resolve(here, '..');
const phase4 = join(parent, 'B18-route-b-phase4-candidate-20261017');
const row10b = join(parent, 'B18-route-b-row10b-candidate-20261017');
const fullReview = join(parent, 'B18-route-b-phase4-full-editorial-review-20261017.md');
const sha = (file) => createHash('sha256').update(readFileSync(file)).digest('hex');
const requireHash = (file, expected) => {
  const actual = sha(file);
  if (actual !== expected) throw new Error(`${file} drift: ${actual}`);
};
const ids = [
  'H01', 'H02', 'H03', 'O01', 'O02', 'O03', 'O04', 'I01', 'I02', 'I03', 'I04',
  'E01', 'E02', 'E03', 'E04', 'E05', 'T01', 'T02', 'T03', 'T04', 'T05', 'T06',
  'N01', 'N02', 'N03',
];

requireHash(join(phase4, 'B18.md'), '73236441aebc92e804436fd9371a3044a27e5decdd7438905459ef214023768f');
requireHash(join(phase4, 'sha256.json'), 'efdf3994152db18892d70c35f6ae10ba3f1d4a9076078922a8a988ee0bbd7422');
requireHash(join(phase4, 'design.json'), '610e2924544d02e5cc0d3daa210b51d6b4a659ceabbab3b903ade2f4a1fdec99');
requireHash(join(phase4, 'remapped-chapters', 'hook.json'), 'd23323b1c1590d5286304d90dac9a2d87465aa80bdc90f040b8c07290c6d2e25');
requireHash(join(phase4, 'remapped-chapters', 'turn.json'), 'ed35fb524d4fbae005de7804a9cb9c35189fe24fe3417c78f57eddadb79f1dde');
requireHash(join(row10b, 'B18.json'), '6c2eb6172d0afc6d5c92a91736cf1ad606ea3302d904c749d42d1b74533b14bc');
requireHash(fullReview, '52172dd22d2a0d349bea7ff7568cbaa2aecef5ab61d2929ad82048df967d745e');

const script = readFileSync(join(phase4, 'B18.md'), 'utf8');
const paragraphs = [...script.matchAll(/^>\s*(.+)$/gmu)].map((match) => match[1]);
if (paragraphs.length !== ids.length) throw new Error(`expected 25 spoken paragraphs, got ${paragraphs.length}`);
const units = (value) => (String(value).match(/[\p{Script=Han}0-9〇]/gu) ?? []).length;
const times = [];
let sum = 0;
for (let index = 0; index < paragraphs.length; index += 1) {
  const length = units(paragraphs[index]);
  times.push({ id: ids[index], units: length, startSeconds: sum / 5, endSeconds: (sum + length) / 5 });
  sum += length;
}
if (sum !== 2669) throw new Error(`Phase 4 voiced units drift: ${sum}`);

const at = (id, phrase) => {
  const index = ids.indexOf(id);
  const offset = paragraphs[index].indexOf(phrase);
  if (offset < 0) throw new Error(`missing exact spoken anchor ${id}: ${phrase}`);
  return times[index].startSeconds + units(paragraphs[index].slice(0, offset)) / 5;
};
const loops = [
  ['轉角', 'H02', '這道彎怎麼過', 'I03', '沿著吧台角落轉向'],
  ['萬博', 'H02', '盤子能跟上人潮', 'E05', '放上輸送帶'],
  ['後場', 'H02', '後場送到客席', 'T04', '送到用餐區'],
].map(([name, setupId, setup, payoffId, payoff]) => ({
  name, setupId, payoffId,
  setupSeconds: at(setupId, setup),
  payoffSeconds: at(payoffId, payoff),
  openSeconds: at(payoffId, payoff) - at(setupId, setup),
}));
const hook = JSON.parse(readFileSync(join(phase4, 'remapped-chapters', 'hook.json'), 'utf8'));
const turn = JSON.parse(readFileSync(join(phase4, 'remapped-chapters', 'turn.json'), 'utf8'));
const spoiler = hook.scenes.find((scene) => scene.id === 'hook-s006');
if (!spoiler?.data?.prompt?.includes('straight lane')) throw new Error('hook-s006 spoiler prompt changed');
const visualPatch = JSON.parse(readFileSync(join(here, 'visual-patch.json'), 'utf8'));
if (visualPatch.status !== 'ISOLATED_PHASE5_STATIC_PROMPT_PROPOSAL_HOLD') throw new Error('visual patch must remain HOLD');
if (visualPatch.phase4_manifest_sha256 !== 'efdf3994152db18892d70c35f6ae10ba3f1d4a9076078922a8a988ee0bbd7422') throw new Error('visual patch manifest drift');
const wantedScenes = new Set(['hook-s006', 'turn-s081', 'turn-s070', 'turn-s072', 'turn-s075', 'turn-s076', 'turn-s080b', 'turn-s080']);
if (visualPatch.scenes.length !== wantedScenes.size) throw new Error('visual patch must contain eight scenes');
const patched = { hook: structuredClone(hook), turn: structuredClone(turn) };
for (const item of visualPatch.scenes) {
  if (!wantedScenes.delete(item.id)) throw new Error(`unexpected or duplicate visual scene ${item.id}`);
  if (!['hook', 'turn'].includes(item.chapter)) throw new Error(`unexpected chapter for ${item.id}`);
  const sourceScene = { hook, turn }[item.chapter].scenes.find((scene) => scene.id === item.id);
  const proposedScene = patched[item.chapter].scenes.find((scene) => scene.id === item.id);
  if (!sourceScene || !proposedScene) throw new Error(`missing Phase 4 visual scene ${item.id}`);
  if (!sourceScene.lines.some((line) => line.id === item.line_id)) throw new Error(`line anchor drift for ${item.id}`);
  if (sourceScene.data.prompt !== item.original_prompt) throw new Error(`original prompt drift for ${item.id}`);
  if (!item.proposed_prompt || item.proposed_prompt.length < 60 || item.proposed_prompt.length > 400) throw new Error(`invalid proposed prompt for ${item.id}`);
  if (item.proposed_prompt === item.original_prompt) throw new Error(`unchanged proposed prompt for ${item.id}`);
  if (!item.narrative_reason || !item.source_boundary) throw new Error(`missing narrative/source boundary for ${item.id}`);
  if (!Array.isArray(item.source_indices) || item.source_indices.length === 0 || item.source_indices.some((index) => !Number.isInteger(index) || index < 0 || index >= visualPatch.source_urls.length)) throw new Error(`invalid source indices for ${item.id}`);
  if (['hook-s006', 'turn-s070', 'turn-s081'].includes(item.id) && /straight|lane|belt|conveyor|route|track/i.test(item.proposed_prompt)) throw new Error(`premature solution in ${item.id}`);
  if (['turn-s072', 'turn-s075'].includes(item.id) && !/straight (?:serving )?conveyor/i.test(item.proposed_prompt)) throw new Error(`missing T04 solution in ${item.id}`);
  if (['turn-s070', 'turn-s072', 'turn-s075'].includes(item.id) && /\b(?:19|20)\d{2}s?\b/i.test(item.proposed_prompt)) throw new Error(`unsupported date in ${item.id}`);
  if (item.id === 'turn-s076' && /courtroom|judge|trial|\b(?:19|20)\d{2}s?\b/i.test(item.proposed_prompt)) throw new Error(`unsupported dated court image in ${item.id}`);
  if (item.id === 'turn-s080b' && /\b(?:19|20)\d{2}s?\b/i.test(item.proposed_prompt)) throw new Error(`unsupported date in ${item.id}`);
  if (item.id === 'turn-s080' && /envelope|letter|warning|arrow|rights|expire/i.test(item.proposed_prompt)) throw new Error(`causal shorthand in ${item.id}`);
  proposedScene.data.prompt = item.proposed_prompt;
}
if (wantedScenes.size) throw new Error(`missing visual scenes: ${[...wantedScenes].join(', ')}`);
for (const item of visualPatch.scenes) {
  patched[item.chapter].scenes.find((scene) => scene.id === item.id).data.prompt = item.original_prompt;
}
if (JSON.stringify(patched.hook) !== JSON.stringify(hook) || JSON.stringify(patched.turn) !== JSON.stringify(turn)) throw new Error('visual patch touched fields other than data.prompt');
const diagnostic = readFileSync(join(here, 'README.md'), 'utf8');
const examples = [
  { id: 'A', until: '### B.', oldIds: ['H01', 'H02', 'H03'], expectedUnits: 177 },
  { id: 'B', until: '### C.', oldIds: ['E04', 'T01', 'T02'], expectedUnits: 230 },
  { id: 'C', until: '## 現階段結論', oldIds: ['N01', 'N02', 'N03'], expectedUnits: 213 },
].map(({ id, until, oldIds, expectedUnits }) => {
  const section = diagnostic.split(`### ${id}.`)[1]?.split(until)[0];
  if (!section) throw new Error(`missing example ${id}`);
  const voiced = [...section.matchAll(/^>\s*(.+)$/gmu)].map((match) => match[1]);
  if (voiced.length !== 3) throw new Error(`example ${id} must have exactly three voiced paragraphs`);
  const newUnits = units(voiced.join(''));
  const oldUnits = oldIds.reduce((count, oldId) => count + units(paragraphs[ids.indexOf(oldId)]), 0);
  if (newUnits !== expectedUnits) throw new Error(`example ${id} wording changed: ${newUnits}`);
  return { id, oldIds, oldUnits, exampleUnits: newUnits, deltaUnits: newUnits - oldUnits };
});
const hypotheticalUnits = sum + examples.reduce((count, example) => count + example.deltaUnits, 0);

console.log(JSON.stringify({
  status: 'READ_ONLY_PHASE5_HOOK_DIAGNOSTIC_HOLD',
  timingMethod: 'Han + ASCII digits + 〇, 300 units/min; excludes the 5-second intro, 21-second outro, pauses, and actual TTS',
  totalUnits: sum,
  estimatedBodySeconds: sum / 5,
  paragraphs: times,
  existingOpeningLoops: loops,
  openingVisualSpoiler: { scene: spoiler.id, phrase: 'straight lane' },
  visualPatch: { status: visualPatch.status, sceneCount: visualPatch.scenes.length, memoryOnlyChangedField: 'scenes[].data.prompt' },
  isolatedExamples: examples,
  hypotheticalBodySecondsIfAllExamplesUsedWithoutOtherChanges: hypotheticalUnits / 5,
}, null, 2));
