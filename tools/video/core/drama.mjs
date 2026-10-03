// The drama format: a story told through AI-generated shots (docs/videos/DRAMA.md).
//
// A drama video.json adds a look (the style every image and clip shares), characters with their
// own voices, "shot" scenes whose data is a prompt instead of slide fields, a speaker per line,
// music and optional legacy burned-in subtitles (new productions use CC). Everything the format adds is validated here, so schema.mjs
// stays the slides validator plus one call. The hashes below decide what the media stages may
// reuse: a look edit redraws the character sheets, keyframes and clips; a music edit never does.
// It imports nothing from schema.mjs or timeline.mjs: they import it, and a cycle would leave one
// side's bindings undefined at load time.
import { createHash } from "node:crypto";
import { substitutions, termPattern } from "./lexicon.mjs";
import { isLongAnime } from "./anime-policy.mjs";

export const DRAMA_FORMAT = "drama";
const FPS = 30;
export const SHOT_TEMPLATE = "shot";
// Card templates a drama may still use between shots: the title card, chapter cards, the outro.
export const CARD_TEMPLATES = ["title", "chapter", "outro"];
// An explainer (the flat-explainer preset, docs/videos/so-thats-why/) also puts its numbers and
// comparisons on cards between the illustrations.
export const EXPLAINER_CARD_TEMPLATES = [...CARD_TEMPLATES, "big", "stats", "compare"];
export const NARRATOR = "narrator";
export const CHARACTER_ID = /^[a-z][a-z0-9-]{1,23}$/;
export const FIT_MODES = ["auto", "freeze", "slow", "trim"];
export const TRANSITIONS = ["cut", "dissolve"];
// How a shot reaches the screen: as a generated clip, or as a still (its keyframe under a slow
// camera move that ffmpeg animates in assemble). A still costs one image instead of clip seconds.
export const VISUAL_MODES = ["clip", "still"];
// A binge series' visual tier caps the share of its shots that may be clips (docs/videos/BINGE.md).
export const VISUAL_TIERS = ["clips", "hybrid", "stills"];
export const TIER_CLIP_SHARE_MAX = { clips: 1, hybrid: 0.4, stills: 0.1 };
export const SUBTITLE_STYLES = ["drama", "plain"];
export const MUSIC_TRACK = /^[a-z0-9][a-z0-9._-]{0,63}\.(?:mp3|m4a|wav|flac)$/;
// An episode of a long series (docs/videos/SERIES.md): the series' slug as the site knows it.
export const SERIES_SLUG = /^[a-z0-9][a-z0-9-]{1,39}$/;
const SHA256 = /^[0-9a-f]{64}$/;
export const MAX_SHOT_CHARACTERS = 3;
export const MAX_SHOT_SECONDS = 12;
export const WARN_SHOT_SECONDS = 10;
// A drama with a cast is cut like the dramas that were measured (drama-craft.md: a median shot
// of 1.5–2.25 s); under 2 s this pipeline pays a clip per cut, so that is where its warning
// starts. A narrated drama (an explainer) and illustrated slides keep the older 3 s.
export const MIN_MEDIAN_SHOT_SECONDS = 2;
export const MIN_MEDIAN_SHOT_SECONDS_NARRATED = 3;
// A clip from the models runs at most this long, so a cut from another shot's clip must end inside it.
export const MAX_SOURCE_CLIP_SECONDS = 10;
export const LONG_SHOT_SHARE_WARN = 0.3;
export const PROMPT_SIMILARITY_WARN = 0.8;
// Picture variety of illustrated slides (docs/videos/ILLUSTRATED.md §畫面不像 AI): three stills in
// a row under one camera move is an error; a place or object in more than a third of the
// pictures, a prompt with no shot size, or one that restates the look's style, each a warning.
export const SAME_MOVE_RUN_MAX = 2;
export const MOTIF_SHARE_WARN = 1 / 3;
export const MOTIF_MIN_SHOTS = 6;
export const EMOTION_MAX = 80;
const STYLE_MAX = 400;
const LIMITS = { style: 600, negative: 400, motion: 300, appearance: 800, prompt: 1000, camera: 120, sheet_prompt: 600 };
// Part of every media cache key: bump it and every keyframe and clip is generated again.
export const MEDIA_CACHE_VERSION = "media-v1";

/**
 * Style presets: what "cinematic 3D like the reference" or "2D anime" means as a prompt. A look
 * names one and may override any field; `custom` supplies everything itself.
 */
