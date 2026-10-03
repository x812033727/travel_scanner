// The items of the final-cut QA that read what earlier stages already checked and recorded
// (docs/videos/HANDS-OFF.md §自動品管). Each function takes data already read from the work
// directory and answers { id, ok, detail, warnings? }; cli.mjs does the reading and writing.
import path from "node:path";

import { illustrated, isDrama, resolveLook } from "../core/drama.mjs";
import { animeDurationProblems, knowledgeDurationProblems } from "../core/duration.mjs";
import { formatClock, FPS } from "../core/timeline.mjs";

// Look presets whose pictures could pass for a photograph or a film: YouTube's disclosure covers
// realistic synthetic people, events and places. Flat, painterly and ink illustrations do not.
export const REALISTIC_PRESETS = ["cinematic-3d"];

/** The eleven items, in the order qa.json lists them; the server requires every one of them. */
export const ITEM_IDS = ["assemble", "render", "narration", "pace", "captions", "metadata", "facts", "links", "thumbnail", "policy", "disclosure"];
/**
 * A series' compilation (docs/videos/BINGE.md) has no narration, slides, facts or stance of its
 * own: its episodes passed those. Its six items are the join, the merged captions, the
 * metadata with every chapter, the links, the thumbnail and the disclosure.
 */
export const COMPILATION_ITEM_IDS = ["assemble", "captions", "metadata", "links", "thumbnail", "disclosure"];

export function item(id, ok, detail, warnings = []) {
  return { id, ok: Boolean(ok), detail: String(detail), ...(warnings.length ? { warnings: warnings.map(String) } : {}) };
}

/**
 * The report the server reads: { ok, final_sha256, items }, items in `required` order (ITEM_IDS,
 * or COMPILATION_ITEM_IDS with `kind: "compilation"` so the server requires those six instead).
 */
export function qaReport(items, finalSha256, required = ITEM_IDS) {
  const ids = items.map((each) => each.id);
  if (ids.length !== required.length || ids.some((id, index) => id !== required[index])) {
    throw new Error(`qa items must be exactly ${required.join(", ")}; got ${ids.join(", ")}`);
  }
  return { ok: items.every((each) => each.ok), final_sha256: finalSha256 ?? null, ...(required === COMPILATION_ITEM_IDS ? { kind: "compilation" } : {}), items };
}

/**
 * assemble: checks.json says final.mp4 is the cut of this very script and passed every check
 * (frame count, audio drift, loudness, the PSNR of every chapter's first frame).
 * `current` is package/cli.mjs's checksCurrent verdict.
 */
export function assembleItem({ checks, current, finalExists, doc, timeline, presented, timelineCurrent, finalSha256, command = "assemble", stale = "an older script, look or clips", minMinutes = 0 }) {
  if (!finalExists) return item("assemble", false, `final.mp4 is missing; run ${command}`);
  if (!checks) return item("assemble", false, `checks.json is missing; run ${command}`);
  if (!checks.ok) return item("assemble", false, `checks failed: ${(checks.problems ?? []).join("; ") || "no reason recorded"}`);
  if (!current) return item("assemble", false, `checks.json was written for ${stale}; run ${command} again`);
  const durationProblems = [...knowledgeDurationProblems({ doc, timeline, presented, timelineCurrent, checks }), ...animeDurationProblems({ doc, timeline, presented, timelineCurrent, checks, finalSha256 })];
  if (durationProblems.length) return item("assemble", false, durationProblems.join("; "));
  const metrics = checks.metrics ?? {};
  // The eight-minute floor (core/schema.mjs MIN_EPISODE_MINUTES), measured on the cut: the
  // writer's estimate reads 250 characters a minute and the voice speaks faster.
  if (minMinutes > 0) {
    if (!Number.isSafeInteger(metrics.frames) || metrics.frames <= 0) return item("assemble", false, "checks.json records no positive integer frame count; run assemble again");
    if (metrics.fps !== undefined && metrics.fps !== FPS) return item("assemble", false, `checks.json frame rate must be ${FPS} fps; run assemble again`);
    const seconds = Number(metrics.frames) / FPS;
    if (seconds < minMinutes * 60) {
      return item("assemble", false, `the cut runs ${formatClock(seconds)}, under the ${minMinutes}-minute floor every episode but a drama's keeps; write more narration, then run tts and assemble again`);
    }
  }
  const loudness = metrics.loudness?.integrated;
  const psnr = Array.isArray(metrics.psnr) ? `, ${metrics.psnr.length} frames matched their slides` : "";
  return item("assemble", true, `${metrics.frames ?? "?"} frames${loudness === undefined ? "" : `, ${loudness} LUFS`}${psnr}; every check passed`);
}

