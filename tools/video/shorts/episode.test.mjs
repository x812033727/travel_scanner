import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { explainerFixture, sandbox } from '../core/fixtures/load.mjs';
import { main } from './cli.mjs';
import { cameraWords as cameraWordOf, episodeShort, sceneHtml, sha256, validate, verifyEvidence } from './core.mjs';
import { EPISODE_SERIES, episodeShortFields, episodeShortsProblems, loadEpisodeShorts, shortsFile } from './episode.mjs';

/** The explainer fixture in a sandbox, with a keyframe per shot in its work directory. */
function episodeBox({ review = [] } = {}) {
  const box = sandbox('fixture-explainer', 'explainer');
  const shots = {};
  mkdirSync(path.join(box.workdir, 'keyframes'), { recursive: true });
  for (const scene of explainerFixture().scenes.filter((each) => each.template === 'shot')) {
    const bytes = Buffer.from(`png of ${scene.id}`);
    const file = `keyframes/${scene.id}-1.png`;
    writeFileSync(path.join(box.workdir, file), bytes);
    shots[scene.id] = { file, sha256: sha256(bytes), needs_review: review.includes(scene.id) };
  }
  writeFileSync(path.join(box.workdir, 'keyframes', 'manifest.json'), JSON.stringify({ shots }));
  return { box, load: () => loadEpisodeShorts({ slug: box.slug, root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base }) };
}

const shortsOf = (box) => JSON.parse(readFileSync(shortsFile(box.slug, box.root), 'utf8'));

test('an episode Short is a cut of its episode whose scenes may name shots; other lines may not', () => {
  const [doc] = JSON.parse(readFileSync(new URL('../core/fixtures/explainer/shorts.json', import.meta.url), 'utf8'));
  assert.deepEqual(validate(doc), []);
  assert.deepEqual(validate({ ...doc, source: undefined }), ['source.slug required']);
  const lab = { ...doc, line: 'lab', series: 'daily', experiment_summary: 'x', limitations: 'y', evidence: [{ path: 'a.json', sha256: 'a'.repeat(64) }] };
  assert.deepEqual(validate(lab), [0, 1, 2].map((i) => `scene ${i}: shot names a keyframe of the video a cut comes from (line cut only)`));
  const both = structuredClone(doc);
  both.scenes[0].asset = 'x.png';
  assert.ok(validate(both).includes('scene 0: a scene shows a shot or an asset, not both'));
  assert.deepEqual(episodeShortFields('b08-nokia', 1), { schema_version: 2, slug: 'b08-nokia-short-2', format: 'shorts', locale: 'zh-TW', line: 'cut', series: EPISODE_SERIES, source: { slug: 'b08-nokia' } });
});

test('shots become keyframe evidence bound by hash; a changed, missing or unreviewed keyframe is refused', () => {
  const { box, load } = episodeBox();
  const episode = load();
  assert.equal(episode.shorts.length, 2);
  const [first] = episode.shorts;
  assert.equal(first.scenes[0].asset, 'keyframes/flash-1.png');
  assert.equal(first.scenes[0].shot, undefined);
  assert.deepEqual(first.evidence.map((item) => item.path), ['keyframes/flash-1.png', 'keyframes/race-1.png', 'keyframes/count-1.png']);
  assert.equal(verifyEvidence(first, episode.workdir).length, 3);
  assert.equal(episode.shorts[1].evidence.length, 2, 'a scene without a shot has no picture to bind');

  writeFileSync(path.join(box.workdir, 'keyframes', 'race-1.png'), 'redrawn');
  assert.throws(() => verifyEvidence(first, episode.workdir), /evidence changed: keyframes\/race-1\.png/);
  assert.throws(() => episodeShort(shortsOf(box)[0], { shots: {} }), /shot "flash" has no keyframe/);
  assert.throws(() => episodeBox({ review: ['count'] }).load(), /shot "count" still needs a prompt fix/);
});

test("shorts.json holds this episode's two Shorts, cut from it, named after it, showing only its shots", () => {
  const video = explainerFixture();
  const { box } = episodeBox();
  const shorts = shortsOf(box);
  assert.deepEqual(episodeShortsProblems(shorts, video), []);
  assert.deepEqual(episodeShortsProblems(shorts.slice(0, 1), video), ['shorts.json must hold 2 Shorts']);
  const wrong = structuredClone(shorts);
  wrong[1].source.slug = 'other-video';
  wrong[1].slug = 'other';
  wrong[0].scenes[0].shot = 'answer';
  wrong[0].line = 'drama';
  assert.deepEqual(episodeShortsProblems(wrong, video), [
    'short 1: scene 0: shot names a keyframe of the video a cut comes from (line cut only)',
    'short 1: scene 1: shot names a keyframe of the video a cut comes from (line cut only)',
    'short 1: scene 2: shot names a keyframe of the video a cut comes from (line cut only)',
    'short 1: must be a cut (schema_version 2, line "cut")',
    'short 1, scene 0: "answer" is not a shot of fixture-explainer',
    'short 2: source.slug must be fixture-explainer',
    'short 2: slug must be fixture-explainer-short-2',
  ]);
});

