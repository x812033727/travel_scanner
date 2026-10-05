import { NextRequest } from "next/server";
import { SPEECH_LOST, forwardToSpeech } from "../forward";

export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "speech/judge", "POST", undefined, undefined, SPEECH_LOST);
}
