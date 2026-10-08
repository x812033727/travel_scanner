#!/usr/bin/env node
// A real, offline media check with the owner's selected bookends. Creates a ten-second blue
// body with a steady test tone, checks the WAV sample grid, unchanged quiet body and frame count
// of the MP4, and leaves the files, seam stills and JSON evidence outside the repository.
// node tools/video/assemble/branding-smoke.mjs --assets <package-directory> --workdir <evidence-directory>
import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { sha256File } from "../core/approvals.mjs";
import { presentationTimeline, validateBranding } from "../core/branding.mjs";
import { isInside, ROOT } from "../core/paths.mjs";
import { toSrt } from "../core/captions.mjs";
import { buildCues } from "../core/captions.mjs";
import { parseWav } from "../tts/wav.mjs";
import { wrapAudio, wrapVideo } from "./branding.mjs";
import { locateFfmpeg, runTool } from "./ffmpeg.mjs";
import { checkProbe, ebur128Args, parseEbur128, probeArgs, segmentArgs } from "./plan.mjs";

const values = parseArgs({ options: { assets: { type: "string" }, workdir: { type: "string" } }, strict: true }).values;
if (!values.assets || !values.workdir) throw new Error("branding smoke needs --assets and --workdir");
const assets = path.resolve(values.assets);
const workdir = path.resolve(values.workdir);
if (isInside(workdir, ROOT)) throw new Error("smoke media must stay outside the repository");
mkdirSync(workdir, { recursive: true });
const source = JSON.parse(readFileSync(path.join(assets, "manifest.json"), "utf8").replace(/^\uFEFF/, ""));
const branding = validateBranding({ schema_version: 1, id: source.package_id, ...Object.fromEntries(source.assets.map((clip) => [clip.role, { file: path.join(assets, clip.file), sha256: clip.sha256, frames: clip.frames }])) });
assert.equal(branding.intro.frames, 150);
assert.equal(branding.outro.frames, 90);
const tools = await locateFfmpeg();
const body = path.join(workdir, "body.mp4");
const settings = segmentArgs("unused", body, 300);
const picture = settings.slice(settings.indexOf("-vf"), settings.indexOf("-an"));
await runTool(tools.ffmpeg, ["-hide_banner", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=0x1e5ae8:s=1920x1080:r=30:d=10", "-f", "lavfi", "-i", "sine=frequency=997:sample_rate=48000:duration=10", "-map", "0:v:0", "-map", "1:a:0", ...picture, "-af", "pan=stereo|c0=c0|c1=c0,loudnorm=I=-14:TP=-1:LRA=11,aresample=48000", "-c:a", "aac", "-b:a", "384k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", body]);
const bodyBefore = await sha256File(body);
assert.deepEqual(checkProbe(JSON.parse((await runTool(tools.ffprobe, probeArgs(body))).stdout), { frames: 300 }), []);
const final = path.join(workdir, "final.mp4");
const applied = await wrapVideo({ tools, workdir, bodyFile: body, bodyFrames: 300, branding, outFile: final });
const probe = JSON.parse((await runTool(tools.ffprobe, probeArgs(final))).stdout);
assert.deepEqual(checkProbe(probe, { frames: 540 }), []);
const loudness = parseEbur128((await runTool(tools.ffmpeg, ebur128Args(final))).stderr);
assert.ok(loudness.truePeak <= -1, `decoded AAC peak ${loudness.truePeak} dBTP exceeds -1`);
assert.equal(await sha256File(body), bodyBefore);
const wavFile = path.join(workdir, "dub.wav");
await wrapAudio({ tools, bodyFile: body, bodyFrames: 300, branding, outFile: wavFile, outputCodec: ["-c:a", "pcm_s16le"] });
const wav = parseWav(readFileSync(wavFile));
assert.equal(wav.channels, 2);
assert.equal(wav.sampleRate, 48000);
assert.equal(wav.samples.length / wav.channels, 864000);
const comparisons = [];
let cursor = 0;
for (const [role, clip] of [["intro", branding.intro], ["body", { file: body, frames: 300 }], ["outro", branding.outro]]) {
  const expectedFile = path.join(workdir, `${role}-decoded.wav`);
  const samples = clip.frames * 1600;
  await runTool(tools.ffmpeg, ["-hide_banner", "-y", "-loglevel", "error", "-i", clip.file, "-vn", "-af", `aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,atrim=end_sample=${samples},apad=whole_len=${samples},atrim=end_sample=${samples}`, "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", expectedFile]);
  const expected = parseWav(readFileSync(expectedFile));
  assert.equal(expected.samples.length, samples * 2);
  let changedSamples = 0;
  let maximumDifference = 0;
  let bodyInteriorDifference = 0;
  for (let i = 0; i < expected.samples.length; i++) {
    const difference = Math.abs(expected.samples[i] - wav.samples[cursor * 2 + i]);
    if (difference) changedSamples++;
    maximumDifference = Math.max(maximumDifference, difference);
    // Bookend transients may be limited; the quiet body is unity gain and is checked at its
    // original absolute sample offset, away from resampling/limiter boundary transients.
    if (role === "body" && i >= 9600 && i < expected.samples.length - 9600) bodyInteriorDifference = Math.max(bodyInteriorDifference, difference);
  }
  if (role === "body") assert.ok(bodyInteriorDifference <= 3, `body at sample ${cursor} was moved or amplified (PCM error ${bodyInteriorDifference})`);
  comparisons.push({ role, start_sample: cursor, samples_per_channel: samples, changed_samples: changedSamples, maximum_pcm_difference: maximumDifference, ...(role === "body" ? { interior_pcm_difference: bodyInteriorDifference } : {}) });
  cursor += samples;
}
const bodyTimeline = { fps: 30, sample_rate: 48000, total_frames: 300, lines: [{ id: "tone", start_frame: 0, end_frame: 300, audio_samples: 480000 }], scenes: [], chapters: [{ title: "Test body", start_frame: 0 }] };
const full = presentationTimeline(bodyTimeline, applied);
assert.equal(full.total_frames, 540);
assert.equal(full.lines[0].start_frame, 150);
assert.equal(full.content_end_frame, 450);
assert.equal(full.chapters[0].start_frame, 0);
const { cues } = buildCues(full, { tone: "Test body" }, "en");
assert.equal(cues[0].start_ms, 5000);
assert.equal(cues.at(-1).end_ms, 15000);
writeFileSync(path.join(workdir, "en.srt"), toSrt(cues));
for (const frame of [149, 150, 449, 450]) await runTool(tools.ffmpeg, ["-hide_banner", "-y", "-loglevel", "error", "-i", final, "-vf", `select=eq(n\\,${frame})`, "-frames:v", "1", path.join(workdir, `seam-${frame}.png`)]);
const report = { ok: true, checked_at: new Date().toISOString(), tools: tools.version, branding: applied, body_sha256_unchanged: bodyBefore, final_sha256: await sha256File(final), frames: 540, seconds: 18, intro_frames: 150, body_frames: 300, outro_frames: 90, wav_samples_per_channel: 864000, audio_segments: comparisons, loudness, caption_start_ms: 5000, caption_end_ms: 15000, chapter_start_frame: 0, source_timeline: bodyTimeline, presentation_timeline: full, probe, human_listening: "not asserted by this automated smoke" };
writeFileSync(path.join(workdir, "evidence.json"), `${JSON.stringify(report, null, 2)}\n`);
console.log(`branding smoke passed: 540 frames / 18 seconds, 864000 samples per channel, quiet body aligned at 5 seconds, decoded peak ${loudness.truePeak} dBTP; ${workdir}`);
