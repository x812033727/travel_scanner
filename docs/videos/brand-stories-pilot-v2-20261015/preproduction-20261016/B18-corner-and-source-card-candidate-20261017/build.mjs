#!/usr/bin/env node
// Isolated, deterministic successor to the four-pointer B18 candidate. No active inputs are written.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.resolve(here, '../B18-scene-source-pointers-candidate-20261017');
const pilot = path.resolve(here, '../..');
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
const sha = (data) => crypto.createHash('sha256').update(data).digest('hex');
const canonical = (data) => JSON.stringify(data, null, 2) + '\n';
const readParent = (name) => fs.readFileSync(path.join(parent, name));
const parentManifestSha = '88ce01e6108927a6d22a59d14196719139010bd086478dcb2a62d1c27bf5eba1';
const parentManifestBytes = readParent('sha256.json');
assert.equal(sha(parentManifestBytes), parentManifestSha, 'parent manifest drift');
const parentManifest = JSON.parse(parentManifestBytes);
for (const [name, hash] of Object.entries(parentManifest.files))
  assert.equal(sha(readParent(name)), hash, `parent file drift: ${name}`);
assert.equal(sha(readParent('README.md')), parentManifest.README_sha256, 'parent README drift');
assert.equal(sha(readParent('build.mjs')), parentManifest.build_sha256, 'parent builder drift');

const rowBeforeBytes = readParent('B18.json');
const reviewBeforeBytes = readParent('reviews/B18.json');
const seriesBeforeBytes = readParent('series-adoption.json');
assert.equal(sha(fs.readFileSync(path.join(pilot, 'episodes/B18.json'))), sha(rowBeforeBytes), 'active row drift');
assert.equal(sha(fs.readFileSync(path.join(pilot, 'episodes/reviews/B18.json'))), sha(reviewBeforeBytes), 'active review drift');
const rowBefore = JSON.parse(rowBeforeBytes);
const seriesBefore = JSON.parse(seriesBeforeBytes);
const row = structuredClone(rowBefore);
const series = structuredClone(seriesBefore);
const chaptersBefore = Object.fromEntries(keys.map((key) => [key, JSON.parse(readParent(`remapped-chapters/${key}.json`))]));
const chapters = structuredClone(chaptersBefore);
const coverageBefore = JSON.parse(readParent('claim-coverage.json'));
const coverage = structuredClone(coverageBefore);
const changes = [];
const replaceOne = (value, before, after, location) => {
  assert.equal(value.split(before).length, 2, `expected one match at ${location}`);
  changes.push({ location, before, after });
  return value.replace(before, after);
};
const ideaOld = '直線能走，轉彎卻讓壽司盤卡住。';
const ideaNew = '直線能走，轉角的輸送帶卻會壅塞，壽司盤跟著掉落。';
const factOld = '轉彎卡盤約花十年解決；';
const factNew = '轉角輸送帶壅塞、壽司盤掉落的難題約花十年解決；';
assert.equal(row.chapters[2].key, 'idea');
assert.equal(series.plan.chapters[2].key, 'idea');
for (const [label, plan] of [['row', row], ['series', series.plan]]) {
  plan.chapters[2].point = replaceOne(plan.chapters[2].point, ideaOld, ideaNew, `${label}.chapters.idea.point`);
  plan.must_verify[3].claim = replaceOne(plan.must_verify[3].claim, factOld, factNew, `${label}.must_verify[3].claim`);
}
const hook = chapters.hook;
const hookScene = hook.scenes.find((scene) => scene.id === 'hook-s004');
assert(hookScene, 'missing hook-s004');
assert.equal(hookScene.lines[0].id, '75ea529f');
hookScene.lines[0].text = replaceOne(
  hookScene.lines[0].text,
  '他把點子帶回小店，盤子卻在轉角卡住；',
  '他把點子帶回小店，輸送帶卻在轉角堵住，盤子掉下來；',
  'hook-s004.lines[75ea529f]'
);
const h5 = hook.claims.find((claim) => claim.id === 'h5');
assert(h5, 'missing h5');
h5.claim = replaceOne(h5.claim, '盤子卻在轉角卡住', '轉角的輸送帶壅塞，盤子掉落', 'hook.claims.h5.claim');
assert.deepEqual([h5.source, h5.fact, h5.verdict], [0, 3, 'UNCHECKED']);
const loop = hook.loops.find((item) => item.setup === '5ef6c449');
assert(loop, 'missing H02 loop');
loop.what = replaceOne(loop.what, '轉角卡住如何解開', '轉角堵帶掉盤的難題如何解開', 'hook.loops.H02.what');
const ideaLoop = chapters.idea.loops.find((item) => item.setup === '5ef6c449' && item.payoff === '28713224');
assert(ideaLoop, 'missing I01 payoff for H02 loop');
ideaLoop.what = replaceOne(ideaLoop.what, '轉角卡住如何解開', '轉角堵帶掉盤的難題如何解開', 'idea.loops.H02.what');
const h5Coverage = coverage.scene_claims.find((claim) => claim.id === 'h5');
assert(h5Coverage, 'missing h5 coverage');
h5Coverage.claim = replaceOne(h5Coverage.claim, '盤子卻在轉角卡住', h5.claim, 'coverage.h5.claim');
const card = chapters.engine.scenes.find((scene) => scene.id === 'engine-s041');
assert.equal(card?.template, 'title');
card.data.tag = replaceOne(card.data.tag, '機械學會／發明協會', 'J-Net21／發明協會', 'engine-s041.data.tag');
coverage.status = 'OFFLINE_PROPOSED_CORNER_AND_SOURCE_CARD_HOLD';
coverage.parent_candidate_manifest_sha256 = parentManifestSha;

