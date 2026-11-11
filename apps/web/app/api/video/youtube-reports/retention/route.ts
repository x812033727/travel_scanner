import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../speech/forward";

// One video's audience retention curve: the API asks the YouTube Analytics API with the stored
// channel grant (docs/videos/YOUTUBE-REPORTS.md §觀眾續看曲線). Only the known query values are
// passed on, each checked here, so nothing else reaches the API's query string.
const VIDEO = /^[A-Za-z0-9_-]{6,20}$/;
const DAY = /^\d{4}-\d{2}-\d{2}$/;
const TIMEOUT_MS = 60_000;

export async function GET(request: NextRequest) {
  const query = request.nextUrl.searchParams;
  const video = query.get("video_id") ?? "";
  const start = query.get("start");
  const end = query.get("end");
  const organic = query.get("organic");
  if (!VIDEO.test(video) || (start !== null && !DAY.test(start)) || (end !== null && !DAY.test(end))
    || (organic !== null && !["true", "false", "1", "0"].includes(organic))) {
    return problem(422, "video_youtube_retention_query", "video_id is a YouTube video id; start and end are YYYY-MM-DD; organic is true or false");
  }
  const passed = new URLSearchParams({ video_id: video });
  if (start) passed.set("start", start);
  if (end) passed.set("end", end);
  if (organic) passed.set("organic", organic);
  return forwardToSpeech(request, `youtube-reports/retention?${passed.toString()}`, "GET", undefined, TIMEOUT_MS);
}
