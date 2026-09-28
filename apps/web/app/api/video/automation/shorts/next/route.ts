import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";

// The worker's next Shorts job, or none: a weekly plan, a topic to brief, a Short to make with
// its topic and context, or the weekly report (docs/videos/SHORTS.md).
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/shorts/next", "GET");
}
