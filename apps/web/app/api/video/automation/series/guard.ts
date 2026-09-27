import { problem } from "../../speech/forward";

// The video worker's series routes (docs/videos/SERIES.md) take a series slug and an episode
// number in the path; both are checked here so a stray path never reaches the API. The API's
// own patterns are the same (apps/api/app/video_automation/schemas.py).
const SLUG = /^[a-z0-9][a-z0-9-]{1,39}$/;
const NUMBER = /^[1-9][0-9]{0,3}$/;

/** The path under automation/ for a series, or a 404 when the slug or the number is not one. */
export function seriesPath(slug: string, number?: string): string | ReturnType<typeof problem> {
  if (!SLUG.test(slug)) return problem(404, "video_series_not_found", "no such series");
  if (number === undefined) return `automation/series/${slug}`;
  if (!NUMBER.test(number)) return problem(404, "video_series_episode_not_found", "no such episode");
  return `automation/series/${slug}/episodes/${number}`;
}

export const isRefusal = (value: string | ReturnType<typeof problem>): value is ReturnType<typeof problem> => typeof value !== "string";
