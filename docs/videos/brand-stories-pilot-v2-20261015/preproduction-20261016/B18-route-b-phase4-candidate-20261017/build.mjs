import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = dirname(fileURLToPath(import.meta.url));
const base = resolve(dir, '..');
const phase2 = join(base, 'B18-route-b-92-scene-candidate-20261017');
const row10b = join(base, 'B18-route-b-row10b-candidate-20261017');
const chapters = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const read = (file) => readFileSync(file, 'utf8');
const json = (file) => JSON.parse(read(file));
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const hashFile = (file) => sha(readFileSync(file));
const stringify = (value) => `${JSON.stringify(value, null, 2)}\n`;
const assert = (okay, why) => { if (!okay) throw new Error(why); };
const canon = (value) => String(value).replace(/\s+/gu, '');
const glyphs = (value) => [...String(value)];

const sourcePins = {
  phase2: [join(phase2, 'sha256.json'), '0e8613d06888d285f34b40cb2be9af54372c771676592e3dff0a07491f41ec25'],
  row10b: [join(row10b, 'B18.json'), '6c2eb6172d0afc6d5c92a91736cf1ad606ea3302d904c749d42d1b74533b14bc'],
  phase3: [join(base, 'B18-route-b-worker-compatible-candidate-20261017', 'sha256.json'), '14a2ca7370fcbd817c8d2fce636721780fa4217af2168a5df0e0957be076ecf5'],
};
for (const [name, [file, expected]] of Object.entries(sourcePins)) assert(hashFile(file) === expected, `${name} source drift`);
const phase2Manifest = json(sourcePins.phase2[0]);
for (const [relative, expected] of Object.entries(phase2Manifest.files)) assert(hashFile(join(phase2, relative)) === expected, `phase2 file drift ${relative}`);

const design = json(join(dir, 'design.json'));
const oldCoverage = json(join(phase2, 'paragraph-coverage.json'));
const oldClaims = json(join(phase2, 'claim-coverage.json')).claims;
const bindings = json(join(phase2, 'claim-bindings.json'));
const oldChapters = Object.fromEntries(chapters.map((key) => [key, json(join(phase2, 'remapped-chapters', `${key}.json`))]));
const oldScenes = new Map(chapters.flatMap((key) => oldChapters[key].scenes.map((scene) => [scene.id, scene])));
const original = read(join(base, 'B18-spoken-source-cadence-candidate-20261017', 'B18.md'));
const changed = read(join(dir, 'B18.md'));
const paragraphsOf = (text) => [...text.matchAll(/^>\s*(.+)$/gmu)].map((match) => match[1]);
const oldParagraphs = paragraphsOf(original);
const paragraphs = paragraphsOf(changed);
const keys = Object.keys(oldCoverage.paragraph_coverage);
assert(keys.length === 25 && paragraphs.length === 25 && oldParagraphs.length === 25, '25 voiced paragraphs required');
const voices = Object.fromEntries(keys.map((key, i) => [key, paragraphs[i]]));
const oldVoices = Object.fromEntries(keys.map((key, i) => [key, oldParagraphs[i]]));
const oldT06 = '另一種看得見的變化在盤子上。後來有店不再每盤同價，而用盤子的顏色或裝飾區分價位；';
const newT06 = '發明協會的沿革還記下另一種變化：後來有店不再每盤同價，而用盤子的顏色或裝飾區分價位；';
for (const key of keys) assert(voices[key] === (key === 'T06' ? oldVoices[key].replace(oldT06, newT06) : oldVoices[key]), `spoken script drift beyond T06: ${key}`);
assert(oldVoices.T06.includes(oldT06) && voices.T06.includes(newT06), 'T06 source attribution missing');
const countedVoiceGlyphs = (paragraphs.join('').match(/[\p{Script=Han}0-9〇]/gu) ?? []).length;
assert(countedVoiceGlyphs === 2669 && changed.includes('2,669'), `B18 spoken-length metadata drift: ${countedVoiceGlyphs}`);