/**
 * render: frames/manifest.json was drawn for this script and the renderer's layout checks
 * (overflow, missing glyphs, every font face, clipped code) left nothing in frames/cache.json
 * for the states it uses. Render writes the manifest only after a clean run, so the cache is a
 * second look, not the only one.
 */
export function renderItem({ manifest, cache, visual, speech, subtitles, burnIn, hasThumbnail }) {
  if (!manifest) return item("render", false, "frames/manifest.json is missing; run render");
  if (manifest.visual_hash !== visual) return item("render", false, "frames/manifest.json was rendered for an older script; run render again");
  if (burnIn && (manifest.speech_hash !== speech || manifest.subtitles_hash !== subtitles)) {
    return item("render", false, "frames/manifest.json has subtitle strips for an older narration; run render again");
  }
  const problems = [];
  let states = 0;
  for (const scene of manifest.scenes ?? []) {
    (scene.states ?? []).forEach((state, index) => {
      states += 1;
      const key = path.posix.basename(String(state.still ?? ""), ".png");
      for (const message of cache?.[key]?.problems ?? []) problems.push(`${scene.id} state ${index}: ${message}`);
    });
  }
  if (hasThumbnail && !manifest.thumbnail) problems.push("the thumbnail was not drawn; run render again");
  if (problems.length) return item("render", false, problems.join("; "));
  return item("render", true, `${states} slide states drawn with no layout, glyph or font problem${manifest.thumbnail ? ", thumbnail included" : ""}`);
}

/** narration: the timeline the owner (or Jev) approved is the one this script has now. */
export function narrationItem({ approval, current }) {
  if (approval.status === "absent") return item("narration", false, "timeline.json is missing; run tts");
  if (!current) return item("narration", false, "timeline.json was built for an older script; run tts again");
  if (approval.status === "missing") return item("narration", false, "the narration has not been approved yet");
  if (approval.status === "stale") return item("narration", false, "timeline.json changed since the narration was approved");
  return item("narration", true, `timeline.json approved at ${approval.entry?.approved_at ?? "?"}`);
}

const ORPHAN = /no longer open a chapter/;
const READING_SPEED = /characters a second/;

/**
 * captions: every wanted locale (zh-TW and the ones the owner chose, docs/videos/LANGUAGES.md)
 * has a caption file cut from the current narration, and no wanted translation is older than
 * its zh-TW text (lines, chapters, title, description, tags: lint's warnings for
 * i18n/<locale>.json, failures here). Reading-speed overruns are warnings; other cue problems
 * (overlaps, overlong lines) are failures. Chapter titles left over from scenes that no longer
 * open a chapter are dropped by i18n-merge, so they only warn. A dub track the worker gave up on
 * (`skippedDubs`, locale to reason) is a warning: those captions follow the narration.
 */