// What every print look refuses: a render's finish, a machine's composition, a paper margin
// around the picture (or a vertical picture between blurred bars), words and real faces.
const PRINT_NEGATIVE = "photorealistic, 3D render, glossy, airbrushed, smooth gradients, neon glow, bokeh, stock vector, isometric, faceless mannequin, mirror symmetry, paper border, white margin, frame, mat, pillarbox, letterbox, blurred side bars, text, letters, numbers, watermark, logo, brand marks, real person's likeness, mascot, recurring character, extra fingers, deformed hands, cluttered background";
// The two-ink risograph looks: one dark ink, one warm ink, cream paper, in four pairs.
const RISO_INKS = {
  "riso-teal": "a deep teal-green ink and a fluorescent coral-orange ink",
  "riso-navy": "an ink-navy ink and a mustard-yellow ink",
  "riso-forest": "a dark forest-green ink and a bright tangerine ink",
  "riso-plum": "a deep plum ink and a golden-ochre ink",
};
function risoPresets() {
  return Object.fromEntries(Object.entries(RISO_INKS).map(([name, inks]) => [name, {
    style: `risograph print illustration on warm cream paper: ${inks}, overprinted where they meet, visible halftone dot grain, the inks a little off register and not quite covering, shapes built from overlapping flat ink layers with line only where an ink edge makes it, small simple people with dot eyes or seen from behind, one clear focal point in the centre third of the frame with uneven foreground and background layers to either side, the picture runs past all four edges of the frame, matte, slightly rough like a real print, 16:9`,
    negative: PRINT_NEGATIVE,
    motion: "slow push in or gentle drift, no morphing, no cuts",
  }]));
}

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
  // A narrator-only explainer of still illustrations (docs/videos/so-thats-why/look.md): no cast,
  // so nothing asks for a consistent character, and no text in the picture: cards carry it.
  "flat-explainer": {
    style: "flat editorial illustration, bold clean navy outlines, limited palette of warm cream, ink navy, stamp red and mustard yellow, soft paper grain, simple shapes, generous negative space, friendly and clear",
    negative: "photorealistic, 3D render, cinematic lighting, text, letters, watermark, logo, brand marks, real person's likeness, mascot, recurring cartoon character, extra fingers, deformed hands, cluttered background",
    motion: "slow push in or gentle drift, no morphing, no cuts",
  },
  // The channel's own illustrated slides (docs/videos/ILLUSTRATED.md): pictures between the dark
  // data cards, so they share theme.css's ground and accents; no cast, no text in the picture.
  // Written as a printmaker's brief, not a render's: uneven ink, misregistered flat colour and
  // paper grain are what a viewer reads as a hand, and a smooth glossy finish, a lone subject on
  // an empty ground and faceless mannequins are what they read as a machine (§畫面不像 AI). The
  // subject stays in the centre third: a Short covers 9:16 from this 16:9 picture and keeps only
  // the middle 32% of its width (shorts/motion.mjs), so the asymmetry comes from the layers
  // around the subject, never from pushing it to one side.
  "tech-story": {
    style: "hand-drawn editorial illustration for a printed magazine feature: confident ink outlines of slightly uneven weight, flat gouache and screen-print colour with visible paper grain and a little misregistration, textured hand-cut shadows, a limited palette of deep teal-green night ground, warm cream, amber and a touch of brick red, one clear focal point in the centre third of the frame with uneven foreground and background layers to either side, small simple people with dot eyes or seen from behind, matte finish, 16:9",
    negative: "photorealistic, 3D render, CGI, glossy, airbrushed, smooth gradients, neon glow, lens flare, bokeh, stock vector, corporate flat icon style, isometric, faceless mannequin, floating objects, mirror symmetry, text, letters, numbers, watermark, logo, brand marks, real person's likeness, mascot, recurring cartoon character, extra fingers, deformed hands, cluttered background",
    motion: "slow push in or gentle drift, no morphing, no cuts",
  },
  // The channel's print looks since 2026-10-03 (docs/videos/ILLUSTRATED.md §第二輪): the same
  // two-ink risograph print in four pairs of inks, and a linocut, chosen per video by its slug
  // (slidesPresetFor) so each video is its own print run while the channel stays one printer.
  // Drawn and compared on 2026-10-03 against the tech-story look: a print's halftone grain,
  // overprint and off-register inks are what a viewer reads as a hand, where an even ink
  // outline around everything reads as a children's book drawn by a machine. The phrase
  // "full-bleed, edge to edge" makes the model paint a paper margin around the picture, so the
  // looks say the picture runs past the frame and the negative refuses borders instead.
  ...risoPresets(),
  "linocut-teal": {
    style: "two-colour linocut relief print on cream paper: bold carved marks and gouged textures, a deep teal-black key block with an ochre and a brick-red spot colour printed a little off register, rough carved edges, chunky simplified shapes, ink unevenly rolled so some areas print lighter, small simple people with carved dot eyes or seen from behind, one clear focal point in the centre third of the frame with uneven foreground and background layers to either side, the picture runs past all four edges of the frame, matte paper, 16:9",
    negative: PRINT_NEGATIVE,
    motion: "slow push in or gentle drift, no morphing, no cuts",
  },
  custom: { style: "", negative: "", motion: "" },
};
export const EXPLAINER_PRESET = "flat-explainer";
/** The print looks a slides video's illustrations rotate through (docs/videos/ILLUSTRATED.md §第二輪), in rotation order. */
export const SLIDES_PRESETS = ["riso-teal", "riso-navy", "riso-forest", "riso-plum", "linocut-teal"];
/** The look a slides video's illustrations take when nothing chooses one (the first of the rotation). */
export const SLIDES_PRESET = SLIDES_PRESETS[0];
/**
 * The print look of a slides video with no look of its own: one of SLIDES_PRESETS by the slug,
 * so two videos written the same week come off different print runs and the same video always
 * gets the same one (the look is in lookHash; a rotation by date would redraw a video rerun
 * later). The writer may still name one, and the owner may set one in video.json.
 */
export function slidesPresetFor(slug) {
  let hash = 2166136261;
  for (const char of String(slug ?? "")) hash = Math.imul(hash ^ char.charCodeAt(0), 16777619) >>> 0;
  return SLIDES_PRESETS[hash % SLIDES_PRESETS.length];
}
export const PRESET_NAMES = Object.keys(PRESETS);
export const DEFAULT_LOOK_CANDIDATES = 3;
export const DEFAULT_MUSIC = { gain_db: -20, duck_db: -10, fade_in_ms: 1500, fade_out_ms: 3000 };

