// Which parts of a translation file (docs/videos/<slug>/i18n/<locale>.json) still match the script.
//
// Each caption line carries the hash of the zh-TW text it was made from (`lines.<id>.source_hash`).
// The title, the description, the tags and the chapter titles stay plain text, because the package
// step reads them as they are (`chapters` keyed by scene id), so `i18n-merge` keeps their hashes
// beside them in `source_hashes`. A file merged before those hashes were kept has none: its title,
// description, tags and chapters are "unknown", and the next worksheet asks for them again.
import { textHash } from "./schema.mjs";

// The YouTube fields a locale translates, besides the chapters.
export const METADATA_FIELDS = ["title", "description", "tags"];

export const chapterScenes = (doc) => doc.scenes.filter((scene) => scene.chapter);

const filled = (value) => (Array.isArray(value) ? value.length > 0 : typeof value === "string" && value.trim() !== "");

/**
 * The hash of each field's zh-TW source. Tags hash as one ordered list: the first three become the
 * description's hashtags, so a reorder is a change.
 */
export function sourceHashes(doc) {
  return {
    title: textHash(doc.youtube.title),
    description: textHash(doc.youtube.description),
    tags: textHash(JSON.stringify(doc.youtube.tags)),
    chapters: Object.fromEntries(chapterScenes(doc).map((scene) => [scene.id, textHash(scene.chapter)])),
  };
}

function status(translated, recorded, current) {
  if (!filled(translated)) return "missing";
  if (recorded === undefined) return "unknown";
  return recorded === current ? "current" : "stale";
}

/**
 * Each field and chapter as "current", "stale" (merged from other zh-TW text), "unknown" (merged
 * before hashes were kept) or "missing"; and `orphans`, the chapter entries whose scene no longer
 * opens a chapter. A script with no tags has none to translate.
 */
export function metadataStatus(doc, translation) {
  const hashes = sourceHashes(doc);
  const recorded = translation?.source_hashes ?? {};
  const chapters = translation?.chapters ?? {};
  return {
    title: status(translation?.title, recorded.title, hashes.title),
    description: status(translation?.description, recorded.description, hashes.description),
    tags: doc.youtube.tags.length ? status(translation?.tags, recorded.tags, hashes.tags) : "current",
    chapters: Object.fromEntries(
      Object.entries(hashes.chapters).map(([scene, hash]) => [scene, status(chapters[scene], recorded.chapters?.[scene], hash)]),
    ),
    orphans: Object.keys(chapters).filter((scene) => !Object.hasOwn(hashes.chapters, scene)),
  };
}

/** The fields and chapters in one status, named the way lint and the CLI report them. */
export function namedWith(state, wanted) {
  return [
    ...METADATA_FIELDS.filter((name) => state[name] === wanted),
    ...Object.keys(state.chapters).filter((scene) => state.chapters[scene] === wanted).map((scene) => `chapter ${scene}`),
  ];
}
