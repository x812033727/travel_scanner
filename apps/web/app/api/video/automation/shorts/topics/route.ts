import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";
import { PLAN_MAX_BODY_BYTES } from "../guard";

// New topics the planner wrote so the pool covers two weeks (docs/videos/SHORTS.md).
export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "automation/shorts/topics", "POST", PLAN_MAX_BODY_BYTES);
}