const LOOK_KEYS = new Set(["preset", "style", "negative", "motion", "candidates", "style_frames"]);
const CHARACTER_KEYS = new Set(["id", "name", "appearance", "voice", "sheet_prompt", "shot_looks"]);
const SHOT_KEYS = new Set(["prompt", "camera", "motion", "negative", "characters", "character_looks", "fit", "seed", "transition", "start_frame", "end_frame", "visual", "source"]);
const MUSIC_KEYS = new Set(["prompt", "track", "sha256", "gain_db", "duck_db", "fade_in_ms", "fade_out_ms"]);
const SUBTITLE_KEYS = new Set(["burn_in", "style", "speaker_prefix"]);
// Sound effects (docs/videos/ILLUSTRATED.md): a licensed set under <work base>/_sfx/<set>/, placed
// by rules in assemble (a stamp on chapter cards, a whoosh into a dissolve, a pop on a reveal).
const SFX_KEYS = new Set(["set", "gain_db"]);
export const SFX_SET = /^[a-z0-9][a-z0-9._-]{0,63}$/;
export const DEFAULT_SFX = { gain_db: -12 };
const SERIES_KEYS = new Set(["slug", "episode", "chapter"]);
const ANIME_SERIES_KEYS = new Set([...SERIES_KEYS, "kind", "genre", "lead", "planned_episodes", "open_ended", "closed_ending"]);

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
export const isSeriesEpisode = (doc) => isDrama(doc) && isObject(doc.series);
/** A drama drawn in the explainer preset: narrator only, every shot a still. */
export const isExplainer = (doc) => isDrama(doc) && doc.look?.preset === EXPLAINER_PRESET;
/**
 * Whether the eight-minute floor (MIN_EPISODE_MINUTES) holds: slides, screencasts and the
 * explainer, never a drama episode, a brand story or a compilation.
 */
export const needsMinimumLength = (doc) => (!isDrama(doc) || isExplainer(doc)) && !isObject(doc?.compilation);
/** Whether a drama has characters: without any there are no sheets, so no look stage or gate. */
export const hasCast = (doc) => isDrama(doc) && Array.isArray(doc.characters) && doc.characters.length > 0;
// The knowledge and nonfiction long-video catalogues (duration.mjs): a brand story, an AI term,
// an explainer, each held to a 480-second floor that is measured on its narration.
const LONG_FORMATS = new Set(["slides", "screencast", "drama"]);
const KNOWLEDGE_CATEGORIES = new Set(["ai-terms", "explainer", "story"]);
const CATALOGUE_SLUG = /^(?:sothatswhy-|ai-term-|story-)/;
/** Ordinary drama episodes, binge compilations and Shorts retain their own duration rules. */
export function isKnowledgeLongform(doc) {
  return Boolean(doc && LONG_FORMATS.has(doc.format) && !doc.compilation && (
    KNOWLEDGE_CATEGORIES.has(doc.category)
    || doc.look?.preset === "flat-explainer"
    || CATALOGUE_SLUG.test(doc.slug ?? "")
  ));
}
/**
 * Whether a shot without lines may be timed with `action_seconds` outside the long-anime policy:
 * a drama with a cast that carries no length floor, so a silent shot can pad nothing. A knowledge
 * long-form (a brand story with leads, an explainer) is measured on its narration, and an anime
 * episode goes through its production policy (anime-policy.mjs) or not at all.
 */
export const timesSilentShots = (doc) => hasCast(doc) && !needsMinimumLength(doc) && !isKnowledgeLongform(doc) && doc?.category !== "anime";
export const isShot = (scene) => scene?.template === SHOT_TEMPLATE;
export const shotScenes = (doc) => (doc?.scenes ?? []).filter(isShot);
/**
 * A slides video with illustrations (docs/videos/ILLUSTRATED.md): still shots between its cards,
 * drawn by the keyframes stage and animated by assemble like an explainer's. Not a drama: it
 * keeps the slides steps, prompts, pace QA and dubs, and gains the picture and music steps.
 */
export const illustrated = (doc) => !isDrama(doc) && shotScenes(doc).length > 0;
/** Whether the keyframes stage draws for this video: a drama, or illustrated slides. */
export const hasPictures = (doc) => isDrama(doc) || illustrated(doc);
/** "clip" or "still": a shot is a clip unless it says otherwise. */
export const shotVisual = (scene) => scene?.data?.visual ?? "clip";
export const isClipShot = (scene) => isShot(scene) && shotVisual(scene) === "clip";
// A shot cut from another shot's clip (`data.source: { shot, from_s }`, docs/videos/DRAMA.md):
// the references return to a camera setup (speaker, listener, speaker) and cut inside one take,
// so such a shot buys neither a keyframe nor a clip; assemble trims the named clip from from_s.
export const isSourced = (scene) => isShot(scene) && isObject(scene?.data?.source);
export const sourcedShotScenes = (doc) => shotScenes(doc).filter(isSourced);
/** The shots that get a keyframe of their own: every shot but one cut from another shot's clip. */
export const drawnShotScenes = (doc) => shotScenes(doc).filter((scene) => !isSourced(scene));
/** The shots the clips stage generates a clip for. */
export const clipShotScenes = (doc) => shotScenes(doc).filter(isClipShot);
/** The shots assemble animates from their keyframe instead. */
export const stillShotScenes = (doc) => shotScenes(doc).filter((scene) => shotVisual(scene) === "still");

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
  return { burn_in: own.burn_in ?? false, style: own.style ?? "drama", speaker_prefix: own.speaker_prefix ?? false };
}

/** Named visual variants share one approved face sheet and one voice. */
export function shotLooksProblem(character) {
  if (character?.shot_looks === undefined) return null;
  const looks = character.shot_looks;
  if (!Array.isArray(looks) || looks.length > 20) return "shot_looks must be a list of at most 20 named appearances";
  const seen = new Set();
  for (const look of looks) {
    if (!isObject(look) || Object.keys(look).some((key) => !["id", "appearance"].includes(key)) || typeof look.id !== "string" || !CHARACTER_ID.test(look.id) || !isShortText(look.appearance, LIMITS.appearance)) return "each shot look needs only id (2-24 lowercase letters, digits or hyphens) and appearance (1-800 characters)";
    if (seen.has(look.id)) return `duplicate shot look ${look.id}`;
    seen.add(look.id);
  }
  return null;
}

/** The shot's appearance, with the original character identity and voice intact. */
export function shotCast(doc, scene) {
  const byId = new Map((Array.isArray(doc.characters) ? doc.characters : []).filter(isObject).map((character) => [character.id, character]));
  return (Array.isArray(scene.data?.characters) ? scene.data.characters : []).map((id) => {
    const character = byId.get(id);
    if (!character) return null;
    const chosen = scene.data?.character_looks?.[id];
    const look = Array.isArray(character.shot_looks) ? character.shot_looks.find((item) => item?.id === chosen) : null;
    return look ? { ...character, appearance: look.appearance, shot_look: look.id } : character;
  }).filter(Boolean);
}

