import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../speech/forward";

// The video worker reads the owner's backup settings and every uploaded video's Drive folder
// with its video tool token (docs/videos/BACKUP.md). The speech forwarder checks the token's
// shape and keeps cookies out, so a browser session cannot read them through this route.
export async function GET(request: NextRequest) {
  return forwardToSpeech(request, "automation/backup/config", "GET");
}
