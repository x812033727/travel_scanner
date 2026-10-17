#!/usr/bin/env node
// Offline-only B18 import-row proposal. Never writes the active plan or an import file.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const parent = path.resolve(here, '../B18-claim-granularity-candidate-20261017');
const pilot = path.resolve(here, '../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const expectedManifest = '1016d3de91236af487eec891e256f43214d71a06ba806409084831f47584e198';
const sha = (data) => crypto.createHash('sha256').update(data).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (name) => fs.readFileSync(path.join(parent, name));
const manifestBytes = read('sha256.json');
assert.equal(sha(manifestBytes), expectedManifest, 'final B18 candidate manifest drifted');
const manifest = JSON.parse(manifestBytes);
for (const [name, expected] of Object.entries(manifest.files)) {
  assert.equal(sha(read(name)), expected, `final B18 candidate file drift: ${name}`);
}
const seriesBytes = read('series.json');
const series = JSON.parse(seriesBytes);
const source = series.plan;
assert.equal(series.kind, 'story');
assert.equal(series.slug, 'brand-stories-curio-pilot-v2');
assert.equal(series.episode, 2);
assert.equal(series.target_minutes, 10);
assert.equal(series.image_model, 'image-01');
assert.deepEqual(series.look, { preset: 'cute-mystery' });
assert.equal(source.id, 'B18');
assert.equal(source.sources.length, 6);
assert.equal(source.must_verify.length, 13);

// The storyboard's old fact indices remain unchanged. The import schema accepts at most ten
// representative must_verify claims, so first-shop identity and its 20-tsubo/50-yen detail
// share one row-level claim. The source indices remain identical to the reviewed storyboard.
const groups = [
  [0, 6], [1], [2], [3], [4], [5], [7], [8], [10], [12],
];
const mustVerify = [
  { claim: '1958年4月白石義明在大阪布施開出「廻る元禄寿司」首店；發明協會記它約20坪、僅有吧台座位，主要是一盤四貫50日圓。', sources: [0, 1, 2], core: true },
  { claim: 'J-Net21記1948年白石參觀大阪吹田一座啤酒工廠；他看見輸送帶送瓶，想到用同一送盤原理緩解店內人手問題。資料未確定啤酒公司。', sources: [0, 1, 2], core: true },
  { claim: '在較早的立食壽司店，一盤四貫20日圓；人手和師傅工作量跟不上增加的訂單。20日圓不得說成1958年迴轉首店售價。', sources: [0, 2] },
  { claim: '轉彎卡盤約花十年解決；J-Net21記撲克牌扇形，發明協會記名片扇形，兩者是不同來源說法；最後採扇形板片，1957年試作機完成。', sources: [0, 2], attributed: true },
  { claim: '法院判決理由認定「コンベヤ附調理食台」實用新案第579776號1962年登錄、1972年期滿。J-Net21及發明協會另寫1978年；不能當作同一權利的確定期滿年。', sources: [0, 2, 3], core: true },
  { claim: 'J-Net21記元祿曾對相似店警告、部分加盟店後來獨立；法院認定1972年該實用新案期滿後已有無關公司經營。不能把其他業者全歸因於1978年單一權利。', sources: [0, 3], core: true },
  { claim: '1970年大阪萬博有元祿壽司出店；發明協會記出店受表彰、讓更多人認識這種吃法，後來元祿店數達240家。不得把全國知名度當法院已確認事實。', sources: [0, 2], attributed: true },
  { claim: '日本機械學會2021年機械遺產第112號包含元祿堺東店當時仍在使用的1985年製輸送機，及元祿產業另外保存的早期魚鱗板；不是1958年首店同一原機。', sources: [0, 1] },
  { claim: '石野集團官方年表記1980年開始販售供大型店使用的旁通裝置，1986年有ㄇ字型輸送帶店；這不證明兩者在同一店或存在直接因果。', sources: [4] },
  { claim: '發明協會記一些新業者改在後場製作壽司、把盤子放上直線輸送帶送往客區；這是後來不同店的做法，不是白石首店的一次改裝。', sources: [2], attributed: true },
];
assert.equal(groups.length, mustVerify.length);
const oldToNew = new Map(groups.flatMap((indices, next) => indices.map((old) => [old, next])));
assert.equal(oldToNew.size, 11);
assert.deepEqual([...oldToNew.keys()].sort((a, b) => a - b), [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12]);
for (const [index, indices] of groups.entries()) {
  const union = new Set(indices.flatMap((old) => source.must_verify[old].sources));
  for (const cited of union) assert(mustVerify[index].sources.includes(cited), `row claim ${index} lost source ${cited}`);
}

const row = {
  number: 2, id: 'B18', slug: 'story-conveyor-belt-sushi-v2',
  category: source.category, region: source.region, subject: source.subject,
  title: series.title, logline: series.logline, question: source.question,
  chapters: structuredClone(source.chapters), takeaway: source.takeaway,
  must_verify: mustVerify, sources: structuredClone(source.sources),
  names: structuredClone(source.names), cast: structuredClone(source.cast),
  image_notes: source.image_notes, sensitivity: source.sensitivity,
  related_guide: source.related_guide, thumbnail: structuredClone(source.thumbnail),
  caveats: source.caveats, publish: structuredClone(source.publish),
};
assert.deepEqual(row.sources, source.sources, 'storyboard source indices drifted');
assert.deepEqual(row.chapters, source.chapters, 'storyboard chapter points drifted');
assert.equal(row.publish.day, 2);
assert.equal(row.publish.slot, '12:00');

const chapters = Object.fromEntries(keys.map((key) => [key, JSON.parse(read(`chapters/${key}.json`))]));
const scenes = keys.flatMap((key) => chapters[key].scenes);
const sceneIds = new Set(scenes.map((scene) => scene.id));
const claims = keys.flatMap((key) => chapters[key].claims);
assert.equal(scenes.length, 85);
assert.equal(claims.length, 65);
assert.equal(new Set(claims.map((claim) => claim.id)).size, claims.length);
const claimCoverage = claims.map((claim) => {
  assert(sceneIds.has(claim.scene), `missing scene: ${claim.id}`);
  assert(row.sources[claim.source], `missing source: ${claim.id}`);
  assert.equal(claim.verdict, 'UNCHECKED', `review state changed: ${claim.id}`);
  const rowFact = claim.fact == null ? null : oldToNew.get(claim.fact);
  if (claim.fact != null) {
    assert(Number.isInteger(rowFact), `storyboard fact not mapped: ${claim.id}`);
    assert(row.must_verify[rowFact].sources.includes(claim.source), `row fact/source mismatch: ${claim.id}`);
  }
  return {
    id: claim.id, scene: claim.scene, claim: claim.claim,
    source_index: claim.source, storyboard_fact_index: claim.fact ?? null,
    proposed_row_fact_index: rowFact, verdict: claim.verdict,
    coverage: rowFact == null ? 'direct_scene_source_only' : 'representative_row_fact_and_direct_scene_source',
  };
});
const rowToStoryboardFacts = groups.map((indices, rowFact) => ({
  row_fact_index: rowFact, storyboard_fact_indices: indices,
  row_sources: row.must_verify[rowFact].sources,
  scene_claim_ids: claimCoverage.filter((claim) => claim.proposed_row_fact_index === rowFact).map((claim) => claim.id),
}));
const unusedPlanFacts = [9, 11];
assert(unusedPlanFacts.every((index) => !claims.some((claim) => claim.fact === index)));
const coverage = {
  schema_version: 1, status: 'OFFLINE_PROPOSED_ROW_COVERAGE_ONLY',
  parent_manifest_sha256: expectedManifest,
  original_storyboard_fact_count: source.must_verify.length,
  proposed_row_fact_count: row.must_verify.length,
  scene_claim_count: claims.length,
  row_to_storyboard_facts: rowToStoryboardFacts,
  unspoken_storyboard_plan_facts_not_in_row: [
    { fact_index: 9, reason: '2022/2023 market figures are background and absent from final narration; source[0] remains, no current-market claim.' },
    { fact_index: 11, reason: '1971/1974 tea-device discrepancy is a caveat, not a final narration claim; sources[4]/[5] remain.' },
  ],
  scene_claims: claimCoverage,
};

// Isolated chapter copies show exactly what the future author-chapter adapter would need.
// The frozen storyboard is untouched: only fact pointers into the ten-row checklist change.
const remappedChapters = structuredClone(chapters);
let changedFactPointers = 0;
for (const key of keys) {
  const before = chapters[key];
  const after = remappedChapters[key];
  assert.deepEqual(after.scenes, before.scenes, `${key} scene changed`);
  assert.deepEqual(after.loops, before.loops, `${key} loops changed`);
  for (let index = 0; index < after.claims.length; index++) {
    const old = before.claims[index];
    const next = after.claims[index];
    if (old.fact != null) {
      next.fact = oldToNew.get(old.fact);
      if (next.fact !== old.fact) changedFactPointers++;
    }
    assert.deepEqual({ ...next, fact: old.fact }, old, `${key} claim other than fact changed: ${old.id}`);
  }
}
const beats = Object.fromEntries(Object.entries(row).filter(([key]) => !['number', 'title', 'logline', 'slug'].includes(key)));
const adoptionSeries = { ...series, plan: beats };
assert.equal(adoptionSeries.plan.must_verify.length, 10);
assert.deepEqual(adoptionSeries.plan.sources, series.plan.sources);
let externalCalls = 0;
globalThis.fetch = () => { externalCalls++; throw new Error('B18 offline row adoption must not fetch'); };
const { composeStory, cuteStoryVisualProblems } = await import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs')).href);
const authored = path.resolve(here, '../B18-authored-chapters-candidate');
const voice = JSON.parse(fs.readFileSync(path.join(authored, 'synthetic/docroot/docs/videos/story-conveyor-belt-sushi-v2/video.json'), 'utf8')).voice;
const originalVideo = composeStory({ slug: row.slug, info: series, chapters, voice, drama: { music_enabled: false }, root });
const remappedVideo = composeStory({ slug: row.slug, info: adoptionSeries, chapters: remappedChapters, voice, drama: { music_enabled: false }, root });
assert.deepEqual(remappedVideo, originalVideo, 'row/fact remap changed composed video');
assert.deepEqual(cuteStoryVisualProblems(remappedVideo), []);
assert.equal(externalCalls, 0);

const plan = await import(pathToFileURL(path.join(root, 'tools/video/story-plans/plan.mjs')).href);
const projected = Object.fromEntries(plan.STORY_KEYS.map((key) => [key, row[key]]));
const problems = plan.storyProblems(projected, 'B18');
assert.deepEqual(problems, [], `storyProblems: ${problems.join('; ')}`);
const oldReview = JSON.parse(fs.readFileSync(path.join(pilot, 'episodes/reviews/B18.json'), 'utf8'));
const oldReviewProblems = plan.reviewProblems(oldReview, projected, 'B18');
assert(oldReviewProblems.some((problem) => problem.includes('story changed after this review')), 'old review must be stale');
const originalRow = JSON.parse(fs.readFileSync(path.join(pilot, 'episodes/B18.json'), 'utf8'));
assert.notEqual(plan.storyHash(projected), oldReview.story_sha256);
assert.notDeepEqual(row.must_verify, originalRow.must_verify);

// Exercise the same two-row ordering/series shape in memory; no stories.json is written.
const importSeries = JSON.parse(fs.readFileSync(path.join(pilot, 'series.json'), 'utf8'));
const a01 = JSON.parse(fs.readFileSync(path.join(pilot, 'episodes/A01.json'), 'utf8'));
assert.deepEqual(plan.seriesProblems(importSeries), []);
assert.equal(importSeries.slug, series.slug);
assert.equal(importSeries.planned_episodes, 2);
assert.equal(a01.number, 1);
assert.equal(a01.slug, 'story-rolling-suitcase-v2');
const preview = { schema_version: 1, series: importSeries, stories: [a01, row] };
assert.deepEqual(preview.stories.map((story) => story.number), [1, 2]);
assert.equal(new Set(preview.stories.map((story) => story.slug)).size, 2);

const outputs = new Map([
  ['B18.json', canonical(row)],
  ['claim-coverage.json', canonical(coverage)],
  ['series-adoption.json', canonical(adoptionSeries)],
]);
for (const key of keys) outputs.set(`remapped-chapters/${key}.json`, canonical(remappedChapters[key]));
const evidence = {
  schema_version: 1, status: 'OFFLINE_STRUCTURAL_PASS_INDEPENDENT_REVIEW_PENDING',
  parent_manifest_sha256: expectedManifest,
  parent_series_sha256: sha(seriesBytes),
  candidate_row_sha256: sha(outputs.get('B18.json')),
  candidate_story_sha256: plan.storyHash(projected),
  candidate_sources_sha256: sha(canonical(row.sources)),
  candidate_claim_coverage_sha256: sha(outputs.get('claim-coverage.json')),
  candidate_series_adoption_sha256: sha(outputs.get('series-adoption.json')),
  candidate_remapped_chapter_sha256: Object.fromEntries(keys.map((key) => [key, sha(outputs.get(`remapped-chapters/${key}.json`))])),
  active_row_unchanged: true, compiled_import_file_written: false,
  representative_must_verify: row.must_verify.length,
  storyboard_claims_unchecked: claims.length,
  storyboard_claims_with_row_fact: claimCoverage.filter((claim) => claim.proposed_row_fact_index != null).length,
  storyboard_claims_direct_source_only: claimCoverage.filter((claim) => claim.proposed_row_fact_index == null).length,
  changed_fact_pointers_in_isolated_copies: changedFactPointers,
  composed_video_identical: true, cute_story_visual_problems: 0, external_calls: externalCalls,
  storyboard_unspoken_fact_indices: unusedPlanFacts,
  story_problems: problems, old_review_problems: oldReviewProblems,
  worker_source_review_pass: false, import_approved: false, host_written: false, paid_calls: 0,
};
outputs.set('verification.json', canonical(evidence));
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
for (const [name, content] of outputs) {
  const target = path.join(here, name);
  if (mode === '--write') { fs.mkdirSync(path.dirname(target), { recursive: true }); fs.writeFileSync(target, content); }
  else assert.equal(fs.readFileSync(target, 'utf8'), content, `generated output drift: ${name}`);
}
console.log(canonical(evidence));
