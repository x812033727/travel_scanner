// Runtime requirements for the knowledge and nonfiction long-video catalogues. Planning
// estimates are deliberately not accepted here: QA reads the current TTS timeline and the
// frame count assemble checked on the finished cut. Channel bookends never count as content.
import { FPS } from "./timeline.mjs";
import { EXPLAINER_PRESET, isKnowledgeLongform, shotVisual } from "./drama.mjs";
import { ANIME_BODY_TOLERANCE_SECONDS, animeRuntimeContext, hasAnimePolicy, LONG_ANIME_POLICY, runtimePolicyHash, validateAnimePolicy } from "./anime-policy.mjs";

export const KNOWLEDGE_MIN_SECONDS = 480;
export const KNOWLEDGE_TARGET_SECONDS = 600;
// Which documents these floors hold is decided in drama.mjs (isKnowledgeLongform), where the
// schema and the timeline can read it too without a cycle; it is re-exported here for its readers.
export { isKnowledgeLongform };

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

/** Long-anime body timing is measured from WAV samples and directed action intervals, never a draft estimate. */
export function animeBodyDurationProblems({ doc, timeline, timelineCurrent, series = null }) {
  if (!hasAnimePolicy(doc)) return [];
  const policyProblems = validateAnimePolicy(doc, { series });
  if (policyProblems.length) return policyProblems;
  if (!timelineCurrent || !timeline) return ["long-anime needs the current actual body timeline; run tts again"];
  if (timeline.timing_basis !== "measured") return ["long-anime needs measured audio and action timing; a script estimate cannot prove the body duration"];
  if (timeline.fps !== FPS || !positiveFrames(timeline.total_frames) || timeline.branding_hash || timeline.body_total_frames !== undefined) return ["long-anime needs an unwrapped actual body timeline on the 30 fps grid"];
  if (!/^[a-f0-9]{16}$/.test(timeline.speech_hash ?? "")) return ["long-anime body timeline needs its current speech hash"];
  if (timeline.runtime_policy_hash !== runtimePolicyHash(doc, { series })) return ["long-anime body timeline has another runtime policy; run tts again (unchanged voice clips are reused)"];
  const target = doc.runtime_spec.body_target_seconds;
  const low = (target - ANIME_BODY_TOLERANCE_SECONDS) * FPS;
  const high = (target + ANIME_BODY_TOLERANCE_SECONDS) * FPS;
  return timeline.total_frames < low || timeline.total_frames > high
    ? [`long-anime body is ${timeline.total_frames} frames; needs ${low} to ${high} frames (${target - ANIME_BODY_TOLERANCE_SECONDS} to ${target + ANIME_BODY_TOLERANCE_SECONDS} seconds), excluding OP/ED and slot reserve`]
    : [];
}

/** Native body time comes from directed footage at its natural speed, with no frozen tail. */
export function animeShotFitProblems({ doc, timeline, shots }) {
  if (!hasAnimePolicy(doc)) return [];
  const sources = (doc.scenes ?? []).filter((scene) => scene.template === "shot");
  if (!sources.length) return [];
  if (!Array.isArray(shots)) return ["long-anime needs current measured fit evidence for every directed shot; run assemble again"];
  const problems = [];
  const records = new Map();
  const known = new Set(sources.map((scene) => scene.id));
  for (const record of shots) {
    if (!record || !known.has(record.shot) || records.has(record.shot)) problems.push("long-anime shot fit evidence has unknown or duplicate shots; run assemble again");
    else records.set(record.shot, record);
  }
  for (const source of sources) {
    const span = timeline?.scenes?.find((scene) => scene.id === source.id);
    const needed = span ? span.end_frame - span.start_frame : null;
    const record = records.get(source.id);
    if (!positiveFrames(needed) || !record) {
      problems.push(`long-anime shot ${source.id} needs its current measured scene and fit evidence; run assemble again`);
      continue;
    }
    if (shotVisual(source) === "still") {
      if (record.kind !== "motion" || typeof record.move !== "string" || !record.move.trim() || record.fit != null) problems.push(`long-anime shot ${source.id} needs its directed camera motion evidence`);
      continue;
    }
    const fit = record.fit;
    if (record.kind !== "clip" || !fit || fit.speed !== 1 || fit.pad !== 0
      || fit.mode !== (source.data?.fit ?? "auto") || !["auto", "trim"].includes(fit.mode)
      || !positiveFrames(fit.available) || fit.available < needed || fit.source_frames !== needed || fit.stretched !== needed
      || !bookendFrames(fit.trim) || fit.trim !== fit.available - needed) {
      problems.push(`long-anime shot ${source.id} must cover its ${needed} frames at natural speed with no frozen tail; regenerate the clip or revise the directed scene`);
    }
  }
  return problems;
}

