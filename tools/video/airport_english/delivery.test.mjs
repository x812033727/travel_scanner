import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { existsSync, mkdtempSync, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { emptyLexicon } from '../core/lexicon.mjs';
import { ITEM_IDS } from '../qa/checks.mjs';
import { encodeWav } from '../tts/wav.mjs';
import { TEACHING_SCHEMA } from './teaching-audio.mjs';
import { buildDelivery, combinedReviewTemplate, copyVerified, planDelivery, previewLesson, requireMainQa, requireMixedCheck } from './delivery.mjs';

const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const sha = (letter) => letter.repeat(64);
function temporary(t) { const dir = mkdtempSync(path.join(tmpdir(), 'airport-delivery-test-')); t.after(() => rmSync(dir, { recursive: true, force: true })); return dir; }
function fixture() {
  const bytes = encodeWav(Int16Array.from({ length: 48000 }, (_, index) => Math.round(4000 * Math.sin(index / 30))));
  const lines = [{ id: 'coach001', text: '番号を聞きましょう。', speech_locale: 'ja' }, { id: 'dial0001', text: 'Gate B thirty-two.', speech_locale: 'en' }].map((line) => ({ ...line, clip: `audio/${line.id}.wav`, clip_sha256: hash(bytes), audio_samples: 48000 }));
  const manifest = { lines, artifacts: { 'track.m4a': sha('a') } };
  const manifestSha = sha('b');
  const report = { schema: TEACHING_SCHEMA, status: 'mixed_audio_check_passed_pending_final_review', manifest_sha256: manifestSha, track_sha256: sha('a'), flags: [], unchecked: 0,
    lines: Object.fromEntries(lines.map((line) => [line.id, { clip: hash(bytes).slice(0, 16), clip_sha256: hash(bytes), language: line.speech_locale, intended: line.text, spoken_form: line.text, heard: line.text, noul: null, passed: true }])) };
  return { manifest, manifestSha, report, readClip: () => bytes, lexicon: emptyLexicon() };
}

test('official main QA requires exactly eleven passed items bound to the current cut', () => {
  const report = { ok: true, final_sha256: sha('a'), items: ITEM_IDS.map((id) => ({ id, ok: true })) };
  assert.doesNotThrow(() => requireMainQa(report, sha('a')));
  assert.throws(() => requireMainQa(report, sha('b')), /eleven genuine/);
  assert.throws(() => requireMainQa({ ...report, items: [] }, sha('a')), /eleven genuine/);
  assert.throws(() => requireMainQa({ ...report, items: report.items.map((item, index) => index ? item : { ...item, ok: false }) }, sha('a')), /eleven genuine/);
});

test('delivery accepts a complete exact-byte mixed check, then rejects missing, stale and merely asserted passes', () => {
  assert.doesNotThrow(() => requireMixedCheck(fixture()));
  for (const change of [
    (input) => { input.report.lines = {}; },
    (input) => { input.report.manifest_sha256 = sha('c'); },
    (input) => { input.report.track_sha256 = sha('d'); },
    (input) => { input.report.unchecked = 1; },
    (input) => { input.report.flags.push('dial0001'); },
    (input) => { input.report.lines.dial0001.language = 'ja'; },
    (input) => { input.report.lines.dial0001.heard = 'Gate B twenty.'; input.report.lines.dial0001.noul = .1; },
    (input) => { input.manifest.lines[0].audio_samples = 24000; },
    (input) => { input.report.lines.coach001.intended = 'old source'; },
  ]) { const input = fixture(); change(input); assert.throws(() => requireMixedCheck(input)); }
});

test('verified copies bind source and destination bytes without hard-linking mutable media', async (t) => {
  const dir = temporary(t), source = path.join(dir, 'source.txt'), out = path.join(dir, 'delivery');
  writeFileSync(source, 'approved bytes');
  const file = { source, destination: 'day01/main/description.en.txt', sha256: hash(Buffer.from('approved bytes')) };
  const copied = await copyVerified(file, out);
  assert.equal(copied.sha256, file.sha256);
  writeFileSync(path.join(out, file.destination), 'edited delivery copy');
  assert.equal(readFileSync(source, 'utf8'), 'approved bytes');
  writeFileSync(source, 'source changed');
  await assert.rejects(copyVerified(file, out), /Source changed/);
  await assert.rejects(copyVerified({ ...file, destination: '../escape' }, out), /Unsafe/);
  const link = path.join(dir, 'link.txt'); symlinkSync(source, link);
  await assert.rejects(copyVerified({ ...file, source: link }, out), /regular file/);
});

test('preview maps the four audio and CC locales independently and uses final measured chapters', () => {
  const tracks = Object.fromEntries(['zh-TW', 'zh-CN', 'ja', 'ko'].map((locale) => [locale, { audio: `day01/teaching-audio/${locale}.m4a`, cues: [{ start_ms: 5000, end_ms: 6000, text: `CC ${locale}` }] }]));
  const episode = { day: 1, title: '報到櫃檯', tracks, chapters: [{ start: 0, title: 'Introduction' }, { start: 45, title: 'Listen' }], copies: [] };
  const lesson = previewLesson(episode);
  assert.equal(lesson.master, 'day01/main/final.mp4');
  assert.equal(lesson.audio['zh-Hant'], 'day01/teaching-audio/zh-TW.m4a');
  assert.deepEqual(lesson.captions['zh-Hans'], [[5, 6, 'CC zh-CN']]);
  assert.equal(lesson.chapters[1].start, 45);
});

test('combined-review checklist binds exact delivery, audio and CC hashes without approving anything', () => {
  const delivery = { episodes: [{ day: 1, source_final_sha256: sha('a'), tracks: Object.fromEntries(['zh-TW', 'zh-CN', 'ja', 'ko'].map((locale) => [locale, { audio_sha256: sha('b'), captions_sha256: sha('c') }])) }] };
  const review = combinedReviewTemplate(delivery, sha('d'));
  assert.equal(review.delivery_sha256, sha('d'));
  assert.equal(review.official_qa_approval, false);
  assert.equal(review.publication_approval, false);
  assert.ok(review.episodes[0].items.every((item) => item.checked === false));
  assert.equal(review.episodes[0].items.filter((item) => item.track_sha256 === sha('b')).length, 4);
});

test('offline delivery planning reports concrete missing-source blockers and creates no media', async (t) => {
  const dir = temporary(t), projectRoot = path.join(dir, 'project'), mediaRoot = path.join(dir, 'media');
  mkdirSync(projectRoot);
  const report = await planDelivery({ projectRoot, mediaRoot, days: [1, 2] });
  assert.equal(report.status, 'blocked_before_delivery');
  assert.equal(report.episodes.length, 2);
  assert.ok(report.episodes.every((episode) => episode.blocker.includes('does not exist')));
  assert.equal(report.paid_requests, 0);
  assert.equal(report.media_created, false);
  assert.equal(existsSync(mediaRoot), false);
});

test('build refuses missing evidence and never promotes a partial or overwrites an existing delivery', async (t) => {
  const dir = temporary(t), projectRoot = path.join(dir, 'project'), mediaRoot = path.join(dir, 'media'), out = path.join(dir, 'delivery');
  mkdirSync(projectRoot);
  await assert.rejects(buildDelivery({ projectRoot, mediaRoot, out, days: [1] }), /does not exist/);
  assert.equal(existsSync(out), false);
  assert.equal(existsSync(path.join(mediaRoot, 'airport-english-day01', 'LEASE')), false);
  mkdirSync(out); writeFileSync(path.join(out, 'existing.txt'), 'keep');
  await assert.rejects(buildDelivery({ projectRoot, mediaRoot, out, days: [1] }), /never overwritten/);
  assert.equal(readFileSync(path.join(out, 'existing.txt'), 'utf8'), 'keep');
});
