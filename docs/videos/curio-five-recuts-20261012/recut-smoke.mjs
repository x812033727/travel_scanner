#!/usr/bin/env node
// Real FFmpeg integration smoke with synthetic source media. Never reads/writes a production video.
import { createHash } from 'node:crypto';
import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(process.argv[2] ?? path.join(tmpdir(), `curio-five-recuts-assembler-smoke-${Date.now()}`));
const src = path.join(root, 'fixture-source'), out = path.join(root, 'output'), slug = 'curio-h02';
const locales = ['zh-TW', 'en', 'ja', 'ko'];
const bytes = (o) => `${JSON.stringify(o, null, 2)}\n`;
const save = (p, o) => { mkdirSync(path.dirname(p), { recursive: true }); writeFileSync(p, bytes(o)); };
const hash = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');
function run(bin, a) { const r = spawnSync(bin, a, { encoding: 'utf8', windowsHide: true, maxBuffer: 4e7 }); assert.equal(r.status, 0, r.error?.message ?? r.stderr); return r.stdout; }
const ff = (a) => run('ffmpeg', ['-v', 'error', '-nostdin', '-y', ...a]);
for (const d of ['segments', 'build', 'keyframes', 'upload/captions']) mkdirSync(path.join(src, d), { recursive: true });
for (const [id, seconds, color] of [['hook', 1, 'red'], ['body', 2, 'blue']]) {
  ff(['-f', 'lavfi', '-i', `color=c=${color}:s=1920x1080:r=30:d=${seconds}`, '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', '-an', path.join(src, 'segments', `${id}.mp4`)]);
}
writeFileSync(path.join(src, 'build', 'segments.ffconcat'), `ffconcat version 1.0\nfile '${path.join(src, 'segments/hook.mp4').replaceAll('\\', '/')}'\nfile '${path.join(src, 'segments/body.mp4').replaceAll('\\', '/')}'\n`);
ff(['-f', 'concat', '-safe', '0', '-i', path.join(src, 'build/segments.ffconcat'), '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=3', '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-ac', '2', path.join(src, 'build/body.mp4')]);
copyFileSync(path.join(src, 'build/body.mp4'), path.join(src, 'final.mp4'));
ff(['-i', path.join(src, 'segments/body.mp4'), '-frames:v', '1', path.join(src, 'keyframes/body-1.png')]);
const timeline = { fps: 30, sample_rate: 48000, total_frames: 90, scenes: [{ id: 'hook', start_frame: 0, end_frame: 30 }, { id: 'body', start_frame: 30, end_frame: 90 }], chapters: [{ title: 'Old hook', scene: 'hook', start_frame: 0 }, { title: 'Retained body', scene: 'body', start_frame: 30 }] };
save(path.join(src, 'timeline.json'), timeline);
save(path.join(src, 'checks.json'), { ok: true, synthetic_test_fixture: true, branding: { intro_frames: 0, outro_frames: 0, body_frames: 90, body_file: 'build/body.mp4', body_sha256: hash(path.join(src, 'build/body.mp4')) } });
const description = 'Synthetic test only.\n\n00:00 Old hook\n00:01 Retained body\n\nPreserved source credit\n\n#fixture';
save(path.join(src, 'upload/metadata.json'), { slug, title: 'SYNTHETIC TEST', description, tags: ['fixture'], category_id: 27, final_sha256: hash(path.join(src, 'final.mp4')), localizations: Object.fromEntries(locales.slice(1).map((l) => [l, { title: `${l} synthetic title`, description: description.replace('Retained body', `${l} retained body`) }])) });
const localeSources = {};
for (const locale of locales) {
  const cap = path.join(src, 'upload/captions', `${locale}.srt`);
  writeFileSync(cap, `1\n00:00:00,000 --> 00:00:00,800\n${locale} OLD HOOK\n\n2\n00:00:01,000 --> 00:00:02,800\n${locale} RETAIN THIS TEXT\n`);
  localeSources[locale] = { captions: cap, audio: path.join(src, 'final.mp4') };
}
const sourceMap = path.join(root, 'source-map.json');
save(sourceMap, { episodes: [{ slug, workdir: src, metadata: path.join(src, 'upload/metadata.json'), locales: localeSources }] });
const specs = path.join(root, 'intro-specs.json');
save(specs, { episodes: [{ slug, lines: [{ id: 'intro01', text: 'Fixture', scene: 'body' }] }] });
const common = { fps: 30, sample_rate: 48000, total_frames: 900, seconds: 30, duration_ok: true, padding_ok: true, lines: [{ id: 'intro01', source_scene: 'body', start_frame: 0, end_frame: 900 }], tracks: {} };
for (const locale of locales) {
  const dir = path.join(out, slug, 'intro', locale); mkdirSync(dir, { recursive: true });
  ff(['-f', 'lavfi', '-i', 'sine=frequency=660:sample_rate=48000:duration=30', '-c:a', 'pcm_s16le', path.join(dir, 'narration.wav')]);
  writeFileSync(path.join(dir, `${locale}.srt`), `1\n00:00:00,000 --> 00:00:29,000\n${locale} SYNTHETIC OPENING\n`);
  save(path.join(dir, 'timeline.json'), { total_frames: 900, synthetic_test_fixture: true });
  const binding = { narration_sha256: hash(path.join(dir, 'narration.wav')), timeline_sha256: hash(path.join(dir, 'timeline.json')), captions_sha256: hash(path.join(dir, `${locale}.srt`)) };
  save(path.join(dir, 'receipt.json'), { ...binding, aligned: true, padding_ok: true, duration_ok: true, synthetic_test_fixture: true });
  save(path.join(dir, 'check.json'), { ...binding, ok: true, synthetic_test_fixture: true });
  common.tracks[locale] = { ...binding, receipt_sha256: hash(path.join(dir, 'receipt.json')) };
}
save(path.join(out, slug, 'intro/shared-timeline.json'), common);
const logs = run(process.execPath, [path.join(here, 'recut.mjs'), '--slug', slug, '--output-root', out, '--source-map', sourceMap, '--specs', specs]);
writeFileSync(path.join(root, 'run.log'), logs);
const result = JSON.parse(readFileSync(path.join(out, slug, 'qa.json'), 'utf8'));
assert.equal(result.total_frames, 1740);
assert.equal(result.sources_unchanged, true);
assert.equal(result.retained_body_picture_unchanged, true);
assert.equal(result.body_video_reencoded, false);
for (const locale of locales) {
  const srt = readFileSync(path.join(out, slug, 'upload/captions', `${locale}.srt`), 'utf8');
  assert.ok(!srt.includes('OLD HOOK'));
  assert.ok(srt.includes('00:00:35,000 --> 00:00:36,800'));
  assert.ok(srt.includes(`${locale} RETAIN THIS TEXT`));
  assert.equal(result.audio[locale].samples, 1740 * 1600);
  assert.equal(result.audio[locale].body_samples_unchanged, true);
}
const metadata = JSON.parse(readFileSync(path.join(out, slug, 'upload/metadata.json'), 'utf8'));
assert.ok(metadata.description.includes('Preserved source credit'));
assert.ok(metadata.description.includes('Golden Hour — Telecasted'));
assert.equal(metadata.video_id, null);
assert.equal(metadata.uploaded, false);
assert.equal(metadata.chapters[1].at, '00:35');
assert.equal(result.ok, true);
console.log(JSON.stringify({ ok: true, kind: 'synthetic-ffmpeg-integration-smoke', root, frames: result.total_frames, locales, retention: result.retained_body_picture_check }, null, 2));
