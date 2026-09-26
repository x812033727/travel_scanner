import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";

// The oldest drama request the owner filed and nobody has started, or none: what the video
// worker makes before any scheduled draft (docs/videos/DRAMA.md).
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/drama-requests/next", "GET");
}
