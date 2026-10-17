#!/usr/bin/env node
// An offline, deterministic child of the reviewed B18 corner/source-card candidate.
// This tool only writes within its own directory; it never adopts active data.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.resolve(here, '../B18-corner-and-source-card-candidate-20261017');
const pilot = path.resolve(here, '../..');
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
const sha = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => JSON.stringify(value, null, 2) + '\n';
const readParent = (name) => fs.readFileSync(path.join(parent, name));
const readActive = (name) => fs.readFileSync(path.join(pilot, name));

const parentManifestSha = '03bcf39dbbbeb7c1159154effbe99f645088cc3a6a449b3d0349e62ab6543a9a';
const parentReviewSha = '2d30144e7d2be77d12dbc9ec24b945b1fa75af7a02e8cc19aa4ccd3da97072c5';
const manifestBytes = readParent('sha256.json');
assert.equal(sha(manifestBytes), parentManifestSha, 'parent manifest drift');
const parentManifest = JSON.parse(manifestBytes);
for (const [name, expected] of Object.entries(parentManifest.files))
  assert.equal(sha(readParent(name)), expected, `parent output drift: ${name}`);
assert.equal(sha(readParent('README.md')), parentManifest.README_sha256, 'parent README drift');
assert.equal(sha(readParent('build.mjs')), parentManifest.build_sha256, 'parent builder drift');
assert.equal(sha(readParent('INDEPENDENT-ROW-SOURCE-REVIEW.md')), parentReviewSha, 'parent review drift');
assert.equal(sha(readActive('episodes/B18.json')), '21122b7db5f97957ca89399b249a02e47e0b4465003e3653efbbf422b6043e9d', 'active row drift');
assert.equal(sha(readActive('episodes/reviews/B18.json')), '06012b65e0e3a9b911dda1432c9de61f73f01f28a91fb5b23a7fad0354e794ed', 'active review drift');

const rowBefore = JSON.parse(readParent('B18.json'));
const seriesBefore = JSON.parse(readParent('series-adoption.json'));
const coverageBefore = JSON.parse(readParent('claim-coverage.json'));
const chaptersBefore = Object.fromEntries(keys.map((key) => [key, JSON.parse(readParent(`remapped-chapters/${key}.json`))]));
const row = structuredClone(rowBefore);
const series = structuredClone(seriesBefore);
const coverage = structuredClone(coverageBefore);
const chapters = structuredClone(chaptersBefore);

const factBefore = '轉角輸送帶壅塞、壽司盤掉落的難題約花十年解決；J-Net21記撲克牌扇形，發明協會記名片扇形，兩者是不同來源說法；最後採扇形板片，1957年試作機完成。';
const factAfter = '據J-Net21，轉角輸送帶壅塞、壽司盤掉落的難題約花十年解決，最後採扇形板片、1957年試作機完成；扇形靈感有兩種來源說法：J-Net21記撲克牌，發明協會記名片，不可合成單一現場。';
assert.equal(row.must_verify[3].claim, factBefore, 'parent row fact drift');
assert.equal(series.plan.must_verify[3].claim, factBefore, 'parent series fact drift');
assert.deepEqual(row.must_verify[3].sources, [0, 2], 'fact sources drift');
assert.equal(row.must_verify[3].attributed, true, 'attributed gate drift');
row.must_verify[3].claim = factAfter;
series.plan.must_verify[3].claim = factAfter;

