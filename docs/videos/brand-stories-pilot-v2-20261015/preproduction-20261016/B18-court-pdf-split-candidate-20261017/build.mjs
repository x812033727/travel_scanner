#!/usr/bin/env node
// Exact, offline-only court-PDF/source-granularity successor for the B18 candidate.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const parent = path.resolve(here, '../B18-worker-input-name-trim-candidate-20261017');
const pilot = path.resolve(here, '../..');
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const parentManifestSha = 'da3820bd403c4a9fb33d2b904cbf3f2b112579a060ee9ab6709c3ab07d7137c3';
const sha = (data) => crypto.createHash('sha256').update(data).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (file) => fs.readFileSync(path.join(parent, file));

assert.equal(sha(read('sha256.json')), parentManifestSha, 'parent manifest changed');
for (const [file, hash] of Object.entries(JSON.parse(read('sha256.json')).files)) {
  assert.equal(sha(read(file)), hash, `parent file changed: ${file}`);
}

const oldRow = JSON.parse(read('B18.json'));
const oldSeries = JSON.parse(read('series-adoption.json'));
const oldCoverage = JSON.parse(read('claim-coverage.json'));
const oldChapters = Object.fromEntries(keys.map((key) => [key, JSON.parse(read(`remapped-chapters/${key}.json`))]));
assert.equal(oldRow.must_verify.length, 10);
assert.equal(oldCoverage.scene_claims.length, 65);
assert.deepEqual(oldSeries.plan.must_verify, oldRow.must_verify);
assert.deepEqual(oldRow.must_verify[4].sources, [0, 2, 3]);
assert.deepEqual(oldRow.must_verify[5].sources, [0, 3]);

// Ten facts is the schema maximum. Fact 4 is court-only; fact 5 is the readable
// J-Net21 account of warnings and affiliate independence. The disputed 1978
// versions stay in source supports/caveats, explicitly outside narration.
const courtFact = {
  claim: '法院判決理由認定「コンベヤ附調理食台」實用新案第579776號於1962年登錄，1972年因存續期間屆滿而消滅；判決並認定此後已有許多與原告無關的企業經營輸送帶壽司店。這只涉及該特定權利，不能推定所有權利同時到期，或其他店只因期滿才出現。',
  sources: [3],
  core: true,
};
const readableFact = {
  claim: 'J-Net21報導元祿在東京和大阪聘請律師與專利代理人，對相似店發出警告；也記載部分加盟店後來獨立並換上新招牌。這是該報導的經營情節，不能推成所有壽司店均被禁止，或所有加盟店同時獨立。',
  sources: [0],
  attributed: true,
};
const row = structuredClone(oldRow);
row.must_verify[4] = courtFact;
row.must_verify[5] = readableFact;
const oldTurnPoint = oldRow.chapters.find((chapter) => chapter.key === 'turn').point;
const courtOverreach = '此後已有元祿以外的經營者';
const courtBound = '此後已有與本案原告無關的多家公司經營輸送帶壽司店';
assert(oldTurnPoint.includes(courtOverreach), 'parent turn point moved');
assert.equal(oldTurnPoint.split(courtOverreach).length, 2, 'court overreach appears more than once');
row.chapters.find((chapter) => chapter.key === 'turn').point = oldTurnPoint.replace(courtOverreach, courtBound);
const oldPdfSupports = oldRow.sources[3].supports;
const oldOtherRight = '被告答辯 P5 L306–315 所述另一權利851953的期滿日並非法院獨立認定。';
const newOtherRight = '被告答辯 P5 L306–315 提及另一第851953號權利，並未提供它的期滿年；該段也不是法院的獨立認定。';
assert(oldPdfSupports.includes(oldOtherRight), 'parent court source summary moved');
row.sources[3].supports = oldPdfSupports.replace(oldOtherRight, newOtherRight);
const oldCaveats = oldRow.caveats;
const caveatMarker = '不能寫成原案到期日或唯一入場開關。';
assert(oldCaveats.includes(caveatMarker), 'parent 1978 caveat moved');
row.caveats = oldCaveats.replace(caveatMarker,
  `${caveatMarker}本片不口播1978年，只保留為來源分歧註記。`);
