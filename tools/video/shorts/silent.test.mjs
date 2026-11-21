// A silent drama (docs/videos/shorts-drama/): a vertical comedy with no dialogue, no narration
// and no captions, made whole by its own pipeline and cut from no video. It goes through import,
// check-audio, qa, package and push like any other Short, held to what it is.
import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { checkAudio, CHECK_FILE } from './check.mjs';
import { SILENT_RANGE, isSilent, phrasesOf, sha256, validate } from './core.mjs';
import { importShort, silentScriptFromImport } from './import.mjs';
import { captionLocales, composeMetadata, packageBuild, packageItems } from './package.mjs';
import { push } from './push.mjs';
import { ITEM_IDS, profileItem, runQa, scriptShape, silentCaptionsItem, silentGrammarItem } from './qa.mjs';

const temp = (t, prefix) => {
  const dir = mkdtempSync(path.join(os.tmpdir(), prefix));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
};
const META = Object.freeze({
  slug: 'shechu-hell-e06',
  line: 'drama',
  silent: true,
  series: 'shechu-hell',
  titles: ['請貓老闆在文件上蓋個章，結果… #社畜地獄', '喵總的印章，是貓掌 #社畜地獄'],
  description: '員工是狗，老闆是貓。阿金只是想請喵總在文件上蓋個章。\nEP6｜社畜地獄\n本片畫面、配樂由 AI 生成。',
  hashtags: ['#社畜地獄', '#AI短劇'],
  tags: ['社畜地獄', '零台詞'],
  localizations: {
    en: { title: 'I asked the cat boss to stamp one document… #OfficeHell', description: 'The employees are dogs; the boss is a cat.' },
    th: { title: 'ขอให้บอสแมวประทับตราเอกสารแค่แผ่นเดียว… #นรกออฟฟิศ', description: 'พนักงานเป็นหมา บอสเป็นแมว' },
  },
});
const script = (changes = {}) => ({ schema_version: 2, format: 'shorts', locale: 'zh-TW', ...META, ...changes });
// 10.8 seconds on the 30 fps grid, as shechu-hell-e06 is.
const FRAMES = 324;
const measured = (changes = {}) => ({
  video: { width: 1080, height: 1920, codec_name: 'h264', r_frame_rate: '30/1', nb_frames: String(FRAMES), duration: '10.800000', ...changes.video },
  audio: { codec_name: 'aac', sample_rate: '48000', duration: '10.80', ...changes.audio },
  loudness: { input_i: '-14.10', input_tp: '-1.40' },
});
// Stand-ins that cannot run: a silent import that brings its cover calls neither.
const NO_TOOLS = { ffmpeg: path.join(os.tmpdir(), 'no-ffmpeg'), ffprobe: path.join(os.tmpdir(), 'no-ffprobe') };

function importDirectory(t, { meta = META, captions = null, cover = true } = {}) {
  const from = temp(t, 'shorts-silent-from-');
  writeFileSync(path.join(from, 'final.mp4'), 'a silent drama of 10.8 seconds');
  writeFileSync(path.join(from, 'meta.json'), JSON.stringify(meta));
  if (cover) writeFileSync(path.join(from, 'cover.png'), 'the frame its maker chose');
  if (captions !== null) writeFileSync(path.join(from, 'zh-TW.srt'), captions);
  return from;
}

test('a silent drama is a drama-line Short that says nothing, of its own length, cut from no video', () => {
  assert.deepEqual(validate(script()), []);
  assert.equal(isSilent(script()), true);
  assert.deepEqual(phrasesOf(script()), []);
  assert.deepEqual(SILENT_RANGE, { minSeconds: 9, maxSeconds: 20 });
  assert.deepEqual(validate(script({ source: { slug: 'shechu-hell' } })), [], 'it may still name a video it came from');
  assert.ok(validate(script({ source: { slug: 'Not A Slug' } })).includes('source.slug required'));
  assert.ok(validate(script({ line: 'cut', source: { slug: 'x' } })).some((e) => e.startsWith('silent is true')), 'only a drama is silent');
  assert.ok(validate(script({ silent: false })).some((e) => e.startsWith('silent is true')));
  assert.ok(validate(script({ scenes: [{ headline: '蓋章', narration: ['喵總蓋章'] }] })).some((e) => e.includes('no scenes')));
  assert.deepEqual(validate(script({ scenes: [] })), []);
  assert.ok(validate(script({ music: { track: 'bed.mp3' } })).some((e) => e.includes('own pipeline')));
  assert.ok(validate(script({ localizations: { fr: { title: 'x', description: 'y' } } })).some((e) => e.includes('localizations.fr')));
  assert.ok(validate(script({ localizations: { en: { title: 'x'.repeat(101), description: 'y' } } })).some((e) => e.includes('localizations.en: a title')));
  assert.ok(validate(script({ localizations: { ja: { title: 'x', description: '' } } })).some((e) => e.includes('localizations.ja: a description')));
  const { silent: _silent, ...talking } = script();
  assert.ok(validate(talking).includes('source.slug required'), 'a drama that talks is still cut from a video');
  assert.deepEqual(scriptShape(script()), { opening: '', structure: '' }, 'variety compares it on nothing it does not have');
});

