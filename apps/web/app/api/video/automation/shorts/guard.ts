import { problem } from "../../speech/forward";

// The Shorts routes of the video worker (docs/videos/SHORTS.md) take a Short's slug in the path;
// it is checked here so a stray path never reaches the API. The rule is the Shorts tool's own
// (tools/video/shorts/core.mjs), which is narrower than the API's.
const SLUG = /^[a-z][a-z0-9-]{2,79}$/;
// A weekly plan, a batch of new topics and a weekly report carry far more than a narration
// request; the rest of the Shorts routes carry next to nothing.
export const PLAN_MAX_BODY_BYTES = 1024 * 1024;
export const SMALL_MAX_BODY_BYTES = 64 * 1024;

/** The path under automation/ for a Short, or a 404 when the slug is not one. */
export function shortPath(slug: string): string | ReturnType<typeof problem> {
  if (!SLUG.test(slug)) return problem(404, "video_shorts_not_found", "no such Short");
  return `automation/shorts/${slug}`;
}

export const isRefusal = (value: string | ReturnType<typeof problem>): value is ReturnType<typeof problem> => typeof value !== "string";
