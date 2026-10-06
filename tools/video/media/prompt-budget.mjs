// How long an image prompt may be for the model that will draw it, and how a shot's prompt is
// composed to fit. A picture is asked for as "<scene prompt>. Style: <look>. Camera: <move>.
// Characters: <cast>. Corrections: <judge fixes>", and the server appends ". Avoid: <negative>"
// before it reaches the vendor (apps/api/app/video_media/providers/minimax.py), who refuses
// the whole request when that is too long. MiniMax image-01 takes under 1500 characters; a
// riso look's style and avoidance text alone take about a thousand of them, so what is left
// for the scene is the budget the writer has to hear about, not a refusal the next seed cannot
// change (on 2026-10-06 two slides videos blocked on 30 shots refused on every seed).
import { MediaError } from "./client.mjs";

/** Per-vendor prompt limits (the prompt must be strictly shorter), for a server that does not report them. */
export const IMAGE_PROMPT_LIMITS = { minimax: 1500 };
// The vendor of each image model the settings may name by id alone: the worker's settings
// carry the slides image model (`slides.slides_image_model`) without its vendor, and the
// writer's first draft has to hear the budget of the model that will draw it. The ids are the
// catalog's (apps/api/app/video_media/catalog.py; media.test.mjs holds this table to it).
export const IMAGE_MODEL_VENDORS = { "gemini-3-pro-image": "gemini", "gemini-3.1-flash-image": "gemini", "image-01": "minimax" };
// The server's own limit on a prompt field (apps/api/app/video_media/schemas.py MAX_PROMPT_CHARS).
export const DEFAULT_IMAGE_PROMPT_LIMIT = 4000;
// What the server puts between the prompt and the negative prompt: minimax.py's
// f"{request.prompt}. Avoid: {request.negative_prompt}". Both sides spell it the same, and
// media.test.mjs holds this constant to the server's source.
export const AVOID = ". Avoid: ";
// Under this many characters for the scene the look, not the shot, is what has to change.
export const MIN_SHOT_PROMPT_BUDGET = 40;

const STYLE = ". Style: ";
const CAMERA = ". Camera: ";
const CHARACTERS = ". Characters: ";
const CORRECTIONS = ". Corrections: ";

/**
 * The longest prompt the chosen image model takes, exclusive: the server's word for the vendor
 * (`limits.image_prompt_chars_<provider>`), else its word for itself (`limits.image_prompt_chars`),
 * else the table above, else the server's field limit.
 */
export function imagePromptLimit(choice, status) {
  const provider = choice?.provider;
  const limits = status?.limits ?? {};
  const reported = (provider && limits[`image_prompt_chars_${provider}`]) ?? limits.image_prompt_chars;
  if (typeof reported === "number" && Number.isFinite(reported) && reported > 0) return reported;
  return (provider && IMAGE_PROMPT_LIMITS[provider]) ?? DEFAULT_IMAGE_PROMPT_LIMIT;
}

/** The vendor of an image model named by id (IMAGE_MODEL_VENDORS, else a Gemini-looking id), or `fallback`. */
export function imageModelVendor(model, fallback = null) {
  if (typeof model !== "string" || !model) return fallback;
  return IMAGE_MODEL_VENDORS[model] ?? (/^gemini-/.test(model) ? "gemini" : fallback);
}

/** The fixed text that goes round a shot's prompt: style, camera, cast and the server's avoidance text. */
function parts({ look, camera, cast }) {
  return {
    style: look?.style ? `${STYLE}${look.style}` : "",
    camera: camera ? `${CAMERA}${camera}` : "",
    cast: cast ? `${CHARACTERS}${cast}` : "",
    avoid: look?.negative ? `${AVOID}${look.negative}` : "",
  };
}

/** How many characters of a request the look, the camera, the cast and the avoidance text take. */
export function promptOverhead({ look, camera = null, cast = null }) {
  const fixed = parts({ look, camera, cast });
  return fixed.style.length + fixed.camera.length + fixed.cast.length + fixed.avoid.length;
}

/**
 * How many characters a shot's own prompt may have under `limit` once the look, the camera, the
 * cast and the avoidance text are counted. A budget under MIN_SHOT_PROMPT_BUDGET is the look's
 * fault (its style or negative is written for a model with a longer limit), and the owner's.
 */
export function shotPromptBudget({ look, camera = null, cast = null, limit = DEFAULT_IMAGE_PROMPT_LIMIT }) {
  const budget = limit - 1 - promptOverhead({ look, camera, cast });
  if (budget < MIN_SHOT_PROMPT_BUDGET) {
    throw new MediaError(
      `the look leaves ${budget} characters for a shot's prompt under the image model's limit of ${limit}: its style is ${look?.style?.length ?? 0} characters and its negative ${look?.negative?.length ?? 0}; shorten the look (video.json look.style / look.negative) or choose an image model with a longer limit`,
      { code: "video_media_prompt_budget", who: "owner" },
    );
  }
  return budget;
}

/** `text` cut to at most `max` characters at the last word boundary that fits, with no trailing punctuation. */
function cutAtWord(text, max) {
  if (max <= 0) return "";
  if (text.length <= max) return text;
  let cut = text.slice(0, max);
  const space = cut.lastIndexOf(" ");
  if (space > 0) cut = cut.slice(0, space);
  return cut.replace(/[\s,;:.、，；：。]+$/u, "");
}

/**
 * A shot's request text under the model's limit: the scene prompt, then the style, the camera,
 * the cast and the corrections in that order, counted with the avoidance text the server will
 * append. When that is not shorter than `limit` the corrections go first, the last one first
 * (a later fix answers a later take, and the earliest are the ones every take since was asked
 * with); when the scene prompt still does not fit it is cut at a word boundary. The style, the
 * camera, the cast and the negative are never touched: they are the look, and the same in every
 * picture. Returns { prompt, droppedFixes, cutChars }.
 */
export function composeShotPrompt({ prompt, look = null, camera = null, cast = null, fixes = [], limit = DEFAULT_IMAGE_PROMPT_LIMIT }) {
  const scene = String(prompt ?? "");
  const fixed = parts({ look, camera, cast });
  const tail = `${fixed.style}${fixed.camera}${fixed.cast}`;
  const kept = [...(fixes ?? [])];
  const corrections = () => (kept.length ? `${CORRECTIONS}${kept.join("; ")}` : "");
  const length = (text) => text.length + corrections().length + tail.length + fixed.avoid.length;
  let droppedFixes = 0;
  while (length(scene) >= limit && kept.length) {
    kept.pop();
    droppedFixes += 1;
  }
  let text = scene;
  if (length(text) >= limit) {
    const budget = shotPromptBudget({ look, camera, cast, limit });
    text = cutAtWord(scene, budget);
  }
  return { prompt: `${text}${tail}${corrections()}`, droppedFixes, cutChars: scene.length - text.length };
}
