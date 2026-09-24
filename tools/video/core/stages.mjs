// The stages that need nothing but the timeline: caption files for every locale.
import path from "node:path";

import { buildCues, checkCues, toSrt, toVtt } from "./captions.mjs";
import { atomicWrite, readJson } from "./paths.mjs";
import { eachLine, LOCALES, NARRATION_LOCALE, textHash } from "./schema.mjs";
import { ARTIFACTS, lintProject, loadProject, recordStage } from "./state.mjs";
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
 * Write captions/<locale>.srt and .vtt for zh-TW and every locale whose translation is complete
 * and current. A locale with missing or stale lines is reported and not written: a caption track
 * that silently skips sentences is worse than none.
 */
export function runCaptions({ slug, root, workdir, now = new Date() }) {
  const project = loadProject({ slug, root });
  const lint = lintProject(project);
  if (lint.errors.length) throw new StageError(`${slug} has ${lint.errors.length} lint errors; run lint first`, "lint");
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
    const { cues } = buildCues(timeline, byLine, locale);
    atomicWrite(path.join(workdir, "captions", `${locale}.srt`), toSrt(cues));
    atomicWrite(path.join(workdir, "captions", `${locale}.vtt`), toVtt(cues));
    manifest.locales[locale] = { cues: cues.length, problems: checkCues(cues, locale) };
  }
  atomicWrite(path.join(workdir, ARTIFACTS.captions), `${JSON.stringify(manifest, null, 2)}\n`);
  recordStage(workdir, "captions", { locales: Object.keys(manifest.locales) }, now);
  return manifest;
}
