// `import` of a Short made outside this tool that says nothing (docs/videos/SHORTS.md §無台詞原創):
// a 17-second cut with no captions and no full video behind it goes through the same quality
// check and package as any other, and carries its title and description in English too.
import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { ToolMissing, locateFfmpeg, runTool } from '../assemble/ffmpeg.mjs';
import { phrasesOf, sha256, validate } from './core.mjs';
import { importShort, importedCues, scriptFromImport } from './import.mjs';
import { captionLocales, composeMetadata, metadataProblems, packageBuild } from './package.mjs';
import { captionsItem, evidenceItem, runQa, scriptShape, varietyItem } from './qa.mjs';

const temp = (t, prefix) => {
  const dir = mkdtempSync(path.join(os.tmpdir(), prefix));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
};

const META = Object.freeze({
  slug: 'wangjia-couple-e01',
  line: 'drama',
  series: 'wangjia-couple',
  original: true,
  silent: true,
  titles: ['老公偷吃最後一塊雞排', '最後一塊雞排的下場'],
  description: '王家夫妻的零台詞日常：一塊雞排引發的眼神大戰。',
  headlines: ['最後一塊雞排', '眼神交鋒', '老婆贏了'],
  hashtags: ['#Shorts', '#夫妻日常'],
  localizations: {
    en: { title: 'Husband Steals the Last Fried Chicken', description: 'A wordless married-couple comedy: one piece of fried chicken, one stare-down.', hashtags: ['#Shorts', '#couplecomedy'] },
  },
});

test('a silent original names its cards, says nothing and leads back to no video', () => {
  const doc = scriptFromImport(META, []);
  assert.deepEqual(validate(doc), []);
  assert.deepEqual([doc.scenes.length, phrasesOf(doc).length, 'headlines' in doc], [3, 0, false]);
  assert.deepEqual(doc.scenes[1], { headline: '眼神交鋒', narration: [] });
  assert.ok(validate({ ...doc, scenes: doc.scenes.map((scene) => ({ ...scene, narration: ['一句話'] })) }).some((e) => e.includes('a silent Short says nothing')));
  assert.ok(validate({ ...doc, line: 'cut', source: undefined }).some((e) => e.startsWith('silent: only a drama')));
  assert.ok(validate({ ...doc, source: { slug: 'wangjia-couple' } }).includes('an original Short names no source'));
  assert.ok(validate({ ...doc, original: false }).includes('original is true or left out'));
  const { original: _original, ...sourceless } = doc;
  assert.ok(validate(sourceless).includes('source.slug required'), 'a drama that is not original still names its full video');
  assert.ok(validate({ ...doc, localizations: { fr: { title: 'x', description: 'y' } } }).some((e) => e.startsWith('localizations.fr')));
  assert.ok(validate({ ...doc, localizations: { en: { title: '<b>x</b>', description: 'y' } } }).some((e) => e.startsWith('localizations.en.title')));
  assert.ok(validate({ ...doc, localizations: { en: { title: 'x' } } }).some((e) => e.startsWith('localizations.en.description')));
});

test('a silent cut may leave its captions out or empty; a spoken one may not', (t) => {
  const from = temp(t, 'shorts-silent-from-');
  assert.deepEqual(importedCues(from, META), []);
  writeFileSync(path.join(from, 'zh-TW.srt'), '﻿\n');
  assert.deepEqual(importedCues(from, META), []);
  assert.throws(() => importedCues(from, { ...META, silent: undefined }), /says "silent": true in meta\.json/);
  writeFileSync(path.join(from, 'zh-TW.srt'), '1\n00:00:00,000 --> 00:00:02,000\n喂\n');
  assert.throws(() => importedCues(from, META), /says the cut is silent, and zh-TW\.srt has 1 captions/);
});

