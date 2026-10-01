#!/usr/bin/env node
// End-to-end smoke test of the media stages on an example video, with stand-in narration (and,
// for the drama and story examples, stand-in keyframes, clips and music) so it needs neither the
// narration server, a token nor any media vendor:
// render → assemble (with its own checks) → review → approve the final video → package.
// The drama example runs from a copy with its first shot marked visual "still", so assemble also
// encodes one motion segment (the keyframe under a push-in) beside the clips. The story example
// (docs/videos/STORY.md) is narrator-only and every shot is a still, so its cut must be motion
// segments only: checks.json is read back to prove it.
//
//   node tools/video/assemble/smoke.mjs [--fixture minimal|drama|story] [--workdir DIR] [--channel msedge] [--until assemble]
//
// CI runs all three fixtures in .github/workflows/video-tooling.yml after installing Chromium and ffmpeg.
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { illustrated, isDrama, isShot } from "../core/drama.mjs";
import { loadProject } from "../core/state.mjs";
import { locateFfmpeg } from "./ffmpeg.mjs";
import { writeSyntheticClips, writeSyntheticKeyframes, writeSyntheticMusic, writeSyntheticNarration, writeSyntheticSfx, writeSyntheticTrack } from "./synthetic.mjs";

// The fixtures run seconds, under the eight-minute floor lint and qa keep for real episodes.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const STEPS = ["render", "assemble", "review", "package"];
// illustrated (docs/videos/ILLUSTRATED.md): slides with still shots between the cards, the owner's
// music file and a sound-effect set, so assemble mixes motion segments, drifting cards,
// dissolves, a music bed and the effects.
const FIXTURES = ["minimal", "drama", "story", "illustrated"];

const values = parseArgs({
  options: { workdir: { type: "string" }, channel: { type: "string" }, until: { type: "string", default: "package" }, fixture: { type: "string", default: "minimal" } },
  strict: true,
}).values;
if (!FIXTURES.includes(values.fixture)) {
  process.stderr.write(`smoke: --fixture is ${FIXTURES.join(", ")}\n`);
  process.exit(2);
}
const EXAMPLE = fileURLToPath(new URL(`../core/fixtures/${values.fixture}/video.json`, import.meta.url));
const base = path.resolve(values.workdir ?? mkdtempSync(path.join(tmpdir(), "video-smoke-")));
let FIXTURE = EXAMPLE;
if (values.fixture === "drama") {
  // A copy beside a copy of the shared lexicon (loadProject reads it from the parent directory),
  // with the opening shot as a still: the example itself keeps every shot a clip for the tests.
  const dir = path.join(base, "example", "drama");
  cpSync(path.dirname(EXAMPLE), dir, { recursive: true });
  cpSync(path.join(path.dirname(EXAMPLE), "..", "lexicon.json"), path.join(base, "example", "lexicon.json"));
  const doc = JSON.parse(readFileSync(EXAMPLE, "utf8"));
  doc.scenes.find((scene) => scene.template === "shot").data.visual = "still";
  FIXTURE = path.join(dir, "video.json");
  writeFileSync(FIXTURE, `${JSON.stringify(doc, null, 2)}\n`);
}
const project = loadProject({ file: FIXTURE });
const workdir = path.join(base, project.doc.slug);
mkdirSync(workdir, { recursive: true });
const timeline = writeSyntheticNarration(project.doc, project.lexicon, workdir);
if (isDrama(project.doc)) {
  const tools = await locateFfmpeg(process.env);
  writeSyntheticKeyframes(project.doc, workdir, tools.ffmpeg);
  writeSyntheticClips(project.doc, timeline, project.lexicon, workdir, tools.ffmpeg);
  writeSyntheticMusic(project.doc, workdir, tools.ffmpeg);
} else if (illustrated(project.doc)) {
  const tools = await locateFfmpeg(process.env);
  writeSyntheticKeyframes(project.doc, workdir, tools.ffmpeg);
  if (project.doc.music?.track) writeSyntheticTrack(base, project.doc.music.track, tools.ffmpeg);
  if (project.doc.sfx?.set) writeSyntheticSfx(base, project.doc.sfx.set, tools.ffmpeg);
}

