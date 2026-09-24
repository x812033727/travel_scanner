// `render`: draw every slide state of a video into <VIDEO_WORKDIR>/<slug>/frames/.
//
// Writes frames/manifest.json with the visual hash status compares, the thumbnail, and a contact
// sheet. Frames are cached by content key, so a rerun after editing one scene redraws that scene
// only. A STOP file ends the run after the current scene; the next run picks up from the cache.
import { existsSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { atomicWrite, resolveWorkdir, stopRequested, UsageError } from "../core/paths.mjs";
import { lintProject, loadProject, recordStage, ARTIFACTS } from "../core/state.mjs";
import { visualHash } from "../core/timeline.mjs";
import { SIZE, THUMB_SIZE } from "../templates/templates.mjs";
import { openRenderer, RendererError } from "./browser.mjs";
import { contactSheetHtml, SHEET_WIDTH } from "./contact.mjs";
import { bundledCoverage, uncovered } from "./fonts.mjs";
import { renderPlan, renderProblems, stillFile, themeHash, transitionFile } from "./plan.mjs";

export const THUMBNAIL_FILE = "thumbnail.jpg";
export const THUMBNAIL_MAX_BYTES = 2 * 1024 * 1024;
const CACHE_FILE = path.join("frames", "cache.json");

function print(out, label, problems) {
  for (const problem of problems) out.write(`${label} ${problem.path}: ${problem.message}\n`);
}

/** Characters no bundled font covers, per scene state. */
export function coverageProblems(plan, coverage) {
  const problems = [];
  for (const scene of plan.scenes) {
    scene.states.forEach((state, index) => {
      const missing = uncovered(state.text, coverage);
      if (missing.length) problems.push({ path: `${scene.id} state ${index}`, message: `no bundled font has ${missing.map((char) => `"${char}" U+${char.codePointAt(0).toString(16).toUpperCase()}`).join(", ")}` });
    });
  }
  const missing = plan.thumbnail ? uncovered(plan.thumbnail.text, coverage) : [];
  if (missing.length) problems.push({ path: "thumbnail", message: `no bundled font has ${missing.join(" ")}` });
  return problems;
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({
    args,
    options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" }, channel: { type: "string" }, force: { type: "boolean" } },
    strict: true,
  }).values;
  if (!values.slug && !values.file) throw new UsageError("render needs --slug (or --file for an example outside docs/videos)");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const slug = project.doc.slug;
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  const { doc } = project;
  const dataProblems = renderProblems(doc, ctx.root);
  if (dataProblems.length) {
    print(ctx.stdout, "ERROR", dataProblems);
    return EXIT.lint;
  }
  const plan = renderPlan(doc, themeHash(), ctx.root);
  const glyphs = coverageProblems(plan, bundledCoverage());
  if (glyphs.length) {
    print(ctx.stdout, "ERROR", glyphs);
    return EXIT.lint;
  }

  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug, root: ctx.root });
  mkdirSync(path.join(workdir, "frames"), { recursive: true });
  const cacheFile = path.join(workdir, CACHE_FILE);
  const cache = values.force || !existsSync(cacheFile) ? {} : JSON.parse(readFileSync(cacheFile, "utf8"));
  const started = Date.now();
  const layout = [];
  let drawn = 0;
  let reused = 0;
  let stopped = false;
  const channel = values.channel ?? ctx.env.VIDEO_BROWSER_CHANNEL;
  let renderer;
  try {
    renderer = await openRenderer({ root: ctx.root, workdir, channel });
  } catch (error) {
    if (!(error instanceof RendererError)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return EXIT.missing;
  }
  try {
    for (const scene of plan.scenes) {
      if (stopRequested(workdir)) {
        stopped = true;
        break;
      }
      for (const state of scene.states) {
        const known = cache[state.key];
        const files = known ? [stillFile(state.key), ...Array.from({ length: known.transition }, (_, index) => transitionFile(state.key, index))] : [];
        if (known && files.every((file) => existsSync(path.join(workdir, file)))) {
          reused += 1;
          continue;
        }
        const shot = await renderer.capture(state.key, state.html, { transition: true });
        for (const problem of shot.problems) layout.push({ path: `${scene.id} state ${scene.states.indexOf(state)}`, message: problem });
        writeFileSync(path.join(workdir, stillFile(state.key)), shot.still);
        shot.frames.forEach((frame, index) => writeFileSync(path.join(workdir, transitionFile(state.key, index)), frame));
        cache[state.key] = { transition: shot.frames.length, problems: shot.problems };
        drawn += 1;
      }
      atomicWrite(cacheFile, `${JSON.stringify(cache)}\n`);
    }
    if (!stopped && plan.thumbnail) {
      const thumb = await renderer.capture(plan.thumbnail.key, plan.thumbnail.html, { size: THUMB_SIZE, type: "jpeg", quality: 90 });
      for (const problem of thumb.problems) layout.push({ path: "thumbnail", message: problem });
      if (thumb.still.length > THUMBNAIL_MAX_BYTES) layout.push({ path: "thumbnail", message: `${thumb.still.length} bytes; YouTube's mobile upload limit is 2 MB` });
      writeFileSync(path.join(workdir, THUMBNAIL_FILE), thumb.still);
    }
    // Problems found in an earlier run stay problems until the state is redrawn.
    for (const scene of plan.scenes) {
      scene.states.forEach((state, index) => {
        if (cache[state.key]?.problems?.length && !layout.some((problem) => problem.path === `${scene.id} state ${index}`)) {
          for (const message of cache[state.key].problems) layout.push({ path: `${scene.id} state ${index}`, message });
        }
      });
    }
    if (!stopped) {
      const tiles = plan.scenes.flatMap((scene) => scene.states.map((state, index) => ({ file: stillFile(state.key), label: `${scene.id} · ${scene.template} · ${index + 1}/${scene.states.length}` })));
      writeFileSync(path.join(workdir, ARTIFACTS.contactSheet), await renderer.sheet(contactSheetHtml(`${doc.slug}：${tiles.length} slide states`, tiles), SHEET_WIDTH));
    }
  } finally {
    await renderer.close();
  }

  const seconds = Math.round((Date.now() - started) / 1000);
  if (stopped) {
    ctx.stdout.write(`stopped by the STOP file after ${drawn} new states; rerun to continue from the cache\n`);
    return EXIT.ok;
  }
  if (layout.length) {
    print(ctx.stdout, "ERROR", layout);
    ctx.stdout.write(`${layout.length} layout problems; frames are cached, fix the scenes and rerun\n`);
    return EXIT.lint;
  }
  const manifest = {
    visual_hash: visualHash(doc),
    theme_hash: themeHash(),
    fps: 30,
    size: SIZE,
    scenes: plan.scenes.map((scene) => ({
      id: scene.id,
      states: scene.states.map((state) => ({
        reveal: state.reveal,
        still: stillFile(state.key),
        transition: Array.from({ length: cache[state.key].transition }, (_, index) => transitionFile(state.key, index)),
      })),
    })),
    thumbnail: plan.thumbnail ? THUMBNAIL_FILE : null,
  };
  atomicWrite(path.join(workdir, ARTIFACTS.frames), `${JSON.stringify(manifest, null, 2)}\n`);
  recordStage(workdir, "render", { states: drawn + reused, drawn, reused, seconds, channel: channel ?? "bundled chromium" }, ctx.now());
  ctx.stdout.write(`${drawn} states drawn, ${reused} reused, in ${seconds} s; contact sheet: ${path.join(workdir, ARTIFACTS.contactSheet)}\n`);
  return EXIT.ok;
}
