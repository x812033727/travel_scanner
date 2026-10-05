import { NextRequest } from "next/server";
import { JUDGE_LOST, forwardToSpeech } from "../../../speech/forward";

// Jev judges whether a final cut's narration keeps to the channel's stance, shows something the
// viewer can do, and sells or advises nothing (docs/videos/HANDS-OFF.md §自動品管, the policy
// item). Only the worker's video tool token is forwarded, never a browser session.
export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "automation/judge/policy", "POST", undefined, undefined, JUDGE_LOST);
}
