import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Offline corrective successor. Parent rows and production state stay immutable.
const here = path.dirname(fileURLToPath(import.meta.url));
const base = path.resolve(here, '../B18-one-thread-narrative-candidate-20261017');
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const baseManifestSha = '039131fdaba3107668062722af6e126b06aa6acc9d46a5b8481a9402e287997a';
const sha = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (file) => fs.readFileSync(file, 'utf8');
assert.equal(sha(fs.readFileSync(path.join(base, 'sha256.json'))), baseManifestSha, 'parent manifest drift');
for (const [name, expected] of Object.entries(JSON.parse(read(path.join(base, 'sha256.json'))).files)) {
  assert.equal(sha(fs.readFileSync(path.join(base, name))), expected, `parent file drift: ${name}`);
}

const previousSeries = JSON.parse(read(path.join(base, 'series.json')));
const series = structuredClone(previousSeries);
const previous = Object.fromEntries(keys.map((key) => [key, JSON.parse(read(path.join(base, 'chapters', `${key}.json`)))]));
const chapters = structuredClone(previous);
const scene = (key, id) => { const value = chapters[key].scenes.find((row) => row.id === id); assert(value, `missing scene ${id}`); return value; };
const claim = (key, id) => { const value = chapters[key].claims.find((row) => row.id === id); assert(value, `missing claim ${id}`); return value; };

// The manufacturer says a bypass device was sold for large stores. It names no purchaser.
const turn081 = scene('turn', 'turn-s081');
assert.deepEqual(turn081.lines.map((line) => line.id), ['d8ecd870']);
turn081.lines[0].text = '其他新店出現後，盤子要怎麼走，也有人重新設計。';
Object.assign(claim('turn', 't10'), {
  claim: '新業者另行設計送盤路線', scene: 'turn-s081', source: 2, fact: 12,
  note: '發明協會後場直線輸送路線；不以萬博、加盟或單一權利期滿解釋其直接原因。',
});
const turn086 = scene('turn', 'turn-s086');
assert.deepEqual(turn086.lines.map((line) => line.id), ['ed0c5c6c']);
turn086.lines[0].text = '石野集團年表記下，一九八〇年開始販售供大型店使用的旁通裝置。';
Object.assign(claim('turn', 't12'), {
  claim: '一九八〇年開始販售供大型店使用的旁通裝置', scene: 'turn-s086', source: 4, fact: 10,
  note: '石野官方年表的「大型店対応」是裝置用途，未指某家店已購得。',
});
Object.assign(claim('turn', 't18'), {
  claim: '元祿壽司自己的店後來仍有一台舊輸送機在使用', scene: 'turn-s092', source: 1, fact: 8,
  note: '本句只作懸念；2021、1985與堺東店留待第95景揭曉，不暗示無間斷或現今仍在用。',
});
series.plan.must_verify[10].claim = '石野集團官方年表記1980年開始販售供大型店使用的旁通裝置，1986年已有ㄇ字型輸送帶的店；不得說旁通已售給某家指定大型店、兩者是同一家店的一次改造，或旁通直接導致ㄇ字型店。';
series.plan.sources[2].checked = '2026-10-17';

// Answer the previous chapter's year question immediately; then identify No.112's two objects.
const now093 = scene('now', 'now-s093');
assert.deepEqual(now093.lines.map((line) => line.id), ['233e1a3a']);
now093.lines[0].text = '它製於一九八五年，不是白石開第一家店時的原機。';
const now095 = scene('now', 'now-s095');
assert.deepEqual(now095.lines.map((line) => line.id), ['bb7022f4', '8b88e002']);
now095.lines[0].text = '二〇二一年，這台輸送機仍在元祿壽司堺東店使用。';
now095.lines[1].text = '日本機械學會把這台輸送機列入第一百一十二號機械遺產。';
const now096 = scene('now', 'now-s096');
assert.deepEqual(now096.lines.map((line) => line.id), ['1585ea8b']);
now096.lines[0].text = '元祿產業另外保存的早期「魚鱗板」板片，也列在同一號機械遺產裡。';
Object.assign(claim('now', 'n2'), { claim: '該輸送機製於一九八五年，不是白石開第一家店時的原機', scene: 'now-s093', source: 1, fact: 8 });
Object.assign(claim('now', 'n3'), { claim: '二〇二一年這台輸送機仍在元祿壽司堺東店使用', scene: 'now-s095', source: 1, fact: 8 });
Object.assign(claim('now', 'n4'), { claim: '日本機械學會把這台輸送機列入第一百一十二號機械遺產', scene: 'now-s095', source: 1, fact: 8 });
Object.assign(claim('now', 'n5'), { claim: '元祿產業另外保存的早期魚鱗板板片也列在第112號內', scene: 'now-s096', source: 1, fact: 8 });
const removedSceneId = 'now-s097';
assert.equal(scene('now', removedSceneId).template, 'shot');
chapters.now.scenes = chapters.now.scenes.filter((row) => row.id !== removedSceneId);
const removedClaimIds = ['n6', 'n8'];
chapters.now.claims = chapters.now.claims.filter((row) => !removedClaimIds.includes(row.id));
assert.equal(chapters.now.claims.find((row) => row.id === 'n7')?.scene, 'now-s098');

