// `from-drama` (from-drama.mjs): the span, the captions, the shots and their windows, the crop
// expression, the caption layer and the Short's script as pure functions; then a stand-in
// episode made of lavfi pictures and tones, cut end to end through the CLI against a fake site,
// its windows read back off the picture. Nothing here reaches the live site: locate is answered
// by the fake, and the end-to-end part skips where ffmpeg or Chromium is missing.
import assert from 'node:assert/strict';
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import test from 'node:test';

import { DISSOLVE_FRAMES } from '../assemble/drama.mjs';
import { ToolMissing, locateFfmpeg, runTool } from '../assemble/ffmpeg.mjs';
import { writeSyntheticKeyframes, writeSyntheticNarration } from '../assemble/synthetic.mjs';
import { approve } from '../core/approvals.mjs';
import { buildCues, toSrt } from '../core/captions.mjs';
import { sandbox, tempDir } from '../core/fixtures/load.mjs';
import { eachLine } from '../core/schema.mjs';
import { main } from './cli.mjs';
import { PROFILE, captionHtml, parseSrt, phrasesOf, sha256, validate } from './core.mjs';
import {
  CAPTION_FILES, CENTRE_X, META_KEYS, MOVE_FRAMES, REFRAME_VERSION, SOURCE, WINDOW,
  captionLayerEntries, cropExpr, cropPieces, cueText, cutAudioArgs, dramaCaptionHtml, fromDrama, phraseScenes, pickSubject, readEpisode, reframeArgs, reframeChain,
  seriesOf, shortScript, shortSlugOf, shotLabels, shotSpans, spanCues, spanFrames, windowAt, windowFor, windowX,
} from './from-drama.mjs';
import { CAPTION_BOX } from './karaoke.mjs';
import { themeOf } from './layouts.mjs';
import { captionProblems, packageBuild } from './package.mjs';
import { runQa } from './qa.mjs';
import { CHANNEL_VOICE, siteClient } from './site.mjs';

const TOKEN = `mkv_${'a'.repeat(43)}`;
const SITE = 'https://site.test';
const env = { MOKAAIR_SITE: SITE, MOKAAIR_VIDEO_TOKEN: TOKEN };
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
const video = () => ({
  youtube: { title: '精衛為什麼要填海？', description: '炎帝最小的女兒化成一隻鳥。', tags: ['山海經', 'AI漫劇', 'a,b', 'x'.repeat(31)] },
  characters: [{ id: 'jingwei', name: '精衛' }, { id: 'yandi', name: '炎帝' }],
  scenes: [{ id: 'farewell', template: 'shot', data: { characters: ['jingwei', 'yandi'] } }, { id: 'bird', template: 'shot', data: { characters: [] } }, { id: 'wrap', template: 'outro', data: {} }],
});
const cue = (start, end, text) => ({ start, end, text });
const threeCues = () => [cue(0, 2, '父王，我去看看海就回來'), cue(2, 5, '海不是山，它不會等你'), cue(5, 8, '早點回來')];

// --- the span --------------------------------------------------------------------------------------

test('the span is read in seconds onto the frame grid, inside the episode and inside the Shorts length', () => {
  assert.deepEqual(spanFrames(10, 40, 1500), { startFrame: 300, endFrame: 1200, frames: 900 });
  assert.deepEqual(spanFrames('9.5', '42.5', 1275), { startFrame: 285, endFrame: 1275, frames: 990 }, 'the CLI hands strings in');
  assert.deepEqual(spanFrames(1, 7, 300, { minSeconds: 5, maxSeconds: 60 }), { startFrame: 30, endFrame: 210, frames: 180 }, "the owner's range");
  assert.throws(() => spanFrames(10, 20, 1500), /the span is 10\.00s; a Short is 25–55s/);
  assert.throws(() => spanFrames(10, 70, 3000), /the span is 60\.00s/);
  assert.throws(() => spanFrames(10, 50, 1200), /--to 50 is past the end of the episode \(40 s\)/);
  assert.throws(() => spanFrames(10, 5, 1500), /--to must come after --from/);
  for (const bad of ['x', '', -1, true, undefined, null]) assert.throws(() => spanFrames(bad, 40, 1500), /--from must be a number of seconds/);
  assert.throws(() => spanFrames(10, 'soon', 1500), /--to must be a number of seconds/);
});

test('a caption\'s two lines become one phrase; a break between Latin words keeps its space', () => {
  assert.equal(cueText('很久以前，發鳩山上\n住著炎帝最小的女兒'), '很久以前，發鳩山上住著炎帝最小的女兒');
  assert.equal(cueText('  the sea\n  will not wait '), 'the sea will not wait');
  assert.equal(cueText('GPT-5.5\n跟 Gemini'), 'GPT-5.5跟 Gemini', 'a CJK character after the break takes no space');
  assert.equal(cueText('一句話'), '一句話');
});

test('the captions inside the span move onto the Short\'s clock; one the span cuts in half is refused with better times', () => {
  const cues = [cue(0, 4.4, '很久以前'), cue(9.5, 12.2, '父王，我去\n看看海就回來'), cue(12.2, 15.72, '海不是山'), cue(16.333, 18.893, '那一天'), cue(40, 41.1, '再見')];
  assert.deepEqual(spanCues(cues, 285, 1200), [
    { start: 0, end: 2.7, text: '父王，我去看看海就回來' },
    { start: 2.7, end: 6.233, text: '海不是山' },
    { start: 6.833, end: 9.4, text: '那一天' },
  ], 'on the frame grid, from the span\'s first frame');
  assert.throws(() => spanCues(cues, 300, 1200), /caption 2 \(9\.5–12\.2 s, 「父王，我去看看海就回來」\) is cut by --from: use --from 9\.5 or --from 12\.2, so no phrase is cut in half/);
  assert.throws(() => spanCues(cues, 285, 500), /caption 4 \(16\.333–18\.9 s, 「那一天」\) is cut by --to: use --to 18\.9 or --to 16\.333/);
  assert.deepEqual(spanCues(cues, 600, 1100), [], 'a span with nobody speaking has no phrase');
});

