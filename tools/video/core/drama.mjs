// The drama format: a story told through AI-generated shots (docs/videos/DRAMA.md).
//
// A drama video.json adds a look (the style every image and clip shares), characters with their
// own voices, "shot" scenes whose data is a prompt instead of slide fields, a speaker per line,
// music and burned-in subtitles. Everything the format adds is validated here, so schema.mjs
// stays the slides validator plus one call. The hashes below decide what the media stages may
// reuse: a look edit redraws the character sheets, keyframes and clips; a music edit never does.
// It imports nothing from schema.mjs or timeline.mjs: they import it, and a cycle would leave one
// side's bindings undefined at load time.
import { createHash } from "node:crypto";

export const DRAMA_FORMAT = "drama";
const FPS = 30;
export const SHOT_TEMPLATE = "shot";
// Card templates a drama may still use between shots: the title card, chapter cards, the outro.
export const CARD_TEMPLATES = ["title", "chapter", "outro"];
export const NARRATOR = "narrator";
export const CHARACTER_ID = /^[a-z][a-z0-9-]{1,23}$/;
export const FIT_MODES = ["auto", "freeze", "slow", "trim"];
export const TRANSITIONS = ["cut", "dissolve"];
export const SUBTITLE_STYLES = ["drama", "plain"];
export const MUSIC_TRACK = /^[a-z0-9][a-z0-9._-]{0,63}\.(?:mp3|m4a|wav|flac)$/;
const SHA256 = /^[0-9a-f]{64}$/;
export const MAX_SHOT_CHARACTERS = 3;
export const MAX_SHOT_SECONDS = 12;
export const WARN_SHOT_SECONDS = 10;
export const MIN_MEDIAN_SHOT_SECONDS = 3;
export const LONG_SHOT_SHARE_WARN = 0.3;
export const PROMPT_SIMILARITY_WARN = 0.8;
export const EMOTION_MAX = 80;
const STYLE_MAX = 400;
const LIMITS = { style: 600, negative: 400, motion: 300, appearance: 800, prompt: 1000, camera: 120, sheet_prompt: 600 };
// Part of every media cache key: bump it and every keyframe and clip is generated again.
export const MEDIA_CACHE_VERSION = "media-v1";

/**
 * Style presets: what "cinematic 3D like the reference" or "2D anime" means as a prompt. A look
 * names one and may override any field; `custom` supplies everything itself.
 */
export const PRESETS = {
  "cinematic-3d": {
    style: "semi-realistic 3D CG render, cinematic lighting, volumetric light, shallow depth of field, 35mm film look, detailed fabric and skin, ancient Chinese fantasy production design",
    negative: "text, watermark, logo, signature, extra fingers, deformed hands, distorted face, modern clothing, blurry, low resolution",
    motion: "slow cinematic camera move, subtle natural motion, consistent character, no morphing, no cuts",
  },
  "anime-2d": {
    style: "2D anime illustration, clean line art, cel shading, painterly background, consistent character design",
    negative: "text, watermark, logo, photorealistic, 3D render, extra fingers, deformed hands, blurry",
    motion: "gentle camera move, limited animation, consistent character design, no morphing, no cuts",
  },
  "ink-wash": {
    style: "Chinese ink wash painting style, soft brush strokes, muted palette, misty atmosphere, consistent character design",
    negative: "text, watermark, logo, photorealistic, neon colours, extra fingers, blurry",
    motion: "slow drifting camera, ink diffusing softly, no morphing, no cuts",
  },
  custom: { style: "", negative: "", motion: "" },
};
export const PRESET_NAMES = Object.keys(PRESETS);
export const DEFAULT_LOOK_CANDIDATES = 3;
export const DEFAULT_MUSIC = { gain_db: -20, duck_db: -10, fade_in_ms: 1500, fade_out_ms: 3000 };

