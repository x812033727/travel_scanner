import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../speech/forward";

// Every video on /admin/videos, dropped ones too, with the article each retells: the video
// worker checks a new draft's topic against them (docs/videos/AUTOMATION.md).
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/videos", "GET");
}
