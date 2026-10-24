// Nonpaid C20 v8 source, schema, and estimated visual preflight.
// Exit 3 records known production holds; it never spends or imports.
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { validateVideo } from "../../../tools/video/core/schema.mjs";
import { storyCuteVisualProblems } from "../../../tools/video/core/story.mjs";
import { estimateTimeline, FPS } from "../../../tools/video/core/timeline.mjs";
import { loadProject, lintProject } from "../../../tools/video/core/state.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../../..");
execFileSync(process.execPath, [path.join(here, "build.mjs"), "--check"], { stdio: "inherit" });
const file = path.join(here, "video.json");
const doc = JSON.parse(readFileSync(file, "utf8"));
const schema = validateVideo(doc);
const visual = storyCuteVisualProblems(doc);
if (schema.length || visual.length) throw new Error(JSON.stringify({ schema, visual }));
const timeline = estimateTimeline(doc);
const bodyFrames = timeline.scenes.at(-1).end_frame;
const stillIds = new Set(doc.scenes.filter((scene) => scene.template === "shot").map((scene) => scene.id));
const stillFrames = timeline.scenes.filter((scene) => stillIds.has(scene.id))
  .reduce((total, scene) => total + scene.end_frame - scene.start_frame, 0);
const lint = lintProject(loadProject({ file, root }));
const knownHolds = [
  /starts at 5 minutes; every episode but a drama's runs at least 8/,
  /every episode but a drama's runs at least 8: write more narration/,
];
const unexpected = lint.errors.filter((error) => !knownHolds.some((pattern) => pattern.test(error.message)));
const report = {
  result: unexpected.length ? "FAIL" : lint.errors.length ? "HOLD" : "PASS",
  scenes: doc.scenes.length,
  stills: stillIds.size,
  cards: doc.scenes.length - stillIds.size,
  schema_errors: schema.length,
  visual_errors: visual.length,
  paper_body_frames: bodyFrames,
  paper_body_seconds: Number((bodyFrames / FPS).toFixed(3)),
  paper_still_share: Number((stillFrames / bodyFrames).toFixed(5)),
  lint_errors: lint.errors,
  lint_warnings: lint.warnings.length,
  note: "Estimated frames are not measured speech or final-cut proof.",
};
console.log(JSON.stringify(report, null, 2));
if (unexpected.length) process.exitCode = 1;
else if (lint.errors.length) process.exitCode = 3;
