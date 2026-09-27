import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";

// The next document to plan or episode to start across every series, or none while they all
// wait for the owner (docs/videos/SERIES.md). The worker asks before any one-off request.
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/series/next", "GET");
}
