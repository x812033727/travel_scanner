import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../speech/forward";

// Candidate topics for the video worker's next draft: the site's recent articles, then a web
// search within the daily Brave budget (docs/videos/AUTOMATION.md).
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/topics", "GET");
}
