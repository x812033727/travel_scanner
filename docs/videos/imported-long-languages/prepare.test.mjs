import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, rmSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { APPROVED_CUTS, adapterLexicon, assertOriginalCut, assertOutputIsolation, buildAdapter, captionText, normalizedNarration, requireSlug, validateCaptionUnits, validateTiming } from './prepare.mjs';
import { speechHash } from '../../../tools/video/core/timeline.mjs';
import { windowsOf } from '../../../tools/video/dubs/plan.mjs';

const slug = 'ai-real-world-01-image-trust';
function fixture() {
  const bounds = [0, 10.113, 20.279, 31.193, 40.417, 50.803, 60.509];
  const words = ['第一句原始旁白。', '第二句保留原文。', '第三句帶有限制。', '第四句只是示意。', '第五句需要查證。', '第六句結束說明。'];
  const units = words.map((text, index) => ({ scene: Math.floor(index / 2), text, start: bounds[index], end: bounds[index + 1] }));
  const scenes = ['辨認來源', '檢查時間', '比對紀錄'].map((heading, index) => ({ heading, cards: ['來源', '時間', '佐證'], narration: words.slice(index * 2, index * 2 + 2).join('') }));
  return { slug, episode: { id: '01-image-trust', theme: '來源查證', thumb_a: '先問來源', sources: [], scenes },
    timing: { duration: bounds.at(-1), units, scenes: scenes.map(({ heading }, index) => ({ heading, start: bounds[index * 2], end: bounds[index * 2 + 2] })) },
    meta: { slug, titles: ['原始長片標題'], description: '本片說明查證方法。\n\n章節\n00:00 辨認來源' },
    catalog: { checked_on: '2026-09-28', sources: [] }, lexicon: { schema_version: 1, terms: {} },
    audioSamples: units.map((unit) => Math.round((unit.end - unit.start - 0.08) * 48000)) };
}

test('allows only the six frozen long cuts and refuses a revision, Short or traversal', () => {
  assert.equal(Object.keys(APPROVED_CUTS).length, 6);
  for (const id of Object.keys(APPROVED_CUTS)) assert.equal(requireSlug(id), id);
  for (const id of ['ai-real-world-01-image-trust-short-1', 'image-trust-opening-v2', '../ai-real-world-01-image-trust']) assert.throws(() => requireSlug(id), /allowed original long/);
  assert.throws(() => assertOriginalCut(slug, 'wrong', APPROVED_CUTS[slug]), /frozen original/);
  assert.doesNotThrow(() => assertOriginalCut(slug, APPROVED_CUTS[slug], APPROVED_CUTS[slug]));
});

test('normalization preserves numerical and factual differences', () => {
  assert.equal(normalizedNarration('原句， 限制！'), normalizedNarration('原句,限制!'));
  assert.notEqual(normalizedNarration('1.0'), normalizedNarration('10'));
  assert.notEqual(normalizedNarration('-10%'), normalizedNarration('10%'));
  const input = fixture();
  input.episode.scenes[0].narration = input.episode.scenes[0].narration.replace('原始', '新的');
  assert.throws(() => validateTiming(input.episode, input.timing), /differs from current long narration/);
});

test('caption equality accepts only encoding-newline differences', () => {
  const srt = '1\n00:00:00,000 --> 00:00:01,000\n原句。\n';
  assert.equal(captionText('\uFEFF' + srt.replaceAll('\n', '\r\n')), captionText(srt));
  assert.notEqual(captionText(srt.replace('01,000', '02,000')), captionText(srt));
  assert.notEqual(captionText(srt.replace('原句', '改句')), captionText(srt));
});

test('source captions bind each text and rounded timestamp to the original timing unit', () => {
  const srt = '1\n00:00:00,000 --> 00:00:01,124\n第一句，\n原始旁白。\n\n2\n00:00:01,124 --> 00:00:02,000\n第二句。\n';
  const timing = { units: [{ text: '第一句,原始旁白。', start: 0, end: 1.1236 }, { text: '第二句。', start: 1.1236, end: 2 }] };
  const result = validateCaptionUnits('\uFEFF' + srt.replaceAll('\n', '\r\n'), timing);
  assert.equal(result.cue_count, 2);
  assert.ok(result.maximum_timestamp_error_seconds < 0.001);
  assert.throws(() => validateCaptionUnits(srt.replace('原始', '新的'), timing), /text differs/);
  assert.throws(() => validateCaptionUnits(srt.replace('01,124', '01,130'), timing), /timestamp differs/);
  assert.throws(() => validateCaptionUnits(srt.replace('\n\n2\n', '\n\n3\n'), timing), /out-of-order/);
  assert.throws(() => validateCaptionUnits(srt.split('\n\n')[0], timing), /cue count/);
});