const extra = new Map(design.extra_scenes.map((row) => [row.id, row]));
assert(extra.size === 4, 'four isolated additional scenes expected');
const extraAfter = new Map();
for (const row of design.extra_scenes) {
  assert(!oldScenes.has(row.id) && row.id.startsWith(`${row.paragraph[0] === 'H' ? 'hook' : 'turn'}-`), `extra ID conflicts ${row.id}`);
  const sequence = extraAfter.get(row.after) ?? [];
  sequence.push(row);
  extraAfter.set(row.after, sequence);
}
const idsByParagraph = {};
for (const key of keys) {
  if (key === 'N03') { idsByParagraph[key] = ['now-s101', 'now-outro']; continue; }
  const ids = [];
  for (const id of oldCoverage.paragraph_coverage[key].scene_ids) {
    ids.push(id);
    for (const row of extraAfter.get(id) ?? []) {
      assert(row.paragraph === key, `extra scene ${row.id} in wrong paragraph`);
      ids.push(row.id);
      for (const nested of extraAfter.get(row.id) ?? []) {
        assert(nested.paragraph === key, `nested extra scene ${nested.id} in wrong paragraph`);
        ids.push(nested.id);
      }
    }
  }
  idsByParagraph[key] = ids;
}
assert(new Set(Object.values(idsByParagraph).flat()).size === Object.values(idsByParagraph).flat().length, 'scene ID repeats');
assert(Object.values(idsByParagraph).flat().length === 95, 'expected 95 scenes after four additions and one terminal merge');

const claimsFor = (paragraph) => oldClaims.filter((row) => bindings[row.id]?.paragraph === paragraph).map((row) => ({ id: row.id, anchor: bindings[row.id].anchor }));
const extraProtected = { I03: ['沿著吧台角落轉向'], E05: ['放上輸送帶'], T04: ['送到用餐區'] };

// A scene may hold multiple spoken lines, but an exact claim anchor stays in one scene.
// Prefer sentence boundaries and 25–42 visible glyphs without changing any spoken glyph.
function distributeVoice(paragraph, ids) {
  const source = voices[paragraph];
  const fixed = design.fixed_paragraph_scenes[paragraph];
  if (fixed) {
    assert(Object.keys(fixed).join('|') === ids.join('|'), `fixed scene IDs drift ${paragraph}`);
    assert(Object.values(fixed).join('') === source, `fixed narration drift ${paragraph}`);
    return ids.map((id) => fixed[id]);
  }
  const chars = glyphs(source);
  const length = chars.length;
  const protectedSpans = [...claimsFor(paragraph).map((row) => row.anchor), ...(extraProtected[paragraph] ?? [])].map((anchor) => {
    const start = source.indexOf(anchor);
    assert(start >= 0, `claim/loop anchor missing ${paragraph}: ${anchor}`);
    return [glyphs(source.slice(0, start)).length, glyphs(source.slice(0, start + anchor.length)).length];
  });
  const canCut = (index) => index === 0 || index === length || (!/[，。；：？！、]/u.test(chars[index]) && protectedSpans.every(([start, end]) => !(start < index && index < end)));
  const count = ids.length;
  const dp = Array.from({ length: count + 1 }, () => Array(length + 1).fill(Infinity));
  const prev = Array.from({ length: count + 1 }, () => Array(length + 1).fill(-1));
  dp[0][0] = 0;
  const target = length / count;
  for (let group = 1; group <= count; group++) {
    for (let end = group; end <= length; end++) {
      if (!canCut(end)) continue;
      for (let start = group - 1; start < end; start++) {
        if (!canCut(start) || !Number.isFinite(dp[group - 1][start])) continue;
        const size = end - start;
        const over = Math.max(0, size - 42);
        const under = Math.max(0, 20 - size);
        const boundary = end === length || /[，。；：？！、]/u.test(chars[end - 1]) ? 0 : /\s/u.test(chars[end - 1]) ? 2 : 200;
        const cost = dp[group - 1][start] + (size - target) ** 2 + over ** 2 * 30 + under ** 2 * 3 + boundary;
        if (cost < dp[group][end]) { dp[group][end] = cost; prev[group][end] = start; }
      }
    }
  }
  assert(Number.isFinite(dp[count][length]), `no fact-safe segmentation ${paragraph}`);
  const chunks = [];
  let end = length;
  for (let group = count; group > 0; group--) {
    const start = prev[group][end];
    chunks.unshift(chars.slice(start, end).join(''));
    end = start;
  }
  assert(chunks.join('') === source, `distribution changed spoken words ${paragraph}`);
  return chunks;
}

function splitLines(text, id) {
  if (id === 'hook-s005b') {
    const at = text.indexOf('盤子能跟上人潮嗎？');
    assert(at > 0, 'hook Expo split missing');
    return [text.slice(0, at), text.slice(at)];
  }
  if (id === 'now-outro') {
    const sentences = text.match(/[^。？]+[。？]/gu) ?? [];
    assert(sentences.length === 3 && sentences.join('') === text, 'outro must have answer, comment, subscribe');
    return sentences;
  }
  const lines = [];
  let rest = text;
  while (glyphs(rest).length > 40) {
    const chars = glyphs(rest);
    let cut = 40;
    for (let i = 40; i >= 22; i--) if (/[，。；：？！、]/u.test(chars[i - 1])) { cut = i; break; }
    lines.push(chars.slice(0, cut).join(''));
    rest = chars.slice(cut).join('');
  }
  if (rest) lines.push(rest);
  assert(lines.join('') === text && lines.every((line) => glyphs(line).length <= 40), `line split error ${id}`);
  return lines;
}