export function captionsItem({ lintWarnings, manifest, current, locales, hasCaptionFile, skippedDubs = {} }) {
  const problems = [];
  const warnings = [];
  for (const warning of lintWarnings) {
    if (!/^i18n\//.test(warning.path)) continue;
    const locale = /^i18n\/([^.]+)\.json$/.exec(warning.path)?.[1];
    if (locale && !locales.includes(locale)) continue;
    (ORPHAN.test(warning.message) ? warnings : problems).push(`${warning.path}: ${warning.message}`);
  }
  for (const [locale, reason] of Object.entries(skippedDubs)) warnings.push(`${locale}: dub track skipped (${reason || "no reason recorded"}); its captions follow the narration`);
  if (!manifest) problems.push("captions/manifest.json is missing; run captions");
  else if (!current) problems.push("captions were written for an older narration; run captions again");
  else {
    for (const locale of locales) {
      const skipped = manifest.skipped?.[locale];
      if (skipped) {
        problems.push(`${locale}: no caption file, ${skipped.length} lines missing or older than zh-TW (${skipped.join(", ")})`);
        continue;
      }
      if (!manifest.locales?.[locale] || !hasCaptionFile(locale)) {
        problems.push(`${locale}: no caption file`);
        continue;
      }
      for (const problem of manifest.locales[locale].problems ?? []) (READING_SPEED.test(problem) ? warnings : problems).push(`${locale}: ${problem}`);
    }
  }
  if (problems.length) return item("captions", false, problems.join("; "), warnings);
  return item("captions", true, `caption files for ${locales.join(", ")}, every translation current`, warnings);
}

/**
 * captions of a compilation: the episodes' caption files merged for every locale every episode
 * has (compile's manifest), and the compilation's own translations current (lint's warnings
 * for i18n/<locale>.json, failures here). A locale an episode lacks is named with the episodes.
 */
export function compilationCaptionsItem({ lintWarnings, manifest, current, locales, hasCaptionFile }) {
  const problems = [];
  const warnings = [];
  for (const warning of lintWarnings) {
    if (/^i18n\//.test(warning.path)) problems.push(`${warning.path}: ${warning.message}`);
  }
  if (!manifest) problems.push("captions/manifest.json is missing; run compile");
  else if (!current) problems.push("captions were merged for other cuts; run compile again");
  else {
    for (const locale of locales) {
      const missing = manifest.skipped?.[locale];
      if (Array.isArray(missing) && missing.length) {
        problems.push(`${locale}: no caption file, ${missing.length} episodes have none (${missing.join(", ")})`);
        continue;
      }
      if (!manifest.locales?.[locale] || !hasCaptionFile(locale)) {
        problems.push(`${locale}: no caption file`);
        continue;
      }
      for (const problem of manifest.locales[locale].problems ?? []) problems.push(`${locale}: ${problem}`);
    }
  }
  if (problems.length) return item("captions", false, problems.join("; "), warnings);
  return item("captions", true, `caption files for ${locales.join(", ")}, merged from every episode`, warnings);
}

/**
 * metadata: every locale's title, description (as composed) and tags within YouTube's limits,
 * and chapters YouTube will show. `problems` is composeMetadata's list, `tagProblems`
 * checkYoutubeFields' on the tags, `chapterProblems` checkChapters' on the real timeline.
 */
export function metadataItem({ problems, tagProblems, chapterProblems, locales, chapters, timelineCurrent, command = "tts" }) {
  const all = [...problems, ...tagProblems, ...chapterProblems];
  if (!timelineCurrent) all.unshift(`timeline.json is missing or was built for an older script, so the chapter times are unknown; run ${command}`);
  if (all.length) return item("metadata", false, all.join("; "));
  return item("metadata", true, `title, description and tags within YouTube's limits for ${locales.join(", ")}; ${chapters} chapters`);
}

/**
 * disclosure: whether YouTube Studio's "altered or synthetic content" must be ticked. The
 * channel's rule (upload/UPLOAD.md, docs/videos/DRAMA.md): slides read by a stock TTS voice are
 * not a realistic depiction of a person, event or place, so no; a drama's 3D shots and generated
 * music always are, so yes. The answer never fails the QA; package's metadata carries it.
 */
export function disclosureDecision(doc, { musicSource = null } = {}) {
  if (isDrama(doc)) return { synthetic: true, reason: "a drama: AI-generated shots and music are always disclosed" };
  // Illustrated slides (docs/videos/ILLUSTRATED.md): stylised pictures under a licensed bed need
  // no disclosure; a realistic preset or a generated track does (docs/videos/SHORTS.md keeps AI
  // music disclosed, and the conservative answer costs nothing).
  const generated = musicSource === "generated";
  if (illustrated(doc)) {
    const preset = resolveLook(doc.look).preset;
    if (REALISTIC_PRESETS.includes(preset)) return { synthetic: true, reason: `illustrated slides in the ${preset} look: pictures that could pass for real are disclosed` };
    if (generated) return { synthetic: true, reason: "illustrated slides under AI-generated music: the music is disclosed" };
    return { synthetic: false, reason: `illustrated slides: stylised ${preset} pictures, a licensed music bed and a stock TTS voice; YouTube's disclosure covers realistic synthetic people, events and places` };
  }
  if (generated) return { synthetic: true, reason: "slides under AI-generated music: the music is disclosed" };
  return { synthetic: false, reason: "slides read by a stock TTS voice; YouTube's disclosure covers realistic synthetic people, events and places" };
}

export function disclosureItem(decision, written) {
  const answer = decision.synthetic ? "tick altered or synthetic content" : "no disclosure needed";
  return item("disclosure", true, `${answer}: ${decision.reason}${written === null ? "" : written ? "; written to upload/metadata.json" : "; upload/metadata.json already says so"}`);
}
