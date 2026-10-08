// The stages that need nothing but the timeline: caption files for the locales the owner chose,
// which dub tracks are current enough to caption, upload and review, and the owner's language
// choice itself as the worker copies it into the work directory (docs/videos/LANGUAGES.md).
import { existsSync, rmSync } from "node:fs";
import path from "node:path";

import { defaultDubLocales, dubScript, translationHash } from "../dubs/plan.mjs";
import { appliedBranding, brandingCurrent, presentationTimeline, readBranding } from "./branding.mjs";
import { verifiedManualPresentation } from "../review/renewal-handoff.mjs";
import { buildCues, checkCues, toSrt, toVtt } from "./captions.mjs";
import { atomicWrite, readJson } from "./paths.mjs";
import { eachLine, LOCALES, NARRATION_LOCALE, narrationLocale, textHash } from "./schema.mjs";
import { ARTIFACTS, dubArtifacts, dubSpeechCurrent, lintProject, loadProject, recordStage } from "./state.mjs";
import { checkChapters, speechHash } from "./timeline.mjs";

export class StageError extends Error {
  constructor(message, code) {
    super(message);
    this.code = code;
  }
}

// The owner's language choice for this video, as the worker copies it from the site each round
// (docs/videos/LANGUAGES.md): { locales: { en: { metadata, captions, dub } }, decided_at }. Only
// the languages with something ticked are listed; zh-TW and the narration's own locale always get
// captions, a title and a description (alwaysLocales), so a zh-TW entry is dropped. The captions,
// package, qa and review-push commands read it from the work directory, so a hand run on the owner's
// machine and the worker's run agree; without the file (a video from before the panel, an
// example outside the site) every locale with a translation is made, as before.
export const LANGUAGES_FILE = "languages.json";
export const LOCALE_PARTS = ["metadata", "captions", "dub"];

/** The choice in the work directory, or null when none was written. */
export function readLanguages(workdir) {
  const record = readJson(path.join(workdir, LANGUAGES_FILE), null);
  if (!record || typeof record !== "object" || !record.locales || typeof record.locales !== "object") return null;
  const locales = {};
  for (const locale of LOCALES) {
    const choice = record.locales[locale];
    if (!choice || typeof choice !== "object" || locale === NARRATION_LOCALE) continue;
    // A dub is read from the captions' translation, so choosing it chooses them (the site does the same).
    const dub = choice.dub === true;
    const entry = { metadata: choice.metadata === true, captions: choice.captions === true || dub, dub };
    if (entry.metadata || entry.captions || entry.dub) locales[locale] = entry;
  }
  return { locales, decided_at: typeof record.decided_at === "string" ? record.decided_at : null };
}

/** Write the site's choice for the commands to read; `locales` is the site's `locales` field. */
export function writeLanguages(workdir, { locales, decided_at = null, synced_at = null }) {
  const record = { locales: locales ?? {}, decided_at, ...(synced_at ? { synced_at } : {}) };
  atomicWrite(path.join(workdir, LANGUAGES_FILE), `${JSON.stringify(record, null, 2)}\n`);
  return record;
}

/** The locales with `part` ticked, in the page's order; null without a choice (every locale, as before). */
export function chosenLocales(languages, part) {
  if (!languages) return null;
  return LOCALES.filter((locale) => languages.locales[locale]?.[part]);
}

/**
 * The locales a video gets captions, a title and a description in whatever the owner chose: its
 * narration, and zh-TW, the channel's own language, which the site's panel never offers. A zh-TW
 * video has just the one; an English-narrated video has both, English first.
 */
export const alwaysLocales = (narration = NARRATION_LOCALE) => [...new Set([narration, NARRATION_LOCALE])];

/** The caption locales a video is made in: its narration and zh-TW, then the chosen ones; every locale without a choice. */
export function captionLocalesOf(languages, narration = NARRATION_LOCALE) {
  const chosen = chosenLocales(languages, "captions");
  return chosen ? [...new Set([...alwaysLocales(narration), ...chosen])] : [...LOCALES];
}

/** The title and description locales asked for: its narration and zh-TW, then the chosen ones; null without a choice (every translated locale). */
export function metadataLocalesOf(languages, narration = NARRATION_LOCALE) {
  const chosen = chosenLocales(languages, "metadata");
  return chosen ? [...new Set([...alwaysLocales(narration), ...chosen])] : null;
}

