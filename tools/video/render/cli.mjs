// `render`: draw every slide state of a video into <VIDEO_WORKDIR>/<slug>/frames/.
//
// Writes frames/manifest.json with the visual hash status compares, the thumbnail, and a contact
// sheet. Frames are cached by content key, so a rerun after editing one scene redraws that scene
// only. A STOP file ends the run after the current scene; the next run picks up from the cache.
// A drama's shots are clips the media stages make, so render draws only its cards, its subtitle
// strips (when they are burned in) and its thumbnail, on the chosen shot's keyframe. Every other
// caption locale whose i18n file has current thumbnail words gets its own thumbnail as well, in
// thumbnails/<locale>.jpg (YouTube Studio's 「語言」 page takes one per language).
import { existsSync, readFileSync, rmSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { isCompilation, THUMB_SOURCE } from "../core/compilation.mjs";
import { burnIn, hasPictures, isDrama, subtitlesHash } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkdir, stopRequested, UsageError } from "../core/paths.mjs";
import { lintProject, loadProject, recordStage, ARTIFACTS } from "../core/state.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { SIZE, THUMB_SIZE, THUMB_VARIANT_IDS } from "../templates/templates.mjs";
import { openRenderer, RendererError } from "./browser.mjs";
import { contactSheetHtml, SHEET_WIDTH } from "./contact.mjs";
import { bundledCoverage, uncovered } from "./fonts.mjs";
import { LOCALES } from "../core/schema.mjs";
import { localeThumbnailFile, renderPlan, renderProblems, stillFile, themeHash, thumbnailVariantFile, transitionFile } from "./plan.mjs";
import { BLANK_STRIP, blankStripHtml, blankStripKey, STRIP_SIZE, stripFile, subtitlePlan } from "./subtitles.mjs";
import { BrowserMissing } from "../screencast/browser.mjs";
import { ensureCaptures } from "../screencast/capture.mjs";
import { NetworkError, StepError } from "../screencast/runner.mjs";
import { isScreencast } from "../screencast/steps.mjs";

export const THUMBNAIL_FILE = "thumbnail.jpg";
export const THUMBNAIL_MAX_BYTES = 2 * 1024 * 1024;
const CACHE_FILE = path.join("frames", "cache.json");

function print(out, label, problems) {
  for (const problem of problems) out.write(`${label} ${problem.path}: ${problem.message}\n`);
}

const glyphList = (missing) => missing.map((char) => `"${char}" U+${char.codePointAt(0).toString(16).toUpperCase()}`).join(", ");

/** The thumbnail and its test variants, each with the path its problems are reported under. */
const thumbnailsOf = (plan) => (plan.thumbnail ? [["thumbnail", plan.thumbnail], ...(plan.thumbnail.variants ?? []).map((variant) => [`thumbnail variant ${variant.id}`, variant])] : []);

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
  for (const [where, thumb] of thumbnailsOf(plan)) {
    const missing = uncovered(thumb.text, coverage);
    if (missing.length) problems.push({ path: where, message: `no bundled font has ${missing.join(" ")}` });
  }
  return problems;
}

/**
 * The caption locales' own thumbnails to draw: { drawable, drawn: {}, gaps }. One whose words a
 * bundled font cannot draw (Hangul is only partly covered) joins the gaps instead of failing the
 * render; `drawn` is filled as the files are written.
 */
