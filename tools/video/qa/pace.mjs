// The pace check: no slide state stays on screen longer than MAX_STATE_SECONDS.
//
// A scene's picture enters its first state when the scene's first line starts; every later line
// that carries a reveal starts the next state. A state lasts until the next state, or the next
// scene, begins; the last state of the last scene lasts until the video ends. Line times come
// from timeline.json (the narration as synthesized), scenes and reveals from video.json, so the
// check reads the video as it was cut rather than the estimate lint makes. This is the local
// script the 2026-09-26 re-pacing of batch 2 was checked with, made a pure function.
// The state list itself lives in core/cadence.mjs, where lint reads it on the estimated timeline
// for illustrated videos; this module keeps the plain slides rule and the QA wording.
export { slideStates } from "../core/cadence.mjs";

export const MAX_STATE_SECONDS = 15;

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