const series = structuredClone(oldSeries);
series.plan.must_verify = structuredClone(row.must_verify);
series.plan.chapters = structuredClone(row.chapters);
series.plan.sources = structuredClone(row.sources);
series.plan.caveats = row.caveats;

const chapters = structuredClone(oldChapters);
const chapterClaims = Object.fromEntries(keys.flatMap((key) => chapters[key].claims.map((claim) => [claim.id, { key, claim }])));
const oldS077Prompt = oldChapters.turn.scenes.find((scene) => scene.id === 'turn-s077').data.prompt;
const newS077Prompt = 'Medium shot at a separate 1962-era Japanese records desk, one clerk closing a plain utility-model registration binder beside a simplified counter diagram, the binder\'s worn blank tab nearest the viewer, quiet desk-lamp light.';
const oldS079Prompt = oldChapters.turn.scenes.find((scene) => scene.id === 'turn-s079').data.prompt;
const newS079Prompt = 'Wide shot of a Japanese commercial street at an unspecified later time after 1972, one pedestrian walking toward an unsigned conveyor sushi restaurant while a different modest counter frontage stands farther back, separate doorways clear in overcast daylight, no opening-day or calendar cues.';
assert.equal(oldS077Prompt, 'Medium shot at a separate early-1970s Japanese records desk, one clerk closing a plain application binder beside a simplified counter diagram, the binder\'s worn blank tab nearest the viewer, quiet desk-lamp light.');
assert.equal(oldS079Prompt, 'Wide shot of a 1970s Japanese commercial street, one pedestrian walking toward a newly opened unsigned conveyor sushi shop while a different modest counter frontage stands farther back, separate doorways clear in overcast daylight.');
chapters.turn.scenes.find((scene) => scene.id === 'turn-s077').data.prompt = newS077Prompt;
chapters.turn.scenes.find((scene) => scene.id === 'turn-s079').data.prompt = newS079Prompt;
const oldT8Line = oldChapters.turn.scenes.find((scene) => scene.id === 'turn-s079').lines[0].text;
const newT8Line = '判決也說，後來已有許多與提告的元祿壽司公司無關的業者，經營輸送帶壽司店。';
const oldT8Claim = chapterClaims.t8.claim.claim;
const newT8Claim = '後來已有許多與提告的元祿壽司公司無關的業者，經營輸送帶壽司店';
assert.equal(oldT8Line, '此後，已有許多公司在元祿之外，開起自己的輸送帶壽司店。');
assert.equal(oldT8Claim, '已有許多公司在元祿之外，開起自己的輸送帶壽司店');
chapters.turn.scenes.find((scene) => scene.id === 'turn-s079').lines[0].text = newT8Line;
chapterClaims.t8.claim.claim = newT8Claim;
assert.equal(chapterClaims.t8.claim.fact, 5);
assert.equal(chapterClaims.t8.claim.source, 3);
assert.equal(chapterClaims.e8.claim.fact, 5);
assert.equal(chapterClaims.e8.claim.source, 0);
assert.equal(chapterClaims.t9.claim.fact, 5);
assert.equal(chapterClaims.t9.claim.source, 0);
chapterClaims.t8.claim.fact = 4;      // Court: unrelated companies after expiry.

