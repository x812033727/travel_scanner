// `render`: draw every slide state of a video into <VIDEO_WORKDIR>/<slug>/frames/.
//
// Writes frames/manifest.json with the visual hash status compares, the thumbnail, and a contact
// sheet. Frames are cached by content key, so a rerun after editing one scene redraws that scene
// only. A STOP file ends the run after the current scene; the next run picks up from the cache.
// A drama's shots are clips the media stages make, so render draws only its cards, its subtitle
// strips (when they are burned in) and its thumbnail, on the chosen shot's keyframe.
import { existsSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { burnIn, isDrama, subtitlesHash } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkdir, stopRequested, UsageError } from "../core/paths.mjs";
import { lintProject, loadProject, recordStage, ARTIFACTS } from "../core/state.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { SIZE, THUMB_SIZE } from "../templates/templates.mjs";
import { openRenderer, RendererError } from "./browser.mjs";
import { contactSheetHtml, SHEET_WIDTH } from "./contact.mjs";
import { bundledCoverage, uncovered } from "./fonts.mjs";
import { renderPlan, renderProblems, stillFile, themeHash, transitionFile } from "./plan.mjs";
import { BLANK_STRIP, blankStripHtml, blankStripKey, STRIP_SIZE, stripFile, subtitlePlan } from "./subtitles.mjs";

export const THUMBNAIL_FILE = "thumbnail.jpg";
export const THUMBNAIL_MAX_BYTES = 2 * 1024 * 1024;
const CACHE_FILE = path.join("frames", "cache.json");

function print(out, label, problems) {
  for (const problem of problems) out.write(`${label} ${problem.path}: ${problem.message}\n`);
}

const glyphList = (missing) => missing.map((char) => `"${char}" U+${char.codePointAt(0).toString(16).toUpperCase()}`).join(", ");

