// `import` of a zero-dialogue Short (docs/videos/SHORTS.md §工具端, the `import` row): a finished
// cut with no captions and its cards named in meta.json, and an original Short cut from no long
// video. The 17 s cut is made here with ffmpeg (a colour field and a tone, no speech) and the
// test skips where ffmpeg is missing. Nothing calls a service: qa runs offline.
import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { ToolMissing, locateFfmpeg, runTool } from '../assemble/ffmpeg.mjs';
import { PROFILE, SCRIPT_FILE, phrasesOf, validate } from './core.mjs';
import { importShort, scriptFromImport, timelineFromCaptions } from './import.mjs';
import { evidenceItem, runQa, silentImport } from './qa.mjs';

const temp = (t, prefix) => {
  const dir = mkdtempSync(path.join(os.tmpdir(), prefix));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
};
const SECONDS = 17;
const meta = (changes = {}) => ({
  slug: 'wangjia-couple-e01', line: 'drama', series: 'wangjia-couple', original: true,
  titles: ['老公偷吃最後一塊', '最後一塊誰吃的？'], description: '零台詞的夫妻小劇場。',
  headlines: ['最後一塊', '誰吃的？', '原來是貓'], synthetic_media: true, ...changes,
});

test('a cut with no captions becomes a script of meta.json\'s cards, with no phrase', () => {
  const doc = scriptFromImport(meta(), []);
  assert.deepEqual(validate(doc, { imported: true }), []);
  assert.deepEqual([doc.dialogue, doc.original, 'headlines' in doc, phrasesOf(doc).length], [false, true, false, 0]);
  assert.deepEqual(doc.scenes, [{ headline: '最後一塊', narration: [] }, { headline: '誰吃的？', narration: [] }, { headline: '原來是貓', narration: [] }]);
  assert.deepEqual(timelineFromCaptions([], doc.scenes), []);
  assert.throws(() => scriptFromImport(meta({ headlines: undefined }), []), /no captions \(no dialogue\): meta\.json must list its cards as headlines/);
  assert.throws(() => scriptFromImport(meta({ headlines: [] }), []), /must list its cards as headlines/);
  assert.throws(() => scriptFromImport(meta({ dialogue: false }), [{ start: 0, end: 2, text: '你好' }]), /says the cut has no dialogue, but zh-TW\.srt has 1 captions/);
});

test('dialogue and original are an import\'s words only, and an original Short has no source', () => {
  const doc = scriptFromImport(meta(), []);
  assert.deepEqual(validate(doc), ['dialogue is a field of an imported cut only', 'original is a field of an imported cut only', 'source.slug required', ...[0, 1, 2].map((i) => `scene ${i}: narration phrases 1–38 characters`)]);
  const { original: _original, ...sourceless } = doc;
  assert.ok(validate(sourceless, { imported: true }).includes('source.slug required'), 'a drama with no source must say it is original');
  assert.ok(validate({ ...doc, source: { slug: 'wangjia' } }, { imported: true }).includes('an original Short has no source: it is cut from no long video'));
  assert.ok(validate({ ...doc, line: 'cut' }, { imported: true }).includes('an original Short is line drama'));
  assert.ok(validate({ ...doc, original: false }, { imported: true }).includes('original may only be true (a Short cut from no long video)'));
  assert.ok(validate({ ...doc, dialogue: true }, { imported: true }).includes('dialogue may only be false (a cut with no spoken words)'));
  assert.ok(validate({ ...doc, scenes: [{ headline: 'a', narration: ['有人說話'] }, ...doc.scenes.slice(1)] }, { imported: true }).includes('scene 0: a cut with no dialogue has no narration phrases'));
});

test('an import with no headlines for a cut with no captions is refused before anything is made', async (t) => {
  const from = temp(t, 'shorts-silent-from-');
  writeFileSync(path.join(from, 'final.mp4'), 'not read');
  writeFileSync(path.join(from, 'zh-TW.srt'), '');
  const { headlines: _headlines, ...bare } = meta();
  writeFileSync(path.join(from, 'meta.json'), JSON.stringify(bare));
  const workdir = temp(t, 'shorts-silent-work-');
  await assert.rejects(importShort({ from, workdir, tools: { ffmpeg: 'no-ffmpeg', ffprobe: 'no-ffprobe' } }), /must list its cards as headlines/);
  assert.ok(!existsSync(path.join(workdir, 'wangjia-couple-e01')));
});

