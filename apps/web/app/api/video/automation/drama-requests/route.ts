import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../speech/forward";

// The owner's drama requests still queued or in the making, oldest first, so a restarted video
// worker can tell which of its videos answers which request (docs/videos/DRAMA.md). Only the
// worker's video tool token is forwarded, never a browser session.
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/drama-requests", "GET");
}
