import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";

// The Shorts tool and the worker read the voice, the length and the languages a Short is made
// with (docs/videos/SHORTS.md). The owner's consent to publish is not part of the answer.
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/shorts/settings", "GET");
}