const all = [];
for (const key of keys) {
  const ids = idsByParagraph[key];
  const chunks = distributeVoice(key, ids);
  ids.forEach((id, position) => {
    const original = oldScenes.get(id);
    const added = extra.get(id);
    let scene;
    if (id === 'now-outro') scene = { id, template: 'outro', data: { title: '盤子終於走到客人面前', cta: '參考資料在說明欄' } };
    else {
      const converted = design.card_to_shot_prompts[id];
      const overridden = design.shot_prompt_overrides[id];
      const prompt = added?.prompt ?? converted ?? overridden ?? original?.data?.prompt;
      assert(typeof prompt === 'string' && prompt.length > 40, `missing scene-specific image ${id}`);
      const cameras = ['push in', 'pan right', 'pull out', 'pan left', 'tilt down', 'drift'];
      const camera = design.shot_camera_overrides?.[id] ?? (converted || added || overridden ? cameras[all.length % cameras.length] : original?.data?.camera ?? cameras[all.length % cameras.length]);
      scene = { id, template: 'shot', data: { prompt, camera, visual: 'still' } };
    }
    const parts = splitLines(chunks[position], id);
    scene.lines = parts.map((part, index) => ({ id: sha(`${id}\u0000${index}\u0000${part}`).slice(0, 8), text: part }));
    all.push(scene);
  });
}
assert(canon(all.flatMap((scene) => scene.lines.map((line) => line.text)).join('')) === canon(paragraphs.join('')), 'spoken order changed');
assert(all.at(-1).id === 'now-outro' && all.at(-1).template === 'outro', 'terminal card missing');
const previouslyTitle = [...oldScenes.values()].filter((scene) => scene.template === 'title').map((scene) => scene.id);
assert(previouslyTitle.length === 19 && previouslyTitle.every((id) => typeof design.card_to_shot_prompts[id] === 'string') && Object.keys(design.card_to_shot_prompts).length === 19, '19 exact card conversions required');
assert(all.filter((scene) => scene.template === 'shot').length === 94 && all.filter((scene) => scene.template === 'outro').length === 1, 'shot/outro count');

const paragraphOfScene = new Map(Object.entries(idsByParagraph).flatMap(([paragraph, ids]) => ids.map((id) => [id, paragraph])));
const claims = oldClaims.map((previous) => {
  const paragraph = bindings[previous.id].paragraph;
  const anchor = bindings[previous.id].anchor;
  const owners = idsByParagraph[paragraph].filter((id) => canon(all.find((scene) => scene.id === id).lines.map((line) => line.text).join('')).includes(canon(anchor)));
  assert(owners.length === 1, `claim ${previous.id} exact anchor crosses scenes (${paragraph})`);
  const row = { ...previous, scene: owners[0], verdict: 'UNCHECKED', note: `隔離 Phase4；${paragraph} 精確口播錨點「${anchor}」位於同一景；尚未正式查核。` };
  if (row.id === 't18') {
    row.source = 2; row.fact = null;
    row.note += '發明協會歸屬已寫入口播；正式 verifier 前仍須把 source:2/fact:null 寫入章稿並讀回。';
  }
  return row;
});
assert(claims.length === 65 && claims.every((row) => row.verdict === 'UNCHECKED'), '65 unverified claims preserved');
assert(claims.find((row) => row.id === 't18').scene === 'turn-s088', 't18 must remain in its picture scene');
const lineContaining = (paragraph, phrase) => {
  const matches = all.filter((scene) => idsByParagraph[paragraph].includes(scene.id)).flatMap((scene) => scene.lines).filter((line) => line.text.includes(phrase));
  assert(matches.length === 1, `loop phrase not in one line ${paragraph}: ${phrase}`);
  return matches[0].id;
};
const loopSpecs = [
  { setup: lineContaining('H02', '這道彎怎麼過'), payoff: lineContaining('I03', '沿著吧台角落轉向'), chapter: 'idea', what: '堵帶掉盤的轉角如何走通' },
  { setup: lineContaining('H02', '盤子能跟上人潮'), payoff: lineContaining('E05', '放上輸送帶'), chapter: 'engine', what: '萬博客流下套組如何上帶送餐' },
  { setup: lineContaining('H02', '後場送到客席'), payoff: lineContaining('T04', '送到用餐區'), chapter: 'turn', what: '後場做好的一盤如何送到客席' },
];
assert(new Set(loopSpecs.map((loop) => loop.setup)).size === 3, 'three hook setup IDs must differ');
const chapterFiles = {};
for (const key of chapters) chapterFiles[key] = {
  key, title: oldChapters[key].title,
  scenes: all.filter((scene) => scene.id.startsWith(`${key}-`)),
  claims: claims.filter((row) => paragraphOfScene.get(row.scene)?.startsWith(key === 'hook' ? 'H' : key === 'origin' ? 'O' : key === 'idea' ? 'I' : key === 'engine' ? 'E' : key === 'turn' ? 'T' : 'N')),
  loops: key === 'hook' ? loopSpecs.map(({ setup, what }) => ({ setup, what })) : loopSpecs.filter((loop) => loop.chapter === key).map(({ setup, payoff, what }) => ({ setup, payoff, what })),
  ...(key === 'hook' ? { thumbnail_shot: oldChapters.hook.thumbnail_shot } : {}),
};
assert(chapters.every((key) => chapterFiles[key].scenes.length > 0), 'empty chapter');
assert(chapters.reduce((sum, key) => sum + chapterFiles[key].claims.length, 0) === 65, 'claim/chapter assignment drift');
const row = json(sourcePins.row10b[0]);
assert(row.must_verify.length === 10 && row.sources[2].supports.includes('盤色或裝飾'), 'Row10b fact/source drift');