// Reverse every named edit and reject all unlisted content changes.
const restoredRow = structuredClone(row);
restoredRow.chapters[2].point = restoredRow.chapters[2].point.replace(ideaNew, ideaOld);
restoredRow.must_verify[3].claim = restoredRow.must_verify[3].claim.replace(factNew, factOld);
assert.deepEqual(restoredRow, rowBefore, 'row changed beyond two named fields');
const restoredSeries = structuredClone(series);
restoredSeries.plan.chapters[2].point = restoredSeries.plan.chapters[2].point.replace(ideaNew, ideaOld);
restoredSeries.plan.must_verify[3].claim = restoredSeries.plan.must_verify[3].claim.replace(factNew, factOld);
assert.deepEqual(restoredSeries, seriesBefore, 'series changed beyond two named fields');
const restoredChapters = structuredClone(chapters);
restoredChapters.hook.scenes.find((scene) => scene.id === 'hook-s004').lines[0].text =
  chaptersBefore.hook.scenes.find((scene) => scene.id === 'hook-s004').lines[0].text;
restoredChapters.hook.claims.find((claim) => claim.id === 'h5').claim =
  chaptersBefore.hook.claims.find((claim) => claim.id === 'h5').claim;
restoredChapters.hook.loops.find((item) => item.setup === '5ef6c449').what =
  chaptersBefore.hook.loops.find((item) => item.setup === '5ef6c449').what;
restoredChapters.idea.loops.find((item) => item.setup === '5ef6c449' && item.payoff === '28713224').what =
  chaptersBefore.idea.loops.find((item) => item.setup === '5ef6c449' && item.payoff === '28713224').what;
restoredChapters.engine.scenes.find((scene) => scene.id === 'engine-s041').data.tag =
  chaptersBefore.engine.scenes.find((scene) => scene.id === 'engine-s041').data.tag;
assert.deepEqual(restoredChapters, chaptersBefore, 'chapter changed beyond named fields');
const restoredCoverage = structuredClone(coverage);
restoredCoverage.status = coverageBefore.status;
restoredCoverage.parent_candidate_manifest_sha256 = coverageBefore.parent_candidate_manifest_sha256;
restoredCoverage.scene_claims.find((claim) => claim.id === 'h5').claim =
  coverageBefore.scene_claims.find((claim) => claim.id === 'h5').claim;
assert.deepEqual(restoredCoverage, coverageBefore, 'coverage changed beyond named fields');
assert.deepEqual(series.plan.must_verify, row.must_verify, 'series and row facts differ');

