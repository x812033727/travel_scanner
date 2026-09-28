import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";
import { PLAN_MAX_BODY_BYTES } from "../guard";

// The weekly report the planner wrote from the numbers YouTube reported, as they were stored
// (docs/videos/SHORTS.md).
export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "automation/shorts/report", "POST", PLAN_MAX_BODY_BYTES);
}
