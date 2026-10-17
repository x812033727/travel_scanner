import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = dirname(fileURLToPath(import.meta.url));
const base = resolve(dir, '..');
const flow = join(base, 'B18-attribution-flow-candidate-20261017');
const row10b = join(base, 'B18-route-b-row10b-candidate-20261017');
const planDir = join(base, 'B18-fullscript-route-b-plan-20261017');
const reviewed = join(base, 'B18-spoken-source-cadence-candidate-20261017');
const chapters = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const read = (path) => readFileSync(path, 'utf8');
const json = (path) => JSON.parse(read(path));
const sha = (data) => createHash('sha256').update(data).digest('hex');
const hashFile = (path) => sha(readFileSync(path));
const stringify = (value) => `${JSON.stringify(value, null, 2)}\n`;
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const canon = (text) => text.replace(/\s+/gu, '');
const units = (text) => [...text].length;

const pins = {
  fullscript: ['B18.md', '7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1', reviewed],
  script_review: ['review-candidate.md', '603f0a5340b197cc6cbe527991e63bb1629c4f1245e780fdb3981109dea871d4', reviewed],
  scene_plan: ['route-b-plan.json', '3b3183525d995950bc9366ecffd82595938817eca09a8a4d6ca95100d1e88985', planDir],
  row10b: ['B18.json', '6c2eb6172d0afc6d5c92a91736cf1ad606ea3302d904c749d42d1b74533b14bc', row10b],
  row10b_review: ['INDEPENDENT-ROW10B-REVIEW-ADDENDUM.md', 'f716d95f6b69d4e250759bc696fd9f3ca9d1c6e63e868cb8e0efa5981e8ff1aa', row10b],
  old_flow: ['sha256.json', '8b77652b8263fd33b02a95a3ee1288e85f96d6a847b4b88c2efd488a84ca3754', flow],
};
for (const [key, [filename, expected, folder]] of Object.entries(pins)) {
  assert(hashFile(join(folder, filename)) === expected, `source pin drift ${key}`);
}

const design = json(join(dir, 'design.json'));
const plan = json(join(planDir, 'route-b-plan.json'));
const old = Object.fromEntries(chapters.map((key) => [key, json(join(flow, 'remapped-chapters', `${key}.json`))]));
const text = read(join(reviewed, 'B18.md'));
const paragraphs = [...text.matchAll(/^>\s*(.+)$/gmu)].map((match) => match[1]);
const keys = Object.keys(plan.paragraph_scene_map);
assert(paragraphs.length === 25 && keys.length === 25, 'expected 25 reviewed voice paragraphs');
const para = Object.fromEntries(keys.map((key, i) => [key, paragraphs[i]]));

// Clause punctuation is kept verbatim. A long clause may be divided only when
// necessary to keep a 5–12 second scene plausible; readback checks every word.
function atoms(text) {
  const raw = text.match(/[^，。；：？！、]+[，。；：？！、]?/gu) ?? [text];
  const out = [];
  for (const piece of raw) {
    if (units(piece) <= 42) { out.push(piece); continue; }
    let rest = piece;
    while (units(rest) > 42) {
      const glyphs = [...rest];
      let cut = 39;
      for (let i = 30; i <= 42; i += 1) if (/\s/u.test(glyphs[i] ?? '')) cut = i + 1;
      out.push(glyphs.slice(0, cut).join(''));
      rest = glyphs.slice(cut).join('');
    }
    if (rest) out.push(rest);
  }
  assert(out.join('') === text, 'atom split changed voice');
  return out;
}
function segmentVoice(text, count) {
  const a = atoms(text);
  const n = a.length;
  assert(n >= count, `too few clauses for ${count} scenes`);
  const len = Array.from({ length: n }, () => Array(n + 1).fill(0));
  for (let i = 0; i < n; i += 1) for (let j = i + 1; j <= n; j += 1) len[i][j] = units(a.slice(i, j).join(''));
  const dp = Array.from({ length: count + 1 }, () => Array(n + 1).fill(Infinity));
  const prev = Array.from({ length: count + 1 }, () => Array(n + 1).fill(-1));
  dp[0][0] = 0;
  const target = units(text) / count;
  for (let groups = 1; groups <= count; groups += 1) {
    for (let end = groups; end <= n; end += 1) {
      for (let start = groups - 1; start < end; start += 1) {
        if (!Number.isFinite(dp[groups - 1][start])) continue;
        const size = len[start][end];
        const overflow = Math.max(0, size - 42);
        const tiny = Math.max(0, 10 - size);
        const cost = dp[groups - 1][start] + (size - target) ** 2 + overflow ** 2 * 200 + tiny ** 2 * 5;
        if (cost < dp[groups][end]) { dp[groups][end] = cost; prev[groups][end] = start; }
      }
    }
  }
  assert(Number.isFinite(dp[count][n]), 'voice segmentation failed');
  const chunks = [];
  let end = n;
  for (let groups = count; groups > 0; groups -= 1) {
    const start = prev[groups][end];
    chunks.unshift(a.slice(start, end).join(''));
    end = start;
  }
  assert(chunks.join('') === text, 'segmented voice differs');
  return chunks;
}
function splitLines(chunk) {
  if (units(chunk) <= 40) return [chunk];
  const glyphs = [...chunk];
  let cut = Math.ceil(glyphs.length / 2);
  for (let offset = 0; offset <= 12; offset += 1) {
    for (const index of [cut - offset, cut + offset]) {
      if (/[，。；：？！、]/u.test(glyphs[index - 1] ?? '')) { cut = index; offset = 13; break; }
    }
  }
  return [glyphs.slice(0, cut).join(''), glyphs.slice(cut).join('')];
}