// Check exact untouched scope and metadata bindings before composing.
for (const key of ['hook', 'origin', 'idea', 'engine']) assert.deepEqual(chapters[key], previous[key], `early chapter changed: ${key}`);
const allScenes = keys.flatMap((key) => chapters[key].scenes);
const sceneIds = new Set(allScenes.map((row) => row.id));
assert.equal(sceneIds.size, allScenes.length, 'duplicate scene');
const allClaims = keys.flatMap((key) => chapters[key].claims);
assert.equal(new Set(allClaims.map((row) => row.id)).size, allClaims.length, 'duplicate claim');
for (const row of allClaims) {
  assert(sceneIds.has(row.scene), `claim scene missing: ${row.id}`);
  assert(series.plan.sources[row.source], `claim source missing: ${row.id}`);
  if (row.fact !== null && row.fact !== undefined) assert(series.plan.must_verify[row.fact]?.sources.includes(row.source), `fact/source mismatch: ${row.id}`);
  assert.equal(row.verdict, 'UNCHECKED', `unreviewed claim promoted: ${row.id}`);
}
const allLines = allScenes.flatMap((row) => row.lines);
const lineIds = new Set(allLines.map((row) => row.id));
assert.equal(lineIds.size, allLines.length, 'duplicate line');
for (const loop of keys.flatMap((key) => chapters[key].loops)) {
  assert(lineIds.has(loop.setup), `loop setup missing: ${loop.setup}`);
  if (loop.payoff) assert(lineIds.has(loop.payoff), `loop payoff missing: ${loop.payoff}`);
}
const yearLoop = chapters.turn.loops.find((loop) => loop.setup === 'f996e543');
assert.equal(yearLoop?.payoff, '8b88e002', 'old year loop drift');
yearLoop.payoff = '233e1a3a';
yearLoop.what = '元祿店後來在用的舊輸送機是哪一年製';
assert(now093.lines[0].text.includes('一九八五年') && now093.lines[0].text.includes('不是'), 'chapter start must answer both year and original-machine question');
const lateText = [...chapters.turn.scenes, ...chapters.now.scenes].flatMap((row) => row.lines.map((line) => line.text)).join('\n');
assert(!/(?:1974|一九七四|給茶|採購|盤價|廣辭苑|市場規模)/u.test(lateText), 'retired branch returned');
assert(![...chapters.turn.scenes, ...chapters.now.scenes].some((row) => /1974/u.test(row.data?.title ?? '')), 'tea year card returned');

const { composeStory, cuteStoryVisualProblems } = await import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs')).href);
const { loadProject, lintProject } = await import(pathToFileURL(path.join(root, 'tools/video/core/state.mjs')).href);
const { estimateTimeline } = await import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs')).href);
const slug = 'story-conveyor-belt-sushi-v2';
const authored = path.resolve(base, '../B18-authored-chapters-candidate');
const voice = JSON.parse(read(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'video.json'))).voice;
const beforeDoc = composeStory({ slug, info: previousSeries, chapters: previous, voice, drama: { music_enabled: false }, root });
const doc = composeStory({ slug, info: series, chapters, voice, drama: { music_enabled: false }, root });
assert.deepEqual(doc.look, { preset: 'cute-mystery' });
assert.equal(doc.subtitles.burn_in, false);
assert.equal(doc.scenes.length, 85);
assert.equal(doc.scenes.flatMap((row) => row.lines).length, 88);
const cuteErrors = cuteStoryVisualProblems(doc);
assert.deepEqual(cuteErrors, []);
assert.deepEqual(doc.scenes.flatMap((row) => row.lines).filter((row) => /^[\p{P}\p{S}\s]+$/u.test(row.text)), []);
assert.equal(allClaims.length, 65);
let externalCalls = 0;
globalThis.fetch = () => { externalCalls++; throw new Error('offline candidate must not fetch'); };
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'b18-precision-'));
assert(/^b18-precision-[^\\/]+$/.test(path.relative(path.resolve(os.tmpdir()), path.resolve(tmp))), 'unsafe temporary cleanup path');
let lint;
try {
  const shelf = path.join(tmp, 'docs', 'videos');
  const dir = path.join(shelf, slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'video.json'), canonical(doc));
  fs.writeFileSync(path.join(dir, 'series.json'), canonical(series));
  fs.copyFileSync(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'brief.md'), path.join(dir, 'brief.md'));
  fs.copyFileSync(path.join(authored, 'fixtures/lexicon.json'), path.join(shelf, 'lexicon.json'));
  lint = lintProject(loadProject({ slug, root: tmp }));
} finally { fs.rmSync(tmp, { recursive: true, force: true }); }
assert.deepEqual(lint.errors, []);
assert.equal(externalCalls, 0);
const beforeSeconds = estimateTimeline(beforeDoc).total_frames / 30;
const bodySeconds = estimateTimeline(doc).total_frames / 30;
assert(bodySeconds >= 540 && bodySeconds <= 600, 'static body escaped near-ten-minute plan');