const coverage = structuredClone(oldCoverage);
coverage.status = 'OFFLINE_PROPOSED_COURT_PDF_SOURCE_SPLIT_ONLY';
coverage.parent_candidate_manifest_sha256 = parentManifestSha;
coverage.row_to_storyboard_facts[4] = {
  row_fact_index: 4,
  storyboard_fact_indices: [4, 5],
  row_sources: [3],
  scene_claim_ids: ['h7', 'e6', 'e7', 't7', 't8'],
};
coverage.row_to_storyboard_facts[5] = {
  row_fact_index: 5,
  storyboard_fact_indices: [5],
  row_sources: [0],
  scene_claim_ids: ['e8', 't9'],
  note: 'J-Net21 warnings and affiliate independence; the disputed 1978 year stays in caveats, not narration.',
};
const coverageById = Object.fromEntries(coverage.scene_claims.map((claim) => [claim.id, claim]));
assert.equal(coverageById.t8.proposed_row_fact_index, 5);
assert.equal(coverageById.e8.proposed_row_fact_index, 5);
assert.equal(coverageById.t9.proposed_row_fact_index, 5);
coverageById.t8.proposed_row_fact_index = 4;
coverageById.t8.claim = newT8Claim;

const { STORY_KEYS, storyProblems, storyHash, reviewProblems, LIMITS } =
  await import(pathToFileURL(path.join(root, 'tools/video/story-plans/plan.mjs')).href);
const story = Object.fromEntries(STORY_KEYS.map((key) => [key, row[key]]));
const storySha = storyHash(story);
assert.deepEqual(storyProblems(story, 'B18'), []);
assert(row.must_verify.every((fact) => [...fact.claim].length <= LIMITS.claim));
const expectedSources = structuredClone(row.sources);
expectedSources[3].supports = oldPdfSupports;
assert.deepEqual(expectedSources, oldRow.sources, 'sources changed beyond court supports');
const expectedChapters = structuredClone(row.chapters);
expectedChapters.find((chapter) => chapter.key === 'turn').point = oldTurnPoint;
assert.deepEqual(expectedChapters, oldRow.chapters, 'chapters changed beyond turn point');
assert.deepEqual(series.plan.sources, row.sources);
assert.deepEqual(series.plan.chapters, row.chapters);
assert.deepEqual({ ...row, must_verify: oldRow.must_verify, sources: expectedSources,
  chapters: expectedChapters, caveats: oldCaveats }, oldRow,
  'row changed beyond facts 4/5, turn point, court supports, caveat');
assert.deepEqual({ ...series, plan: { ...series.plan, must_verify: oldSeries.plan.must_verify,
  sources: oldSeries.plan.sources, chapters: oldSeries.plan.chapters, caveats: oldSeries.plan.caveats } }, oldSeries,
  'series changed beyond facts 4/5, turn point, court supports, caveat');
assert(!row.chapters.some((chapter) => /元祿以外|元禄以外/.test(chapter.point)),
  'broader-than-court shorthand remains in chapter point');
assert(!row.sources[3].supports.includes('851953的期滿日'));
for (const index of [0, 1, 2, 3, 6, 7, 8, 9]) assert.deepEqual(row.must_verify[index], oldRow.must_verify[index]);
assert.deepEqual(row.must_verify[4].sources, [3]);
assert.deepEqual(row.must_verify[5].sources, [0]);
assert.equal(row.must_verify[5].attributed, true);
assert(row.caveats.includes('本片不口播1978年'));
const authorFacing = [row.title, row.logline, row.question, row.takeaway,
  ...row.chapters.map((chapter) => chapter.point), ...row.must_verify.map((fact) => fact.claim),
  ...Object.values(chapters).flatMap((chapter) => chapter.scenes.flatMap((scene) =>
    (scene.lines ?? []).map((line) => line.text)))].join('\n');
assert(!/1978|一九七八|七八年/.test(authorFacing), 'disputed 1978 year leaked into speakable plan or authored lines');
assert(row.must_verify.every((fact) => !Object.hasOwn(fact, 'reviewer_only')),
  'reviewer_only is a later independent-review decision, never self-issued by this candidate');

