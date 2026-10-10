// The shape of docs/videos/<slug>/video.json, the single source every stage of the automated
// video pipeline reads (docs/videos/DESIGN.md explains the pipeline).
//
// Validation is hand-written rather than a JSON Schema library: the repository keeps tool
// dependencies near zero, and an error that names the scene and the line id ("scenes[3].lines[2]
// (k7p2)") is what a writer agent needs to fix its draft, which a generic validator does not give.
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { isCompilation, validateCompilation } from "./compilation.mjs";
import { DRAMA_FORMAT, SHOT_TEMPLATE, timesSilentShots, validateDrama } from "./drama.mjs";
import { SCREENCAST_TEMPLATE } from "../screencast/steps.mjs";
import { hasAnimePolicy, isLongAnime, validateAnimePolicy } from "./anime-policy.mjs";
import { localizationPlanProblems } from "../production/retention.mjs";

export const SCHEMA_VERSION = 1;
// drama: AI-generated shots instead of slides (docs/videos/DRAMA.md); its rules live in drama.mjs.
export const FORMATS = ["slides", "screencast", DRAMA_FORMAT];
// The languages a video can carry (docs/videos/LANGUAGES.md): zh-TW is the narration language,
// the other three are the ones the owner may add. The site itself has five locales
// (apps/api/app/i18n.py, with zh-CN); the owner dropped zh-CN from videos on 2026-10-09.
export const LOCALES = ["zh-TW", "en", "ja", "ko"];
export const NARRATION_LOCALE = "zh-TW";
/** The locale a video is narrated in: its `narration_locale`, zh-TW when it has none or an unknown one. */
export const narrationLocale = (doc) => (LOCALES.includes(doc?.narration_locale) ? doc.narration_locale : NARRATION_LOCALE);
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
  "chat",
  "quote",
  "stats",
  "terminal",
  "cta",
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
// The owner's rule (2026-10-01): every episode runs at least eight minutes, except a drama's.
// The explainer (原來如此事務所) is held to it too; drama.mjs's needsMinimumLength says which.
export const MIN_EPISODE_MINUTES = 8;
/**
 * Short fixtures may override the estimate/final-only floor inside Node's test runner or the
 * repository's stand-in media smoke entry point. An ordinary worker/CLI ignores an override,
 * including zero. The catalogue's actual-body floor is fixed separately in duration.mjs.
 */
export function minEpisodeMinutes(env = process.env, entrypoint = process.argv[1]) {
  const smoke = fileURLToPath(new URL("../assemble/smoke.mjs", import.meta.url));
  const tools = fileURLToPath(new URL("../../", import.meta.url));
  const relative = entrypoint ? path.relative(tools, path.resolve(entrypoint)) : "";
  const repoTest = relative.endsWith(".test.mjs") && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
  const fixtures = (env.NODE_TEST_CONTEXT === "child-v8" && repoTest) || (entrypoint && path.resolve(entrypoint) === path.resolve(smoke));
  const raw = env.VIDEO_MIN_EPISODE_MINUTES;
  const value = raw === undefined || raw === "" ? NaN : Number(raw);
  return fixtures && Number.isFinite(value) && value >= 0 ? value : MIN_EPISODE_MINUTES;
}

export const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
// What kind of video this is, for /admin/videos' filters: the same list as
// apps/api/app/models.py VIDEO_CATEGORIES. The site takes it from the first report that
// carries it and leaves a category the owner set on the page alone.
export const VIDEO_CATEGORIES = ["ai-terms", "ai-news", "tutorial", "comparison", "explainer", "story", "drama", "long-drama", "anime", "travel", "other"];
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
  // The language the voice reads and the captions translate from; zh-TW when absent.
  "narration_locale",
  "source_guide",
  "category",
  "target_minutes",
  "voice",
  "pronunciation_hints",
  "localization_plan",
  "youtube",
  "thumbnail",
  "sources",
  "assets",
  "scenes",
  // Validated in drama.mjs: the cast is drama-only; the look belongs to a drama or to illustrated
  // slides (docs/videos/ILLUSTRATED.md); music, sound effects and subtitles may go with any format.
  "characters",
  "look",
  "music",
  "sfx",
  "subtitles",
  // Drama-only: which long series and episode this is (docs/videos/SERIES.md).
  "series",
  // A series' compilation, validated in compilation.mjs: the episodes it joins (docs/videos/BINGE.md).
  "compilation",
  "production_policy",
  "runtime_spec",
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
const SCENE_KEYS = new Set(["id", "chapter", "template", "data", "claims", "lines", "action_seconds"]);
const LINE_KEYS = new Set(["id", "text", "say", "say_for", "pause_after_ms", "reveal", "speaker", "emotion", "audio_ref"]);

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
export function validateVoice(voice, errors, where = "voice", locale = NARRATION_LOCALE) {
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
  if (voice.lang !== undefined && voice.lang !== locale) {
    errors.push({ path: `${where}.lang`, message: `narration is ${locale}; omit the field or set it to that` });
  }
}