test('the import takes final.mp4, meta.json and the chosen cover, and writes no captions', async (t) => {
  const from = importDirectory(t);
  const workdir = temp(t, 'shorts-silent-work-');
  const result = await importShort({ from, workdir, tools: NO_TOOLS, measureImpl: async () => measured(), now: () => new Date('2026-11-21T12:00:00Z') });
  assert.deepEqual([result.status, result.phrases, result.silent, result.seconds], ['imported', 0, true, 10.8]);
  const { directory } = result;
  const doc = JSON.parse(readFileSync(path.join(directory, 'script.json'), 'utf8'));
  assert.deepEqual(doc, silentScriptFromImport(META));
  assert.equal('scenes' in doc, false);
  assert.deepEqual(JSON.parse(readFileSync(path.join(directory, 'timeline.json'), 'utf8')), { fps: 30, frames: FRAMES, seconds: 10.8, cues: [] });
  assert.equal(readFileSync(path.join(directory, 'upload', 'cover.png'), 'utf8'), 'the frame its maker chose');
  assert.equal(existsSync(path.join(directory, 'upload', 'zh-TW.srt')), false);
  const manifest = JSON.parse(readFileSync(path.join(directory, 'upload', 'manifest.json'), 'utf8'));
  assert.deepEqual(manifest.files.map((file) => file.name), ['final.mp4', 'cover.png', 'titles.json']);
  // Without a cover, the first frame is taken: the stand-in ffmpeg is called and fails.
  await assert.rejects(importShort({ from: importDirectory(t, { cover: false }), workdir, tools: NO_TOOLS, measureImpl: async () => measured() }), /no-ffmpeg failed/);
});

