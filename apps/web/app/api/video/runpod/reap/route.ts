import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../speech/forward";

// The video worker's five-minute `auto` asks the API to stop RunPod pods that are idle, past
// the longest run, past the monthly cap, or deleted on RunPod. It only ever stops pods.
export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "runpod/reap", "POST");
}