const lineEdits = [
  {
    chapter: 'hook', scene: 'hook-s004', claim: 'h5', line: '75ea529f', source: 0,
    before: '他把點子帶回小店，輸送帶卻在轉角堵住，盤子掉下來；一九五八年第一家店要開門，',
    after: 'J-Net21 記下，試作輸送帶到了轉角就堵住，盤子掉下來；一九五八年第一家店要開門，',
  },
  {
    chapter: 'idea', scene: 'idea-s024', claim: 'i1', line: '9538ed4b', source: 0,
    before: '一到轉角，帶子擠在一起，盤子就可能掉下來。客人還沒伸手，',
    after: 'J-Net21 記載，輸送帶一到轉角就壅塞，盤子跟著掉下來。客人還沒伸手，',
  },
  {
    chapter: 'idea', scene: 'idea-s031', claim: 'i5', line: '28713224', source: 0,
    before: '最後用來轉彎的，是一片片扇形的板子。它們排在一起，讓輸送帶繞過吧台角落；',
    after: '依 J-Net21 的記載，最後用來轉彎的是一片片扇形板。它們排在一起，讓輸送帶繞過吧台角落；',
  },
  {
    chapter: 'idea', scene: 'idea-s032', claim: 'i6', line: '3f5899d2', source: 0,
    before: '這種板子後來被叫作「魚鱗板」。原本會把盤子擠掉的地方，終於有了能走的路。',
    after: 'J-Net21 說，這種板子後來叫「魚鱗板」。原本會把盤子擠掉的地方，終於有了能走的路。',
  },
  {
    chapter: 'idea', scene: 'idea-s033', claim: 'i7', line: '464491bc', source: 0,
    before: '從工廠參觀到試作機完成，前後約十年。',
    after: 'J-Net21 記載，從工廠參觀到試作機完成，前後約十年。',
  },
  {
    chapter: 'now', scene: 'now-s098', claim: 'n7', line: '99e3065a', source: 0,
    before: '早期的扇形板片，回答了當年那個彎怎麼過。',
    after: '按 J-Net21 的記載，早期的扇形板片，回答了當年那個彎怎麼過。',
  },
];

for (const edit of lineEdits) {
  const scene = chapters[edit.chapter].scenes.find((item) => item.id === edit.scene);
  const line = scene?.lines?.find((item) => item.id === edit.line);
  const claim = chapters[edit.chapter].claims.find((item) => item.id === edit.claim);
  assert.equal(line?.text, edit.before, `parent narration drift: ${edit.claim}`);
  assert.deepEqual([claim?.scene, claim?.source, claim?.fact, claim?.verdict],
    [edit.scene, edit.source, 3, 'UNCHECKED'], `claim route drift: ${edit.claim}`);
  assert.match(edit.after, /J-Net21/, `missing audible attribution: ${edit.claim}`);
  line.text = edit.after;
}
// The two mutually exclusive inspiration accounts were already attributed aloud.
assert.match(chapters.idea.scenes.find((scene) => scene.id === 'idea-s027').lines[0].text, /日本中小企業基盤整備機構/);
assert.match(chapters.idea.scenes.find((scene) => scene.id === 'idea-s029').lines[0].text, /發明協會/);
for (const [name, plan] of [['row', row], ['series', series.plan]]) {
  assert.deepEqual(plan.must_verify[3].sources, [0, 2], `${name} source list drift`);
  assert.equal(plan.must_verify[3].attributed, true, `${name} attribution flag drift`);
}
assert.deepEqual(series.plan.must_verify, row.must_verify, 'series and row facts differ');

coverage.status = 'OFFLINE_PROPOSED_ATTRIBUTED_NARRATION_HOLD';
coverage.parent_candidate_manifest_sha256 = parentManifestSha;
assert.deepEqual(coverage.scene_claims, coverageBefore.scene_claims, 'coverage mapping changed');

// Allow only the declared row fact and six narration lines to differ from the parent.
const restoredRow = structuredClone(row);
restoredRow.must_verify[3].claim = factBefore;
assert.deepEqual(restoredRow, rowBefore, 'row changed beyond fact 3');
const restoredSeries = structuredClone(series);
restoredSeries.plan.must_verify[3].claim = factBefore;
assert.deepEqual(restoredSeries, seriesBefore, 'series changed beyond fact 3');
const restoredChapters = structuredClone(chapters);
for (const edit of lineEdits)
  restoredChapters[edit.chapter].scenes.find((scene) => scene.id === edit.scene)
    .lines.find((line) => line.id === edit.line).text = edit.before;