test('the episode\'s scenes inside the span are clipped to it, each knowing the frame to locate on', () => {
  const timeline = { scenes: [{ id: 'opening', template: 'shot', start_frame: 0, end_frame: 285 }, { id: 'farewell', template: 'shot', start_frame: 285, end_frame: 490 }, { id: 'wrap', template: 'outro', start_frame: 490, end_frame: 600 }] };
  assert.deepEqual(shotSpans(timeline, 300, 550), [
    { id: 'farewell', template: 'shot', start: 0, end: 190, picture_frame: 395 },
    { id: 'wrap', template: 'outro', start: 190, end: 250, picture_frame: 520 },
  ]);
  assert.deepEqual(shotSpans(timeline, 0, 285).map((span) => span.id), ['opening']);
  assert.throws(() => shotSpans({ scenes: [{ id: 'a', template: 'shot', start_frame: 0, end_frame: 100 }] }, 50, 150), /does not cover the span/);
  assert.throws(() => shotSpans({ scenes: [{ id: 'a', template: 'shot', start_frame: 0, end_frame: 100 }, { id: 'b', template: 'shot', start_frame: 110, end_frame: 200 }] }, 50, 150), /does not cover the span/);
  assert.throws(() => shotSpans({ scenes: [] }, 0, 10), /does not cover the span/);
});

// --- the window -------------------------------------------------------------------------------------

test('the window centres on the subject\'s box and never leaves the picture', () => {
  assert.deepEqual([WINDOW, SOURCE, CENTRE_X], [{ width: 608, height: 1080 }, { width: 1920, height: 1080 }, 656]);
  assert.equal(windowX(768), 464);
  assert.equal(windowX(10), 0);
  assert.equal(windowX(1900), 1312);
  assert.equal(windowFor([100, 200, 900, 600]), 464, 'a box 0–1000 of the picture, centred');
  assert.equal(windowFor([100, 200, 900, 600], { width: 960, height: 540 }), 464, 'a smaller picture scales to the cut');
  assert.equal(windowFor([0, 0, 1000, 100]), 0);
  assert.equal(windowFor([0, 900, 1000, 1000]), 1312);
});

test('the subject is the first of the shot\'s characters that was found, else the surest box, else nobody', () => {
  const boxes = [{ label: '炎帝', score: 0.8, box: [50, 300, 950, 600] }, { label: ' jingwei ', score: 0.6, box: [100, 0, 900, 240] }];
  assert.deepEqual(pickSubject(boxes, ['Jingwei', '炎帝']), { label: ' jingwei ', score: 0.6, box: [100, 0, 900, 240] }, 'by label, folded');
  assert.deepEqual(pickSubject(boxes, ['夸父']).label, '炎帝', 'nobody named: the surest');
  assert.equal(pickSubject(boxes).label, '炎帝');
  assert.equal(pickSubject([{ label: 'x', box: [1, 2] }, { label: 'y' }], ['x']), null, 'a box without four edges is no box');
  assert.equal(pickSubject([]), null);
  assert.equal(pickSubject(undefined), null);
  assert.deepEqual(pickSubject([{ box: [1, 2, 3, 4] }]), { label: 'subject', score: 0, box: [1, 2, 3, 4] });
});

test('a shot\'s labels are its characters\' names in the script\'s order', () => {
  assert.deepEqual(shotLabels(video(), 'farewell'), ['精衛', '炎帝']);
  assert.deepEqual(shotLabels(video(), 'bird'), []);
  assert.deepEqual(shotLabels({ ...video(), scenes: [{ id: 's', data: { characters: ['jingwei', 'ghost', 'jingwei'] } }] }, 's'), ['精衛', 'ghost'], 'an unknown id is its own label, once');
  assert.deepEqual(shotLabels(null, 'farewell'), [], 'no video.json, no labels');
});

// --- the crop ---------------------------------------------------------------------------------------

test('each shot holds its window and moves to the next one over the last frames before the change', () => {
  assert.equal(MOVE_FRAMES, DISSOLVE_FRAMES);
  const pieces = cropPieces([{ start: 0, end: 60, x: 0 }, { start: 60, end: 120, x: 1312 }, { start: 120, end: 180, x: 656 }, { start: 180, end: 200, x: 656 }]);
  assert.deepEqual(pieces, [
    { from: 0, to: 45, x0: 0, x1: 0 },
    { from: 45, to: 60, x0: 0, x1: 1312 },
    { from: 60, to: 105, x0: 1312, x1: 1312 },
    { from: 105, to: 120, x0: 1312, x1: 656 },
    { from: 120, to: 200, x0: 656, x1: 656 },
  ], 'two scenes with the same window hold together; nothing moves into a card at the same place');
  assert.deepEqual([0, 44, 45, 59, 60, 104, 105, 119, 120, 199, 500].map((n) => windowAt(pieces, n)), [0, 0, 87, 1312, 1312, 1312, 1268, 656, 656, 656, 656], 'the move ends on the next window the frame before the change');
  assert.equal(cropExpr(pieces), "if(lt(n,45),0,if(lt(n,60),0+(1312)*(n-45+1)/15,if(lt(n,105),1312,if(lt(n,120),1312+(-656)*(n-105+1)/15,656))))");
  const short = cropPieces([{ start: 0, end: 10, x: 0 }, { start: 10, end: 20, x: 100 }]);
  assert.deepEqual(short, [{ from: 0, to: 10, x0: 0, x1: 100 }, { from: 10, to: 20, x0: 100, x1: 100 }], 'a shot shorter than the move moves for its whole length');
  assert.deepEqual([windowAt(short, 0), windowAt(short, 9)], [10, 100]);
  assert.deepEqual(cropPieces([{ start: 0, end: 90, x: 300 }]), [{ from: 0, to: 90, x0: 300, x1: 300 }]);
  assert.equal(cropExpr([{ from: 0, to: 90, x0: 300, x1: 300 }]), '300');
  assert.equal(cropExpr([]), '656');
  assert.equal(windowAt([], 5), 656);
});

