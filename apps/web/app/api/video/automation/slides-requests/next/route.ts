import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";

// The oldest site article the owner asked to have made into a slides video and nobody has started,
// or none: what the video worker plans before any scheduled draft (docs/videos/AUTOMATION.md). A
// request whose article is no longer published is skipped by the API.
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/slides-requests/next", "GET");
}
