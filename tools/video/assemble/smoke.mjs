#!/usr/bin/env node
// End-to-end smoke test of the media stages on an example video, with stand-in narration (and,
// for the drama example, stand-in keyframes, clips and music) so it needs neither the narration
// server, a token nor any media vendor:
// render → assemble (with its own checks) → review → approve the final video → package.
//
//   node tools/video/assemble/smoke.mjs [--fixture minimal|drama] [--workdir DIR] [--channel msedge] [--until assemble]
//
// CI runs both fixtures in .github/workflows/video-tooling.yml after installing Chromium and ffmpeg.
import { existsSync, mkdirSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { isDrama } from "../core/drama.mjs";
import { loadProject } from "../core/state.mjs";
import { locateFfmpeg } from "./ffmpeg.mjs";
import { writeSyntheticClips, writeSyntheticKeyframes, writeSyntheticMusic, writeSyntheticNarration } from "./synthetic.mjs";

const STEPS = ["render", "assemble", "review", "package"];

const values = parseArgs({
  options: { workdir: { type: "string" }, channel: { type: "string" }, until: { type: "string", default: "package" }, fixture: { type: "string", default: "minimal" } },
  strict: true,
}).values;
if (!["minimal", "drama"].includes(values.fixture)) {
  process.stderr.write("smoke: --fixture is minimal or drama\n");
  process.exit(2);
}
const FIXTURE = fileURLToPath(new URL(`../core/fixtures/${values.fixture}/video.json`, import.meta.url));
const base = path.resolve(values.workdir ?? mkdtempSync(path.join(tmpdir(), "video-smoke-")));
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
process.stdout.write(`smoke: ok in ${workdir}\n`);