/** Every delivery path compares the actual cut with the same body, policy and final-file evidence. */
export function animeDurationProblems({ doc, timeline, presented = timeline, timelineCurrent, checks, finalSha256, series = null }) {
  if (!hasAnimePolicy(doc)) return [];
  const problems = animeBodyDurationProblems({ doc, timeline, timelineCurrent, series });
  if (problems.length) return problems;
  const hash = runtimePolicyHash(doc, { series });
  problems.push(...animeShotFitProblems({ doc, timeline, shots: checks?.metrics?.shots }));
  if (checks?.runtime_policy_hash !== hash) problems.push("long-anime checks have another runtime policy; run assemble again");
  if (checks?.speech_hash !== timeline.speech_hash) problems.push("long-anime checks and body must have the same speech hash; run assemble again");
  if (!presented || presented.fps !== FPS || !positiveFrames(presented.total_frames) || presented.speech_hash !== timeline.speech_hash) return [...problems, "long-anime presentation must be bound to the current actual body at 30 fps"];
  const branding = checks?.branding;
  const opEdFrames = branding ? branding.intro_frames + branding.outro_frames : 0;
  if (branding) {
    if (!bookendFrames(branding.intro_frames) || !bookendFrames(branding.outro_frames)
      || branding.body_frames !== timeline.total_frames || presented.body_total_frames !== timeline.total_frames
      || presented.branding_hash !== branding.hash || presented.total_frames !== timeline.total_frames + opEdFrames) problems.push("long-anime presentation frames do not match its body and actual OP/ED; run assemble again");
  } else if (presented.total_frames !== timeline.total_frames || presented.branding_hash) problems.push("long-anime unbranded presentation must match the actual body exactly");
  if (opEdFrames > doc.runtime_spec.op_ed_budget_seconds * FPS) problems.push("long-anime actual OP/ED exceeds its separate budget");
  if (presented.total_frames > (doc.runtime_spec.broadcast_slot_seconds - doc.runtime_spec.slot_reserve_seconds) * FPS) problems.push("long-anime presentation consumes the reserved broadcast-slot time; reserve must never be rendered");
  if (!positiveFrames(checks?.metrics?.frames) || checks.metrics.frames !== presented.total_frames || checks.metrics.fps !== FPS) problems.push("long-anime checked final frames must match the current presentation at 30 fps");
  if (!/^[a-f0-9]{64}$/.test(finalSha256 ?? "") || checks?.final_sha256 !== finalSha256) problems.push("long-anime checks must be bound to the current final.mp4 SHA-256; run assemble again");
  return problems;
}

/** This record is emitted only after every measured/current-file check passed. */
export function animeRuntimeProof(input) {
  if (!hasAnimePolicy(input.doc)) return null;
  const problems = animeDurationProblems(input);
  if (problems.length) throw new RangeError(problems.join("; "));
  const { doc, timeline, finalSha256, series = null } = input;
  const presented = input.presented ?? timeline;
  const opEdFrames = presented.total_frames - timeline.total_frames;
  return {
    basis: "measured", production_policy: LONG_ANIME_POLICY, policy_hash: runtimePolicyHash(doc, { series }), runtime_spec: { ...doc.runtime_spec },
    runtime_context: animeRuntimeContext(doc, { series }),
    fps: FPS, body_frames: timeline.total_frames, presentation_frames: presented.total_frames, op_ed_frames: opEdFrames,
    body_seconds: timeline.total_frames / FPS, op_ed_seconds: opEdFrames / FPS, presentation_seconds: presented.total_frames / FPS,
    speech_hash: timeline.speech_hash, final_sha256: finalSha256,
  };
}
