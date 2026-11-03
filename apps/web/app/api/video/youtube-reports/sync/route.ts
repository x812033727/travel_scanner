import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../speech/forward";

// Fetch the reports YouTube made since the last run. It only reads YouTube and writes the site's
// copy, so a lost answer is safe to send again; the API refuses a run already in progress.
const TIMEOUT_MS = 240_000;

export async function POST(request: NextRequest) {
  return forwardToSpeech(request, "youtube-reports/sync", "POST", 4 * 1024, TIMEOUT_MS);
}
