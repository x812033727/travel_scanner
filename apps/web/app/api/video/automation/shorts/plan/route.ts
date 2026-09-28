import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";
import { PLAN_MAX_BODY_BYTES } from "../guard";

// The planner's week: which topic goes to which slot (docs/videos/SHORTS.md). The API checks it
// against the topics, the quotas and the calendar before any slot changes.
export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "automation/shorts/plan", "POST", PLAN_MAX_BODY_BYTES);
}
