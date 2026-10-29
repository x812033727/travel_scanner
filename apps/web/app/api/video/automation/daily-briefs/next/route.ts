import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";

// The oldest day of AI and tech news the worker should make into a daily brief, or none; the API
// files yesterday's (Asia/Taipei) first once the settings' hour has come
// (.agents/skills/youtube-video/references/daily-brief.md).
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/daily-briefs/next", "GET");
}
