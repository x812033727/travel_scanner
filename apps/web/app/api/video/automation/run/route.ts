import { NextRequest } from "next/server";
import { forwardToSpeech, type LostAnswer } from "../../speech/forward";

// One writing stage of a video, run by the server with the model the owner chose
// (docs/videos/AUTOMATION.md). A fact-check sends the source pages it read, so the body is far
// larger than a narration request; it stays under the API's 5 MiB cap and nginx's 6 MB.
const RUN_MAX_BODY_BYTES = 4 * 1024 * 1024;
// A stage writes a whole script without streaming; nginx allows 300 s for /api/, and Node's fetch
// waits at most 300 s for the API's headers, so a longer deadline here would not help.
const RUN_TIMEOUT_MS = 295_000;
// The API may still be running the stage when that deadline passes: a subscription run may take
// 15 minutes, and on 2026-09-29 a translation finished after 302 s, recorded as ok and paid for,
// with nobody left to read its answer. The worker must not ask the model again on its own then
// (tools/video/automation/client.mjs RUN_UNCERTAIN), so the route says the answer is lost instead
// of "unreachable", which it keeps for an API it never reached.
const RUN_LOST: LostAnswer = {
  status: 504,
  code: "video_ai_run_uncertain",
  detail: "no answer within the deadline; the stage may still be running on the server or have finished there",
};

export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "automation/run", "POST", RUN_MAX_BODY_BYTES, RUN_TIMEOUT_MS, RUN_LOST);
}
