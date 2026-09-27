import { NextRequest } from "next/server";
import { TRANSCRIBE_MAX_BODY_BYTES, forwardToSpeech } from "../forward";

export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "speech/transcribe", "POST", TRANSCRIBE_MAX_BODY_BYTES);
}
