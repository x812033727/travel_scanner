// Runtime requirements for the knowledge and nonfiction long-video catalogues. Planning
// estimates are deliberately not accepted here: QA reads the current TTS timeline and the
// frame count assemble checked on the finished cut. Channel bookends never count as content.
import { FPS } from "./timeline.mjs";
import { EXPLAINER_PRESET } from "./drama.mjs";

export const KNOWLEDGE_MIN_SECONDS = 480;
export const KNOWLEDGE_TARGET_SECONDS = 600;
const LONG_FORMATS = new Set(["slides", "screencast", "drama"]);
const KNOWLEDGE_CATEGORIES = new Set(["ai-terms", "explainer", "story"]);
const CATALOGUE_SLUG = /^(?:sothatswhy-|ai-term-|story-)/;

/**
 * The request length used by every explainer writing path, including old auto.json files.
 * Missing or short legacy targets take the reviewed ten-minute default; an explicit 8–20
 * minute target stays the owner's choice. Other drama presets and brand stories keep theirs.
 */
export function effectiveEpisodeMinutes(minutes, preset) {
  if (preset !== EXPLAINER_PRESET) return minutes;
  if (minutes === undefined || minutes === null) return KNOWLEDGE_TARGET_SECONDS / 60;
  if (!Number.isSafeInteger(minutes) || minutes > 20) {
    throw new RangeError("an explainer target must be an integer no longer than 20 minutes");
  }
  return minutes < KNOWLEDGE_MIN_SECONDS / 60 ? KNOWLEDGE_TARGET_SECONDS / 60 : minutes;
}

/** Ordinary drama episodes, binge compilations and Shorts retain their own duration rules. */
export function isKnowledgeLongform(doc) {
  return Boolean(doc && LONG_FORMATS.has(doc.format) && !doc.compilation && (
    KNOWLEDGE_CATEGORIES.has(doc.category)
    || doc.look?.preset === "flat-explainer"
    || CATALOGUE_SLUG.test(doc.slug ?? "")
  ));
}

const positiveFrames = (value) => Number.isSafeInteger(value) && value > 0;
const bookendFrames = (value) => Number.isSafeInteger(value) && value >= 0;

/**
 * Apply the current floor even to a legacy checks.json that previously passed QA. `timeline`
 * is the unwrapped body; `presented` is the player's timeline after the selected bookends.
 * Both are bound to the same narration and checks, on the pipeline's exact 30 fps grid.
 */
export function knowledgeDurationProblems({ doc, timeline, presented = timeline, timelineCurrent, checks }) {
  if (!isKnowledgeLongform(doc)) return [];
  if (!timelineCurrent || !timeline) return ["knowledge long videos need the current actual narration timeline; run tts again"];
  if (timeline.fps !== FPS || !positiveFrames(timeline.total_frames) || timeline.branding_hash || timeline.body_total_frames !== undefined) {
    return ["knowledge long videos need an unwrapped narration timeline with a positive integer frame count at 30 fps"];
  }
  if (typeof timeline.speech_hash !== "string" || !timeline.speech_hash || checks?.speech_hash !== timeline.speech_hash) {
    return ["knowledge long-video checks and narration timeline must have the same speech hash; run assemble again"];
  }
  if (!presented || presented.fps !== FPS || !positiveFrames(presented.total_frames) || presented.speech_hash !== timeline.speech_hash) {
    return ["knowledge long videos need a presentation timeline bound to the current narration at 30 fps"];
  }

  const problems = [];
  const branding = checks?.branding;
  if (branding) {
    if (!bookendFrames(branding.intro_frames) || !bookendFrames(branding.outro_frames)
      || branding.body_frames !== timeline.total_frames
      || presented.body_total_frames !== timeline.total_frames
      || presented.branding_hash !== branding.hash
      || presented.total_frames !== timeline.total_frames + branding.intro_frames + branding.outro_frames) {
      problems.push("knowledge long-video presentation frames do not match the current body and selected bookends; run assemble again");
    }
  } else if (presented.total_frames !== timeline.total_frames || presented.branding_hash) {
    problems.push("knowledge long-video presentation frames differ from the unbranded narration; run assemble again");
  }
  const frames = checks?.metrics?.frames;
  if (!positiveFrames(frames) || frames !== presented.total_frames
    || (checks.metrics.fps !== undefined && checks.metrics.fps !== FPS)) {
    problems.push("knowledge long-video checked final frame count must match the current presentation timeline at 30 fps; run assemble again");
  }
  const minimumFrames = KNOWLEDGE_MIN_SECONDS * FPS;
  if (timeline.total_frames < minimumFrames) {
    problems.push(`knowledge long-video body is ${timeline.total_frames} frames (${timeline.total_frames / FPS} s); needs at least ${minimumFrames} frames (${KNOWLEDGE_MIN_SECONDS} s), excluding intro and outro`);
  }
  if (positiveFrames(frames) && frames < minimumFrames) {
    problems.push(`knowledge long-video final cut is ${frames} frames (${frames / FPS} s); needs at least ${minimumFrames} frames (${KNOWLEDGE_MIN_SECONDS} s)`);
  }
  return problems;
}
