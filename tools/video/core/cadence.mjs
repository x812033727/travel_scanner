// The picture cadence of an illustrated slides video (docs/videos/ILLUSTRATED.md): how long each
// picture stays, how often one changes, and how much of the runtime is illustration rather than
// cards. Pure functions over a timeline (estimated by lint, synthesized for QA), so lint and the
// final gate read the same rules. Nothing here imports from qa/, assemble/ or media/.
import { illustrated, isShot } from "./drama.mjs";
import { FPS } from "./timeline.mjs";

// A picture (a slide state or an illustration) stays on screen this long at most.
export const MAX_PICTURE_SECONDS = 8;
// The average a lively video lands around: a new picture about every six seconds.
export const TARGET_AVERAGE_SECONDS = 6;
// At least this share of the runtime is illustration; the rest is cards with the numbers.
export const MIN_ILLUSTRATION_SHARE = 0.5;
// The hook of an illustrated video lands within the first twenty seconds.
export const HOOK_SECONDS = 20;

/**
 * Every slide state in order: [{ scene, index, start_frame, end_frame, seconds }]. `index` is
 * the state's position in its scene, 0 being the picture the scene opens with. A scene's picture
 * enters its first state when the scene's first line starts; every later line that carries a
 * reveal starts the next state (a shot has no reveals, so it is one state). A state lasts until
 * the next state, or the next scene, begins; the last state of the last scene lasts until the
 * video ends. Throws when a line of the script has no entry in the timeline (a timeline built
 * for another script).
 */
export function slideStates(doc, timeline) {
  const fps = timeline.fps || FPS;
  const startOf = new Map((timeline.lines ?? []).map((line) => [line.id, line.start_frame]));
  const states = [];
  for (const scene of doc.scenes ?? []) {
    let index = 0;
    (scene.lines ?? []).forEach((line, lineIndex) => {
      const start = startOf.get(line.id);
      if (start === undefined) throw new Error(`timeline.json has no line ${line.id}; run tts again`);
      // A reveal on the scene's first line changes its opening state rather than adding one.
      if (lineIndex === 0 || line.reveal) states.push({ scene: scene.id, index: index++, start_frame: start });
    });
  }
  states.forEach((state, position) => {
    state.end_frame = states[position + 1]?.start_frame ?? timeline.total_frames;
    state.seconds = Math.round(((state.end_frame - state.start_frame) / fps) * 10) / 10;
  });
  return states;
}

/** How many states there are, the longest hold and the average hold, in seconds. */
export function cadenceSummary(states) {
  const count = states.length;
  const longest = states.reduce((max, state) => Math.max(max, state.seconds), 0);
  const total = states.reduce((sum, state) => sum + state.seconds, 0);
  return { count, longest, average: count ? Math.round((total / count) * 10) / 10 : 0 };
}

/** The share of the runtime spent on shot scenes, 0 to 1. */
export function illustrationShare(doc, timeline) {
  const total = timeline.total_frames || 0;
  if (!total) return 0;
  const shots = new Set((doc.scenes ?? []).filter(isShot).map((scene) => scene.id));
  const frames = (timeline.scenes ?? []).filter((scene) => shots.has(scene.id)).reduce((sum, scene) => sum + (scene.end_frame - scene.start_frame), 0);
  return frames / total;
}

/**
 * Where an illustrated slides video breaks the cadence: [{ kind, path, message }], kind being
 * "over" (a picture held past `max` seconds), "average" (pictures change slower than `average`
 * on the whole) or "share" (less than `share` of the runtime is illustration). Empty for a video
 * that is not illustrated: plain slides keep the pace rule of qa/pace.mjs. Lint reports these as
 * warnings on the estimated timeline; the final gate fails on "over" and "share" (docs/videos/
 * ILLUSTRATED.md).
 */
export function cadenceProblems(doc, timeline, limits = {}) {
  if (!illustrated(doc)) return [];
  const max = limits.max ?? MAX_PICTURE_SECONDS;
  const average = limits.average ?? TARGET_AVERAGE_SECONDS;
  const share = limits.share ?? MIN_ILLUSTRATION_SHARE;
  const states = slideStates(doc, timeline);
  const problems = [];
  for (const state of states) {
    if (state.seconds > max) {
      problems.push({ kind: "over", path: `scenes (${state.scene} state ${state.index})`, message: `stays on screen about ${state.seconds} s; a picture changes at least every ${max} s: split the shot, reveal one item per sentence, or put an illustration here` });
    }
  }
  const summary = cadenceSummary(states);
  if (summary.average > average) problems.push({ kind: "average", path: "scenes", message: `a new picture every ${summary.average} s on average; aim for ${average} s or less` });
  const covered = illustrationShare(doc, timeline);
  if (covered < share) problems.push({ kind: "share", path: "scenes", message: `illustrations cover ${Math.round(covered * 100)}% of the runtime; at least ${Math.round(share * 100)}% of an illustrated video is pictures, the cards carry the numbers` });
  return problems;
}