test('proper-name spellings are isolated and do not overwrite known pronunciations', () => {
  const original = { schema_version: 1, terms: { YouTube: '既有唸法' } };
  const { lexicon, additions } = adapterLexicon(original);
  assert.equal(lexicon.terms.YouTube, '既有唸法');
  assert.equal(lexicon.terms.DeepMind, 'DeepMind');
  assert.equal(original.terms.DeepMind, undefined);
  assert.equal(additions.YouTube, undefined);
});

test('rejects gaps, overlaps, scene mismatch, and an untimed tail', () => {
  for (const change of [
    (input) => { input.timing.units[1].start += 0.1; },
    (input) => { input.timing.units[1].start -= 0.1; },
    (input) => { input.timing.scenes[0].end += 0.1; },
    (input) => { input.timing.duration += 0.1; },
  ]) { const input = fixture(); change(input); assert.throws(() => validateTiming(input.episode, input.timing)); }
});

test('quantizes absolute endpoints without added pause or cumulative drift', () => {
  const input = fixture();
  const result = buildAdapter(input);
  assert.equal(result.timeline.total_frames, Math.round(input.timing.duration * 30));
  assert.equal(result.timeline.lines[0].start_frame, 0);
  for (const [index, line] of result.timeline.lines.entries()) {
    assert.equal(line.start_frame, Math.round(input.timing.units[index].start * 30));
    assert.equal(line.end_frame, Math.round(input.timing.units[index].end * 30));
    assert.equal(line.audio_samples, input.audioSamples[index]);
    if (index) assert.equal(line.start_frame, result.timeline.lines[index - 1].end_frame);
  }
  assert.ok(result.maximumError <= 1 / 60 + 1e-9);
  assert.equal(result.lint.errors.length, 0);
  assert.equal(result.timeline.speech_hash, speechHash(result.doc, input.lexicon));
  assert.equal(result.doc.voice.provider, 'gemini');
  assert.equal(result.doc.voice.name, 'Sulafat');
  assert.ok(result.doc.scenes.every((scene) => scene.lines.every((line) => line.pause_after_ms === 0)));
  assert.equal(result.doc.shorts, undefined);
});

test('each original line occurs in one complete chapter window', () => {
  const { timeline } = buildAdapter(fixture());
  const windows = windowsOf(timeline);
  assert.equal(windows.length, 3);
  assert.deepEqual(windows.flatMap((window) => window.lines), timeline.lines.map((line) => line.id));
  assert.equal(windows.at(-1).end_frame, timeline.total_frames);
  for (let i = 1; i < windows.length; i++) assert.equal(windows[i].start_frame, windows[i - 1].end_frame);
});

test('inserting a different sentence preserves existing content-derived IDs', () => {
  const input = fixture();
  const before = buildAdapter(input);
  input.timing.units.forEach((unit) => { unit.start += 1; unit.end += 1; });
  input.timing.units.unshift({ scene: 0, text: '新增一句。', start: 0, end: 1 });
  input.episode.scenes[0].narration = '新增一句。' + input.episode.scenes[0].narration;
  input.timing.scenes.forEach((scene, index) => { if (index) scene.start += 1; scene.end += 1; });
  input.timing.duration += 1;
  input.audioSamples.unshift(44160);
  const after = buildAdapter(input);
  assert.deepEqual(after.timeline.lines.slice(1).map((line) => line.id), before.timeline.lines.map((line) => line.id));
});

test('does not treat the original 80ms tail as spoken clip samples', () => {
  const input = fixture();
  const result = buildAdapter(input);
  assert.equal(result.timeline.lines[0].audio_samples, Math.round((10.113 - 0.08) * 48000));
  input.audioSamples[0] = Math.round(11 * 48000);
  assert.throws(() => buildAdapter(input), /Invalid spoken sample count/);
});

test('output may not contain, equal, or sit inside protected inputs', () => {
  const base = mkdtempSync(path.join(os.tmpdir(), 'long-language-prepare-'));
  try {
    const source = path.join(base, 'source'); mkdirSync(source);
    for (const output of [base, source, path.join(source, 'new')]) assert.throws(() => assertOutputIsolation(output, [source]), /overlaps/);
    assert.equal(assertOutputIsolation(path.join(base, 'output'), [source]), path.join(base, 'output'));
  } finally { rmSync(base, { recursive: true, force: true }); }
});
