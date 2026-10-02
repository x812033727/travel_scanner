// Which parts of a translation file (docs/videos/<slug>/i18n/<locale>.json) still match the script.
//
// Each caption line carries the hash of the zh-TW text it was made from (`lines.<id>.source_hash`).
// The title, the description, the tags and the chapter titles stay plain text, because the package
// step reads them as they are (`chapters` keyed by scene id), so `i18n-merge` keeps their hashes
// beside them in `source_hashes`. A file merged before those hashes were kept has none: its title,
// description, tags and chapters are "unknown", and the next worksheet asks for them again.
// The thumbnail's words (`thumbnail.{tag,headline,sub}`) work the same way, under
// `source_hashes.thumbnail`, but stay optional: render draws a locale's own thumbnail only from
// current words, and a locale without them keeps the zh-TW thumbnail.
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

// The thumbnail's words a locale translates (the `thumb` template's data): its own thumbnail in
// YouTube Studio's 「語言」 page wears them over the same picture and layout.
export const THUMBNAIL_FIELDS = ["tag", "headline", "sub"];

/** The thumbnail words the script has, in THUMBNAIL_FIELDS order, or null without a thumbnail. */
export function thumbnailSource(doc) {
  const data = doc.thumbnail?.data;
  if (!data) return null;
  return Object.fromEntries(THUMBNAIL_FIELDS.filter((name) => typeof data[name] === "string" && data[name].trim() !== "").map((name) => [name, data[name]]));
}

/** The hash of the thumbnail's words, as one record like the tags: any of them changing makes the translation stale. */
export const thumbnailSourceHash = (doc) => {
  const source = thumbnailSource(doc);
  return source ? textHash(JSON.stringify(source)) : null;
};

/**
 * A translation's thumbnail words: "none" when the script has no thumbnail, else "current",
 * "stale", "unknown" (no recorded hash) or "missing" (a word the script has is not translated).
 * Kept apart from metadataStatus: a locale without thumbnail words is a note, never a lint
 * warning, so the videos translated before thumbnails were localized stay as they are.
 */
export function thumbnailStatus(doc, translation) {
  const source = thumbnailSource(doc);
  if (!source) return "none";
  const words = translation?.thumbnail;
  if (!words || !Object.keys(source).every((name) => filled(words[name]))) return "missing";
  const recorded = translation.source_hashes?.thumbnail;
  if (recorded === undefined) return "unknown";
  return recorded === thumbnailSourceHash(doc) ? "current" : "stale";
}

/**
 * The thumbnail a locale wears: the script's, with the translated words in place of its own, or
 * null unless the words are current. A word the script does not have is left out.
 */
export function localizedThumbnail(doc, translation) {
  if (thumbnailStatus(doc, translation) !== "current") return null;
  const source = thumbnailSource(doc);
  const data = { ...doc.thumbnail.data };
  for (const name of THUMBNAIL_FIELDS) {
    if (Object.hasOwn(source, name)) data[name] = translation.thumbnail[name].trim();
    else delete data[name];
  }
  return { template: doc.thumbnail.template, data };
}

/**
 * What a locale's own thumbnail was drawn from, as a hash: render records it beside the file and
 * package takes the file only while the hash still matches, so words merged after render are
 * never uploaded under an older picture. Null when the locale has no thumbnail of its own.
 */
export function localizedThumbnailHash(doc, translation) {
  const own = localizedThumbnail(doc, translation);
  return own ? textHash(JSON.stringify(own)) : null;
}

/** Why a locale has no thumbnail of its own, for render's and package's notes; null when it has one. */
export function thumbnailGap(doc, translation, locale) {
  const status = thumbnailStatus(doc, translation);
  if (status === "current" || status === "none") return null;
  if (status === "missing") return `i18n/${locale}.json has no thumbnail words (i18n-sheet --locale ${locale} --parts metadata, then i18n-merge)`;
  if (status === "stale") return `i18n/${locale}.json's thumbnail words were made from an older thumbnail; i18n-sheet marks them todo`;
  return `i18n/${locale}.json's thumbnail words were not merged by i18n-merge, so their source is unknown; i18n-sheet marks them todo`;
}

/** The fields and chapters in one status, named the way lint and the CLI report them. */
export function namedWith(state, wanted) {
  return [
    ...METADATA_FIELDS.filter((name) => state[name] === wanted),
    ...Object.keys(state.chapters).filter((scene) => state.chapters[scene] === wanted).map((scene) => `chapter ${scene}`),
  ];
}