export function shotAppearancePrompt(characters) {
  return characters.map((character) => character.shot_look
    ? `${character.name}: keep the same facial identity and recognizable bone structure as the approved reference sheet; use look ${character.shot_look} for clothing, hair and age instead of the sheet's styling: ${character.appearance}`
    : `${character.name}: ${character.appearance}`).join("; ");
}

export function resolveMusic(doc) {
  return doc?.music ? { ...DEFAULT_MUSIC, ...doc.music } : null;
}

export function resolveSfx(doc) {
  return doc?.sfx ? { ...DEFAULT_SFX, ...doc.sfx } : null;
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
    const looksProblem = shotLooksProblem(character);
    if (looksProblem) errors.push({ path: `${where}.shot_looks`, message: looksProblem });
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
  if (data.visual !== undefined && !VISUAL_MODES.includes(data.visual)) errors.push({ path: `${where}.visual`, message: `must be one of ${VISUAL_MODES.join(", ")}` });
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
  // A still is its keyframe with a camera move: an end frame would be bought and never shown.
  if (data.visual === "still" && data.end_frame !== undefined) errors.push({ path: `${where}.end_frame`, message: "a still shot has no end_frame: it belongs to a clip" });
  if (data.source !== undefined) {
    const origin = isObject(data.source) && typeof data.source.shot === "string" ? earlierShots.get(data.source.shot) : undefined;
    if (!origin || !(typeof data.source.from_s === "number" && Number.isFinite(data.source.from_s) && data.source.from_s >= 0)) {
      errors.push({ path: `${where}.source`, message: 'must be { shot: "<an earlier shot id>", from_s: <seconds, 0 or more> }: the shot is cut from that shot\'s clip, starting there' });
    } else if (shotVisual({ data: origin }) !== "clip" || origin.source !== undefined) {
      errors.push({ path: `${where}.source`, message: `${data.source.shot} must be a clip shot with a clip of its own (not a still, not itself cut from another shot)` });
    }
    if (data.visual === "still") errors.push({ path: `${where}.visual`, message: "a still has no clip to cut from: a shot cut from another shot's clip is a clip shot" });
    for (const key of ["start_frame", "end_frame"]) if (data[key] !== undefined) errors.push({ path: `${where}.${key}`, message: `a shot cut from another shot's clip has no ${key}: that clip is already made` });
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

function validateSfx(sfx, errors) {
  if (!isObject(sfx)) {
    errors.push({ path: "sfx", message: "must be an object { set, gain_db? }: a licensed sound-effect set under <work base>/_sfx/" });
    return;
  }
  unknownKeys(sfx, SFX_KEYS, "sfx", errors);
  if (!(typeof sfx.set === "string" && SFX_SET.test(sfx.set))) errors.push({ path: "sfx.set", message: "must be the set's directory name under <work base>/_sfx/, like studio-a" });
  if (sfx.gain_db !== undefined && !inRange(sfx.gain_db, -40, 0)) errors.push({ path: "sfx.gain_db", message: "must be -40 to 0 dB" });
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
/** `series`: which series and episode this video is, so the cast and the sheets are shared. */
function validateSeries(series, errors, anime = false) {
  if (!isObject(series)) {
    errors.push({ path: "series", message: "must be an object { slug, episode, chapter }" });
    return;
  }
  unknownKeys(series, anime ? ANIME_SERIES_KEYS : SERIES_KEYS, "series", errors);
  if (typeof series.slug !== "string" || !SERIES_SLUG.test(series.slug)) errors.push({ path: "series.slug", message: "must be the series' slug: lowercase letters, digits and hyphens" });
  for (const key of ["episode", "chapter"]) {
    if (!Number.isInteger(series[key]) || series[key] < 1) errors.push({ path: `series.${key}`, message: "must be a positive integer" });
  }
  if (anime) {
    if (!Number.isSafeInteger(series.planned_episodes) || series.planned_episodes < 1 || series.episode > series.planned_episodes) errors.push({ path: "series.planned_episodes", message: "must declare a positive episode count that includes this episode" });
    for (const key of ["open_ended", "closed_ending"]) {
      if (typeof series[key] !== "boolean") errors.push({ path: `series.${key}`, message: "must be the approved series or episode's boolean declaration" });
    }
    const final = series.open_ended === false && series.episode === series.planned_episodes;
    if (series.closed_ending === true && !final) errors.push({ path: "series.closed_ending", message: "only the declared final episode of a closed series can use a closed ending" });
    if (final && series.closed_ending !== true) errors.push({ path: "series.closed_ending", message: "the declared final episode of a closed series must deliver its approved closed ending" });
  }
}

export function validateDrama(doc, errors, validateVoice) {
  const drama = isDrama(doc);
  if (doc.pronunciation_hints !== undefined) {
    const hints = doc.pronunciation_hints;
    if (!drama || !isObject(hints) || Object.keys(hints).length > 300 || Object.entries(hints).some(([term, hint]) => !isShortText(term, 40) || !/[\u3400-\u9fff]/u.test(term) || (hint !== null && !isShortText(hint, 200)))) {
      errors.push({ path: "pronunciation_hints", message: "must be a drama-local map of at most 300 Chinese names/terms (1–40 chars) to short reading directions (1–200 chars) or null" });
    }
  }
  if (!drama) {
    for (const key of ["characters", "series"]) {
      if (doc[key] !== undefined) errors.push({ path: key, message: `only a video with format "${DRAMA_FORMAT}" has ${key}` });
    }
  }
  if (doc.music !== undefined) validateMusic(doc.music, errors);
  if (doc.sfx !== undefined) validateSfx(doc.sfx, errors);
  if (doc.subtitles !== undefined) validateSubtitles(doc.subtitles, errors);
  if (!Array.isArray(doc.scenes)) return;

  const characterIds = drama ? validateCharacters(doc.characters, errors, validateVoice) : new Set();
  // A drama always has a look; illustrated slides need one for their shots, and plain slides may
  // not carry one (there is nothing to draw with it).
  const pictures = drama || doc.scenes.some(isShot);
  if (drama || doc.look !== undefined) validateLook(doc.look, errors);
  if (!drama && pictures && doc.look === undefined) errors.push({ path: "look", message: "illustrations need a look: name a preset such as \"" + SLIDES_PRESET + "\" (docs/videos/ILLUSTRATED.md)" });
  if (!drama && doc.look !== undefined && !pictures) errors.push({ path: "look", message: `a slides video with no "${SHOT_TEMPLATE}" scenes has nothing to draw with a look` });
  const explainer = isExplainer(doc);
  const cards = explainer ? EXPLAINER_CARD_TEMPLATES : CARD_TEMPLATES;
  if (explainer && characterIds.size) errors.push({ path: "characters", message: `an explainer (look preset "${EXPLAINER_PRESET}") has no characters: the narrator tells it` });
  if (drama && doc.series !== undefined) {
    validateSeries(doc.series, errors, isLongAnime(doc));
    // An episode lists its cast by id, so lookHash changes only when the cast itself changes
    // and the series' character sheets are reused (docs/videos/SERIES.md).
    const ids = Array.isArray(doc.characters) ? doc.characters.map((character) => character?.id).filter((id) => typeof id === "string") : [];
    if (ids.some((id, index) => index > 0 && id < ids[index - 1])) errors.push({ path: "characters", message: "an episode of a series lists its characters by id in order" });
  }
  // Each earlier shot's data by id: a continued or a cut-from shot names one of them.
  const earlierShots = new Map();
  const earlierTakes = new Map();
  let shots = 0;
  doc.scenes.forEach((scene, sceneIndex) => {
    if (!isObject(scene)) return;
    const where = `scenes[${sceneIndex}]`;
    const shot = isShot(scene);
    if (shot) {
      shots += 1;
      validateShotData(scene.data, `${where}.data`, characterIds, earlierShots, errors);
      if (!drama && isObject(scene.data) && scene.data.source !== undefined) errors.push({ path: `${where}.data.source`, message: "only a drama's shot is cut from another shot's clip; an illustration is its own picture" });
      if (isLongAnime(doc) && ["freeze", "slow"].includes(scene.data?.fit)) errors.push({ path: `${where}.data.fit`, message: "long-anime story duration cannot be supplied by frozen tails or slowed clips" });
      if (isObject(scene.data) && scene.data.character_looks !== undefined) {
        const selected = scene.data.character_looks;
        if (!drama || !isObject(selected)) errors.push({ path: `${where}.data.character_looks`, message: "must map a drama shot's character ids to their named shot_looks" });
        else for (const [id, lookId] of Object.entries(selected)) {
          const character = (doc.characters ?? []).find((item) => item?.id === id);
          if (!Array.isArray(scene.data.characters) || !scene.data.characters.includes(id) || !Array.isArray(character?.shot_looks) || !character.shot_looks.some((look) => look?.id === lookId)) {
            errors.push({ path: `${where}.data.character_looks.${id}`, message: "must name a shot_look of a character present in this shot" });
          }
        }
      }
      if (explainer && isObject(scene.data) && shotVisual(scene) !== "still") {
        errors.push({ path: `${where}.data.visual`, message: `an explainer's shots are all "still": its keyframe under a camera move, no clip` });
      }
      // A slides illustration is a still under a camera move: no clip, no cast, no clip-only fields.
      if (!drama && isObject(scene.data)) {
        if (shotVisual(scene) !== "still") errors.push({ path: `${where}.data.visual`, message: `a slides illustration is "still": its keyframe under a camera move (docs/videos/ILLUSTRATED.md)` });
        for (const key of ["characters", "fit", "start_frame", "end_frame"]) {
          if (scene.data[key] !== undefined) errors.push({ path: `${where}.data.${key}`, message: `a slides illustration has no ${key}: that belongs to a drama's clips` });
        }
      }
    } else if (drama && !cards.includes(scene.template)) {
      errors.push({ path: `${where}.template`, message: `a drama scene is a "${SHOT_TEMPLATE}" or one of the cards ${cards.join(", ")}` });
    }
    if (Array.isArray(scene.lines)) {
      scene.lines.forEach((line, lineIndex) => {
        if (!isObject(line)) return;
        const label = `${where}.lines[${lineIndex}]${typeof line.id === "string" ? ` (${line.id})` : ""}`;
        if (shot && line.reveal !== undefined) errors.push({ path: `${label}.reveal`, message: "a shot has nothing to reveal; split the narration into shots instead" });
        if (!drama) {
          for (const key of ["speaker", "emotion", "audio_ref"]) {
            if (line[key] !== undefined) errors.push({ path: `${label}.${key}`, message: `only a video with format "${DRAMA_FORMAT}" has line ${key}` });
          }
          return;
        }
        if (line.speaker !== undefined && line.speaker !== NARRATOR && !characterIds.has(line.speaker)) {
          errors.push({ path: `${label}.speaker`, message: `must be "${NARRATOR}" or a character id` });
        }
        if (line.emotion !== undefined && !isShortText(line.emotion, EMOTION_MAX)) {
          errors.push({ path: `${label}.emotion`, message: `must be a short direction for the voice, at most ${EMOTION_MAX} characters` });
        }
        try {
          const voice = voiceFor(doc, line);
          if (line.audio_ref !== undefined) {
            const original = earlierTakes.get(line.audio_ref);
            if (!original || original.audio_ref !== undefined || (original.speaker ?? NARRATOR) !== (line.speaker ?? NARRATOR) || String(spoken(original) ?? "").normalize("NFC").trim() !== String(spoken(line) ?? "").normalize("NFC").trim() || JSON.stringify(voiceFor(doc, original)) !== JSON.stringify(voice)) {
              errors.push({ path: `${label}.audio_ref`, message: "must reference an earlier original take with identical speaker, spoken text and effective voice; pauses may differ" });
            }
          }
        } catch (error) {
          errors.push({ path: label, message: error.message });
        }
        earlierTakes.set(line.id, line);
      });
    }
    if (shot && typeof scene.id === "string") earlierShots.set(scene.id, isObject(scene.data) ? scene.data : {});
  });
  if (drama && shots === 0) errors.push({ path: "scenes", message: `a drama needs at least one "${SHOT_TEMPLATE}" scene` });
  if (pictures && isObject(doc.thumbnail?.data) && doc.thumbnail.data.shot !== undefined && (!earlierShots.has(doc.thumbnail.data.shot) || earlierShots.get(doc.thumbnail.data.shot).source !== undefined)) {
    errors.push({ path: "thumbnail.data.shot", message: "must name a shot scene whose keyframe becomes the thumbnail background (a shot cut from another shot's clip has none)" });
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
  const hints = pronunciationHintsFor(doc, line);
  if (hints.length && voice.provider !== "gemini") throw new Error("pronunciation_hints require a Gemini voice with speech metadata");
  if ((line?.emotion || hints.length) && voice.provider === "gemini") {
    const style = [voice.style, line?.emotion, hints.length ? `發音提示（不唸指示）：${hints.map(([term, hint]) => `${term}＝${hint}`).join("；")}` : null].filter(Boolean).join("。");
    if (doc.pronunciation_hints !== undefined && style.length > STYLE_MAX) throw new Error(`line ${line?.id ?? "?"}: voice direction plus pronunciation exceeds ${STYLE_MAX} characters; shorten the line or direction without dropping required readings`);
    voice.style = style.slice(0, STYLE_MAX);
  }
  return voice;
}

/** Only the names/terms actually spoken by this line, longest match first, never CC replacement. */
export function pronunciationHintsFor(doc, line) {
  if (!isObject(doc?.pronunciation_hints)) return [];
  const entries = substitutions({ terms: doc.pronunciation_hints });
  const pattern = termPattern(entries);
  if (!pattern) return [];
  const readings = new Map(entries);
  const matched = [...new Set(String(spoken(line) ?? "").normalize("NFC").match(pattern) ?? [])];
  return matched.map((term) => [term, readings.get(term)]);
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

/** What changes the sound-effect track apart from the picture's cut points: the set and its gain. */
export function sfxHash(doc) {
  return hash16(["sfx", resolveSfx(doc)]);
}

/** Hash of the shots in order with the clip each one uses, written by `clips` and compared by `assemble`. */
export function clipsHash(shots) {
  return hash16(["clips", shots.map((shot) => [shot.id, shot.sha256])]);
}

/**
 * What a slides video's illustrations are drawn from: each shot's id, prompt and camera word.
 * The keyframes manifest of an illustrated slides video is bound to this and the look, not to
 * visualHash, so a card's text can change without every picture being judged again.
 */
export function picturesHash(doc) {
  return hash16(["pictures", shotScenes(doc).map((scene) => [scene.id, scene.data?.prompt ?? "", scene.data?.camera ?? null])]);
}

/** The pictures a cut was assembled from: each shot's keyframe hash, in scene order, from the keyframes manifest. */
export function keyframesHash(doc, manifest) {
  return clipsHash(shotScenes(doc).map((scene) => ({ id: scene.id, sha256: manifest?.shots?.[scene.id]?.sha256 ?? null })));
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

// The camera words a still may carry, folded to the move they name. assemble/drama.mjs
// (motionMove) reads them the same way: the camera direction alone, never the motion prompt
// (a person who "pushes the box back" or "rises" is not a camera move), on whole words, and a
// shot that names no move drifts. "locked" is the absence of a move: the picture holds still.
export const CAMERA_MOVES = [
  ["drift", /\bdrift(?:s|ing)?\b/],
  ["locked", /\blocked\b|\bstatic\b|\bfixed\b|\btripod\b|\bno camera move\b|\bstill camera\b/],
  ["push in", /\bpush(?:es|ing)?\b|\bdolly(?:ing)? in\b|\bzoom(?:s|ing)? in\b|\bcloser\b|\bmov(?:e|es|ing) in\b/],
  ["pull out", /\bpull(?:s|ing)?\b|\bzoom(?:s|ing)? out\b|\bwiden(?:s|ing)?\b|\bback(?:s|ing)? away\b/],
  ["pan left", /\bpan(?:s|ning)? (?:to the )?left\b|\bleft to right\b/],
  ["pan right", /\bpan(?:s|ning)? (?:to the )?right\b|\bright to left\b/],
  ["tilt up", /\btilt(?:s|ing)? up\b|\bcrane(?:s|ing)? up\b|\brises?\b|\brising\b/],
  ["tilt down", /\btilt(?:s|ing)? down\b|\bcrane(?:s|ing)? down\b|\bdescend(?:s|ing)?\b/],
];
export function cameraMove(data) {
  if (typeof data?.camera !== "string") return "drift";
  const lower = data.camera.toLowerCase();
  return CAMERA_MOVES.find(([, pattern]) => pattern.test(lower))?.[0] ?? "drift";
}
// How close the camera is: a prompt that says none of these leaves the picture to the model's
// habit, a medium shot of a thing in the middle. Every size the writer's guide and the warning
// below name is accepted as written there, in its usual spellings (low-angle, bird's eye, top
// down, over-the-shoulder), and as a size: at the start of the prompt, or followed by shot,
// view, angle or of, so "a medium bowl", "over medium heat" and "a wide street" are not sizes.
const SIZE_WORD = "extreme close[- ]?up|close[- ]?up|close shot|macro|medium|mid shot|wide|establishing|bird'?s[- ]?eye|overhead|from above|from directly above|top[- ]?down|low[- ]angle|worm'?s[- ]?eye|high[- ]angle|aerial|full shot|two[- ]?shot|over[- ]the[- ]shoulder|from behind|in profile|silhouette";
const SHOT_SIZE = new RegExp(`(?:^\\W*(?:${SIZE_WORD})\\b|\\b(?:${SIZE_WORD})(?:[- ]+(?:shot|view|angle)\\b|\\s+of\\b))`, "i");
// What the look already says: a prompt that repeats it pins every picture to one palette and
// one finish, which is the sameness a viewer reads as a slideshow. Only the slides looks' own
// words (the techniques of SLIDES_PRESETS and the palette they share), and "cream" as a colour,
// not as the dairy in a cone, a cake or a coffee.
const LOOK_WORDS = /\b(?:flat (?:editorial )?illustration|editorial illustration|painterly|paper grain|risograph|riso print|linocut|woodcut|gouache|screen[- ]?print|halftone|misregist\w+|teal|(?<!ice[- ])(?<!whipped )(?<!sour )(?<!double )cream(?! cone| cheese| puff| cake| pie| tea| soda| poured| in (?:the|a|his|her) coffee)|amber|16:9)\b/i;
// Where and when the light comes from: a video told entirely at night under one lamp is the
// other sameness (the first scripts put a lamp in a quarter of their pictures and the night in
// half); more than half of the pictures in the dark is a warning per video.
const DARK_LIGHT = /\b(?:night|midnight|dusk|late evening|after dark|\d\s*a\.?m\b|lamp|lamplight|lantern|candle|torch|moonlight|neon|street[- ]?light|floodlight|single (?:hanging |bare |pendant )?(?:bulb|light))\b/i;
export const DARK_SHARE_WARN = 1 / 2;
// Words of a prompt that are not a place or an object (grammar, sizes, light, materials, the
// look's own palette and finish, the camera): a motif is counted on the rest.
const PROMPT_STOPWORDS = new Set(["with", "from", "into", "onto", "over", "under", "behind", "beside", "above", "below", "between", "through", "across", "along", "around", "down", "their", "there", "them", "they", "this", "that", "these", "those", "where", "while", "what", "when", "which", "small", "large", "tiny", "huge", "little", "dark", "light", "warm", "cold", "soft", "bright", "night", "view", "shot", "frame", "side", "left", "right", "centre", "center", "centred", "centered", "middle", "front", "back", "close", "wide", "seen", "single", "each", "some", "many", "only", "same", "other", "like", "still", "long", "tall", "short", "open", "flat", "plain", "simple", "clean", "whole", "half", "away", "near", "high", "deep", "wooden", "paper", "glass", "metal", "brass", "stone", "very", "more", "most", "just", "then", "than", "also", "both", "being", "person", "figure", "people", "anonymous", "hand", "hands", "angle", "level", "overhead", "profile", "edge", "corner", "lying", "standing", "sitting", "holding", "looking", "resting", "composition", "picture", "scene", "image", "illustration", "editorial", "painterly", "grain", "shape", "shapes", "line", "lines", "colour", "color", "ground", "background", "foreground", "teal", "cream", "amber", "green", "navy", "mustard", "ochre", "brick", "highlight", "highlights", "accent", "accents", "glow", "glowing", "lamplight", "spotlight", "medium", "extreme", "establishing", "aerial", "macro", "silhouette", "shoulder", "closeup"]);
// A plural folds to its singular (benches → bench, lamps → lamp, ferries → ferry, shelves →
// shelf, boxes → box, dishes → dish) so a prop written in both numbers counts once.
const motifOf = (word) => {
  if (word === "series" || word === "species") return word;
  if (word.length > 4 && word.endsWith("ies")) return `${word.slice(0, -3)}y`;
  if (word.length > 5 && word.endsWith("ves")) return `${word.slice(0, -3)}f`;
  // potatoes and heroes, but shoes and canoes keep their o and lose only the s below.
  if (word.length > 6 && word.endsWith("oes")) return word.slice(0, -2);
  if (word.length > 5 && /(?:ch|sh|ss)es$/.test(word)) return word.slice(0, -2);
  if (word.length > 4 && word.endsWith("xes")) return word.slice(0, -2);
  return word.length > 4 && word.endsWith("s") && !/(?:ss|us|is)$/.test(word) ? word.slice(0, -1) : word;
};
function promptMotifs(scene) {
  const words = String(scene.data?.prompt ?? "").toLowerCase().match(/[a-z]{4,}/g) ?? [];
  // A stopword is one in either form: "figures" is no more a prop than "figure" is.
  return new Set(words.filter((word) => !PROMPT_STOPWORDS.has(word) && !PROMPT_STOPWORDS.has(motifOf(word))).map(motifOf));
}
const fewIds = (ids) => `${ids.slice(0, 4).join(", ")}${ids.length > 4 ? ` and ${ids.length - 4} more` : ""}`;

/**
 * What makes a run of illustrated slides read as one monotonous slideshow, caught on the
 * prompts and camera words before a picture is paid for (docs/videos/ILLUSTRATED.md §畫面不像 AI).
 * Returns { errors, warnings } like shotProblems; empty for anything but illustrated slides.
 */
export function pictureVarietyProblems(doc) {
  const errors = [];
  const warnings = [];
  if (!illustrated(doc)) return { errors, warnings };
  const shots = [];
  doc.scenes.forEach((scene, index) => {
    if (isShot(scene)) shots.push({ scene, where: `scenes[${index}] (${scene.id})` });
  });
  let run = 0;
  let last = null;
  const unsized = [];
  const restated = [];
  const dark = [];
  const lookWords = new Set();
  for (const { scene, where } of shots) {
    const move = cameraMove(scene.data);
    run = move === last ? run + 1 : 1;
    last = move;
    if (run === SAME_MOVE_RUN_MAX + 1) errors.push({ path: `${where}.data.camera`, message: `${SAME_MOVE_RUN_MAX + 1} stills in a row under "${move}"; alternate the moves (push in, pull out, pan left, pan right, tilt up, tilt down, drift)` });
    const prompt = String(scene.data?.prompt ?? "");
    if (!SHOT_SIZE.test(prompt)) unsized.push(scene.id);
    const look = prompt.match(LOOK_WORDS);
    if (look) {
      restated.push(scene.id);
      lookWords.add(look[0].toLowerCase());
    }
    if (DARK_LIGHT.test(prompt)) dark.push(scene.id);
  }
  if (unsized.length) warnings.push({ path: "scenes", message: `${unsized.length} of ${shots.length} pictures name no shot size (close-up, medium, wide, overhead, low angle, from behind…): say how close the camera is in ${fewIds(unsized)}` });
  if (restated.length) warnings.push({ path: "scenes", message: `${restated.length} of ${shots.length} pictures restate the look (${[...lookWords].slice(0, 3).map((word) => `"${word}"`).join(", ")}); the look adds the style and the palette, the prompt describes the picture: ${fewIds(restated)}` });
  if (shots.length >= MOTIF_MIN_SHOTS && dark.length > shots.length * DARK_SHARE_WARN) warnings.push({ path: "scenes", message: `${dark.length} of ${shots.length} pictures are at night or under a lamp; vary the time of day, the weather and where the light comes from (morning, noon, rain, an overcast afternoon, a crowded daylight place): ${fewIds(dark)}` });
  if (shots.length >= MOTIF_MIN_SHOTS) {
    const counts = new Map();
    for (const { scene } of shots) for (const motif of promptMotifs(scene)) counts.set(motif, (counts.get(motif) ?? 0) + 1);
    const repeated = [...counts.entries()].filter(([, count]) => count > shots.length * MOTIF_SHARE_WARN).sort((a, b) => b[1] - a[1]).slice(0, 3);
    for (const [motif, count] of repeated) warnings.push({ path: "scenes", message: `"${motif}" is in ${count} of ${shots.length} pictures (a third is plenty): give each chapter its own place and props so the video travels` });
  }
  return { errors, warnings };
}

/**
 * Shot-level lint on the estimated timeline: overlong shots are errors (the clip models stop at
 * ten seconds, and a shot frozen for longer looks broken), long or very short runs are warnings.
 * Illustrated slides add the picture variety rules above. Returns { errors: [{ path, message }],
 * warnings: [...] }.
 */
export function shotProblems(doc, timeline) {
  const variety = pictureVarietyProblems(doc);
  const errors = [...variety.errors];
  const warnings = [...variety.warnings];
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
    // A shot cut from another shot's clip repeats that setup's camera and prompt on purpose.
    if (previous && isShot(previous) && !isSourced(scene) && promptSimilarity(previous, scene) >= PROMPT_SIMILARITY_WARN) {
      warnings.push({ path: where, message: `its prompt is nearly the same as ${previous.id}'s; two near-identical shots read as a stall` });
    }
    if (isSourced(scene) && scene.data.source.from_s + length > MAX_SOURCE_CLIP_SECONDS) {
      errors.push({ path: `${where}.data.source`, message: `cut from ${scene.data.source.shot}'s clip at ${scene.data.source.from_s} s and about ${length.toFixed(1)} s long, it ends past ${MAX_SOURCE_CLIP_SECONDS} s, where every clip model stops; start earlier or shorten its lines` });
    }
  });
  if (seconds.length >= 3) {
    const sorted = [...seconds].sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];
    if (hasCast(doc)) {
      if (median < MIN_MEDIAN_SHOT_SECONDS) warnings.push({ path: "scenes", message: `the median shot is ${median.toFixed(1)} s; the measured dramas sit at 1.5–2.25 s, but under ${MIN_MEDIAN_SHOT_SECONDS} s this pipeline pays a clip per cut: merge some shots (.agents/skills/youtube-video/references/drama-craft.md §五)` });
    } else if (median < MIN_MEDIAN_SHOT_SECONDS_NARRATED) {
      warnings.push({ path: "scenes", message: `the median shot is ${median.toFixed(1)} s; cuts this fast read as a montage, merge some shots` });
    }
    const long = seconds.filter((length) => length > WARN_SHOT_SECONDS).length / seconds.length;
    if (long > LONG_SHOT_SHARE_WARN) warnings.push({ path: "scenes", message: `${Math.round(long * 100)}% of the shots run over ${WARN_SHOT_SECONDS} s; the clip models cannot hold a shot that long` });
  }
  return { errors, warnings };
}

/**
 * Whether the script keeps to a binge series' visual tier (docs/videos/BINGE.md): the tier caps
 * how many of the shots may be clips, rounded up, so a 30-shot episode has at most 12 clips in
 * the hybrid tier and 3 in the stills tier. The clips tier caps nothing and only remarks on
 * stills, since the series is paying for clips anyway. Returns { errors, warnings } like
 * shotProblems, with an error for a tier this file does not know.
 */
export function visualTierProblems(doc, tier) {
  const errors = [];
  const warnings = [];
  if (!VISUAL_TIERS.includes(tier)) {
    errors.push({ path: "series.visual_tier", message: `"${tier}" is not a visual tier; the tiers are ${VISUAL_TIERS.join(", ")}` });
    return { errors, warnings };
  }
  const shots = shotScenes(doc).length;
  const clips = clipShotScenes(doc).length;
  if (tier === "clips") {
    if (shots - clips > 0) warnings.push({ path: "scenes", message: `the clips tier plays every shot as a clip; ${shots - clips} still shots here will be animated keyframes instead` });
    return { errors, warnings };
  }
  const allowed = Math.ceil(TIER_CLIP_SHARE_MAX[tier] * shots);
  if (clips > allowed) {
    errors.push({ path: "scenes", message: `${clips} of ${shots} shots are clips; the "${tier}" tier allows at most ${allowed}: mark the rest visual "still"` });
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