const LOOK_KEYS = new Set(["preset", "style", "negative", "motion", "candidates", "style_frames"]);
const CHARACTER_KEYS = new Set(["id", "name", "appearance", "voice", "sheet_prompt"]);
const SHOT_KEYS = new Set(["prompt", "camera", "motion", "negative", "characters", "fit", "seed", "transition", "start_frame", "end_frame"]);
const MUSIC_KEYS = new Set(["prompt", "track", "sha256", "gain_db", "duck_db", "fade_in_ms", "fade_out_ms"]);
const SUBTITLE_KEYS = new Set(["burn_in", "style", "speaker_prefix"]);

const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isText = (value) => typeof value === "string" && value.trim().length > 0;
const isShortText = (value, max) => isText(value) && value.length <= max;
const inRange = (value, low, high) => typeof value === "number" && Number.isFinite(value) && value >= low && value <= high;
const hash16 = (...parts) => {
  const digest = createHash("sha256");
  for (const part of parts) digest.update(typeof part === "string" ? part : JSON.stringify(part));
  return digest.digest("hex").slice(0, 16);
};

export const isDrama = (doc) => doc?.format === DRAMA_FORMAT;
export const isShot = (scene) => scene?.template === SHOT_TEMPLATE;
export const shotScenes = (doc) => (doc?.scenes ?? []).filter(isShot);

/** Scenes and lines in order with lint-style labels (schema.mjs's eachLine, kept local to avoid the cycle). */
function* lines(doc) {
  for (const [sceneIndex, scene] of (doc.scenes ?? []).entries()) {
    for (const [lineIndex, line] of (scene.lines ?? []).entries()) {
      yield { scene, line, label: `scenes[${sceneIndex}].lines[${lineIndex}]${typeof line?.id === "string" ? ` (${line.id})` : ""}` };
    }
  }
}
const spoken = (line) => line.say ?? line.text;

function unknownKeys(value, allowed, where, errors) {
  for (const key of Object.keys(value)) {
    if (!allowed.has(key)) errors.push({ path: `${where}.${key}`, message: `unknown field "${key}"` });
  }
}

/** The look with its preset's defaults filled in, so every stage prompts the same way. */
export function resolveLook(look) {
  const preset = PRESETS[look?.preset ?? "custom"] ?? PRESETS.custom;
  return {
    preset: look?.preset ?? "custom",
    style: look?.style ?? preset.style,
    negative: look?.negative ?? preset.negative,
    motion: look?.motion ?? preset.motion,
    candidates: look?.candidates ?? DEFAULT_LOOK_CANDIDATES,
    style_frames: look?.style_frames ?? [],
  };
}

export function resolveSubtitles(doc) {
  const own = doc?.subtitles ?? {};
  return { burn_in: own.burn_in ?? isDrama(doc), style: own.style ?? "drama", speaker_prefix: own.speaker_prefix ?? false };
}

export function resolveMusic(doc) {
  return doc?.music ? { ...DEFAULT_MUSIC, ...doc.music } : null;
}

export const burnIn = (doc) => resolveSubtitles(doc).burn_in;

function validateLook(look, errors) {
  if (!isObject(look)) {
    errors.push({ path: "look", message: "must be an object: the style every image and clip shares" });
    return;
  }
  unknownKeys(look, LOOK_KEYS, "look", errors);
  if (look.preset !== undefined && !PRESET_NAMES.includes(look.preset)) {
    errors.push({ path: "look.preset", message: `must be one of ${PRESET_NAMES.join(", ")}` });
  }
  if ((look.preset === undefined || look.preset === "custom") && !isText(look.style)) {
    errors.push({ path: "look.style", message: "a custom look needs a style prompt; or name a preset" });
  }
  for (const key of ["style", "negative", "motion"]) {
    if (look[key] !== undefined && !(typeof look[key] === "string" && look[key].length <= LIMITS[key])) {
      errors.push({ path: `look.${key}`, message: `must be text of at most ${LIMITS[key]} characters` });
    }
  }
  if (look.candidates !== undefined && !(Number.isInteger(look.candidates) && look.candidates >= 2 && look.candidates <= 4)) {
    errors.push({ path: "look.candidates", message: "must be 2 to 4 character sheets to choose from" });
  }
  if (look.style_frames !== undefined && !(Array.isArray(look.style_frames) && look.style_frames.length <= 2 && look.style_frames.every((frame) => isShortText(frame, LIMITS.prompt)))) {
    errors.push({ path: "look.style_frames", message: "must be at most 2 prompts for style anchor images" });
  }
}