// Every scene, picture prompt, source URL and UNCHECKED verdict must survive.
// One spoken line and its scene claim narrow "outside Genroku" to the court's
// actual "unrelated to the plaintiff" finding. No other wording may change.
let lines = 0; let scenes = 0; let claimCount = 0;
for (const key of keys) {
  const before = oldChapters[key];
  const after = chapters[key];
  scenes += after.scenes.length;
  lines += after.scenes.flatMap((scene) => scene.lines ?? []).length;
  claimCount += after.claims.length;
  const expectedScenes = structuredClone(after.scenes);
  if (key === 'turn') {
    expectedScenes.find((scene) => scene.id === 'turn-s077').data.prompt = oldS077Prompt;
    expectedScenes.find((scene) => scene.id === 'turn-s079').data.prompt = oldS079Prompt;
    expectedScenes.find((scene) => scene.id === 'turn-s079').lines[0].text = oldT8Line;
  }
  assert.deepEqual(expectedScenes, before.scenes, `${key}: extra scene/narration change`);
  const expected = structuredClone(after);
  expected.scenes = expectedScenes;
  for (const claim of expected.claims) {
    claim.fact = before.claims.find((old) => old.id === claim.id).fact;
    if (claim.id === 't8') claim.claim = oldT8Claim;
  }
  assert.deepEqual(expected, before, `${key}: changes beyond one fact pointer`);
  for (const claim of after.claims) assert.equal(claim.verdict, 'UNCHECKED', `${claim.id}: verdict changed`);
}
assert.deepEqual([scenes, lines, claimCount], [85, 88, 65]);
assert.deepEqual(coverage.scene_claims.map((claim) => claim.id), oldCoverage.scene_claims.map((claim) => claim.id));
assert.deepEqual(coverage.scene_claims.map((claim) => claim.id === 't8' ? oldT8Claim : claim.claim),
  oldCoverage.scene_claims.map((claim) => claim.claim));
assert.deepEqual(coverage.scene_claims.map((claim) => claim.source_index), oldCoverage.scene_claims.map((claim) => claim.source_index));
assert(coverage.scene_claims.every((claim) => claim.verdict === 'UNCHECKED'));
for (const [key, chapter] of Object.entries(chapters)) {
  for (const claim of chapter.claims) {
    const mapped = coverageById[claim.id];
    assert(mapped, `${key}/${claim.id}: missing coverage`);
    assert.equal(mapped.proposed_row_fact_index, claim.fact, `${key}/${claim.id}: coverage fact drift`);
    assert.equal(mapped.source_index, claim.source, `${key}/${claim.id}: coverage source drift`);
  }
}
for (const mapping of coverage.row_to_storyboard_facts) {
  assert.deepEqual(mapping.row_sources, row.must_verify[mapping.row_fact_index].sources);
  assert.deepEqual(mapping.scene_claim_ids.sort(), coverage.scene_claims
    .filter((claim) => claim.proposed_row_fact_index === mapping.row_fact_index)
    .map((claim) => claim.id).sort(), `fact ${mapping.row_fact_index}: scene list drift`);
}

const staleReview = JSON.parse(fs.readFileSync(path.join(parent, 'reviews/B18.json'), 'utf8'));
assert(reviewProblems(staleReview, story, 'B18').some((problem) => problem.includes('story changed after this review')));
const { fetchProblems } = await import(pathToFileURL(path.join(root, 'tools/video/story-plans/validate.mjs')).href);
const fakeRead = row.sources.map((source, index) => ({ id: 'B18', index, url: source.url, status: 200,
  readable: index !== 3, ...(index === 3 ? { error: 'not a text page (application/pdf)' } : {}) }));
const fakePlan = { stories: [{ id: 'B18', story: row, review: { reviewer_only: [] } }] };
assert(fetchProblems(fakePlan, fakeRead).some((problem) => problem.includes('must_verify[4] cites only pages')));
fakePlan.stories[0].review.reviewer_only = [4];
assert.deepEqual(fetchProblems(fakePlan, fakeRead), [], 'future independent reviewer_only [4] would not satisfy reader rule');

