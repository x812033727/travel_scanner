// The shape of docs/videos/<slug>/video.json, the single source every stage of the automated
// video pipeline reads (docs/videos/DESIGN.md explains the pipeline).
//
// Validation is hand-written rather than a JSON Schema library: the repository keeps tool
// dependencies near zero, and an error that names the scene and the line id ("scenes[3].lines[2]
// (k7p2)") is what a writer agent needs to fix its draft, which a generic validator does not give.
import { createHash } from "node:crypto";

import { DRAMA_FORMAT, SHOT_TEMPLATE, validateDrama } from "./drama.mjs";

export const SCHEMA_VERSION = 1;
// drama: AI-generated shots instead of slides (docs/videos/DRAMA.md); its rules live in drama.mjs.
export const FORMATS = ["slides", "screencast", DRAMA_FORMAT];
// Same order as apps/api/app/i18n.py; zh-TW is the narration language.
export const LOCALES = ["zh-TW", "en", "ja", "ko", "zh-CN"];
export const NARRATION_LOCALE = "zh-TW";
export const TEMPLATES = [
  "title",
  "chapter",
  "bullets",
  "compare",
  "steps",
  "table",
  "code",
  "big",
  "diagram",
  "screenshot",
  "outro",
];
export const THUMBNAIL_TEMPLATES = ["thumb"];
export const VOICE_PROVIDERS = ["azure", "gemini"];
// Mirrors the model list and the voice-name pattern in apps/api/app/video_speech/gemini.py.
export const GEMINI_MODELS = ["gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts"];
const GEMINI_VOICE = /^[A-Za-z][A-Za-z0-9_-]{1,79}$/;
const STYLE_MAX = 400;
export const MAX_PAUSE_MS = 5000;
export const DEFAULT_TARGET_MINUTES = [8, 12];

export const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
// Short and random, never positional: inserting a line must not renumber the ones after it,
// because translations, the audio cache and the owner's audio flags all key on these ids.
export const LINE_ID = /^[a-z0-9]{4,8}$/;
export const SCENE_ID = SLUG;
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const RATE = /^[+-]\d{1,2}%$/;

const TOP_KEYS = new Set([
  "schema_version",
  "slug",
  "format",
  "source_guide",
  "target_minutes",
  "voice",
  "youtube",
  "thumbnail",
  "sources",
  "assets",
  "scenes",
  // Drama-only, validated in drama.mjs: the shared look and the cast; music and subtitles for any format.
  "characters",
  "look",
  "music",
  "subtitles",
]);
const VOICE_KEYS = new Set(["provider", "name", "rate", "lang", "style", "model"]);
const YOUTUBE_KEYS = new Set([
  "category_id",
  "made_for_kids",
  "default_language",
  "title",
  "description",
  "tags",
  "video_id",
]);
const SCENE_KEYS = new Set(["id", "chapter", "template", "data", "claims", "lines"]);
const LINE_KEYS = new Set(["id", "text", "say", "say_for", "pause_after_ms", "reveal", "speaker", "emotion"]);

/** A short content hash: what `say_for` and translation `source_hash` fields hold. */
export function textHash(text) {
  return createHash("sha256").update(String(text).normalize("NFC"), "utf8").digest("hex").slice(0, 12);
}

const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;

function unknownKeys(value, allowed, where, errors) {
  for (const key of Object.keys(value)) {
    if (!allowed.has(key)) errors.push({ path: `${where}.${key}`, message: `unknown field "${key}"` });
  }
}

function lineLabel(sceneIndex, lineIndex, line) {
  const id = isObject(line) && typeof line.id === "string" ? ` (${line.id})` : "";
  return `scenes[${sceneIndex}].lines[${lineIndex}]${id}`;
}

/** One voice object: the narration's `voice`, or a drama character's (`where` names which). */
export function validateVoice(voice, errors, where = "voice") {
  if (!isObject(voice)) {
    errors.push({ path: where, message: "must be an object with provider and name" });
    return;
  }
  unknownKeys(voice, VOICE_KEYS, where, errors);
  if (!VOICE_PROVIDERS.includes(voice.provider)) {
    errors.push({ path: `${where}.provider`, message: `must be one of ${VOICE_PROVIDERS.join(", ")}` });
  }
  if (!isText(voice.name)) errors.push({ path: `${where}.name`, message: "must name the voice, e.g. zh-TW-HsiaoChenNeural" });
  if (voice.rate !== undefined && !RATE.test(voice.rate)) {
    errors.push({ path: `${where}.rate`, message: 'must look like "+5%" or "-10%"' });
  }
  if (voice.provider === "gemini") {
    if (isText(voice.name) && !GEMINI_VOICE.test(voice.name)) {
      errors.push({ path: `${where}.name`, message: "a Gemini voice is a name like Sulafat or a voice_... id, without the gemini: prefix" });
    }
    if (voice.rate !== undefined) {
      errors.push({ path: `${where}.rate`, message: "Gemini takes its pace from voice.style; remove rate" });
    }
    if (voice.model !== undefined && !GEMINI_MODELS.includes(voice.model)) {
      errors.push({ path: `${where}.model`, message: `must be one of ${GEMINI_MODELS.join(", ")}` });
    }
  } else if (voice.style !== undefined || voice.model !== undefined) {
    errors.push({ path: where, message: "style and model are for Gemini voices only" });
  }
  if (voice.style !== undefined && !(isText(voice.style) && voice.style.length <= STYLE_MAX)) {
    errors.push({ path: `${where}.style`, message: `must be text of at most ${STYLE_MAX} characters` });
  }
  if (voice.lang !== undefined && voice.lang !== NARRATION_LOCALE) {
    errors.push({ path: `${where}.lang`, message: `narration is ${NARRATION_LOCALE}; omit the field or set it to that` });
  }
}