assert.deepEqual(restoredChapters, chaptersBefore, 'chapters changed beyond six named lines');
const restoredCoverage = structuredClone(coverage);
restoredCoverage.status = coverageBefore.status;
restoredCoverage.parent_candidate_manifest_sha256 = coverageBefore.parent_candidate_manifest_sha256;
assert.deepEqual(restoredCoverage, coverageBefore, 'coverage changed beyond child metadata');

let scenes = 0;
let lines = 0;
let claims = 0;
const claimIds = new Set();
for (const key of keys) {
  const chapter = chapters[key];
  scenes += chapter.scenes.length;
  lines += chapter.scenes.flatMap((scene) => scene.lines || []).length;
  claims += chapter.claims.length;
  const priorClaims = chaptersBefore[key].claims;
  assert.deepEqual(chapter.claims, priorClaims, `chapter claim/source route changed: ${key}`);
  for (const claim of chapter.claims) {
    assert(!claimIds.has(claim.id), `duplicate claim: ${claim.id}`);
    claimIds.add(claim.id);
    assert.equal(claim.verdict, 'UNCHECKED', `verdict drift: ${claim.id}`);
    assert(claim.source >= 0 && claim.source < row.sources.length, `source out of range: ${claim.id}`);
    if (claim.fact !== null)
      assert(row.must_verify[claim.fact].sources.includes(claim.source), `fact source mismatch: ${claim.id}`);
    const mapped = coverage.scene_claims.find((item) => item.id === claim.id);
    assert.deepEqual([mapped?.claim, mapped?.source_index, mapped?.proposed_row_fact_index],
      [claim.claim, claim.source, claim.fact], `coverage mismatch: ${claim.id}`);
  }
}
assert.deepEqual([scenes, lines, claims], [85, 88, 65], 'episode shape drift');
assert.deepEqual([...claimIds].sort(), coverage.scene_claims.map((item) => item.id).sort());
assert.deepEqual(row.must_verify[4].sources, [3], 'court source route drift');
for (const id of ['h7', 't7', 't8']) {
  const claim = keys.flatMap((key) => chapters[key].claims).find((item) => item.id === id);
  assert.deepEqual([claim?.source, claim?.fact], [3, 4], `court-only route drift: ${id}`);
}
for (const id of ['e6', 'e7']) {
  const claim = keys.flatMap((key) => chapters[key].claims).find((item) => item.id === id);
  assert.deepEqual([claim?.source, claim?.fact], [2, null], `registration route drift: ${id}`);
}

const { STORY_KEYS, storyHash, storyProblems, reviewProblems } = await import(
  pathToFileURL(path.join(root, 'tools/video/story-plans/plan.mjs')).href
);
const storyFrom = (plan) => Object.fromEntries(STORY_KEYS.map((key) => [key, plan[key]]));
const oldStory = storyFrom(rowBefore);
const newStory = storyFrom(row);
const oldStorySha = storyHash(oldStory);
const newStorySha = storyHash(newStory);
assert.equal(oldStorySha, '4585c9e5a2826cc1d1a4b2436958b17edad9c405dd81e195026d221deef80280', 'parent story hash drift');
assert.deepEqual(storyProblems(newStory, 'B18'), [], 'new row invalid');
// The series plan intentionally differs from the episode row in title/logline.
// Its fact list must track the row, while the parent-vs-child projection delta stays narrow.
assert.notEqual(storyHash(storyFrom(series.plan)), storyHash(storyFrom(seriesBefore.plan)),
  'series projection fact revision missing');
assert.notEqual(newStorySha, oldStorySha, 'new story hash unchanged');
const oldReview = JSON.parse(readActive('episodes/reviews/B18.json'));
assert.deepEqual(oldReview.reviewer_only, [4], 'historical court reviewer-only routing drift');
const staleProblems = reviewProblems(oldReview, newStory, 'B18');
assert(staleProblems.length > 0, 'old row review unexpectedly validates new story');

