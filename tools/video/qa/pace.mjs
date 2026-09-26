// The pace check: no slide state stays on screen longer than MAX_STATE_SECONDS.
//
// A scene's picture enters its first state when the scene's first line starts; every later line
// that carries a reveal starts the next state. A state lasts until the next state, or the next
// scene, begins; the last state of the last scene lasts until the video ends. Line times come
// from timeline.json (the narration as synthesized), scenes and reveals from video.json, so the
// check reads the video as it was cut rather than the estimate lint makes. This is the local
// script the 2026-09-26 re-pacing of batch 2 was checked with, made a pure function.
import { FPS } from "../core/timeline.mjs";

export const MAX_STATE_SECONDS = 15;

/**
 * Every slide state in order: [{ scene, index, start_frame, end_frame, seconds }]. `index` is
 * the state's position in its scene, 0 being the picture the scene opens with. Throws when a
 * line of the script has no entry in the timeline (a timeline built for another script).
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

/** The states held longer than `limit` seconds: [{ scene, index, seconds }]. */
export function paceProblems(states, limit = MAX_STATE_SECONDS) {
  return states.filter((state) => state.seconds > limit).map(({ scene, index, seconds }) => ({ scene, index, seconds }));
}

/** The pace item's detail line for a list of problems, or for none. */
export function paceDetail(states, problems, limit = MAX_STATE_SECONDS) {
  if (!problems.length) {
    const longest = states.reduce((max, state) => Math.max(max, state.seconds), 0);
    return `${states.length} slide states, the longest ${longest} s; none over ${limit} s`;
  }
  return `${problems.length} of ${states.length} slide states stay over ${limit} s: ${problems.map((problem) => `${problem.scene} state ${problem.index} (${problem.seconds} s)`).join(", ")}`;
}