const common = ["--file", FIXTURE, "--workdir", base];
for (const step of STEPS.slice(0, STEPS.indexOf(values.until) + 1)) {
  if (step === "package") await approve({ gate: "final", docDir: path.dirname(FIXTURE), workdir, note: "smoke test" });
  const args = step === "render" && values.channel ? [...common, "--channel", values.channel] : common;
  const code = await main([step, ...args]);
  if (code !== 0) {
    process.stderr.write(`smoke: ${step} exited ${code}\n`);
    process.exit(1);
  }
}
const expected = { render: "frames/manifest.json", assemble: "checks.json", review: "review/audio.html", package: "upload/metadata.json" };
for (const step of STEPS.slice(0, STEPS.indexOf(values.until) + 1)) {
  if (!existsSync(path.join(workdir, expected[step]))) {
    process.stderr.write(`smoke: ${step} did not write ${expected[step]}\n`);
    process.exit(1);
  }
}
if (values.fixture === "story" && STEPS.indexOf(values.until) >= STEPS.indexOf("assemble")) {
  // A story buys no clip: every shot of its cut is a motion segment, its keyframe under a move.
  const shots = JSON.parse(readFileSync(path.join(workdir, expected.assemble), "utf8")).metrics?.shots ?? [];
  const wanted = project.doc.scenes.filter(isShot).length;
  if (shots.length !== wanted || shots.some((shot) => shot.kind !== "motion")) {
    process.stderr.write(`smoke: the story's cut should be ${wanted} motion shots; checks.json has ${shots.map((shot) => `${shot.shot}=${shot.kind}`).join(", ") || "none"}\n`);
    process.exit(1);
  }
  process.stdout.write(`smoke: ${wanted} motion shots (${[...new Set(shots.map((shot) => shot.move))].join(", ")})\n`);
}
if (values.fixture === "illustrated" && STEPS.indexOf(values.until) >= STEPS.indexOf("assemble")) {
  // Every shot is a motion segment, single-state cards drift, at least one picture dissolves in,
  // the bed sits under the voice and the effects fall on the cut's beats.
  const checks = JSON.parse(readFileSync(path.join(workdir, expected.assemble), "utf8"));
  const shots = checks.metrics?.shots ?? [];
  const wantedShots = project.doc.scenes.filter(isShot).map((scene) => scene.id);
  const problems = [];
  for (const id of wantedShots) if (!shots.some((shot) => shot.shot === id && shot.kind === "motion" && !shot.card)) problems.push(`shot ${id} is not a motion segment`);
  if (!shots.some((shot) => shot.card)) problems.push("no card drifts");
  if (!shots.some((shot) => shot.transition === "dissolve")) problems.push("no dissolve");
  if (!(checks.metrics?.music_bed_lufs <= -24)) problems.push(`music bed ${checks.metrics?.music_bed_lufs} LUFS`);
  if (!(checks.metrics?.sfx?.events > 0)) problems.push("no sound effect placed");
  for (const key of ["look_hash", "pictures_hash", "mix_hash", "sfx_hash"]) if (!checks[key]) problems.push(`checks.json has no ${key}`);
  if (problems.length) {
    process.stderr.write(`smoke: the illustrated cut is wrong: ${problems.join("; ")}\n`);
    process.exit(1);
  }
  process.stdout.write(`smoke: ${wantedShots.length} motion shots, ${shots.filter((shot) => shot.card).length} drifting cards, ${shots.filter((shot) => shot.transition === "dissolve").length} dissolves, bed ${checks.metrics.music_bed_lufs} LUFS, ${checks.metrics.sfx.events} effects\n`);
}
process.stdout.write(`smoke: ok in ${workdir}\n`);