const files = new Map([
  ['B18.json', canonical(row)],
  ['series-adoption.json', canonical(series)],
  ['claim-coverage.json', canonical(coverage)],
  ['attribution-map.json', canonical({
    schema_version: 1, status: 'OFFLINE_PROPOSED_HOLD', parent_candidate_manifest_sha256: parentManifestSha,
    row_fact_3: { before: factBefore, after: factAfter },
    changed_narration: lineEdits,
    retained_adjacent_attribution: { i3: 'idea-s027 says 日本中小企業基盤整備機構', i4: 'idea-s029 says 發明協會' },
  })],
  ['fullscript-impact.json', canonical({
    schema_version: 1, status: 'FULLSCRIPT_MUST_BE_REBUILT_AND_REVIEWED_HOLD',
    parent_fullscript_impact_sha256: sha(readParent('fullscript-impact.json')),
    parent_canonical_story_sha256: oldStorySha, candidate_canonical_story_sha256: newStorySha,
    line_ids_requiring_alignment: lineEdits.map((item) => item.line),
    historical_script_review_reusable: false, current_fullscript_review_complete: false,
  })],
]);
for (const key of keys) {
  const name = `remapped-chapters/${key}.json`;
  files.set(name, ['hook', 'idea', 'now'].includes(key) ? canonical(chapters[key]) : readParent(name));
}
const sourceFiles = ['B18.json', 'series-adoption.json', 'claim-coverage.json',
  ...keys.map((key) => `remapped-chapters/${key}.json`)];
const fileDelta = Object.fromEntries(sourceFiles.map((name) => [name, {
  before_sha256: sha(readParent(name)), after_sha256: sha(files.get(name)),
  changed: sha(readParent(name)) !== sha(files.get(name)),
}]));
for (const name of ['remapped-chapters/origin.json', 'remapped-chapters/engine.json', 'remapped-chapters/turn.json'])
  assert.equal(fileDelta[name].changed, false, `unintended chapter change: ${name}`);
files.set('delta.json', canonical({
  schema_version: 1, status: 'OFFLINE_CANDIDATE_HOLD', parent_candidate_manifest_sha256: parentManifestSha,
  row_fact_3_only: true, changed_line_ids: lineEdits.map((item) => item.line),
  source_files: fileDelta, old_story_sha256: oldStorySha, new_story_sha256: newStorySha,
  old_row_review_valid_for_new_story: false,
}));
files.set('verification.json', canonical({
  schema_version: 1, status: 'PASS_OFFLINE_STRUCTURE_ONLY_HOLD',
  scenes, narration_lines: lines, scene_claims: claims, all_scene_claims_unchecked: true,
  all_claim_source_and_fact_routes_unchanged: true, court_reviewer_only_required_in_new_review: true,
  canonical_story_sha256: newStorySha, stale_row_review_problems: staleProblems,
  formal_worker_verifier_complete: false, independent_new_review_complete: false,
  paid_calls: 0, rendered_video: false, import_approved: false,
}));

for (const [name, content] of files) {
  const target = path.join(here, name);
  if (mode === '--write') {
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, content);
  } else {
    assert.equal(fs.readFileSync(target, 'utf8'), content.toString(), `output drift: ${name}`);
  }
}
const manifest = {
  schema_version: 1, parent_candidate_manifest_sha256: parentManifestSha,
  parent_independent_review_sha256: parentReviewSha,
  files: Object.fromEntries([...files].map(([name, content]) => [name, sha(content)])),
  README_sha256: sha(fs.readFileSync(path.join(here, 'README.md'))),
  build_sha256: sha(fs.readFileSync(fileURLToPath(import.meta.url))),
};
const manifestPath = path.join(here, 'sha256.json');
if (mode === '--write') fs.writeFileSync(manifestPath, canonical(manifest));
else assert.equal(fs.readFileSync(manifestPath, 'utf8'), canonical(manifest), 'manifest drift');
console.log(JSON.stringify({ status: 'PASS_OFFLINE_CANDIDATE_HOLD', mode,
  story_sha256: newStorySha, scenes, lines, claims,
  changed_files: Object.values(fileDelta).filter((item) => item.changed).length }));
