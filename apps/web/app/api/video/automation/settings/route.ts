import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../speech/forward";

// The video worker reads the owner's automation settings with its video tool token
// (docs/videos/AUTOMATION.md). The speech forwarder already checks the token's shape and keeps
// cookies out, so a browser session cannot read the settings through this route.
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/settings", "GET");
}
