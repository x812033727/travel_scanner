#!/usr/bin/env node
// Draw a video's slide states several times, each in a browser of its own, and say which frames
// came out different. A frame key promises the same picture every time it is drawn
// (2026-10-02-video-render-stills-differ-run-to); this is how to check that promise on a machine.
//
//   node tools/video/render/repeat.mjs --slug <slug> [--channel msedge] [--runs 2] [--scenes id,id] [--out dir]
//
// Nothing is written to the work directory: the frames are compared as bytes in memory (--out
// keeps each run's PNGs in <dir>/run-<n>/). Exits 0 when every run drew every frame alike, 1 when
// some differ (they are listed), 2 on bad usage. Screencast scenes are left out: their captures
// live in the work directory.
import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

import { ROOT } from "../core/paths.mjs";
import { loadProject } from "../core/state.mjs";
import { isScreencast } from "../screencast/steps.mjs";
import { openRenderer } from "./browser.mjs";
import { renderPlan, stillFile, themeHash, transitionFile } from "./plan.mjs";

const md5 = (buffer) => createHash("md5").update(buffer).digest("hex");

/**
 * Draw `states` once in a fresh browser: key -> { still, frames } as md5 hashes. With `out`, the
 * PNGs are also written there, named like the frames directory's, to look at what differs.
 */
export async function drawOnce(states, { channel, root = ROOT, out = null } = {}) {
  const renderer = await openRenderer({ root, channel });
  const drawn = new Map();
  if (out) mkdirSync(out, { recursive: true });
  try {
    for (const state of states) {
      const shot = await renderer.capture(state.key, state.html, { transition: true });
      drawn.set(state.key, { still: md5(shot.still), frames: shot.frames.map(md5) });
      if (!out) continue;
      writeFileSync(path.join(out, path.basename(stillFile(state.key))), shot.still);
      shot.frames.forEach((frame, index) => writeFileSync(path.join(out, path.basename(transitionFile(state.key, index))), frame));
    }
  } finally {
    await renderer.close();
  }
  return drawn;
}

/** Compare runs: counts of identical stills and transition frames, and the keys that differ. */
export function compareRuns(runs) {
  const [first, ...rest] = runs;
  const result = { stills: 0, sameStills: 0, frames: 0, sameFrames: 0, stillsDiffer: [], framesDiffer: [] };
  for (const [key, own] of first) {
    result.stills += 1;
    if (rest.every((run) => run.get(key)?.still === own.still)) result.sameStills += 1;
    else result.stillsDiffer.push(key);
    const differ = [];
    own.frames.forEach((frame, index) => {
      result.frames += 1;
      if (rest.every((run) => run.get(key)?.frames[index] === frame)) result.sameFrames += 1;
      else differ.push(index);
    });
    if (rest.some((run) => run.get(key)?.frames.length !== own.frames.length)) differ.push("count");
    if (differ.length) result.framesDiffer.push(`${key} (${differ.join(",")})`);
  }
  return result;
}

async function main() {
  const { values } = parseArgs({
    options: { slug: { type: "string" }, file: { type: "string" }, channel: { type: "string" }, runs: { type: "string", default: "2" }, scenes: { type: "string" }, out: { type: "string" } },
    strict: true,
  });
  const runs = Number(values.runs);
  if ((!values.slug && !values.file) || !(runs >= 2)) {
    process.stderr.write("usage: repeat.mjs --slug <slug> [--channel msedge] [--runs 2] [--scenes id,id] [--out dir]\n");
    return 2;
  }
  const { doc } = loadProject({ slug: values.slug, file: values.file, root: ROOT });
  // The whole video is planned, so the keys are render's; --scenes only picks what is drawn.
  const plan = renderPlan({ ...doc, scenes: doc.scenes.filter((scene) => !isScreencast(scene)) }, themeHash(), ROOT);
  const only = values.scenes ? new Set(values.scenes.split(",")) : null;
  const picked = plan.scenes.filter((scene) => !only || only.has(scene.id));
  const states = [...new Map(picked.flatMap((scene) => scene.states).map((state) => [state.key, state])).values()];
  const channel = values.channel ?? process.env.VIDEO_BROWSER_CHANNEL;
  const drawn = [];
  for (let run = 0; run < runs; run++) {
    process.stdout.write(`run ${run + 1}/${runs}: drawing ${states.length} states\n`);
    drawn.push(await drawOnce(states, { channel, out: values.out ? path.join(values.out, `run-${run + 1}`) : null }));
  }
  const result = compareRuns(drawn);
  process.stdout.write(`stills ${result.sameStills}/${result.stills} identical, transition frames ${result.sameFrames}/${result.frames} identical\n`);
  for (const key of result.stillsDiffer) process.stdout.write(`still differs: ${key}\n`);
  for (const line of result.framesDiffer) process.stdout.write(`transition frames differ: ${line}\n`);
  return result.stillsDiffer.length || result.framesDiffer.length ? 1 : 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = await main();
}
