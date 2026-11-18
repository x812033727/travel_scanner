import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../speech/forward";

// One report family's rows for a span of Pacific days, as YouTube wrote them. Only the known
// query values are passed on, each checked here, so nothing else reaches the API's query string.
const REPORT = /^[a-z0-9_]{3,100}$/;
const DAY = /^\d{4}-\d{2}-\d{2}$/;
const VIDEO = /^[A-Za-z0-9_-]{6,20}$/;
const MAX_VIDEOS = 50;
const CHANNEL = /^[a-z][a-z0-9-]{1,31}$/;
const TIMEOUT_MS = 120_000;

export async function GET(request: NextRequest) {
  const query = request.nextUrl.searchParams;
  const report = query.get("report") ?? "";
  const start = query.get("start") ?? "";
  const end = query.get("end") ?? "";
  const format = query.get("format") ?? "json";
  const videos = query.getAll("video_id");
  if (!REPORT.test(report) || !DAY.test(start) || !DAY.test(end) || !["json", "csv"].includes(format)) {
    return problem(422, "video_youtube_report_query", "report, start and end (YYYY-MM-DD) are required; format is json or csv");
  }
  if (videos.length > MAX_VIDEOS || videos.some((video) => !VIDEO.test(video))) {
    return problem(422, "video_youtube_report_videos", `at most ${MAX_VIDEOS} video_id values, each a YouTube video id`);
  }
  const passed = new URLSearchParams({ report, start, end, format });
  for (const video of videos) passed.append("video_id", video);
  // A linked channel other than the main one (docs/videos/YOUTUBE-REPORTS.md §頻道).
  const channel = query.get("channel") ?? "";
  if (channel && channel !== "default") {
    if (!CHANNEL.test(channel)) return problem(422, "video_youtube_channel_unknown", "channel is a channel code: 2 to 32 lowercase letters, digits or hyphens");
    passed.set("channel", channel);
  }
  return forwardToSpeech(request, `youtube-reports/rows?${passed.toString()}`, "GET", undefined, TIMEOUT_MS);
}
