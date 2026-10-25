// The explicit, checked loop of a generated music track shorter than its cut (`music --loop`,
// docs/videos/ILLUSTRATED.md §配樂與音效): read by the mix inputs (assemble/sound.mjs) and by
// status (core/state.mjs), so it lives apart from both.

/** A looped bed shorter than this is a jingle, not a bed: a loop is not recorded for it. */
export const MIN_LOOP_SECONDS = 30;
// The cut may come out a few frames longer when it is assembled again with the same script.
const LOOP_SLACK_SECONDS = 0.5;

/**
 * Whether a generated track's recorded loop (music --loop) covers `neededSeconds`: the decision
 * names this very file, its fully decoded length, at least MIN_LOOP_SECONDS long, and a cut no
 * shorter than this one. Every mix plays the bed with `-stream_loop -1` cut to the video's
 * length (assemble/drama.mjs soundGraph), so the loop is the one the approved cut was mixed
 * with; the record makes it a decision instead of a silent pass, and a new cut length or a new
 * file needs a new one.
 */
export function loopCovers(generated, neededSeconds) {
  const loop = generated?.loop;
  return Boolean(loop) && loop.method === "stream_loop" && typeof generated.sha256 === "string" && loop.sha256 === generated.sha256 &&
    Number.isFinite(generated.actual_seconds) && generated.actual_seconds >= MIN_LOOP_SECONDS && loop.track_seconds === generated.actual_seconds &&
    Number.isFinite(loop.cut_seconds) && Number.isFinite(neededSeconds) && neededSeconds > 0 && neededSeconds <= loop.cut_seconds + LOOP_SLACK_SECONDS;
}
