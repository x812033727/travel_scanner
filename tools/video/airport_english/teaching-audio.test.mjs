import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { emptyLexicon } from '../core/lexicon.mjs';
import { textHash } from '../core/schema.mjs';
import { encodeWav } from '../tts/wav.mjs';
import { planTeachingAudio, passedCurrentCheck, teachingWindows, tempoForWindow, teachingCaptions, synthesizeTeachingClips, checkMixedLines, validateTeachingManifest, requireCurrentTeachingPlan, TEACHING_ARTIFACTS, TEACHING_SCHEMA } from './teaching-audio.mjs';

const hash = (value) => createHash('sha256').update(Buffer.isBuffer(value) ? value : JSON.stringify(value)).digest('hex');
function fixture() {
  const lines = [{ id: 'coac0001', text: 'Listen for the gate number.' }, { id: 'dial0001', text: 'Your gate is B thirty-two.' }, { id: 'rept0001', text: 'Your gate is B thirty-two.', audio_ref: 'dial0001' }];
  const doc = { schema_version: 1, slug: 'airport-english-test', format: 'slides', narration_locale: 'en', voice: { provider: 'gemini', name: 'Sulafat', model: 'gemini-3.8-flash-tts', style: 'Natural English.' }, scenes: lines.map((line, index) => ({ id: `s${index}`, data: { source: index ? 'Staff' : 'Airport English' }, lines: [line] })) };
  const translated = ['搭乗ゲート番号を聞き取りましょう。', '搭乗ゲートはB32です。', '搭乗ゲートはB32です。'];
  const entries = lines.map((line, index) => ({ id: line.id, kind: index ? 'dialogue' : 'coach', text: index ? line.text : translated[index], speech_locale: index ? 'en' : 'ja', ...(index ? { reuse_source_take: 'dial0001' } : {}), cc_text: translated[index] }));
  const specification = { schema_version: 1, source_locale: 'en', source_script_sha256: hash(doc), locales: { ja: { lines: entries } } };
  const project = { doc, lexicon: emptyLexicon(), shelfLexicon: emptyLexicon(), translations: { ja: { lines: Object.fromEntries(lines.map((line, index) => [line.id, { text: translated[index], source_hash: textHash(line.text) }])) } } };
  const timeline = { fps: 30, sample_rate: 48000, total_frames: 300,
    lines: lines.map((line, index) => ({ id: line.id, scene: `s${index}`, start_frame: index * 90, end_frame: (index + 1) * 90, audio_samples: 48000 })),
    scenes: lines.map((line, index) => ({ id: `s${index}`, states: [{ start_frame: index * 90, end_frame: (index + 1) * 90 }] })) };
  return { project, specification, timeline, locale: 'ja' };
}
function temporary(t) { const directory = mkdtempSync(path.join(tmpdir(), 'airport-teaching-test-')); t.after(() => rmSync(directory, { recursive: true, force: true })); return directory; }
const tone = (frequency = 220) => Int16Array.from({ length: 48000 }, (_, index) => Math.round(4000 * Math.sin(2 * Math.PI * frequency * index / 48000)));

test('mixed planner requests only translated coaching and retains distinct English speech / Japanese CC', () => {
  const input = fixture(), plan = planTeachingAudio(input);
  assert.equal(plan.requests.length, 1);
  assert.equal(plan.requests[0].body.voice, 'gemini:Sulafat');
  assert.match(plan.requests[0].body.style, /日本語/);
  assert.equal(plan.requests[0].lines[0].id, 'coac0001');
  assert.equal(plan.lines[1].text, 'Your gate is B thirty-two.');
  assert.equal(plan.lines[1].cc_text, '搭乗ゲートはB32です。');
  assert.equal(plan.lines[2].reuse_source_take, 'dial0001');
  assert.equal(plan.approvals_claimed, false);
});

