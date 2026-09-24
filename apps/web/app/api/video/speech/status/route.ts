import { NextRequest } from "next/server";
import { forwardToSpeech } from "../forward";

export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "speech/status", "GET");
}
