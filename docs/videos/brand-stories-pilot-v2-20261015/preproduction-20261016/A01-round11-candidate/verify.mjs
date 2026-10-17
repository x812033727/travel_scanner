import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Read-only check of the offline round 11 package. No provider, host or file writes.
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../../../..');
const prior = path.resolve(here, '../A01-round10-candidate');
const keys = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const read = (relative) => fs.readFileSync(path.join(here, relative));
const json = (relative) => JSON.parse(read(relative).toString('utf8'));
const manifest = json('manifest.json');
const delta = json('exact-delta.json');
assert.equal(manifest.status, 'HOLD_UNREVIEWED_OFFLINE_CANDIDATE');
assert.equal(manifest.changed_shot_visual_review, 'INVALIDATED_PENDING_EXACT_REVIEW');
assert.equal(manifest.authorizes_worker_or_media, false);
assert.equal(sha(fs.readFileSync(path.join(prior, 'manifest.json'))), manifest.base.round10_manifest_sha256);
assert.equal(sha(read('exact-delta.json')), manifest.exact_delta_sha256);
assert.equal(sha(read('validation.json')), manifest.validation_file_sha256);
assert.equal(delta.status, 'UNREVIEWED_OFFLINE_CANDIDATE');
assert.deepEqual(delta.changes.map((item) => item.scene_id), manifest.changed_scene_ids);

const candidate = {};
for (const key of keys) {
  const sourceBytes = fs.readFileSync(path.join(prior, 'candidate/chapters', `${key}.json`));
  const candidateBytes = read(`candidate/chapters/${key}.json`);
  assert.equal(sha(sourceBytes), manifest.source_chapters_sha256[key], `source ${key}`);
  assert.equal(sha(candidateBytes), manifest.candidate_chapters_sha256[key], `candidate ${key}`);
  let expected = sourceBytes;
  const oldChapter = JSON.parse(sourceBytes.toString('utf8'));
  const newChapter = JSON.parse(candidateBytes.toString('utf8'));
  for (const change of delta.changes.filter((item) => item.chapter === key)) {
    assert.equal(change.source_chapter_sha256, manifest.source_chapters_sha256[key]);
    assert.equal(change.candidate_chapter_sha256, manifest.candidate_chapters_sha256[key]);
    const oldScene = oldChapter.scenes.find((scene) => scene.id === change.scene_id);
    const newScene = newChapter.scenes.find((scene) => scene.id === change.scene_id);
    assert.ok(oldScene && newScene, change.scene_id);
    assert.equal(oldScene.data.prompt, change.before);
    assert.equal(newScene.data.prompt, change.after);
    assert.deepEqual(oldScene.lines.map((line) => line.id), change.line_ids);
    const before = Buffer.from(JSON.stringify(change.before));
    const after = Buffer.from(JSON.stringify(change.after));
    const offset = expected.indexOf(before);
    assert.ok(offset >= 0, `missing ${change.scene_id}`);
    assert.equal(expected.indexOf(before, offset + 1), -1, `duplicate ${change.scene_id}`);
    expected = Buffer.concat([expected.subarray(0, offset), after, expected.subarray(offset + before.length)]);
    newScene.data.prompt = oldScene.data.prompt;
  }
  assert.ok(expected.equals(candidateBytes), `other bytes changed in ${key}`);
  assert.deepEqual(newChapter, oldChapter, `non-prompt JSON changed in ${key}`);
  candidate[key] = JSON.parse(candidateBytes.toString('utf8'));
}

const historic = JSON.parse(fs.readFileSync(path.join(prior, 'evidence/round9-narrative.json'), 'utf8'));
assert.equal(sha(fs.readFileSync(path.join(prior, 'evidence/round9-narrative.json'))), manifest.historic_round9_narrative.sha256);
assert.equal(historic.passed, false);
assert.deepEqual(historic.failed, manifest.historic_round9_narrative.failed);
const [{ composeStory, cuteStoryVisualProblems }, { lintVideo }, { estimateTimeline }] = await Promise.all([
  import(pathToFileURL(path.join(root, 'tools/video/automation/story.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/lint.mjs'))),
  import(pathToFileURL(path.join(root, 'tools/video/core/timeline.mjs'))),
]);
const series = JSON.parse(fs.readFileSync(path.join(prior, 'evidence/round9-series.json'), 'utf8'));
const archivedVideo = JSON.parse(fs.readFileSync(path.join(prior, 'evidence/round9-composed-video.json'), 'utf8'));
const preview = composeStory({
  slug: manifest.slug,
  info: series,
  chapters: candidate,
  voice: archivedVideo.voice,
  drama: { music_enabled: Boolean(archivedVideo.music) },
  root,
  videoId: archivedVideo.youtube.video_id ?? null,
});
const context = {
  lexicon: JSON.parse(fs.readFileSync(path.join(prior, 'evidence/round9-lexicon.json'), 'utf8')),
  brief: fs.readFileSync(path.join(prior, 'evidence/round9-brief.md'), 'utf8'),
  translations: {}, others: [], series,
};
const lint = lintVideo(preview, context);
const cuteErrors = cuteStoryVisualProblems(preview);
assert.equal(lint.errors.length, 0, 'lint errors');
assert.equal(cuteErrors.length, 0, 'cute-story errors');
const scenes = preview.scenes.length;
const lines = preview.scenes.reduce((count, scene) => count + (scene.lines?.length ?? 0), 0);
assert.equal(scenes, 63);
assert.equal(lines, 92);
const estimatedSeconds = estimateTimeline(preview).total_frames / 30;
assert.equal(estimatedSeconds, 520.3333333333334);
console.log(JSON.stringify({
  status: 'MECHANICAL_ONLY_HOLD_UNREVIEWED',
  exact_prompt_only_delta: true,
  changed_scene_ids: manifest.changed_scene_ids,
  prior_visual_review_invalidated: true,
  historic_round9_passed: false,
  scenes, lines,
  lint_errors: lint.errors.length,
  lint_warnings: lint.warnings.length,
  cute_errors: cuteErrors.length,
  estimated_seconds: estimatedSeconds,
  preview_sha256: sha(Buffer.from(JSON.stringify(preview))),
  media_or_provider_calls: 0,
}, null, 2));