/** A 17 s Short with music and no speech, on the Shorts profile; null when ffmpeg is missing. */
async function silentCut(t, file) {
  let tools;
  try {
    tools = await locateFfmpeg();
  } catch (error) {
    if (error instanceof ToolMissing) return t.skip(error.message) ?? null;
    throw error;
  }
  await runTool(tools.ffmpeg, ['-y', '-v', 'error', '-f', 'lavfi', '-i', `color=c=0x335577:s=${PROFILE.width}x${PROFILE.height}:r=${PROFILE.fps}:d=${SECONDS}`,
    '-f', 'lavfi', '-i', `sine=frequency=220:sample_rate=48000:duration=${SECONDS}`, '-af', 'volume=0.5',
    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '45', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '48000', '-shortest', file]);
  return tools;
}

test('a 17 s zero-dialogue original Short imports, and qa passes narration, captions and evidence for it', async (t) => {
  const from = temp(t, 'shorts-silent-from-');
  const tools = await silentCut(t, path.join(from, 'final.mp4'));
  if (!tools) return;
  writeFileSync(path.join(from, 'zh-TW.srt'), '');
  writeFileSync(path.join(from, 'meta.json'), JSON.stringify(meta()));
  const result = await importShort({ from, workdir: temp(t, 'shorts-silent-work-'), tools });
  assert.deepEqual([result.status, result.phrases, result.dialogue, result.original], ['imported', 0, false, true]);
  assert.ok(Math.abs(result.seconds - SECONDS) < 0.05, `${result.seconds}s`);
  const { directory } = result;
  const read = (name) => JSON.parse(readFileSync(path.join(directory, name), 'utf8'));
  const checks = read('checks.json');
  assert.deepEqual([checks.imported, checks.dialogue, checks.original, checks.final_sha256.length], [true, false, true, 64]);
  const timeline = read('timeline.json');
  assert.deepEqual([timeline.cues, timeline.frames], [[], SECONDS * PROFILE.fps]);
  assert.equal(readFileSync(path.join(directory, 'upload', 'zh-TW.srt'), 'utf8'), '');
  assert.ok(!existsSync(path.join(directory, 'audio', '000.wav')), 'no phrase, no phrase audio');
  const doc = read(SCRIPT_FILE);
  assert.ok(silentImport({ doc, timeline, checks }));

  const report = await runQa({ directory, offline: true, settings: { seconds_min: 9, seconds_max: 18, locales: ['en'] }, tools });
  const items = Object.fromEntries(report.items.map((each) => [each.id, each]));
  assert.deepEqual(items.narration, { id: 'narration', ok: true, detail: 'no spoken words: zero-dialogue cut' });
  assert.deepEqual(items.captions, { id: 'captions', ok: true, detail: 'no spoken words: zero-dialogue cut' }, 'no en.srt is wanted either');
  assert.equal(items.evidence.ok, true);
  assert.equal(items.evidence.detail, `an original Short, cut from no long video: bound to the cut itself, sha256 ${checks.final_sha256}`);
  assert.equal(report.final_sha256, checks.final_sha256);
  assert.equal(items.profile.ok, true, items.profile.detail);
  // The rest stay as they are for an import: the owner looks at the layout, nobody checked the facts offline.
  assert.equal(items.layout.ok, false);
  assert.match(items.layout.detail, /a cut made elsewhere has no layout measurement/);
  assert.equal(items.facts.ok, false);
  assert.equal(report.ok, false);

  // A caption that turns up in a zero-dialogue cut is named.
  writeFileSync(path.join(directory, 'upload', 'zh-TW.srt'), '1\n00:00:01,000 --> 00:00:02,000\n有人說話\n');
  const spoken = await runQa({ directory, offline: true, settings: { seconds_min: 9, seconds_max: 18 }, tools });
  assert.deepEqual(spoken.items.find((each) => each.id === 'captions'), { id: 'captions', ok: false, detail: '1 captions for 0 phrases' });
});

test('an original Short\'s evidence is the cut the import measured, nothing else', () => {
  const doc = scriptFromImport(meta(), []);
  const sha = 'a'.repeat(64);
  const checks = { imported: true, original: true, final_sha256: sha };
  assert.equal(evidenceItem({ doc, finalSha256: sha, checks }).ok, true);
  assert.deepEqual(evidenceItem({ doc, finalSha256: 'b'.repeat(64), checks }), { id: 'evidence', ok: false, detail: 'the cut differs from the one imported: import it again' });
  assert.equal(evidenceItem({ doc, finalSha256: sha, checks: null }).ok, false);
  assert.equal(evidenceItem({ doc, finalSha256: sha, checks: { ...checks, original: false } }).ok, false);
  // A cut with dialogue but no checks.json is not silent: its narration and captions are checked as ever.
  assert.equal(silentImport({ doc, timeline: { cues: [] }, checks: { imported: true, dialogue: true } }), false);
  assert.equal(silentImport({ doc, timeline: { cues: [] }, checks: null }), false);
});