let scenes = 0;
let lines = 0;
let claims = 0;
const ids = new Set();
for (const key of keys) {
  const chapter = chapters[key];
  scenes += chapter.scenes.length;
  lines += chapter.scenes.flatMap((scene) => scene.lines || []).length;
  claims += chapter.claims.length;
  for (const claim of chapter.claims) {
    assert(!ids.has(claim.id), `duplicate claim ${claim.id}`);
    ids.add(claim.id);
    assert.equal(claim.verdict, 'UNCHECKED', `verdict drift: ${claim.id}`);
    assert(claim.source >= 0 && claim.source < row.sources.length, `source range: ${claim.id}`);
    if (claim.fact !== null) assert(row.must_verify[claim.fact].sources.includes(claim.source), `fact source: ${claim.id}`);
    const mapped = coverage.scene_claims.find((item) => item.id === claim.id);
    assert(mapped, `coverage missing ${claim.id}`);
    assert.deepEqual([mapped.claim, mapped.source_index, mapped.proposed_row_fact_index],
      [claim.claim, claim.source, claim.fact], `coverage mismatch ${claim.id}`);
  }
}
assert.deepEqual([scenes, lines, claims], [85, 88, 65], 'episode shape drift');
assert.deepEqual([...ids].sort(), coverage.scene_claims.map((item) => item.id).sort());
for (const id of ['h7', 't7', 't8']) {
  const claim = keys.flatMap((key) => chapters[key].claims).find((item) => item.id === id);
  assert.deepEqual([claim.source, claim.fact], [3, 4], `court-only pointer drift: ${id}`);
}
for (const id of ['e6', 'e7']) {
  const claim = keys.flatMap((key) => chapters[key].claims).find((item) => item.id === id);
  assert.deepEqual([claim.source, claim.fact], [2, null], `registration pointer drift: ${id}`);
}

const { STORY_KEYS, storyHash, storyProblems, reviewProblems } = await import(
  pathToFileURL(path.join(root, 'tools/video/story-plans/plan.mjs')).href
);
const story = Object.fromEntries(STORY_KEYS.map((key) => [key, row[key]]));
const oldStory = Object.fromEntries(STORY_KEYS.map((key) => [key, rowBefore[key]]));
assert.equal(storyHash(oldStory), 'da692f3833f3d5448e3ec7603f0549a4f9b1afe2828c00aa8ee657618584a5e1');
assert.deepEqual(storyProblems(story, 'B18'), [], 'new row invalid');
const newStorySha = storyHash(story);
assert.notEqual(newStorySha, storyHash(oldStory), 'new story hash unchanged');
const oldReview = JSON.parse(reviewBeforeBytes);
assert.deepEqual(reviewProblems(oldReview, oldStory, 'B18'), [], 'parent row review invalid before edit');
const staleReviewProblems = reviewProblems(oldReview, story, 'B18');
assert(staleReviewProblems.length > 0, 'old review unexpectedly validates new story');

const oldScriptPath = path.join(pilot, 'scripts/B18.md');
const oldScriptReviewPath = path.join(pilot, 'scripts/reviews/B18.md');
const oldScriptBytes = fs.readFileSync(oldScriptPath);
const oldScriptReviewBytes = fs.readFileSync(oldScriptReviewPath);
assert.equal(sha(oldScriptBytes), '5326bd6633ad69931fe542badd6cddd2378324ff0bcc4b0f05652941642dc724', 'historical script drift');
assert.equal(sha(oldScriptReviewBytes), '1583b36311fde688a49f70aa546bb1c30b53ab294afeb1119bb576c73a479cdb', 'historical script review drift');
const scriptReplacements = [
  ['盤子卻在轉角卡住', '輸送帶卻在轉角堵住，盤子掉下來'],
  ['開場那個會卡住的轉角', '開場那個輸送帶壅塞、盤子掉落的轉角'],
  ['H02「轉角卡住；一九五八年第一家店要開門」', 'H02「轉角堵帶、盤子掉落；一九五八年第一家店要開門」'],
  ['卡在轉角的盤子怎麼真的走進首店？', '轉角堵帶、盤子掉落的難題怎麼解開，讓首店開門？'],
];
let partialScript = oldScriptBytes.toString('utf8');
const scriptMap = [];
for (const [before, after] of scriptReplacements) {
  const count = partialScript.split(before).length - 1;
  assert.equal(count, 1, `historical script phrase count: ${before}`);
  partialScript = partialScript.replace(before, after);
  scriptMap.push({ before, after, occurrence_count: count });
}
assert(/一九七八年|1978 年/.test(partialScript), 'historical 1978 issue missing');
const fullscriptImpact = {
  schema_version: 1, status: 'MAPPING_ONLY_OLD_FULLSCRIPT_AND_REVIEW_STALE',
  historical_script_sha256: sha(oldScriptBytes),
  historical_script_review_sha256: sha(oldScriptReviewBytes),
  narrow_phrase_swap_sha256_not_current_script: sha(partialScript),
  exact_phrase_map: scriptMap,
  stale_reasons: ['H02/I01 narrator wording differs from candidate', 'historical 1978 expiry narration conflicts with current court-bound fact 4', 'new row story hash invalidates prior row review'],
  reviewed_fullscript_for_new_candidate: false,
};