function validateCharacters(characters, errors, validateVoice) {
  if (!Array.isArray(characters)) {
    errors.push({ path: "characters", message: "must be an array (empty for a narrator-only drama)" });
    return new Set();
  }
  const ids = new Map();
  characters.forEach((character, index) => {
    const where = `characters[${index}]`;
    if (!isObject(character)) {
      errors.push({ path: where, message: "must be an object" });
      return;
    }
    unknownKeys(character, CHARACTER_KEYS, where, errors);
    if (typeof character.id !== "string" || !CHARACTER_ID.test(character.id) || character.id === NARRATOR) {
      errors.push({ path: `${where}.id`, message: `must be 2-24 lowercase letters, digits or hyphens, and not "${NARRATOR}"` });
    } else if (ids.has(character.id)) {
      errors.push({ path: `${where}.id`, message: `duplicates ${ids.get(character.id)}` });
    } else {
      ids.set(character.id, where);
    }
    if (!isText(character.name)) errors.push({ path: `${where}.name`, message: "must be the character's name as the viewer reads it" });
    if (!isShortText(character.appearance, LIMITS.appearance)) {
      errors.push({ path: `${where}.appearance`, message: `must describe the character for the image model, at most ${LIMITS.appearance} characters` });
    }
    if (character.sheet_prompt !== undefined && !isShortText(character.sheet_prompt, LIMITS.sheet_prompt)) {
      errors.push({ path: `${where}.sheet_prompt`, message: `must be text of at most ${LIMITS.sheet_prompt} characters` });
    }
    validateVoice(character.voice, errors, `${where}.voice`);
  });
  return new Set(ids.keys());
}

function validateShotData(data, where, characterIds, earlierShots, errors) {
  if (!isObject(data)) return;
  unknownKeys(data, SHOT_KEYS, where, errors);
  if (!isShortText(data.prompt, LIMITS.prompt)) errors.push({ path: `${where}.prompt`, message: `must describe the picture, at most ${LIMITS.prompt} characters` });
  for (const key of ["camera", "motion", "negative"]) {
    if (data[key] !== undefined && !isShortText(data[key], LIMITS[key])) errors.push({ path: `${where}.${key}`, message: `must be text of at most ${LIMITS[key]} characters` });
  }
  if (data.characters !== undefined) {
    if (!Array.isArray(data.characters) || data.characters.length > MAX_SHOT_CHARACTERS || new Set(data.characters).size !== data.characters.length) {
      errors.push({ path: `${where}.characters`, message: `must list at most ${MAX_SHOT_CHARACTERS} distinct character ids` });
    } else {
      for (const id of data.characters) if (!characterIds.has(id)) errors.push({ path: `${where}.characters`, message: `"${id}" is not in characters` });
    }
  }
  if (data.fit !== undefined && !FIT_MODES.includes(data.fit)) errors.push({ path: `${where}.fit`, message: `must be one of ${FIT_MODES.join(", ")}` });
  if (data.seed !== undefined && !(Number.isInteger(data.seed) && data.seed >= 0 && data.seed <= 2_147_483_647)) errors.push({ path: `${where}.seed`, message: "must be a non-negative 31-bit integer" });
  if (data.transition !== undefined && !TRANSITIONS.includes(data.transition)) errors.push({ path: `${where}.transition`, message: `must be one of ${TRANSITIONS.join(", ")}` });
  if (data.start_frame !== undefined) {
    if (!isObject(data.start_frame) || data.start_frame.at !== "last" || !earlierShots.has(data.start_frame.shot)) {
      errors.push({ path: `${where}.start_frame`, message: 'must be { shot: "<an earlier shot id>", at: "last" }: the clip continues from that shot\'s last frame' });
    }
  }
  if (data.end_frame !== undefined && !(isObject(data.end_frame) && isShortText(data.end_frame.prompt, LIMITS.prompt))) {
    errors.push({ path: `${where}.end_frame`, message: "must be { prompt } for the shot's last frame" });
  }
}