test('the import refuses what contradicts a silent drama, and a talking cut without captions', async (t) => {
  const workdir = temp(t, 'shorts-silent-work-');
  const run = (options) => importShort({ from: importDirectory(t, options), workdir, tools: NO_TOOLS, measureImpl: async () => measured() });
  await assert.rejects(run({ captions: '1\n00:00:00,000 --> 00:00:01,000\n喵\n' }), /holds zh-TW\.srt, but meta\.json says the drama is silent/);
  await assert.rejects(run({ meta: { ...META, scenes: [], music: { track: 'bed.mp3' } } }), /does not make the script of a silent drama:\n.*mixed by its own pipeline/);
  const { silent: _silent, ...talking } = META;
  await assert.rejects(run({ meta: talking }), /has no zh-TW\.srt \(a silent drama says "silent": true/);
  await assert.rejects(run({ meta: talking, captions: '' }), /holds no caption/);
  await assert.rejects(run({ meta: talking, captions: '﻿\r\n' }), /holds no caption/);
});

test('a silent drama goes through check-audio, qa, package and push with nothing said', async (t) => {
  const from = importDirectory(t);
  const workdir = temp(t, 'shorts-silent-work-');
  const { directory } = await importShort({ from, workdir, tools: NO_TOOLS, measureImpl: async () => measured() });

  // check-audio: nothing to hear, nothing sent.
  const check = await checkAudio({ directory, client: null, transcribeImpl: () => assert.fail('nothing is transcribed'), judgeImpl: () => assert.fail('nothing is judged') });
  assert.deepEqual([check.ok, check.silent, check.lines, check.transcribe_calls, check.judge_calls], [true, true, 0, 0, 0]);
  assert.ok(existsSync(path.join(directory, CHECK_FILE)));
  assert.equal(existsSync(path.join(directory, '.speech-journal')), false);

  // qa: the owner's narrated-Shorts range (13 s) and ticked caption languages do not apply.
  const asked = [];
  const client = {
    settings: async () => ({ seconds_min: 13, seconds_max: 55, locales: ['en', 'ja'], made_for_kids: false }),
    judgePolicy: async (body) => (asked.push(body), { passed: true, note: 'Fine for the channel.' }),
    project: async () => assert.fail('a silent drama names no source'),
  };
  const grammar = { cover_psnr: 18.2, loop_psnr: 21.5 };
  const report = await runQa({ directory, client, tools: NO_TOOLS, measureImpl: async () => ({ ...measured(), grammar }), linkCheck: async () => ({ ok: true }), history: [] });
  const by = Object.fromEntries(report.items.map((each) => [each.id, each]));
  assert.deepEqual(report.items.map((each) => each.id), [...ITEM_IDS]);
  assert.deepEqual(report.items.filter((each) => !each.ok).map((each) => each.id), ['layout'], 'only the safe area waits for the owner\'s look, as for any import');
  assert.match(by.profile.detail, /10\.80s, 324 frames/);
  assert.match(by.narration.detail, /no narration, only music and sound effects/);
  assert.match(by.evidence.detail, /cut from no video/);
  assert.match(by.facts.detail, /makes no claim/);
  assert.match(by.captions.detail, /no captions, nothing is said/);
  assert.match(by.disclosure.detail, /零台詞短劇/);
  assert.deepEqual(by.grammar.warnings.length, 2, 'the chosen cover and the story loop are recorded, not failed');
  assert.equal(asked[0].script, [...META.titles, META.description].join('\n'), 'Jev reads what a viewer reads: the titles and description');

  // profile: 9 to 20 seconds, whatever the settings say (10.8 s passed above against a 13 s minimum).
  assert.match(profileItem({ measured: measured({ video: { nb_frames: '630' }, audio: { duration: '21.00' } }), frames: 630, range: SILENT_RANGE }).detail, /21\.00s is outside 9–20s/);

  // package: no caption file, the eight-language titles carried, the captions tag's signal set.
  const { metadata, report: packaged } = packageBuild({ directory, settings: { locales: ['en', 'ja'], made_for_kids: false } });
  assert.equal(packaged.ok, true, JSON.stringify(packaged.items));
  assert.deepEqual([metadata.silent, metadata.locales, metadata.category_id, metadata.contains_synthetic_media, metadata.source], [true, [], '24', true, null]);
  assert.deepEqual(metadata.captions_sha256, {});
  assert.deepEqual(Object.keys(metadata.localizations), ['en', 'th']);
  assert.match(packaged.items[0].detail, /^final\.mp4, cover\.png, metadata\.json; final\.mp4 is the checked cut/);
  assert.equal(packaged.items[2].detail, 'a silent drama: no captions, nothing is said');

  // push: a drama-line Short, no caption uploaded, sent by hand so the owner decides both gates.
  const calls = [];
  const site = {
    report: async (slug, body) => (calls.push(['report', slug, body]), {}),
    part: async (_slug, digest, bytes, query) => (calls.push(['part', digest]), { complete: Number(query.part) === Number(query.parts) - 1 }),
    submit: async (slug, review) => (calls.push(['submit', slug, review]), { id: `${review.gate}-review`, gate: review.gate, status: 'approved', payload: structuredClone(review.payload) }),
  };
  const sent = await push({ directory, client: site, handPushed: true });
  assert.equal(sent.waits, null);
  const body = calls.find(([kind]) => kind === 'report')[2];
  assert.deepEqual([body.format, body.shorts_line, body.shorts_series, 'source_slug' in body], ['drama', 'drama', 'shechu-hell', false]);
  const [final, publish] = calls.filter(([kind]) => kind === 'submit').map(([, , review]) => review);
  assert.deepEqual(final.files.map((file) => file.role), ['preview', 'thumbnail']);
  assert.equal(final.payload.hand_pushed, true);
  assert.deepEqual(publish.files.map((file) => file.role), ['metadata', 'final', 'description_zh-TW'], 'no caption track goes');
  assert.deepEqual(publish.payload.locales, []);
  assert.equal(publish.payload.disclosure.synthetic, true);
  assert.equal(sha256(readFileSync(path.join(directory, 'upload', 'metadata.json'))), publish.content_sha256);
});

test('a caption file left in a silent drama\'s package is named, not ignored', () => {
  const metadata = composeMetadata({ doc: script(), finalSha256: 'f'.repeat(64), seconds: 10.8, settings: { locales: ['en'] } });
  assert.deepEqual(captionLocales(metadata), []);
  const files = new Map([['final.mp4', Buffer.from('x')], ['cover.png', Buffer.from('c')], ['metadata.json', Buffer.from('{}')], ['description.zh-TW.txt', Buffer.from(metadata.description)], ['zh-TW.srt', Buffer.from('1\n00:00:00,000 --> 00:00:01,000\n喵\n')]]);
  const items = packageItems({ files, metadata, timeline: { fps: 30, cues: [] }, qa: null });
  assert.equal(items[2].ok, false);
  assert.match(items[2].detail, /zh-TW\.srt is in the package of a silent drama/);
  const caption = silentCaptionsItem({ captions: new Map([['en', 'x']]), timeline: { cues: [{}] } });
  assert.equal(caption.ok, false);
  assert.match(caption.detail, /en\.srt is there.*; the timeline has 1 cues/);
  const asking = silentGrammarItem({ doc: script({ localizations: { en: { title: 'Like and subscribe', description: 'x' } } }), grammar: null });
  assert.deepEqual([asking.ok, asking.warnings], [false, undefined]);
  assert.match(asking.detail, /the en title asks the viewer to act/);
  assert.equal(silentGrammarItem({ doc: script(), grammar: { cover_psnr: Infinity, loop_psnr: 40 } }).warnings, undefined);
});
