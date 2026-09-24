#!/usr/bin/env node
// End-to-end smoke test of the media stages on the minimal example video, with a stand-in
// narration so it needs neither the narration server nor a token:
// render → assemble (with its own checks) → review → approve the final video → package.
//
//   node tools/video/assemble/smoke.mjs [--workdir DIR] [--channel msedge] [--until assemble]
//
// CI runs it in .github/workflows/video-tooling.yml after installing Chromium and ffmpeg.
import { existsSync, mkdirSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { loadProject } from "../core/state.mjs";
import { writeSyntheticNarration } from "./synthetic.mjs";

const FIXTURE = fileURLToPath(new URL("../core/fixtures/minimal/video.json", import.meta.url));
const STEPS = ["render", "assemble", "review", "package"];

const values = parseArgs({ options: { workdir: { type: "string" }, channel: { type: "string" }, until: { type: "string", default: "package" } }, strict: true }).values;
const base = path.resolve(values.workdir ?? mkdtempSync(path.join(tmpdir(), "video-smoke-")));
const project = loadProject({ file: FIXTURE });
const workdir = path.join(base, project.doc.slug);
mkdirSync(workdir, { recursive: true });
writeSyntheticNarration(project.doc, project.lexicon, workdir);

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