test('an original Short is its own evidence, and a silent one passes narration and captions with a reason', () => {
  const doc = { ...scriptFromImport(META, []), evidence: [{ path: 'final.mp4', sha256: 'a'.repeat(64) }] };
  assert.deepEqual(evidenceItem({ doc, finalSha256: 'a'.repeat(64) }).ok, true);
  assert.match(evidenceItem({ doc, finalSha256: 'b'.repeat(64) }).detail, /lists no file with the final cut's hash/);
  assert.equal(evidenceItem({ doc, evidenceError: 'evidence changed: final.mp4', finalSha256: 'a'.repeat(64) }).ok, false);
  const timeline = { fps: 30, frames: 510, seconds: 17, cues: [] };
  assert.match(captionsItem({ captions: new Map(), timeline, locales: ['en'], silent: true }).detail, /carries no caption track/);
  assert.equal(captionsItem({ captions: new Map([['zh-TW', '']]), timeline, silent: true }).ok, false);
  // Two silent episodes of one series are built alike; only their openings are compared.
  const previous = { slug: 'wangjia-couple-e00', series: 'wangjia-couple', ...scriptShape(doc), opening: '別的開場' };
  assert.equal(varietyItem({ doc, history: [previous] }).ok, true);
  assert.equal(varietyItem({ doc, history: [{ ...previous, opening: scriptShape(doc).opening }] }).ok, false);
});

test('the package carries the English title and description, and no caption track for a silent Short', () => {
  const doc = scriptFromImport(META, []);
  const metadata = composeMetadata({ doc, finalSha256: 'f', seconds: 17, settings: { locales: ['en', 'ja'] } });
  assert.deepEqual([metadata.captions, metadata.locales, captionLocales(metadata)], [false, [], []]);
  assert.deepEqual(metadata.localizations, { en: { title: 'Husband Steals the Last Fried Chicken', description: 'A wordless married-couple comedy: one piece of fried chicken, one stare-down.\n\n#Shorts #couplecomedy\n' } });
  assert.deepEqual(metadataProblems(metadata), []);
  assert.ok(metadataProblems({ ...metadata, localizations: { en: { title: 'x'.repeat(101), description: '' } } }).length === 2);
  const cut = { ...doc, original: undefined, silent: undefined, line: 'cut', source: { slug: 'ai-model-choice' }, scenes: doc.scenes.map((scene) => ({ ...scene, narration: ['一句'] })) };
  const spoken = composeMetadata({ doc: cut, finalSha256: 'f', seconds: 30, settings: { locales: ['en'] }, sourceUrl: 'https://youtu.be/dQw4w9WgXcQ' });
  assert.deepEqual(['captions' in spoken, captionLocales(spoken)], [false, ['zh-TW', 'en']]);
  assert.match(spoken.localizations.en.description, /^Full video: https:\/\/youtu\.be\/dQw4w9WgXcQ\n\n/);
});

test('a 17-second cut with no words goes through import, qa and package', async (t) => {
  let tools;
  try {
    tools = await locateFfmpeg();
  } catch (error) {
    if (error instanceof ToolMissing) return t.skip('ffmpeg is not installed');
    throw error;
  }
  const from = temp(t, 'shorts-silent-from-');
  // Picture and a quiet tone, no speech: what a cut made of generated clips and music looks like.
  await runTool(tools.ffmpeg, ['-y', '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=1080x1920:rate=30', '-f', 'lavfi', '-i', 'sine=frequency=220:sample_rate=48000', '-t', '17', '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '48000', '-shortest', path.join(from, 'final.mp4')]);
  writeFileSync(path.join(from, 'zh-TW.srt'), '');
  writeFileSync(path.join(from, 'meta.json'), JSON.stringify(META));
  const work = temp(t, 'shorts-silent-work-');
  const imported = await importShort({ from, workdir: work, tools });
  assert.equal(imported.phrases, 0);
  assert.ok(Math.abs(imported.seconds - 17) < 0.1, `${imported.seconds}s`);
  const { directory } = imported;
  assert.equal(existsSync(path.join(directory, 'upload', 'zh-TW.srt')), false, 'a silent cut carries no caption track');
  const finalSha = sha256(readFileSync(path.join(directory, 'upload', 'final.mp4')));
  const script = JSON.parse(readFileSync(path.join(directory, 'script.json'), 'utf8'));
  assert.deepEqual(script.evidence, [{ path: 'final.mp4', sha256: finalSha }]);
  assert.equal(sha256(readFileSync(path.join(directory, 'evidence', 'final.mp4'))), finalSha);
  const manifest = JSON.parse(readFileSync(path.join(directory, 'upload', 'manifest.json'), 'utf8'));
  assert.deepEqual(manifest.files.map((file) => file.name), ['final.mp4', 'cover.png', 'titles.json']);

  const report = await runQa({ directory, offline: true, settings: { locales: ['en'] }, tools, history: [] });
  const items = Object.fromEntries(report.items.map((each) => [each.id, each]));
  for (const id of ['narration', 'evidence', 'captions', 'metadata', 'disclosure']) assert.equal(items[id].ok, true, `${id}: ${items[id].detail}`);
  assert.match(items.narration.detail, /silent: true/);
  assert.match(items.evidence.detail, /its evidence is the cut itself/);
  // A Short shorter than the owner's range still says so: the length is the owner's setting.
  assert.match(items.profile.detail, /17\.00s is outside 25–55s/);

  const { metadata, report: packaged } = packageBuild({ directory, settings: { locales: ['en'] } });
  const byId = Object.fromEntries(packaged.items.map((each) => [each.id, each]));
  assert.deepEqual([byId.files.ok, byId.descriptions.ok, byId.captions.ok], [true, true, true], JSON.stringify(packaged.items));
  assert.match(byId.descriptions.detail, /translated into en/);
  assert.equal(metadata.localizations.en.title, 'Husband Steals the Last Fried Chicken');
  assert.deepEqual(metadata.captions_sha256, {});
});
