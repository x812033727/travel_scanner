import { NextRequest } from "next/server";
import { forwardToSpeech } from "./forward";

export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "speech", "POST");
}