function validateYoutube(youtube, errors, locale = NARRATION_LOCALE) {
  if (!isObject(youtube)) {
    errors.push({ path: "youtube", message: "must be an object" });
    return;
  }
  unknownKeys(youtube, YOUTUBE_KEYS, "youtube", errors);
  if (!Number.isInteger(youtube.category_id)) {
    errors.push({ path: "youtube.category_id", message: "must be an integer (28 Science & Technology, 27 Education)" });
  }
  if (typeof youtube.made_for_kids !== "boolean") errors.push({ path: "youtube.made_for_kids", message: "must be true or false" });
  if (youtube.default_language !== locale) {
    errors.push({ path: "youtube.default_language", message: `must be ${locale}, the narration language` });
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
  if (line.audio_ref !== undefined && !(typeof line.audio_ref === "string" && LINE_ID.test(line.audio_ref) && seenLines.has(line.audio_ref) && line.audio_ref !== line.id)) {
    errors.push({ path: `${label}.audio_ref`, message: "must name an earlier original line's take; no forward or self references" });
  }
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

function validateScenes(scenes, errors, format, compilation = false, doc = null) {
  // A compilation's scenes are its cards, and one without cards or an outro has none at all.
  if (!Array.isArray(scenes) || (scenes.length === 0 && !compilation)) {
    errors.push({ path: "scenes", message: compilation ? "must be an array" : "must be a non-empty array" });
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
    // A compilation's chapters are its episodes, one each, wherever its first card sits.
    if (sceneIndex === 0 && !compilation && !isText(scene.chapter)) {
      errors.push({ path: `${where}.chapter`, message: "the first scene must open a chapter: YouTube needs one at 00:00" });
    }
    // A "shot" is not an HTML template: a drama's clip or still, or a slides video's illustration; drama.mjs checks its data.
    // A "screencast" is stills a browser takes from steps on a public page (tools/video/screencast); lint checks its steps.
    if (!TEMPLATES.includes(scene.template) && scene.template !== SHOT_TEMPLATE && scene.template !== SCREENCAST_TEMPLATE) {
      errors.push({ path: `${where}.template`, message: `must be one of ${TEMPLATES.join(", ")}, ${SHOT_TEMPLATE} or ${SCREENCAST_TEMPLATE}` });
    }
    if (!isObject(scene.data)) errors.push({ path: `${where}.data`, message: "must be an object (the template's fields)" });
    if (scene.claims !== undefined && (!Array.isArray(scene.claims) || scene.claims.some((claim) => !isText(claim)))) {
      errors.push({ path: `${where}.claims`, message: "must be an array of claim ids from claims.md" });
    }
    const action = scene.action_seconds !== undefined;
    const validAnime = isLongAnime(doc) && validateAnimePolicy(doc).length === 0;
    // A silent shot is timed by hand: in a long anime under its production policy, and in a
    // drama with a cast that carries no length floor (a beat in which nobody speaks,
    // docs/videos/DRAMA.md). A narrated video and a knowledge long-form have none: their
    // narration is their clock, and their floors are measured on that narration.
    const timedAction = validAnime || timesSilentShots(doc);
    if (action) {
      if (!timedAction) errors.push({ path: `${where}.action_seconds`, message: "requires a drama with a cast and no length floor, or a complete long-anime production policy" });
      if (!Number.isSafeInteger(scene.action_seconds) || scene.action_seconds < 1 || scene.action_seconds > 8) errors.push({ path: `${where}.action_seconds`, message: "must be an integer from 1 to 8 seconds of visible action" });
      if (scene.template !== SHOT_TEMPLATE || !isText(scene.data?.prompt) || !isText(scene.data?.motion)) errors.push({ path: `${where}.action_seconds`, message: "requires a directed shot with a visible-action prompt and motion" });
      if (!Array.isArray(scene.lines) || scene.lines.length !== 0) errors.push({ path: `${where}.lines`, message: "a timed action shot has an empty lines array; dialogue uses measured speech timing" });
    }
    if (!Array.isArray(scene.lines) || (scene.lines.length === 0 && !(action && timedAction))) {
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
  if (hasAnimePolicy(doc)) {
    for (const message of validateAnimePolicy(doc)) errors.push({ path: "production_policy", message });
  } else if (doc.format === DRAMA_FORMAT && doc.category === "anime" && Array.isArray(doc.target_minutes) && doc.target_minutes.some((value) => value > 8)) {
    errors.push({ path: "production_policy", message: "an anime episode longer than eight minutes requires an explicit long-anime production policy" });
  }
  if (doc.schema_version !== SCHEMA_VERSION) {
    errors.push({ path: "schema_version", message: `must be ${SCHEMA_VERSION}` });
  }
  if (typeof doc.slug !== "string" || !SLUG.test(doc.slug)) {
    errors.push({ path: "slug", message: "must be lowercase words joined by hyphens" });
  }
  if (!FORMATS.includes(doc.format)) errors.push({ path: "format", message: `must be one of ${FORMATS.join(", ")}` });
  if (doc.narration_locale !== undefined && !LOCALES.includes(doc.narration_locale)) {
    errors.push({ path: "narration_locale", message: `must be one of ${LOCALES.join(", ")}; leave it out for ${NARRATION_LOCALE}` });
  }
  const locale = narrationLocale(doc);
  if (doc.localization_plan !== undefined) {
    for (const message of localizationPlanProblems(doc.localization_plan)) errors.push({ path: "localization_plan", message });
  }
  if (doc.source_guide !== undefined && (typeof doc.source_guide !== "string" || !SLUG.test(doc.source_guide))) {
    errors.push({ path: "source_guide", message: "must be the slug of a Mokaair content pack" });
  }
  if (doc.category !== undefined && !VIDEO_CATEGORIES.includes(doc.category)) {
    errors.push({ path: "category", message: `must be one of ${VIDEO_CATEGORIES.join(", ")}` });
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
  // A compilation narrates nothing, so its voice is optional; anything else needs one.
  const compilation = isCompilation(doc);
  if (!compilation || doc.voice !== undefined) validateVoice(doc.voice, errors, "voice", locale);
  validateYoutube(doc.youtube, errors, locale);
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
  validateScenes(doc.scenes, errors, doc.format, compilation, doc);
  // A compilation is a drama without shots, a cast or a look: compilation.mjs has its rules,
  // and the drama rules (which would demand all three) do not apply.
  if (compilation) validateCompilation(doc, errors);
  else validateDrama(doc, errors, validateVoice);
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
