import { NextRequest } from "next/server";
import { forwardToSpeech } from "../forward";

// What is left of the owner's MiniMax M Plan (apps/api/app/video_speech/admin_api.py minimax_quota).
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "speech/minimax/quota", "GET");
}
