import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { explainerFixture, sandbox } from '../core/fixtures/load.mjs';
import { encodeWav, parseWav } from '../tts/wav.mjs';
import { EPISODE_SERIES, episodeShort, sceneHtml, sha256, validate, verifyEvidence } from './core.mjs';
import { episodeShortsProblems, loadEpisodeShorts, shortsFile } from './episode.mjs';
import { phraseBody, serverPhrases } from './voice.mjs';

const TOKEN = `mkv_${'s'.repeat(43)}`;

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

test('an episode Short needs its episode and shots, not an experiment report; the campaign series keep theirs', () => {
  const [doc] = JSON.parse(readFileSync(new URL('../core/fixtures/explainer/shorts.json', import.meta.url), 'utf8'));
  assert.deepEqual(validate(doc), []);
  assert.deepEqual(validate({ ...doc, episode: undefined }), ["episode must be the long video's slug"]);
  assert.deepEqual(validate({ ...doc, series: 'daily' }).sort(), ['evidence required', 'experiment_summary required', 'limitations required', 'scene 0: shot names a keyframe of the long episode (series sothatswhy only)', 'scene 1: shot names a keyframe of the long episode (series sothatswhy only)', 'scene 2: shot names a keyframe of the long episode (series sothatswhy only)'].sort());
  const both = structuredClone(doc);
  both.scenes[0].asset = 'x.png';
  assert.ok(validate(both).includes('scene 0: a scene shows a shot or an asset, not both'));
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

test("shorts.json holds this episode's two Shorts, named after it, showing only its shots", () => {
  const video = explainerFixture();
  const { box } = episodeBox();
  const shorts = shortsOf(box);
  assert.deepEqual(episodeShortsProblems(shorts, video), []);
  assert.deepEqual(episodeShortsProblems(shorts.slice(0, 1), video), ['shorts.json must hold 2 Shorts']);
  const wrong = structuredClone(shorts);
  wrong[1].episode = 'other-video';
  wrong[1].slug = 'other';
  wrong[0].scenes[0].shot = 'answer';
  assert.deepEqual(episodeShortsProblems(wrong, video), [
    'short 1, scene 0: "answer" is not a shot of fixture-explainer',
    'short 2: episode must be fixture-explainer',
    'short 2: slug must be fixture-explainer-short-2',
  ]);
});

test('the episode brand is on every frame and the last scene points to the long video', () => {
  const { load } = episodeBox();
  const [doc] = load().shorts;
  const first = sceneHtml(doc, { sceneIndex: 0, text: '閃電亮了' });
  const last = sceneHtml(doc, { sceneIndex: doc.scenes.length - 1, text: '原來如此' });
  assert.match(first, /<div class="brand">原來如此事務所<\/div>/);
  assert.match(first, /<div class="series">為什麼？<\/div>/);
  assert.doesNotMatch(first, /完整版在長片/);
  assert.match(last, /<div class="more">完整版在長片 ▶<\/div>/);
  assert.match(last, /· 原來如此<\/div>/);
  assert.equal(doc.series, EPISODE_SERIES);
});

test('the channel voice reads each phrase through the narration server, through the lexicon, one WAV each', async () => {
  const requests = [];
  const tone = encodeWav(Int16Array.from({ length: 48_000 }, (_, i) => (i > 4800 && i < 43_200 ? Math.round(8000 * Math.sin(i / 7)) : 0)));
  const fetchImpl = async (url, init) => {
    assert.equal(url, 'https://mokaair.test/api/video/speech');
    assert.equal(new Headers(init.headers).get('authorization'), `Bearer ${TOKEN}`);
    requests.push(JSON.parse(init.body));
    return new Response(tone, { headers: { 'Content-Type': 'audio/wav', 'X-Billable-Characters': '12' } });
  };
  const voice = { provider: 'gemini', name: 'Sulafat', style: '輕鬆' };
  const lexicon = { schema_version: 1, terms: { API: 'A P I' } };
  const result = await serverPhrases({ phrases: ['光先到。', 'API 很快。'], voice, lexicon, site: 'https://mokaair.test', token: TOKEN, fetchImpl, sleep: async () => {} });
  assert.equal(result.wavs.length, 2);
  assert.equal(result.billable, 24);
  assert.deepEqual(requests[0], { voice: 'gemini:Sulafat', style: '輕鬆', segments: [{ parts: [{ text: '光先到。' }], break_after_ms: 0 }] });
  assert.deepEqual(requests[1].segments[0].parts, [{ text: 'API', alias: 'A P I' }, { text: ' 很快。' }]);
  const wav = parseWav(result.wavs[0]);
  assert.equal(wav.sampleRate, 48_000);
  assert.ok(wav.samples.length < 48_000, 'the silence around the phrase is trimmed');
  assert.deepEqual(phraseBody({ provider: 'azure', name: 'zh-TW-HsiaoChenNeural', rate: '+5%' }, '好', lexicon), { voice: 'zh-TW-HsiaoChenNeural', rate: '+5%', segments: [{ parts: [{ text: '好' }], break_after_ms: 0 }] });
});