function validateMusic(music, errors) {
  if (!isObject(music)) {
    errors.push({ path: "music", message: "must be an object with a prompt to generate a track, or a track file name" });
    return;
  }
  unknownKeys(music, MUSIC_KEYS, "music", errors);
  if (music.prompt === undefined && music.track === undefined) errors.push({ path: "music", message: "needs a prompt (generated) or a track (a file in <workdir>/../_music/)" });
  if (music.prompt !== undefined && !isShortText(music.prompt, LIMITS.prompt)) errors.push({ path: "music.prompt", message: `must be text of at most ${LIMITS.prompt} characters` });
  if (music.track !== undefined && !(typeof music.track === "string" && MUSIC_TRACK.test(music.track))) errors.push({ path: "music.track", message: "must be a file name like guqin-mist.mp3 (mp3, m4a, wav or flac)" });
  if (music.sha256 !== undefined && !(typeof music.sha256 === "string" && SHA256.test(music.sha256))) errors.push({ path: "music.sha256", message: "must be the track file's SHA-256, 64 hex characters" });
  if (music.gain_db !== undefined && !inRange(music.gain_db, -40, 0)) errors.push({ path: "music.gain_db", message: "must be -40 to 0 dB" });
  if (music.duck_db !== undefined && !inRange(music.duck_db, -24, 0)) errors.push({ path: "music.duck_db", message: "must be -24 to 0 dB" });
  if (music.fade_in_ms !== undefined && !(Number.isInteger(music.fade_in_ms) && inRange(music.fade_in_ms, 0, 10_000))) errors.push({ path: "music.fade_in_ms", message: "must be 0 to 10000" });
  if (music.fade_out_ms !== undefined && !(Number.isInteger(music.fade_out_ms) && inRange(music.fade_out_ms, 0, 15_000))) errors.push({ path: "music.fade_out_ms", message: "must be 0 to 15000" });
}

function validateSubtitles(subtitles, errors) {
  if (!isObject(subtitles)) {
    errors.push({ path: "subtitles", message: "must be an object: { burn_in, style, speaker_prefix }" });
    return;
  }
  unknownKeys(subtitles, SUBTITLE_KEYS, "subtitles", errors);
  if (subtitles.burn_in !== undefined && typeof subtitles.burn_in !== "boolean") errors.push({ path: "subtitles.burn_in", message: "must be true or false" });
  if (subtitles.style !== undefined && !SUBTITLE_STYLES.includes(subtitles.style)) errors.push({ path: "subtitles.style", message: `must be one of ${SUBTITLE_STYLES.join(", ")}` });
  if (subtitles.speaker_prefix !== undefined && typeof subtitles.speaker_prefix !== "boolean") errors.push({ path: "subtitles.speaker_prefix", message: "must be true or false" });
}

/**
 * Every drama-only rule, appended to `errors`. Runs after the shared structure checks, so the
 * scenes and lines are known to be objects with ids. `validateVoice(voice, errors, where)` is
 * schema.mjs's voice check, passed in to avoid an import cycle.
 */
