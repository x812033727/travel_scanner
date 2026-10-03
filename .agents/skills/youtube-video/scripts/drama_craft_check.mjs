#!/usr/bin/env node
// Craft check for one drama episode with a cast: is the storyboard structured the way the
// dramas that were measured are, before any picture is paid for?
//
//   node .agents/skills/youtube-video/scripts/drama_craft_check.mjs <file> [--json] [--strict]
//
// <file> is a drama `video.json` (lengths are estimated from the lines, the way `lint` does) or a
// measured edit (`shots[]` with `editorial_duration_s`, as the competition pilot writes them).
// It prints one row per check: the value, the target, what the reference dramas measured, and
// under a missed row the shots that cause it. --json adds one entry per shot (how its size, its
// camera move and its motion were read), which is how a misreading is found.
// Exit code 0 unless --strict is given and a check missed (1); 2 when the file cannot be read.
//
// `lint` answers "can the pipeline build this"; this answers "is the storyboard built like the
// ones that were measured". The reading itself lives in tools/video/core/craft.mjs, which `lint`
// prints as warnings and the worker's script verdict reads, so the three never disagree; this
// file is the command, run from a repository checkout. Every target comes from
// .agents/skills/youtube-video/references/drama-craft.md, which records where the numbers were
// measured, which targets are editorial rules, and what none of them prove. A miss is a question
// the writer answers in the report (fix it, or say why this episode is different); it blocks no
// command, and it is never a reason to lower a target for one episode.
//
// The shot-size, camera-move and motion rows read the English `camera`, `prompt` and `motion`
// text, so they are heuristics. They agree with a shot-by-shot hand reading of the 81 pilot
// shots on 80 sizes and 81 motions (the study record has the comparison); a shot that names no
// size counts as unknown rather than guessed; and meeting every row says the storyboard is
// structured, not that the picture is good.
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { craftChecks, renderCraftReport } from "../../../../tools/video/core/craft.mjs";

export { CPM, PAUSE_MS, SCENE_GAP_MS, SILENT_SHOT_SECONDS, TARGETS, REFERENCE, CRAFT_GATE_ROWS, cameraMove, craftChecks, isLookOnly, normalize, quantile, shotSize, sizesDisagree, spokenUnits } from "../../../../tools/video/core/craft.mjs";

function main(argv) {
  const flags = new Set(argv.filter((arg) => arg.startsWith("--")));
  const file = argv.find((arg) => !arg.startsWith("--"));
  if (!file) {
    console.error("usage: drama_craft_check.mjs <video.json | measured-edit.json> [--json] [--strict]");
    return 2;
  }
  let report;
  try {
    report = craftChecks(JSON.parse(readFileSync(file, "utf8")));
  } catch (error) {
    console.error(`${file}: ${error.message}`);
    return 2;
  }
  console.log(flags.has("--json") ? JSON.stringify(report, null, 2) : renderCraftReport(report, file));
  return flags.has("--strict") && report.checks.some((check) => !check.ok) ? 1 : 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) process.exitCode = main(process.argv.slice(2));