const oldScene = new Map(chapters.flatMap((key) => old[key].scenes.map((scene) => [scene.id, scene])));
const extra = new Map(design.additional_scenes.map((row) => [row.after, row]));
assert(extra.size === 7, 'expected seven distinct extra shots');
const map = {};
const sceneParagraph = {};
const sceneIndex = {};
const all = [];
const usedOld = new Set();
for (const key of keys) {
  const ids = [];
  for (const id of plan.paragraph_scene_map[key]) {
    assert(oldScene.has(id) && !usedOld.has(id), `missing/reused old scene ${id}`);
    usedOld.add(id); ids.push(id);
    if (extra.has(id)) {
      assert(extra.get(id).paragraph === key, `extra paragraph mismatch ${id}`);
      ids.push(extra.get(id).id);
    }
  }
  map[key] = ids;
  const chunks = segmentVoice(para[key], ids.length);
  ids.forEach((id, i) => {
    const source = oldScene.get(id);
    const added = design.additional_scenes.find((entry) => entry.id === id);
    const override = design.scene_overrides[id];
    const template = added ? 'shot' : override?.template ?? source.template;
    const data = structuredClone(added ? added.data : override?.data ?? source.data);
    const lines = splitLines(chunks[i]).map((part, li) => ({
      id: sha(`${id}\u0000${li}\u0000${part}`).slice(0, 8), text: part.trim(),
    }));
    assert(lines.every((line) => line.text && units(line.text) <= 40), `long/empty line ${id}`);
    const scene = { id, template, data, lines };
    sceneParagraph[id] = key;
    sceneIndex[id] = i;
    all.push(scene);
  });
}
assert(usedOld.size === 85 && all.length === 92, `scene count ${usedOld.size}/${all.length}`);
assert(all.map((scene) => scene.id).every((id, i, arr) => arr.indexOf(id) === i), 'duplicate scene id');
assert(canon(all.flatMap((scene) => scene.lines.map((line) => line.text)).join('')) === canon(paragraphs.join('')), 'fullscript voice byte order differs after space normalization');