export function validateDrama(doc, errors, validateVoice) {
  const drama = isDrama(doc);
  if (!drama) {
    for (const key of ["characters", "look"]) {
      if (doc[key] !== undefined) errors.push({ path: key, message: `only a video with format "${DRAMA_FORMAT}" has ${key}` });
    }
  }
  if (doc.music !== undefined) validateMusic(doc.music, errors);
  if (doc.subtitles !== undefined) validateSubtitles(doc.subtitles, errors);
  if (!Array.isArray(doc.scenes)) return;

  const characterIds = drama ? validateCharacters(doc.characters, errors, validateVoice) : new Set();
  if (drama) validateLook(doc.look, errors);
  const earlierShots = new Set();
  let shots = 0;
  doc.scenes.forEach((scene, sceneIndex) => {
    if (!isObject(scene)) return;
    const where = `scenes[${sceneIndex}]`;
    const shot = isShot(scene);
    if (shot) {
      if (!drama) {
        errors.push({ path: `${where}.template`, message: `"${SHOT_TEMPLATE}" scenes belong to format "${DRAMA_FORMAT}"` });
      } else {
        shots += 1;
        validateShotData(scene.data, `${where}.data`, characterIds, earlierShots, errors);
      }
    } else if (drama && !CARD_TEMPLATES.includes(scene.template)) {
      errors.push({ path: `${where}.template`, message: `a drama scene is a "${SHOT_TEMPLATE}" or one of the cards ${CARD_TEMPLATES.join(", ")}` });
    }
    if (Array.isArray(scene.lines)) {
      scene.lines.forEach((line, lineIndex) => {
        if (!isObject(line)) return;
        const label = `${where}.lines[${lineIndex}]${typeof line.id === "string" ? ` (${line.id})` : ""}`;
        if (!drama) {
          for (const key of ["speaker", "emotion"]) {
            if (line[key] !== undefined) errors.push({ path: `${label}.${key}`, message: `only a video with format "${DRAMA_FORMAT}" has line ${key}` });
          }
          return;
        }
        if (shot && line.reveal !== undefined) errors.push({ path: `${label}.reveal`, message: "a shot has nothing to reveal; split the narration into shots instead" });
        if (line.speaker !== undefined && line.speaker !== NARRATOR && !characterIds.has(line.speaker)) {
          errors.push({ path: `${label}.speaker`, message: `must be "${NARRATOR}" or a character id` });
        }
        if (line.emotion !== undefined && !isShortText(line.emotion, EMOTION_MAX)) {
          errors.push({ path: `${label}.emotion`, message: `must be a short direction for the voice, at most ${EMOTION_MAX} characters` });
        }
      });
    }
    if (shot && typeof scene.id === "string") earlierShots.add(scene.id);
  });
  if (drama && shots === 0) errors.push({ path: "scenes", message: `a drama needs at least one "${SHOT_TEMPLATE}" scene` });
  if (drama && isObject(doc.thumbnail?.data) && doc.thumbnail.data.shot !== undefined && !earlierShots.has(doc.thumbnail.data.shot)) {
    errors.push({ path: "thumbnail.data.shot", message: "must name a shot scene whose keyframe becomes the thumbnail background" });
  }
}

/** The character a line's speaker names, or null for the narrator. */
export function characterOf(doc, line) {
  const speaker = line?.speaker ?? NARRATOR;
  if (speaker === NARRATOR) return null;
  return (doc.characters ?? []).find((character) => character.id === speaker) ?? null;
}

/**
 * The voice a line is synthesized with: the character's own, or the narrator's. A line's emotion
 * rides in a Gemini voice's style prompt; Azure voices have no such field, so lint warns instead.
 */
export function voiceFor(doc, line) {
  const character = characterOf(doc, line);
  const base = character ? character.voice : doc.voice;
  const voice = { ...base };
  if (line?.emotion && voice.provider === "gemini") {
    voice.style = `${voice.style ? `${voice.style}。` : ""}${line.emotion}`.slice(0, STYLE_MAX);
  }
  return voice;
}

/** Everything that changes the character sheets: the resolved look and each character's appearance. */
export function lookHash(doc) {
  const characters = (doc.characters ?? []).map((character) => [character.id, character.appearance, character.sheet_prompt ?? null]);
  return hash16([resolveLook(doc.look), characters]);
}

/** The cache key of one generated image: provider, model, prompt, size, seed and the reference images' hashes. */
export function keyframeKey({ provider, model, prompt, negative = "", width, height, seed = null, references = [] }) {
  return hash16([MEDIA_CACHE_VERSION, "image", provider, model, prompt, negative, width, height, seed, [...references].sort()]);
}

/** The cache key of one generated clip: like a keyframe's, plus the start and end frames and the duration. */
export function clipKey({ provider, model, prompt, negative = "", seconds, resolution, seed = null, startFrame, endFrame = null, references = [] }) {
  return hash16([MEDIA_CACHE_VERSION, "clip", provider, model, prompt, negative, seconds, resolution, seed, startFrame, endFrame, [...references].sort()]);
}