const sceneSizes = all.map((scene) => ({ id: scene.id, chars: glyphs(scene.lines.map((line) => line.text).join('')).length }));
const coverage = {
  schema_version: 1, status: 'ISOLATED_PHASE4_HOLD_UNREVIEWED',
  paragraph_count: keys.length, scenes: all.length, illustrated_shots: all.filter((scene) => scene.template === 'shot').length,
  title_cards: 0, outro_cards: 1, claims: claims.length, unchecked_claims: claims.length,
  loops: loopSpecs, t18: claims.find((claim) => claim.id === 't18'),
  scenes_over_42_visible_chars: sceneSizes.filter((scene) => scene.chars > 42),
  scenes_under_25_visible_chars: sceneSizes.filter((scene) => scene.chars < 25 && scene.id !== 'now-outro'),
  measured_tts_seconds: null, measured_video_seconds: null,
  source_to_scene: Object.fromEntries(keys.map((key) => [key, { scene_ids: idsByParagraph[key], source: voices[key], reconstructed: idsByParagraph[key].map((id) => all.find((scene) => scene.id === id).lines.map((line) => line.text).join('')).join('') }])),
};
for (const [paragraph, value] of Object.entries(coverage.source_to_scene)) assert(value.source === value.reconstructed, `paragraph ${paragraph} changed`);
const outputs = {
  'coverage.json': coverage,
  'claim-coverage.json': { schema_version: 1, status: 'ALL_65_UNCHECKED_HOLD', claims },
  ...Object.fromEntries(chapters.map((key) => [`remapped-chapters/${key}.json`, chapterFiles[key]])),
};
const manifest = {
  schema_version: 1, status: 'ISOLATED_PHASE4_HOLD_UNREVIEWED',
  pins: Object.fromEntries(Object.entries(sourcePins).map(([key, [, digest]]) => [key, digest])),
  inputs: Object.fromEntries(['B18.md', 'build.mjs', 'design.json', 'verify-worker.mjs', 'README.md'].map((name) => [name, hashFile(join(dir, name))])),
  outputs: Object.fromEntries(Object.entries(outputs).map(([name, value]) => [name, sha(stringify(value))])),
};
const write = process.argv.includes('--write');
const check = process.argv.includes('--check');
assert(write !== check, 'use exactly one of --write or --check');
if (write) {
  for (const [name, value] of Object.entries(outputs)) {
    const target = join(dir, name); mkdirSync(dirname(target), { recursive: true }); writeFileSync(target, stringify(value));
  }
  writeFileSync(join(dir, 'sha256.json'), stringify(manifest));
} else {
  for (const [name, value] of Object.entries(outputs)) assert(read(join(dir, name)) === stringify(value), `output drift ${name}`);
  assert(read(join(dir, 'sha256.json')) === stringify(manifest), 'manifest drift');
}
console.log(`PASS_OFFLINE_PHASE4_HOLD scenes=${all.length} shots=${coverage.illustrated_shots} claims=${claims.length} loops=${loopSpecs.length} long=${coverage.scenes_over_42_visible_chars.length}`);