const bindings = json(join(dir, 'claim-bindings.json'));
const oldClaims = chapters.flatMap((key) => old[key].claims.map((claim) => ({ ...claim, chapter: key })));
const ids = oldClaims.map((claim) => claim.id);
assert(oldClaims.length === 65 && Object.keys(bindings).length === 65, '65 claim binding count');
assert(ids.every((id) => Object.hasOwn(bindings, id)) && Object.keys(bindings).every((id) => ids.includes(id)), '65 IDs not exactly preserved');
const claims = oldClaims.map((claim) => {
  const bind = bindings[claim.id];
  const spoken = para[bind.paragraph];
  const start = spoken.indexOf(bind.anchor);
  assert(start >= 0, `claim ${claim.id} anchor missing from ${bind.paragraph}`);
  const sequence = map[bind.paragraph];
  let cumulative = 0;
  let sceneId = sequence.at(-1);
  for (const id of sequence) {
    const size = all.find((scene) => scene.id === id).lines.map((line) => line.text).join('').length;
    if (start < cumulative + size) { sceneId = id; break; }
    cumulative += size;
  }
  const result = {
    id: claim.id,
    claim: bind.claim ?? bind.anchor,
    scene: bind.scene ?? sceneId,
    source: Object.hasOwn(bind, 'source') ? bind.source : claim.source,
    fact: Object.hasOwn(bind, 'fact') ? bind.fact : claim.fact,
    verdict: 'UNCHECKED',
    note: `隔離候選；${bind.paragraph} 口播定位「${bind.anchor}」；未送正式 verifier。${bind.note ?? ''}`,
  };
  assert(map[bind.paragraph].includes(result.scene), `claim ${claim.id} scene outside paragraph`);
  return result;
});
assert(claims.find((row) => row.id === 't18').scene === 'turn-s088' && claims.find((row) => row.id === 't18').source === 2 && claims.find((row) => row.id === 't18').fact === null, 'pre-verifier t18 route incorrect');
for (const [id, fact] of [['h7', 9], ['i1', 3], ['i5', 3], ['e9', 6], ['n7', 3]]) assert(claims.find((row) => row.id === id).fact === fact, `${id} fact trace lost`);
const crossSceneClaims = claims.filter((claim) => {
  const binding = bindings[claim.id];
  const scene = all.find((row) => row.id === claim.scene);
  return !canon(scene.lines.map((line) => line.text).join('')).includes(canon(binding.anchor));
}).map((claim) => ({ id: claim.id, scene: claim.scene, paragraph: bindings[claim.id].paragraph, exact_voice_anchor: bindings[claim.id].anchor }));

const row = json(join(row10b, 'B18.json'));
assert(row.must_verify.length === 10, '10 fact schema drift');
assert(row.must_verify[4].claim.includes('1967') && row.must_verify[4].claim.includes('1972'), 'court fact scope drift');
assert(row.must_verify[9].claim.includes('後場') && !row.must_verify[9].claim.includes('盤色'), 'backroom fact scope drift');
assert(row.sources[2].supports.includes('盤色或裝飾'), 'plate-pricing source support drift');

const chaptersOut = {};
for (const key of chapters) {
  const scenes = all.filter((scene) => scene.id.startsWith(`${key}-`));
  const chapterClaims = claims.filter((claim) => claim.scene.startsWith(`${key}-`));
  chaptersOut[key] = { key, title: old[key].title, scenes, claims: chapterClaims, loops: [], ...(key === 'hook' ? { thumbnail_shot: old.hook.thumbnail_shot } : {}) };
}
const lineFor = (paragraph, word) => {
  const scene = all.find((row) => map[paragraph].includes(row.id) && row.lines.some((line) => line.text.includes(word)));
  assert(scene, `loop word absent ${paragraph}: ${word}`);
  return scene.lines.find((line) => line.text.includes(word)).id;
};
chaptersOut.hook.loops = [
  { setup: lineFor('H02', '這道彎怎麼過'), payoff: lineFor('I03', '沿著吧台角落轉向'), what: '堵帶掉盤的轉角如何走通' },
  { setup: lineFor('H02', '盤子能跟上人潮'), payoff: lineFor('E05', '壽司仍得由人先備好'), what: '萬博客流下送餐與備料怎麼調整' },
  { setup: lineFor('H02', '後場送到客席'), payoff: lineFor('T04', '送到用餐區'), what: '後場做好的一盤如何送到客席' },
];