test('the series theme brands every card and points every card to the long video', () => {
  const { load } = episodeBox();
  const [doc] = load().shorts;
  const card = sceneHtml(doc, { sceneIndex: 0, text: '閃電亮了' });
  assert.match(card, /data-theme="cut-sothatswhy"/);
  assert.match(card, /<div class="brand">原來如此事務所<\/div>/);
  assert.match(card, /<div class="series">原來如此<\/div>/);
  assert.match(card, /· 完整版在長片 ▶<\/div>/);
  assert.match(card, /background:#1f2a44/, 'the ink navy of the series');
  assert.match(sceneHtml({ ...doc, series: 'other-video' }, { sceneIndex: 0, text: 'x' }), /data-theme="cut"/, "another cut keeps the highlights' theme");
});

test('from-episode needs the episode and one of its two Shorts', async () => {
  await assert.rejects(main(['from-episode']), /--slug required/);
  await assert.rejects(main(['from-episode', '--slug', 'x', '--short', '3']), /--short must be 1 or 2/);
});

test('a shot\'s picture moves in the Short as it did in the long video, and an illustrated slides video\'s Shorts carry their own series and theme', async () => {
  const { illustratedFixture, sandbox: box } = await import('../core/fixtures/load.mjs');
  const { episodeSeries, ILLUSTRATED_SERIES } = await import('./episode.mjs');
  const { themeOf } = await import('./layouts.mjs');
  const { explainerFixture } = await import('../core/fixtures/load.mjs');
  assert.equal(episodeSeries(explainerFixture()), EPISODE_SERIES);
  assert.equal(episodeSeries(illustratedFixture()), ILLUSTRATED_SERIES);
  assert.equal(episodeShortFields('jev-model', 0, ILLUSTRATED_SERIES).series, 'illustrated');
  assert.equal(themeOf({ schema_version: 2, line: 'cut', series: ILLUSTRATED_SERIES }).id, 'cut-illustrated');

  // The explainer's Shorts: each shot's camera direction becomes the scene's camera word.
  const { load } = episodeBox();
  const [first] = load().shorts;
  const cameras = Object.fromEntries(explainerFixture().scenes.filter((scene) => scene.template === 'shot').map((scene) => [scene.id, scene.data.camera]));
  assert.ok(first.scenes.every((scene) => typeof scene.camera === 'string'), 'every picture scene moves');
  assert.equal(first.scenes[0].camera, cameraWordOf(cameras.flash));
  assert.deepEqual(validate(first), []);

  // An illustrated slides video with shorts.json naming its shots: its keyframes, its cameras, its series.
  const sand = box('ranking-first', 'illustrated');
  const video = { ...illustratedFixture(), slug: 'ranking-first' };
  writeFileSync(path.join(sand.dir, 'video.json'), JSON.stringify(video));
  const shots = {};
  mkdirSync(path.join(sand.workdir, 'keyframes'), { recursive: true });
  for (const scene of video.scenes.filter((each) => each.template === 'shot')) {
    const bytes = Buffer.from(`png of ${scene.id}`);
    writeFileSync(path.join(sand.workdir, `keyframes/${scene.id}-1.png`), bytes);
    shots[scene.id] = { file: `keyframes/${scene.id}-1.png`, sha256: sha256(bytes), needs_review: false };
  }
  writeFileSync(path.join(sand.workdir, 'keyframes', 'manifest.json'), JSON.stringify({ shots }));
  const shorts = [0, 1].map((index) => ({
    ...episodeShortFields('ranking-first', index, ILLUSTRATED_SERIES),
    titles: ['第一名不一定最好用', '排行榜是考試'], description: '完整故事在長片。',
    scenes: [{ headline: '你以為第一名最好用', narration: ['你以為第一名最好用'], shot: 'podium' }, { headline: '三個數字', narration: ['三秒對二十秒'], big: '20 秒' }, { headline: '先看工作', narration: ['先看工作再看排行榜'], shot: 'door', camera: 'tilt up' }],
  }));
  writeFileSync(shortsFile('ranking-first', sand.root), JSON.stringify(shorts));
  const loaded = loadEpisodeShorts({ slug: 'ranking-first', root: sand.root, env: { VIDEO_WORKDIR: sand.work }, home: sand.base });
  assert.equal(loaded.shorts[0].scenes[0].camera, cameraWordOf(video.scenes.find((scene) => scene.id === 'podium').data.camera), "the long video's camera");
  assert.equal(loaded.shorts[0].scenes[2].camera, 'tilt up', "the Short's own word wins");
  assert.equal(loaded.shorts[0].scenes[1].camera, undefined, 'a scene of cards has no picture to move');
  assert.equal(loaded.shorts[0].scenes[0].asset, 'keyframes/podium-1.png');
  assert.deepEqual(episodeShortsProblems(shorts.map((doc) => ({ ...doc, series: 'sothatswhy' })), video), ['short 1: series must be illustrated', 'short 2: series must be illustrated']);
  writeFileSync(path.join(sand.dir, 'video.json'), JSON.stringify({ ...video, scenes: video.scenes.filter((scene) => scene.template !== 'shot') }));
  assert.throws(() => loadEpisodeShorts({ slug: 'ranking-first', root: sand.root, env: { VIDEO_WORKDIR: sand.work }, home: sand.base }), /has no shots/);
});
