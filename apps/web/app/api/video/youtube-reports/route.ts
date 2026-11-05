import { NextRequest } from "next/server";
import { forwardToSpeech } from "../speech/forward";

// A paired video tool (tools/video/youtube-reports, skill youtube-channel-reports) asks which of
// the channel's YouTube Reporting API reports the site keeps, for which days, and which of the
// site's videos are on YouTube. Only a video tool token is forwarded, never cookies.
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "youtube-reports", "GET");
}
