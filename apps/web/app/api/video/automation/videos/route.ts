import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../speech/forward";

// Every video on /admin/videos, dropped ones too, with the article each retells: the video
// worker checks a new draft's topic against them (docs/videos/AUTOMATION.md). The rounds that
// make tutorials and dramas ask with shorts=exclude, so ninety days of Shorts do not push their
// videos past the list's cap, and the Shorts round asks with shorts=only (docs/videos/SHORTS.md).
// Only the filters the API knows are forwarded, each checked here; anything else in the query is
// left behind.
const FILTERS: Record<string, RegExp> = {
  format: /^(?:slides|drama|shorts)$/,
  shorts: /^(?:only|exclude)$/,
  state: /^(?:making|needs_you|library|slotted|scheduled|published|missed|dropped)$/,
  limit: /^(?:[1-9][0-9]?|1[0-9]{2}|200)$/,
  before: /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$/,
};

export async function GET(request: NextRequest) {
  const query = new URLSearchParams();
  for (const [name, pattern] of Object.entries(FILTERS)) {
    const value = request.nextUrl.searchParams.get(name);
    if (value === null) continue;
    // A filter dropped quietly would answer with every video instead of the few asked for.
    if (!pattern.test(value)) return problem(422, "video_list_filter_invalid", `${name} is not a value the list takes`);
    query.set(name, value);
  }
  const filters = query.toString();
  return forwardToSpeech(request, `automation/videos${filters ? `?${filters}` : ""}`, "GET");
}
