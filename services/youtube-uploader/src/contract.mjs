import { createHash } from "node:crypto";

export const HASH = /^[a-f0-9]{64}$/;
export const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
export const VIDEO = /^[A-Za-z0-9_-]{11}$/;
export const CHANNEL = /^UC[A-Za-z0-9_-]{22}$/;
export const CHUNK = 4 * 1024 * 1024;
export const LANGUAGES = { "zh-TW": "Chinese (Taiwan)", "zh-CN": "Chinese (China)", en: "English", ja: "Japanese", ko: "Korean" };
export const ACTIVE = new Set(["staging", "queued", "running", "needs_action"]);
export class Refused extends Error {
  constructor(code, status = 409) { super(code); this.code = code; this.status = status; }
}
export const hash = (value) => createHash("sha256").update(value).digest("hex");
const object = (value) => value && typeof value === "object" && !Array.isArray(value);
function field(value, max, empty = false) {
  return typeof value === "string" && [...value].length <= max && (empty || value.trim().length > 0) && !/[<>\0]/.test(value);
}
const description = (value) => field(value, 5000, true) && Buffer.byteLength(value, "utf8") <= 5000;
export function validateManifest(value, channel) {
  if (!object(value) || value.version !== 1 || !SLUG.test(value.slug) || !HASH.test(value.review_sha256)
      || value.channel_id !== channel || !CHANNEL.test(channel) || (value.video_id !== null && !VIDEO.test(value.video_id))) throw new Refused("invalid_manifest", 422);
  const m = value.metadata;
  if (!object(m) || !field(m.title, 100) || !description(m.description)
      || !Object.hasOwn(LANGUAGES, m.default_language) || typeof m.made_for_kids !== "boolean"
      || typeof m.contains_synthetic_media !== "boolean" || !/^[1-9][0-9]?$/.test(String(m.category_id))
      || !Array.isArray(m.tags) || m.tags.length > 100 || !m.tags.every((t) => field(t, 100))
      || m.tags.join(",").length > 500 || !object(m.localizations)
      || Object.entries(m.localizations).some(([locale, entry]) => !Object.hasOwn(LANGUAGES, locale)
        || locale === m.default_language || !object(entry) || !field(entry.title, 100) || !description(entry.description))) throw new Refused("invalid_metadata", 422);
  if (!Array.isArray(value.files) || value.files.length > 8) throw new Refused("invalid_files", 422);
  const roles = new Set();
  const files = value.files.map((f) => {
    if (!object(f) || typeof f.role !== "string" || !HASH.test(f.sha256) || !Number.isSafeInteger(f.size) || f.size < 1
        || f.size > 100 * 1024 ** 3 || roles.has(f.role)) throw new Refused("invalid_files", 422);
    roles.add(f.role);
    const media = f.role === "final" ? ["video/mp4"] : f.role === "thumbnail" ? ["image/png", "image/jpeg"]
      : f.role.startsWith("captions_") && Object.hasOwn(LANGUAGES, f.role.slice(9)) ? ["text/plain", "application/x-subrip", "text/vtt"] : [];
    if (!media.includes(f.content_type) || (f.role !== "final" && f.size > 20 * 1024 ** 2)) throw new Refused("invalid_files", 422);
    return { role: f.role, sha256: f.sha256, size: f.size, content_type: f.content_type };
  });
  if (!value.video_id && !roles.has("final")) throw new Refused("video_missing", 422);
  return {
    version: 1, slug: value.slug, review_sha256: value.review_sha256, channel_id: channel,
    video_id: value.video_id,
    metadata: { title: m.title, description: m.description, default_language: m.default_language,
      made_for_kids: m.made_for_kids, contains_synthetic_media: m.contains_synthetic_media,
      category_id: String(m.category_id), tags: m.tags, localizations: m.localizations },
    files,
  };
}
export function jobSteps(manifest) {
  return ["video", "details", ...(manifest.files.some((f) => f.role === "thumbnail") ? ["thumbnail"] : []),
    ...manifest.files.filter((f) => f.role.startsWith("captions_")).map((f) => f.role),
    ...Object.keys(manifest.metadata.localizations).map((locale) => "localization_" + locale), "verify"];
}
