#!/usr/bin/env node
// End-to-end smoke test of the Shorts tool with stand-in narration, so it needs neither the
// site, a token nor a speech service: build (from supplied clips) → qa (offline) → package.
//
//   node tools/video/shorts/smoke.mjs [--workdir DIR] [--channel msedge]
//
// What can be checked without the site must pass: the cut's size, frames and loudness, the cards
// inside the safe area, the evidence, the metadata, the captions. What needs the site (the
// listener, Jev, the links, the latest Shorts) must fail saying it was not checked, never pass.
// CI runs it in .github/workflows/video-tooling.yml after installing Chromium and ffmpeg.
import { existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

import { encodeWav } from '../tts/wav.mjs';
import { build } from './build.mjs';
import { phrasesOf, sha256 } from './core.mjs';
import { packageBuild } from './package.mjs';
import { runQa } from './qa.mjs';

const values = parseArgs({ options: { workdir: { type: 'string' }, channel: { type: 'string' } }, strict: true }).values;
const FIXTURE = fileURLToPath(new URL('./fixtures/smoke/', import.meta.url));
const base = path.resolve(values.workdir ?? mkdtempSync(path.join(tmpdir(), 'shorts-smoke-')));
const fail = (message) => {
  process.stderr.write(`shorts smoke: ${message}\n`);
  process.exit(1);
};

// A tone for each phrase, long enough for the whole to be a Short's length: three seconds a
// phrase, each at its own pitch so two clips are never the same bytes.
const doc = JSON.parse(readFileSync(path.join(FIXTURE, 'script.json'), 'utf8'));
const audioDir = path.join(base, 'stand-in-audio');
mkdirSync(audioDir, { recursive: true });
for (const [index] of phrasesOf(doc).entries()) {
  const samples = new Int16Array(48_000 * 3);
  const pitch = 220 + index * 20;
  for (let i = 0; i < samples.length; i++) {
    // Fade the ends so no clip starts or stops on a click.
    const edge = Math.min(1, i / 2400, (samples.length - i) / 2400);
    samples[i] = Math.round(Math.sin((2 * Math.PI * pitch * i) / 48_000) * 9000 * edge);
  }
  writeFileSync(path.join(audioDir, `${String(index).padStart(3, '0')}.wav`), encodeWav(samples));
}

const built = await build({ file: path.join(FIXTURE, 'script.json'), sourceBase: FIXTURE, workdir: base, speech: 'files', audioDir, ...(values.channel ? { channel: values.channel } : {}) });
const report = await runQa({ directory: built.directory, offline: true });
const { metadata, report: packaged } = packageBuild({ directory: built.directory });

const verdicts = Object.fromEntries(report.items.map((each) => [each.id, each]));
const offline = ['narration', 'facts', 'policy', 'links', 'variety'];
for (const each of report.items) {
  const expected = !offline.includes(each.id);
  if (each.ok !== expected) fail(`${each.id} should ${expected ? 'pass' : 'fail without the site'}: ${each.detail}`);
}
if (report.ok) fail('the quality check passed although five items were never checked');
if (report.kind !== 'shorts' || report.line !== 'lab') fail(`the report says ${report.kind}/${report.line}`);
if (!/1080×1920/.test(verdicts.profile.detail)) fail(`profile: ${verdicts.profile.detail}`);
for (const name of ['final.mp4', 'zh-TW.srt', 'cover.png', 'metadata.json', 'description.zh-TW.txt', 'manifest.json']) {
  if (!existsSync(path.join(built.directory, 'upload', name))) fail(`upload/${name} is missing`);
}
if (metadata.final_sha256 !== sha256(readFileSync(built.final))) fail('metadata.json records another cut');
if (metadata.category_id !== '28' || metadata.contains_synthetic_media !== false) fail('the metadata of an experiment is wrong');
// The package's files item wants a quality check of this cut; the other three stand on their own.
const items = Object.fromEntries(packaged.items.map((each) => [each.id, each.ok]));
if (!items.files || !items.descriptions || !items.captions || !items.disclosure) fail(`the package check: ${JSON.stringify(packaged.items)}`);
const manifest = JSON.parse(readFileSync(path.join(built.directory, 'upload', 'manifest.json'), 'utf8'));
if (manifest.status !== 'qa-failed') fail(`the manifest says ${manifest.status}, and the check did not pass`);
process.stdout.write(`shorts smoke: ${built.seconds.toFixed(2)}s, ${report.items.filter((each) => each.ok).length} of ${report.items.length} items checked without the site, package complete\n  ${built.directory}\n`);