test('planner rejects stale translations, changed source and falsely localized dialogue', () => {
  for (const change of [
    (f) => { f.project.translations.ja.lines.dial0001.source_hash = 'stale'; },
    (f) => { f.project.doc.voice.name = 'Changed'; },
    (f) => { f.specification.locales.ja.lines[1].text = '搭乗ゲートはB32です。'; },
    (f) => { f.specification.locales.ja.lines.pop(); },
    (f) => { for (const entry of f.specification.locales.ja.lines.slice(1)) { entry.kind = 'coach'; entry.text = entry.cc_text; entry.speech_locale = 'ja'; delete entry.reuse_source_take; } },
  ]) { const input = fixture(); change(input); assert.throws(() => planTeachingAudio(input)); }
});

test('English dialogue never changes speed; coaching cannot borrow the following dialogue or exceed1.15', () => {
  const input = fixture(), windows = teachingWindows(planTeachingAudio(input), input.timeline);
  assert.equal(tempoForWindow(windows[0], 129600), 1);
  assert.equal(tempoForWindow(windows[0], 142000), 1.1);
  assert.throws(() => tempoForWindow(windows[0], 154000), /Shorten coaching/);
  assert.throws(() => tempoForWindow(windows[1], 145000), /English take/);
  assert.equal(windows[0].window_end_frame, windows[1].start_frame - 9);
});

test('CC ends at the selected actual utterance rather than the common longest-language slot', () => {
  const input = fixture(), plan = planTeachingAudio(input);
  const lines = plan.lines.map((line, index) => ({ ...line, start_frame: index * 90, end_frame: index * 90 + 30, audio_samples: 48000 }));
  const result = teachingCaptions(lines, 'ja', 150);
  assert.equal(result.cues[0].start_ms, 5000);
  assert.equal(result.cues.filter((cue) => cue.line === 'coac0001').at(-1).end_ms, 6000);
  assert.ok(result.cues.some((cue) => cue.line === 'dial0001' && cue.text.includes('B32')));
  assert.ok(result.cues.every((cue) => cue.end_ms > cue.start_ms));
});

test('main English check must bind exact WAV bytes and current intended words', () => {
  const bytes = encodeWav(tone()), line = { id: 'dial0001', text: 'Gate B thirty-two.' };
  const entry = { clip: hash(bytes).slice(0, 16), intended: line.text, spoken_form: line.text, heard: line.text, noul: null };
  assert.equal(passedCurrentCheck(entry, line, bytes, emptyLexicon(), 'en'), true);
  assert.equal(passedCurrentCheck(entry, line, encodeWav(tone(330)), emptyLexicon(), 'en'), false);
  assert.equal(passedCurrentCheck({ ...entry, intended: 'Old text' }, line, bytes, emptyLexicon(), 'en'), false);
  assert.equal(passedCurrentCheck({ ...entry, heard: 'Gate B twenty.', noul: .2 }, line, bytes, emptyLexicon(), 'en'), false);
});

test('official synthesis adapter caches coaching by request and full WAV hash, without synthesizing English', async (t) => {
  const workdir = temporary(t), directory = path.join(workdir, 'teaching-audio', 'ja');
  const plan = planTeachingAudio(fixture());
  const calls = [];
  const send = async ({ body }) => { calls.push(body); return { wav: encodeWav(tone()), billable: 20 }; };
  await synthesizeTeachingClips({ plan, workdir, directory, options: {}, send });
  await synthesizeTeachingClips({ plan, workdir, directory, options: {}, send });
  assert.equal(calls.length, 1);
  assert.equal(calls[0].segments[0].parts[0].text, '搭乗ゲート番号を聞き取りましょう。');
  const file = path.join(directory, 'audio', 'coac0001.wav');
  const changed = readFileSync(file); changed[changed.length - 2] ^= 1; writeFileSync(file, changed);
  await synthesizeTeachingClips({ plan, workdir, directory, options: {}, send });
  assert.equal(calls.length, 2, 'corrupt cached bytes must trigger a new official request');
});

