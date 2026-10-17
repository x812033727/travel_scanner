import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// This is an offline editorial candidate. It neither installs author chapters
// nor creates an image-asset alias in the production worker.
const here = path.dirname(fileURLToPath(import.meta.url));
const base = path.resolve(here, '../B18-visual-direction-candidate-20261016');
const root = path.resolve(here, '../../../../..');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const pins = {
  'series.json': '54152ce70772ffb1890ef83fdc0dec8dfd8071afe75db976b7b08975cfea5c97',
  'chapters/hook.json': 'eb502bc4436ecf5b82edd49f6fd0f31502565d54b61145fb2e5a8465665691a2',
  'chapters/origin.json': '8d464a318133bf04ca804e3e4576fa6705ba483803277dc1c1664aae7bc32328',
  'chapters/idea.json': '60c5f60fb7548e7ec670cb8c5fa18372a00f58613a8b525eb4ea8b27a258a70b',
  'chapters/engine.json': '37610084a186c8d0774e63ea5f182a46952ce6104320baaa7afee1227ab8ed1d',
  'chapters/turn.json': '0a236c80489249634e5bb3aa716d9256b71813d9abea25756100eac86b7e1e37',
  'chapters/now.json': '324d3e43542206466ab03b389f3ff8ccecfc80edc5f098ecc8fe65df7c1c65a2',
};
const sourceMapping = path.resolve(base, '../B18-authored-chapters-candidate/mapping.json');
const sourceMappingSha = '46f8a6c27e79c42e733fda1e91a57e07144094907e3184d6e59d5af43cddedbc';
const cardVariantFile = path.resolve(base, '../B18-mobile-card-revision-candidate/variant.json');
const cardVariantSha = '6dda79642d299c933fa56c63d74ac95b97f947918764ad56b9705ff02cb96a24';
const sha = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const canonical = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (file) => fs.readFileSync(file, 'utf8');

for (const [name, expected] of Object.entries(pins)) {
  assert.equal(sha(fs.readFileSync(path.join(base, name))), expected, `visual-head input drift: ${name}`);
}
assert.equal(sha(fs.readFileSync(sourceMapping)), sourceMappingSha, 'prior reuse mapping drift');
assert.equal(sha(fs.readFileSync(cardVariantFile)), cardVariantSha, 'reviewed card variant drift');
const variant = JSON.parse(read(cardVariantFile));
const series = JSON.parse(read(path.join(base, 'series.json')));
const previous = Object.fromEntries(keys.map((key) => [key, JSON.parse(read(path.join(base, 'chapters', `${key}.json`)))]));
const chapters = structuredClone(previous);
const mapping = JSON.parse(read(sourceMapping));

const cardBefore = previous.idea.scenes.find((scene) => scene.id === variant.scene_id);
const cardAfter = chapters.idea.scenes.find((scene) => scene.id === variant.scene_id);
assert.equal(cardBefore?.template, 'title');
assert.equal(cardBefore.data.title, variant.title);
assert.equal(cardBefore.data.tag, variant.tag);
assert.equal(cardBefore.data.subtitle, variant.before_subtitle);
assert.equal(variant.after_subtitle, '兩份資料，兩種說法');
cardAfter.data.subtitle = variant.after_subtitle;
const reset = structuredClone(chapters);
reset.idea.scenes.find((scene) => scene.id === variant.scene_id).data.subtitle = variant.before_subtitle;
assert.deepEqual(reset, previous, 'chapter change must be the one reviewed subtitle field');