/** The dub tracks asked for: the chosen ones but the narration's own, or the video's default without a choice. */
export function dubLocalesOf(languages, doc) {
  const chosen = chosenLocales(languages, "dub");
  return chosen ? chosen.filter((locale) => locale !== narrationLocale(doc)) : defaultDubLocales(doc);
}

/** The text each locale shows for each line; translations older than their narration line are left out. */
export function localeTexts(doc, translations) {
  const narration = narrationLocale(doc);
  const texts = { [narration]: {} };
  const skipped = {};
  for (const { line } of eachLine(doc)) texts[narration][line.id] = line.text;
  for (const locale of LOCALES.filter((each) => each !== narration)) {
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
 * this translation, with the voice and pronunciation `dub` would use now (dubSpeechCurrent): the dub
 * timeline plus `file`, the track's path. Null when there is no dub, or an older one; `stale`
 * tells the two apart for the caption manifest.
 */
export function currentDub(project, workdir, locale, speech) {
  const files = dubArtifacts(workdir, locale);
  const dub = readJson(files.timeline, null);
  if (!dub) return null;
  const words = translationHash(dubScript(project.doc, project.translations[locale], locale).doc);
  const file = files.track(dub.format);
  const checks = readJson(path.join(workdir, ARTIFACTS.checks), null);
  const manual = verifiedManualPresentation({ project, workdir, timeline: readJson(path.join(workdir, ARTIFACTS.timeline), null) });
  const applied = manual ?? appliedBranding(checks);
  const bodyTimeline = applied ? readJson(path.join(workdir, ARTIFACTS.timeline), null) : null;
  if ((!manual && !brandingCurrent(checks, readBranding(workdir))) || (dub.branding_hash ?? null) !== (applied?.hash ?? null)
      || (applied && ((!manual && checks.speech_hash !== speech) || bodyTimeline?.speech_hash !== speech || applied.body_frames !== bodyTimeline?.total_frames))
      || (applied && (dub.body_total_frames !== applied.body_frames || dub.content_end_frame !== applied.intro_frames + applied.body_frames
        || dub.total_frames !== applied.intro_frames + applied.body_frames + applied.outro_frames))
      || dub.speech_hash !== speech || dub.translation_hash !== words || !existsSync(file)
      // A target alias or the dub voice changed, or an older track's clip cache no longer matches (state.mjs).
      || !dubSpeechCurrent(project, workdir, locale, dub)) return { stale: true };
  return { ...dub, file };
}

/** The review file role of a locale's dub track: `dub_en`, `dub_zh_cn` (roles are lower-case words). */
export const dubRole = (locale) => `dub_${locale.toLowerCase().replace(/-/g, "_")}`;

/**
 * The current dub track of every locale asked for (the owner's dub choice, or every locale but
 * zh-CN without one), and the locales the worker gave up on with its reason. A locale the worker
 * gave up on stays skipped even when an older track of it exists: the reason is the last word.
 */
export function dubsForUpload(project, workdir, speech, locales = defaultDubLocales(project.doc)) {
  const dubs = [];
  const skipped = {};
  for (const locale of locales) {
    const gaveUp = readJson(dubArtifacts(workdir, locale).skipped, null);
    if (gaveUp) {
      skipped[locale] = gaveUp.reason ?? "";
      continue;
    }
    const dub = currentDub(project, workdir, locale, speech);
    if (dub && !dub.stale) dubs.push({ locale, file: dub.file, format: dub.format, total_frames: dub.total_frames, tempo_max: dub.tempo_max ?? 1, ...(dub.branding_hash ? { branding_hash: dub.branding_hash } : {}) });
  }
  return { dubs, skipped };
}

/**
 * The cues of `locale` as runCaptions writes them: under its current dub's own timeline, or under
 * the narration's presented one, where a translation's cue changes move onto the narration's
 * measured ones (`timing.chars`). The renewal checks (review/renewal.mjs, renewal-handoff.mjs)
 * rebuild the bytes they expect with it, so they never expect another cut than the one written.
 */
export function localeCues(presented, texts, locale, narration, dub = null) {
  return buildCues(dub ? captionTimelineOf(dub) : presented, texts[locale], locale, dub ? null : { locale: narration, texts: texts[narration] });
}

/**
 * A dub's lines as the timeline captions are cut on: the pause after a dubbed line belongs to
 * its cues, as the narration's does, so each line runs to the next dubbed line's start.
 */
export function captionTimelineOf(dub) {
  const lines = [...dub.lines].sort((a, b) => a.start_frame - b.start_frame);
  const contentEnd = dub.content_end_frame ?? dub.total_frames;
  return {
    ...dub,
    lines: lines.map((line, index) => ({
      ...line,
      end_frame: Math.min(contentEnd, Math.max(line.end_frame, index + 1 < lines.length ? lines[index + 1].start_frame : contentEnd)),
    })),
  };
}

/**
 * Write captions/<locale>.srt and .vtt for the narration locale, zh-TW and every chosen locale
 * whose translation is complete and current (every translated locale when no choice was
 * written). A locale with missing or stale lines is reported and not written: a caption track
 * that silently skips sentences is worse than none. A locale with a current dub is cut on the
 * dub's timing, so a viewer who picks that audio and those captions reads what they hear, when
 * they hear it. The files of a locale not written this run are removed, so captions/ holds
 * exactly the current set.
 */
export function runCaptions({ slug, file, root, workdir, now = new Date() }) {
  const project = loadProject({ slug, file, root });
  const lint = lintProject(project);
  if (lint.errors.length) throw new StageError(`${project.doc.slug} has ${lint.errors.length} lint errors; run lint first`, "lint");
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  const speech = speechHash(project.doc, project.lexicon);
  if (!timeline) throw new StageError("no timeline.json yet; run tts first", "order");
  if (timeline.speech_hash !== speech) throw new StageError("timeline.json was built for an older script; run tts again", "order");
  const checks = readJson(path.join(workdir, ARTIFACTS.checks), null);
  const manual = verifiedManualPresentation({ project, workdir, timeline });
  if (!manual && !brandingCurrent(checks, readBranding(workdir))) throw new StageError("final.mp4 does not match the selected branding; run assemble again before captions", "order");
  const applied = manual ?? appliedBranding(checks);
  if (applied && ((!manual && checks.speech_hash !== speech) || applied.body_frames !== timeline.total_frames)) throw new StageError("the branded final.mp4 was built for another body timeline; run assemble again before captions", "order");
  const presented = presentationTimeline(timeline, applied);

  const languages = readLanguages(workdir);
  const wanted = new Set(captionLocalesOf(languages, narrationLocale(project.doc)));
  const dubbed = dubLocalesOf(languages, project.doc);
  const { texts, skipped } = localeTexts(project.doc, project.translations);
  const manifest = { speech_hash: speech, ...(applied ? { branding_hash: applied.hash } : {}), chapters: checkChapters(presented), locales: {}, skipped: {} };
  for (const [locale, byLine] of Object.entries(texts)) {
    if (!wanted.has(locale)) continue;
    if (skipped[locale]?.length) {
      manifest.skipped[locale] = skipped[locale];
      continue;
    }
    const dub = locale === narrationLocale(project.doc) || !dubbed.includes(locale) ? null : currentDub(project, workdir, locale, speech);
    const timed = dub && !dub.stale;
    // Dub timelines already describe their padded presentation; only narration is shifted here.
    // A translation under the narration's timeline takes its cue changes from the narration's
    // measured ones; a dub-timed one follows its own track (localeCues).
    const { cues } = localeCues(presented, texts, locale, narrationLocale(project.doc), timed ? dub : null);
    atomicWrite(path.join(workdir, "captions", `${locale}.srt`), toSrt(cues));
    atomicWrite(path.join(workdir, "captions", `${locale}.vtt`), toVtt(cues));
    const problems = checkCues(cues, locale);
    if (dub?.stale) problems.unshift(`the ${locale} dub track is older than the script or its translation (or how they are pronounced), or does not match the branding; these cues follow the narration, run dub again`);
    manifest.locales[locale] = { cues: cues.length, problems, timing: timed ? "dub" : "narration" };
  }
  for (const locale of LOCALES) {
    if (manifest.locales[locale]) continue;
    for (const kind of ["srt", "vtt"]) rmSync(path.join(workdir, "captions", `${locale}.${kind}`), { force: true });
  }
  atomicWrite(path.join(workdir, ARTIFACTS.captions), `${JSON.stringify(manifest, null, 2)}\n`);
  recordStage(workdir, "captions", { locales: Object.keys(manifest.locales) }, now);
  return manifest;
}
