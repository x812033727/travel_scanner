// The stages that need nothing but the timeline: caption files for every locale, and which dub
// tracks are current enough to caption, upload and review.
import { existsSync } from "node:fs";
import path from "node:path";

import { DUB_LOCALES, dubScript, translationHash } from "../dubs/plan.mjs";
import { buildCues, checkCues, toSrt, toVtt } from "./captions.mjs";
import { atomicWrite, readJson } from "./paths.mjs";
import { eachLine, LOCALES, NARRATION_LOCALE, textHash } from "./schema.mjs";
import { ARTIFACTS, dubArtifacts, lintProject, loadProject, recordStage } from "./state.mjs";
import { checkChapters, speechHash } from "./timeline.mjs";

export class StageError extends Error {
  constructor(message, code) {
    super(message);
    this.code = code;
  }
}

/** The text each locale shows for each line; translations older than their zh-TW line are left out. */
export function localeTexts(doc, translations) {
  const texts = { [NARRATION_LOCALE]: {} };
  const skipped = {};
  for (const { line } of eachLine(doc)) texts[NARRATION_LOCALE][line.id] = line.text;
  for (const locale of LOCALES.filter((each) => each !== NARRATION_LOCALE)) {
    const translation = translations[locale];
    if (!translation) continue;
    texts[locale] = {};
    skipped[locale] = [];
    for (const { line } of eachLine(doc)) {
      const entry = translation.lines?.[line.id];
      if (entry && entry.source_hash === textHash(line.text)) texts[locale][line.id] = entry.text;
      else skipped[locale].push(line.id);
    }
  }
  return { texts, skipped };
}

/**
 * A locale's dub (docs/videos/DUBS.md) when its track exists and was made from this script and
 * this translation: the dub timeline plus `file`, the track's path. Null when there is no dub, or
 * an older one; `stale` tells the two apart for the caption manifest.
 */
export function currentDub(project, workdir, locale, speech) {
  const files = dubArtifacts(workdir, locale);
  const dub = readJson(files.timeline, null);
  if (!dub) return null;
  const words = translationHash(dubScript(project.doc, project.translations[locale], locale).doc);
  const file = files.track(dub.format);
  if (dub.speech_hash !== speech || dub.translation_hash !== words || !existsSync(file)) return { stale: true };
  return { ...dub, file };
}

/** The review file role of a locale's dub track: `dub_en`, `dub_zh_cn` (roles are lower-case words). */
export const dubRole = (locale) => `dub_${locale.toLowerCase().replace(/-/g, "_")}`;

/** Every locale's current dub track, and the locales the worker gave up on with its reason. */
export function dubsForUpload(project, workdir, speech) {
  const dubs = [];
  const skipped = {};
  for (const locale of DUB_LOCALES) {
    const dub = currentDub(project, workdir, locale, speech);
    if (dub && !dub.stale) {
      dubs.push({ locale, file: dub.file, format: dub.format, total_frames: dub.total_frames, tempo_max: dub.tempo_max ?? 1 });
      continue;
    }
    const gaveUp = readJson(dubArtifacts(workdir, locale).skipped, null);
    if (gaveUp) skipped[locale] = gaveUp.reason ?? "";
  }
  return { dubs, skipped };
}

/**
 * A dub's lines as the timeline captions are cut on: the pause after a dubbed line belongs to
 * its cues, as the narration's does, so each line runs to the next dubbed line's start.
 */
export function captionTimelineOf(dub) {
  const lines = [...dub.lines].sort((a, b) => a.start_frame - b.start_frame);
  return {
    ...dub,
    lines: lines.map((line, index) => ({
      ...line,
      end_frame: Math.max(line.end_frame, index + 1 < lines.length ? lines[index + 1].start_frame : dub.total_frames),
    })),
  };
}

/**
 * Write captions/<locale>.srt and .vtt for zh-TW and every locale whose translation is complete
 * and current. A locale with missing or stale lines is reported and not written: a caption track
 * that silently skips sentences is worse than none. A locale with a current dub is cut on the
 * dub's timing, so a viewer who picks that audio and those captions reads what they hear, when
 * they hear it.
 */
export function runCaptions({ slug, file, root, workdir, now = new Date() }) {
  const project = loadProject({ slug, file, root });
  const lint = lintProject(project);
  if (lint.errors.length) throw new StageError(`${project.doc.slug} has ${lint.errors.length} lint errors; run lint first`, "lint");
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  const speech = speechHash(project.doc, project.lexicon);
  if (!timeline) throw new StageError("no timeline.json yet; run tts first", "order");
  if (timeline.speech_hash !== speech) throw new StageError("timeline.json was built for an older script; run tts again", "order");

  const { texts, skipped } = localeTexts(project.doc, project.translations);
  const manifest = { speech_hash: speech, chapters: checkChapters(timeline), locales: {}, skipped: {} };
  for (const [locale, byLine] of Object.entries(texts)) {
    if (skipped[locale]?.length) {
      manifest.skipped[locale] = skipped[locale];
      continue;
    }
    const dub = locale === NARRATION_LOCALE ? null : currentDub(project, workdir, locale, speech);
    const timed = dub && !dub.stale;
    const { cues } = buildCues(timed ? captionTimelineOf(dub) : timeline, byLine, locale);
    atomicWrite(path.join(workdir, "captions", `${locale}.srt`), toSrt(cues));
    atomicWrite(path.join(workdir, "captions", `${locale}.vtt`), toVtt(cues));
    const problems = checkCues(cues, locale);
    if (dub?.stale) problems.unshift(`the ${locale} dub track is older than the script or its translation; these cues follow the narration, run dub again`);
    manifest.locales[locale] = { cues: cues.length, problems, timing: timed ? "dub" : "narration" };
  }
  atomicWrite(path.join(workdir, ARTIFACTS.captions), `${JSON.stringify(manifest, null, 2)}\n`);
  recordStage(workdir, "captions", { locales: Object.keys(manifest.locales) }, now);
  return manifest;
}