const sceneById = new Map(keys.flatMap((key) => chapters[key].scenes.map((scene) => [scene.id, scene])));
assert.equal(mapping.image_reuse.length, 3);
const reusePairs = mapping.image_reuse.map((row) => {
  const setup = sceneById.get(row.setup_scene_id);
  const payoff = sceneById.get(row.payoff_scene_id);
  assert.equal(setup?.template, 'shot');
  assert.equal(payoff?.template, 'shot');
  assert.equal(row.same_prompt_camera_key, true);
  assert.equal(row.actual_same_file_verified, null);
  assert.notEqual(setup.data.prompt, payoff.data.prompt, `visual-head prompts unexpectedly equal: ${setup.id}`);
  assert.equal(setup.data.camera, payoff.data.camera, `camera change needs new review: ${setup.id}`);
  assert.equal(setup.data.image_asset_key, undefined);
  assert.equal(payoff.data.image_asset_key, undefined);
  return {
    setup_scene_id: setup.id,
    payoff_scene_id: payoff.id,
    prior_asset_key: row.original.asset_key,
    visual_head_prompt_equal: false,
    visual_head_camera_equal: true,
    candidate_treatment: 'separate_illustrations_with_story_motif_callback',
    same_file_required_by_this_candidate: false,
    accepted_asset_sha256: null,
  };
});
const endIds = ['now-s101', 'now-s101b', 'now-s102', 'now-s103'];
assert.deepEqual(mapping.end_visual_reuse.native_scene_ids, endIds);
assert.equal(mapping.end_visual_reuse.actual_same_file_verified, null);
const endScenes = endIds.map((id) => sceneById.get(id));
assert(endScenes.every((scene) => scene?.template === 'shot'));
assert.equal(new Set(endScenes.map((scene) => scene.data.prompt)).size, 4, 'ending prompts must stay distinct');
assert(endScenes.every((scene) => scene.data.image_asset_key === undefined));
const reuseDecision = {
  schema_version: 1,
  status: 'OFFLINE_EDITORIAL_REUSE_INTENT_ONLY',
  prior_mapping_sha256: sourceMappingSha,
  visual_head_sha256_manifest: '1fa55f086c06a402d8d8ca501b35bf427e8a2093c66ed84c6ce274171e0f1f2c',
  production_alias_installed: false,
  old_mapping_unchanged: true,
  adoption_requires_explicit_reconciliation: true,
  must_not_claim_same_file_for_this_candidate: true,
  generated_images: 0,
  accepted_asset_sha256: null,
  hook_payoff: reusePairs,
  ending: {
    scene_ids: endIds,
    prior_asset_key: mapping.end_visual_reuse.original.asset_key,
    visual_head_distinct_prompts: true,
    candidate_treatment: 'four_distinct_illustrative_moments',
    same_file_required_by_this_candidate: false,
    accepted_asset_sha256: null,
  },
  note: 'This candidate withdraws the old same-file promise for its distinct scene prompts. It does not change the original mapping, install worker aliases, or prove generated-media identity. A later decision to require exact same files needs a new pinned visual and runtime change.',
};

const { composeStory, cuteStoryVisualProblems } = await import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs')).href);
const { loadProject, lintProject } = await import(pathToFileURL(path.join(root, 'tools/video/core/state.mjs')).href);
const { estimateTimeline } = await import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs')).href);
let externalCalls = 0;
globalThis.fetch = () => { externalCalls++; throw new Error('offline candidate must not fetch'); };
const slug = 'story-conveyor-belt-sushi-v2';
const authored = path.resolve(base, '../B18-authored-chapters-candidate');
const voice = JSON.parse(read(path.join(authored, 'synthetic/docroot/docs/videos', slug, 'video.json'))).voice;
const beforeDoc = composeStory({ slug, info: series, chapters: previous, voice, drama: { music_enabled: false }, root });
const doc = composeStory({ slug, info: series, chapters, voice, drama: { music_enabled: false }, root });
const beforeWithoutCard = structuredClone(beforeDoc);
beforeWithoutCard.scenes.find((scene) => scene.id === variant.scene_id).data.subtitle = variant.after_subtitle;
assert.deepEqual(beforeWithoutCard, doc, 'composed output changed outside approved card subtitle');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'b18-card-reuse-'));
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
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
assert.deepEqual(lint.errors, []);
assert.deepEqual(cuteStoryVisualProblems(doc), []);
assert.equal(externalCalls, 0);
assert.deepEqual(doc.look, { preset: 'cute-mystery' });
assert.equal(doc.subtitles.burn_in, false);
assert.equal(doc.scenes.length, 90);
assert.equal(doc.scenes.filter((scene) => scene.template === 'shot').length, 71);
assert.equal(keys.flatMap((key) => chapters[key].claims).length, 65);
assert(keys.every((key) => chapters[key].claims.every((claim) => claim.verdict === 'UNCHECKED')));
const estimatedBodySeconds = estimateTimeline(doc).total_frames / 30;
assert.equal(estimatedBodySeconds, 573);
const lineCount = keys.flatMap((key) => chapters[key].scenes.flatMap((scene) => scene.lines)).length;
assert.equal(lineCount, 93);