export function localizedThumbnails(plan, coverage) {
  const gaps = { ...(plan.thumbnail?.gaps ?? {}) };
  const drawable = [];
  for (const own of plan.thumbnail?.locales ?? []) {
    const missing = uncovered(own.text, coverage);
    if (missing.length) gaps[own.locale] = `no bundled font has ${glyphList(missing)}`;
    else drawable.push(own);
  }
  return { drawable, drawn: {}, gaps };
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({
    args,
    // --recapture takes the screencast scenes' pages again; --profile points their browser at a
    // persistent profile the owner signed in to himself (agents never pass it).
    options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" }, channel: { type: "string" }, force: { type: "boolean" }, recapture: { type: "boolean" }, profile: { type: "string" } },
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
  // A series' compilation (docs/videos/BINGE.md) is a drama with cards and a thumbnail only:
  // the episodes' cuts already carry their subtitles, so nothing is timed to a narration here.
  const compilation = isCompilation(doc);
  const drama = isDrama(doc);
  // Burned-in subtitles are cut and timed to the narration, like the captions, so a drama's
  // strips need the timeline the tts stage wrote for this very script.
  let subtitles = null;
  if (drama && !compilation && burnIn(doc)) {
    const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
    if (!timeline || timeline.speech_hash !== speechHash(doc, lexicon)) {
      ctx.stderr.write("timeline.json is missing or was built for an older script; run tts first (the burned-in subtitles follow the narration)\n");
      return EXIT.usage;
    }
    subtitles = subtitlePlan(doc, timeline);
  }
  const channel = values.channel ?? ctx.env.VIDEO_BROWSER_CHANNEL;
  // Screencast scenes (tools/video/screencast) draw stills a browser takes from their steps on a
  // public page; they are cached by the steps, so this opens a browser only for new or changed ones.
  let screencasts = {};
  if (doc.scenes.some(isScreencast)) {
    try {
      const taken = await ensureCaptures(doc, workdir, {
        channel,
        profile: values.profile ?? ctx.env.VIDEO_SCREENCAST_PROFILE,
        recapture: values.recapture,
        now: ctx.now,
        log: (text) => ctx.stdout.write(text),
      });
      screencasts = taken.manifests;
    } catch (error) {
      if (error instanceof BrowserMissing) {
        ctx.stderr.write(`${error.message}\n`);
        return EXIT.missing;
      }
      if (error instanceof NetworkError) {
        ctx.stderr.write(`${error.message}\n`);
        return EXIT.external;
      }
      if (!(error instanceof StepError)) throw error;
      ctx.stdout.write(`ERROR screencast ${error.message}\n`);
      return EXIT.lint;
    }
  }
  // A drama's thumbnail and an illustrated slides video's may sit on a keyframe (docs/videos/ILLUSTRATED.md).
  const keyframes = hasPictures(doc) ? (readJson(path.join(workdir, ARTIFACTS.keyframes), null)?.shots ?? {}) : {};
  const plan = renderPlan(doc, themeHash(), ctx.root, { keyframes, screencasts, translations: project.translations });
  const undrawn = (plan.thumbnail?.variants ?? []).find((variant) => variant.shot && !variant.keyframe);
  if (undrawn) {
    ctx.stderr.write(`thumbnail variant ${undrawn.id}'s background is the keyframe of shot ${undrawn.shot}, which is not drawn yet; run keyframes first\n`);
    return EXIT.usage;
  }
  if (plan.thumbnail?.shot && !plan.thumbnail.keyframe) {
    if (compilation) ctx.stderr.write(`the thumbnail's background is ${THUMB_SOURCE}, listed in keyframes/manifest.json under shots.${plan.thumbnail.shot}; the worker copies an episode's keyframe there when it plans the metadata (docs/videos/BINGE.md)\n`);
    else ctx.stderr.write(`the thumbnail's background is the keyframe of shot ${plan.thumbnail.shot}, which is not drawn yet; run keyframes first\n`);
    return EXIT.usage;
  }
  const glyphs = coverageProblems(plan, bundledCoverage(), subtitles);
  if (glyphs.length) {
    print(ctx.stdout, "ERROR", glyphs);
    return EXIT.lint;
  }
  // A caption locale's own thumbnail is an extra: what keeps one from being drawn is a note, and
  // the locale keeps the video's own thumbnail in Studio.
  const localized = localizedThumbnails(plan, bundledCoverage());

  mkdirSync(path.join(workdir, "frames"), { recursive: true });
  const cacheFile = path.join(workdir, CACHE_FILE);
  const cache = values.force || !existsSync(cacheFile) ? {} : JSON.parse(readFileSync(cacheFile, "utf8"));
  const started = Date.now();
  const layout = [];
  let drawn = 0;
  let reused = 0;
  let stopped = false;
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
      for (const [where, own] of thumbnailsOf(plan)) {
        const thumb = await renderer.capture(own.key, own.html, { size: THUMB_SIZE, type: "jpeg", quality: 90 });
        for (const problem of thumb.problems) layout.push({ path: where, message: problem });
        if (thumb.still.length > THUMBNAIL_MAX_BYTES) layout.push({ path: where, message: `${thumb.still.length} bytes; YouTube's mobile upload limit is 2 MB` });
        writeFileSync(path.join(workdir, own.file ?? THUMBNAIL_FILE), thumb.still);
      }
      // A variant taken out of video.json leaves no stale file for the package to pick up.
      for (const id of THUMB_VARIANT_IDS) {
        const file = path.join(workdir, thumbnailVariantFile(id));
        if (!plan.thumbnail.variants?.some((variant) => variant.id === id) && existsSync(file)) rmSync(file);
      }
      for (const own of localized.drawable) {
        const thumb = await renderer.capture(own.key, own.html, { size: THUMB_SIZE, type: "jpeg", quality: 90 });
        const problems = [...thumb.problems, ...(thumb.still.length > THUMBNAIL_MAX_BYTES ? [`${thumb.still.length} bytes; YouTube's limit is 2 MB`] : [])];
        if (problems.length) {
          localized.gaps[own.locale] = `its thumbnail did not fit and was not drawn: ${problems.join("; ")}`;
          continue;
        }
        mkdirSync(path.join(workdir, path.dirname(own.file)), { recursive: true });
        writeFileSync(path.join(workdir, own.file), thumb.still);
        localized.drawn[own.locale] = { file: own.file, hash: own.hash };
      }
      // A locale that lost its words, or whose thumbnail no longer fits, leaves no older picture behind.
      for (const locale of LOCALES) {
        const file = path.join(workdir, localeThumbnailFile(locale));
        if (!localized.drawn[locale] && existsSync(file)) rmSync(file);
      }
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
    // B and C for YouTube's "Test & compare", when video.json has them; A is `thumbnail`.
    ...(plan.thumbnail?.variants ? { thumbnail_variants: plan.thumbnail.variants.map((variant) => variant.file) } : {}),
    // Each caption locale's own thumbnail (YouTube Studio's 「語言」 page), with the hash of what it
    // was drawn from for package to compare; the locales without one and why, for its notes.
    ...(Object.keys(localized.drawn).length ? { thumbnail_locales: localized.drawn } : {}),
    ...(Object.keys(localized.gaps).length ? { thumbnail_locale_gaps: localized.gaps } : {}),
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
  const own = Object.keys(localized.drawn);
  if (own.length) ctx.stdout.write(`thumbnails of their own: ${own.map((locale) => localized.drawn[locale].file).join(", ")}\n`);
  for (const [locale, why] of Object.entries(localized.gaps)) ctx.stdout.write(`note: no ${locale} thumbnail of its own (it keeps ${THUMBNAIL_FILE}): ${why}\n`);
  return EXIT.ok;
}
