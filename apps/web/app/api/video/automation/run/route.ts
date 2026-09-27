import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../speech/forward";

// One writing stage of a video, run by the server with the model the owner chose
// (docs/videos/AUTOMATION.md). A fact-check sends the source pages it read, so the body is far
// larger than a narration request; it stays under the API's 5 MiB cap and nginx's 6 MB.
const RUN_MAX_BODY_BYTES = 4 * 1024 * 1024;
// A stage writes a whole script without streaming; nginx allows 300 s for /api/.
const RUN_TIMEOUT_MS = 295_000;

export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "automation/run", "POST", RUN_MAX_BODY_BYTES, RUN_TIMEOUT_MS);
}