/** Characters no bundled font covers, per scene state, subtitle strip and the thumbnail. */
export function coverageProblems(plan, coverage, subtitles = null) {
  const problems = [];
  for (const scene of plan.scenes) {
    scene.states.forEach((state, index) => {
      const missing = uncovered(state.text, coverage);
      if (missing.length) problems.push({ path: `${scene.id} state ${index}`, message: `no bundled font has ${glyphList(missing)}` });
    });
  }
  for (const strip of subtitles?.strips ?? []) {
    const missing = uncovered(strip.text, coverage);
    if (missing.length) problems.push({ path: `subtitle "${strip.text}"`, message: `no bundled font has ${glyphList(missing)}` });
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
  const { doc, lexicon } = project;
  const dataProblems = renderProblems(doc, ctx.root);
  if (dataProblems.length) {
    print(ctx.stdout, "ERROR", dataProblems);
    return EXIT.lint;
  }
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug, root: ctx.root });
  const drama = isDrama(doc);
  // Burned-in subtitles are cut and timed to the narration, like the captions, so a drama's
  // strips need the timeline the tts stage wrote for this very script.
  let subtitles = null;
  if (drama && burnIn(doc)) {
    const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
    if (!timeline || timeline.speech_hash !== speechHash(doc, lexicon)) {
      ctx.stderr.write("timeline.json is missing or was built for an older script; run tts first (the burned-in subtitles follow the narration)\n");
      return EXIT.usage;
    }
    subtitles = subtitlePlan(doc, timeline);
  }
  const keyframes = drama ? (readJson(path.join(workdir, ARTIFACTS.keyframes), null)?.shots ?? {}) : {};
  const plan = renderPlan(doc, themeHash(), ctx.root, { keyframes });
  if (plan.thumbnail?.shot && !plan.thumbnail.keyframe) {
    ctx.stderr.write(`the thumbnail's background is the keyframe of shot ${plan.thumbnail.shot}, which is not drawn yet; run keyframes first\n`);
    return EXIT.usage;
  }
  const glyphs = coverageProblems(plan, bundledCoverage(), subtitles);
  if (glyphs.length) {
    print(ctx.stdout, "ERROR", glyphs);
    return EXIT.lint;
  }

  mkdirSync(path.join(workdir, "frames"), { recursive: true });
  const cacheFile = path.join(workdir, CACHE_FILE);
  const cache = values.force || !existsSync(cacheFile) ? {} : JSON.parse(readFileSync(cacheFile, "utf8"));
  const started = Date.now();
  const layout = [];
  let drawn = 0;
  let reused = 0;
  let stopped = false;
  const channel = values.channel ?? ctx.env.VIDEO_BROWSER_CHANNEL;
  // The contact sheet shows the slide states; a drama's shots get theirs from the keyframes
  // stage, so a drama with no cards has no sheet here.
  const tiles = plan.scenes.flatMap((scene) => scene.states.map((state, index) => ({ file: stillFile(state.key), label: `${scene.id} · ${scene.template} · ${index + 1}/${scene.states.length}` })));
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
    if (!stopped && subtitles) {
      for (const strip of subtitles.strips) {
        if (stopRequested(workdir)) {
          stopped = true;
          break;
        }
        if (cache[strip.key] && existsSync(path.join(workdir, stripFile(strip.key)))) {
          reused += 1;
          continue;
        }
        const shot = await renderer.capture(strip.key, strip.html, { size: STRIP_SIZE, omitBackground: true });
        for (const problem of shot.problems) layout.push({ path: `subtitle "${strip.text}"`, message: problem });
        writeFileSync(path.join(workdir, stripFile(strip.key)), shot.still);
        cache[strip.key] = { transition: 0, problems: shot.problems, strip: strip.text };
        drawn += 1;
      }
      atomicWrite(cacheFile, `${JSON.stringify(cache)}\n`);
      if (!stopped && !existsSync(path.join(workdir, BLANK_STRIP))) {
        const blank = await renderer.capture(blankStripKey(), blankStripHtml(), { size: STRIP_SIZE, omitBackground: true });
        writeFileSync(path.join(workdir, BLANK_STRIP), blank.still);
      }
    }
    if (!stopped && plan.thumbnail) {
      const thumb = await renderer.capture(plan.thumbnail.key, plan.thumbnail.html, { size: THUMB_SIZE, type: "jpeg", quality: 90 });
      for (const problem of thumb.problems) layout.push({ path: "thumbnail", message: problem });
      if (thumb.still.length > THUMBNAIL_MAX_BYTES) layout.push({ path: "thumbnail", message: `${thumb.still.length} bytes; YouTube's mobile upload limit is 2 MB` });
      writeFileSync(path.join(workdir, THUMBNAIL_FILE), thumb.still);
    }
    // Problems found in an earlier run stay problems until the state is redrawn.
    const remembered = (key, where) => {
      if (cache[key]?.problems?.length && !layout.some((problem) => problem.path === where)) {
        for (const message of cache[key].problems) layout.push({ path: where, message });
      }
    };
    for (const scene of plan.scenes) scene.states.forEach((state, index) => remembered(state.key, `${scene.id} state ${index}`));
    for (const strip of subtitles?.strips ?? []) remembered(strip.key, `subtitle "${strip.text}"`);
    if (!stopped && tiles.length) {
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
      kind: scene.kind,
      states: scene.states.map((state) => ({
        reveal: state.reveal,
        still: stillFile(state.key),
        transition: Array.from({ length: cache[state.key].transition }, (_, index) => transitionFile(state.key, index)),
      })),
    })),
    thumbnail: plan.thumbnail ? THUMBNAIL_FILE : null,
    // Burned-in subtitles follow the narration, so status compares these two hashes as well.
    ...(subtitles
      ? {
          speech_hash: speechHash(doc, lexicon),
          subtitles_hash: subtitlesHash(doc),
          subtitles: {
            style: subtitles.style,
            size: STRIP_SIZE,
            blank: BLANK_STRIP,
            cues: subtitles.cues.map((cue) => ({ line: cue.line, start_frame: cue.start_frame, end_frame: cue.end_frame, text: cue.text, file: stripFile(cue.key) })),
          },
        }
      : {}),
  };
  atomicWrite(path.join(workdir, ARTIFACTS.frames), `${JSON.stringify(manifest, null, 2)}\n`);
  const strips = subtitles ? subtitles.strips.length : 0;
  recordStage(workdir, "render", { states: drawn + reused, drawn, reused, strips, seconds, channel: channel ?? "bundled chromium" }, ctx.now());
  const sheet = tiles.length ? `; contact sheet: ${path.join(workdir, ARTIFACTS.contactSheet)}` : "";
  ctx.stdout.write(`${drawn} states drawn, ${reused} reused${subtitles ? ` (${strips} subtitle strips, ${subtitles.cues.length} cues)` : ""}, in ${seconds} s${sheet}\n`);
  return EXIT.ok;
}