function validateYoutube(youtube, errors) {
  if (!isObject(youtube)) {
    errors.push({ path: "youtube", message: "must be an object" });
    return;
  }
  unknownKeys(youtube, YOUTUBE_KEYS, "youtube", errors);
  if (!Number.isInteger(youtube.category_id)) {
    errors.push({ path: "youtube.category_id", message: "must be an integer (28 Science & Technology, 27 Education)" });
  }
  if (typeof youtube.made_for_kids !== "boolean") errors.push({ path: "youtube.made_for_kids", message: "must be true or false" });
  if (youtube.default_language !== NARRATION_LOCALE) {
    errors.push({ path: "youtube.default_language", message: `must be ${NARRATION_LOCALE}, the narration language` });
  }
  if (!isText(youtube.title)) errors.push({ path: "youtube.title", message: "must be a non-empty string" });
  if (!isText(youtube.description)) errors.push({ path: "youtube.description", message: "must be a non-empty string" });
  if (!Array.isArray(youtube.tags) || youtube.tags.some((tag) => !isText(tag))) {
    errors.push({ path: "youtube.tags", message: "must be an array of non-empty strings" });
  }
  if (youtube.video_id !== null && youtube.video_id !== undefined && !/^[A-Za-z0-9_-]{11}$/.test(youtube.video_id)) {
    errors.push({ path: "youtube.video_id", message: "must be null or an 11-character YouTube video id" });
  }
}

function validateLine(line, label, seenLines, errors) {
  if (!isObject(line)) {
    errors.push({ path: label, message: "must be an object" });
    return;
  }
  unknownKeys(line, LINE_KEYS, label, errors);
  if (typeof line.id !== "string" || !LINE_ID.test(line.id)) {
    errors.push({ path: `${label}.id`, message: "must be 4-8 lowercase letters or digits; get fresh ones with `cli.mjs ids`" });
  } else if (seenLines.has(line.id)) {
    errors.push({ path: `${label}.id`, message: `duplicates ${seenLines.get(line.id)}` });
  } else {
    seenLines.set(line.id, label);
  }
  if (!isText(line.text)) errors.push({ path: `${label}.text`, message: "must be the narration sentence" });
  if (line.say !== undefined) {
    if (!isText(line.say)) errors.push({ path: `${label}.say`, message: "must be a non-empty string when present" });
    if (typeof line.say_for !== "string") {
      errors.push({ path: `${label}.say_for`, message: "is required with `say`: the textHash of `text` it was written for" });
    }
  } else if (line.say_for !== undefined) {
    errors.push({ path: `${label}.say_for`, message: "only belongs next to `say`" });
  }
  if (
    line.pause_after_ms !== undefined &&
    !(Number.isInteger(line.pause_after_ms) && line.pause_after_ms >= 0 && line.pause_after_ms <= MAX_PAUSE_MS)
  ) {
    errors.push({ path: `${label}.pause_after_ms`, message: `must be an integer from 0 to ${MAX_PAUSE_MS}` });
  }
  if (line.reveal !== undefined && !(Number.isInteger(line.reveal) && line.reveal >= 1)) {
    errors.push({ path: `${label}.reveal`, message: "must be a positive integer: how many new elements appear" });
  }
}