const outputs = new Map([
  ['B18.json', canonical(row)],
  ['series-adoption.json', canonical(series)],
  ['claim-coverage.json', canonical(coverage)],
]);
for (const key of keys) outputs.set(`remapped-chapters/${key}.json`, canonical(chapters[key]));
const delta = {
  schema_version: 1,
  status: 'OFFLINE_EXACT_SOURCE_BINDING_DELTA_INDEPENDENT_REVIEW_PENDING',
  parent_candidate_manifest_sha256: parentManifestSha,
  changed_row_facts: [4, 5],
  old_fact_4_sources: oldRow.must_verify[4].sources,
  new_fact_4_sources: row.must_verify[4].sources,
  old_fact_5_sources: oldRow.must_verify[5].sources,
  new_fact_5_sources: row.must_verify[5].sources,
  chapter_turn_point_precision_change: { from: oldTurnPoint, to: row.chapters.find((chapter) => chapter.key === 'turn').point },
  court_source_supports_precision_change: { from: oldPdfSupports, to: row.sources[3].supports },
  no_spoken_1978_caveat_change: { from: oldCaveats, to: row.caveats },
  scene_fact_pointer_changes: [
    { id: 't8', from: 5, to: 4, source: 3 },
  ],
  spoken_source_precision_change: { scene: 'turn-s079', line_id: '230c59db', from: oldT8Line, to: newT8Line },
  scene_claim_precision_change: { id: 't8', from: oldT8Claim, to: newT8Claim },
  visual_prompt_precision_changes: [
    { scene: 'turn-s077', from: oldS077Prompt, to: newS077Prompt },
    { scene: 'turn-s079', from: oldS079Prompt, to: newS079Prompt },
  ],
  unchanged: ['source URLs/kinds/publishers/check dates and five other source supports', 'other eight row facts',
    'other five chapter points and all other authored chapters/scenes/lines/visuals',
    '64 other claim texts and all 65 direct sources/verdicts', 'names/cast/look/thumbnail',
    'active episode/review/stories'],
  court_pdf_source_index: 3,
  readable_fact_5_source_indices: [0],
  disputed_1978_only_in_source_supports_and_caveat: true,
  reviewer_only_receipt: 'NOT_ISSUED_PENDING_INDEPENDENT_PDF_REVIEW',
};
outputs.set('delta.json', canonical(delta));
const verification = {
  schema_version: 1,
  status: 'PASS_OFFLINE_STRUCTURAL_DELTA_ONLY_REVIEW_PENDING',
  parent_candidate_manifest_sha256: parentManifestSha,
  row_sha256: sha(outputs.get('B18.json')),
  canonical_story_sha256: storySha,
  series_adoption_sha256: sha(outputs.get('series-adoption.json')),
  coverage_sha256: sha(outputs.get('claim-coverage.json')),
  scene_count: scenes, narration_line_count: lines, scene_claim_count: claimCount,
  spoken_line_precision_changes: 1, scene_claim_precision_changes: 1,
  visual_prompt_precision_changes: 2,
  chapter_point_precision_changes: 1, source_supports_precision_changes: 1,
  all_scene_claims_unchecked: true, story_problems: [],
  old_review_invalid: true, pdf_only_fact_index: 4, readable_jnet21_fact_index: 5,
  no_spoken_1978_caveat_added: true,
  simulated_fetch_without_reviewer_only_blocks: true,
  simulated_fetch_with_independently_approved_reviewer_only_would_pass: true,
  independent_pdf_review_for_new_hash: false, import_approved: false, host_written: false,
  paid_calls: 0, rendered_video: false,
};
outputs.set('verification.json', canonical(verification));

const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
for (const [file, content] of outputs) {
  const target = path.join(here, file);
  if (mode === '--write') { fs.mkdirSync(path.dirname(target), { recursive: true }); fs.writeFileSync(target, content); }
  else assert.equal(fs.readFileSync(target, 'utf8'), content, `candidate drift: ${file}`);
}
console.log(canonical(verification));