test('the picture is cut by frame number, cropped as the expression says, scaled to the Shorts frame, the caption layer over it', () => {
  assert.deepEqual(reframeChain(30, 210, '300'), ['trim=start_frame=30:end_frame=210', 'setpts=PTS-STARTPTS', "crop=608:1080:x='300':y=0", 'scale=1080:1920:flags=lanczos']);
  const args = reframeArgs({ final: '/w/final.mp4', startFrame: 30, endFrame: 210, expr: 'if(lt(n,45),0,10)', captionsList: '/s/build/captions.txt', outFile: '/s/build/video.mp4' });
  assert.deepEqual(args.slice(0, 11), ['-y', '-v', 'error', '-i', '/w/final.mp4', '-f', 'concat', '-safe', '0', '-i', '/s/build/captions.txt']);
  const graph = args[args.indexOf('-filter_complex') + 1];
  assert.match(graph, /^\[0:v\]trim=start_frame=30:end_frame=210,setpts=PTS-STARTPTS,crop=608:1080:x='if\(lt\(n,45\),0,10\)':y=0,scale=1080:1920:flags=lanczos\[pic\];\[1:v\]format=rgba\[captions\];\[pic\]\[captions\]overlay=80:1430:eof_action=pass\[captioned\];\[captioned\]format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709\[out\]$/);
  assert.equal(args[args.indexOf('-frames:v') + 1], '180');
  assert.ok(args.includes('-an'), 'no sound in the picture pass');
  for (const flag of ['libx264', '-profile:v', 'high', '-g', '60', '-keyint_min', '60', '-sc_threshold', '0', '+cgop', 'bt709', '-fps_mode', 'cfr']) assert.ok(args.includes(flag), flag);
  assert.equal(args.at(-1), '/s/build/video.mp4');
  assert.ok(!args.join(' ').includes('-ss '), 'never by seeking');
});

test('the sound is the span of the episode\'s mix through loudnorm\'s two passes, without the picture', () => {
  const measure = cutAudioArgs('/w/final.mp4', 9.5, 33, '/s/build/audio.m4a');
  assert.deepEqual(measure.slice(0, 7), ['-hide_banner', '-nostats', '-i', '/w/final.mp4', '-vn', '-af', 'atrim=start=9.500000:end=42.500000,asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-14:TP=-1:LRA=11:print_format=json']);
  assert.deepEqual(measure.slice(-3), ['-f', 'null', '-']);
  const measured = { input_i: '-18.1', input_tp: '-6.2', input_lra: '4.0', input_thresh: '-28.3', target_offset: '0.4' };
  const apply = cutAudioArgs('/w/final.mp4', 9.5, 33, '/s/build/audio.m4a', measured);
  assert.ok(apply.includes('-vn'));
  assert.match(apply[apply.indexOf('-af') + 1], /^atrim=start=9\.500000:end=42\.500000,.*loudnorm=I=-14:TP=-1:LRA=11:measured_I=-18\.1:measured_TP=-6\.2:measured_LRA=4\.0:measured_thresh=-28\.3:offset=0\.4:linear=true,aresample=48000$/);
  for (const flag of ['-ar', '48000', '-ac', '2', '-c:a', 'aac', '-b:a', '192k']) assert.ok(apply.includes(flag), flag);
  assert.equal(apply.at(-1), '/s/build/audio.m4a');
});

// --- the caption layer -------------------------------------------------------------------------------

