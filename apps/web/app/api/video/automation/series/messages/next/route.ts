import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../../speech/forward";

// The oldest of the owner's lines on a document or a screenplay still waiting for the model,
// with the thread and the series' context, or none (docs/videos/DRAMA-FLOW.md, section 3). The
// worker asks before it plans any series document.
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/series/messages/next", "GET");
}