const files = new Map([
  ['B18.json', canonical(row)],
  ['series-adoption.json', canonical(series)],
  ['claim-coverage.json', canonical(coverage)],
  ['fullscript-impact.json', canonical(fullscriptImpact)],
]);
for (const key of keys) files.set(`remapped-chapters/${key}.json`,
  ['hook', 'idea', 'engine'].includes(key) ? canonical(chapters[key]) : readParent(`remapped-chapters/${key}.json`));
const sourceFiles = ['B18.json', 'series-adoption.json', 'claim-coverage.json', ...keys.map((key) => `remapped-chapters/${key}.json`)];
const fileDelta = Object.fromEntries(sourceFiles.map((name) => [name, {
  before_sha256: sha(readParent(name)), after_sha256: sha(files.get(name)),
  changed: sha(readParent(name)) !== sha(files.get(name)),
}]));
for (const name of ['remapped-chapters/origin.json', 'remapped-chapters/turn.json', 'remapped-chapters/now.json'])
  assert.equal(fileDelta[name].changed, false, `unintended file change: ${name}`);
files.set('delta.json', canonical({
  schema_version: 1, status: 'OFFLINE_CANDIDATE_HOLD', parent_candidate_manifest_sha256: parentManifestSha,
  named_changes: changes, source_files: fileDelta,
  active_row_sha256: sha(rowBeforeBytes), active_review_sha256: sha(reviewBeforeBytes),
  canonical_story_sha256_before: storyHash(oldStory), canonical_story_sha256_after: newStorySha,
  old_review_valid_for_new_story: false,
}));
files.set('verification.json', canonical({
  schema_version: 1, status: 'PASS_OFFLINE_STRUCTURE_ONLY_HOLD',
  scenes, narration_lines: lines, scene_claims: claims, all_scene_claims_unchecked: true,
  preserved_parent_source_pointer_changes: ['e1', 'h5', 'i1', 'i5'],
  canonical_story_sha256: newStorySha, stale_row_review_problems: staleReviewProblems,
  historical_fullscript_and_review_stale: true,
  formal_worker_verifier_complete: false, independent_new_review_complete: false,
  paid_calls: 0, rendered_video: false, import_approved: false,
}));

for (const [name, content] of files) {
  const target = path.join(here, name);
  if (mode === '--write') { fs.mkdirSync(path.dirname(target), { recursive: true }); fs.writeFileSync(target, content); }
  else assert.equal(fs.readFileSync(target, 'utf8'), content.toString(), `output drift: ${name}`);
}
const manifest = {
  schema_version: 1, parent_candidate_manifest_sha256: parentManifestSha,
  files: Object.fromEntries([...files].map(([name, content]) => [name, sha(content)])),
  README_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  build_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))),
};
const manifestPath = path.join(here, 'sha256.json');
if (mode === '--write') fs.writeFileSync(manifestPath, canonical(manifest));
else assert.equal(fs.readFileSync(manifestPath, 'utf8'), canonical(manifest), 'manifest drift');
console.log(JSON.stringify({ status: 'PASS_OFFLINE_CANDIDATE_HOLD', mode, story_sha256: newStorySha,
  scenes, lines, claims, changed_files: Object.values(fileDelta).filter((item) => item.changed).length }));