test('the drama\'s caption layer is the Shorts layer with the bar\'s background on it; nothing in the layout moves', () => {
  const doc = { schema_version: 2, line: 'drama', series: 'jingwei' };
  const options = { lines: ['父王，我去', '看看海就回來'], groups: [{ text: '父王，我去', line: 0 }, { text: '看看海就回來', line: 1 }], active: 1 };
  const plain = captionHtml(doc, options);
  const layer = dramaCaptionHtml(doc, options);
  assert.equal(layer, plain.replace('</style>', `\n.caption{background:${themeOf(doc).colors.caption}}\n</style>`));
  assert.match(layer, /\.caption\{background:#[0-9a-f]{8}\}\n<\/style>/);
  assert.match(layer, /<div class="caption"><div class="words"><span class="g">父王，我去<\/span><br><span class="g on">看看海就回來<\/span><\/div><\/div>/, 'the words are core.mjs\'s');
  assert.match(layer, /\.caption\{position:absolute;left:80px;top:1430px;width:820px;height:165px;/, 'the bar stays where the card puts it');
  assert.equal((layer.match(/<\/style>/g) ?? []).length, 1);
  assert.equal(dramaCaptionHtml(doc, { ...options, active: -1 }).includes(' on"'), false, 'plain captions light nothing');
});

test('the layer\'s list covers the Short exactly: the blank between phrases, each state for its frames', () => {
  const timeline = { frames: 100, cues: [{ index: 0, startFrame: 10, endFrame: 40, frames: 30 }, { index: 1, startFrame: 40, endFrame: 70, frames: 30 }] };
  const phrases = [{ cue: 0, states: [{ group: 0, frames: 12 }, { group: 1, frames: 18 }] }, { cue: 1, states: [{ group: -1, frames: 30 }] }];
  const fileOf = (cue, state) => `${cue}-${state}`;
  assert.deepEqual(captionLayerEntries(timeline, phrases, 'blank', fileOf), [
    { file: 'blank', frames: 10 }, { file: '0-0', frames: 12 }, { file: '0-1', frames: 18 }, { file: '1-0', frames: 30 }, { file: 'blank', frames: 30 },
  ]);
  assert.deepEqual(captionLayerEntries({ frames: 30, cues: [{ index: 0, startFrame: 0, endFrame: 30, frames: 30 }] }, [{ cue: 0, states: [{ group: 0, frames: 30 }] }], 'blank', fileOf), [{ file: '0-0', frames: 30 }], 'a phrase from the first frame to the last needs no blank');
  assert.throws(() => captionLayerEntries(timeline, [{ cue: 0, states: [{ group: 0, frames: 12 }] }, phrases[1]], 'blank', fileOf), /covers 82 frames of a 100-frame Short/);
  assert.throws(() => captionLayerEntries(timeline, [phrases[0]], 'blank', fileOf), /no caption states for phrase 1/);
});

// --- the script -------------------------------------------------------------------------------------

test('the Short is named after the episode and the span, in the series the episode belongs to', () => {
  assert.equal(shortSlugOf('jingwei-fills-the-sea', 285, 1275), 'jingwei-fills-the-sea-short-285-1275');
  const long = shortSlugOf(`${'a'.repeat(70)}-tail`, 285, 1275);
  assert.equal(long.length, 80);
  assert.ok(long.endsWith('-short-285-1275') && !long.includes('--'));
  assert.equal(seriesOf({ series: { slug: 'shanhaijing', episode: 3 } }, 'jingwei-3'), 'shanhaijing');
  assert.equal(seriesOf(null, 'jingwei-3'), 'jingwei-3');
  assert.equal(seriesOf({}, `${'b'.repeat(39)}-c`).length, 39);
});

test('the Short\'s script takes its phrases from the captions and its words from the episode, unless --meta says otherwise', () => {
  const doc = shortScript({ slug: 'jingwei', video: video(), cues: threeCues(), startFrame: 285, endFrame: 1275 });
  assert.deepEqual(validate(doc), []);
  assert.equal(doc.schema_version, 2);
  assert.deepEqual([doc.slug, doc.line, doc.series, doc.format, doc.locale], ['jingwei-short-285-1275', 'drama', 'jingwei', 'shorts', 'zh-TW']);
  assert.deepEqual(doc.titles, ['精衛為什麼要填海？', '父王，我去看看海就回來｜精衛為什麼要填海？']);
  assert.equal(doc.description, '炎帝最小的女兒化成一隻鳥。');
  assert.deepEqual(doc.source, { slug: 'jingwei', start_seconds: 9.5, end_seconds: 42.5 });
  assert.deepEqual(doc.tags, ['山海經', 'AI漫劇'], 'a tag with a comma or over thirty characters is left out');
  assert.deepEqual(phrasesOf(doc), threeCues().map((each) => each.text));
  assert.equal(doc.scenes.length, 3);
  assert.ok(!('headlines' in doc) && !('evidence' in doc));
  const meta = { slug: 'jingwei-hook', series: 'shanhaijing', titles: ['海不會等你', '精衛的第一句話'], description: '一個鉤子。', hashtags: ['山海經'], tags: ['神話'], links: [{ label: '文章', url: 'https://mokaair.com/zh-TW/guides/jingwei' }], headlines: ['父王', '海', '回來'], synthetic_media: true };
  const own = shortScript({ slug: 'jingwei', video: video(), meta, cues: threeCues(), startFrame: 285, endFrame: 1275 });
  assert.deepEqual(validate(own), []);
  assert.deepEqual([own.slug, own.series, own.titles, own.description, own.hashtags, own.tags, own.links, own.synthetic_media], ['jingwei-hook', 'shanhaijing', meta.titles, '一個鉤子。', ['山海經'], ['神話'], meta.links, true]);
  assert.deepEqual(own.scenes.map((scene) => scene.headline), ['父王', '海', '回來']);
  assert.throws(() => shortScript({ slug: 'jingwei', video: video(), meta: { line: 'lab', titles: ['a', 'b'] }, cues: threeCues(), startFrame: 0, endFrame: 900 }), new RegExp(`--meta may set ${META_KEYS.join(', ')}; not line`));
  assert.throws(() => shortScript({ slug: 'jingwei', video: video(), meta: [], cues: threeCues(), startFrame: 0, endFrame: 900 }), /--meta must be a JSON object/);
  assert.throws(() => shortScript({ slug: 'jingwei', video: null, cues: threeCues(), startFrame: 0, endFrame: 900 }), /jingwei has no video\.json in this checkout.*give --meta with titles and description/);
  assert.throws(() => shortScript({ slug: 'jingwei', video: { youtube: {} }, cues: threeCues(), startFrame: 0, endFrame: 900 }), /the episode's video\.json names none/);
  assert.throws(() => shortScript({ slug: 'jingwei', video: video(), cues: threeCues().slice(0, 2), startFrame: 0, endFrame: 900 }), /only 2 captions between --from and --to; a Short needs at least 3 phrases/);
  const many = shortScript({ slug: 'jingwei', video: video(), cues: Array.from({ length: 40 }, (_x, i) => cue(i, i + 1, `第 ${i + 1} 句`)), startFrame: 0, endFrame: 1200 });
  assert.deepEqual(validate(many), []);
  assert.deepEqual(many.scenes.map((scene) => scene.narration.length), [4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3], 'forty phrases in the twelve scenes a Short may have, as even as they divide');
  assert.equal(phrasesOf(many).length, 40);
  const four = shortScript({ slug: 'jingwei', video: video(), cues: [...threeCues(), cue(8, 9, '回來')], startFrame: 0, endFrame: 900 });
  assert.deepEqual(validate(four), []);
  assert.deepEqual(four.scenes.map((scene) => scene.narration.length), [2, 1, 1], 'four phrases still make the three scenes a script needs');
  assert.deepEqual(phraseScenes(threeCues(), ['一', '二']).map((scene) => [scene.headline, scene.narration.length]), [['一', 2], ['二', 1]]);
  assert.throws(() => phraseScenes(threeCues(), ['一', '二', '三', '四']), /3 phrases cannot fill 4 scenes: fewer headlines in --meta/);
});

test('the episode is read with its approved cut, its captions and its timeline as presented after the channel intro', () => {
  const workdir = tempDir('shorts-from-drama-episode-');
  const timeline = { fps: 30, total_frames: 600, scenes: [{ id: 'a', template: 'shot', start_frame: 0, end_frame: 300, states: [{ start_frame: 0, end_frame: 300 }] }, { id: 'b', template: 'outro', start_frame: 300, end_frame: 600, states: [] }], lines: [{ id: 'l1', scene: 'a', start_frame: 0, end_frame: 300 }], chapters: [] };
  assert.throws(() => readEpisode({ slug: 'ep', workdir, root: workdir }), /no final\.mp4 in .*: assemble ep first/);
  writeFileSync(path.join(workdir, 'final.mp4'), 'not a real cut');
  assert.throws(() => readEpisode({ slug: 'ep', workdir, root: workdir }), /no timeline\.json in .*: run tts for ep first/);
  writeFileSync(path.join(workdir, 'timeline.json'), JSON.stringify(timeline));
  assert.throws(() => readEpisode({ slug: 'ep', workdir, root: workdir }), new RegExp(`no zh-TW captions in .* \\(${CAPTION_FILES.join(', ').replace(/[/.]/g, '\\$&')}\\): run captions for ep first`));
  mkdirSync(path.join(workdir, 'upload'));
  writeFileSync(path.join(workdir, 'upload', 'zh-TW.srt'), '1\n00:00:05,000 --> 00:00:07,000\n第一句\n');
  const plain = readEpisode({ slug: 'ep', workdir, root: workdir });
  assert.deepEqual([plain.final, plain.captionFile, plain.video, plain.keyframes, plain.docDir], [path.join(workdir, 'final.mp4'), path.join(workdir, 'upload', 'zh-TW.srt'), null, null, path.join(workdir, 'docs', 'videos', 'ep')]);
  assert.deepEqual(plain.cues, [{ start: 5, end: 7, text: '第一句' }]);
  assert.equal(plain.timeline.total_frames, 600);
  assert.equal(plain.timeline.scenes[0].start_frame, 0);
  mkdirSync(path.join(workdir, 'captions'));
  writeFileSync(path.join(workdir, 'captions', 'zh-TW.srt'), '1\n00:00:10,000 --> 00:00:12,000\n第一句\n');
  writeFileSync(path.join(workdir, 'checks.json'), JSON.stringify({ ok: true, branding: { hash: 'h', intro_frames: 150, outro_frames: 60, body_frames: 600 } }));
  const branded = readEpisode({ slug: 'ep', workdir, root: workdir });
  assert.equal(branded.captionFile, path.join(workdir, 'captions', 'zh-TW.srt'), 'the captions stage\'s file comes first');
  assert.deepEqual(branded.cues, [{ start: 10, end: 12, text: '第一句' }]);
  assert.equal(branded.timeline.total_frames, 810, 'the intro and the outro are in the cut');
  assert.deepEqual(branded.timeline.scenes.map((scene) => [scene.start_frame, scene.end_frame]), [[150, 450], [450, 750]], 'the shots sit after the intro, where the captions already are');
});

test('from-drama needs the episode, the span and a place for the Short', async () => {
  await assert.rejects(main(['from-drama']), /--slug required: the drama episode/);
  await assert.rejects(main(['from-drama', '--slug', 'x', '--from', '1']), /--from and --to required/);
  await assert.rejects(main(['from-drama', '--slug', 'x', '--from', '1', '--to', '2']), /--workdir required/);
});

// --- a stand-in episode, cut end to end -------------------------------------------------------------

/** ffmpeg and a Chromium for Playwright, or the reason this test skips. */
async function toolsOrSkip(t) {
  let tools;
  try {
    tools = await locateFfmpeg();
  } catch (error) {
    if (error instanceof ToolMissing) {
      t.skip(error.message);
      return null;
    }
    throw error;
  }
  try {
    const { chromium } = await import('@playwright/test');
    const browser = await chromium.launch({ headless: true });
    await browser.close();
  } catch (error) {
    t.skip(`no Chromium for Playwright: ${String(error.message).split('\n')[0]}`);
    return null;
  }
  return tools;
}

/**
 * A fake site: the Shorts settings with a wide length range (the fixture is short), the media
 * status with locate, the uploads (kept by hash), and locate's answer by the uploaded picture:
 * `boxesOf(sha256, body)`. Anything else is a 404, as the live site must never be reached.
 */
function fakeSite(boxesOf, settings = { seconds_min: 5, seconds_max: 60 }) {
  const calls = { put: [], locate: [], other: [] };
  const fetchImpl = async (url, init = {}) => {
    const { pathname } = new URL(url);
    const route = `${init.method ?? 'GET'} ${pathname}`;
    if (route === 'GET /api/video/automation/shorts/settings') return json({ voice: CHANNEL_VOICE, locales: [], made_for_kids: false, ...settings });
    if (route === 'GET /api/video/media/status') return json({ enabled: true, limits: { locate_labels: 8, judge_checks: 8 } });
    const put = /^PUT \/api\/video\/media\/files\/([^/]+)\/([a-f0-9]{64})$/.exec(route);
    if (put) {
      calls.put.push({ slug: put[1], sha256: put[2], bytes: init.body.length, query: new URL(url).search });
      return json({ received: [0], complete: true });
    }
    if (route === 'POST /api/video/media/locate') {
      const body = JSON.parse(init.body);
      calls.locate.push(body);
      return json({ boxes: boxesOf(body.sha256, body), width: 1920, height: 1080, model: 'stand-in' });
    }
    calls.other.push(route);
    return json({ code: 'video_media_route_unknown', detail: `no ${route}` }, 404);
  };
  return { fetchImpl, calls };
}

/**
 * The stand-in episode in a throwaway repository: the drama fixture's timeline and tones (as the
 * tts stage leaves them), its captions as the captions stage writes them, a keyframe for every
 * shot but the storm, and a final.mp4 whose every frame is a luma ramp from black at the left
 * edge to white at the right, so where the Short's window sat can be read off its brightness.
 */
async function standInEpisode(tools) {
  const sand = sandbox('fixture-drama', 'drama');
  const doc = JSON.parse(readFileSync(path.join(sand.dir, 'video.json'), 'utf8'));
  const lexicon = JSON.parse(readFileSync(path.join(sand.videos, 'lexicon.json'), 'utf8'));
  mkdirSync(sand.workdir, { recursive: true });
  const timeline = writeSyntheticNarration(doc, lexicon, sand.workdir);
  const texts = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, line.text]));
  const { cues } = buildCues(timeline, texts, 'zh-TW');
  mkdirSync(path.join(sand.workdir, 'captions'));
  writeFileSync(path.join(sand.workdir, 'captions', 'zh-TW.srt'), toSrt(cues));
  const keyframes = writeSyntheticKeyframes(doc, sand.workdir, tools.ffmpeg);
  delete keyframes.shots['sea-storm'];
  writeFileSync(path.join(sand.workdir, 'keyframes', 'manifest.json'), JSON.stringify(keyframes));
  const ramp = path.join(sand.base, 'ramp.png');
  await runTool(tools.ffmpeg, ['-y', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=gray:s=1920x1080:r=30', '-vf', "format=gray,geq=lum='255*X/W'", '-frames:v', '1', ramp]);
  await runTool(tools.ffmpeg, ['-y', '-v', 'error', '-loop', '1', '-framerate', '30', '-t', (timeline.total_frames / 30).toFixed(6), '-i', ramp, '-i', path.join(sand.workdir, 'narration.wav'), '-vf', 'format=yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-ac', '2', '-ar', '48000', '-frames:v', String(timeline.total_frames), path.join(sand.workdir, 'final.mp4')]);
  return { sand, doc, timeline, cues, keyframes };
}

/**
 * The mean brightness of every frame of a cut above the caption bar, by frame number. ffmpeg runs
 * in the stats file's directory and the filter graph names the file alone: a Windows temp path's
 * drive colon and backslashes would read as option separators and escapes inside the graph.
 */
async function brightness(tools, file, stats) {
  const graph = `crop=1080:${CAPTION_BOX.y - 30}:0:0,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=${path.basename(stats)}`;
  await runTool(tools.ffmpeg, ['-hide_banner', '-nostats', '-v', 'error', '-i', path.resolve(file), '-vf', graph, '-f', 'null', '-'], { cwd: path.dirname(stats) });
  const levels = [];
  let frame = null;
  for (const line of readFileSync(stats, 'utf8').split('\n')) {
    const at = /^frame:(\d+)/.exec(line);
    if (at) frame = Number(at[1]);
    const value = /lavfi\.signalstats\.YAVG=([\d.]+)/.exec(line);
    if (value && frame !== null) levels[frame] = Number(value[1]);
  }
  return levels;
}
// The ramp's brightness over a window at x: its middle column, in the cut's limited range.
const rampLevel = (x) => 16 + (219 * (x + WINDOW.width / 2)) / SOURCE.width;
const buildDirs = (base, slug) => (existsSync(path.join(base, slug)) ? readdirSync(path.join(base, slug)).map((name) => path.join(base, slug, name)) : []);

test('the brightness probe reads a stats file whose path has a drive colon and backslashes, as a Windows temp path does', async (t) => {
  let tools;
  try {
    tools = await locateFfmpeg();
  } catch (error) {
    if (error instanceof ToolMissing) return t.skip(error.message);
    throw error;
  }
  const base = tempDir('brightness-path-');
  t.after(() => rmSync(base, { recursive: true, force: true }));
  // A directory named like a Windows path: legal on Linux, and the characters the filter graph
  // would read as an option separator and escapes if the path were written into it.
  const directory = path.join(base, 'C:\\Users\\runner\\AppData');
  mkdirSync(directory, { recursive: true });
  const video = path.join(base, 'grey.mp4');
  await runTool(tools.ffmpeg, ['-hide_banner', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=gray:s=1080x1920:r=30:d=0.2', '-pix_fmt', 'yuv420p', video]);
  const levels = await brightness(tools, video, path.join(directory, 'brightness.txt'));
  assert.equal(levels.length, 6, 'one level per frame');
  for (const level of levels) assert.ok(level > 100 && level < 150, `mid grey, not ${level}`);
});

test('a stand-in episode is cut to a Short whose window follows the located subjects and whose captions are the Shorts layer', async (t) => {
  const tools = await toolsOrSkip(t);
  if (!tools) return;
  const { sand, timeline, keyframes } = await standInEpisode(tools);
  const scenes = Object.fromEntries(timeline.scenes.map((scene) => [scene.id, scene]));
  const farewell = keyframes.shots.farewell.sha256;
  const bird = keyframes.shots.bird.sha256;
  // The farewell's keyframe shows both characters, the girl at the left edge; the storm has no
  // keyframe here, so its frame is pulled out of the cut and answered with a figure at the
  // right; the bird's keyframe shows nobody, so the window stays in the middle.
  const site = fakeSite((sha256) => {
    if (sha256 === farewell) return [{ label: '炎帝', box: [50, 300, 950, 600], score: 0.8 }, { label: '精衛', box: [100, 0, 900, 240], score: 0.9 }];
    if (sha256 === bird) return [];
    return [{ label: 'subject', box: [100, 760, 900, 1000], score: 0.5 }];
  });
  const run = (args, options = {}) => main(['from-drama', '--slug', 'fixture-drama', '--workdir', sand.work, '--episode-workdir', sand.work, ...args], { env, home: sand.base, fetch: site.fetchImpl, root: sand.root, ...options });
  const from = String(scenes.farewell.start_frame / 30);
  const to = String(scenes.wrap.end_frame / 30);
  const slug = `fixture-drama-short-${scenes.farewell.start_frame}-${scenes.wrap.end_frame}`;

  // Nothing is cut from a cut nobody approved.
  await assert.rejects(run(['--from', from, '--to', to]), /the final cut of fixture-drama is not approved \(.*final\.mp4\): run review-pull, or approve --gate final/);
  assert.deepEqual([site.calls.put.length, site.calls.locate.length], [0, 0]);
  await approve({ gate: 'final', docDir: sand.dir, workdir: sand.workdir, note: 'test' });
  // A span that cuts a phrase in half, or is not a Short's length, stops before any call.
  await assert.rejects(run(['--from', '10', '--to', to]), /caption 3 \(9\.5–12\.2 s, 「父王，我去看看海就回來」\) is cut by --from: use --from 9\.5 or --from 12\.2/);
  await assert.rejects(run(['--from', from, '--to', '12.2']), /the span is 2\.70s; a Short is 5–60s/);
  assert.deepEqual([site.calls.put.length, site.calls.locate.length, buildDirs(sand.work, slug)], [0, 0, []]);

  const code = await run(['--from', from, '--to', to, '--captions', 'karaoke']);
  assert.equal(code, 0);
  const [directory] = buildDirs(sand.work, slug);
  assert.ok(directory, 'a build directory under the Short\'s slug');
  const checks = JSON.parse(readFileSync(path.join(directory, 'checks.json'), 'utf8'));
  const short = JSON.parse(readFileSync(path.join(directory, 'timeline.json'), 'utf8'));
  const doc = JSON.parse(readFileSync(path.join(directory, 'script.json'), 'utf8'));
  const frames = scenes.wrap.end_frame - scenes.farewell.start_frame;

  // The script: the episode's words, the captions as the phrases, the span it was cut from.
  assert.deepEqual(validate(doc), []);
  assert.deepEqual([doc.slug, doc.line, doc.series, doc.source], [slug, 'drama', 'fixture-drama', { slug: 'fixture-drama', start_seconds: 9.5, end_seconds: 42.5 }]);
  assert.equal(doc.titles[0], '精衛為什麼要填海？山海經最倔強的一隻鳥');
  assert.deepEqual(doc.tags, ['山海經', '精衛填海', 'AI漫劇']);
  assert.equal(phrasesOf(doc).length, 8);
  assert.equal(phrasesOf(doc)[0], '父王，我去看看海就回來');
  assert.equal(phrasesOf(doc)[6], '這就是精衛填海的故事。她填不平大海，但她從來沒有停下來', 'the two lines of a drama cue are one phrase');

  // The cut: the Shorts profile, exactly the span's frames, the captions on its clock.
  assert.deepEqual([checks.video.width, checks.video.height, checks.video.fps, checks.frames, short.frames, short.cues.length], [1080, 1920, '30/1', frames, frames, 8]);
  assert.equal(short.cues[0].startFrame, 0);
  assert.equal(short.cues[3].startFrame, 573 - scenes.farewell.start_frame, 'the fourth phrase starts at 19.1 s of the episode');
  assert.deepEqual(captionProblems(readFileSync(path.join(directory, 'upload', 'zh-TW.srt'), 'utf8'), short), []);
  assert.deepEqual(checks.profile, PROFILE);
  assert.deepEqual(checks.range, { minSeconds: 5, maxSeconds: 60 });
  assert.ok(Math.abs(Number(checks.loudness.input_i) + 14) <= 1, `the cut is brought to −14 LUFS: ${checks.loudness.input_i}`);

  // One locate call a shot, the picture uploaded under the episode, the characters as labels.
  assert.equal(site.calls.other.length, 0, 'nothing but the settings, the status, the uploads and locate');
  assert.deepEqual(site.calls.put.map((call) => call.slug), ['fixture-drama', 'fixture-drama', 'fixture-drama']);
  assert.ok(site.calls.put.every((call) => call.query.startsWith('?part=0&parts=1&size=')));
  assert.deepEqual(site.calls.locate.map((call) => call.labels ?? null), [['精衛', '炎帝'], ['精衛'], null]);
  assert.deepEqual(site.calls.locate.map((call) => call.sha256), [farewell, site.calls.put[1].sha256, bird]);
  assert.deepEqual(checks.reframe.locate, { calls: 3, model: 'stand-in' });
  assert.equal(checks.reframe.version, REFRAME_VERSION);
  assert.deepEqual(checks.reframe.window, WINDOW);
  assert.deepEqual(checks.reframe.source, { slug: 'fixture-drama', final_sha256: sha256(readFileSync(path.join(sand.workdir, 'final.mp4'))), start_frame: scenes.farewell.start_frame, end_frame: scenes.wrap.end_frame, width: 1920, height: 1080 });
  const shots = checks.reframe.shots;
  assert.deepEqual(shots.map((shot) => [shot.shot, shot.template, shot.picture, shot.x, shot.subject?.label ?? null]), [
    ['farewell', 'shot', 'keyframe', 0, '精衛'],
    ['sea-storm', 'shot', 'frame', 1312, 'subject'],
    ['bird', 'shot', 'keyframe', 656, null],
    ['wrap', 'outro', 'card', 656, null],
  ], 'the girl at the left edge, the figure at the right, nobody in the middle, the card in the middle');
  assert.equal(shots[1].frame, scenes['sea-storm'].start_frame + Math.floor((scenes['sea-storm'].end_frame - scenes['sea-storm'].start_frame) / 2), 'the storm\'s frame is pulled from the middle of the shot');
  assert.ok(existsSync(path.join(directory, 'build', 'frame-sea-storm.png')));
  assert.deepEqual(shots.map((shot) => [shot.start, shot.end]), [[0, 205], [205, 362], [362, 610], [610, 990]]);
  const pieces = checks.reframe.pieces;
  assert.deepEqual(pieces, [
    { from: 0, to: 190, x0: 0, x1: 0 }, { from: 190, to: 205, x0: 0, x1: 1312 },
    { from: 205, to: 347, x0: 1312, x1: 1312 }, { from: 347, to: 362, x0: 1312, x1: 656 },
    { from: 362, to: 990, x0: 656, x1: 656 },
  ], 'two moves of fifteen frames before the cuts; none into the card');

  // The picture itself: the window read off the ramp's brightness, frame by frame.
  const levels = await brightness(tools, path.join(directory, 'upload', 'final.mp4'), path.join(sand.base, 'brightness.txt'));
  assert.equal(levels.length, frames);
  for (const n of [0, 100, 189, 190, 197, 204, 205, 300, 346, 347, 354, 361, 362, 500, 609, 610, 800, 989]) {
    const expected = rampLevel(windowAt(pieces, n));
    assert.ok(Math.abs(levels[n] - expected) <= 3, `frame ${n}: window ${windowAt(pieces, n)} reads ${expected.toFixed(1)}, the cut shows ${levels[n]}`);
  }

  // The caption layer: karaoke states from estimated timing, one picture a state, measured.
  assert.deepEqual([checks.captions.style, checks.captions.source], ['karaoke', 'estimated']);
  const timing = JSON.parse(readFileSync(path.join(directory, 'timing.json'), 'utf8'));
  assert.equal(timing.phrases.length, 8);
  assert.deepEqual(checks.layout, short.cues.map((each) => ({ cue: each.index, problems: [] })));
  const pictures = readdirSync(path.join(directory, 'captions')).filter((name) => name.endsWith('.png'));
  assert.equal(pictures.length, checks.captions.states + 1, 'every state and the blank');
  assert.ok(pictures.includes('blank.png'));
  const list = readFileSync(path.join(directory, 'build', 'captions.txt'), 'utf8');
  assert.match(list, /^ffconcat version 1\.0\n/);
  assert.ok(list.includes("/captions/blank.png'"), 'the blank sits where nobody speaks');
  assert.equal(readdirSync(path.join(directory, 'audio')).length, 8, 'a clip a phrase for the listener\'s check');
  assert.equal(checks.ok, true);
  assert.equal(checks.imported, undefined);

  // The usage: nothing synthesized, nothing under stages that the site would price.
  assert.deepEqual(JSON.parse(readFileSync(path.join(directory, 'usage.json'), 'utf8')), { narration: { seconds: 0, characters: 0, calls: 0, provider: 'episode' }, stages: {}, checks: {} });
  const manifest = JSON.parse(readFileSync(path.join(directory, 'upload', 'manifest.json'), 'utf8'));
  assert.deepEqual([manifest.status, manifest.line, manifest.narrator, manifest.reframe, manifest.source.slug], ['built', 'drama', { source: 'episode', provider: 'episode', voice: null }, REFRAME_VERSION, 'fixture-drama']);
  assert.equal(manifest.files.find((file) => file.name === 'final.mp4').sha256, checks.final_sha256);
  for (const name of ['final.mp4', 'zh-TW.srt', 'cover.png', 'titles.json']) assert.ok(existsSync(path.join(directory, 'upload', name)), name);

  // The quality check takes the build as any other: the cut, its loudness, its layout and its
  // captions pass without the site; what needs the site fails saying so.
  const report = await runQa({ directory, offline: true });
  const verdicts = Object.fromEntries(report.items.map((each) => [each.id, each]));
  assert.deepEqual(report.items.filter((each) => each.ok).map((each) => each.id), ['profile', 'loudness', 'layout', 'captions', 'disclosure']);
  assert.match(verdicts.layout.detail, /8 cards inside the safe area/);
  assert.match(verdicts.narration.detail, /run check-audio/);
  assert.match(verdicts.evidence.detail, /without the site/);
  assert.match(verdicts.captions.warnings[0], /estimated timing/);
  assert.match(verdicts.disclosure.detail, /disclosed as altered or synthetic content/);
  assert.equal(report.line, 'drama');
  const { metadata, report: packaged } = packageBuild({ directory, source: { youtube_video_id: 'dQw4w9WgXcQ' } });
  assert.ok(packaged.items.every((each) => each.ok), JSON.stringify(packaged.items));
  assert.deepEqual([metadata.category_id, metadata.contains_synthetic_media, metadata.source.url], ['24', true, 'https://youtu.be/dQw4w9WgXcQ']);
  assert.match(metadata.description, /^完整影片：https:\/\/youtu\.be\/dQw4w9WgXcQ\n/);

  // Plain captions: the same layer with nothing lit, one state a phrase, no timing file.
  const plainSite = fakeSite(() => []);
  const client = siteClient({ env, home: sand.base, fetch: plainSite.fetchImpl });
  const plain = await fromDrama({ slug: 'fixture-drama', from: scenes['sea-storm'].start_frame / 30, to: scenes.bird.end_frame / 30, workdir: sand.work, episodeWorkdir: sand.work, captions: 'plain', client, root: sand.root, env, home: sand.base });
  assert.deepEqual([plain.status, plain.phrases, plain.shots, plain.locate], ['built', 4, 2, { calls: 2, model: 'stand-in' }]);
  const plainChecks = JSON.parse(readFileSync(path.join(plain.directory, 'checks.json'), 'utf8'));
  assert.deepEqual(plainChecks.captions, { style: 'plain' });
  assert.ok(!existsSync(path.join(plain.directory, 'timing.json')));
  assert.deepEqual(plainChecks.reframe.shots.map((shot) => shot.x), [656, 656], 'nobody found: the middle');
  assert.deepEqual(plainChecks.reframe.pieces, [{ from: 0, to: 405, x0: 656, x1: 656 }]);
  assert.equal(readdirSync(path.join(plain.directory, 'captions')).filter((name) => /^\d{3}-\d{2}\.png$/.test(name)).length, 4);
  assert.deepEqual(plainChecks.layout.map((entry) => entry.problems), [[], [], [], []]);
  assert.equal(plainChecks.frames, 405);
});
