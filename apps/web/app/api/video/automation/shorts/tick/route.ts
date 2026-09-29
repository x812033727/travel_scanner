import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";
import { SMALL_MAX_BODY_BYTES } from "../guard";

// The worker knocks at the start of every round (docs/videos/SHORTS.md): the API locks the slots
// whose time has come, sends what is due to YouTube and reads the numbers that are due. The
// review store and the channel's grant are only there, so the clock is the worker's and the work
// is the API's. The answer is counts, never a token or a video.
export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "automation/shorts/tick", "POST", SMALL_MAX_BODY_BYTES);
}