test('real mixed checker transcribes by spoken locale, deduplicates repeated English and judges actual spoken text', async (t) => {
  const workdir = temporary(t), directory = path.join(workdir, 'teaching-audio', 'ja');
  mkdirSync(path.join(directory, 'audio'), { recursive: true });
  const plan = planTeachingAudio(fixture());
  const lines = plan.lines.map((line, index) => {
    const bytes = encodeWav(tone(index ? 220 : 330));
    const clip = `audio/${line.id}.wav`; writeFileSync(path.join(directory, clip), bytes);
    return { ...line, clip, clip_sha256: hash(bytes), audio_samples: 48000 };
  });
  const heard = [], judged = [];
  const transcribe = async ({ language }) => { heard.push(language); return language === 'en' ? 'Your gate is B thirty-two.' : '搭乗ゲート番号を聞いてください。'; };
  const judge = async ({ lines: questions, language }) => { judged.push({ questions, language }); return new Map(questions.map((line) => [line.id, .9])); };
  const options = { lines, directory, workdir, lexicon: emptyLexicon(), options: {}, transcribe, judge };
  const result = await checkMixedLines(options);
  assert.deepEqual(heard, ['ja', 'en']);
  assert.equal(judged.length, 1);
  assert.equal(judged[0].language, 'ja');
  assert.equal(judged[0].questions[0].intended, lines[0].text);
  assert.equal(result.dial0001.intended, 'Your gate is B thirty-two.');
  assert.equal(Object.values(result).every((entry) => entry.passed), true);
  await checkMixedLines(options);
  assert.equal(heard.length, 2, 'unchanged checked takes must not be bought again');
  await assert.rejects(checkMixedLines({ ...options, lines: [{ ...lines[0], audio_samples: 24000 }] }), /sample count/);
  const changed = readFileSync(path.join(directory, lines[1].clip)); changed[45] ^= 1; writeFileSync(path.join(directory, lines[1].clip), changed);
  await assert.rejects(checkMixedLines(options), /clip changed/);
});

test('manifest checker refuses replacing dialogue, speeding English or changing source clip hashes', () => {
  const input = fixture(), plan = planTeachingAudio(input);
  for (const line of input.timeline.lines) line.audio_sha256 = 'a'.repeat(64);
  const source = { timeline: input.timeline, source_timeline_sha256: 'b'.repeat(64), branding: { hash: 'c'.repeat(64), intro: { frames: 150 } } };
  const manifest = { schema: TEACHING_SCHEMA, fingerprint: plan.fingerprint, source_timeline_sha256: source.source_timeline_sha256, branding_hash: source.branding.hash, total_frames: 18000, body_frames: 300,
    intro_frames: 150, sample_rate: 48000, slug: plan.slug, locale: plan.locale, source_script_sha256: plan.source_script_sha256, specification_sha256: plan.specification_sha256,
    artifacts: Object.fromEntries(TEACHING_ARTIFACTS.map((name) => [name, 'f'.repeat(64)])),
    lines: teachingWindows(plan, input.timeline).map((line) => ({ ...line, end_frame: line.start_frame + 30, audio_samples: 48000, tempo: 1, clip: `audio/${line.id}.wav`, clip_sha256: 'a'.repeat(64), source_take_sha256: line.kind === 'dialogue' ? 'a'.repeat(64) : null })) };
  assert.doesNotThrow(() => validateTeachingManifest(manifest, plan, source));
  for (const change of [
    (copy) => { copy.lines[1].text = 'Gate B20.'; },
    (copy) => { copy.lines[1].tempo = 1.1; },
    (copy) => { copy.lines[1].clip_sha256 = 'd'.repeat(64); },
    (copy) => { copy.lines[1].clip = '../../secret.wav'; },
    (copy) => { copy.artifacts = {}; },
    (copy) => { delete copy.artifacts['track.m4a']; },
    (copy) => { copy.artifacts['captions.srt'] = 'bad'; },
    (copy) => { copy.intro_frames = 0; },
    (copy) => { copy.sample_rate = 24000; },
    (copy) => { copy.locale = 'ko'; },
    (copy) => { copy.source_script_sha256 = '0'.repeat(64); },
    (copy) => { copy.specification_sha256 = '0'.repeat(64); },
  ]) { const copy = structuredClone(manifest); change(copy); assert.throws(() => validateTeachingManifest(copy, plan, source)); }
});