function validateScenes(scenes, errors, format) {
  if (!Array.isArray(scenes) || scenes.length === 0) {
    errors.push({ path: "scenes", message: "must be a non-empty array" });
    return;
  }
  const seenScenes = new Map();
  const seenLines = new Map();
  scenes.forEach((scene, sceneIndex) => {
    const where = `scenes[${sceneIndex}]`;
    if (!isObject(scene)) {
      errors.push({ path: where, message: "must be an object" });
      return;
    }
    unknownKeys(scene, SCENE_KEYS, where, errors);
    if (typeof scene.id !== "string" || !SCENE_ID.test(scene.id)) {
      errors.push({ path: `${where}.id`, message: "must be lowercase words joined by hyphens" });
    } else if (seenScenes.has(scene.id)) {
      errors.push({ path: `${where}.id`, message: `duplicates ${seenScenes.get(scene.id)}` });
    } else {
      seenScenes.set(scene.id, where);
    }
    if (scene.chapter !== undefined && !isText(scene.chapter)) {
      errors.push({ path: `${where}.chapter`, message: "must be a non-empty string when present" });
    }
    if (sceneIndex === 0 && !isText(scene.chapter)) {
      errors.push({ path: `${where}.chapter`, message: "the first scene must open a chapter: YouTube needs one at 00:00" });
    }
    // A drama's "shot" is not an HTML template; drama.mjs checks its data, and refuses it in any other format.
    if (!TEMPLATES.includes(scene.template) && scene.template !== SHOT_TEMPLATE) {
      errors.push({ path: `${where}.template`, message: `must be one of ${TEMPLATES.join(", ")}${format === DRAMA_FORMAT ? ` or ${SHOT_TEMPLATE}` : ""}` });
    }
    if (!isObject(scene.data)) errors.push({ path: `${where}.data`, message: "must be an object (the template's fields)" });
    if (scene.claims !== undefined && (!Array.isArray(scene.claims) || scene.claims.some((claim) => !isText(claim)))) {
      errors.push({ path: `${where}.claims`, message: "must be an array of claim ids from claims.md" });
    }
    if (!Array.isArray(scene.lines) || scene.lines.length === 0) {
      errors.push({ path: `${where}.lines`, message: "must be a non-empty array: a scene lasts as long as its narration" });
      return;
    }
    scene.lines.forEach((line, lineIndex) => validateLine(line, lineLabel(sceneIndex, lineIndex, line), seenLines, errors));
  });
}

/** Every structural problem in a parsed video.json, as { path, message }. Empty means valid. */
export function validateVideo(doc) {
  const errors = [];
  if (!isObject(doc)) return [{ path: "", message: "video.json must hold a JSON object" }];
  unknownKeys(doc, TOP_KEYS, "", errors);
  if (doc.schema_version !== SCHEMA_VERSION) {
    errors.push({ path: "schema_version", message: `must be ${SCHEMA_VERSION}` });
  }
  if (typeof doc.slug !== "string" || !SLUG.test(doc.slug)) {
    errors.push({ path: "slug", message: "must be lowercase words joined by hyphens" });
  }
  if (!FORMATS.includes(doc.format)) errors.push({ path: "format", message: `must be one of ${FORMATS.join(", ")}` });
  if (doc.source_guide !== undefined && (typeof doc.source_guide !== "string" || !SLUG.test(doc.source_guide))) {
    errors.push({ path: "source_guide", message: "must be the slug of a Mokaair content pack" });
  }
  if (
    doc.target_minutes !== undefined &&
    !(
      Array.isArray(doc.target_minutes) &&
      doc.target_minutes.length === 2 &&
      doc.target_minutes.every((value) => typeof value === "number" && value > 0) &&
      doc.target_minutes[0] <= doc.target_minutes[1]
    )
  ) {
    errors.push({ path: "target_minutes", message: "must be [min, max] in minutes" });
  }
  validateVoice(doc.voice, errors);
  validateYoutube(doc.youtube, errors);
  if (doc.thumbnail !== undefined) {
    if (!isObject(doc.thumbnail) || !THUMBNAIL_TEMPLATES.includes(doc.thumbnail.template) || !isObject(doc.thumbnail.data)) {
      errors.push({ path: "thumbnail", message: `must be { template: ${THUMBNAIL_TEMPLATES.join("|")}, data: {...} }` });
    }
  }
  if (doc.sources !== undefined) {
    if (!Array.isArray(doc.sources)) {
      errors.push({ path: "sources", message: "must be an array" });
    } else {
      doc.sources.forEach((source, index) => {
        if (!isObject(source) || !isText(source.title) || !/^https:\/\//.test(source.url ?? "") || !DATE.test(source.checked_on ?? "")) {
          errors.push({ path: `sources[${index}]`, message: "must be { title, url (https), checked_on (YYYY-MM-DD) }" });
        }
      });
    }
  }
  if (doc.assets !== undefined) {
    if (!Array.isArray(doc.assets)) {
      errors.push({ path: "assets", message: "must be an array" });
    } else {
      doc.assets.forEach((asset, index) => {
        if (!isObject(asset) || !isText(asset.path) || !isText(asset.source) || !isText(asset.license)) {
          errors.push({ path: `assets[${index}]`, message: "must be { path, source, license }" });
        }
      });
    }
  }
  validateScenes(doc.scenes, errors, doc.format);
  validateDrama(doc, errors, validateVoice);
  return errors;
}

/** Scenes and lines in narration order, with their position labels, for the other modules. */
export function* eachLine(doc) {
  for (const [sceneIndex, scene] of doc.scenes.entries()) {
    for (const [lineIndex, line] of scene.lines.entries()) {
      yield { scene, sceneIndex, line, lineIndex, label: lineLabel(sceneIndex, lineIndex, line), last: lineIndex === scene.lines.length - 1 };
    }
  }
}

/** The words the voice will actually say for a line. */
export function spokenText(line) {
  return line.say ?? line.text;
}
