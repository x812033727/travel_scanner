import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";

// This submits a durable receipt, never waits for the model. Repeating its request_key
// returns the same job even if the first HTTP response was lost.
export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "automation/run/jobs", "POST", 4 * 1024 * 1024, 30_000);
}
