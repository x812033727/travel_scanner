#!/usr/bin/env node
// End-to-end smoke test of the Shorts tool with stand-in narration, so it needs neither the
// site, a token nor a speech service: build (from supplied clips) → qa (offline) → package.
//
//   node tools/video/shorts/smoke.mjs [--workdir DIR] [--channel msedge]
//
// What can be checked without the site must pass: the cut's size, frames and loudness, the cards
// inside the safe area, the evidence, the metadata, the captions. What needs the site (the
// listener, Jev, the links, the latest Shorts) must fail saying it was not checked, never pass.
// The script gets what a cut of an illustrated video has (docs/videos/ILLUSTRATED.md): a picture
// scene under a camera move (a stand-in picture, generated here), a music bed and a sound-effect
// set (stand-ins under the work base), so the moving segments, the dissolves, the bed and the
// effects go through the same chain. CI runs it in .github/workflows/video-tooling.yml after
// installing Chromium and ffmpeg.
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

import { locateFfmpeg, runTool } from '../assemble/ffmpeg.mjs';
import { MAX_BED_LUFS } from '../assemble/drama.mjs';
import { writeSyntheticSfx, writeSyntheticTrack } from '../assemble/synthetic.mjs';
import { encodeWav } from '../tts/wav.mjs';
import { build } from './build.mjs';
import { phrasesOf, sha256, validate } from './core.mjs';
import { packageBuild } from './package.mjs';
import { runQa } from './qa.mjs';

const values = parseArgs({ options: { workdir: { type: 'string' }, channel: { type: 'string' } }, strict: true }).values;
const FIXTURE = fileURLToPath(new URL('./fixtures/smoke/', import.meta.url));
const base = path.resolve(values.workdir ?? mkdtempSync(path.join(tmpdir(), 'shorts-smoke-')));
const fail = (message) => {
  process.stderr.write(`shorts smoke: ${message}\n`);
  process.exit(1);
};

// The fixture copied beside the work, with a stand-in picture (a wide gradient, as a keyframe of
// the long video is) that the second scene shows under a push in, and the owner's licensed bed
// and effect set as stand-ins under the work base.
const { ffmpeg } = await locateFfmpeg();
const source = path.join(base, 'source');
cpSync(FIXTURE, source, { recursive: true });
await runTool(ffmpeg, ['-y', '-v', 'error', '-f', 'lavfi', '-i', 'gradients=size=1920x1080:duration=1:speed=0.01:c0=#0b2026:c1=#50d2b7:c2=#ffb36a', '-frames:v', '1', path.join(source, 'evidence', 'picture.png')]);
const pictureBytes = readFileSync(path.join(source, 'evidence', 'picture.png'));
const doc = JSON.parse(readFileSync(path.join(FIXTURE, 'script.json'), 'utf8'));
doc.evidence.push({ path: 'evidence/picture.png', sha256: sha256(pictureBytes) });
doc.scenes[1] = { ...doc.scenes[1], asset: 'evidence/picture.png', camera: 'push in' };
doc.music = { track: 'bed.mp3', gain_db: -22 };
doc.sfx = { set: 'studio-a' };
const invalid = validate(doc);
if (invalid.length) fail(`the smoke script is not valid: ${invalid.join('; ')}`);
writeFileSync(path.join(source, 'script.json'), `${JSON.stringify(doc, null, 2)}\n`);
writeSyntheticTrack(base, 'bed.mp3', ffmpeg);
writeSyntheticSfx(base, 'studio-a', ffmpeg);

// A tone for each phrase, long enough for the whole to be a Short's length: three seconds a
// phrase, each at its own pitch so two clips are never the same bytes.
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

// The captions are the karaoke ones (karaoke.mjs): the layer, its timing file and its warning go
// through the same chain as the picture and the sound.
const built = await build({ file: path.join(source, 'script.json'), sourceBase: source, workdir: base, speech: 'files', audioDir, captions: 'karaoke', ...(values.channel ? { channel: values.channel } : {}) });
const checks = JSON.parse(readFileSync(path.join(built.directory, 'checks.json'), 'utf8'));
// The caption layer: a timing file with every phrase, one state picture per state, the lit group
// moving between the states of a phrase, and the estimate declared as one.
if (checks.captions?.style !== 'karaoke' || checks.captions.source !== 'estimated') fail(`the captions: ${JSON.stringify(checks.captions)}`);
const timing = JSON.parse(readFileSync(path.join(built.directory, 'timing.json'), 'utf8'));
if (timing.source !== 'estimated' || timing.phrases.length !== phrasesOf(doc).length) fail(`timing.json: ${timing.source}, ${timing.phrases?.length} phrases for ${phrasesOf(doc).length}`);
if (!timing.phrases.every((phrase) => phrase.groups.length >= 1 && phrase.states.length >= 1)) fail('a phrase has no group or no state');
const stateFiles = readdirSync(path.join(built.directory, 'captions')).filter((name) => name.endsWith('.png'));
if (stateFiles.length !== checks.captions.states) fail(`${stateFiles.length} caption state pictures for ${checks.captions.states} states`);
const lit = timing.phrases.find((phrase) => phrase.states.length > 1);
if (!lit) fail('no phrase of the smoke script lights in more than one group');
const pictures = new Set(lit.states.map((_state, index) => sha256(readFileSync(path.join(built.directory, 'captions', `${String(lit.cue).padStart(3, '0')}-${String(index).padStart(2, '0')}.png`)))));
if (pictures.size !== lit.states.length) fail(`two caption states of phrase ${lit.cue} are the same picture`);
// The moving picture: one segment per scene, the second on the picture under its push in, every
// later scene opening on a dissolve, and the bed and the effects in the mix.
if (!Array.isArray(checks.motion) || checks.motion.length !== doc.scenes.length) fail(`${checks.motion?.length} moving scenes for ${doc.scenes.length} scenes`);
if (checks.motion[1].background !== 'picture' || checks.motion[1].camera !== 'push-in') fail(`scene 2 is ${JSON.stringify(checks.motion[1])}, not the picture under a push in`);
if (!checks.motion.slice(1).every((scene) => scene.dissolve) || checks.motion[0].dissolve) fail(`dissolves: ${checks.motion.map((scene) => scene.dissolve)}`);
if (checks.motion.filter((scene) => scene.background === 'backdrop').length !== doc.scenes.length - 1) fail('every scene of cards drifts over the backdrop');
if (!(checks.music && checks.music.track === 'bed.mp3' && checks.music.bed_lufs <= MAX_BED_LUFS)) fail(`the music bed: ${JSON.stringify(checks.music)}`);
if (!(checks.sfx && checks.sfx.set === 'studio-a' && checks.sfx.events > 0)) fail(`the sound effects: ${JSON.stringify(checks.sfx)}`);
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
if (!(verdicts.captions.ok && verdicts.captions.warnings?.length === 1 && /estimated/.test(verdicts.captions.warnings[0]))) fail(`captions: ${JSON.stringify(verdicts.captions)}`);
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
process.stdout.write(`shorts smoke: ${built.seconds.toFixed(2)}s, ${checks.motion.length} moving scenes (one on a picture), ${checks.captions.groups} caption groups in ${checks.captions.states} states (${checks.captions.source}), bed ${checks.music.bed_lufs} LUFS, ${checks.sfx.events} effects; ${report.items.filter((each) => each.ok).length} of ${report.items.length} items checked without the site, package complete\n  ${built.directory}\n`);
