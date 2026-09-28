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
import { isDrama, isShot } from "../core/drama.mjs";
import { loadProject } from "../core/state.mjs";
import { locateFfmpeg } from "./ffmpeg.mjs";
import { writeSyntheticClips, writeSyntheticKeyframes, writeSyntheticMusic, writeSyntheticNarration } from "./synthetic.mjs";

const STEPS = ["render", "assemble", "review", "package"];
const FIXTURES = ["minimal", "drama", "story"];

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
process.stdout.write(`smoke: ok in ${workdir}\n`);
