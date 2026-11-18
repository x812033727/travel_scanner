import { NextRequest } from "next/server";
import { forwardToSpeech } from "../speech/forward";

// A paired video tool (tools/video/youtube-reports, skill youtube-channel-reports) asks which of
// the channel's YouTube Reporting API reports the site keeps, for which days, and which of the
// site's videos are on YouTube. Only a video tool token is forwarded, never cookies.
// A linked channel other than the main one (docs/videos/YOUTUBE-REPORTS.md §頻道), passed on only
// when it looks like a channel code.
const CHANNEL = /^[a-z][a-z0-9-]{1,31}$/;
const channelQuery = (request: NextRequest) => {
  const channel = request.nextUrl.searchParams.get("channel") ?? "";
  return CHANNEL.test(channel) && channel !== "default" ? `?channel=${channel}` : "";
};

export async function GET(request: NextRequest) {
  return forwardToSpeech(request, `youtube-reports${channelQuery(request)}`, "GET");
}