const beforeScenes = new Map(keys.flatMap((key) => previous[key].scenes.map((row) => [row.id, row])));
const afterScenes = new Map(allScenes.map((row) => [row.id, row]));
const beforeClaims = new Map(keys.flatMap((key) => previous[key].claims.map((row) => [row.id, row])));
const afterClaims = new Map(allClaims.map((row) => [row.id, row]));
const changedSceneIds = ['turn-s081', 'turn-s086', 'now-s093', 'now-s095', 'now-s096', removedSceneId];
const changedClaimIds = ['t10', 't12', 't18', 'n2', 'n3', 'n4', 'n5', ...removedClaimIds];
const delta = {
  schema_version: 1, status: 'OFFLINE_PRECISION_CORRECTION_ONLY', base_manifest_sha256: baseManifestSha,
  scene_rows: changedSceneIds.map((id) => ({ id, before: beforeScenes.get(id), after: afterScenes.get(id) ?? null })),
  claim_rows: changedClaimIds.map((id) => ({ id, before: beforeClaims.get(id), after: afterClaims.get(id) ?? null })),
  series_rows: {
    source_2: { before: previousSeries.plan.sources[2], after: series.plan.sources[2] },
    fact_10: { before: previousSeries.plan.must_verify[10], after: series.plan.must_verify[10] },
  },
  loop_rows: {
    before: previous.turn.loops.find((row) => row.setup === 'f996e543'),
    after: chapters.turn.loops.find((row) => row.setup === 'f996e543'),
  },
  unchanged_chapters: ['hook', 'origin', 'idea', 'engine'],
  removed_scene_ids: [removedSceneId], removed_claim_ids: removedClaimIds,
  claim_count_before: keys.flatMap((key) => previous[key].claims).length, claim_count_after: allClaims.length,
  estimated_body_seconds_before: beforeSeconds, estimated_body_seconds_after: bodySeconds,
  actual_tts_seconds: null, external_calls: externalCalls,
};
const verification = {
  schema_version: 1, status: 'VERIFIED_OFFLINE_PRECISION_STRUCTURE_ONLY_FULL_STORY_HOLD',
  scenes: doc.scenes.length, lines: doc.scenes.flatMap((row) => row.lines).length,
  illustrations: doc.scenes.filter((row) => row.template === 'shot').length,
  cards: doc.scenes.filter((row) => row.template !== 'shot').length,
  claims_unchecked: allClaims.length, estimated_body_seconds: bodySeconds, measured_body_seconds: null,
  lint_errors: lint.errors, lint_warnings: lint.warnings.length,
  lint_warning_kinds: [...new Set(lint.warnings.map((warning) => warning.message.split(':', 1)[0]))],
  cute_errors: cuteErrors, external_calls: externalCalls,
  worker_pass: false, full_story_pass: false, full_source_pass: false, tts_generated: false,
};
const output = new Map([
  ['series.json', canonical(series)],
  ['reuse-intent.json', read(path.join(base, 'reuse-intent.json'))],
  ['delta.json', canonical(delta)], ['verification.json', canonical(verification)],
]);
for (const key of keys) output.set(`chapters/${key}.json`, ['turn', 'now'].includes(key) ? canonical(chapters[key]) : read(path.join(base, 'chapters', `${key}.json`)));
const hashes = Object.fromEntries([
  ['build.mjs', sha(fs.readFileSync(path.join(here, 'build.mjs')))],
  ['README.md', sha(fs.readFileSync(path.join(here, 'README.md')))],
  ...[...output].map(([name, content]) => [name, sha(content)]),
]);
output.set('sha256.json', canonical({ schema_version: 1, base_manifest_sha256: baseManifestSha, files: hashes }));
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
for (const [name, content] of output) {
  const file = path.join(here, name);
  if (mode === '--write') { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, content); }
  else assert.equal(read(file), content, `generated output drift: ${name}`);
}
console.log(JSON.stringify(verification, null, 2));