const delta = {
  schema_version: 1,
  status: 'OFFLINE_VISUAL_HEAD_INTEGRATION_CANDIDATE',
  base_pins: pins,
  old_card_variant_sha256: cardVariantSha,
  old_reuse_mapping_sha256: sourceMappingSha,
  chapter_changes: [{
    chapter: 'idea', scene: variant.scene_id, field: 'data.subtitle',
    before: variant.before_subtitle, after: variant.after_subtitle,
  }],
  reuse_intent_changes: {
    prior_hook_payoff_same_file_intents: reusePairs.map((row) => row.prior_asset_key),
    candidate_hook_payoff_treatment: 'separate_illustrations_with_story_motif_callback',
    prior_ending_same_file_intent: mapping.end_visual_reuse.original.asset_key,
    candidate_ending_treatment: 'four_distinct_illustrative_moments',
    runtime_alias_change: false,
  },
};
const verification = {
  schema_version: 1,
  status: 'VERIFIED_OFFLINE_CANDIDATE_STRUCTURE_ONLY',
  base_pins: pins,
  scenes: doc.scenes.length,
  lines: lineCount,
  illustrations: 71,
  cards: 19,
  claims_unchecked: 65,
  chapter_field_changes: 1,
  narration_changes: 0,
  claim_changes: 0,
  prompt_changes: 0,
  camera_changes: 0,
  estimated_body_seconds: estimatedBodySeconds,
  measured_body_seconds: null,
  lint_errors: lint.errors,
  cute_errors: [],
  lint_warnings: lint.warnings.length,
  hook_payoff_same_file_verified: false,
  ending_same_file_verified: false,
  worker_pass: false,
  images_generated: 0,
  external_calls: externalCalls,
};
const output = new Map([
  ['series.json', read(path.join(base, 'series.json'))],
  ['delta.json', canonical(delta)],
  ['reuse-intent.json', canonical(reuseDecision)],
  ['verification.json', canonical(verification)],
]);
for (const key of keys) {
  output.set(`chapters/${key}.json`, key === 'idea' ? canonical(chapters[key]) : read(path.join(base, 'chapters', `${key}.json`)));
}
const hashes = Object.fromEntries([
  ['build.mjs', sha(fs.readFileSync(path.join(here, 'build.mjs')))],
  ['README.md', sha(fs.readFileSync(path.join(here, 'README.md')))],
  ...[...output].map(([name, content]) => [name, sha(content)]),
]);
output.set('sha256.json', canonical({ schema_version: 1, files: hashes }));
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
for (const [name, content] of output) {
  const file = path.join(here, name);
  if (mode === '--write') {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, content);
  } else assert.equal(read(file), content, `generated output drift: ${name}`);
}
console.log(JSON.stringify({ status: verification.status, scenes: verification.scenes, lines: verification.lines,
  chapter_field_changes: 1, narration_changes: 0, claim_changes: 0, lint_errors: 0,
  cute_errors: 0, lint_warnings: verification.lint_warnings, external_calls: 0 }, null, 2));
