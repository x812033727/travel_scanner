import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../speech/forward";

// Fetch the reports YouTube made since the last run. It only reads YouTube and writes the site's
// copy, so a lost answer is safe to send again; the API refuses a run already in progress.
const TIMEOUT_MS = 240_000;

// A linked channel other than the main one (docs/videos/YOUTUBE-REPORTS.md §頻道), passed on only
// when it looks like a channel code.
const CHANNEL = /^[a-z][a-z0-9-]{1,31}$/;
const channelQuery = (request: NextRequest) => {
  const channel = request.nextUrl.searchParams.get("channel") ?? "";
  return CHANNEL.test(channel) && channel !== "default" ? `?channel=${channel}` : "";
};

export async function POST(request: NextRequest) {
  return forwardToSpeech(request, `youtube-reports/sync${channelQuery(request)}`, "POST", 4 * 1024, TIMEOUT_MS);
}