const oldCards = chapters.flatMap((key) => old[key].scenes).filter((scene) => scene.template === 'title').length;
const shots = all.filter((scene) => scene.template === 'shot').length;
const cards = all.filter((scene) => scene.template === 'title').length;
let longestCards = 0, run = 0;
for (const scene of all) { run = scene.template === 'title' ? run + 1 : 0; longestCards = Math.max(run, longestCards); }
const paragraphCoverage = Object.fromEntries(keys.map((key) => [key, {
  scene_ids: map[key], source: para[key], reconstructed: map[key].map((id) => all.find((scene) => scene.id === id).lines.map((line) => line.text).join('')).join(''),
  visible_chars: units(para[key]), scenes: map[key].length,
  max_scene_visible_chars: Math.max(...map[key].map((id) => units(all.find((scene) => scene.id === id).lines.map((line) => line.text).join('')))),
}]));
for (const [key, row] of Object.entries(paragraphCoverage)) assert(canon(row.source) === canon(row.reconstructed), `paragraph ${key} not fully covered`);
const coverage = {
  schema_version: 1,
  status: 'OFFLINE_DRAFT_HOLD',
  exact_source_pins: Object.fromEntries(Object.entries(pins).map(([key, [file, digest]]) => [key, { file, sha256: digest }])),
  paragraph_coverage: paragraphCoverage,
  scene_count: all.length,
  prior_scene_count: oldScene.size,
  additional_scene_ids: design.additional_scenes.map((row) => row.id),
  shot_count: shots,
  card_count: cards,
  prior_card_count: oldCards,
  illustration_ratio: shots / all.length,
  max_consecutive_cards: longestCards,
  claim_ids: ids,
  claim_count: claims.length,
  unchecked_count: claims.filter((row) => row.verdict === 'UNCHECKED').length,
  cross_scene_claims: crossSceneClaims,
  scenes_over_42_visible_chars: all.filter((scene) => units(scene.lines.map((line) => line.text).join('')) > 42).map((scene) => ({ id: scene.id, visible_chars: units(scene.lines.map((line) => line.text).join('')) })),
  t18_pre_verifier_route: claims.find((row) => row.id === 't18'),
  approximate_300_han_per_minute_spoken_seconds: 2667 / 300 * 60,
  measured_tts_seconds: null,
  illustrative_added_image_list_price_usd: 7 * 0.0035,
  illustrative_shot_only_extra_19_image_list_price_usd: 19 * 0.0035,
  timing_status: 'HOLD_TTS_UNMEASURED',
  worker_status: 'HOLD_19_TITLE_CARDS_REJECTED_BY_READ_CHAPTER_ANSWER',
};
assert(cards === 19 && shots === 73 && shots / all.length >= .7 && longestCards <= 3, 'visual quota or card run changed');

const outputs = {
  'paragraph-coverage.json': coverage,
  'claim-coverage.json': { schema_version: 1, status: 'ALL_65_UNCHECKED_HOLD', claims },
  ...Object.fromEntries(chapters.map((key) => [`remapped-chapters/${key}.json`, chaptersOut[key]])),
};
const manifest = { schema_version: 1, status: 'OFFLINE_DRAFT_HOLD', pins: Object.fromEntries(Object.entries(pins).map(([key, [, digest]]) => [key, digest])), inputs: {
  'build.mjs': hashFile(join(dir, 'build.mjs')),
  'design.json': hashFile(join(dir, 'design.json')),
  'claim-bindings.json': hashFile(join(dir, 'claim-bindings.json')),
  'verify-worker.mjs': hashFile(join(dir, 'verify-worker.mjs')),
  'README.md': hashFile(join(dir, 'README.md')),
}, files: {} };
for (const [file, value] of Object.entries(outputs)) manifest.files[file] = sha(stringify(value));
const write = process.argv.includes('--write');
const check = process.argv.includes('--check');
assert(write !== check, 'use --write or --check');
if (write) {
  for (const [file, value] of Object.entries(outputs)) {
    const target = join(dir, file); mkdirSync(dirname(target), { recursive: true }); writeFileSync(target, stringify(value));
  }
  writeFileSync(join(dir, 'sha256.json'), stringify(manifest));
} else {
  for (const [file, value] of Object.entries(outputs)) assert(read(join(dir, file)) === stringify(value), `generated file drift ${file}`);
  assert(read(join(dir, 'sha256.json')) === stringify(manifest), 'manifest drift');
}
console.log(`PASS_OFFLINE_92_SCENE_DRAFT_HOLD scenes=${all.length} shots=${shots} cards=${cards} claims=${claims.length} paragraphs=${keys.length}`);