test('trailing freshness re-reads specification and i18n files, not only video.json', (t) => {
  const directory = temporary(t), input = fixture();
  mkdirSync(path.join(directory, 'i18n'));
  input.project.dir = directory;
  input.project.file = path.join(directory, 'video.json');
  const specFile = path.join(directory, 'teaching-audio.json');
  const translationFile = path.join(directory, 'i18n', 'ja.json');
  writeFileSync(input.project.file, JSON.stringify(input.project.doc));
  writeFileSync(specFile, JSON.stringify(input.specification));
  writeFileSync(translationFile, JSON.stringify(input.project.translations.ja));
  const plan = planTeachingAudio(input);
  const args = { project: input.project, locale: 'ja', fingerprint: plan.fingerprint };
  assert.doesNotThrow(() => requireCurrentTeachingPlan(args));
  const changed = structuredClone(input.project.translations.ja);
  changed.lines.coac0001.text = 'Changed translation';
  writeFileSync(translationFile, JSON.stringify(changed));
  assert.throws(() => requireCurrentTeachingPlan(args), /CC translation/);
  writeFileSync(translationFile, JSON.stringify(input.project.translations.ja));
  const changedSpec = structuredClone(input.specification);
  changedSpec.locales.ja.lines[1].reuse_source_take = 'wrong000';
  writeFileSync(specFile, JSON.stringify(changedSpec));
  assert.throws(() => requireCurrentTeachingPlan(args), /take reuse/);
});

test('mixed checker reuses genuine current main English evidence without buying the same transcription', async (t) => {
  const workdir = temporary(t), directory = path.join(workdir, 'teaching-audio', 'ja');
  mkdirSync(path.join(directory, 'audio'), { recursive: true });
  const line = planTeachingAudio(fixture()).lines[1];
  const bytes = encodeWav(tone());
  const clip = 'audio/dial0001.wav'; writeFileSync(path.join(directory, clip), bytes);
  const sourceChecks = { lines: { dial0001: { clip: hash(bytes).slice(0, 16), intended: line.text, spoken_form: line.text, heard: line.text, noul: null } } };
  const result = await checkMixedLines({ lines: [{ ...line, clip, clip_sha256: hash(bytes), audio_samples: 48000 }], directory, workdir, lexicon: emptyLexicon(), options: {}, sourceChecks,
    transcribe: async () => { throw new Error('must reuse current exact-byte check'); }, judge: async () => { throw new Error('must not judge matching text'); } });
  assert.equal(result.dial0001.passed, true);
  assert.equal(result.dial0001.provenance, 'current_checked_approved_main_take');
});

test('localized choose instruction preserves all four seconds of learner response time', () => {
  const input = fixture();
  input.project.doc.scenes[0].lines[0].pause_after_ms = 4000;
  input.specification.source_script_sha256 = hash(input.project.doc);
  input.timeline.lines[0].end_frame = 180;
  for (const line of input.timeline.lines.slice(1)) { line.start_frame += 90; line.end_frame += 90; }
  for (const scene of input.timeline.scenes.slice(1)) { scene.states[0].start_frame += 90; scene.states[0].end_frame += 90; }
  input.timeline.total_frames += 90;
  input.timeline.scenes[0].states[0].end_frame = 180;
  const window = teachingWindows(planTeachingAudio(input), input.timeline)[0];
  assert.equal(window.window_end_frame, 60, 'six-second line window reserves four seconds for the learner');
  assert.throws(() => tempoForWindow(window, 3 * 48000), /Shorten coaching/);
});