/** What changes the burned-in subtitle strips apart from the words and their timing (those are the speech hash). */
export function subtitlesHash(doc) {
  return hash16(["subtitles", resolveSubtitles(doc)]);
}

/** What changes the audio mix apart from the narration: the music and how it sits under the voice. */
export function mixHash(doc) {
  return hash16(["mix", resolveMusic(doc)]);
}

/** Hash of the shots in order with the clip each one uses, written by `clips` and compared by `assemble`. */
export function clipsHash(shots) {
  return hash16(["clips", shots.map((shot) => [shot.id, shot.sha256])]);
}

/** The words of a shot's prompt, for the near-duplicate warning. */
function promptTokens(scene) {
  return new Set(String(scene.data?.prompt ?? "").toLowerCase().match(/[a-z0-9一-鿿]+/g) ?? []);
}

export function promptSimilarity(a, b) {
  const x = promptTokens(a);
  const y = promptTokens(b);
  if (!x.size || !y.size) return 0;
  let shared = 0;
  for (const token of x) if (y.has(token)) shared += 1;
  return shared / (x.size + y.size - shared);
}

/**
 * Shot-level lint on the estimated timeline: overlong shots are errors (the clip models stop at
 * ten seconds, and a shot frozen for longer looks broken), long or very short runs are warnings.
 * Returns { errors: [{ path, message }], warnings: [...] }.
 */
export function shotProblems(doc, timeline) {
  const errors = [];
  const warnings = [];
  const seconds = [];
  doc.scenes.forEach((scene, index) => {
    if (!isShot(scene)) return;
    const placed = timeline.scenes.find((each) => each.id === scene.id);
    if (!placed) return;
    const length = (placed.end_frame - placed.start_frame) / FPS;
    seconds.push(length);
    const where = `scenes[${index}] (${scene.id})`;
    if (length > MAX_SHOT_SECONDS) errors.push({ path: where, message: `about ${length.toFixed(1)} s of narration; a shot is at most ${MAX_SHOT_SECONDS} s (the clip models stop at 10), split it` });
    else if (length > WARN_SHOT_SECONDS) warnings.push({ path: where, message: `about ${length.toFixed(1)} s; shots over ${WARN_SHOT_SECONDS} s are stretched or frozen to fit` });
    const previous = doc.scenes[index - 1];
    if (previous && isShot(previous) && promptSimilarity(previous, scene) >= PROMPT_SIMILARITY_WARN) {
      warnings.push({ path: where, message: `its prompt is nearly the same as ${previous.id}'s; two near-identical shots read as a stall` });
    }
  });
  if (seconds.length >= 3) {
    const sorted = [...seconds].sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];
    if (median < MIN_MEDIAN_SHOT_SECONDS) warnings.push({ path: "scenes", message: `the median shot is ${median.toFixed(1)} s; cuts this fast read as a montage, merge some shots` });
    const long = seconds.filter((length) => length > WARN_SHOT_SECONDS).length / seconds.length;
    if (long > LONG_SHOT_SHARE_WARN) warnings.push({ path: "scenes", message: `${Math.round(long * 100)}% of the shots run over ${WARN_SHOT_SECONDS} s; the clip models cannot hold a shot that long` });
  }
  return { errors, warnings };
}

/** Lines whose emotion cannot reach the voice (the provider has no style prompt). */
export function emotionProblems(doc) {
  const warnings = [];
  for (const { line, label } of lines(doc)) {
    if (line.emotion && voiceFor(doc, line).provider !== "gemini") {
      warnings.push({ path: label, message: `emotion "${line.emotion}" is ignored: the ${voiceFor(doc, line).provider} voice has no style prompt` });
    }
  }
  return warnings;
}

/** The spoken text per speaker, for tts --dry-run and the budget estimate. */
export function charactersBySpeaker(doc) {
  const totals = {};
  for (const { line } of lines(doc)) {
    const speaker = line.speaker ?? NARRATOR;
    totals[speaker] = (totals[speaker] ?? 0) + [...spoken(line)].length;
  }
  return totals;
}
