import { NextRequest } from "next/server";
import { JUDGE_LOST, forwardToSpeech } from "../../../speech/forward";

// Jev chooses among a brief's outlines against the channel's stance (docs/videos/HANDS-OFF.md
// §Jev 挑大綱). Only the worker's video tool token is forwarded, never a browser session.
export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "automation/judge/outline", "POST", undefined, undefined, JUDGE_LOST);
}
